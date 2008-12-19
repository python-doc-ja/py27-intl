
:mod:`SocketServer` --- ネットワークサーバ構築のための フレームワーク
=====================================================================

.. module:: SocketServer
   :synopsis: ネットワークサーバ構築のためのフレームワーク。


:mod:`SocketServer` モジュールはネットワークサーバを実装するタスクを 単純化します。

このモジュールには 4 つのサーバクラスがあります: :class:`TCPServer` は、クライアントとサーバ間に継続的なデータ流路を提供
する、インターネット TCP プロトコルを使います。 :class:`UDPServer` は、順序通りに到着しなかったり、転送中に喪失して
しまってもかまわない情報の断続的なパケットである、データグラムを使います。 :class:`UnixStreamServer` および
:class:`UnixDatagramServer` クラスも 同様ですが、Unix ドメインソケットを使います; 従って非 Unix
プラットフォームでは利用できません。ネットワークプログラミングに ついての詳細は、W. Richard Steven 著 UNIX Network
Programming や、 Ralph Davis 著 Win32 Network Programming のような 書籍を参照してください。

これらの 4 つのクラスは要求を :dfn:`同期的に (synchronously)` 処理します;
各要求は次の要求を開始する前に完結していなければなりません。 同期的な処理は、サーバで大量の計算を必要とする、あるいはクライアントが
処理するには時間がかかりすぎるような大量のデータを返す、といった理由に よってリクエストに長い時間がかかる状況には向いていません。
こうした状況の解決方法は別のプロセスを生成するか、個々の要求を 扱うスレッドを生成することです;  :class:`ForkingMixIn` および
:class:`ThreadingMixIn` 配合クラス (mix-in classes) を使えば、非同期的な動作をサポートできます。

サーバの作成にはいくつかのステップがあります。最初に、 :class:`BaseRequestHandler` クラスをサブクラス化して 要求処理クラス
(request hander class) を生成し、その :meth:`handle` メソッドを上書きしなければなりません; このメソッドで入力される
要求を処理します。次に、サーバクラスのうち一つをインスタンス化して、 サーバのアドレスと要求処理クラスを渡さなければなりません。最後に、 サーバオブジェクトの
:meth:`handle_request` または  :meth:`serve_forever` メソッドを呼び出して、単一または多数の 要求を処理します。

:class:`ThreadingMixIn` から継承してスレッドを利用した接続を行う場合、 突発的な通信切断時の処理を明示的に指定する必要があります。
:class:`ThreadingMixIn` クラスには *daemon_threads* 属性があり、
サーバがスレッドの終了を待ち合わせるかどうかを指定する事ができます。 スレッドが独自の処理を行う場合は、このフラグを明示的に指定します。
デフォルトは:const:`False`で、Pythonは:class:`ThreadingMixIn`クラス
が起動した全てのスレッドが終了するまで実行し続けます。

サーバクラス群は使用するネットワークプロトコルに関わらず、同じ外部 メソッドおよび属性を持ちます:


サーバ生成に関するノート
------------------------

継承図にある五つのクラスのうち四つは四種類の同期サーバを表わしています。 ::

   +------------+
   | BaseServer |
   +------------+
         |
         v
   +-----------+        +------------------+
   | TCPServer |------->| UnixStreamServer |
   +-----------+        +------------------+
         |
         v
   +-----------+        +--------------------+
   | UDPServer |------->| UnixDatagramServer |
   +-----------+        +--------------------+

:class:`UnixDatagramServer` は :class:`UDPServer` から派生していて、
:class:`UnixStreamServer` からではないことに注意してください --- IP と Unix
ストリームサーバの唯一の違いはアドレスファミリーで それは両方の Unix サーバクラスで単純に繰り返されています。

それぞれのタイプのサーバのフォークしたりスレッド実行したりするバージョンは :class:`ForkingMixIn` および
:class:`ThreadingMixIn` ミクシン(mix-in)クラスを使って 作ることができます。たとえば、スレッド実行する UDP
サーバクラスは以下のようにして 作られます。 ::

   class ThreadingUDPServer(ThreadingMixIn, UDPServer): pass

ミクシンクラスは :class:`UDPServer` で定義されるメソッドをオーバライドするために、
先に来なければなりません。様々なメンバ変数を設定することで元になるサーバ機構の 振る舞いを変えられます。

サービスの実装には、:class:`BaseRequestHandler` からクラスを派生させて その :meth:`handle`
メソッドを再定義しなければなりません。このようにすれば、 サーバクラスと要求処理クラスを結合して様々なバージョンのサービスを
実行することができます。要求処理クラスはデータグラムサービスかストリームサービスかで 異なることでしょう。この違いは処理サブクラス
:class:`StreamRequestHandler` または :class:`DatagramRequestHandler`
を使うという形で隠蔽できます。

もちろん、まだ頭を使わなければなりません! たとえば、サービスがリクエストによっては
書き換えられるようなメモリ上の状態を使うならば、フォークするサーバを使うのは馬鹿げています。
というのも子プロセスでの書き換えは親プロセスで保存されている初期状態にも 親プロセスから分配される各子プロセスの状態にも届かないからです。この場合、
スレッド実行するサーバを使うことはできますが、共有データの一貫性を保つために ロックを使わなければならなくなるでしょう。

一方、全てのデータが外部に(たとえばファイルシステムに)保存される HTTP サーバを
作っているのだとすると、同期クラスではどうしても一つの要求が処理されている間 サービスが「耳の聞こえない」状態を呈することになります --- この状態はもし
クライアントが要求した全てのデータをゆっくり受け取るととても長い時間続きかねません。 こういう場合にはサーバをスレッド実行したりフォークすることが適切です。

ある場合には、要求の一部を同期的に処理する一方で、要求データに依って子プロセスを
フォークして処理を終了させる、といった方法も適当かもしれません。こうした処理方法 は同期サーバを使って要求処理クラスの :meth:`handle`
メソッドの中で自分で フォークするようにして実装することができます。

スレッドも :func:`fork` もサポートされない環境で (もしくはサービスにとってそれらがあまりに高価についたり不適切な場合に)
多数の同時要求を捌くもう一つのアプローチは、部分的に処理し終えた要求のテーブルを 自分で管理し、次にどの要求に対処するか
(または新しく入ってきた要求を扱うかどうか)を決めるのに :func:`select` を使う方法です。
これは(もしスレッドやサブプロセスが使えなければ)特にストリームサービスに対して重要で、 そのようなサービスでは各クライアントが潜在的に長く接続し続けます。

.. % XXX should data and methods be intermingled, or separate?
.. % how should the distinction between class and instance variables be
.. % drawn?


Serverオブジェクト
------------------


.. function:: fileno()

   サーバが要求待ちを行っているソケットのファイル記述子を整数で返します。 この関数は一般的に、同じプロセス中の複数のサーバを監視できるように するために、
   :func:`select.select` に渡されます。


.. function:: handle_request()

   単一の要求を処理します。この関数は以下のメソッド: :meth:`get_request`、 :meth:`verify_request`、および
   :meth:`process_request` を順番に呼び出します。 ハンドラ中でユーザによって提供された :meth:`handle` が例外
   を送出した場合、サーバの :meth:`handle_error` メソッドが 呼び出されます。


.. function:: serve_forever()

   無限個の要求を処理します。この関数は単に無限ループ内で :meth:`handle_request` を呼び出します。


.. data:: address_family

   サーバのソケットが属しているプロトコルファミリです。 取りえる値は :const:`socket.AF_INET` および
   :const:`socket.AF_UNIX`  です。


.. data:: RequestHandlerClass

   ユーザが提供する要求処理クラスです; 要求ごとにこのクラスのインスタンス が生成されます。


.. data:: server_address

   サーバが要求待ちを行うアドレスです。アドレスの形式はプロトコルファミリ によって異なります。詳細は :mod:`socket` モジュールを参照してください。
   インターネットプロトコルでは、この値は例えば``('127.0.0.1', 80)``の ようにアドレスを与える文字列と整数のポート番号を含むタプルです。


.. data:: socket

   サーバが入力の要求待ちを行うためのソケットオブジェクトです。

サーバクラスは以下のクラス変数をサポートします:

.. % XXX should class variables be covered before instance variables, or
.. % vice versa?


.. data:: allow_reuse_address

   サーバがアドレスの再使用を許すかどうかを示す値です。この値は標準 で :const:`False` で、サブクラスで再使用ポリシを変更するために
   設定することができます。


.. data:: request_queue_size

   要求待ち行列 (queue) のサイズです。単一の要求を処理するのに長時間 かかる場合には、サーバが処理中に届いた要求は最大
   :attr:`request_queue_size` 個まで待ち行列に置かれます。 待ち行列が一杯になると、それ以降のクライアントからの要求は "接続拒否
   (Connection denied)" エラーになります。標準の値は 通常 5 ですが、この値はサブクラスで上書きすることができます。


.. data:: socket_type

   サーバが使うソケットの型です; 取りえる値は 2 つで、 :const:`socket.SOCK_STREAM` と
   :const:`socket.SOCK_DGRAM` です。

:class:`TCPServer` のような基底クラスのサブクラスで上書きできる サーバメソッドは多数あります; これらのメソッドはサーバオブジェクトの
外部のユーザにとっては役にたたないものです。

.. % should the default implementations of these be documented, or should
.. % it be assumed that the user will look at SocketServer.py?


.. function:: finish_request()

   :attr:`RequestHandlerClass` をインスタンス化し、:meth:`handle` メソッドを呼び出して、実際に要求を処理します。


.. function:: get_request()

   ソケットから要求を受理して、 クライアントとの通信に使われる *新しい* ソケットオブジェクト、およびクライアントのアドレスからなる、 2
   要素のタプルを返します。


.. function:: handle_error(request, client_address)

   この関数は :attr:`RequestHandlerClass` の :meth:`handle`
   メソッドが例外を送出した際に呼び出されます。標準の動作では 標準出力へトレースバックを出力し、後続する要求を継続して処理します。


.. function:: process_request(request, client_address)

   :meth:`finish_request` を呼び出して、:meth:`RequestHandlerClass`
   のインスタンスを生成します。必要なら、この関数から 新たなプロセスかスレッドを生成して要求を処理することができます; その処理は
   :class:`ForkingMixIn` または :class:`ThreadingMixIn`  クラスが行います。

.. % Is there any point in documenting the following two functions?
.. % What would the purpose of overriding them be: initializing server
.. % instance variables, adding new network families?


.. function:: server_activate()

   サーバのコンストラクタによって呼び出され、サーバを活動状態に します。デフォルトではサーバのソケットを :meth:`listen` するだけです。
   このメソッドは上書きできます。


.. function:: server_bind()

   サーバのコンストラクタによって呼び出され、適切なアドレスにソケットを バインドします。 このメソッドは上書きできます。


.. function:: verify_request(request, client_address)

   ブール値を返さなければなりません; 値が:const:`True`の場合には要求が処理され、 :const:`False`の場合には要求は拒否されます。
   サーバへのアクセス制御を実装するためにこの関数を上書きすることが できます。標準の実装では常に:const:`True`を返します。


RequestHandlerオブジェクト
--------------------------

要求処理クラスでは、新たな :meth:`handle` メソッドを定義 しなくてはならず、また以下のメソッドのいずれかを上書きすることができます。
各要求ごとに新たなインスタンスが生成されます。


.. function:: finish()

   :meth:`handle` メソッドが呼び出された後、何らかの後始末を行うために 呼び出されます。標準の実装では何も行いません。:meth:`setup`
   または :meth:`handle` が例外を送出した場合には、この関数は呼び出されません。


.. function:: handle()

   この関数では、クライアントからの要求を実現するために必要な全ての作業を 行わなければなりません。デフォルト実装では何もしません。
   この作業の上で、いくつかのインスタンス属性を 利用することができます; クライアントからの要求は :attr:`self.request` です;
   クライアントのアドレスは :attr:`self.client_address` です;  そしてサーバごとの情報にアクセスする場合には、サーバインスタンスを
   :attr:`self.server` で取得できます。

   :attr:`self.request` の型はサービスがデータグラム型かストリーム型かで
   異なります。ストリーム型では、:attr:`self.request` はソケットオブジェクト です;
   データグラムサービスでは、:attr:`self.request` は文字列になります。
   しかし、この違いは要求処理サブクラスの:class:`StreamRequestHandler` や
   :class:`DatagramRequestHandler`を使うことで隠蔽することができます。 これらのクラスでは :meth:`setup` および
   :meth:`finish` メソッド を上書きしており、:attr:`self.rfile` および :attr:`self.wfile` 属性を
   提供しています。 :attr:`self.rfile` および :attr:`self.wfile` は、要求データを取得したり
   クライアントにデータを返すために、それぞれ読み出し、書き込みを行うことが できます。


.. function:: setup()

   :meth:`handle`   メソッドより前に呼び出され、何らかの必要な 初期化処理を行います。標準の実装では何も行いません。

