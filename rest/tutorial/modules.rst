.. _tut-modules:

*****
モジュール
*****

Python インタプリタを終了させ、再び起動すると、これまでに行ってきた 定義 (関数や変数) は失われています。ですから、より長いプログラムを
書きたいなら、テキストエディタを使ってインタプリタへの入力を用意して おき、手作業の代わりにファイルを入力に使って動作させるとよいでしょう。 この作業を
*スクリプト (script)* の作成と言います; プログラムが 長くなるにつれ、メンテナンスを楽にするために、スクリプトをいくつかの
ファイルに分割したくなるかもしれません。また、いくつかのプログラムで 書いてきた便利な関数について、その定義をコピーすることなく個々の
プログラムで使いたいと思うかもしれません。

.. % Modules
.. % % If you quit from the Python interpreter and enter it again, the
.. % % definitions you have made (functions and variables) are lost.
.. % % Therefore, if you want to write a somewhat longer program, you are
.. % % better off using a text editor to prepare the input for the interpreter
.. % % and running it with that file as input instead.  This is known as creating a
.. % % \emph{script}.  As your program gets longer, you may want to split it
.. % % into several files for easier maintenance.  You may also want to use a
.. % % handy function that you've written in several programs without copying
.. % % its definition into each program.

こういった要求をサポートするために、Python では定義をファイルに書いて おき、スクリプトの中やインタプリタの対話インスタンス上で使う方法が あります。
このファイルを *モジュール (module)* と呼びます; モジュール にある定義は、他のモジュールや *main* モジュール (実行の
トップレベルや電卓モードでアクセスできる変数の集まりを指します) に *import* (取り込み) することができます。

.. % % To support this, Python has a way to put definitions in a file and use
.. % % them in a script or in an interactive instance of the interpreter.
.. % % Such a file is called a \emph{module}; definitions from a module can be
.. % % \emph{imported} into other modules or into the \emph{main} module (the
.. % % collection of variables that you have access to in a script
.. % % executed at the top level
.. % % and in calculator mode).

モジュールは Python の定義や文が入ったファイルです。 ファイル名はモジュール名に接尾語 :file:`,py` がついたものになります。
モジュールの中では、(文字列の) モジュール名をグローバル変数 ``__name__`` で取得できます。例えば、お気に入りのテキストエディタ
を使って、現在のディレクトリに以下の内容のファイル :file:`fibo.py` を 作成してみましょう:

.. % % A module is a file containing Python definitions and statements.  The
.. % % file name is the module name with the suffix \file{.py} appended.  Within
.. % % a module, the module's name (as a string) is available as the value of
.. % % the global variable \code{__name__}.  For instance, use your favorite text
.. % % editor to create a file called \file{fibo.py} in the current directory
.. % % with the following contents:

::

   # フィボナッチ数列モジュール

   def fib(n):    # nまで加算されるフィボナッチ級数を印字
       a, b = 0, 1
       while b < n:
           print b,
           a, b = b, a+b

   def fib2(n): # nまで加算されるフィボナッチ級数を返す
       result = []
       a, b = 0, 1
       while b < n:
           result.append(b)
           a, b = b, a+b
       return result

次に Python インタプリタに入り、モジュールを以下のコマンドで import しましょう。

.. % % Now enter the Python interpreter and import this module with the
.. % % following command:

::

   >>> import fibo

この操作では、``fibo`` で定義された関数の名前を直接現在の シンボルテーブルに入力することはありません; 単にモジュール名 ``fibo``
だけをシンボルテーブルに入れます。 関数にはモジュール名を使ってアクセスします:

.. % % This does not enter the names of the functions defined in \code{fibo}
.. % % directly in the current symbol table; it only enters the module name
.. % % \code{fibo} there.
.. % % Using the module name you can access the functions:

::

   >>> fibo.fib(1000)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987
   >>> fibo.fib2(100)
   [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
   >>> fibo.__name__
   'fibo'

関数を度々使うのなら、ローカルな名前に代入できます:

.. % % If you intend to use a function often you can assign it to a local name:

::

   >>> fib = fibo.fib
   >>> fib(500)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377


.. _tut-moremodules:

モジュールについてもうすこし
==============

モジュールには、関数定義に加えて実行文を入れることができます。 これらの実行文はモジュールを初期化するためのものです。
これらの実行文は、モジュールがどこかで*最初に* import された 時にだけ実行されます。 [#]_

.. % More on Modules
.. % % A module can contain executable statements as well as function
.. % % definitions.
.. % % These statements are intended to initialize the module.
.. % % They are executed only the
.. % % \emph{first} time the module is imported somewhere.\footnote{
.. % %         In fact function definitions are also `statements' that are
.. % %         `executed'; the execution enters the function name in the
.. % %         module's global symbol table.
.. % % }

各々のモジュールは、自前のプライベートなシンボルテーブルを持っていて、 モジュールで定義されている関数はこのテーブルをグローバルな
シンボルテーブルとして使います。 したがって、モジュールの作者は、ユーザのグローバル変数と偶然的な衝突が
起こる心配をせずに、グローバルな変数をモジュールで使うことができます。 一方、自分が行っている操作をきちんと理解していれば、モジュール内の
関数を参照するのと同じ表記法 ``modname.itemname`` で、モジュールの グローバル変数をいじることもできます。

.. % % Each module has its own private symbol table, which is used as the
.. % % global symbol table by all functions defined in the module.
.. % % Thus, the author of a module can use global variables in the module
.. % % without worrying about accidental clashes with a user's global
.. % % variables.
.. % % On the other hand, if you know what you are doing you can touch a
.. % % module's global variables with the same notation used to refer to its
.. % % functions,
.. % % \code{modname.itemname}.

モジュールが他のモジュールを import することもできます。:keyword:`import` 文は全てモジュールの先頭に (さらに言えばスクリプトでも)
置きますが、 これは慣習であって必須ではありません。import されたモジュール名は import
を行っているモジュールのグローバルなシンボルテーブルに置かれます。

.. % % Modules can import other modules.  It is customary but not required to
.. % % place all \keyword{import} statements at the beginning of a module (or
.. % % script, for that matter).  The imported module names are placed in the
.. % % importing module's global symbol table.

:keyword:`import` 文には、あるモジュール内の名前を、import を実行 しているモジュールのシンボルテーブル内に直接取り込むという変型が
あります。例えば:

.. % % There is a variant of the \keyword{import} statement that imports
.. % % names from a module directly into the importing module's symbol
.. % % table.  For example:

::

   >>> from fibo import fib, fib2
   >>> fib(500)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377

この操作は、import の対象となるモジュール名をローカルな シンボルテーブル内に取り入れることはありません (従って上の例では、 ``fibo``
は定義されません)。

.. % % This does not introduce the module name from which the imports are taken
.. % % in the local symbol table (so in the example, \code{fibo} is not
.. % % defined).

モジュールで定義されている名前を全て import するという変型もあります:

.. % % There is even a variant to import all names that a module defines:

::

   >>> from fibo import *
   >>> fib(500)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377

上の操作は、アンダースコア (``_``) で開始する名前以外の全ての名前を import します。

.. % % This imports all names except those beginning with an underscore
.. % % (\code{_}).


.. _tut-searchpath:

モジュール検索パス
---------

.. index:: triple: module; search; path

:mod:`spam` という名前のモジュールが import されると、インタプリタ は :file:`spam.py`
という名前のファイルを現在のディレクトリ内で探し、 次に環境変数:envvar:`PYTHONPATH` に指定されているディレクトリのリスト
から探します。:envvar:`PYTHONPATH` はシェル変数 :envvar:`PATH` と
同じ構文、すなわちディレクトリ名を並べたものです。:envvar:`PYTHONPATH` が設定されていないか、探しているファイルが見つからなかった場合は、
検索対象をインストール方法に依存するデフォルトのパスにして続けます; Unixでは、このパスは通常
:file:`.:/usr/locall/lib/python` です。

.. % The Module Search Path
.. % % \indexiii{module}{search}{path}
.. % % When a module named \module{spam} is imported, the interpreter searches
.. % % for a file named \file{spam.py} in the current directory,
.. % % and then in the list of directories specified by
.. % % the environment variable \envvar{PYTHONPATH}.  This has the same syntax as
.. % % the shell variable \envvar{PATH}, that is, a list of
.. % % directory names.  When \envvar{PYTHONPATH} is not set, or when the file
.. % % is not found there, the search continues in an installation-dependent
.. % % default path; on \UNIX, this is usually \file{.:/usr/local/lib/python}.

実際には、モジュールは変数 ``sys.path`` で指定されたディレクトリの リストから検索されます。``sys.path`` は、入力とするスクリプトの
入ったディレクトリ (現在のディレクトリ)、:envvar:`PYTHONPATH`、 およびインストール方法依存のデフォルト値を使って初期化されます。
Python プログラマは、自分の行っている操作を理解しているなら、 この変数を使ってモジュール検索パスを修正したり置き換えたりすることが できます。
起動しようとするスクリプトの入ったディレクトリが検索パス上にある ため、スクリプトが標準モジュールと同じ名前をもたないようにすることが
重要です。さもなければ、Python が標準モジュールを import するときに スクリプトをモジュールとして import しようと試みてしまうので注意
してください。このような誤りを犯すと、通常はエラーになります。 詳しくは  :ref:`tut-standardmodules` 節、"標準モジュール."
を参照して ください。

.. % % Actually, modules are searched in the list of directories given by the
.. % % variable \code{sys.path} which is initialized from the directory
.. % % containing the input script (or the current directory),
.. % % \envvar{PYTHONPATH} and the installation-dependent default.  This allows
.. % % Python programs that know what they're doing to modify or replace the
.. % % module search path.  Note that because the directory containing the
.. % % script being run is on the search path, it is important that the
.. % % script not have the same name as a standard module, or Python will
.. % % attempt to load the script as a module when that module is imported.
.. % % This will generally be an error.  See section~\ref{standardModules},
.. % % ``Standard Modules,'' for more information.


"コンパイル" された Python ファイル
-----------------------

たくさんの標準モジュールを使うような短いプログラムで重要となる 起動時間の高速化を行うために、:file:`spam.py` が見つかったディレクトリに
:file:`spam.pyc` という名前のファイルがあった場合には、このファイルを モジュール :mod:`spam` の "バイトコンパイルされた"
バージョン であると仮定します。 :file:`spam.pyc` を生成するのに使われたバージョンの :file:`spam.py` の ファイル修正時刻が
:file:`spam.pyc` に記録されており、この値が 一致しなければ :file:`spam.pyc` ファイルは無視されます。

.. % ``Compiled'' Python files
.. % % As an important speed-up of the start-up time for short programs that
.. % % use a lot of standard modules, if a file called \file{spam.pyc} exists
.. % % in the directory where \file{spam.py} is found, this is assumed to
.. % % contain an already-``byte-compiled'' version of the module \module{spam}.
.. % % The modification time of the version of \file{spam.py} used to create
.. % % \file{spam.pyc} is recorded in \file{spam.pyc}, and the
.. % % \file{.pyc} file is ignored if these don't match.

通常、:file:`spam.pyc` ファイルを生成するために何かをする必要は ありません。:file:`spam.py` が無事コンパイルされると、常に
コンパイルされたバージョンを :file:`spam.pyc` へ書き出すよう 試みます。この試みが失敗してもエラーにはなりません;
何らかの理由でファイルが完全に書き出されなかった場合、作成された :file:`smap.pyc` は無効であるとみなされ、それ以後無視されます。
:file:`spam.pyc` ファイルの内容はプラットフォームに依存しないので、 Python のモジュールのディレクトリは異なるアーキテクチャのマシン間で
共有することができます。

.. % % Normally, you don't need to do anything to create the
.. % % \file{spam.pyc} file.  Whenever \file{spam.py} is successfully
.. % % compiled, an attempt is made to write the compiled version to
.. % % \file{spam.pyc}.  It is not an error if this attempt fails; if for any
.. % % reason the file is not written completely, the resulting
.. % % \file{spam.pyc} file will be recognized as invalid and thus ignored
.. % % later.  The contents of the \file{spam.pyc} file are platform
.. % % independent, so a Python module directory can be shared by machines of
.. % % different architectures.

エキスパートへの助言:

.. % % Some tips for experts:

* Python インタプリタを :option:`-O` フラグ付きで起動すると、 最適化 (optimize) されたコードが生成されて
  :file:`.pyo` ファイルに 保存されます。最適化機構は今のところあまり役に立っていません; 最適化機構は :keyword:`assert` 文と
  ``SET_LINENO`` 命令を除去 しているだけです。:option:`-O` を使うと、*すべての*  バイトコードが最適化されます; ``.pyc``
  ファイルは無視され、 ``.py`` ファイルは最適化されたバイトコードにコンパイルされます。

* 二つの :option:`-O` フラグ (:option:`-OO`) を Python インタプリタへ 渡すと、バイトコードコンパイラは、
  まれにプログラムが正しく動作しなくなるかもしれないような最適化を 実行します。 現状では、ただ ``__doc__`` 文字列をバイトコードから除去して、
  よりコンパクトな :file:`.pyo` ファイルにするだけです。 この文字列が利用できることをあてにしているプログラムがあるかもしれない
  ので、自分の行っている操作が何かわかっているときにだけこのオプションを 使うべきです。

* :file:`.pyc` ファイルや :file:`.pyo` ファイルから 読み出されたとしても、プログラムは何ら高速に動作するわけでは
  ありません。:file:`.pyc` ファイルや :file:`.pyo` ファイルで高速化される のは、読み込まれるときの速度だけです。

* スクリプトの名前をコマンドラインで指定して実行した場合、 そのスクリプトのバイトコードが :file:`.pyc` や :file:`.pyo` に
  書き出されることはありません。従って、スクリプトのほとんどのコードを モジュールに移し、そのモジュールを import する小さなブートストラップ
  スクリプトを作れば、スクリプトの起動時間を短縮できるときがあります。 :file:`.pyc` または :file:`.pyo`
  ファイルの名前を直接コマンドラインに 指定することもできます。

* 一つのモジュールについて、ファイル :file:`spam.py` のない :file:`spam.pyc` (:option:`-O` を使ったときは
  :file:`spam.pyo`)  があってもかまいません。この仕様は、Python コードでできたライブラリを
  リバースエンジニアリングがやや困難な形式で配布するために使えます。

  .. index:: module: compileall

* :mod:`compileall` (XXX reference: ../lib/module-compileall.html)
  は、:file:`.pyc` ファイル (または :option:`-O` を使ったときは:file:`.pyo` ファイル) を
  ディレクトリ内の全てのモジュールに対して生成することができます。

  .. % 


.. _tut-standardmodules:

標準モジュール
=======

.. index:: module: sys

Python には標準モジュールのライブラリが付属しています。ライブラリは 独立したドキュメント Python ライブラリ リファレンス (Python
Library Reference) (XXX reference: ../lib/lib.html)  (以降  "ライブラリリファレンス")
で記述されています。 モジュールによってはインタプリタに組み込まれたものがあります;  インタプリタに組み込まれているモジュールが提供しているのは、
言語の中核の部分ではありませんが、効率化のためや、システムコールのような オペレーティングシステムの根本機能へのアクセス手段を提供するための
操作です。これらのモジュールのセットは設定時に選択可能で、また 根底にあるプラットフォームにも依存します。例えば、:mod:`amoeba`  モジュールは、
Amoeba の根本機能を何らかの形でサポートしているような システムでのみ提供されます。 とりわけ、注目に値するモジュールが一つあります:
:mod:`sys` (XXX reference: ../lib/module-sys.html)  はどの Python インタプリタにも
組み込まれています。変数 ``sys.ps1`` と ``sys.ps2`` は、それぞれ 一次プロンプトと二次プロンプトとして使われる文字列を定義しています:

.. % Standard Modules
.. % % Python comes with a library of standard modules, described in a separate
.. % % document, the \citetitle[../lib/lib.html]{Python Library Reference}
.. % % (``Library Reference'' hereafter).  Some modules are built into the
.. % % interpreter; these provide access to operations that are not part of
.. % % the core of the language but are nevertheless built in, either for
.. % % efficiency or to provide access to operating system primitives such as
.. % % system calls.  The set of such modules is a configuration option which
.. % % also dependson the underlying platform  For example,
.. % % the \module{amoeba} module is only provided on systems that somehow
.. % % support Amoeba primitives.  One particular module deserves some
.. % % attention: \ulink{\module{sys}}{../lib/module-sys.html}%
.. % % {}\refstmodindex{sys}, which is built into every
.. % % Python interpreter.  The variables \code{sys.ps1} and
.. % % \code{sys.ps2} define the strings used as primary and secondary
.. % % prompts:

::

   >>> import sys
   >>> sys.ps1
   '>>> '
   >>> sys.ps2
   '... '
   >>> sys.ps1 = 'C> '
   C> print 'Yuck!'
   Yuck!
   C> 

これらの二つの変数は、インタプリタが対話モードにあるときだけ 定義されています。

.. % % These two variables are only defined if the interpreter is in
.. % % interactive mode.

変数 ``sys.path`` は文字列からなるリストで、インタプリタがモジュール を検索するときのパスを決定します。 ``sys.path`` は環境変数
:envvar:`PYTHONPATH` から得たデフォルトパスに、 :envvar:`PYTHONPATH`
が設定されていなければ組み込みのデフォルト値に設定 されます。標準的なリスト操作で変更することができます:

.. % % The variable \code{sys.path} is a list of strings that determine the
.. % % interpreter's search path for modules. It is initialized to a default
.. % % path taken from the environment variable \envvar{PYTHONPATH}, or from
.. % % a built-in default if \envvar{PYTHONPATH} is not set.  You can modify
.. % % it using standard list operations:

::

   >>> import sys
   >>> sys.path.append('/ufs/guido/lib/python')


.. _tut-dir:

:func:`dir` 関数
==============

組込み関数 :func:`dir` は、あるモジュールがどんな名前を定義して いるか調べるために使われます。 :func:`dir`
はソートされた文字列のリストを返します:

.. % The \function{dir()} Function
.. % % The built-in function \function{dir()} is used to find out which names
.. % % a module defines.  It returns a sorted list of strings:

::

   >>> import fibo, sys
   >>> dir(fibo)
   ['__name__', 'fib', 'fib2']
   >>> dir(sys)
   ['__displayhook__', '__doc__', '__excepthook__', '__name__', '__stderr__',
    '__stdin__', '__stdout__', '_getframe', 'api_version', 'argv', 
    'builtin_module_names', 'byteorder', 'callstats', 'copyright',
    'displayhook', 'exc_clear', 'exc_info', 'exc_type', 'excepthook',
    'exec_prefix', 'executable', 'exit', 'getdefaultencoding', 'getdlopenflags',
    'getrecursionlimit', 'getrefcount', 'hexversion', 'maxint', 'maxunicode',
    'meta_path', 'modules', 'path', 'path_hooks', 'path_importer_cache',
    'platform', 'prefix', 'ps1', 'ps2', 'setcheckinterval', 'setdlopenflags',
    'setprofile', 'setrecursionlimit', 'settrace', 'stderr', 'stdin', 'stdout',
    'version', 'version_info', 'warnoptions']

引数がなければ、:func:`dir` は現在定義している名前を列挙します。

.. % % Without arguments, \function{dir()} lists the names you have defined
.. % % currently:

::

   >>> a = [1, 2, 3, 4, 5]
   >>> import fibo
   >>> fib = fibo.fib
   >>> dir()
   ['__builtins__', '__doc__', '__file__', '__name__', 'a', 'fib', 'fibo', 'sys']

変数、モジュール、関数、その他の、すべての種類の名前をリストすることに 注意してください。

.. % % Note that it lists all types of names: variables, modules, functions, etc.

.. index:: module: __builtin__

:func:`dir` は、組込みの関数や変数の名前はリストしません。 これらの名前からなるリストが必要なら、標準モジュール
:mod:`__builtin__` で定義されています:

.. % % \function{dir()} does not list the names of built-in functions and
.. % % variables.  If you want a list of those, they are defined in the
.. % % standard module \module{__builtin__}\refbimodindex{__builtin__}:

::

   >>> import __builtin__
   >>> dir(__builtin__)
   ['ArithmeticError', 'AssertionError', 'AttributeError', 'DeprecationWarning',
    'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False',
    'FloatingPointError', 'FutureWarning', 'IOError', 'ImportError',
    'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt',
    'LookupError', 'MemoryError', 'NameError', 'None', 'NotImplemented',
    'NotImplementedError', 'OSError', 'OverflowError', 
    'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError',
    'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError',
    'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True',
    'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
    'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
    'UserWarning', 'ValueError', 'Warning', 'WindowsError',
    'ZeroDivisionError', '_', '__debug__', '__doc__', '__import__',
    '__name__', 'abs', 'apply', 'basestring', 'bool', 'buffer',
    'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile',
    'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod',
    'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float',
    'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex',
    'id', 'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter',
    'len', 'license', 'list', 'locals', 'long', 'map', 'max', 'min',
    'object', 'oct', 'open', 'ord', 'pow', 'property', 'quit', 'range',
    'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set',
    'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super',
    'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']


.. _tut-packages:

パッケージ
=====

パッケージ (package) は、Python のモジュール名前空間 を "ドット付きモジュール名 (dotted module names)" を使って
構造化する手段です。例えば、モジュール名 :mod:`A.B` は、 ``A`` というパッケージのサブモジュール ``B`` を表します。
ちょうど、モジュールを利用すると、別々のモジュールの著者が互いの グローバル変数名について心配しなくても済むようになるのと同じように、
ドット付きモジュール名を利用すると、 NumPy や Python Imaging Library のように複数モジュールからなる
パッケージの著者が、互いのモジュール名について心配しなくても済むように なります。

.. % Packages
.. % % Packages are a way of structuring Python's module namespace
.. % % by using ``dotted module names''.  For example, the module name
.. % % \module{A.B} designates a submodule named \samp{B} in a package named
.. % % \samp{A}.  Just like the use of modules saves the authors of different
.. % % modules from having to worry about each other's global variable names,
.. % % the use of dotted module names saves the authors of multi-module
.. % % packages like NumPy or the Python Imaging Library from having to worry
.. % % about each other's module names.

音声ファイルや音声データを一様に扱うためのモジュールのコレクション ("パッケージ") を設計したいと仮定しましょう。音声ファイルには 多くの異なった形式がある
(通常は拡張子、例えば :file:`.wav`,  :file:`.aiff`, :file:`.au` などで認識されます) ので、
様々なファイル形式間で変換を行うためのモジュールからなる、 次第に増えていくモジュールのコレクションを作成したりメンテナンス
したりする必要がありかもしれません。また、音声データに対して 実行したい様々な独自の操作 (ミキシング、エコーの追加、
イコライザ関数の適用、人工的なステレオ効果の作成など) があるかも しれません。そうなると、こうした操作を実行するモジュールを果てしなく
書くことになるでしょう。以下に (階層的なファイルシステムで表現した)  パッケージの構造案を示します:

.. % % Suppose you want to design a collection of modules (a ``package'') for
.. % % the uniform handling of sound files and sound data.  There are many
.. % % different sound file formats (usually recognized by their extension,
.. % % for example: \file{.wav}, \file{.aiff}, \file{.au}), so you may need
.. % % to create and maintain a growing collection of modules for the
.. % % conversion between the various file formats.  There are also many
.. % % different operations you might want to perform on sound data (such as
.. % % mixing, adding echo, applying an equalizer function, creating an
.. % % artificial stereo effect), so in addition you will be writing a
.. % % never-ending stream of modules to perform these operations.  Here's a
.. % % possible structure for your package (expressed in terms of a
.. % % hierarchical filesystem):

::

   Sound/                          トップレベルのパッケージ
         __init__.py               サウンドパッケージを初期化する
         Formats/                  ファイルフォーマット変換用の下位パッケージ
                 __init__.py
                 wavread.py
                 wavwrite.py
                 aiffread.py
                 aiffwrite.py
                 auread.py
                 auwrite.py
                 ...
         Effects/                  サウンド効果用の下位パッケージ
                 __init__.py
                 echo.py
                 surround.py
                 reverse.py
                 ...
         Filters/                  フィルタ用の下位パッケージ
                 __init__.py
                 equalizer.py
                 vocoder.py
                 karaoke.py
                 ...

パッケージを import する際、 Python は ``sys.path`` 上のディレクトリ
を検索して、トップレベルのパッケージの入ったサブディレクトリを探します。

.. % % When importing the package, Python searches through the directories
.. % % on \code{sys.path} looking for a subdirectory containing the
.. % % top-level package.

あるディレクトリを、パッケージが入ったディレクトリとしてPython に 扱わせるには、ファイル :file:`__init__.py` が必要です:
このファイルを置かなければならないのは、``string`` のような よくある名前のディレクトリにより、モジュール検索パスの後の方で見つかる
正しいモジュールが意図せず隠蔽されてしまうのを防ぐためです。 最も簡単なケースでは :file:`__init__.py` はただの空ファイルで
構いませんが、:file:`__init__.py` ではパッケージのための初期化コード を実行したり、後述の ``__all__``
変数を設定してもかまいません。

.. % % The \file{__init__.py} files are required to make Python treat the
.. % % directories as containing packages; this is done to prevent
.. % % directories with a common name, such as \samp{string}, from
.. % % unintentionally hiding valid modules that occur later on the module
.. % % search path. In the simplest case, \file{__init__.py} can just be an
.. % % empty file, but it can also execute initialization code for the
.. % % package or set the \code{__all__} variable, described later.

パッケージのユーザは、個々のモジュールをパッケージから import  することができます。例えば:

.. % % Users of the package can import individual modules from the
.. % % package, for example:

::

   import Sound.Effects.echo

この操作はサブモジュール :mod:`Sound.Effects.echo` をロードします。
このモジュールは、以下のように完全な名前で参照しなければなりません:

.. % % This loads the submodule \module{Sound.Effects.echo}.  It must be referenced
.. % % with its full name.

::

   Sound.Effects.echo.echofilter(input, output, delay=0.7, atten=4)

サブモジュールを import するもう一つの方法を示します:

.. % % An alternative way of importing the submodule is:

::

   from Sound.Effects import echo

これもサブモジュール :mod:`echo` をロードし、:mod:`echo` を パッケージ名を表す接頭辞なしで利用できるようにします。従って以下のように
用いることができます:

.. % % This also loads the submodule \module{echo}, and makes it available without
.. % % its package prefix, so it can be used as follows:

::

   echo.echofilter(input, output, delay=0.7, atten=4)

さらにもう一つのバリエーションとして、必要な関数や変数を直接 import する 方法があります:

.. % % Yet another variation is to import the desired function or variable directly:

::

   from Sound.Effects.echo import echofilter

この操作も同様にサブモジュール :mod:`echo` をロードしますが、 :func:`echofilter` を直接利用できるようにします。

.. % % Again, this loads the submodule \module{echo}, but this makes its function
.. % % \function{echofilter()} directly available:

::

   echofilter(input, output, delay=0.7, atten=4)

``from package import item`` を使う場合、*item* は パッケージ *package* のサブモジュール
(またはサブパッケージ) でも かまいませんし、関数やクラス、変数のような、*package* で定義されて いる別の名前でもかまわないことに注意してください。
``import`` 文はまず、*item* がパッケージ内で定義されているか どうか調べます; 定義されていなければ、*item* はモジュール
名であると仮定して、モジュールをロードしようと試みます。もし モジュールが見つからなければ、:exc:`ImportError` が送出されます。

.. % % Note that when using \code{from \var{package} import \var{item}}, the
.. % % item can be either a submodule (or subpackage) of the package, or some
.. % % other name defined in the package, like a function, class or
.. % % variable.  The \code{import} statement first tests whether the item is
.. % % defined in the package; if not, it assumes it is a module and attempts
.. % % to load it.  If it fails to find it, an
.. % % \exception{ImportError} exception is raised.

反対に、``import item.subitem.subsubitem`` のような構文を 使った場合、最後の ``subsubitem``
を除く各要素はパッケージで なければなりません; 最後の要素はモジュールかパッケージにできますが、
一つ前の要素で定義されているクラスや関数や変数にはできません。

.. % % Contrarily, when using syntax like \code{import
.. % % \var{item.subitem.subsubitem}}, each item except for the last must be
.. % % a package; the last item can be a module or a package but can't be a
.. % % class or function or variable defined in the previous item.


.. _tut-pkg-import-star:

パッケージから \* を import する
----------------------

.. index:: single: __all__

.. % Importing * From a Package
.. % The \code{__all__} Attribute

それでは、ユーザが ``from Sound.Effects import *`` と書いたら、 どうなるのでしょうか？
理想的には、何らかの方法でファイルシステムが 調べられ、そのパッケージにどんなサブモジュールがあるかを調べ上げ、 全てを import
する、という処理を望むことでしょう。残念ながら、 この操作は Mac や Windows のプラットフォームではうまく動作しません。
これらのプラットフォームでは、ファイルシステムはファイル名の 大小文字の区別について正しい情報をもっているとは限らないからです！
こうしたプラットフォームでは、ファイル :file:`ECHO.PY` を モジュール :mod:`echo` として import
すべきか、:mod:`Echo` と すべきかが分かる確かな方法がないからです (例えば、 Windows 95 は
すべてのファイル名の最初の文字を大文字にして表示するという困った 慣習があります)。また、DOS の 8+3 のファイル名制限のせいで、
長いモジュール名に関して別の奇妙な問題が追加されています。

.. % % Now what happens when the user writes \code{from Sound.Effects import
.. % % *}?  Ideally, one would hope that this somehow goes out to the
.. % % filesystem, finds which submodules are present in the package, and
.. % % imports them all.  Unfortunately, this operation does not work very
.. % % well on Mac and Windows platforms, where the filesystem does not
.. % % always have accurate information about the case of a filename!  On
.. % % these platforms, there is no guaranteed way to know whether a file
.. % % \file{ECHO.PY} should be imported as a module \module{echo},
.. % % \module{Echo} or \module{ECHO}.  (For example, Windows 95 has the
.. % % annoying practice of showing all file names with a capitalized first
.. % % letter.)  The DOS 8+3 filename restriction adds another interesting
.. % % problem for long module names.

唯一の解決策は、パッケージの作者にパッケージの索引を明示的に提供 させるというものです。 import 文は次の規約を使います: パッケージの
:file:`__init__.py` コード に ``__all__`` という名前のリストが定義されていれば、 ``from package import
*`` が現れたときに import する リストとして使います。新たなパッケージがリリースされるときに
リストを最新の状態に更新するのはパッケージの作者の責任となります。 自分のパッケージから \* を import するという使い方に同意できなければ、
パッケージの作者は :file:`__init__.py` をサポートしないことにしても かまいません。 例えば、ファイル
``Sounds/Effects/__init__.py`` には、次のような コードを入れてもよいかもしれません:

.. % % The only solution is for the package author to provide an explicit
.. % % index of the package.  The import statement uses the following
.. % % convention: if a package's \file{__init__.py} code defines a list
.. % % named \code{__all__}, it is taken to be the list of module names that
.. % % should be imported when \code{from \var{package} import *} is
.. % % encountered.  It is up to the package author to keep this list
.. % % up-to-date when a new version of the package is released.  Package
.. % % authors may also decide not to support it, if they don't see a use for
.. % % importing * from their package.  For example, the file
.. % % \file{Sounds/Effects/__init__.py} could contain the following code:

::

   __all__ = ["echo", "surround", "reverse"]

このコードは、 ``from Sound.Effects import *`` とすると、 :mod:`Sound` パッケージから指定された 3
つのサブモジュールが  import されることになっている、ということを意味します。

.. % % This would mean that \code{from Sound.Effects import *} would
.. % % import the three named submodules of the \module{Sound} package.

もしも ``__all__`` が定義されていなければ、実行文 ``from Sound.Effects import *`` は、パッケージ
:mod:`Sound.Effects`  の全てのサブモジュールを現在の名前空間の中へ import *しません*; この文は単に
(場合によっては初期化コード :file:`__init__.py` を実行して)  パッケージ :mod:`Sound.Effects` が import
されたということを確認し、 そのパッケージで定義されている名前を全て import するだけです。 import
される名前には、:file:`__init__.py` で定義された名前  (と、明示的にロードされたサブモジュール) が含まれます。
パッケージのサブモジュールで、以前の import 文で明示的にロードされた ものも含みます。以下のコードを考えてください:

.. % % If \code{__all__} is not defined, the statement \code{from Sound.Effects
.. % % import *} does \emph{not} import all submodules from the package
.. % % \module{Sound.Effects} into the current namespace; it only ensures that the
.. % % package \module{Sound.Effects} has been imported (possibly running any
.. % % initialization code in \file{__init__.py}) and then imports whatever names are
.. % % defined in the package.  This includes any names defined (and
.. % % submodules explicitly loaded) by \file{__init__.py}.  It also includes any
.. % % submodules of the package that were explicitly loaded by previous
.. % % import statements.  Consider this code:

::

   import Sound.Effects.echo
   import Sound.Effects.surround
   from Sound.Effects import *

上の例では、echo と surround モジュールが現在の名前空間に import されます。これらのモジュールは ``from...import`` 文が
実行された際に :mod:`Sound.Effects` 内で定義されているからです (この機構は``__all__`` が定義されているときにも働きます)。

.. % % In this example, the echo and surround modules are imported in the
.. % % current namespace because they are defined in the
.. % % \module{Sound.Effects} package when the \code{from...import} statement
.. % % is executed.  (This also works when \code{__all__} is defined.)

一般的には、モジュールやパッケージから ``*`` を import するという やり方には賛同できません。というのは、この操作を行うとしばしば可読性に
乏しいコードになるからです。しかし、対話セッションでキータイプの量を 減らすために使うのは構わないでしょう。それに、特定のモジュールでは、
特定のパターンに従った名前のみを公開 (export) するように設計されています。

.. % % Note that in general the practice of importing \code{*} from a module or
.. % % package is frowned upon, since it often causes poorly readable code.
.. % % However, it is okay to use it to save typing in interactive sessions,
.. % % and certain modules are designed to export only names that follow
.. % % certain patterns.

``from package import specific_submodule`` を使っても何も問題は
ないことに留意してください！実際この表記法は、import を行うモジュールが 他のパッケージかと同じ名前を持つサブモジュールを使わなければ
ならない場合を除いて推奨される方式です。

.. % % Remember, there is nothing wrong with using \code{from Package
.. % % import specific_submodule}!  In fact, this is the
.. % % recommended notation unless the importing module needs to use
.. % % submodules with the same name from different packages.


パッケージ内での参照
----------

サブモジュール同士で互いに参照を行う必要がしばしば起こります。 例えば、:mod:`surround` モジュールは :mod:`echo` モジュールを
使うかもしれません。実際には、このような参照はよくあることなので、 :keyword:`import` 文を実行すると、まず最初に import 文の入っている
パッケージを検索し、その後になって標準のモジュール検索パスを 見に行きます。こうして、:mod:`surround` モジュールは単に ``import
echo`` や  ``from echo import echofilter`` を使うことができます。 import されたモジュールが現在のパッケージ
(現在のモジュールを サブモジュールにしているパッケージ) 内に見つからなかった場合、 :keyword:`import`
文は指定した名前のトップレベルのモジュールを検索 します。

.. % Intra-package References
.. % % The submodules often need to refer to each other.  For example, the
.. % % \module{surround} module might use the \module{echo} module.  In
.. % % fact,
.. % % such references
.. % % are so common that the \keyword{import} statement first looks in the
.. % % containing package before looking in the standard module search path.
.. % % Thus, the \module{surround} module can simply use \code{import echo} or
.. % % \code{from echo import echofilter}.  If the imported module is not
.. % % found in the current package (the package of which the current module
.. % % is a submodule), the \keyword{import} statement looks for a top-level module
.. % % with the given name.

パッケージが (前述の例の :mod:`Sound` パッケージのように)  サブパッケージの集まりに構造化されている場合、兄弟関係にある
パッケージを短縮された記法で参照する方法は存在しません - サブパッケージ の完全な名前を使わなければなりません。例えば、モジュール
:mod:`Sound.Filters.vocoder` で :mod:`Sound.Effects` パッケージの :mod:`echo`
モジュールを使いたいとすると、 ``from Sound.Effects import echo`` を使うことはできます。

.. % % When packages are structured into subpackages (as with the
.. % % \module{Sound} package in the example), there's no shortcut to refer
.. % % to submodules of sibling packages - the full name of the subpackage
.. % % must be used.  For example, if the module
.. % % \module{Sound.Filters.vocoder} needs to use the \module{echo} module
.. % % in the \module{Sound.Effects} package, it can use \code{from
.. % % Sound.Effects import echo}.

Python 2.5 からは、上で説明した暗黙の相対importに加えて、明示的な 相対importを　``from module import name``
の形式のimport文で利用で きます。 この明示的な相対importでは、先頭のドットで現在および親パッケージを指定 して相対importを行います。
:mod:`surround`モジュールの例では、以下の ように記述できます:

.. % % +Starting with Python 2.5, in addition to the implicit relative imports
.. % % +described above, you can write explicit relative imports with the
.. % % +\code{from module import name} form of import statement. These explicit
.. % % +relative imports use leading dots to indicate the current and parent
.. % % +packages involved in the relative import. From the \module{surround}
.. % % +module for example, you might use:

::

   from . import echo
   from .. import Formats
   from ..Filters import equalizer

明示的および暗黙的な相対importのどちらもカレントモジュールの名前をベー スにすることに注意してください。メインモジュールの名前は常に
``"__main__"`` なので、Pythonアプリケーションのメインモジュールとし
て利用されることを意図しているモジュールでは絶対importを利用するべきで す。

.. % % +Note that both explicit and implicit relative imports are based on the
.. % % +name of the current module. Since the name of the main module is always
.. % % +\code{"__main__"}, modules intended for use as the main module of a
.. % % +Python application should always use absolute imports.


複数ディレクトリ中のパッケージ
---------------

パッケージのサポートする特殊な属性には、もう一つ :attr:`__path__` が あります。この属性は、パッケージの
:file:`__init__.py` 中のコードが 実行されるよりも前に、:file:`__init__.py` の収められているディレクトリ名
の入ったリストになるよう初期化されます。 この変数は変更することができます; 変更を加えると、以降そのパッケージに
入っているモジュールやサブパッケージの検索に影響します。

.. % Packages in Multiple Directories
.. % % Packages support one more special attribute, \member{__path__}.  This
.. % % is initialized to be a list containing the name of the directory
.. % % holding the package's \file{__init__.py} before the code in that file
.. % % is executed.  This variable can be modified; doing so affects future
.. % % searches for modules and subpackages contained in the package.

この機能はほとんど必要にはならないのですが、パッケージ内に見つかる モジュールのセットを拡張するために使うことができます。

.. % % While this feature is not often needed, it can be used to extend the
.. % % set of modules found in a package.


.. rubric:: Footnotes

.. [#] 実際には、関数定義も '実行' される '文' です; モジュールを実行すると、関数名はモジュールのグローバルな シンボルテーブルに入力されます。

