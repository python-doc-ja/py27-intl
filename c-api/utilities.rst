.. highlightlang:: c


.. _utilities:

******************
ユーティリティ関数
******************

この章の関数は、 C で書かれたコードをプラットフォーム間で可搬性のあるものにする上で役立つものから、C から Python モジュールを使う
もの、そして関数の引数を解釈したり、 C の値から Python の値を構築するものまで、様々なユーティリティ的タスクを行います。


.. _os:

オペレーティングシステム関連のユーティリティ
============================================


.. cfunction:: int Py_FdIsInteractive(FILE *fp, const char *filename)

   *filename* という名前の標準 I/O ファイル *fp* が対話的 (interactive) であると考えられる場合に真 (非ゼロ) を返します。
   これは ``isatty(fileno(fp))`` が真になるファイルの場合です。グローバルなフラグ :cdata:`Py_InteractiveFlag`
   が真の場合には、 *filename* ポインタが *NULL* か、名前が ``'<stdin>'`` または ``'???'``
   のいずれかに等しい場合にも真を返します。


.. cfunction:: long PyOS_GetLastModificationTime(char *filename)

   ファイル *filename* の最終更新時刻を返します。結果は標準 C ライブラリ関数 :cfunc:`time` が返すタイムスタンプと
   同じ様式で符号化されています。


.. cfunction:: void PyOS_AfterFork()

   プロセスが fork した後の内部状態を更新するための関数です; fork 後 Python インタプリタを使い続ける場合、新たなプロセス内で
   この関数を呼び出さねばなりません。新たなプロセスに新たな実行可能物をロードする場合、この関数を呼び出す必要はありません。


.. cfunction:: int PyOS_CheckStack()

   インタプリタがスタック空間を使い尽くしたときに真を返します。このチェック関数には信頼性がありますが、 :const:`USE_STACKCHECK`
   が定義されている場合 (現状では Microsoft Visual C++ コンパイラでビルドした Windows 版) にしか利用できません .
   :const:`USE_CHECKSTACK` は自動的に定義されます; 自前のコードでこの定義を変更してはなりません。


.. cfunction:: PyOS_sighandler_t PyOS_getsig(int i)

   シグナル *i* に対する現在のシグナルハンドラを返します。この関数は :cfunc:`sigaction` または :cfunc:`signal`
   のいずれかに対する薄いラッパです。 :cfunc:`sigaction` や :cfunc:`signal` を直接呼び出してはなりません!
   :ctype:`PyOS_sighandler_t` は :ctype:`void (\*)(int)` の typedef  による別名です。


.. cfunction:: PyOS_sighandler_t PyOS_setsig(int i, PyOS_sighandler_t h)

   シグナル *i* に対する現在のシグナルハンドラを *h* に設定します; 以前のシグナルハンドラを返します。この関数は
   :cfunc:`sigaction` または :cfunc:`signal` のいずれかに対する薄いラッパです。 :cfunc:`sigaction` や
   :cfunc:`signal` を直接呼び出してはなりません!  :ctype:`PyOS_sighandler_t` は :ctype:`void
   (\*)(int)` の typedef  による別名です。


.. _systemfunctions:

System Functions
================

These are utility functions that make functionality from the :mod:`sys` module
accessible to C code.  They all work with the current interpreter thread's
:mod:`sys` module's dict, which is contained in the internal thread state structure.

.. cfunction:: PyObject *PySys_GetObject(char *name)

   Return the object *name* from the :mod:`sys` module or *NULL* if it does
   not exist, without setting an exception.

.. cfunction:: FILE *PySys_GetFile(char *name, FILE *def)

   Return the :ctype:`FILE*` associated with the object *name* in the
   :mod:`sys` module, or *def* if *name* is not in the module or is not associated
   with a :ctype:`FILE*`.

.. cfunction:: int PySys_SetObject(char *name, PyObject *v)

   Set *name* in the :mod:`sys` module to *v* unless *v* is *NULL*, in which
   case *name* is deleted from the sys module. Returns ``0`` on success, ``-1``
   on error.

.. cfunction:: void PySys_ResetWarnOptions(void)

   Reset :data:`sys.warnoptions` to an empty list.

.. cfunction:: void PySys_AddWarnOption(char *s)

   Append *s* to :data:`sys.warnoptions`.

.. cfunction:: void PySys_SetPath(char *path)

   Set :data:`sys.path` to a list object of paths found in *path* which should
   be a list of paths separated with the platform's search path delimiter
   (``:`` on Unix, ``;`` on Windows).

.. cfunction:: void PySys_WriteStdout(const char *format, ...)

   Write the output string described by *format* to :data:`sys.stdout`.  No
   exceptions are raised, even if truncation occurs (see below).

   *format* should limit the total size of the formatted output string to
   1000 bytes or less -- after 1000 bytes, the output string is truncated.
   In particular, this means that no unrestricted "%s" formats should occur;
   these should be limited using "%.<N>s" where <N> is a decimal number
   calculated so that <N> plus the maximum size of other formatted text does not
   exceed 1000 bytes.  Also watch out for "%f", which can print hundreds of
   digits for very large numbers.

   If a problem occurs, or :data:`sys.stdout` is unset, the formatted message
   is written to the real (C level) *stdout*.

.. cfunction:: void PySys_WriteStderr(const char *format, ...)

   As above, but write to :data:`sys.stderr` or *stderr* instead.

.. _processcontrol:

プロセス制御
============


.. cfunction:: void Py_FatalError(const char *message)

   .. index:: single: abort()

   致命的エラーメッセージ (fatal error message) を出力してプロセスを強制終了 (kill)
   します。後始末処理は行われません。この関数は、Python  インタプリタを使い続けるのが危険であるような状況が検出されたとき;
   例えば、オブジェクト管理が崩壊していると思われるときにのみ、呼び出されるようにしなければなりません。Unixでは、標準 C ライブラリ関数
   :cfunc:`abort` を呼び出して :file:`core` を生成しようと試みます。


.. cfunction:: void Py_Exit(int status)

   .. index::
      single: Py_Finalize()
      single: exit()

   現在のプロセスを終了 (exit) します。この関数は :cfunc:`Py_Finalize` を呼び出し、次いで標準 C ライブラリ関数
   ``exit(status)`` を呼び出します。


.. cfunction:: int Py_AtExit(void (*func) ())

   .. index::
      single: Py_Finalize()
      single: cleanup functions

   :cfunc:`Py_Finalize` から呼び出される後始末処理を行う関数 (cleanup function) を登録します。
   後始末関数は引数無しで呼び出され、値を返しません。最大で 32 の後始末処理関数を登録できます。登録に成功すると、 :cfunc:`Py_AtExit` は
   ``0`` を返します;  失敗すると ``-1`` を返します。最後に登録した後始末処理関数から先に呼び出されます。各関数は高々一度しか呼び出されません。
   Python の内部的な終了処理は後始末処理関数より以前に完了しているので、 *func* からはいかなる Python API も呼び出してはなりません。


.. _importing:

モジュールの import
===================


.. cfunction:: PyObject* PyImport_ImportModule(const char *name)

   .. index::
      single: __all__ (package variable)
      single: package variable; __all__
      single: modules (in module sys)

   この関数は下で述べる :cfunc:`PyImport_ImportModuleEx` を単純化したインタフェースで、 *globals* および
   *locals*  引数を *NULL* のままにし、 *level* を 0 にしたものです。
   *name* 引数にドットが含まれる場合 (あるパッケージのサブモジュールを指定している場合)、
   *fromlist* 引数がリスト ``['*']`` に追加され、戻り値がモジュールを含む
   トップレベルパッケージではなく名前つきモジュール (named module) になるようにします。 (残念ながらこのやり方には、 *name*
   が実際にはサブモジュールでなくサブパッケージを指定している場合、パッケージの  ``__all__``   変数に指定されている
   サブモジュールがロードされてしまうという副作用があります。) import されたモジュールへの新たな参照を返します。失敗した
   場合には例外をセットし、 *NULL* を返します。 Python 2.4 以前では、失敗した場合でもモジュールは生成されていることがあります ---
   ``sys.modules``  を使って調べてください。 Python 2.4 以降では、 import に失敗したモジュールは
   ``sys.modules`` に残りません。

   .. versionchanged:: 2.4
      import に失敗した場合、不完全なモジュールを除去するようになりました.

   .. versionchanged:: 2.6
      always use absolute imports


.. cfunction:: PyObject* PyImport_ImportModuleNoBlock(const char *name)

   This version of :cfunc:`PyImport_ImportModule` does not block. It's intended
   to be used in C functions that import other modules to execute a function.
   The import may block if another thread holds the import lock. The function
   :cfunc:`PyImport_ImportModuleNoBlock` never blocks. It first tries to fetch
   the module from sys.modules and falls back to :cfunc:`PyImport_ImportModule`
   unless the lock is held, in which case the function will raise an
   :exc:`ImportError`.

   .. versionadded:: 2.6


.. cfunction:: PyObject* PyImport_ImportModuleEx(char *name, PyObject *globals, PyObject *locals, PyObject *fromlist)

   .. index:: builtin: __import__

   モジュールを import します。モジュールの import については組み込みの Python 関数 :func:`__import__`
   を読むとよく分かります。というのも、標準の :func:`__import__`  はこの関数を直接呼び出しているからです。

   戻り値は import されたモジュールかトップレベルパッケージへの新たな参照になります。失敗した場合には例外をセットし、 *NULL* を返します
   (Python 2.4 よりも前のバージョンでは、モジュールは生成されている場合があります) :func:`__import__`
   と同じく、パッケージに対してサブモジュールを要求した場合の戻り値は通常、空でない *fromlist* を指定しない限りトップレベルパッケージになります。

   .. versionchanged:: 2.4
      import に失敗した場合、不完全なモジュールを除去するようになりました.

   .. versionchanged:: 2.6
      The function is an alias for :cfunc:`PyImport_ImportModuleLevel` with
      -1 as level, meaning relative import.


.. cfunction:: PyObject* PyImport_ImportModuleLevel(char *name, PyObject *globals, PyObject *locals, PyObject *fromlist, int level)

   Import a module.  This is best described by referring to the built-in Python
   function :func:`__import__`, as the standard :func:`__import__` function calls
   this function directly.

   The return value is a new reference to the imported module or top-level package,
   or *NULL* with an exception set on failure.  Like for :func:`__import__`,
   the return value when a submodule of a package was requested is normally the
   top-level package, unless a non-empty *fromlist* was given.

   .. versionadded:: 2.5


.. cfunction:: PyObject* PyImport_Import(PyObject *name)

   .. index::
      module: rexec
      module: ihooks

   現在の "import フック関数" を呼び出すための高水準のインタフェースです。この関数は現在のグローバル変数辞書内の ``__builtins__``
   から :func:`__import__` 関数を呼び出します。すなわち、現在の環境にインストールされている import フック、例えば
   :mod:`rexec` や :mod:`ihooks` を使って import を行います。

   .. versionchanged:: 2.6
      always use absolute imports


.. cfunction:: PyObject* PyImport_ReloadModule(PyObject *m)

   .. index:: builtin: reload

   モジュールを再ロード (reload) します。モジュールの再ロードについては組み込みの Python 関数 :func:`reload`
   を読むとよく分かります。というのも、標準の :func:`reload`  はこの関数を直接呼び出しているからです。
   戻り値は再ロードしたモジュールかトップレベルパッケージへの新たな参照になります。失敗した場合には例外をセットし、 *NULL* を返します
   (その場合でも、モジュールは生成されている場合があります)


.. cfunction:: PyObject* PyImport_AddModule(const char *name)

   モジュール名に対応するモジュールオブジェクトを返します。 *name* 引数は ``package.module`` の形式でもかまいません。
   まずモジュール辞書に該当するモジュールがあるかどうか調べ、なければ新たなモジュールを生成してモジュール辞書に挿入します。失敗した場合には例外をセットして
   *NULL* を返します。

   .. note::

      この関数はモジュールの import やロードを行いません; モジュールがまだロードされていなければ、空のモジュールオブジェクトを得ることになります。
      :cfunc:`PyImport_ImportModule` やその別形式を使ってモジュールを import してください。ドット名表記で
      指定した *name* が存在しない場合、パッケージ構造は作成されません。


.. cfunction:: PyObject* PyImport_ExecCodeModule(char *name, PyObject *co)

   .. index:: builtin: compile

   モジュール名 (``package.module`` 形式でもかまいません) および Python のバイトコードファイルや組み込み関数
   :func:`compile`  で得られたコードオブジェクトを元にモジュールをロードします。モジュールオブジェクトへの新たな参照を返します。失敗した
   場合には例外をセットし、 *NULL* を返します。Python 2.4 以前では、失敗した場合でもモジュールは生成されていることがありました。 Python
   2.4 以降では、たとえ :cfunc:`PyImport_ExecCodeModule` の処理に入った時に *name* が :attr:``sys.modules``
   に入っていたとしても、 import に失敗したモジュールは :attr:``sys.modules`` に残りません。初期化の不完全なモジュールを
   :attr:``sys.modules`` に残すのは危険であり、そのようなモジュールを import するコードにとっては、モジュールの状態がわからない
   (モジュール作者の意図から外れた壊れた状態かもしれない) からです。

   この関数は、すでに import されているモジュールの場合には再ロードを行います。意図的にモジュールの再ロードを行う方法は
   :cfunc:`PyImport_ReloadModule` を参照してください。

   *name* が ``package.module`` 形式のドット名表記であった場合、まだ作成されていないパッケージ構造はその作成されないままになります。

   .. versionchanged:: 2.4
      エラーが発生した場合に *name* を :attr:``sys.modules`` から除去するようになりました.


.. cfunction:: long PyImport_GetMagicNumber()

   Python バイトコードファイル (いわゆる :file:`.pyc` および :file:`.pyo` ファイル)
   のマジックナンバを返します。マジックナンバはバイトコードファイルの先頭 4 バイトにリトルエンディアン整列で配置されています。


.. cfunction:: PyObject* PyImport_GetModuleDict()

   モジュール管理のための辞書 (いわゆる ``sys.modules`` )を返します。この辞書はインタプリタごとに一つだけある変数なので注意してください。


.. cfunction:: void _PyImport_Init()

   import 機構を初期化します。内部使用だけのための関数です。


.. cfunction:: void PyImport_Cleanup()

   モジュールテーブルを空にします。内部使用だけのための関数です。


.. cfunction:: void _PyImport_Fini()

   import 機構を終了処理します。内部使用だけのための関数です。


.. cfunction:: PyObject* _PyImport_FindExtension(char *, char *)

   内部使用だけのための関数です。


.. cfunction:: PyObject* _PyImport_FixupExtension(char *, char *)

   内部使用だけのための関数です。


.. cfunction:: int PyImport_ImportFrozenModule(char *name)

   *name* という名前のフリーズ (freeze) されたモジュールをロードします。成功すると ``1`` を、モジュールが見つからなかった場合には
   ``0`` を、初期化が失敗した場合には例外をセットして ``-1`` を返します。ロードに成功したモジュールにアクセスするには
   :cfunc:`PyImport_ImportModule` を使ってください。 (Note この関数名はいささか誤称めいています --- この関数はすでに
   import 済みのモジュールをリロードしてしまいます。)


.. ctype:: struct _frozen

   .. index:: single: freeze utility

   :program:`freeze` ユーティリティが生成するようなフリーズ化モジュールデスクリプタの構造体型定義です。 (Python ソース配布物の
   :file:`Tools/freeze/` を参照してください) この構造体の定義は :file:`Include/import.h` にあり、以下のように
   なっています::

      struct _frozen {
          char *name;
          unsigned char *code;
          int size;
      };


.. cvar:: struct _frozen* PyImport_FrozenModules

   このポインタは :ctype:`struct _frozen` のレコードからなり、終端の要素のメンバが *NULL* かゼロになっているような配列
   を指すよう初期化されます。フリーズされたモジュールを import するとき、このテーブルを検索します。サードパーティ製のコードから
   このポインタに仕掛けを講じて、動的に生成されたフリーズ化モジュールの集合を提供するようにできます。


.. cfunction:: int PyImport_AppendInittab(char *name, void (*initfunc)(void))

   既存の組み込みモジュールテーブルに単一のモジュールを追加します。この関数は利便性を目的とした :cfunc:`PyImport_ExtendInittab`
   のラッパ関数で、テーブルが拡張できないときには ``-1`` を返します。新たなモジュールは *name* で import でき、最初に import を
   試みた際に呼び出される関数として *initfunc* を使います。 :cfunc:`Py_Initialize` よりも前に呼び出さねばなりません。


.. ctype:: struct _inittab

   組み込みモジュールリスト内の一つのエントリを記述している構造体です。リスト内の各構造体には、インタプリタ内に組み込まれているモジュールの
   名前と初期化関数が指定されています。 Python を埋め込むようなプログラムは、この構造体の配列と
   :cfunc:`PyImport_ExtendInittab` を組み合わせて、追加の
   組み込みモジュールを提供できます。構造体は :file:`Include/import.h`  で以下のように定義されています::

      struct _inittab {
          char *name;
          void (*initfunc)(void);
      };


.. cfunction:: int PyImport_ExtendInittab(struct _inittab *newtab)

   組み込みモジュールのテーブルに一群のモジュールを追加します。配列 *newtab* は :attr:`name` フィールドが *NULL* になっている
   センチネル (sentinel) エントリで終端されていなければなりません; センチネル値を与えられなかった場合にはメモリ違反になるかもしれません。成功すると
   ``0`` を、内部テーブルを拡張するのに十分なメモリを確保できなかった場合には ``-1`` を返します。操作が失敗した場合、
   モジュールは一切内部テーブルに追加されません。 :cfunc:`Py_Initialize` よりも前に呼び出さねばなりません。


.. _marshalling-utils:

データ整列化 (data marshalling) のサポート
==========================================

以下のルーチン群は、 :mod:`marshal` モジュールと同じ形式を使った整列化オブジェクトを C コードから使えるようにします。
整列化形式でデータを書き出す関数に加えて、データを読み戻す関数もあります。整列化されたデータを記録するファイルはバイナリモードで
開かれていなければなりません。

数値は最小桁が先にくるように記録されます。

このモジュールでは、二つのバージョンのデータ形式をサポートしています。バージョン 0 は従来のもので、(Python 2.4 で新たに追加された) バージョン
1  は intern 化された文字列をファイル内で共有し、逆マーシャル化の時にも共有されるようにします。 *PY_MARSHAL_VERSION*
は現在のバージョン (バージョン 1) を示します。


.. cfunction:: void PyMarshal_WriteLongToFile(long value, FILE *file, int version)

   :ctype:`long` 型の整数値 *value* を *file* へ整列化します。この関数は *value* の下桁 32 ビットを書き込むだけです;
   ネイティブの :ctype:`long` 型サイズには関知しません。

   .. versionchanged:: 2.4
      ファイル形式を示す *version* が追加されました.


.. cfunction:: void PyMarshal_WriteObjectToFile(PyObject *value, FILE *file, int version)

   Python オブジェクト *value* を *file* へ整列化します。

   .. versionchanged:: 2.4
      ファイル形式を示す *version* が追加されました.


.. cfunction:: PyObject* PyMarshal_WriteObjectToString(PyObject *value, int version)

   *value* の整列化表現が入った文字列オブジェクトを返します。

   .. versionchanged:: 2.4
      ファイル形式を示す *version* が追加されました.

以下の関数を使うと、整列化された値を読み戻せます。

.. % XXX What about error detection?  It appears that reading past the end
.. % of the file will always result in a negative numeric value (where
.. % that's relevant), but it's not clear that negative values won't be
.. % handled properly when there's no error.  What's the right way to tell?
.. % Should only non-negative values be written using these routines?


.. cfunction:: long PyMarshal_ReadLongFromFile(FILE *file)

   読み出し用に開かれた :ctype:`FILE\*` 内のデータストリームから、 C の :ctype:`long` 型データを読み出して返します。
   この関数は、ネイティブの :ctype:`long` のサイズに関係なく、 32 ビットの値だけを読み出せます。


.. cfunction:: int PyMarshal_ReadShortFromFile(FILE *file)

   読み出し用に開かれた :ctype:`FILE\*` 内のデータストリームから、 C の :ctype:`short` 型データを読み出して返します。
   この関数は、ネイティブの :ctype:`short` のサイズに関係なく、 16 ビットの値だけを読み出せます。


.. cfunction:: PyObject* PyMarshal_ReadObjectFromFile(FILE *file)

   読み出し用に開かれた :ctype:`FILE\*` 内のデータストリームから、 Python オブジェクトを読み出して返します。
   エラーが生じた場合、適切な例外 (:exc:`EOFError` または :exc:`TypeError`) を送出して *NULL* を返します。


.. cfunction:: PyObject* PyMarshal_ReadLastObjectFromFile(FILE *file)

   読み出し用に開かれた :ctype:`FILE\*` 内のデータストリームから、 Python オブジェクトを読み出して返します。
   :cfunc:`PyMarshal_ReadObjectFromFile` と違い、この関数はファイル中に後続のオブジェクトが存在しないと仮定し、ファイルから
   メモリ上にファイルデータを一気にメモリにロードして、逆整列化機構がファイルから一バイトづつ読み出す代わりにメモリ上のデータを操作
   できるようにします。対象のファイルから他に何も読み出さないと分かっている場合にのみ、この関数を使ってください。エラーが生じた場合、適切な例外
   (:exc:`EOFError` または :exc:`TypeError`) を送出して *NULL* を返します。


.. cfunction:: PyObject* PyMarshal_ReadObjectFromString(char *string, Py_ssize_t len)

   *string* が指している *len* バイトの文字列バッファに納められたデータストリームから Python オブジェクトを読み出して返します。
   エラーが生じた場合、適切な例外 (:exc:`EOFError` または :exc:`TypeError`) を送出して *NULL* を返します。


.. _arg-parsing:

引数の解釈と値の構築
====================

これらの関数は独自の拡張モジュール用の関数やメソッドを作成する際に便利です。詳しい情報や用例は Python インタプリタの拡張と埋め込み (XXX
reference: ../ext/ext.html) にあります。

最初に説明する 3 つの関数、 :cfunc:`PyArg_ParseTuple` 、
:cfunc:`PyArg_ParseTupleAndKeywords` 、および :cfunc:`PyArg_Parse` はいずれも *書式化文字列
(format string)* を使います。書式化文字列は、関数が受け取るはずの引数に関する情報を伝えるのに
用いられます。いずれの関数における書式化文字列も、同じ書式を使っています。

書式化文字列は、ゼロ個またはそれ以上の "書式化単位 (format unit)" から成り立ちます。一つの書式化単位は一つの Python オブジェクトを
表します; 通常は単一の文字か、書式化単位からなる文字列を括弧で囲ったものになります。例外として、括弧で囲われていない
書式化単位文字列が単一のアドレス引数に対応する場合がいくつかあります。以下の説明では、引用符のついた形式は書式化単位です;
(丸)括弧で囲った部分は書式化単位に対応する Python のオブジェクト型です; [角] 括弧は値をアドレス渡しする際に使う C の変数型です。

``s`` (文字列型または Unicode オブジェクト型) [const char \*]
   Python の文字列または Unicode オブジェクトを、キャラクタ文字列を指す C のポインタに変換します。
   変換先の文字列自体の記憶領域を提供する必要はありません; キャラクタ型ポインタ変数のアドレスを渡すと、すでに存在している
   文字列へのポインタをその変数に記録します。C 文字列は NUL で終端されています。Python の文字列型は、NUL バイトが途中に埋め込まれて
   いてはなりません; もし埋め込まれていれば :exc:`TypeError` 例外を送出します。Unicode オブジェクトはデフォルトエンコーディングを使って
   C 文字列に変換されます。変換に失敗すると :exc:`UnicodeError` を送出します。

``s#`` (文字列型、Unicode オブジェクト型または任意の読み出しバッファ互換型) [const char \*, int]
   これは ``s`` の変化形で、値を二つの変数に記録します。一つ目の変数はキャラクタ文字列へのポインタで、二つ目はその長さです。
   この書式化単位の場合には、Python 文字列に null バイトが埋め込まれていてもかまいません。 Unicode オブジェクトの場合、デフォルト
   エンコーディングでの変換が可能ならば、変換したオブジェクトから文字列へのポインタを返します。その他の読み出しバッファ互換オブジェクトは
   生の内部データ表現への参照を返します。

``z `` (文字列型または `` None``) [const char \*]
   ``s`` に似ていますが、Python オブジェクトは ``None`` でもよく、その場合には C のポインタは *NULL* にセットされます。

``z# `` (文字列型、`` None``、または任意の読み出しバッファ互換型) [const char \*, int]
   ``s#`` の ``s`` を ``z`` にしたような意味です。

``u`` (Unicode オブジェクト型) [Py_UNICODE \*]
   Python の Unicode オブジェクトを、NUL で終端された 16 ビットの Unicode (UTF-16) データに変換します。 ``s``
   と同様に、 Unicode データバッファ用に記憶領域を提供する必要はありません; :ctype:`Py_UNICODE`
   型ポインタ変数のアドレスを渡すと、すでに存在している Unicode データへのポインタをその変数に記録します。

``u#`` (Unicode オブジェクト型) [Py_UNICODE \*, int]
   これは ``u`` の変化形で、値を二つの変数に記録します。一つ目の変数は Unicode データバッファへのポインタで、二つ目はその長さです。非
   Unicode のオブジェクトの場合、読み出しバッファのポインタを :ctype:`Py_UNICODE` 型シーケンスへのポインタと解釈して扱います。

``es`` (文字列型、Unicode オブジェクト型または任意の読み出しバッファ互換型)[const char \*encoding, char \*\*buffer]
   これは ``s`` の変化形で、Unicode オブジェクトや Unicode に変換可能なオブジェクトをキャラクタ型バッファにエンコードするために
   用いられます。NUL バイトが埋め込まれていない文字列でのみ動作します。

   この書式化単位には二つの引数が必要です。一つ目は入力にのみ用いられ、 NUL で終端されたエンコード名文字列を指す :ctype:`const char\*`
   型でなければなりません。指定したエンコード名を Python が理解できない場合には例外を送出します。第二の引数は :ctype:`char\*\*`
   でなければなりません; この引数が参照しているポインタの値は、引数に指定したテキストの内容が入ったバッファへのポインタになります。
   テキストは最初の引数に指定したエンコード方式でエンコードされます。

   :cfunc:`PyArg_ParseTuple` を使うと、必要なサイズのバッファを確保し、そのバッファにエンコード後のデータをコピーして、
   *\*buffer* がこの新たに確保された記憶領域を指すように変更します。呼び出し側には、確保されたバッファを使い終わった後に
   :cfunc:`PyMem_Free` で解放する責任があります。

``et`` (文字列型、Unicode オブジェクト型または文字列バッファ互換型) [const char \*encoding, char \*\*buffer]
   ``es`` と同じです。ただし、8 ビット幅の文字列オブジェクトをエンコードし直さずに渡します。その代わり、実装では文字列オブジェクトが
   パラメタに渡したエンコードを使っているものと仮定します。

``es#`` (文字列型、Unicode オブジェクト型または文字列バッファ互換型) [const char \*encoding, char \*\*buffer, int \*buffer_length]
   ``s#`` の変化形で、Unicode オブジェクトや Unicode に変換可能なオブジェクトをキャラクタ型バッファにエンコードするために
   用いられます。 ``es`` 書式化単位と違って、この変化形はバイトが埋め込まれていてもかまいません。

   この書式化単位には三つの引数が必要です。一つ目は入力にのみ用いられ、 NUL で終端されたエンコード名文字列を指す :ctype:`const char\*`
   型か *NULL* でなければなりません。 *NULL* の場合にはデフォルトエンコーディングを使います。指定したエンコード名を Python が理解できない
   場合には例外を送出します。第二の引数は :ctype:`char\*\*` でなければなりません; この引数が参照しているポインタの値は、引数に指定した
   テキストの内容が入ったバッファへのポインタになります。テキストは最初の引数に指定したエンコード方式でエンコードされます。
   第三の引数は整数へのポインタでなければなりません; ポインタが参照している整数の値は出力バッファ内のバイト数にセットされます。

   この書式化単位の処理には二つのモードがあります:

   *\*buffer * が* NULL* ポインタを指している場合、関数は必要なサイズのバッファを確保し、そのバッファにエンコード後の
   データをコピーして、*\*buffer* がこの新たに確保された記憶領域を指すように変更します。呼び出し側には、確保されたバッファを使い終わった後に
   :cfunc:`PyMem_Free` で解放する責任があります。

   *\*buffer* が非 *NULL* のポインタ (すでにメモリ確保済みのバッファ) を指している場合、 :cfunc:`PyArg_ParseTuple`
   はこのメモリ位置をバッファとして用い、*\*buffer_length*
   の初期値をバッファサイズとして用います。 :cfunc:`PyArg_ParseTuple`  は次にエンコード済みのデータをバッファにコピーして、NUL で終端
   します。バッファの大きさが足りなければ :exc:`ValueError`  がセットされます。

   どちらの場合も、 *\*buffer_length* は終端の NUL バイトを含まないエンコード済みデータの長さにセットされます。

``et#`` (文字列型、Unicode オブジェクト型または文字列バッファ互換型) [const char \*encoding, char \*\*buffer]
   ``es#`` と同じです。ただし、文字列オブジェクトをエンコードし直さずに渡します。その代わり、実装では文字列オブジェクトが
   パラメタに渡したエンコードを使っているものと仮定します。

``b`` (整数型) [char]
   Python の整数型を、 C の :ctype:`char` 型の小さな整数に変換します。

``B`` (整数型) [unsigned char]
   Python の整数型を、オーバフローチェックを行わずに、 C の  :ctype:`unsigned char` 型の小さな整数に変換します。

   .. versionadded:: 2.3

``h`` (整数型) [short int]
   Python の整数型を、 C の :ctype:`short int` 型に変換します。

``H`` (整数型) [unsigned short int]
   Python の整数型を、オーバフローチェックを行わずに、 C の  :ctype:`unsigned short int` 型に変換します。

   .. versionadded:: 2.3

``i`` (整数型) [int]
   Python の整数型を、 C の :ctype:`int` 型に変換します。

``I`` (整数型) [unsigned int]
   Python の整数型を、オーバフローチェックを行わずに、 C の  :ctype:`unsigned int` 型に変換します。

   .. versionadded:: 2.3

``l`` (整数型) [long int]
   Python の整数型を、 C の :ctype:`long int` 型に変換します。

``k`` (整数型) [unsigned long]
   Python の整数型もしくは長整数型を、オーバフローチェックを行わずに、 C の  :ctype:`unsigned long int` 型に変換します。

   .. versionadded:: 2.3

``L`` (整数型) [PY_LONG_LONG]
   Python の整数型を、 C の :ctype:`long long` 型に変換します。この書式化単位は、 :ctype:`long long` 型 (または
   Windows の  :ctype:`_int64` 型) がサポートされているプラットフォームでのみ利用できます。 Convert a Python
   integer to a C :ctype:`long long`.  This format is only available on platforms
   that support :ctype:`long long` (or :ctype:`_int64` on Windows).

``K`` (整数型) [unsigned PY_LONG_LONG]
   Python の整数型もしくは長整数型を、オーバフローチェックを行わずに、 C の  :ctype:`unsigned long long` 型に変換します。
   この書式化単位は、 :ctype:`unsigned long long` 型 (または Windows の  :ctype:`unsigned _int64`
   型) がサポートされているプラットフォームでのみ利用できます。

   .. versionadded:: 2.3

``n`` (integer) [Py_ssize_t]
   Python の整数型もしくは長整数型をCの :ctype:`Py_ssize_t` 型に変換します。

   .. versionadded:: 2.5

``c`` (長さ 1 の文字列型) [char]
   長さ 1 の文字列として表現されている Python キャラクタを C の :ctype:`char` 型に変換します。

``f`` (浮動小数点型) [float]
   Python の浮動小数点型を、 C の :ctype:`float` 型に変換します。

``d`` (浮動小数点型) [double]
   Python の浮動小数点型を、 C の :ctype:`double` 型に変換します。

``D`` (複素数型) [Py_complex]
   Python の複素数型を、 C の :ctype:`Py_complex` 構造体に変換します。

``O`` (オブジェクト) [PyObject \*]
   Python オブジェクトを (一切変換を行わずに) C の Python オブジェクト型ポインタに保存します。これにより、C
   プログラムは実際のオブジェクトを受け渡しされます。オブジェクトの参照カウントは増加しません。保存されるポインタが *NULL* になることはありません。

``O!`` (オブジェクト) [*typeobject*, PyObject \*]
   Python オブジェクトを C の Python オブジェクト型ポインタに保存します。 ``O`` に似ていますが、二つの C の引数をとります:
   一つ目の引数は Python の型オブジェクトへのアドレスで、二つ目の引数はオブジェクトへのポインタが保存されている (:ctype:`PyObject\*`
   の) C の変数へのアドレスです。Python オブジェクトが指定した型ではない場合、 :exc:`TypeError` を送出します。

``O&`` (オブジェクト) [*converter*, *anything*]
   Python オブジェクトを *converter* 関数を介して C の変数に変換します。二つの引数をとります: 一つ目は関数で、二つ目は (任意の型の)
   C 変数へのアドレスを :ctype:`void \*` 型に変換したものです。 *converter* は以下のようにして呼び出されます:

   *status* ``=``*converter *``(``* object*, *address* ``);``

   ここで *object* は変換対象の Python オブジェクトで、 *address* は :cfunc:`PyArg_Parse\*` に渡した
   :ctype:`void\*`  型の引数です。戻り値 *status* は変換に成功した際に ``1`` 、失敗した場合には ``0``
   になります。変換に失敗した場合、 *converter* 関数は例外を送出しなくてはなりません。

``S`` (文字列型) [PyStringObject \*]
   ``O`` に似ていますが、Python オブジェクトは文字列オブジェクトでなければなりません。
   オブジェクトが文字列オブジェクトでない場合には :exc:`TypeError` を送出します。 C 変数は :ctype:`PyObject\*`
   で宣言しておいてもかまいません。

``U`` (Unicode 文字列型) [PyUnicodeObject \*]
   ``O`` に似ていますが、Python オブジェクトは Unicode オブジェクトでなければなりません。オブジェクトが Unicode
   オブジェクトでない場合には :exc:`TypeError` を送出します。 C 変数は :ctype:`PyObject\*` で宣言しておいてもかまいません。

``t#`` (読み出し専用キャラクタバッファ) [char \*, int]
   ``s#`` に似ていますが、読み出し専用バッファインタフェースを実装している任意のオブジェクトを受理します。 :ctype:`char\*`
   変数はバッファの最初のバイトを指すようにセットされ、 :ctype:`int` はバッファの長さにセットされます。
   単一セグメントからなるバッファオブジェクトだけを受理します; それ以外の場合には :exc:`TypeError` を送出します。

``w`` (読み書き可能なキャラクタバッファ) [char \*]
   ``s`` と同様ですが、読み書き可能なバッファインタフェースを実装している任意のオブジェクトを受理します。
   呼び出し側は何らかの別の手段でバッファの長さを決定するか、あるいは ``w#`` を使わねばなりません。
   単一セグメントからなるバッファオブジェクトだけを受理します; それ以外の場合には :exc:`TypeError` を送出します。

``w#`` (読み書き可能なキャラクタバッファ) [char \*, int]
   ``s#`` に似ていますが、読み書き可能なバッファインタフェースを実装している任意のオブジェクトを受理します。 :ctype:`char\*`
   変数はバッファの最初のバイトを指すようにセットされ、 :ctype:`int` はバッファの長さにセットされます。
   単一セグメントからなるバッファオブジェクトだけを受理します; それ以外の場合には :exc:`TypeError` を送出します。

``(items)`` (タプル) [*matching-items*]
   オブジェクトは *items* に入っている書式化単位の数だけの長さを持つ Python のシーケンス型でなくてはなりません。各 C 引数は *items* 内の
   個々の書式化単位に対応づけできねばなりません。シーケンスの書式化単位は入れ子構造にできます。

   .. note::

      Python のバージョン 1.5.2 より以前は、この書式化指定文字列はパラメタ列ではなく、個別のパラメタが入ったタプルでなければなりません
      でした。このため、以前は :exc:`TypeError` を引き起こしていたようなコードが現在は例外を出さずに処理されるかもしれません。
      とはいえ、既存のコードにとってこれは問題ないと思われます。

Python 整数型を要求している場所に Python 長整数型を渡すのは可能です; しかしながら、適切な値域チェックはまったく行われません ---
値を受け取るためのフィールドが、値全てを受け取るには小さすぎる場合、上桁のビット群は暗黙のうちに切り詰められます (実際のところ、このセマンティクスは C
のダウンキャスト (downcast) から継承しています --- その恩恵は人それぞれかもしれませんが)。

その他、書式化文字列において意味を持つ文字がいくつかあります。それらの文字は括弧による入れ子内には使えません。以下に文字を示します:

``|``
   Python 引数リスト中で、この文字以降の引数がオプションであることを示します。オプションの引数に対応する C の変数はデフォルトの値で初期化して
   おかねばなりません --- オプションの引数が省略された場合、 :cfunc:`PyArg_ParseTuple` は対応する C 変数の内容に
   手を加えません。

``:``
   この文字があると、書式化単位の記述はそこで終わります; コロン以降の文字列は、エラーメッセージにおける関数名
   (:cfunc:`PyArg_ParseTuple` が送出する例外の "付属値 (associated value)") として使われます。

``;``
   この文字があると、書式化単位の記述はそこで終わります; セミコロン以降の文字列は、デフォルトエラーメッセージを *置き換える*
   エラーメッセージとして使われます。言うまでもなく、 ``:`` と ``;`` は相互に排他の文字です。

呼び出し側に提供される Python オブジェクトの参照は全て  *借りた (borrowed)* ものです; オブジェクトの参照カウントを
デクリメントしてはなりません!

以下の関数に渡す補助引数 (additional argument) は、書式化文字列から決定される型へのアドレスでなければなりません; 補助引数に指定した
アドレスは、タプルから入力された値を保存するために使います。上の書式化単位のリストで説明したように、補助引数を入力値として使う場合がいくつかあります;
その場合、対応する書式化単位の指定する形式に従うようにせねばなりません。

変換を正しく行うためには、 *arg* オブジェクトは書式化文字に一致しなければならず、かつ書式化文字列内の書式化単位に全て値が入るようにせねばなりません。
成功すると、 :cfunc:`PyArg_Parse\*` 関数は真を返します。それ以外の場合には偽を返し、適切な例外を送出します。


.. cfunction:: int PyArg_ParseTuple(PyObject *args, const char *format, ...)

   固定引数のみを引数にとる関数のパラメタを解釈して、ローカルな変数に変換します。成功すると真を返します;失敗すると偽を返し、適切な例外を送出します。


.. cfunction:: int PyArg_VaParse(PyObject *args, const char *format, va_list vargs)

   :cfunc:`PyArg_ParseTuple` と同じですが、可変長の引数ではなく *va_list* を引数にとります。


.. cfunction:: int PyArg_ParseTupleAndKeywords(PyObject *args, PyObject *kw, const char *format, char *keywords[], ...)

   固定引数およびキーワード引数をとる関数のパラメタを解釈して、ローカルな変数に変換します。成功すると真を返します;失敗すると偽を返し、適切な例外を送出します。


.. cfunction:: int PyArg_VaParseTupleAndKeywords(PyObject *args, PyObject *kw, const char *format, char *keywords[], va_list vargs)

   :cfunc:`PyArg_ParseTupleAndKeywords` と同じですが、可変長の引数ではなく *va_list* を引数にとります。


.. cfunction:: int PyArg_Parse(PyObject *args, const char *format, ...)

   "旧スタイル" の関数における引数リストを分析するために使われる関数です --- 旧スタイルの関数は、引数解釈手法に
   :const:`METH_OLDARGS` を使います。新たに書かれるコードでのパラメタ解釈にはこの関数の使用は奨められず、
   標準のインタプリタにおけるほとんどのコードがもはや引数解釈のためにこの関数を使わないように変更済みです。
   この関数を残しているのは、この関数が依然として引数以外のタプルを分析する上で便利だからですが、この目的においては将来も使われつづけるかもしれません。


.. cfunction:: int PyArg_UnpackTuple(PyObject *args, const char *name, Py_ssize_t min, Py_ssize_t max, ...)

   パラメータ取得を簡単にした形式で、引数の型を指定する書式化文字列を使いません。パラメタの取得にこの手法を使う関数は、関数宣言テーブル、またはメソッド
   宣言テーブル内で :const:`METH_VARARGS` として宣言しなくてはなりません。実引数の入ったタプルは *args* に渡します;
   このタプルは本当のタプルでなくてはなりません。タプルの長さは少なくとも *min* で、 *max* を超えてはなりません; *min* と *max*
   が等しくてもかまいません。補助引数を関数に渡さなくてはならず、各補助引数は :ctype:`PyObject\*`  変数へのポインタでなくてはなりません;
   これらの補助引数には、 *args* の値が入ります; 値の参照は借りた参照です。オプションのパラメタに対応する変数のうち、 *args* に指定していない
   ものには値が入りません; 呼び出し側はそれらの値を初期化しておかねばなりません。この関数は成功すると真を返し、 *args* がタプルでない場合や
   間違った数の要素が入っている場合に偽を返します; 何らかの失敗が起きた場合には例外をセットします。

   この関数の使用例を以下に示します。この例は、弱参照のための :mod:`_weakref` 補助モジュールのソースコードからとったものです::

      static PyObject *
      weakref_ref(PyObject *self, PyObject *args)
      {
          PyObject *object;
          PyObject *callback = NULL;
          PyObject *result = NULL;

          if (PyArg_UnpackTuple(args, "ref", 1, 2, &object, &callback)) {
              result = PyWeakref_NewRef(object, callback);
          }
          return result;
      }

   この例における :cfunc:`PyArg_UnpackTuple` 呼び出しは、 :cfunc:`PyArg_ParseTuple` を使った以下の呼び出し::

      PyArg_ParseTuple(args, "O|O:ref", &object, &callback)

   と全く等価です。

   .. versionadded:: 2.2


.. cfunction:: PyObject* Py_BuildValue(const char *format, ...)

   :cfunc:`PyArg_Parse\*` ファミリの関数が受け取るのと似た形式の書式化文字列および値列に基づいて、新たな値を生成します。
   生成した値を返します。エラーの場合には *NULL* を返します; *NULL* を返す場合、例外を送出するでしょう。

   :cfunc:`Py_BuildValue` は常にタプルを生成するとは限りません。この関数がタプルを生成するのは、書式化文字列に二つ以上の書式化単位
   が入っているときだけです。書式化文字列が空の場合、 ``None``  を返します; 書式化単位が厳密に一つだけ入っている場合、
   書式化単位で指定されている何らかのオブジェクト単体を返します。サイズがゼロや 1 のタプルを返すように強制するには、丸括弧で囲われた書式化文字列を使います。

   書式化単位 ``s`` や ``s#`` の場合のように、オブジェクトを構築する際にデータを供給するためにメモリバッファをパラメタとして渡す
   場合には、指定したデータはコピーされます。 :cfunc:`Py_BuildValue` が生成したオブジェクトは、呼び出し側が提供したバッファを決して参照
   しません。別の言い方をすれば、 :cfunc:`malloc` を呼び出してメモリを確保し、それを :cfunc:`Py_BuildValue`
   に渡した場合、コード内で :cfunc:`Py_BuildValue` が返った後で :cfunc:`free` を呼び出す責任があるということです。

   以下の説明では、引用符のついた形式は書式化単位です; (丸)括弧で囲った部分は書式化単位が返す Python のオブジェクト型です; [角]
   括弧は関数に渡す値の C 変数型です。

   書式化文字列内では、(``s#`` のような書式化単位を除いて) スペース、タブ、コロンおよびコンマは無視されます。
   これらの文字を使うと、長い書式化文字列をちょっとだけ読みやすくできます。

   ``s`` (文字列型) [char \*]
      null 終端された C 文字列から Python オブジェクトに変換します。 C 文字列ポインタが *NULL* の場合、 ``None`` になります。

   ``s#`` (文字列型) [char \*, int]
      C 文字列とその長さから Python オブジェクトに変換します。 C 文字列ポインタが *NULL* の場合、長さは無視され ``None`` になります。

   ``z`` (string or ``None``) [char \*]
      ``s`` と同じです。

   ``z#`` (string or ``None``) [char \*, int]
      ``s#`` と同じです。

   ``u`` (Unicode string) [Py_UNICODE \*]
      null 終端された Unicode (UCS-2 または UCS-4) データのバッファから Python オブジェクトに変換します。 Unicode
      バッファポインタが *NULL* の場合、 ``None`` になります。

   ``u#`` (Unicode string) [Py_UNICODE \*, int]
      null 終端された Unicode (UCS-2 または UCS-4) データのバッファとその長さから Python オブジェクトに変換します。
      Unicode バッファポインタが *NULL* の場合、長さは無視され ``None`` になります。

   ``i`` (整数型) [int]
      通常の C の :ctype:`int` を Python の整数オブジェクトに変換します。

   ``b`` (整数型) [char]
      ``i`` と同じです。通常のC の :ctype:`char` を Python の整数オブジェクトに変換します。

   ``h`` (整数型) [short int]
      通常のC の :ctype:`short int` を Python の整数オブジェクトに変換します。

   ``l`` (整数型) [long int]
      C の :ctype:`long int` を Python の整数オブジェクトに変換します。

   ``B`` (integer) [unsigned char]
      C の :ctype:`unsigned char` を Python の整数オブジェクトに変換します。

   ``H`` (integer) [unsigned short int]
      C の :ctype:`unsigned short int` を Python の整数オブジェクトに変換します。

   ``I`` (integer/long) [unsigned int]
      C の :ctype:`unsigned int` を Python の整数オブジェクト、あるいは、値が ``sys.maxint``
      より大きければ長整数オブジェクトに変換します。

   ``k`` (integer/long) [unsigned long]
      C の :ctype:`unsigned long` を Python の整数オブジェクト、あるいは、値が ``sys.maxint``
      より大きければ長整数オブジェクトに変換します。

   ``L`` (long) [PY_LONG_LONG]
      C の :ctype:`long long` を Python の長整数オブジェクトに変換します。 :ctype:`long long`
      をサポートしているプラットフォームでのみ利用可能です。

   ``K`` (long) [unsigned PY_LONG_LONG]
      C の :ctype:`unsigned long long` を Python の長整数オブジェクトに変換します。 :ctype:`long long`
      をサポートしているプラットフォームでのみ利用可能です。

   ``n`` (int) [Py_ssize_t]
      C の :ctype:`unsigned long` を Python の整数オブジェクト、あるいは長整数オブジェクトに変換します。

      .. versionadded:: 2.5

   ``c`` (string of length 1) [char]
      文字を表す通常の C の :ctype:`int` を、長さ 1 の Python の文字列オブジェクトに変換します。

   ``d`` (浮動小数点型) [double]
      C の :ctype:`double` を Python の浮動小数点数に変換します。

   ``f`` (浮動小数点型) [float]
      ``d`` と同じです。

   ``D`` (複素数型) [Py_complex \*]
      C の :ctype:`Py_complex` 構造体を Python の複素数に変換します。

   ``O`` (オブジェクト) [PyObject \*]
      Python オブジェクトを手を加えずに渡します (ただし、参照カウントは 1 インクリメントします)。渡したオブジェクトが *NULL* ポインタ
      の場合、この引数を生成するのに使った何らかの呼び出しがエラーになったのが原因であると仮定して、例外をセットします。従ってこのとき
      :cfunc:`Py_BuildValue` は *NULL* を返しますが :cfunc:`Py_BuildValue` 自体は例外を送出しません。
      例外をまだ送出していなければ :exc:`SystemError` をセットします。

   ``S`` (オブジェクト) [PyObject \*]
      ``O`` と同じです。

   ``N`` (オブジェクト) [PyObject \*]
      ``O`` と同じです。ただし、オブジェクトの参照カウントをインクリメントしません。オブジェクトが引数リスト内のオブジェクト
      コンストラクタ呼び出しによって生成されている場合に便利です。

   ``O&`` (オブジェクト) [*converter*, *anything*]
      *anything* を *converter* 関数を介して Python オブジェクトに変換します。この関数は *anything*
      (:ctype:`void \*` と互換の型でなければなりません) を引数にして呼び出され、"新たな" オブジェクトを返すか、失敗した場合には
      *NULL* を返すようにしなければなりません。

   ``(items)`` (タプル型) [*matching-items*]
      C の値からなる配列を、同じ要素数を持つ Python のタプルに変換します。

   ``[items]`` (リスト型) [*matching-items*]
      C の値からなる配列を、同じ要素数を持つ Python のリストに変換します。

   ``{items}`` (辞書型) [*matching-items*]
      C の値からなる配列を Python の辞書に変換します。一連のペアからなる C の値が、それぞれキーおよび値となって辞書に追加されます。

   書式化文字列に関するエラーが生じると、 :exc:`SystemError` 例外をセットして *NULL* を返します。

