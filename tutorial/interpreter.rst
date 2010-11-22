.. _tut-using:

*************************
Python インタプリタを使う
*************************

.. % Using the Python Interpreter


.. _tut-invoking:

インタプリタを起動する
======================

Python が使える計算機なら、インタプリタはたいてい :file:`/usr/local/bin/python` にインストールされています。Unix シェ
ルのサーチパスに :file:`/usr/local/bin` を入れれば、シェルで

.. % Invoking the Interpreter
.. % % The Python interpreter is usually installed as
.. % % \file{/usr/local/bin/python} on those machines where it is available;
.. % % putting \file{/usr/local/bin} in your \UNIX{} shell's search path
.. % % makes it possible to start it by typing the command

Windows マシンの場合には、Pythonは大抵の場合 :file:`C:\Python26` にインストールされますが、インストーラ実行時に変更すること
ができます。このディレクトリをあなたのパスに追加するには、以下のコマンドをコマンドプロンプトで実行してください::

   set path=%path%;C:\python26

::

   python

とコマンドを入力すれば使えるようになります。インストールする際にどのディレクトリに Python インタプリタを入れるかをオプションで指定できるので、
インタプリタは他のディレクトリにあるかもしれません; 身近な Python の導師 (guru) か、システム管理者に聞いてみてください。(例えば、その他の場
所としては :file:`/usr/local/python` が一般的です。)

.. % % to the shell.  Since the choice of the directory where the interpreter
.. % % lives is an installation option, other places are possible; check with
.. % % your local Python guru or system administrator.  (E.g.,
.. % % \file{/usr/local/python} is a popular alternative location.)

ファイル終端文字 (Unixでは :kbd:`Control-D` 、DOS や Windows では :kbd:`Control-Z`) を一次プロンプト
(primary prompt) に入力すると、インタプリタが終了状態ゼロで終了します。もしこの操作がうまく働かないなら、コマンド: ``import
sys; sys.exit()`` と入力すればインタプリタを終了できます。

.. % % Typing an end-of-file character (\kbd{Control-D} on \UNIX,
.. % % \kbd{Control-Z} on DOS or Windows) at the primary prompt causes the
.. % % interpreter to exit with a zero exit status.  If that doesn't work,
.. % % you can exit the interpreter by typing the following commands:
.. % % \samp{import sys; sys.exit()}.

通常、インタプリタの行編集機能は、あまり洗練されたものではありません。 Unixシステムでは、インタプリタをインストールした誰かが GNU readline
ライブラリのサポートを有効にしていれば、洗練された対話的行編集やヒストリ機能が追加されます。
コマンドライン編集機能がサポートされているかを最も手っ取り早く調べる方法は、おそらく最初に表示された Python プロンプトに Control-P を入力し
てみることでしょう。ビープ音が鳴るなら、コマンドライン編集機能があります。編集キーについての解説は付録 :ref:`tut-interacting`
を参照してください。何も起こらないように見えるか、 ``^P`` がエコーバックされるなら、コ
マンドライン編集機能は利用できません。この場合、現在編集中の行から文字を削除するにはバックスペースを使うしかありません。

.. % % The interpreter's line-editing features usually aren't very
.. % % sophisticated.  On \UNIX, whoever installed the interpreter may have
.. % % enabled support for the GNU readline library, which adds more
.. % % elaborate interactive editing and history features. Perhaps the
.. % % quickest check to see whether command line editing is supported is
.. % % typing Control-P to the first Python prompt you get.  If it beeps, you
.. % % have command line editing; see Appendix \ref{interacting} for an
.. % % introduction to the keys.  If nothing appears to happen, or if
.. % % \code{\^P} is echoed, command line editing isn't available; you'll
.. % % only be able to use backspace to remove characters from the current
.. % % line.

インタプリタはさながら Unix シェルのように働きます。標準入力が端末に接続された状態で呼び出されると、コマンドを対話的に読み込んで実行しま
す。ファイル名を引数にしたり、標準入力からファイルを入力すると、インタプリタはファイルから *スクリプト* を読み込んで実行します。

.. % % The interpreter operates somewhat like the \UNIX{} shell: when called
.. % % with standard input connected to a tty device, it reads and executes
.. % % commands interactively; when called with a file name argument or with
.. % % a file as standard input, it reads and executes a \emph{script} from
.. % % that file.

インタプリタを起動する第二の方法は ``python -c command [arg] ...`` です。この形式では、シェルの :option:`-c`
オプションと同じように、 *command* に指定した文を実行します。Python 文には、スペースなどの
シェルにとって特殊な意味をもつ文字がしばしば含まれるので、 *command* 全体を二重引用符を囲っておいたほうが良いでしょう。

.. % % A second way of starting the interpreter is
.. % % \samp{\program{python} \programopt{-c} \var{command} [arg] ...}, which
.. % % executes the statement(s) in \var{command}, analogous to the shell's
.. % % \programopt{-c} option.  Since Python statements often contain spaces
.. % % or other characters that are special to the shell, it is best to quote
.. % % \var{command} in its entirety with double quotes.

Python のモジュールには、スクリプトとしても便利に使えるものがあります。 ``python -m module [arg] ...`` のようにすると、
*module* のソースファイルを、フルパスを指定して起動したかのように実行できます。

.. % +Some Python modules are also useful as scripts.  These can be invoked using
.. % +\samp{\program{python} \programopt{-m} \var{module} [arg] ...}, which
.. % +executes the source file for \var{module} as if you had spelled out its
.. % +full name on the command line.

``python file`` と ``python <file`` の違いに注意してください。後者の場合、プログラム内で :func:`input` や
:func:`raw_input` が呼び出され、ユーザからの入力が必要な場合、入力は *ファイル* から
取り込まれます。この場合、パーザはプログラムの実行を開始される前にファイルを終端まで読み込んでおくので、プログラムはすぐに入力の終わりまで到
達してしまいます。前者の場合 (大抵はこちらの方が望ましい動作です)、入力には Python インタプリタの標準入力に接続された何らかのファイルまたは
デバイスが充てられます。

.. % % Note that there is a difference between \samp{python file} and
.. % % \samp{python <file}.  In the latter case, input requests from the
.. % % program, such as calls to \code{input()} and \code{raw_input()}, are
.. % % satisfied from \emph{file}.  Since this file has already been read
.. % % until the end by the parser before the program starts executing, the
.. % % program will encounter end-of-file immediately.  In the former case
.. % % (which is usually what you want) they are satisfied from whatever file
.. % % or device is connected to standard input of the Python interpreter.

スクリプトファイルが使われた場合、スクリプトを走らせて、そのまま対話モードに入れると便利なことがあります。これには :option:`-i` をスク
リプトの前に追加します。(前の段落で述べたのと同じ理由から、スクリプトを標準入力から読み込んだ場合には、このオプションはうまく働きません。)

.. % % When a script file is used, it is sometimes useful to be able to run
.. % % the script and enter interactive mode afterwards.  This can be done by
.. % % passing \programopt{-i} before the script.  (This does not work if the
.. % % script is read from standard input, for the same reason as explained
.. % % in the previous paragraph.)


.. _tut-argpassing:

引数の受け渡し
--------------

スクリプト名と引数を指定してインタプリタを起動した場合、スクリプト名やスクリプト名以後に指定した引数は、スクリプトからは ``sys.argv`` で
アクセスできるようになります。 ``sys.argv`` は文字列からなるリストで、少なくとも一つ要素が入っています。スクリプト名も引数も指定し
なければ ``sys.argv[0]`` は空の文字列になります。スクリプト名の代わりに ``'-'`` (標準入力を意味します) を指定すると、
``sys.argv[0]`` は ``'-'`` になります。 :option:`-c`  *command* を使うと、 ``sys.argv[0]`` は
``'-c'`` になります。 :option:`-m` *module* を使った場合、 ``sys.argv[0]`` は
モジュールのフルパスになります。 :option:`-c` *command* や :option:`-m` *module*
の後ろにオプションを指定した場合、Python インタプリタ自体はこれらの引数を処理せず、 ``sys.argv`` を介して
*command* や *module* から扱えるようになります。

.. % Argument Passing
.. % % When known to the interpreter, the script name and additional
.. % % arguments thereafter are passed to the script in the variable
.. % % \code{sys.argv}, which is a list of strings.  Its length is at least
.. % % one; when no script and no arguments are given, \code{sys.argv[0]} is
.. % % an empty string.  When the script name is given as \code{'-'} (meaning
.. % % standard input), \code{sys.argv[0]} is set to \code{'-'}.  When
.. % % \programopt{-c} \var{command} is used, \code{sys.argv[0]} is set to
.. % \code{'-c'}.  When \programopt{-m} \var{module} is used, \code{sys.argv[0]}
.. % is set to the full name of the located module.  Options found after
.. % \programopt{-c} \var{command} or \programopt{-m} \var{module} are
.. % not consumed
.. % by the Python interpreter's option processing but left in \code{sys.argv} for
.. % the command or module to handle.


.. _tut-interactive:

対話モード
----------

インタプリタが命令を端末 (tty) やコマンドプロンプトから読み取っている場合、インタプリタは *対話モード (interactive mode)*
で動作しているといいます。このモードでは、インタプリタは *一次プロンプト (primary prompt)*
を表示して、ユーザにコマンドを入力するようします。一次プロンプトは普通、三つの「大なり記号」 (``>>>``) です。一つの入力が次の行まで続く
(行継続: continuation line を行う) 場合、インタプリタは *二次プロンプト (secondary prompt)* を表示します。二
次プロンプトは、デフォルトでは三つのドット (``...``) です。インタプリタは、最初のプロンプトを出す前にバージョン番号と著作権表示から始ま
る起動メッセージを出力します。

.. % Interactive Mode
.. % % When commands are read from a tty, the interpreter is said to be in
.. % % \emph{interactive mode}.  In this mode it prompts for the next command
.. % % with the \emph{primary prompt}, usually three greater-than signs
.. % % (\samp{>\code{>}>~}); for continuation lines it prompts with the
.. % % \emph{secondary prompt}, by default three dots (\samp{...~}).
.. % % The interpreter prints a welcome message stating its version number
.. % % and a copyright notice before printing the first prompt:

::

   python
   Python 2.6 (#1, Feb 28 2007, 00:02:06)
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

行継続は、例えば以下の :keyword:`if` 文のように、複数の行からなる構文を入力するときに必要です:

.. % % Continuation lines are needed when entering a multi-line construct.
.. % % As an example, take a look at this \keyword{if} statement:

::

   >>> the_world_is_flat = 1
   >>> if the_world_is_flat:
   ...     print "Be careful not to fall off!"
   ...
   Be careful not to fall off!

.. % %% XXX ProofReeding Done To Here XXX %%%


.. _tut-interp:

インタプリタとその環境
======================

.. % The Interpreter and Its Environment


.. _tut-error:

エラー処理
----------

エラーが発生すると、インタプリタはエラーメッセージとスタックトレース (stack trace) を出力します。対話モードにいるときは、インタプリタは
一次プロンプトに戻ります; 入力がファイルからきているときには、インタプリタはスタックトレースを出力した後、非ゼロの終了状態で終了します。 (``try``
文の :keyword:`except` 節で処理された例外は、ここでいうエラーにはあたりません。)
いくつかのエラーは無条件に致命的であり、非ゼロの終了状態となるプログラムの終了を引き起こします; これにはインタプリタ内部の矛盾や
ある種のメモリ枯渇が当てはまります。エラーメッセージは全て標準エラー出力ストリームに書き込まれます;
これに対して、実行した命令からの通常出力される内容は標準出力に書き込まれます。

.. % Error Handling
.. % % When an error occurs, the interpreter prints an error
.. % % message and a stack trace.  In interactive mode, it then returns to
.. % % the primary prompt; when input came from a file, it exits with a
.. % % nonzero exit status after printing
.. % % the stack trace.  (Exceptions handled by an \code{except} clause in a
.. % % \code{try} statement are not errors in this context.)  Some errors are
.. % % unconditionally fatal and cause an exit with a nonzero exit; this
.. % % applies to internal inconsistencies and some cases of running out of
.. % % memory.  All error messages are written to the standard error stream;
.. % % normal output from the executed commands is written to standard
.. % % output.

割り込み文字 (interrupt character、普通は Control-C か DEL) を
一次または二次プロンプトに対して打鍵すると、入力が取り消されて一次プロンプトに戻ります。  [#]_ コマンドの実行中に割り込み文字を打鍵すると
:exc:`KeyboardInterrupt`  例外が送出されます。この例外は ``try`` 文で処理できます。

.. % % Typing the interrupt character (usually Control-C or DEL) to the
.. % % primary or secondary prompt cancels the input and returns to the
.. % % primary prompt.\footnote{
.. % %         A problem with the GNU Readline package may prevent this.
.. % % }
.. % % Typing an interrupt while a command is executing raises the
.. % % \code{KeyboardInterrupt} exception, which may be handled by a
.. % % \code{try} statement.


.. _tut-scripts:

実行可能な Python スクリプト
----------------------------

BSD 風の Unix システムでは、Python スクリプトはシェルスクリプトのようにして直接実行可能にできます。これを行うには、以下の行

.. % Executable Python Scripts
.. % % On BSD'ish \UNIX{} systems, Python scripts can be made directly
.. % % executable, like shell scripts, by putting the line

::

   #! /usr/bin/env python

(ここではインタプリタがユーザの :envvar:`PATH` 上にあると仮定しています) をスクリプトの先頭に置き、スクリプトファイルに実行可能モードを
与えます。 ``#!`` はファイルの最初の２文字でなければなりません。プラットフォームによっては、この最初の行を終端する改行文字が
Windows 形式 (``'\r\n'``) ではなく、 Unix形式(``'\n'``)でなければならないことがあります。
ハッシュまたはポンド文字、すなわち ``'#'`` は、Python  ではコメントを書き始めるために使われているので注意してください。

.. % % (assuming that the interpreter is on the user's \envvar{PATH}) at the
.. % % beginning of the script and giving the file an executable mode.  The
.. % % \samp{\#!} must be the first two characters of the file.  On some
.. % % platforms, this first line must end with a \UNIX-style line ending
.. % % (\character{\e n}), not a Mac OS (\character{\e r}) or Windows
.. % % (\character{\e r\e n}) line ending.  Note that
.. % % the hash, or pound, character, \character{\#}, is used to start a
.. % % comment in Python.

:program:`chmod` コマンドを使えば、スクリプトに実行モード (または実行権限) を与えることができます:

.. % % The script can be given a executable mode, or permission, using the
.. % % \program{chmod} command:
.. % % begin{verbatim}
.. % % $ chmod +x myscript.py
.. % % end{verbatim} % $ <-- bow to font-lock

::

   $ chmod +x myscript.py

Windows では、"実行モード" のような概念はありません。
Python のインストーラーは自動的に ``.py`` ファイルを ``python.exe``
に関連付けるので、 Python ファイルをダブルクリックするとそれをスクリプトとして実行します。
``.pyw`` 拡張子も(訳注: ``pythonw.exe`` に)関連付けられ、通常コンソールウィンドウを
抑制して実行します。


ソースコードの文字コード方式 (encoding)
---------------------------------------

ASCII 形式でない文字コード化方式 (エンコーディング: encoding) を Python  ソースコードファイル中で使うことができます。最良の方法は、
``#!`` 行の直後に一行かそれ以上の特殊なコメントを挿入して、ソースファイルのエンコードを指定するというものです:

.. % % It is possible to use encodings different than \ASCII{} in Python source
.. % % files. The best way to do it is to put one more special comment line
.. % % right after the \code{\#!} line to define the source file encoding:

::

   # -\*- coding: encoding -\*-


このように宣言しておくと、ソースファイル中の全ての文字は *encoding* という文字コードでエンコードされているものとして扱われ、Unicode 文字列
リテラルを指定したエンコードで直接記述できます。
利用可能なエンコードのリストは Python ライブラリリファレンスの
:mod:`codecs` の節にあります。

.. % % With that declaration, all characters in the source file will be treated as
.. % % {}\code{iso-8859-1}, and it will be
.. % % possible to directly write Unicode string literals in the selected
.. % % encoding.  The list of possible encodings can be found in the
.. % % \citetitle[../lib/lib.html]{Python Library Reference}, in the section
.. % % on \ulink{\module{codecs}}{../lib/module-codecs.html}.

例えばユーロ通過記号を含む Unicode リテラルを書くには、 ISO-8859-15 エンコーディングを使えます。 ISO-8859-15 では、ユーロ
通過記号の序数 (ordinal) は 164 です。以下のスクリプトは 8364 という値 (Unicode でユーロ記号に対応するコードポイントの値) を
出力して終了します:

.. % For example, to write Unicode literals including the Euro currency
.. % symbol, the ISO-8859-15 encoding can be used, with the Euro symbol
.. % having the ordinal value 164.  This script will print the value 8364
.. % (the Unicode codepoint corresponding to the Euro symbol) and then
.. % exit:

::

   # -*- coding: iso-8859-15 -*-

   currency = u"€"
   print ord(currency)

利用しているエディタがファイルを UTF-8 バイト整列記号 (通称 BOM: Byte Order Mark) 付きの ``UTF-8``
で保存できる場合、エンコード宣言の代わりに使うことができます。 IDLE は  ``Options/General/Default Source
Encoding/UTF-8`` が設定されている場合、 UTF-8 でエンコードされたファイルの識別機能をサポートします。ただし、 (2.2 以前の) 古い
Python リリースは UTF-8 シグネチャを理解しませんし、オペレーティングシステムは (Unix システムでしか使われていませんが) ``#!``
の行を含むスクリプトファイルを判別できなくなるので注意してください。

.. % % If your editor supports saving files as \code{UTF-8} with a UTF-8
.. % % \emph{byte order mark} (aka BOM), you can use that instead of an
.. % % encoding declaration. IDLE supports this capability if
.. % % \code{Options/General/Default Source Encoding/UTF-8} is set. Notice
.. % % that this signature is not understood in older Python releases (2.2
.. % % and earlier), and also not understood by the operating system for
.. % +script files with \code{\#!} lines (only used on \UNIX{} systems).

UTF-8 を (シグネチャやエンコード宣言を行って) 使うと、世界中のほとんどの言語で使われている文字を文字列リテラルやコメントの中に
同時に使うことができます。識別子に対する非 ASCII 文字の使用はサポートされていません。全ての文字を正しく表示できるようにするには、使っている
エディタがファイルを UTF-8 であると認識することができなければならず、かつファイル内で使われている全ての文字をサポートするようなフォントを
使わなければなりません。

.. % % By using UTF-8 (either through the signature or an encoding
.. % % declaration), characters of most languages in the world can be used
.. % % simultaneously in string literals and comments. Using non-\ASCII
.. % % characters in identifiers is not supported. To display all these
.. % % characters properly, your editor must recognize that the file is
.. % % UTF-8, and it must use a font that supports all the characters in the
.. % % file.


.. _tut-startup:

対話モード用の起動時実行ファイル
--------------------------------

Python を対話的に使うときには、インタプリタが起動する度に実行される何らかの標準的なコマンドがあると便利なことがよくあります。
これを行うには、 :envvar:`PYTHONSTARTUP` と呼ばれる環境変数を、インタプリタ起動時に実行されるコマンドが入ったファイル名に設定します。
この機能は Unix シェルの :file:`.profile` に似ています。

このファイルは対話セッションのときだけ読み出されます。Python がコマンドをスクリプトから読み出しているときや、 :file:`/dev/tty`
がコマンドの入力元として明示的に指定されている (この場合対話的セッションのように動作します) *わけではない* 場合にはこのファイルは読み出されません。
ファイル内のコマンドは、対話的コマンドが実行される名前空間と同じ名前空間内で実行されます。このため、ファイル内で定義されていたり import された
オブジェクトは、限定子をつけなくても対話セッション内で使うことができます。また、このファイル内で ``sys.ps1`` や ``sys.ps2``
を変更して、プロンプトを変更することもできます。

.. % % This file is only read in interactive sessions, not when Python reads
.. % % commands from a script, and not when \file{/dev/tty} is given as the
.. % % explicit source of commands (which otherwise behaves like an
.. % % interactive session).  It is executed in the same namespace where
.. % % interactive commands are executed, so that objects that it defines or
.. % % imports can be used without qualification in the interactive session.
.. % % You can also change the prompts \code{sys.ps1} and \code{sys.ps2} in
.. % % this file.

もし現在のディレクトリから追加的なスタートアップファイルを読み出したいのなら、グローバルのスタートアップファイルの中で ``if
os.path.isfile('.pythonrc.py'): execfile('.pythonrc.py')``
のようなコードのプログラムを書くことができます。スクリプト中でスタートアップファイルを使いたいのなら、以下のようにして
スクリプト中で明示的に実行しなければなりません:

.. % % If you want to read an additional start-up file from the current
.. % % directory, you can program this in the global start-up file using code
.. % % like \samp{if os.path.isfile('.pythonrc.py'):
.. % % execfile('.pythonrc.py')}.  If you want to use the startup file in a
.. % % script, you must do this explicitly in the script:

::

   import os
   filename = os.environ.get('PYTHONSTARTUP')
   if filename and os.path.isfile(filename):
       execfile(filename)


.. rubric:: 脚注

.. [#] GNU Readline パッケージに関する問題のせいで妨げられることがあります。

