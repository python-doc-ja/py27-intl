
:mod:`xml.sax.handler` --- SAX ハンドラの基底クラス
===================================================

.. module:: xml.sax.handler
   :synopsis: SAX イベント・ハンドラの基底クラス
.. moduleauthor:: Lars Marius Garshol <larsga@garshol.priv.no>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>


.. versionadded:: 2.0

SAX API はコンテント・ハンドラ、DTD ハンドラ、エラー・ハンドラ、エンティ ティ・リゾルバという4つのハンドラを規定しています。通常アプリケーショ
ン側で実装する必要があるのは、これらのハンドラが発生させるイベントのう ち、処理したいものへのインターフェースだけです。インターフェースは1つ
のオブジェクトにまとめることも、複数のオブジェクトに分けることも可能で す。ハンドラはすべてのメソッドがデフォルトで実装されるように、
:mod:`xml.sax.handler` で提供される基底クラスを継承しなくてはなりません。


.. class:: ContentHandler

   アプリケーションにとって最も重要なメインの SAX コールバック・インター フェースです。このインターフェースで発生するイベントの順序はドキュメ
   ント内の情報の順序を反映しています。


.. class:: DTDHandler

   DTD イベントのハンドラです。

   未構文解析エンティティや属性など、パースに必要な DTD イベントの抽出 だけをおこなうインターフェースです。


.. class:: EntityResolver

   エンティティ解決用の基本インターフェースです。このインターフェースを 実装したオブジェクトを作成しパーサに登録することで、パーサはすべての
   外部エンティティを解決するメソッドを呼び出すようになります。


.. class:: ErrorHandler

   エラーや警告メッセージをアプリケーションに通知するためにパーサが使用 するインターフェースです。このオブジェクトのメソッドが、エラーをただ
   ちに例外に変換するか、あるいは別の方法で処理するかの制御をしています。

これらのクラスに加え、:mod:`xml.sax.handler` は機能やプロパティ名の シンボル定数を提供しています。


.. data:: feature_namespaces

   値: ``"http://xml.org/sax/features/namespaces"`` ---  true: 名前空間の処理を有効にする。 ---
   false: オプションで名前空間の処理を無効にする (暗黙に namespace-prefixes も無効にする - デフォルト )。 ---  アクセス:
   (パース時) リードオンリー; (パース時以外) 読み書き可


.. data:: feature_namespace_prefixes

   値: ``"http://xml.org/sax/features/namespace-prefixes"`` ---  true:
   名前空間宣言で用いられているオリジナルのプリフィックス名と属性 を通知する。 ---  false: 名前空間宣言で用いられている属性を通知しない。
   オプションでオリジナルのプリフィックス名も通知しない(デフォルト)。 ---  アクセス: (パース時) リードオンリー; (パース時以外) 読み書き可


.. data:: feature_string_interning

   値: ``"http://xml.org/sax/features/string-interning"`` ---  true:
   すべての要素名、プリフィックス、属性、名前、名前空間、URI、 ローカル名を組込みの intern 関数を使ってシンボルに登録する。 ---  false:
   名前のすべてを必ずしもシンボルに登録しない(デフォルト)。 ---  アクセス: (パース時) リードオンリー; (パース時以外) 読み書き可


.. data:: feature_validation

   値: ``"http://xml.org/sax/features/validation"`` ---  true:
   すべての妥当性検査エラーを通知する(external-general-entities  とexternal-parameter-entities
   が暗黙の前提になっている)。 ---  false: 妥当性検査エラーを通知しない。 ---  アクセス: (パース時) リードオンリー; (パース時以外)
   読み書き可


.. data:: feature_external_ges

   値: ``"http://xml.org/sax/features/external-general-entities"`` ---  true:
   外部一般(テキスト)エンティティの取り込みをおこなう。 ---  false: 外部一般エンティティを取り込まない。 ---  アクセス: (パース時)
   リードオンリー; (パース時以外) 読み書き可


.. data:: feature_external_pes

   値: ``"http://xml.org/sax/features/external-parameter-entities"`` ---  true: 外部
   DTD サブセットを含むすべての外部パラメータ・エンティティ の取り込みをおこなう。 ---  false: 外部パラーメタ・エンティティおよび外部 DTD
   サブセットを取り込 まない。 ---  アクセス: (パース時) リードオンリー; (パース時以外) 読み書き可


.. data:: all_features

   すべての機能の一覧。


.. data:: property_lexical_handler

   値: ``"http://xml.org/sax/properties/lexical-handler"`` ---  data type:
   xml.sax.sax2lib.LexicalHandler (Python 2 では未サポート) ---  description:
   コメントなど字句解析イベント用のオプション拡張ハンドラ。 ---  アクセス: 読み書き可


.. data:: property_declaration_handler

   Value: ``"http://xml.org/sax/properties/declaration-handler"`` ---  data type:
   xml.sax.sax2lib.DeclHandler (Python 2 では未サポート) ---  description:
   ノーテーションや未解析エンティティをのぞく DTD 関連イベン ト用のオプション拡張ハンドラ。 ---  access: read/write


.. data:: property_dom_node

   Value: ``"http://xml.org/sax/properties/dom-node"`` ---  data type:
   org.w3c.dom.Node (Python 2 では未サポート)  ---  description: パース時は DOM イテレータにおけるカレント
   DOM ノード、 非パース時はルート DOM ノードを指す。 ---  アクセス: (パース時) リードオンリー; (パース時以外) 読み書き可


.. data:: property_xml_string

   値: ``"http://xml.org/sax/properties/xml-string"`` ---  データ型: 文字列 ---  説明:
   カレント・イベントの元になったリテラル文字列 ---  アクセス: リードオンリー


.. data:: all_properties

   既知のプロパティ名の全リスト。


.. _content-handler-objects:

ContentHandler オブジェクト
---------------------------

:class:`ContentHandler` はアプリケーション側でサブクラス化して利用する
ことが前提になっています。パーサは入力ドキュメントのイベントにより、そ れぞれに対応する以下のメソッドを呼び出します。


.. method:: ContentHandler.setDocumentLocator(locator)

   アプリケーションにドキュメント・イベントの発生位置を通知するためにパー サから呼び出されます。

   SAX パーサによるロケータの提供は強く推奨されています(必須ではありま せん)。もし提供する場合は、DocumentHandler インターフェースのどのメ
   ソッドよりも先にこのメソッドが呼び出されるようにしなければなりません。

   アプリケーションはパーサがエラーを通知しない場合でもロケータによって、 すべてのドキュメント関連イベントの終了位置を知ることが可能になります。
   典型的な利用方法としては、アプリケーション側でこの情報を使い独自のエ ラーを発生させること(文字コンテンツがアプリケーション側で決めた規則
   に沿っていない場合等)があげられます。しかしロケータが返す情報は検索 エンジンなどで利用するものとしてはおそらく不充分でしょう。

   ロケータが正しい情報を返すのは、インターフェースからイベントの呼出し が実行されている間だけです。それ以外のときは使用すべきでありません。


.. method:: ContentHandler.startDocument()

   ドキュメントの開始通知を受け取ります。

   SAX パーサはこのインターフェースやDTDHandler のどのメソッド
   (:meth:`setDocumentLocator`を除く)よりも先にこのメソッドを一度だ け呼び出します。


.. method:: ContentHandler.endDocument()

   ドキュメントの終了通知を受け取ります。

   SAX パーサはこのメソッドを一度だけ、パース過程の最後に呼び出します。 パーサは(回復不能なエラーで)パース処理を中断するか、あるいは入力の
   最後に到達するまでこのメソッドを呼び出しません。


.. method:: ContentHandler.startPrefixMapping(prefix, uri)

   プリフィックスと URI の名前空間の関連付けを開始します。

   このイベントから返る情報は通常の名前空間処理では使われません。SAX XML リーダは ``feature_namespaces``
   機能が有効になっている場合(デ フォルト)、要素と属性名のプリフィックスを自動的に置換するようになっ ています。

   しかしアプリケーション側でプリフィックスを文字データや属性値の中で扱 う必要が生じることもあります。この場合プリフィックスの自動展開は保証
   されないため、必要に応じ :meth:`startPrefixMapping` や  :meth:`endPrefixMapping`
   イベントからアプリケーションに提供される 情報を用いてプリフィックスの展開をおこないます。

   .. % % XXX This is not really the default, is it? MvL

   :meth:`startPrefixMapping` と :meth:`endPrefixMapping` イベン
   トは相互に正しい入れ子関係になることが保証されていないので注意が必要 です。すべての :meth:`startPrefixMapping` は対応する
   :meth:`startElement` の前に発生し、:meth:`endPrefixMapping` イ ベントは対応する
   :meth:`endElement` の後で発生しますが、その順序 は保証されていません。


.. method:: ContentHandler.endPrefixMapping(prefix)

   プリフィックスと URI の名前空間の関連付けを終了します。

   詳しくは :meth:`startPrefixMapping` を参照してください。このイベ ントは常に対応する :meth:`endElement`
   の後で発生しますが、複数の  :meth:`endPrefixMapping` イベントの順序は特に保証されません。


.. method:: ContentHandler.startElement(name, attrs)

   非名前空間モードで要素の開始を通知します。

   *name* パラーメータには要素型の raw XML 1.0名を文字列として、 *attrs* パラメータには要素の属性を保持する
   :class:`Attributes` インターフェース (XXX reference: attributes-objects.html)
   オブジェクトをそれぞれ指定します。*attrs* として渡されたオブジェ クトはパーサで再利用することも可能ですが、属性のコピーを保持するた
   めにこれを参照し続けるのは確実な方法ではありません。属性のコピーを保 持したいときは *attrs* オブジェクトの :meth:`copy` メソッドを
   用いてください。


.. method:: ContentHandler.endElement(name)

   非名前空間モードで要素の終了を通知します。

   *name* パラメータには :meth:`startElement` イベント同様の要素 型名を指定します。


.. method:: ContentHandler.startElementNS(name, qname, attrs)

   名前空間モードで要素の開始を通知します。

   *name* パラーメータには要素型を ``(uri, localname)`` のタプルとして、*qname* パラメータにはソース・
   ドキュメントで用いられている raw XML 1.0名、*attrs* には要素の属 性を保持する :class:`AttributesNS` インターフェース
   (XXX reference: attributes-ns-objects.html) のインスタンスをそれぞれ指定します。要
   素に関連付けられた名前空間がないときは、*name* コンポーネントの  *uri* が ``None`` になります。*attrs* として渡されたオブジェ
   クトはパーサで再利用することも可能ですが、属性のコピーを保持するた めにこれを参照し続けるのは確実な方法ではありません。属性のコピーを保 持したいときは
   *attrs* オブジェクトの :meth:`copy` メソッドを 用いてください。

   ``feature_namespace_prefixes`` 機能が有効になっていなければ、パー サで *qname* を ``None``
   にセットすることも可能です。


.. method:: ContentHandler.endElementNS(name, qname)

   非名前空間モードで要素の終了を通知します。

   *name* パラメータには :meth:`startElementNS` イベント同様の要素 型を指定します。*qname* パラメータも同じです。


.. method:: ContentHandler.characters(content)

   文字データの通知を受け取ります。

   パーサは文字データのチャンクごとにこのメソッドを呼び出して通知します。 SAX パーサは一連の文字データを単一のチャンクとして返す場合と複数のチャ
   ンクに分けて返す場合がありますが、ロケータの情報が正しく保たれるよう に、一つのイベントの文字データは常に同じ外部エンティティのものでなけ ればなりません。

   *content* はユニコード文字列、バイト文字列のどちらでもかまいませ んが、``expat`` リーダ・モジュールは常にユニコード文字列を生成す
   るようになっています。

   .. note::

      Python XML SIG が提供していた初期 SAX 1 では、このメソッドにもっ と JAVA 風のインターフェースが用いられています。しかし
      Python で採用 されている大半のパーサでは古いインターフェースを有効に使うことができ ないため、よりシンプルなものに変更されました。古いコードを新しいイン
      ターフェースに変更するには、古い *offset* と *length* パラメー タでスライスせずに、*content* を指定するようにしてください。


.. method:: ContentHandler.ignorableWhitespace(whitespace)

   要素コンテンツに含まれる無視可能な空白文字の通知を受け取ります。

   妥当性検査をおこなうパーサは無視可能な空白文字(W3C XML 1.0 勧告のセ クション 2.10 参照)のチャンクごとに、このメソッドを使って通知しなけ
   ればなりません。妥当性検査をしないパーサもコンテンツモデルの利用とパー スが可能な場合、このメソッドを利用することが可能です。

   SAX パーサは一連の空白文字を単一のチャンクとして返す場合と複数のチャ ンクに分けて返す場合がありますが、ロケータの情報が正しく保たれるよう
   に、一つのイベントの文字データは常に同じ外部エンティティのものでなけ ればなりません。


.. method:: ContentHandler.processingInstruction(target, data)

   処理命令の通知を受け取ります。

   パーサは処理命令が見つかるたびにこのメソッドを呼び出します。処理命令 はメインのドキュメント要素の前や後にも発生することがあるので注意して ください。

   SAX パーサがこのメソッドを使って XML 宣言(XML 1.0 のセクション 2.8)や テキスト宣言(XML 1.0 のセクション
   4.3.1)の通知をすることはありません。


.. method:: ContentHandler.skippedEntity(name)

   スキップしたエンティティの通知を受け取ります。

   パーサはエンティティをスキップするたびにこのメソッドを呼び出します。 妥当性検査をしないプロセッサは(外部 DTD サブセットで宣言されているな
   どの理由で)宣言が見当たらないエンティティをスキップします。すべての プロセッサは ``feature_external_ges`` および
   ``feature_external_pes`` 属性の値によっては外部エンティティをスキッ プすることがあります。


.. _dtd-handler-objects:

DTDHandler オブジェクト
-----------------------

:class:`DTDHandler` インスタンスは以下のメソッドを提供します。


.. method:: DTDHandler.notationDecl(name, publicId, systemId)

   表記法宣言イベントの通知を捕捉します。


.. method:: DTDHandler.unparsedEntityDecl(name, publicId, systemId, ndata)

   未構文解析エンティティ宣言イベントの通知を受け取ります Handle an unparsed entity declaration event.


.. _entity-resolver-objects:

EntityResolver オブジェクト
---------------------------


.. method:: EntityResolver.resolveEntity(publicId, systemId)

   エンティティのシステム識別子を解決し、文字列として読み込んだシステム 識別子あるいは InputSource オブジェクトのいずれかを返します。デフォ
   ルトの実装では *systemId* を返します。


.. _sax-error-handler:

ErrorHandler オブジェクト
-------------------------

このインターフェースのオブジェクトは :class:`XMLReader` からのエラーや
警告の情報を受け取るために使われます。このインターフェースを実装したオ ブジェクトを作成し :class:`XMLReader`
に登録すると、パーサは警告やエラー の通知のためにそのオブジェクトのメソッドを呼び出すようになります。エラー
には警告、回復可能エラー、回復不能エラーの3段階があります。すべてのメ ソッドは :exc:`SAXParseException`
だけをパラメータとして受け取り ます。受け取った例外オブジェクトを raise することで、エラーや警告は例 外に変換されることもあります。


.. method:: ErrorHandler.error(exception)

   パーサが回復可能なエラーを検知すると呼び出されます。このメソッドが例 外を raise しないとパースは継続されますが、アプリケーション側では
   エラー以降のドキュメント情報を期待していないこともあります。パー サが処理を継続した場合、入力ドキュメント内のほかのエラーを見つけるこ とができます。


.. method:: ErrorHandler.fatalError(exception)

   パーサが回復不能なエラーを検知すると呼び出されます。このメソッドが return した後、すぐにパースを停止することが求められています。


.. method:: ErrorHandler.warning(exception)

   パーサが軽微な警告情報をアプリケーションに通知するために呼び出されま す。このメソッドが return した後もパースを継続し、ドキュメント情報を
   アプリケーションに送り続けるよう求められています。このメソッドで例外 を発生させた場合、パースは中断されてしまいます。

