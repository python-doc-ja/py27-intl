
:mod:`xml.etree.ElementTree` --- ElementTree XML API
====================================================

.. module:: xml.etree.ElementTree
   :synopsis: Implementation of the ElementTree API.
.. moduleauthor:: Fredrik Lundh <fredrik@pythonware.com>


.. versionadded:: 2.5

エレメント型は柔軟性のあるコンテナオブジェクトで、階層的データ構造をメモリーに格納するようにデザインされています。この型は言わばリストと辞書の\
間の子のようなものです。

各エレメントは関連する多くのプロパティを具えています:

* このエレメントがどういう種類のデータを表現しているかを同定する文字列であるタグ(別の言い方をすればエレメントの型)

* 幾つもの属性(Python 辞書に収められます)

* テキスト文字列

* オプションの末尾文字列

* 幾つもの子エレメント(Python シーケンスに収められます)

エレメントのインスタンスを作るには、Element や SubElement といったファクトリー関数を使います。

:class:`ElementTree` クラスはエレメントの構造を包み込み、それと XML を行き来するのに使えます。

この API の C 実装である :mod:`xml.etree.cElementTree` も使用可能です。

チュートリアルその他のドキュメントへのリンクについては
http://effbot.org/zone/element-index.htm を参照して下さい。
Fredrik Lundh　のページも xml.etree.ElementTree の開発バージョンの置き場所です。


.. _elementtree-functions:

関数
----


.. function:: Comment([text])

   コメント・エレメントのファクトリーです。このファクトリー関数は XML コメントにシリアライズされる特別な要素を作ります。コメント文字列は、8-bit
   ASCII 文字列でも Unicode 文字列でも構いません。 *text* はそのコメント文字列を含んだ文字列です。
   コメントを表わすエレメントのインスタンスを返します。


.. function:: dump(elem)

   エレメントの木もしくはエレメントの構造を sys.stdout に書き込みます。この関数はデバグ目的でだけ使用してください。

   出力される形式の正確なところは実装依存です。このバージョンでは、通常の XML ファイルとして書き込まれます。

   *elem* はエレメントの木もしくは個別のエレメントです。


.. function:: Element(tag[, attrib][, **extra])

   エレメントのファクトリー。この関数は標準エレメント・インタフェースを実装したオブジェクトを返します。このオブジェクトのクラスや型が正確に何であるかは
   実装に依存しますが、いつでもこのモジュールにある _ElementInterface クラスと互換性があります。

   エレメント名、アトリビュート名およびアトリビュート値は8-bit ASCII 文字列でも Unicode 文字列でも構いません。 *tag*
   はエレメント名です。 *attrib* はオプションの辞書で、エレメントのアトリビュートを含んでいます。 *extra*
   は追加のアトリビュートで、キーワード引数として与えられたものです。
   エレメント・インスタンスを返します。


.. function:: fromstring(text)

   文字列定数で与えられた XML 断片を構文解析します。XML 関数と同じです。 *text* は XML データを含んだ文字列です。
   Element インスタンス を返します。


.. function:: iselement(element)

   オブジェクトが正当なエレメント・オブジェクトであるかをチェックします。 *element* はエレメント・インスタンスです。
   引数がエレメント・オブジェクトならば真値を返します。


.. function:: iterparse(source[, events])

   XML 断片を構文解析してエレメントの木を漸増的に作っていき、その間進行状況をユーザーに報告します。 *source* は XML
   データを含むファイル名またはファイル風オブジェクト。 *events* は報告すべきイベントのリスト。省略された場合は "end" イベントだけが報告されます。
   ``(event, elem)`` ペアのイテレータ(:term:`iterator`)を返します。

   .. note::
      :func:`iterparse` は "start" イベントを送り出すとき\
      開始タグの ">" なる文字を見たことだけを保証しますので、
      アトリビュートは定義されますが、その時点ではテキストの内容も\
      テール・アトリビュートもまだ定義されていません。
      同じことは子エレメントにも言えて、その時点ではあるともないとも言えません。

      全部が揃ったエレメントが必要ならば、"end" イベントを探すようにして下さい。


.. function:: parse(source[, parser])

   XML 断片を構文解析してエレメントの木にしていきます。 *source* は XML データを含むファイル名またはファイル風オブジェクト。 *parser*
   はオプションの構文解析器インスタンスです。これが与えられない場合、標準の XMLTreeBuilder 構文解析器が使われます。
   ElementTree インスタンスを返します。


.. function:: ProcessingInstruction(target[, text])

   PI エレメントのファクトリー。このファクトリー関数は XML の処理命令(processing instruction)
   としてシリアライズされる特別なエレメントを作ります。 *target* は PI ターゲットを含んだ文字列です。 *text* は与えられるならば PI
   コンテンツを含んだ文字列です。
   PI を表わすエレメント・インスタンスを返します。


.. function:: SubElement(parent, tag[, attrib[, **extra]])

   部分エレメントのファクトリー。この関数はエレメント・インスタンスを作り、それを既存のエレメントに追加します。

   エレメント名、アトリビュート名およびアトリビュート値は 8-bit ASCII 文字列でも Unicode 文字列でも構いません。 *parent*
   は親エレメントです。 *tag* はエレメント名です。 *attrib* はオプションの辞書で、エレメントのアトリビュートを含んでいます。 *extra*
   は追加のアトリビュートで、キーワード引数として与えられたものです。
   エレメント・インスタンスを返します。


.. function:: tostring(element[, encoding])

   XML エレメントを全ての子エレメントを含めて表現する文字列を生成します。 *element* はエレメント・インスタンス。 *encoding*
   は出力エンコーディング(デフォルトは US-ASCII)です。
   XML データを含んだエンコードされた文字列を返します。


.. function:: XML(text)

   文字列定数で与えられた XML 断片を構文解析します。この関数は Python コードに「XML リテラル」を埋め込むのに使えます。 *text* は XML
   データを含んだ文字列です。
   エレメント・インスタンスを返します。


.. function:: XMLID(text)

   文字列定数で与えられた XML 断片を構文解析し、エレメント ID からエレメントへのマッピングを与える辞書も同時に返します。 *text* は XML
   データを含んだ文字列です。
   エレメント・インスタンスと辞書のタプルを返します。

.. _elementtree-element-interface:

Element インタフェース
----------------------

Element や SubElement が返す Element オブジェクトには以下のメソッドとアトリビュートがあります。

.. attribute:: Element.tag

   このエレメントが表すデータの種類を示す文字列です(言い替えるとエレメントの型です)。 

.. attribute:: Element.text

   *text* アトリビュートはエレメントに結びつけられた付加的なデータを保持するのに使われます。
   名前が示唆しているようにこのアトリビュートはたいてい文字列ですがアプリケーション固有のオブジェクトであって構いません。
   エレメントが XML ファイルから作られたものならば、このアトリビュートはエレメント・タグの間にあるテキストを丸ごと含みます。


.. attribute:: Element.tail

   *tail* アトリビュートはエレメントに結びつけられた付加的なデータを保持するのに使われます。
   このアトリビュートはたいてい文字列ですがアプリケーション固有のオブジェクトであって構いません。
   エレメントが XML ファイルから作られたものならば、このアトリビュートはエレメントの終了タグと次のタグの直前までの間に見つかったテキストを丸ごと含みます。


.. attribute:: Element.attrib

   エレメントのアトリビュートを保持する辞書です。
   次のことに注意しましょう。
   *attrib* は普通の書き換え可能な Python 辞書ではあるのですが、
   ElementTree の実装によっては別の内部表現を選択して要求されたときにだけ辞書を作るようにするかもしれません。
   そうした実装の利益を享受するために、可能な限り下記の辞書メソッドを通じて使いましょう。

以下の辞書風メソッドがエレメントのアトリビュートに対して働きます。

.. method:: Element.clear()

   エレメントをリセットします。全ての下部エレメントを削除し、アトリビュートをクリアし、
   テキストとテールのアトリビュートを ``None`` にセットします。


.. method:: Element.get(key[, default=None])

   エレメントの *key* という名前のアトリビュートを取得します。

   アトリビュートの値、またはアトリビュートがない場合は *default* を返します。


.. method:: Element.items()

   エレメントのアトリビュートを (名前, 値) ペアのシーケンスとして返します。
   返されるアトリビュートの順番は決まっていません。


.. method:: Element.keys()

   エレメントのアトリビュート名をリストとして返します。
   返される名前の順番は決まっていません。

.. method:: Element.set(key, value)

   エレメントのアトリビュート *key* に *value* をセットします。

以下のメソッドはエレメントの子(サブエレメント)に対して働きます。

.. method:: Element.append(subelement)

   エレメント *subelement* をこのエレメントの内部リストの最後に追加します。

.. method:: Element.find(match)

   *match* にマッチする最初のサブエレメントを探します。
   *match* はタグ名かパス(path)です。
   エレメント・インスタンスまたは ``None`` を返します。

.. method:: Element.findall(match)

   *match* にマッチする全てのサブエレメントを探します。
   *match* はタグ名かパス(path)です。
   マッチするエレメントの文書中での出現順に yield するイテレート可能オブジェクトを返します。

.. method:: Element.findtext(condition[, default=None])

   *condition* にマッチする最初のサブエレメントのテキストを探します。
   *condition* はタグ名かパスです。
   最初にマッチするエレメントのテキスト内容を返すか、エレメントが見あたらなかった場合
   *default* を返します。
   マッチしたエレメントにテキストがなければ空文字列が返されるので気を付けましょう。

.. method:: Element.getchildren()

   全てのサブエレメントを返します。エレメントは文書中での出現順に返されます。 

.. method:: Element.getiterator([tag=None])

   現在のエレメントを根とするツリーのイテレータを作ります。
   イテレータは現在のエレメントとそれ以下の全てのエレメントで与えられたタグにマッチするものについてイテレートします。
   タグが ``None`` または ``'*'`` の場合は全てのエレメントがイテレーションの対象です。
   エレメント・オブジェクトの文書中での出現順(深さ優先順)でのイテレート可能オブジェクトを返します。

.. method:: Element.insert(index, element)

   サブエレメントをこのエレメントの与えられた位置に挿入します。 

.. method:: Element.makeelement(tag, attrib)

   現在のエレメントと同じ型の新しいエレメント・オブジェクトを作ります。
   このメソッドは呼び出さずに、 SubElement ファクトリー関数を使って下さい。

.. method:: Element.remove(subelement)

   現在のエレメントから *subelement* を削除します。
   findXYZ メソッド群と違ってこのメソッドはエレメントをインスタンスの同一性で比較します。
   タグや内容では比較しません。

Element オブジェクトは以下のシーケンス型のメソッドをサブエレメントを操作するためにサポートします:  :meth:`__delitem__`, :meth:`__getitem__`, :meth:`__setitem__`,
:meth:`__len__` 。

要注意: Element オブジェクトでは :meth:`__nonzero__` メソッドを定義していないので、
サブエレメントのないエレメントは偽と判定されます。::
 
   element = root.find('foo')
 
   if not element: # careful!
       print "element not found, or element has no subelements"
 
   if element is None:
       print "element not found"


.. _elementtree-elementtree-objects:

ElementTree オブジェクト
------------------------


.. class:: ElementTree([element,] [file])

   ElementTree ラッパー・クラス。このクラスはエレメントの全階層を表現し、さらに標準 XML との相互変換を追加しています。

   *element* は根エレメントです。木はもし *file* が与えられればその XML の内容により初期化されます。


   .. method:: _setroot(element)

      この木の根エレメントを置き換えます。
      したがって現在の木の内容は破棄され、与えられたエレメントが代わりに使われます。
      注意して使ってください。 *element* はエレメント・インスタンスです。


   .. method:: find(path)

      子孫エレメントの中で与えられたタグを持つ最初のものを見つけます。
      getroot().find(path) と同じです。 *path*
      は探したいエレメントです。
      最初に条件に合ったエレメント、または見つからない時は ``None`` を返します。


   .. method:: findall(path)

      子孫エレメントの中で与えられたタグを持つものを全て見つけます。
      getroot().findall(path) と同じです。 *path*
      は探したいエレメントです。
      全ての条件に合ったエレメントのリストまたはイテレータ(:term:`iterator`)を返します、セクション順です。


   .. method:: findtext(path[, default])

      子孫エレメントの中で与えられたタグを持つ最初のもののテキストを見つけます。
      getroot().findtext(path) と同じです。 *path*
      は探したい直接の子エレメントです。
      *default* はエレメントが見つからなかった場合に返される値です。
      条件に合った最初のエレメントのテキスト、または見つからなかった場合にはデフォルト値を返します。
      もしエレメントが見つかったもののテキストがなかった場合には、このメソッドは空文字列を返す、ということに気をつけてください。


   .. method:: getiterator([tag])

      根エレメントに対する木を巡るイテレータを作ります。
      イテレータは木の全てのエレメントに渡ってセクション順にループします。
      *tag* は探したいタグです(デフォルトでは全てのエレメントを返します)。


   .. method:: getroot()

      この木の根エレメントを返します。


   .. method:: parse(source[, parser])

      外部の XML 断片をこのエレメントの木に読み込みます。
      *source* は XML データを含むファイル名またはファイル風オブジェクト。
      *parser* はオプションの構文解析器インスタンスです。
      これが与えられない場合、標準の XMLTreeBuilder 構文解析器が使われます。
      断片の根エレメントを返します。


   .. method:: write(file[, encoding])

      エレメントの木をファイルに XML として書き込みます。
      *file* はファイル名またはファイル風オブジェクトで書き込み用に開かれたもの。
      *encoding* [1]_ は出力エンコーディング(デフォルトは US-ASCII)です。


次に示すのがこれから操作する XML ファイルです::

    <html>
        <head>
            <title>Example page</title>
        </head>
        <body>
            <p>Moved to <a href="http://example.org/">example.org</a>
            or <a href="http://example.com/">example.com</a>.</p>
        </body>
    </html>

第1段落の全てのリンクの "target" アトリビュートを変更する例::

    >>> from xml.etree.ElementTree import ElementTree
    >>> tree = ElementTree()
    >>> tree.parse("index.xhtml")
    <Element html at b7d3f1ec>
    >>> p = tree.find("body/p")     # Finds first occurrence of tag p in body
    >>> p
    <Element p at 8416e0c>
    >>> links = p.getiterator("a")  # Returns list of all links
    >>> links
    [<Element a at b7d4f9ec>, <Element a at b7d4fb0c>]
    >>> for i in links:             # Iterates through all found links
    ...     i.attrib["target"] = "blank"
    >>> tree.write("output.xhtml")
 
.. _elementtree-qname-objects:

QName オブジェクト
------------------


.. class:: QName(text_or_uri[, tag])

   QName ラッパー。このクラスは QName アトリビュート値をラップし、出力時に真っ当な名前空間の扱いを得るために使われます。 *text_or_uri*
   は {uri}local という形式の QName 値を含む文字列、または tag 引数が与えられた場合には QName の URI 部分の文字列です。
   *tag* が与えられた場合、一つめの引数は URI と解釈され、この引数はローカル名と解釈されます。
   :class:`QName` インスタンスは不透明です。


.. _elementtree-treebuilder-objects:

TreeBuilder オブジェクト
------------------------


.. class:: TreeBuilder([element_factory])

   汎用のエレメント構造ビルダー。これは start、data、end のメソッド呼び出しの列を整形式のエレメント構造に変換します。このクラスを使うと、好みの
   XML 構文解析器、または他の XML に似た形式の構文解析器を使って、エレメント構造を作り出すことができます。 *element_factory*
   が与えられた場合には新しいエレメント・インスタンスを作る際にこれを呼び出します。


   .. method:: close()

      構文解析器のバッファをフラッシュし、最上位の文書エレメントを返します。
      Element インスタンスを返します。


   .. method:: data(data)

      現在のエレメントにテキストを追加します。 *data* は文字列です。
      8-bit ASCII 文字列もしくは Unicode 文字列でなければなりません。


   .. method:: end(tag)

      現在のエレメントを閉じます。 *tag* はエレメントの名前です。
      閉じられたエレメントを返します。


   .. method:: start(tag, attrs)

      新しいエレメントを開きます。 *tag* はエレメントの名前です。
      *attrs* はエレメントのアトリビュートを保持した辞書です。
      開かれたエレメントを返します。


.. _elementtree-xmltreebuilder-objects:

XMLTreeBuilder オブジェクト
---------------------------


.. class:: XMLTreeBuilder([html,] [target])

   XML ソースからエレメント構造を作るもので、expat 構文解析器に基づいています。 *html* は前もって定義された HTML
   エンティティです。このオプションは現在の実装ではサポートされていません。 *target* はターゲットとなるオブジェクトです。省略された場合、標準の
   TreeBuilder クラスのインスタンスが使われます。


   .. method:: close()

      構文解析器にデータを供給するのを終わりにします。
      エレメント構造を返します。


   .. method:: doctype(name, pubid, system)

      doctype 宣言を扱います。 *name* は doctype の名前です。
      *pubid* は公開識別子です。 *system* はシステム識別子です。


   .. method:: feed(data)

      構文解析器にデータを供給します。
      *data* はエンコードされたデータです。

:meth:`XMLTreeBuilder.feed` は *target* の :meth:`start` メソッドを\
それぞれの開始タグに対して呼び、また :meth:`end` メソッドを終了タグに対して呼び、
そしてデータは :meth:`data` メソッドで処理されます。
:meth:`XMLTreeBuilder.close` は *target* の :meth:`close` メソッドを呼びます。
:class:`XMLTreeBuilder` は木構造を構築する以外にも使えます。
以下の例は、XML ファイルの最高の深さを数えます::

    >>> from xml.etree.ElementTree import XMLTreeBuilder
    >>> class MaxDepth:                     # The target object of the parser
    ...     maxDepth = 0
    ...     depth = 0
    ...     def start(self, tag, attrib):   # Called for each opening tag.
    ...         self.depth += 1
    ...         if self.depth > self.maxDepth:
    ...             self.maxDepth = self.depth
    ...     def end(self, tag):             # Called for each closing tag.
    ...         self.depth -= 1
    ...     def data(self, data):
    ...         pass            # We do not need to do anything with data.
    ...     def close(self):    # Called when all data has been parsed.
    ...         return self.maxDepth
    ...
    >>> target = MaxDepth()
    >>> parser = XMLTreeBuilder(target=target)
    >>> exampleXml = """
    ... <a>
    ...   <b>
    ...   </b>
    ...   <b>
    ...     <c>
    ...       <d>
    ...       </d>
    ...     </c>
    ...   </b>
    ... </a>"""
    >>> parser.feed(exampleXml)
    >>> parser.close()
    4


.. rubric:: Footnotes

.. [#] XML の出力に含まれるエンコーディング文字列は適切な標準に\
   適合していなければなりません。
   たとえば、"UTF-8" は正当ですが、"UTF8" は違います。
   http://www.w3.org/TR/2006/REC-xml11-20060816/#NT-EncodingDecl
   と
   http://www.iana.org/assignments/character-sets
   を参照して下さい。
