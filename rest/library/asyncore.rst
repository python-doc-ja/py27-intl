
:mod:`asyncore` --- 非同期ソケットハンドラ
==========================================

.. module:: asyncore
   :synopsis: 非同期なソケット制御サービスのためのベースクラス
.. moduleauthor:: Sam Rushing <rushing@nightmare.com>
.. sectionauthor:: Christopher Petrilli <petrilli@amber.org>
.. sectionauthor:: Steve Holden <sholden@holdenweb.com>


このモジュールは、非同期ソケットサービスのクライアント・サーバを開発する ための基盤として使われます。

.. % Heavily adapted from original documentation by Sam Rushing.

CPUが一つしかない場合、プログラムが"二つのことを同時に"実行する方法は 二つしかありません。もっとも簡単で一般的なのはマルチスレッドを利用する方
法ですが、これとはまったく異なるテクニックで、一つのスレッドだけでマルチ スレッドと同じような効果を得られるテクニックがあります。このテクニックは
I/O処理が中心である場合にのみ有効で、CPU負荷の高いプログラムでは効果が無 く、この場合にはプリエンプティブなスケジューリングが可能なスレッドが有効
でしょう。しかし、多くの場合、ネットワークサーバではCPU負荷よりはIO負荷 が問題となります。

もしOSのI/Oライブラリがシステムコール :cfunc:`select` をサポートし
ている場合（ほとんどの場合はサポートされている）、I/O処理は"バックグラ ウンド"で実行し、その間に他の処理を実行すれば、複数の通信チャネルを同時
にこなすことができます。一見、この戦略は奇妙で複雑に思えるかもしれません が、いろいろな面でマルチスレッドよりも理解しやすく、制御も容易です。
:mod:`asyncore`は多くの複雑な問題を解決済みなので、洗練され、パフォー マンスにも優れたネットワークサーバとクライアントを簡単に開発することがで
きます。とくに、:mod:`asynchat`のような、対話型のアプリケーションや プロトコルには非常に有効でしょう。

基本的には、この二つのモジュールを使う場合は一つ以上のネットワーク *チャネル*を:class:`asyncore.dispatcher`クラス、または
:class:`asynchat.async_chat`のインスタンスとして作成します。作成されたチ
ャネルはグローバルマップに登録され、:func:`loop`関数で参照されま す。:func:`loop`には、専用のマップを渡す事も可能です。

チャネルを生成後、:func:`loop`を呼び出すとチャネル処理が開始し、最 後のチャネル（非同期処理中にマップに追加されたチャネルを含む）が閉じるま
で継続します。


.. function:: loop([timeout[, use_poll[, map[,count]]]])

   ポーリングループを開始し、count回が過ぎるか、全てのオープン済みチャ ネルがクローズされた場合のみ終了します。全ての引数はオプションです。
   引数*count*のデフォルト値はNoneで、ループは全てのチャネルがクロー ズされた場合のみ終了します。 引数*timeout*は
   :func:`select`または:func:`poll`の引数timeoutとして渡され、
   秒単位で指定します。デフォルト値は30秒です。引数*use_poll*が真のと
   き、:func:`select`ではなく:func:`poll`が使われます。デフォル ト値は``False``です。

   引数*map*には、監視するチャネルをアイテム として格納した辞書を指定します。*map*が省略された場合、グローバル なマップが使用されます。


.. class:: dispatcher()

   :class:`dispatcher`クラスは、低レベルソケットオブジェクトの薄いラッ パーです。便宜上、非同期ループから呼び出されるイベント処理メソッドを
   追加していますが、これ以外の点では、non-blockingなソケットと同様で す。

   :class:`dispatcher`クラスには二つのクラス属性があり、パフォーマンス向上 やメモリの削減のために更新する事ができます。


   .. data:: ac_in_buffer_size

      非同期入力バッファのサイズ(デフォルト ``4096``)


   .. data:: ac_out_buffer_size

      非同期出力バッファのサイズ(デフォルト ``4096``)

   非同期ループ内で低レベルイベントが発生した場合、発生のタイミングやコネ クションの状態から特定の高レベルイベントへと置き換えることができます。
   例えばソケットを他のホストに接続する場合、最初の書き込み可能イベントが 発生すれば接続が完了した事が分かります(この時点で、ソケットへの書き込
   みは成功すると考えられる)。このように判定できる高レベルイベントを以下 に示します：

   +----------------------+-----------------------------------------------------+
   | イベント             | 解説                                                |
   +======================+=====================================================+
   | ``handle_connect()`` | 最初にwriteイベントが発生した時                     |
   +----------------------+-----------------------------------------------------+
   | ``handle_close()``   | 読み込み可能なデータなしでreadイベントが発生 した時 |
   +----------------------+-----------------------------------------------------+
   | ``handle_accept()``  | listen中のソケットでreadイベントが発生した時        |
   +----------------------+-----------------------------------------------------+

   非同期処理中、マップに登録されたチャネルの:meth:`readable`メソッド
   と:meth:`writable`メソッドが呼び出され、:cfunc:`select`か
   :cfunc:`poll`でread/writeイベントを検出するリストに登録するか否か を判定します。

このようにして、チャネルでは低レベルなソケットイベントの種類より多くの種 類のイベントを検出する事ができます。以下にあげるイベントは、サブクラスで
オーバライドすることが可能です：


.. method:: dispatcher.handle_read()

   非同期ループで、チャネルのソケットの:meth:`read`メソッドの呼び出しが 成功した時に呼び出されます。


.. method:: dispatcher.handle_write()

   非同期ループで、書き込み可能ソケットが実際に書き込み可能になった時に呼 び出される。このメソッドは、パフォーマンスの向上のためバッファリングを
   行う場合などに利用できます。例：  ::

      def handle_write(self):
          sent = self.send(self.buffer)
          self.buffer = self.buffer[sent:]


.. method:: dispatcher.handle_expt()

   out of band (OOB)データが検出された時に呼び出されます。OOBはあまりサポー
   トされておらず、また滅多に使われないので、:meth:`handle_expt`が呼び 出されることはほとんどありません。


.. method:: dispatcher.handle_connect()

   ソケットの接続が確立した時に呼び出されます。"welcome"バナーの送信、プ ロトコルネゴシエーションの初期化などを行います。

   .. % ちょっと手抜き...


.. method:: dispatcher.handle_close()

   ソケットが閉じた時に呼び出されます。


.. method:: dispatcher.handle_error()

   捕捉されない例外が発生した時に呼び出されます。デフォルトでは、短縮したト レースバック情報が出力されます。


.. method:: dispatcher.handle_accept()

   listen中のチャネルがリモートホストからの:meth:`connect`で接続され、 接続が確立した時に呼び出されます。

   .. % 手抜き...


.. method:: dispatcher.readable()

   非同期ループ中に呼び出され、readイベントの監視リストに加えるか否かを決 定します。デフォルトのメソッドでは``True``を返し、readイベントの発
   生を監視します。


.. method:: dispatcher.writable()

   非同期ループ中に呼び出され、writeイベントの監視リストに加えるか否かを 決定します。デフォルトのメソッドでは``True``を返し、writeイベントの
   発生を監視します。

さらに、チャネルにはソケットのメソッドとほぼ同じメソッドがあり、チャネル はソケットのメソッドの多くを委譲・拡張しており、ソケットとほぼ同じメソッ
ドを持っています。


.. method:: dispatcher.create_socket(family, type)

   引数も含め、通常のソケット生成と同じ。:mod:`socket`モジュールを参 照のこと。


.. method:: dispatcher.connect(address)

   通常のソケットオブジェクトと同様、*address*には一番目の値が接続先 ホスト、2番目の値がポート番号であるタプルを指定します。


.. method:: dispatcher.send(data)

   リモート側の端点に*data*を送出します。


.. method:: dispatcher.recv(buffer_size)

   リモート側の端点より、最大*buffer_size*バイトのデータを読み込みま す。長さ0の文字列が返ってきた場合、チャネルはリモートから切断された事
   を示します。


.. method:: dispatcher.listen(backlog)

   ソケットへの接続を待つ。引数*backlog*は、キューイングできるコネク ションの最大数を指定します(1以上)。最大数はシステムに依存でします（通 常は5)


.. method:: dispatcher.bind(address)

   ソケットを*address*にバインドします。ソケットはバインド済みであっ てはなりません。(*address*の形式は、アドレスファミリに依存します。
   :mod:`socket`モジュールを参照のこと。)


.. method:: dispatcher.accept()

   接続を受け入れます。ソケットはアドレスにバインド済みであり、 :meth:`listen`で接続待ち状態でなければなりません。戻り値は ``(conn,
   address)``のペアで、*conn*はデータの送受信 を行うソケットオブジェクト、*address*は接続先ソケットがバインドさ れているアドレスです。


.. method:: dispatcher.close()

   ソケットをクローズします。以降の全ての操作は失敗します。リモート端点で は、キューに溜まったデータ以外、これ以降のデータ受信は行えません。ソケ
   ットはガベージコレクト時に自動的にクローズされます。


.. _asyncore-example:

asyncoreの例：簡単なHTTPクライアント
------------------------------------

基本的なサンプルとして、以下に非常に単純なHTTPクライアントを示します。こ
のHTTPクライアントは:class:`dispatcher`クラスでソケットを利用しています。 ::

   import asyncore, socket

   class http_client(asyncore.dispatcher):

       def __init__(self, host, path):
           asyncore.dispatcher.__init__(self)
           self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
           self.connect( (host, 80) )
           self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path

       def handle_connect(self):
           pass

       def handle_close(self):
           self.close()

       def handle_read(self):
           print self.recv(8192)

       def writable(self):
           return (len(self.buffer) > 0)

       def handle_write(self):
           sent = self.send(self.buffer)
           self.buffer = self.buffer[sent:]

   c = http_client('www.python.org', '/')

   asyncore.loop()

