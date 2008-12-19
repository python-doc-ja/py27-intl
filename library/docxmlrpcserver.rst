
:mod:`DocXMLRPCServer` --- セルフ-ドキュメンティング XML-RPC サーバ
===================================================================

.. module:: DocXMLRPCServer
   :synopsis: セルフ-ドキュメンティング XML-RPC サーバの実装。
.. moduleauthor:: Brian Quinlan <brianq@activestate.com>
.. sectionauthor:: Brian Quinlan <brianq@activestate.com>


.. versionadded:: 2.3

:mod:`DocXMLRPCServer` モジュールは :mod:`SimpleXMLRPCServer` クラ スを拡張し、HTTP GET
リクエストに対し HTML ドキュメントを返します。サー バは :class:`DocXMLRPCServer` を使ったスタンドアロン環境、
:class:`DocCGIXMLRPCRequestHandler` を使った CGI 環境の2つがあります。


.. class:: DocXMLRPCServer(addr[,  requestHandler[, logRequests]])

   当たなサーバ・インスタンスを生成します。各パラメータの内容は :class:`SimpleXMLRPCServer.SimpleXMLRPCServer`
   のものと同じですが、 *requestHandler* のデフォルトは :class:`DocXMLRPCRequestHandler` に なっています。


.. class:: DocCGIXMLRPCRequestHandler()

   CGI環境に XMR-RPC リクエスト・ハンドラの新たなインスタンスを生成します。


.. class:: DocXMLRPCRequestHandler()

   リクエスト・ハンドラの新たなインスタンスを生成します。このリクエスト・ ハンドラは XML-RPC POST リクエスト、ドキュメントの GET、そして
   :class:`DocXMLRPCServer` コンストラクタに与えられた *logRequests*
   パラメータ設定を優先するため、ロギングの変更をサポートします。


.. _doc-xmlrpc-servers:

DocXMLRPCServer オブジェクト
----------------------------

:class:`DocXMLRPCServer` は :class:`SimpleXMLRPCServer.SimpleXMLRPCServer`
の派生クラスで、セルフ-  ドキュメンティングの手段と XML-RPC サーバ機能を提供します。HTTP POST  リクエストは XML-RPC
メソッドの呼び出しとして扱われます。HTTP GET リク エストは pydoc スタイルの HTML ドキュメント生成のリクエストとして扱わ
れます。これはサーバが自分自身のドキュメントを Web ベースで提供可能で あることを意味します。


.. method:: DocXMLRPCServer.set_server_title(server_title)

   生成する HTML ドキュメントのタイトルをセットします。このタイトルは HTML の title 要素として使われます。


.. method:: DocXMLRPCServer.set_server_name(server_name)

   生成する HTML ドキュメントの名前をセットします。この名前は HTML 冒頭の h1 要素に使われます。


.. method:: DocXMLRPCServer.set_server_documentation(server_documentation)

   生成する HTML ドキュメントの本文をセットします。この本文は ドキュメント中の名前の下にパラグラフとして出力されます。


DocCGIXMLRPCRequestHandler
--------------------------

:class:`DocCGIXMLRPCRequestHandler` は
:class:`SimpleXMLRPCServer.CGIXMLRPCRequestHandler` の派生クラスで、セ ルフ- ドキュメンティングの手段と
XML-RPC CGI スクリプト機能を提供しま す。HTTP POST リクエストは XML-RCP メソッドの呼び出しとして扱われます。 HTTP GET
リクエストは pydoc スタイルの HTML ドキュメント生成のリクエス トとして扱われます。これはサーバが自分自身のドキュメントを Web ベース
で提供可能であることを意味します。


.. method:: DocCGIXMLRPCRequestHandler.set_server_title(server_title)

   生成する HTML ドキュメントのタイトルをセットします。このタイトルは HTML の title 要素として使われます。


.. method:: DocCGIXMLRPCRequestHandler.set_server_name(server_name)

   生成する HTML ドキュメントの名前をセットします。この名前は HTML 冒頭の h1 要素に使われます。


.. method:: DocCGIXMLRPCRequestHandler.set_server_documentation(server_documentation)

   生成する HTML ドキュメントの本文をセットします。この本文は ドキュメント中の名前の下にパラグラフとして出力されます。

