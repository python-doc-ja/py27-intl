:mod:`wsgiref` --- WSGI ユーティリティとリファレンス実装
========================================================

.. module:: wsgiref
   :synopsis: WSGI ユーティリティとリファレンス実装
.. moduleauthor:: Phillip J. Eby <pje@telecommunity.com>
.. sectionauthor:: Phillip J. Eby <pje@telecommunity.com>


.. versionadded:: 2.5

Web Server Gateway Interface (WSGI) は、Web サーバソフトウェアと Python で記述された Web
アプリケーションとの標準インターフェースです。標準インターフェースを持つことで、WSGI をサポートするアプリケーションを幾つもの異なる Web
サーバで使うことが容易になります。

Web サーバとプログラミングフレームワークの作者だけが、WSGI デザインのあらゆる細部や特例などを知る必要があります。WSGI アプリケーションを
インストールしたり、既存のフレームワークを使ったアプリケーションを記述するだけの皆さんは、全てについて理解する必要はありません。

:mod:`wsgiref` は WSGI 仕様のリファレンス実装で、これは Web サーバやフレームワークに WSGI サポートを加えるのに利用できます。
これは WSGI 環境変数やレスポンスヘッダを操作するユーティリティ、 WSGI サーバ実装時のベースクラス、WSGI アプリケーションを提供する  デモ用
HTTP サーバ、それと WSGI サーバとアプリケーションの WSGI 仕様 (:pep:`333`) 準拠のバリデーションツールを提供します。

.. See http://www.wsgi.org for more information about WSGI, and links to tutorials
   and other resources.

`<http://www.wsgi.org>`_ に、WSGIに関するさらなる情報と、チュートリアルやその他のリソースへのリンクがあります。

.. XXX If you're just trying to write a web application...


:mod:`wsgiref.util` -- WSGI 環境のユーティリティ
------------------------------------------------

.. module:: wsgiref.util
   :synopsis: WSGI 環境のユーティリティ


このモジュールは WSGI 環境で使う様々なユーティリティ関数を提供します。 WSGI 環境は :pep:`333` で記述されているような HTTP
リクエスト変数を含む辞書です。全ての *environ* パラメタを取る関数は WSGI 準拠の辞書を与えられることを期待しています；細かい仕様については
:pep:`333` を参照してください。


.. function:: guess_scheme(environ)

   ``wsgi.url_scheme`` が "http" か "https" かについて、 *environ* 辞書の ``HTTPS``
   環境変数を調べることでその推測を返します。戻り値は文字列(string)です。

   この関数は、CGI や FastCGI のような CGI に似たプロトコルをラップするゲートウェイを作成する場合に便利です。典型的には、それらのプロトコルを
   提供するサーバが SSL 経由でリクエストを受け取った場合には ``HTTPS`` 変数に値 "1" "yes"、または "on"
   を持つでしょう。ですので、この関数はそのような値が見つかった場合には "https" を返し、そうでなければ "http" を返します。


.. function:: request_uri(environ [, include_query=1])

   クエリ文字列をオプションで含むリクエスト URI 全体を、 :pep:`333` の "URL 再構築(URL Reconstruction)"
   にあるアルゴリズムを使って返します。 *include_query* が false の場合、クエリ文字列は結果となる文字列には含まれません。


.. function:: application_uri(environ)

   :func:`request_url` に似ていて、 ``PATH_INFO`` と ``QUERY_STRING`` 変数は
   無視されます。結果はリクエストによって指定されたアプリケーションオブジェクトのベース URI です。


.. function:: shift_path_info(environ)

   ``PATH_INFO`` から ``SCRIPT_NAME`` まで一つの名前をシフトしてその名前を返します。 *environ*
   辞書は *変更されます* ； ``PATH_INFO`` や ``SCRIPT_NAME`` のオリジナルをそのまま残したい場合にはコピーを使ってください。

   ``PATH_INFO`` にパスセグメントが何も残っていなければ、 ``None`` が返されます。

   典型的なこのルーチンの使い方はリクエスト URI のそれぞれの要素の処理で、例えばパスを一連の辞書のキーとして取り扱う場合です。
   このルーチンは、渡された環境を、ターゲット URL で示される別の WSGI アプリケーションの呼び出しに合うように調整します。例えば、 ``/foo`` に
   WSGI アプリケーションがあったとして、そしてリクエスト URL パスが ``/foo/bar/baz`` で、 ``/foo`` の WSGI
   アプリケーションが :func:`shift_path_info` を呼んだ場合、これは "bar" 文字列を受け取り、環境は ``/foo/bar`` の
   WSGI アプリケーションへの受け渡しに適するように更新されます。つまり、 ``SCRIPT_NAME`` は ``/foo`` から ``/foo/bar``
   に変わって、 ``PATH_INFO`` は ``/bar/baz`` から ``/baz`` に変化するのです。

   ``PATH_INFO`` が単に "/" の場合、このルーチンは空の文字列を返し、 ``SCRIPT_NAME`` の末尾にスラッシュを加えます、これはたとえ
   空のパスセグメントが通常は無視され、そして ``SCRIPT_NAME`` は通常スラッシュで終わる事が無かったとしてもです。これは意図的な振る舞いで、
   このルーチンでオブジェクト巡回(object traversal) をした場合に ``/x`` で終わる URI と ``/x/`` で終わるものを
   アプリケーションが識別できることを保証するためのものです。


.. function:: setup_testing_defaults(environ)

   テスト目的で、 *environ* を自明なデフォルト値 (trivial defaults) で更新します。

   このルーチンは WSGI に必要な様々なパラメタを追加し、それには ``HTTP_HOST`` 、 ``SERVER_NAME`` 、 ``SERVER_PORT`` 、
   ``REQUEST_METHOD`` 、 ``SCRIPT_NAME`` 、 ``PATH_INFO`` 、あとは :pep:`333` で定義されている
   ``wsgi.*`` 変数群を含みます。これはデフォルト値のみを追加し、これらの変数の既存設定は一切置きかえません。

   このルーチンは、ダミー環境をセットアップすることによって WSGI サーバとアプリケーションのユニットテストを容易にすることを意図しています。これは実際の
   WSGI サーバやアプリケーションで使うべきではありません。なぜならこのデータは偽物なのです！

   .. Example usage::

   利用例::

      from wsgiref.util import setup_testing_defaults
      from wsgiref.simple_server import make_server

      # 比較的シンプルなWSGIアプリケーション。
      # setup_testing_defaults によって更新されたあとの environment を表示する
      def simple_app(environ, start_response):
          setup_testing_defaults(environ)

          status = '200 OK'
          headers = [('Content-type', 'text/plain')]

          start_response(status, headers)

          ret = ["%s: %s\n" % (key, value)
                 for key, value in environ.iteritems()]
          return ret

      httpd = make_server('', 8000, simple_app)
      print "Serving on port 8000..."
      httpd.serve_forever()


上記の環境用関数に加えて、 :mod:`wsgiref.util` モジュールも以下のようなその他のユーティリティを提供します：


.. function:: is_hop_by_hop(header_name)

   'header_name' が :rfc:`2616` で定義されている HTTP/1.1 の "Hop-by-Hop" ヘッダの場合に true
   を返します。


.. class:: FileWrapper(filelike [, blksize=8192])

   ファイルライクオブジェクトをイテレータ(:term:`iterator`)に変換するラッパです。結果のオブジェクトは :meth:`__getitem__` と :meth:`__iter__`
   両方をサポートしますが、これは Python 2.1 と Jython の互換性のためです。オブジェクトがイテレートされる間、オプションの
   *blksize* パラメタがくり返し *filelike* オブジェクトの :meth:`read` メソッドに渡されて
   受け渡す文字列を取得します。 :meth:`read` が空文字列を返した場合イテレーションは終了して、再開されることはありません。

   *filelike* に :meth:`close` メソッドがある場合、返されたオブジェクトも :meth:`close`
   メソッドを持ち、これが呼ばれた場合には *filelike* オブジェクトの :meth:`close` メソッドを呼び出します。

   .. Example usage::

   利用例::

      from StringIO import StringIO
      from wsgiref.util import FileWrapper

      # We're using a StringIO-buffer for as the file-like object
      filelike = StringIO("This is an example file-like object"*10)
      wrapper = FileWrapper(filelike, blksize=5)

      for chunk in wrapper:
          print chunk



:mod:`wsgiref.headers` -- WSGI レスポンスヘッダツール群
-------------------------------------------------------

.. module:: wsgiref.headers
   :synopsis: WSGI レスポンスヘッダツール群


このモジュールは単一のクラス、 :class:`Headers` を提供し、WSGI レスポンスヘッダの操作をマップに似たインターフェースで便利にします。


.. class:: Headers(headers)

   *headers* をラップするマップに似たオブジェクトを生成します。これは :pep:`333` に定義されるようなヘッダの名前／値のタプルのリストです。
   新しい :class:`Headers` オブジェクトに与えられた変更は、一緒に作成された *headers* リストを直接更新します。

   :class:`Headers` オブジェクトは典型的なマッピング操作をサポートし、これには
   :meth:`__getitem__` 、 :meth:`get` 、 :meth:`__setitem__` 、
   :meth:`setdefault` 、 :meth:`__delitem__` 、 :meth:`__contains__` と :meth:`has_key`
   を含みます。これらメソッドのそれぞれにおいて、キーはヘッダ名で（大文字小文字は区別しません）、値はそのヘッダ名に関連づけられた
   最初の値です。ヘッダを設定すると既存のヘッダ値は削除され、ラップされたヘッダのリストの末尾に新しい値が加えられます。既存のヘッダの順番は
   一般的に整えられていて、ラップされたリストの最後に新しいヘッダが追加されます。

   辞書とは違って、 :class:`Headers` オブジェクトはラップされたヘッダリストに
   存在しないキーを取得または削除しようとした場合にもエラーを発生しません。単に、存在しないヘッダの取得は ``None`` を返し、存在しないヘッダの削除は
   何もしません。

   :class:`Headers` オブジェクトは :meth:`keys` 、 :meth:`values` 、 :meth:`items`
   メソッドもサポートします。 :meth:`keys` と :meth:`items` で
   返されるリストは、同じキーを一回以上含むことがあり、これは複数の値を持つヘッダの場合です。 :class:`Header` オブジェクトの ``len()``
   は、その :meth:`items` の長さと同じであり、ラップされたヘッダリストの長さと同じです。事実、 :meth:`items` メソッドは
   単にラップされたヘッダリストのコピーを返しているだけです。

   :class:`Headers` オブジェクトに対して ``str()`` を呼ぶと、HTTP レスポンスヘッダとして
   送信するのに適した形に整形された文字列を返します。それぞれのヘッダはコロンとスペースで区切られた値と共に一列に並んでいます。
   それぞれの行はキャリッジリターンとラインフィードで終了し、文字列は空行で終了しています。

   これらのマッピングインターフェースと整形機能に加えて、 :class:`Headers` オブジェクトは複数の値を持つヘッダの取得と追加、MIME
   パラメタでヘッダを追加するための以下のようなメソッド群も持っています：


   .. method:: Headers.get_all(name)

      指定されたヘッダの全ての値のリストを返します。

      返されるリストは、元々のヘッダリストに現れる順、またはこのインスタンスに追加された順に並んでいて、複製を含む場合があります。削除されて加えられた
      フィールドは全てヘッダリストの末尾に付きます。ある名前のフィールドが何もなければ、空のリストが返ります。


   .. method:: Headers.add_header(name, value, **_params)

      ヘッダ（複数の値かもしれません）を、キーワード引数を通じて指定するオプションの MIME パラメタと共に追加します。

      *name* は追加するヘッダフィールドです。このヘッダフィールドに MIME パラメタを
      設定するためにキーワード引数を使うことができます。それぞれのパラメタは文字列か ``None`` で
      なければいけません。パラメタ中のアンダースコアはダッシュに変換されます、これはダッシュが Python の識別子としては不正なのですが、多くの MIME
      パラメタはダッシュを含むためです。パラメタ値が文字列の場合、これはヘッダ値のパラメタに ``name="value"`` の形で追加されます。これがもし
      ``None`` の場合、パラメタ名だけが追加されます。（これは値なしの MIME パラメタの場合に使われます。）使い方の例は： ::

         h.add_header('content-disposition', 'attachment', filename='bud.gif')

      上記はこのようなヘッダを追加します： ::

         Content-Disposition: attachment; filename="bud.gif"


:mod:`wsgiref.simple_server` -- シンプルな WSGI HTTP サーバ
-----------------------------------------------------------

.. module:: wsgiref.simple_server
   :synopsis: シンプルな WSGI HTTP サーバ


このモジュールは WSGI アプリケーションを提供するシンプルな HTTP サーバです（ :mod:`BaseHTTPServer` がベースです）。
個々のサーバインスタンスは単一の WSGI アプリケーションを、特定のホストとポート上で
提供します。もし一つのホストとポート上で複数のアプリケーションを提供したいならば、 ``PATH_INFO``
をパースして個々のリクエストでどのアプリケーションを呼び出すか選択するような WSGI アプリケーションを作るべきです。（例えば、
:mod:`wsgiref.util` から :func:`shift_path_info` を利用します。）


.. function:: make_server(host, port, app [, server_class=WSGIServer [, handler_class=WSGIRequestHandler]])

   *host* と *port* 上で待機し、 *app* へのコネクションを受け付ける  WSGI サーバを作成します。戻り値は与えられた
   *server_class* のインスタンスで、指定された *handler_class* を使ってリクエストを処理します。 *app* は
   :pep:`333` で定義されるところの WSGI アプリケーションでなければいけません。

   使用例：  ::

      from wsgiref.simple_server import make_server, demo_app

      httpd = make_server('', 8000, demo_app)
      print "Serving HTTP on port 8000..."

      # プロセスが死ぬまでリクエストに答える
      httpd.serve_forever()

      # 代替：１つのリクエストを受けて終了する
      httpd.handle_request()


.. function:: demo_app(environ, start_response)

   この関数は小規模ながら完全な WSGI アプリケーションで、 "Hello world!" メッセージと、 *environ* パラメタに提供されている
   キー／値のペアを含むテキストページを返します。これは WSGI サーバ（ :mod:`wsgiref.simple_server` のような）がシンプルな
   WSGI アプリケーションを正しく実行できるかを確かめるのに便利です。


.. class:: WSGIServer(server_address, RequestHandlerClass)

   :class:`WSGIServer` インスタンスを作成します。 *server_address* は ``(host,port)`` のタプル、そして
   *RequesthandlerClass* はリクエストの処理に使われる
   :class:`BaseHTTPServer.BaseHTTPRequestHandler` のサブクラスでなければいけません。

   :func:`make_server` が細かい調整をやってくれるので、通常はこのコンストラクタを呼ぶ必要はありません。

   :class:`WSGIServer` は :class:`BaseHTTPServer.HTTPServer` のサブクラスですので、
   この全てのメソッド（ :meth:`serve_forever` や :meth:`handle_request` のような）が利用できます。
   :class:`WSGIServer` も以下のような WSGI 固有メソッドを提供します：


   .. method:: WSGIServer.set_app(application)

      呼び出し可能（callable）な *application* をリクエストを受け取る WSGI アプリケーションとして設定します。


   .. method:: WSGIServer.get_app()

      現在設定されている呼び出し可能（callable）アプリケーションを返します。

   しかしながら、通常はこれらの追加されたメソッドを使う必要はありません。 :meth:`set_app` は普通は :func:`make_server`
   によって呼ばれ、 :meth:`get_app` は主にリクエストハンドラインスタンスの便宜上存在するからです。


.. class:: WSGIRequestHandler(request, client_address, server)

   与えられた *request* （すなわちソケット）の HTTP ハンドラ、 *client_address* （ ``host,port)`` のタプル）、
   *server* （ :class:`WSGIServer` インスタンス）の HTTP ハンドラを作成します。

   このクラスのインスタンスを直接生成する必要はありません；これらは必要に応じて :class:`WSGIServer`
   オブジェクトによって自動的に生成されます。しかしながら、このクラスをサブクラス化し、 :func:`make_server` 関数に
   *handler_class* として与えることは可能でしょう。サブクラスにおいてオーバーライドする意味のありそうなものは：


   .. method:: WSGIRequestHandler.get_environ()

      リクエストに対する WSGI 環境を含む辞書を返します。デフォルト実装では :class:`WSGIServer` オブジェクトの
      :attr:`base_environ` 辞書属性のコンテンツをコピーし、それから HTTP リクエスト由来の様々なヘッダを追加しています。
      このメソッド呼び出し毎に、 :pep:`333` に指定されている関連する CGI 環境変数を全て含む新規の辞書を返さなければいけません。


   .. method:: WSGIRequestHandler.get_stderr()

      ``wsgi.errors`` ストリームとして使われるオブジェクトを返します。デフォルト実装では単に ``sys.stderr`` を返します。


   .. method:: WSGIRequestHandler.handle()

      HTTP リクエストを処理します。デフォルト実装では実際の WGI アプリケーションインターフェースを実装するのに
      :mod:`wsgiref.handlers` クラスを使ってハンドラインスタンスを作成します。


:mod:`wsgiref.validate` --- WSGI 準拠チェッカー
------------------------------------------------

.. module:: wsgiref.validate
   :synopsis: WSGI 準拠チェッカー


WSGI アプリケーションのオブジェクト、フレームワーク、サーバ又はミドルウェアの作成時には、その新規のコードを
:mod:`wsgiref.validate` を使って準拠の検証をすると便利です。このモジュールは WSGI サーバやゲートウェイと WSGI
アプリケーションオブジェクト間の通信を検証する WSGI アプリケーションオブジェクトを作成する関数を提供し、双方のプロトコル準拠をチェックします。

このユーティリティは完全な :pep:`333` 準拠を保証するものでないことは注意してください；
このモジュールでエラーが出ないことは必ずしもエラーが存在しないことを意味しません。しかしこのモジュールがエラーを出したならば、サーバかアプリケーションの
どちらかが 100 このモジュールは lan Bicking の "Python Paste" ライブラリの  :mod:`paste.lint`
モジュールをベースにしています。

.. % 準拠ではないことはほとんど確実です。


.. function:: validator(application)

   *application* をラップし、新しい WSGI アプリケーションオブジェクトを返します。返されたアプリケーションは全てのリクエストを元々の
   *application* にフォワードし、 *application* とそれを呼び出すサーバの両方が WSGI 仕様と RFC 2616
   の両方に準拠しているかをチェックします。

   検出された非準拠は、投げられる :exc:`AssertionError` の中に入ります；
   しかし、このエラーがどう扱われるかはサーバ依存であることに注意してください。例えば、 :mod:`wsgiref.simple_server` とその他
   :mod:`wsgiref.handlers` ベースのサーバ（エラー処理メソッドが他のことをするようにオーバライドしていないもの）は
   単純にエラーが発生したというメッセージとトラックバックのダンプを ``sys.stderr`` やその他のエラーストリームに出力します。

   このラッパは :mod:`warnings` モジュールを使って出力を生成し、疑問の余地はあるが実際には :pep:`333`
   で禁止はされていないかもしれない挙動を指摘します。これらは Python のコマンドラインオプションや :mod:`warnings` API で
   抑制されなければ、 ``sys.stderr`` (たまたま同一のオブジェクトで無い限り  ``wsgi.errors`` では *ない*)に書き出されます。

   .. Example usage:

   利用例::

      from wsgiref.validate import validator
      from wsgiref.simple_server import make_server

      # Our callable object which is intentionally not compliant to the
      # standard, so the validator is going to break
      def simple_app(environ, start_response):
          status = '200 OK' # HTTP Status
          headers = [('Content-type', 'text/plain')] # HTTP Headers
          start_response(status, headers)

          # This is going to break because we need to return a list, and
          # the validator is going to inform us
          return "Hello World"

      # This is the application wrapped in a validator
      validator_app = validator(simple_app)

      httpd = make_server('', 8000, validator_app)
      print "Listening on port 8000...."
      httpd.serve_forever()


:mod:`wsgiref.handlers` -- サーバ／ゲートウェイのベースクラス
-------------------------------------------------------------

.. module:: wsgiref.handlers
   :synopsis: WSGI サーバ／ゲートウェイのベースクラス


このモジュールは WSGI サーバとゲートウェイ実装のベースハンドラクラスを提供します。これらのベースクラスは CGI ライクの環境を与えられれば
入力、出力そしてエラーストリームと共に WSGI アプリケーションとの通信の大部分を処理します。


.. class:: CGIHandler()

   ``sys.stdin`` 、 ``sys.stdout`` 、 ``stderr`` そして ``os.environ`` 経由での CGI
   ベースの呼び出しです。これは、もしあなたが WSGI アプリケーションを持っていて、これを CGI スクリプトとして実行したい場合に有用です。単に
   ``CGIHandler().run(app)`` を起動してください。 ``app`` はあなたが起動したい WSGI アプリケーションオブジェクトです。

   このクラスは :class:`BaseCGIHandler` のサブクラスで、これは ``wsgi.run_once`` を true、
   ``wsgi.multithread`` を false、そして ``wsgi.multiprocess`` を true にセットし、常に
   :mod:`sys` と :mod:`os` を、必要な CGI ストリームと環境を取得するために使用します。


.. class:: BaseCGIHandler(stdin, stdout, stderr, environ [, multithread=True [, multiprocess=False]])

   :class:`CGIHandler` に似ていますが、 :mod:`sys` と :mod:`os` モジュールを使う代わりに CGI 環境と I/O
   ストリームを明示的に指定します。 *multithread* と *multiprocess* の値は、ハンドラインスタンスにより実行されるアプリケーションの
   ``wsgi.multithread`` と ``wsgi.multiprocess`` フラグの設定に使われます。

   このクラスは :class:`SimpleHandler` のサブクラスで、HTTP の "本サーバ" でない
   ソフトウェアと使うことを意図しています。もしあなたが ``Status:`` ヘッダを HTTP ステータスを送信するのに使うような
   ゲートウェイプロトコルの実装（CGI、FastCGI、SCGIなど）を書いているとして、おそらく :class:`SimpleHandler`
   でなくこれをサブクラス化したいことでしょう。


.. class:: SimpleHandler(stdin, stdout, stderr, environ [,multithread=True [, multiprocess=False]])

   :class:`BaseCGIHandler` と似ていますが、HTTP の本サーバと使うためにデザインされています。もしあなたが HTTP
   サーバ実装を書いている場合、おそらく :class:`BaseCGIHandler` でなくこれをサブクラス化したいことでしょう。

   このクラスは :class:`BaseHandler` のサブクラスです。これは :meth:`__init__` 、
   :meth:`get_stdin` 、 :meth:`get_stderr` 、 :meth:`add_cgi_vars` 、 :meth:`_write` 、
   :meth:`_flush` をオーバーライドして、コンストラクタから明示的に環境とストリームを設定するようにしています。与えられた環境とストリームは
   :attr:`stdin` 、 :attr:`stdout` 、 :attr:`stderr` それに :attr:`environ` 属性に保存されています。


.. class:: BaseHandler()

   これは WSGI アプリケーションを実行するための抽象ベースクラスです。原理上は複数のリクエスト用に再利用可能なサブクラスを作成することが
   できますが、それぞれのインスタンスは一つの HTTP リクエストを処理します。

   :class:`BaseHandler` インスタンスは外部からの利用にたった一つのメソッドを持ちます：


   .. method:: BaseHandler.run(app)

      指定された WSGI アプリケーション、 *app* を実行します。

   その他の全ての :class:`BaseHandler` のメソッドはアプリケーション実行プロセスで
   このメソッドから呼ばれます。ですので、主にそのプロセスのカスタマイズのために存在しています。

   以下のメソッドはサブクラスでオーバーライドされなければいけません：


   .. method:: BaseHandler._write(data)

      文字列の *data* をクライアントへの転送用にバッファします。このメソッドが実際にデータを転送しても OK です：
      下部システムが実際にそのような区別をしている場合に効率をより良くするために、 :class:`BaseHandler`
      は書き出しとフラッシュ操作を分けているからです。


   .. method:: BaseHandler._flush()

      バッファされたデータをクライアントに強制的に転送します。このメソッドは何もしなくても OK です（すなわち、 :meth:`_write`
      が実際にデータを送る場合）。


   .. method:: BaseHandler.get_stdin()

      現在処理中のリクエストの ``wsgi.input`` としての利用に適当な入力ストリームオブジェクトを返します。


   .. method:: BaseHandler.get_stderr()

      現在処理中のリクエストの ``wsgi.errors`` としての利用に適当な出力ストリームオブジェクトを返します。


   .. method:: BaseHandler.add_cgi_vars()

      現在のリクエストの CGI 変数を :attr:`environ` 属性に追加します。

   これらがオーバーライドするであろうメソッド及び属性です。しかしながら、このリストは単にサマリであり、オーバーライド可能な全てのメソッドは
   含んでいません。カスタマイズした :class:`BaseHandler` サブクラスを作成しようとする前にドキュメント文字列 (docstrings)
   やソースコードでさらなる情報を調べてください。

   WSGI 環境のカスタマイズのための属性とメソッド：


   .. attribute:: BaseHandler.wsgi_multithread

      ``wsgi.multithread`` 環境変数で使われる値。デフォルトは :class:`BaseHandler` では true
      ですが、別のサブクラスではデフォルトで（またはコンストラクタによって設定されて）異なる値を持つことがあります。


   .. attribute:: BaseHandler.wsgi_multiprocess

      ``wsgi.multiprocess`` 環境変数で使われる値。デフォルトは :class:`BaseHandler` では true
      ですが、別のサブクラスではデフォルトで（またはコンストラクタによって設定されて）異なる値を持つことがあります。


   .. attribute:: BaseHandler.wsgi_run_once

      ``wsgi.run_once`` 環境変数で使われる値。デフォルトは :class:`BaseHandler` では false
      ですが、 :class:`CGIHandler` はデフォルトでこれを true に設定します。


   .. attribute:: BaseHandler.os_environ

      全てのリクエストの WSGI 環境に含まれるデフォルトの環境変数。デフォルトでは、 :mod:`wsgiref.handlers` がインポートされた時点では
      これは ``os.environ`` のコピーですが、サブクラスはクラスまたはインスタンスレベルでそれら自身のものを作ることができます。
      デフォルト値は複数のクラスとインスタンスで共有されるため、この辞書は読み取り専用と考えるべきだという点に注意してください。


   .. attribute:: BaseHandler.server_software

      :attr:`origin_server` 属性が設定されている場合、この属性の値がデフォルトの ``SERVER_SOFTWARE`` WSGI
      環境変数の設定や HTTP レスポンス中のデフォルトの ``Server:``
      ヘッダの設定に使われます。これは（ :class:`BaseCGIHandler` や :class:`CGIHandler` のような）HTTP
      オリジンサーバでないハンドラでは無視されます。


   .. method:: BaseHandler.get_scheme()

      現在のリクエストで使われている URL スキームを返します。デフォルト実装は :mod:`wsgiref.util` の
      :func:`guess_scheme` を使い、現在のリクエストの :attr:`envion` 変数に基づいてスキームが"http" か "https"
      かを推測します。


   .. method:: BaseHandler.setup_environ()

      :attr:`environ` 属性を、全てを導入済みの WSGI 環境に設定します。デフォルトの実装は、上記全てのメソッドと属性、加えて
      :meth:`get_stdin` 、 :meth:`get_stderr` 、 :meth:`add_cgi_vars` メソッドと
      :attr:`wsgi_file_wrapper` 属性を利用します。これは、キーが存在せず、 :attr:`origin_server` 属性が true
      値で :attr:`server_software` 属性も設定されている場合に ``SERVER_SOFTWARE`` を挿入します。

   例外処理のカスタマイズのためのメソッドと属性：


   .. method:: BaseHandler.log_exception(exc_info)

      *exec_info* タプルをサーバログに記録します。 *exc_info* は ``(type, value, traceback)`` のタプルです。
      デフォルトの実装は単純にトレースバックをリクエストの ``wsgi.errors`` ストリームに
      書き出してフラッシュします。サブクラスはこのメソッドをオーバーライドしてフォーマットを変更したり出力先の変更、トレースバックを管理者にメールしたり
      その他適切と思われるいかなるアクションも取ることができます。


   .. attribute:: BaseHandler.traceback_limit

      デフォルトの :meth:`log_exception` メソッドで出力されるトレースバック出力に含まれる最大のフレーム数です。 ``None`` ならば、
      全てのフレームが含まれます。


   .. method:: BaseHandler.error_output(environ, start_response)

      このメソッドは、ユーザに対してエラーページを出力する WSGI アプリケーションです。これはクライアントにヘッダが送出される前にエラーが発生した場合にのみ
      呼び出されます。

      このメソッドは ``sys.exc_info()`` を使って現在のエラー情報にアクセスでき、その情報はこれを呼ぶときに *start_response* に
      渡すべきです（ :pep:`333` の "Error Handling" セクションに記述があります）。

      デフォルト実装は単に :attr:`error_status` 、 :attr:`error_headers` 、そして :attr:`error_body`
      属性を出力ページの生成に使います。サブクラスではこれをオーバーライドしてもっと動的なエラー出力をすることが出来ます。

      しかし、セキュリティの観点からは診断をあらゆる老練ユーザに吐き出すことは推奨されないことに気をつけてください；理想的には、診断的な出力を有効に
      するには何らかの特別なことをする必要があるようにすべきで、これがデフォルト実装では何も含まれていない理由です。


   .. attribute:: BaseHandler.error_status

      エラーレスポンスで使われる HTTP ステータスです。これは :pep:`333` で定義されているステータス文字列です；デフォルトは 500
      コードとメッセージです。


   .. attribute:: BaseHandler.error_headers

      エラーレスポンスで使われる HTTP ヘッダです。これは :pep:`333` で述べられているような、 WSGI レスポンスヘッダ（``(name,
      value)`` タプル）のリストであるべきです。デフォルトのリストはコンテントタイプを ``text/plain`` にセットしているだけです。


   .. attribute:: BaseHandler.error_body

      エラーレスポンスボディ。これは HTTP レスポンスのボディ文字列であるべきです。これはデフォルトではプレーンテキストで "A server error
      occurred.  Please contact the administrator." です。

   :pep:`333` の "オプションのプラットフォーム固有のファイルハンドリング" 機能のためのメソッドと属性：


   .. attribute:: BaseHandler.wsgi_file_wrapper

      ``wsgi.file_wrapper`` ファクトリ、または ``None`` です。この属性のデフォルト値は :mod:`wsgiref.util` の
      :class:`FileWrapper` クラスです。


   .. method:: BaseHandler.sendfile()

      オーバーライドしてプラットフォーム固有のファイル転送を実装します。このメソッドはアプリケーションの戻り値が :attr:`wsgi_file_wrapper`
      属性で指定されたクラスのインスタンスの場合にのみ呼ばれます。これはファイルの転送が成功できた場合には true を返して、デフォルトの転送コードが
      実行されないようにするべきです。このデフォルトの実装は単に false 値を返します。

   その他のメソッドと属性：


   .. attribute:: BaseHandler.origin_server

      この属性はハンドラの :meth:`_write` と :meth:`_flush` が、特別に ``Status:`` ヘッダに HTTP
      ステータスを求めるような CGI 状のゲートウェイプロトコル経由でなく、クライアントと直接通信をするような場合には true 値に設定されているべきです。

      この属性のデフォルト値は :class:`BaseHandler` では true ですが、 :class:`BaseCGIHandler` と
      :class:`CGIHandler` では false です。


   .. attribute:: BaseHandler.http_version

      :attr:`origin_server` が true の場合、この文字列属性はクライアントへのレスポンスセットの HTTP
      バージョンの設定に使われます。デフォルトは ``"1.0"`` です。


例
--------

.. This is a working "Hello World" WSGI application::

これは動作する "Hello World" WSGIアプリケーションです。 ::

   from wsgiref.simple_server import make_server

   # Every WSGI application must have an application object - a callable
   # object that accepts two arguments. For that purpose, we're going to
   # use a function (note that you're not limited to a function, you can
   # use a class for example). The first argument passed to the function
   # is a dictionary containing CGI-style envrironment variables and the
   # second variable is the callable object (see PEP333)
   def hello_world_app(environ, start_response):
       status = '200 OK' # HTTP Status
       headers = [('Content-type', 'text/plain')] # HTTP Headers
       start_response(status, headers)

       # The returned object is going to be printed
       return ["Hello World"]

   httpd = make_server('', 8000, hello_world_app)
   print "Serving on port 8000..."

   # Serve until process is killed
   httpd.serve_forever()
