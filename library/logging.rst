
:mod:`logging` --- Python 用ロギング機能
========================================

.. module:: logging
   :synopsis: アプリケーションのための、柔軟なエラーロギングシステム


.. moduleauthor:: Vinay Sajip <vinay_sajip@red-dove.com>
.. sectionauthor:: Vinay Sajip <vinay_sajip@red-dove.com>


.. index:: pair: Errors; logging

.. versionadded:: 2.3

このモジュールでは、アプリケーションのための柔軟なエラーログ記録 (logging) システムを実装するための関数やクラスを定義しています。

ログ記録は :class:`Logger` クラスのインスタンス (以降 :dfn:`ロガー` :logger)
におけるメソッドを呼び出すことで行われます。各インスタンスは名前をもち、ドット (ピリオド) を区切り文字として表記することで、
概念的には名前空間中の階層構造に配置されることになります。例えば、"scan" と名づけられたロガーは "scan.text"、"scan.html"、
および "scan.pdf" ロガーの親ロガーとなります。ロガー名には何をつけてもよく、ログに記録されるメッセージの生成元となるアプリケーション中の特定の
領域を示すことになります。

ログ記録されたメッセージにはまた、重要度レベル (level of importance) が関連付けられています。デフォルトのレベルとして提供されているものは
:const:`DEBUG` 、 :const:`INFO` 、 :const:`WARNING` 、 :const:`ERROR` および
:const:`CRITICAL` です。簡便性のために、 :class:`Logger` の適切なメソッド群を呼ぶことで、ログに記録されたメッセージの
重要性を指定することができます。それらのメソッドとは、デフォルトのレベルを反映する形で、 :meth:`debug` 、 :meth:`info` 、
:meth:`warning` 、 :meth:`error` および :meth:`critical` となっています。
これらのレベルを指定するにあたって制限はありません: :class:`Logger` のより汎用的なメソッドで、明示的なレベル指定のための引数を持つ
:meth:`log` を使って自分自身でレベルを定義したり使用したりできます。

ログレベルの数値は以下の表のように与えられています。これらは基本的に自分でレベルを定義したい人のためのもので、
定義するレベルを既存のレベルの間に位置づけるために具体的な値が必要になります。もし数値が他のレベルと同じだったら、既存の値は上書きされその名前は失われます。

+--------------+------+
| レベル       | 数値 |
+==============+======+
| ``CRITICAL`` | 50   |
+--------------+------+
| ``ERROR``    | 40   |
+--------------+------+
| ``WARNING``  | 30   |
+--------------+------+
| ``INFO``     | 20   |
+--------------+------+
| ``DEBUG``    | 10   |
+--------------+------+
| ``NOTSET``   | 0    |
+--------------+------+

レベルもロガーに関連付けることができ、デベロッパが設定することも、保存されたログ記録設定を読み込む際に設定することもできます。
ロガーに対してログ記録メソッドが呼び出されると、ロガーは自らのレベルとメソッド呼び出しに関連付けられたレベルを比較します。
ロガーのレベルがメソッド呼び出しのレベルよりも高い場合、実際のログメッセージは生成されません。これはログ出力の冗長性を制御するための基本的なメカニズムです。

ログ記録されるメッセージは :class:`LogRecord` クラスのインスタンスとして
コード化されます。ロガーがあるイベントを実際にログ出力すると決定した場合、ログメッセージから :class:`LogRecord`
インスタンスが生成されます。

ログ記録されるメッセージは、ハンドラ (:dfn:`handlers`) を通して、処理機構 (dispatch mechanism)
にかけられます。ハンドラは :class:`Handler` クラスのサブクラスのインスタンスで、ログ記録された (:class:`LogRecord`
形式の) メッセージが、そのメッセージの伝達対象となる相手  (エンドユーザ、サポートデスクのスタッフ、システム管理者、開発者)
に行き着くようにする役割を持ちます。ハンドラには特定の行き先に方向付けられた :class:`LogRecord` インスタンスが渡されます。各ロガーは
ゼロ個、単一またはそれ以上のハンドラを (:class:`Logger` の :meth:`addHandler` メソッド) で関連付けることができます。
ロガーに直接関連付けられたハンドラに加えて、 *ロガーの上位にあるロガー全てに関連付けられたハンドラ* がメッセージを処理する際に呼び出されます。

ロガーと同様に、ハンドラは関連付けられたレベルを持つことができます。ハンドラのレベルはロガーのレベルと同じ方法で、フィルタとして働きます。
ハンドラがあるイベントを実際に処理すると決定した場合、 :meth:`emit` メソッドが使われ、メッセージを発送先に送信します。ほとんどのユーザ定義の
:class:`Handler` のサブクラスで、この :meth:`emit` をオーバライドする必要があるでしょう。

基底クラスとなる :class:`Handler` クラスに加えて、多くの有用なサブクラスが提供されています:

#. :class:`StreamHandler` のインスタンスはストリーム (ファイル様オブジェクト) にエラーメッセージを送信します。

#. :class:`FileHandler` のインスタンスはディスク上のファイルにエラーメッセージを送信します。

#. :class:`BaseRotatingHandler` はログファイルをある時点で交替させる
   ハンドラの基底クラスです。直接インスタンス化するためのクラスではありません。 :class:`RotatingFileHandler`
   や :class:`TimedRotatingFileHandler` を使うようにしてください。

#. :class:`RotatingFileHandler` のインスタンスは最大ログファイルの
   サイズ指定とログファイルの交替機能をサポートしながら、ディスク上のファイルにエラーメッセージを送信します。

#. :class:`TimedRotatingFileHandler` のインスタンスは、ログファイルを
   一定時間間隔ごとに交替しながら、ディスク上のファイルにエラーメッセージを送信します。

#. :class:`SocketHandler` のインスタンスは TCP/IP ソケットにエラーメッセージを送信します。

#. :class:`DatagramHandler` のインスタンスは UDP ソケットにエラーメッセージを送信します。

#. :class:`SMTPHandler` のインスタンスは指定された電子メールアドレスにエラーメッセージを送信します。

#. :class:`SysLogHandler` のインスタンスは遠隔を含むマシン上の syslog デーモンにエラーメッセージを送信します。

#. :class:`NTEventLogHandler` のインスタンスは Windows NT/2000/XP イベントログにエラーメッセージを送信します。

#. :class:`MemoryHandler` のインスタンスはメモリ上のバッファにエラーメッセージを送信し、指定された条件でフラッシュされるようにします。

#. :class:`HTTPHandler` のインスタンスは ``GET`` か ``POST`` セマンティクスを使って HTTP
   サーバにエラーメッセージを送信します。

:class:`StreamHandler` および :class:`FileHandler` クラスは、中核となる
ログ化機構パッケージ内で定義されています。他のハンドラはサブモジュール、 :mod:`logging.handlers` で定義されています。
(サブモジュールにはもうひとつ :mod:`logging.config` があり、これは環境設定機能のためのものです。)

ログ記録されたメッセージは :class:`Formatter` クラスのインスタンスを介し、表示用に書式化されます。これらのインスタンスは %
演算子と辞書を使うのに適した書式化文字列で初期化されます。

複数のメッセージの初期化をバッチ処理するために、 :class:`BufferingFormatter` のインスタンスを使うことができます。書式化文字列
(バッチ処理で各メッセージに適用されます) に加えて、ヘッダ (header) およびトレイラ (trailer) 書式化文字列が用意されています。

ロガーレベル、ハンドラレベルの両方または片方に基づいたフィルタリングが十分でない場合、 :class:`Logger` および :class:`Handler`
インスタンスに :class:`Filter` のインスタンスを (:meth:`addFilter` メソッドを介して)
追加することができます。メッセージの処理を進める前に、ロガーとハンドラはともに、全てのフィルタでメッセージの処理が許可されているか調べます。
いずれかのフィルタが偽となる値を返した場合、メッセージの処理は行われません。

基本的な :class:`Filter` 機能では、指定されたロガー名でフィルタを行えるようになっています。この機能が利用された場合、名前付けされた
ロガーとその下位にあるロガーに送られたメッセージがフィルタを通過できるようになり、その他のメッセージは捨てられます。

上で述べたクラスに加えて、いくつかのモジュールレベルの関数が存在します。


.. function:: getLogger([name])

   指定された名前のロガーを返します。名前が指定されていない場合、ロガー階層のルート (root) にあるロガーを返します。 *name*
   を指定する場合には、通常は *"a"*, *"a.b"*,  あるいは *"a.b.c.d"* といったようなドット区切りの階層的な
   名前にします。名前の付け方はログ機能を使う開発者次第です。

   与えられた名前に対して、この関数はどの呼び出しでも同じロガーインスタンスを返します。従って、ロガーインスタンスをアプリケーションの各部
   でやりとりする必要はなくなります。


.. function:: getLoggerClass()

   標準の :class:`Logger` クラスか、最後に :func:`setLoggerClass` に渡した
   クラスを返します。この関数は、新たに定義するクラス内で呼び出し、カスタマイズした :class:`Logger` クラスのインストールを行うときに
   既に他のコードで適用したカスタマイズを取り消そうとしていないか確かめるのに使います。例えば以下のようにします::

      class MyLogger(logging.getLoggerClass()):
          # ... override behaviour here


.. function:: debug(msg[, *args[, **kwargs]])

   レベル :const:`DEBUG` のメッセージをルートロガーで記録します。 *msg* はメッセージの書式化文字列で、 *args* は *msg* に
   文字列書式化演算子を使って取り込むための引数です。(これは、書式化文字列でキーワードを使い引数に辞書を渡すことができる、ということを意味します。)

   キーワード引数 *kwargs* からは二つのキーワードが調べられます。一つめは *exc_info* で、この値の評価値が偽でない場合、
   例外情報をログメッセージに追加します。(:func:`sys.exc_info`  の返す形式の) 例外情報を表すタプルが与えられていれば、それを
   メッセージに使います。それ以外の場合には、 :func:`sys.exc_info`  を呼び出して例外情報を取得します。

   もう一つのキーワード引数は *extra* で、当該ログイベント用に作られた LogRecoed の __dict__
   にユーザー定義属性を増やすのに使われる辞書を渡すのに用いられます。これらの属性は好きなように使えます。たとえば、ログメッセージの一部に
   することもできます。以下の例を見てください::

      FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
      logging.basicConfig(format=FORMAT)
      d = { 'clientip' : '192.168.0.1', 'user' : 'fbloggs' }
      logging.warning("Protocol problem: %s", "connection reset", extra=d)

   出力はこのようになります。  ::

      2006-02-08 22:20:02,165 192.168.0.1 fbloggs  Protocol problem: connection reset

   *extra* で渡される辞書のキーはロギングシステムで使われているものとぶつからない
   ようにしなければなりません。(どのキーがロギングシステムで使われているかについての詳細は :class:`Formatter`
   のドキュメントを参照してください。)

   これらの属性をログメッセージに使うことにしたなら、少し注意が必要です。上の例では、'clientip' と 'user' が LogRecord
   の属性辞書に含まれていることを期待した書式化文字列で :class:`Formatter` はセットアップされてい
   ます。これらの属性が欠けていると、書式化例外が発生してしまうためメッセージはログに残りません。したがってこの場合、常にこれらのキーがある *extra*
   辞書を渡す必要があります。

   このようなことは煩わしいかもしれませんが、この機能は限定された場面で使われるように意図しているものなのです。たとえば同じコードがいくつものコ
   ンテキストで実行されるマルチスレッドのサーバで、興味のある条件が現れるのがそのコンテキストに依存している(上の例で言えば、リモートのクライアント IP
   アドレスや認証されたユーザ名など)、というような場合です。そういった場面では、それ用の :class:`Formatter` が特定の
   :class:`Handler` と共に使われるというのはよくあることです。

   .. versionchanged:: 2.5
      *extra* が追加されました.


.. function:: info(msg[, *args[, **kwargs]])

   レベル :const:`INFO` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。


.. function:: warning(msg[, *args[, **kwargs]])

   レベル :const:`WARNING` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。


.. function:: error(msg[, *args[, **kwargs]])

   レベル :const:`ERROR` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。


.. function:: critical(msg[, *args[, **kwargs]])

   レベル :const:`CRITICAL` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。


.. function:: exception(msg[, *args])

   レベル :const:`ERROR` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。
   例外情報はログメッセージに追加されます。このメソッドは例外ハンドラからのみ呼び出されます。


.. function:: log(level, msg[, *args[, **kwargs]])

   レベル :const:`level` のメッセージをルートロガーで記録します。その他の引数は :func:`debug` と同じように解釈されます。


.. function:: disable(lvl)

   全てのロガーに対して、ロガー自体のレベルに優先するような上書きレベル *lvl* を与えます。アプリケーション全体にわたって一時的にログ出力の
   頻度を押し下げる必要が生じた場合にはこの関数が有効です。


.. function:: addLevelName(lvl, levelName)

   内部辞書内でレベル *lvl* をテキスト *levelName* に関連付けます。これは例えば :class:`Formatter`
   でメッセージを書式化する際のように、数字のレベルをテキスト表現に対応付ける際に用いられます。この関数は自作のレベルを定義するために使うこともできます。
   使われるレベル対する唯一の制限は、レベルは正の整数でなくてはならず、メッセージの深刻さが上がるに従ってレベルの数も上がらなくてはならないということです。


.. function:: getLevelName(lvl)

   ログ記録レベル *lvl* のテキスト表現を返します。レベルが定義済みのレベル :const:`CRITICAL` 、 :const:`ERROR` 、
   :const:`WARNING` 、 :const:`INFO` 、あるいは :const:`DEBUG` のいずれかである場合、対応する文字列が返されます。
   :func:`addLevelName` を使ってレベルに名前を関連づけていた場合、 *lvl* に関連付けられていた名前が返されます。
   定義済みのレベルに対応する数値を指定した場合、レベルに対応した文字列表現を返します。そうでない場合、文字列 "Level %s" % lvl を返します。


.. function:: makeLogRecord(attrdict)

   属性が *attrdict* で定義された、新たな :class:`LogRecord`  インスタンスを生成して返します。この関数は pickle 化された
   :class:`LogRecord` 属性の辞書を作成し、ソケットを介して送信し、受信端で :class:`LogRecord`
   インスタンスとして再構成する際に便利です。


.. function:: makeLogRecord(attrdict)

   *attrdict* で属性を定義した、新しい :class:`LogRecord` インスタンスを返します。この関数は、逆 pickle 化された
   :class:`LogRecord` 属性辞書を  socket 越しに受け取り、受信端で :class:`LogRecord` インスタンスに再構築す
   る場合に有用です。


.. function:: basicConfig([**kwargs])

   デフォルトの :class:`Formatter` を持つ :class:`StreamHandler`
   を生成してルートロガーに追加し、ログ記録システムの基本的な環境設定を行います。関数
   :func:`debug` 、 :func:`info` 、 :func:`warning` 、 :func:`error` 、および :func:`critical`
   は、ルートロガーにハンドラが定義されていない場合に自動的に :func:`basicConfig`  を呼び出します。

   .. versionchanged:: 2.4
      以前は :func:`basicConfig` はキーワード引数をとりませんでした.

   以下のキーワード引数がサポートされます。

   +--------------+----------------------------------------------------------------------+
   | Format       | 説明                                                                 |
   +==============+======================================================================+
   | ``filename`` | StreamHandler ではなく指定された名前で FileHandler                   |
   |              | が作られます                                                         |
   +--------------+----------------------------------------------------------------------+
   | ``filemode`` | filename が指定されているとき、ファイルモードを指定します            |
   |              | (filemode が指定されない場合デフォルトは 'a' です)                   |
   +--------------+----------------------------------------------------------------------+
   | ``format``   | 指定された書式化文字列をハンドラで使います                           |
   +--------------+----------------------------------------------------------------------+
   | ``datefmt``  | 指定された日付/時刻の書式を使います                                  |
   +--------------+----------------------------------------------------------------------+
   | ``level``    | ルートロガーのレベルを指定されたものにします                         |
   +--------------+----------------------------------------------------------------------+
   | ``stream``   | 指定されたストリームを StreamHandler の初期化に使います。この引数は |
   |              | 'filename' と同時には使えないことに注意してください。                |
   |              | 両方が指定されたときには 'stream' は無視されます                     |
   +--------------+----------------------------------------------------------------------+


.. function:: shutdown()

   ログ記録システムに対して、バッファのフラッシュを行い、全てのハンドラを閉じることで順次シャットダウンを行うように告知します。


.. function:: setLoggerClass(klass)

   ログ記録システムに対して、ロガーをインスタンス化する際にクラス *klass* を使うように指示します。指定するクラスは引数として名前だけをとるようなメソッド
   :meth:`__init__` を定義していなければならず、 :meth:`__init__` では :meth:`Logger.__init__`
   を呼び出さなければなりません。典型的な利用法として、この関数は自作のロガーを必要とするようなアプリケーションにおいて、他のロガーが
   インスタンス化される前にインスタンス化されます。


.. seealso::

   :pep:`282` - A Logging System
      本機能を Python 標準ライブラリに含めるよう記述している提案書。

   `この :mod:`logging` パッケージのオリジナル <http://www.red-dove.com/python_logging.html>`_
      オリジナルの :mod:`logging` パッケージ。このサイトにあるバージョンのパッケージは、標準で :mod:`logging` パッケージを含まな
      いPython 1.5.2 と 2.1.x、2.2.xでも使用できます


Logger オブジェクト
-------------------

ロガーは以下の属性とメソッドを持ちます。ロガーを直接インスタンス化することはできず、常にモジュール関数
:func:`logging.getLogger(name)` を介してインスタンス化するので注意してください。


.. attribute:: Logger.propagate

   この値の評価結果が偽になる場合、ログ記録しようとするメッセージはこのロガーに渡されず、また子ロガーから上位の (親の) ロガーに
   渡されません。コンストラクタはこの属性を 1 に設定します。


.. method:: Logger.setLevel(lvl)

   このロガーの閾値を *lvl* に設定します。ログ記録しようとするメッセージで、 *lvl* よりも深刻でないものは無視されます。
   ロガーが生成された際、レベルは :const:`NOTSET` (これにより全てのメッセージについて、ロガーがルートロガーであれば処理される、
   そうでなくてロガーが非ルートロガーの場合には親ロガーに代行させる) に設定されます。ルートロガーは :const:`WARNING` レベル
   で生成されることに注意してください。

   「親ロガーに代行させる」という用語の意味は、もしロガーのレベルが NOTEST ならば、祖先ロガーの系列の中を NOTEST 以外のレベルの祖先を見つけるかルー
   トに到達するまで辿っていく、ということです。

   もし NOTEST 以外のレベルの祖先が見つかったなら、その祖先のレベルが祖先の探索を開始したロガーの実効レベルとして取り扱われ、ログイベントがどの
   ように処理されるかを決めるのに使われます。

   ルートに到達した場合、ルートのレベルが NOTEST ならば全てのメッセージは処理されます。そうでなければルートのレベルが実効レベルとして使われます。


.. method:: Logger.isEnabledFor(lvl)

   深刻さが *lvl* のメッセージが、このロガーで処理されることになっているかどうかを示します。このメソッドはまず、
   :func:`logging.disable(lvl)` で設定されるモジュールレベルの深刻さレベルを調べ、次にロガーの実効レベルを
   :meth:`getEffectiveLevel` で調べます。


.. method:: Logger.getEffectiveLevel()

   このロガーの実効レベルを示します。 :const:`NOTSET` 以外の値が :meth:`setLevel` で設定されていた場合、その値が返されます。
   そうでない場合、 :const:`NOTSET` 以外の値が見つかるまでロガーの階層をルートロガーの方向に追跡します。見つかった場合、その値が返されます。


.. method:: Logger.debug(msg[, *args[, **kwargs]])

   レベル :const:`DEBUG` のメッセージをこのロガーで記録します。 *msg* はメッセージの書式化文字列で、 *args* は *msg* に
   文字列書式化演算子を使って取り込むための引数です。(これは、書式化文字列でキーワードを使い引数に辞書を渡すことができる、ということを意味します。)

   キーワード引数 *kwargs* からは二つのキーワードが調べられます。一つめは *exc_info* で、この値の評価値が偽でない場合、
   例外情報をログメッセージに追加します。(:func:`sys.exc_info`  の返す形式の) 例外情報を表すタプルが与えられていれば、それを
   メッセージに使います。それ以外の場合には、 :func:`sys.exc_info`  を呼び出して例外情報を取得します。

   もう一つのキーワード引数は *extra* で、当該ログイベント用に作られた LogRecoed の __dict__
   にユーザー定義属性を増やすのに使われる辞書を渡すのに用いられます。これらの属性は好きなように使えます。たとえば、ログメッセージの一部に
   することもできます。以下の例を見てください::

      FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
      logging.basicConfig(format=FORMAT)
      d = { 'clientip' : '192.168.0.1', 'user' : 'fbloggs' }
      logger = logging.getLogger("tcpserver")
      logger.warning("Protocol problem: %s", "connection reset", extra=d)

   出力はこのようになります。  ::

      2006-02-08 22:20:02,165 192.168.0.1 fbloggs  Protocol problem: connection reset

   *extra* で渡される辞書のキーはロギングシステムで使われているものとぶつからない
   ようにしなければなりません。(どのキーがロギングシステムで使われているかについての詳細は :class:`Formatter`
   のドキュメントを参照してください。)

   これらの属性をログメッセージに使うことにしたなら、少し注意が必要です。上の例では、'clientip' と 'user' が LogRecord
   の属性辞書に含まれていることを期待した書式化文字列で :class:`Formatter` はセットアップされてい
   ます。これらの属性が欠けていると、書式化例外が発生してしまうためメッセージはログに残りません。したがってこの場合、常にこれらのキーがある *extra*
   辞書を渡す必要があります。

   このようなことは煩わしいかもしれませんが、この機能は限定された場面で使われるように意図しているものなのです。たとえば同じコードがいくつものコ
   ンテキストで実行されるマルチスレッドのサーバで、興味のある条件が現れるのがそのコンテキストに依存している(上の例で言えば、リモートのクライアント IP
   アドレスや認証されたユーザ名など)、というような場合です。そういった場面では、それ用の :class:`Formatter` が特定の
   :class:`Handler` と共に使われるというのはよくあることです。

   .. versionchanged:: 2.5
      *extra* が追加されました.


.. method:: Logger.info(msg[, *args[, **kwargs]])

   レベル :const:`INFO` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.warning(msg[, *args[, **kwargs]])

   レベル :const:`WARNING` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.error(msg[, *args[, **kwargs]])

   レベル :const:`ERROR` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.critical(msg[, *args[, **kwargs]])

   レベル :const:`CRITICAL` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.log(lvl, msg[, *args[, **kwargs]])

   整数で表したレベル *lvl* のメッセージをこのロガーで記録します。その他の引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.exception(msg[, *args])

   レベル :const:`ERROR` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。
   例外情報はログメッセージに追加されます。このメソッドは例外ハンドラからのみ呼び出されます。


.. method:: Logger.addFilter(filt)

   指定されたフィルタ *filt* をこのロガーに追加します。


.. method:: Logger.removeFilter(filt)

   指定されたフィルタ *filt* をこのロガーから除去します。


.. method:: Logger.filter(record)

   このロガーのフィルタをレコード (record) に適用し、レコードがフィルタを透過して処理されることになる場合には真を返します。


.. method:: Logger.addHandler(hdlr)

   指定されたハンドラ *hdlr* をこのロガーに追加します。


.. method:: Logger.removeHandler(hdlr)

   指定されたハンドラ *hdlr* をこのロガーから除去します。


.. method:: Logger.findCaller()

   呼び出し元のソースファイル名と行番号を調べます。ファイル名と行番号を 2 要素のタプルで返します。


.. method:: Logger.handle(record)

   レコードをこのロガーおよびその上位ロガーに (*propagate* の値が偽になるまで) さかのぼった関連付けられている全てのハンドラに渡して
   処理します。このメソッドはソケットから受信した逆 pickle 化されたレコードに対してもレコードがローカルで生成された場合と同様に用いられます。
   :meth:`filter` によって、ロガーレベルでのフィルタが適用されます。


.. method:: Logger.makeRecord(name, lvl, fn, lno, msg, args, exc_info, func, extra)

   このメソッドは、特殊な :class:`LogRecord` インスタンスを生成するためにサブクラスでオーバライドできるファクトリメソッドです。

   .. versionchanged:: 2.5
      *func* と *extra* が追加されました.


.. _minimal-example:

基本的な使い方
--------------

.. versionchanged:: 2.4
   以前は :func:`basicConfig` はキーワード引数をとりませんでした.

:mod:`logging` パッケージには高い柔軟性があり、その設定にたじろぐこともあるでしょう。そこでこの節では、 :mod:`logging`
パッケージを簡単に使う方法もあることを示します。

以下の最も単純な例では、コンソールにログを表示します::

   import logging

   logging.debug('A debug message')
   logging.info('Some information')
   logging.warning('A shot across the bows')

上のスクリプトを実行すると、以下のようなメッセージを目にするでしょう::

   WARNING:root:A shot across the bows

ここではロガーを特定しなかったので、システムはルートロガーを使っています。デバッグメッセージや情報メッセージは表示されませんが、これはデフォルトの
ルートロガーが WARNING 以上の重要度を持つメッセージしか処理しないように設定されているからです。
メッセージの書式もデフォルトの設定に従っています。出力先は ``sys.stderr`` で、これもデフォルトの設定です。
重要度レベルやメッセージの形式、ログの出力先は、以下の例のように簡単に変更できます::

   import logging

   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s %(levelname)s %(message)s',
                       filename='/tmp/myapp.log',
                       filemode='w')
   logging.debug('A debug message')
   logging.info('Some information')
   logging.warning('A shot across the bows')

ここでは、 :meth:`basicConfig` メソッドを使って、以下のような出力例になる (そして ``/tmp/myapp.log`` に書き込まれる)
ように、デフォルト設定を変更しています::

   2004-07-02 13:00:08,743 DEBUG A debug message
   2004-07-02 13:00:08,743 INFO Some information
   2004-07-02 13:00:08,743 WARNING A shot across the bows

今度は、重要度が DEBUG か、それ以上のメッセージが処理されました。メッセージの形式も変更され、出力はコンソールではなく特定のファイル
に書き出されました。

出力の書式化には、通常の Python 文字列に対する初期化を使います -  :ref:`typesseq-strings`
節を参照してください。書式化文字列は、以下の指定子 (specifier) を常にとります。指定子の完全なリストについては
:class:`Formatter` のドキュメントを参照してください。

+-------------------+------------------------------------------------------------------+
| 書式              | 説明                                                             |
+===================+==================================================================+
| ``%(name)s``      | ロガーの名前 (ログチャネル) の名前です。                         |
+-------------------+------------------------------------------------------------------+
| ``%(levelname)s`` | メッセージのログレベル (``'DEBUG'``, ``'INFO'``,                 |
|                   | ``'WARNING'``, ``'ERROR'``, ``'CRITICAL'``)                      |
|                   | です。                                                           |
+-------------------+------------------------------------------------------------------+
| ``%(asctime)s``   | :class:`LogRecord` が生成された際の時刻を、                      |
|                   | 人間が読み取れる形式にしたものです。デフォルトでは、 "2003-07-08 |
|                   | 16:49:45,896" のような形式 (コンマの後ろはミリ秒) です。         |
+-------------------+------------------------------------------------------------------+
| ``%(message)s``   | ログメッセージです。                                             |
+-------------------+------------------------------------------------------------------+

以下のように、追加のキーワードパラメタ *datefmt* を渡すと日付や時刻の書式を変更できます::

   import logging

   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s %(levelname)-8s %(message)s',
                       datefmt='%a, %d %b %Y %H:%M:%S',
                       filename='/temp/myapp.log',
                       filemode='w')
   logging.debug('A debug message')
   logging.info('Some information')
   logging.warning('A shot across the bows')

出力は以下のようになります::

   Fri, 02 Jul 2004 13:06:18 DEBUG    A debug message
   Fri, 02 Jul 2004 13:06:18 INFO     Some information
   Fri, 02 Jul 2004 13:06:18 WARNING  A shot across the bows

日付を書式化する文字列は、 :func:`strftime` の要求に従います -  :mod:`time` モジュールを参照してください。

コンソールやファイルではなく、別個に作成しておいたファイル類似オブジェクトにログを出力したい場合には、 :func:`basicConfig` に
*stream* キーワード引数で渡します。 *stream* と *filename*  の両方の引数を指定した場合、 *stream*
は無視されるので注意してください。

状況に応じて変化する情報ももちろんログ出力できます。以下のように、単にメッセージを書式化文字列にして、その後ろに可変情報の引数を渡すだけです::

   import logging

   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s %(levelname)-8s %(message)s',
                       datefmt='%a, %d %b %Y %H:%M:%S',
                       filename='/temp/myapp.log',
                       filemode='w')
   logging.error('Pack my box with %d dozen %s', 5, 'liquor jugs')

出力は以下のようになります::

   Wed, 21 Jul 2004 15:35:16 ERROR    Pack my box with 5 dozen liquor jugs


.. _multiple-destinations:

複数の出力先にログを出力する
----------------------------

コンソールとファイルに、別々のメッセージ書式で、別々の状況に応じたログ出力を行わせたいとしましょう。例えば DEBUG よりも高いレベルの
メッセージはファイルに記録し、INFO 以上のレベルのメッセージはコンソールに出力したいという場合です。また、ファイルにはタイムスタンプを
記録し、コンソールには出力しないとします。以下のようにすれば、こうした挙動を実現できます::

   import logging

   # set up logging to file - see previous section for more details
   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                       datefmt='%m-%d %H:%M',
                       filename='/temp/myapp.log',
                       filemode='w')
   # define a Handler which writes INFO messages or higher to the sys.stderr
   console = logging.StreamHandler()
   console.setLevel(logging.INFO)
   # set a format which is simpler for console use
   formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
   # tell the handler to use this format
   console.setFormatter(formatter)
   # add the handler to the root logger
   logging.getLogger('').addHandler(console)

   # Now, we can log to the root logger, or any other logger. First the root...
   logging.info('Jackdaws love my big sphinx of quartz.')

   # Now, define a couple of other loggers which might represent areas in your
   # application:

   logger1 = logging.getLogger('myapp.area1')
   logger2 = logging.getLogger('myapp.area2')

   logger1.debug('Quick zephyrs blow, vexing daft Jim.')
   logger1.info('How quickly daft jumping zebras vex.')
   logger2.warning('Jail zesty vixen who grabbed pay from quack.')
   logger2.error('The five boxing wizards jump quickly.')

このスクリプトを実行すると、コンソールには以下のように表示されるでしょう::

   root        : INFO     Jackdaws love my big sphinx of quartz.
   myapp.area1 : INFO     How quickly daft jumping zebras vex.
   myapp.area2 : WARNING  Jail zesty vixen who grabbed pay from quack.
   myapp.area2 : ERROR    The five boxing wizards jump quickly.

そして、ファイルは以下のようになるはずです::

   10-22 22:19 root         INFO     Jackdaws love my big sphinx of quartz.
   10-22 22:19 myapp.area1  DEBUG    Quick zephyrs blow, vexing daft Jim.
   10-22 22:19 myapp.area1  INFO     How quickly daft jumping zebras vex.
   10-22 22:19 myapp.area2  WARNING  Jail zesty vixen who grabbed pay from quack.
   10-22 22:19 myapp.area2  ERROR    The five boxing wizards jump quickly.

ご覧のように、 DEBUG メッセージはファイルだけに出力され、その他のメッセージは両方に出力されます。

この例題では、コンソールとファイルのハンドラだけを使っていますが、実際には任意の数のハンドラや組み合わせを使えます。


.. _network-logging:

ログイベントをネットワーク越しに送受信する
------------------------------------------

ログイベントをネットワーク越しに送信し、受信端でそれを処理したいとしましょう。 :class:`SocketHandler`
インスタンスを送信端のルートロガーに接続すれば、簡単に実現できます::

   import logging, logging.handlers

   rootLogger = logging.getLogger('')
   rootLogger.setLevel(logging.DEBUG)
   socketHandler = logging.handlers.SocketHandler('localhost',
                       logging.handlers.DEFAULT_TCP_LOGGING_PORT)
   # don't bother with a formatter, since a socket handler sends the event as
   # an unformatted pickle
   rootLogger.addHandler(socketHandler)

   # Now, we can log to the root logger, or any other logger. First the root...
   logging.info('Jackdaws love my big sphinx of quartz.')

   # Now, define a couple of other loggers which might represent areas in your
   # application:

   logger1 = logging.getLogger('myapp.area1')
   logger2 = logging.getLogger('myapp.area2')

   logger1.debug('Quick zephyrs blow, vexing daft Jim.')
   logger1.info('How quickly daft jumping zebras vex.')
   logger2.warning('Jail zesty vixen who grabbed pay from quack.')
   logger2.error('The five boxing wizards jump quickly.')

受信端では、 :mod:`SocketServer` モジュールを使って受信プログラムを作成しておきます。簡単な実用プログラムを以下に示します::

   import cPickle
   import logging
   import logging.handlers
   import SocketServer
   import struct


   class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
       """Handler for a streaming logging request.

       This basically logs the record using whatever logging policy is
       configured locally.
       """

       def handle(self):
           """
           Handle multiple requests - each expected to be a 4-byte length,
           followed by the LogRecord in pickle format. Logs the record
           according to whatever policy is configured locally.
           """
           while 1:
               chunk = self.connection.recv(4)
               if len(chunk) < 4:
                   break
               slen = struct.unpack(">L", chunk)[0]
               chunk = self.connection.recv(slen)
               while len(chunk) < slen:
                   chunk = chunk + self.connection.recv(slen - len(chunk))
               obj = self.unPickle(chunk)
               record = logging.makeLogRecord(obj)
               self.handleLogRecord(record)

       def unPickle(self, data):
           return cPickle.loads(data)

       def handleLogRecord(self, record):
           # if a name is specified, we use the named logger rather than the one
           # implied by the record.
           if self.server.logname is not None:
               name = self.server.logname
           else:
               name = record.name
           logger = logging.getLogger(name)
           # N.B. EVERY record gets logged. This is because Logger.handle
           # is normally called AFTER logger-level filtering. If you want
           # to do filtering, do it at the client end to save wasting
           # cycles and network bandwidth!
           logger.handle(record)

   class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer):
       """simple TCP socket-based logging receiver suitable for testing.
       """

       allow_reuse_address = 1

       def __init__(self, host='localhost',
                    port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                    handler=LogRecordStreamHandler):
           SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
           self.abort = 0
           self.timeout = 1
           self.logname = None

       def serve_until_stopped(self):
           import select
           abort = 0
           while not abort:
               rd, wr, ex = select.select([self.socket.fileno()],
                                          [], [],
                                          self.timeout)
               if rd:
                   self.handle_request()
               abort = self.abort

   def main():
       logging.basicConfig(
           format="%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s")
       tcpserver = LogRecordSocketReceiver()
       print "About to start TCP server..."
       tcpserver.serve_until_stopped()

   if __name__ == "__main__":
       main()

先にサーバを起動しておき、次にクライアントを起動します。クライアント側では、コンソールには何も出力されません; サーバ側では以下のようなメッセージ
を目にするはずです::

   About to start TCP server...
      59 root            INFO     Jackdaws love my big sphinx of quartz.
      59 myapp.area1     DEBUG    Quick zephyrs blow, vexing daft Jim.
      69 myapp.area1     INFO     How quickly daft jumping zebras vex.
      69 myapp.area2     WARNING  Jail zesty vixen who grabbed pay from quack.
      69 myapp.area2     ERROR    The five boxing wizards jump quickly.


Handler オブジェクト
--------------------

ハンドラは以下の属性とメソッドを持ちます。 :class:`Handler` は直接インスタンス化されることはありません; このクラスは
より便利なサブクラスの基底クラスとして働きます。しかしながら、サブクラスにおける :meth:`__init__` メソッドでは、
:meth:`Handler.__init__` を呼び出す必要があります。


.. method:: Handler.__init__(level=NOTSET)

   レベルを設定して、 :class:`Handler` インスタンスを初期化します。空のリストを使ってフィルタを設定し、I/O 機構へのアクセスを
   直列化するために (:meth:`createLock` を使って) ロックを生成します。


.. method:: Handler.createLock()

   スレッド安全でない根底の I/O 機能に対するアクセスを直列化するために用いられるスレッドロック (thread lock) を初期化します。


.. method:: Handler.acquire()

   :meth:`createLock` で生成されたスレッドロックを獲得します。


.. method:: Handler.release()

   :meth:`acquire` で獲得したスレッドロックを解放します。


.. method:: Handler.setLevel(lvl)

   このハンドラに対する閾値を *lvl* に設定します。ログ記録しようとするメッセージで、 *lvl* よりも深刻でないものは
   無視されます。ハンドラが生成された際、レベルは :const:`NOTSET`  (全てのメッセージが処理される) に設定されます。


.. method:: Handler.setFormatter(form)

   このハンドラのフォーマッタを *form* に設定します。


.. method:: Handler.addFilter(filt)

   指定されたフィルタ *filt* をこのハンドラに追加します。


.. method:: Handler.removeFilter(filt)

   指定されたフィルタ *filt* をこのハンドラから除去します。


.. method:: Handler.filter(record)

   このハンドラのフィルタをレコードに適用し、レコードがフィルタを透過して処理されることになる場合には真を返します。


.. method:: Handler.flush()

   全てのログ出力がフラッシュされるようにします。このクラスのバージョンではなにも行わず、サブクラスで実装するためのものです。


.. method:: Handler.close()

   ハンドラで使われている全てのリソースを始末します。このクラスのバージョンではなにも行わず、サブクラスで実装するためのものです。


.. method:: Handler.handle(record)

   ハンドラに追加されたフィルタの条件に応じて、指定されたログレコードを発信します。このメソッドは I/O スレッドロックの獲得/開放を伴う実際の
   ログ発信をラップします。


.. method:: Handler.handleError(record)

   このメソッドは :meth:`emit` の呼び出し中に例外に遭遇した際にハンドラから呼び出されます。デフォルトではこのメソッドは
   何も行いません。すなわち、例外は暗黙のまま無視されます。ほとんどのログ記録システムでは、これがほぼ望ましい機能です -
   というのは、ほとんどのユーザはログ記録システム自体のエラーは気にせず、むしろアプリケーションのエラーに興味があるからです。
   しかしながら、望むならこのメソッドを自作のハンドラと置き換えることはできます。 *record* には、例外発生時に処理されていたレコードが入ります。


.. method:: Handler.format(record)

   レコードに対する書式化を行います - フォーマッタが設定されていれば、それを使います。そうでない場合、
   モジュールにデフォルト指定されたフォーマッタを使います。


.. method:: Handler.emit(record)

   指定されたログ記録レコードを実際にログ記録する際の全ての処理を行います。このメソッドのこのクラスのバージョンはサブクラスで
   実装するためのものなので、 :exc:`NotImplementedError` を送出します。


StreamHandler
^^^^^^^^^^^^^

:class:`StreamHandler` クラスは、 :mod:`logging` パッケージのコアにありますが、ログ出力を
*sys.stdout* 、 *sys.stderr* あるいは何らかのファイル類似オブジェクト(あるいは、もっと正確にいえば、 :meth:`write`
および :meth:`flush` メソッドをサポートする何らかのオブジェクト) といったストリームに送信します。


.. class:: StreamHandler([strm])

   :class:`StreamHandler` クラスの新たなインスタンスを返します。 *strm* が指定された場合、インスタンスはログ出力先として
   指定されたストリームを使います; そうでない場合、 *sys.stderr* が使われます。


.. method:: StreamHandler.emit(record)

   フォーマッタが指定されていれば、フォーマッタを使ってレコードを書式化します。次に、レコードがストリームに書き込まれ、末端に
   改行がつけられます。例外情報が存在する場合、 :func:`traceback.print_exception` を使って書式化され、
   ストリームの末尾につけられます。


.. method:: StreamHandler.flush()

   ストリームの :meth:`flush` メソッドを呼び出してバッファをフラッシュします。 :meth:`close` メソッドは
   :class:`Handler` から継承しているため何も行わないので、 :meth:`flush` 呼び出しを明示的に行う必要があります。


FileHandler
^^^^^^^^^^^

:class:`FileHandler` クラスは、 :mod:`logging` パッケージのコアにありま
すが、ログ出力をディスク上のファイルに送信します。このクラスは出力機能を :class:`StreamHandler` から継承しています。


.. class:: FileHandler(filename[, mode])

   :class:`FileHandler` クラスの新たなインスタンスを返します。指定されたファイルが開かれ、ログ記録のためのストリームとして
   使われます。 *mode* が指定されなかった場合、 :const:`'a'`  が使われます。デフォルトでは、ファイルは無制限に大きくなりつづけます。


.. method:: FileHandler.close()

   ファイルを閉じます。


.. method:: FileHandler.emit(record)

   *record* をファイルに出力します。


RotatingFileHandler
^^^^^^^^^^^^^^^^^^^

:class:`RotatingFileHandler` クラスは、 :mod:`logging.handlers` モジュー
ルの中にありますが、ディスク上のログファイルに対するローテーション処理をサポートします。


.. class:: RotatingFileHandler(filename[, mode[, maxBytes[, backupCount]]])

   :class:`RotatingFileHandler` クラスの新たなインスタンスを返します。指定されたファイルが開かれ、ログ記録のためのストリームとして
   使われます。 *mode* が指定されなかった場合、 :const:`"a"`  が使われます。デフォルトでは、ファイルは無制限に大きくなりつづけます。

   あらかじめ決められたサイズでファイルをロールオーバ (:dfn:`rollover`)  させられるように、 *maxBytes* および
   *backupCount* 値を指定することができます。指定サイズを超えそうになると、ファイルは
   閉じられ、暗黙のうちに新たなファイルが開かれます。ロールオーバは現在のログファイルの長さが *maxBytes* に近くなると常に起きます。
   *backupCount* が非ゼロの場合、システムは古いログファイルをファイル名に ".1", ".2" といった拡張子を追加して保存します。
   例えば、 *backupCount* が 5 で、基本のファイル名が :file:`app.log` なら、 :file:`app.log` 、
   :file:`app.log.1` 、 :file:`app.log.2` 、 ... と続き、 :file:`app.log.5`
   までを得ることになります。ログの書き込み対象になるファイルは常に :file:`app.log` です。このファイルが満杯になると、
   ファイルは閉じられ、 :file:`app.log.1` に名称変更されます。 :file:`app.log.1` 、 :file:`app.log.2`
   などが存在する場合、それらのファイルはそれぞれ :file:`app.log.2` 、 :file:`app.log.3` といった具合に名前変更されます。


.. method:: RotatingFileHandler.doRollover()

   上述のような方法でロールオーバを行います。


.. method:: RotatingFileHandler.emit(record)

   上述のようなロールオーバを行いながら、レコードをファイルに出力します。


TimedRotatingFileHandler
^^^^^^^^^^^^^^^^^^^^^^^^

:class:`TimedRotatingFileHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、特定の時間間隔でのログ交替をサポートしています。


.. class:: TimedRotatingFileHandler(filename [,when [,interval [,backupCount]]])

   :class:`TimedRotatingFileHandler` クラスの新たなインスタンスを返します。 *filename*
   に指定したファイルを開き、ログ出力先のストリームとして使います。ログファイルの交替時には、ファイル名に拡張子 (suffix) を
   つけます。ログファイルの交替は *when* および *interval*  の積に基づいて行います。

   *when* は *interval* の単位を指定するために使います。使える値は下表の通りで、大小文字の区別を行いません:

   +----------+-------------------+
   | 値       | *interval* の単位 |
   +==========+===================+
   | S        | 秒                |
   +----------+-------------------+
   | M        | 分                |
   +----------+-------------------+
   | H        | 時間              |
   +----------+-------------------+
   | D        | 日                |
   +----------+-------------------+
   | W        | 曜日 (0=Monday)   |
   +----------+-------------------+
   | midnight | 深夜              |
   +----------+-------------------+

   *backupCount* がゼロでない場合、古いログファイルを保存する際にロギングシステムは拡張子を付けます。拡張子は日付と時間に基づいて、
   strftime の ``%Y-%m-%d_%H-%M-%S`` 形式かその前の方の一部分を、ロールオーバ間隔に依存した形で使います。
   保存されるファイル数は高々 *backupCount* 個で、それ以上のファイルがロールオーバされる時に作られるならば、一番古いものが削除されます。


.. method:: TimedRotatingFileHandler.doRollover()

   上記の方法でロールオーバを行います。


.. method:: TimedRotatingFileHandler.emit(record)

   :meth:`setRollover` で解説した方法でロールオーバを行いながら、レコードをファイルに出力します。


SocketHandler
^^^^^^^^^^^^^

:class:`SocketHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、ログ出力をネットワークソケットに送信します。基底クラスでは TCP ソケットを用います。


.. class:: SocketHandler(host, port)

   アドレスが *host* および *port* で与えられた遠隔のマシンと通信するようにした :class:`SocketHandler`
   クラスのインスタンスを生成して返します。


.. method:: SocketHandler.close()

   ソケットを閉じます。


.. method:: SocketHandler.handleError()


.. method:: SocketHandler.emit()

   レコードの属性辞書を pickle 化し、バイナリ形式でソケットに書き込みます。ソケット操作でエラーが生じた場合、暗黙のうちにパケットは
   捨てられます。前もって接続が失われていた場合、接続を再度確立します。受信端でレコードを逆 pickle 化して :class:`LogRecord`
   にするには、 :func:`makeLogRecord` 関数を使ってください。


.. method:: SocketHandler.handleError()

   :meth:`emit` の処理中に発生したエラーを処理します。よくある原因は接続の消失です。次のイベント発生時に再度
   接続確立を試みることができるようにソケットを閉じます。


.. method:: SocketHandler.makeSocket()

   サブクラスで必要なソケット形式を詳細に定義できるようにするためのファクトリメソッドです。デフォルトの実装では、TCP ソケット
   (:const:`socket.SOCK_STREAM`) を生成します。


.. method:: SocketHandler.makePickle(record)

   レコードの属性辞書を pickle 化して、長さを指定プレフィクス付きのバイナリにし、ソケットを介して送信できるようにして返します。


.. method:: SocketHandler.send(packet)

   pickle 化された文字列 *packet* をソケットに送信します。この関数はネットワークが処理待ち状態の時に発生しうる部分的送信を行えます。


DatagramHandler
^^^^^^^^^^^^^^^

:class:`DatagramHandler` クラスは、 :mod:`logging.handlers` モジュールの中にありますが、
:class:`SocketHandler` を継承しており、ログ記録メッセージを UDP ソケットを介して送れるようサポートしています。


.. class:: DatagramHandler(host, port)

   アドレスが *host* および *port* で与えられた遠隔のマシンと通信するようにした :class:`DatagramHandler`
   クラスのインスタンスを生成して返します。


.. method:: DatagramHandler.emit()

   レコードの属性辞書を pickle 化し、バイナリ形式でソケットに書き込みます。ソケット操作でエラーが生じた場合、暗黙のうちにパケットは
   捨てられます。前もって接続が失われていた場合、接続を再度確立します。受信端でレコードを逆 pickle 化して :class:`LogRecord`
   にするには、 :func:`makeLogRecord` 関数を使ってください。


.. method:: DatagramHandler.makeSocket()

   ここで :class:`SocketHandler` のファクトリメソッドをオーバライドして UDP ソケット
   (:const:`socket.SOCK_DGRAM`) を生成しています。


.. method:: DatagramHandler.send(s)

   pickle 化された文字列をソケットに送信します。


SysLogHandler
^^^^^^^^^^^^^

:class:`SysLogHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、ログ記録メッセージを遠隔またはローカルの Unix syslog に送信する機能をサポートしています。


.. class:: SysLogHandler([address[, facility]])

   遠隔のUnix マシンと通信するための、 :class:`SysLogHandler` クラスの新たなインスタンスを返します。マシンのアドレスは
   ``(host, port)`` のタプル形式をとる *address*  で与えられます。 *address*
   が指定されない場合、 ``('localhost', 514)`` が使われます。アドレスは UDP ソケットを使って開かれます。 *facility*
   が指定されない場合、 :const:`LOG_USER` が使われます。


.. method:: SysLogHandler.close()

   遠隔ホストのソケットを閉じます。


.. method:: SysLogHandler.emit(record)

   レコードは書式化された後、syslog サーバに送信されます。例外情報が存在しても、サーバには *送信されません* 。


.. method:: SysLogHandler.encodePriority(facility, priority)

   便宜レベル (facility) および優先度を整数に符号化します。値は文字列でも整数でも渡すことができます。文字列が渡された場合、内部の
   対応付け辞書が使われ、整数に変換されます。


NTEventLogHandler
^^^^^^^^^^^^^^^^^

:class:`NTEventLogHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、ログ記録メッセージをローカルな Windows NT、Windows 2000 、または Windows XP のイベントログ
(event log) に送信する機能をサポートします。この機能を使えるようにするには、 Mark Hammond による Python 用 Win32
拡張パッケージをインストールする必要があります。


.. class:: NTEventLogHandler(appname[, dllname[, logtype]])

   :class:`NTEventLogHandler` クラスの新たなインスタンスを返します。 *appname*
   はイベントログに表示する際のアプリケーション名を定義するために使われます。この名前を使って適切なレジストリエントリが生成されます。 *dllname*
   はログに保存するメッセージ定義の入った .dll または .exe  ファイルへの完全に限定的な (fully qualified) パス名を与えなければ
   なりません (指定されない場合、 :const:`'win32service.pyd'` が使われます - このライブラリは Win32
   拡張とともにインストールされ、いくつかのプレースホルダとなるメッセージ定義を含んでいます)。
   これらのプレースホルダを利用すると、メッセージの発信源全体がログに記録されるため、イベントログは巨大になるので注意してください。 *logtype* は
   :const:`'Application'` 、 :const:`'System'`  または :const:`'Security'`
   のいずれかであるか、デフォルトの :const:`'Application'` でなければなりません。


.. method:: NTEventLogHandler.close()

   現時点では、イベントログエントリの発信源としてのアプリケーション名をレジストリから除去することができます。
   しかしこれを行うと、イベントログビューアで意図したログをみることができなくなるでしょう - これはイベントログが .dll 名を取得するために
   レジストリにアクセスできなければならないからです。現在のバージョンではこの操作を行いません (実際、このメソッドは何も行いません)。


.. method:: NTEventLogHandler.emit(record)

   メッセージ ID、イベントカテゴリおよびイベント型を決定し、メッセージを NT イベントログに記録します。


.. method:: NTEventLogHandler.getEventCategory(record)

   レコードに対するイベントカテゴリを返します。自作のカテゴリを指定したい場合、このメソッドをオーバライドしてください。このクラスのバージョンのメソッドは 0
   を返します。


.. method:: NTEventLogHandler.getEventType(record)

   レコードのイベント型を返します。自作の型を指定したい場合、このメソッドをオーバライドしてください。このクラスのバージョンのメソッドは、ハンドラの
   *typemap* 属性を使って対応付けを行います。この属性は :meth:`__init__` で初期化
   され、 :const:`DEBUG` 、 :const:`INFO` 、 :const:`WARNING` 、 :const:`ERROR` 、および
   :const:`CRITICAL` が入っています。自作のレベルを使っているのなら、このメソッドをオーバライドするか、ハンドラの *typemap*
   属性に適切な辞書を配置する必要があるでしょう。


.. method:: NTEventLogHandler.getMessageID(record)

   レコードのメッセージ ID を返します。自作のメッセージを使っているのなら、ロガーに渡される *msg* を書式化文字列ではなく ID に
   します。その上で、辞書参照を行ってメッセージ ID を得ます。このクラスのバージョンでは 1 を返します。この値は
   :file:`win32service.pyd` における基本となるメッセージ ID です。


SMTPHandler
^^^^^^^^^^^

:class:`SMTPHandler` クラスは、 :mod:`logging.handlers` モジュールの中にありますが、SMTP
を介したログ記録メッセージの送信機能をサポートします。


.. class:: SMTPHandler(mailhost, fromaddr, toaddrs, subject)

   新たな :class:`SMTPHandler` クラスのインスタンスを返します。インスタンスは email の from および to アドレス行、および
   subject 行とともに初期化されます。 *toaddrs* は文字列からなるリストでなければなりません非標準の SMTP
   ポートを指定するには、 *mailhost* 引数に (host, port)  のタプル形式を指定します。文字列を使った場合、標準の SMTP ポートが
   使われます。


.. method:: SMTPHandler.emit(record)

   レコードを書式化し、指定されたアドレスに送信します。


.. method:: SMTPHandler.getSubject(record)

   レコードに応じたサブジェクト行を指定したいなら、このメソッドをオーバライドしてください。


MemoryHandler
^^^^^^^^^^^^^

:class:`MemoryHandler` は、 :mod:`logging.handlers` モ
ジュールの中にありますが、ログ記録するレコードをメモリ上にバッファし、定期的にその内容をターゲット (:dfn:`target`) となるハンドラに
フラッシュする機能をサポートしています。フラッシュ処理はバッファが一杯になるか、ある深刻さかそれ以上のレベルをもったイベントが観測された際に行われます。

:class:`MemoryHandler` はより一般的な抽象クラス、 :class:`BufferingHandler`
のサブクラスです。この抽象クラスでは、ログ記録するレコードをメモリ上にバッファします。各レコードがバッファに
追加される毎に、 :meth:`shouldFlush` を呼び出してバッファをフラッシュ
すべきかどうか調べます。フラッシュする必要がある場合、 :meth:`flush` が必要にして十分な処理を行うものと想定しています。


.. class:: BufferingHandler(capacity)

   指定し許容量のバッファでハンドラを初期化します。


.. method:: BufferingHandler.emit(record)

   レコードをバッファに追加します。 :meth:`shouldFlush` が真を返す場合、バッファを処理するために :meth:`flush`
   を呼び出します。


.. method:: BufferingHandler.flush()

   このメソッドをオーバライドして、自作のフラッシュ動作を実装することができます。このクラスのバージョンのメソッドでは、単にバッファの内容を削除して空にします。


.. method:: BufferingHandler.shouldFlush(record)

   バッファが許容量に達している場合に真を返します。このメソッドは自作のフラッシュ処理方針を実装するためにオーバライドすることができます。


.. class:: MemoryHandler(capacity[, flushLevel [, target]])

   :class:`MemoryHandler` クラスの新たなインスタンスを返します。インスタンスはサイズ *capacity*
   のバッファとともに初期化されます。 *flushLevel* が指定されていない場合、 :const:`ERROR` が使われます。 *target*
   が指定されていない場合、ハンドラが何らかの有意義な処理を行う前に :meth:`setTarget` でターゲットを指定する必要があります。


.. method:: MemoryHandler.close()

   :meth:`flush` を呼び出し、ターゲットを :const:`None` に設定してバッファを消去します。


.. method:: MemoryHandler.flush()

   :class:`MemoryHandler` の場合、フラッシュ処理は単に、バッファされたレコードをターゲットがあれば送信することを意味します。
   違った動作を行いたい場合、オーバライドしてください。


.. method:: MemoryHandler.setTarget(target)

   ターゲットハンドラをこのハンドラに設定します。


.. method:: MemoryHandler.shouldFlush(record)

   バッファが満杯になっているか、 *flushLevel* またはそれ以上のレコードでないかを調べます。


HTTPHandler
^^^^^^^^^^^

:class:`HTTPHandler` クラスは、 :mod:`logging.handlers` モジュールの中にありますが、ログ記録メッセージを
``GET`` または ``POST`` セマンティクスを使って Web サーバに送信する機能をサポートしています。


.. class:: HTTPHandler(host, url[, method])

   :class:`HTTPHandler` クラスの新たなインスタンスを返します。インスタンスはホストアドレス、URL および HTTP メソッドと
   ともに初期化されます。 *host* は特別なポートを使うことが必要な場合には、 ``host:port`` の形式で使うこともできます。 *method*
   が指定されなかった場合 ``GET`` が使われます。


.. method:: HTTPHandler.emit(record)

   レコードを URL エンコードされた辞書形式で Web サーバに送信します。


Formatter オブジェクト
----------------------

:class:`Formatter` は以下の属性とメソッドを持っています。 :class:`Formatter` は :class:`LogRecord` を
(通常は) 人間か外部のシステムで解釈できる文字列に変換する役割を担っています。基底クラスの :class:`Formatter`
では書式化文字列を指定することができます。何も指定されなかった場合、 ``'%(message)s'`` の値が使われます。

Formatter は書式化文字列とともに初期化され、 :class:`LogRecord` 属性に入っている知識を利用できるようにします -
上で触れたデフォルトの値では、ユーザによるメッセージと引数はあらかじめ書式化されて、 :class:`LogRecord` の *message*
属性に入っていることを利用しているようにです。この書式化文字列は、Python 標準の % を使った変換文字列で構成されます。文字列整形に関する詳細は
:ref:`typesseq-strings` "String Formatting Operations" の章を参照してください。

現状では、 :class:`LogRecord` の有用な属性は以下のようになっています:

+--------------------+------------------------------------------------------------------------+
| Format             | Description                                                            |
+====================+========================================================================+
| ``%(name)s``       | ロガー (ログ記録チャネル) の名前                                       |
+--------------------+------------------------------------------------------------------------+
| ``%(levelno)s``    | メッセージのログ記録レベルを表す数字 (DEBUG, INFO, WARNING,            |
|                    | ERROR, CRITICAL)                                                       |
+--------------------+------------------------------------------------------------------------+
| ``%(levelname)s``  | メッセージのログ記録レベルを表す文字列 ("DEBUG",  "INFO",              |
|                    | "WARNING", "ERROR", "CRITICAL")                                        |
+--------------------+------------------------------------------------------------------------+
| ``%(pathname)s``   | ログ記録の呼び出しが行われたソースファイルの全パス名 (取得できる場合)  |
+--------------------+------------------------------------------------------------------------+
| ``%(filename)s``   | パス名中のファイル名部分                                               |
+--------------------+------------------------------------------------------------------------+
| ``%(module)s``     | モジュール名 (ファイル名の名前部分)                                    |
+--------------------+------------------------------------------------------------------------+
| ``%(funcName)s``   | ログ記録の呼び出しを含む関数の名前                                     |
+--------------------+------------------------------------------------------------------------+
| ``%(lineno)d``     | ログ記録の呼び出しが行われたソース行番号 (取得できる場合)              |
+--------------------+------------------------------------------------------------------------+
| ``%(created)f``    | :class:`LogRecord` が生成された時刻 (time.time()                       |
|                    | の返した値)                                                            |
+--------------------+------------------------------------------------------------------------+
| ``%(asctime)s``    | :class:`LogRecord` が生成された時刻を人間が読める書式で表したもの。    |
|                    | デフォルトでは "2003-07-08 16:49:45,896" 形式                          |
|                    | (コンマ以降の数字は時刻のミリ秒部分) です                              |
+--------------------+------------------------------------------------------------------------+
| ``%(msecs)d``      | :class:`LogRecord` が生成された時刻の、ミリ秒部分                      |
+--------------------+------------------------------------------------------------------------+
| ``%(thread)d``     | スレッド ID (取得できる場合)                                           |
+--------------------+------------------------------------------------------------------------+
| ``%(threadName)s`` | スレッド名 (取得できる場合)                                            |
+--------------------+------------------------------------------------------------------------+
| ``%(process)d``    | プロセス ID (取得できる場合)                                           |
+--------------------+------------------------------------------------------------------------+
| ``%(message)s``    | レコードが発信された際に処理された  ``msg % args`` の結果              |
+--------------------+------------------------------------------------------------------------+

.. versionchanged:: 2.5
   *funcName* が追加されました.


.. class:: Formatter([fmt[, datefmt]])

   :class:`Formatter` クラスの新たなインスタンスを返します。インスタンスは全体としてのメッセージに対する書式化文字列と、メッセージの
   日付/時刻部分のための書式化文字列を伴って初期化されます。 *fmt*  が指定されない場合、 ``'%(message)s'`` が使われます。
   *datefmt* が指定されない場合、ISO8601 日付書式が使われます。


.. method:: Formatter.format(record)

   レコードの属性辞書が、文字列を書式化する演算で被演算子として使われます。書式化された結果の文字列を返します。辞書を書式化する前に、二つの準備段階を経ます。
   レコードの *message* 属性が *msg* % *args* を使って処理されます。書式化された文字列が :const:`'(asctime)'`
   を含むなら、 :meth:`formatTime` が呼び出され、イベントの発生時刻を
   書式化します。例外情報が存在する場合、 :meth:`formatException`  を使って書式化され、メッセージに追加されます。


.. method:: Formatter.formatTime(record[, datefmt])

   このメソッドは、フォーマッタが書式化された時間を利用したい際に、 :meth:`format` から呼び出されます。このメソッドは特定の要求を
   提供するためにフォーマッタで上書きすることができますが、基本的な振る舞いは以下のようになります: *datefmt* (文字列) が指定された
   場合、レコードが生成された時刻を書式化するために :func:`time.strftime` で使われます。そうでない場合、 ISO8601
   書式が使われます。結果の文字列が返されます。


.. method:: Formatter.formatException(exc_info)

   指定された例外情報 (:func:`sys.exc_info` が返すような標準例外のタプル) を文字列として書式化します。デフォルトの実装は単に
   :func:`traceback.print_exception` を使います。結果の文字列が返されます。


Filter オブジェクト
-------------------

:class:`Filter` は :class:`Handler` と :class:`Logger` によって利用され、
レベルによる制御よりも洗練されたフィルタ処理を提供します。基底のフィルタクラスでは、ロガーの階層構造のある点よりも下層にあるイベント
だけを通過させます。例えば、"A.B" で初期化されたフィルタはロガー "A.B"、 "A.B.C"、 "A.B.C.D"、 "A.B.D"
などでログ記録されたイベントを通過させます。しかし、 "A.BB"、"B.A.B" などは通過させません。
空の文字列で初期化された場合、全てのイベントを通過させます。


.. class:: Filter([name])

   :class:`Filter` クラスのインスタンスを返します。 *name* が指定されていれば、 *name*
   はロガーの名前を表します。指定されたロガーとその子ロガーのイベントがフィルタを通過できるようになります。
   *name* が指定されなければ、全てのイベントを通過させます。


.. method:: Filter.filter(record)

   指定されたレコードがログされているか？されていなければゼロを、されていればゼロでない値を返します。適切と判断されれば、このメソッドによってレコードは in
   place で修正されることがあります。


LogRecord オブジェクト
----------------------

何かをログ記録する際には常に :class:`LogRecord` インスタンスが生成されます。
インスタンスにはログ記録されることになっているイベントに関係する全ての情報が入っています。インスタンスに渡される主要な情報は  *msg* および
*args* で、これらは msg % args を使って組み合わせられ、レコードのメッセージフィールドを生成します。
レコードはまた、レコードがいつ生成されたか、ログ記録がソースコード行のどこで呼び出されたか、あるいはログ記録すべき何らかの例外情報
といった情報も含んでいます。


.. class:: LogRecord(name, lvl, pathname, lineno, msg, args, exc_info)

   関係のある情報とともに初期化された :class:`LogRecord` のインスタンスを返します。 *name* はロガーの名前です; *lvl*
   は数字で表されたレベルです; *pathname* はログ記録呼び出しが見つかったソースファイルの絶対パス名です。 *msg* はユーザ定義のメッセージ
   (書式化文字列) です; *args* はタプルで、 *msg* と合わせて、ユーザメッセージを生成します; *exc_info* は例外情報のタプルで、
   :func:`sys.exc_info()` を呼び出して得られたもの (または、例外情報が取得できない場合には :const:`None`) です。


.. method:: LogRecord.getMessage()

   ユーザが供給した引数をメッセージに交ぜた後、この :class:`LogRecord` インスタンスへのメッセージを返します。


スレッド安全性
--------------

*logging* モジュールは、クライアントで特殊な作業を必要としないかぎりスレッド安全 (thread-safe) なようになっています。このスレッド
安全性はスレッドロックによって達成されています;  モジュールの共有データへのアクセスを直列化するためのロックが一つ存在し、各ハンドラでも根底にある I/O
へのアクセスを直列化するためにロックを生成します。


環境設定
--------


.. _logging-config-api:

環境設定のための関数
^^^^^^^^^^^^^^^^^^^^

以下の関数で :mod:`logging` モジュールの環境設定をします。これらの関数は、 :mod:`logging.config` にあります。
これらの関数の使用はオプションです ---  :mod:`logging` モジュールはこれらの関数を使うか、 (:mod:`logging` 自体で
定義されている) 主要な API を呼び出し、 :mod:`logging` か :mod:`logging.handlers`
で宣言されているハンドラを定義することで設定することができます。


.. function:: fileConfig(fname[, defaults])

   ログ記録の環境設定をファイル名 *fname* の ConfigParser 形式ファイルから読み出します。この関数はアプリケーションから何度も呼び出すことが
   でき、これによって、(設定の選択と、選択された設定を読み出す機構をデベロッパが提供していれば) 複数のお仕着せの設定からエンドユーザが
   選択するようにできます。ConfigParser に渡すためのデフォルト値は *defaults* 引数で指定できます。


.. function:: listen([port])

   指定されたポートでソケットサーバを開始し、新たな設定を待ち受け (listen) ます。ポートが指定されなければ、モジュールのデフォルト設定である
   :const:`DEFAULT_LOGGING_CONFIG_PORT` が使われます。ログ記録の環境設定は :func:`fileConfig`
   で処理できるようなファイルとして送信されます。 :class:`Thread` インスタンスを返し、サーバを開始するために :meth:`start`
   を呼び、適切な状況で :meth:`join` を呼び出すことができます。サーバを停止するには :func:`stopListening` を呼んでください。
   設定を送るには、まず設定ファイルを読み、それを4バイトからなる長さを struct.\ ``pack('>L', n)`` を使ってバイナリにパックしたものを
   前に付けたバイト列としてソケットに送ります。


.. function:: stopListening()

   :func:`listen` を呼び出して作成された、待ち受け中のサーバを停止します。通常 :func:`listen` の戻り値に対して
   :meth:`join` が呼ばれる前に呼び出します。


.. _logging-config-fileformat:

環境設定ファイルの書式
^^^^^^^^^^^^^^^^^^^^^^

.. % 

:func:`fileConfig` が解釈できる環境設定ファイルの形式は、 ConfigParser の機能に基づいています。
ファイルには、 ``[loggers]`` 、 ``[handlers]`` 、および ``[formatters]`` といったセクションが入っていなければならず、
各セクションではファイル中で定義されている各タイプのエンティティを名前で指定しています。こうしたエンティティの各々について、
そのエンティティをどう設定するかを示した個別のセクションがあります。すなわち、 ``log01`` という名前の ``[loggers]`` セクションにある
ロガーに対しては、対応する詳細設定がセクション ``[logger_log01]`` に収められています。同様に、 ``hand01`` という名前の
``[handlers]`` セクションにあるハンドラは ``[handler_hand01]``
と呼ばれるセクションに設定をもつことになり、 ``[formatters]``  セクションにある ``form01`` は
``[formatter_form01]`` というセクションで設定が指定されています。ルートロガーの設定は ``[logger_root]``
と呼ばれるセクションで指定されていなければなりません。

ファイルにおけるこれらのセクションの例を以下に示します。 ::

   [loggers]
   keys=root,log02,log03,log04,log05,log06,log07

   [handlers]
   keys=hand01,hand02,hand03,hand04,hand05,hand06,hand07,hand08,hand09

   [formatters]
   keys=form01,form02,form03,form04,form05,form06,form07,form08,form09

ルートロガーでは、レベルとハンドラのリストを指定しなければなりません。ルートロガーのセクションの例を以下に示します。 ::

   [logger_root]
   level=NOTSET
   handlers=hand01

``level`` エントリは ``DEBUG, INFO, WARNING, ERROR, CRITICAL`` のうちの一つか、 ``NOTSET``
になります。ルートロガーの場合にのみ、 ``NOTSET`` は全てのメッセージがログ記録されることを意味します。レベル値は ``logging``
パッケージの名前空間のコンテキストにおいて :func:`eval` されます。

``handlers`` エントリはコンマで区切られたハンドラ名からなるリストで、 ``[handlers]`` セクションになくてはなりません。
また、これらの各ハンドラの名前に対応するセクションが設定ファイルに存在しなければなりません。

ルートロガー以外のロガーでは、いくつか追加の情報が必要になります。これは以下の例のように表されます。 ::

   [logger_parser]
   level=DEBUG
   handlers=hand01
   propagate=1
   qualname=compiler.parser

``level`` および ``handlers`` エントリはルートロガーのエントリと同様に解釈されますが、非ルートロガーのレベルが ``NOTSET``
に指定された場合、ログ記録システムはロガー階層のより上位のロガーにロガーの実効レベルを問い合わせるところが違います。 ``propagate``
エントリは、メッセージをロガー階層におけるこのロガーの上位のハンドラに伝播させることを示す 1 に設定されるか、メッセージを階層の上位に伝播 **しない**
ことを示す 0 に設定されます。 ``qualname`` エントリはロガーのチャネル名を階層的に表した
もの、すなわちアプリケーションがこのロガーを取得する際に使う名前になります。

ハンドラの環境設定を指定しているセクションは以下の例のようになります。 ::

   [handler_hand01]
   class=StreamHandler
   level=NOTSET
   formatter=form01
   args=(sys.stdout,)

``class`` エントリはハンドラのクラス (``logging`` パッケージの名前空間において :func:`eval` で決定されます)
を示します。 ``level`` はロガーの場合と同じように解釈され、 ``NOTSET``  は "全てを記録する (log everything)"
と解釈されます。

``formatter`` エントリはこのハンドラのフォーマッタに対するキー名を表します。空文字列の場合、デフォルトのフォーマッタ
(``logging._defaultFormatter``) が使われます。名前が指定されている場合、その名前は ``[formatters]``
セクションになくてはならず、対応するセクションが設定ファイル中になければなりません。

``args`` エントリは、 ``logging`` パッケージの名前空間のコンテキストで :func:`eval` される際、ハンドラクラスの
コンストラクタに対する引数からなるリストになります。
典型的なエントリがどうやって作成されるかについては、対応するハンドラのコンストラクタか、以下の例を参照してください。 ::

   [handler_hand02]
   class=FileHandler
   level=DEBUG
   formatter=form02
   args=('python.log', 'w')

   [handler_hand03]
   class=handlers.SocketHandler
   level=INFO
   formatter=form03
   args=('localhost', handlers.DEFAULT_TCP_LOGGING_PORT)

   [handler_hand04]
   class=handlers.DatagramHandler
   level=WARN
   formatter=form04
   args=('localhost', handlers.DEFAULT_UDP_LOGGING_PORT)

   [handler_hand05]
   class=handlers.SysLogHandler
   level=ERROR
   formatter=form05
   args=(('localhost', handlers.SYSLOG_UDP_PORT), handlers.SysLogHandler.LOG_USER)

   [handler_hand06]
   class=handlers.NTEventLogHandler
   level=CRITICAL
   formatter=form06
   args=('Python Application', '', 'Application')

   [handler_hand07]
   class=handlers.SMTPHandler
   level=WARN
   formatter=form07
   args=('localhost', 'from@abc', ['user1@abc', 'user2@xyz'], 'Logger Subject')

   [handler_hand08]
   class=handlers.MemoryHandler
   level=NOTSET
   formatter=form08
   target=
   args=(10, ERROR)

   [handler_hand09]
   class=handlers.HTTPHandler
   level=NOTSET
   formatter=form09
   args=('localhost:9022', '/log', 'GET')

フォーマッタの環境設定を指定しているセクションは以下のような形式です。 ::

   [formatter_form01]
   format=F1 %(asctime)s %(levelname)s %(message)s
   datefmt=
   class=logging.Formatter

``format`` エントリは全体を書式化する文字列で、 ``datefmt``  エントリは :func:`strftime`
互換の日付/時刻書式化文字列です。空文字列の場合、パッケージによって ISO8601 形式の日付/時刻に置き換えられ、日付書式化文字列 "ISO8601
形式ではミリ秒も指定しており、上の書式化文字列の結果にカンマで区切って追加されます。ISO8601 形式の時刻の例は ``2003-01-23
00:29:50,411`` です。

.. % Y-%m-%d %H:%M:%S" を指定した場合とほとんど同じになります。

``class`` エントリはオプションです。 ``class`` はフォーマッタのクラス名
(ドット区切りのモジュールとクラス名として)を示します。このオプションは :class:`Formatter` のサブクラスをインスタンス化するのに有用です。
:class:`Formatter` のサブクラスは例外トレースバックを展開された形式または圧縮された形式で表現することができます。

