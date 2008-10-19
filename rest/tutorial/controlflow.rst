.. _tut-morecontrol:

************
その他の制御フローツール
************

今しがた紹介した :keyword:`while` 文の他に、Python では他の言語で おなじみの普通の制御フロー文を備えていますが、これらには多少
ひねりを加えてあります。

.. % More Control Flow Tools
.. % % Besides the \keyword{while} statement just introduced, Python knows
.. % % the usual control flow statements known from other languages, with
.. % % some twists.


.. _tut-if:

:keyword:`if` 文
===============

おそらく最もおなじみの文型は :keyword:`if` 文でしょう。 例えば、

.. % \keyword{if} Statements
.. % % Perhaps the most well-known statement type is the
.. % % \keyword{if} statement.  For example:

::

   >>> x = int(raw_input("Please enter an integer: "))
   >>> if x < 0:
   ...      x = 0
   ...      print 'Negative changed to zero'
   ... elif x == 0:
   ...      print 'Zero'
   ... elif x == 1:
   ...      print 'Single'
   ... else:
   ...      print 'More'
   ... 

:keyword:`elif` 部はゼロ個またはそれ以上にできます。 :keyword:`else` 部を付けることもできます。 キーワード
':keyword:`elif`' は 'else if' を短くしたもので、 過剰なインデントを避けるのに役立ちます。 一連の :keyword:`if`
... :keyword:`elif` ... :keyword:`elif` ...  は、他の言語における *switch* 文や *case* 文の代用と
なります。

.. % % There can be zero or more \keyword{elif} parts, and the
.. % % \keyword{else} part is optional.  The keyword `\keyword{elif}' is
.. % % short for `else if', and is useful to avoid excessive indentation.  An
.. % % \keyword{if} \ldots\ \keyword{elif} \ldots\ \keyword{elif} \ldots\ sequence
.. % % %    Weird spacings happen here if the wrapping of the source text
.. % % %    gets changed in the wrong way.
.. % % is a substitute for the \keyword{switch} or
.. % % \keyword{case} statements found in other languages.


.. _tut-for:

:keyword:`for` 文
================

.. index::
   statement: for
   statement: for

Python の :keyword:`for` 文は、読者が C 言語や Pascal 言語 で使いなれているかもしれない :keyword:`for`
文とは少し違います。 (Pascal のように) 常に算術型の数列にわたる反復を行ったり、 (C のように)
繰返しステップと停止条件を両方ともユーザが定義できるように するのとは違い、Python の :keyword:`for` 文は、任意の シーケンス型
(リストまたは文字列) にわたって反復を行います。反復の順番は シーケンス中に要素が現れる順番です。 (for example というしゃれではないけれど)
例えば 、

.. % \keyword{for} Statements
.. % % The \keyword{for}\stindex{for} statement in Python differs a bit from
.. % % what you may be used to in C or Pascal.  Rather than always
.. % % iterating over an arithmetic progression of numbers (like in Pascal),
.. % % or giving the user the ability to define both the iteration step and
.. % % halting condition (as C), Python's
.. % % \keyword{for}\stindex{for} statement iterates over the items of any
.. % % sequence (a list or a string), in the order that they appear in
.. % % the sequence.  For example (no pun intended):
.. % % % One suggestion was to give a real C example here, but that may only
.. % % % serve to confuse non-C programmers.
.. % One suggestion was to give a real C example here, but that may only
.. % serve to confuse non-C programmers.

::

   >>> # いくつかの文字列の長さを測る:
   ... a = ['cat', 'window', 'defenestrate']
   >>> for x in a:
   ...     print x, len(x)
   ... 
   cat 3
   window 6
   defenestrate 12

反復操作の対象になっているシーケンスをループので書き換える操作 (リストのような、変更可能 (mutable) なシーケンス型でおきます) は、安全
ではありません。もし反復処理を行う対象とするリスト型を変更したいのなら、 (対象の要素を複製するなどして) コピーに対して反復を行わなければ
なりません。この操作にはスライス表記を使うと特に便利です:

.. % % It is not safe to modify the sequence being iterated over in the loop
.. % % (this can only happen for mutable sequence types, such as lists).  If
.. % % you need to modify the list you are iterating over (for example, to
.. % % duplicate selected items) you must iterate over a copy.  The slice
.. % % notation makes this particularly convenient:

::

   >>> for x in a[:]: # リスト全体のスライス・コピーを作る
   ...    if len(x) > 6: a.insert(0, x)
   ... 
   >>> a
   ['defenestrate', 'cat', 'window', 'defenestrate']


.. _tut-range:

:func:`range` 関数
================

数列にわたって反復を行う必要がある場合、組み込み関数 :func:`range`  が便利です。この関数は算術型の数列が入ったリストを生成します。

.. % The \function{range()} Function
.. % % If you do need to iterate over a sequence of numbers, the built-in
.. % % function \function{range()} comes in handy.  It generates lists
.. % % containing arithmetic progressions:

::

   >>> range(10)
   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

指定した終端値は生成されるリストには入りません。 ``range(10)`` は 10 個の値からなるリストを生成し、 長さ 10
のシーケンスにおける各項目のインデクスとなります。 range を別の数から開始したり、他の増加量 (負の増加量でさえも; 増加量は時に
'ステップ(step)' と呼ばれることもあります) を指定する こともできます:

.. % % The given end point is never part of the generated list;
.. % % \code{range(10)} generates a list of 10 values, the legal
.. % % indices for items of a sequence of length 10.  It is possible to let
.. % % the range start at another number, or to specify a different increment
.. % % (even negative; sometimes this is called the `step'):

::

   >>> range(5, 10)
   [5, 6, 7, 8, 9]
   >>> range(0, 10, 3)
   [0, 3, 6, 9]
   >>> range(-10, -100, -30)
   [-10, -40, -70]

あるシーケンスにわたってインデクスで反復を行うには、 :func:`range` と :func:`len` を次のように組み合わせます:

.. % % To iterate over the indices of a sequence, combine
.. % % \function{range()} and \function{len()} as follows:

::

   >>> a = ['Mary', 'had', 'a', 'little', 'lamb']
   >>> for i in range(len(a)):
   ...     print i, a[i]
   ... 
   0 Mary
   1 had
   2 a
   3 little
   4 lamb


.. _tut-break:

:keyword:`break` 文と :keyword:`continue` 文と ループの :keyword:`else` 節
=================================================================

:keyword:`break` 文は、C 言語と同じく、最も内側の :keyword:`for` または :keyword:`while`
ループを中断します。

.. % \keyword{break} and \keyword{continue} Statements, and
.. % \keyword{else} Clauses on Loops
.. % % The \keyword{break} statement, like in C, breaks out of the smallest
.. % % enclosing \keyword{for} or \keyword{while} loop.

:keyword:`continue` 文は、これもまた C 言語から借りてきたものですが、 ループを次の反復処理に飛ばします。

.. % % The \keyword{continue} statement, also borrowed from C, continues
.. % % with the next iteration of the loop.

ループ文は :keyword:`else` 節を持つことができます; :keyword:`else` 節は、 (:keyword:`for` で)
反復処理対象のリストを使い切ってループが終了したとき、 または (:keyword:`while` で) 条件が偽になったときに実行されますが、
:keyword:`break` 文でループが終了したときは実行されません。 この動作を、素数を探す下記のループを例にとって示します:

.. % % Loop statements may have an \code{else} clause; it is executed when
.. % % the loop terminates through exhaustion of the list (with
.. % % \keyword{for}) or when the condition becomes false (with
.. % % \keyword{while}), but not when the loop is terminated by a
.. % % \keyword{break} statement.  This is exemplified by the following loop,
.. % % which searches for prime numbers:

::

   >>> for n in range(2, 10):
   ...     for x in range(2, n):
   ...         if n % x == 0:
   ...            print n, 'equals', x, '*', n/x
   ...            break
   ...     else:
   ...          # 因数が見つからずにループが終了
   ...          print n, 'is a prime number'
   ... 
   2 is a prime number
   3 is a prime number
   4 equals 2 * 2
   5 is a prime number
   6 equals 2 * 3
   7 is a prime number
   8 equals 2 * 4
   9 equals 3 * 3


.. _tut-pass:

:keyword:`pass` 文
=================

:keyword:`pass` 文は何もしません。:keyword:`pass` は、文を書くことが
構文上要求されているが、プログラム上何の動作もする必要がない時に 使われます。

.. % \keyword{pass} Statements
.. % % The \keyword{pass} statement does nothing.
.. % % It can be used when a statement is required syntactically but the
.. % % program requires no action.
.. % % For example:

::

   >>> while True:
   ...       pass # キーボード割り込み (keyboard interrupt) をbusy-wait で待つ  
   ... 


.. _tut-functions:

関数を定義する
=======

フィボナッチ数列 (Fibonacci series) を任意の上限値まで書き出すような 関数を作成できます:

.. % Defining Functions
.. % % We can create a function that writes the Fibonacci series to an
.. % % arbitrary boundary:

::

   >>> def fib(n):    # n までのフィボナッチ級数を出力する
   ...     """Print a Fibonacci series up to n."""
   ...     a, b = 0, 1
   ...     while b < n:
   ...         print b,
   ...         a, b = b, a+b
   ... 
   >>> # 今しがた定義した関数を呼び出す:
   ... fib(2000)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597

.. index::
   single: documentation strings
   single: docstrings
   single: strings, documentation

:keyword:`def` は関数の*定義 (definition)* を導くキーワードです。 :keyword:`def` の後には、関数名と仮引数
(formal parameter) を 丸括弧で囲んだリストを続けなければなりません。関数の実体を
校正する実行文は次の行から始め、インデントされていなければなりません。 関数の本体の記述する文の最初の行は文字列リテラルにすることもできます;
その場合、文字列は関数の  ドキュメンテーション文字列 (documentation string)、または :dfn:`docstring`  です。

.. % % The keyword \keyword{def} introduces a function \emph{definition}.  It
.. % % must be followed by the function name and the parenthesized list of
.. % % formal parameters.  The statements that form the body of the function
.. % % start at the next line, and must be indented.  The first statement of
.. % % the function body can optionally be a string literal; this string
.. % % literal is the function's \index{documentation strings}documentation
.. % % string, or \dfn{docstring}.\index{docstrings}\index{strings, documentation}

ドキュメンテーション文字列を使ったツールには、オンライン文書や 印刷文書を自動的に生成したり、ユーザが対話的にコードを閲覧できる ようにするものがあります;
自分が書くコードにドキュメンテーション 文字列を入れるのはよい習慣です。書く癖をつけるようにしてください。

.. % % There are tools which use docstrings to automatically produce online
.. % % or printed documentation, or to let the user interactively browse
.. % % through code; it's good practice to include docstrings in code that
.. % % you write, so try to make a habit of it.

関数を *実行 (execution)* すると、関数のローカル変数のために 使われる新たなシンボルテーブル (symbol table) が取り込まれます。
もっと正確にいうと、関数内で変数への代入を行うと、その値はすべて このローカルなシンボルテーブルに記憶されます; 一方、変数の参照を
行うと、まずローカルなシンボルテーブルが検索され、その後グローバル なシンボルテーブルを調べ、最後に組み込みの名前テーブルを調べます。
従って、関数の中では、グローバルな変数を参照することはできますが、 直接値を代入することは (:keyword:`global` 文で名前を挙げておかない限り)
できません。

.. % % The \emph{execution} of a function introduces a new symbol table used
.. % % for the local variables of the function.  More precisely, all variable
.. % % assignments in a function store the value in the local symbol table;
.. % % whereas variable references first look in the local symbol table, then
.. % % in the global symbol table, and then in the table of built-in names.
.. % % Thus,  global variables cannot be directly assigned a value within a
.. % % function (unless named in a \keyword{global} statement), although
.. % % they may be referenced.

関数を呼び出す際の実際のパラメタ (引数) は、関数が呼び出されるときに 関数のローカルなシンボルテーブル内に取り込まれます; そうすることで、 引数は
*値渡し (call by value)* で関数に渡されることになります (ここでの *値 (value)* とは常にオブジェクトへの *参照
(reference)* をいい、オブジェクトの値そのものでは ありません)  [#]_ 。 ある関数がほかの関数を呼び出すときには、新たな呼び出しのために
ローカルなシンボルテーブルが新たに作成されます。

.. % % The actual parameters (arguments) to a function call are introduced in
.. % % the local symbol table of the called function when it is called; thus,
.. % % arguments are passed using \emph{call by value} (where the
.. % % \emph{value} is always an object \emph{reference}, not the value of
.. % % the object).\footnote{
.. % %          Actually, \emph{call by object reference} would be a better
.. % %          description, since if a mutable object is passed, the caller
.. % %          will see any changes the callee makes to it (items
.. % %          inserted into a list).
.. % % } When a function calls another function, a new local symbol table is
.. % % created for that call.

関数の定義を行うと、関数名は現在のシンボルテーブル内に取り入れられます。 関数名の値は、インタプリタからはユーザ定義関数 (user-defined
function) として認識される型を持ちます。この値は別の名前に代入して、 その名前を後に関数として使うこともできます。
これは一般的な名前変更のメカニズムとして働きます。

.. % % A function definition introduces the function name in the current
.. % % symbol table.  The value of the function name
.. % % has a type that is recognized by the interpreter as a user-defined
.. % % function.  This value can be assigned to another name which can then
.. % % also be used as a function.  This serves as a general renaming
.. % % mechanism:

::

   >>> fib
   <function fib at 10042ed0>
   >>> f = fib
   >>> f(100)
   1 1 2 3 5 8 13 21 34 55 89

``fib`` は関数ではなく手続き (procedure) だと異論があるかも しれませんね。Python では C 言語と同様、手続きはただの関数で、
値を返さないに過ぎません。技術的に言えば、実際には手続きも ややつまらない値ですが値を返しています。この値は ``None`` と呼ばれます
(これは組み込みの名前です)。``None`` だけを 書き出そうとすると、インタプリタは通常出力を抑制します。
本当に出力したいのなら、以下のようにすると見ることができます:

.. % % You might object that \code{fib} is not a function but a procedure.  In
.. % % Python, like in C, procedures are just functions that don't return a
.. % % value.  In fact, technically speaking, procedures do return a value,
.. % % albeit a rather boring one.  This value is called \code{None} (it's a
.. % % built-in name).  Writing the value \code{None} is normally suppressed by
.. % % the interpreter if it would be the only value written.  You can see it
.. % % if you really want to:

::

   >>> print fib(0)
   None

フィボナッチ数列の数からなるリストを出力する代わりに、値を返すような 関数を書くのは簡単です:

.. % % It is simple to write a function that returns a list of the numbers of
.. % % the Fibonacci series, instead of printing it:

::

   >>> def fib2(n): #  n までのフィボナッチ級数を返す
   ...     """Return a list containing the Fibonacci series up to n."""
   ...     result = []
   ...     a, b = 0, 1
   ...     while b < n:
   ...         result.append(b)    # 下記参照
   ...         a, b = b, a+b
   ...     return result
   ... 
   >>> f100 = fib2(100)    # 関数を呼び出す
   >>> f100                # 結果を出力する
   [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

例によって、この例は Python の新しい機能を示しています:

.. % % This example, as usual, demonstrates some new Python features:

* :keyword:`return` 文では、関数から一つ値を返します。 :keyword:`return` の引数となる式がない場合、 ``None``
  が返ります。 手続きが終了したときにも ``None`` が返ります。

* 文 ``result.append(b)`` では、リストオブジェクト ``result`` の *メソッド (method)* を呼び出しています。
  メソッドとは、オブジェクトに '属している' 関数のことで、 ``obj`` を何らかのオブジェクト (式であっても構いません)、 ``methodname``
  をそのオブジェクトで定義されているメソッド名 とすると、``obj.methodname`` と書き表されます。
  異なる型は異なるメソッドを定義しています。異なる型のメソッドで 同じ名前のメソッドを持つことができ、あいまいさを生じることはありません。
  (自前のオブジェクト型とメソッドを定義することもできます。これには、 後でこのチュートリアルで述べる *クラス (class)* を使います。)
  例で示されているメソッド :meth:`append` は、リストオブジェクトで 定義されています; このメソッドはリストの末尾に新たな要素を追加します。
  この例での :meth:`append` は ``result = result + [b]`` と等価 ですが、より効率的です。


.. _tut-defining:

関数定義についてもう少し
============

可変個の引数を伴う関数を定義することもできます。引数の定義方法には 3 つの形式があり、それらを組み合わせることができます。

.. % More on Defining Functions
.. % % It is also possible to define functions with a variable number of
.. % % arguments.  There are three forms, which can be combined.


.. _tut-defaultargs:

デフォルトの引数値
---------

もっとも便利なのは、一つ以上の引数に対してデフォルトの値を指定する 形式です。この形式を使うと、定義されている引数より少ない個数の引数
で呼び出せる関数を作成します:

.. % Default Argument Values
.. % % The most useful form is to specify a default value for one or more
.. % % arguments.  This creates a function that can be called with fewer
.. % % arguments than it is defined

::

   def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
       while True:
           ok = raw_input(prompt)
           if ok in ('y', 'ye', 'yes'): return True
           if ok in ('n', 'no', 'nop', 'nope'): return False
           retries = retries - 1
           if retries < 0: raise IOError, 'refusenik user'
           print complaint

この関数は、 ``ask_ok('Do you really want to quit?')`` のようにも、 ``ask_ok('OK to
overwrite the file?', 2)`` のようにも呼び出す ことができます。

.. % % This function can be called either like this:
.. % % \code{ask_ok('Do you really want to quit?')} or like this:
.. % % \code{ask_ok('OK to overwrite the file?', 2)}.

デフォルト値は、関数が定義された時点で、関数を *定義している* 側の スコープ (scope) で評価されるので、

.. % % The default values are evaluated at the point of function definition
.. % % in the \emph{defining} scope, so that

::

   i = 5

   def f(arg=i):
       print arg

   i = 6
   f()

は ``5`` を出力します。

.. % % will print \code{5}.

**重要な警告:**  デフォルト値は 1 度だけしか評価されません。 デフォルト値がリストや辞書のような変更可能なオブジェクトの時には
その影響がでます。例えば以下の関数は、後に続く関数呼び出しで 関数に渡されている引数を累積します:

.. % % \strong{Important warning:}  The default value is evaluated only once.
.. % % This makes a difference when the default is a mutable object such as a
.. % % list or dictionary.  For example, the following function accumulates
.. % % the arguments passed to it on subsequent calls:

::

   def f(a, L=[]):
       L.append(a)
       return L

   print f(1)
   print f(2)
   print f(3)

このコードは、

.. % % This will print

::

   [1]
   [1, 2]
   [1, 2, 3]

を出力します。

後続の関数呼び出しでデフォルト値を共有したくなければ、 代わりに以下のように関数を書くことができます:

.. % % If you don't want the default to be shared between subsequent calls,
.. % % you can write the function like this instead:

::

   def f(a, L=None):
       if L is None:
           L = []
       L.append(a)
       return L


.. _tut-keywordargs:

キーワード引数
-------

関数を ``keyword = value`` という形式のキーワード引数を 使って呼び出すこともできます。例えば、以下の関数:

.. % Keyword Arguments
.. % % Functions can also be called using
.. % % keyword arguments of the form \samp{\var{keyword} = \var{value}}.  For
.. % % instance, the following function:

::

   def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
       print "-- This parrot wouldn't", action,
       print "if you put", voltage, "volts through it."
       print "-- Lovely plumage, the", type
       print "-- It's", state, "!"

は、以下のいずれの方法でも呼び出せます:

.. % % could be called in any of the following ways:

::

   parrot(1000)
   parrot(action = 'VOOOOOM', voltage = 1000000)
   parrot('a thousand', state = 'pushing up the daisies')
   parrot('a million', 'bereft of life', 'jump')

しかし、以下の呼び出しはすべて不正なものです:

.. % % but the following calls would all be invalid:

::

   parrot()                     # 必要な引数がない
   parrot(voltage=5.0, 'dead')  # キーワード引数の後に非キーワード引数がある
   parrot(110, voltage=220)     # 引数に対して値が重複している
   parrot(actor='John Cleese')  # 未知のキーワードを使用している

一般に、引数リストでは、固定引数 (positional argument) の後ろに キーワード引数を置かねばならず、キーワードは仮引数名から選ばなければ
なりません。仮引数がデフォルト値を持っているかどうかは重要では ありません。引数はいずれも一つ以上の値を受け取りません ---
同じ関数呼び出しの中では、固定引数に対応づけられた仮引数名を キーワードとして使うことはできません。この制限のために 実行が失敗する例を以下に示します。

.. % % In general, an argument list must have any positional arguments
.. % % followed by any keyword arguments, where the keywords must be chosen
.. % % from the formal parameter names.  It's not important whether a formal
.. % % parameter has a default value or not.  No argument may receive a
.. % % value more than once --- formal parameter names corresponding to
.. % % positional arguments cannot be used as keywords in the same calls.
.. % % Here's an example that fails due to this restriction:

::

   >>> def function(a):
   ...     pass
   ... 
   >>> function(0, a=0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: function() got multiple values for keyword argument 'a'

仮引数の最後に ``**name`` の形式のものがあると、 それまでの仮引数に対応したものをのぞくすべてのキーワード引数が入った 辞書 (XXX
reference: ../lib/typesmapping.html) を受け取ります。 ``**name`` は ``*name``
の形式をとる、仮引数のリスト を超えた固定引数の入ったタプルを受け取る引数 (次の節で述べます)  と組み合わせることができます。 (``*name`` は
``**name`` より前になければなりません)。 例えば、ある関数の定義を以下:

.. % % When a final formal parameter of the form \code{**\var{name}} is
.. % % present, it receives a \ulink{dictionary}{../lib/typesmapping.html}
.. % % containing all keyword arguments except for those corresponding to
.. % % a formal parameter.  This may be
.. % % combined with a formal parameter of the form
.. % % \code{*\var{name}} (described in the next subsection) which receives a
.. % % tuple containing the positional arguments beyond the formal parameter
.. % % list.  (\code{*\var{name}} must occur before \code{**\var{name}}.)
.. % % For example, if we define a function like this:

::

   def cheeseshop(kind, *arguments, **keywords):
       print "-- Do you have any", kind, '?'
       print "-- I'm sorry, we're all out of", kind
       for arg in arguments: print arg
       print '-'*40
       keys = keywords.keys()
       keys.sort()
       for kw in keys: print kw, ':', keywords[kw]

のようにすると、呼び出しは以下:

.. % % It could be called like this:

::

   cheeseshop('Limburger', "It's very runny, sir.",
              "It's really very, VERY runny, sir.",
              client='John Cleese',
              shopkeeper='Michael Palin',
              sketch='Cheese Shop Sketch')

のようになり、もちろん以下のように出力されます:

.. % % and of course it would print:

::

   -- Do you have any Limburger ?
   -- I'm sorry, we're all out of Limburger
   It's very runny, sir.
   It's really very, VERY runny, sir.
   ----------------------------------------
   client : John Cleese
   shopkeeper : Michael Palin
   sketch : Cheese Shop Sketch

キーワード引数名のリストに対して :meth:`sort` を呼び出した後に ``keywords`` 辞書の内容を出力していることに注意してください;
:meth:`sort` が呼び出されていないと、引数が出力される順番は 不確定となります。

.. % % Note that the \method{sort()} method of the list of keyword argument
.. % % names is called before printing the contents of the \code{keywords}
.. % % dictionary; if this is not done, the order in which the arguments are
.. % % printed is undefined.


.. _tut-arbitraryargs:

任意引数リスト
-------

最後に、最も使うことの少ない選択肢として、関数が任意の個数の引数で 呼び出せるよう指定する方法があります。これらの引数はタプルに
くるまれます。可変個の引数の前に、ゼロ個かそれ以上の引数があっても 構いません。

.. % Arbitrary Argument Lists
.. % % Finally, the least frequently used option is to specify that a
.. % % function can be called with an arbitrary number of arguments.  These
.. % % arguments will be wrapped up in a tuple.  Before the variable number
.. % % of arguments, zero or more normal arguments may occur.

::

   def fprintf(file, format, *args):
       file.write(format % args)


.. _tut-unpacking-arguments:

引数リストのアンパック
-----------

引数がすでにリストやタプルになっていて、個別な固定引数を要求する 関数呼び出しに渡すためにアンパックする必要がある場合には、逆の
状況が起こります。例えば、組み込み関数 :func:`range` は 引数 *start* と *stop* を別に与える必要があります。
個別に引数を与えることができない場合、関数呼び出しを ``*`` 演算子を使って書き、リストやタプルから引数をアンパック します::

   >>> range(3, 6)             # 個別の引数を使った通常の呼び出し
   [3, 4, 5] 
   >>> args = [3, 6] 
   >>> range(*args)            # リストからアンパックされた引数での呼び出し
   [3, 4, 5] 

同じやりかたで、``**``オペレータを使って辞書でもキーワード引数を  渡すことができます:

.. % % In the same fashion, dictionaries can deliver keyword arguments with the
.. % % \code{**}-operator:

::

   >>> def parrot(voltage, state='a stiff', action='voom'):
   ...     print "-- This parrot wouldn't", action,
   ...     print "if you put", voltage, "volts through it.",
   ...     print "E's", state, "!"
   ...
   >>> d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
   >>> parrot(**d)
   -- This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !


.. _tut-lambda:

ラムダ形式
-----

多くの人の要望により、Lispのような関数型プログラミング言語によくある いくつかの機能が Python に加えられました。 キーワード
:keyword:`lambda` を使うと、名前のない小さな関数を生成できます。 例えば ``lambda a, b: a+b``
は、二つの引数の和を返す関数です。 ラムダ形式 (lambda form) は、関数オブジェクトが要求されている場所
にならどこでも使うことができます。ラムダ形式は、構文上単一の式に 制限されています。意味付け的には、ラムダ形式はただ通常の関数に
構文的な糖衣をかぶせたものに過ぎません。入れ子構造になった関数定義 と同様、ラムダ形式もそれを取り囲むスコープから変数を参照することが できます。

.. % Lambda Forms
.. % % By popular demand, a few features commonly found in functional
.. % % programming languages like Lisp have been added to Python.  With the
.. % % \keyword{lambda} keyword, small anonymous functions can be created.
.. % % Here's a function that returns the sum of its two arguments:
.. % % \samp{lambda a, b: a+b}.  Lambda forms can be used wherever function
.. % % objects are required.  They are syntactically restricted to a single
.. % % expression.  Semantically, they are just syntactic sugar for a normal
.. % % function definition.  Like nested function definitions, lambda forms
.. % % can reference variables from the containing scope:

::

   >>> def make_incrementor(n):
   ...     return lambda x: x + n
   ...
   >>> f = make_incrementor(42)
   >>> f(0)
   42
   >>> f(1)
   43


.. _tut-docstrings:

ドキュメンテーション文字列
-------------

.. index::
   single: docstrings
   single: documentation strings
   single: strings, documentation

ドキュメンテーション文字列については、その内容と書式に関する 慣習ができつつあります。

.. % Documentation Strings
.. % % There are emerging conventions about the content and formatting of
.. % % documentation strings.

最初の行は、常に対象物の目的を短く簡潔にまとめたものでなくてはなりません。 簡潔に書くために、対象物の名前や型を明示する必要はありません。
名前や型は他の方法でも得られるからです (名前がたまたま関数の演算内容 を記述する動詞である場合は例外です)。
最初の行は大文字で始まり、ピリオドで終わっていなければなりません。

.. % % The first line should always be a short, concise summary of the
.. % % object's purpose.  For brevity, it should not explicitly state the
.. % % object's name or type, since these are available by other means
.. % % (except if the name happens to be a verb describing a function's
.. % % operation).  This line should begin with a capital letter and end with
.. % % a period.

ドキュメンテーション文字列中にさらに記述すべき行がある場合、 二行目は空行にし、まとめの行と残りの記述部分を視覚的に分離
します。つづく行は一つまたはそれ以上の段落で、対象物の 呼び出し規約や副作用について記述します。

.. % % If there are more lines in the documentation string, the second line
.. % % should be blank, visually separating the summary from the rest of the
.. % % description.  The following lines should be one or more paragraphs
.. % % describing the object's calling conventions, its side effects, etc.

Python のパーザは複数行にわたる Python 文字列リテラルからインデントを 剥ぎ取らないので、ドキュメントを処理するツールでは必要に応じて
インデントを剥ぎ取らなければなりません。この処理は以下の規約に従って 行います。最初の行の *後にある* 空行でない最初の行が、ドキュメント
全体のインデントの量を決めます。 (最初の行は通常、文字列を開始する クオートに隣り合っているので、インデントが文字列リテラル中に現れない ためです。)
このインデント量と "等価な" 空白が、文字列のすべての 行頭から剥ぎ取られます。インデントの量が少ない行を書いてはならないの
ですが、もしそういう行があると、先頭の空白すべてが剥ぎ取られます。 インデントの空白の大きさが等しいかどうかは、タブ文字を (通常は 8 文字の
スペースとして) 展開した後に調べられます。

.. % % The Python parser does not strip indentation from multi-line string
.. % % literals in Python, so tools that process documentation have to strip
.. % % indentation if desired.  This is done using the following convention.
.. % % The first non-blank line \emph{after} the first line of the string
.. % % determines the amount of indentation for the entire documentation
.. % % string.  (We can't use the first line since it is generally adjacent
.. % % to the string's opening quotes so its indentation is not apparent in
.. % % the string literal.)  Whitespace ``equivalent'' to this indentation is
.. % % then stripped from the start of all lines of the string.  Lines that
.. % % are indented less should not occur, but if they occur all their
.. % % leading whitespace should be stripped.  Equivalence of whitespace
.. % % should be tested after expansion of tabs (to 8 spaces, normally).

以下に複数行のドキュメンテーション文字列の例を示します:

.. % % Here is an example of a multi-line docstring:

::

   >>> def my_function():
   ...     """Do nothing, but document it.
   ... 
   ...     No, really, it doesn't do anything.
   ...     """
   ...     pass
   ... 
   >>> print my_function.__doc__
   Do nothing, but document it.

       No, really, it doesn't do anything.



.. rubric:: Footnotes

.. [#] 実際には、*オブジェクトへの参照渡し (call by object reference) *
   と書けばよいのかもしれません。というのは、変更可能なオブジェクトが 渡されると、関数の呼び出し側は、呼び出された側の関数がオブジェクト に
   (リストに値が挿入されるといった) 何らかの変更に出くわすことに なるからです。

