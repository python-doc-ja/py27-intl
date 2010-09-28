
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


チュートリアル
--------------

標準ライブラリモジュールが提供するログ記録 API があることの御利益は、
全ての Python モジュールがログ記録に参加できることであり、
これによってあなたが書くアプリケーションのログにサードパーティーのモジュールが出力するメッセージを含ませることができます。

もちろん、複数のメッセージをそれぞれ別々の冗舌性レベルで別々の出力先にログ記録することができます。
ログメッセージをファイルへ、HTTP GET/POST 先へ、SMTP 経由で電子メールへ、汎用のソケットへ、もしくは OS ごとのログ記録機構へ書き込むことを全て標準モジュールでサポートします。
これら組み込まれたクラスが特別な要求仕様に合わないような場合には、
独自のログ記録先クラスを作り出すこともできます。

単純な例
^^^^^^^^

.. sectionauthor:: Doug Hellmann
.. (see <http://blog.doughellmann.com/2007/05/pymotw-logging.html>)

ほとんどのアプリケーションではファイルにログ記録することを望むことになるでしょうから、
まずはこのケースから始めましょう。
:func:`basicConfig` 関数を使って、デバッグメッセージがファイルに書き込まれるように、
デフォルトのハンドラをセットアップします::

   import logging
   LOG_FILENAME = '/tmp/logging_example.out'
   logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

   logging.debug('This message should go to the log file')

ではこのファイルを開いて結果を確認しましょう。
こんなログメッセージが見つかるでしょう::

   DEBUG:root:This message should go to the log file

スクリプトを繰り返し実行すると、
さらなるログメッセージがファイルに追記されていきます。
毎回新しいファイルの方が良ければ、 :func:`basicConfig` に渡すファイルモード引数を
``'w'`` にします。
ファイルサイズを自分で管理する代わりに、
もっと簡単に :class:`RotatingFileHandler` を使う手があります::

   import glob
   import logging
   import logging.handlers

   LOG_FILENAME = '/tmp/logging_rotatingfile_example.out'

   # Set up a specific logger with our desired output level
   my_logger = logging.getLogger('MyLogger')
   my_logger.setLevel(logging.DEBUG)

   # Add the log message handler to the logger
   handler = logging.handlers.RotatingFileHandler(
                 LOG_FILENAME, maxBytes=20, backupCount=5)

   my_logger.addHandler(handler)

   # Log some messages
   for i in range(20):
       my_logger.debug('i = %d' % i)

   # See what files are created
   logfiles = glob.glob('%s*' % LOG_FILENAME)

   for filename in logfiles:
       print filename

結果は分割された 6 ファイルになっているはずで、
それぞれがアプリケーションのログ記録の一部になっています::

   /tmp/logging_rotatingfile_example.out
   /tmp/logging_rotatingfile_example.out.1
   /tmp/logging_rotatingfile_example.out.2
   /tmp/logging_rotatingfile_example.out.3
   /tmp/logging_rotatingfile_example.out.4
   /tmp/logging_rotatingfile_example.out.5

最新のファイルはいつでも :file:`/tmp/logging_rotatingfile_example.out` で、
サイズの上限に達するたびに拡張子 ``.1`` を付けた名前に改名されます。
既にあるバックアップファイルはその拡張子がインクリメントされ
(``.1`` が ``.2`` になるなど)、 ``.5`` ファイルは消去されます。

見て判るようにここでは例示のためにファイルの大きさをとんでもなく小さな値に設定しています。
実際に使うときは *maxBytes* を適切な値に設定して下さい。

ログ記録 API のもう一つの有用な仕組みが異なるメッセージを異なるログレベルで生成する能力です。
これを使えば、たとえばコードの中にデバッグメッセージを埋め込みつつ、
出荷段階でログ記録レベルを落としてこれが記録されないようにするといったことができます。
デフォルトで設定されているレベルは
``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, ``DEBUG``, ``NOTSET`` です。

ロガー、ハンドラ、メッセージをログ記録する関数呼び出しは、どれもレベルを指定します。
ログメッセージはハンドラとロガーがそのレベル以下を吐き出す設定の時だけ吐き出されます。
たとえば、メッセージが ``CRITICAL`` でロガーが ``ERROR`` の設定ならばメッセージは吐き出されます。
一方、メッセージが ``WARNING`` でロガーが ``ERROR`` だけ生成するならば、
メッセージは吐き出されません::

   import logging
   import sys

   LEVELS = {'debug': logging.DEBUG,
             'info': logging.INFO,
             'warning': logging.WARNING,
             'error': logging.ERROR,
             'critical': logging.CRITICAL}

   if len(sys.argv) > 1:
       level_name = sys.argv[1]
       level = LEVELS.get(level_name, logging.NOTSET)
       logging.basicConfig(level=level)

   logging.debug('This is a debug message')
   logging.info('This is an info message')
   logging.warning('This is a warning message')
   logging.error('This is an error message')
   logging.critical('This is a critical error message')

スクリプトを 'debug' とか 'warning' といった引数で実行して、
レベルの違いによってどのメッセージが現れるようになるか見てみましょう::

   $ python logging_level_example.py debug
   DEBUG:root:This is a debug message
   INFO:root:This is an info message
   WARNING:root:This is a warning message
   ERROR:root:This is an error message
   CRITICAL:root:This is a critical error message

   $ python logging_level_example.py info
   INFO:root:This is an info message
   WARNING:root:This is a warning message
   ERROR:root:This is an error message
   CRITICAL:root:This is a critical error message

気付いたかもしれませんが、全てのログメッセージに ``root`` が埋め込まれています。
ログ記録モジュールは異なる名前のロガーの階層をサポートしているのです。
ログメッセージがどこから発生しているかを教える簡単な方法は、
プログラムのモジュールごとに別々のロガーオブジェクトを利用することです。
それぞれの新しいロガーはその親の設定を「継承」していて、
あるロガーに送られたログメッセージはそのロガーの名前を含みます。
場合によっては、ロガーをそれぞれ異なるように設定して、
それぞれのモジュールからのメッセージを異なったやり方で扱うこともできます。
では、単純な例でメッセージの出所が簡単に追跡できるように別々のモジュールからログ記録を行う方法を見てみましょう::

   import logging

   logging.basicConfig(level=logging.WARNING)

   logger1 = logging.getLogger('package1.module1')
   logger2 = logging.getLogger('package2.module2')

   logger1.warning('This message comes from one module')
   logger2.warning('And this message comes from another module')

出力はこうなります::

   $ python logging_modules_example.py
   WARNING:package1.module1:This message comes from one module
   WARNING:package2.module2:And this message comes from another module

他にもオプションはもっといろいろあります。
ログ記録方法の設定、たとえばログメッセージフォーマットを変えるオプション、
メッセージを複数の送り先に配送するようなもの、
ソケットインターフェイスを通して長く走り続けるアプリケーションの設定を途中で変更するものなどです。
全てのオプションはライブラリモジュールの文書の中でもっと細かく説明してあります。

ロガー
^^^^^^

logging ライブラリはモジュラー・アプローチを取ってコンポーネントのカテゴリーをいくつかに分けています: ロガー、ハンドラ、フィルタ、フォーマッタ。
ロガーはアプリケーションのコードが直接使うインターフェイスを外部に公開しています。
ハンドラはログ記録を適切な行き先に送ります。
フィルタはどのログ記録をハンドラにおくるかを決めるさらにきめ細かい機構を提供します。
フォーマッタは最終的なログ記録のレイアウトを指定します。

:class:`Logger` オブジェクトの仕事は大きく三つに分かれます。
一つめは、アプリケーションが実行中にメッセージを記録できるように、
いくつかのメソッドをアプリケーションから呼べるようにしています。
二つめに、ロガーオブジェクトはどのメッセージに対して作用するかを、
深刻さ(デフォルトのフィルター機構)またはフィルターオブジェクトに基づいて決定します。
三つめに、ロガーオブジェクトはログハンドラがそれぞれ持っている興味に関連するログメッセージを回送します。

ロガーオブジェクトのとりわけ広く使われるメソッドは二つのカテゴリーに分類できます:
設定とメッセージ送信です。

* :meth:`Logger.setLevel` ロガーが扱うログメッセージの最も低い深刻さを指定します。
  ここで組み込まれた深刻さは debug が一番低く、 critical が一番高くなります。
  たとえば、深刻さが info と設定されたロガーは info, warning, error, critical
  のメッセージしか扱わず debug メッセージは無視します。

* :meth:`Logger.addFilter` と :meth:`Logger.removeFilter`
  はロガーオブジェクトにフィルターを追加したり削除したりします。
  このチュートリアルではフィルターは説明しません。

設定されたロガーオブジェクトを使えば、以下のメソッドはログメッセージを作り出します:

* :meth:`Logger.debug`, :meth:`Logger.info`, :meth:`Logger.warning`,
  :meth:`Logger.error`, :meth:`Logger.critical` は全て、
  メッセージとメソッド名に対応したレベルでログ記録を作り出します。
  メッセージは実際にはフォーマット文字列であり、通常の文字列代入に使う
  :const:`%s`, :const:`%d`, :const:`%f` などを含み得ます。
  残りの引数はメッセージの代入される位置に対応するオブジェクトのリストです。
  :const:`**kwargs` については、ログ記録メソッドが気にするキーワードは
  :const:`exc_info` だけで、例外の情報をログに記録するかを決定するのに使います。

* :meth:`Logger.exception` は :meth:`Logger.error` と似たログメッセージを作成します。
  違いは :meth:`Logger.exception` がスタックトレースを一緒に吐き出すことです。
  例外ハンドラでだけ使うようにして下さい。

* :meth:`Logger.log` はログレベルを陽に引き渡される引数として取ります。
  これは上に挙げた便宜的なログレベルごとのメソッドを使うより少しコード量が多くなりますが、
  独自のログレベルを使うにはこのようにするものなのです。

:func:`getLogger` は指定されればその特定の、そうでなければ ``root``
のロガーインスタンスへの参照を返します。
ロガーの名前はピリオド区切りの階層構造を表します。
同じ名前で :func:`getLogger` を複数回呼び出した場合、
同一のロガーオブジェクトへの参照が返されます。
階層リストを下ったロガーはリスト上位のロガーの子です。
たとえば、名前が ``foo`` であるロガーがあったとして、
``foo.bar``, ``foo.bar.baz``, ``foo.bam`` といった名前のロガーは全て
``foo`` の子になります。
子ロガーはメッセージを親ロガーに伝えます。
このため、アプリケーションが使っている全てのロガーを定義して設定する必要はありません。
トップレベルのロガーだけ設定しておいて必要に応じて子ロガーを作成すれば十分です。


ハンドラ
^^^^^^^^

:class:`Handler` オブジェクトは適切なログメッセージを(ログメッセージの深刻さに基づいて)
ハンドラの指定された宛先に振り分けることに責任を持ちます。
ロガーオブジェクトには :func:`addHandler` メソッドで0個以上のハンドラを追加することができます。
有り得るシナリオとして、あるアプリケーションが全てのログメッセージをログファイルに、
error 以上の全てのログメッセージを標準出力に、
critical のメッセージは全てメールアドレスに、
送りたいとします。
この場合、三つの個別のハンドラがそれぞれの深刻さと宛先に応じて必要になります。

このライブラリには多数のハンドラを用意してありますが、
このチュートリアルでは
:class:`StreamHandler` と :class:`FileHandler` だけを例に取り上げます。

アプリケーション開発者にとってハンドラを扱う上で気にするべきメソッドは極々限られています。
備え付けのハンドラオブジェクトを使う (つまり自作ハンドラを作らない)
開発者に関係あるハンドラのメソッドは次の設定用のメソッドだけでしょう:

* :meth:`Handler.setLevel` メソッドは、ロガーオブジェクトの場合と同様に、
  適切な宛先に振り分けられるべき最も低い深刻さを指定します。
  なぜ二つも :func:`setLevel` メソッドがあるのでしょう?
  ロガーでセットされるレベルはメッセージのどの深刻さを付随するハンドラに渡すか決めます。
  ハンドラでセットされるレベルはハンドラがどのメッセージを送るべきか決めます。
  :func:`setFormatter` でこのハンドラが使用する Formatter オブジェクトを選択します。

* :func:`addFilter` および :func:`removeFilter` はそれぞれハンドラへのフィルタオブジェクトの設定、設定解除を行います。

アプリケーションのコード中ではハンドラを直接インスタンス化して使ってはなりません。
そうではなく、 :class:`Handler` クラスは全てのハンドラが持つべきインターフェイスを定義し、
子クラスが使える (もしくはオーバライドできる) いくつかのデフォルトの振る舞いを確立します。


フォーマッタ
^^^^^^^^^^^^

フォーマッタオブジェクトは最終的なログメッセージの順序、構造および内容を設定します。
基底クラスの :class:`logging.Handler` とは違って、
アプリケーションのコードはフォーマッタクラスをインスタンス化して構いませんが、
特別な振る舞いをさせたいアプリケーションではフォーマッタのサブクラスを使う可能性もあります。
コンストラクタは二つのオプション引数を取ります: メッセージのフォーマット文字列と日付のフォーマット文字列です。
メッセージのフォーマット文字列がなければ、デフォルトではメッセージをそのまま使います。
日付のフォーマット文字列がなければデフォルトは::

    %Y-%m-%d %H:%M:%S

で、最後にミリ秒が付きます。

メッセージのフォーマット文字列は ``%(<dictionary key>)s`` 形式の文字列代入を用います。
使えるキーについては :ref:`formatter-objects` に書いてあります。

下のメッセージのフォーマット文字列は、人が読みやすい形式の時刻、メッセージの深刻さ、
メッセージの内容をその順番に出力します::

    "%(asctime)s - %(levelname)s - %(message)s"


ログ記録方法の設定
^^^^^^^^^^^^^^^^^^

プログラマはログ記録方法を設定できます。
一つの方法は中心となるモジュールで上で述べたような設定メソッドで
(Python コードを使って) ロガー、ハンドラ、フォーマッタを自ら手を下して作成することです。
もう一つの方法は、ログ記録設定ファイルを作ることです。
以下のコードは、例としてごく単純なロガー、コンソールハンドラ、そして単純なフォーマッタを
Python モジュールの中で設定しています::

    import logging

    # create logger
    logger = logging.getLogger("simple_example")
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    # "application" code
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")

このモジュールをコマンドラインから実行すると、以下の出力が得られます::

    $ python simple_logging_module.py
    2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
    2005-03-19 15:10:26,620 - simple_example - INFO - info message
    2005-03-19 15:10:26,695 - simple_example - WARNING - warn message
    2005-03-19 15:10:26,697 - simple_example - ERROR - error message
    2005-03-19 15:10:26,773 - simple_example - CRITICAL - critical message

次の Python モジュールもロガー、ハンドラ、フォーマッタを上の例とほぼ同じ形で生成しますが、
オブジェクトの名前だけが異なります::

    import logging
    import logging.config

    logging.config.fileConfig("logging.conf")

    # create logger
    logger = logging.getLogger("simpleExample")

    # "application" code
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")

そしてこれが logging.conf ファイルです::

    [loggers]
    keys=root,simpleExample

    [handlers]
    keys=consoleHandler

    [formatters]
    keys=simpleFormatter

    [logger_root]
    level=DEBUG
    handlers=consoleHandler

    [logger_simpleExample]
    level=DEBUG
    handlers=consoleHandler
    qualname=simpleExample
    propagate=0

    [handler_consoleHandler]
    class=StreamHandler
    level=DEBUG
    formatter=simpleFormatter
    args=(sys.stdout,)

    [formatter_simpleFormatter]
    format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
    datefmt=

出力は設定ファイルを使わないバージョンとほぼ同じです::

    $ python simple_logging_config.py
    2005-03-19 15:38:55,977 - simpleExample - DEBUG - debug message
    2005-03-19 15:38:55,979 - simpleExample - INFO - info message
    2005-03-19 15:38:56,054 - simpleExample - WARNING - warn message
    2005-03-19 15:38:56,055 - simpleExample - ERROR - error message
    2005-03-19 15:38:56,130 - simpleExample - CRITICAL - critical message

設定ファイル経由の方が Python コード経由に比べていくつかの利点を有していることが見て取れると思います。
設定とコードの分離が最大の違いで、プログラマ以外にも容易にログ出力の表現を変更できます。

.. _library-config:

ライブラリのためのログ記録方法の設定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ログ記録を行うライブラリを開発するときには、いくつかその設定について考えておくべきことがあります。
ライブラリを使うアプリケーションが logging を使っていないときに、
ライブラリが logging を呼び出すと "No handlers could be found for logger X.Y.Z"
(「ロガー X.Y.Z に対するハンドラが見つかりません」)
というメッセージがコンソールに一度だけ流れます。
このメッセージは logging の設定ミスを捕らえるためのものですが、
ライブラリが logging を使っているとアプリケーション開発者が知らない場合混乱につながりかねません。

ライブラリが logging をどのように使っているかを文書に書くだけでなく、
意図しないメッセージを出さないために何もしないハンドラを加えるように設定しておくのが良い方法です。
こうすればメッセージが出力されるのを(ハンドラが見つかるので)防げるので、何も出力しないようになります。
ライブラリを使ってアプリケーションを書くユーザーが logging の設定をするならば、
おそらくその設定で何かハンドラを追加することでしょう。
その中でレベルが適切に設定されていればライブラリコード中の logging 呼び出しはそのハンドラに(普段通りに)出力を送ります。

何もしないハンドラは以下のよう簡単に定義できます::

    import logging

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

このハンドラのインスタンスがライブラリで使われるログ記録の名前空間の最上位ロガーに追加されなければなりません。
ライブラリ *foo* のログ記録が全て "foo.x.y" にマッチする名前のロガーで行われるならば、
次のコードで望むような効果を得られます::

    import logging

    h = NullHandler()
    logging.getLogger("foo").addHandler(h)

組織がいくつものライブラリを世に出しているならば、指定されるロガーの名前は単なる "foo"
ではなく "orgname.foo" かもしれませんね。


ログレベル
----------

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

#. :class:`handlers.BaseRotatingHandler` はログファイルをある時点で交替させる\
   ハンドラの基底クラスです。直接インスタンス化するためのクラスではありません。
   :class:`RotatingFileHandler`
   や :class:`TimedRotatingFileHandler` を使うようにしてください。

#. :class:`handlers.RotatingFileHandler` のインスタンスは最大ログファイルの\
   サイズ指定とログファイルの交替機能をサポートしながら、ディスク上のファイルにエラーメッセージを送信します。

#. :class:`handlers.TimedRotatingFileHandler` のインスタンスは、ログファイルを\
   一定時間間隔ごとに交替しながら、ディスク上のファイルにエラーメッセージを送信します。

#. :class:`handlers.SocketHandler` のインスタンスは TCP/IP ソケットにエラーメッセージを送信します。

#. :class:`handlers.DatagramHandler` のインスタンスは UDP ソケットにエラーメッセージを送信します。

#. :class:`handlers.SMTPHandler` のインスタンスは指定された電子メールアドレスにエラーメッセージを送信します。

#. :class:`handlers.SysLogHandler` のインスタンスは遠隔を含むマシン上の syslog デーモンにエラーメッセージを送信します。

#. :class:`handlers.NTEventLogHandler` のインスタンスは Windows NT/2000/XP イベントログにエラーメッセージを送信します。

#. :class:`handlers.MemoryHandler` のインスタンスはメモリ上のバッファにエラーメッセージを送信し、指定された条件でフラッシュされるようにします。

#. :class:`handlers.HTTPHandler` のインスタンスは ``GET`` か ``POST`` セマンティクスを使って HTTP
   サーバにエラーメッセージを送信します。

#. :class:`handlers.WatchedFileHandler` のインスタンスはログ記録を行うファイルを監視します。
   もしファイルが変われば、一旦ファイルを閉じた後ファイル名を使って再度開きます。
   このハンドラは Unix ライクなシステムでだけ有用です。
   Windows では元にしている機構がサポートされていません。

:class:`StreamHandler` および :class:`FileHandler` クラスは、中核となる\
ログ化機構パッケージ内で定義されています。他のハンドラはサブモジュール、
:mod:`logging.handlers` で定義されています。
(サブモジュールにはもうひとつ :mod:`logging.config` があり、
これは環境設定機能のためのものです。)

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
   を生成してルートロガーに追加し、ログ記録システムの基本的な環境設定を行います。
   この関数はルートロガーに対しハンドラが一つも定義されていなければ何もしません。
   関数 :func:`debug`, :func:`info`, :func:`warning`, :func:`error`, および :func:`critical`
   は、ルートロガーにハンドラが定義されていない場合に自動的に :func:`basicConfig`
   を呼び出します。

   この関数はルートロガーに設定されたハンドラがあれば何もしません。

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
   | ``stream``   | 指定されたストリームを StreamHandler の初期化に使います。この引数は  |
   |              | 'filename' と同時には使えないことに注意してください。                |
   |              | 両方が指定されたときには 'stream' は無視されます                     |
   +--------------+----------------------------------------------------------------------+


.. function:: shutdown()

   ログ記録システムに対して、バッファのフラッシュを行い、全てのハンドラを閉じることで順次シャットダウンを行うように告知します。
   この関数はアプリケーションの exit 時に呼ばれるべきであり、
   また呼びだし以降はそれ以上ログ記録システムを使ってはなりません。


.. function:: setLoggerClass(klass)

   ログ記録システムに対して、ロガーをインスタンス化する際にクラス *klass* を使うように指示します。指定するクラスは引数として名前だけをとるようなメソッド
   :meth:`__init__` を定義していなければならず、 :meth:`__init__` では :meth:`Logger.__init__`
   を呼び出さなければなりません。典型的な利用法として、この関数は自作のロガーを必要とするようなアプリケーションにおいて、他のロガーが
   インスタンス化される前にインスタンス化されます。


.. seealso::

   :pep:`282` - A Logging System
      本機能を Python 標準ライブラリに含めるよう記述している提案書。

   `この logging パッケージのオリジナル <http://www.red-dove.com/python_logging.html>`_
      オリジナルの :mod:`logging` パッケージ。このサイトにあるバージョンのパッケージは、標準で :mod:`logging` パッケージを含まな
      いPython 1.5.2 と 2.1.x、2.2.xでも使用できます


Logger オブジェクト
-------------------

ロガーは以下の属性とメソッドを持ちます。ロガーを直接インスタンス化することはできず、常にモジュール関数
``logging.getLogger(name)`` を介してインスタンス化するので注意してください。


.. attribute:: Logger.propagate

   この値の評価結果が偽になる場合、ログ記録しようとするメッセージはこのロガーに渡されず、
   また子ロガーから上位の (親の) ロガーに渡されません。
   コンストラクタはこの属性を 1 に設定します。


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
   ``logging.disable(lvl)`` で設定されるモジュールレベルの深刻さレベルを調べ、次にロガーの実効レベルを
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

   呼び出し元のソースファイル名と行番号を調べます。
   ファイル名と行番号と関数名を 3 要素のタプルで返します。

   .. versionchanged:: 2.4
      関数名も加えられました。
      以前のバージョンではファイル名と行番号を 2 要素のタプルで返していました。


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

出力の書式化には、通常の Python 文字列に対する初期化を使います -  :ref:`string-formatting`
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

.. _context-info:

文脈情報をログ記録出力に付加する
--------------------------------

時にはログ記録出力にログ関数の呼び出し時に渡されたパラメータに加えて文脈情報を含めたいこともあるでしょう。
たとえば、ネットワークアプリケーションで、クライアント固有の情報
(例: リモートクライアントの名前、IP アドレス)
もログ記録に残しておきたいと思ったとしましょう。
*extra* パラメータをこの目的に使うこともできますが、
いつでもこの方法で情報を渡すのが便利なやり方とも限りません。
また接続ごとに :class:`Logger` インスタンスを生成する誘惑に駆られるかもしれませんが、
インスタンスがガーベジコレクションで回収されず良いアイデアとは言えません。
現実的な問題ではないかもしれませんが、
:class:`Logger` インスタンスの個数がアプリケーションの中でログ記録を行いたい粒度のレベルに依存する場合、
:class:`Logger` インスタンスの個数がきちんと押さえられないと管理が難しくなってしまいます。

ログ記録イベントの情報と一緒に出力される文脈情報を渡す簡単な方法は、
:class:`LoggerAdapter` を使うことです。
このクラスは :class:`Logger` のように見えるようにデザインされていて、
:meth:`debug`, :meth:`info`, :meth:`warning`, :meth:`error`,
:meth:`exception`, :meth:`critical`, :meth:`log` の各メソッドを呼び出せるようになっています。
これらのメソッドは対応する :class:`Logger` のメソッドと同じ引数を取りますので、
二つの型を取り替えて使うことができます。

:class:`LoggerAdapter` のインスタンスを生成する際には、
:class:`Logger` インスタンスと文脈情報を収めた辞書風のオブジェクトを渡します。
:class:`LoggerAdapter` のログ記録メソッドを呼び出すと、
呼び出しをコンストラクタに渡された配下の :class:`Logger` インスタンスに委譲し、
その際文脈情報をその委譲された呼び出しに埋め込みます。
:class:`LoggerAdapter` のコードから少し抜き出してみます::

    def debug(self, msg, *args, **kwargs):
        """
        Delegate a debug call to the underlying logger, after adding
        contextual information from this adapter instance.
        """
        msg, kwargs = self.process(msg, kwargs)
        self.logger.debug(msg, *args, **kwargs)

:class:`LoggerAdapter` の :meth:`process` メソッドが文脈情報をログ出力に加える舞台です。
そこではログ記録呼び出しのメッセージとキーワード引数が渡され、
加工された(はずの)それらの情報を配下のロガーへの呼び出しに渡し直します。
このメソッドのデフォルト実装ではメッセージは元のままですが、
キーワード引数にはコンストラクタに渡された辞書風オブジェクトを値として
"extra" キーが挿入されます。
もちろん、呼び出し時に "extra" キーワードを使った場合には何事もなかったかのように上書きされます。

"extra" を用いる利点は辞書風オブジェクトの中の値が :class:`LogRecord` インスタンスの
__dict__ にマージされることで、
辞書風オブジェクトのキーを知っている :class:`Formatter` を用意して文字列をカスタマイズするようにできることです。
それ以外のメソッドが必要なとき、たとえば文脈情報をメッセージの前や後ろにつなげたい場合には、
:class:`LoggerAdapter` から :meth:`process` を望むようにオーバライドしたサブクラスを作ることが必要なだけです。
次に挙げるのはこのクラスを使った例で、どの辞書風の振る舞いがコンストラクタで使われる「辞書風」オブジェクトに必要なのかも見せます::

   import logging

   class ConnInfo:
       """
       An example class which shows how an arbitrary class can be used as
       the 'extra' context information repository passed to a LoggerAdapter.
       """

       def __getitem__(self, name):
           """
           To allow this instance to look like a dict.
           """
           from random import choice
           if name == "ip":
               result = choice(["127.0.0.1", "192.168.0.1"])
           elif name == "user":
               result = choice(["jim", "fred", "sheila"])
           else:
               result = self.__dict__.get(name, "?")
           return result

       def __iter__(self):
           """
           To allow iteration over keys, which will be merged into
           the LogRecord dict before formatting and output.
           """
           keys = ["ip", "user"]
           keys.extend(self.__dict__.keys())
           return keys.__iter__()

   if __name__ == "__main__":
       from random import choice
       levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
       a1 = logging.LoggerAdapter(logging.getLogger("a.b.c"),
                                  { "ip" : "123.231.231.123", "user" : "sheila" })
       logging.basicConfig(level=logging.DEBUG,
                           format="%(asctime)-15s %(name)-5s %(levelname)-8s IP: %(ip)-15s User: %(user)-8s %(message)s")
       a1.debug("A debug message")
       a1.info("An info message with %s", "some parameters")
       a2 = logging.LoggerAdapter(logging.getLogger("d.e.f"), ConnInfo())
       for x in range(10):
           lvl = choice(levels)
           lvlname = logging.getLevelName(lvl)
           a2.log(lvl, "A message at %s level with %d %s", lvlname, 2, "parameters")

このスクリプトが実行されると、出力は以下のようになります::

   2008-01-18 14:49:54,023 a.b.c DEBUG    IP: 123.231.231.123 User: sheila   A debug message
   2008-01-18 14:49:54,023 a.b.c INFO     IP: 123.231.231.123 User: sheila   An info message with some parameters
   2008-01-18 14:49:54,023 d.e.f CRITICAL IP: 192.168.0.1     User: jim      A message at CRITICAL level with 2 parameters
   2008-01-18 14:49:54,033 d.e.f INFO     IP: 192.168.0.1     User: jim      A message at INFO level with 2 parameters
   2008-01-18 14:49:54,033 d.e.f WARNING  IP: 192.168.0.1     User: sheila   A message at WARNING level with 2 parameters
   2008-01-18 14:49:54,033 d.e.f ERROR    IP: 127.0.0.1       User: fred     A message at ERROR level with 2 parameters
   2008-01-18 14:49:54,033 d.e.f ERROR    IP: 127.0.0.1       User: sheila   A message at ERROR level with 2 parameters
   2008-01-18 14:49:54,033 d.e.f WARNING  IP: 192.168.0.1     User: sheila   A message at WARNING level with 2 parameters
   2008-01-18 14:49:54,033 d.e.f WARNING  IP: 192.168.0.1     User: jim      A message at WARNING level with 2 parameters
   2008-01-18 14:49:54,033 d.e.f INFO     IP: 192.168.0.1     User: fred     A message at INFO level with 2 parameters
   2008-01-18 14:49:54,033 d.e.f WARNING  IP: 192.168.0.1     User: sheila   A message at WARNING level with 2 parameters
   2008-01-18 14:49:54,033 d.e.f WARNING  IP: 127.0.0.1       User: jim      A message at WARNING level with 2 parameters

.. versionadded:: 2.6

:class:`LoggerAdapter` クラスは以前のバージョンにはありません。


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

   ハンドラで使われている全てのリソースを始末します。
   このバージョンでは何も出力しませんが、内部リストから
   :func:`shutdown` が呼ばれたときに閉じられるハンドラを削除します。
   サブクラスではオーバライドされた :meth:`close` メソッドからこのメソッドが必ず呼ばれるようにして下さい。


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

.. module:: logging.handlers

:class:`StreamHandler` クラスは、 :mod:`logging` パッケージのコアにありますが、ログ出力を
*sys.stdout*, *sys.stderr* あるいは何らかのファイル類似オブジェクト(あるいは、もっと正確にいえば、 :meth:`write`
および :meth:`flush` メソッドをサポートする何らかのオブジェクト) といったストリームに送信します。


.. class:: StreamHandler([strm])

   :class:`StreamHandler` クラスの新たなインスタンスを返します。 *strm* が指定された場合、インスタンスはログ出力先として
   指定されたストリームを使います; そうでない場合、 *sys.stderr* が使われます。


   .. method:: emit(record)

      フォーマッタが指定されていれば、フォーマッタを使ってレコードを書式化します。
      次に、レコードがストリームに書き込まれ、末端に改行がつけられます。
      例外情報が存在する場合、 :func:`traceback.print_exception` を使って書式化され、
      ストリームの末尾につけられます。


   .. method:: flush()

      ストリームの :meth:`flush` メソッドを呼び出してバッファをフラッシュします。
      :meth:`close` メソッドは :class:`Handler` から継承しているため何も行わないので、 :meth:`flush` 呼び出しを明示的に行う必要があります。


FileHandler
^^^^^^^^^^^

:class:`FileHandler` クラスは、 :mod:`logging` パッケージのコアにありますが、ログ出力をディスク上のファイルに送信します。このクラスは出力機能を :class:`StreamHandler` から継承しています。


.. class:: FileHandler(filename[, mode[, encoding[, delay]]])

   :class:`FileHandler` クラスの新たなインスタンスを返します。
   指定されたファイルが開かれ、ログ記録のためのストリームとして使われます。 
   *mode* が指定されなかった場合、 :const:`'a'` が使われます。
   *encoding* が *None* でない場合、その値はファイルを開くときのエンコーディングとして使われます。
   *delay* が真であるならば、ファイルを開くのは最初の :meth:`emit` 呼び出しまで遅らせられます。
   デフォルトでは、ファイルは無制限に大きくなりつづけます。


   .. method:: close()

      ファイルを閉じます。


   .. method:: emit(record)

      *record* をファイルに出力します。

:class:`NullHandler` の使い方について詳しくは :ref:`library-config` を参照して下さい。

WatchedFileHandler
^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.6

:class:`WatchedFileHandler` クラスは、 :mod:`logging.handlers` モジュールにあり、
ログ記録先のファイルを監視する :class:`FileHandler` の一種です。
ファイルが変わった場合、ファイルを閉じてからファイル名を使って開き直します。

ファイルはログファイルをローテーションさせる *newsyslog* や
*logrotate* のようなプログラムを使うことで変わることがあります。
このハンドラは、Unix/Linux で使われることを意図していますが、
ファイルが最後にログを emit してから変わったかどうかを監視します。
(ファイルはデバイスや inode が変わることで変わったと判断します。)
ファイルが変わったら古いファイルのストリームは閉じて、現在のファイルを新しいストリームを取得するために開きます。

このハンドラを Windows で使うことは適切ではありません。
というのも Windows では開いているログファイルを動かしたり削除したりできないからです
- logging はファイルを排他的ロックを掛けて開きます -
そしてそれゆえにこうしたハンドラは必要ないのです。
さらに、Windows では *ST_INO* がサポートされていません
(:func:`stat` はこの値として常に 0 を返します)。

.. class:: WatchedFileHandler(filename[,mode[, encoding[, delay]]])

   :class:`WatchedFileHandler` クラスの新たなインスタンスを返します。
   指定されたファイルが開かれ、ログ記録のためのストリームとして使われます。
   *mode* が指定されなかった場合、 :const:`"a"` が使われます。
   *encoding* が *None* でない場合、その値はファイルを開くときのエンコーディングとして使われます。
   *delay* が真であるならば、ファイルを開くのは最初の :meth:`emit` 呼び出しまで遅らせられます。
   デフォルトでは、ファイルは無制限に大きくなりつづけます。

   .. method:: emit(record)

      レコードをファイルに出力しますが、その前にファイルが変わっていないかチェックします。
      もし変わっていれば、レコードをファイルに出力する前に、
      既存のストリームはフラッシュして閉じられ、ファイルが再度開かれます。


RotatingFileHandler
^^^^^^^^^^^^^^^^^^^

:class:`RotatingFileHandler` クラスは、
:mod:`logging.handlers` モジュールの中にありますが、
ディスク上のログファイルに対するローテーション処理をサポートします。


.. class:: RotatingFileHandler(filename[, mode[, maxBytes[, backupCount[, encoding[, delay]]]]])

   :class:`RotatingFileHandler` クラスの新たなインスタンスを返します。
   指定されたファイルが開かれ、ログ記録のためのストリームとして使われます。
   *mode* が指定されなかった場合、 :const:`"a"` が使われます。
   *encoding* が *None* でない場合、その値はファイルを開くときのエンコーディングとして使われます。
   *delay* が真であるならば、ファイルを開くのは最初の :meth:`emit` 呼び出しまで遅らせられます。
   デフォルトでは、ファイルは無制限に大きくなりつづけます。

   あらかじめ決められたサイズでファイルをロールオーバ (:dfn:`rollover`)  させられるように、 *maxBytes* および
   *backupCount* 値を指定することができます。指定サイズを超えそうになると、ファイルは
   閉じられ、暗黙のうちに新たなファイルが開かれます。ロールオーバは現在のログファイルの長さが *maxBytes* に近くなると常に起きます。
   *backupCount* が非ゼロの場合、システムは古いログファイルをファイル名に ".1", ".2" といった拡張子を追加して保存します。
   例えば、 *backupCount* が 5 で、基本のファイル名が :file:`app.log` なら、 :file:`app.log` 、
   :file:`app.log.1` 、 :file:`app.log.2` 、 ... と続き、 :file:`app.log.5`
   までを得ることになります。ログの書き込み対象になるファイルは常に :file:`app.log` です。このファイルが満杯になると、
   ファイルは閉じられ、 :file:`app.log.1` に名称変更されます。 :file:`app.log.1` 、 :file:`app.log.2`
   などが存在する場合、それらのファイルはそれぞれ :file:`app.log.2` 、 :file:`app.log.3` といった具合に名前変更されます。


   .. method:: doRollover()

      上述のような方法でロールオーバを行います。


   .. method:: emit(record)

      上述のようなロールオーバを行いながら、レコードをファイルに出力します。


TimedRotatingFileHandler
^^^^^^^^^^^^^^^^^^^^^^^^

:class:`TimedRotatingFileHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、特定の時間間隔でのログ交替をサポートしています。


.. class:: TimedRotatingFileHandler(filename [,when [,interval [,backupCount[, encoding[, delay[, utc]]]]]])

   :class:`TimedRotatingFileHandler` クラスの新たなインスタンスを返します。 *filename*
   に指定したファイルを開き、ログ出力先のストリームとして使います。ログファイルの交替時には、ファイル名に拡張子 (suffix) を
   つけます。ログファイルの交替は *when* および *interval*  の積に基づいて行います。

   *when* は *interval* の単位を指定するために使います。
   使える値は下表の通りです。大小文字の区別は行いません:

   +----------------+-------------------+
   | 値             | *interval* の単位 |
   +================+===================+
   | ``'S'``        | 秒                |
   +----------------+-------------------+
   | ``'M'``        | 分                |
   +----------------+-------------------+
   | ``'H'``        | 時間              |
   +----------------+-------------------+
   | ``'D'``        | 日                |
   +----------------+-------------------+
   | ``'W'``        | 曜日 (0=Monday)   |
   +----------------+-------------------+
   | ``'midnight'`` | 深夜              |
   +----------------+-------------------+

   古いログファイルを保存する際にロギングシステムは拡張子を付けます。
   拡張子は日付と時間に基づいて、
   strftime の ``%Y-%m-%d_%H-%M-%S`` 形式かその前の方の一部分を、
   ロールオーバ間隔に依存した形で使います。
   *utc* 引数が真の場合時刻は UTC になり、それ以外では現地時間が使われます。

   *backupCount* がゼロでない場合、保存されるファイル数は高々 *backupCount* 個で、それ以上のファイルがロールオーバされる時に作られるならば、一番古いものが削除されます。
   削除するロジックは interval で決まるファイルを削除しますので、
   interval を変えると古いファイルが残ったままになることもあります。


   .. method:: doRollover()

      上記の方法でロールオーバを行います。


   .. method:: emit(record)

      :meth:`setRollover` で解説した方法でロールオーバを行いながら、レコードをファイルに出力します。


SocketHandler
^^^^^^^^^^^^^

:class:`SocketHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、ログ出力をネットワークソケットに送信します。基底クラスでは TCP ソケットを用います。


.. class:: SocketHandler(host, port)

   アドレスが *host* および *port* で与えられた遠隔のマシンと通信するようにした :class:`SocketHandler`
   クラスのインスタンスを生成して返します。


   .. method:: close()

      ソケットを閉じます。


   .. method:: emit()

      レコードの属性辞書を pickle 化し、バイナリ形式でソケットに書き込みます。
      ソケット操作でエラーが生じた場合、暗黙のうちにパケットは捨てられます。
      前もって接続が失われていた場合、接続を再度確立します。
      受信端でレコードを逆 pickle 化して :class:`LogRecord`
      にするには、 :func:`makeLogRecord` 関数を使ってください。


   .. method:: handleError()

      :meth:`emit` の処理中に発生したエラーを処理します。
      よくある原因は接続の消失です。
      次のイベント発生時に再度接続確立を試みることができるようにソケットを閉じます。


   .. method:: makeSocket()

      サブクラスで必要なソケット形式を詳細に定義できるようにするためのファクトリメソッドです。デフォルトの実装では、TCP ソケット
      (:const:`socket.SOCK_STREAM`) を生成します。


   .. method:: makePickle(record)

      レコードの属性辞書を pickle 化して、長さを指定プレフィクス付きのバイナリにし、ソケットを介して送信できるようにして返します。


   .. method:: send(packet)

      pickle 化された文字列 *packet* をソケットに送信します。
      この関数はネットワークが処理待ち状態の時に発生しうる部分的送信を行えます。


DatagramHandler
^^^^^^^^^^^^^^^

:class:`DatagramHandler` クラスは、 :mod:`logging.handlers` モジュールの中にありますが、
:class:`SocketHandler` を継承しており、ログ記録メッセージを UDP ソケットを介して送れるようサポートしています。


.. class:: DatagramHandler(host, port)

   アドレスが *host* および *port* で与えられた遠隔のマシンと通信するようにした :class:`DatagramHandler`
   クラスのインスタンスを生成して返します。


   .. method:: emit()

      レコードの属性辞書を pickle 化し、バイナリ形式でソケットに書き込みます。
      ソケット操作でエラーが生じた場合、暗黙のうちにパケットは捨てられます。
      前もって接続が失われていた場合、接続を再度確立します。
      受信端でレコードを逆 pickle 化して :class:`LogRecord`
      にするには、 :func:`makeLogRecord` 関数を使ってください。


   .. method:: makeSocket()

      ここで :class:`SocketHandler` のファクトリメソッドをオーバライドして UDP ソケット
      (:const:`socket.SOCK_DGRAM`) を生成しています。


   .. method:: send(s)

      pickle 化された文字列をソケットに送信します。


SysLogHandler
^^^^^^^^^^^^^

:class:`SysLogHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、ログ記録メッセージを遠隔またはローカルの Unix syslog に送信する機能をサポートしています。


.. class:: SysLogHandler([address[, facility]])

   遠隔のUnix マシンと通信するための、 :class:`SysLogHandler` クラスの新たなインスタンスを返します。マシンのアドレスは
   ``(host, port)`` のタプル形式をとる *address* で与えられます。
   *address* が指定されない場合、 ``('localhost', 514)`` が使われます。
   アドレスは UDP ソケットを使って開かれます。
   ``(host, port)`` のタプル形式の代わりに文字列で "/dev/log" のように与えることもできます。
   この場合、Unix ドメインソケットが syslog にメッセージを送るのに使われます。
   *facility* が指定されない場合、 :const:`LOG_USER` が使われます。


   .. method:: close()

      遠隔ホストのソケットを閉じます。


   .. method:: emit(record)

      レコードは書式化された後、syslog サーバに送信されます。
      例外情報が存在しても、サーバには *送信されません* 。


   .. method:: encodePriority(facility, priority)

      便宜レベル (facility) および優先度を整数に符号化します。
      値は文字列でも整数でも渡すことができます。
      文字列が渡された場合、内部の対応付け辞書が使われ、整数に変換されます。


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


   .. method:: close()

      現時点では、イベントログエントリの発信源としてのアプリケーション名をレジストリから除去することができます。
      しかしこれを行うと、イベントログビューアで意図したログをみることができなくなるでしょう - これはイベントログが .dll 名を取得するために\
      レジストリにアクセスできなければならないからです。現在のバージョンではこの操作を行いません。


   .. method:: emit(record)

      メッセージ ID、イベントカテゴリおよびイベント型を決定し、メッセージを NT イベントログに記録します。


   .. method:: getEventCategory(record)

      レコードに対するイベントカテゴリを返します。
      自作のカテゴリを指定したい場合、このメソッドをオーバライドしてください。
      このクラスのバージョンのメソッドは 0 を返します。


   .. method:: getEventType(record)

      レコードのイベント型を返します。
      自作の型を指定したい場合、このメソッドをオーバライドしてください。
      このクラスのバージョンのメソッドは、
      ハンドラの *typemap* 属性を使って対応付けを行います。
      この属性は :meth:`__init__` で初期化され、
      :const:`DEBUG`, :const:`INFO`, :const:`WARNING`, :const:`ERROR`, および
      :const:`CRITICAL` が入っています。
      自作のレベルを使っているのなら、このメソッドをオーバライドするか、
      ハンドラの *typemap* 属性に適切な辞書を配置する必要があるでしょう。


   .. method:: getMessageID(record)

      レコードのメッセージ ID を返します。
      自作のメッセージを使っているのなら、ロガーに渡される *msg* を書式化文字列ではなく ID にします。
      その上で、辞書参照を行ってメッセージ ID を得ます。
      このクラスのバージョンでは 1 を返します。この値は
      :file:`win32service.pyd` における基本となるメッセージ ID です。


SMTPHandler
^^^^^^^^^^^

:class:`SMTPHandler` クラスは、 :mod:`logging.handlers` モジュールの中にありますが、SMTP
を介したログ記録メッセージの送信機能をサポートします。


.. class:: SMTPHandler(mailhost, fromaddr, toaddrs, subject[, credentials])

   新たな :class:`SMTPHandler` クラスのインスタンスを返します。
   インスタンスは email の from および to アドレス行、および
   subject 行とともに初期化されます。
   *toaddrs* は文字列からなるリストでなければなりません非標準の SMTP
   ポートを指定するには、 *mailhost* 引数に (host, port)  のタプル形式を指定します。
   文字列を使った場合、標準の SMTP ポートが使われます。
   もし SMTP サーバが認証を必要とするならば、(username, password) のタプル形式を
   *credentials* 引数に指定することができます。

   .. versionchanged:: 2.6
      *credentials* が追加されました。


   .. method:: emit(record)

      レコードを書式化し、指定されたアドレスに送信します。


   .. method:: getSubject(record)

      レコードに応じたサブジェクト行を指定したいなら、このメソッドをオーバライドしてください。


MemoryHandler
^^^^^^^^^^^^^

:class:`MemoryHandler` は、 :mod:`logging.handlers` モジュールの中にありますが、
ログ記録するレコードをメモリ上にバッファし、
定期的にその内容をターゲット (:dfn:`target`)
となるハンドラにフラッシュする機能をサポートしています。
フラッシュ処理はバッファが一杯になるか、
ある深刻さかそれ以上のレベルをもったイベントが観測された際に行われます。

:class:`MemoryHandler` はより一般的な抽象クラス、
:class:`BufferingHandler` のサブクラスです。
この抽象クラスでは、ログ記録するレコードをメモリ上にバッファします。
各レコードがバッファに追加される毎に、
:meth:`shouldFlush` を呼び出してバッファをフラッシュすべきかどうか調べます。
フラッシュする必要がある場合、
:meth:`flush` が必要にして十分な処理を行うものと想定しています。


.. class:: BufferingHandler(capacity)

   指定した許容量のバッファでハンドラを初期化します。


   .. method:: emit(record)

      レコードをバッファに追加します。
      :meth:`shouldFlush` が真を返す場合、バッファを処理するために :meth:`flush`
      を呼び出します。


   .. method:: flush()

      このメソッドをオーバライドして、自作のフラッシュ動作を実装することができます。
      このクラスのバージョンのメソッドでは、単にバッファの内容を削除して空にします。


   .. method:: shouldFlush(record)

      バッファが許容量に達している場合に真を返します。
      このメソッドは自作のフラッシュ処理方針を実装するためにオーバライドすることができます。


.. class:: MemoryHandler(capacity[, flushLevel [, target]])

   :class:`MemoryHandler` クラスの新たなインスタンスを返します。
   インスタンスはサイズ *capacity* のバッファとともに初期化されます。
   *flushLevel* が指定されていない場合、 :const:`ERROR` が使われます。
   *target* が指定されていない場合、ハンドラが何らかの有意義な処理を行う前に
   :meth:`setTarget` でターゲットを指定する必要があります。


   .. method:: close()

      :meth:`flush` を呼び出し、ターゲットを :const:`None` に設定してバッファを消去します。


   .. method:: flush()

      :class:`MemoryHandler` の場合、フラッシュ処理は単に、バッファされたレコードをターゲットがあれば送信することを意味します。
      違った動作を行いたい場合、オーバライドしてください。


   .. method:: setTarget(target)

      ターゲットハンドラをこのハンドラに設定します。


   .. method:: shouldFlush(record)

      バッファが満杯になっているか、 *flushLevel* またはそれ以上のレコードでないかを調べます。


HTTPHandler
^^^^^^^^^^^

:class:`HTTPHandler` クラスは、 :mod:`logging.handlers` モジュールの中にありますが、ログ記録メッセージを
``GET`` または ``POST`` セマンティクスを使って Web サーバに送信する機能をサポートしています。


.. class:: HTTPHandler(host, url[, method])

   :class:`HTTPHandler` クラスの新たなインスタンスを返します。インスタンスはホストアドレス、URL および HTTP メソッドと
   ともに初期化されます。 *host* は特別なポートを使うことが必要な場合には、 ``host:port`` の形式で使うこともできます。 *method*
   が指定されなかった場合 ``GET`` が使われます。


   .. method:: emit(record)

      レコードを URL エンコードされた辞書形式で Web サーバに送信します。


.. _formatter-objects:

Formatter オブジェクト
----------------------

.. currentmodule:: logging

:class:`Formatter` は以下の属性とメソッドを持っています。 :class:`Formatter` は :class:`LogRecord` を
(通常は) 人間か外部のシステムで解釈できる文字列に変換する役割を担っています。基底クラスの :class:`Formatter`
では書式化文字列を指定することができます。何も指定されなかった場合、 ``'%(message)s'`` の値が使われます。

Formatter は書式化文字列とともに初期化され、 :class:`LogRecord` 属性に入っている知識を利用できるようにします -
上で触れたデフォルトの値では、ユーザによるメッセージと引数はあらかじめ書式化されて、 :class:`LogRecord` の *message*
属性に入っていることを利用しているようにです。この書式化文字列は、Python 標準の % を使った変換文字列で構成されます。文字列整形に関する詳細は
:ref:`string-formatting` を参照してください。

現状では、 :class:`LogRecord` の有用な属性は以下のようになっています:

+-------------------------+------------------------------------------------------------------------+
| Format                  | 説明                                                                   |
+=========================+========================================================================+
| ``%(name)s``            | ロガー (ログ記録チャネル) の名前                                       |
+-------------------------+------------------------------------------------------------------------+
| ``%(levelno)s``         | メッセージのログ記録レベルを表す数字 (DEBUG, INFO, WARNING,            |
|                         | ERROR, CRITICAL)                                                       |
+-------------------------+------------------------------------------------------------------------+
| ``%(levelname)s``       | メッセージのログ記録レベルを表す文字列 ("DEBUG",  "INFO",              |
|                         | "WARNING", "ERROR", "CRITICAL")                                        |
+-------------------------+------------------------------------------------------------------------+
| ``%(pathname)s``        | ログ記録の呼び出しが行われたソースファイルの全パス名 (取得できる場合)  |
+-------------------------+------------------------------------------------------------------------+
| ``%(filename)s``        | パス名中のファイル名部分                                               |
+-------------------------+------------------------------------------------------------------------+
| ``%(module)s``          | モジュール名 (ファイル名の名前部分)                                    |
+-------------------------+------------------------------------------------------------------------+
| ``%(funcName)s``        | ログ記録の呼び出しを含む関数の名前                                     |
+-------------------------+------------------------------------------------------------------------+
| ``%(lineno)d``          | ログ記録の呼び出しが行われたソース行番号 (取得できる場合)              |
+-------------------------+------------------------------------------------------------------------+
| ``%(created)f``         | :class:`LogRecord` が生成された時刻 (time.time()                       |
|                         | の返した値)                                                            |
+-------------------------+------------------------------------------------------------------------+
| ``%(relativeCreated)d`` | LogRecord が生成された時刻の logging                                   |
|                         | モジュールが読み込まれた時刻に対するミリ秒単位での相対的な値。         |
+-------------------------+------------------------------------------------------------------------+
| ``%(asctime)s``         | :class:`LogRecord` が生成された時刻を人間が読める書式で表したもの。    |
|                         | デフォルトでは "2003-07-08 16:49:45,896" 形式                          |
|                         | (コンマ以降の数字は時刻のミリ秒部分) です                              |
+-------------------------+------------------------------------------------------------------------+
| ``%(msecs)d``           | :class:`LogRecord` が生成された時刻の、ミリ秒部分                      |
+-------------------------+------------------------------------------------------------------------+
| ``%(thread)d``          | スレッド ID (取得できる場合)                                           |
+-------------------------+------------------------------------------------------------------------+
| ``%(threadName)s``      | スレッド名 (取得できる場合)                                            |
+-------------------------+------------------------------------------------------------------------+
| ``%(process)d``         | プロセス ID (取得できる場合)                                           |
+-------------------------+------------------------------------------------------------------------+
| ``%(message)s``         | レコードが発信された際に処理された  ``msg % args`` の結果              |
+-------------------------+------------------------------------------------------------------------+

.. versionchanged:: 2.5
   *funcName* が追加されました.


.. class:: Formatter([fmt[, datefmt]])

   :class:`Formatter` クラスの新たなインスタンスを返します。インスタンスは全体としてのメッセージに対する書式化文字列と、メッセージの
   日付/時刻部分のための書式化文字列を伴って初期化されます。 *fmt*  が指定されない場合、 ``'%(message)s'`` が使われます。
   *datefmt* が指定されない場合、ISO8601 日付書式が使われます。


   .. method:: format(record)

      レコードの属性辞書が、文字列を書式化する演算で被演算子として使われます。
      書式化された結果の文字列を返します。辞書を書式化する前に、二つの準備段階を経ます。
      レコードの *message* 属性が *msg* % *args* を使って処理されます。
      書式化された文字列が :const:`'(asctime)'` を含むなら、
      :meth:`formatTime` が呼び出され、イベントの発生時刻を書式化します。
      例外情報が存在する場合、 :meth:`formatException`  を使って書式化され、メッセージに追加されます。
      ここで注意していただきたいのは、書式化された例外情報は *exc_text*
      にキャッシュされるという点です。
      これが有用なのは例外情報がピックル化されて回線上を送ることができるからですが、
      しかし二つ以上の :class:`Formatter` サブクラスで例外情報の書式化をカスタマイズしている場合には注意が必要になります。
      この場合、フォーマッタが書式化を終えるごとにキャッシュをクリアして、
      次のフォーマッタがキャッシュされた値を使わずに新鮮な状態で再計算するようにしなければならないことになります。


   .. method:: formatTime(record[, datefmt])

      このメソッドは、フォーマッタが書式化された時間を利用したい際に、
      :meth:`format` から呼び出されます。このメソッドは特定の要求を\
      提供するためにフォーマッタで上書きすることができますが、
      基本的な振る舞いは以下のようになります: *datefmt* (文字列) が指定された\
      場合、レコードが生成された時刻を書式化するために :func:`time.strftime`
      で使われます。そうでない場合、ISO8601 書式が使われます。結果の文字列が返されます。


   .. method:: formatException(exc_info)

      指定された例外情報 (:func:`sys.exc_info` が返すような標準例外のタプル)
      を文字列として書式化します。
      デフォルトの実装は単に :func:`traceback.print_exception` を使います。
      結果の文字列が返されます。


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


   .. method:: filter(record)

      指定されたレコードがログされているか？
      されていなければゼロを、されていればゼロでない値を返します。
      適切と判断されれば、このメソッドによってレコードはその場で修正されることがあります。


LogRecord オブジェクト
----------------------

何かをログ記録する際には常に :class:`LogRecord` インスタンスが生成されます。
インスタンスにはログ記録されることになっているイベントに関係する全ての情報が入っています。インスタンスに渡される主要な情報は  *msg* および
*args* で、これらは msg % args を使って組み合わせられ、レコードのメッセージフィールドを生成します。
レコードはまた、レコードがいつ生成されたか、ログ記録がソースコード行のどこで呼び出されたか、あるいはログ記録すべき何らかの例外情報
といった情報も含んでいます。


.. class:: LogRecord(name, lvl, pathname, lineno, msg, args, exc_info [, func])

   関係のある情報とともに初期化された :class:`LogRecord` のインスタンスを返します。 *name* はロガーの名前です; *lvl*
   は数字で表されたレベルです; *pathname* はログ記録呼び出しが見つかったソースファイルの絶対パス名です。 *msg* はユーザ定義のメッセージ
   (書式化文字列) です; *args* はタプルで、 *msg* と合わせて、ユーザメッセージを生成します; *exc_info* は例外情報のタプルで、
   :func:`sys.exc_info` を呼び出して得られたもの (または、例外情報が取得できない場合には :const:`None`) です。
   *func* は logging 呼び出しを行った関数の名前です。
   指定されなければデフォルトは ``None`` です。

   .. versionchanged:: 2.5
      *func* が追加されました。


   .. method:: getMessage()

      ユーザが供給した引数をメッセージに交ぜた後、この :class:`LogRecord` インスタンスへのメッセージを返します。


LoggerAdapter オブジェクト
--------------------------

.. versionadded:: 2.6

:class:`LoggerAdapter` インスタンスは文脈情報をログ記録呼び出しに渡すのを簡単にするために使われます。
使い方の例は `文脈情報をログ記録出力に付加する`__ を参照して下さい。

__ context-info_

.. class:: LoggerAdapter(logger, extra)

   内部で使う :class:`Logger` インスタンスと辞書風オブジェクトで初期化した
   :class:`LoggerAdapter` のインスタンスを返します。

   .. method:: process(meg, kwargs)

      文脈情報を挿入するために、ログ記録呼び出しに渡されたメッセージおよび/またはキーワード引数に変更を加えます。
      ここでの実装は *extra* としてコンストラクタに渡されたオブジェクトを取り、
      'extra' キーを使って *kwargs* に加えます。
      返値は (*msg*, *kwargs*) というタプルで、
      (変更されているはずの) 渡された引数を含みます。

上のメソッドに加えて、 :class:`LoggerAdapter` は :class:`Logger` にある全てのログ記録メソッド、すなわち
:meth:`debug`, :meth:`info`, :meth:`warning`,
:meth:`error`, :meth:`exception`, :meth:`critical`, :meth:`log`
をサポートします。
これらのメソッドは対応する :class:`Logger` のメソッドと同じ引数を取りますので、
二つの型を取り替えて使うことができます。

.. ここまで


スレッド安全性
--------------

*logging* モジュールは、クライアントで特殊な作業を必要としないかぎりスレッド安全
(thread-safe) なようになっています。
このスレッド安全性はスレッドロックによって達成されています;
モジュールの共有データへのアクセスを直列化するためのロックが一つ存在し、
各ハンドラでも根底にある I/O へのアクセスを直列化するためにロックを生成します。


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

   設定を送るには、まず設定ファイルを読み、それを4バイトからなる長さを
   ``struct.pack('>L', n)`` を使ってバイナリにパックしたものを\
   前に付けたバイト列としてソケットに送ります。


.. function:: stopListening()

   :func:`listen` を呼び出して作成された、待ち受け中のサーバを停止します。通常 :func:`listen` の戻り値に対して
   :meth:`join` が呼ばれる前に呼び出します。


.. _logging-config-fileformat:

環境設定ファイルの書式
^^^^^^^^^^^^^^^^^^^^^^

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

.. versionchanged:: 2.6
   ハンドラクラスのドット区切りモジュールおよびクラス名としての解決のサポートが追加された。

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
互換の日付/時刻書式化文字列です。空文字列の場合、パッケージによって ISO8601 形式の日付/時刻に置き換えられ、日付書式化文字列 ``"%Y-%m-%d %H:%M:%S"`` を指定した場合とほとんど同じになります。
ISO8601 形式ではミリ秒も指定しており、上の書式化文字列の結果にカンマで区切って追加されます。ISO8601 形式の時刻の例は ``2003-01-23
00:29:50,411`` です。

``class`` エントリはオプションです。 ``class`` はフォーマッタのクラス名
(ドット区切りのモジュールとクラス名として)を示します。このオプションは :class:`Formatter` のサブクラスをインスタンス化するのに有用です。
:class:`Formatter` のサブクラスは例外トレースバックを展開された形式または圧縮された形式で表現することができます。


設定サーバの例
^^^^^^^^^^^^^^

ログ記録設定サーバを使うモジュールの例です::

    import logging
    import logging.config
    import time
    import os

    # read initial config file
    logging.config.fileConfig("logging.conf")

    # create and start listener on port 9999
    t = logging.config.listen(9999)
    t.start()

    logger = logging.getLogger("simpleExample")

    try:
        # loop through logging calls to see the difference
        # new configurations make, until Ctrl+C is pressed
        while True:
            logger.debug("debug message")
            logger.info("info message")
            logger.warn("warn message")
            logger.error("error message")
            logger.critical("critical message")
            time.sleep(5)
    except KeyboardInterrupt:
        # cleanup
        logging.config.stopListening()
        t.join()

そしてファイル名を受け取ってそのファイルをサーバに送るスクリプトですが、
それに先だってバイナリエンコード長を新しいログ記録の設定として先に送っておきます::

    #!/usr/bin/env python
    import socket, sys, struct

    data_to_send = open(sys.argv[1], "r").read()

    HOST = 'localhost'
    PORT = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "connecting..."
    s.connect((HOST, PORT))
    print "sending config..."
    s.send(struct.pack(">L", len(data_to_send)))
    s.send(data_to_send)
    s.close()
    print "complete"


さらなる例
----------

複数のハンドラおよびフォーマッタ
--------------------------------

ロガーは通常の Python オブジェクトです。
:func:`addHandler` メソッドには追加されるハンドラの個数について最少数も最多数も定めていません。
時にアプリケーションが全ての深刻さの全てのメッセージをテキストファイルに記録しつつ、
同時にエラーやそれ以上のものをコンソールに出力することが役に立ちます。
これを実現する方法は、単に適切なハンドラを設定するだけです。
アプリケーションコードの中のログ記録の呼び出しは変更されずに残ります。
少し前に取り上げた単純なモジュール式の例を少し変えるとこうなります::

    import logging

    logger = logging.getLogger("simple_example")
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler("spam.log")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    # "application" code
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")

「アプリケーション」のコードは複数のハンドラについて何も気にしていないことに注目して下さい。
変更した箇所は新しい *fh* という名のハンドラを追加して設定したところが全てです。

新しいハンドラを高い(もしくは低い)深刻さに対するフィルタを具えて生成できることは、
アプリケーションを書いてテストを行うときとても助けになります。
デバッグ用にたくさんの ``print`` 文を使う代わりに ``logger.debug`` を使いましょう。
あとで消したりコメントアウトしたりしなければならない print 文と違って、
logger.debug 命令はソースコードの中にそのまま残しておいて再び必要になるまで休眠させておけます。
その時必要になるのはただロガーおよび/またはハンドラの深刻さの設定をいじることだけです。


複数のモジュールで logging を使う
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

上で述べたように ``logging.getLogger('someLogger')`` の複数回の呼び出しは同じロガーへの参照を返します。
これは一つのモジュールの中からに限らず、同じ Python インタプリタプロセス乗で動いている限りはモジュールをまたいでも正しいのです。
同じオブジェクトへの参照という点でも正しいです。
さらに、一つのモジュールの中で親ロガーを定義して設定し、別のモジュールで子ロガーを定義する(ただし設定はしない)ことが可能で、全ての子ロガーへの呼び出しは親にまで渡されます。
まずはメインのモジュールです::

    import logging
    import auxiliary_module

    # create logger with "spam_application"
    logger = logging.getLogger("spam_application")
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler("spam.log")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("creating an instance of auxiliary_module.Auxiliary")
    a = auxiliary_module.Auxiliary()
    logger.info("created an instance of auxiliary_module.Auxiliary")
    logger.info("calling auxiliary_module.Auxiliary.do_something")
    a.do_something()
    logger.info("finished auxiliary_module.Auxiliary.do_something")
    logger.info("calling auxiliary_module.some_function()")
    auxiliary_module.some_function()
    logger.info("done with auxiliary_module.some_function()")

そして補助モジュール(auxiliary_module)がこちらです::

    import logging

    # create logger
    module_logger = logging.getLogger("spam_application.auxiliary")

    class Auxiliary:
        def __init__(self):
            self.logger = logging.getLogger("spam_application.auxiliary.Auxiliary")
            self.logger.info("creating an instance of Auxiliary")
        def do_something(self):
            self.logger.info("doing something")
            a = 1 + 1
            self.logger.info("done doing something")

    def some_function():
        module_logger.info("received a call to \"some_function\"")

出力はこのようになります::

    2005-03-23 23:47:11,663 - spam_application - INFO -
       creating an instance of auxiliary_module.Auxiliary
    2005-03-23 23:47:11,665 - spam_application.auxiliary.Auxiliary - INFO -
       creating an instance of Auxiliary
    2005-03-23 23:47:11,665 - spam_application - INFO -
       created an instance of auxiliary_module.Auxiliary
    2005-03-23 23:47:11,668 - spam_application - INFO -
       calling auxiliary_module.Auxiliary.do_something
    2005-03-23 23:47:11,668 - spam_application.auxiliary.Auxiliary - INFO -
       doing something
    2005-03-23 23:47:11,669 - spam_application.auxiliary.Auxiliary - INFO -
       done doing something
    2005-03-23 23:47:11,670 - spam_application - INFO -
       finished auxiliary_module.Auxiliary.do_something
    2005-03-23 23:47:11,671 - spam_application - INFO -
       calling auxiliary_module.some_function()
    2005-03-23 23:47:11,672 - spam_application.auxiliary - INFO -
       received a call to "some_function"
    2005-03-23 23:47:11,673 - spam_application - INFO -
       done with auxiliary_module.some_function()
