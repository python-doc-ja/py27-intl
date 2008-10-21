
:mod:`xmlrpclib` --- XML-RPC クライアントアクセス
=================================================

.. module:: xmlrpclib
   :synopsis: XML-RPC client access.
.. moduleauthor:: Fredrik Lundh <fredrik@pythonware.com>
.. sectionauthor:: Eric S. Raymond <esr@snark.thyrsus.com>


.. % Not everyting is documented yet.  It might be good to describe
.. % Marshaller, Unmarshaller, getparser, dumps, loads, and Transport.

.. versionadded:: 2.2

XML-RPCはXMLを利用した遠隔手続き呼び出し(Remote Procedure Call)の一種 で、HTTPをトランスポートとして使用します。XML-
RPCでは、クライアントはリ モートサーバ(URIで指定されたサーバ)上のメソッドをパラメータを指定して呼
び出し、構造化されたデータを取得します。このモジュールは、XML-RPCクライ アントの開発をサポートしており、Pythonオブジェクトに適合する転送用XMLの
変換の全てを行います。


.. class:: ServerProxy(uri[, transport[, encoding[, verbose[,  allow_none[, use_datetime]]]]])

   :class:`ServerProxy`は、リモートのXML-RPCサーバとの通信を管理するオブジェ クトです。最初のパラメータはURI(Uniform
   Resource Indicator)で、通常は サーバのURLを指定します。2番目のパラメータにはトランスポート・ファクトリ
   を指定する事ができます。トランスポート・ファクトリを省略した場合、URLが https:
   ならモジュール内部の:class:`SafeTransport`インスタンスを使用し、そ
   れ以外の場合にはモジュール内部の:class:`Transport`インスタンスを使用しま す。オプションの 3 番目の引数はエンコード方法で、デフォルトでは
   UTF-8 です。オプションの 4 番目の引数はデバッグフラグです。 *allow_none* が真の場合、Python の定数 ``None`` は XML
   に翻訳されます; デフォルトの動作は ``None`` に対して :exc:`TypeError` を送出します。 この仕様は XML-RPC
   仕様でよく用いられている拡張ですが、 全てのクライアントやサーバでサポートされているわけではありません; 詳細記述については
   `<http://ontosys.com/xml-rpc/extensions.html>`_  を参照してください。
   *use_datetime*フラグは:class:`datetime.datetime`のオブジェクトとして 日付/時刻を表現する時に使用し、デフォルトでは
   false に設定されています。 :class:`datetime.datetime`、
   :class:`datetime.date`および:class:`datetime.time` のオブジェクトを渡すことができます。
   :class:`datetime.date`オブジェクトは 時刻"00:00:00"に変換されます。
   :class:`datetime.time`オブジェクトは、 今日の日付に変換されます。

   HTTP及びHTTPS通信の両方で、``http://user:pass@host:port/path``のよう
   なHTTP基本認証のための拡張URL構文をサポートしています。``user:pass`` はbase64でエンコードしてHTTPの'Authorization
   'ヘッダとなり、XML-RPCメソッ ド呼び出し時に接続処理の一部としてリモートサーバに送信されます。リモート
   サーバが基本認証を要求する場合のみ、この機能を利用する必要があります。

   生成されるインスタンスはリモートサーバへのプロクシオブジェクトで、RPC呼 び出しを行う為のメソッドを持ちます。リモートサーバがイントロスペクション
   APIをサポートしている場合は、リモートサーバのサポートするメソッドを検索 (サービス検索)やサーバのメタデータの取得なども行えます。

   :class:`ServerProxy`インスタンスのメソッドは引数としてPythonの基礎型とオ
   ブジェクトを受け取り、戻り値としてPythonの基礎型かオブジェクトを返しま す。以下の型をXMLに変換(XMLを通じてマーシャルする)する事ができます(特別
   な指定がない限り、逆変換でも同じ型として変換されます):

   +---------------------+-------------------------------------------------------------------------+
   | 名前                | 意味                                                                    |
   +=====================+=========================================================================+
   | :const:`boolean`    | 定数:const:`True`と:const:`False`                                       |
   +---------------------+-------------------------------------------------------------------------+
   | :const:`整数`       | そのまま                                                                |
   +---------------------+-------------------------------------------------------------------------+
   | :const:`浮動小数点` | そのまま                                                                |
   +---------------------+-------------------------------------------------------------------------+
   | :const:`文字列`     | そのまま                                                                |
   +---------------------+-------------------------------------------------------------------------+
   | :const:`配列`       | 変換可能な要素を含むPythonシーケンス。 戻り値はリスト。                 |
   +---------------------+-------------------------------------------------------------------------+
   | :const:`構造体`     | Pythonの辞書。キーは文字列のみ。全ての値は変換可能でな くてはならない。 |
   +---------------------+-------------------------------------------------------------------------+
   | :const:`日付`       | エポックからの経過秒数。引数として指定する時は                          |
   |                     | :class:`DataTime`ラッパクラスまたは、                                   |
   |                     | :class:`datetime.datetime`、                                            |
   |                     | :class:`datetime.date`、                                                |
   |                     | :class:`datetime.time`のいずれかのインスタンスを使用する。              |
   +---------------------+-------------------------------------------------------------------------+
   | :const:`バイナリ`   | :class:`Binary`ラッパクラスのインスタンス                               |
   +---------------------+-------------------------------------------------------------------------+

   上記のXML-RPCでサポートする全データ型を使用することができます。メソッド 呼び出し時、XML-
   RPCサーバエラーが発生すると:exc:`Fault`インスタンス を送出し、HTTP/HTTPSトランスポート層でエラーが発生した場合には
   :exc:`ProtocolError`を送出します。 :exc:`Error`をベースとする
   :exc:`Fault`と:exc:`ProtocolError`の両方が発生します。 Python 2.2以降では組み込み型のサ
   ブクラスを作成する事ができますが、現在のところxmlrpclibではそのようなサ ブクラスのインスタンスをマーシャルすることはできません。

   文字列を渡す場合、``<``・``>``・``&``などのXMLで特殊な意味を持
   つ文字は自動的にエスケープされます。しかし、ASCII値0〜31の制御文字などの XMLで使用することのできない文字を使用することはできず、使用するとその
   XML-RPCリクエストはwell-formedなXMLとはなりません。そのような文字列を渡
   す必要がある場合は、後述の:class:`Binary`ラッパクラスを使用してください。

   :class:`Server`は、上位互換性の為に:class:`ServerProxy`の別名として残され
   ています。新しいコードでは:class:`ServerProxy`を使用してください。

   .. versionchanged:: 2.5
      The *use_datetime* flag was added.


.. seealso::

   `XML-RPC HOWTO <http://www.tldp.org/HOWTO/XML-RPC-HOWTO/index.html>`_
      週種類のプログラミング言語で記述された XMLの操作とクライアントソフトウェアの素晴らしい 説明が掲載されています。 XML-
      RPCクライアントの開発者が知っておくべきことが ほとんど全て記載されています。

   `XML-RPC-Hacks page <http://xmlrpc-c.sourceforge.net/hacks.php>`_
      イントロスペクションとマルチコールを サポートしているオープンソースの拡張ライブラリについて説明しています。


.. _serverproxy-objects:

ServerProxy オブジェクト
------------------------

:class:`ServerProxy`インスタンスの各メソッドはそれぞれXML-RPCサーバの遠隔
手続き呼び出しに対応しており、メソッドが呼び出されると名前と引数をシグネ チャとしてRPCを実行します(同じ名前のメソッドでも、異なる引数シグネチャに
よってオーバロードされます)。RPC実行後、変換された値を返すか、または
:class:`Fault`オブジェクトもしくは:class:`ProtocolError`オブジェクトでエ ラーを通知します。

予約メンバ:attr:`system`から、XMLイントロスペクションAPIの一般的なメソ ッドを利用する事ができます。


.. method:: ServerProxy.system.listMethods()

   XML-RPCサーバがサポートするメソッド名(system以外)を格納する文字列のリス トを返します。


.. method:: ServerProxy.system.methodSignature(name)

   XML-RPCサーバで実装されているメソッドの名前を指定し、利用可能なシグネチ ャの配列を取得します。シグネチャは型のリストで、先頭の型は戻り値の型を示
   し、以降はパラメータの型を示します。

   XML-RPCでは複数のシグネチャ(オーバロード)を使用することができるので、単 独のシグネチャではなく、シグネチャのリストを返します。

   シグネチャは、メソッドが使用する最上位のパラメータにのみ適用されます。例 えばあるメソッドのパラメータが構造体の配列で戻り値が文字列の場合、シグネ
   チャは単に"文字列, 配列" となります。パラメータが三つの整数で戻り値が文 字列の場合は"文字列, 整数, 整数, 整数"となります。

   メソッドにシグネチャが定義されていない場合、配列以外の値が返ります。 Pythonでは、この値はlist以外の値となります。


.. method:: ServerProxy.system.methodHelp(name)

   XML-RPCサーバで実装されているメソッドの名前を指定し、そのメソッドを解説 する文書文字列を取得します。文書文字列を取得できない場合は空文字列を返し
   ます。文書文字列にはHTMLマークアップが含まれます

イントロスペクション用のメソッドは、PHP・C・Microsoft .NETのサーバなどで サポートされています。UserLand
Frontierの最近のバージョンでもイントロス ペクションを部分的にサポートしています。Perl, Python, Javaでのイントロス
ペクションサポートについては `XML-RPC Hacks
<http://xmlrpc-c.sourceforge.net/hacks.php>`_を参照してください。


.. _boolean-objects:

Boolean オブジェクト
--------------------

このクラスは全てのPythonの値で初期化することができ、生成されるインスタン スは指定した値の真偽値によってのみ決まります。Booleanという名前から想像
される通りに各種のPython演算子を実装しており、:meth:`__cmp__`, :meth:`__repr__`, :meth:`__int__`,
:meth:`__nonzero__`で定義さ れる演算子を使用することができます。

以下のメソッドは、主に内部的にアンマーシャル時に使用されます:


.. method:: Boolean.encode(out)

   出力ストリームオブジェクト ``out`` に、XML-RPCエンコーディングのBoolean値を出力します。


.. _datetime-objects:

DateTime オブジェクト
---------------------

このクラスは、エポックからの秒数、タプルで表現された時刻、ISO 8601形式の 時間/日付文字列、 :class:`datetime.datetime`、
:class:`datetime.date`または:class:`datetime.time` のインスタンス の何れかで初期化することができます。

このクラスには以下のメソッドがあり、 主にコードをマーシャル/アンマーシャルするための内部処理を行います。


.. method:: Binary.decode(string)

   文字列をインスタンスの新しい時間を示す値として指定します。


.. method:: Binary.encode(out)

   出力ストリームオブジェクト ``out`` に、XML-RPCエンコーディングの :class:`DateTime`値を出力します。

また、:meth:`__cmp__`と:meth:`__repr__`で定義される演算子を使用するこ とができます。


.. _binary-objects:

Binary オブジェクト
-------------------

このクラスは、文字列(NULを含む)で初期化することができます。 :class:`Binary`の内容は、属性で参照します。


.. attribute:: Binary.data

   :class:`Binary`インスタンスがカプセル化しているバイナリデータ。このデータ は8bitクリーンです。

以下のメソッドは、主に内部的にマーシャル/アンマーシャル時に使用されます:


.. method:: Binary.decode(string)

   指定されたbase64文字列をデコードし、インスタンスのデータとします。


.. method:: Binary.encode(out)

   バイナリ値をbase64でエンコードし、出力ストリームオブジェクト ``out`` に出力します。

また、:meth:`__cmp__`で定義される演算子を使用することができます。


.. _fault-objects:

Fault オブジェクト
------------------

:class:`Fault`オブジェクトは、XML-RPCのfaultタグの内容をカプセル化してお り、以下のメンバを持ちます:


.. attribute:: Fault.faultCode

   失敗のタイプを示す文字列。


.. attribute:: Fault.faultString

   失敗の診断メッセージを含む文字列。


.. _protocol-error-objects:

ProtocolError オブジェクト
--------------------------

:class:`ProtocolError`オブジェクトはトランスポート層で発生したエラー(URI で指定したサーバが見つからなかった場合に発生する404
'not found'など)の内 容を示し、以下のメンバを持ちます:


.. attribute:: ProtocolError.url

   エラーの原因となったURIまたはURL。


.. attribute:: ProtocolError.errcode

   エラーコード。


.. attribute:: ProtocolError.errmsg

   エラーメッセージまたは診断文字列。


.. attribute:: ProtocolError.headers

   エラーの原因となったHTTP/HTTPSリクエストを含む文字列。


MultiCall オブジェクト
----------------------

.. versionadded:: 2.4

遠隔のサーバに対する複数の呼び出しをひとつのリクエストにカプセル化
する方法は、`<http://www.xmlrpc.com/discuss/msgReader%241208>`_ で 示されています。


.. class:: MultiCall(server)

   巨大な (boxcar) メソッド呼び出しに使えるオブジェクトを作成します。 *server* には最終的に呼び出しを行う対象を指定します。 作成した
   MultiCall オブジェクトを使って呼び出しを行うと、 即座に*None* を返し、呼び出したい手続き名とパラメタに保存する だけに留まります。
   オブジェクト自体を呼び出すと、それまでに保存しておいたすべての 呼び出しを単一の``system.multicall`` リクエストの形で伝送します。
   呼び出し結果はジェネレータになります。このジェネレータにわたって イテレーションを行うと、個々の呼び出し結果を返します。

以下にこのクラスの使い方を示します。 ::

   multicall = MultiCall(server_proxy)
   multicall.add(2,3)
   multicall.get_address("Guido")
   add_result, address = multicall()


補助関数
--------


.. function:: boolean(value)

   Pythonの値を、XML-RPCのBoolean定数 ``True``または``False``に変換し ます。


.. function:: dumps(params[, methodname[,  methodresponse[, encoding[, allow_none]]]])

   *params* を XML-RPC リクエストの形式に変換します。 *methodresponse* が真の場合、XML-RPC
   レスポンスの形式に変換します。 *params* に指定できるのは、引数からなるタプルか :exc:`Fault` 例外クラスのインスタンスです。
   *methodresponse* が真の場合、単一の値だけを返します。従って、 *params* の長さも 1 でなければなりません。 *encoding*
   を指定した場合、生成される XML のエンコード方式に なります。デフォルトは UTF-8 です。 Python の :const:`None` は標準の
   XML-RPC には利用できません。 :const:`None` を使えるようにするには、*allow_none* を真に して、拡張機能つきにしてください。


.. function:: loads(data[, use_datetime])

   XML-RPC リクエストまたはレスポンスを ``(params, methodname)`` の形式をとる Python オブジェクトにします。
   *params* は引数のタプルです。*methodname* は 文字列で、パケット中にメソッド名がない場合には ``None`` に なります。
   例外条件を示す XML-RPC パケットの場合には、 :exc:`Fault` 例外 を送出します。
   *use_datetime*フラグは:class:`datetime.datetime`のオブジェクトとして 日付/時刻を表現する時に使用し、デフォルトでは
   false に設定されています。

   もし、 :class:`datetime.date`、:class:`datetime.time`の オブジェクトとともにXML-RPCを呼び出した場合は、
   内部で:class:`DateTime`のオブジェクトに変換され、 戻り値として:class:`datetime.datetime`のオブジェクトのみが返される
   ことに注意してください。

   .. versionchanged:: 2.5
      *use_datetime*フラグを追加.


.. _xmlrpc-client-example:

クライアントのサンプル
----------------------

::

   # simple test program (from the XML-RPC specification)
   from xmlrpclib import ServerProxy, Error

   # server = ServerProxy("http://localhost:8000") # local server
   server = ServerProxy("http://betty.userland.com")

   print server

   try:
       print server.examples.getStateName(41)
   except Error, v:
       print "ERROR", v

XML-RPCサーバにプロキシを経由して接続する場合、 カスタムトランスポートを定義する必要があります。 以下にNoboNoboが作成した例を示します:

.. % fill in original author's name if we ever learn it
.. % Example taken from http://lowlife.jp/nobonobo/wiki/xmlrpcwithproxy.html

::

   import xmlrpclib, httplib

   class ProxiedTransport(xmlrpclib.Transport):
       def set_proxy(self, proxy):
           self.proxy = proxy
       def make_connection(self, host):
           self.realhost = host
   	h = httplib.HTTP(self.proxy)
   	return h
       def send_request(self, connection, handler, request_body):
           connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))
       def send_host(self, connection, host):
           connection.putheader('Host', self.realhost)

   p = ProxiedTransport()
   p.set_proxy('proxy-server:8080')
   server = xmlrpclib.Server('http://time.xmlrpc.com/RPC2', transport=p)
   print server.currentTime.getCurrentTime()

