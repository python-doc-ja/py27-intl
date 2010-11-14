.. _tut-errors:

************
エラーと例外
************

これまでエラーメッセージについては簡単に触れるだけでしたが、チュートリアル中の例を自分で試していたら、実際にいくつかのエラーメッセージを見ている
ことでしょう。エラーには (少なくとも) 二つのはっきり異なる種類があります: それは *構文エラー (syntax error)* と*例外
(exception)* です。



.. _tut-syntaxerrors:

構文エラー
==========

構文エラーは構文解析エラー (parsing error) としても知られており、まだ Python
を学習中なら、おそらくもっともよく受け取る種の文句でしょう:


::

   >>> while True print 'Hello world'
     File "<stdin>", line 1, in ?
       while True print 'Hello world'
                      ^
   SyntaxError: invalid syntax

パーサは違反の起きている行を繰り返し、小さな '矢印' を表示して、
違反の起きている行中でエラーが検出された最初の位置を示します。エラーは矢印の *直前の*
トークンでひき起こされています (または、少なくともそこで検出されています)。上述の例の中では、エラーは :keyword:`print`
で検出されています。コロン (``':'``) がその前に無いからです。入力がスクリプトから来ている場合は、どこを見ればよいか分かるように
ファイル名と行番号が出力されます。



.. _tut-exceptions:

例外
====

たとえ文や式が構文的に正しくても、実行しようとしたときにエラーが発生するかもしれません。実行中に検出されたエラーは *例外 (exception)*
と呼ばれ、常に致命的とは限りません: Python プログラムで例外をどのように扱うかは、
すぐに習得することでしょう。ほとんどの例外はプログラムで処理されず、以下に示されるようなメッセージになります:


::

   >>> 10 * (1/0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ZeroDivisionError: integer division or modulo by zero
   >>> 4 + spam*3
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NameError: name 'spam' is not defined
   >>> '2' + 2
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: cannot concatenate 'str' and 'int' objects

エラーメッセージの最終行は何が起こったかを示しています。例外は様々な例外型 (type) で起こり、その型がエラーメッセージの一部として出力されます:
上の例での型は :exc:`ZeroDivisionError`, :exc:`NameError`, :exc:`TypeError` です。
例外型として出力される文字列は、発生した例外の組み込み名です。これは全ての組み込み例外について成り立ちますが、ユーザ定義の例外では
(成り立つようにするのは有意義な慣習ですが) 必ずしも成り立ちません。標準例外の名前は組み込みの識別子です (予約語ではありません)。


残りの行は例外の詳細で、その例外の型と何が起きたかに依存します。


エラーメッセージの先頭部分では、例外が発生した実行コンテキスト (context) を、スタックのトレースバック (stack traceback) の
形式で示しています。一般には、この部分にはソースコード行をリストしたトレースバックが表示されます; しかし、標準入力から
読み取られた行については表示しません。


:ref:`bltin-exceptions` 
には、組み込み例外とその意味がリストされています。



.. _tut-handling:

例外を処理する
==============

例外を選別して処理するようなプログラムを書くことができます。以下の例を見てください。この例では、有効な文字列が入力されるまで
ユーザに入力を促しますが、ユーザがプログラムに (:kbd:`Control-C` か、またはオペレーティングシステムがサポートしている何らかのキーを使って)
割り込みをかけてプログラムを中断させることができるようにしています; ユーザが生成した割り込みは、 :exc:`KeyboardInterrupt`
例外が送出されることで通知されるということに注意してください。


::

   >>> while True:
   ...     try:
   ...         x = int(raw_input("Please enter a number: "))
   ...         break
   ...     except ValueError:
   ...         print "Oops!  That was no valid number.  Try again..."
   ...

:keyword:`try` 文は下記のように動作します。


* まず、 *try 節 (try clause)* (キーワード :keyword:`try` と :keyword:`except` の間の文)
  が実行されます。

* 何も例外が発生しなければ、 *except 節* をスキップして  :keyword:`try` 文の実行を終えます。

* try 節内の実行中に例外が発生すると、その節の残りは飛ばされます。
  次に、例外型が :keyword:`except` キーワードの後に指定されている
  例外に一致する場合、except 節が実行された後、 :keyword:`try` 節の後の文に実行が継続されます。

* もしも except 節で指定された例外と一致しない例外が発生すると、その例外は
  :keyword:`try` 文の外側に渡されます。例外に対する
  ハンドラ (handler、処理部) がどこにもなければ、 *処理されない例外 (unhandled exception)* となり、
  上記に示したようなメッセージを出して実行を停止します。

一つの :keyword:`try` 文に複数の except 節を設けて、さまざまな例外に対するハンドラを指定することができます。同時に一つ以上のハンドラが
実行されることはありません。ハンドラは対応する try 節内で発生した例外だけを処理し、同じ try 節内の別の例外ハンドラで起きた例外は
処理しません。except 節には複数の例外を丸括弧で囲ったタプルにして渡すことができます。例えば以下のようにします:


::

   ... except (RuntimeError, TypeError, NameError):
   ...     pass

最後の except 節では例外名を省いて、ワイルドカード (wildcard、総称記号) にすることができます。ワイルドカードの except
節は非常に注意して使ってください。というのは、ワイルドカードは通常のプログラムエラーをたやすく隠してしまうからです！ワイルドカードの except
節はエラーメッセージを出力した後に例外を再送出する (関数やメソッドの呼び出し側が同様にして例外を処理できるようにする) 用途にも使えます:


::

   import sys

   try:
       f = open('myfile.txt')
       s = f.readline()
       i = int(s.strip())
   except IOError as (errno, strerror):
       print "I/O error({0}): {1}".format(errno, strerror)
   except ValueError:
       print "Could not convert data to an integer."
   except:
       print "Unexpected error:", sys.exc_info()[0]
       raise

:keyword:`try` ... :keyword:`except` 文には、オプションで *else 節 (else clause)*
を設けることができます。 :keyword:`else` 節を設ける場合、全ての :keyword:`except` 節よりも後ろに置かねばなりません。
:keyword:`except` 節は、try 節で全く例外が送出されなかったときに実行されるコードを書くのに役立ちます。例えば以下のようにします:


::

   for arg in sys.argv[1:]:
       try:
           f = open(arg, 'r')
       except IOError:
           print 'cannot open', arg
       else:
           print arg, 'has', len(f.readlines()), 'lines'
           f.close()

追加のコードを追加するのは :keyword:`try` 節の後ろよりも :keyword:`else`  節の方がよいでしょう。なぜなら、そうすることで
:keyword:`try` ... :keyword:`except` 文で保護したいコードから
送出されたもの以外の例外を偶然に捕捉してしまうという事態を避けられるからです。


例外が発生するとき、例外に関連付けられた値を持つことができます。この値は例外の例外の *引数 (argument)* としても知られています。
引数の有無と引数の型がどうなっているかは例外の型に依存します。


except 節では、例外名 (または例外名タプル) の後に変数を指定することができます。この変数は例外インスタンスに結び付けられており、
``instance.args`` に例外インスタンス生成時の引数が入っています。例外インスタンスには :meth:`__getitem__` および
:meth:`__str__` が定義されており、 ``.args`` を参照しなくても引数に直接アクセスしたり印字したりできるように利便性が図られています。


しかし ``.args`` の利用は推奨されません。そのかわりに、例外へ引数を1つだけ渡してください（複数の値が必要な場合にはタプルを使用でき
ます）。そしてそれを ``message`` 属性に結びつけます。例外をraiseする前にインスタンス化をするときだけでなく、必要に応じて属性を追加できます。


::

   >>> try:
   ...    raise Exception('spam', 'eggs')
   ... except Exception as inst:
   ...    print type(inst)     # 例外インスタンス
   ...    print inst.args      # .args に記憶されている引数
   ...    print inst           # __str__ で引数を直接出力できる
   ...    x, y = inst          # __getitem__ で引数を直接アンパックできる
   ...    print 'x =', x
   ...    print 'y =', y
   ...
   <type 'exceptions.Exception'>
   ('spam', 'eggs')
   ('spam', 'eggs')
   x = spam
   y = eggs

処理されない例外の場合、例外が引数を持っていれば、メッセージの最後の ('詳細説明の') 部分に出力されます。


例外ハンドラは、try 節でじかに発生した例外を処理するだけではなく、その try 節から呼び出された関数の内部で発生した例外も処理します
(間接的に呼ばれていてもです) 。例えば:


::

   >>> def this_fails():
   ...     x = 1/0
   ...
   >>> try:
   ...     this_fails()
   ... except ZeroDivisionError, detail:
   ...     print 'Handling run-time error:', detail
   ...
   Handling run-time error: integer division or modulo by zero


.. _tut-raising:

例外を送出する
==============

:keyword:`raise` 文を使うと、プログラマは指定した例外を強制的に送出させられます。例えば:


::

   >>> raise NameError, 'HiThere'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NameError: HiThere


:keyword:`raise` の第一引数には、ひき起こすべき例外を指定します。オプションの第二引数では例外の引数を指定します。同じことを　``raise
NameError('HiThere')``　としても記述できます。どちらの形式でもうまく動きますが後者のほうがスタイルがよくみえます。

例外が発生したかどうかは判定したいが、その処理を行おうとは思っていない場合、単純な形式の :keyword:`raise` 文を使って例外を再送出させることが
できます:


::

   >>> try:
   ...     raise NameError, 'HiThere'
   ... except NameError:
   ...     print 'An exception flew by!'
   ...     raise
   ...
   An exception flew by!
   Traceback (most recent call last):
     File "<stdin>", line 2, in ?
   NameError: HiThere


.. _tut-userexceptions:

ユーザ定義の例外
================

プログラム上で新しい例外クラスを作成することで、独自の例外を指定することができます。例外は、典型的に :exc:`Exception` クラスから、
直接または間接的に導出したものです。例えば:


::

   >>> class MyError(Exception):
   ...     def __init__(self, value):
   ...         self.value = value
   ...     def __str__(self):
   ...         return repr(self.value)
   ...
   >>> try:
   ...     raise MyError(2*2)
   ... except MyError as e:
   ...     print 'My exception occurred, value:', e.value
   ...
   My exception occurred, value: 4
   >>> raise MyError, 'oops!'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   __main__.MyError: 'oops!'

この例では :class:`Exception` のデフォルト :meth:`__init__` がオーバーライドされています。新しいふるまいでは、単に
*value* 属性を作ります。これはデフォルトの *args* 属性を作成するふるまいを置き換えています。


例外クラスでは、他のクラスができることなら何でも定義することができますが、通常は単純なものにしておきます。たいていは、いくつかの
属性だけを提供し、例外が発生したときにハンドラがエラーに関する情報を取り出せるようにする程度にとどめます。
複数の別個の例外を送出するようなモジュールを作成する際には、そのモジュールで定義されている例外の基底クラスを作成するのが一般的なならわしです:


::

   class Error(Exception):
       """Base class for exceptions in this module."""
       pass

   class InputError(Error):
       """Exception raised for errors in the input.

       Attributes:
           expression -- input expression in which the error occurred
           message -- explanation of the error
       """

       def __init__(self, expression, message):
           self.expression = expression
           self.message = message

   class TransitionError(Error):
       """Raised when an operation attempts a state transition that's not
       allowed.

       Attributes:
           previous -- state at beginning of transition
           next -- attempted new state
           message -- explanation of why the specific transition is not allowed
       """

       def __init__(self, previous, next, message):
           self.previous = previous
           self.next = next
           self.message = message

ほとんどの例外は、標準の例外の名前付けと同様に、 "Error,"  で終わる名前で定義されています。


多くの標準モジュールでは、モジュールで定義されている関数内で発生する可能性のあるエラーを報告させるために、独自の例外を定義しています。
クラスについての詳細な情報は :ref:`tut-classes` 章で提供されています。



.. _tut-cleanup:

後片付け動作を定義する
======================

:keyword:`try` 文にはもう一つオプションの節があります。この節はクリーンアップ動作を定義するためのもので、どんな状況でも必ず
実行されます。例えば:


::

   >>> try:
   ...     raise KeyboardInterrupt
   ... finally:
   ...     print 'Goodbye, world!'
   ...
   Goodbye, world!
   Traceback (most recent call last):
     File "<stdin>", line 2, in ?
   KeyboardInterrupt

*finally 節 (finally clause)* は、 :keyword:`try`
節で例外が発生したかどうかに関係なく常に :keyword:`try` 節のあとに実行されます。
:keyword:`try` 節の中で例外が発生して、 :keyword:`except` 節でハンドルされ
ていない場合、または :keyword:`except` 節か :keyword:`else` 節で例外が発生した場合は、 :keyword:`finally`
節を実行した後、その例外を再送出します。 :keyword:`finally` 節はまた、 :keyword:`try` 節から :keyword:`break`
文や  :keyword:`continue` 文、 :keyword:`return` 文経由で抜ける際にも、 "抜ける途中で" 実行されます。
より複雑な例です (:keyword:`except` 節や :keyword:`finally` 節が同じ :keyword:`try` 文の中にあっても Python 2.5 と同じように動作します):


::

   >>> def divide(x, y):
   ...     try:
   ...         result = x / y
   ...     except ZeroDivisionError:
   ...         print "division by zero!"
   ...     else:
   ...         print "result is", result
   ...     finally:
   ...         print "executing finally clause"
   ...
   >>> divide(2, 1)
   result is 2
   executing finally clause
   >>> divide(2, 0)
   division by zero!
   executing finally clause
   >>> divide("2", "1")
   executing finally clause
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
     File "<stdin>", line 3, in divide
   TypeError: unsupported operand type(s) for /: 'str' and 'str'

見てわかるとおり、 :keyword:`finally` 節はどの場合にも実行されています。文字列を割り算することで発生した　 :exc:`TypeError` は
:keyword:`except` 節でハンドルされていませんので、 :keyword:`finally` 節実行後に再度raiseされています。


実世界のアプリケーションでは、 :keyword:`finally` 節は(ファイルやネットワー
ク接続などの)外部リソースを利用の成否にかかわらず開放するために便利です。




.. _tut-cleanup-with:

定義済み完了処理
================

オブジェクトのなかには、その利用の成否にかかわらず、不要になった際に実行される標準的な完了処理が定義されているものがあります。
以下の、ファイルをオープンして内容を画面に表示する例をみてください:


::

   for line in open("myfile.txt"):
       print line

このコードの問題点は、このコードが実行されてから、ファイルをいつまで openしたままでいるかわからないことです。
これは単純なスクリプトでは問題になりませんが、大きなアプリケーションでは問題になりえます。 :keyword:`with` 文はファイルのようなオブジェクトが
常に、即座に正しく完了されることを保証します。


::

   with open("myfile.txt") as f:
       for line in f:
           print line

文が実行されたあと、行の処理中に問題があったかどうかに関係なく、ファイル *f* は常にcloseされます。他の定義済み完了処理をもつオブジェクト
については、それぞれのドキュメントで示されます。



