
:mod:`thread` --- マルチスレッドのコントロール
================================

.. module:: thread
   :synopsis: 1つのインタープリタの中でのマルチスレッド制御


.. index::
   single: light-weight processes
   single: processes, light-weight
   single: binary semaphores
   single: semaphores, binary

このモジュールはマルチスレッド(別名 :dfn:`軽量プロセス` (:dfn:`light-weight processes`)または:dfn:`タスク`\
(:dfn:`tasks`)) に用いられる低レベルプリミティブを提供します --- グローバルデータ空間を共有するマルチスレッドを制御します。
同期のための単純なロック(別名 :dfn:`mutexes`または バイナリセマフォ(:dfn:`binary semaphores`))が提供されています。

このモジュールはオプションです。 Windows, Linux, SGI IRIX, Solaris 2.x、そして同じようなPOSIXスレッド
(別名"pthread")実装のシステム上でサポートされます。 :mod:`thread`を使用することのできないシステムでは、
:mod:`dummy_thread`が用意されています。 :mod:`dummy_thread`はこのモジュールと同じインターフェース
を持ち、置き換えて使用することができます。

.. index::
   single: pthreads
   pair: threads; POSIX

定数と関数は以下のように定義されています:


.. exception:: error

   スレッド特有のエラーで送出されます。


.. data:: LockType

   これはロックオブジェクトのタイプです。


.. function:: start_new_thread(function, args[, kwargs])

   新しいスレッドを開始して、そのIDを返します。 スレッドは引数リスト*args*(タプルでなければなりません)の 関数*function*を実行します。
   オプション引数*kwargs*はキーワード引数の辞書を指定します。 関数が戻るとき、スレッドは黙って終了します。
   関数が未定義の例外でターミネートしたとき、スタックトレースが表示され、 そしてスレッドが終了します(しかし他のスレッドは走り続けます)。


.. function:: interrupt_main()

   メインスレッドで :exc:`KeyboardInterrupt` を送出します。サブスレッドは
   この関数を使ってメインスレッドに割り込みをかけることができます。

   .. versionadded:: 2.3


.. function:: exit()

   :exc:`SystemExit`例外を送出します。 それが捕えられないときは、黙ってスレッドを終了させます。

.. % \begin{funcdesc}{exit_prog}{status}
.. % Exit all threads and report the value of the integer argument
.. % \var{status} as the exit status of the entire program.
.. % \strong{Caveat:} code in pending \keyword{finally} clauses, in this thread
.. % or in other threads, is not executed.
.. % \end{funcdesc}
.. % \begin{funcdesc}{exit_prog}{status}
.. % 全てのスレッドを終了し、全体のプログラムの終了ステータスとして
.. % 全ての整数の引数\var{status}の値を報告します。
.. % 未解決の\keyword{finally}項内の\strong{Caveat:}コードは、
.. % このスレッドや他のスレッドも含め、実行されません。
.. % \end{funcdesc}


.. function:: allocate_lock()

   新しいロックオブジェクトを返します。 ロックのメソッドはこの後に記述されます。 ロックは初期状態としてアンロック状態です。


.. function:: get_ident()

   現在のスレッドの'スレッドID'を返します。 これは0でない整数です。 この値は直接の意味を持っていません;
   例えばスレッド特有のデータの辞書に索引をつけるためのような、 マジッククッキーとして意図されています。 スレッドが終了し、他のスレッドが作られたとき、
   スレッドIDは再利用されるかもしれません。


.. function:: stack_size([size])

   新しいスレッドが作られる際に使われるスレッドのスタックサイズを返します。 オプションの *size* 引数は次に作られるスレッドに対する
   スタックサイズを指定するものですが、0 (プラットフォームまたは設定されたデフォルト) または少なくとも 32,768 (32kB)
   であるような正の整数でなければなりません。 もしスタックサイズの変更がサポートされていなければ :exc:`ThreadError`
   が送出されます。また指定されたスタックサイズが条件を満たしていなければ :exc:`ValueError`
   が送出されスタックサイズは変更されないままになります。 32kB は今のところインタプリタ自体に十分なスタックスペースを保証するための値として
   サポートされる最小のスタックサイズです。プラットフォームによってはスタックサイズの 値に固有の制限が課されることもあります。たとえば 32kB
   より大きな最小スタックサイズを 要求されたり、システムメモリサイズの倍数の割り当てを要求されるなどです - より
   詳しい情報はプラットフォームごとの文書で確認してください(4kB ページは一般的ですので、 情報が見当たらないときには 4096
   の倍数を指定しておくといいかもしれません)。 利用可能: Windows, POSIX スレッドのあるシステム。

   .. versionadded:: 2.5

ロックオブジェクトは次のようなメソッドを持っています:


.. method:: lock.acquire([waitflag])

   オプションの引数なしで使用すると、このメソッドは他のスレッドがロックし ているかどうかにかかわらずロックを獲得します。
   ただし他のスレッドがすでにロックしている場合には解除されるまで 待ってからロックを獲得します (同時にロックを獲得できるスレッドは
   ひとつだけであり、これこそがロックの存在理由です)。 整数の引数 *waitflag* を指定すると、その値によって動作が変わります。 引数が ``0``
   のときは、待たずにすぐ獲得できる場合にだけロックを獲得 します。``0`` 以外の値を与えると、先の例と同様、ロックの状態に
   かかわらず獲得をおこないます。なお、ロックを獲得すると ``True``、できなかったときには ``False`` を返します。


.. method:: lock.release()

   ロックを解放します。そのロックは既に獲得されたものでなければなりませんが、 しかし同じスレッドによって獲得されたものである必要はありません。


.. method:: lock.locked()

   ロックの状態を返します: 同じスレッドによって獲得されたものなら``True``、 違うのなら``False``を返します。

これらのメソッドに加えて、ロックオブジェクトは :keyword:`with` 文を通じて 以下の例のように使うこともできます。 ::

   from __future__ import with_statement
   import thread

   a_lock = thread.allocate_lock()

   with a_lock:
       print "a_lock is locked while this executes"

**Caveats:**

  .. index:: module: signal

* スレッドは割り込みと奇妙な相互作用をします: :exc:`KeyboardInterrupt`例外は任意のスレッドによって受け取られます。
  (:mod:`signal`モジュールが利用可能なとき、 割り込みは常にメインスレッドへ行きます。)

* :func:`sys.exit`を呼び出す、 あるいは:exc:`SystemExit`例外を送出することは、
  :func:`exit`を呼び出すことと同じです。

* I/O待ちをブロックするかもしれない全ての組込み関数が、 他のスレッドの走行を許すわけではありません。 (ほとんどの一般的なもの
  (:func:`time.sleep`, :meth:`file.read`, :func:`select.select`)は期待通りに働きます。)

* ロックの:meth:`acquire`メソッドに割り込むことはできません ---
  :exc:`KeyboardInterrupt`例外は、ロックが獲得された後に発生します。

  .. index:: pair: threads; IRIX

* メインスレッドが終了したとき、他のスレッドが生き残るかどうかは、 システムが定義します。 ネイティブスレッド実装を使うSGI IRIXでは生き残ります。
  その他の多くのシステムでは、:keyword:`try` ... :keyword:`finally`節
  を実行せずに殺されたり、デストラクタを実行せずに殺されたりします。

* メインスレッドが終了したとき、それの通常のクリーンアップは行なわれず (:keyword:`try` ...
  :keyword:`finally`節が尊重されることは除きます)、 標準I/Oファイルはフラッシュされません。

