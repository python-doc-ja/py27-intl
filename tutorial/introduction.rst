.. _tut-informal:

**************************
形式ばらない Python の紹介
**************************

以下の例では、入力と出力は (``>>>`` や ``...``) といったプロンプトがあるかないかで区別します: 例どおりに実行するなら、
プロンプトが表示されているときに、例中のプロンプトよりも後ろの内容全てをタイプ入力しなければなりません; プロンプトが先頭にない行はインタプリタ
からの出力です  [#]_ 。

例中には二次プロンプトだけが表示されている行がありますが、これは空行を入力しなければならないことを意味するので注意してください;
空行の入力は複数の行からなる命令の終わりをインタプリタに教えるために使われます。

このマニュアルにある例の多くは、対話プロンプトで入力されるものでもコメントを含んでいます。
Python におけるコメント文はハッシュ文字 ``#`` で始まり、物理行の終わりまで続きます。
コメントは行の先頭にも、空白やコードの後にも書くことができますが、文字列リテラル (string literal)
の内部に置くことはできません。文字列リテラル中のハッシュ文字はただのハッシュ文字です。

コメントはコードを明快にするためのものであり、Pythonはコメントを解釈しません。
なので、コードサンプルを実際に入力して試して見るときは、コメントをを省いても大丈夫です。

例::

   # これは１番目のコメント
   SPAM = 1                 # そしてこれは２番目のコメント
                            # ... そしてこれは３番目!
   STRING = "# これはコメントではありません。"


.. _tut-calculator:

Python を電卓として使う
=======================

それでは、簡単な Python コマンドをいくつか試しましょう。インタプリタを起動して、一次プロンプト、 ``>>>`` が現れるのを待ちます。
(そう長くはかからないはずです)

.. % Using Python as a Calculator
.. % % Let's try some simple Python commands.  Start the interpreter and wait
.. % % for the primary prompt, \samp{>>>~}.  (It shouldn't take long.)


.. _tut-numbers:

数
--

インタプリタは単純な電卓のように動作します:  式をタイプ入力することができ、その結果が書き出されます。式の文法は素直なものです: 演算子 ``+``,
``-``, ``*``, ``/``  は (Pascal や C といった) 他のほとんどの言語と同じように動作します。
括弧をグループ化に使うこともできます。例えば:

.. % Numbers
.. % % The interpreter acts as a simple calculator: you can type an
.. % % expression at it and it will write the value.  Expression syntax is
.. % % straightforward: the operators \code{+}, \code{-}, \code{*} and
.. % % \code{/} work just like in most other languages (for example, Pascal
.. % % or C); parentheses can be used for grouping.  For example:

::

   >>> 2+2
   4
   >>> # これはコメント
   ... 2+2
   4
   >>> 2+2  # そしてこれはコードと同じ行にあるコメント
   4
   >>> (50-5*6)/4
   5
   >>> # 整数の除算は floor (実数の解を越えない最大の整数) を返す:
   ... 7/3
   2
   >>> 7/-3
   -3

等号 (``'='``) は変数に値を代入するときに使います。代入を行っても、その結果が次のプロンプトの前に出力されたりはしません:

.. % +The equal sign (\character{=}) is used to assign a value to a variable.
.. % +Afterwards, no result is displayed before the next interactive prompt:
.. % % Like in C, the equal sign (\character{=}) is used to assign a value to a
.. % % variable.  The value of an assignment is not written:

::

   >>> width = 20
   >>> height = 5*9
   >>> width * height
   900

複数の変数に同時に値を代入することができます:

.. % % A value can be assigned to several variables simultaneously:

::

   >>> x = y = z = 0  # x と y と z をゼロにする
   >>> x
   0
   >>> y
   0
   >>> z
   0

変数は、利用する前に(値を代入することにより) "定義" しなければなりません。
定義していない変数を利用しようとするとエラーが発生します。 ::

   >>> # try to access an undefined variable
   ... n
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   NameError: name 'n' is not defined

浮動小数点は完全にサポートしています; 被演算子の型が混合されているときには、演算子は整数の被演算子を浮動小数点型に変換します。

.. % % There is full support for floating point; operators with mixed type
.. % % operands convert the integer operand to floating point:

::

   >>> 3 * 3.75 / 1.5
   7.5
   >>> 7.0 / 2
   3.5

複素数もサポートされています。虚数は接尾辞 ``j`` または ``J`` を付けて書き表します。ゼロでない実数部をもつ複素数は
``(real+imagj)`` のように書き表すか、 ``complex(real, imag)`` 関数で生成できます。

.. % % Complex numbers are also supported; imaginary numbers are written with
.. % % a suffix of \samp{j} or \samp{J}.  Complex numbers with a nonzero
.. % % real component are written as \samp{(\var{real}+\var{imag}j)}, or can
.. % % be created with the \samp{complex(\var{real}, \var{imag})} function.

::

   >>> 1j * 1J
   (-1+0j)
   >>> 1j * complex(0,1)
   (-1+0j)
   >>> 3+1j*3
   (3+3j)
   >>> (3+1j)*3
   (9+3j)
   >>> (1+2j)/(1+1j)
   (1.5+0.5j)

複素数は、常に実部と虚部に相当する二つの浮動小数点数で表されます。複素数 *z* からそれぞれの部分を取り出すには、 ``z.real``  と
``z.imag`` を使います。

.. % % Complex numbers are always represented as two floating point numbers,
.. % % the real and imaginary part.  To extract these parts from a complex
.. % % number \var{z}, use \code{\var{z}.real} and \code{\var{z}.imag}.

::

   >>> a=1.5+0.5j
   >>> a.real
   1.5
   >>> a.imag
   0.5

数値を浮動小数点数や整数へに変換する関数 (:func:`float`,  :func:`int`, :func:`long`) は複素数に対しては動作しません
---  複素数を実数に変換する方法には、ただ一つの正解というものがないからです。絶対値 (magnitude) を (浮動小数点数として) 得るには
``abs(z)`` を使い、実部を得るには ``z.real`` を使ってください。

.. % % The conversion functions to floating point and integer
.. % % (\function{float()}, \function{int()} and \function{long()}) don't
.. % % work for complex numbers --- there is no one correct way to convert a
.. % % complex number to a real number.  Use \code{abs(\var{z})} to get its
.. % % magnitude (as a float) or \code{z.real} to get its real part.

::

   >>> a=3.0+4.0j
   >>> float(a)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: can't convert complex to float; use abs(z)
   >>> a.real
   3.0
   >>> a.imag
   4.0
   >>> abs(a)  # sqrt(a.real **2 + a.imag** 2)
   5.0
   >>>

対話モードでは、最後に印字された式は変数 ``_`` に代入されます。このことを利用すると、 Python を電卓として使うときに、計算を連続して
行う作業が多少楽になります。以下に例を示します:

.. % % In interactive mode, the last printed expression is assigned to the
.. % % variable \code{_}.  This means that when you are using Python as a
.. % % desk calculator, it is somewhat easier to continue calculations, for
.. % % example:

::

   >>> tax = 12.5 / 100
   >>> price = 100.50
   >>> price * tax
   12.5625
   >>> price + _
   113.0625
   >>> round(_, 2)
   113.06
   >>>

ユーザはこの変数を読取り専用の値として扱うべきです。この変数に明示的な代入を行ってはいけません --- そんなことをすれば、
この組み込み変数と同じ名前で、元の組み込み変数の不思議な動作を覆い隠してしまうような、別個のローカルな変数が生成されてしまいます。

.. % % This variable should be treated as read-only by the user.  Don't
.. % % explicitly assign a value to it --- you would create an independent
.. % % local variable with the same name masking the built-in variable with
.. % % its magic behavior.


.. _tut-strings:

文字列
------

数のほかに、Python は文字列も操作できます。文字列はいくつもの方法で表現できます。文字列はシングルまたはダブルのクォートで囲みます。

.. % Strings
.. % % Besides numbers, Python can also manipulate strings, which can be
.. % % expressed in several ways.  They can be enclosed in single quotes or
.. % % double quotes:

::

   >>> 'spam eggs'
   'spam eggs'
   >>> 'doesn\'t'
   "doesn't"
   >>> "doesn't"
   "doesn't"
   >>> '"Yes," he said.'
   '"Yes," he said.'
   >>> "\"Yes,\" he said."
   '"Yes," he said.'
   >>> '"Isn\'t," she said.'
   '"Isn\'t," she said.'

文字列リテラルはいくつかの方法で複数行にまたがって記述できます。継続行を使うことができ、これには行の末尾の文字を
バックスラッシュにします。こうすることで、次の行が現在の行と論理的に継続していることを示します:

.. % % String literals can span multiple lines in several ways.  Continuation
.. % % lines can be used, with a backslash as the last character on the line
.. % % indicating that the next line is a logical continuation of the line:

::

   hello = "This is a rather long string containing\n\
   several lines of text just as you would do in C.\n\
       Note that whitespace at the beginning of the line is\
    significant."

   print hello

``\n`` を使って文字列に改行位置を埋め込まなくてはならないことに注意してください; 末尾のバックスラッシュの後ろにある改行文字は無視されます。
従って、上の例は以下のような出力を行います:

.. % % Note that newlines would still need to be embedded in the string using
.. % % \code{\e n}; the newline following the trailing backslash is
.. % % discarded.  This example would print the following:

::

   This is a rather long string containing
   several lines of text just as you would do in C.
       Note that whitespace at the beginning of the line is significant.

また、対になった三重クォート ``"""`` または ``'''`` で文字列を囲むこともできます。
三重クォートを使っているときには、行末をエスケープする必要はありません、しかし、行末の改行文字も文字列に含まれることになります。
::

   print """
   Usage: thingy [OPTIONS]
        -h                        Display this usage message
        -H hostname               Hostname to connect to
   """

は以下のような出力を行います。 ::

   Usage: thingy [OPTIONS]
        -h                        Display this usage message
        -H hostname               Hostname to connect to

文字列リテラルを "raw" 文字列にすると、 ``\n`` のようなエスケープシーケンスは改行に変換されません。逆に、行末のバックスラッシュ
やソースコード中の改行文字が文字列データに含められます。つまり、以下の例:

.. % % If we make the string literal a ``raw'' string, however, the
.. % % \code{\e n} sequences are not converted to newlines, but the backslash
.. % % at the end of the line, and the newline character in the source, are
.. % % both included in the string as data.  Thus, the example:

::

   hello = r"This is a rather long string containing\n\
   several lines of text much as you would do in C."

   print hello

は、以下のような出力を行います:

.. % % would print:

::

   This is a rather long string containing\n\
   several lines of text much as you would do in C.

インタプリタは、文字列演算の結果を、タイプ入力する時のと同じ方法で出力します: 文字列はクオート文字で囲い、クオート文字自体やその他の
奇妙な文字は、正しい文字が表示されるようにするためにバックスラッシュでエスケープします。
文字列がシングルクオートを含み、かつダブルクオートを含まない場合には、全体をダブルクオートで囲います。そうでない場合にはシングルクオートで囲みます。
(後で述べる :keyword:`print` を使って、クオートやエスケープのない文字列を書くことができます。)

.. % % The interpreter prints the result of string operations in the same way
.. % % as they are typed for input: inside quotes, and with quotes and other
.. % % funny characters escaped by backslashes, to show the precise
.. % % value.  The string is enclosed in double quotes if the string contains
.. % % a single quote and no double quotes, else it's enclosed in single
.. % % quotes.  (The \keyword{print} statement, described later, can be used
.. % % to write strings without quotes or escapes.)

文字列は ``+`` 演算子で連結させる (くっつけて一つにする) ことができ、 ``*`` 演算子で反復させることができます。

.. % % Strings can be concatenated (glued together) with the
.. % % \code{+} operator, and repeated with \code{*}:

::

   >>> word = 'Help' + 'A'
   >>> word
   'HelpA'
   >>> '<' + word*5 + '>'
   '<HelpAHelpAHelpAHelpAHelpA>'

互いに隣あった二つの文字列リテラルは自動的に連結されます: 例えば、上記の最初の行は ``word = 'Help' 'A'`` と書くこともできました;
この機能は二つともリテラルの場合にのみ働くもので、任意の文字列表現で使うことができるわけではありません。

.. % % Two string literals next to each other are automatically concatenated;
.. % % the first line above could also have been written \samp{word = 'Help'
.. % % 'A'}; this only works with two literals, not with arbitrary string
.. % % expressions:

::

   >>> 'str' 'ing'             #  <-  これは ok
   'string'
   >>> 'str'.strip() + 'ing'   #  <-  これは ok
   'string'
   >>> 'str'.strip() 'ing'     #  <-  これはダメ
     File "<stdin>", line 1, in ?
       'str'.strip() 'ing'
                     ^
   SyntaxError: invalid syntax

文字列は添字表記 (インデクス表記) することができます;  C 言語と同じく、文字列の最初の文字の添字 (インデクス) は 0 となります。
独立した文字型というものはありません; 単一の文字は、単にサイズが 1 の文字列です。Icon 言語と同じく、部分文字列を  *スライス表記*:
コロンで区切られた二つのインデクスで指定することができます。

.. % % Strings can be subscripted (indexed); like in C, the first character
.. % % of a string has subscript (index) 0.  There is no separate character
.. % % type; a character is simply a string of size one.  Like in Icon,
.. % % substrings can be specified with the \emph{slice notation}: two indices
.. % % separated by a colon.

::

   >>> word[4]
   'A'
   >>> word[0:2]
   'He'
   >>> word[2:4]
   'lp'

スライスのインデクスには便利なデフォルト値があります; 最初のインデクスを省略すると、0 と見なされます。第 2
のインデクスを省略すると、スライスしようとする文字列のサイズとみなされます。

.. % % Slice indices have useful defaults; an omitted first index defaults to
.. % % zero, an omitted second index defaults to the size of the string being
.. % % sliced.

::

   >>> word[:2]    # 最初の 2 文字
   'He'
   >>> word[2:]    # 最初の 2 文字を除くすべて
   'lpA'

C 言語の文字列と違い、Python の文字列は変更できません。インデクス指定された文字列中のある位置に代入を行おうとするとエラーになります:

.. % % Unlike a C string, Python strings cannot be changed.  Assigning to an
.. % % indexed position in the string results in an error:

::

   >>> word[0] = 'x'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: object doesn't support item assignment
   >>> word[:1] = 'Splat'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: object doesn't support slice assignment

一方、要素どうしを組み合わせた新たな文字列の生成は、簡単で効率的です:

.. % % However, creating a new string with the combined content is easy and
.. % % efficient:

::

   >>> 'x' + word[1:]
   'xelpA'
   >>> 'Splat' + word[4]
   'SplatA'

スライス演算には便利な不変式があります:  ``s[:i] + s[i:]`` は ``s`` に等しくなります。

.. % % Here's a useful invariant of slice operations:
.. % % \code{s[:i] + s[i:]} equals \code{s}.

::

   >>> word[:2] + word[2:]
   'HelpA'
   >>> word[:3] + word[3:]
   'HelpA'

スライス表記に行儀の悪いインデクス指定をしても、値はたしなみよく処理されます: インデクスが大きすぎる場合は文字列のサイズと置き換えられます。
スライスの下境界 (文字列の左端) よりも小さいインデクス値を上境界 (文字列の右端) に指定すると、空文字列が返されます。

.. % % Degenerate slice indices are handled gracefully: an index that is too
.. % % large is replaced by the string size, an upper bound smaller than the
.. % % lower bound returns an empty string.

::

   >>> word[1:100]
   'elpA'
   >>> word[10:]
   ''
   >>> word[2:1]
   ''

インデクスを負の数にして、右から数えることもできます。例えば:

.. % % Indices may be negative numbers, to start counting from the right.
.. % % For example:

::

   >>> word[-1]     # 末尾の文字
   'A'
   >>> word[-2]     # 末尾から 2 つめの文字
   'p'
   >>> word[-2:]    # 末尾の 2 文字
   'pA'
   >>> word[:-2]    # 末尾の 2 文字を除くすべて
   'Hel'

-0 は 0 と全く同じなので、右から数えることができません。注意してください!

.. % % But note that -0 is really the same as 0, so it does not count from
.. % % the right!

::

   >>> word[-0]     # (-0 は 0 に等しい)
   'H'

負で、かつ範囲外のインデクスをスライス表記で行うと、インデクスは切り詰められます。しかし、単一の要素を指定する (スライスでない)
インデクス指定でこれを行ってはいけません:

.. % % Out-of-range negative slice indices are truncated, but don't try this
.. % % for single-element (non-slice) indices:

::

   >>> word[-100:]
   'HelpA'
   >>> word[-10]    # エラー
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   IndexError: string index out of range

スライスの働きかたをおぼえる良い方法は、インデクスが文字と文字の *あいだ (between)* を指しており、最初の文字の左端が 0
になっていると考えることです。そうすると、 *n* 文字からなる文字列中の最後の文字の右端はインデクス *n* となります。例えば:

.. % % The best way to remember how slices work is to think of the indices as
.. % % pointing \emph{between} characters, with the left edge of the first
.. % % character numbered 0.  Then the right edge of the last character of a
.. % % string of \var{n} characters has index \var{n}, for example:

::

    +---+---+---+---+---+
    | H | e | l | p | A |
    +---+---+---+---+---+
    0   1   2   3   4   5
   -5  -4  -3  -2  -1

といった具合です。

数が記された行のうち、最初の方の行は、文字列中のインデクス 0...5 の位置を表します; 次の行は、対応する負のインデクスを表しています。 *i* から
*j* までのスライスは、それぞれ *i*, *j*  とラベル付けされたけられた端点間のすべての文字からなります。

.. % % The first row of numbers gives the position of the indices 0...5 in
.. % % the string; the second row gives the corresponding negative indices.
.. % % The slice from \var{i} to \var{j} consists of all characters between
.. % % the edges labeled \var{i} and \var{j}, respectively.

非負のインデクス対の場合、スライスされたシーケンスの長さは、スライスの両端のインデクスが境界内にあるかぎり、インデクス間の差になります。例えば、
``word[1:3]`` の長さは 2 になります。

.. % % For non-negative indices, the length of a slice is the difference of
.. % % the indices, if both are within bounds.  For example, the length of
.. % % \code{word[1:3]} is 2.

組込み関数 :func:`len` は文字列の長さ (length) を返します。

.. % % The built-in function \function{len()} returns the length of a string:

::

   >>> s = 'supercalifragilisticexpialidocious'
   >>> len(s)
   34


.. seealso::

   :ref:`typesseq`
      次節で記述されている文字列および Unicode 文字列は *シーケンス型* の例であり、
      シーケンス型でサポートされている共通の操作をサポートしています。

   :ref:`string-methods`
      (バイト)文字列や Unicode 文字列では、基本的な変換や検索を行うための
      数多くのメソッドをサポートしています。

   :ref:`new-string-formatting`
      :meth:`str.format` を使った文字列のフォーマットについて、ここで解説されています。

   :ref:`string-formatting`
      (バイト)文字列や Unicode 文字列が ``%`` 演算子の左オペランドである場合に
      呼び出される(古い)フォーマット操作については、ここで詳しく記述されています。


.. _tut-unicodestrings:

Unicode 文字列
--------------

.. sectionauthor:: Marc-Andre Lemburg <mal@lemburg.com>


.. % Unicode Strings

Python 2.0 から、プログラマはテキスト・データを格納するための新しいデータ型、Unicode オブジェクトを利用できるようになりました。
Unicode オブジェクトを使うと、Unicode データ (http://www.unicode.org/ 参照)
を記憶したり、操作したりできます。また、 Unicode オブジェクトは既存の文字列オブジェクトとよく統合していて、必要に応じた自動変換機能を
提供しています。

.. % % Starting with Python 2.0 a new data type for storing text data is
.. % % available to the programmer: the Unicode object. It can be used to
.. % % store and manipulate Unicode data (see \url{http://www.unicode.org/})
.. % % and integrates well with the existing string objects providing
.. % % auto-conversions where necessary.

Unicode には、古今のテキストで使われているあらゆる書き文字のあらゆる文字について、対応付けを行うための一つの序数を規定しているという利点があります。
これまでは、書き文字のために利用可能な序数は 256 個しかなく、テキストは書き文字の対応付けを行っているコードページに束縛されているのが通常でした。
このことは、とりわけソフトウェアの国際化 (通常 ``i18n`` --- ``'i'`` + 18 文字 + ``'n'`` の意) に対して大きな
混乱をもたらしました。Unicode では、すべての書き文字に対して単一のコードページを定義することで、これらの問題を解決しています。

.. % % Unicode has the advantage of providing one ordinal for every character
.. % % in every script used in modern and ancient texts. Previously, there
.. % % were only 256 possible ordinals for script characters and texts were
.. % % typically bound to a code page which mapped the ordinals to script
.. % % characters. This lead to very much confusion especially with respect
.. % % to internationalization (usually written as \samp{i18n} ---
.. % % \character{i} + 18 characters + \character{n}) of software.  Unicode
.. % % solves these problems by defining one code page for all scripts.

Python では、Unicode 文字列の作成は通常の文字列を作成するのと同じように単純なものです:

.. % % Creating Unicode strings in Python is just as simple as creating
.. % % normal strings:

::

   >>> u'Hello World !'
   u'Hello World !'

クオートの前にある小文字の ``'u'`` は、Unicode 文字列を生成することになっていることを示します。文字列に特殊な文字を
含めたければ、Python の *Unicode-Escape* エンコーディングを使って行えます。以下はその方法を示しています:

.. % % The small \character{u} in front of the quote indicates that an
.. % % Unicode string is supposed to be created. If you want to include
.. % % special characters in the string, you can do so by using the Python
.. % % \emph{Unicode-Escape} encoding. The following example shows how:

::

   >>> u'Hello\u0020World !'
   u'Hello World !'

エスケープシーケンス ``\u0020`` は、序数の値 0x0020 を持つ  Unicode 文字 (スペース文字) を、指定場所に挿入することを示します。

.. % % The escape sequence \code{\e u0020} indicates to insert the Unicode
.. % % character with the ordinal value 0x0020 (the space character) at the
.. % % given position.

他の文字は、それぞれの序数値をそのまま Unicode の序数値に用いて解釈されます。多くの西洋諸国で使われている標準 Latin-1 エンコーディング
のリテラル文字列があれば、Unicode の下位 256 文字が Latin-1 の 256  文字と同じになっていて便利だと思うことでしょう。

.. % % Other characters are interpreted by using their respective ordinal
.. % % values directly as Unicode ordinals.  If you have literal strings
.. % % in the standard Latin-1 encoding that is used in many Western countries,
.. % % you will find it convenient that the lower 256 characters
.. % % of Unicode are the same as the 256 characters of Latin-1.

上級者のために、通常の文字列の場合と同じく raw モードもあります。
これには、文字列を開始するクオート文字の前に 'ur' を付けて、 Python に
*Raw-Unicode-Escape* エンコーディングを使わせなければなりません。
このモードでは、上記の ``\uXXXX`` の変換は、小文字の
'u' の前に奇数個のバックスラッシュがあるときにだけ適用されます。

.. % % For experts, there is also a raw mode just like the one for normal
.. % % strings. You have to prefix the opening quote with 'ur' to have
.. % % Python use the \emph{Raw-Unicode-Escape} encoding. It will only apply
.. % % the above \code{\e uXXXX} conversion if there is an uneven number of
.. % % backslashes in front of the small 'u'.

::

   >>> ur'Hello\u0020World !'
   u'Hello World !'
   >>> ur'Hello\\u0020World !'
   u'Hello\\\\u0020World !'

raw モードは、正規表現を記述する時のように、沢山のバックスラッシュを入力しなければならないときとても役に立ちます。

.. % % The raw mode is most useful when you have to enter lots of
.. % % backslashes, as can be necessary in regular expressions.

これら標準のエンコーディングにとは別に、Python では、既知の文字エンコーディングに基づいて Unicode 文字列を生成する一連の
手段を提供しています。

.. % % Apart from these standard encodings, Python provides a whole set of
.. % % other ways of creating Unicode strings on the basis of a known
.. % % encoding.

.. index:: builtin: unicode

組込み関数 :func:`unicode` は、登録されているすべての Unicode codecs (COder: エンコーダと DECoder
デコーダ) へのアクセス機能を提供します。codecs が変換できるエンコーディングには、よく知られているものとして *Latin-1*, *ASCII*,
*UTF-8* および *UTF-16* があります。後者の二つは可変長のエンコードで、各 Unicode 文字を 1
バイトまたはそれ以上のバイト列に保存します。デフォルトのエンコーディングは通常 ASCIIに設定されています。ASCIIでは 0 から 127 の範囲の
文字だけを通過させ、それ以外の文字は受理せずエラーを出します。 Unicode 文字列を印字したり、ファイルに書き出したり、 :func:`str`
で変換すると、デフォルトのエンコーディングを使った変換が行われます。

.. % % The built-in function \function{unicode()}\bifuncindex{unicode} provides
.. % % access to all registered Unicode codecs (COders and DECoders). Some of
.. % % the more well known encodings which these codecs can convert are
.. % % \emph{Latin-1}, \emph{ASCII}, \emph{UTF-8}, and \emph{UTF-16}.
.. % % The latter two are variable-length encodings that store each Unicode
.. % % character in one or more bytes. The default encoding is
.. % % normally set to \ASCII, which passes through characters in the range
.. % % 0 to 127 and rejects any other characters with an error.
.. % % When a Unicode string is printed, written to a file, or converted
.. % % with \function{str()}, conversion takes place using this default encoding.

::

   >>> u"abc"
   u'abc'
   >>> u"あいう"
   u'\x82\xa0\x82\xa2\x82\xa4'
   >>> str(u"あいう")
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-5: 
   ordinal not in range(128)

特定のエンコーディングを使って Unicode 文字列を 8 ビットの文字列に変換するために、Unicode オブジェクトでは :func:`encode`
メソッドを提供しています。このメソッドは単一の引数としてエンコーディングの名前をとります。エンコーディング名には小文字の使用が推奨されています。

.. % % To convert a Unicode string into an 8-bit string using a specific
.. % % encoding, Unicode objects provide an \function{encode()} method
.. % % that takes one argument, the name of the encoding.  Lowercase names
.. % % for encodings are preferred.

::

   >>> u"あいう".encode('utf-8')
   '\xc2\x82\xc2\xa0\xc2\x82\xc2\xa2\xc2\x82\xc2\xa4'

特定のエンコーディングで書かれているデータがあり、そこから Unicode 文字列を生成したいなら、 :func:`unicode` を使い、第 2
引数にエンコーディング名を指定します。

.. % % If you have data in a specific encoding and want to produce a
.. % % corresponding Unicode string from it, you can use the
.. % % \function{unicode()} function with the encoding name as the second
.. % % argument.

::

   unicode('\xc2\x82\xc2\xa0\xc2\x82\xc2\xa2\xc2\x82\xc2\xa4', 'utf-8')
   u'\x82\xa0\x82\xa2\x82\xa4'


.. _tut-lists:

リスト
------

Python は数多くの *複合 (compound)* データ型を備えており、別々の値を一まとめにするために使えます。最も汎用的なデータ型は *リスト
(list) * で、コンマで区切られた値からなるリストを各カッコで囲んだものとして書き表されます。リストの要素をすべて同じ型にする必要はありません。

.. % Lists
.. % % Python knows a number of \emph{compound} data types, used to group
.. % % together other values.  The most versatile is the \emph{list}, which
.. % % can be written as a list of comma-separated values (items) between
.. % % square brackets.  List items need not all have the same type.

::

   >>> a = ['spam', 'eggs', 100, 1234]
   >>> a
   ['spam', 'eggs', 100, 1234]

文字列のインデクスと同じく、リストのインデクスは 0 から開始します。また、スライス、連結なども行えます:

.. % % Like string indices, list indices start at 0, and lists can be sliced,
.. % % concatenated and so on:

::

   >>> a[0]
   'spam'
   >>> a[3]
   1234
   >>> a[-2]
   100
   >>> a[1:-1]
   ['eggs', 100]
   >>> a[:2] + ['bacon', 2*2]
   ['spam', 'eggs', 'bacon', 4]
   >>> 3*a[:3] + ['Boo!']
   ['spam', 'eggs', 100, 'spam', 'eggs', 100, 'spam', 'eggs', 100, 'Boo!']

*変化不可能 (immutable)* な文字列型と違い、リストは個々の要素を変更することができます。

.. % % Unlike strings, which are \emph{immutable}, it is possible to change
.. % % individual elements of a list:

::

   >>> a
   ['spam', 'eggs', 100, 1234]
   >>> a[2] = a[2] + 23
   >>> a
   ['spam', 'eggs', 123, 1234]

スライスに代入することもできます。スライスの代入を行って、リストのサイズを変更したり、完全に消すことさえできます:

.. % % Assignment to slices is also possible, and this can even change the size
.. % % of the list or clear it entirely:

::

   >>> # いくつかの項目を置換する:
   ... a[0:2] = [1, 12]
   >>> a
   [1, 12, 123, 1234]
   >>> # いくつかの項目を除去する:
   ... a[0:2] = []
   >>> a
   [123, 1234]
   >>> # いくつかの項目を挿入する:
   ... a[1:1] = ['bletch', 'xyzzy']
   >>> a
   [123, 'bletch', 'xyzzy', 1234]
   >>> # それ自身 (のコピー) を先頭に挿入する
   >>> a[:0] = a    
   >>> a
   [123, 'bletch', 'xyzzy', 1234, 123, 'bletch', 'xyzzy', 1234]
   >>> # リストをクリアする: 全てのアイテムを空のリストに置換する
   >>> a[:] = []
   >>> a
   []

組込み関数 :func:`len` はリストにも適用できます。

.. % % The built-in function \function{len()} also applies to lists:

::

   >>> a = ['a', 'b', 'c', 'd']
   >>> len(a)
   4

リストを入れ子にする (ほかのリストを含むリストを造る) ことも可能です。例えば、

.. % % It is possible to nest lists (create lists containing other lists),
.. % % for example:

::

   >>> q = [2, 3]
   >>> p = [1, q, 4]
   >>> len(p)
   3
   >>> p[1]
   [2, 3]
   >>> p[1][0]
   2
   >>> p[1].append('xtra')     # 5.1節を参照
   >>> p
   [1, [2, 3, 'xtra'], 4]
   >>> q
   [2, 3, 'xtra']

最後の例では、 ``p[1]`` と ``q`` が実際には同一のオブジェクトを参照していることに注意してください!　 *オブジェクトの意味付け
(semantics)* については、後ほど触れることにします。

.. % % Note that in the last example, \code{p[1]} and \code{q} really refer to
.. % % the same object!  We'll come back to \emph{object semantics} later.


.. _tut-firststeps:

プログラミングへの第一歩
========================

もちろん、2 たす 2 よりももっと複雑な仕事にも Python を使うことができます。 *Fibonacci* 級数列の先頭の部分列は次のようにして
書くことができます:

.. % First Steps Towards Programming
.. % % Of course, we can use Python for more complicated tasks than adding
.. % % two and two together.  For instance, we can write an initial
.. % % sub-sequence of the \emph{Fibonacci} series as follows:

::

   >>> # Fibonacci 級数:
   ... # 二つの要素の和が次の要素を定義する
   ... a, b = 0, 1
   >>> while b < 10:
   ...     print b
   ...     a, b = b, a+b
   ... 
   1
   1
   2
   3
   5
   8

上の例では、いくつか新しい機能を取り入れています。

.. % % This example introduces several new features.

* 最初の行には * 複数同時の代入 (multiple assignment)* が入っています: 変数 ``a`` と ``b`` は、それぞれ同時に新しい値
  0 と 1 になっています。この代入は最後の行でも再度使われており、代入が行われる前に右辺の式がまず評価されます。右辺の式は左から右へと
  順番に評価されます。

* :keyword:`while` は、条件 (ここでは ``b < 10``) が真である限り実行を繰り返し (ループし) ます。Python では、C
  言語と同様に、ゼロでない整数値は真となり、ゼロは偽です。条件式は文字列値やリスト値、実際には任意のシーケンス型でもかまいません。例中で使われている条件テスト
  は単なる比較です。標準的な比較演算子は C 言語と同様です: すなわち、 ``<`` (より小さい)、 ``>`` (より大きい)、 ``==`` (等しい)、
  ``<=`` (より小さいか等しい)、 ``>=`` (より大きいか等しい)、および ``!=`` (等しくない) 、です。

* ループの* 本体 (body)* は* インデント (indent, 字下げ)*  されています: インデントは Python
  において実行文をグループにまとめる方法です。Python は (いまだに!) 賢い入力行編集機能を提供していないので、
  インデントされた各行を入力するにはタブや (複数個の) スペースを使わなければなりません。実際には、Python へのより複雑な入力を準備する
  にはテキストエディタを使うことになるでしょう; ほとんどのテキストエディタは自動インデント機能を持っています。
  複合文を対話的に入力するときには、(パーザはいつ最後の行を入力したのか推し量ることができないので) 入力の完了を示すために最後に空行を
  続けなければなりません。基本ブロックの各行は同じだけインデントされていなければならないので注意してください。

* :keyword:`print` は指定した (1 つまたは複数の) 式の値を書き出します。 :keyword:`print` は、(電卓の例でしたように)
  単に値を出力したい式を書くのとは、複数の式や文字列を扱う方法が違います。文字列は引用符無しで出力され、複数の要素の間にはスペースが挿入されるので、
  以下のように出力をうまく書式化できます。 ::

     >>> i = 256*256
     >>> print 'The value of i is', i
     The value of i is 65536

  末尾にコンマを入れると、出力を行った後に改行されません:

  .. % % A trailing comma avoids the newline after the output:

  ::

     >>> a, b = 0, 1
     >>> while b < 1000:
     ...     print b,
     ...     a, b = b, a+b
     ...
     1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987

  インタプリタは、最後に入力した行がまだ完全な文になっていない場合、
  改行をはさんで次のプロンプトを出力することに注意してください。

  .. % % Note that the interpreter inserts a newline before it prints the next
  .. % % prompt if the last line was not completed.

