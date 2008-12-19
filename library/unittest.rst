
:mod:`unittest` --- 単体テストフレームワーク
============================================

.. module:: unittest
   :synopsis: 単体テストフレームワーク
.. moduleauthor:: Steve Purcell <stephen_purcell@yahoo.com>
.. sectionauthor:: Steve Purcell <stephen_purcell@yahoo.com>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. sectionauthor:: Raymond Hettinger <python@rcn.com>


.. versionadded:: 2.1

このPython単体テストフレームワーク は時に"PyUnit"とも呼ばれ、Kent Beck と Erich
GammaによるJUnitのPython版です。JUnitはまたKentのSmalltalk用テスト
フレームワークのJava版で、どちらもそれぞれの言語で業界標準の単体テストフ レームワークとなっています。

:mod:`unittest`では、テストの自動化・初期設定と終了処理の共有・テストの分類・テス
ト実行と結果レポートの分離などの機能を提供しており、:mod:`unittest`の クラスを使って簡単にたくさんのテストを開発できるようになっています。

このようなことを実現するために :mod:`unittest`では、 テストを以下のような構成で開発します。

Fixture
   :dfn:`test fixture(テスト設備)`とは、テスト実行のために必要な準備や終了処
   理を指します。例:テスト用データベースの作成・ディレクトリ・サーバプロセ スの起動など。

テストケース
   :dfn:`テストケース`はテストの最小単位で、各入力に対する結果をチェックしま
   す。テストケースを作成する場合は、:mod:`unittest`が提供する:class:`TestCase`クラス を基底クラスとして利用することができます。

テストスイート
   :dfn:`テストスイート`はテストケースとテストスイートの集まりで、同時に実行 しなければならないテストをまとめる場合に使用します。

テストランナー
   :dfn:`テストランナー`はテストの実行と結果表示を管理するコンポーネントで す。ランナーはグラフィカルインターフェースでもテキストインターフェースで
   も良いですし、何も表示せずにテスト結果を示す値を返すだけの場合もありま す。

:mod:`unittest`では、テストケースとfixtureを、:class:`TestCase`クラスと
:class:`FunctionTestCase`クラスで提供しています。:class:`TestCase`クラスは
新規にテストを作成する場合に使用し、:class:`FunctionTestCase`は既存のテス
トを:mod:`unittest`に組み込む場合に使用します。fixtureの設定処理と終了処理は、
:class:`TestCase`では:meth:`setUp`メソッドと:meth:`tearDown`をオー
バーライドして記述し、:class:`FunctionTestCase`では初期設定・終了処理を行
う既存の関数をコンストラクタで指定します。テスト実行時、まずfixtureの初 期設定が最初に実行されます。初期設定が正常終了した場合、テスト実行後には
テスト結果に関わらず終了処理が実行されます。:class:`TestCase`の各インスタ
ンスが実行するテストは一つだけで、fixtureは各テストごとに新しく作成され ます。

テストスイートは:class:`TestSuite`クラスで実装されており、複数のテストと
テストスイートをまとめる事ができます。テストスイートを実行すると、スイー トと子スイートに追加されている全てのテストが実行されます。

テストランナーは:meth:`run`メソッドを持つオブジェクトで、
:meth:`run`は引数として:class:`TestCase`か:class:`TestSuite`オブジェク
トを受け取り、テスト結果を:class:`TestResult`オブジェクトで戻します。
:mod:`unittest`ではデフォルトでテスト結果を標準エラーに出力する
:class:`TextTestRunner`をサンプルとして実装しています。これ以外のランナー
(グラフィックインターフェース用など)を実装する場合でも、特定のクラスから 派生する必要はありません。


.. seealso::

   Module :mod:`doctest`
      Another test-support module with a very different flavor.

   `Simple Smalltalk Testing: With Patterns <http://www.XProgramming.com/testfram.htm>`_
      Kent Beck's original paper on testing frameworks using the pattern shared by
      :mod:`unittest`.


.. _minimal-example:

基礎的な例
----------

:mod:`unittest`モジュールには、テストの開発や実行の為の優れたツールが 用意されており、この節では、その一部を紹介します。ほとんどのユーザとって
は、ここで紹介するツールだけで十分でしょう。

以下は、:mod:`random`モジュールの三つの関数をテストするスクリプトです。 ::

   import random
   import unittest

   class TestSequenceFunctions(unittest.TestCase):

       def setUp(self):
           self.seq = range(10)

       def testshuffle(self):
           # make sure the shuffled sequence does not lose any elements
           random.shuffle(self.seq)
           self.seq.sort()
           self.assertEqual(self.seq, range(10))

       def testchoice(self):
           element = random.choice(self.seq)
           self.assert_(element in self.seq)

       def testsample(self):
           self.assertRaises(ValueError, random.sample, self.seq, 20)
           for element in random.sample(self.seq, 5):
               self.assert_(element in self.seq)

   if __name__ == '__main__':
       unittest.main()

テストケースは、:class:`unittest.TestCase`のサブクラスとして作成します。メ
ソッド名が``test``で始まる三つのメソッドがテストです。テストランナー はこの命名規約によってテストを行うメソッドを検索します。

これらのテスト内では、予定の結果が得られていることを確かめるために
:meth:`assertEqual`を、条件のチェックに:meth:`assert_`を、例外が発
生する事を確認するために:meth:`assertRaises`をそれぞれ呼び出していま
す。:keyword:`assert`文の代わりにこれらのメソッドを使用すると、テストラン ナーでテスト結果を集計してレポートを作成する事ができます。

:meth:`setUp`メソッドが定義されている場合、テストランナーは各テストを 実行する前に:meth:`setUp`メソッドを呼び出します。同様に、
:meth:`tearDown`メソッドが定義されている場合は各テストの実行後に呼び
出します。上のサンプルでは、それぞれのテスト用に新しいシーケンスを作成するため に:meth:`setUp`を使用しています。

サンプルの末尾が、簡単なテストの実行方法です。:func:`unittest.main`は、
テストスクリプトのコマンドライン用インターフェースです。コマンドラインか ら起動された場合、上記のスクリプトから以下のような結果が出力されます::

   ...
   ----------------------------------------------------------------------
   Ran 3 tests in 0.000s

   OK

簡略化した結果を出力したり、コマンドライン以外からも起動する等のより細かい
制御が必要であれば、:func:`unittest.main`を使用せずに別の方法でテストを
実行します。例えば、上記サンプルの最後の2行は以下のように書くことができ ます::

   suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
   unittest.TextTestRunner(verbosity=2).run(suite)

変更後のスクリプトをインタープリタや別のスクリプトから実行すると、以下の 出力が得られます::

   testchoice (__main__.TestSequenceFunctions) ... ok
   testsample (__main__.TestSequenceFunctions) ... ok
   testshuffle (__main__.TestSequenceFunctions) ... ok

   ----------------------------------------------------------------------
   Ran 3 tests in 0.110s

   OK

以上が:mod:`unittest`モジュールでよく使われる機能で、ほとんどのテスト ではこれだけでも十分です。基礎となる概念や全ての機能については以降の章を
参照してください。


.. _organizing-tests:

テストの構成
------------

単体テストの基礎となる構築要素は、:dfn:`テストケース` --- セットアップと 正しさのチェックを行う、独立したシナリオ ---
です。:mod:`unittest`では、テスト ケースは:mod:`unittest`モジュールの:class:`TestCase`クラスのインスタ
ンスで示します。テストケースを作成するには:class:`TestCase`のサブクラスを
記述するか、または:class:`FunctionTestCase`を使用します。

:class:`TestCase`から派生したクラスのインスタンスは、このオブジェクトだけ で一件のテストと初期設定・終了処理を行います。

:class:`TestCase`インスタンスは外部から完全に独立し、単独で実行する事も、 他の任意のテストと一緒に実行する事もできなければなりません。

以下のように、:class:`TestCase`のサブクラスは:meth:`runTest`をオーバライドし、
必要なテスト処理を記述するだけで簡単に書くことができます::

   import unittest

   class DefaultWidgetSizeTestCase(unittest.TestCase):
       def runTest(self):
           widget = Widget('The widget')
           self.assertEqual(widget.size(), (50,50), 'incorrect default size')

何らかのテストを行う場合、ベースクラス:class:`TestCase`の :meth:`assert\*` か
:meth:`fail\*`メソッドを使用してください。 テストが失敗すると例外が送出され、:mod:`unittest`はテスト結果を
:dfn:`failure`とします。その他の例外は:dfn:`error`となります。
これによりどこに問題があるかが判ります。:dfn:`failure`は間違った結果 (6 になるはずが 5
だった)で発生します。:dfn:`error`は間違ったコード (たとえば間違った関数呼び出しによる:exc:`TypeError`)で発生します。

テストの実行方法については後述とし、まずはテストケースインスタンスの作成 方法を示します。テストケースインスタンスは、以下のように引数なしでコンス
トラクタを呼び出して作成します。 ::

   testCase = DefaultWidgetSizeTestCase()

似たようなテストを数多く行う場合、同じ環境設定処理を何度も必要となりま す。例えば上記のようなWidgetのテストが100種類も必要な場合、それぞれのサ
ブクラスで:class:`Widget`オブジェクトを生成する処理を記述するのは好ましくあり ません。

このような場合、初期化処理は:meth:`setUp`メソッドに切り出し、テスト実 行時にテストフレームワークが自動的に実行するようにすることができます::

   import unittest

   class SimpleWidgetTestCase(unittest.TestCase):
       def setUp(self):
           self.widget = Widget('The widget')

   class DefaultWidgetSizeTestCase(SimpleWidgetTestCase):
       def runTest(self):
           self.failUnless(self.widget.size() == (50,50),
                           'incorrect default size')

   class WidgetResizeTestCase(SimpleWidgetTestCase):
       def runTest(self):
           self.widget.resize(100,150)
           self.failUnless(self.widget.size() == (100,150),
                           'wrong size after resize')

テスト中に:meth:`setUp`メソッドで例外が発生した場合、テストフレーム
ワークはテストを実行することができないとみなし、:meth:`runTest`を実行 しません。

同様に、終了処理を:meth:`tearDown`メソッドに記述すると、 :meth:`runTest`メソッド終了後に実行されます::

   import unittest

   class SimpleWidgetTestCase(unittest.TestCase):
       def setUp(self):
           self.widget = Widget('The widget')

       def tearDown(self):
           self.widget.dispose()
           self.widget = None

:meth:`setUp`が正常終了した場合、:meth:`runTest`が成功したかどうかに従って :meth:`tearDown`が実行されます。

このような、テストを実行する環境を:dfn:`fixture`と呼びます。

JUnitでは、多数の小さなテストケースを同じテスト環境で実行する場合、全て
のテストについて:class:`DefaultWidgetSizeTestCase`のような
:class:`SimpleWidgetTestCase`のサブクラスを作成する必要があります。これは
時間のかかる、うんざりする作業ですので、:mod:`unittest`ではより簡単なメカニズムを 用意しています::

   import unittest

   class WidgetTestCase(unittest.TestCase):
       def setUp(self):
           self.widget = Widget('The widget')

       def tearDown(self):
           self.widget.dispose()
           self.widget = None

       def testDefaultSize(self):
           self.failUnless(self.widget.size() == (50,50),
                           'incorrect default size')

       def testResize(self):
           self.widget.resize(100,150)
           self.failUnless(self.widget.size() == (100,150),
                           'wrong size after resize')

この例では:meth:`runTest`がありませんが、二つのテストメソッドを定義し
ています。このクラスのインスタンスは:meth:`test\*`メソッドのどちらか一
方の実行と、``self.widget``の生成・解放を行います。この場合、テスト ケースインスタンス生成時に、コンストラクタの引数として実行するメソッド名
を指定します::

   defaultSizeTestCase = WidgetTestCase('testDefaultSize')
   resizeTestCase = WidgetTestCase('testResize')

:mod:`unittest`では:class:`テストスイート`によってテストケースインスタンスをテスト
対象の機能によってグループ化することができます。:dfn:`テストスイート`
は、:mod:`unittest`の:class:`TestSuite`クラスで作成します。 ::

   widgetTestSuite = unittest.TestSuite()
   widgetTestSuite.addTest(WidgetTestCase('testDefaultSize'))
   widgetTestSuite.addTest(WidgetTestCase('testResize'))

各テストモジュールで、テストケースを組み込んだテストスイートオブジェクト を作成する呼び出し可能オブジェクトを用意しておくと、テストの実行や参照が
容易になります::

   def suite():
       suite = unittest.TestSuite()
       suite.addTest(WidgetTestCase('testDefaultSize'))
       suite.addTest(WidgetTestCase('testResize'))
       return suite

または::

   def suite():
       tests = ['testDefaultSize', 'testResize']

       return unittest.TestSuite(map(WidgetTestCase, tests))

一般的には、:class:`TestCase`のサブクラスには良く似た名前のテスト関数が複 数定義されますので、:mod:`unittest`では
テストスイートを作成して個々のテストで満たすプロセスを自動化するのに使う :class:`TestLoader`を用意しています。 たとえば、 ::

   suite = unittest.TestLoader().loadTestsFromTestCase(WidgetTestCase)

は``WidgetTestCase.testDefaultSize()``と``WidgetTestCase.testResize``
を走らせるテストスイートを作成します。 :class:`TestLoader`は自動的にテストメソッドを識別するのに``'test'``という
メソッド名の接頭辞を使います。

いろいろなテストケースが実行される順序は、テスト関数名を組み込み関数:func:`cmp` でソートして決定されます。

システム全体のテストを行う場合など、テストスイートをさらにグループ化した
い場合がありますが、このような場合、:class:`TestSuite`インスタンスには
:class:`TestSuite`と同じように:class:`TestSuite`を追加する事ができます。 ::

   suite1 = module1.TheTestSuite()
   suite2 = module2.TheTestSuite()
   alltests = unittest.TestSuite([suite1, suite2])

テストケースやテストスイートは (:file:`widget.py` のような)  テスト対象のモジュール内にも記述できますが、テストは
(:file:`test_widget.py` のような) 独立したモジュールに置いた方が 以下のような点で有利です:

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

既存のテストコードが有るとき、このテストを:mod:`unittest`で実行しようと
するために古いテスト関数をいちいち:class:`TestCase`クラスのサブクラスに 変換するのは大変です。

このような場合は、:mod:`unittest`では:class:`TestCase`のサブクラスである
:class:`FunctionTestCase`クラスを使い、既存のテスト関数をラップします。初 期設定と終了処理も行なえます。

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

既存のテストスイートからの移行を容易にするため、:mod:`unittest`は
:exc:`AssertionError`の送出でテストの失敗を示すような書き方もサポートしています。
しかしながら、:meth:`TestCase.fail\*`および:meth:`TestCase.assert\*`
メソッドを使って明確に書くことが推奨されています。:mod:`unittest`の
将来のバージョンでは、:exc:`AssertionError`は別の目的に使用される可能性が有ります。

.. note::

   :class:`FunctionTestCase`を使って既存のテストを:mod:`unittest`ベースの
   テスト体系に変換することができますが、この方法は推奨されません。時間を掛けて
   :class:`TestCase`のサブクラスに書き直した方が将来的なテストのリファクタリングが 限りなく易しくなります。


.. _unittest-contents:

クラスと関数
------------


.. class:: TestCase([methodName])

   :class:`TestCase`クラスのインスタンスは、:mod:`unittest`の世界における テストの最小実行単位を示しま
   す。このクラスをベースクラスとして使用し、必要なテストを具象サブクラス に実装します。:class:`TestCase`クラスでは、テストランナーがテストを実行
   するためのインターフェースと、各種のチェックやテスト失敗をレポートする ためのメソッドを実装しています。

   それぞれの:class:`TestCase`クラスのインスタンスはただ一つのテストメソッド、
   *methodName*という名のメソッドを実行します。既に次のような例を扱った ことを憶えているでしょうか。 ::

      def suite():
          suite = unittest.TestSuite()
          suite.addTest(WidgetTestCase('testDefaultSize'))
          suite.addTest(WidgetTestCase('testResize'))
          return suite

   ここでは、それぞれが一つずつのテストを実行するような:class:`WidgetTestCase`の 二つのインスタンスを作成しています。

   *methodName*のデフォルトは``'runTest'``です。


.. class:: FunctionTestCase(testFunc[, setUp[, tearDown[, description]]])

   このクラスでは:class:`TestCase`インターフェースの内、テストランナーがテ ストを実行するためのインターフェースだけを実装しており、テスト結果のチ
   ェックやレポートに関するメソッドは実装していません。既存のテストコード を:mod:`unittest`によるテストフレームワークに組み込むために使用し ます。


.. class:: TestSuite([tests])

   このクラスは、個々のテストケースやテストスイートの集約を示します。通常 のテストケースと同じようにテストランナーで実行するためのインタフェース
   を備えています。:class:`TestSuite`インスタンスを実行することはスイートの 繰り返しを使って個々のテストを実行することと同じです。

   引数*tests*が与えられるならば、それはテストケースに亘る繰り返し可能オブジェクト
   または内部でスイートを組み立てるための他のテストスイートでなければなりません。
   後からテストケースやスイートをコレクションに付け加えるためのメソッドも提供されています。


.. class:: TestLoader()

   モジュールまたは:class:`TestCase`クラスから、指定した条件に従ってテス
   トをロードし、:class:`TestSuite`にラップして返します。このクラスは与え
   られたモジュールまたは:class:`TestCase`のサブクラスの中から全てのテス トをロードできます。


.. class:: TestResult()

   このクラスはどのテストが成功しどのテストが失敗したかの情報を集積する のに使います。


.. data:: defaultTestLoader

   :class:`TestLoader`のインスタンスで、共用することが目的です。 :class:`TestLoader`をカスタマイズする必要がなければ、新しい
   :class:`TestLoader`オブジェクトを作らずにこのインスタンスを使用します。


.. class:: TextTestRunner([stream[, descriptions[, verbosity]]])

   実行結果を標準エラーに出力する、単純なテストランナー。いくつかの設定項目 がありますが、非常に単純です。グラフィカルなテスト実行アプリケーション
   では、独自のテストランナーを作成してください。


.. function:: main([module[, defaultTest[, argv[, testRunner[, testRunner]]]]])

   テストを実行するためのコマンドラインプログラム。この関数を使えば、 簡単に実行可能なテストモジュールを作成する事ができます。
   一番簡単なこの関数の使い方は、以下の行をテストスクリプトの最後に置くことです。 ::

      if __name__ == '__main__':
          unittest.main()

場合によっては、:mod:`doctest` モジュールを使って書かれた 既存のテストがあります。その場合、モジュールは
既存の:mod:`doctest`に基づいたテストコードから :class:`unittest.TestSuite` インスタンスを 自動的に構築できる
:class:`DocTestSuite` クラスを提供します。

.. versionadded:: 2.3


.. _testcase-objects:

TestCase オブジェクト
---------------------

:class:`TestCase`クラスのインスタンスは個別のテストをあらわすオブジェクト
ですが、:class:`TestCase`の具象サブクラスには複数のテストを定義する事がで きます ---
具象サブクラスは、特定のfixture(テスト設備)を示している、と考 えてください。fixtureは、それぞれのテストケースごとに作成・解放されま す。

:class:`TestCase`インスタンスには、次の3種類のメソッドがあります:テストを
実行するためのメソッド・条件のチェックやテスト失敗のレポートのためのメソ ッド・テストの情報収集に使用する問い合わせメソッド。

テストを実行するためのメソッドを以下に示します:


.. method:: TestCase.setUp()

   テストを実行する直前に、fixtureを作成する為に呼び出されます。このメソ ッドを実行中に例外が発生した場合、テストの失敗ではなくエラーとされま
   す。デフォルトの実装では何も行いません。


.. method:: TestCase.tearDown()

   テストを実行し、結果を記録した直後に呼び出されます。テスト実行中に例外 が発生しても呼び出されますので、内部状態に注意して処理を行ってくださ
   い。メソッドを実行中に例外が発生した場合、テストの失敗ではなくエラーと みなされます。このメソッドは、:meth:`setUp`が正常終了した場合にはテ
   ストメソッドの実行結果に関わり無く呼び出されます。デフォルトの実装では 何も行いません。


.. method:: TestCase.run([result])

   テストを実行し、テスト結果を*result*に指定されたテスト結果オブジェ クトに収集します。*result*が:const:`None`か省略された場合、一時
   的な結果オブジェクトを(:meth:`defaultTestCase`メソッドを呼んで)生
   成して使用しますが:meth:`run`の呼び出し元には渡されません。

   このメソッドは、:class:`TestCase`インスタンスの呼び出しと等価です。


.. method:: TestCase.debug()

   テスト結果を収集せずにテストを実行します。例外が呼び出し元に通知される ため、テストをデバッガで実行することができます。

テスト結果のチェックとレポートには、以下のメソッドを使用してください。


.. method:: TestCase.assert_(expr[, msg])
            TestCase.failUnless(expr[, msg])

   *expr*が偽の場合、テスト失敗を通知します。*msg*にはエラーの説 明を指定するか、または:const:`None`を指定してください。


.. method:: TestCase.assertEqual(first, second[, msg])
            TestCase.failUnlessEqual(first, second[, msg])

   *first*と*second**expr*が等しくない場合、テスト失敗を通知
   します。エラー内容は*msg*に指定された値か、または:const:`None`となり
   ます。:meth:`failUnlessEqual`では*msg*のデフォルト値は *first*と*second*を含んだ文字列となりますので、
   :meth:`failUnless`の第一引数に比較の結果を指定するよりも便利です。


.. method:: TestCase.assertNotEqual(first, second[, msg])
            TestCase.failIfEqual(first, second[, msg])

   *first*と*second**expr*が等しい場合、テスト失敗を通知しま
   す。エラー内容は*msg*に指定された値か、または:const:`None`となりま
   す。:meth:`failUnlessEqual`では*msg*のデフォルト値は*first*
   と*second*を含んだ文字列となりますので、:meth:`failUnless`の第 一引数に比較の結果を指定するよりも便利です。


.. method:: TestCase.assertAlmostEqual(first, second[, places[, msg]])
            TestCase.failUnlessAlmostEqual(first, second[, places[, msg]])

   *first* と *second* を *places* で与えた小数位で値を丸めて差分を計算し、
   ゼロと比較することで、近似的に等価であるかどうかをテストします。 指定小数位の比較というものは指定有効桁数の比較ではないので注意してください。
   値の比較結果が等しくなかった場合、テストは失敗し、*msg* で指定した 説明か、:const:`None` を返します。


.. method:: TestCase.assertNotAlmostEqual(first, second[, places[, msg]])
            TestCase.failUnlessAlmostEqual(first, second[, places[, msg]])

   *first* と *second* を *places* で与えた小数位で値を丸めて差分を計算し、
   ゼロと比較することで、近似的に等価でないかどうかをテストします。 指定小数位の比較というものは指定有効桁数の比較ではないので注意してください。
   値の比較結果が等しかった場合、テストは失敗し、*msg* で与えた 説明か、:const:`None` を返します。


.. method:: TestCase.assertRaises(exception, callable, ...)
            TestCase.failUnlessRaises(exception, callable, ...)

   *callable*を呼び出し、発生した例外をテストします。 :meth:`assertRaises`には、任意の位置パラメータとキーワードパラメー
   タを指定する事ができます。*exception*で指定した例外が発生した場合 はテスト成功とし、それ以外の例外が発生するか例外が発生しない場合にテス
   ト失敗となります。複数の例外を指定する場合には、例外クラスのタプルを *exception*に指定します。


.. method:: TestCase.failIf(expr[, msg])

   :meth:`failIf`は:meth:`failUnless`の逆で、*expr*が真の場合、
   テスト失敗を通知します。エラー内容は*msg*に指定された値か、または :const:`None`となります。


.. method:: TestCase.fail([msg])

   無条件にテスト失敗を通知します。エラー内容は*msg*に指定された値 か、または:const:`None`となります。


.. attribute:: TestCase.failureException

   :meth:`test`メソッドが送出する例外を指定するクラス属性。テストフ レームワークで追加情報を持つ等の特殊な例外を使用する場合、この例外のサ
   ブクラスとして作成します。この属性の初期値は:exc:`AssertionError` です。

テストフレームワークは、テスト情報を収集するために以下のメソッドを使用し ます:


.. method:: TestCase.countTestCases()

   テストオブジェクトに含まれるテストの数を返します。:class:`TestCase`イン スタンスは常に``1``を返します。


.. method:: TestCase.defaultTestResult()

   このテストケースクラスで使われるテスト結果クラスのインスタンス を(もし:meth:`run`メソッドに他の結果インスタンスが提供されないなら ば)返します。

   :class:`TestCase`インスタンスに対しては、いつも:class:`TestResult`のイ
   ンスタンスですので、:class:`TestCase`のサブクラスでは必要に応じてこの メソッドをオーバライドしてください。


.. method:: TestCase.id()

   テストケースを特定する文字列を返します。通常、*id*はモジュール名・ クラス名を含む、テストメソッドのフルネームを指定します。


.. method:: TestCase.shortDescription()

   テストの説明を一行分、または説明がない場合には:const:`None`を返します。 デフォルトでは、テストメソッドのdocstringの先頭の一行、または
   :const:`None`を返します。


.. _testsuite-objects:

TestSuite オブジェクト
----------------------

:class:`TestSuite`オブジェクトは:class:`TestCase`とよく似た動作をします
が、実際のテストは実装せず、一まとめにに実行するテストのグループをまとめ
るために使用します。:class:`TestSuite`には以下のメソッドが追加されていま す:


.. method:: TestSuite.addTest(test)

   :class:`TestCase`又は:class:`TestSuite`のインスタンスをスイートに追加し ます。


.. method:: TestSuite.addTests(tests)

   イテラブル*tests*に含まれる全ての:class:`TestCase`又は :class:`TestSuite`のインスタンスをスイートに追加します。

   このメソッドは*test*上のイテレーションをしながらそれぞれの要素に :meth:`addTest`を呼び出すのと等価です。

:class:`TestSuite`クラスは:class:`TestCase`と以下のメソッドを共有します:


.. method:: TestSuite.run(result)

   スイート内のテストを実行し、結果を*result*で指定した結果オブジェク トに収集します。:meth:`TestCase.run`と異なり、
   :meth:`TestSuite.run`では必ず結果オブジェクトを指定する必要がありま す。


.. method:: TestSuite.debug()

   このスイートに関連づけられたテストを結果を収集せずに実行します。 これによりテストで送出された例外は呼び出し元に伝わるようになり、
   デバッガの下でのテスト実行をサポートできるようになります。


.. method:: TestSuite.countTestCases()

   このテストオブジェクトによって表現されるテストの数を返します。 これには個別のテストと下位のスイートも含まれます。

通常、:class:`TestSuite`の:meth:`run`メソッドは:class:`TestRunner`が起
動するため、ユーザが直接実行する必要はありません。


.. _testresult-objects:

TestResultオブジェクト
----------------------

:class:`TestResult`は、複数のテスト結果を記録します。:class:`TestCase`クラ
スと:class:`TestSuite`クラスのテスト結果を正しく記録しますので、テスト開 発者が独自にテスト結果を管理する処理を開発する必要はありません。

:mod:`unittest`を利用したテストフレームワークでは、
:meth:`TestRunner.run`が返す:class:`TestResult`インスタンスを参照し、 テスト結果をレポートします。

以下の属性は、テストの実行結果を検査する際に使用することができます:


.. attribute:: TestResult.errors

   :class:`TestCase`と例外のトレースバック情報をフォーマットした文字列の
   2要素タプルからなるリスト。それぞれのタプルは予想外の例外を送出したテストに 対応します。

   .. versionchanged:: 2.2
      :func:`sys.exc_info`の結果ではなく、 フォーマットしたトレースバックを保存.


.. attribute:: TestResult.failures

   :class:`TestCase`と例外のトレースバック情報をフォーマットした文字列の
   2要素タプルからなるリスト。それぞれのタプルは:meth:`TestCase.fail\*`や
   :meth:`TestCase.assert\*`メソッドを使って見つけ出した失敗に対応します。

   .. versionchanged:: 2.2
      :func:`sys.exc_info`の結果ではなく、フォーマット したトレースバックを保存.


.. attribute:: TestResult.testsRun

   これまでに実行したテストの総数。


.. method:: TestResult.wasSuccessful()

   これまでに実行したテストが全て成功していれば:const:`True`を、 それ以外なら:const:`False`を返す。


.. method:: TestResult.stop()

   このメソッドを呼び出して:class:`TestResult`の``shouldStop``属性
   に:const:`True`をセットすることで、実行中のテストは中断しなければな
   らないというシグナルを送ることができます。:class:`TestRunner`オブジェ クトはこのフラグを尊重してそれ以上のテストを実行することなく復帰しな
   ければなりません。

   たとえばこの機能は、ユーザのキーボード割り込みを受け取っ て:class:`TextTestRunner`クラスがテストフレームワークを停止させるのに
   使えます。:class:`TestRunner`の実装を提供する対話的なツールでも同じよ うに使用することができます。

以下のメソッドは内部データ管理用のメソッドですが、対話的にテスト結果をレ ポートするテストツールを開発する場合などにはサブクラスで拡張することがで きます。


.. method:: TestResult.startTest(test)

   *test*を実行する直前に呼び出されます。

   デフォルトの実装では単純にインスタンスの``testRun``カウンタをイン クリメントします。


.. method:: TestResult.stopTest(test)

   *test*の実行直後に、テスト結果に関わらず呼び出されます。

   デフォルトの実装では何もしません。


.. method:: TestResult.addError(test, err)

   テスト*test*実行中に、想定外の例外が発生した場合に呼び出されます。 *err*は:func:`sys.exc_info`が返すタプル``(type,
   value, traceback)``です。

   デフォルトの実装ではインスタンスの``errors``属性 に``(test, err)``を追加します。


.. method:: TestResult.addFailure(test, err)

   テストが失敗した場合に呼び出されます。*err*は :func:`sys.exc_info`が返すタプル``(type, value,
   traceback)``です。

   デフォルトの実装ではインスタンスの``failures``属性 に``(test, err)``を追加します。


.. method:: TestResult.addSuccess(test)

   テストケース*test*が成功した場合に呼び出されます。

   デフォルトの実装では何もしません。


.. _testloader-objects:

TestLoader オブジェクト
-----------------------

:class:`TestLoader`クラスは、クラスやモジュールからテストスイートを作成す
るために使用します。通常はこのクラスのインスタンスを作成する必要はなく、
:mod:`unittest`モジュールのモジュール属性``unittest.defaultTestLoader``を
共用インスタンスとして使用することができます。 ただ、サブクラスや別のインスタンスを活用すると設定可能なプロパティを カスタマイズすることもできます。

:class:`TestLoader` オブジェクトには以下のメソッドがあります:


.. method:: TestLoader.loadTestsFromTestCase(testCaseClass)

   :class:`TestCase`の派生クラス:class:`testCaseClass`に含まれる全テスト ケースのスイートを返します。


.. method:: TestLoader.loadTestsFromModule(module)

   指定したモジュールに含まれる全テストケースのスイートを返します。このメ
   ソッドは*module*内の:class:`TestCase`派生クラスを検索し、見つかった クラスのテストメソッドごとにクラスのインスタンスを作成します。

   .. warning::

      :class:`TestCase`クラスを基底クラスとしてクラス階層を構築する とfixtureや補助的な関数をうまく共用することができますが、基底クラスに
      直接インスタンス化できないテストメソッドがあると、この :meth:`loadTestsFromModule`を使うことができません。この場合でも、
      fixtureが全て別々で定義がサブクラスにある場合は使用することができま す。


.. method:: TestLoader.loadTestsFromName(name[, module])

   文字列で指定される全テストケースを含むスイートを返します。

   *name*には"ドット修飾名"でモジュールかテストケースクラス、テス トケースクラス内のメソッド、:class:`TestSuite`インスタンスまた
   は:class:`TestCase`か:class:`TestSuite`のインスタンスを返す呼び出し可能
   オブジェクトを指定します。このチェックはここで挙げた順番に行なわれます。 すなわち、候補テストケースクラス内のメソッドは「呼び出し可能オブジェクト」
   としてではなく「テストケースクラス内のメソッド」として拾い出されます。

   例えば:mod:`SampleTests`モジュールに
   :class:`TestCase`から派生した:class:`SampleTestCase`クラスがあり、
   :class:`SampleTestCase`にはテストメソッド:meth:`test_one`・
   :meth:`test_two`・:meth:`test_three`があるとします。この場合、
   *name*に``'SampleTests.SampleTestCase'``と指定すると、
   :class:`SampleTestCase`の三つのテストメソッドを実行するテストスイートが
   作成されます。``'SampleTests.SampleTestCase.test_two'``と指定すれ
   ば、:meth:`test_two`だけを実行するテストスイートが作成されます。イ ンポートされていないモジュールやパッケージ名を含んだ名前を指定した場合
   は自動的にインポートされます。

   また、*module*を指定した場合、*module*内の*name*を取得しま す。


.. method:: TestLoader.loadTestsFromNames(names[, module])

   :meth:`loadTestsFromName`と同じですが、名前を一つだけ指定するのでは なく、複数の名前のシーケンスを指定する事ができます。戻り値は
   *names*中の名前で指定されるテスト全てを含むテストスイートです。


.. method:: TestLoader.getTestCaseNames(testCaseClass)

   *testCaseClass*中の全てのメソッド名を含むソート済みシーケンスを返
   します。*testCaseClass*は:class:`TestCase`のサブクラスでなければな りません。

以下の属性は、サブクラス化またはインスタンスの属性値を変更し て:class:`TestLoader`をカスタマイズする場合に使用します。


.. attribute:: TestLoader.testMethodPrefix

   テストメソッドの名前と判断されるメソッド名の接頭語を示す文字列。デフォ ルト値は``'test'``です。

   この値は:meth:`getTestCaseNames`と全て の:meth:`loadTestsFrom\*`メソッドに影響を与えます。


.. attribute:: TestLoader.sortTestMethodsUsing

   :meth:`getTestCaseNames`および全て の:meth:`loadTestsFrom\*`メソッドでメソッド名をソートする際に使用する比較関
   数。デフォルト値は組み込み関数:func:`cmp`です。ソートを行なわないように この属性に:const:`None`を指定することもできます。


.. attribute:: TestLoader.suiteClass

   テストのリストからテストスイートを構築する呼び出し可能オブジェクト。メ ソッドを持つ必要はありません。デフォルト値は:class:`TestSuite`です。

   この値は全ての:meth:`loadTestsFrom\*`メソッドに影響を与えます。

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

