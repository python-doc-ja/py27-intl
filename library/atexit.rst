
:mod:`atexit` --- 終了ハンドラ
==============================

.. module:: atexit
   :synopsis: 後始末関数の登録と実行。
.. moduleauthor:: Skip Montanaro <skip@mojam.com>
.. sectionauthor:: Skip Montanaro <skip@mojam.com>


.. versionadded:: 2.0

:mod:`atexit` モジュールでは、後始末関数を登録するための関数を一つだ け定義しています。この関数を使って登録した後始末関数は、インタプリタが
終了するときに自動的に実行されます。

.. note::

   プログラムがシグナルで停止させられたとき、Python の致命的な内部 エラーが検出されたとき、あるいは:func:`os._exit`が呼び出された
   ときには、このモジュールを通して登録した関数は呼び出されません。

.. index:: single: exitfunc (in sys)

このモジュールは、``sys.exitfunc`` 変数の提供している機能の代用とな るインタフェースです。

.. note::

   ``sys.exitfunc``を設定する他のコードとともに使用した場合には、 このモジュールは正しく動作しないでしょう。特に、他のコア Python
   モジュールでは、プログラマの意図を知らなくても:mod:`atexit`を自由に 使えます。``sys.exitfunc`` を使っている人は、代わりに
   :mod:`atexit`を使うコードに変換してください。 ``sys.exitfunc`` を設定するコードを変換するには、:mod:`atexit` を
   import し、``sys.exitfunc`` へ束縛されていた関数を登録するのが 最も簡単です。


.. function:: register(func[, *args[, **kargs]])

   終了時に実行される関数として*func*を登録します。すべての*func* へ渡すオプションの引数を、:func:`register`へ引数としてわたさなけ
   ればなりません。

   通常のプログラムの終了時、例えば:func:`sys.exit` が呼び出されると き、あるいは、メインモジュールの実行が完了したときに、登録された全ての
   関数を、最後に登録されたものから順に呼び出します。通常、より低レベルの モジュールはより高レベルのモジュールより前に import されるので、
   後で後始末が行われるという仮定に基づいています。

   終了ハンドラの実行中に例外が発生すると、(:exc:`SystemExit`以外の 場合は)トレースバックを表示して、例外の情報を保存します。
   全ての終了ハンドラに動作するチャンスを与えた後に、最後に送出された 例外を再送出します。


.. seealso::

   Module :mod:`readline`
      :mod:`readline`ヒストリファイルを読み書き するための:mod:`atexit`の有用な例です。


.. _atexit-example:

:mod:`atexit` 例
----------------

次の簡単な例では、あるモジュールを import した時にカウンタを初期化し ておき、プログラムが終了するときにアプリケーションがこのモジュールを明
示的に呼び出さなくてもカウンタが更新されるようにする方法を示しています。 ::

   try:
       _count = int(open("/tmp/counter").read())
   except IOError:
       _count = 0

   def incrcounter(n):
       global _count
       _count = _count + n

   def savecounter():
       open("/tmp/counter", "w").write("%d" % _count)

   import atexit
   atexit.register(savecounter)

:func:`register` に指定した固定引数とキーワードパラメタは 登録した関数を呼び出す際に渡されます。 ::

   def goodbye(name, adjective):
       print 'Goodbye, %s, it was %s to meet you.' % (name, adjective)

   import atexit
   atexit.register(goodbye, 'Donny', 'nice')

   # or:
   atexit.register(goodbye, adjective='nice', name='Donny')

