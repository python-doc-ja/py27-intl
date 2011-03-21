
:mod:`sys` --- システムパラメータと関数
=======================================

.. module:: sys
   :synopsis: システムパラメータと関数へのアクセス


このモジュールでは、インタープリタで使用・管理している変数や、インタープリタの動作に深く関連する関数を定義しています。このモジュールは常に利用可能です。


.. data:: argv

   Pythonスクリプトに渡されたコマンドライン引数のリスト。
   ``argv[0]`` はスクリプトの名前となりますが、フルパス名かどうかは、OSによって異なります。
   コマンドライン引数に :option:`-c` を付けて
   Pythonを起動した場合、 ``argv[0]`` は文字列 ``'-c'`` となります。
   スクリプト名なしでPythonを起動した場合、 ``argv[0]`` は空文字列になります。

   .. To loop over the standard input, or the list of files given on the
      command line, see the :mod:`fileinput` module.

   標準入力もしくはコマンドライン引数で指定されたファイルのリストに対してループするには、
   :mod:`fileinput` モジュールを参照してください。

.. data:: byteorder

   プラットフォームのバイト順を示します。
   ビッグエンディアン (最上位バイトが先頭) のプラットフォームでは ``'big'``,
   リトルエンディアン (最下位バイトが先頭) では ``'little'`` となります。

   .. versionadded:: 2.0


.. data:: subversion

   3つ組 (repo, branch, version) で Python インタプリタの Subversion 情報を表します。 *repo*
   はリポジトリの名前で、 ``'CPython'`` 。 *branch* は ``'trunk'``, ``'branches/name'`` または
   ``'tags/name'`` のいずれかの形式の文字列です。 *version* はもしインタプリタが Subversion のチェックアウトから
   ビルドされたものならば ``svnversion`` の出力であり、リビジョン番号 (範囲) とローカルでの変更がある場合には最後に 'M' が付きます。
   ツリーがエクスポートされたもの (または svnversion が取得できない) で、 branch がタグならば
   ``Include/patchlevel.h`` のリビジョンになります。それ以外の場合には ``None`` です。

   .. versionadded:: 2.5


.. data:: builtin_module_names

   コンパイル時にPythonインタープリタに組み込まれた、全てのモジュール名のタプル(この情報は、他の手段では取得することができません。
   ``modules.keys()`` は、インポートされたモジュールのみのリストを返します。)


.. data:: copyright

   Pythonインタープリタの著作権を表示する文字列。


.. function:: _clear_type_cache()

   .. Clear the internal type cache. The type cache is used to speed up attribute
      and method lookups. Use the function *only* to drop unnecessary references
      during reference leak debugging.

   内部の型キャッシュをクリアします。型キャッシュは属性とメソッドの検索を高速化するために利用されます。
   この関数は、参照リークをデバッグするときに不要な参照を削除するため **だけ** に利用してください。

   .. This function should be used for internal and specialized purposes only.

   この関数は、内部的かつ特殊な目的にのみ利用されるべきです。

   .. versionadded:: 2.6


.. function:: _current_frames()

   各スレッドの識別子を関数が呼ばれた時点のそのスレッドでアクティブになっている一番上のスタックフレームに結びつける辞書を返します。モジュール
   :mod:`traceback` の関数を使えばそのように与えられたフレームのコールスタックを構築できます。

   この関数はデッドロックをデバッグするのに非常に有効です。デッドロック状態のスレッドの協調動作を必要としませんし、そういったスレッドのコー
   ルスタックはデッドロックである限り凍り付いたままです。デッドロックにないスレッドのフレームについては、そのフレームを調べるコードを呼んだ
   時にはそのスレッドの現在の実行状況とは関係ないところを指し示しているかもしれません。

   この関数は外部に見せない特別な目的でのみ使われるべきです。

   .. versionadded:: 2.5


.. data:: dllhandle

   Python DLLのハンドルを示す整数。利用可能: Windows


.. function:: displayhook(value)

   *value* が ``None`` 以外の場合、 ``value`` を ``sys.stdout`` に出力して ``__builtin__._`` に保存します。

   ``sys.displayhook`` は、Pythonの対話セッションで入力された式(:term:`expression`)が評価されたときに呼び出されます。
   対話セッションの出力をカスタマイズする場合、 ``sys.displayhook`` に引数の数が一つの関数を指定します。


.. function:: excepthook(type, value, traceback)

   指定したトレースバックと例外を ``sys.stderr`` に出力します。

   例外が発生し、その例外が捕捉されない場合、インタープリタは例外クラス・例外インスタンス・トレースバックオブジェクトを引数として
   ``sys.excepthook`` を呼び出します。対話セッション中に発生した場合は
   プロンプトに戻る直前に呼び出され、Pythonプログラムの実行中に発生した場合はプログラムの終了直前に呼び出されます。このトップレベルでの例外情報出
   力処理をカスタマイズする場合、 ``sys.excepthook`` に引数の数が三つの関数を指定します。


.. data:: __displayhook__
          __excepthook__

   それぞれ、起動時の ``displayhook`` と ``excepthook`` の値を保存して
   います。この値は、 ``displayhook`` と ``excepthook`` に不正なオブジェクトが指定された場合に、元の値に復旧するために使用します。


.. function:: exc_info()

   この関数は、現在処理中の例外を示す三つの値のタプルを返します。
   この値は、現在のスレッド・現在のスタックフレームのものです。
   現在のスタックフレームが例外処理中でない場合、例外処理中のスタックフレームが見つかるまで次々とその呼び出し元スタックフレームを調べます。
   ここで、"例外処理中" とは "except 節を実行中、または実行した" フレームを指します。
   どのスタックフレームでも、最後に処理した例外の情報のみを参照することができます。

   .. index:: object: traceback

   スタック上で例外が発生していない場合、三つの ``None`` のタプルを返します。例外が発生している場合、
   ``(type, value, traceback)`` を返します。
   *type* は、処理中の例外の型を示します (クラスオブジェクト)。
   *value* は、例外パラメータ (例外に :dfn:`関連する値` または :keyword:`raise` の第二引数。
   *type* がクラスオブジェクトの場合は常にクラスインスタンス) です。
   *traceback* は、トレースバックオブジェクトで、例外が発生した時点でのコールスタック\
   をカプセル化したオブジェクトです(リファレンスマニュアル参照)。

   :func:`exc_clear` が呼び出されると、現在のスレッドで他の例外が発生するか、又は別の例外を処理中のフレームに実行スタックが復帰するまで、
   :func:`exc_info` は三つの ``None`` を返します。

   .. warning::

      例外処理中に戻り値の *traceback* をローカル変数に代入すると循環参照が発生し、関数内のローカル変数やトレースバックが参照している全
      てのオブジェクトは解放されなくなります。特にトレースバック情報が必要ではなければ
      ``exctype, value = sys.exc_info()[:2]`` のように例外型と例外オブジェクトのみを取得するようにして下さい。もしトレースバックが必要
      な場合には、処理終了後にdeleteして下さい。このdeleteは、 :keyword:`try` ... :keyword:`finally`
      ...で行うと良いでしょう。

   .. note::

      Python 2.2 以降では、ガベージコレクションが有効であればこのような到達不能オブジェクトは自動的に削除されます。
      しかし、循環参照を作らないようにしたほうが効率的です。


.. function:: exc_clear()

   この関数は、現在のスレッドで処理中、又は最後に発生した例外の情報を全てクリアします。この関数を呼び出すと、現在のスレッドで他の例外が発生するか、
   又は別の例外を処理中のフレームに実行スタックが復帰するまで、 :func:`exc_info` は三つの ``None`` を返します。

   この関数が必要となることは滅多にありません。ロギングやエラー処理などで最後に発生したエラーの報告を行う場合などに使用します。また、リソースを解放して\
   オブジェクトの終了処理を起動するために使用することもできますが、オブジェクトが実際にされるかどうかは保障の限りではありません。

   .. versionadded:: 2.3


.. data:: exc_type
          exc_value
          exc_traceback

   .. deprecated:: 1.5
      :func:`exc_info` を使用してください

   これらの変数はグローバル変数なのでスレッド毎の情報を示すことができません。
   この為、マルチスレッドなプログラムでは安全に参照することはできません。
   例外処理中でない場合、 ``exc_type`` の値は ``None`` となり、
   ``exc_value`` と ``exc_traceback`` は未定義となります。


.. data:: exec_prefix

   Python のプラットフォーム依存なファイルがインストールされているディレクトリ名(サイト固有)。デフォルトでは、この値は ``'/usr/local'`` です
   が、ビルド時に :program:`configure` の :option:`--exec-prefix` 引数で
   指定することができます。全ての設定ファイル(:file:`pyconfig.h` など)は
   ``exec_prefix + '/lib/pythonversion/config'`` に、共有ライブラリは
   ``exec_prefix + '/lib/pythonversion/lib-dynload'`` にインストールされます
   (但し *version* は ``version[:3]``)。


.. data:: executable

   Python インタープリタの実行ファイルの名前を示す文字列。
   このような名前が意味を持つシステムでは利用可能。


.. function:: exit([arg])

   Python を終了します。 :func:`exit` は :exc:`SystemExit` を送出するので、
   :keyword:`try` ステートメントの :keyword:`finally` 節に終了処理を記\
   述したり、上位レベルで例外を捕捉して exit 処理を中断したりすることができます。
   オプション引数 *arg* には、終了ステータスとして整数(デフォルトは0）
   または整数以外の型のオブジェクトを指定することができます。
   整数を指定した場合、シェル等は 0 は"正常終了"、 0 以外の整数を"異常終了"として扱います。
   多くのシステムでは、有効な終了ステータスは 0-127 で、これ以外の値を返した場合の動作は未定義です。
   システムによっては特定の終了コードに個別の意味を持たせている場合がありますが、このような定義は僅かしかありません。
   Unix プログラムでは文法エラーの場合には 2 を、それ以外のエラーならば 1 を返します。
   *arg* に *None* を指定した場合は、数値の 0 を指定した場合と同じです。
   それ以外のオブジェクトを指定すると、そのオブェクトが ``sys.stderr`` に出力され、終了コードとして 1 を返します。
   エラー発生時には ``sys.exit("エラーメッセージ")`` と書くと、簡単にプログラムを終了することができます。


.. data:: exitfunc

   この値はモジュールに存在しませんが、ユーザプログラムでプログラム終了時に呼び出される終了処理関数として、引数の数が 0 の関数を設定することができます。
   この関数は、インタープリタ終了時に呼び出されます。 ``exitfunc`` に指定することができる終了処理関数は一つだけですので、
   複数のクリーンアップ処理が必要な場合は :mod:`atexit` モジュールを使用してください。

   .. note::

      プログラムがシグナルで kill された場合、
      Python 内部で致命的なエラーが発生した場合、
      ``os._exit()`` が呼び出された場合には、
      終了処理関数は呼び出されません。

   .. deprecated:: 2.4
      :mod:`atexit` を使ってください。


.. data:: flags

   .. The struct sequence *flags* exposes the status of command line flags. The
      attributes are read only.

   属性とシーケンスを利用して、コマンドラインフラグの状態を提供しています。
   属性は読み込み専用になっています。

   +------------------------------+------------------------------------------+
   | 属性                         | フラグ                                   |
   +==============================+==========================================+
   | :const:`debug`               | -d                                       |
   +------------------------------+------------------------------------------+
   | :const:`py3k_warning`        | -3                                       |
   +------------------------------+------------------------------------------+
   | :const:`division_warning`    | -Q                                       |
   +------------------------------+------------------------------------------+
   | :const:`division_new`        | -Qnew                                    |
   +------------------------------+------------------------------------------+
   | :const:`inspect`             | -i                                       |
   +------------------------------+------------------------------------------+
   | :const:`interactive`         | -i                                       |
   +------------------------------+------------------------------------------+
   | :const:`optimize`            | -O or -OO                                |
   +------------------------------+------------------------------------------+
   | :const:`dont_write_bytecode` | -B                                       |
   +------------------------------+------------------------------------------+
   | :const:`no_site`             | -S                                       |
   +------------------------------+------------------------------------------+
   | :const:`ignore_environment`  | -E                                       |
   +------------------------------+------------------------------------------+
   | :const:`tabcheck`            | -t or -tt                                |
   +------------------------------+------------------------------------------+
   | :const:`verbose`             | -v                                       |
   +------------------------------+------------------------------------------+
   | :const:`unicode`             | -U                                       |
   +------------------------------+------------------------------------------+

   .. versionadded:: 2.6


.. data:: float_info

   .. A structseq holding information about the float type. It contains low level
      information about the precision and internal representation. Please study
      your system's :file:`float.h` for more information.

   属性とシーケンスを利用して、 float 型に関する情報を提供します。
   精度と内部表現に関する情報を含みます。
   詳細については、システムの :file:`float.h` を調べてください。

   +---------------------+------------------------------------------------------------+
   | 属性                |  説明                                                      |
   +=====================+============================================================+
   | :const:`epsilon`    | 1と、その次の表現可能なfloat値の差                         |
   +---------------------+------------------------------------------------------------+
   | :const:`dig`        | digits (:file:`float.h` を参照)                            |
   +---------------------+------------------------------------------------------------+
   | :const:`mant_dig`   | mantissa digits (:file:`float.h` を参照)                   |
   +---------------------+------------------------------------------------------------+
   | :const:`max`        | floatが表せる最大の(infiniteではない)値                    |
   +---------------------+------------------------------------------------------------+
   | :const:`max_exp`    | floatが radix**(e-1) を表現可能な、最大の整数 e            |
   +---------------------+------------------------------------------------------------+
   | :const:`max_10_exp` | floatが 10**e を表現可能な、最大の整数 e                   |
   +---------------------+------------------------------------------------------------+
   | :const:`min`        | floatが表現可能な最小の正の値                              |
   +---------------------+------------------------------------------------------------+
   | :const:`min_exp`    | radix**(e-1) が正規化floatであるような最小の整数 e         |
   +---------------------+------------------------------------------------------------+
   | :const:`min_10_exp` | 10**e が正規化floatであるような最小の整数 e                |
   +---------------------+------------------------------------------------------------+
   | :const:`radix`      | radix of exponent                                          |
   +---------------------+------------------------------------------------------------+
   | :const:`rounds`     | addition rounds (file:`float.h` を参照)                    |
   +---------------------+------------------------------------------------------------+

   .. note::

      .. The information in the table is simplified.

      このテーブルの情報は簡易的なものです。

   .. versionadded:: 2.6


.. function:: getcheckinterval()

   インタプリタの "チェックインターバル (check interval)" を返します; :func:`setcheckinterval`
   を参照してください。

   .. versionadded:: 2.3


.. function:: getdefaultencoding()

   現在の Unicode 処理のデフォルトエンコーディング名を返します。

   .. versionadded:: 2.0


.. function:: getdlopenflags()

   :cfunc:`dlopen` で指定されるフラグを返します。
   このフラグは :mod:`dl` と :mod:`DLFCN` で定義されています。

   利用可能: Unix.

   .. versionadded:: 2.2


.. function:: getfilesystemencoding()

   Unicode ファイル名をシステムのファイル名に変換する際に使用するエンコード名を返します。
   システムのデフォルトエンコーディングを使用する場合には ``None`` を返します。

   * Windows 9x では、エンコーディングは "mbcs" となります。

   * OS X では、エンコーディングは "utf-8" となります。

   * Unix では、エンコーディングは ``nl_langinfo(CODESET)`` が返すユーザの設定となります。
     ``nl_langinfo(CODESET)`` が失敗すると :const:`None` を返します。

   * Windows NT+ では、 Unicode をファイル名として使用できるので変換の必要はありません。
     :func:`getfilesystemencoding` は ``'mbcs'`` を返しますが、これはある Unicode
     文字列をバイト文字列に明示的に変換して、ファイル名として使うと同じファイルを指すようにしたい場合に、アプリケーションが使わねばならないエンコーディングです。

   .. versionadded:: 2.3


.. function:: getrefcount(object)

   *object* の参照数を返します。
   *object* は(一時的に) :func:`getrefcount` からも参照されるため、参照数は予想される数よりも 1 多くなります。


.. function:: getrecursionlimit()

   現在の最大再帰数を返します。
   最大再帰数は、Python インタープリタスタックの最大の深さです。
   この制限は Python プログラムが無限に再帰し、C スタックがオーバーフローしてクラッシュすることを防止するために設けられています。
   この値は :func:`setrecursionlimit` で指定することができます。


.. function:: getsizeof(object[, default])

   .. Return the size of an object in bytes. The object can be any type of
      object. All built-in objects will return correct results, but this
      does not have to hold true for third-party extensions as it is implementation
      specific.

   *object* のサイズをバイト数で返します。
   *object* は任意の型のオブジェクトです。
   全てのビルトイン型は正しい値を返します。
   サードパーティー製の型については実装依存になります。

   .. The *default* argument allows to define a value which will be returned
      if the object type does not provide means to retrieve the size and would
      cause a `TypeError`.

   *default* 引数は、オブジェクトの型がサイズの情報を提供していない場合に、
   `TypeError` 例外を発生させる代わりに返す値です。

   .. func:`getsizeof` calls the object's __sizeof__ method and adds an additional
      garbage collector overhead if the object is managed by the garbage collector.

   :func:`getsizeof` は *object* の ``__sizeof__`` メソッドを呼び出し、
   そのオブジェクトがガベージコレクタに管理されていた場合はガベージコレクタの\
   オーバーヘッドを増やします。

   .. versionadded:: 2.6


.. function:: _getframe([depth])

   コールスタックからフレームオブジェクトを取得します。
   オプション引数 *depth* を指定すると、スタックのトップから *depth* だけ下のフレー\
   ムオブジェクトを取得します。
   *depth* がコールスタックよりも深ければ、 :exc:`ValueError` が発生します。
   *depth* のデフォルト値は 0 で、この場合はコールスタックのトップのフレームを返します。

   この関数は、内部的な、特殊な用途にのみ利用することができます。


.. function:: getprofile()

   .. index::
      single: profile function
      single: profiler

   .. Get the profiler function as set by :func:`setprofile`.

   :func:`setprofile` 関数などで設定した profiler 関数を取得します。

   .. versionadded:: 2.6


.. function:: gettrace()

   .. index::
      single: trace function
      single: debugger

   .. Get the trace function as set by :func:`settrace`.

   :func:`settrace` 関数などで設定した trace 関数を取得します。

   .. note::

      .. The :func:`gettrace` function is intended only for implementing debuggers,
         profilers, coverage tools and the like. Its behavior is part of the
         implementation platform, rather than part of the language definition,
         and thus may not be available in all Python implementations.

      :func:`gettrace` 関数は、デバッガ、プロファイラ、カバレッジツールなどの実装に使うことのみを想定しています。
      この関数の振る舞いは言語定義ではなく実装プラットフォームの一部です。
      そのため、他の Python 実装では利用できないかもしれません。

   .. versionadded:: 2.6


.. function:: getwindowsversion()

   実行中の Windows のバージョンを示す、以下の値のタプルを返します：
   *major*, *minor*, *build*, *platform*, *text* 。
   *text* は文字列、それ以外の値は整数です。

   *platform* は、以下の値となります:

   +-----------------------------------------+-------------------------+
   | Constant                                | Platform                |
   +=========================================+=========================+
   | :const:`0 (VER_PLATFORM_WIN32s)`        | Win32s on Windows 3.1   |
   +-----------------------------------------+-------------------------+
   | :const:`1 (VER_PLATFORM_WIN32_WINDOWS)` | Windows 95/98/ME        |
   +-----------------------------------------+-------------------------+
   | :const:`2 (VER_PLATFORM_WIN32_NT)`      | Windows NT/2000/XP/x64  |
   +-----------------------------------------+-------------------------+
   | :const:`3 (VER_PLATFORM_WIN32_CE)`      | Windows CE              |
   +-----------------------------------------+-------------------------+

   この関数は、Win32 :func:`GetVersionEx` 関数を呼び出します。詳細はマイクロソフトのドキュメントを参照してください。

   利用可能: Windows.

   .. versionadded:: 2.3


.. data:: hexversion

   整数にエンコードされたバージョン番号。
   この値は新バージョン(正規リリース以外であっても)ごとにかならず増加します。
   例えば、Python 1.5.2 以降でのみ動作するプログラムでは、以下のようなチェックを行います。 ::

      if sys.hexversion >= 0x010502F0:
          # use some advanced feature
          ...
      else:
          # use an alternative implementation or warn the user
          ...

   ``hexversion`` は :func:`hex` で16進数に変換しなければ値の意味がわかりません。
   より読みやすいバージョン番号が必要な場合には
   ``version_info`` を使用してください。

   .. versionadded:: 1.5.2


.. data:: last_type
          last_value
          last_traceback

   通常は定義されておらず、捕捉されない例外が発生してインタープリタがエラーメッセージとトレースバックを出力した場合にのみ設定されます。
   この値は、対話セッション中にエラーが発生したとき、デバッグモジュールをロード (例:``import pdb; pdb.pm()`` など。
   詳細は :ref:`debugger` を参照)して発生したエラーを調査する場合に利用します。
   デバッガをロードすると、プログラムを再実行せずに情報を取得することができます。

   変数の意味は、上の :func:`exc_info` の戻り値と同じです。
   対話セッションを実行するスレッドは常に1つだけなので、 ``exc_type`` のようにスレッドに関する問題は発生しません。


.. data:: maxint

   Pythonの整数型でサポートされる、最大の整数。この値は最低でも 2\*\*31-1 です。
   最大の負数は ``-maxint-1`` となります。正負の最大数が非対称ですが、これは 2 の補数計算を行うためです。

.. data:: maxsize

   .. The largest positive integer supported by the platform's Py_ssize_t type,
      and thus the maximum size lists, strings, dicts, and many other containers
      can have.

   プラットフォームの Py_ssize_t 型がサポートしている最大の正の整数。
   したがって、リスト、文字列、辞書、その他コンテナ型の最大のサイズ。

.. data:: maxunicode

   Unicode 文字の最大のコードポイントを示す整数。この値は、オプション設定で
   Unicode 文字の保存形式として USC-2 と UCS-4 のいずれを指定したかによって異なります。


.. data:: meta_path

    .. A list of :term:`finder` objects that have their :meth:`find_module`
       methods called to see if one of the objects can find the module to be
       imported. The :meth:`find_module` method is called at least with the
       absolute name of the module being imported. If the module to be imported is
       contained in package then the parent package's :attr:`__path__` attribute
       is passed in as a second argument. The method returns :keyword:`None` if
       the module cannot be found, else returns a :term:`loader`.

    :term:`finder` オブジェクトのリストです。
    :term:`finder` オブジェクトの :meth:`find_module` メソッドは、
    import するモジュールを探すために呼び出されます。
    import するモジュールがパッケージに含まれる場合、
    親パッケージの :attr:`__path__` 属性が第 2 引数として渡されます。
    そのメソッドは、モジュールが見つからなかった場合は :const:`None` を、
    見つかった場合は :term:`loader` を返します。

    .. :data:`sys.meta_path` is searched before any implicit default finders or
       :data:`sys.path`.

    :data:`sys.meta_path` は、デフォルトの暗黙の finder や、
    :data:`sys.path` よりも先に検索されます。

    .. See :pep:`302` for the original specification.

    オリジナルの仕様については、 :pep:`302` を参照してください。


.. data:: modules

   .. index:: builtin: reload

   ロード済みモジュールのモジュール名とモジュールオブジェクトの辞書。
   強制的にモジュールを再読み込みする場合などに使用します。
   この辞書からモジュールを削除するのは、 :func:`reload` の呼び出しと等価では *ありません* 。


.. data:: path

   .. index:: triple: module; search; path

   モジュールを検索するパスを示す文字列のリスト。
   :envvar:`PYTHONPATH` 環境変数と、インストール時に指定したデフォルトパスで初期化されます。

   開始時に初期化された後、リストの先頭(``path[0]``)には Python インタープリタを起動するために指定したスクリプトのディレクトリが挿入されます。
   スクリプトのディレクトリがない(インタープリタで対話セッションで起動された時や、スクリプトを標準入力から読み込む場合など)場合、
   ``path[0]`` には空文字列となり、Python はカレントディレクトリからモジュールの検索を開始します。
   スクリプトディレクトリは、
   :envvar:`PYTHONPATH` で指定したディレクトリの *前* に挿入されますので注意が必要です。

   必要に応じて、プログラム内で自由に変更することができます。

   .. versionchanged:: 2.3
      Unicode 文字列が無視されなくなりました.

   .. seealso::
      :mod:`site` モジュールのドキュメントで、 .pth ファイルを使って :data:`sys.path` を拡張する方法を解説しています。


.. data:: path_hooks

    .. A list of callables that take a path argument to try to create a
       :term:`finder` for the path. If a finder can be created, it is to be
       returned by the callable, else raise :exc:`ImportError`.

    path を引数にとって、その path に対する :term:`finder` の作成を試みる呼び出し可能オブジェクトのリスト。
    finder の作成に成功したら、その呼出可能オブジェクトのは finder を返します。
    失敗した場合は、 :exc:`ImportError` を発生させます。

    .. Originally specified in :pep:`302`.

    オリジナルの仕様は :pep:`302` を参照してください。


.. data:: path_importer_cache

   .. A dictionary acting as a cache for :term:`finder` objects. The keys are
      paths that have been passed to :data:`sys.path_hooks` and the values are
      the finders that are found. If a path is a valid file system path but no
      explicit finder is found on :data:`sys.path_hooks` then :keyword:`None` is
      stored to represent the implicit default finder should be used. If the path
      is not an existing path then :class:`imp.NullImporter` is set.

   :term:`finder` オブジェクトのキャッシュとなる辞書。
   キーは :data:`sys.path_hooks` に渡される path で、値は見つかった finder オブジェクト。
   path が有効なファイルシステムパスであり、かつ finder が :data:`sys.path_hooks` から見つからない場合、
   暗黙のデフォルト finder を利用するという意味で :const:`None` が格納されます。
   path が既存のパスではない場合、 :class:`imp.NullImporter` が格納されます。

   .. Originally specified in :pep:`302`.

   オリジナルの仕様は :pep:`302` を参照してください。


.. data:: platform

   プラットフォームを識別する文字列で、 ``path``
   にプラットフォーム別のサブディレクトリを追加する場合などに利用します。

   .. For Unix systems, this is the lowercased OS name as returned by ``uname -s``
      with the first part of the version as returned by ``uname -r`` appended,
      e.g. ``'sunos5'`` or ``'linux2'``, *at the time when Python was built*.
      For other systems, the values are:

   Unix システムでは、この値は ``uname -s`` が返す小文字のOS名を前半に、
   ``uname -r`` が返すバージョン名を後半に追加したものになります。
   例えば、 ``'sunos5'`` や ``'linux2'`` といった具合です。
   *この値はPythonをビルドした時のものです* 。
   それ以外のシステムでは、次のような値になります。 :

   ================ ===========================
   システム           :data:`platform` の値
   ================ ===========================
   Windows          ``'win32'``
   Windows/Cygwin   ``'cygwin'``
   Mac OS X         ``'darwin'``
   OS/2             ``'os2'``
   OS/2 EMX         ``'os2emx'``
   RiscOS           ``'riscos'``
   AtheOS           ``'atheos'``
   ================ ===========================

.. data:: prefix

   サイト固有の、プラットフォームに依存しないファイルを格納するディレクトリを示す文字列。
   デフォルトでは ``'/usr/local'`` になります。
   この値はビルド時に :program:`configure` スクリプトの :option:`--prefix` 引数で指定する事ができます。
   Python　ライブラリの主要部分は ``prefix + '/lib/pythonversion'`` にインストールされ、プラットフォーム非依存なヘッダファイル(:file:`pyconfig.h` 以外)は
   ``prefix + '/include/pythonversion'`` に格納されます (但し *version* は ``version[:3]``)。


.. data:: ps1
          ps2

   .. index::
      single: interpreter prompts
      single: prompts, interpreter

   インタープリタの一次プロンプト、二次プロンプトを指定する文字列。対話モードで実行中のみ定義され、初期値は ``'>>> '`` と
   ``'... '`` です。文字列以外のオブジェクトを指定した場合、インタープリタが対話コマンドを読み込むごとにオブジェクトの :func:`str` を評価します。
   この機能は、動的に変化するプロンプトを実装する場合に利用します。


.. data:: py3kwarning

   .. Bool containing the status of the Python 3.0 warning flag. It's ``True``
      when Python is started with the -3 option.  (This should be considered
      read-only; setting it to a different value doesn't have an effect on
      Python 3.0 warnings.)

   Python 3.0 warning flag の状態を格納する Bool 値。
   Python が -3 オプションを付けて起動された場合は ``True`` になります。
   (この値は定数として扱ってください。この変数を変更しても、Python 3.0 warning
   の動作には影響しません)

   .. versionadded:: 2.6


.. data:: dont_write_bytecode

   .. If this is true, Python won't try to write ``.pyc`` or ``.pyo`` files on the
      import of source modules.  This value is initially set to ``True`` or ``False``
      depending on the ``-B`` command line option and the ``PYTHONDONTWRITEBYTECODE``
      environment variable, but you can set it yourself to control bytecode file
      generation.

   この値が true の時、 Python はソースモジュールを import するときに ``.pyc`` や ``.pyo``
   ファイルを生成しません。
   この値は ``-B`` コマンドラインオプションと ``PYTHONDONTWRITEBYTECODE`` 環境変数の
   値によって起動時に ``True`` か ``False`` に設定されます。
   しかし、実行時にこの変数を変更して、バイトコード生成を制御することもできます。

   .. versionadded:: 2.6


.. function:: setcheckinterval(interval)

   インタープリタの"チェック間隔"を示す整数値を指定します。
   この値はスレッドスイッチやシグナルハンドラのチェックを行う周期を決定します。
   デフォルト値は ``100`` で、この場合 100 の仮想命令を実行するとチェックを行います。
   この値を大きくすればスレッドを利用するプログラムのパフォーマンスが向上します。
   この値が 0 以下の場合、全ての仮想命令を実行するたびにチェックを行い、レスポンス速度と最大になりますがオーバヘッドもまた最大となります。

   .. Note that :mod:`site` is not imported if the :option:`-S` option is passed
      to the interpreter, in which case this function will remain available.

.. function:: setdefaultencoding(name)

   現在の Unicode 処理のデフォルトエンコーディング名を設定します。
   *name* に一致するエンコーディングが見つからない場合、
   :exc:`LookupError` が発生します。
   この関数は、 :mod:`site` モジュールの実装が、 :mod:`sitecustomize` モジュールから使用するためだけに定義されています。
   :mod:`site` から呼び出された後、この関数は :mod:`sys` から削除されます。

   .. versionadded:: 2.0


.. function:: setdlopenflags(n)

   インタープリタが拡張モジュールをロードする時、 :cfunc:`dlopen` で使用するフラグを設定します。
   ``sys.setdlopenflags(0)`` とすれば、モジュールインポート時にシンボルの遅延解決を行う事ができます。
   シンボルを拡張モジュール間で共有する場合には、
   ``sys.setdlopenflags(dl.RTLD_NOW | dl.RTLD_GLOBAL)`` と指定します。
   フラグの定義名は :mod:`dl` か :mod:`DLFCN` で定義されています。
   :mod:`DLFCN` が存在しない場合、 :program:`h2py` スクリプトを使って
   :file:`/usr/include/dlfcn.h` から生成することができます。

   利用可能: Unix.

   .. versionadded:: 2.2


.. function:: setprofile(profilefunc)

   .. index:: single: profiler

   システムのプロファイル関数を登録します。
   プロファイル関数は、 Python のソースコードプロファイルを行う関数で、
   Python で記述することができます。
   詳細は :ref:`profile` を参照してください。
   プロファイル関数はトレース関数(:func:`settrace` 参照)と似ていますが、ソース行が実行されるごとに呼び出されるのではなく、関数の呼出しと復帰時のみ呼び出されます(例外が発生している場合でも、復帰時のイベントは発生します)。
   プロファイル関数はスレッド毎に設定することができますが、プロファイラはスレッド間のコンテキスト切り替えを検出することはできません。
   従って、マルチスレッド環境でのプロファイルはあまり意味がありません。
   :func:`setprofile` は常に ``None`` を返します。


.. function:: setrecursionlimit(limit)

   Python インタープリタの、スタックの最大の深さを *limit* に設定します。
   この制限は Python プログラムが無限に再帰し、
   C スタックがオーバーフローしてクラッシュすることを防止するために設けられています。

   *limit* の最大値はプラットフォームによって異なります。
   深い再帰処理が必要な場合にはプラットフォームがサポートしている範囲内でより大きな値\
   を指定することができますが、この値が大きすぎればクラッシュするので注意が必要です。


.. function:: settrace(tracefunc)

   .. index:: single: debugger

   システムのトレース関数を登録します。
   トレース関数は Python のソースデバッガを実装するために使用することができます。
   トレース関数はスレッド毎に設定することができるので、デバッグを行う全てのスレッドで
   :func:`settrace` を呼び出し、トレース関数を登録してください。

   .. Trace functions should have three arguments: *frame*, *event*, and
      *arg*. *frame* is the current stack frame.  *event* is a string: ``'call'``,
      ``'line'``, ``'return'``, ``'exception'``, ``'c_call'``, ``'c_return'``, or
      ``'c_exception'``. *arg* depends on the event type.

   Trace関数は3つの引数: *frame*, *event*, *arg* を受け取る必要があります。
   *event* は文字列です。 ``'call'``, ``'line'``, ``'return'``, ``'exception'``, ``'c_call'``,
   ``'c_return'``, ``'c_exception'`` のどれかが渡されます。
   *arg* はイベントの種類によって異なります。

   .. The trace function is invoked (with *event* set to ``'call'``) whenever a new
      local scope is entered; it should return a reference to a local trace
      function to be used that scope, or ``None`` if the scope shouldn't be traced.

   trace 関数は (*event* に ``'call'`` を渡された状態で) 新しいローカルスコープに入るたびに呼ばれます。
   この場合、そのスコープで利用するローカルの trace 関数か、そのスコープを trace しないのであれば
   ``None`` を返します。

   .. The local trace function should return a reference to itself (or to another
      function for further tracing in that scope), or ``None`` to turn off tracing
      in that scope.

   ローカル trace 関数は自身への参照 (もしくはそのスコープの以降の trace を行う別の関数)
   を返すべきです。
   もしくは、そのスコープの trace を止めるために ``None`` を返します。

   .. The events have the following meaning:

   *event* には以下の意味があります。

   ``'call'``
      .. A function is called (or some other code block entered).  The
         global trace function is called; *arg* is ``None``; the return value
         specifies the local trace function.

      関数が呼び出された(もしくは、何かのコードブロックに入った)。
      グローバルの trace 関数が呼ばれる。
      *arg* は ``None`` が渡される。
      戻り値はローカルの trace 関数。

   ``'line'``
      .. The interpreter is about to execute a new line of code (sometimes multiple
         line events on one line exist).  The local trace function is called; *arg*
         is ``None``; the return value specifies the new local trace function.

      インタプリタが新しい行を実行しようとしている。
      (1つの行に対して複数回の line イベントが発生する場合があります)
      戻り値は新しいローカルの trace 関数。

   ``'return'``
      .. A function (or other code block) is about to return.  The local trace
         function is called; *arg* is the value that will be returned.  The trace
         function's return value is ignored.

      関数(あるいは別のコードブロック)から戻ろうとしている。
      ローカルの trace 関数が呼ばれる。
      *arg* は返り値。
      trace 関数の戻り値は無視される。

   ``'exception'``
      .. An exception has occurred.  The local trace function is called; *arg* is a
         tuple ``(exception, value, traceback)``; the return value specifies the
         new local trace function.

      例外が発生した。
      ローカルの trace 関数が呼ばれる。
      *arg* は ``(exception, value, traceback)`` のタプル。
      戻り値は新しいローカルの trace 関数。

   ``'c_call'``
      .. A C function is about to be called.  This may be an extension function or
         a builtin.  *arg* is the C function object.

      C 関数(拡張関数かビルトイン関数)が呼ばれようとしている。
      *arg* は C 関数オブジェクト。

   ``'c_return'``
      .. A C function has returned. *arg* is ``None``.

      C 関数から戻った。 *arg* は ``None``

   ``'c_exception'``
      .. A C function has thrown an exception.  *arg* is ``None``.

      C 関数が例外を発生させた。 *arg* は ``None``

   .. Note that as an exception is propagated down the chain of callers, an
      ``'exception'`` event is generated at each level.

   例外が呼び出しチェインを辿って伝播していくことに注意してください。
   ``'exception'`` イベントは各レベルで発生します。

   .. For more information on code and frame objects, refer to :ref:`types`.

   code と frame オブジェクトについては、 :ref:`types` を参照してください。

   .. note::

      :func:`settrace` 関数は、デバッガ、プロファイラ、カバレッジツール等で使うためだけのものです。
      この関数の挙動は言語定義よりも実装プラットフォームの分野の問題で、全ての Python 実装で利用できるとは限りません。


.. function:: settscdump(on_flag)

   *on_flag* が真の場合、Pentium タイムスタンプカウンタを使った VM 計測結果のダンプ出力を有効にします。
   *on_flag* をオフにするとダンプ出力を無効化します。
   この関数は Python を :option:`--with-tsc` つきでコンパイルしたときにのみ利用できます。
   ダンプの内容を理解したければ、 Python ソースコード中の :file:`Python/ceval.c` を読んでください。

   .. versionadded:: 2.4


.. data:: stdin
          stdout
          stderr

   .. index::
      builtin: input
      builtin: raw_input

   インタープリタの標準入力・標準出力・標準エラー出力に対応するファイルオブジェクト。
   ``stdin`` はスクリプトの読み込みを除く全ての入力処理で使用され、
   :func:`input` や :func:`raw_input` も ``stdin`` から読み込みます。
   ``stdout`` は、 :keyword:`print` や式(:term:`expression`)の評価結果、
   :func:`input`, :func:`raw_input` のプロンプトの出力先となります。
   インタープリタのプロンプトは(ほとんど) ``stderr`` に出力されます。
   ``stdout`` と ``stderr`` は必ずしも組み込みのファイルオブジェクトである必要はなく、
   :meth:`write` メソッドを持つオブジェクトであれば使用することができます。
   ``stdout`` と ``stderr`` を別のオブジェクトに置き換えても、 :func:`os.popen`, :func:`os.system`,
   :mod:`os` の :func:`exec\*` などから起動されたプロセスが使用する標準 I/O ストリームは変更されません。


.. data:: __stdin__
          __stdout__
          __stderr__

   それぞれ起動時の ``stdin``, ``stderr``, ``stdout`` の値を保存します。
   終了処理時に利用されます。
   また、 ``sys.std*`` オブジェクトが(訳注:別のファイルライクオブジェクトに)リダイレクトされている場合でも、
   本当の標準ストリームに表示する場合に利用できます。

   .. It can also be used to restore the actual files to known working file objects
      in case they have been overwritten with a broken object.  However, the
      preferred way to do this is to explicitly save the previous stream before
      replacing it, and restore the saved object.

   また、標準ストリームを置き換えたオブジェクトが壊れた場合に、動作する本物のファイルをリストアするために
   利用することもできます。
   しかし、明示的に置き換え前のストリームを保存しておき、そのオブジェクトをリストアする事を推奨します。


.. data:: tracebacklimit

   捕捉されない例外が発生した時、出力されるトレースバック情報の最大レベル数を指定する整数値(デフォルト値は ``1000``)。 ``0`` 以下の値が設定
   された場合、トレースバック情報は出力されず例外型と例外値のみが出力されます。


.. data:: version

   Pythonインタープリタのバージョンとビルド番号・使用コンパイラなどの情報を示す文字列で、
   ``'バージョン(#ビルド番号, ビルド日付, ビルド時間)[コンパイラ]'`` となります。先頭の三文字は、バージョンごとのインストール先ディレクトリ内を識別するために使用されます。例::

      >>> import sys
      >>> sys.version
      '1.5.2 (#0 Apr 13 1999, 10:51:12) [MSC 32 bit (Intel)]'


.. data:: api_version

   使用中のインタープリタの C API バージョン。
   Python と拡張モジュール間の不整合をデバッグする場合などに利用できます。

   .. versionadded:: 2.3


.. data:: version_info

   バージョン番号を示す５つの値のタプル:*major*, *minor*, *micro*, *releaselevel*, *serial* 。
   *releaselevel* 以外は全て整数です。 *releaselevel* の値は、 ``'alpha'``, ``'beta'``,
   ``'candidate'``, ``'final'`` の何れかです。
   Python 2.0 の ``version_info`` は、 ``(2, 0, 0, 'final', 0)`` となります。

   .. versionadded:: 2.0


.. data:: warnoptions

   この値は、warnings framework 内部のみ使用され、変更することはできません。
   詳細は :mod:`warnings` を参照してください。


.. data:: winver

   Windows プラットフォームで、レジストリのキーとなるバージョン番号。
   Python DLL の文字列リソース 1000 に設定されています。
   通常、この値は :const:`version` の先頭三文字となります。
   この値は参照専用で、別の値を設定しても Python が使用するレジストリキーを変更することはできません。
   利用可能: Windows.
