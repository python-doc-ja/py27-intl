.. _tut-io:

*****
入力と出力
*****

プログラムの出力をもたらす方法はいくつかあります; データは人間が可読 な形で出力することも、将来使うためにファイルに書くこともできます。
この章では、こうした出力のいくつかの可能性について議論します。

.. % Input and Output
.. % % There are several ways to present the output of a program; data can be
.. % % printed in a human-readable form, or written to a file for future use.
.. % % This chapter will discuss some of the possibilities.


.. _tut-formatting:

ファンシーな出力の書式化
============

これまでのところ、値を出力する二つの方法: *式でできた文 (expression statement)* と :keyword:`print`
文が出てきました。(第三は ファイルオブジェクトの :meth:`write` を使う方法です; 標準出力 を表すファイルは ``sys.stdout``
で参照できます。詳細は ライブラリリファレンスを参照してください。)

.. % Fancier Output Formatting
.. % % So far we've encountered two ways of writing values: \emph{expression
.. % % statements} and the \keyword{print} statement.  (A third way is using
.. % % the \method{write()} method of file objects; the standard output file
.. % % can be referenced as \code{sys.stdout}.  See the Library Reference for
.. % % more information on this.)

.. index:: module: string

出力を書式化する際に、単に値をスペースで区切って出力するよりも もっときめ細かな制御をしたいと思うことがしばしばあるでしょう。
出力を書式化するには二つの方法があります; 第一の方法は、全ての 文字列を自分で処理するというものです; 文字列のスライスや結合といった操作を
使えば、思い通りのレイアウトを作成することができます。 標準モジュール :mod:`string` には、
文字列を指定されたカラム幅にそろえるための便利な操作がいくつか あります; これらの操作については後で簡単に説明します。 第二の方法は ``%``
演算子を使い、文字列を演算子の左引数 (left argument) として使う方法です。``%`` 演算子は、左引数を :cfunc:`sprintf`
のような形式で解釈して右引数に適用し、 その書式化操作で得られた文字列を返します。

.. % % Often you'll want more control over the formatting of your output than
.. % % simply printing space-separated values.  There are two ways to format
.. % % your output; the first way is to do all the string handling yourself;
.. % % using string slicing and concatenation operations you can create any
.. % % lay-out you can imagine.  The standard module
.. % % \module{string}\refstmodindex{string} contains some useful operations
.. % % for padding strings to a given column width; these will be discussed
.. % % shortly.  The second way is to use the \code{\%} operator with a
.. % % string as the left argument.  The \code{\%} operator interprets the
.. % % left argument much like a \cfunction{sprintf()}-style format
.. % % string to be applied to the right argument, and returns the string
.. % % resulting from this formatting operation.

.. % % One question remains, of course: how do you convert values to strings?
.. % % Luckily, Python has ways to convert any value to a string: pass it to
.. % % the \function{repr()}  or \function{str()} functions.  Reverse quotes
.. % % (\code{``}) are equivalent to \function{repr()}, but they are no
.. % % longer used in modern Python code and will likely not be in future
.. % % versions of the language.

もちろん、一つ問題があります。値をどうやって文字列に変換したら いいのでしょうか？幸運なことに、Python には値を文字列に変換する方法が あります: 値を
:func:`repr` か :func:`str` 関数に渡して ください。逆クオート (``````) は :func:`repr` と等しい
操作ですが、最近のPythonコードでは使われませんし、将来のバージョンには 含まれないでしょう。

:func:`str` 関数は、値を表現するときにかなり人間にとって可読な ものにするためのものです。一方、:func:`repr` は
インタプリタで読めるような表現にする (あるいは、等価な値を表現する ための構文がない場合には :exc:`SyntaxError` を送出させる)
ためのものです。 人間が利用するための特別な表現をもたないオブジェクトでは、 :func:`str` は :func:`repr` と同じ値を返します。
数値や、リストや辞書といった構造体のような多くの値は、どちらの関数でも 同じ表現になります。文字列と浮動小数点は特別で、二つの 別個の表現となります。

.. % % The \function{str()} function is meant to return representations of
.. % % values which are fairly human-readable, while \function{repr()} is
.. % % meant to generate representations which can be read by the interpreter
.. % % (or will force a \exception{SyntaxError} if there is not equivalent
.. % % syntax).  For objects which don't have a particular representation for
.. % % human consumption, \function{str()} will return the same value as
.. % % \function{repr()}.  Many values, such as numbers or structures like
.. % % lists and dictionaries, have the same representation using either
.. % % function.  Strings and floating point numbers, in particular, have two
.. % % distinct representations.

下にいくつか例を挙げます:

.. % % Some examples:

::

   >>> s = 'Hello, world.'
   >>> str(s)
   'Hello, world.'
   >>> repr(s)
   "'Hello, world.'"
   >>> str(0.1)
   '0.1'
   >>> repr(0.1)
   '0.10000000000000001'
   >>> x = 10 * 3.25
   >>> y = 200 * 200
   >>> s = 'The value of x is ' + repr(x) + ', and y is ' + repr(y) + '...'
   >>> print s
   The value of x is 32.5, and y is 40000...
   >>> # 文字列への repr() はクォートとバックスラッシュが付加される:
   ... hello = 'hello, world\n'
   >>> hellos = repr(hello)
   >>> print hellos
   'hello, world\n'
   >>> # repr() の引数は Python オブジェクトの場合もある:
   ... repr((x, y, ('spam', 'eggs')))
   "(32.5, 40000, ('spam', 'eggs'))"
   >>> # 逆クォートは対話セッショで便利である:
   ... `x, y, ('spam', 'eggs')`
   "(32.5, 40000, ('spam', 'eggs'))"

以下に 2 乗と 3 乗の値からなる表を書く二つの方法を示します:

.. % % Here are two ways to write a table of squares and cubes:

::

   >>> for x in range(1, 11):
   ...     print repr(x).rjust(2), repr(x*x).rjust(3),
   ...     # 上の行の末尾のコンマに注意
   ...     print repr(x*x*x).rjust(4)
   ...
    1   1    1
    2   4    8
    3   9   27
    4  16   64
    5  25  125
    6  36  216
    7  49  343
    8  64  512
    9  81  729
   10 100 1000
   >>> for x in range(1,11):
   ...     print '%2d %3d %4d' % (x, x*x, x*x*x)
   ... 
    1   1    1
    2   4    8
    3   9   27
    4  16   64
    5  25  125
    6  36  216
    7  49  343
    8  64  512
    9  81  729
   10 100 1000

(各カラムの間のスペース一個は :keyword:`print` の働きで追加されて いることに注意してください: :keyword:`print`
は引数間に常に 空白を追加します)

.. % % (Note that one space between each column was added by the way
.. % % \keyword{print} works: it always adds spaces between its arguments.)

この例では、メソッド :meth:`rjust` を実際に利用しています。 :meth:`rjust` は文字列を指定された幅のフィールド内に
右詰めで入るように、左に空白を追加します。同様のメソッドとして、 :meth:`ljust` と :meth:`center` が
あります。これらのメソッドは何か出力を行うわけではなく、ただ新しい文字列を 返します。入力文字列が長すぎる場合、文字列を切り詰めることはせず、
ただ値をそのまま返します; この仕様のために、カラムのレイアウトが 滅茶苦茶になるかもしれませんが、嘘の値が代わりに書き出される
よりはましです。(本当に切り詰めを行いたいのなら、全てのカラムに ``x.ljust(n)[:n]``) のようにスライス表記を加える こともできます。)

.. % % This example demonstrates the function \method{rjust()},
.. % % which right-justifies a string in a field of a given width by padding
.. % % it with spaces on the left.  There are similar methods
.. % % \method{ljust()} and \method{center()}.  These
.. % % functions do not write anything, they just return a new string.  If
.. % % the input string is too long, they don't truncate it, but return it
.. % % unchanged; this will mess up your column lay-out but that's usually
.. % % better than the alternative, which would be lying about a value.  (If
.. % % you really want truncation you can always add a slice operation, as in
.. % % \samp{ljust(x,~n)[0:n]}.)

もう一つのメソッド、 :func:`zfill` は、数値文字列 の左側をゼロ詰めします。このメソッドは正と負の符号を正しく扱います:

.. % % There is another method, \method{zfill()}, which pads a
.. % % numeric string on the left with zeros.  It understands about plus and
.. % % minus signs:

::

   >>> '12'.zfill(5)
   '00012'
   >>> '-3.14'.zfill(7)
   '-003.14'
   >>> '3.14159265359'.zfill(5)
   '3.14159265359'

``%`` 演算子を使う場合は以下のようになります:

.. % % Using the \code{\%} operator looks like this:

::

   >>> import math
   >>> print 'The value of PI is approximately %5.3f.' % math.pi
   The value of PI is approximately 3.142.

文字列の中に複数の書式がある場合には、以下の例のように、右側の被演算子 にタプルを渡す必要があります:

.. % % If there is more than one format in the string, you need to pass a
.. % % tuple as right operand, as in this example:

::

   >>> table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
   >>> for name, phone in table.items():
   ...     print '%-10s ==> %10d' % (name, phone)
   ... 
   Jack       ==>       4098
   Dcab       ==>       7678
   Sjoerd     ==>       4127

ほとんどの書式化は C 言語と同じように動作し、正しい型を渡す 必要があります; しかし、正しい型を渡さなかった場合にはコアダンプ
ではなく例外の送出になります。書式 ``%s`` はもっと寛大です: 対応する引数が文字列オブジェクトでなければ、組込み関数 :func:`str`
を使って文字列に変換してくれます。また、数値表現の桁幅や精度を別個の (整数の) 引数として渡せるよう、``*`` がサポートされています。 C 言語の書式
``%n`` と ``%p`` はサポートされていません。

.. % % Most formats work exactly as in C and require that you pass the proper
.. % % type; however, if you don't you get an exception, not a core dump.
.. % % The \code{\%s} format is more relaxed: if the corresponding argument is
.. % % not a string object, it is converted to string using the
.. % % \function{str()} built-in function.  Using \code{*} to pass the width
.. % % or precision in as a separate (integer) argument is supported.  The
.. % % C formats \code{\%n} and \code{\%p} are not supported.

もしも長い書式化文字列があり、それを分割したくない場合には、 変数を引数の位置ではなく、変数の名前で参照できるとよいでしょう。 以下の形式
``%(name)format`` を使えば可能になります:

.. % % If you have a really long format string that you don't want to split
.. % % up, it would be nice if you could reference the variables to be
.. % % formatted by name instead of by position.  This can be done by using
.. % % form \code{\%(name)format}, as shown here:

::

   >>> table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
   >>> print 'Jack: %(Jack)d; Sjoerd: %(Sjoerd)d; Dcab: %(Dcab)d' % table
   Jack: 4098; Sjoerd: 4127; Dcab: 8637678

全てのローカルな変数が入った辞書を返す、新たに紹介する組み込み関数 :func:`vars` と組み合わせると特に便利です。

.. % % This is particularly useful in combination with the new built-in
.. % % \function{vars()} function, which returns a dictionary containing all
.. % % local variables.


.. _tut-files:

ファイルを読み書きする
===========

.. index::
   builtin: open
   object: file

:func:`open` はファイルオブジェクトを 返します。 :func:`open` は、 ``open(filename, mode)``
のように二つの引数を伴って 呼び出されることがほとんどです。

.. % Reading and Writing Files
.. % Opening files
.. % % \function{open()}\bifuncindex{open} returns a file
.. % % object\obindex{file}, and is most commonly used with two arguments:
.. % % \samp{open(\var{filename}, \var{mode})}.

::

   >>> f=open('/tmp/workfile', 'w')
   >>> print f
   <open file '/tmp/workfile', mode 'w' at 80a0960>

最初の引数はファイル名の入った文字列です。二つめの引数もまた文字列で、 ファイルをどのように使うかを示す数個の文字が入っています。 *mode*
は、ファイルが読み出し専用なら ``'r'`` 、 書き込み専用 (同名の既存のファイルがあれば消去されます) なら ``'w'``  とします。``'a'``
はファイルを追記用に開きます; ファイルに書き込まれた 内容は自動的にファイルの終端に追加されます。``'r+'`` はファイルを読み
書き両用に開きます。*mode* 引数はオプションです; 省略された場合には ``'r'`` であると仮定します。

.. % % The first argument is a string containing the filename.  The second
.. % % argument is another string containing a few characters describing the
.. % % way in which the file will be used.  \var{mode} can be \code{'r'} when
.. % % the file will only be read, \code{'w'} for only writing (an existing
.. % % file with the same name will be erased), and \code{'a'} opens the file
.. % % for appending; any data written to the file is automatically added to
.. % % the end.  \code{'r+'} opens the file for both reading and writing.
.. % % The \var{mode} argument is optional; \code{'r'} will be assumed if
.. % % it's omitted.

Windows や Macintosh では、*mode* に ``'b'`` を追加すると ファイルをバイナリモードで開きます。したがって、
``'rb'``,  ``'wb'``, ``'r+b'`` といったモードがあります。 Windows はテキストファイルとバイナリファイルを区別しています;
テキストファイルでは、読み書きの際に行末文字が自動的に少し変更 されます。 この舞台裏でのファイルデータ変更は、ASCII でできたテキストファイル
では差し支えないものですが、:file:`JPEG` や :file:`EXE` ファイルのような バイナリデータは破損してしまうことになるでしょう。
こうしたファイルを読み書きする際にはバイナリモードを使うよう十分 注意してください。

.. % % On Windows and the Macintosh, \code{'b'} appended to the
.. % % mode opens the file in binary mode, so there are also modes like
.. % % \code{'rb'}, \code{'wb'}, and \code{'r+b'}.  Windows makes a
.. % % distinction between text and binary files; the end-of-line characters
.. % % in text files are automatically altered slightly when data is read or
.. % % written.  This behind-the-scenes modification to file data is fine for
.. % % \ASCII{} text files, but it'll corrupt binary data like that in \file{JPEG} or
.. % % \file{EXE} files.  Be very careful to use binary mode when reading and
.. % % writing such files.


.. _tut-filemethods:

ファイルオブジェクトのメソッド
---------------

この節の以降の例は、``f`` というファイルオブジェクトが既に 生成されているものと仮定します。

.. % Methods of File Objects
.. % % The rest of the examples in this section will assume that a file
.. % % object called \code{f} has already been created.

ファイルの内容を読み出すには、``f.read(size)`` を呼び出します。 このメソッドはある量のデータを読み出して、文字列として返します。 *size*
はオプションの数値引数です。*size* が省略されたり 負の数であった場合、ファイルの内容全てを読み出して返します; ただし、
ファイルがマシンのメモリの二倍の大きさもある場合にはどうなるか わかりません。 *size* が負でない数ならば、最大で *size* バイトを読み出して
返します。ファイルの終端にすでに達していた場合、``f.read()`` は 空の文字列 (``""``) を返します。

.. % % To read a file's contents, call \code{f.read(\var{size})}, which reads
.. % % some quantity of data and returns it as a string.  \var{size} is an
.. % % optional numeric argument.  When \var{size} is omitted or negative,
.. % % the entire contents of the file will be read and returned; it's your
.. % % problem if the file is twice as large as your machine's memory.
.. % % Otherwise, at most \var{size} bytes are read and returned.  If the end
.. % % of the file has been reached, \code{f.read()} will return an empty
.. % % string (\code {""}).

::

   >>> f.read()
   'This is the entire file.\n'
   >>> f.read()
   ''

``f.readline()`` はファイルから 1 行だけを読み取ります; 改行文字 (``\n``) は読み出された文字列の終端に残ります。
改行が省略されるのは、ファイルが改行で終わっていない場合の最終行 のみです。これは、戻り値があいまいでないようにするためです; ``f.readline()``
が空の文字列を返したら、ファイルの終端に 達したことが分かります。一方、空行は ``'\n'`` 、すなわち 改行 1 文字だけからなる文字列で表現されます。

.. % % \code{f.readline()} reads a single line from the file; a newline
.. % % character (\code{\e n}) is left at the end of the string, and is only
.. % % omitted on the last line of the file if the file doesn't end in a
.. % % newline.  This makes the return value unambiguous; if
.. % % \code{f.readline()} returns an empty string, the end of the file has
.. % % been reached, while a blank line is represented by \code{'\e n'}, a
.. % % string containing only a single newline.

::

   >>> f.readline()
   'This is the first line of the file.\n'
   >>> f.readline()
   'Second line of the file\n'
   >>> f.readline()
   ''

``f.readlines()`` は、ファイルに入っているデータの全ての行からなる リストを返します。オプションのパラメタ *sizehint* が指定されて
いれば、ファイルから指定されたバイト数を読み出し、さらに一行を完成 させるのに必要なだけを読み出して、読み出された行からなる
リストを返します。このメソッドは巨大なファイルを行単位で効率的に 読み出すためによく使われます。未完成の行が返されることはありません。

.. % % \code{f.readlines()} returns a list containing all the lines of data
.. % % in the file.  If given an optional parameter \var{sizehint}, it reads
.. % % that many bytes from the file and enough more to complete a line, and
.. % % returns the lines from that.  This is often used to allow efficient
.. % % reading of a large file by lines, but without having to load the
.. % % entire file in memory.  Only complete lines will be returned.

::

   >>> f.readlines()
   ['This is the first line of the file.\n', 'Second line of the file\n']

行を読む別のアプローチは、ファイルオブジェクトについてループをおこなう ことです。これは省メモリで、速く、コードがよりシンプルになります:

.. % % An alternate approach to reading lines is to loop over the file object.
.. % % This is memory efficient, fast, and leads to simpler code:

::

   >>> for line in f:
           print line,

   This is the first line of the file.
   Second line of the file

この方法はシンプルですが細かなコントロールをすることができません。 行バッファを管理する方法が異なるので、これらを混在させて使うことはできま せん。

.. % % The alternative approach is simpler but does not provide as fine-grained
.. % % control.  Since the two approaches manage line buffering differently,
.. % % they should not be mixed.

``f.write(string)`` は、 *string* の内容をファイルに 書き込み、``None`` を返します。

.. % % \code{f.write(\var{string})} writes the contents of \var{string} to
.. % % the file, returning \code{None}.

::

   >>> f.write('This is a test\n')

文字列以外のものを出力したい場合、まず文字列に変換してやる必要が あります:

.. % % To write something other than a string, it needs to be converted to a
.. % % string first:

::

   >>> value = ('the answer', 42)
   >>> s = str(value)
   >>> f.write(s)

``f.tell()`` は、ファイルオブジェクトが指しているあるファイル中の 位置を示す整数を、ファイルの先頭からのバイト数で図った値で返します。
ファイルオブジェクトの位置を変更するには、``f.seek(offset,  from_what)`` を使います。ファイル位置は基準点 (reference
point) にオフセット値 *offset* を足して計算されます; 参照点は *from_what* 引数で選びます。 *from_what* の値が 0
ならばファイルの先頭から測り、 1 ならば現在のファイル位置を使い、2 ならばファイルの終端を 参照点として使います。 *from_what*
は省略することができ、デフォルトの値は 0 、すなわち 参照点としてファイルの先頭を使います。

.. % % \code{f.tell()} returns an integer giving the file object's current
.. % % position in the file, measured in bytes from the beginning of the
.. % % file.  To change the file object's position, use
.. % % \samp{f.seek(\var{offset}, \var{from_what})}.  The position is
.. % % computed from adding \var{offset} to a reference point; the reference
.. % % point is selected by the \var{from_what} argument.  A
.. % % \var{from_what} value of 0 measures from the beginning of the file, 1
.. % % uses the current file position, and 2 uses the end of the file as the
.. % % reference point.  \var{from_what} can be omitted and defaults to 0,
.. % % using the beginning of the file as the reference point.

::

   >>> f = open('/tmp/workfile', 'r+')
   >>> f.write('0123456789abcdef')
   >>> f.seek(5)     # ファイルの第6バイトへ行く
   >>> f.read(1)        
   '5'
   >>> f.seek(-3, 2) # 終端から前へ第3バイトへ行く
   >>> f.read(1)
   'd'

ファイルが用済みになったら、``f.close()`` を呼び出してファイルを 閉じ、ファイルを開くために取られていたシステム資源を解放します。
``f.close()`` を呼び出した後、そのファイルオブジェクトを使おうと すると自動的に失敗します。

.. % % When you're done with a file, call \code{f.close()} to close it and
.. % % free up any system resources taken up by the open file.  After calling
.. % % \code{f.close()}, attempts to use the file object will automatically fail.

::

   >>> f.close()
   >>> f.read()
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: I/O operation on closed file

ファイルオブジェクトには、他にも :meth:`isatty` や :meth:`truncate`  といった、あまり使われないメソッドがあります;
ファイルオブジェクトについての完全なガイドは、ライブラリリファレンスを 参照してください。

.. % % File objects have some additional methods, such as
.. % % \method{isatty()} and \method{truncate()} which are less frequently
.. % % used; consult the Library Reference for a complete guide to file
.. % % objects.


.. _tut-pickle:

:mod:`pickle` モジュール
-------------------

.. index:: module: pickle

.. % The \module{pickle} Module

文字列をファイルに読み書きするのは簡単にできます。数値でもほんの わずかに苦労するくらいです。というのは、:meth:`read` は文字列だけを
返すので、``'123'`` のような文字列を受け取って、その数値 123 を返す :func:`int` のような関数に対して文字列を渡してやらなければ
ならないからです。ところが、リストや辞書、クラスのインスタンスのように、 もっと複雑なデータ型を保存したいなら、事態はもっと複雑になります。

.. % % Strings can easily be written to and read from a file. Numbers take a
.. % % bit more effort, since the \method{read()} method only returns
.. % % strings, which will have to be passed to a function like
.. % % \function{int()}, which takes a string like \code{'123'} and
.. % % returns its numeric value 123.  However, when you want to save more
.. % % complex data types like lists, dictionaries, or class instances,
.. % % things get a lot more complicated.

複雑なデータ型を保存するためのコードを利用者に毎回毎回書かせて デバッグさせる代わりに、Python では :mod:`pickle` という標準
モジュールを用意しています。:mod:`pickle` は驚くべきモジュールで、 ほとんどどんな Python オブジェクトも (ある形式の Python
コード でさえも!) 受け取って文字列表現へ変換できます。 この変換過程は :dfn:`pickling` (ピクルス (漬物) 化、以降 pickle 化)
と呼ばれます。文字列表現からオブジェクトを再構成する操作は :dfn:`unpickling` (逆 pickle 化)と呼びます。 pickle 化や
unpickle 化の間、オブジェクトを表現する文字列は ファイルやデータに保存したり、ネットワーク接続を介して離れたマシンに 送信したりできます。

.. % % Rather than have users be constantly writing and debugging code to
.. % % save complicated data types, Python provides a standard module called
.. % % \module{pickle}.  This is an amazing module that can take almost
.. % % any Python object (even some forms of Python code!), and convert it to
.. % % a string representation; this process is called \dfn{pickling}.
.. % % Reconstructing the object from the string representation is called
.. % % \dfn{unpickling}.  Between pickling and unpickling, the string
.. % % representing the object may have been stored in a file or data, or
.. % % sent over a network connection to some distant machine.

オブジェクト ``x`` と、書込み用に開かれているファイルオブジェクト ``f`` があると仮定すると、オブジェクトを pickle 化する最も簡単な
方法は、たった一行のコードしか必要ありません:

.. % % If you have an object \code{x}, and a file object \code{f} that's been
.. % % opened for writing, the simplest way to pickle the object takes only
.. % % one line of code:

::

   pickle.dump(x, f)

逆 pickle 化して再びオブジェクトに戻すには、 ``f`` を読取り用に開かれているファイル・オブジェクトと仮定して:

.. % % To unpickle the object again, if \code{f} is a file object which has
.. % % been opened for reading:

::

   x = pickle.load(f)

とします。

(逆 pickle 化にはいくつか変型があり、たくさんのオブジェクトを pickle 化 したり、 pickle
化されたデータをファイルに書きたくないときに使われます。 完全なドキュメントについては、 ライブラリリファレンス (XXX reference:
../lib/) の  :mod:`pickle` (XXX reference: ../lib/module-pickle.html) を調べてください。)

.. % % (There are other variants of this, used when pickling many objects or
.. % % when you don't want to write the pickled data to a file; consult the
.. % % complete documentation for
.. % % \ulink{\module{pickle}}{../lib/module-pickle.html} in the
.. % % \citetitle[../lib/]{Python Library Reference}.)

:mod:`pickle` (XXX reference: ../lib/module-pickle.html) は、Python
のオブジェクトを保存できるようにし、 他のプログラムや、同じプログラムが将来起動されたときに再利用 できるようにする標準の方法です; 技術的な用語でいうと
:dfn:`persistent` (永続性) オブジェクトです。 :mod:`pickle` (XXX reference: ../lib/module-
pickle.html) はとても広範に使われている ので、Python 拡張モジュールの多くの作者は、行列のような新たなデータ型が 正しく pickle
化/unpickle 化できるよう気をつけています。

.. % % \ulink{\module{pickle}}{../lib/module-pickle.html} is the standard way to make Python objects which can
.. % % be stored and reused by other programs or by a future invocation of
.. % % the same program; the technical term for this is a
.. % % \dfn{persistent} object.  Because \ulink{\module{pickle}}{../lib/module-pickle.html} is so widely used,
.. % % many authors who write Python extensions take care to ensure that new
.. % % data types such as matrices can be properly pickled and unpickled.


