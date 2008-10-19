====================================================
 urllib2 を利用したインターネットリソースの取得方法
====================================================
----------------------------
  Python による URL の取得
----------------------------


.. note::
    この HOWTO の以前のバージョンにはフランス語の翻訳版があり、
    以下から入手できます。`urllib2 - Le Manuel manquant 
    <http://www.voidspace/python/articles/urllib2_francais.shtml>`

.. contents:: urllib2 チュートリアル
 

紹介
============

.. sidebar:: 関連記事

    Python に関する以下の Web リソースに当たることは
    有用でしょう：   
    
    * `Basic Authentication <http://www.voidspace.org.uk/python/articles/authentication.shtml>`_

      	*ベーシック認証* のチュートリアルで、Python での例があります。
    
    この HOWTO は `Michael Foord
    <http://www.voidspace.org.uk/python/index.shtml>`_ によって書かれました。

**urllib2** は URL (Uniform Resource Locator) を取得するための
`Python <http://www.python.org>`_ モジュールです。これは *urlopen* 関数の形で
非常にシンプルなインターフェースを提供します。これは様々な異なるプロトコルを使って
URL を取得することができます。これはまた、よくある状況を処理するためのもう少し
複雑なインターフェースも提供します - ベーシック認証、クッキー、プロキシ
などのようなものです。これらは handler や opener と呼ばれるオブジェクトで
提供されています。

urllib2 はたくさんの "URL スキーム"（URL の ":" の前の文字列で
識別されます - 例えば "ftp" は "ftp://python.org/" の URL スキームで、
それらに関連づいたネットワークプロトコルを使用します（例.FTP、HTTP）。
このチュートリアルでは最も良くあるケース、HTTP にフォーカスします。

素直な状況では、 *urlopen* は非常に簡単に扱えます。しかし、
HTTP の URL を開く際にエラーや普通でないケースに遭遇した場合は、
HyperText Transfer Protocol についていくらか理解することが
必要でしょう。HTTP の最も包括的かつ信頼できるリファレンスは
:RFC:`2616` です。これはテクニカルなドキュメントであり、簡単に
読めることを意図していません。この HOWTO は あなたの助けに十分な HTTP の詳細を含む
*urllib2* の使用の概説を目指します。これは 
`urllib2 ドキュメント <http://docs.python.org/lib/module-urllib2.html>`_ の置き換えは
目指さず、補完となるものです。

URL の取得
=============

urllib2 の最もシンプルな使用例は以下です： ::

    import urllib2
    response = urllib2.urlopen('http://python.org/')
    html = response.read()

urllib2 の利用の大部分はこのようにシンプルなものです（'http:' URL の
代わりに 'ftp:'、'file:' なども使えるということに注目
してください）。しかし、このチュートリアルの目的は HTTP にフォーカスし、
もっと複雑なケースについて説明することです。

HTTP の基本はリクエストとレスポンスです - クライアントはリクエストを作り、
サーバはレスポンスを送ります。urllib2 は ``Request`` オブジェクトが
これを反映していて、作成している HTTP リクエストを表現しています。これの
最も単純な形は、取得したい URL を指定したリクエストオブジェクトを作成する
ことです。``urlopen`` をこのリクエストオブジェクトで呼ぶと、リクエストされた
URL に対するレスポンスオブジェクトが返ります。このレスポンスは file 類似（file-like）の
オブジェクトで、つまり例えばレスポンスに対して .read() が呼べることを意味します：
::

    import urllib2

    req = urllib2.Request('http://www.voidspace.org.uk')
    response = urllib2.urlopen(req)
    the_page = response.read()

urllib2 は同じ Request インターフェースで全ての URL スキームを処理できる
ことに注目してください。例えば、FTP リクエストも以下のような感じです： ::

    req = urllib2.Request('ftp://example.com/')

HTTP のケースでは、リクエストオブジェクトは追加で二つ出来ることが
あります：一つ目は、サーバに送信するデータを渡せます。
二つ目は、サーバに送るデータ、またはリクエストそのものに *関する*
追加情報（"メタデータ"）が渡せます - この情報は HTTP "ヘッダ" として
送られます。それぞれを順番に見ていきましょう。

データ
-------

URL に対してデータを送りたい（たいてい URL は CGI（Common Gateway Interface）
スクリプト [#]_ または web アプリケーションを参照します）ということが
しばしばあります。HTTP では、これは **POST** リクエストとして知られているものを
使って行います。これはあなたが HTML フォームに記入し、送信する際に
ブラウザが行っていることです。全ての POST がフォームからくるわけでは
ありません：任意のデータをあなたのアプリケーションに送信する場合にも
POST は使えます。通常の HTML フォームのケースでは、データは標準的な方法で
エンコードされる必要があり、Request オブジェクトに ``data`` 引数として
引き渡されます。エンコーディングは ``urllib2`` でなく ``urllib`` ライブラリの
関数を使って行われます。 ::

    import urllib
    import urllib2  

    url = 'http://www.someserver.com/cgi-bin/register.cgi'
    values = {'name' : 'Michael Foord',
              'location' : 'Northampton',
              'language' : 'Python' }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

他のエンコーディングが必要な場合もあることに注意してください（例. HTML
フォームからのファイルアップロード - 詳しくは
`HTML Specification, Form Submission <http://www.w3.org/TR/REC-html40/interact/forms.html#h-17.13>`_
を参照してください）。

``data`` 引数を渡さなければ、urllib2 は **GET** リクエストを
使用します。GET と POST リクエストが異なる一つは、 POST リクエストが
しばしば "副作用" を持つことです：これは何らかの形でシステムの状態を
変更します（例えばウェブサイトで 100 ポンドの缶詰めスパムを注文して
ドアの前まで配達してもらうとか）。
HTTP 標準では明確に POST が *常に* 副作用を起こすことを意図するとし、
GET は *決して* 副作用を起こさないとしていますが、
GET リクエストが副作用を起こすことを阻むものは何もありませんし、
POST リクエストが副作用を起こさないことを阻むものも何もありません。データは、
URL そのものにエンコードしてしまうことで HTTP の GET リクエストでも渡すことが可能です。

これは以下のように行われます::

    >>> import urllib2
    >>> import urllib
    >>> data = {}
    >>> data['name'] = 'Somebody Here'
    >>> data['location'] = 'Northampton'
    >>> data['language'] = 'Python'
    >>> url_values = urllib.urlencode(data)
    >>> print url_values
    name=Somebody+Here&language=Python&location=Northampton
    >>> url = 'http://www.example.com/example.cgi'
    >>> full_url = url + '?' + url_values
    >>> data = urllib2.open(full_url)

URL 全体は、URL に対してエンコードされた値が続く ``?`` を加えることで
作成されることに注目してください。


ヘッダ
-------

ここでは、HTTP リクエストにヘッダを追加するやり方を説明するために
特定の HTTP ヘッダについて論じていきましょう。

いくつかのウェブサイト [#]_ はプログラムから閲覧されることを嫌ったり、または
異なるブラウザ [#]_ には異なるバージョンを送ったりします。デフォルトでは、 urllib2 は
それ自身を ``Python-urllib/x.y`` (``x`` と ``y`` は 
Python リリースのメジャーおよびマイナーバージョンです。
例. ``Python-urllib/2.5``) と宣言しますが、これではサイトが混乱したり、または単に
動作しないかも知れません。ブラウザは、自身を ``User-Agent`` ヘッダを
通じて宣言しています [#]_ 。Request オブジェクトを作成する時に、
ヘッダの辞書を含めることができます。以下の例は上記と同じリクエストを
作成しますが、自身を Internet Explorer のバージョンであるとしてします [#]_ 。::

    import urllib
    import urllib2  
    
    url = 'http://www.someserver.com/cgi-bin/register.cgi'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
    values = {'name' : 'Michael Foord',
              'location' : 'Northampton',
              'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()

レスポンスには 2 つの便利なメソッドもあります。エラーの時に
何が起こるかについて見た後にある `info と geturl`_ セクションを参照してください。


例外の処理
===================

*urlopen* は、レスポンスが処理できないと ``URLError`` を送出します（通常の
Python API と同様に、ValueError、
TypeError なども送出されます）。

``HTTPError`` は ``URLError`` のサブクラスで、HTTP URL の特定の
ケースにおいて送出されます。

URLError
--------

しばしば、URLError はネットワーク接続がない（指定した
サーバに到達できない）、または指定したサーバが存在しない時に送出されます。
このケースでは、送出された例外は 'reason' 属性を持ち、
これはエラーコードと、テキストのエラーメッセージを含むタプルです。

例 ::

    >>> req = urllib2.Request('http://www.pretend_server.org')
    >>> try: urllib2.urlopen(req)
    >>> except URLError, e:
    >>>    print e.reason
    >>>
    (4, 'getaddrinfo failed')


HTTPError
---------

サーバからの HTTP レスポンスは全て数字の "ステータス
コード" を含んでいます。ステータスコードは、サーバがリクエストに
応えられないということをしばしば示します。デフォルトのハンドラは、これらのレスポンスの
いくつかを処理します（例えば、レスポンスが "redirection" の場合、
これはクライアントに別の URL からドキュメントを取得するように求めるものですが、
urllib2 はこれを処理してくれます）。処理できない場合には、urlopen は
``HTTPError`` を送出します。典型的なエラーには '404'(ページが見つからない)、
'403'(リクエスト禁止)、'401'(認証が
必要)があります。

全ての HTTP エラーコードのリファレンスには、RFC 2616 の
セクション 10 を参照してください。

送出される ``HTTPError`` インスタンスには整数の 'code' 
属性があり、これがサーバから送られたエラーに対応します。

エラーコード
~~~~~~~~~~~~~~

デフォルトのハンドラがリダイレクト (300 番台のコード) を処理し、
100-200 番台のコードは成功を示しますので、通常は
400-599 台のエラーコードだけを見ることでしょう。

``BaseHTTPServer.BaseHTTPRequestHandler.responses`` はレスポンスコードの
便利な辞書で、この中には RFC 2616 で使われている全てのレスポンスコードが
あります。便利のため、ここに辞書を再生成しておきます ::

    # レスポンスコードとメッセージの対応表；エントリは
    # {code: (短いメッセージ、長いメッセージ)} の形式です。
    responses = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols',
              'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted',
              'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices',
              'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified',
              'Document has not changed since given time'),
        305: ('Use Proxy',
              'You must use proxy specified in Location to access this '
              'resource.'),
        307: ('Temporary Redirect',
              'Object moved temporarily -- see URI list'),

        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        401: ('Unauthorized',
              'No permission -- see authorization schemes'),
        402: ('Payment Required',
              'No payment -- see charging schemes'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this server.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
              'this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
              'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
              'Cannot satisfy request range.'),
        417: ('Expectation Failed',
              'Expect condition could not be satisfied.'),

        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented',
              'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable',
              'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout',
              'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
        }

エラーが送出されると、サーバは HTTP エラー 、 *加えて* エラーページ
を返して応答します。 ``HTTPError`` インスタンスは、返されたページの
レスポンスとすることができます。これは、code 属性と共に、
read、geturl、info メソッドも持つことを意味します ::

    >>> req = urllib2.Request('http://www.python.org/fish.html')
    >>> try: 
    >>>     urllib2.urlopen(req)
    >>> except URLError, e:
    >>>     print e.code
    >>>     print e.read()
    >>> 
    404
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" 
        "http://www.w3.org/TR/html4/loose.dtd">
    <?xml-stylesheet href="./css/ht2html.css" 
        type="text/css"?>
    <html><head><title>Error 404: File Not Found</title> 
    ...... etc...

まとめ
--------------

``HTTPError`` *または* ``URLError`` に対する準備ができたら、
2 つの基本的なアプローチがあります。私は 2 番目のアプローチが好きですね。

1 番目
~~~~~~~~~~~~~~

::


    from urllib2 import Request, urlopen, URLError, HTTPError
    req = Request(someurl)
    try:
        response = urlopen(req)
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except URLError, e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    else:
        # everything is fine


.. note::
    ``except HTTPError`` は最初にくる *必要があります* 。でなければ、 ``except URLError`` が
    ``HTTPError`` *も* キャッチしてしまうでしょう。

2 番目
~~~~~~~~

::

    from urllib2 import Request, urlopen, URLError
    req = Request(someurl)
    try:
        response = urlopen(req)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        # everything is fine
        

info と geturl
===============

urlopen によって返されるレスポンス (または ``HTTPError`` インスタンス) は
2 つの便利なメソッド ``info`` と ``geturl`` を持ちます。

**geturl** - これは取得したページの実際の URL を返します。これは
``urlopen`` (または使用した opener オブジェクト) がリダイレクトされている
かもしれないために有用です。取得されたページの URL は、リクエストした
URL と同じでないかも知れないのです。

**info** - これは辞書に似たオブジェクトで、取得したページについて、
特にサーバから送られたヘッダについて記述しています。これは
現在は ``httplib.HTTPMessage`` のインスタンスです。

典型的なヘッダは 'Content-length'、'Content-type' などを
含みます。HTTP ヘッダと簡単な説明、それらの意味と利用についての便利なリストは
`Quick Reference to HTTP Headers <http://www.cs.tut.fi/~jkorpela/http.html>`_
を参照してください。


Openers と Handlers
====================

URL を取得する時は opener (きっと紛らわしい名前である ``urllib2.OpenerDirector`` 
のインスタンス)。これまで普通に、デフォルトの opener を - ``urlopen`` を通じて - 
使ってきました。しかしカスタムの opener を作ることも
可能です。Opener はハンドラを使用します。すべての "やっかいごと" は
ハンドラによって行われます。各々のハンドラは特定の URL スキーム (http、ftpなど) に
対してどのように URL をオープンするか、または HTTP リダイレクトや HTTP クッキーといった 
URL オープン時の局面にどのように対処するかを知っています。

もし、URL をインストールされた特定のハンドラで取得したい際には、
opener を作成したいことでしょう。例えば、cookie を処理する
opener を取得したり、またはリダイレクトを処理しない opener 等。

opener を作成するには、OpenerDirector をインスタンス化して、それから
.add_handler(some_handler_instance) をくり返し呼びます。

代替として ``build_opener`` を使うこともでき、これは一つの関数呼び出しで 
opener オブジェクトを作成するための便利な関数です。
``build_opener`` はデフォルトでいくつかのハンドラを追加しながら、
手早くハンドラを追加、そして/またはデフォルトハンドラをオーバーライドする
手段を提供します。

別の種類のハンドラでは、プロキシ、認証、その他
一般的ながらも少し特化された状況を処理するハンドラが
欲しくなるかもしれません。

``install_opener`` は ``opener`` オブジェクトを (グローバルな) デフォルトの 
opener とするのに使えます。これは、 ``urlopen`` の呼び出しで
あなたがインストールした opener を使うということを意味します。

opener オブジェクトは、 ``urlopen`` 関数と同じやり方で url を取得するために
直接呼ぶことのできる ``open`` 関数を持ちます：便宜のためを除いて、
``install_opener`` を呼ぶ必要はありません。


ベーシック認証
====================

ハンドラの作成とインストールを説明するために、 ``HTTPBasicAuthHandler`` を使いましょう。
このテーマについてのより詳しい議論 - ベーシック認証がどのように機能するかを含む - については
`Basic Authentication Tutorial  <http://www.voidspace.org.uk/python/articles/authentication.shtml>`_.
を参照してください。

認証が必要とされると、サーバは (401 エラーコードに加えて) 
認証を要求するヘッダを送ります。これは
認証方法と '領域(realm)' を指定します。ヘッダは以下のような感じです：
``Www-authenticate: SCHEME realm="REALM"``.

例 :: 

    Www-authenticate: Basic realm="cPanel Users"


そうすると、クライアントは領域に対する適切な名前とパスワードを
リクエストヘッダに含めて再度リクエストを行います。これが
'ベーシック認証' です。このプロセスを単純にするために、
``HTTPBasicAuthHandler`` のインスタンスと、このハンドラを
使うための opener が作成できます。

``HTTPBasicAuthHandler`` はパスワードマネージャと呼ばれるオブジェクトを使って、
URL と、領域に対するパスワードとユーザ名の対応を処理します。
(サーバから送られる認証ヘッダから) 領域 (realm) が分かっていれば、
``HTTPPasswordMgr`` が使えます。領域 (realm) が何であるかを気にしないのは
良くあることで、このようなケースでは、 
``HTTPPasswordMgrWithDefaultRealm`` を使うことができます。これは
URL に対するデフォルトのユーザ名とパスワードを指定することができます。
これは特定の領域 (realm) に対する組み合わせを備えることで
自動的に提供されます。このことは ``add_password`` の領域 (realm) 引数に
``None`` を与えることで示します。

top_level URL は認証を要求する最初の URL です。
.add_password() に渡した URL より "深い" URL にも対応します。 ::

    # パスワードマネージャの作成
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()                        

    # ユーザ名とパスワードの追加
    # 領域 (realm) が分かっていれば、それを ``None`` の代わりにできます。
    top_level_url = "http://example.com/foo/"
    password_mgr.add_password(None, top_level_url, username, password)

    handler = urllib2.HTTPBasicAuthHandler(password_mgr)                            

    # "opener" の作成 (OpenerDirector のインスタンス)
    opener = urllib2.build_opener(handler)         

    # opener を使って URL を取得する
    opener.open(a_url)      

    # opener のインストール。
    # これで全ての urllib2.urlopen 呼び出しが私たちの opener を利用します。
    urllib2.install_opener(opener)                               

.. note::
    上記の例では、 ``HTTPBasicAuthHandler`` だけを ``build_opener`` に
    与えました。デフォルトで opener は通常の状況に対するハンドラ - 
    ``ProxyHandler`` 、 ``UnknownHandler`` 、
    ``HTTPHandler`` 、 ``HTTPDefaultErrorHandler`` 、 
    ``HTTPRedirectHandler`` 、 ``FTPHandler`` 、 ``FileHandler`` 、
    ``HTTPErrorProcessor`` を持っています。

top_level_url は、実際はフルの URL ('http:' スキーム
コンポーネントとホスト名とオプションでポート番号を含む) 
例えば "http://example.com/" *または* "認証局 (authority)" 
(例. ホスト名、オプションでポート番号を含む) 例えば "example.com" や 
"example.com:8080" (後者はポート番号を含む)  のどちらかです。
認証局は、それがあるとして、"ユーザ情報 (userinfo)" コンポーネントを含んでは
いけません - 例えば "joe@password:example.com" は正しくありません。


プロキシ
===========

**urllib2** はプロキシ設定を自動検出してそれを使います。これは
普通のハンドラチェーンの一部である ``ProxyHandler`` を通してです。
通常これは好い事ですが、これが助けとならないようなケース [#]_ も
あります。これを処する一つの方法は、我々自身の、プロキシを定義しない
``ProxyHandler`` を設定することです。これは `ベーシック認証`_ ハンドラの
設定に似たステップで行います。

    >>> proxy_support = urllib2.ProxyHandler({})
    >>> opener = urllib2.build_opener(proxy_support)
    >>> urllib2.install_opener(opener)

.. note::

    現在は ``urllib2`` はプロキシ経由での ``https`` ロケーションの
    取得をサポート *していません* 。これは問題となり得ます。

ソケットとレイヤ
==================

Web からのリソース取得に対する Python のサポートは
レイヤ化されています。urllib2 は httplib ライブラリを使っていて、これは
今度は socket ライブラリを使用しています。

Python 2.3 から、タイムアウトまでにソケットがレスポンスをどのぐらい
待つかを指定できます。これは Web ページを取得するアプリケーションで
便利です。デフォルトでは socket モジュールは *タイムアウトなし* であり、
ハングが起こり得ます。現在では、socket のタイムアウトは httplib または
urllib2 レベルには出てきません。しかし、以下を使えば全てのソケットに対して
グローバルに、デフォルトのタイムアウトを設定できます： ::

    import socket
    import urllib2

    # タイムアウトを秒で
    timeout = 10
    socket.setdefaulttimeout(timeout) 

    # この urllib2.urlopen 呼び出しは socket モジュールに設定したところの
    # デフォルトタイムアウトを使います。
    req = urllib2.Request('http://www.voidspace.org.uk')
    response = urllib2.urlopen(req)


-------


脚注
=========

このドキュメントは John Lee によってレビューされ、改訂されました。

.. [#] CGI プロトコルの紹介は、以下を参照してください。
       `Writing Web Applications in Python <http://www.pyzine.com/Issue008/Section_Articles/article_CGIOne.html>`_. 
.. [#] 例えば Google のような。google をプログラムから利用する *正当な* 方法は、もちろん
       `PyGoogle <http://pygoogle.sourceforge.net>`_ を使うことです。
       `Voidspace Google <http://www.voidspace.org.uk/python/recipebook.shtml#google>`_
       の Google API 使用例を参照してください。
.. [#] ブラウザの検出はウェブサイトデザインにおいて非常に悪い慣習で - 
       Web 標準を利用したサイト構築のほうがずっと賢明です。不幸なことに、
       たくさんのサイトデザインが未だに異なるブラウザには異なるバージョンを送っています。
.. [#] MSIE 6 のユーザーエージェントは
       *'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'* です。
.. [#] HTTP リクエストヘッダについて、より詳しくは以下を参照してください：
       `Quick Reference to HTTP Headers`_.
.. [#] 私の例では、仕事でのインターネットアクセスにプロキシを使わねばなりません。
       *localhost* の URL をこのプロキシ経由で取得しようと試みた場合に、それはこれをブロックします。
       IE をプロキシを使う設定にしていて、これを urllib2 が拾うのです。
       localhost サーバでスクリプトをテストするために、私は urllib2 がプロキシを使うことを
       防がねばなりません。
