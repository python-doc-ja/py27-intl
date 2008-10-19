
:mod:`asynchat` --- 非同期ソケット コマンド/レスポンス ハンドラ
===========================================

.. module:: asynchat
   :synopsis: 非同期コマンド/レスポンスプロトコルの開発サポート
.. moduleauthor:: Sam Rushing <rushing@nightmare.com>
.. sectionauthor:: Steve Holden <sholden@holdenweb.com>


:mod:`asynchat`を使うと、:mod:`asyncore`を基盤とした非同期な サーバ・クライアントをより簡単に開発する事ができます。
:mod:`asynchat`では、プロトコルの要素が任意の文字列で終了するか、ま たは可変長の文字列であるようなプロトコルを容易に制御できるようになってい
ます。:mod:`asynchat`は、抽象クラス:class:`async_chat`を定義してお
り、:class:`async_chat`を継承して:meth:`collect_incoming_data`メソッド
と:meth:`found_terminator`メソッドを実装すれば使うことができます。
:class:`async_chat`と:mod:`asyncore`は同じ非同期ループを使用してお
り、:class:`asyncore.dispatcher`も:class:`asynchat.async_chat`も同じチャネ
ルマップに登録する事ができます。通常、:class:`asyncore.dispatcher`はサー バチャネルとして使用し、リクエストの受け付け時に
:class:`asynchat.async_chat`オブジェクトを生成します。


.. class:: async_chat()

   このクラスは、:class:`asyncore.dispatcher`から継承した抽象クラスです。
   使用する際には:class:`async_chat`のサブクラスを作成し、
   :meth:`collect_incoming_data`と:meth:`found_terminator`を定義し
   なければなりません。:class:`asyncore.dispatcher`のメソッドを使用する事
   もできますが、メッセージ/レスポンス処理を中心に行う場合には使えないメ ソッドもあります。

   :class:`asyncore.dispatcher`と同様に、:class:`async_chat`も
   :cfunc:`select`呼出し後のソケットの状態からイベントを生成します。 ポーリングループ開始後、イベント処理フレームワークが自動的に
   :class:`async_chat`のメソッドを呼び出しますので、プログラマが処理を記述 する必要はありません。

   :class:`asyncore.dispatcher`と違い、:class:`async_chat`では *プロデューサ*の first-in-first-
   outキュー(fifo)を作成する事ができ ます。プロデューサは:meth:`more`メソッドを必ず持ち、このメソッドで
   チャネル上に送出するデータを返します。プロデューサが枯渇状態 (*i.e.* これ以上のデータを持たない状態)にある場合、
   :meth:`more`は空文字列を返します。この時、:class:`async_chat`は枯渇
   状態にあるプロデューサをfifoから除去し、次のプロデューサが存在すればそ のプロデューサを使用します。fifoにプロデューサが存在しない場合、
   :meth:`handle_write`は何もしません。リモート端点からの入力の終了や
   重要な中断点を検出する場合は、:meth:`set_terminator`に記述します。

   :class:`async_chat`のサブクラスでは、入力メソッド
   :meth:`collect_incoming_data`と:meth:`found_terminator`を定義
   し、チャネルが非同期に受信するデータを処理します。以下にメソッドの解説 を示します。


.. method:: async_chat.close_when_done()

   プロデューサfifoのトップに``None``をプッシュします。このプロデュー サがポップされると、チャネルがクローズします。


.. method:: async_chat.collect_incoming_data(data)

   チャネルが受信した不定長のデータを*data*に指定して呼び出されます。 このメソッドは必ずオーバライドする必要があり、デフォルトの実装では、
   :exc:`NotImplementedError` 例外を送出します。


.. method:: async_chat.discard_buffers()

   非常用のメソッドで、全ての入出力バッファとプロデューサfifoを廃棄します。


.. method:: async_chat.found_terminator()

   入力データストリームが、:meth:`set_terminator`で指定した終了条件と一
   致した場合に呼び出されます。このメソッドは必ずオーバライドする必要があ り、デフォルトの実装では、:exc:`NotImplementedError`
   例外を送出し ます。入力データを参照する必要がある場合でも引数としては与えられないた め、入力バッファをインスタンス属性として参照しなければなりません。


.. method:: async_chat.get_terminator()

   現在のチャネルの終了条件を返します。


.. method:: async_chat.handle_close()

   チャネル閉じた時に呼び出されます。デフォルトの実装では単にチャネルのソ ケットをクローズします。


.. method:: async_chat.handle_read()

   チャネルの非同期ループでreadイベントが発生した時に呼び出され、デフォル
   トの実装では、:meth:`set_terminator`で設定された終了条件をチェック します。終了条件として、特定の文字列か受信文字数を指定する事ができま
   す。終了条件が満たされている場合、:meth:`handle_read`は終了条件が成立
   するよりも前のデータを引数として:meth:`collect_incoming_data`を呼び
   出し、その後:meth:`found_terminator`を呼び出します。


.. method:: async_chat.handle_write()

   アプリケーションがデータを出力する時に呼び出され、デフォルトの実装では
   :meth:`initiate_send`を呼び出します。:meth:`initiate_send`では
   :meth:`refill_buffer`を呼び出し、チャネルのプロデューサfifoからデー タを取得します。


.. method:: async_chat.push(data)

   dataを持つ:class:`simple_producer`\ (*後述*)オブジェクトを生成し、チ
   ャネルの``producer_fifo``にプッシュして転送します。データをチャネル に書き出すために必要なのはこれだけですが、データの暗号化やチャンク化な
   どを行う場合には独自のプロデューサを使用する事もできます。


.. method:: async_chat.push_with_producer(producer)

   指定したプロデューサオブジェクトをチャネルのfifoに追加します。これより 前にpushされたプロデューサが全て枯渇した後、チャネルはこのプロデューサ
   から:meth:`more`メソッドでデータを取得し、リモート端点に送信しま す。


.. method:: async_chat.readable()

   :cfunc:`select`ループでこのチャネルの読み込み可能チェックを行う場 合には、``True``を返します。


.. method:: async_chat.refill_buffer()

   fifoの先頭にあるプロデューサの:meth:`more`メソッドを呼び出し、出力 バッファを補充します。先頭のプロデューサが枯渇状態の場合にはfifoからポ
   ップされ、その次のプロデューサがアクティブになります。アクティブなプロ デューサが``None``になると、チャネルはクローズされます。


.. method:: async_chat.set_terminator(term)

   チャネルで検出する終了条件を設定します。``term``は入力プロトコルデー タの処理方式によって以下の3つの型の何れかを指定します。

   +-----------+----------------------------------+
   | term      | 説明                               |
   +===========+==================================+
   | *string*  | 入力ストリーム中でstringが検出された時、          |
   |           | :meth:`found_terminator`を呼び出します。 |
   +-----------+----------------------------------+
   | *integer* | 指定された文字数が読み込まれた時、                |
   |           | :meth:`found_terminator`を呼び出します。 |
   +-----------+----------------------------------+
   | ``None``  | 永久にデータを読み込みます。                   |
   +-----------+----------------------------------+

   終了条件が成立しても、その後に続くデータは、 :meth:`found_terminator`の呼出し後に再びチャネルを読み込めば取得す る事ができます。


.. method:: async_chat.writable()

   Should return ``True`` as long as items remain on the producer fifo, or the
   channel is connected and the channel's output buffer is non-empty.

   プロデューサfifoが空ではないか、チャネルが接続中で出力バッファが空でな い場合、``True``を返します。


asynchat - 補助クラスと関数
-------------------


.. class:: simple_producer(data[, buffer_size=512])

   :class:`simple_producer`には、一連のデータと、オプションとしてバッファ
   サイズを指定する事ができます。:meth:`more`が呼び出されると、その都 度*buffer_size*以下の長さのデータを返します。


.. method:: simple_producer.more()

   プロデューサから取得した次のデータか、空文字列を返します。


.. class:: fifo([list=None])

   各チャネルは、アプリケーションからプッシュされ、まだチャネルに書き出さ
   れていないデータを:class:`fifo`に保管しています。:class:`fifo`では、必
   要なデータとプロデューサのリストを管理しています。引数*list*には、 プロデューサかチャネルに出力するデータを指定する事ができます。


.. method:: fifo.is_empty()

   fifoが空のとき``True``を返します。


.. method:: fifo.first()

   fifoに:meth:`push`されたアイテムのうち、最も古いアイテムを返します。


.. method:: fifo.push(data)

   データ(文字列またはプロデューサオブジェクト)をプロデューサfifoに追加します。


.. method:: fifo.pop()

   fifoが空でなければ、``(True, first())``を返し、ポップされたアイテム を削除します。fifoが空であれば``(False,
   None)``を返します。

:mod:`asynchat`は、ネットワークとテキスト分析操作で使えるユーティリテ ィ関数を提供しています。


.. function:: find_prefix_at_end(haystack, needle)

   文字列*haystack*の末尾が*needle*の先頭と一致したとき、``True`` を返します。


.. _asynchat-example:

asynchat 使用例
------------

以下のサンプルは、:class:`async_chat`でHTTPリクエストを読み込む処理の一部 です。Webサーバは、クライアントからの接続毎に
:class:`http_request_handler`オブジェクトを作成します。最初はチャネルの終
了条件に空行を指定してHTTPヘッダの末尾までを検出し、その後ヘッダ読み込み 済みを示すフラグを立てています。

ヘッダ読み込んだ後、リクエストの種類がPOSTであればデータが入力ストリーム に流れるため、``Content-
Length:``ヘッダの値を数値として終了条件に指定 し、適切な長さのデータをチャネルから読み込みます。

必要な入力データを全て入手したら、チャネルの終了条件に``None``を指定 して残りのデータを無視するようにしています。この後、
:meth:`handle_request`が呼び出されます。 ::

   class http_request_handler(asynchat.async_chat):

       def __init__(self, conn, addr, sessions, log):
           asynchat.async_chat.__init__(self, conn=conn)
           self.addr = addr
           self.sessions = sessions
           self.ibuffer = []
           self.obuffer = ""
           self.set_terminator("\r\n\r\n")
           self.reading_headers = True
           self.handling = False
           self.cgi_data = None
           self.log = log

       def collect_incoming_data(self, data):
           """Buffer the data"""
           self.ibuffer.append(data)

       def found_terminator(self):
           if self.reading_headers:
               self.reading_headers = False
               self.parse_headers("".join(self.ibuffer))
               self.ibuffer = []
               if self.op.upper() == "POST":
                   clen = self.headers.getheader("content-length")
                   self.set_terminator(int(clen))
               else:
                   self.handling = True
                   self.set_terminator(None)
                   self.handle_request()
           elif not self.handling:
               self.set_terminator(None) # browsers sometimes over-send
               self.cgi_data = parse(self.headers, "".join(self.ibuffer))
               self.handling = True
               self.ibuffer = []
               self.handle_request()

