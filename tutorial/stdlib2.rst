.. _tut-brieftourtwo:

**********************************
標準ライブラリミニツアー -- その 2
**********************************

もう一つのツアーでは、プロフェッショナルプログラミングを支えるもっと高度なモジュールをカバーします。ここで挙げるモジュールは、
小さなスクリプトの開発ではほとんど使いません。

.. % Brief Tour of the Standard Library -- Part II


.. _tut-output-formatting:

出力のフォーマット
==================

:mod:`repr` モジュールでは、
大きなコンテナや、深くネストしたコンテナを省略して表示するバージョンの :func:`repr` を提供しています:

.. % Output Formatting
.. % The \ulink{\module{repr}}{../lib/module-repr.html} module provides a
.. % version of \function{repr()} customized for abbreviated displays of large
.. % or deeply nested containers:

::

   >>> import repr
   >>> repr.repr(set('supercalifragilisticexpialidocious'))
   "set(['a', 'c', 'd', 'e', 'f', 'g', ...])"

:mod:`pprint` モジュールを使うと、
組み込み型やユーザ定義型がより洗練された形式で出力されるよう制御できます。出力が複数行にわたる場合には、"pretty printer" が改行を追加して、
入れ子構造を理解しやすいようにインデントを挿入します:

.. % The \ulink{\module{pprint}}{../lib/module-pprint.html} module offers
.. % more sophisticated control over printing both built-in and user defined
.. % objects in a way that is readable by the interpreter.  When the result
.. % is longer than one line, the ``pretty printer'' adds line breaks and
.. % indentation to more clearly reveal data structure:

::

   >>> import pprint
   >>> t = [[[['black', 'cyan'], 'white', ['green', 'red']], [['magenta',
   ...     'yellow'], 'blue']]]
   ...
   >>> pprint.pprint(t, width=30)
   [[[['black', 'cyan'],
      'white',
      ['green', 'red']],
     [['magenta', 'yellow'],
      'blue']]]

:mod:`textwrap` モジュールは、
一段落の文を指定したスクリーン幅にぴったり収まるように調整します:

.. % The \ulink{\module{textwrap}}{../lib/module-textwrap.html} module
.. % formats paragraphs of text to fit a given screen width:

::

   >>> import textwrap
   >>> doc = """The wrap() method is just like fill() except that it returns
   ... a list of strings instead of one big string with newlines to separate
   ... the wrapped lines."""
   ...
   >>> print textwrap.fill(doc, width=40)
   The wrap() method is just like fill()
   except that it returns a list of strings
   instead of one big string with newlines
   to separate the wrapped lines.

:mod:`locale` モジュールは、文化ごと
に特化したデータ表現形式のデータベースにアクセスします。 :mod:`locale` の :func:`format` 関数の grouping
属性を使えば、数値の各桁を適切な区切り文字でグループ化してフォーマットできます:

.. % The \ulink{\module{locale}}{../lib/module-locale.html} module accesses
.. % a database of culture specific data formats.  The grouping attribute
.. % of locale's format function provides a direct way of formatting numbers
.. % with group separators:

::

   >>> import locale
   >>> locale.setlocale(locale.LC_ALL, 'English_United States.1252')
   'English_United States.1252'
   >>> conv = locale.localeconv()          # get a mapping of conventions
   >>> x = 1234567.8
   >>> locale.format("%d", x, grouping=True)
   '1,234,567'
   >>> locale.format("%s%.*f", (conv['currency_symbol'],
   ...               conv['frac_digits'], x), grouping=True)
   '$1,234,567.80'


.. _tut-templating:

文字列テンプレート
==================

:mod:`string` モジュールには、
柔軟で、エンドユーザが簡単に編集できる簡単な構文を備えた :class:`Template`
クラスが入っています。このクラスを使うと、ユーザがアプリケーションの出力をカスタマイズしたいときに全てを置き換えなくてもすみます。

.. % Templating
.. % The \ulink{\module{string}}{../lib/module-string.html} module includes a
.. % versatile \class{Template} class with a simplified syntax suitable for
.. % editing by end-users.  This allows users to customize their applications
.. % without having to alter the application.

テンプレートでは、 ``$`` と有効な Python 識別子名 (英数字とアンダースコア) からなるプレースホルダ名を使います。プレースホルダの
周りを丸括弧で囲えば、間にスペースをはさまなくても後ろに英数文字を続けられます。 ``$$`` のようにすると、 ``$`` 自体をエスケープできます:

.. % The format uses placeholder names formed by \samp{\$} with valid Python
.. % identifiers (alphanumeric characters and underscores).  Surrounding the
.. % placeholder with braces allows it to be followed by more alphanumeric letters
.. % with no intervening spaces.  Writing \samp{\$\$} creates a single escaped
.. % \samp{\$}:

::

   >>> from string import Template
   >>> t = Template('${village}folk send $$10 to $cause.')
   >>> t.substitute(village='Nottingham', cause='the ditch fund')
   'Nottinghamfolk send $10 to the ditch fund.'

:meth:`substitute` メソッドは、プレースホルダに相当する値が辞書やキーワード引数にない場合に :exc:`KeyError` を送出します。
メールマージ型アプリケーションの場合、ユーザが入力するデータは不完全なことがあるので、欠落したデータがあるとプレースホルダをそのままにして出力する
:meth:`safe_substitute` メソッドを使う方が適切でしょう:

.. % The \method{substitute} method raises a \exception{KeyError} when a
.. % placeholder is not supplied in a dictionary or a keyword argument. For
.. % mail-merge style applications, user supplied data may be incomplete and the
.. % \method{safe_substitute} method may be more appropriate --- it will leave
.. % placeholders unchanged if data is missing:

::

   >>> t = Template('Return the $item to $owner.')
   >>> d = dict(item='unladen swallow')
   >>> t.substitute(d)
   Traceback (most recent call last):
     . . .
   KeyError: 'owner'
   >>> t.safe_substitute(d)
   'Return the unladen swallow to $owner.'

:class:`Template` をサブクラス化すると、区切り文字を自作できます。例えば、
画像ブラウザ用にバッチで名前を変更するユーティリティを作っていたとして、現在の日付や画像のシーケンス番号、ファイル形式といったプレースホルダに
パーセント記号を選んだとします:

.. % Template subclasses can specify a custom delimiter.  For example, a batch
.. % renaming utility for a photo browser may elect to use percent signs for
.. % placeholders such as the current date, image sequence number, or file format:

::

   >>> import time, os.path
   >>> photofiles = ['img_1074.jpg', 'img_1076.jpg', 'img_1077.jpg']
   >>> class BatchRename(Template):
   ...     delimiter = '%'
   >>> fmt = raw_input('Enter rename style (%d-date %n-seqnum %f-format):  ')
   Enter rename style (%d-date %n-seqnum %f-format):  Ashley_%n%f

   >>> t = BatchRename(fmt)
   >>> date = time.strftime('%d%b%y')
   >>> for i, filename in enumerate(photofiles):
   ...     base, ext = os.path.splitext(filename)
   ...     newname = t.substitute(d=date, n=i, f=ext)
   ...     print '{0} --> {1}'.format(filename, newname)

   img_1074.jpg --> Ashley_0.jpg
   img_1076.jpg --> Ashley_1.jpg
   img_1077.jpg --> Ashley_2.jpg

テンプレートのもう一つの用途は、複数ある出力様式からのプログラムロジックの分離です。テンプレートを使えば、カスタムのテンプレートを XML ファイル
用や平文テキストのレポート、 HTML で書かれた web レポート用などに置き換えられます。

.. % Another application for templating is separating program logic from the
.. % details of multiple output formats.  This makes it possible to substitute
.. % custom templates for XML files, plain text reports, and HMTL web reports.


.. _tut-binary-formats:

バイナリデータレコードの操作
============================

+The :mod:`struct` module provides :func:`pack` and :func:`unpack` functions for
+working with variable length binary record formats.  The following example shows
+how to loop through header information in a ZIP file without using the
+:mod:`zipfile` module.  Pack codes ``"H"`` and ``"I"`` represent two and four
+byte unsigned numbers respectively.  The ``"<"`` indicates that they are
+standard size and in little-endian byte order

:mod:`struct` モジュールでは、
可変長のバイナリレコード形式を操作する :func:`pack` や  :func:`unpack` といった関数を提供しています。
以下の例では、  :mod:`zipfile` モジュールを使わずに、ZIPファイルのヘッダ情報を巡回する方法を示しています
``"H"``  と ``"I"`` というパック符号は、それぞれ2バイトと4バイトの符号無し整数を表しています。
``"<"`` は、そのパック符号が通常のサイズであり、バイトオーダーがリトルエンディアンであることを示しています。

::

   import struct

   data = open('myfile.zip', 'rb').read()
   start = 0
   for i in range(3):                      # show the first 3 file headers
       start += 14
       fields = struct.unpack('<IIIHH', data[start:start+16])
       crc32, comp_size, uncomp_size, filenamesize, extra_size = fields

       start += 16
       filename = data[start:start+filenamesize]
       start += filenamesize
       extra = data[start:start+extra_size]
       print filename, hex(crc32), comp_size, uncomp_size

       start += extra_size + comp_size     # skip to the next header


.. _tut-multi-threading:

マルチスレッド処理
==================

スレッド処理 (threading) とは、順序的な依存関係にない複数のタスクを分割するテクニックです。スレッド処理は、ユーザの入力を受け付けつつ、
背後で別のタスクを動かすようなアプリケーションの応答性を高めます。主なユースケースには、 I/O を別のスレッドの計算処理と並列して
動作させるというものがあります。

.. % Multi-threading
.. % Threading is a technique for decoupling tasks which are not sequentially
.. % dependent.  Threads can be used to improve the responsiveness of
.. % applications that accept user input while other tasks run in the
.. % background.  A related use case is running I/O in parallel with
.. % computations in another thread.

以下のコードでは、高水準のモジュール :mod:`threading`
でメインのプログラムを動かしながら背後で別のタスクを動作させられるようにする方法を示しています:

.. % The following code shows how the high level
.. % \ulink{\module{threading}}{../lib/module-threading.html} module can run
.. % tasks in background while the main program continues to run:

::

   import threading, zipfile

   class AsyncZip(threading.Thread):
       def __init__(self, infile, outfile):
           threading.Thread.__init__(self)
           self.infile = infile
           self.outfile = outfile
       def run(self):
           f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
           f.write(self.infile)
           f.close()
           print 'Finished background zip of: ', self.infile

   background = AsyncZip('mydata.txt', 'myarchive.zip')
   background.start()
   print 'The main program continues to run in foreground.'

   background.join()    # Wait for the background task to finish
   print 'Main program waited until background was done.'

マルチスレッドアプリケーションを作る上で最も難しい問題は、データやリソースを共有するスレッド間の調整 (coordination)
です。この問題を解決するため、 :mod:`threading` モジュールではロックやイベント、状態変数、セマフォ
といった数々の同期プリミティブを提供しています。

.. % The principal challenge of multi-threaded applications is coordinating
.. % threads that share data or other resources.  To that end, the threading
.. % module provides a number of synchronization primitives including locks,
.. % events, condition variables, and semaphores.

こうしたツールは強力な一方、ちょっとした設計上の欠陥で再現困難な問題を引き起こすことがあります。
したがって、タスク間調整では :mod:`Queue`
モジュールを使って他のスレッドから一つのスレッドにリクエストを送り込み、
一つのリソースへのアクセスをできるだけ一つのスレッドに集中させるアプローチを勧めます。
スレッド間の通信や調整に :class:`Queue.Queue`
オブジェクトを使うと、設計が容易になり、可読性が高まり、信頼性が増します。

.. % While those tools are powerful, minor design errors can result in
.. % problems that are difficult to reproduce.  So, the preferred approach
.. % to task coordination is to concentrate all access to a resource
.. % in a single thread and then use the
.. % \ulink{\module{Queue}}{../lib/module-Queue.html} module to feed that
.. % thread with requests from other threads.  Applications using
.. % \class{Queue} objects for inter-thread communication and coordination
.. % are easier to design, more readable, and more reliable.


.. _tut-logging:

ログ記録
========

:mod:`logging` モジュールでは、
数多くの機能をそなえた柔軟性のあるログ記録システムを提供しています。最も簡単な使い方では、ログメッセージをファイルや ``sys.stderr``
に送信します:

.. % Logging
.. % The \ulink{\module{logging}}{../lib/module-logging.html} module offers
.. % a full featured and flexible logging system.  At its simplest, log
.. % messages are sent to a file or to \code{sys.stderr}:

::

   import logging
   logging.debug('Debugging information')
   logging.info('Informational message')
   logging.warning('Warning:config file %s not found', 'server.conf')
   logging.error('Error occurred')
   logging.critical('Critical error -- shutting down')

上記のコードは以下のような出力になります::

   WARNING:root:Warning:config file server.conf not found
   ERROR:root:Error occurred
   CRITICAL:root:Critical error -- shutting down

デフォルトでは、単なる情報やデバッグメッセージの出力は抑制され、出力は標準エラーに送信されます。選択可能な送信先には、email、データグラム、ソケット、
HTTP サーバへの送信などがあります。新たにフィルタを作成すると、 :const:`DEBUG`, :const:`INFO`,
:const:`WARNING`,  :const:`ERROR`, :const:`CRITICAL` といったメッセージのプライオリティに
従って配送先を変更できます。

.. % By default, informational and debugging messages are suppressed and the
.. % output is sent to standard error.  Other output options include routing
.. % messages through email, datagrams, sockets, or to an HTTP Server.  New
.. % filters can select different routing based on message priority:
.. % \constant{DEBUG}, \constant{INFO}, \constant{WARNING}, \constant{ERROR},
.. % and \constant{CRITICAL}.

ログ記録システムは Python から直接設定できますし、アプリケーションを変更しなくてもカスタマイズできるよう、ユーザが編集できる設定ファイル
でも設定できます。

.. % The logging system can be configured directly from Python or can be
.. % loaded from a user editable configuration file for customized logging
.. % without altering the application.


.. _tut-weak-references:

弱参照
======

Python は自動的にメモリを管理します (ほとんどのオブジェクトは参照カウント方式で管理し、
ガベージコレクション(:term:`garbage collection`)で循環参照を除去します)。
オブジェクトに対する最後の参照がなくなってしばらくするとメモリは解放されます。

.. % Weak References

このようなアプローチはほとんどのアプリケーションでうまく動作しますが、
中にはオブジェクトをどこか別の場所で利用するまでの間だけ追跡しておきたい場合もあります。
残念ながら、オブジェクトを追跡するだけでオブジェクトに対する恒久的な参照を作ることになってしまいます。
:mod:`weakref` モジュールでは、オブジェクトへの参照を作らずに追跡するためのツールを提供しています。
弱参照オブジェクトが不要になると、弱参照 (weakref) テーブルから自動的に除去され、
コールバック関数がトリガされます。弱参照を使う典型的な応用例には、作成コストの大きいオブジェクトのキャッシュがあります::

   >>> import weakref, gc
   >>> class A:
   ...     def __init__(self, value):
   ...             self.value = value
   ...     def __repr__(self):
   ...             return str(self.value)
   ...
   >>> a = A(10)                   # create a reference
   >>> d = weakref.WeakValueDictionary()
   >>> d['primary'] = a            # does not create a reference
   >>> d['primary']                # fetch the object if it is still alive
   10
   >>> del a                       # remove the one reference
   >>> gc.collect()                # run garbage collection right away
   0
   >>> d['primary']                # entry was automatically removed
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       d['primary']                # entry was automatically removed
     File "C:/python26/lib/weakref.py", line 46, in __getitem__
       o = self.data[key]()
   KeyError: 'primary'


.. _tut-list-tools:

リスト操作のためのツール
========================

多くのデータ構造は、組み込みリスト型を使った実装で事足ります。とはいえ、時には組み込みリストとは違うパフォーマンス上のトレードオフを
持つような実装が必要になこともあります。

.. % Tools for Working with Lists
.. % Many data structure needs can be met with the built-in list type.
.. % However, sometimes there is a need for alternative implementations
.. % with different performance trade-offs.

:mod:`array` モジュールでは、
同じ形式のデータだけをコンパクトに保存できる、リスト型に似た :class:`array()` オブジェクトを提供しています。
以下の例では、通常要素あたり
16 バイトを必要とする Python 整数型のリストの代りに、 2 バイトの符号無しの 2 進数 (タイプコード ``"H"``)
を使っている数値配列を示します:

.. % The \ulink{\module{array}}{../lib/module-array.html} module provides an
.. % \class{array()} object that is like a list that stores only homogenous
.. % data and stores it more compactly.  The following example shows an array
.. % of numbers stored as two byte unsigned binary numbers (typecode
.. % \code{"H"}) rather than the usual 16 bytes per entry for regular lists
.. % of python int objects:

::

   >>> from array import array
   >>> a = array('H', [4000, 10, 700, 22222])
   >>> sum(a)
   26932
   >>> a[1:3]
   array('H', [10, 700])

:mod:`collections` モジュールでは、
リスト型に似た :class:`deque()` オブジェクトを提供しています。 :class:`deque()`
オブジェクトでは、データの追加と左端からの取り出しが高速な半面、中間にある値の検索が低速になります。
こうしたオブジェクトはキューの実装や幅優先(breadth first)のツリー探索に向いています:

.. % The \ulink{\module{collections}}{../lib/module-collections.html} module
.. % provides a \class{deque()} object that is like a list with faster
.. % appends and pops from the left side but slower lookups in the middle.
.. % These objects are well suited for implementing queues and breadth first
.. % tree searches:

::

   >>> from collections import deque
   >>> d = deque(["task1", "task2", "task3"])
   >>> d.append("task4")
   >>> print "Handling", d.popleft()
   Handling task1

   unsearched = deque([starting_node])
   def breadth_first_search(unsearched):
       node = unsearched.popleft()
       for m in gen_moves(node):
           if is_goal(m):
               return m
           unsearched.append(m)

リストの代わりの実装以外にも、標準ライブラリにはソート済みのリストを操作するための関数を備えた :mod:`bisect`
のようなツールも提供しています:

.. % In addition to alternative list implementations, the library also offers
.. % other tools such as the \ulink{\module{bisect}}{../lib/module-bisect.html}
.. % module with functions for manipulating sorted lists:

::

   >>> import bisect
   >>> scores = [(100, 'perl'), (200, 'tcl'), (400, 'lua'), (500, 'python')]
   >>> bisect.insort(scores, (300, 'ruby'))
   >>> scores
   [(100, 'perl'), (200, 'tcl'), (300, 'ruby'), (400, 'lua'), (500, 'python')]

:mod:`heapq` モジュールでは、
通常のリストでヒープを実装するための関数を提供しています。ヒープでは、最も低い値をもつエントリがつねにゼロの位置に配置
されます。ヒープは、毎回リストをソートすることなく、最小の値をもつ要素に繰り返しアクセスするようなアプリケーションで便利です:

.. % The \ulink{\module{heapq}}{../lib/module-heapq.html} module provides
.. % functions for implementing heaps based on regular lists.  The lowest
.. % valued entry is always kept at position zero.  This is useful for
.. % applications which repeatedly access the smallest element but do not
.. % want to run a full list sort:

::

   >>> from heapq import heapify, heappop, heappush
   >>> data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
   >>> heapify(data)                      # rearrange the list into heap order
   >>> heappush(data, -5)                 # add a new entry
   >>> [heappop(data) for i in range(3)]  # fetch the three smallest entries
   [-5, 0, 1]


.. _tut-decimal-fp:

10 進浮動小数演算
=================

:mod:`decimal` では、 10 進浮動小数の
算術演算をサポートする :class:`Decimal` データ型を提供しています。組み込みの 2 進浮動小数の実装である :class:`float`
に比べて、この新たなクラスがとりわけ便利なのは、厳密な 10 進表記や計算精度の制御、法的または
規制上の理由に基づく値丸めの制御、有効桁数の追跡が必要になる金融計算などのアプリケーションや、ユーザが手計算の結果と同じ演算結果を期待するような
アプリケーションの場合です。

.. % Decimal Floating Point Arithmetic
.. % The \ulink{\module{decimal}}{../lib/module-decimal.html} module offers a
.. % \class{Decimal} datatype for decimal floating point arithmetic.  Compared to
.. % the built-in \class{float} implementation of binary floating point, the new
.. % class is especially helpful for financial applications and other uses which
.. % require exact decimal representation, control over precision, control over
.. % rounding to meet legal or regulatory requirements, tracking of significant
.. % decimal places, or for applications where the user expects the results to
.. % match calculations done by hand.

例えば、 70 セントの電話代にかかる 5% の税金を計算しようとすると、 10 進の浮動小数点値と 2 進の浮動小数点値では違う結果になってしまいます。
例えば以下のような例では、計算結果を四捨五入してセント単位にしようとすると違いがはっきり現れます:

.. % For example, calculating a 5\%{} tax on a 70 cent phone charge gives
.. % different results in decimal floating point and binary floating point.
.. % The difference becomes significant if the results are rounded to the
.. % nearest cent:

::

   >>> from decimal import *
   >>> Decimal('0.70') * Decimal('1.05')
   Decimal("0.7350")
   >>> .70 * 1.05
   0.73499999999999999

:class:`Decimal` を使った計算では、末尾桁のゼロが保存されており、有効数字2桁の被乗数から自動的に有効数字を  4
桁と判断しています。 :class:`Decimal` は手計算と同じ方法で計算を行い、 2 進浮動小数点が 10 進小数成分を正確に
表現できないことによって起きる問題を回避しています。

.. % The \class{Decimal} result keeps a trailing zero, automatically inferring four
.. % place significance from multiplicands with two place significance.  Decimal reproduces
.. % mathematics as done by hand and avoids issues that can arise when binary
.. % floating point cannot exactly represent decimal quantities.

:class:`Decimal` クラスは厳密な値を表現できるため、2 進浮動小数点数では期待通りに計算できないようなモジュロの計算や等値テストも実現
できます:

.. % Exact representation enables the \class{Decimal} class to perform
.. % modulo calculations and equality tests that are unsuitable for binary
.. % floating point:

::

   >>> Decimal('1.00') % Decimal('.10')
   Decimal("0.00")
   >>> 1.00 % 0.10
   0.09999999999999995

   >>> sum([Decimal('0.1')]*10) == Decimal('1.0')
   True
   >>> sum([0.1]*10) == 1.0
   False

:mod:`decimal` モジュールを使うと、必要なだけの精度で算術演算を行えます:

.. % The \module{decimal} module provides arithmetic with as much precision as
.. % needed:

::

   >>> getcontext().prec = 36
   >>> Decimal(1) / Decimal(7)
   Decimal("0.142857142857142857142857142857142857")


