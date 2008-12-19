
:mod:`xml.etree.ElementTree` --- ElementTree XML API
====================================================

.. module:: xml.etree.ElementTree
   :synopsis: Implementation of the ElementTree API.
.. moduleauthor:: Fredrik Lundh <fredrik@pythonware.com>


.. versionadded:: 2.5

エレメント型は柔軟性のあるコンテナオブジェクトで、階層的データ構造をメモ リーに格納するようにデザインされています。この型は言わばリストと辞書の
間の子のようなものです。

各エレメントは関連する多くのプロパティを具えています:

* このエレメントがどういう種類のデータを表現しているかを同定する 文字列であるタグ(別の言い方をすればエレメントの型)

* 幾つもの属性(Python 辞書に収められます)

* テキスト文字列

* オプションの末尾文字列

* 幾つもの子エレメント(Python シーケンスに収められます)

エレメントのインスタンスを作るには、Element や SubElement といったファクトリー 関数を使います。

:class:`ElementTree` クラスはエレメントの構造を包み込み、それと XML を行き来す るのに使えます。

この API の C 実装である :mod:`xml.etree.cElementTree` も使用可能です。


.. _elementtree-functions:

関数
----


.. function:: Comment([text])

   コメント・エレメントのファクトリーです。このファクトリー関数は XML コメントにシリアライズ される特別な要素を作ります。 コメント文字列は、8-bit
   ASCII 文字列でも Unicode 文字列でも構いません。 *text* はそのコメント文字列を含んだ文字列です。


   .. data:: 戻り値:
      :noindex:

      コメントを表わすエレメントのインスタンス。


.. function:: dump(elem)

   エレメントの木もしくはエレメントの構造を sys.stdout に書き込みます。この関数は デバグ目的でだけ使用してください。

   出力される形式の正確なところは実装依存です。このバージョンでは、 通常の XML ファイルとして書き込まれます。

   *elem* はエレメントの木もしくは個別のエレメントです。


.. function:: Element(tag[, attrib][, **extra])

   エレメントのファクトリー。この関数は標準エレメント・インタフェースを実装した オブジェクトを返します。このオブジェクトのクラスや型が正確に何であるかは
   実装に依存しますが、いつでもこのモジュールにある _ElementInterface クラスと 互換性があります。

   エレメント名、アトリビュート名およびアトリビュート値は8-bit ASCII 文字列でも Unicode 文字列でも構いません。 *tag*
   はエレメント名です。 *attrib* はオプションの辞書で、エレメントのアトリビュートを含んでいます。 *extra*
   は追加のアトリビュートで、キーワード引数として与えられたものです。


   .. data:: 戻り値:
      :noindex:

      エレメント・インスタンス。


.. function:: fromstring(text)

   文字列定数で与えられた XML 断片を構文解析します。XML 関数と同じです。 *text* は XML データを含んだ文字列です。


   .. data:: 戻り値:
      :noindex:

      エレメント・インスタンス。


.. function:: iselement(element)

   オブジェクトが正当なエレメント・オブジェクトであるかをチェックします。 *element* はエレメント・インスタンスです。


   .. data:: 戻り値:
      :noindex:

      引数がエレメント・オブジェクトならば真値。


.. function:: iterparse(source[, events])

   XML 断片を構文解析してエレメントの木を漸増的に作っていき、その間 進行状況をユーザーに報告します。 *source* は XML
   データを含むファイル名またはファイル風オブジェクト。 *events* は報告すべきイベントのリスト。省略された場合は "end" イベントだけが報告されます。


   .. data:: 戻り値:
      :noindex:

      (イベント, エレメント) イテレータ。


.. function:: parse(source[, parser])

   XML 断片を構文解析してエレメントの木にしていきます。 *source* は XML データを含むファイル名またはファイル風オブジェクト。 *parser*
   はオプションの構文解析器インスタンスです。これが与えられない場合、 標準の XMLTreeBuilder 構文解析器が使われます。


   .. data:: 戻り値:
      :noindex:

      ElementTree インスタンス。


.. function:: ProcessingInstruction(target[, text])

   PI エレメントのファクトリー。このファクトリー関数は XML の 処理命令(processing instruction)
   としてシリアライズされる特別なエレメントを作ります。 *target* は PI ターゲットを含んだ文字列です。 *text* は与えられるならば PI
   コンテンツを含んだ文字列です。


   .. data:: 戻り値:
      :noindex:

      PI を表わすエレメント・インスタンス。


.. function:: SubElement(parent, tag[, attrib] [, **extra])

   部分エレメントのファクトリー。この関数はエレメント・インスタンスを作り、それを 既存のエレメントに追加します。

   エレメント名、アトリビュート名およびアトリビュート値は8-bit ASCII 文字列でも Unicode 文字列でも構いません。 *parent*
   は親エレメントです。 *tag* はエレメント名です。 *attrib* はオプションの辞書で、エレメントのアトリビュートを含んでいます。 *extra*
   は追加のアトリビュートで、キーワード引数として与えられたものです。


   .. data:: 戻り値:
      :noindex:

      エレメント・インスタンス。


.. function:: tostring(element[, encoding])

   XML エレメントを全ての子エレメントを含めて表現する文字列を生成します。 *element* はエレメント・インスタンス。 *encoding*
   は出力エンコーディング(デフォルトは US-ASCII)です。


   .. data:: 戻り値:
      :noindex:

      XML データを含んだエンコードされた文字列。


.. function:: XML(text)

   文字列定数で与えられた XML 断片を構文解析します。この関数は Python コードに 「XML リテラル」を埋め込むのに使えます。 *text* は XML
   データを含んだ文字列です。


   .. data:: 戻り値:
      :noindex:

      エレメント・インスタンス。


.. function:: XMLID(text)

   文字列定数で与えられた XML 断片を構文解析し、エレメント ID からエレメント へのマッピングを与える辞書も同時に返します。 *text* は XML
   データを含んだ文字列です。


   .. data:: 戻り値:
      :noindex:

      エレメント・インスタンスと辞書のタプル。


.. _elementtree-elementtree-objects:

ElementTree オブジェクト
------------------------


.. class:: ElementTree([element,] [file])

   ElementTree ラッパー・クラス。このクラスはエレメントの全階層を表現し、 さらに標準 XML との相互変換を追加しています。

   *element* は根エレメントです。 木はもし *file* が与えられればその XML の内容により初期化されます。


.. method:: ElementTree._setroot(element)

   この木の根エレメントを置き換えます。したがって現在の木の内容は破棄され、 与えられたエレメントが代わりに使われます。注意して使ってください。 *element*
   はエレメント・インスタンスです。


.. method:: ElementTree.find(path)

   子孫エレメントの中で与えられたタグを持つ最初のものを見つけます。 getroot().find(path) と同じです。 *path*
   は探したいエレメントです。


   .. data:: 戻り値:
      :noindex:

      最初に条件に合ったエレメント、または見つからない時は None。


.. method:: ElementTree.findall(path)

   子孫エレメントの中で与えられたタグを持つものを全て見つけます。 getroot().findall(path) と同じです。 *path*
   は探したいエレメントです。


   .. data:: 戻り値:
      :noindex:

      全ての条件に合ったエレメントのリストまたはイテレータで、セクション順です。


.. method:: ElementTree.findtext(path[, default])

   子孫エレメントの中で与えられたタグを持つ最初のもののテキストを見つけます。 getroot().findtext(path) と同じです。 *path*
   は探したい直接の子エレメントです。 *default* はエレメントが見つからなかった場合に返される値です。


   .. data:: 戻り値:
      :noindex:

      条件に合った最初のエレメントのテキスト、または見つからなかった場合にはデフォルト値。
      もしエレメントが見つかったもののテキストがなかった場合には、このメソッドは空文字列を返す、 ということに気をつけてください。


.. method:: ElementTree.getiterator([tag])

   根エレメントに対する木を巡るイテレータを作ります。イテレータは木の全てのエレメントに 渡ってセクション順にループします。 *tag*
   は探したいタグです(デフォルトでは全てのエレメントを返します)。


   .. data:: 戻り値:
      :noindex:

      イテレータ。


.. method:: ElementTree.getroot()

   この木の根エレメントを返します。


   .. data:: 戻り値:
      :noindex:

      エレメント・インスタンス。


.. method:: ElementTree.parse(source[, parser])

   外部の XML 断片をこのエレメントの木に読み込みます。 *source* は XML データを含むファイル名またはファイル風オブジェクト。 *parser*
   はオプションの構文解析器インスタンスです。これが与えられない場合、 標準の XMLTreeBuilder 構文解析器が使われます。


   .. data:: 戻り値:
      :noindex:

      断片の根エレメント。


.. method:: ElementTree.write(file[, encoding])

   エレメントの木をファイルに XML として書き込みます。 *file* はファイル名またはファイル風オブジェクトで書き込み用に開かれたもの。
   *encoding* は出力エンコーディング(デフォルトは US-ASCII)です。


.. _elementtree-qname-objects:

QName オブジェクト
------------------


.. class:: QName(text_or_uri[, tag])

   QName ラッパー。このクラスは QName アトリビュート値をラップし、出力時に 真っ当な名前空間の扱いを得るために使われます。 *text_or_uri*
   は {uri}local という形式の QName 値を含む文字列、 または tag 引数が与えられた場合には QName の URI 部分の文字列です。
   *tag* が与えられた場合、一つめの引数は URI と解釈され、この引数は ローカル名と解釈されます。


   .. data:: 戻り値:
      :noindex:

      QName を表わす不透明オブジェクト。


.. _elementtree-treebuilder-objects:

TreeBuilder オブジェクト
------------------------


.. class:: TreeBuilder([element_factory])

   汎用のエレメント構造ビルダー。 これは start、data、end のメソッド呼び出しの 列を整形式のエレメント構造に変換します。このクラスを使うと、 好みの
   XML 構文解析器、または他の XML に似た形式の構文解析器を使って、 エレメント構造を作り出すことができます。 *element_factory*
   が与えられた場合には新しいエレメント・インスタンスを 作る際にこれを呼び出します。


.. method:: TreeBuilder.close()

   構文解析器のバッファをフラッシュし、最上位の文書エレメントを返します。


   .. data:: 戻り値:
      :noindex:

      エレメント・インスタンス。


.. method:: TreeBuilder.data(data)

   現在のエレメントにテキストを追加します。 *data* は文字列です。8-bit ASCII 文字列もしくは Unicode 文字列でなければなりません。


.. method:: TreeBuilder.end(tag)

   現在のエレメントを閉じます。 *tag* はエレメントの名前です。


   .. data:: 戻り値:
      :noindex:

      閉じられたエレメント。


.. method:: TreeBuilder.start(tag, attrs)

   新しいエレメントを開きます。 *tag* はエレメントの名前です。 *attrs* はエレメントのアトリビュートを保持した辞書です。


   .. data:: 戻り値:
      :noindex:

      開かれたエレメント。


.. _elementtree-xmltreebuilder-objects:

XMLTreeBuilder オブジェクト
---------------------------


.. class:: XMLTreeBuilder([html,] [target])

   XML ソースからエレメント構造を作るもので、expat 構文解析器に基づいています。 *html* は前もって定義された HTML
   エンティティです。このオプションは 現在の実装ではサポートされていません。 *target* はターゲットとなるオブジェクトです。省略された場合、標準の
   TreeBuilder クラスのインスタンスが使われます。


.. method:: XMLTreeBuilder.close()

   構文解析器にデータを供給するのを終わりにします。


   .. data:: 戻り値:
      :noindex:

      エレメント構造。


.. method:: XMLTreeBuilder.doctype(name, pubid, system)

   doctype 宣言を扱います。 *name* は doctype の名前です。 *pubid* は公開識別子です。 *system* はシステム識別子です。


.. method:: XMLTreeBuilder.feed(data)

   構文解析器にデータを供給します。

   *data* はエンコードされたデータです。

