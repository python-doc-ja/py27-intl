.. _tut-brieftour:

************************
標準ライブラリミニツアー
************************


.. _tut-os-interface:

オペレーティングシステムへのインタフェース
==========================================

:mod:`os` (XXX reference: ../lib/module-os.html) モジュールは、
オペレーティングシステムと対話するための何ダースもの関数を 提供しています:

.. % % The \ulink{\module{os}}{../lib/module-os.html}
.. % % module provides dozens of functions for interacting with the
.. % % operating system:

::

   >>> import os 
   >>> os.system('time 0:02') 
   0 
   >>> os.getcwd()      # 現在の作業ディレクトリを返す
   'C:\\Python24' 
   >>> os.chdir('/server/accesslogs') 

``from os import *`` ではなく、 ``import os`` 形式を使う ようにしてください。そうすることで、
動作が大きく異なる組み込み関数 :func:`open` が :func:`os.open` で隠蔽されるのを避けられます。

.. % % Be sure to use the \samp{import os} style instead of
.. % % \samp{from os import *}.  This will keep \function{os.open()} from
.. % % shadowing the builtin \function{open()} function which operates much
.. % % differently.

.. index:: builtin: help

組み込み関数 :func:`dir` および :func:`help` は、 :mod:`os` のような大規模なモジュールで作業をするときに、対話的な
操作上の助けになります:

.. % % The builtin \function{dir()} and \function{help()} functions are useful
.. % % as interactive aids for working with large modules like \module{os}:

::

   >>> import os 
   >>> dir(os) 
   <returns a list of all module functions> 
   >>> help(os) 
   <returns an extensive manual page created from the module's docstrings> 

ファイルやディレクトリの日常的な管理作業のために、 より簡単に使える高レベルインタフェースが :mod:`shutil` (XXX reference:
../lib/module-shutil.html)  モジュールで提供されています:

.. % % For daily file and directory management tasks, the
.. % % \ulink{\module{shutil}}{../lib/module-shutil.html}
.. % % module provides a higher level interface that is easier to use:

::

   >>> import shutil 
   >>> shutil.copyfile('data.db', 'archive.db') 
   >>> shutil.move('/build/executables', 'installdir') 


.. _tut-file-wildcards:

ファイルのワイルドカード表記
============================

:mod:`glob` (XXX reference: ../lib/module-glob.html) モジュールでは、
ディレクトリのワイルドカード検索からファイルのリストを生成する ための関数を提供しています:

.. % % The \ulink{\module{glob}}{../lib/module-glob.html}
.. % % module provides a function for making file lists from directory
.. % % wildcard searches:

::

   >>> import glob 
   >>> glob.glob('*.py') 
   ['primes.py', 'random.py', 'quote.py'] 


.. _tut-command-line-arguments:

コマンドライン引数
==================

広く使われているユーティリティスクリプトでは、しばしばコマンドライン 引数の処理を呼び出します。これらの引数は :mod:`sys` (XXX
reference: ../lib/module-sys.html) モジュールの *argv*  属性にリストとして記憶されます。例えば、以下の出力は、
``python demo.py one two three`` をコマンドライン上で起動した際に 得られるものです:

.. % % Common utility scripts often need to process command line arguments.
.. % % These arguments are stored in the
.. % % \ulink{\module{sys}}{../lib/module-sys.html}\ module's \var{argv}
.. % % attribute as a list.  For instance the following output results from
.. % % running \samp{python demo.py one two three} at the command line:

::

   >>> import sys 
   >>> print sys.argv 
   ['demo.py', 'one', 'two', 'three'] 

:mod:`getopt` (XXX reference: ../lib/module-getopt.html)  モジュールは、*sys.argv* を
Unix の :func:`getopt` 関数の 慣習に従って処理します。より強力で柔軟性のあるコマンドライン処理機能は、 :mod:`optparse`
(XXX reference: ../lib/module-optparse.html) モジュールで 提供されています。

.. % % The \ulink{\module{getopt}}{../lib/module-getopt.html}
.. % % module processes \var{sys.argv} using the conventions of the \UNIX{}
.. % % \function{getopt()} function.  More powerful and flexible command line
.. % % processing is provided by the
.. % % \ulink{\module{optparse}}{../lib/module-optparse.html} module.


.. _tut-stderr:

エラー出力のリダイレクトとプログラムの終了
==========================================

:mod:`sys` (XXX reference: ../lib/module-sys.html) モジュールには、 *stdin*、
*stdout*、および *stderr* を表す属性値も 存在します。後者の *stderr* は、警告やエラーメッセージを出力して、 *stdout*
がリダイレクトされた場合でもそれらが読めるようにする 上で便利です:

.. % % The \ulink{\module{sys}}{../lib/module-sys.html}
.. % % module also has attributes for \var{stdin}, \var{stdout}, and
.. % % \var{stderr}.  The latter is useful for emitting warnings and error
.. % % messages to make them visible even when \var{stdout} has been redirected:

::

   >>> sys.stderr.write('Warning, log file not found starting a new one\n') 
   Warning, log file not found starting a new one 

``sys.exit()`` は、スクリプトを終了させるもっとも直接的な方法です。

.. % % The most direct way to terminate a script is to use \samp{sys.exit()}.


.. _tut-string-pattern-matching:

文字列のパターンマッチング
==========================

:mod:`re` (XXX reference: ../lib/module-re.html)  モジュールでは、より高度な文字列処理のための正規表現
(regular expression)  を提供しています。正規表現は複雑な一致検索や操作に対して簡潔で最適化 された解決策を与えます:

.. % % The \ulink{\module{re}}{../lib/module-re.html}
.. % % module provides regular expression tools for advanced string processing.
.. % % For complex matching and manipulation, regular expressions offer succinct,
.. % % optimized solutions:

::

   >>> import re 
   >>> re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest') 
   ['foot', 'fell', 'fastest'] 
   >>> re.sub(r'(\b[a-z]+) \1', r'\1', 'cat in the the hat') 
   'cat in the hat' 

最小限の機能だけが必要なら、読みやすくデバッグしやすい文字列メソッドの 方がお勧めです:

.. % % When only simple capabilities are needed, string methods are preferred
.. % % because they are easier to read and debug:

::

   >>> 'tea for too'.replace('too', 'two') 
   'tea for two' 


.. _tut-mathematics:

数学
====

:mod:`math` (XXX reference: ../lib/module-math.html) モジュールでは、 根底にある浮動小数点演算のための C
言語ライブラリ関数にアクセス する手段を提供しています:

.. % % The \ulink{\module{math}}{../lib/module-math.html} module gives
.. % % access to the underlying C library functions for floating point math:

::

   >>> import math 
   >>> math.cos(math.pi / 4.0) 
   0.70710678118654757 
   >>> math.log(1024, 2) 
   10.0 

:mod:`random` (XXX reference: ../lib/module-random.html)
モジュールでは、乱数に基づいた要素選択のためのツールを提供しています:

.. % % The \ulink{\module{random}}{../lib/module-random.html}
.. % % module provides tools for making random selections:

::

   >>> import random 
   >>> random.choice(['apple', 'pear', 'banana']) 
   'apple' 
   >>> random.sample(xrange(100), 10)   # 要素を戻さないサンプリング
   [30, 83, 16, 4, 8, 81, 41, 50, 18, 33] 
   >>> random.random()    # ランダムな浮動小数点数
   0.17970987693706186 
   >>> random.randrange(6)    # range(6) からランダムに選ばれた整数
   4 


.. _tut-internet-access:

インターネットへのアクセス
==========================

インターネットにアクセスしたり、インターネットプロトコルを処理したり するための数多くのモジュールがあります。その中でも最も単純な二つ のモジュールは、URL
を指定してデータを取得するための :mod:`urllib2` (XXX reference: ../lib/module-urllib2.html)
と、メイルを送信するための :mod:`smtplib` (XXX reference: ../lib/module-smtplib.html)  です:

.. % % There are a number of modules for accessing the internet and processing
.. % % internet protocols. Two of the simplest are
.. % % \ulink{\module{urllib2}}{../lib/module-urllib2.html}
.. % % for retrieving data from urls and
.. % % \ulink{\module{smtplib}}{../lib/module-smtplib.html}
.. % % for sending mail:

::

   >>> import urllib2 
   >>> for line in urllib2.urlopen('http://tycho.usno.navy.mil/cgi-bin/timer.pl'): 
   ...     if 'EST' in line or 'EDT' in line:      # look for Eastern Time 
   ...         print line 

   <BR>Nov. 25, 09:43:32 PM EST 

   >>> import smtplib 
   >>> server = smtplib.SMTP('localhost') 
   >>> server.sendmail('soothsayer@example.org', 'jcaesar@example.org', 
   """To: jcaesar@example.org 
   From: soothsayer@example.org 

   Beware the Ides of March. 
   """) 
   >>> server.quit() 


.. _tut-dates-and-times:

日付と時刻
==========

:mod:`datetime` (XXX reference: ../lib/module-datetime.html) モジュールは、
日付や時刻を操作するためのクラスを、単純な方法と複雑な方法の両方で 供給しています。日付や時刻に対する算術がサポートされている一方、
実装では出力の書式化や操作のための効率的なデータメンバ抽出に 重点を置いています。 このモジュールでは、タイムゾーンに対応したオブジェクトもサポート
しています。

.. % % The \ulink{\module{datetime}}{../lib/module-datetime.html} module
.. % % supplies classes for manipulating dates and times in both simple
.. % % and complex ways. While date and time arithmetic is supported, the
.. % % focus of the implementation is on efficient member extraction for
.. % % output formatting and manipulation.  The module also supports objects
.. % % that are time zone aware.

::

   # dates are easily constructed and formatted 
   >>> from datetime import date 
   >>> now = date.today() 
   >>> now 
   datetime.date(2003, 12, 2) 
   >>> now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B") 
   '12-02-03. 02 Dec 2003 is a Tuesday on the 02 day of December' 

   # dates support calendar arithmetic 
   >>> birthday = date(1964, 7, 31) 
   >>> age = now - birthday 
   >>> age.days 
   14368 


.. _tut-data-compression:

データ圧縮
==========

データの書庫化や圧縮で広く使われている形式については、 :mod:`zlib` (XXX reference: ../lib/module-
zlib.html)、 :mod:`gzip` (XXX reference: ../lib/module-gzip.html)、 :mod:`bz2`
(XXX reference: ../lib/module-bz2.html)、 :mod:`zipfile` (XXX reference: ../lib
/module-zipfile.html)、および :mod:`tarfile` (XXX reference: ../lib/module-
tarfile.html) と いったモジュールで直接サポートしています。

.. % % Common data archiving and compression formats are directly supported
.. % % by modules including:
.. % % \ulink{\module{zlib}}{../lib/module-zlib.html},
.. % % \ulink{\module{gzip}}{../lib/module-gzip.html},
.. % % \ulink{\module{bz2}}{../lib/module-bz2.html},
.. % % \ulink{\module{zipfile}}{../lib/module-zipfile.html}, and
.. % % \ulink{\module{tarfile}}{../lib/module-tarfile.html}.

::

   >>> import zlib 
   >>> s = 'witch which has which witches wrist watch' 
   >>> len(s) 
   41 
   >>> t = zlib.compress(s) 
   >>> len(t) 
   37 
   >>> zlib.decompress(t) 
   'witch which has which witches wrist watch' 
   >>> zlib.crc32(s) 
   226805979


.. _tut-performance-measurement:

パフォーマンスの計測
====================

Python ユーザの中には、同じ問題を異なったアプローチで解いた 際の相対的なパフォーマンスについて知りたいという深遠な興味を
抱いている人がいます。Python では、そういった疑問に即座に答える 計測ツールを提供しています。

.. % % Some Python users develop a deep interest in knowing the relative
.. % % performance between different approaches to the same problem.
.. % % Python provides a measurement tool that answers those questions
.. % % immediately.

例えば、引数の入れ替え操作に対して、伝統的なアプローチの代わりに タプルのパックやアンパックを使ってみたい気持ちになるかもしれません。
:mod:`timeit` (XXX reference: ../lib/module-timeit.html) モジュールを
使えば、パフォーマンス上の利点はほぼ互角だとわかります:

.. % % For example, it may be tempting to use the tuple packing and unpacking
.. % % feature instead of the traditional approach to swapping arguments.
.. % % The \ulink{\module{timeit}}{../lib/module-timeit.html} module
.. % % quickly demonstrates a modest performance advantage:

::

   >>> from timeit import Timer 
   >>> Timer('t=a; a=b; b=t', 'a=1; b=2').timeit() 
   0.57535828626024577
   >>> Timer('a,b = b,a', 'a=1; b=2').timeit()
   0.54962537085770791

:mod:`timeit` では高い粒度レベルを提供しているのに対し、 :mod:`profile` (XXX reference: ../lib
/module-profile.html) や :mod:`pstats`  モジュールではより大きなコードブロックにおいて律速となる部分を
判定するためのツールを提供しています。

.. % % In contrast to \module{timeit}'s fine level of granularity, the
.. % % \ulink{\module{profile}}{../lib/module-profile.html} and \module{pstats}
.. % % modules provide tools for identifying time critical sections in larger
.. % % blocks of code.


.. _tut-quality-control:

品質管理
========

高い品質のソフトウェアを開発するための一つのアプローチは、全ての関数 に対して開発と同時にテストを書き、開発の過程で頻繁にテストを走らせる というものです。

.. % % One approach for developing high quality software is to write tests for
.. % % each function as it is developed and to run those tests frequently during
.. % % the development process.

:mod:`doctest` (XXX reference: ../lib/module-doctest.html) モジュールでは、
モジュールを検索して、プログラムの docstring に埋め込まれたテストの 評価を行うためのツールを提供しています。テストの作り方は単純で、
典型的な呼び出し例とその結果を docstring にカット& ペーストすると いうものです。この作業は、ユーザに使用例を与えるという意味で
ドキュメントの情報を増やすと同時に、ドキュメントに書かれている内容が 正しいかどうか doctest モジュールが確認できるようにしています:

.. % % The \ulink{\module{doctest}}{../lib/module-doctest.html} module provides
.. % % a tool for scanning a module and validating tests embedded in a program's
.. % % docstrings.  Test construction is as simple as cutting-and-pasting a
.. % % typical call along with its results into the docstring.  This improves
.. % % the documentation by providing the user with an example and it allows the
.. % % doctest module to make sure the code remains true to the documentation:

::

   def average(values): 
       """Computes the arithmetic mean of a list of numbers. 

       >>> print average([20, 30, 70]) 
       40.0 
       """ 
       return sum(values, 0.0) / len(values) 

   import doctest 
   doctest.testmod()   # automatically validate the embedded tests 

:mod:`unittest` (XXX reference: ../lib/module-unittest.html) モジュールは
:mod:`doctest` モジュールほど気楽に使えるものではありませんが、 より網羅的なテストセットを別のファイルで管理することができます:

.. % % The \ulink{\module{unittest}}{../lib/module-unittest.html} module is not
.. % % as effortless as the \module{doctest} module, but it allows a more
.. % % comprehensive set of tests to be maintained in a separate file:

::

   import unittest 

   class TestStatisticalFunctions(unittest.TestCase): 

       def test_average(self): 
           self.assertEqual(average([20, 30, 70]), 40.0) 
           self.assertEqual(round(average([1, 5, 7]), 1), 4.3) 
           self.assertRaises(ZeroDivisionError, average, []) 
           self.assertRaises(TypeError, average, 20, 30, 70) 

   unittest.main() # Calling from the command line invokes all tests 


.. _tut-batteries-included:

バッテリー同梱
==============

Python には "バッテリー同梱 (batteries included)" 哲学が あります。この哲学は、洗練され、安定した機能を持つ Python
の膨大な パッケージ群に如実に表れています。例えば:

.. % % Python has a ``batteries included'' philosophy.  This is best seen
.. % % through the sophisticated and robust capabilities of its larger
.. % % packages. For example:

* The :mod:`xmlrpclib` (XXX reference: ../lib/module-xmlrpclib.html) および
  :mod:`SimpleXMLRPCServer` (XXX reference: ../lib/module-SimpleXMLRPCServer.html)
  モジュールは、遠隔手続き呼び出し (remote procedure call) を全く たいしたことのない作業に変えてしまいます。モジュール名とは違い、XML
  を扱う ための直接的な知識は必要ありません。

  .. % % \item The \ulink{\module{email}}{../lib/module-email.html}
  .. % % package is a library for managing email messages,
  .. % % including MIME and other RFC 2822-based message documents.  Unlike
  .. % % \module{smtplib} and \module{poplib} which actually send and receive
  .. % % messages, the email package has a complete toolset for building or
  .. % % decoding complex message structures (including attachments)
  .. % % and for implementing internet encoding and header protocols.

* The :mod:`email` (XXX reference: ../lib/module-email.html)  パッケージは、MIME やその他の
  RFC 2822 に基づくメッセージ文書を含む 電子メイルメッセージを管理するためのライブラリです。 実際にメッセージを送信したり受信したりする
  :mod:`smtplib` や :mod:`poplib` と違って、email パッケージには (添付文書を 含む)
  複雑なメッセージ構造の構築やデコードを行ったり、 インターネット標準のエンコードやヘッダプロトコルの実装を行ったり するための完全なツールセットを備えています。

  .. % % \item The \ulink{\module{xml.dom}}{../lib/module-xml.dom.html} and
  .. % % \ulink{\module{xml.sax}}{../lib/module-xml.sax.html} packages provide
  .. % % robust support for parsing this popular data interchange format.  Likewise,
  .. % % the \module{csv} module supports direct reads and writes in a common
  .. % % database format.  Together, these modules and packages greatly simplify
  .. % % data interchange between python applications and other tools.

* :mod:`xml.dom` (XXX reference: ../lib/module-xml.dom.html) および :mod:`xml.sax`
  (XXX reference: ../lib/module-xml.sax.html) パッケージでは、 一般的なデータ交換形式である XML
  を解析するための頑健なサポートを 提供しています。同様に、:mod:`csv` モジュールでは、広く用いられている
  データベース形式のデータを直接読み書きする機能をサポートしています。 これらのモジュールやパッケージは併用することで、Python アプリケーション
  と他のツール群との間でのデータ交換を劇的に簡単化します。

  .. % % \item Internationalization is supported by a number of modules including
  .. % % \ulink{\module{gettext}}{../lib/module-gettext.html},
  .. % % \ulink{\module{locale}}{../lib/module-locale.html}, and the
  .. % % \ulink{\module{codecs}}{../lib/module-codecs.html} package.

* 国際化に関する機能は、 :mod:`gettext` (XXX reference: ../lib/module-gettext.html)、
  :mod:`locale` (XXX reference: ../lib/module-locale.html)、および :mod:`codecs` (XXX
  reference: ../lib/module-codecs.html) パッケージ といったモジュール群でサポートされています。


