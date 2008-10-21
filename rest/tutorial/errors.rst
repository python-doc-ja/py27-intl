.. _tut-errors:

************
エラーと例外
************

これまでエラーメッセージについては簡単に触れるだけでしたが、チュートリアル 中の例を自分で試していたら、実際にいくつかのエラーメッセージを見ている
ことでしょう。エラーには (少なくとも) 二つのはっきり異なる種類があります: それは *構文エラー (syntax error)* と*例外
(exception)* です。

.. % Errors and Exceptions
.. % % Until now error messages haven't been more than mentioned, but if you
.. % % have tried out the examples you have probably seen some.  There are
.. % % (at least) two distinguishable kinds of errors:
.. % % \emph{syntax errors} and \emph{exceptions}.


.. _tut-syntaxerrors:

構文エラー
==========

構文エラーは構文解析エラー (parsing error) としても知られており、 まだ Python
を学習中なら、おそらくもっともよく受け取る種の文句でしょう:

.. % Syntax Errors
.. % % Syntax errors, also known as parsing errors, are perhaps the most common
.. % % kind of complaint you get while you are still learning Python:

::

   >>> while True print 'Hello world'
     File "<stdin>", line 1, in ?
       while True print 'Hello world'
                      ^
   SyntaxError: invalid syntax

パーサは違反の起きている行を繰り返し、小さな '矢印' を表示して、 違反の起きている行中でエラーが検出された最初の位置を示します。 エラーは矢印の*直前の*
トークンでひき起こされています (または、 少なくともそこで検出されています)。 上述の例の中では、エラーは :keyword:`print`
で検出されています。 コロン (``':'``) がその前に無いからです。 入力がスクリプトから来ている場合は、どこを見ればよいか分かるように
ファイル名と行番号が出力されます。

.. % % The parser repeats the offending line and displays a little `arrow'
.. % % pointing at the earliest point in the line where the error was
.. % % detected.  The error is caused by (or at least detected at) the token
.. % % \emph{preceding} the arrow: in the example, the error is detected at
.. % % the keyword \keyword{print}, since a colon (\character{:}) is missing
.. % % before it.  File name and line number are printed so you know where to
.. % % look in case the input came from a script.


.. _tut-exceptions:

例外
====

たとえ文や式が構文的に正しくても、実行しようとしたときにエラーが 発生するかもしれません。 実行中に検出されたエラーは *例外 (exception)*
と呼ばれ、 常に致命的とは限りません: Python プログラムで例外をどのように扱うかは、
すぐに習得することでしょう。ほとんどの例外はプログラムで処理されず、 以下に示されるようなメッセージになります:

.. % Exceptions
.. % % Even if a statement or expression is syntactically correct, it may
.. % % cause an error when an attempt is made to execute it.
.. % % Errors detected during execution are called \emph{exceptions} and are
.. % % not unconditionally fatal: you will soon learn how to handle them in
.. % % Python programs.  Most exceptions are not handled by programs,
.. % % however, and result in error messages as shown here:

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

エラーメッセージの最終行は何が起こったかを示しています。 例外は様々な例外型 (type) で起こり、その型がエラーメッセージの 一部として出力されます:
上の例での型は :exc:`ZeroDivisionError`, :exc:`NameError`, :exc:`TypeError` です。
例外型として出力される文字列は、発生した例外の組み込み名です。 これは全ての組み込み例外について成り立ちますが、 ユーザ定義の例外では
(成り立つようにするのは有意義な慣習ですが) 必ずしも成り立ちません。 標準例外の名前は組み込みの識別子です (予約語ではありません)。

.. % % The last line of the error message indicates what happened.
.. % % Exceptions come in different types, and the type is printed as part of
.. % % the message: the types in the example are
.. % % \exception{ZeroDivisionError}, \exception{NameError} and
.. % % \exception{TypeError}.
.. % % The string printed as the exception type is the name of the built-in
.. % % name for the exception that occurred.  This is true for all built-in
.. % % exceptions, but need not be true for user-defined exceptions (although
.. % % it is a useful convention).
.. % % Standard exception names are built-in identifiers (not reserved
.. % % keywords).

残りの行は例外の詳細で、その例外の型と何が起きたかに依存します。

.. % % The rest of the line provides detail based on the type of exception
.. % %and what caused it.

エラーメッセージの先頭部分では、例外が発生した実行コンテキスト (context) を、スタックのトレースバック (stack traceback) の
形式で示しています。一般には、この部分にはソースコード行を リストしたトレースバックが表示されます; しかし、標準入力から
読み取られた行については表示しません。

.. % % The preceding part of the error message shows the context where the
.. % % exception happened, in the form of a stack traceback.
.. % % In general it contains a stack traceback listing source lines; however,
.. % % it will not display lines read from standard input.

Python ライブラリリファレンス (XXX reference: ../lib/module-exceptions.html)
には、組み込み例外とその意味がリストされています。

.. % % The \citetitle[../lib/module-exceptions.html]{Python Library
.. % % Reference} lists the built-in exceptions and their meanings.


.. _tut-handling:

例外を処理する
==============

例外を選別して処理するようなプログラムを書くことができます。 以下の例を見てください。この例では、有効な文字列が入力されるまで
ユーザに入力を促しますが、ユーザがプログラムに (:kbd:`Control-C` か、またはオペレーティングシステムがサポート している何らかのキーを使って)
割り込みをかけてプログラムを 中断させることができるようにしています; ユーザが生成した割り込みは、 :exc:`KeyboardInterrupt`
例外が送出されることで通知される ということに注意してください。

.. % Handling Exceptions
.. % % It is possible to write programs that handle selected exceptions.
.. % % Look at the following example, which asks the user for input until a
.. % % valid integer has been entered, but allows the user to interrupt the
.. % % program (using \kbd{Control-C} or whatever the operating system
.. % % supports); note that a user-generated interruption is signalled by
.. % % raising the \exception{KeyboardInterrupt} exception.

::

   >>> while True:
   ...     try:
   ...         x = int(raw_input("Please enter a number: "))
   ...         break
   ...     except ValueError:
   ...         print "Oops!  That was no valid number.  Try again..."
   ...     

:keyword:`try` 文は下記のように動作します。

.. % % The \keyword{try} statement works as follows.

* まず、 *try 節 (try clause)* (キーワード :keyword:`try` と  :keyword:`except` のあいだの文)
  が実行されます。

* 何も例外が発生しなければ、*except 節* をスキップして  :keyword:`try` 文の実行を終えます。

* try 節内の実行中に例外が発生すると、その節の残りは飛ばされます。 次に、例外型が :keyword:`except` キーワードの後に指定されている
  例外に一致する場合、except 節が実行 された後、 :keyword:`try` 節の後の文に実行が継続されます。

* もしも except 節で指定された例外と一致しない例外が発生すると、 その例外は :keyword:`try` 文の外側に渡されます。例外に対する
  ハンドラ (handler、処理部) がどこにもなければ、 *処理されない例外 (unhandled exception)* となり、
  上記に示したようなメッセージを出して実行を停止します。

一つの :keyword:`try` 文に複数の except 節を設けて、さまざまな例外に 対するハンドラを指定することができます。同時に一つ以上のハンドラが
実行されることはありません。ハンドラは対応する try 節内で発生した 例外だけを処理し、同じ try 節内の別の例外ハンドラで起きた例外は
処理しません。except 節には複数の例外を丸括弧で囲ったタプルにして 渡すことができます。例えば以下のようにします:

.. % % A \keyword{try} statement may have more than one except clause, to
.. % % specify handlers for different exceptions.  At most one handler will
.. % % be executed.  Handlers only handle exceptions that occur in the
.. % % corresponding try clause, not in other handlers of the same
.. % % \keyword{try} statement.  An except clause may name multiple exceptions
.. % % as a parenthesized list, for example:

::

   ... except (RuntimeError, TypeError, NameError):
   ...     pass

最後の except 節では例外名を省いて、ワイルドカード (wildcard、総称記号) にすることができます。ワイルドカードの except
節は非常に注意して使って ください。というのは、ワイルドカードは通常のプログラムエラーをたやすく 隠してしまうからです！ワイルドカードの except
節はエラーメッセージを 出力した後に例外を再送出する (関数やメソッドの呼び出し側が同様にして 例外を処理できるようにする) 用途にも使えます:

.. % % The last except clause may omit the exception name(s), to serve as a
.. % % wildcard.  Use this with extreme caution, since it is easy to mask a
.. % % real prognnnnramming error in this way!  It can also be used to print an
.. % % error message and then re-raise the exception (allowing a caller to
.. % % handle the exception as well):

::

   import sys

   try:
       f = open('myfile.txt')
       s = f.readline()
       i = int(s.strip())
   except IOError, (errno, strerror):
       print "I/O error(%s): %s" % (errno, strerror)
   except ValueError:
       print "Could not convert data to an integer."
   except:
       print "Unexpected error:", sys.exc_info()[0]
       raise

:keyword:`try` ... :keyword:`except` 文には、オプションで *else 節 (else clause)*
を設けることができます。:keyword:`else` 節を設ける場合、全ての :keyword:`except` 節よりも後ろに置かねばなりません。
:keyword:`except` 節は、try 節で全く例外が送出されなかったときに 実行されるコードを書くのに役立ちます。例えば以下のようにします:

.. % % The \keyword{try} \ldots\ \keyword{except} statement has an optional
.. % % \emph{else clause}, which, when present, must follow all except
.. % % clauses.  It is useful for code that must be executed if the try
.. % % clause does not raise an exception.  For example:

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
送出されたもの以外の例外を偶然に捕捉してしまうという事態を避けられる からです。

.. % % The use of the \keyword{else} clause is better than adding additional
.. % % code to the \keyword{try} clause because it avoids accidentally
.. % % catching an exception that wasn't raised by the code being protected
.. % % by the \keyword{try} \ldots\ \keyword{except} statement.

例外が発生するとき、例外に関連付けられた値を持つことができます。 この値は例外の例外の*引数 (argument)* としても知られています。
引数の有無と引数の型がどうなっているかは例外の型に依存します。

.. % % When an exception occurs, it may have an associated value, also known as
.. % % the exception's \emph{argument}.
.. % % The presence and type of the argument depend on the exception type.

except 節では、例外名 (または例外名タプル) の後に変数を指定することが できます。この変数は例外インスタンスに結び付けられており、
``instance.args`` に例外インスタンス生成時の引数が入っています。 例外インスタンスには :meth:`__getitem__` および
:meth:`__str__` が 定義されており、``.args`` を参照しなくても引数に直接アクセスしたり 印字したりできるように利便性が図られています。

.. % % The except clause may specify a variable after the exception name (or tuple).
.. % % The variable is bound to an exception instance with the arguments stored
.. % % in \code{instance.args}.  For convenience, the exception instance
.. % % defines \method{__getitem__} and \method{__str__} so the arguments can
.. % % be accessed or printed directly without having to reference \code{.args}.

しかし ``.args``の利用は推奨されません。そのかわりに、例外へ 引数を1つだけ渡してください（複数の値が必要な場合にはタプルを使用でき
ます）。そしてそれを ``message``属性に結びつけます。 例外をraiseする前にインスタンス化をするときだけでなく、必要に応じて 属性を追加できます。

.. % % But use of \code{.args} is discouraged.  Instead, the preferred use is to pass
.. % % a single argument to an exception (which can be a tuple if multiple arguments
.. % % are needed) and have it bound to the \code{message} attribute.  One my also
.. % % instantiate an exception first before raising it and add any attributes to it
.. % % as desired.

::

   >>> try:
   ...    raise Exception('spam', 'eggs')
   ... except Exception, inst:
   ...    print type(inst)     # 例外インスタンス
   ...    print inst.args      # .args に記憶されている引数
   ...    print inst           # __str__ で引数を直接出力できる
   ...    x, y = inst          # __getitem__ で引数を直接アンパックできる
   ...    print 'x =', x
   ...    print 'y =', y
   ...
   <type 'instance'>
   ('spam', 'eggs')
   ('spam', 'eggs')
   x = spam
   y = eggs

処理されない例外の場合、例外が引数を持っていれば、メッセージの 最後の ('詳細説明の') 部分に出力されます。

.. % % If an exception has an argument, it is printed as the last part
.. % % (`detail') of the message for unhandled exceptions.

例外ハンドラは、try 節でじかに発生した例外を処理するだけではなく、 その try 節から呼び出された関数の内部で発生した例外も処理します
(間接的に呼ばれていてもです) 。例えば:

.. % % Exception handlers don't just handle exceptions if they occur
.. % % immediately in the try clause, but also if they occur inside functions
.. % % that are called (even indirectly) in the try clause.
.. % % For example:

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

:keyword:`raise` 文を使うと、プログラマは指定した例外を強制的に 送出させられます。例えば:

.. % Raising Exceptions
.. % % The \keyword{raise} statement allows the programmer to force a
.. % % specified exception to occur.
.. % % For example:

::

   >>> raise NameError, 'HiThere'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NameError: HiThere

.. % % The first argument to \keyword{raise} names the exception to be
.. % % raised.  The optional second argument specifies the exception's
.. % % argument.  Alternatively, the above could be written as
.. % % \code{raise NameError('HiThere')}.  Either form works fine, but there
.. % % seems to be a growing stylistic preference for the latter.

:keyword:`raise` の第一引数には、ひき起こすべき例外を指定します。 オプションの第二引数では例外の引数を指定します。 同じことを　``raise
NameError('HiThere')``　としても記述できます。 どちらの形式でもうまく動きますが後者のほうがスタイルがよくみえます。

例外が発生したかどうかは判定したいが、その処理を行おうとは思っていない 場合、単純な形式の :keyword:`raise` 文を使って例外を再送出させることが
できます:

.. % % If you need to determine whether an exception was raised but don't
.. % % intend to handle it, a simpler form of the \keyword{raise} statement
.. % % allows you to re-raise the exception:

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

プログラム上で新しい例外クラスを作成することで、独自の例外を指定する ことができます。例外は、典型的に :exc:`Exception` クラスから、
直接または間接的に導出したものです。例えば:

.. % User-defined Exceptions
.. % % Programs may name their own exceptions by creating a new exception
.. % % class.  Exceptions should typically be derived from the
.. % % \exception{Exception} class, either directly or indirectly.  For
.. % % example:

::

   >>> class MyError(Exception):
   ...     def __init__(self, value):
   ...         self.value = value
   ...     def __str__(self):
   ...         return repr(self.value)
   ... 
   >>> try:
   ...     raise MyError(2*2)
   ... except MyError, e:
   ...     print 'My exception occurred, value:', e.value
   ... 
   My exception occurred, value: 4
   >>> raise MyError, 'oops!'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   __main__.MyError: 'oops!'

この例では:class:`Exception`のデフォルト:meth:`__init__`がオーバーライ ドされています。新しいふるまいでは、単に
*value*属性を作ります。 これはデフォルトの*args*属性を作成するふるまいを置き換えています。

.. % % In this example, the default \method{__init__} of \class{Exception}
.. % % has been overridden.  The new behavior simply creates the \var{value}
.. % % attribute.  This replaces the default behavior of creating the
.. % % \var{args} attribute.

例外クラスでは、他のクラスができることなら何でも定義することが できますが、通常は単純なものにしておきます。たいていは、いくつかの
属性だけを提供し、例外が発生したときにハンドラがエラーに関する情報 を取り出せるようにする程度にとどめます。
複数の別個の例外を送出するようなモジュールを作成する際には、 そのモジュールで定義されている例外の基底クラスを作成するのが 一般的なならわしです:

.. % % Exception classes can be defined which do anything any other class can
.. % % do, but are usually kept simple, often only offering a number of
.. % % attributes that allow information about the error to be extracted by
.. % % handlers for the exception.  When creating a module that can raise
.. % % several distinct errors, a common practice is to create a base class
.. % % for exceptions defined by that module, and subclass that to create
.. % % specific exception classes for different error conditions:

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

.. % % Most exceptions are defined with names that end in ``Error,'' similar
.. % % to the naming of the standard exceptions.

多くの標準モジュールでは、モジュールで定義されている関数内で発生する 可能性のあるエラーを報告させるために、独自の例外を定義しています。
クラスについての詳細な情報は :ref:`tut-classes` 章、 "クラス" で 提供されています。

.. % % Many standard modules define their own exceptions to report errors
.. % % that may occur in functions they define.  More information on classes
.. % % is presented in chapter \ref{classes}, ``Classes.''


.. _tut-cleanup:

後片付け動作を定義する
======================

:keyword:`try` 文にはもう一つオプションの節があります。この節は クリーンアップ動作を定義するためのもので、どんな状況でも必ず
実行されます。例えば:

.. % Defining Clean-up Actions
.. % % The \keyword{try} statement has another optional clause which is
.. % % intended to define clean-up actions that must be executed under all
.. % % circumstances.  For example:

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
節で例外が発生したかどうかに関係なく常に:keyword:`try`節のあとに実 行されます。
:keyword:`try`節の中で例外が発生して、:keyword:`except`節でハンドルされ
ていない場合、または:keyword:`except`節か:keyword:`else`節で例外が発生し た場合は、:keyword:`finally`
節を実行した後、その例外を再送出します。 :keyword:`finally` 節はまた、:keyword:`try` 節から :keyword:`break`
文や  :keyword:`continue` 文、:keyword:`return` 文経由で抜ける際にも、 "抜ける途中で" 実行されます。
より複雑な例です:

.. % % A \emph{finally clause} is always executed before leaving the
.. % % \keyword{try} statement, whether an exception has occurred or not.
.. % % When an exception has occurred in the \keyword{try} clause and has not
.. % % been handled by an \keyword{except} clause (or it has occurred in a
.. % % \keyword{except} or \keyword{else} clause), it is re-raised after the
.. % % \keyword{finally} clause has been executed.  The \keyword{finally} clause
.. % % is also executed ``on the way out'' when any other clause of the
.. % % \keyword{try} statement is left via a \keyword{break}, \keyword{continue}
.. % % or \keyword{return} statement.  A more complicated example:

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

見てわかるとおり、:keyword:`finally`節はどの場合にも実行されています。 文字列を割り算することで発生した　:exc:`TypeError` は
:keyword:`except`節でハンドルされていませんので、:keyword:`finally`節 実行後に再度raiseされています。

.. % % As you can see, the \keyword{finally} clause is executed in any
.. % % event.  The \exception{TypeError} raised by dividing two strings
.. % % is not handled by the \keyword{except} clause and therefore
.. % % re-raised after the \keyword{finally} clauses has been executed.

実世界のアプリケーションでは、:keyword:`finally`節は(ファイルやネットワー
ク接続などの)外部リソースを利用の成否にかかわらず開放するために便利です。

.. % % In real world applications, the \keyword{finally} clause is useful
.. % % for releasing external resources (such as files or network connections),
.. % % regardless of whether the use of the resource was successful.

.. % % \section{Predefined Clean-up Actions \label{cleanup-with}}


.. _tut-cleanup-with:

定義済み完了処理
================

オブジェクトのなかには、その利用の成否にかかわらず、不要になった際に 実行される標準的な完了処理が定義されているものがあります。
以下の、ファイルをオープンして内容を画面に表示する例をみてください:

.. % % Some objects define standard clean-up actions to be undertaken when
.. % % the object is no longer needed, regardless of whether or not the
.. % % operation using the object succeeded or failed.
.. % % Look at the following example, which tries to open a file and print
.. % % its contents to the screen.

::

   for line in open("myfile.txt"):
       print line

このコードの問題点は、このコードが実行されてから、ファイルをいつまで openしたままでいるかわからないことです。
これは単純なスクリプトでは問題になりませんが、大きなアプリケーションで は問題になりえます。:keyword:`with`文はファイルのようなオブジェクトが
常に、即座に正しく完了されることを保証します。

.. % % The problem with this code is that it leaves the file open for an
.. % % indeterminate amount of time after the code has finished executing.
.. % % This is not an issue in simple scripts, but can be a problem for
.. % % larger applications. The \keyword{with} statement allows
.. % % objects like files to be used in a way that ensures they are
.. % % always cleaned up promptly and correctly.

::

   with open("myfile.txt") as f:
       for line in f:
           print line

文が実行されたあと、行の処理中に問題があったかどうかに関係なく、ファイ ル*f*は常にcloseされます。他の定義済み完了処理をもつオブジェクト
については、それぞれのドキュメントで示されます。

.. % % After the statement is executed, the file \var{f} is always closed,
.. % % even if a problem was encountered while processing the lines. Other
.. % % objects which provide predefined clean-up actions will indicate
.. % % this in their documentation.


