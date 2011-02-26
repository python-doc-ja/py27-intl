
:mod:`unittest` --- ユニットテストフレームワーク
================================================

.. module:: unittest
   :synopsis: ユニットテストフレームワーク
.. moduleauthor:: Steve Purcell <stephen_purcell@yahoo.com>
.. sectionauthor:: Steve Purcell <stephen_purcell@yahoo.com>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. sectionauthor:: Raymond Hettinger <python@rcn.com>


.. versionadded:: 2.1

この Python ユニットテストフレームワークは時に "PyUnit" とも呼ばれ、
Kent Beck と Erich Gamma による JUnit の Python 版です。
JUnit はまた Kent の Smalltalk 用テストフレームワークの Java 版で、
どちらもそれぞれの言語で業界標準のユニットテストフレームワークとなっています。

:mod:`unittest` では、テストの自動化・初期設定と終了処理の共有・テスト
の分類・テスト実行と結果レポートの分離などの機能を提供しており、
:mod:`unittest` のクラスを使って簡単にたくさんのテストを開発できるよ
うになっています。

このようなことを実現するために :mod:`unittest` では、テストを以下のよ
うな構成で開発します。

test fixture (テストフィクスチャー)
   :dfn:`test fixture` とは、テスト実行のために必要な準備や終了処理を
   指します。例: テスト用データベースの作成・ディレクトリ・サーバプロ
   セスの起動など。

test case (テストケース)
   :dfn:`test case` はテストの最小単位で、各入力に対する結果をチェック
   します。テストケースを作成する場合は、 :mod:`unittest` が提供する
   :class:`TestCase` クラスを基底クラスとして利用することができます。

test suite (テストスイート)
   :dfn:`test suite` はテストケースとテストスイートの集まりで、同時に
   実行しなければならないテストをまとめる場合に使用します。

test runner (テストランナー)
   :dfn:`test runner` はテストの実行と結果表示を管理するコンポーネント
   です。ランナーはグラフィカルインターフェースでもテキストインターフェー
   スでも良いですし、何も表示せずにテスト結果を示す値を返すだけの場合
   もあります。

:mod:`unittest` では、テストケースとテストフィクスチャーを、
:class:`TestCase` クラスと :class:`FunctionTestCase` クラスで提供して
います。 :class:`TestCase` クラスは新規にテストを作成する場合に使用し、
:class:`FunctionTestCase` は既存のテストを :mod:`unittest` に組み込む
場合に使用します。テストフィクスチャーの設定処理と終了処理は、
:class:`TestCase` では :meth:`setUp` メソッドと :meth:`tearDown` をオー
バーライドして記述し、 :class:`FunctionTestCase` では初期設定・終了処
理を行う既存の関数をコンストラクタで指定します。テスト実行時、まずテス
トフィクスチャーの初期設定が最初に実行されます。初期設定が正常終了した
場合、テスト実行後にはテスト結果に関わらず終了処理が実行されます。
:class:`TestCase` の各インスタンスが実行するテストは一つだけで、テスト
フィクスチャーは各テストごとに新しく作成されます。

テストスイートは :class:`TestSuite` クラスで実装されており、複数のテス
トとテストスイートをまとめる事ができます。テストスイートを実行すると、
スイートと子スイートに追加されている全てのテストが実行されます。

テストランナーは :meth:`run` メソッドを持つオブジェクトで、
:meth:`run` は引数として :class:`TestCase` か :class:`TestSuite` オブ
ジェクトを受け取り、テスト結果を :class:`TestResult` オブジェクトで戻
します。 :mod:`unittest` ではデフォルトでテスト結果を標準エラーに出力
する :class:`TextTestRunner` をサンプルとして実装しています。これ以外
のランナー (グラフィックインターフェース用など) を実装する場合でも、特
定のクラスから派生する必要はありません。


.. seealso::

   Module :mod:`doctest`
      もうひとつのテストをサポートするモジュールで、本モジュールと趣きが異なっています。

   `Simple Smalltalk Testing: With Patterns <http://www.XProgramming.com/testfram.htm>`_
      Kent Beck のテスティングフレームワークに関する原論文で、ここに記載されたパターンを
      :mod:`unittest` が使用しています。

   `Nose <http://code.google.com/p/python-nose/>`_ と `py.test <http://pytest.org>`_
      サードパーティのユニットテストフレームワークで軽量な文法でテストを書くことができます。
      例えば、``assert func(10) == 42``  のように書きます。

   `python-mock <http://python-mock.sourceforge.net/>`_ と `minimock <http://blog.ianbicking.org/minimock.html>`_
      テスト用のモックオブジェクトを作成するツールです (モックオブジェクトは外部リソースをシミュレートします)。

.. _unittest-minimal-example:

基礎的な例
----------

:mod:`unittest` モジュールには、テストの開発や実行の為の優れたツールが
用意されており、この節では、その一部を紹介します。ほとんどのユーザとっ
ては、ここで紹介するツールだけで十分でしょう。

以下は、 :mod:`random` モジュールの三つの関数をテストするスクリプトです。::

   import random
   import unittest

   class TestSequenceFunctions(unittest.TestCase):

       def setUp(self):
           self.seq = range(10)

       def test_shuffle(self):
           # make sure the shuffled sequence does not lose any elements
           random.shuffle(self.seq)
           self.seq.sort()
           self.assertEqual(self.seq, range(10))

       def test_choice(self):
           element = random.choice(self.seq)
           self.assertTrue(element in self.seq)

       def test_sample(self):
           self.assertRaises(ValueError, random.sample, self.seq, 20)
           for element in random.sample(self.seq, 5):
               self.assertTrue(element in self.seq)

   if __name__ == '__main__':
       unittest.main()

テストケースは、 :class:`unittest.TestCase` のサブクラスとして作成しま
す。メソッド名が ``test`` で始まる三つのメソッドがテストです。テストラ
ンナーはこの命名規約によってテストを行うメソッドを検索します。

これらのテスト内では、予定の結果が得られていることを確かめるために
:meth:`assertEqual` を、条件のチェックに :meth:`assert_` を、例外が発
生する事を確認するために :meth:`assertRaises` をそれぞれ呼び出していま
す。 :keyword:`assert` 文の代わりにこれらのメソッドを使用すると、テス
トランナーでテスト結果を集計してレポートを作成する事ができます。

:meth:`setUp` メソッドが定義されている場合、テストランナーは各テストを
実行する前に :meth:`setUp` メソッドを呼び出します。同様に、
:meth:`tearDown` メソッドが定義されている場合は各テストの実行後に呼び
出します。上のサンプルでは、それぞれのテスト用に新しいシーケンスを作成
するために :meth:`setUp` を使用しています。

サンプルの末尾が、簡単なテストの実行方法です。 :func:`unittest.main`
は、テストスクリプトのコマンドライン用インターフェースです。コマンドラ
インから起動された場合、上記のスクリプトから以下のような結果が出力され
ます::

   ...
   ----------------------------------------------------------------------
   Ran 3 tests in 0.000s

   OK

簡略化した結果を出力したり、コマンドライン以外からも起動する等のより細かい
制御が必要であれば、 :func:`unittest.main` を使用せずに別の方法でテス
トを実行します。例えば、上記サンプルの最後の2行は以下のように書くこと
ができます::

   suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
   unittest.TextTestRunner(verbosity=2).run(suite)

変更後のスクリプトをインタープリタや別のスクリプトから実行すると、以下
の出力が得られます::

   test_choice (__main__.TestSequenceFunctions) ... ok
   test_sample (__main__.TestSequenceFunctions) ... ok
   test_shuffle (__main__.TestSequenceFunctions) ... ok

   ----------------------------------------------------------------------
   Ran 3 tests in 0.110s

   OK

以上が :mod:`unittest` モジュールでよく使われる機能で、ほとんどのテス
トではこれだけでも十分です。基礎となる概念や全ての機能については以降の
章を参照してください。


.. _organizing-tests:

テストの構成
------------

ユニットテストの基礎となる構築要素は、 :dfn:`test case` --- セットアップと
正しさのチェックを行う、独立したシナリオ --- です。 :mod:`unittest` で
は、テストケースは :mod:`unittest` モジュールの :class:`TestCase` クラ
スのインスタンスで示します。テストケースを作成するには
:class:`TestCase` のサブクラスを記述するか、または
:class:`FunctionTestCase` を使用します。

:class:`TestCase` から派生したクラスのインスタンスは、このオブジェクト
だけで一件のテストと初期設定・終了処理を行います。

:class:`TestCase` インスタンスは外部から完全に独立し、単独で実行する事
も、他の任意のテストと一緒に実行する事もできなければなりません。

以下のように、 :class:`TestCase` のサブクラスは :meth:`runTest` をオー
バライドし、必要なテスト処理を記述するだけで簡単に書くことができます::

   import unittest

   class DefaultWidgetSizeTestCase(unittest.TestCase):
       def runTest(self):
           widget = Widget('The widget')
           self.assertEqual(widget.size(), (50,50), 'incorrect default size')

何らかのテストを行う場合、ベースクラス :class:`TestCase` の
:meth:`assert\*` か :meth:`fail\*` メソッドを使用してください。テスト
が失敗すると例外が送出され、 :mod:`unittest` はテスト結果を
:dfn:`failure` とします。その他の例外は :dfn:`error` となります。
これによりどこに問題があるかが判ります。 :dfn:`failure` は間違った結果
(6 になるはずが 5 だった) で発生します。 :dfn:`error` は間違ったコード
(たとえば間違った関数呼び出しによる :exc:`TypeError`) で発生します。

テストの実行方法については後述とし、まずはテストケースインスタンスの作
成方法を示します。テストケースインスタンスは、以下のように引数なしでコ
ンストラクタを呼び出して作成します。::

   testCase = DefaultWidgetSizeTestCase()

似たようなテストを数多く行う場合、同じ環境設定処理を何度も必要となりま
す。例えば上記のような Widget のテストが 100 種類も必要な場合、それぞ
れのサブクラスで :class:`Widget` オブジェクトを生成する処理を記述する
のは好ましくありません。

このような場合、初期化処理は :meth:`setUp` メソッドに切り出し、テスト
実行時にテストフレームワークが自動的に実行するようにすることができます::

   import unittest

   class SimpleWidgetTestCase(unittest.TestCase):
       def setUp(self):
           self.widget = Widget('The widget')

   class DefaultWidgetSizeTestCase(SimpleWidgetTestCase):
       def runTest(self):
           self.assertEqual(self.widget.size(), (50,50),
                           'incorrect default size')

   class WidgetResizeTestCase(SimpleWidgetTestCase):
       def runTest(self):
           self.widget.resize(100,150)
           self.assertEqual(self.widget.size(), (100,150),
                           'wrong size after resize')

テスト中に :meth:`setUp` メソッドで例外が発生した場合、テストフレーム
ワークはテストを実行することができないとみなし、 :meth:`runTest` を実
行しません。

同様に、終了処理を :meth:`tearDown` メソッドに記述すると、
:meth:`runTest` メソッド終了後に実行されます::

   import unittest

   class SimpleWidgetTestCase(unittest.TestCase):
       def setUp(self):
           self.widget = Widget('The widget')

       def tearDown(self):
           self.widget.dispose()
           self.widget = None

:meth:`setUp` が正常終了した場合、 :meth:`runTest` が成功したかどうか
に従って :meth:`tearDown` が実行されます。

このような、テストを実行する環境を :dfn:`fixture` と呼びます。

JUnit では、多数の小さなテストケースを同じテスト環境で実行する場合、全
てのテストについて :class:`DefaultWidgetSizeTestCase` のような
:class:`SimpleWidgetTestCase` のサブクラスを作成する必要があります。こ
れは時間のかかる、うんざりする作業ですので、 :mod:`unittest` ではより
簡単なメカニズムを用意しています::

   import unittest

   class WidgetTestCase(unittest.TestCase):
       def setUp(self):
           self.widget = Widget('The widget')

       def tearDown(self):
           self.widget.dispose()
           self.widget = None

       def test_default_size(self):
           self.assertEqual(self.widget.size(), (50,50),
                            'incorrect default size')

       def test_resize(self):
           self.widget.resize(100,150)
           self.assertEqual(self.widget.size(), (100,150),
                            'wrong size after resize')

この例では :meth:`~TestCase.runTest` がありませんが、二つのテストメソッドを定義
しています。このクラスのインスタンスは :meth:`test_\*` メソッドのどちら
か一方の実行と、 ``self.widget`` の生成・解放を行います。この場合、テ
ストケースインスタンス生成時に、コンストラクタの引数として実行するメソッ
ド名を指定します::

   defaultSizeTestCase = WidgetTestCase('test_default_size')
   resizeTestCase = WidgetTestCase('test_resize')

:mod:`unittest` では :class:`test suite` によってテストケースインスタ
ンスをテスト対象の機能によってグループ化することができます。
:dfn:`test suite` は、 :mod:`unittest` の :class:`TestSuite` クラスで
作成します。::

   widgetTestSuite = unittest.TestSuite()
   widgetTestSuite.addTest(WidgetTestCase('test_default_size'))
   widgetTestSuite.addTest(WidgetTestCase('test_resize'))

各テストモジュールで、テストケースを組み込んだテストスイートオブジェク
トを作成する呼び出し可能オブジェクトを用意しておくと、テストの実行や参
照が容易になります::

   def suite():
       suite = unittest.TestSuite()
       suite.addTest(WidgetTestCase('test_default_size'))
       suite.addTest(WidgetTestCase('test_resize'))
       return suite

または::

   def suite():
       tests = ['test_default_size', 'test_resize']

       return unittest.TestSuite(map(WidgetTestCase, tests))

一般的には、 :class:`TestCase` のサブクラスには良く似た名前のテスト関
数が複数定義されますので、 :mod:`unittest` ではテストスイートを作成し
て個々のテストで満たすプロセスを自動化するのに使う :class:`TestLoader`
を用意しています。たとえば、::

   suite = unittest.TestLoader().loadTestsFromTestCase(WidgetTestCase)

は ``WidgetTestCase.test_default_size()`` と
``WidgetTestCase.test_resize`` を走らせるテストスイートを作成します。
:class:`TestLoader` は自動的にテストメソッドを識別するのに ``'test'``
というメソッド名の接頭辞を使います。

いろいろなテストケースが実行される順序は、テスト関数名を組み込み関数
:func:`cmp` でソートして決定されます。

システム全体のテストを行う場合など、テストスイートをさらにグループ化し
たい場合がありますが、このような場合、 :class:`TestSuite` インスタンス
には :class:`TestSuite` と同じように :class:`TestSuite` を追加する事が
できます。::

   suite1 = module1.TheTestSuite()
   suite2 = module2.TheTestSuite()
   alltests = unittest.TestSuite([suite1, suite2])

テストケースやテストスイートは (:file:`widget.py` のような) テスト対象
のモジュール内にも記述できますが、テストは (:file:`test_widget.py` の
ような) 独立したモジュールに置いた方が以下のような点で有利です:

* テストモジュールだけをコマンドラインから実行することができる。

* テストコードと出荷するコードを分離する事ができる。

* テストコードを、テスト対象のコードに合わせて修正する誘惑に駆られにくい。

* テストコードは、テスト対象コードほど頻繁に更新されない。

* テストコードをより簡単にリファクタリングすることができる。

* Cで書いたモジュールのテストは、どっちにしろ独立したモジュールとなる。

* テスト戦略を変更した場合でも、ソースコードを変更する必要がない。


.. _legacy-unit-tests:

既存テストコードの再利用
------------------------

既存のテストコードが有るとき、このテストを :mod:`unittest` で実行しよ
うとするために古いテスト関数をいちいち :class:`TestCase` クラスのサブ
クラスに変換するのは大変です。

このような場合は、 :mod:`unittest` では :class:`TestCase` のサブクラス
である :class:`FunctionTestCase` クラスを使い、既存のテスト関数をラッ
プします。初期設定と終了処理も行なえます。

以下のテストコードがあった場合::

   def testSomething():
       something = makeSomething()
       assert something.name is not None
       # ...

テストケースインスタンスは次のように作成します::

   testcase = unittest.FunctionTestCase(testSomething)

初期設定、終了処理が必要な場合は、次のように指定します::

   testcase = unittest.FunctionTestCase(testSomething,
                                        setUp=makeSomethingDB,
                                        tearDown=deleteSomethingDB)

既存のテストスイートからの移行を容易にするため、 :mod:`unittest` は
:exc:`AssertionError` の送出でテストの失敗を示すような書き方もサポート
しています。
しかしながら、 :meth:`TestCase.fail\*` および
:meth:`TestCase.assert\*` メソッドを使って明確に書くことが推奨されてい
ます。 :mod:`unittest` の将来のバージョンでは、 :exc:`AssertionError`
は別の目的に使用される可能性が有ります。

.. note::

   :class:`FunctionTestCase` を使って既存のテストを :mod:`unittest` ベー
   スのテスト体系に変換することができますが、この方法は推奨されません。
   時間を掛けて :class:`TestCase` のサブクラスに書き直した方が将来的な
   テストのリファクタリングが限りなく易しくなります。


.. _unittest-contents:

クラスと関数
------------


.. class:: TestCase([methodName])

   :class:`TestCase` クラスのインスタンスは、 :mod:`unittest` の世界に
   おけるテストの最小実行単位を示します。このクラスをベースクラスとし
   て使用し、必要なテストを具象サブクラスに実装します。
   :class:`TestCase` クラスでは、テストランナーがテストを実行するため
   のインターフェースと、各種のチェックやテスト失敗をレポートするため
   のメソッドを実装しています。

   それぞれの :class:`TestCase` クラスのインスタンスはただ一つのテスト
   メソッド、 *methodName* という名のメソッドを実行します。既に次のよ
   うな例を扱ったことを憶えているでしょうか。::

      def suite():
          suite = unittest.TestSuite()
          suite.addTest(WidgetTestCase('test_default_size'))
          suite.addTest(WidgetTestCase('test_resize'))
          return suite

   ここでは、それぞれが一つずつのテストを実行するような
   :class:`WidgetTestCase` の二つのインスタンスを作成しています。

   *methodName* のデフォルトは ``'runTest'`` です。


.. class:: FunctionTestCase(testFunc[, setUp[, tearDown[, description]]])

   このクラスでは :class:`TestCase` インターフェースの内、テストランナー
   がテストを実行するためのインターフェースだけを実装しており、テスト
   結果のチェックやレポートに関するメソッドは実装していません。既存の
   テストコードを :mod:`unittest` によるテストフレームワークに組み込む
   ために使用します。


.. class:: TestSuite([tests])

   このクラスは、個々のテストケースやテストスイートの集約を示します。
   通常のテストケースと同じようにテストランナーで実行するためのインタ
   フェースを備えています。 :class:`TestSuite` インスタンスを実行する
   ことはスイートの繰り返しを使って個々のテストを実行することと同じで
   す。

   引数 *tests* が与えられるならば、それはテストケースに亘る繰り返し可
   能オブジェクトまたは内部でスイートを組み立てるための他のテストスイー
   トでなければなりません。
   後からテストケースやスイートをコレクションに付け加えるためのメソッ
   ドも提供されています。


.. class:: TestLoader()

   モジュールまたは :class:`TestCase` クラスから、指定した条件に従って
   テストをロードし、 :class:`TestSuite` にラップして返します。このク
   ラスは与えられたモジュールまたは :class:`TestCase` のサブクラスの中
   から全てのテストをロードできます。


.. class:: TestResult()

   このクラスはどのテストが成功しどのテストが失敗したかの情報を集積す
   るのに使います。


.. data:: defaultTestLoader

   :class:`TestLoader` のインスタンスで、共用することが目的です。
   :class:`TestLoader` をカスタマイズする必要がなければ、新しい
   :class:`TestLoader` オブジェクトを作らずにこのインスタンスを使用し
   ます。


.. class:: TextTestRunner([stream[, descriptions[, verbosity]]])

   実行結果を標準エラーに出力する、単純なテストランナー。いくつかの設
   定項目がありますが、非常に単純です。グラフィカルなテスト実行アプリ
   ケーションでは、独自のテストランナーを作成してください。


.. function:: main([module[, defaultTest[, argv[, testRunner[, testLoader]]]]])

   テストを実行するためのコマンドラインプログラム。この関数を使えば、
   簡単に実行可能なテストモジュールを作成する事ができます。
   一番簡単なこの関数の使い方は、以下の行をテストスクリプトの最後に置
   くことです。 ::

      if __name__ == '__main__':
          unittest.main()

   引数、 *testRunner* は、test runner class、あるいは、そのインスタン
   スのどちらでも構いません。

場合によっては、 :mod:`doctest` モジュールを使って書かれた既存のテスト
があります。その場合、モジュールは既存の :mod:`doctest` に基づいたテス
トコードから :class:`unittest.TestSuite` インスタンスを自動的に構築で
きる :class:`DocTestSuite` クラスを提供します。

.. versionadded:: 2.3


.. _testcase-objects:

TestCase オブジェクト
---------------------

:class:`TestCase` クラスのインスタンスは個別のテストをあらわすオブジェ
クトですが、 :class:`TestCase` の具象サブクラスには複数のテストを定義
する事ができます --- 具象サブクラスは、特定の fixture (テスト設備) を示し
ている、と考えてください。 fixture は、それぞれのテストケースごとに作成・
解放されます。

:class:`TestCase` インスタンスには、次の3種類のメソッドがあります:
テストを実行するためのメソッド・条件のチェックやテスト失敗のレポートの
ためのメソッド・テストの情報収集に使用する問い合わせメソッドです。

テストを実行するためのメソッドを以下に示します:


.. method:: TestCase.setUp()

   テストを実行する直前に、 fixture を作成する為に呼び出されます。この
   メソッドを実行中に例外が発生した場合、テストの失敗ではなくエラーと
   されます。デフォルトの実装では何も行いません。


.. method:: TestCase.tearDown()

   テストを実行し、結果を記録した直後に呼び出されます。テスト実行中に
   例外が発生しても呼び出されますので、内部状態に注意して処理を行って
   ください。メソッドを実行中に例外が発生した場合、テストの失敗ではな
   くエラーとみなされます。このメソッドは、 :meth:`setUp` が正常終了し
   た場合にはテストメソッドの実行結果に関わり無く呼び出されます。デフォ
   ルトの実装では何も行いません。


.. method:: TestCase.run([result])

   テストを実行し、テスト結果を *result* に指定されたテスト結果オブジェ
   クトに収集します。 *result* が :const:`None` か省略された場合、一時
   的な結果オブジェクトを( :meth:`defaultTestCase` メソッドを呼んで)生成
   して使用しますが :meth:`run` の呼び出し元には渡されません。

   このメソッドは、 :class:`TestCase` インスタンスの呼び出しと等価です。


.. method:: TestCase.debug()

   テスト結果を収集せずにテストを実行します。例外が呼び出し元に通知さ
   れるため、テストをデバッガで実行することができます。

テスト結果のチェックとレポートには、以下のメソッドを使用してください。


.. method:: TestCase.assert_(expr[, msg])
            TestCase.failUnless(expr[, msg])
            TestCase.assertTrue(expr[, msg])

   *expr* が偽の場合、テスト失敗を通知します。 *msg* にはエラーの説明
    を指定するか、または :const:`None` を指定してください。


.. method:: TestCase.assertEqual(first, second[, msg])
            TestCase.failUnlessEqual(first, second[, msg])

   *first* と *second* *expr* が等しくない場合、テスト失敗を通知します。
   エラー内容は *msg* に指定された値か、または :const:`None` となりま
   す。 :meth:`failUnlessEqual` では *msg* のデフォルト値は *first* と
   *second* を含んだ文字列となりますので、 :meth:`failUnless` の第一引
   数に比較の結果を指定するよりも便利です。


.. method:: TestCase.assertNotEqual(first, second[, msg])
            TestCase.failIfEqual(first, second[, msg])

   *first* と *second* *expr* が等しい場合、テスト失敗を通知します。エ
   ラー内容は *msg* に指定された値か、または :const:`None` となります。
   :meth:`failUnlessEqual` では *msg* のデフォルト値は *first* と
   *second* を含んだ文字列となりますので、 :meth:`failUnless` の第一引
   数に比較の結果を指定するよりも便利です。


.. method:: TestCase.assertAlmostEqual(first, second[, places[, msg]])
            TestCase.failUnlessAlmostEqual(first, second[, places[, msg]])

   *first* と *second* を *places* (デフォルトは 7 です) で与えた小数
   位で値を丸めて差分を計算し、ゼロと比較することで、近似的に等価であ
   るかどうかをテストします。指定小数位の比較というものは指定有効桁数
   の比較ではないので注意してください。
   値の比較結果が等しくなかった場合、テストは失敗し、 *msg* で指定した
   説明か、 :const:`None` を返します。


.. method:: TestCase.assertNotAlmostEqual(first, second[, places[, msg]])
            TestCase.failUnlessAlmostEqual(first, second[, places[, msg]])

   *first* と *second* を *places* (デフォルトは 7 です) で与えた小数
   位で値を丸めて差分を計算し、ゼロと比較することで、近似的に等価でな
   いかどうかをテストします。指定小数位の比較というものは指定有効桁数
   の比較ではないので注意してください。
   値の比較結果が等しかった場合、テストは失敗し、 *msg* で与えた説明か、
   :const:`None` を返します。


.. method:: TestCase.assertRaises(exception, callable, ...)
            TestCase.failUnlessRaises(exception, callable, ...)

   *callable* を呼び出し、発生した例外をテストします。
   :meth:`assertRaises` には、任意の位置パラメータとキーワードパラメー
   タを指定する事ができます。 *exception* で指定した例外が発生した場合
   はテスト成功とし、それ以外の例外が発生するか例外が発生しない場合に
   テスト失敗となります。複数の例外を指定する場合には、例外クラスのタ
   プルを *exception* に指定します。


.. method:: TestCase.failIf(expr[, msg])
            TestCase.assertFalse(expr[, msg])

   :meth:`failIf` は :meth:`failUnless` の逆で、 *expr* が真の場合、テ
   スト失敗を通知します。エラー内容は *msg* に指定された値か、または
   :const:`None` となります。


.. method:: TestCase.fail([msg])

   無条件にテスト失敗を通知します。エラー内容は *msg* に指定された値か、
   または :const:`None` となります。


.. attribute:: TestCase.failureException

   :meth:`test` メソッドが送出する例外を指定するクラス属性。テストフレー
   ムワークで追加情報を持つ等の特殊な例外を使用する場合、この例外のサ
   ブクラスとして作成します。この属性の初期値は :exc:`AssertionError`
   です。

テストフレームワークは、テスト情報を収集するために以下のメソッドを使用
します:


.. method:: TestCase.countTestCases()

   テストオブジェクトに含まれるテストの数を返します。
   :class:`TestCase` インスタンスは常に ``1`` を返します。


.. method:: TestCase.defaultTestResult()

   このテストケースクラスで使われるテスト結果クラスのインスタンスを (
   もし :meth:`run` メソッドに他の結果インスタンスが提供されないならば
   ) 返します。

   :class:`TestCase` インスタンスに対しては、いつも
   :class:`TestResult` のインスタンスですので、 :class:`TestCase` のサ
   ブクラスでは必要に応じてこのメソッドをオーバライドしてください。


.. method:: TestCase.id()

   テストケースを特定する文字列を返します。通常、 *id* はモジュール名・
   クラス名を含む、テストメソッドのフルネームを指定します。


.. method:: TestCase.shortDescription()

   テストの説明を一行分、または説明がない場合には :const:`None` を返し
   ます。デフォルトでは、テストメソッドの docstring の先頭の一行、また
   は :const:`None` を返します。


.. _testsuite-objects:

TestSuite オブジェクト
----------------------

:class:`TestSuite` オブジェクトは :class:`TestCase` とよく似た動作をし
ますが、実際のテストは実装せず、一まとめにに実行するテストのグループを
まとめるために使用します。 :class:`TestSuite` には以下のメソッドが追加
されています:


.. method:: TestSuite.addTest(test)

   :class:`TestCase` 又は :class:`TestSuite` のインスタンスをスイート
   に追加します。


.. method:: TestSuite.addTests(tests)

   イテラブル *tests* に含まれる全ての :class:`TestCase` 又は
   :class:`TestSuite` のインスタンスをスイートに追加します。

   このメソッドは *test* 上のイテレーションをしながらそれぞれの要素に
   :meth:`addTest` を呼び出すのと等価です。

:class:`TestSuite` クラスは :class:`TestCase` と以下のメソッドを共有し
ます:


.. method:: TestSuite.run(result)

   スイート内のテストを実行し、結果を *result* で指定した結果オブジェ
   クトに収集します。 :meth:`TestCase.run` と異なり、
   :meth:`TestSuite.run` では必ず結果オブジェクトを指定する必要があり
   ます。


.. method:: TestSuite.debug()

   このスイートに関連づけられたテストを結果を収集せずに実行します。こ
   れによりテストで送出された例外は呼び出し元に伝わるようになり、デバッ
   ガの下でのテスト実行をサポートできるようになります。


.. method:: TestSuite.countTestCases()

   このテストオブジェクトによって表現されるテストの数を返します。これ
   には個別のテストと下位のスイートも含まれます。

通常、 :class:`TestSuite` の :meth:`run` メソッドは
:class:`TestRunner` が起動するため、ユーザが直接実行する必要はありませ
ん。


.. _testresult-objects:

TestResultオブジェクト
----------------------

:class:`TestResult` は、複数のテスト結果を記録します。
:class:`TestCase` クラスと :class:`TestSuite` クラスのテスト結果を正し
く記録しますので、テスト開発者が独自にテスト結果を管理する処理を開発す
る必要はありません。

:mod:`unittest` を利用したテストフレームワークでは、
:meth:`TestRunner.run` が返す :class:`TestResult` インスタンスを参照し、
テスト結果をレポートします。

以下の属性は、テストの実行結果を検査する際に使用することができます:


.. attribute:: TestResult.errors

   :class:`TestCase` と例外のトレースバック情報をフォーマットした文字
   列の 2 要素タプルからなるリスト。それぞれのタプルは予想外の例外を送
   出したテストに対応します。

   .. versionchanged:: 2.2
      :func:`sys.exc_info` の結果ではなく、フォーマットしたトレースバッ
      クを保存します。


.. attribute:: TestResult.failures

   :class:`TestCase` と例外のトレースバック情報をフォーマットした文字列の
   2 要素タプルからなるリスト。それぞれのタプルは
   :meth:`TestCase.fail\*` や :meth:`TestCase.assert\*` メソッドを使っ
   て見つけ出した失敗に対応します。

   .. versionchanged:: 2.2
      :func:`sys.exc_info` の結果ではなく、フォーマットしたトレースバッ
      クを保存します。


.. attribute:: TestResult.testsRun

   これまでに実行したテストの総数です。


.. method:: TestResult.wasSuccessful()

   これまでに実行したテストが全て成功していれば :const:`True` を、それ
   以外なら :const:`False` を返します。


.. method:: TestResult.stop()

   このメソッドを呼び出して :class:`TestResult` の ``shouldStop`` 属性
   に :const:`True` をセットすることで、実行中のテストは中断しなければ
   ならないというシグナルを送ることができます。 :class:`TestRunner` オ
   ブジェクトはこのフラグを尊重してそれ以上のテストを実行することなく
   復帰しなければなりません。

   たとえばこの機能は、ユーザのキーボード割り込みを受け取って
   :class:`TextTestRunner` クラスがテストフレームワークを停止させるの
   に使えます。 :class:`TestRunner` の実装を提供する対話的なツールでも
   同じように使用することができます。

以下のメソッドは内部データ管理用のメソッドですが、対話的にテスト結果を
レポートするテストツールを開発する場合などにはサブクラスで拡張すること
ができます。


.. method:: TestResult.startTest(test)

   *test* を実行する直前に呼び出されます。

   デフォルトの実装では単純にインスタンスの ``testRun`` カウンタをインクリメントします。


.. method:: TestResult.stopTest(test)

   *test* の実行直後に、テスト結果に関わらず呼び出されます。

   デフォルトの実装では何もしません。


.. method:: TestResult.addError(test, err)

   テスト *test* 実行中に、想定外の例外が発生した場合に呼び出されます。
   *err* は :func:`sys.exc_info` が返すタプル ``(type, value,
   traceback)`` です。

   デフォルトの実装では、タプル、 ``(test, formatted_err)`` をインスタ
   ンスの ``errors`` 属性に追加します。ここで、 *formatted_err* は、
   *err* から導出される、整形されたトレースバックです。


.. method:: TestResult.addFailure(test, err)

   テストが失敗した場合に呼び出されます。 *err* は
   :func:`sys.exc_info` が返すタプル ``(type, value, traceback)`` です。

   デフォルトの実装では、タプル、 ``(test, formatted_err)`` をインスタ
   ンスの ``errors`` 属性に追加します。ここで、 *formatted_err* は、
   *err* から導出される、整形されたトレースバックです。


.. method:: TestResult.addSuccess(test)

   テストケース *test* が成功した場合に呼び出されます。

   デフォルトの実装では何もしません。


.. _testloader-objects:

TestLoader オブジェクト
-----------------------

:class:`TestLoader` クラスは、クラスやモジュールからテストスイートを作
成するために使用します。通常はこのクラスのインスタンスを作成する必要は
なく、 :mod:`unittest` モジュールのモジュール属性
``unittest.defaultTestLoader`` を共用インスタンスとして使用することが
できます。ただ、サブクラスや別のインスタンスを活用すると設定可能なプロ
パティをカスタマイズすることもできます。

:class:`TestLoader` オブジェクトには以下のメソッドがあります:


.. method:: TestLoader.loadTestsFromTestCase(testCaseClass)

   :class:`TestCase` の派生クラス :class:`testCaseClass` に含まれる全
   テストケースのスイートを返します。


.. method:: TestLoader.loadTestsFromModule(module)

   指定したモジュールに含まれる全テストケースのスイートを返します。このメ
   ソッドは *module* 内の :class:`TestCase` 派生クラスを検索し、見つかっ
   たクラスのテストメソッドごとにクラスのインスタンスを作成します。

   .. warning::

      :class:`TestCase` クラスを基底クラスとしてクラス階層を構築すると
      fixture や補助的な関数をうまく共用することができますが、基底クラ
      スに直接インスタンス化できないテストメソッドがあると、この
      :meth:`loadTestsFromModule` を使うことができません。この場合でも、
      fixture が全て別々で定義がサブクラスにある場合は使用することがで
      きます。


.. method:: TestLoader.loadTestsFromName(name[, module])

   文字列で指定される全テストケースを含むスイートを返します。

   *name* には "ドット修飾名" でモジュールかテストケースクラス、テスト
   ケースクラス内のメソッド、 :class:`TestSuite` インスタンスまたは
   :class:`TestCase` か :class:`TestSuite` のインスタンスを返す呼び出
   し可能オブジェクトを指定します。このチェックはここで挙げた順番に行
   なわれます。すなわち、候補テストケースクラス内のメソッドは「呼び出
   し可能オブジェクト」としてではなく「テストケースクラス内のメソッド」
   として拾い出されます。

   例えば :mod:`SampleTests` モジュールに :class:`TestCase` から派生し
   た :class:`SampleTestCase` クラスがあり、 :class:`SampleTestCase`
   にはテストメソッド :meth:`test_one` ・ :meth:`test_two` ・
   :meth:`test_three` があるとします。この場合、 *name* に
   ``'SampleTests.SampleTestCase'`` と指定すると、
   :class:`SampleTestCase` の三つのテストメソッドを実行するテストスイートが
   作成されます。 ``'SampleTests.SampleTestCase.test_two'`` と指定すれ
   ば、 :meth:`test_two` だけを実行するテストスイートが作成されます。
   インポートされていないモジュールやパッケージ名を含んだ名前を指定し
   た場合は自動的にインポートされます。

   また、 *module* を指定した場合、 *module* 内の *name* を取得します。


.. method:: TestLoader.loadTestsFromNames(names[, module])

   :meth:`loadTestsFromName` と同じですが、名前を一つだけ指定するので
   はなく、複数の名前のシーケンスを指定する事ができます。戻り値は
   *names* 中の名前で指定されるテスト全てを含むテストスイートです。


.. method:: TestLoader.getTestCaseNames(testCaseClass)

   *testCaseClass* 中の全てのメソッド名を含むソート済みシーケンスを返
   します。 *testCaseClass* は :class:`TestCase` のサブクラスでなけれ
   ばなりません。

以下の属性は、サブクラス化またはインスタンスの属性値を変更して
:class:`TestLoader` をカスタマイズする場合に使用します。


.. attribute:: TestLoader.testMethodPrefix

   テストメソッドの名前と判断されるメソッド名の接頭語を示す文字列。デ
   フォルト値は ``'test'`` です。

   この値は :meth:`getTestCaseNames` と全ての :meth:`loadTestsFrom\*`
   メソッドに影響を与えます。


.. attribute:: TestLoader.sortTestMethodsUsing

   :meth:`getTestCaseNames` および全ての :meth:`loadTestsFrom\*` メソッ
   ドでメソッド名をソートする際に使用する比較関数。デフォルト値は組み
   込み関数 :func:`cmp` です。ソートを行なわないようにこの属性に
   :const:`None` を指定することもできます。


.. attribute:: TestLoader.suiteClass

   テストのリストからテストスイートを構築する呼び出し可能オブジェクト。
   メソッドを持つ必要はありません。デフォルト値は :class:`TestSuite`
   です。

   この値は全ての :meth:`loadTestsFrom\*` メソッドに影響を与えます。

.. % \subsection{追加エラー情報の取得
.. % \label{unittest-error-info}}
.. % 統合開発環境(IDE)等のアプリケーションでは、より詳細なエラー情報を使用す
.. % る場合があります。この場合、独自の\class{TestResult}クラスの実装を使用
.. % し、\class{TestCase}クラスの\method{defaultTestResult()}メソッドを拡張し
.. % て必要な情報を取得する事ができます。
.. % 以下に\class{TestResult}を拡張して例外オブジェクトとトレースバックオブジ
.. % ェクトをそのまま格納する例を示します。(トレースバックオブジェクトを保存
.. % すると、通常は解放されるメモリが解放されなくなり、テストの実行に影響を与
.. % える場合がありますので注意してください。)
.. % %begin{verbatim}
.. % import unittest
.. % class MyTestCase(unittest.TestCase):
.. % def defaultTestResult(self):
.. % return MyTestResult()
.. % class MyTestResult(unittest.TestResult):
.. % def __init__(self):
.. % self.errors_tb = []
.. % self.failures_tb = []
.. % def addError(self, test, err):
.. % self.errors_tb.append((test, err))
.. % unittest.TestResult.addError(self, test, err)
.. % def addFailure(self, test, err):
.. % self.failures_tb.append((test, err))
.. % unittest.TestResult.addFailure(self, test, err)
.. % %end{verbatim}
.. % \class{TestCase}ではなく\class{MyTestCase}をベースクラスとしたテストで
.. % は、追加情報がテスト結果オブジェクトに格納されます。

