:mod:`logging` --- Python 用ロギング機能
========================================

.. module:: logging
   :synopsis: アプリケーションのための、柔軟なエラーロギングシステム


.. moduleauthor:: Vinay Sajip <vinay_sajip@red-dove.com>
.. sectionauthor:: Vinay Sajip <vinay_sajip@red-dove.com>


.. index:: pair: Errors; logging

.. versionadded:: 2.3


.. This module defines functions and classes which implement a flexible error
.. logging system for applications.

このモジュールでは、アプリケーションのための柔軟なエラーログ記録 (logging) システムを実装するための関数やクラスを定義しています。


.. Logging is performed by calling methods on instances of the :class:`Logger`
.. class (hereafter called :dfn:`loggers`). Each instance has a name, and they are
.. conceptually arranged in a namespace hierarchy using dots (periods) as
.. separators. For example, a logger named "scan" is the parent of loggers
.. "scan.text", "scan.html" and "scan.pdf". Logger names can be anything you want,
.. and indicate the area of an application in which a logged message originates.

ログ記録は :class:`Logger` クラスのインスタンス (以降 :dfn:`ロガー` :logger)
におけるメソッドを呼び出すことで行われます。各インスタンスは名前をもち、ドット (ピリオド) を区切り文字として表記することで、
概念的には名前空間中の階層構造に配置されることになります。例えば、"scan" と名づけられたロガーは "scan.text"、"scan.html"、
および "scan.pdf" ロガーの親ロガーとなります。ロガー名には何をつけてもよく、ログに記録されるメッセージの生成元となるアプリケーション中の特定の
領域を示すことになります。


.. Logged messages also have levels of importance associated with them. The default
.. levels provided are :const:`DEBUG`, :const:`INFO`, :const:`WARNING`,
.. :const:`ERROR` and :const:`CRITICAL`. As a convenience, you indicate the
.. importance of a logged message by calling an appropriate method of
.. :class:`Logger`. The methods are :meth:`debug`, :meth:`info`, :meth:`warning`,
.. :meth:`error` and :meth:`critical`, which mirror the default levels. You are not
.. constrained to use these levels: you can specify your own and use a more general
.. :class:`Logger` method, :meth:`log`, which takes an explicit level argument.

ログ記録されたメッセージにはまた、重要度レベル (level of importance) が関連付けられています。デフォルトのレベルとして提供されているものは
:const:`DEBUG` 、 :const:`INFO` 、 :const:`WARNING` 、 :const:`ERROR` および
:const:`CRITICAL` です。簡便性のために、 :class:`Logger` の適切なメソッド群を呼ぶことで、ログに記録されたメッセージの
重要性を指定することができます。それらのメソッドとは、デフォルトのレベルを反映する形で、 :meth:`debug` 、 :meth:`info` 、
:meth:`warning` 、 :meth:`error` および :meth:`critical` となっています。
これらのレベルを指定するにあたって制限はありません: :class:`Logger` のより汎用的なメソッドで、明示的なレベル指定のための引数を持つ
:meth:`log` を使って自分自身でレベルを定義したり使用したりできます。


チュートリアル
--------------

.. The key benefit of having the logging API provided by a standard library module
.. is that all Python modules can participate in logging, so your application log
.. can include messages from third-party modules.

標準ライブラリモジュールが提供するログ記録 API があることの御利益は、
全ての Python モジュールがログ記録に参加できることであり、
これによってあなたが書くアプリケーションのログにサードパーティーのモジュールが出力するメッセージを含ませることができます。


.. It is, of course, possible to log messages with different verbosity levels or to
.. different destinations.  Support for writing log messages to files, HTTP
.. GET/POST locations, email via SMTP, generic sockets, or OS-specific logging
.. mechanisms are all supported by the standard module.  You can also create your
.. own log destination class if you have special requirements not met by any of the
.. built-in classes.

もちろん、複数のメッセージをそれぞれ別々の冗舌性レベルで別々の出力先にログ記録することができます。
ログメッセージをファイルへ、HTTP GET/POST 先へ、SMTP 経由で電子メールへ、汎用のソケットへ、もしくは OS ごとのログ記録機構へ書き込むことを全て標準モジュールでサポートします。
これら組み込まれたクラスが特別な要求仕様に合わないような場合には、
独自のログ記録先クラスを作り出すこともできます。


単純な例
^^^^^^^^

.. sectionauthor:: Doug Hellmann
.. (see <http://blog.doughellmann.com/2007/05/pymotw-logging.html>)


.. Most applications are probably going to want to log to a file, so let's start
.. with that case. Using the :func:`basicConfig` function, we can set up the
.. default handler so that debug messages are written to a file:

ほとんどのアプリケーションではファイルにログ記録することを望むことになるでしょうから、
まずはこのケースから始めましょう。
:func:`basicConfig` 関数を使って、デバッグメッセージがファイルに書き込まれるように、
デフォルトのハンドラをセットアップします。


::

   import logging
   LOG_FILENAME = '/tmp/logging_example.out'
   logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

   logging.debug('This message should go to the log file')


.. And now if we open the file and look at what we have, we should find the log
.. message:

ではこのファイルを開いて結果を確認しましょう。
こんなログメッセージが見つかるでしょう:


::

   DEBUG:root:This message should go to the log file


.. If you run the script repeatedly, the additional log messages are appended to
.. the file.  To create a new file each time, you can pass a filemode argument to
.. :func:`basicConfig` with a value of ``'w'``.  Rather than managing the file size
.. yourself, though, it is simpler to use a :class:`RotatingFileHandler`:

スクリプトを繰り返し実行すると、
さらなるログメッセージがファイルに追記されていきます。
毎回新しいファイルの方が良ければ、 :func:`basicConfig` に渡すファイルモード引数を
``'w'`` にします。
ファイルサイズを自分で管理する代わりに、
もっと簡単に :class:`RotatingFileHandler` を使う手があります。


::

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


.. The result should be 6 separate files, each with part of the log history for the
.. application:

結果は分割された 6 ファイルになっているはずで、
それぞれがアプリケーションのログ記録の一部になっています。


::

   /tmp/logging_rotatingfile_example.out
   /tmp/logging_rotatingfile_example.out.1
   /tmp/logging_rotatingfile_example.out.2
   /tmp/logging_rotatingfile_example.out.3
   /tmp/logging_rotatingfile_example.out.4
   /tmp/logging_rotatingfile_example.out.5


.. The most current file is always :file:`/tmp/logging_rotatingfile_example.out`,
.. and each time it reaches the size limit it is renamed with the suffix
.. ``.1``. Each of the existing backup files is renamed to increment the suffix
.. (``.1`` becomes ``.2``, etc.)  and the ``.5`` file is erased.

最新のファイルはいつでも :file:`/tmp/logging_rotatingfile_example.out` で、
サイズの上限に達するたびに拡張子 ``.1`` を付けた名前に改名されます。
既にあるバックアップファイルはその拡張子がインクリメントされ
(``.1`` が ``.2`` になるなど)、 ``.5`` ファイルは消去されます。


.. Obviously this example sets the log length much much too small as an extreme
.. example.  You would want to set *maxBytes* to an appropriate value.

見て判るようにここでは例示のためにファイルの大きさをとんでもなく小さな値に設定しています。
実際に使うときは *maxBytes* を適切な値に設定して下さい。


.. Another useful feature of the logging API is the ability to produce different
.. messages at different log levels.  This allows you to instrument your code with
.. debug messages, for example, but turning the log level down so that those debug
.. messages are not written for your production system.  The default levels are
.. ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, ``DEBUG`` and ``NOTSET``.

ログ記録 API のもう一つの有用な仕組みが異なるメッセージを異なるログレベルで生成する能力です。
これを使えば、たとえばコードの中にデバッグメッセージを埋め込みつつ、
出荷段階でログ記録レベルを落としてこれが記録されないようにするといったことができます。
デフォルトで設定されているレベルは
``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, ``DEBUG``, ``NOTSET`` です。


.. The logger, handler, and log message call each specify a level.  The log message
.. is only emitted if the handler and logger are configured to emit messages of
.. that level or lower.  For example, if a message is ``CRITICAL``, and the logger
.. is set to ``ERROR``, the message is emitted.  If a message is a ``WARNING``, and
.. the logger is set to produce only ``ERROR``\s, the message is not emitted:

ロガー、ハンドラ、メッセージをログ記録する関数呼び出しは、どれもレベルを指定します。
ログメッセージはハンドラとロガーがそのレベル以下を吐き出す設定の時だけ吐き出されます。
たとえば、メッセージが ``CRITICAL`` でロガーが ``ERROR`` の設定ならばメッセージは吐き出されます。
一方、メッセージが ``WARNING`` でロガーが ``ERROR`` だけ生成するならば、
メッセージは吐き出されません。


::

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


.. Run the script with an argument like 'debug' or 'warning' to see which messages
.. show up at different levels:

スクリプトを 'debug' とか 'warning' といった引数で実行して、
レベルの違いによってどのメッセージが現れるようになるか見てみましょう。


::

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


.. You will notice that these log messages all have ``root`` embedded in them.  The
.. logging module supports a hierarchy of loggers with different names.  An easy
.. way to tell where a specific log message comes from is to use a separate logger
.. object for each of your modules.  Each new logger "inherits" the configuration
.. of its parent, and log messages sent to a logger include the name of that
.. logger.  Optionally, each logger can be configured differently, so that messages
.. from different modules are handled in different ways.  Let's look at a simple
.. example of how to log from different modules so it is easy to trace the source
.. of the message:

気付いたかもしれませんが、全てのログメッセージに ``root`` が埋め込まれています。
ログ記録モジュールは異なる名前のロガーの階層をサポートしているのです。
ログメッセージがどこから発生しているかを教える簡単な方法は、
プログラムのモジュールごとに別々のロガーオブジェクトを利用することです。
それぞれの新しいロガーはその親の設定を「継承」していて、
あるロガーに送られたログメッセージはそのロガーの名前を含みます。
場合によっては、ロガーをそれぞれ異なるように設定して、
それぞれのモジュールからのメッセージを異なったやり方で扱うこともできます。
では、単純な例でメッセージの出所が簡単に追跡できるように別々のモジュールからログ記録を行う方法を見てみましょう。


::

   import logging

   logging.basicConfig(level=logging.WARNING)

   logger1 = logging.getLogger('package1.module1')
   logger2 = logging.getLogger('package2.module2')

   logger1.warning('This message comes from one module')
   logger2.warning('And this message comes from another module')


.. And the output:

出力はこうなります:


::

   $ python logging_modules_example.py
   WARNING:package1.module1:This message comes from one module
   WARNING:package2.module2:And this message comes from another module


.. There are many more options for configuring logging, including different log
.. message formatting options, having messages delivered to multiple destinations,
.. and changing the configuration of a long-running application on the fly using a
.. socket interface.  All of these options are covered in depth in the library
.. module documentation.

他にもオプションはもっといろいろあります。
ログ記録方法の設定、たとえばログメッセージフォーマットを変えるオプション、
メッセージを複数の送り先に配送するようなもの、
ソケットインターフェイスを通して長く走り続けるアプリケーションの設定を途中で変更するものなどです。
全てのオプションはライブラリモジュールの文書の中でもっと細かく説明してあります。


ロガー
^^^^^^

.. The logging library takes a modular approach and offers the several categories
.. of components: loggers, handlers, filters, and formatters.  Loggers expose the
.. interface that application code directly uses.  Handlers send the log records to
.. the appropriate destination. Filters provide a finer grained facility for
.. determining which log records to send on to a handler.  Formatters specify the
.. layout of the resultant log record.

logging ライブラリはモジュラー・アプローチを取ってコンポーネントのカテゴリーをいくつかに分けています: ロガー、ハンドラ、フィルタ、フォーマッタ。
ロガーはアプリケーションのコードが直接使うインターフェイスを外部に公開しています。
ハンドラはログ記録を適切な行き先に送ります。
フィルタはどのログ記録をハンドラにおくるかを決めるさらにきめ細かい機構を提供します。
フォーマッタは最終的なログ記録のレイアウトを指定します。


.. :class:`Logger` objects have a threefold job.  First, they expose several
.. methods to application code so that applications can log messages at runtime.
.. Second, logger objects determine which log messages to act upon based upon
.. severity (the default filtering facility) or filter objects.  Third, logger
.. objects pass along relevant log messages to all interested log handlers.

:class:`Logger` オブジェクトの仕事は大きく三つに分かれます。
一つめは、アプリケーションが実行中にメッセージを記録できるように、
いくつかのメソッドをアプリケーションから呼べるようにしています。
二つめに、ロガーオブジェクトはどのメッセージに対して作用するかを、
深刻さ(デフォルトのフィルター機構)またはフィルターオブジェクトに基づいて決定します。
三つめに、ロガーオブジェクトはログハンドラがそれぞれ持っている興味に関連するログメッセージを回送します。


.. The most widely used methods on logger objects fall into two categories:
.. configuration and message sending.

ロガーオブジェクトのとりわけ広く使われるメソッドは二つのカテゴリーに分類できます:
設定とメッセージ送信です。


.. * :meth:`Logger.setLevel` specifies the lowest-severity log message a logger
..   will handle, where debug is the lowest built-in severity level and critical is
..   the highest built-in severity.  For example, if the severity level is info,
..   the logger will handle only info, warning, error, and critical messages and
..   will ignore debug messages.

* :meth:`Logger.setLevel` ロガーが扱うログメッセージの最も低い深刻さを指定します。
  ここで組み込まれた深刻さは debug が一番低く、 critical が一番高くなります。
  たとえば、深刻さが info と設定されたロガーは info, warning, error, critical
  のメッセージしか扱わず debug メッセージは無視します。


.. * :meth:`Logger.addFilter` and :meth:`Logger.removeFilter` add and remove filter
..   objects from the logger object.  This tutorial does not address filters.

* :meth:`Logger.addFilter` と :meth:`Logger.removeFilter`
  はロガーオブジェクトにフィルターを追加したり削除したりします。
  このチュートリアルではフィルターは説明しません。


.. With the logger object configured, the following methods create log messages:

設定されたロガーオブジェクトを使えば、以下のメソッドはログメッセージを作り出します:


.. * :meth:`Logger.debug`, :meth:`Logger.info`, :meth:`Logger.warning`,
..   :meth:`Logger.error`, and :meth:`Logger.critical` all create log records with
..   a message and a level that corresponds to their respective method names. The
..   message is actually a format string, which may contain the standard string
..   substitution syntax of :const:`%s`, :const:`%d`, :const:`%f`, and so on.  The
..   rest of their arguments is a list of objects that correspond with the
..   substitution fields in the message.  With regard to :const:`**kwargs`, the
..   logging methods care only about a keyword of :const:`exc_info` and use it to
..   determine whether to log exception information.

* :meth:`Logger.debug`, :meth:`Logger.info`, :meth:`Logger.warning`,
  :meth:`Logger.error`, :meth:`Logger.critical` は全て、
  メッセージとメソッド名に対応したレベルでログ記録を作り出します。
  メッセージは実際にはフォーマット文字列であり、通常の文字列代入に使う
  :const:`%s`, :const:`%d`, :const:`%f` などを含み得ます。
  残りの引数はメッセージの代入される位置に対応するオブジェクトのリストです。
  :const:`**kwargs` については、ログ記録メソッドが気にするキーワードは
  :const:`exc_info` だけで、例外の情報をログに記録するかを決定するのに使います。


.. * :meth:`Logger.exception` creates a log message similar to
..   :meth:`Logger.error`.  The difference is that :meth:`Logger.exception` dumps a
..   stack trace along with it.  Call this method only from an exception handler.

* :meth:`Logger.exception` は :meth:`Logger.error` と似たログメッセージを作成します。
  違いは :meth:`Logger.exception` がスタックトレースを一緒に吐き出すことです。
  例外ハンドラでだけ使うようにして下さい。


.. * :meth:`Logger.log` takes a log level as an explicit argument.  This is a
..   little more verbose for logging messages than using the log level convenience
..   methods listed above, but this is how to log at custom log levels.

* :meth:`Logger.log` はログレベルを陽に引き渡される引数として取ります。
  これは上に挙げた便宜的なログレベルごとのメソッドを使うより少しコード量が多くなりますが、
  独自のログレベルを使うにはこのようにするものなのです。


.. :func:`getLogger` returns a reference to a logger instance with the specified
.. if it it is provided, or ``root`` if not.  The names are period-separated
.. hierarchical structures.  Multiple calls to :func:`getLogger` with the same name
.. will return a reference to the same logger object.  Loggers that are further
.. down in the hierarchical list are children of loggers higher up in the list.
.. For example, given a logger with a name of ``foo``, loggers with names of
.. ``foo.bar``, ``foo.bar.baz``, and ``foo.bam`` are all children of ``foo``.
.. Child loggers propagate messages up to their parent loggers.  Because of this,
.. it is unnecessary to define and configure all the loggers an application uses.
.. It is sufficient to configure a top-level logger and create child loggers as
.. needed.

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

.. :class:`Handler` objects are responsible for dispatching the appropriate log
.. messages (based on the log messages' severity) to the handler's specified
.. destination.  Logger objects can add zero or more handler objects to themselves
.. with an :func:`addHandler` method.  As an example scenario, an application may
.. want to send all log messages to a log file, all log messages of error or higher
.. to stdout, and all messages of critical to an email address.  This scenario
.. requires three individual handlers where each handler is responsible for sending
.. messages of a specific severity to a specific location.

:class:`Handler` オブジェクトは適切なログメッセージを(ログメッセージの深刻さに基づいて)
ハンドラの指定された宛先に振り分けることに責任を持ちます。
ロガーオブジェクトには :func:`addHandler` メソッドで0個以上のハンドラを追加することができます。
有り得るシナリオとして、あるアプリケーションが全てのログメッセージをログファイルに、
error 以上の全てのログメッセージを標準出力に、
critical のメッセージは全てメールアドレスに、
送りたいとします。
この場合、三つの個別のハンドラがそれぞれの深刻さと宛先に応じて必要になります。


.. The standard library includes quite a few handler types; this tutorial uses only
.. :class:`StreamHandler` and :class:`FileHandler` in its examples.

このライブラリには多数のハンドラを用意してありますが、
このチュートリアルでは
:class:`StreamHandler` と :class:`FileHandler` だけを例に取り上げます。


.. There are very few methods in a handler for application developers to concern
.. themselves with.  The only handler methods that seem relevant for application
.. developers who are using the built-in handler objects (that is, not creating
.. custom handlers) are the following configuration methods:

アプリケーション開発者にとってハンドラを扱う上で気にするべきメソッドは極々限られています。
備え付けのハンドラオブジェクトを使う (つまり自作ハンドラを作らない)
開発者に関係あるハンドラのメソッドは次の設定用のメソッドだけでしょう:


.. * The :meth:`Handler.setLevel` method, just as in logger objects, specifies the
..   lowest severity that will be dispatched to the appropriate destination.  Why
..   are there two :func:`setLevel` methods?  The level set in the logger
..   determines which severity of messages it will pass to its handlers.  The level
..   set in each handler determines which messages that handler will send on.
..   :func:`setFormatter` selects a Formatter object for this handler to use.

* :meth:`Handler.setLevel` メソッドは、ロガーオブジェクトの場合と同様に、
  適切な宛先に振り分けられるべき最も低い深刻さを指定します。
  なぜ二つも :func:`setLevel` メソッドがあるのでしょう?
  ロガーでセットされるレベルはメッセージのどの深刻さを付随するハンドラに渡すか決めます。
  ハンドラでセットされるレベルはハンドラがどのメッセージを送るべきか決めます。
  :func:`setFormatter` でこのハンドラが使用する Formatter オブジェクトを選択します。


.. * :func:`addFilter` and :func:`removeFilter` respectively configure and
..   deconfigure filter objects on handlers.

* :func:`addFilter` および :func:`removeFilter` はそれぞれハンドラへのフィルタオブジェクトの設定、設定解除を行います。


.. Application code should not directly instantiate and use handlers.  Instead, the
.. :class:`Handler` class is a base class that defines the interface that all
.. Handlers should have and establishes some default behavior that child classes
.. can use (or override).

アプリケーションのコード中ではハンドラを直接インスタンス化して使ってはなりません。
そうではなく、 :class:`Handler` クラスは全てのハンドラが持つべきインターフェイスを定義し、
子クラスが使える (もしくはオーバライドできる) いくつかのデフォルトの振る舞いを確立します。


フォーマッタ
^^^^^^^^^^^^

.. Formatter objects configure the final order, structure, and contents of the log
.. message.  Unlike the base :class:`logging.Handler` class, application code may
.. instantiate formatter classes, although you could likely subclass the formatter
.. if your application needs special behavior.  The constructor takes two optional
.. arguments: a message format string and a date format string.  If there is no
.. message format string, the default is to use the raw message.  If there is no
.. date format string, the default date format is:

フォーマッタオブジェクトは最終的なログメッセージの順序、構造および内容を設定します。
基底クラスの :class:`logging.Handler` とは違って、
アプリケーションのコードはフォーマッタクラスをインスタンス化して構いませんが、
特別な振る舞いをさせたいアプリケーションではフォーマッタのサブクラスを使う可能性もあります。
コンストラクタは二つのオプション引数を取ります: メッセージのフォーマット文字列と日付のフォーマット文字列です。
メッセージのフォーマット文字列がなければ、デフォルトではメッセージをそのまま使います。
日付のフォーマット文字列がなければデフォルトは


::

    %Y-%m-%d %H:%M:%S


.. with the milliseconds tacked on at the end.

で、最後にミリ秒が付きます。


.. The message format string uses ``%(<dictionary key>)s`` styled string
.. substitution; the possible keys are documented in :ref:`formatter-objects`.

メッセージのフォーマット文字列は ``%(<dictionary key>)s`` 形式の文字列代入を用います。
使えるキーについては :ref:`formatter-objects` に書いてあります。


.. The following message format string will log the time in a human-readable
.. format, the severity of the message, and the contents of the message, in that
.. order:

下のメッセージのフォーマット文字列は、人が読みやすい形式の時刻、メッセージの深刻さ、
メッセージの内容をその順番に出力します。


::

    "%(asctime)s - %(levelname)s - %(message)s"


ログ記録方法の設定
^^^^^^^^^^^^^^^^^^

.. Programmers can configure logging either by creating loggers, handlers, and
.. formatters explicitly in a main module with the configuration methods listed
.. above (using Python code), or by creating a logging config file.  The following
.. code is an example of configuring a very simple logger, a console handler, and a
.. simple formatter in a Python module:

プログラマはログ記録方法を設定できます。
一つの方法は中心となるモジュールで上で述べたような設定メソッドで
(Python コードを使って) ロガー、ハンドラ、フォーマッタを自ら手を下して作成することです。
もう一つの方法は、ログ記録設定ファイルを作ることです。
以下のコードは、例としてごく単純なロガー、コンソールハンドラ、そして単純なフォーマッタを
Python モジュールの中で設定しています。


::

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


.. Running this module from the command line produces the following output:

このモジュールをコマンドラインから実行すると、以下の出力が得られます。


::

    $ python simple_logging_module.py
    2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
    2005-03-19 15:10:26,620 - simple_example - INFO - info message
    2005-03-19 15:10:26,695 - simple_example - WARNING - warn message
    2005-03-19 15:10:26,697 - simple_example - ERROR - error message
    2005-03-19 15:10:26,773 - simple_example - CRITICAL - critical message


.. The following Python module creates a logger, handler, and formatter nearly
.. identical to those in the example listed above, with the only difference being
.. the names of the objects:

次の Python モジュールもロガー、ハンドラ、フォーマッタを上の例とほぼ同じ形で生成しますが、
オブジェクトの名前だけが異なります。


::

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


.. Here is the logging.conf file:

そしてこれが logging.conf ファイルです:


::

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


.. The output is nearly identical to that of the non-config-file-based example:

出力は設定ファイルを使わないバージョンとほぼ同じです。


::

    $ python simple_logging_config.py
    2005-03-19 15:38:55,977 - simpleExample - DEBUG - debug message
    2005-03-19 15:38:55,979 - simpleExample - INFO - info message
    2005-03-19 15:38:56,054 - simpleExample - WARNING - warn message
    2005-03-19 15:38:56,055 - simpleExample - ERROR - error message
    2005-03-19 15:38:56,130 - simpleExample - CRITICAL - critical message


.. You can see that the config file approach has a few advantages over the Python
.. code approach, mainly separation of configuration and code and the ability of
.. noncoders to easily modify the logging properties.

設定ファイル経由の方が Python コード経由に比べていくつかの利点を有していることが見て取れると思います。
設定とコードの分離が最大の違いで、プログラマ以外にも容易にログ出力の表現を変更できます。


.. _library-config:

ライブラリのためのログ記録方法の設定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. When developing a library which uses logging, some consideration needs to be
.. given to its configuration. If the using application does not use logging, and
.. library code makes logging calls, then a one-off message "No handlers could be
.. found for logger X.Y.Z" is printed to the console. This message is intended
.. to catch mistakes in logging configuration, but will confuse an application
.. developer who is not aware of logging by the library.

ログ記録を行うライブラリを開発するときには、いくつかその設定について考えておくべきことがあります。
ライブラリを使うアプリケーションが logging を使っていないときに、
ライブラリが logging を呼び出すと "No handlers could be found for logger X.Y.Z"
(「ロガー X.Y.Z に対するハンドラが見つかりません」)
というメッセージがコンソールに一度だけ流れます。
このメッセージは logging の設定ミスを捕らえるためのものですが、
ライブラリが logging を使っているとアプリケーション開発者が知らない場合混乱につながりかねません。


.. In addition to documenting how a library uses logging, a good way to configure
.. library logging so that it does not cause a spurious message is to add a
.. handler which does nothing. This avoids the message being printed, since a
.. handler will be found: it just doesn't produce any output. If the library user
.. configures logging for application use, presumably that configuration will add
.. some handlers, and if levels are suitably configured then logging calls made
.. in library code will send output to those handlers, as normal.

ライブラリが logging をどのように使っているかを文書に書くだけでなく、
意図しないメッセージを出さないために何もしないハンドラを加えるように設定しておくのが良い方法です。
こうすればメッセージが出力されるのを(ハンドラが見つかるので)防げるので、何も出力しないようになります。
ライブラリを使ってアプリケーションを書くユーザーが logging の設定をするならば、
おそらくその設定で何かハンドラを追加することでしょう。
その中でレベルが適切に設定されていればライブラリコード中の logging 呼び出しはそのハンドラに(普段通りに)出力を送ります。


.. A do-nothing handler can be simply defined as follows:

何もしないハンドラは以下のよう簡単に定義できます。


::

    import logging

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


.. An instance of this handler should be added to the top-level logger of the
.. logging namespace used by the library. If all logging by a library *foo* is
.. done using loggers with names matching "foo.x.y", then the code:

このハンドラのインスタンスがライブラリで使われるログ記録の名前空間の最上位ロガーに追加されなければなりません。
ライブラリ *foo* のログ記録が全て "foo.x.y" にマッチする名前のロガーで行われるならば、
次のコードで望むような効果を得られます。


::

    import logging

    h = NullHandler()
    logging.getLogger("foo").addHandler(h)


.. should have the desired effect. If an organisation produces a number of
.. libraries, then the logger name specified can be "orgname.foo" rather than
.. just "foo".

組織がいくつものライブラリを世に出しているならば、指定されるロガーの名前は単なる "foo"
ではなく "orgname.foo" かもしれませんね。


ログレベル
----------

.. The numeric values of logging levels are given in the following table. These are
.. primarily of interest if you want to define your own levels, and need them to
.. have specific values relative to the predefined levels. If you define a level
.. with the same numeric value, it overwrites the predefined value; the predefined
.. name is lost.

ログレベルの数値は以下の表のように与えられています。これらは基本的に自分でレベルを定義したい人のためのもので、
定義するレベルを既存のレベルの間に位置づけるために具体的な値が必要になります。もし数値が他のレベルと同じだったら、既存の値は上書きされその名前は失われます。


.. +--------------+---------------+
.. | Level        | Numeric value |
.. +==============+===============+
.. | ``CRITICAL`` | 50            |
.. +--------------+---------------+
.. | ``ERROR``    | 40            |
.. +--------------+---------------+
.. | ``WARNING``  | 30            |
.. +--------------+---------------+
.. | ``INFO``     | 20            |
.. +--------------+---------------+
.. | ``DEBUG``    | 10            |
.. +--------------+---------------+
.. | ``NOTSET``   | 0             |
.. +--------------+---------------+

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


.. Levels can also be associated with loggers, being set either by the developer or
.. through loading a saved logging configuration. When a logging method is called
.. on a logger, the logger compares its own level with the level associated with
.. the method call. If the logger's level is higher than the method call's, no
.. logging message is actually generated. This is the basic mechanism controlling
.. the verbosity of logging output.

レベルもロガーに関連付けることができ、デベロッパが設定することも、保存されたログ記録設定を読み込む際に設定することもできます。
ロガーに対してログ記録メソッドが呼び出されると、ロガーは自らのレベルとメソッド呼び出しに関連付けられたレベルを比較します。
ロガーのレベルがメソッド呼び出しのレベルよりも高い場合、実際のログメッセージは生成されません。これはログ出力の冗長性を制御するための基本的なメカニズムです。


.. Logging messages are encoded as instances of the :class:`LogRecord` class. When
.. a logger decides to actually log an event, a :class:`LogRecord` instance is
.. created from the logging message.

ログ記録されるメッセージは :class:`LogRecord` クラスのインスタンスとして
コード化されます。ロガーがあるイベントを実際にログ出力すると決定した場合、ログメッセージから :class:`LogRecord`
インスタンスが生成されます。


.. Logging messages are subjected to a dispatch mechanism through the use of
.. :dfn:`handlers`, which are instances of subclasses of the :class:`Handler`
.. class. Handlers are responsible for ensuring that a logged message (in the form
.. of a :class:`LogRecord`) ends up in a particular location (or set of locations)
.. which is useful for the target audience for that message (such as end users,
.. support desk staff, system administrators, developers). Handlers are passed
.. :class:`LogRecord` instances intended for particular destinations. Each logger
.. can have zero, one or more handlers associated with it (via the
.. :meth:`addHandler` method of :class:`Logger`). In addition to any handlers
.. directly associated with a logger, *all handlers associated with all ancestors
.. of the logger* are called to dispatch the message.

ログ記録されるメッセージは、ハンドラ (:dfn:`handlers`) を通して、処理機構 (dispatch mechanism)
にかけられます。ハンドラは :class:`Handler` クラスのサブクラスのインスタンスで、ログ記録された (:class:`LogRecord`
形式の) メッセージが、そのメッセージの伝達対象となる相手  (エンドユーザ、サポートデスクのスタッフ、システム管理者、開発者)
に行き着くようにする役割を持ちます。ハンドラには特定の行き先に方向付けられた :class:`LogRecord` インスタンスが渡されます。各ロガーは
ゼロ個、単一またはそれ以上のハンドラを (:class:`Logger` の :meth:`addHandler` メソッド) で関連付けることができます。
ロガーに直接関連付けられたハンドラに加えて、 *ロガーの上位にあるロガー全てに関連付けられたハンドラ* がメッセージを処理する際に呼び出されます。


.. Just as for loggers, handlers can have levels associated with them. A handler's
.. level acts as a filter in the same way as a logger's level does. If a handler
.. decides to actually dispatch an event, the :meth:`emit` method is used to send
.. the message to its destination. Most user-defined subclasses of :class:`Handler`
.. will need to override this :meth:`emit`.

ロガーと同様に、ハンドラは関連付けられたレベルを持つことができます。ハンドラのレベルはロガーのレベルと同じ方法で、フィルタとして働きます。
ハンドラがあるイベントを実際に処理すると決定した場合、 :meth:`emit` メソッドが使われ、メッセージを発送先に送信します。ほとんどのユーザ定義の
:class:`Handler` のサブクラスで、この :meth:`emit` をオーバライドする必要があるでしょう。


.. In addition to the base :class:`Handler` class, many useful subclasses are
.. provided:

基底クラスとなる :class:`Handler` クラスに加えて、多くの有用なサブクラスが提供されています:


.. #. :class:`StreamHandler` instances send error messages to streams (file-like
..    objects).

1. :class:`StreamHandler` のインスタンスはストリーム (ファイル様オブジェクト) にエラーメッセージを送信します。


.. #. :class:`FileHandler` instances send error messages to disk files.

2. :class:`FileHandler` のインスタンスはディスク上のファイルにエラーメッセージを送信します。


.. #. :class:`handlers.BaseRotatingHandler` is the base class for handlers that
..    rotate log files at a certain point. It is not meant to be  instantiated
..    directly. Instead, use :class:`RotatingFileHandler` or
..    :class:`TimedRotatingFileHandler`.

3. :class:`handlers.BaseRotatingHandler` はログファイルをある時点で交替させる\
   ハンドラの基底クラスです。直接インスタンス化するためのクラスではありません。
   :class:`RotatingFileHandler`
   や :class:`TimedRotatingFileHandler` を使うようにしてください。


.. #. :class:`handlers.RotatingFileHandler` instances send error messages to disk files,
..    with support for maximum log file sizes and log file rotation.

4. :class:`handlers.RotatingFileHandler` のインスタンスは最大ログファイルの\
   サイズ指定とログファイルの交替機能をサポートしながら、ディスク上のファイルにエラーメッセージを送信します。


.. #. :class:`handlers.TimedRotatingFileHandler` instances send error messages to disk files
..    rotating the log file at certain timed intervals.

5. :class:`handlers.TimedRotatingFileHandler` のインスタンスは、ログファイルを\
   一定時間間隔ごとに交替しながら、ディスク上のファイルにエラーメッセージを送信します。


.. #. :class:`handlers.SocketHandler` instances send error messages to TCP/IP sockets.

6. :class:`handlers.SocketHandler` のインスタンスは TCP/IP ソケットにエラーメッセージを送信します。


.. #. :class:`handlers.DatagramHandler` instances send error messages to UDP sockets.

7. :class:`handlers.DatagramHandler` のインスタンスは UDP ソケットにエラーメッセージを送信します。


.. #. :class:`handlers.SMTPHandler` instances send error messages to a designated email
..    address.

8. :class:`handlers.SMTPHandler` のインスタンスは指定された電子メールアドレスにエラーメッセージを送信します。


.. #. :class:`handlers.SysLogHandler` instances send error messages to a Unix syslog daemon,
..    possibly on a remote machine.

9. :class:`handlers.SysLogHandler` のインスタンスは遠隔を含むマシン上の syslog デーモンにエラーメッセージを送信します。


.. #. :class:`handlers.NTEventLogHandler` instances send error messages to a Windows
..    NT/2000/XP event log.

10. :class:`handlers.NTEventLogHandler` のインスタンスは Windows NT/2000/XP イベントログにエラーメッセージを送信します。


.. #. :class:`handlers.MemoryHandler` instances send error messages to a buffer in memory,
..    which is flushed whenever specific criteria are met.

11. :class:`handlers.MemoryHandler` のインスタンスはメモリ上のバッファにエラーメッセージを送信し、指定された条件でフラッシュされるようにします。


.. #. :class:`handlers.HTTPHandler` instances send error messages to an HTTP server using
..    either ``GET`` or ``POST`` semantics.

12. :class:`handlers.HTTPHandler` のインスタンスは ``GET`` か ``POST`` セマンティクスを使って HTTP
    サーバにエラーメッセージを送信します。

.. #. :class:`handlers.WatchedFileHandler` instances watch the file they are logging to. If
.. the file changes, it is closed and reopened using the file name. This handler
.. is only useful on Unix-like systems; Windows does not support the underlying
.. mechanism used.

13. :class:`handlers.WatchedFileHandler` のインスタンスはログ記録を行うファイルを監視します。
    もしファイルが変われば、一旦ファイルを閉じた後ファイル名を使って再度開きます。
    このハンドラは Unix ライクなシステムでだけ有用です。
    Windows では元にしている機構がサポートされていません。


.. The :class:`StreamHandler` and :class:`FileHandler`
.. classes are defined in the core logging package. The other handlers are
.. defined in a sub- module, :mod:`logging.handlers`. (There is also another
.. sub-module, :mod:`logging.config`, for configuration functionality.)

:class:`StreamHandler` および :class:`FileHandler` クラスは、中核となる\
ログ化機構パッケージ内で定義されています。他のハンドラはサブモジュール、
:mod:`logging.handlers` で定義されています。
(サブモジュールにはもうひとつ :mod:`logging.config` があり、
これは環境設定機能のためのものです。)


.. Logged messages are formatted for presentation through instances of the
.. :class:`Formatter` class. They are initialized with a format string suitable for
.. use with the % operator and a dictionary.

ログ記録されたメッセージは :class:`Formatter` クラスのインスタンスを介し、表示用に書式化されます。これらのインスタンスは %
演算子と辞書を使うのに適した書式化文字列で初期化されます。


.. For formatting multiple messages in a batch, instances of
.. :class:`BufferingFormatter` can be used. In addition to the format string (which
.. is applied to each message in the batch), there is provision for header and
.. trailer format strings.

複数のメッセージの初期化をバッチ処理するために、 :class:`BufferingFormatter` のインスタンスを使うことができます。書式化文字列
(バッチ処理で各メッセージに適用されます) に加えて、ヘッダ (header) およびトレイラ (trailer) 書式化文字列が用意されています。


.. When filtering based on logger level and/or handler level is not enough,
.. instances of :class:`Filter` can be added to both :class:`Logger` and
.. :class:`Handler` instances (through their :meth:`addFilter` method). Before
.. deciding to process a message further, both loggers and handlers consult all
.. their filters for permission. If any filter returns a false value, the message
.. is not processed further.

ロガーレベル、ハンドラレベルの両方または片方に基づいたフィルタリングが十分でない場合、 :class:`Logger` および :class:`Handler`
インスタンスに :class:`Filter` のインスタンスを (:meth:`addFilter` メソッドを介して)
追加することができます。メッセージの処理を進める前に、ロガーとハンドラはともに、全てのフィルタでメッセージの処理が許可されているか調べます。
いずれかのフィルタが偽となる値を返した場合、メッセージの処理は行われません。


.. The basic :class:`Filter` functionality allows filtering by specific logger
.. name. If this feature is used, messages sent to the named logger and its
.. children are allowed through the filter, and all others dropped.

基本的な :class:`Filter` 機能では、指定されたロガー名でフィルタを行えるようになっています。この機能が利用された場合、名前付けされた
ロガーとその下位にあるロガーに送られたメッセージがフィルタを通過できるようになり、その他のメッセージは捨てられます。


.. In addition to the classes described above, there are a number of module- level
.. functions.

上で述べたクラスに加えて、いくつかのモジュールレベルの関数が存在します。


.. function:: getLogger([name])

   .. Return a logger with the specified name or, if no name is specified, return a
   .. logger which is the root logger of the hierarchy. If specified, the name is
   .. typically a dot-separated hierarchical name like *"a"*, *"a.b"* or *"a.b.c.d"*.
   .. Choice of these names is entirely up to the developer who is using logging.

   指定された名前のロガーを返します。名前が指定されていない場合、ロガー階層のルート (root) にあるロガーを返します。 *name*
   を指定する場合には、通常は *"a"*, *"a.b"*,  あるいは *"a.b.c.d"* といったようなドット区切りの階層的な
   名前にします。名前の付け方はログ機能を使う開発者次第です。


   .. All calls to this function with a given name return the same logger instance.
   .. This means that logger instances never need to be passed between different parts
   .. of an application.

   与えられた名前に対して、この関数はどの呼び出しでも同じロガーインスタンスを返します。従って、ロガーインスタンスをアプリケーションの各部
   でやりとりする必要はなくなります。


.. function:: getLoggerClass()

   .. Return either the standard :class:`Logger` class, or the last class passed to
   .. :func:`setLoggerClass`. This function may be called from within a new class
   .. definition, to ensure that installing a customised :class:`Logger` class will
   .. not undo customisations already applied by other code. For example:

   標準の :class:`Logger` クラスか、最後に :func:`setLoggerClass` に渡した
   クラスを返します。この関数は、新たに定義するクラス内で呼び出し、カスタマイズした :class:`Logger` クラスのインストールを行うときに
   既に他のコードで適用したカスタマイズを取り消そうとしていないか確かめるのに使います。例えば以下のようにします:


   ::

      class MyLogger(logging.getLoggerClass()):
          # ... override behaviour here


.. function:: debug(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`DEBUG` on the root logger. The *msg* is the
   .. message format string, and the *args* are the arguments which are merged into
   .. *msg* using the string formatting operator. (Note that this means that you can
   .. use keywords in the format string, together with a single dictionary argument.)

   レベル :const:`DEBUG` のメッセージをルートロガーで記録します。 *msg* はメッセージの書式化文字列で、 *args* は *msg* に
   文字列書式化演算子を使って取り込むための引数です。(これは、書式化文字列でキーワードを使い引数に辞書を渡すことができる、ということを意味します。)


   .. There are two keyword arguments in *kwargs* which are inspected: *exc_info*
   .. which, if it does not evaluate as false, causes exception information to be
   .. added to the logging message. If an exception tuple (in the format returned by
   .. :func:`sys.exc_info`) is provided, it is used; otherwise, :func:`sys.exc_info`
   .. is called to get the exception information.

   キーワード引数 *kwargs* からは二つのキーワードが調べられます。一つめは *exc_info* で、この値の評価値が偽でない場合、
   例外情報をログメッセージに追加します。(:func:`sys.exc_info`  の返す形式の) 例外情報を表すタプルが与えられていれば、それを
   メッセージに使います。それ以外の場合には、 :func:`sys.exc_info`  を呼び出して例外情報を取得します。


   .. The other optional keyword argument is *extra* which can be used to pass a
   .. dictionary which is used to populate the __dict__ of the LogRecord created for
   .. the logging event with user-defined attributes. These custom attributes can then
   .. be used as you like. For example, they could be incorporated into logged
   .. messages. For example:

   もう一つのキーワード引数は *extra* で、当該ログイベント用に作られた LogRecoed の __dict__
   にユーザー定義属性を増やすのに使われる辞書を渡すのに用いられます。これらの属性は好きなように使えます。たとえば、ログメッセージの一部に
   することもできます。以下の例を見てください。


   ::

      FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
      logging.basicConfig(format=FORMAT)
      d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
      logging.warning("Protocol problem: %s", "connection reset", extra=d)


   .. would print something like

   出力はこのようになります:


   ::

      2006-02-08 22:20:02,165 192.168.0.1 fbloggs  Protocol problem: connection reset


   .. The keys in the dictionary passed in *extra* should not clash with the keys used
   .. by the logging system. (See the :class:`Formatter` documentation for more
   .. information on which keys are used by the logging system.)

   *extra* で渡される辞書のキーはロギングシステムで使われているものとぶつからない
   ようにしなければなりません。(どのキーがロギングシステムで使われているかについての詳細は :class:`Formatter`
   のドキュメントを参照してください。)


   .. If you choose to use these attributes in logged messages, you need to exercise
   .. some care. In the above example, for instance, the :class:`Formatter` has been
   .. set up with a format string which expects 'clientip' and 'user' in the attribute
   .. dictionary of the LogRecord. If these are missing, the message will not be
   .. logged because a string formatting exception will occur. So in this case, you
   .. always need to pass the *extra* dictionary with these keys.

   これらの属性をログメッセージに使うことにしたなら、少し注意が必要です。上の例では、'clientip' と 'user' が LogRecord
   の属性辞書に含まれていることを期待した書式化文字列で :class:`Formatter` はセットアップされてい
   ます。これらの属性が欠けていると、書式化例外が発生してしまうためメッセージはログに残りません。したがってこの場合、常にこれらのキーがある *extra*
   辞書を渡す必要があります。


   .. While this might be annoying, this feature is intended for use in specialized
   .. circumstances, such as multi-threaded servers where the same code executes in
   .. many contexts, and interesting conditions which arise are dependent on this
   .. context (such as remote client IP address and authenticated user name, in the
   .. above example). In such circumstances, it is likely that specialized
   .. :class:`Formatter`\ s would be used with particular :class:`Handler`\ s.

   このようなことは煩わしいかもしれませんが、この機能は限定された場面で使われるように意図しているものなのです。たとえば同じコードがいくつものコ
   ンテキストで実行されるマルチスレッドのサーバで、興味のある条件が現れるのがそのコンテキストに依存している(上の例で言えば、リモートのクライアント IP
   アドレスや認証されたユーザ名など)、というような場合です。そういった場面では、それ用の :class:`Formatter` が特定の
   :class:`Handler` と共に使われるというのはよくあることです。


   .. .. versionchanged:: 2.5
   ..    *extra* was added.

   .. versionchanged:: 2.5
      *extra* が追加されました.


.. function:: info(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`INFO` on the root logger. The arguments are
   .. interpreted as for :func:`debug`.

   レベル :const:`INFO` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。


.. function:: warning(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`WARNING` on the root logger. The arguments are
   .. interpreted as for :func:`debug`.

   レベル :const:`WARNING` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。


.. function:: error(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`ERROR` on the root logger. The arguments are
   .. interpreted as for :func:`debug`.

   レベル :const:`ERROR` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。


.. function:: critical(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`CRITICAL` on the root logger. The arguments
   .. are interpreted as for :func:`debug`.

   レベル :const:`CRITICAL` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。


.. function:: exception(msg[, *args])

   .. Logs a message with level :const:`ERROR` on the root logger. The arguments are
   .. interpreted as for :func:`debug`. Exception info is added to the logging
   .. message. This function should only be called from an exception handler.

   レベル :const:`ERROR` のメッセージをルートロガーで記録します。引数は :func:`debug` と同じように解釈されます。
   例外情報はログメッセージに追加されます。このメソッドは例外ハンドラからのみ呼び出されます。


.. function:: log(level, msg[, *args[, **kwargs]])

   .. Logs a message with level *level* on the root logger. The other arguments are
   .. interpreted as for :func:`debug`.

   レベル :const:`level` のメッセージをルートロガーで記録します。その他の引数は :func:`debug` と同じように解釈されます。


.. function:: disable(lvl)

   .. Provides an overriding level *lvl* for all loggers which takes precedence over
   .. the logger's own level. When the need arises to temporarily throttle logging
   .. output down across the whole application, this function can be useful.

   全てのロガーに対して、ロガー自体のレベルに優先するような上書きレベル *lvl* を与えます。アプリケーション全体にわたって一時的にログ出力の
   頻度を押し下げる必要が生じた場合にはこの関数が有効です。


.. function:: addLevelName(lvl, levelName)

   .. Associates level *lvl* with text *levelName* in an internal dictionary, which is
   .. used to map numeric levels to a textual representation, for example when a
   .. :class:`Formatter` formats a message. This function can also be used to define
   .. your own levels. The only constraints are that all levels used must be
   .. registered using this function, levels should be positive integers and they
   .. should increase in increasing order of severity.

   内部辞書内でレベル *lvl* をテキスト *levelName* に関連付けます。これは例えば :class:`Formatter`
   でメッセージを書式化する際のように、数字のレベルをテキスト表現に対応付ける際に用いられます。この関数は自作のレベルを定義するために使うこともできます。
   使われるレベル対する唯一の制限は、レベルは正の整数でなくてはならず、メッセージの深刻さが上がるに従ってレベルの数も上がらなくてはならないということです。


.. function:: getLevelName(lvl)

   .. Returns the textual representation of logging level *lvl*. If the level is one
   .. of the predefined levels :const:`CRITICAL`, :const:`ERROR`, :const:`WARNING`,
   .. :const:`INFO` or :const:`DEBUG` then you get the corresponding string. If you
   .. have associated levels with names using :func:`addLevelName` then the name you
   .. have associated with *lvl* is returned. If a numeric value corresponding to one
   .. of the defined levels is passed in, the corresponding string representation is
   .. returned. Otherwise, the string "Level %s" % lvl is returned.

   ログ記録レベル *lvl* のテキスト表現を返します。レベルが定義済みのレベル :const:`CRITICAL` 、 :const:`ERROR` 、
   :const:`WARNING` 、 :const:`INFO` 、あるいは :const:`DEBUG` のいずれかである場合、対応する文字列が返されます。
   :func:`addLevelName` を使ってレベルに名前を関連づけていた場合、 *lvl* に関連付けられていた名前が返されます。
   定義済みのレベルに対応する数値を指定した場合、レベルに対応した文字列表現を返します。そうでない場合、文字列 "Level %s" % lvl を返します。


.. function:: makeLogRecord(attrdict)

   .. Creates and returns a new :class:`LogRecord` instance whose attributes are
   .. defined by *attrdict*. This function is useful for taking a pickled
   .. :class:`LogRecord` attribute dictionary, sent over a socket, and reconstituting
   .. it as a :class:`LogRecord` instance at the receiving end.

   属性が *attrdict* で定義された、新たな :class:`LogRecord`  インスタンスを生成して返します。この関数は pickle 化された
   :class:`LogRecord` 属性の辞書を作成し、ソケットを介して送信し、受信端で :class:`LogRecord`
   インスタンスとして再構成する際に便利です。

   *attrdict* で属性を定義した、新しい :class:`LogRecord` インスタンスを返します。この関数は、逆 pickle 化された
   :class:`LogRecord` 属性辞書を  socket 越しに受け取り、受信端で :class:`LogRecord` インスタンスに再構築す
   る場合に有用です。


.. function:: basicConfig([**kwargs])

   .. Does basic configuration for the logging system by creating a
   .. :class:`StreamHandler` with a default :class:`Formatter` and adding it to the
   .. root logger. The function does nothing if any handlers have been defined for
   .. the root logger. The functions :func:`debug`, :func:`info`, :func:`warning`,
   .. :func:`error` and :func:`critical` will call :func:`basicConfig` automatically
   .. if no handlers are defined for the root logger.

   デフォルトの :class:`Formatter` を持つ :class:`StreamHandler`
   を生成してルートロガーに追加し、ログ記録システムの基本的な環境設定を行います。
   この関数はルートロガーに対しハンドラが一つも定義されていなければ何もしません。
   関数 :func:`debug`, :func:`info`, :func:`warning`, :func:`error`, および :func:`critical`
   は、ルートロガーにハンドラが定義されていない場合に自動的に :func:`basicConfig`
   を呼び出します。


   .. This function does nothing if the root logger already has handlers configured.

   この関数はルートロガーに設定されたハンドラがあれば何もしません。


   .. .. versionchanged:: 2.4
   ..    Formerly, :func:`basicConfig` did not take any keyword arguments.

   .. versionchanged:: 2.4
      以前は :func:`basicConfig` はキーワード引数をとりませんでした.


   .. The following keyword arguments are supported.

   以下のキーワード引数がサポートされます。


   .. +--------------+---------------------------------------------+
   .. | Format       | Description                                 |
   .. +==============+=============================================+
   .. | ``filename`` | Specifies that a FileHandler be created,    |
   .. |              | using the specified filename, rather than a |
   .. |              | StreamHandler.                              |
   .. +--------------+---------------------------------------------+
   .. | ``filemode`` | Specifies the mode to open the file, if     |
   .. |              | filename is specified (if filemode is       |
   .. |              | unspecified, it defaults to 'a').           |
   .. +--------------+---------------------------------------------+
   .. | ``format``   | Use the specified format string for the     |
   .. |              | handler.                                    |
   .. +--------------+---------------------------------------------+
   .. | ``datefmt``  | Use the specified date/time format.         |
   .. +--------------+---------------------------------------------+
   .. | ``level``    | Set the root logger level to the specified  |
   .. |              | level.                                      |
   .. +--------------+---------------------------------------------+
   .. | ``stream``   | Use the specified stream to initialize the  |
   .. |              | StreamHandler. Note that this argument is   |
   .. |              | incompatible with 'filename' - if both are  |
   .. |              | present, 'stream' is ignored.               |
   .. +--------------+---------------------------------------------+

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

   .. Informs the logging system to perform an orderly shutdown by flushing and
   .. closing all handlers. This should be called at application exit and no
   .. further use of the logging system should be made after this call.

   ログ記録システムに対して、バッファのフラッシュを行い、全てのハンドラを閉じることで順次シャットダウンを行うように告知します。
   この関数はアプリケーションの exit 時に呼ばれるべきであり、
   また呼びだし以降はそれ以上ログ記録システムを使ってはなりません。


.. function:: setLoggerClass(klass)

   .. Tells the logging system to use the class *klass* when instantiating a logger.
   .. The class should define :meth:`__init__` such that only a name argument is
   .. required, and the :meth:`__init__` should call :meth:`Logger.__init__`. This
   .. function is typically called before any loggers are instantiated by applications
   .. which need to use custom logger behavior.

   ログ記録システムに対して、ロガーをインスタンス化する際にクラス *klass* を使うように指示します。指定するクラスは引数として名前だけをとるようなメソッド
   :meth:`__init__` を定義していなければならず、 :meth:`__init__` では :meth:`Logger.__init__`
   を呼び出さなければなりません。典型的な利用法として、この関数は自作のロガーを必要とするようなアプリケーションにおいて、他のロガーが
   インスタンス化される前にインスタンス化されます。


.. seealso::

   .. :pep:`282` - A Logging System
   ..    The proposal which described this feature for inclusion in the Python standard
   ..    library.

   :pep:`282` - A Logging System
      本機能を Python 標準ライブラリに含めるよう記述している提案書。


   .. `Original Python logging package <http://www.red-dove.com/python_logging.html>`_
   ..    This is the original source for the :mod:`logging` package.  The version of the
   ..    package available from this site is suitable for use with Python 1.5.2, 2.1.x
   ..    and 2.2.x, which do not include the :mod:`logging` package in the standard
   ..    library.

   `この logging パッケージのオリジナル <http://www.red-dove.com/python_logging.html>`_
      オリジナルの :mod:`logging` パッケージ。このサイトにあるバージョンのパッケージは、標準で :mod:`logging` パッケージを含まな
      いPython 1.5.2 と 2.1.x、2.2.xでも使用できます


Logger オブジェクト
-------------------

.. Loggers have the following attributes and methods. Note that Loggers are never
.. instantiated directly, but always through the module-level function
.. ``logging.getLogger(name)``.

ロガーは以下の属性とメソッドを持ちます。ロガーを直接インスタンス化することはできず、常にモジュール関数
``logging.getLogger(name)`` を介してインスタンス化するので注意してください。


.. attribute:: Logger.propagate

   .. If this evaluates to false, logging messages are not passed by this logger or by
   .. child loggers to higher level (ancestor) loggers. The constructor sets this
   .. attribute to 1.

   この値の評価結果が偽になる場合、ログ記録しようとするメッセージはこのロガーに渡されず、
   また子ロガーから上位の (親の) ロガーに渡されません。
   コンストラクタはこの属性を 1 に設定します。


.. method:: Logger.setLevel(lvl)

   .. Sets the threshold for this logger to *lvl*. Logging messages which are less
   .. severe than *lvl* will be ignored. When a logger is created, the level is set to
   .. :const:`NOTSET` (which causes all messages to be processed when the logger is
   .. the root logger, or delegation to the parent when the logger is a non-root
   .. logger). Note that the root logger is created with level :const:`WARNING`.

   このロガーの閾値を *lvl* に設定します。ログ記録しようとするメッセージで、 *lvl* よりも深刻でないものは無視されます。
   ロガーが生成された際、レベルは :const:`NOTSET` (これにより全てのメッセージについて、ロガーがルートロガーであれば処理される、
   そうでなくてロガーが非ルートロガーの場合には親ロガーに代行させる) に設定されます。ルートロガーは :const:`WARNING` レベル
   で生成されることに注意してください。


   .. The term "delegation to the parent" means that if a logger has a level of
   .. NOTSET, its chain of ancestor loggers is traversed until either an ancestor with
   .. a level other than NOTSET is found, or the root is reached.

   「親ロガーに代行させる」という用語の意味は、もしロガーのレベルが NOTEST ならば、祖先ロガーの系列の中を NOTEST 以外のレベルの祖先を見つけるかルー
   トに到達するまで辿っていく、ということです。


   .. If an ancestor is found with a level other than NOTSET, then that ancestor's
   .. level is treated as the effective level of the logger where the ancestor search
   .. began, and is used to determine how a logging event is handled.

   もし NOTEST 以外のレベルの祖先が見つかったなら、その祖先のレベルが祖先の探索を開始したロガーの実効レベルとして取り扱われ、ログイベントがどの
   ように処理されるかを決めるのに使われます。


   .. If the root is reached, and it has a level of NOTSET, then all messages will be
   .. processed. Otherwise, the root's level will be used as the effective level.

   ルートに到達した場合、ルートのレベルが NOTEST ならば全てのメッセージは処理されます。そうでなければルートのレベルが実効レベルとして使われます。


.. method:: Logger.isEnabledFor(lvl)

   .. Indicates if a message of severity *lvl* would be processed by this logger.
   .. This method checks first the module-level level set by
   .. ``logging.disable(lvl)`` and then the logger's effective level as determined
   .. by :meth:`getEffectiveLevel`.

   深刻さが *lvl* のメッセージが、このロガーで処理されることになっているかどうかを示します。このメソッドはまず、
   ``logging.disable(lvl)`` で設定されるモジュールレベルの深刻さレベルを調べ、次にロガーの実効レベルを
   :meth:`getEffectiveLevel` で調べます。


.. method:: Logger.getEffectiveLevel()

   .. Indicates the effective level for this logger. If a value other than
   .. :const:`NOTSET` has been set using :meth:`setLevel`, it is returned. Otherwise,
   .. the hierarchy is traversed towards the root until a value other than
   .. :const:`NOTSET` is found, and that value is returned.

   このロガーの実効レベルを示します。 :const:`NOTSET` 以外の値が :meth:`setLevel` で設定されていた場合、その値が返されます。
   そうでない場合、 :const:`NOTSET` 以外の値が見つかるまでロガーの階層をルートロガーの方向に追跡します。見つかった場合、その値が返されます。


.. method:: Logger.debug(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`DEBUG` on this logger. The *msg* is the
   .. message format string, and the *args* are the arguments which are merged into
   .. *msg* using the string formatting operator. (Note that this means that you can
   .. use keywords in the format string, together with a single dictionary argument.)

   レベル :const:`DEBUG` のメッセージをこのロガーで記録します。 *msg* はメッセージの書式化文字列で、 *args* は *msg* に
   文字列書式化演算子を使って取り込むための引数です。(これは、書式化文字列でキーワードを使い引数に辞書を渡すことができる、ということを意味します。)


   .. There are two keyword arguments in *kwargs* which are inspected: *exc_info*
   .. which, if it does not evaluate as false, causes exception information to be
   .. added to the logging message. If an exception tuple (in the format returned by
   .. :func:`sys.exc_info`) is provided, it is used; otherwise, :func:`sys.exc_info`
   .. is called to get the exception information.

   キーワード引数 *kwargs* からは二つのキーワードが調べられます。一つめは *exc_info* で、この値の評価値が偽でない場合、
   例外情報をログメッセージに追加します。(:func:`sys.exc_info`  の返す形式の) 例外情報を表すタプルが与えられていれば、それを
   メッセージに使います。それ以外の場合には、 :func:`sys.exc_info`  を呼び出して例外情報を取得します。


   .. The other optional keyword argument is *extra* which can be used to pass a
   .. dictionary which is used to populate the __dict__ of the LogRecord created for
   .. the logging event with user-defined attributes. These custom attributes can then
   .. be used as you like. For example, they could be incorporated into logged
   .. messages. For example:

   もう一つのキーワード引数は *extra* で、当該ログイベント用に作られた LogRecoed の __dict__
   にユーザー定義属性を増やすのに使われる辞書を渡すのに用いられます。これらの属性は好きなように使えます。たとえば、ログメッセージの一部に
   することもできます。以下の例を見てください。


   ::

      FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
      logging.basicConfig(format=FORMAT)
      d = { 'clientip' : '192.168.0.1', 'user' : 'fbloggs' }
      logger = logging.getLogger("tcpserver")
      logger.warning("Protocol problem: %s", "connection reset", extra=d)


   .. would print something like

   出力はこのようになります:


   ::

      2006-02-08 22:20:02,165 192.168.0.1 fbloggs  Protocol problem: connection reset


   .. The keys in the dictionary passed in *extra* should not clash with the keys used
   .. by the logging system. (See the :class:`Formatter` documentation for more
   .. information on which keys are used by the logging system.)

   *extra* で渡される辞書のキーはロギングシステムで使われているものとぶつからない
   ようにしなければなりません。(どのキーがロギングシステムで使われているかについての詳細は :class:`Formatter`
   のドキュメントを参照してください。)


   .. If you choose to use these attributes in logged messages, you need to exercise
   .. some care. In the above example, for instance, the :class:`Formatter` has been
   .. set up with a format string which expects 'clientip' and 'user' in the attribute
   .. dictionary of the LogRecord. If these are missing, the message will not be
   .. logged because a string formatting exception will occur. So in this case, you
   .. always need to pass the *extra* dictionary with these keys.

   これらの属性をログメッセージに使うことにしたなら、少し注意が必要です。上の例では、'clientip' と 'user' が LogRecord
   の属性辞書に含まれていることを期待した書式化文字列で :class:`Formatter` はセットアップされてい
   ます。これらの属性が欠けていると、書式化例外が発生してしまうためメッセージはログに残りません。したがってこの場合、常にこれらのキーがある *extra*
   辞書を渡す必要があります。


   .. While this might be annoying, this feature is intended for use in specialized
   .. circumstances, such as multi-threaded servers where the same code executes in
   .. many contexts, and interesting conditions which arise are dependent on this
   .. context (such as remote client IP address and authenticated user name, in the
   .. above example). In such circumstances, it is likely that specialized
   .. :class:`Formatter`\ s would be used with particular :class:`Handler`\ s.

   このようなことは煩わしいかもしれませんが、この機能は限定された場面で使われるように意図しているものなのです。たとえば同じコードがいくつものコ
   ンテキストで実行されるマルチスレッドのサーバで、興味のある条件が現れるのがそのコンテキストに依存している(上の例で言えば、リモートのクライアント IP
   アドレスや認証されたユーザ名など)、というような場合です。そういった場面では、それ用の :class:`Formatter` が特定の
   :class:`Handler` と共に使われるというのはよくあることです。


   .. .. versionchanged:: 2.5
   ..    *extra* was added.

   .. versionchanged:: 2.5
      *extra* が追加されました.


.. method:: Logger.info(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`INFO` on this logger. The arguments are
   .. interpreted as for :meth:`debug`.

   レベル :const:`INFO` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.warning(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`WARNING` on this logger. The arguments are
   .. interpreted as for :meth:`debug`.

   レベル :const:`WARNING` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.error(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`ERROR` on this logger. The arguments are
   .. interpreted as for :meth:`debug`.

   レベル :const:`ERROR` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.critical(msg[, *args[, **kwargs]])

   .. Logs a message with level :const:`CRITICAL` on this logger. The arguments are
   .. interpreted as for :meth:`debug`.

   レベル :const:`CRITICAL` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.log(lvl, msg[, *args[, **kwargs]])

   .. Logs a message with integer level *lvl* on this logger. The other arguments are
   .. interpreted as for :meth:`debug`.

   整数で表したレベル *lvl* のメッセージをこのロガーで記録します。その他の引数は :meth:`debug` と同じように解釈されます。


.. method:: Logger.exception(msg[, *args])

   .. Logs a message with level :const:`ERROR` on this logger. The arguments are
   .. interpreted as for :meth:`debug`. Exception info is added to the logging
   .. message. This method should only be called from an exception handler.

   レベル :const:`ERROR` のメッセージをこのロガーで記録します。引数は :meth:`debug` と同じように解釈されます。
   例外情報はログメッセージに追加されます。このメソッドは例外ハンドラからのみ呼び出されます。


.. method:: Logger.addFilter(filt)

   .. Adds the specified filter *filt* to this logger.

   指定されたフィルタ *filt* をこのロガーに追加します。


.. method:: Logger.removeFilter(filt)

   .. Removes the specified filter *filt* from this logger.

   指定されたフィルタ *filt* をこのロガーから除去します。


.. method:: Logger.filter(record)

   .. Applies this logger's filters to the record and returns a true value if the
   .. record is to be processed.

   このロガーのフィルタをレコード (record) に適用し、レコードがフィルタを透過して処理されることになる場合には真を返します。


.. method:: Logger.addHandler(hdlr)

   .. Adds the specified handler *hdlr* to this logger.

   指定されたハンドラ *hdlr* をこのロガーに追加します。


.. method:: Logger.removeHandler(hdlr)

   .. Removes the specified handler *hdlr* from this logger.

   指定されたハンドラ *hdlr* をこのロガーから除去します。


.. method:: Logger.findCaller()

   .. Finds the caller's source filename and line number. Returns the filename, line
   .. number and function name as a 3-element tuple.

   呼び出し元のソースファイル名と行番号を調べます。
   ファイル名と行番号と関数名を 3 要素のタプルで返します。


   .. .. versionchanged:: 2.4
   ..    The function name was added. In earlier versions, the filename and line number
   ..    were returned as a 2-element tuple..

   .. versionchanged:: 2.4
      関数名も加えられました。
      以前のバージョンではファイル名と行番号を 2 要素のタプルで返していました。


.. method:: Logger.handle(record)

   .. Handles a record by passing it to all handlers associated with this logger and
   .. its ancestors (until a false value of *propagate* is found). This method is used
   .. for unpickled records received from a socket, as well as those created locally.
   .. Logger-level filtering is applied using :meth:`filter`.

   レコードをこのロガーおよびその上位ロガーに (*propagate* の値が偽になるまで) さかのぼった関連付けられている全てのハンドラに渡して
   処理します。このメソッドはソケットから受信した逆 pickle 化されたレコードに対してもレコードがローカルで生成された場合と同様に用いられます。
   :meth:`filter` によって、ロガーレベルでのフィルタが適用されます。


.. method:: Logger.makeRecord(name, lvl, fn, lno, msg, args, exc_info [, func, extra])

   .. This is a factory method which can be overridden in subclasses to create
   .. specialized :class:`LogRecord` instances.

   このメソッドは、特殊な :class:`LogRecord` インスタンスを生成するためにサブクラスでオーバライドできるファクトリメソッドです。


   .. .. versionchanged:: 2.5
   ..    *func* and *extra* were added.

   .. versionchanged:: 2.5
      *func* と *extra* が追加されました.


.. _minimal-example:

基本的な使い方
--------------

.. .. versionchanged:: 2.4
..    formerly :func:`basicConfig` did not take any keyword arguments.

.. versionchanged:: 2.4
   以前は :func:`basicConfig` はキーワード引数をとりませんでした.


.. The :mod:`logging` package provides a lot of flexibility, and its configuration
.. can appear daunting.  This section demonstrates that simple use of the logging
.. package is possible.

:mod:`logging` パッケージには高い柔軟性があり、その設定にたじろぐこともあるでしょう。そこでこの節では、 :mod:`logging`
パッケージを簡単に使う方法もあることを示します。


.. The simplest example shows logging to the console:

以下の最も単純な例では、コンソールにログを表示します。


::

   import logging

   logging.debug('A debug message')
   logging.info('Some information')
   logging.warning('A shot across the bows')


.. If you run the above script, you'll see this:

上のスクリプトを実行すると、以下のようなメッセージを目にするでしょう:


::

   WARNING:root:A shot across the bows


.. Because no particular logger was specified, the system used the root logger. The
.. debug and info messages didn't appear because by default, the root logger is
.. configured to only handle messages with a severity of WARNING or above. The
.. message format is also a configuration default, as is the output destination of
.. the messages - ``sys.stderr``. The severity level, the message format and
.. destination can be easily changed, as shown in the example below:

ここではロガーを特定しなかったので、システムはルートロガーを使っています。デバッグメッセージや情報メッセージは表示されませんが、これはデフォルトの
ルートロガーが WARNING 以上の重要度を持つメッセージしか処理しないように設定されているからです。
メッセージの書式もデフォルトの設定に従っています。出力先は ``sys.stderr`` で、これもデフォルトの設定です。
重要度レベルやメッセージの形式、ログの出力先は、以下の例のように簡単に変更できます。


::

   import logging

   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s %(levelname)s %(message)s',
                       filename='/tmp/myapp.log',
                       filemode='w')
   logging.debug('A debug message')
   logging.info('Some information')
   logging.warning('A shot across the bows')


.. The :meth:`basicConfig` method is used to change the configuration defaults,
.. which results in output (written to ``/tmp/myapp.log``) which should look
.. something like the following:

ここでは、 :meth:`basicConfig` メソッドを使って、以下のような出力例になる (そして ``/tmp/myapp.log`` に書き込まれる)
ように、デフォルト設定を変更しています。


::

   2004-07-02 13:00:08,743 DEBUG A debug message
   2004-07-02 13:00:08,743 INFO Some information
   2004-07-02 13:00:08,743 WARNING A shot across the bows


.. This time, all messages with a severity of DEBUG or above were handled, and the
.. format of the messages was also changed, and output went to the specified file
.. rather than the console.

今度は、重要度が DEBUG か、それ以上のメッセージが処理されました。メッセージの形式も変更され、出力はコンソールではなく特定のファイル
に書き出されました。


.. Formatting uses standard Python string formatting - see section
.. :ref:`string-formatting`. The format string takes the following common
.. specifiers. For a complete list of specifiers, consult the :class:`Formatter`
.. documentation.

出力の書式化には、通常の Python 文字列に対する初期化を使います -  :ref:`string-formatting`
節を参照してください。書式化文字列は、以下の指定子 (specifier) を常にとります。指定子の完全なリストについては
:class:`Formatter` のドキュメントを参照してください。


.. +-------------------+-----------------------------------------------+
.. | Format            | Description                                   |
.. +===================+===============================================+
.. | ``%(name)s``      | Name of the logger (logging channel).         |
.. +-------------------+-----------------------------------------------+
.. | ``%(levelname)s`` | Text logging level for the message            |
.. |                   | (``'DEBUG'``, ``'INFO'``, ``'WARNING'``,      |
.. |                   | ``'ERROR'``, ``'CRITICAL'``).                 |
.. +-------------------+-----------------------------------------------+
.. | ``%(asctime)s``   | Human-readable time when the                  |
.. |                   | :class:`LogRecord` was created.  By default   |
.. |                   | this is of the form "2003-07-08 16:49:45,896" |
.. |                   | (the numbers after the comma are millisecond  |
.. |                   | portion of the time).                         |
.. +-------------------+-----------------------------------------------+
.. | ``%(message)s``   | The logged message.                           |
.. +-------------------+-----------------------------------------------+

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


.. To change the date/time format, you can pass an additional keyword parameter,
.. *datefmt*, as in the following:

以下のように、追加のキーワードパラメタ *datefmt* を渡すと日付や時刻の書式を変更できます。


::

   import logging

   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s %(levelname)-8s %(message)s',
                       datefmt='%a, %d %b %Y %H:%M:%S',
                       filename='/temp/myapp.log',
                       filemode='w')
   logging.debug('A debug message')
   logging.info('Some information')
   logging.warning('A shot across the bows')


.. which would result in output like

出力は以下のようになります


::

   Fri, 02 Jul 2004 13:06:18 DEBUG    A debug message
   Fri, 02 Jul 2004 13:06:18 INFO     Some information
   Fri, 02 Jul 2004 13:06:18 WARNING  A shot across the bows


.. The date format string follows the requirements of :func:`strftime` - see the
.. documentation for the :mod:`time` module.

日付を書式化する文字列は、 :func:`strftime` の要求に従います -  :mod:`time` モジュールを参照してください。


.. If, instead of sending logging output to the console or a file, you'd rather use
.. a file-like object which you have created separately, you can pass it to
.. :func:`basicConfig` using the *stream* keyword argument. Note that if both
.. *stream* and *filename* keyword arguments are passed, the *stream* argument is
.. ignored.

コンソールやファイルではなく、別個に作成しておいたファイル類似オブジェクトにログを出力したい場合には、 :func:`basicConfig` に
*stream* キーワード引数で渡します。 *stream* と *filename*  の両方の引数を指定した場合、 *stream*
は無視されるので注意してください。


.. Of course, you can put variable information in your output. To do this, simply
.. have the message be a format string and pass in additional arguments containing
.. the variable information, as in the following example:

状況に応じて変化する情報ももちろんログ出力できます。以下のように、単にメッセージを書式化文字列にして、その後ろに可変情報の引数を渡すだけです。


::

   import logging

   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s %(levelname)-8s %(message)s',
                       datefmt='%a, %d %b %Y %H:%M:%S',
                       filename='/temp/myapp.log',
                       filemode='w')
   logging.error('Pack my box with %d dozen %s', 5, 'liquor jugs')


.. which would result in

出力は以下のようになります。


::

   Wed, 21 Jul 2004 15:35:16 ERROR    Pack my box with 5 dozen liquor jugs


.. _multiple-destinations:

複数の出力先にログを出力する
----------------------------

.. Let's say you want to log to console and file with different message formats and
.. in differing circumstances. Say you want to log messages with levels of DEBUG
.. and higher to file, and those messages at level INFO and higher to the console.
.. Let's also assume that the file should contain timestamps, but the console
.. messages should not. Here's how you can achieve this:

コンソールとファイルに、別々のメッセージ書式で、別々の状況に応じたログ出力を行わせたいとしましょう。例えば DEBUG よりも高いレベルの
メッセージはファイルに記録し、INFO 以上のレベルのメッセージはコンソールに出力したいという場合です。また、ファイルにはタイムスタンプを
記録し、コンソールには出力しないとします。以下のようにすれば、こうした挙動を実現できます。


::

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


.. When you run this, on the console you will see

このスクリプトを実行すると、コンソールには以下のように表示されるでしょう。


::

   root        : INFO     Jackdaws love my big sphinx of quartz.
   myapp.area1 : INFO     How quickly daft jumping zebras vex.
   myapp.area2 : WARNING  Jail zesty vixen who grabbed pay from quack.
   myapp.area2 : ERROR    The five boxing wizards jump quickly.


.. and in the file you will see something like

そして、ファイルは以下のようになるはずです。


::

   10-22 22:19 root         INFO     Jackdaws love my big sphinx of quartz.
   10-22 22:19 myapp.area1  DEBUG    Quick zephyrs blow, vexing daft Jim.
   10-22 22:19 myapp.area1  INFO     How quickly daft jumping zebras vex.
   10-22 22:19 myapp.area2  WARNING  Jail zesty vixen who grabbed pay from quack.
   10-22 22:19 myapp.area2  ERROR    The five boxing wizards jump quickly.


.. As you can see, the DEBUG message only shows up in the file. The other messages
.. are sent to both destinations.

ご覧のように、 DEBUG メッセージはファイルだけに出力され、その他のメッセージは両方に出力されます。


.. This example uses console and file handlers, but you can use any number and
.. combination of handlers you choose.

この例題では、コンソールとファイルのハンドラだけを使っていますが、実際には任意の数のハンドラや組み合わせを使えます。


.. _context-info:

文脈情報をログ記録出力に付加する
--------------------------------

.. Sometimes you want logging output to contain contextual information in
.. addition to the parameters passed to the logging call. For example, in a
.. networked application, it may be desirable to log client-specific information
.. in the log (e.g. remote client's username, or IP address). Although you could
.. use the *extra* parameter to achieve this, it's not always convenient to pass
.. the information in this way. While it might be tempting to create
.. :class:`Logger` instances on a per-connection basis, this is not a good idea
.. because these instances are not garbage collected. While this is not a problem
.. in practice, when the number of :class:`Logger` instances is dependent on the
.. level of granularity you want to use in logging an application, it could
.. be hard to manage if the number of :class:`Logger` instances becomes
.. effectively unbounded.

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


.. An easy way in which you can pass contextual information to be output along
.. with logging event information is to use the :class:`LoggerAdapter` class.
.. This class is designed to look like a :class:`Logger`, so that you can call
.. :meth:`debug`, :meth:`info`, :meth:`warning`, :meth:`error`,
.. :meth:`exception`, :meth:`critical` and :meth:`log`. These methods have the
.. same signatures as their counterparts in :class:`Logger`, so you can use the
.. two types of instances interchangeably.

ログ記録イベントの情報と一緒に出力される文脈情報を渡す簡単な方法は、
:class:`LoggerAdapter` を使うことです。
このクラスは :class:`Logger` のように見えるようにデザインされていて、
:meth:`debug`, :meth:`info`, :meth:`warning`, :meth:`error`,
:meth:`exception`, :meth:`critical`, :meth:`log` の各メソッドを呼び出せるようになっています。
これらのメソッドは対応する :class:`Logger` のメソッドと同じ引数を取りますので、
二つの型を取り替えて使うことができます。


.. When you create an instance of :class:`LoggerAdapter`, you pass it a
.. :class:`Logger` instance and a dict-like object which contains your contextual
.. information. When you call one of the logging methods on an instance of
.. :class:`LoggerAdapter`, it delegates the call to the underlying instance of
.. :class:`Logger` passed to its constructor, and arranges to pass the contextual
.. information in the delegated call. Here's a snippet from the code of
.. :class:`LoggerAdapter`:

:class:`LoggerAdapter` のインスタンスを生成する際には、
:class:`Logger` インスタンスと文脈情報を収めた辞書風のオブジェクトを渡します。
:class:`LoggerAdapter` のログ記録メソッドを呼び出すと、
呼び出しをコンストラクタに渡された配下の :class:`Logger` インスタンスに委譲し、
その際文脈情報をその委譲された呼び出しに埋め込みます。
:class:`LoggerAdapter` のコードから少し抜き出してみます。


::

    def debug(self, msg, *args, **kwargs):
        """
        Delegate a debug call to the underlying logger, after adding
        contextual information from this adapter instance.
        """
        msg, kwargs = self.process(msg, kwargs)
        self.logger.debug(msg, *args, **kwargs)


.. The :meth:`process` method of :class:`LoggerAdapter` is where the contextual
.. information is added to the logging output. It's passed the message and
.. keyword arguments of the logging call, and it passes back (potentially)
.. modified versions of these to use in the call to the underlying logger. The
.. default implementation of this method leaves the message alone, but inserts
.. an "extra" key in the keyword argument whose value is the dict-like object
.. passed to the constructor. Of course, if you had passed an "extra" keyword
.. argument in the call to the adapter, it will be silently overwritten.

:class:`LoggerAdapter` の :meth:`process` メソッドが文脈情報をログ出力に加える舞台です。
そこではログ記録呼び出しのメッセージとキーワード引数が渡され、
加工された(はずの)それらの情報を配下のロガーへの呼び出しに渡し直します。
このメソッドのデフォルト実装ではメッセージは元のままですが、
キーワード引数にはコンストラクタに渡された辞書風オブジェクトを値として
"extra" キーが挿入されます。
もちろん、呼び出し時に "extra" キーワードを使った場合には何事もなかったかのように上書きされます。


.. The advantage of using "extra" is that the values in the dict-like object are
.. merged into the :class:`LogRecord` instance's __dict__, allowing you to use
.. customized strings with your :class:`Formatter` instances which know about
.. the keys of the dict-like object. If you need a different method, e.g. if you
.. want to prepend or append the contextual information to the message string,
.. you just need to subclass :class:`LoggerAdapter` and override :meth:`process`
.. to do what you need. Here's an example script which uses this class, which
.. also illustrates what dict-like behaviour is needed from an arbitrary
.. "dict-like" object for use in the constructor:

"extra" を用いる利点は辞書風オブジェクトの中の値が :class:`LogRecord` インスタンスの
__dict__ にマージされることで、
辞書風オブジェクトのキーを知っている :class:`Formatter` を用意して文字列をカスタマイズするようにできることです。
それ以外のメソッドが必要なとき、たとえば文脈情報をメッセージの前や後ろにつなげたい場合には、
:class:`LoggerAdapter` から :meth:`process` を望むようにオーバライドしたサブクラスを作ることが必要なだけです。
次に挙げるのはこのクラスを使った例で、どの辞書風の振る舞いがコンストラクタで使われる「辞書風」オブジェクトに必要なのかも見せます。


::

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


.. When this script is run, the output should look something like this:

このスクリプトが実行されると、出力は以下のようになります。


::

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


.. The :class:`LoggerAdapter` class was not present in previous versions.

:class:`LoggerAdapter` クラスは以前のバージョンにはありません。


.. _network-logging:

ログイベントをネットワーク越しに送受信する
------------------------------------------

.. Let's say you want to send logging events across a network, and handle them at
.. the receiving end. A simple way of doing this is attaching a
.. :class:`SocketHandler` instance to the root logger at the sending end:

ログイベントをネットワーク越しに送信し、受信端でそれを処理したいとしましょう。 :class:`SocketHandler`
インスタンスを送信端のルートロガーに接続すれば、簡単に実現できます。


::

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


.. At the receiving end, you can set up a receiver using the :mod:`SocketServer`
.. module. Here is a basic working example:

受信端では、 :mod:`SocketServer` モジュールを使って受信プログラムを作成しておきます。簡単な実用プログラムを以下に示します。


::

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


.. First run the server, and then the client. On the client side, nothing is
.. printed on the console; on the server side, you should see something like:

先にサーバを起動しておき、次にクライアントを起動します。クライアント側では、コンソールには何も出力されません; サーバ側では以下のようなメッセージ
を目にするはずです。


::

   About to start TCP server...
      59 root            INFO     Jackdaws love my big sphinx of quartz.
      59 myapp.area1     DEBUG    Quick zephyrs blow, vexing daft Jim.
      69 myapp.area1     INFO     How quickly daft jumping zebras vex.
      69 myapp.area2     WARNING  Jail zesty vixen who grabbed pay from quack.
      69 myapp.area2     ERROR    The five boxing wizards jump quickly.


Handler オブジェクト
--------------------

.. Handlers have the following attributes and methods. Note that :class:`Handler`
.. is never instantiated directly; this class acts as a base for more useful
.. subclasses. However, the :meth:`__init__` method in subclasses needs to call
.. :meth:`Handler.__init__`.

ハンドラは以下の属性とメソッドを持ちます。 :class:`Handler` は直接インスタンス化されることはありません; このクラスは
より便利なサブクラスの基底クラスとして働きます。しかしながら、サブクラスにおける :meth:`__init__` メソッドでは、
:meth:`Handler.__init__` を呼び出す必要があります。


.. method:: Handler.__init__(level=NOTSET)

   .. Initializes the :class:`Handler` instance by setting its level, setting the list
   .. of filters to the empty list and creating a lock (using :meth:`createLock`) for
   .. serializing access to an I/O mechanism.

   レベルを設定して、 :class:`Handler` インスタンスを初期化します。空のリストを使ってフィルタを設定し、I/O 機構へのアクセスを
   直列化するために (:meth:`createLock` を使って) ロックを生成します。


.. method:: Handler.createLock()

   .. Initializes a thread lock which can be used to serialize access to underlying
   .. I/O functionality which may not be threadsafe.

   スレッド安全でない根底の I/O 機能に対するアクセスを直列化するために用いられるスレッドロック (thread lock) を初期化します。


.. method:: Handler.acquire()

   .. Acquires the thread lock created with :meth:`createLock`.

   :meth:`createLock` で生成されたスレッドロックを獲得します。


.. method:: Handler.release()

   .. Releases the thread lock acquired with :meth:`acquire`.

   :meth:`acquire` で獲得したスレッドロックを解放します。


.. method:: Handler.setLevel(lvl)

   .. Sets the threshold for this handler to *lvl*. Logging messages which are less
   .. severe than *lvl* will be ignored. When a handler is created, the level is set
   .. to :const:`NOTSET` (which causes all messages to be processed).

   このハンドラに対する閾値を *lvl* に設定します。ログ記録しようとするメッセージで、 *lvl* よりも深刻でないものは
   無視されます。ハンドラが生成された際、レベルは :const:`NOTSET`  (全てのメッセージが処理される) に設定されます。


.. method:: Handler.setFormatter(form)

   .. Sets the :class:`Formatter` for this handler to *form*.

   このハンドラのフォーマッタを *form* に設定します。


.. method:: Handler.addFilter(filt)

   .. Adds the specified filter *filt* to this handler.

   指定されたフィルタ *filt* をこのハンドラに追加します。


.. method:: Handler.removeFilter(filt)

   .. Removes the specified filter *filt* from this handler.

   指定されたフィルタ *filt* をこのハンドラから除去します。


.. method:: Handler.filter(record)

   .. Applies this handler's filters to the record and returns a true value if the
   .. record is to be processed.

   このハンドラのフィルタをレコードに適用し、レコードがフィルタを透過して処理されることになる場合には真を返します。


.. method:: Handler.flush()

   .. Ensure all logging output has been flushed. This version does nothing and is
   .. intended to be implemented by subclasses.

   全てのログ出力がフラッシュされるようにします。このクラスのバージョンではなにも行わず、サブクラスで実装するためのものです。


.. method:: Handler.close()

   .. Tidy up any resources used by the handler. This version does no output but
   .. removes the handler from an internal list of handlers which is closed when
   .. :func:`shutdown` is called. Subclasses should ensure that this gets called
   .. from overridden :meth:`close` methods.

   ハンドラで使われている全てのリソースを始末します。
   このバージョンでは何も出力しませんが、内部リストから
   :func:`shutdown` が呼ばれたときに閉じられるハンドラを削除します。
   サブクラスではオーバライドされた :meth:`close` メソッドからこのメソッドが必ず呼ばれるようにして下さい。


.. method:: Handler.handle(record)

   .. Conditionally emits the specified logging record, depending on filters which may
   .. have been added to the handler. Wraps the actual emission of the record with
   .. acquisition/release of the I/O thread lock.

   ハンドラに追加されたフィルタの条件に応じて、指定されたログレコードを発信します。このメソッドは I/O スレッドロックの獲得/開放を伴う実際の
   ログ発信をラップします。


.. method:: Handler.handleError(record)

   .. This method should be called from handlers when an exception is encountered
   .. during an :meth:`emit` call. By default it does nothing, which means that
   .. exceptions get silently ignored. This is what is mostly wanted for a logging
   .. system - most users will not care about errors in the logging system, they are
   .. more interested in application errors. You could, however, replace this with a
   .. custom handler if you wish. The specified record is the one which was being
   .. processed when the exception occurred.

   このメソッドは :meth:`emit` の呼び出し中に例外に遭遇した際にハンドラから呼び出されます。デフォルトではこのメソッドは
   何も行いません。すなわち、例外は暗黙のまま無視されます。ほとんどのログ記録システムでは、これがほぼ望ましい機能です -
   というのは、ほとんどのユーザはログ記録システム自体のエラーは気にせず、むしろアプリケーションのエラーに興味があるからです。
   しかしながら、望むならこのメソッドを自作のハンドラと置き換えることはできます。 *record* には、例外発生時に処理されていたレコードが入ります。


.. method:: Handler.format(record)

   .. Do formatting for a record - if a formatter is set, use it. Otherwise, use the
   .. default formatter for the module.

   レコードに対する書式化を行います - フォーマッタが設定されていれば、それを使います。そうでない場合、
   モジュールにデフォルト指定されたフォーマッタを使います。


.. method:: Handler.emit(record)

   .. Do whatever it takes to actually log the specified logging record. This version
   .. is intended to be implemented by subclasses and so raises a
   .. :exc:`NotImplementedError`.

   指定されたログ記録レコードを実際にログ記録する際の全ての処理を行います。このメソッドのこのクラスのバージョンはサブクラスで
   実装するためのものなので、 :exc:`NotImplementedError` を送出します。


StreamHandler
^^^^^^^^^^^^^

.. module:: logging.handlers

.. The :class:`StreamHandler` class, located in the core :mod:`logging` package,
.. sends logging output to streams such as *sys.stdout*, *sys.stderr* or any
.. file-like object (or, more precisely, any object which supports :meth:`write`
.. and :meth:`flush` methods).

:class:`StreamHandler` クラスは、 :mod:`logging` パッケージのコアにありますが、ログ出力を
*sys.stdout*, *sys.stderr* あるいは何らかのファイル類似オブジェクト(あるいは、もっと正確にいえば、 :meth:`write`
および :meth:`flush` メソッドをサポートする何らかのオブジェクト) といったストリームに送信します。


.. class:: StreamHandler([strm])

   .. Returns a new instance of the :class:`StreamHandler` class. If *strm* is
   .. specified, the instance will use it for logging output; otherwise, *sys.stderr*
   .. will be used.

   :class:`StreamHandler` クラスの新たなインスタンスを返します。 *strm* が指定された場合、インスタンスはログ出力先として
   指定されたストリームを使います; そうでない場合、 *sys.stderr* が使われます。


   .. method:: emit(record)

      .. If a formatter is specified, it is used to format the record. The record
      .. is then written to the stream with a trailing newline. If exception
      .. information is present, it is formatted using
      .. :func:`traceback.print_exception` and appended to the stream.

      フォーマッタが指定されていれば、フォーマッタを使ってレコードを書式化します。
      次に、レコードがストリームに書き込まれ、末端に改行がつけられます。
      例外情報が存在する場合、 :func:`traceback.print_exception` を使って書式化され、
      ストリームの末尾につけられます。


   .. method:: flush()

      .. Flushes the stream by calling its :meth:`flush` method. Note that the
      .. :meth:`close` method is inherited from :class:`Handler` and so does
      .. no output, so an explicit :meth:`flush` call may be needed at times.

      ストリームの :meth:`flush` メソッドを呼び出してバッファをフラッシュします。
      :meth:`close` メソッドは :class:`Handler` から継承しているため何も行わないので、 :meth:`flush` 呼び出しを明示的に行う必要があります。


FileHandler
^^^^^^^^^^^

.. The :class:`FileHandler` class, located in the core :mod:`logging` package,
.. sends logging output to a disk file.  It inherits the output functionality from
.. :class:`StreamHandler`.

:class:`FileHandler` クラスは、 :mod:`logging` パッケージのコアにありますが、ログ出力をディスク上のファイルに送信します。このクラスは出力機能を :class:`StreamHandler` から継承しています。


.. class:: FileHandler(filename[, mode[, encoding[, delay]]])

   .. Returns a new instance of the :class:`FileHandler` class. The specified file is
   .. opened and used as the stream for logging. If *mode* is not specified,
   .. :const:`'a'` is used.  If *encoding* is not *None*, it is used to open the file
   .. with that encoding.  If *delay* is true, then file opening is deferred until the
   .. first call to :meth:`emit`. By default, the file grows indefinitely.

   :class:`FileHandler` クラスの新たなインスタンスを返します。
   指定されたファイルが開かれ、ログ記録のためのストリームとして使われます。
   *mode* が指定されなかった場合、 :const:`'a'` が使われます。
   *encoding* が *None* でない場合、その値はファイルを開くときのエンコーディングとして使われます。
   *delay* が真であるならば、ファイルを開くのは最初の :meth:`emit` 呼び出しまで遅らせられます。
   デフォルトでは、ファイルは無制限に大きくなりつづけます。


   .. method:: close()

      .. Closes the file.

      ファイルを閉じます。


   .. method:: emit(record)

      .. Outputs the record to the file.

      *record* をファイルに出力します。


.. See :ref:`library-config` for more information on how to use
.. :class:`NullHandler`.

:class:`NullHandler` の使い方について詳しくは :ref:`library-config` を参照して下さい。


WatchedFileHandler
^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.6


.. The :class:`WatchedFileHandler` class, located in the :mod:`logging.handlers`
.. module, is a :class:`FileHandler` which watches the file it is logging to. If
.. the file changes, it is closed and reopened using the file name.

:class:`WatchedFileHandler` クラスは、 :mod:`logging.handlers` モジュールにあり、
ログ記録先のファイルを監視する :class:`FileHandler` の一種です。
ファイルが変わった場合、ファイルを閉じてからファイル名を使って開き直します。


.. A file change can happen because of usage of programs such as *newsyslog* and
.. *logrotate* which perform log file rotation. This handler, intended for use
.. under Unix/Linux, watches the file to see if it has changed since the last emit.
.. (A file is deemed to have changed if its device or inode have changed.) If the
.. file has changed, the old file stream is closed, and the file opened to get a
.. new stream.

ファイルはログファイルをローテーションさせる *newsyslog* や
*logrotate* のようなプログラムを使うことで変わることがあります。
このハンドラは、Unix/Linux で使われることを意図していますが、
ファイルが最後にログを emit してから変わったかどうかを監視します。
(ファイルはデバイスや inode が変わることで変わったと判断します。)
ファイルが変わったら古いファイルのストリームは閉じて、現在のファイルを新しいストリームを取得するために開きます。


.. This handler is not appropriate for use under Windows, because under Windows
.. open log files cannot be moved or renamed - logging opens the files with
.. exclusive locks - and so there is no need for such a handler. Furthermore,
.. *ST_INO* is not supported under Windows; :func:`stat` always returns zero for
.. this value.

このハンドラを Windows で使うことは適切ではありません。
というのも Windows では開いているログファイルを動かしたり削除したりできないからです
- logging はファイルを排他的ロックを掛けて開きます -
そしてそれゆえにこうしたハンドラは必要ないのです。
さらに、Windows では *ST_INO* がサポートされていません
(:func:`stat` はこの値として常に 0 を返します)。


.. class:: WatchedFileHandler(filename[,mode[, encoding[, delay]]])

   .. Returns a new instance of the :class:`WatchedFileHandler` class. The specified
   .. file is opened and used as the stream for logging. If *mode* is not specified,
   .. :const:`'a'` is used.  If *encoding* is not *None*, it is used to open the file
   .. with that encoding.  If *delay* is true, then file opening is deferred until the
   .. first call to :meth:`emit`.  By default, the file grows indefinitely.

   :class:`WatchedFileHandler` クラスの新たなインスタンスを返します。
   指定されたファイルが開かれ、ログ記録のためのストリームとして使われます。
   *mode* が指定されなかった場合、 :const:`"a"` が使われます。
   *encoding* が *None* でない場合、その値はファイルを開くときのエンコーディングとして使われます。
   *delay* が真であるならば、ファイルを開くのは最初の :meth:`emit` 呼び出しまで遅らせられます。
   デフォルトでは、ファイルは無制限に大きくなりつづけます。


   .. method:: emit(record)

      .. Outputs the record to the file, but first checks to see if the file has
      .. changed.  If it has, the existing stream is flushed and closed and the
      .. file opened again, before outputting the record to the file.

      レコードをファイルに出力しますが、その前にファイルが変わっていないかチェックします。
      もし変わっていれば、レコードをファイルに出力する前に、
      既存のストリームはフラッシュして閉じられ、ファイルが再度開かれます。


RotatingFileHandler
^^^^^^^^^^^^^^^^^^^

.. The :class:`RotatingFileHandler` class, located in the :mod:`logging.handlers`
.. module, supports rotation of disk log files.

:class:`RotatingFileHandler` クラスは、
:mod:`logging.handlers` モジュールの中にありますが、
ディスク上のログファイルに対するローテーション処理をサポートします。


.. class:: RotatingFileHandler(filename[, mode[, maxBytes[, backupCount[, encoding[, delay]]]]])

   .. Returns a new instance of the :class:`RotatingFileHandler` class. The specified
   .. file is opened and used as the stream for logging. If *mode* is not specified,
   .. ``'a'`` is used.  If *encoding* is not *None*, it is used to open the file
   .. with that encoding.  If *delay* is true, then file opening is deferred until the
   .. first call to :meth:`emit`.  By default, the file grows indefinitely.

   :class:`RotatingFileHandler` クラスの新たなインスタンスを返します。
   指定されたファイルが開かれ、ログ記録のためのストリームとして使われます。
   *mode* が指定されなかった場合、 :const:`"a"` が使われます。
   *encoding* が *None* でない場合、その値はファイルを開くときのエンコーディングとして使われます。
   *delay* が真であるならば、ファイルを開くのは最初の :meth:`emit` 呼び出しまで遅らせられます。
   デフォルトでは、ファイルは無制限に大きくなりつづけます。


   .. You can use the *maxBytes* and *backupCount* values to allow the file to
   .. :dfn:`rollover` at a predetermined size. When the size is about to be exceeded,
   .. the file is closed and a new file is silently opened for output. Rollover occurs
   .. whenever the current log file is nearly *maxBytes* in length; if *maxBytes* is
   .. zero, rollover never occurs.  If *backupCount* is non-zero, the system will save
   .. old log files by appending the extensions ".1", ".2" etc., to the filename. For
   .. example, with a *backupCount* of 5 and a base file name of :file:`app.log`, you
   .. would get :file:`app.log`, :file:`app.log.1`, :file:`app.log.2`, up to
   .. :file:`app.log.5`. The file being written to is always :file:`app.log`.  When
   .. this file is filled, it is closed and renamed to :file:`app.log.1`, and if files
   .. :file:`app.log.1`, :file:`app.log.2`, etc.  exist, then they are renamed to
   .. :file:`app.log.2`, :file:`app.log.3` etc.  respectively.

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

      .. Does a rollover, as described above.

      上述のような方法でロールオーバを行います。


   .. method:: emit(record)

      .. Outputs the record to the file, catering for rollover as described
      .. previously.

      上述のようなロールオーバを行いながら、レコードをファイルに出力します。


TimedRotatingFileHandler
^^^^^^^^^^^^^^^^^^^^^^^^

.. The :class:`TimedRotatingFileHandler` class, located in the
.. :mod:`logging.handlers` module, supports rotation of disk log files at certain
.. timed intervals.

:class:`TimedRotatingFileHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、特定の時間間隔でのログ交替をサポートしています。


.. class:: TimedRotatingFileHandler(filename [,when [,interval [,backupCount[, encoding[, delay[, utc]]]]]])

   .. Returns a new instance of the :class:`TimedRotatingFileHandler` class. The
   .. specified file is opened and used as the stream for logging. On rotating it also
   .. sets the filename suffix. Rotating happens based on the product of *when* and
   .. *interval*.

   :class:`TimedRotatingFileHandler` クラスの新たなインスタンスを返します。 *filename*
   に指定したファイルを開き、ログ出力先のストリームとして使います。ログファイルの交替時には、ファイル名に拡張子 (suffix) を
   つけます。ログファイルの交替は *when* および *interval*  の積に基づいて行います。


   .. You can use the *when* to specify the type of *interval*. The list of possible
   .. values is below.  Note that they are not case sensitive.

   *when* は *interval* の単位を指定するために使います。
   使える値は下表の通りです。大小文字の区別は行いません:


   .. +----------------+-----------------------+
   .. | Value          | Type of interval      |
   .. +================+=======================+
   .. | ``'S'``        | Seconds               |
   .. +----------------+-----------------------+
   .. | ``'M'``        | Minutes               |
   .. +----------------+-----------------------+
   .. | ``'H'``        | Hours                 |
   .. +----------------+-----------------------+
   .. | ``'D'``        | Days                  |
   .. +----------------+-----------------------+
   .. | ``'W'``        | Week day (0=Monday)   |
   .. +----------------+-----------------------+
   .. | ``'midnight'`` | Roll over at midnight |
   .. +----------------+-----------------------+

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


   .. The system will save old log files by appending extensions to the filename.
   .. The extensions are date-and-time based, using the strftime format
   .. ``%Y-%m-%d_%H-%M-%S`` or a leading portion thereof, depending on the
   .. rollover interval.
   .. If the *utc* argument is true, times in UTC will be used; otherwise
   .. local time is used.

   古いログファイルを保存する際にロギングシステムは拡張子を付けます。
   拡張子は日付と時間に基づいて、
   strftime の ``%Y-%m-%d_%H-%M-%S`` 形式かその前の方の一部分を、
   ロールオーバ間隔に依存した形で使います。
   *utc* 引数が真の場合時刻は UTC になり、それ以外では現地時間が使われます。


   .. If *backupCount* is nonzero, at most *backupCount* files
   .. will be kept, and if more would be created when rollover occurs, the oldest
   .. one is deleted. The deletion logic uses the interval to determine which
   .. files to delete, so changing the interval may leave old files lying around.

   *backupCount* がゼロでない場合、保存されるファイル数は高々 *backupCount* 個で、それ以上のファイルがロールオーバされる時に作られるならば、一番古いものが削除されます。
   削除するロジックは interval で決まるファイルを削除しますので、
   interval を変えると古いファイルが残ったままになることもあります。


   .. method:: doRollover()

      .. Does a rollover, as described above.

      上記の方法でロールオーバを行います。


   .. method:: emit(record)

      .. Outputs the record to the file, catering for rollover as described above.

      :meth:`setRollover` で解説した方法でロールオーバを行いながら、レコードをファイルに出力します。


SocketHandler
^^^^^^^^^^^^^

.. The :class:`SocketHandler` class, located in the :mod:`logging.handlers` module,
.. sends logging output to a network socket. The base class uses a TCP socket.

:class:`SocketHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、ログ出力をネットワークソケットに送信します。基底クラスでは TCP ソケットを用います。


.. class:: SocketHandler(host, port)

   .. Returns a new instance of the :class:`SocketHandler` class intended to
   .. communicate with a remote machine whose address is given by *host* and *port*.

   アドレスが *host* および *port* で与えられた遠隔のマシンと通信するようにした :class:`SocketHandler`
   クラスのインスタンスを生成して返します。


   .. method:: close()

      .. Closes the socket.

      ソケットを閉じます。


   .. method:: emit()

      .. Pickles the record's attribute dictionary and writes it to the socket in
      .. binary format. If there is an error with the socket, silently drops the
      .. packet. If the connection was previously lost, re-establishes the
      .. connection. To unpickle the record at the receiving end into a
      .. :class:`LogRecord`, use the :func:`makeLogRecord` function.

      レコードの属性辞書を pickle 化し、バイナリ形式でソケットに書き込みます。
      ソケット操作でエラーが生じた場合、暗黙のうちにパケットは捨てられます。
      前もって接続が失われていた場合、接続を再度確立します。
      受信端でレコードを逆 pickle 化して :class:`LogRecord`
      にするには、 :func:`makeLogRecord` 関数を使ってください。


   .. method:: handleError()

      .. Handles an error which has occurred during :meth:`emit`. The most likely
      .. cause is a lost connection. Closes the socket so that we can retry on the
      .. next event.

      :meth:`emit` の処理中に発生したエラーを処理します。
      よくある原因は接続の消失です。
      次のイベント発生時に再度接続確立を試みることができるようにソケットを閉じます。


   .. method:: makeSocket()

      .. This is a factory method which allows subclasses to define the precise
      .. type of socket they want. The default implementation creates a TCP socket
      .. (:const:`socket.SOCK_STREAM`).

      サブクラスで必要なソケット形式を詳細に定義できるようにするためのファクトリメソッドです。デフォルトの実装では、TCP ソケット
      (:const:`socket.SOCK_STREAM`) を生成します。


   .. method:: makePickle(record)

      .. Pickles the record's attribute dictionary in binary format with a length
      .. prefix, and returns it ready for transmission across the socket.

      レコードの属性辞書を pickle 化して、長さを指定プレフィクス付きのバイナリにし、ソケットを介して送信できるようにして返します。


   .. method:: send(packet)

      .. Send a pickled string *packet* to the socket. This function allows for
      .. partial sends which can happen when the network is busy.

      pickle 化された文字列 *packet* をソケットに送信します。
      この関数はネットワークが処理待ち状態の時に発生しうる部分的送信を行えます。


DatagramHandler
^^^^^^^^^^^^^^^

.. The :class:`DatagramHandler` class, located in the :mod:`logging.handlers`
.. module, inherits from :class:`SocketHandler` to support sending logging messages
.. over UDP sockets.

:class:`DatagramHandler` クラスは、 :mod:`logging.handlers` モジュールの中にありますが、
:class:`SocketHandler` を継承しており、ログ記録メッセージを UDP ソケットを介して送れるようサポートしています。


.. class:: DatagramHandler(host, port)

   .. Returns a new instance of the :class:`DatagramHandler` class intended to
   .. communicate with a remote machine whose address is given by *host* and *port*.

   アドレスが *host* および *port* で与えられた遠隔のマシンと通信するようにした :class:`DatagramHandler`
   クラスのインスタンスを生成して返します。


   .. method:: emit()

      .. Pickles the record's attribute dictionary and writes it to the socket in
      .. binary format. If there is an error with the socket, silently drops the
      .. packet. To unpickle the record at the receiving end into a
      .. :class:`LogRecord`, use the :func:`makeLogRecord` function.

      レコードの属性辞書を pickle 化し、バイナリ形式でソケットに書き込みます。
      ソケット操作でエラーが生じた場合、暗黙のうちにパケットは捨てられます。
      前もって接続が失われていた場合、接続を再度確立します。
      受信端でレコードを逆 pickle 化して :class:`LogRecord`
      にするには、 :func:`makeLogRecord` 関数を使ってください。


   .. method:: makeSocket()

      .. The factory method of :class:`SocketHandler` is here overridden to create
      .. a UDP socket (:const:`socket.SOCK_DGRAM`).

      ここで :class:`SocketHandler` のファクトリメソッドをオーバライドして UDP ソケット
      (:const:`socket.SOCK_DGRAM`) を生成しています。


   .. method:: send(s)

      .. Send a pickled string to a socket.

      pickle 化された文字列をソケットに送信します。


SysLogHandler
^^^^^^^^^^^^^

.. The :class:`SysLogHandler` class, located in the :mod:`logging.handlers` module,
.. supports sending logging messages to a remote or local Unix syslog.

:class:`SysLogHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、ログ記録メッセージを遠隔またはローカルの Unix syslog に送信する機能をサポートしています。


.. class:: SysLogHandler([address[, facility]])

   .. Returns a new instance of the :class:`SysLogHandler` class intended to
   .. communicate with a remote Unix machine whose address is given by *address* in
   .. the form of a ``(host, port)`` tuple.  If *address* is not specified,
   .. ``('localhost', 514)`` is used.  The address is used to open a UDP socket.  An
   .. alternative to providing a ``(host, port)`` tuple is providing an address as a
   .. string, for example "/dev/log". In this case, a Unix domain socket is used to
   .. send the message to the syslog. If *facility* is not specified,
   .. :const:`LOG_USER` is used.

   遠隔のUnix マシンと通信するための、 :class:`SysLogHandler` クラスの新たなインスタンスを返します。マシンのアドレスは
   ``(host, port)`` のタプル形式をとる *address* で与えられます。
   *address* が指定されない場合、 ``('localhost', 514)`` が使われます。
   アドレスは UDP ソケットを使って開かれます。
   ``(host, port)`` のタプル形式の代わりに文字列で "/dev/log" のように与えることもできます。
   この場合、Unix ドメインソケットが syslog にメッセージを送るのに使われます。
   *facility* が指定されない場合、 :const:`LOG_USER` が使われます。


   .. method:: close()

      .. Closes the socket to the remote host.

      遠隔ホストのソケットを閉じます。


   .. method:: emit(record)

      .. The record is formatted, and then sent to the syslog server. If exception
      .. information is present, it is *not* sent to the server.

      レコードは書式化された後、syslog サーバに送信されます。
      例外情報が存在しても、サーバには *送信されません* 。


   .. method:: encodePriority(facility, priority)

      .. Encodes the facility and priority into an integer. You can pass in strings
      .. or integers - if strings are passed, internal mapping dictionaries are
      .. used to convert them to integers.

      便宜レベル (facility) および優先度を整数に符号化します。
      値は文字列でも整数でも渡すことができます。
      文字列が渡された場合、内部の対応付け辞書が使われ、整数に変換されます。


NTEventLogHandler
^^^^^^^^^^^^^^^^^

.. The :class:`NTEventLogHandler` class, located in the :mod:`logging.handlers`
.. module, supports sending logging messages to a local Windows NT, Windows 2000 or
.. Windows XP event log. Before you can use it, you need Mark Hammond's Win32
.. extensions for Python installed.

:class:`NTEventLogHandler` クラスは、 :mod:`logging.handlers` モ
ジュールの中にありますが、ログ記録メッセージをローカルな Windows NT、Windows 2000 、または Windows XP のイベントログ
(event log) に送信する機能をサポートします。この機能を使えるようにするには、 Mark Hammond による Python 用 Win32
拡張パッケージをインストールする必要があります。


.. class:: NTEventLogHandler(appname[, dllname[, logtype]])

   .. Returns a new instance of the :class:`NTEventLogHandler` class. The *appname* is
   .. used to define the application name as it appears in the event log. An
   .. appropriate registry entry is created using this name. The *dllname* should give
   .. the fully qualified pathname of a .dll or .exe which contains message
   .. definitions to hold in the log (if not specified, ``'win32service.pyd'`` is used
   .. - this is installed with the Win32 extensions and contains some basic
   .. placeholder message definitions. Note that use of these placeholders will make
   .. your event logs big, as the entire message source is held in the log. If you
   .. want slimmer logs, you have to pass in the name of your own .dll or .exe which
   .. contains the message definitions you want to use in the event log). The
   .. *logtype* is one of ``'Application'``, ``'System'`` or ``'Security'``, and
   .. defaults to ``'Application'``.

   :class:`NTEventLogHandler` クラスの新たなインスタンスを返します。 *appname*
   はイベントログに表示する際のアプリケーション名を定義するために使われます。この名前を使って適切なレジストリエントリが生成されます。 *dllname*
   はログに保存するメッセージ定義の入った .dll または .exe  ファイルへの完全に限定的な (fully qualified) パス名を与えなければ
   なりません (指定されない場合、 :const:`'win32service.pyd'` が使われます - このライブラリは Win32
   拡張とともにインストールされ、いくつかのプレースホルダとなるメッセージ定義を含んでいます)。
   これらのプレースホルダを利用すると、メッセージの発信源全体がログに記録されるため、イベントログは巨大になるので注意してください。 *logtype* は
   :const:`'Application'` 、 :const:`'System'`  または :const:`'Security'`
   のいずれかであるか、デフォルトの :const:`'Application'` でなければなりません。


   .. method:: close()

      .. At this point, you can remove the application name from the registry as a
      .. source of event log entries. However, if you do this, you will not be able
      .. to see the events as you intended in the Event Log Viewer - it needs to be
      .. able to access the registry to get the .dll name. The current version does
      .. not do this.

      現時点では、イベントログエントリの発信源としてのアプリケーション名をレジストリから除去することができます。
      しかしこれを行うと、イベントログビューアで意図したログをみることができなくなるでしょう - これはイベントログが .dll 名を取得するために\
      レジストリにアクセスできなければならないからです。現在のバージョンではこの操作を行いません。


   .. method:: emit(record)

      .. Determines the message ID, event category and event type, and then logs
      .. the message in the NT event log.

      メッセージ ID、イベントカテゴリおよびイベント型を決定し、メッセージを NT イベントログに記録します。


   .. method:: getEventCategory(record)

      .. Returns the event category for the record. Override this if you want to
      .. specify your own categories. This version returns 0.

      レコードに対するイベントカテゴリを返します。
      自作のカテゴリを指定したい場合、このメソッドをオーバライドしてください。
      このクラスのバージョンのメソッドは 0 を返します。


   .. method:: getEventType(record)

      .. Returns the event type for the record. Override this if you want to
      .. specify your own types. This version does a mapping using the handler's
      .. typemap attribute, which is set up in :meth:`__init__` to a dictionary
      .. which contains mappings for :const:`DEBUG`, :const:`INFO`,
      .. :const:`WARNING`, :const:`ERROR` and :const:`CRITICAL`. If you are using
      .. your own levels, you will either need to override this method or place a
      .. suitable dictionary in the handler's *typemap* attribute.

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

      .. Returns the message ID for the record. If you are using your own messages,
      .. you could do this by having the *msg* passed to the logger being an ID
      .. rather than a format string. Then, in here, you could use a dictionary
      .. lookup to get the message ID. This version returns 1, which is the base
      .. message ID in :file:`win32service.pyd`.

      レコードのメッセージ ID を返します。
      自作のメッセージを使っているのなら、ロガーに渡される *msg* を書式化文字列ではなく ID にします。
      その上で、辞書参照を行ってメッセージ ID を得ます。
      このクラスのバージョンでは 1 を返します。この値は
      :file:`win32service.pyd` における基本となるメッセージ ID です。


SMTPHandler
^^^^^^^^^^^

.. The :class:`SMTPHandler` class, located in the :mod:`logging.handlers` module,
.. supports sending logging messages to an email address via SMTP.

:class:`SMTPHandler` クラスは、 :mod:`logging.handlers` モジュールの中にありますが、SMTP
を介したログ記録メッセージの送信機能をサポートします。


.. class:: SMTPHandler(mailhost, fromaddr, toaddrs, subject[, credentials])

   .. Returns a new instance of the :class:`SMTPHandler` class. The instance is
   .. initialized with the from and to addresses and subject line of the email. The
   .. *toaddrs* should be a list of strings. To specify a non-standard SMTP port, use
   .. the (host, port) tuple format for the *mailhost* argument. If you use a string,
   .. the standard SMTP port is used. If your SMTP server requires authentication, you
   .. can specify a (username, password) tuple for the *credentials* argument.

   新たな :class:`SMTPHandler` クラスのインスタンスを返します。
   インスタンスは email の from および to アドレス行、および
   subject 行とともに初期化されます。
   *toaddrs* は文字列からなるリストでなければなりません非標準の SMTP
   ポートを指定するには、 *mailhost* 引数に (host, port)  のタプル形式を指定します。
   文字列を使った場合、標準の SMTP ポートが使われます。
   もし SMTP サーバが認証を必要とするならば、(username, password) のタプル形式を
   *credentials* 引数に指定することができます。


   .. .. versionchanged:: 2.6
   ..    *credentials* was added.

   .. versionchanged:: 2.6
      *credentials* が追加されました。


   .. method:: emit(record)

      .. Formats the record and sends it to the specified addressees.

      レコードを書式化し、指定されたアドレスに送信します。


   .. method:: getSubject(record)

      .. If you want to specify a subject line which is record-dependent, override
      .. this method.

      レコードに応じたサブジェクト行を指定したいなら、このメソッドをオーバライドしてください。


MemoryHandler
^^^^^^^^^^^^^

.. The :class:`MemoryHandler` class, located in the :mod:`logging.handlers` module,
.. supports buffering of logging records in memory, periodically flushing them to a
.. :dfn:`target` handler. Flushing occurs whenever the buffer is full, or when an
.. event of a certain severity or greater is seen.

:class:`MemoryHandler` は、 :mod:`logging.handlers` モジュールの中にありますが、
ログ記録するレコードをメモリ上にバッファし、
定期的にその内容をターゲット (:dfn:`target`)
となるハンドラにフラッシュする機能をサポートしています。
フラッシュ処理はバッファが一杯になるか、
ある深刻さかそれ以上のレベルをもったイベントが観測された際に行われます。


.. :class:`MemoryHandler` is a subclass of the more general
.. :class:`BufferingHandler`, which is an abstract class. This buffers logging
.. records in memory. Whenever each record is added to the buffer, a check is made
.. by calling :meth:`shouldFlush` to see if the buffer should be flushed.  If it
.. should, then :meth:`flush` is expected to do the needful.

:class:`MemoryHandler` はより一般的な抽象クラス、
:class:`BufferingHandler` のサブクラスです。
この抽象クラスでは、ログ記録するレコードをメモリ上にバッファします。
各レコードがバッファに追加される毎に、
:meth:`shouldFlush` を呼び出してバッファをフラッシュすべきかどうか調べます。
フラッシュする必要がある場合、
:meth:`flush` が必要にして十分な処理を行うものと想定しています。


.. class:: BufferingHandler(capacity)

   .. Initializes the handler with a buffer of the specified capacity.

   指定した許容量のバッファでハンドラを初期化します。


   .. method:: emit(record)

      .. Appends the record to the buffer. If :meth:`shouldFlush` returns true,
      .. calls :meth:`flush` to process the buffer.

      レコードをバッファに追加します。
      :meth:`shouldFlush` が真を返す場合、バッファを処理するために :meth:`flush`
      を呼び出します。


   .. method:: flush()

      .. You can override this to implement custom flushing behavior. This version
      .. just zaps the buffer to empty.

      このメソッドをオーバライドして、自作のフラッシュ動作を実装することができます。
      このクラスのバージョンのメソッドでは、単にバッファの内容を削除して空にします。


   .. method:: shouldFlush(record)

      .. Returns true if the buffer is up to capacity. This method can be
      .. overridden to implement custom flushing strategies.

      バッファが許容量に達している場合に真を返します。
      このメソッドは自作のフラッシュ処理方針を実装するためにオーバライドすることができます。


.. class:: MemoryHandler(capacity[, flushLevel [, target]])

   .. Returns a new instance of the :class:`MemoryHandler` class. The instance is
   .. initialized with a buffer size of *capacity*. If *flushLevel* is not specified,
   .. :const:`ERROR` is used. If no *target* is specified, the target will need to be
   .. set using :meth:`setTarget` before this handler does anything useful.

   :class:`MemoryHandler` クラスの新たなインスタンスを返します。
   インスタンスはサイズ *capacity* のバッファとともに初期化されます。
   *flushLevel* が指定されていない場合、 :const:`ERROR` が使われます。
   *target* が指定されていない場合、ハンドラが何らかの有意義な処理を行う前に
   :meth:`setTarget` でターゲットを指定する必要があります。


   .. method:: close()

      .. Calls :meth:`flush`, sets the target to :const:`None` and clears the
      .. buffer.

      :meth:`flush` を呼び出し、ターゲットを :const:`None` に設定してバッファを消去します。


   .. method:: flush()

      .. For a :class:`MemoryHandler`, flushing means just sending the buffered
      .. records to the target, if there is one. Override if you want different
      .. behavior.

      :class:`MemoryHandler` の場合、フラッシュ処理は単に、バッファされたレコードをターゲットがあれば送信することを意味します。
      違った動作を行いたい場合、オーバライドしてください。


   .. method:: setTarget(target)

      .. Sets the target handler for this handler.

      ターゲットハンドラをこのハンドラに設定します。


   .. method:: shouldFlush(record)

      .. Checks for buffer full or a record at the *flushLevel* or higher.

      バッファが満杯になっているか、 *flushLevel* またはそれ以上のレコードでないかを調べます。


HTTPHandler
^^^^^^^^^^^

.. The :class:`HTTPHandler` class, located in the :mod:`logging.handlers` module,
.. supports sending logging messages to a Web server, using either ``GET`` or
.. ``POST`` semantics.

:class:`HTTPHandler` クラスは、 :mod:`logging.handlers` モジュールの中にありますが、ログ記録メッセージを
``GET`` または ``POST`` セマンティクスを使って Web サーバに送信する機能をサポートしています。


.. class:: HTTPHandler(host, url[, method])

   .. Returns a new instance of the :class:`HTTPHandler` class. The instance is
   .. initialized with a host address, url and HTTP method. The *host* can be of the
   .. form ``host:port``, should you need to use a specific port number. If no
   .. *method* is specified, ``GET`` is used.

   :class:`HTTPHandler` クラスの新たなインスタンスを返します。インスタンスはホストアドレス、URL および HTTP メソッドと
   ともに初期化されます。 *host* は特別なポートを使うことが必要な場合には、 ``host:port`` の形式で使うこともできます。 *method*
   が指定されなかった場合 ``GET`` が使われます。


   .. method:: emit(record)

      .. Sends the record to the Web server as an URL-encoded dictionary.

      レコードを URL エンコードされた辞書形式で Web サーバに送信します。


.. _formatter-objects:

Formatter オブジェクト
----------------------

.. currentmodule:: logging


.. :class:`Formatter`\ s have the following attributes and methods. They are
.. responsible for converting a :class:`LogRecord` to (usually) a string which can
.. be interpreted by either a human or an external system. The base
.. :class:`Formatter` allows a formatting string to be specified. If none is
.. supplied, the default value of ``'%(message)s'`` is used.

:class:`Formatter` は以下の属性とメソッドを持っています。 :class:`Formatter` は :class:`LogRecord` を
(通常は) 人間か外部のシステムで解釈できる文字列に変換する役割を担っています。基底クラスの :class:`Formatter`
では書式化文字列を指定することができます。何も指定されなかった場合、 ``'%(message)s'`` の値が使われます。


.. A Formatter can be initialized with a format string which makes use of knowledge
.. of the :class:`LogRecord` attributes - such as the default value mentioned above
.. making use of the fact that the user's message and arguments are pre-formatted
.. into a :class:`LogRecord`'s *message* attribute.  This format string contains
.. standard python %-style mapping keys. See section :ref:`string-formatting`
.. for more information on string formatting.

Formatter は書式化文字列とともに初期化され、 :class:`LogRecord` 属性に入っている知識を利用できるようにします -
上で触れたデフォルトの値では、ユーザによるメッセージと引数はあらかじめ書式化されて、 :class:`LogRecord` の *message*
属性に入っていることを利用しているようにです。この書式化文字列は、Python 標準の % を使った変換文字列で構成されます。文字列整形に関する詳細は
:ref:`string-formatting` を参照してください。


.. Currently, the useful mapping keys in a :class:`LogRecord` are:

現状では、 :class:`LogRecord` の有用な属性は以下のようになっています:


.. +-------------------------+-----------------------------------------------+
.. | Format                  | Description                                   |
.. +=========================+===============================================+
.. | ``%(name)s``            | Name of the logger (logging channel).         |
.. +-------------------------+-----------------------------------------------+
.. | ``%(levelno)s``         | Numeric logging level for the message         |
.. |                         | (:const:`DEBUG`, :const:`INFO`,               |
.. |                         | :const:`WARNING`, :const:`ERROR`,             |
.. |                         | :const:`CRITICAL`).                           |
.. +-------------------------+-----------------------------------------------+
.. | ``%(levelname)s``       | Text logging level for the message            |
.. |                         | (``'DEBUG'``, ``'INFO'``, ``'WARNING'``,      |
.. |                         | ``'ERROR'``, ``'CRITICAL'``).                 |
.. +-------------------------+-----------------------------------------------+
.. | ``%(pathname)s``        | Full pathname of the source file where the    |
.. |                         | logging call was issued (if available).       |
.. +-------------------------+-----------------------------------------------+
.. | ``%(filename)s``        | Filename portion of pathname.                 |
.. +-------------------------+-----------------------------------------------+
.. | ``%(module)s``          | Module (name portion of filename).            |
.. +-------------------------+-----------------------------------------------+
.. | ``%(funcName)s``        | Name of function containing the logging call. |
.. +-------------------------+-----------------------------------------------+
.. | ``%(lineno)d``          | Source line number where the logging call was |
.. |                         | issued (if available).                        |
.. +-------------------------+-----------------------------------------------+
.. | ``%(created)f``         | Time when the :class:`LogRecord` was created  |
.. |                         | (as returned by :func:`time.time`).           |
.. +-------------------------+-----------------------------------------------+
.. | ``%(relativeCreated)d`` | Time in milliseconds when the LogRecord was   |
.. |                         | created, relative to the time the logging     |
.. |                         | module was loaded.                            |
.. +-------------------------+-----------------------------------------------+
.. | ``%(asctime)s``         | Human-readable time when the                  |
.. |                         | :class:`LogRecord` was created.  By default   |
.. |                         | this is of the form "2003-07-08 16:49:45,896" |
.. |                         | (the numbers after the comma are millisecond  |
.. |                         | portion of the time).                         |
.. +-------------------------+-----------------------------------------------+
.. | ``%(msecs)d``           | Millisecond portion of the time when the      |
.. |                         | :class:`LogRecord` was created.               |
.. +-------------------------+-----------------------------------------------+
.. | ``%(thread)d``          | Thread ID (if available).                     |
.. +-------------------------+-----------------------------------------------+
.. | ``%(threadName)s``      | Thread name (if available).                   |
.. +-------------------------+-----------------------------------------------+
.. | ``%(process)d``         | Process ID (if available).                    |
.. +-------------------------+-----------------------------------------------+
.. | ``%(message)s``         | The logged message, computed as ``msg %       |
.. |                         | args``.                                       |
.. +-------------------------+-----------------------------------------------+

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


.. .. versionchanged:: 2.5
..    *funcName* was added.

.. versionchanged:: 2.5
   *funcName* が追加されました.


.. class:: Formatter([fmt[, datefmt]])

   .. Returns a new instance of the :class:`Formatter` class. The instance is
   .. initialized with a format string for the message as a whole, as well as a format
   .. string for the date/time portion of a message. If no *fmt* is specified,
   .. ``'%(message)s'`` is used. If no *datefmt* is specified, the ISO8601 date format
   .. is used.

   :class:`Formatter` クラスの新たなインスタンスを返します。インスタンスは全体としてのメッセージに対する書式化文字列と、メッセージの
   日付/時刻部分のための書式化文字列を伴って初期化されます。 *fmt*  が指定されない場合、 ``'%(message)s'`` が使われます。
   *datefmt* が指定されない場合、ISO8601 日付書式が使われます。


   .. method:: format(record)

      .. The record's attribute dictionary is used as the operand to a string
      .. formatting operation. Returns the resulting string. Before formatting the
      .. dictionary, a couple of preparatory steps are carried out. The *message*
      .. attribute of the record is computed using *msg* % *args*. If the
      .. formatting string contains ``'(asctime)'``, :meth:`formatTime` is called
      .. to format the event time. If there is exception information, it is
      .. formatted using :meth:`formatException` and appended to the message. Note
      .. that the formatted exception information is cached in attribute
      .. *exc_text*. This is useful because the exception information can be
      .. pickled and sent across the wire, but you should be careful if you have
      .. more than one :class:`Formatter` subclass which customizes the formatting
      .. of exception information. In this case, you will have to clear the cached
      .. value after a formatter has done its formatting, so that the next
      .. formatter to handle the event doesn't use the cached value but
      .. recalculates it afresh.

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

      .. This method should be called from :meth:`format` by a formatter which
      .. wants to make use of a formatted time. This method can be overridden in
      .. formatters to provide for any specific requirement, but the basic behavior
      .. is as follows: if *datefmt* (a string) is specified, it is used with
      .. :func:`time.strftime` to format the creation time of the
      .. record. Otherwise, the ISO8601 format is used.  The resulting string is
      .. returned.

      このメソッドは、フォーマッタが書式化された時間を利用したい際に、
      :meth:`format` から呼び出されます。このメソッドは特定の要求を\
      提供するためにフォーマッタで上書きすることができますが、
      基本的な振る舞いは以下のようになります: *datefmt* (文字列) が指定された\
      場合、レコードが生成された時刻を書式化するために :func:`time.strftime`
      で使われます。そうでない場合、ISO8601 書式が使われます。結果の文字列が返されます。


   .. method:: formatException(exc_info)

      .. Formats the specified exception information (a standard exception tuple as
      .. returned by :func:`sys.exc_info`) as a string. This default implementation
      .. just uses :func:`traceback.print_exception`. The resulting string is
      .. returned.

      指定された例外情報 (:func:`sys.exc_info` が返すような標準例外のタプル)
      を文字列として書式化します。
      デフォルトの実装は単に :func:`traceback.print_exception` を使います。
      結果の文字列が返されます。


Filter オブジェクト
-------------------

.. :class:`Filter`\ s can be used by :class:`Handler`\ s and :class:`Logger`\ s for
.. more sophisticated filtering than is provided by levels. The base filter class
.. only allows events which are below a certain point in the logger hierarchy. For
.. example, a filter initialized with "A.B" will allow events logged by loggers
.. "A.B", "A.B.C", "A.B.C.D", "A.B.D" etc. but not "A.BB", "B.A.B" etc. If
.. initialized with the empty string, all events are passed.

:class:`Filter` は :class:`Handler` と :class:`Logger` によって利用され、
レベルによる制御よりも洗練されたフィルタ処理を提供します。基底のフィルタクラスでは、ロガーの階層構造のある点よりも下層にあるイベント
だけを通過させます。例えば、"A.B" で初期化されたフィルタはロガー "A.B"、 "A.B.C"、 "A.B.C.D"、 "A.B.D"
などでログ記録されたイベントを通過させます。しかし、 "A.BB"、"B.A.B" などは通過させません。
空の文字列で初期化された場合、全てのイベントを通過させます。


.. class:: Filter([name])

   .. Returns an instance of the :class:`Filter` class. If *name* is specified, it
   .. names a logger which, together with its children, will have its events allowed
   .. through the filter. If no name is specified, allows every event.

   :class:`Filter` クラスのインスタンスを返します。 *name* が指定されていれば、 *name*
   はロガーの名前を表します。指定されたロガーとその子ロガーのイベントがフィルタを通過できるようになります。
   *name* が指定されなければ、全てのイベントを通過させます。


   .. method:: filter(record)

      .. Is the specified record to be logged? Returns zero for no, nonzero for
      .. yes. If deemed appropriate, the record may be modified in-place by this
      .. method.

      指定されたレコードがログされているか？
      されていなければゼロを、されていればゼロでない値を返します。
      適切と判断されれば、このメソッドによってレコードはその場で修正されることがあります。


LogRecord オブジェクト
----------------------

.. :class:`LogRecord` instances are created every time something is logged. They
.. contain all the information pertinent to the event being logged. The main
.. information passed in is in msg and args, which are combined using msg % args to
.. create the message field of the record. The record also includes information
.. such as when the record was created, the source line where the logging call was
.. made, and any exception information to be logged.

何かをログ記録する際には常に :class:`LogRecord` インスタンスが生成されます。
インスタンスにはログ記録されることになっているイベントに関係する全ての情報が入っています。インスタンスに渡される主要な情報は  *msg* および
*args* で、これらは msg % args を使って組み合わせられ、レコードのメッセージフィールドを生成します。
レコードはまた、レコードがいつ生成されたか、ログ記録がソースコード行のどこで呼び出されたか、あるいはログ記録すべき何らかの例外情報
といった情報も含んでいます。


.. class:: LogRecord(name, lvl, pathname, lineno, msg, args, exc_info [, func])

   .. Returns an instance of :class:`LogRecord` initialized with interesting
   .. information. The *name* is the logger name; *lvl* is the numeric level;
   .. *pathname* is the absolute pathname of the source file in which the logging
   .. call was made; *lineno* is the line number in that file where the logging
   .. call is found; *msg* is the user-supplied message (a format string); *args*
   .. is the tuple which, together with *msg*, makes up the user message; and
   .. *exc_info* is the exception tuple obtained by calling :func:`sys.exc_info`
   .. (or :const:`None`, if no exception information is available). The *func* is
   .. the name of the function from which the logging call was made. If not
   .. specified, it defaults to ``None``.

   関係のある情報とともに初期化された :class:`LogRecord` のインスタンスを返します。 *name* はロガーの名前です; *lvl*
   は数字で表されたレベルです; *pathname* はログ記録呼び出しが見つかったソースファイルの絶対パス名です。 *msg* はユーザ定義のメッセージ
   (書式化文字列) です; *args* はタプルで、 *msg* と合わせて、ユーザメッセージを生成します; *exc_info* は例外情報のタプルで、
   :func:`sys.exc_info` を呼び出して得られたもの (または、例外情報が取得できない場合には :const:`None`) です。
   *func* は logging 呼び出しを行った関数の名前です。
   指定されなければデフォルトは ``None`` です。


   .. .. versionchanged:: 2.5
   ..    *func* was added.

   .. versionchanged:: 2.5
      *func* が追加されました。


   .. method:: getMessage()

      .. Returns the message for this :class:`LogRecord` instance after merging any
      .. user-supplied arguments with the message.

      ユーザが供給した引数をメッセージに交ぜた後、この :class:`LogRecord` インスタンスへのメッセージを返します。


LoggerAdapter オブジェクト
--------------------------

.. versionadded:: 2.6


.. :class:`LoggerAdapter` instances are used to conveniently pass contextual
.. information into logging calls. For a usage example , see the section on
.. `adding contextual information to your logging output`__.

:class:`LoggerAdapter` インスタンスは文脈情報をログ記録呼び出しに渡すのを簡単にするために使われます。
使い方の例は `文脈情報をログ記録出力に付加する`__ を参照して下さい。


__ context-info_


.. class:: LoggerAdapter(logger, extra)

   .. Returns an instance of :class:`LoggerAdapter` initialized with an
   .. underlying :class:`Logger` instance and a dict-like object.

   内部で使う :class:`Logger` インスタンスと辞書風オブジェクトで初期化した
   :class:`LoggerAdapter` のインスタンスを返します。


   .. method:: process(meg, kwargs)

      .. Modifies the message and/or keyword arguments passed to a logging call in
      .. order to insert contextual information. This implementation takes the object
      .. passed as *extra* to the constructor and adds it to *kwargs* using key
      .. 'extra'. The return value is a (*msg*, *kwargs*) tuple which has the
      .. (possibly modified) versions of the arguments passed in.

      文脈情報を挿入するために、ログ記録呼び出しに渡されたメッセージおよび/またはキーワード引数に変更を加えます。
      ここでの実装は *extra* としてコンストラクタに渡されたオブジェクトを取り、
      'extra' キーを使って *kwargs* に加えます。
      返値は (*msg*, *kwargs*) というタプルで、
      (変更されているはずの) 渡された引数を含みます。


.. In addition to the above, :class:`LoggerAdapter` supports all the logging
.. methods of :class:`Logger`, i.e. :meth:`debug`, :meth:`info`, :meth:`warning`,
.. :meth:`error`, :meth:`exception`, :meth:`critical` and :meth:`log`. These
.. methods have the same signatures as their counterparts in :class:`Logger`, so
.. you can use the two types of instances interchangeably.

上のメソッドに加えて、 :class:`LoggerAdapter` は :class:`Logger` にある全てのログ記録メソッド、すなわち
:meth:`debug`, :meth:`info`, :meth:`warning`,
:meth:`error`, :meth:`exception`, :meth:`critical`, :meth:`log`
をサポートします。
これらのメソッドは対応する :class:`Logger` のメソッドと同じ引数を取りますので、
二つの型を取り替えて使うことができます。


スレッド安全性
--------------

.. The logging module is intended to be thread-safe without any special work
.. needing to be done by its clients. It achieves this though using threading
.. locks; there is one lock to serialize access to the module's shared data, and
.. each handler also creates a lock to serialize access to its underlying I/O.

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

.. The following functions configure the logging module. They are located in the
.. :mod:`logging.config` module.  Their use is optional --- you can configure the
.. logging module using these functions or by making calls to the main API (defined
.. in :mod:`logging` itself) and defining handlers which are declared either in
.. :mod:`logging` or :mod:`logging.handlers`.

以下の関数で :mod:`logging` モジュールの環境設定をします。これらの関数は、 :mod:`logging.config` にあります。
これらの関数の使用はオプションです ---  :mod:`logging` モジュールはこれらの関数を使うか、 (:mod:`logging` 自体で
定義されている) 主要な API を呼び出し、 :mod:`logging` か :mod:`logging.handlers`
で宣言されているハンドラを定義することで設定することができます。


.. function:: fileConfig(fname[, defaults])

   .. Reads the logging configuration from a ConfigParser-format file named *fname*.
   .. This function can be called several times from an application, allowing an end
   .. user the ability to select from various pre-canned configurations (if the
   .. developer provides a mechanism to present the choices and load the chosen
   .. configuration). Defaults to be passed to ConfigParser can be specified in the
   .. *defaults* argument.

   ログ記録の環境設定をファイル名 *fname* の ConfigParser 形式ファイルから読み出します。この関数はアプリケーションから何度も呼び出すことが
   でき、これによって、(設定の選択と、選択された設定を読み出す機構をデベロッパが提供していれば) 複数のお仕着せの設定からエンドユーザが
   選択するようにできます。ConfigParser に渡すためのデフォルト値は *defaults* 引数で指定できます。


.. function:: listen([port])

   .. Starts up a socket server on the specified port, and listens for new
   .. configurations. If no port is specified, the module's default
   .. :const:`DEFAULT_LOGGING_CONFIG_PORT` is used. Logging configurations will be
   .. sent as a file suitable for processing by :func:`fileConfig`. Returns a
   .. :class:`Thread` instance on which you can call :meth:`start` to start the
   .. server, and which you can :meth:`join` when appropriate. To stop the server,
   .. call :func:`stopListening`.

   指定されたポートでソケットサーバを開始し、新たな設定を待ち受け (listen) ます。ポートが指定されなければ、モジュールのデフォルト設定である
   :const:`DEFAULT_LOGGING_CONFIG_PORT` が使われます。ログ記録の環境設定は :func:`fileConfig`
   で処理できるようなファイルとして送信されます。 :class:`Thread` インスタンスを返し、サーバを開始するために :meth:`start`
   を呼び、適切な状況で :meth:`join` を呼び出すことができます。サーバを停止するには :func:`stopListening` を呼んでください。


   .. To send a configuration to the socket, read in the configuration file and
   .. send it to the socket as a string of bytes preceded by a four-byte length
   .. string packed in binary using ``struct.pack('>L', n)``.

   設定を送るには、まず設定ファイルを読み、それを4バイトからなる長さを
   ``struct.pack('>L', n)`` を使ってバイナリにパックしたものを\
   前に付けたバイト列としてソケットに送ります。


.. function:: stopListening()

   .. Stops the listening server which was created with a call to :func:`listen`.
   .. This is typically called before calling :meth:`join` on the return value from
   .. :func:`listen`.

   :func:`listen` を呼び出して作成された、待ち受け中のサーバを停止します。通常 :func:`listen` の戻り値に対して
   :meth:`join` が呼ばれる前に呼び出します。


.. _logging-config-fileformat:

環境設定ファイルの書式
^^^^^^^^^^^^^^^^^^^^^^

.. The configuration file format understood by :func:`fileConfig` is based on
.. ConfigParser functionality. The file must contain sections called ``[loggers]``,
.. ``[handlers]`` and ``[formatters]`` which identify by name the entities of each
.. type which are defined in the file. For each such entity, there is a separate
.. section which identified how that entity is configured. Thus, for a logger named
.. ``log01`` in the ``[loggers]`` section, the relevant configuration details are
.. held in a section ``[logger_log01]``. Similarly, a handler called ``hand01`` in
.. the ``[handlers]`` section will have its configuration held in a section called
.. ``[handler_hand01]``, while a formatter called ``form01`` in the
.. ``[formatters]`` section will have its configuration specified in a section
.. called ``[formatter_form01]``. The root logger configuration must be specified
.. in a section called ``[logger_root]``.

:func:`fileConfig` が解釈できる環境設定ファイルの形式は、 ConfigParser の機能に基づいています。
ファイルには、 ``[loggers]`` 、 ``[handlers]`` 、および ``[formatters]`` といったセクションが入っていなければならず、
各セクションではファイル中で定義されている各タイプのエンティティを名前で指定しています。こうしたエンティティの各々について、
そのエンティティをどう設定するかを示した個別のセクションがあります。すなわち、 ``log01`` という名前の ``[loggers]`` セクションにある
ロガーに対しては、対応する詳細設定がセクション ``[logger_log01]`` に収められています。同様に、 ``hand01`` という名前の
``[handlers]`` セクションにあるハンドラは ``[handler_hand01]``
と呼ばれるセクションに設定をもつことになり、 ``[formatters]``  セクションにある ``form01`` は
``[formatter_form01]`` というセクションで設定が指定されています。ルートロガーの設定は ``[logger_root]``
と呼ばれるセクションで指定されていなければなりません。


.. Examples of these sections in the file are given below.

ファイルにおけるこれらのセクションの例を以下に示します。


::

   [loggers]
   keys=root,log02,log03,log04,log05,log06,log07

   [handlers]
   keys=hand01,hand02,hand03,hand04,hand05,hand06,hand07,hand08,hand09

   [formatters]
   keys=form01,form02,form03,form04,form05,form06,form07,form08,form09


.. The root logger must specify a level and a list of handlers. An example of a
.. root logger section is given below.

ルートロガーでは、レベルとハンドラのリストを指定しなければなりません。ルートロガーのセクションの例を以下に示します。


::

   [logger_root]
   level=NOTSET
   handlers=hand01


.. The ``level`` entry can be one of ``DEBUG, INFO, WARNING, ERROR, CRITICAL`` or
.. ``NOTSET``. For the root logger only, ``NOTSET`` means that all messages will be
.. logged. Level values are :func:`eval`\ uated in the context of the ``logging``
.. package's namespace.

``level`` エントリは ``DEBUG, INFO, WARNING, ERROR, CRITICAL`` のうちの一つか、 ``NOTSET``
になります。ルートロガーの場合にのみ、 ``NOTSET`` は全てのメッセージがログ記録されることを意味します。レベル値は ``logging``
パッケージの名前空間のコンテキストにおいて :func:`eval` されます。


.. The ``handlers`` entry is a comma-separated list of handler names, which must
.. appear in the ``[handlers]`` section. These names must appear in the
.. ``[handlers]`` section and have corresponding sections in the configuration
.. file.

``handlers`` エントリはコンマで区切られたハンドラ名からなるリストで、 ``[handlers]`` セクションになくてはなりません。
また、これらの各ハンドラの名前に対応するセクションが設定ファイルに存在しなければなりません。


.. For loggers other than the root logger, some additional information is required.
.. This is illustrated by the following example.

ルートロガー以外のロガーでは、いくつか追加の情報が必要になります。これは以下の例のように表されます。


::

   [logger_parser]
   level=DEBUG
   handlers=hand01
   propagate=1
   qualname=compiler.parser


.. The ``level`` and ``handlers`` entries are interpreted as for the root logger,
.. except that if a non-root logger's level is specified as ``NOTSET``, the system
.. consults loggers higher up the hierarchy to determine the effective level of the
.. logger. The ``propagate`` entry is set to 1 to indicate that messages must
.. propagate to handlers higher up the logger hierarchy from this logger, or 0 to
.. indicate that messages are **not** propagated to handlers up the hierarchy. The
.. ``qualname`` entry is the hierarchical channel name of the logger, that is to
.. say the name used by the application to get the logger.

``level`` および ``handlers`` エントリはルートロガーのエントリと同様に解釈されますが、非ルートロガーのレベルが ``NOTSET``
に指定された場合、ログ記録システムはロガー階層のより上位のロガーにロガーの実効レベルを問い合わせるところが違います。 ``propagate``
エントリは、メッセージをロガー階層におけるこのロガーの上位のハンドラに伝播させることを示す 1 に設定されるか、メッセージを階層の上位に伝播 **しない**
ことを示す 0 に設定されます。 ``qualname`` エントリはロガーのチャネル名を階層的に表した
もの、すなわちアプリケーションがこのロガーを取得する際に使う名前になります。


.. Sections which specify handler configuration are exemplified by the following.

ハンドラの環境設定を指定しているセクションは以下の例のようになります。


::

   [handler_hand01]
   class=StreamHandler
   level=NOTSET
   formatter=form01
   args=(sys.stdout,)


.. The ``class`` entry indicates the handler's class (as determined by :func:`eval`
.. in the ``logging`` package's namespace). The ``level`` is interpreted as for
.. loggers, and ``NOTSET`` is taken to mean "log everything".

``class`` エントリはハンドラのクラス (``logging`` パッケージの名前空間において :func:`eval` で決定されます)
を示します。 ``level`` はロガーの場合と同じように解釈され、 ``NOTSET``  は "全てを記録する (log everything)"
と解釈されます。


.. .. versionchanged:: 2.6
..   Added support for resolving the handler's class as a dotted module and class
..   name.

.. versionchanged:: 2.6
   ハンドラクラスのドット区切りモジュールおよびクラス名としての解決のサポートが追加された。


.. The ``formatter`` entry indicates the key name of the formatter for this
.. handler. If blank, a default formatter (``logging._defaultFormatter``) is used.
.. If a name is specified, it must appear in the ``[formatters]`` section and have
.. a corresponding section in the configuration file.

``formatter`` エントリはこのハンドラのフォーマッタに対するキー名を表します。空文字列の場合、デフォルトのフォーマッタ
(``logging._defaultFormatter``) が使われます。名前が指定されている場合、その名前は ``[formatters]``
セクションになくてはならず、対応するセクションが設定ファイル中になければなりません。


.. The ``args`` entry, when :func:`eval`\ uated in the context of the ``logging``
.. package's namespace, is the list of arguments to the constructor for the handler
.. class. Refer to the constructors for the relevant handlers, or to the examples
.. below, to see how typical entries are constructed.

``args`` エントリは、 ``logging`` パッケージの名前空間のコンテキストで :func:`eval` される際、ハンドラクラスの
コンストラクタに対する引数からなるリストになります。
典型的なエントリがどうやって作成されるかについては、対応するハンドラのコンストラクタか、以下の例を参照してください。


::

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


.. Sections which specify formatter configuration are typified by the following.

フォーマッタの環境設定を指定しているセクションは以下のような形式です。


::

   [formatter_form01]
   format=F1 %(asctime)s %(levelname)s %(message)s
   datefmt=
   class=logging.Formatter


.. The ``format`` entry is the overall format string, and the ``datefmt`` entry is
.. the :func:`strftime`\ -compatible date/time format string.  If empty, the
.. package substitutes ISO8601 format date/times, which is almost equivalent to
.. specifying the date format string ``"%Y-%m-%d %H:%M:%S"``.  The ISO8601 format
.. also specifies milliseconds, which are appended to the result of using the above
.. format string, with a comma separator.  An example time in ISO8601 format is
.. ``2003-01-23 00:29:50,411``.

``format`` エントリは全体を書式化する文字列で、 ``datefmt``  エントリは :func:`strftime`
互換の日付/時刻書式化文字列です。空文字列の場合、パッケージによって ISO8601 形式の日付/時刻に置き換えられ、日付書式化文字列 ``"%Y-%m-%d %H:%M:%S"`` を指定した場合とほとんど同じになります。
ISO8601 形式ではミリ秒も指定しており、上の書式化文字列の結果にカンマで区切って追加されます。ISO8601 形式の時刻の例は ``2003-01-23
00:29:50,411`` です。


.. The ``class`` entry is optional.  It indicates the name of the formatter's class
.. (as a dotted module and class name.)  This option is useful for instantiating a
.. :class:`Formatter` subclass.  Subclasses of :class:`Formatter` can present
.. exception tracebacks in an expanded or condensed format.

``class`` エントリはオプションです。 ``class`` はフォーマッタのクラス名
(ドット区切りのモジュールとクラス名として)を示します。このオプションは :class:`Formatter` のサブクラスをインスタンス化するのに有用です。
:class:`Formatter` のサブクラスは例外トレースバックを展開された形式または圧縮された形式で表現することができます。


設定サーバの例
^^^^^^^^^^^^^^

.. Here is an example of a module using the logging configuration server:

ログ記録設定サーバを使うモジュールの例です。


::

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


.. And here is a script that takes a filename and sends that file to the server,
.. properly preceded with the binary-encoded length, as the new logging
.. configuration:

そしてファイル名を受け取ってそのファイルをサーバに送るスクリプトですが、
それに先だってバイナリエンコード長を新しいログ記録の設定として先に送っておきます:


::

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

.. Loggers are plain Python objects.  The :func:`addHandler` method has no minimum
.. or maximum quota for the number of handlers you may add.  Sometimes it will be
.. beneficial for an application to log all messages of all severities to a text
.. file while simultaneously logging errors or above to the console.  To set this
.. up, simply configure the appropriate handlers.  The logging calls in the
.. application code will remain unchanged.  Here is a slight modification to the
.. previous simple module-based configuration example:

ロガーは通常の Python オブジェクトです。
:func:`addHandler` メソッドには追加されるハンドラの個数について最少数も最多数も定めていません。
時にアプリケーションが全ての深刻さの全てのメッセージをテキストファイルに記録しつつ、
同時にエラーやそれ以上のものをコンソールに出力することが役に立ちます。
これを実現する方法は、単に適切なハンドラを設定するだけです。
アプリケーションコードの中のログ記録の呼び出しは変更されずに残ります。
少し前に取り上げた単純なモジュール式の例を少し変えるとこうなります:


::

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


.. Notice that the "application" code does not care about multiple handlers.  All
.. that changed was the addition and configuration of a new handler named *fh*.

「アプリケーション」のコードは複数のハンドラについて何も気にしていないことに注目して下さい。
変更した箇所は新しい *fh* という名のハンドラを追加して設定したところが全てです。


.. The ability to create new handlers with higher- or lower-severity filters can be
.. very helpful when writing and testing an application.  Instead of using many
.. ``print`` statements for debugging, use ``logger.debug``: Unlike the print
.. statements, which you will have to delete or comment out later, the logger.debug
.. statements can remain intact in the source code and remain dormant until you
.. need them again.  At that time, the only change that needs to happen is to
.. modify the severity level of the logger and/or handler to debug.

新しいハンドラを高い(もしくは低い)深刻さに対するフィルタを具えて生成できることは、
アプリケーションを書いてテストを行うときとても助けになります。
デバッグ用にたくさんの ``print`` 文を使う代わりに ``logger.debug`` を使いましょう。
あとで消したりコメントアウトしたりしなければならない print 文と違って、
logger.debug 命令はソースコードの中にそのまま残しておいて再び必要になるまで休眠させておけます。
その時必要になるのはただロガーおよび/またはハンドラの深刻さの設定をいじることだけです。


複数のモジュールで logging を使う
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. It was mentioned above that multiple calls to
.. ``logging.getLogger('someLogger')`` return a reference to the same logger
.. object.  This is true not only within the same module, but also across modules
.. as long as it is in the same Python interpreter process.  It is true for
.. references to the same object; additionally, application code can define and
.. configure a parent logger in one module and create (but not configure) a child
.. logger in a separate module, and all logger calls to the child will pass up to
.. the parent.  Here is a main module:

上で述べたように ``logging.getLogger('someLogger')`` の複数回の呼び出しは同じロガーへの参照を返します。
これは一つのモジュールの中からに限らず、同じ Python インタプリタプロセス乗で動いている限りはモジュールをまたいでも正しいのです。
同じオブジェクトへの参照という点でも正しいです。
さらに、一つのモジュールの中で親ロガーを定義して設定し、別のモジュールで子ロガーを定義する(ただし設定はしない)ことが可能で、全ての子ロガーへの呼び出しは親にまで渡されます。
まずはメインのモジュールです:


::

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


.. Here is the auxiliary module:

そして補助モジュール(auxiliary_module)がこちらです:


::

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


.. The output looks like this:

出力はこのようになります:


::

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
