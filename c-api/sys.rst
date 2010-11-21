.. highlightlang:: c

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

