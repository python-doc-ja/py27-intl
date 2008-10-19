
:mod:`test` --- Python用回帰テストパッケージ
=================================

.. module:: test


.. sectionauthor:: Brett Cannon <brett@python.org>




:mod:`test` パッケージには、Python 用の全ての回帰テストと、
:mod:`test.test_support`および:mod:`test.regrtest` モジュール
が入っています。:mod:`test.test_support` はテストを充実させる ために使い、:mod:`test.regtest`
はテストスイートを駆動するのに 使います。

:mod:`test`パッケージ内の各モジュールのうち、名前が``test_`` で始まるものは、特定のモジュールや機能に対するテストスイートです。
新しいテストはすべて:mod:`unittest`モジュールを使って書くように してください; 必ずしも:mod:`unittest`
を使う必要はないのですが、 :mod:`unittest` はテストをより柔軟にし、メンテナンスをより簡単に
します。古いテストのいくつかは:mod:`doctest` を利用しており、 "伝統的な" テスト形式になっています。これらのテスト形式をカバー
する予定はありません。


.. seealso::

   Module :mod:`unittest`
      PyUnit 回帰テストを書く。

   Module :mod:`doctest`
      ドキュメンテーション文字列に埋め込まれたテスト。


.. _writing-tests:

:mod:`test`パッケージのためのユニットテストを書く
------------------------------

.. % 

:mod:`test` パッケージ用のテストを書く場合、:mod:`unittest` モジュールを使い、以下のいくつかのガイドラインに従うよう推奨します。
一つは、テストモジュールの名前を、``test_``で始め、テスト 対象となるモジュール名で終えることです。 テストモジュール中のテストメソッドは
名前を``test_``で始めて、そのメソッドが何をテストしているかという説明で終えます。 これはテスト駆動プログラムに
そのメソッドをテストメソッドとして認識させるため必要です。 また、テストメソッドにはドキュメンテーション文字列を入れるべきでは ありません。
テストメソッドのドキュメント記述には、 (``# True あるいは False だけを返すテスト関数`` のような)  コメントを使ってください。
これは、ドキュメンテーション文字列が存在する場合にはその内容が出力 されるため、どのテストを実行しているのかをいちいち表示しなくするためです。

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

この定型的なコードによって、テストスイートを:mod:`regrtest.py` から起動できると同時に、スクリプト自体からも実行できるようになります。

回帰テストの目的はコードの分解です。 そのためには以下のいくつかのガイドラインに従ってください:

* テストスイートはすべてのクラス、関数および定数を用いるべきです。 これは外部に公開される外部APIだけでなく"非公開"コードも含んでいます。

* ホワイトボックス・テスト (テストを書くときに対象のコードをすぐ テストする) を推奨します。ブラックボックス・テスト (最終的に公開された
  ユーザーインターフェイスだけをテストする) は、すべての境界条件と 極端条件を確実にテストするには完全ではありません。

* 無効な値を含み、すべての取りうる値を確実にテストするように してください。そうすることで、全ての有効な値を受理するだけでなく、
  不適切な値を正しく処理することも確認できます。

* できる限り多くのコード経路を網羅してください。分岐が生じる テストし、入力を調整して、コードの全体に渡って取りえる限りの個々の
  処理経路を確実にたどらせるようにしてください。

* テスト対象のコードにどんなバグが発見された場合でも、明示的な テスト追加するようにしてください。そうすることで、将来コードを変更した
  際にエラーが再発しないようにできます。

* (一時ファイルをすべて閉じたり削除したりするといった) テストの 後始末を必ず行ってください。

* テストがオペレーティングシステムの特定の状況に依存する場合、 テストを開始する前に状況を確認してください。

* import するモジュールをできるかぎり少なくし、可能な限り 早期に import を行ってください。そうすることで、てテストの外部依存性を
  最小限にし、モジュールの import による副作用から生じる変則的な動作を 最小限にできます。

* コードの再利用を最大限に行うようにしてください。時として、 テストの多様性はどんな型の入力を受け取るかの違いまで小さくなります。
  例えば以下のように、入力が指定されたサブクラスで基底テストクラスを サブクラス化して、コードの複製を最小化します::

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
      コードより前にテストを書く 方法論に関する Kent Beck の著書


.. _regrtest:

:mod:`test.regrtest`を使ってテストを実行する
--------------------------------

:mod:`test.regrtest` を使うと Python の回帰テストスイートを駆動
できます。スクリプトを単独で実行すると、自動的に:mod:`test` パッケージ内のすべての回帰テストを実行し始めます。パッケージ内の
名前が``test_``で始まる全モジュールを見つけ、それをインポートし、 もしあるなら関数 :func:`test_main` を実行してテストを行います。
実行するテストの名前もスクリプトに渡される可能性もあります。 単一の回帰テストを指定  (:program:`python regrtest.py`
:option:`test_spam.py`) すると、 出力を最小限にします。テストが成功したかあるいは失敗したかだけを出力
するので、出力は最小限になります。

直接 :mod:`test.regrtest` を実行すると、テストに利用するリソースを 設定できます。これを行うには、:option:`-u`
コマンドラインオプションを使います。すべてのリソースを使うには、 :program:`python regrtest.py` :option:`-uall`
を実行します。 :option:`-u` のオプションに :option:`all` を指定すると、 すべてのリソースを有効にします。(よくある場合ですが)
何か一つを除く 全てが必要な場合、カンマで区切った不要なリソースのリストを :option:`all` の後に並べます。
コマンド:program:`python regrtest.py` :option:`-uall,-audio,-largefile`
とすると、:option:`audio` と :option:`largefile` リソースを除く
全てのリソースを使って:mod:`test.regrtest` を実行します。 すべてのリソースのリストと追加のコマンドラインオプションを出力
するには、:program:`python regrtest.py` :option:`-h` を実行 してください。

テストを実行しようとするプラットフォームによっては、回帰テストを 実行する別の方法があります。 Unix では、Python
をビルドしたトップレベルディレクトリで :program:`make` :option:`test` を実行できます。
Windows上では、:file:`PCBuild` ディレクトリから :program:`rt.bat` を 実行すると、すべての回帰テストを実行します。


:mod:`test.test_support` --- テストのためのユーティリティ関数
---------------------------------------------

.. module:: test.test_support
   :synopsis: Python 回帰テストのサポート


:mod:`test.test_support` モジュールでは、 Python の回帰テストに対する サポートを提供しています。

このモジュールは次の例外を定義しています:


.. exception:: TestFailed

   テストが失敗したとき送出される例外です。


.. exception:: TestSkipped

   :exc:`TestFailed`のサブクラスです。 テストがスキップされたとき送出されます。 テスト時に (ネットワーク接続のような) 必要なリソースが利用
   できないときに送出されます。


.. exception:: ResourceDenied

   :exc:`TestSkipped`のサブクラスです。 (ネットワーク接続のような)リソースが利用できないとき送出されます。
   :func:`requires`関数によって送出されます。

:mod:`test.test_support` モジュールでは、以下の定数を定義しています:


.. data:: verbose

   冗長な出力が有効な場合は:const:`True` です。 実行中のテストについてのより詳細な情報が欲しいときにチェックします。 *verbose* は
   :mod:`test.regrtest` によって設定されます。


.. data:: have_unicode

   ユニコードサポートが利用可能ならば:const:`True` になります。


.. data:: is_jython

   実行中のインタプリタが Jython ならば:const:`True` になります。


.. data:: TESTFN

   一時ファイルを作成するパスに設定されます。 作成した一時ファイルは全て閉じ、unlink (削除) せねばなりません。

:mod:`test.test_support` モジュールでは、以下の関数を定義しています:


.. function:: forget(module_name)

   モジュール名*module_name*を:mod:`sys.modules`から取り除き、 モジュールのバイトコンパイル済みファイルを全て削除します。


.. function:: is_resource_enabled(resource)

   *resource* が有効で利用可能ならば:const:`True`を返します。
   利用可能なリソースのリストは、:mod:`test.regrtest`がテストを 実行している間のみ設定されます。


.. function:: requires(resource[, msg])

   *resource* が利用できなければ、:exc:`ResourceDenied`を 送出します。その場合、*msg*は
   :exc:`ResourceDenied` の引数に なります。*__name__* が ``"__main__"`` である関数にから
   呼び出された場合には常に真を返します。 テストを:mod:`test.regrtest` から実行するときに使われます。


.. function:: findfile(filename)

   *filename*という名前のファイルへのパスを返します。 一致するものが見つからなければ、*filename* 自体を返します。 *filename*
   自体もファイルへのパスでありえるので、 *filename* が返っても失敗ではありません。


.. function:: run_unittest(*classes)

   渡された :class:`unittest.TestCase` サブクラスを実行します。 この関数は名前が ``test_`` で始まるメソッドを探して、
   テストを個別に実行します。 この方法をテストの実行方法として推奨しています。


.. function:: run_suite(suite[, testclass=None])

   :class:`unittest.TestSuite` のインスタンス *suite*を実行します。 オプション引数*testclass*
   はテストスイート内のテストクラスの 一つを受け取り、指定するとテストスイートが存在する場所についてさらに 詳細な情報を出力します。

