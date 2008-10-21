
:mod:`pprint` --- データ出力の整然化
====================================

.. module:: pprint
   :synopsis: Data pretty printer.
.. moduleauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


:mod:`pprint`モジュールを使うと、Pythonの任意のデータ構造をインタープ リタへの入力で使われる形式にして"pretty-print"できます。
フォーマット化された構造の中にPythonの基本的なタイプではないオブジェクト があるなら、表示できないかもしれません。
Pythonの定数として表現できない多くの組み込みオブジェクトと同様、ファイ ル、ソケット、クラスあるいはインスタンスのようなオブジェクトが含まれてい
た場合は出力できません。

可能であればオブジェクトをフォーマット化して1行に出力しますが、与えられ た幅に合わないなら複数行に分けて出力します。
無理に幅を設定したいなら、:class:`PrettyPrinter`オブジェクトを作成して明 示してください。

.. versionchanged:: 2.5
   辞書は出力を計算する前にキーでソートされます。 2.5以前では、辞書は1行以上必要な場合にのみソートされていましたが ドキュメントには書かれていませんでした。
   .

:mod:`pprint`モジュールには1つのクラスが定義されています：

.. % First the implementation class:


.. class:: PrettyPrinter(...)

   :class:`PrettyPrinter`インスタンスを作ります。 このコンストラクタにはいくつかのキーワードパラメータを設定できます。

   *stream*キーワードで出力ストリームを設定できます；このストリームに対 して呼び出されるメソッドはファイルプロトコルの:meth:`write`メソッドだ
   けです。 もし設定されなければ、:class:`PrettyPrinter`は``sys.stdout``を使用しま す。
   さらに3つのパラメータで出力フォーマットをコントロールできます。 そのキーワードは*indent*、*depth*と*width*です。

   再帰的なレベルごとに加えるインデントの量は*indent*で設定できます；デ フォルト値は1です。
   他の値にすると出力が少しおかしく見えますが、ネスト化されたところが見分け 易くなります。

   出力されるレベルは*depth*で設定できます； 出力されるデータ構造が深いなら、指定以上の深いレベルのものは``...``で 置き換えられて表示されます。
   デフォルトでは、オブジェクトの深さを制限しません。

   *width*パラメータを使うと、出力する幅を望みの文字数に設定できます； デフォルトでは80文字です。
   もし指定した幅にフォーマットできない場合は、できるだけ近づけます。 ::

      >>> import pprint, sys
      >>> stuff = sys.path[:]
      >>> stuff.insert(0, stuff[:])
      >>> pp = pprint.PrettyPrinter(indent=4)
      >>> pp.pprint(stuff)
      [   [   '',
              '/usr/local/lib/python1.5',
              '/usr/local/lib/python1.5/test',
              '/usr/local/lib/python1.5/sunos5',
              '/usr/local/lib/python1.5/sharedmodules',
              '/usr/local/lib/python1.5/tkinter'],
          '',
          '/usr/local/lib/python1.5',
          '/usr/local/lib/python1.5/test',
          '/usr/local/lib/python1.5/sunos5',
          '/usr/local/lib/python1.5/sharedmodules',
          '/usr/local/lib/python1.5/tkinter']
      >>>
      >>> import parser
      >>> tup = parser.ast2tuple(
      ...     parser.suite(open('pprint.py').read()))[1][1][1]
      >>> pp = pprint.PrettyPrinter(depth=6)
      >>> pp.pprint(tup)
      (266, (267, (307, (287, (288, (...))))))

:class:`PrettyPrinter`クラスにはいくつかの派生する関数が提供されていま す：

.. % Now the derivative functions:


.. function:: pformat(object[, indent[, width[, depth]]])

   *object*をフォーマット化して文字列として返します。
   *indent*、*width*と、*depth*は:class:`PrettyPrinter`コンス トラクタにフォーマット指定引数として渡されます。

   .. versionchanged:: 2.4
      引数 *indent*、 *width*と、*depth*が追加されました.


.. function:: pprint(object[, stream[, indent[, width[, depth]]]])

   *object*をフォーマット化して*stream*に出力し、最後に改行します。 *stream*が省略されたら、``sys.stdout``に出力します。
   これは対話型のインタープリタ上で、求める値を:keyword:`print`する代わりに 使用できます。
   *indent*、*width*と、*depth*は:class:`PrettyPrinter`コンス トラクタにフォーマット指定引数として渡されます。 ::

      >>> stuff = sys.path[:]
      >>> stuff.insert(0, stuff)
      >>> pprint.pprint(stuff)
      [<Recursion on list with id=869440>,
       '',
       '/usr/local/lib/python1.5',
       '/usr/local/lib/python1.5/test',
       '/usr/local/lib/python1.5/sunos5',
       '/usr/local/lib/python1.5/sharedmodules',
       '/usr/local/lib/python1.5/tkinter']

   .. versionchanged:: 2.4
      引数 *indent*、 *width*と、*depth*が追加さ れました.


.. function:: isreadable(object)

   .. index:: builtin: eval

   *object*をフォーマット化して出力できる（"readable"）か、あるいは :func:`eval`を使って値を再構成できるかを返しま す。
   再帰的なオブジェクトに対しては常にfalseを返します。 ::

      >>> pprint.isreadable(stuff)
      False


.. function:: isrecursive(object)

   *object*が再帰的な表現かどうかを返します。

さらにもう1つ、関数が定義されています：


.. function:: saferepr(object)

   *object*の文字列表現を、再帰的なデータ構造から保護した形式で返しま す。 もし*object*の文字列表現が再帰的な要素を持っているなら、再帰的な参照
   は``<Recursion on typename with id=number>``で表示されま す。 出力は他と違ってフォーマット化されません。

.. % This example is outside the {funcdesc} to keep it from running over
.. % the right margin.

::

   >>> pprint.saferepr(stuff)
   "[<Recursion on list with id=682968>, '', '/usr/local/lib/python1.5', '/usr/loca
   l/lib/python1.5/test', '/usr/local/lib/python1.5/sunos5', '/usr/local/lib/python
   1.5/sharedmodules', '/usr/local/lib/python1.5/tkinter']"


.. _prettyprinter objects:

PrettyPrinter オブジェクト
--------------------------

:class:`PrettyPrinter`インスタンスには以下のメソッドがあります：


.. method:: PrettyPrinter.pformat(object)

   *object*のフォーマット化した表現を返します。 これは:class:`PrettyPrinter`のコンストラクタに渡されたオプションを考慮し
   てフォーマット化されます。


.. method:: PrettyPrinter.pprint(object)

   *object*のフォーマット化した表現を指定したストリームに出力し、最後に 改行します。

以下のメソッドは、対応する同じ名前の関数と同じ機能を持っています。
以下のメソッドをインスタンスに対して使うと、新たに:class:`PrettyPrinter` オブジェクトを作る必要がないのでちょっぴり効果的です。


.. method:: PrettyPrinter.isreadable(object)

   .. index:: builtin: eval

   *object*をフォーマット化して出力できる（"readable"）か、あるいは :func:`eval`を使って値を再構成できるかを返しま す。
   これは再帰的なオブジェクトに対してfalseを返すことに注意して下さい。
   もし:class:`PrettyPrinter`の*depth*パラメータが設定されていて、オブ ジェクトのレベルが設定よりも深かったら、falseを返します。


.. method:: PrettyPrinter.isrecursive(object)

   オブジェクトが再帰的な表現かどうかを返します。

このメソッドをフックとして、サブクラスがオブジェクトを文字列に変換する方 法を修正するのが可能になっています。
デフォルトの実装では、内部で:func:`saferepr`を呼び出しています。


.. method:: PrettyPrinter.format(object, context, maxlevels, level)

   3つの値を返します：*object*をフォーマット化して文字列にしたもの、そ の結果が読み込み可能かどうかを示すフラグ、再帰が含まれているかどうかを示
   すフラグ。

   最初の引数は表示するオブジェクトです。 2つめの引数はオブジェクトの:func:`id`をキーとして含むディクショナリ
   で、オブジェクトを含んでいる現在の（直接、間接に*object*のコンテナと して表示に影響を与える）環境です。
   ディクショナリ*context*の中でどのオブジェクトが表示されたか表示する 必要があるなら、3つめの返り値はtrueになります。
   :meth:`format`メソッドの再帰呼び出しではこのディクショナリのコンテナ に対してさらにエントリを加えます。
   3つめの引数*maxlevels*で再帰呼び出しのレベルを設定します； もし制限しないなら、``0``にします。 この引数は再帰呼び出しでそのまま渡されます。
   4つめの引数*level*で現在のレベルを設定します； 再帰呼び出しでは、現在の呼び出しより小さい値が渡されます。

   .. versionadded:: 2.3

