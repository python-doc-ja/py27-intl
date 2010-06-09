
:mod:`test` --- Python用回帰テストパッケージ
============================================

.. module:: test


.. sectionauthor:: Brett Cannon <brett@python.org>




:mod:`test` パッケージには、Python 用の全ての回帰テストと、
:mod:`test.test_support` および :mod:`test.regrtest` モジュール
が入っています。 :mod:`test.test_support` はテストを充実させるために使い、 :mod:`test.regrtest`
はテストスイートを駆動するのに使います。

.. Each module in the :mod:`test` package whose name starts with ``test_`` is a
   testing suite for a specific module or feature. All new tests should be written
   using the :mod:`unittest` or :mod:`doctest` module.  Some older tests are
   written using a "traditional" testing style that compares output printed to
   ``sys.stdout``; this style of test is considered deprecated.

:mod:`test` パッケージ内の各モジュールのうち、名前が ``test_`` で始まるものは、特定のモジュールや機能に対するテストスイートです。
新しいテストはすべて :mod:`unittest` か :mod:`doctest` モジュールを使って書くようにしてください
古いテストのいくつかは、 ``sys.stdout`` への出力を比較する"伝統的な"テスト形式になっていますが、
この形式のテストは廃止予定です。


.. seealso::

   Module :mod:`unittest`
      PyUnit 回帰テストを書く。

   Module :mod:`doctest`
      ドキュメンテーション文字列に埋め込まれたテスト。


.. _writing-tests:

:mod:`test` パッケージのためのユニットテストを書く
--------------------------------------------------

:mod:`unittest` モジュールを使ってテストを書く場合、幾つかのガイドラインに従うことが推奨されます。
1つは、テストモジュールの名前を、 ``test_`` で始め、テスト対象となるモジュール名で終えることです。
テストモジュール中のテストメソッドは名前を ``test_`` で始めて、
そのメソッドが何をテストしているかという説明で終えます。
これはテスト駆動プログラムにそのメソッドをテストメソッドとして認識させるため必要です。
また、テストメソッドにはドキュメンテーション文字列を入れるべきではありません。
テストメソッドのドキュメント記述には、 (``# True あるいは False だけを返すテスト関数`` のような)  コメントを使ってください。
これは、ドキュメンテーション文字列が存在する場合にはその内容が出力されるため、どのテストを実行しているのかをいちいち表示しなくするためです。

以下のような基本的な決まり文句を使います::

   import unittest
   from test import test_support

   class MyTestCase1(unittest.TestCase):

       # Only use setUp() and tearDown() if necessary

       def setUp(self):
           ... code to execute in preparation for tests ...

       def tearDown(self):
           ... code to execute to clean up after tests ...

       def test_feature_one(self):
           # Test feature one.
           ... testing code ...

       def test_feature_two(self):
           # Test feature two.
           ... testing code ...

       ... more test methods ...

   class MyTestCase2(unittest.TestCase):
       ... same structure as MyTestCase1 ...

   ... more test classes ...

   def test_main():
       test_support.run_unittest(MyTestCase1,
                                 MyTestCase2,
                                 ... list other tests ...
                                 )

   if __name__ == '__main__':
       test_main()

この定型的なコードによって、テストスイートを :mod:`regrtest.py` から起動できると同時に、スクリプト自体からも実行できるようになります。

回帰テストの目的はコードの分解です。そのためには以下のいくつかのガイドラインに従ってください:

* テストスイートはすべてのクラス、関数および定数を用いるべきです。これは外部に公開される外部APIだけでなく"非公開"コードも含んでいます。

* ホワイトボックス・テスト (テストを書くときに対象のコードをすぐテストする) を推奨します。ブラックボックス・テスト (最終的に公開された
  ユーザーインターフェイスだけをテストする) は、すべての境界条件と極端条件を確実にテストするには完全ではありません。

* 無効な値を含み、すべての取りうる値を確実にテストするようにしてください。そうすることで、全ての有効な値を受理するだけでなく、
  不適切な値を正しく処理することも確認できます。

* できる限り多くのコード経路を網羅してください。分岐が生じるテストし、入力を調整して、コードの全体に渡って取りえる限りの個々の
  処理経路を確実にたどらせるようにしてください。

* テスト対象のコードにどんなバグが発見された場合でも、明示的なテスト追加するようにしてください。そうすることで、将来コードを変更した
  際にエラーが再発しないようにできます。

* (一時ファイルをすべて閉じたり削除したりするといった) テストの後始末を必ず行ってください。

* テストがオペレーティングシステムの特定の状況に依存する場合、テストを開始する前に状況を確認してください。

* import するモジュールをできるかぎり少なくし、可能な限り早期に import を行ってください。そうすることで、てテストの外部依存性を
  最小限にし、モジュールの import による副作用から生じる変則的な動作を最小限にできます。

* コードの再利用を最大限に行うようにしてください。時として、テストの多様性はどんな型の入力を受け取るかの違いまで小さくなります。
  例えば以下のように、入力が指定されたサブクラスで基底テストクラスをサブクラス化して、コードの複製を最小化します::

     class TestFuncAcceptsSequences(unittest.TestCase):

         func = mySuperWhammyFunction

         def test_func(self):
             self.func(self.arg)

     class AcceptLists(TestFuncAcceptsSequences):
         arg = [1,2,3]

     class AcceptStrings(TestFuncAcceptsSequences):
         arg = 'abc'

     class AcceptTuples(TestFuncAcceptsSequences):
         arg = (1,2,3)


.. seealso::

   Test Driven Development
      コードより前にテストを書く方法論に関する Kent Beck の著書


.. _regrtest:

:mod:`test.regrtest` を使ってテストを実行する
---------------------------------------------

:mod:`test.regrtest` を使うと Python の回帰テストスイートを駆動
できます。スクリプトを単独で実行すると、自動的に :mod:`test` パッケージ内のすべての回帰テストを実行し始めます。パッケージ内の
名前が ``test_`` で始まる全モジュールを見つけ、それをインポートし、もしあるなら関数 :func:`test_main` を実行してテストを行います。
実行するテストの名前もスクリプトに渡される可能性もあります。単一の回帰テストを指定  (:program:`python regrtest.py`
:option:`test_spam.py`) すると、出力を最小限にします。テストが成功したかあるいは失敗したかだけを出力
するので、出力は最小限になります。

直接 :mod:`test.regrtest` を実行すると、テストに利用するリソースを設定できます。これを行うには、 :option:`-u`
コマンドラインオプションを使います。すべてのリソースを使うには、 :program:`python regrtest.py` :option:`-uall`
を実行します。 :option:`-u` のオプションに :option:`all` を指定すると、すべてのリソースを有効にします。(よくある場合ですが)
何か一つを除く全てが必要な場合、カンマで区切った不要なリソースのリストを :option:`all` の後に並べます。
コマンド :program:`python regrtest.py` :option:`-uall,-audio,-largefile`
とすると、 :option:`audio` と :option:`largefile` リソースを除く
全てのリソースを使って :mod:`test.regrtest` を実行します。すべてのリソースのリストと追加のコマンドラインオプションを出力
するには、 :program:`python regrtest.py` :option:`-h` を実行してください。

テストを実行しようとするプラットフォームによっては、回帰テストを実行する別の方法があります。 Unix では、Python
をビルドしたトップレベルディレクトリで :program:`make` :option:`test` を実行できます。
Windows上では、 :file:`PCBuild` ディレクトリから :program:`rt.bat` を実行すると、すべての回帰テストを実行します。


:mod:`test.test_support` --- テストのためのユーティリティ関数
-------------------------------------------------------------

.. module:: test.test_support
   :synopsis: Python 回帰テストのサポート

.. .. note::
   The :mod:`test.test_support` module has been renamed to :mod:`test.support`
   in Python 3.0.  The :term:`2to3` tool will automatically adapt imports when
   converting your sources to 3.0.

.. note::
   :mod:`test.test_support` モジュールは、Python 3では :mod:`test.support` にリネームされました。
   :term:`2to3` ツールは、ソースコード内のimportを自動的にPython 3用に修正します。

:mod:`test.test_support` モジュールでは、 Python の回帰テストに対するサポートを提供しています。

このモジュールは次の例外を定義しています:


.. exception:: TestFailed

   テストが失敗したとき送出される例外です。
   これは、 :mod:`unittest` ベースのテストでは廃止予定で、 :class:`unittest.TestCase`
   の assertXXX メソッドが推奨されます。


.. exception:: TestSkipped

   :exc:`TestFailed` のサブクラスです。テストがスキップされたとき送出されます。テスト時に (ネットワーク接続のような) 必要なリソースが利用
   できないときに送出されます。


.. exception:: ResourceDenied

   :exc:`TestSkipped` のサブクラスです。 (ネットワーク接続のような)リソースが利用できないとき送出されます。
   :func:`requires` 関数によって送出されます。

:mod:`test.test_support` モジュールでは、以下の定数を定義しています:


.. data:: verbose

   冗長な出力が有効な場合は :const:`True` です。実行中のテストについてのより詳細な情報が欲しいときにチェックします。 *verbose* は
   :mod:`test.regrtest` によって設定されます。


.. data:: have_unicode

   ユニコードサポートが利用可能ならば :const:`True` になります。


.. data:: is_jython

   実行中のインタプリタが Jython ならば :const:`True` になります。


.. data:: TESTFN

   一時ファイルを作成するパスに設定されます。作成した一時ファイルは全て閉じ、unlink (削除) せねばなりません。

:mod:`test.test_support` モジュールでは、以下の関数を定義しています:


.. function:: forget(module_name)

   モジュール名 *module_name* を :mod:`sys.modules` から取り除き、モジュールのバイトコンパイル済みファイルを全て削除します。


.. function:: is_resource_enabled(resource)

   *resource* が有効で利用可能ならば :const:`True` を返します。
   利用可能なリソースのリストは、 :mod:`test.regrtest` がテストを実行している間のみ設定されます。


.. function:: requires(resource[, msg])

   *resource* が利用できなければ、 :exc:`ResourceDenied` を送出します。その場合、 *msg* は
   :exc:`ResourceDenied` の引数になります。 *__name__* が ``"__main__"`` である関数にから
   呼び出された場合には常に真を返します。テストを :mod:`test.regrtest` から実行するときに使われます。


.. function:: findfile(filename)

   *filename* という名前のファイルへのパスを返します。一致するものが見つからなければ、 *filename* 自体を返します。 *filename*
   自体もファイルへのパスでありえるので、 *filename* が返っても失敗ではありません。


.. function:: run_unittest(*classes)

   渡された :class:`unittest.TestCase` サブクラスを実行します。この関数は名前が ``test_`` で始まるメソッドを探して、
   テストを個別に実行します。

   .. It is also legal to pass strings as parameters; these should be keys in
      ``sys.modules``. Each associated module will be scanned by
      ``unittest.TestLoader.loadTestsFromModule()``. This is usually seen in the
      following :func:`test_main` function::

   引数に文字列を渡すことも許可されています。その場合、文字列は ``sys.module``
   のキーでなければなりません。
   指定された各モジュールは、 ``unittest.TestLoader.loadTestsFromModule()``
   でスキャンされます。
   この関数は、よく次のような :func:`test_main` 関数の形で利用されます。 ::

      def test_main():
          test_support.run_unittest(__name__)

   .. This will run all tests defined in the named module.

   この関数は、名前で指定されたモジュールの中の全ての定義されたテストを実行します。


.. function:: check_warnings()

   .. A convenience wrapper for ``warnings.catch_warnings()`` that makes
      it easier to test that a warning was correctly raised with a single
      assertion. It is approximately equivalent to calling
      ``warnings.catch_warnings(record=True)``.

   warning が正しく発行されているかどうか1つのassertionでチェックする、
   ``warnings.catch_warnings()`` を使いやすくするラッパーです。
   これは、 ``warnings.catch_warnings(record=True)`` を呼ぶのとほぼ同じです。

   .. The main difference is that on entry to the context manager, a
      :class:`WarningRecorder` instance is returned instead of a simple list.
      The underlying warnings list is available via the recorder object's
      :attr:`warnings` attribute, while the attributes of the last raised
      warning are also accessible directly on the object. If no warning has
      been raised, then the latter attributes will all be :const:`None`.

   主な違いは、この関数がコンテキストマネージャーのエントリーになっていることです。
   ただのリストの代わりに、 :class:`WarningRecorder` のインスタンスが返されます。
   warning のリストには、 recorder オブジェクトの :attr:`warnings` 属性からアクセスできます。
   また、最後に発生した warning には、オブジェクトから直接アクセスすることができます。
   warning が1つも発生しなかった場合は、後者の属性は :const:`None` になります。

   .. todo::
      訳注: 直接アクセスの部分が、具体的にどうするのか判ってないので確認する。

   .. A :meth:`reset` method is also provided on the recorder object. This
      method simply clears the warning list.

   recorder オブジェクトは :meth:`reset` メソッドを持っています。
   このメソッドは warning リストをクリアします。

   .. The context manager is used like this::

   コンテキストマネージャーは次のようにして利用します。 ::

      with check_warnings() as w:
          warnings.simplefilter("always")
          warnings.warn("foo")
          assert str(w.message) == "foo"
          warnings.warn("bar")
          assert str(w.message) == "bar"
          assert str(w.warnings[0].message) == "foo"
          assert str(w.warnings[1].message) == "bar"
          w.reset()
          assert len(w.warnings) == 0

   .. versionadded:: 2.6


.. function:: captured_stdout()

   .. This is a context manager than runs the :keyword:`with` statement body using
      a :class:`StringIO.StringIO` object as sys.stdout.  That object can be
      retrieved using the ``as`` clause of the :keyword:`with` statement.

   これは、 :keyword:`with` 文の body で ``sys.stdout`` として :class:`StringIO.StringIO`
   オブジェクトを利用するコンテキストマネージャーです。
   このオブジェクトは、 :keyword:`with` 文の ``as`` 節で受け取ることができます。

   .. Example use::

   使用例::

      with captured_stdout() as s:
          print "hello"
      assert s.getvalue() == "hello"

   .. versionadded:: 2.6


.. The :mod:`test.test_support` module defines the following classes:

:mod:`test.test_support` モジュールは以下のクラスを定義しています。

.. class:: TransientResource(exc[, **kwargs])

   .. Instances are a context manager that raises :exc:`ResourceDenied` if the
      specified exception type is raised.  Any keyword arguments are treated as
      attribute/value pairs to be compared against any exception raised within the
      :keyword:`with` statement.  Only if all pairs match properly against
      attributes on the exception is :exc:`ResourceDenied` raised.

   このクラスのインスタンスはコンテキストマネージャーで、指定された型の例外が発生した場合に
   :exc:`ResourceDenied` 例外を発生させます。
   キーワード引数は全て、 :keyword:`with` 文の中で発生した全ての例外の 属性名/属性値 と比較されます。
   全てのキーワード引数が例外の属性に一致した場合に、 :exc:`ResourceDenied` 例外が発生します。

   .. versionadded:: 2.6

.. class:: EnvironmentVarGuard()

   .. Class used to temporarily set or unset environment variables.  Instances can be
      used as a context manager.

   一時的に環境変数をセット・アンセットするためのクラスです。
   このクラスのインスタンスはコンテキストマネージャーとして利用されます。

   .. versionadded:: 2.6


.. method:: EnvironmentVarGuard.set(envvar, value)

   .. Temporarily set the environment variable ``envvar`` to the value of ``value``.

   一時的に、 ``envvar`` を ``value`` にセットします。


.. method:: EnvironmentVarGuard.unset(envvar)

   .. Temporarily unset the environment variable ``envvar``.

   一時的に ``envvar`` をアンセットします。

.. class:: WarningsRecorder()

   ..  Class used to record warnings for unit tests. See documentation of
      :func:`check_warnings` above for more details.

   ユニットテスト時にwarningを記録するためのクラスです。
   上の、 :func:`check_warnings` のドキュメントを参照してください。

   .. versionadded:: 2.6

