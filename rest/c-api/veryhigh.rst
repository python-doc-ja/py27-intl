.. highlightlang:: c


.. _veryhigh:

********
超高レベルレイヤ
********

この章の関数を使うとファイルまたはバッファにあるPythonソースコードを 実行できますが、より詳細なやり取りをインタプリタとすることはできないでしょう。

これらの関数のいくつかは引数として文法の開始記号を受け取ります。
使用できる開始記号は:const:`Py_eval_input`と:const:`Py_file_input`、
:const:`Py_single_input`です。開始期号の説明はこれらを引数として取る 関数の後にあります。

これらの関数のいくつかが:ctype:`FILE\*`引数をとることにも注意してください。
注意深く扱う必要がある特別な問題には、異なるCライブラリの:ctype:`FILE`構造体は 異なっていて互換性がない可能性があるということが関係しています。
実際に(少なくとも)Windowsでは、動的リンクされる拡張が異なるライブラリを
使うことが可能であり、したがって、:ctype:`FILE\*`引数がPythonランタイムが
使っているライブラリと同じライブラリによって作成されたことが確かならば、 単にこれらの関数へ渡すだけということに注意すべきです。


.. cfunction:: int Py_Main(int argc, char **argv)

   標準インタプリタのためのメインプログラム。Pythonを組み込む プログラムのためにこれを利用できるようにしています。
   *argc*と*argv*引数をCプログラムの:cfunc:`main`関数へ 渡されるものとまったく同じに作成すべきです。
   引数リストが変更される可能性があるという点に注意することは重要です。 (しかし、引数リストが指している文字列の内容は変更されません)。
   戻り値は:func:`sys.exit`関数へ渡される整数でしょう。 例外が原因でインタプリタが終了した場合は``1``、あるいは、
   引数リストが有効なPythonコマンドラインになっていない場合は``2``です。


.. cfunction:: int PyRun_AnyFile(FILE *fp, const char *filename)

   下記の :cfunc:`PyRun_AnyFileExFlags` の*closeit* を``0`` に、*flags* を
   *NULL*にして単純化したインタフェースです。


.. cfunction:: int PyRun_AnyFileFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   下記の :cfunc:`PyRun_AnyFileExFlags` の*closeit* を``0`` にして単純化したインタフェースです。


.. cfunction:: int PyRun_AnyFileEx(FILE *fp, const char *filename, int closeit)

   下記の :cfunc:`PyRun_AnyFileExFlags` の *flags* を *NULL*にして単純化したインタフェースです。


.. cfunction:: int PyRun_AnyFileExFlags(FILE *fp, const char *filename, int closeit, PyCompilerFlags *flags)

   *fp*が対話的デバイス(コンソールや端末入力あるいはUnix仮想端末)と 関連づけられたファイルを参照しているならば、
   :cfunc:`PyRun_InteractiveLoop`の値を返します。それ以外の場合は、
   :cfunc:`PyRun_SimpleFile`の結果を返します。*filename*が
   *NULL*ならば、この関数はファイル名として``"???"``を使います。


.. cfunction:: int PyRun_SimpleString(const char *command)

   下記の :cfunc:`PyRun_SimpleStringFlags` の *PyCompilerFlags\** を
   *NULL*にして単純化したインタフェースです。


.. cfunction:: int PyRun_SimpleStringFlags(const char *command, PyCompilerFlags *flags)

   :mod:`__main__`モジュールの中で*flags* に従って*command* に含まれる Python ソースコードを
   実行します。:mod:`__main__`がまだ存在しない場合は作成されます。 正常終了の場合は``0``を返し、また例外が発生した場合は``-1``を
   返します。エラーがあっても、例外情報を得る方法はありません。


.. cfunction:: int PyRun_SimpleFile(FILE *fp, const char *filename)

   下記の :cfunc:`PyRun_SimpleStringFileExFlags` の *closeit* を ``0`` に、*flags* を
   *NULL*にして単純化したイ ンタフェースです。


.. cfunction:: int PyRun_SimpleFileFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   下記の :cfunc:`PyRun_SimpleStringFileExFlags` の *closeit* を ``0``
   にして単純化したインタフェースです。


.. cfunction:: int PyRun_SimpleFileEx(FILE *fp, const char *filename, int closeit)

   下記の :cfunc:`PyRun_SimpleStringFileExFlags` の *flags* を *NULL*にして単純化したイ ンタフェースです。


.. cfunction:: int PyRun_SimpleFileExFlags(FILE *fp, const char *filename, int closeit, PyCompilerFlags *flags)

   Similar to :cfunc:`PyRun_SimpleStringFlags`, but the Python source
   :cfunc:`PyRun_SimpleString`と似ていますが、Pythonソースコードを メモリ内の文字列ではなく*fp*から読み込みます。
   *filename*はそのファイルの名前でなければなりません。 *closeit* が真ならば、PyRun_SimpleFileExFlags は処理を戻す前に
   ファイルを閉じます。


.. cfunction:: int PyRun_InteractiveOne(FILE *fp, const char *filename)

   下記の :cfunc:`PyRun_InteractiveOneFlags` の*flags* を *NULL* にして単純化したインタフェースです。


.. cfunction:: int PyRun_InteractiveOneFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   対話的デバイスに関連付けられたファイルから文を一つ読み込み、 *flags* に従って実行します。
   *filename*が*NULL*ならば、``"???"``が代わりに使われます。
   ``sys.ps1``と``sys.ps2``を使って、ユーザにプロンプトを提示します。 入力が正常に実行されたときは``0``を返します。例外が発生した場合は
   ``-1``を返します。パースエラーの場合はPythonの一部として配布されている
   :file:`errcode.h`インクルードファイルにあるエラーコードを返します。
   (:file:`Python.h`は:file:`errcode.h`をインクルードしません。したがって、
   必要ならば特別にインクルードしなければならないことに注意してください。)


.. cfunction:: int PyRun_InteractiveLoop(FILE *fp, const char *filename)

   下記の :cfunc:`PyRun_InteractiveLoopFlags` の*flags* を ``0`` にして単純化したインタフェースです。


.. cfunction:: int PyRun_InteractiveLoopFlags(FILE *fp,  const char *filename, PyCompilerFlags *flags)

   対話的デバイスに関連付けられたファイルからEOF に達するまで複数の文を
   読み込み実行します。*filename*が*NULL*ならば、``"???"``が代わりに
   使われます。``sys.ps1``と``sys.ps2``を使って、ユーザにプロンプトを 提示します。EOFに達すると``0``を返します。


.. cfunction:: struct _node* PyParser_SimpleParseString(const char *str, int start)

   下記の :cfunc:`PyRun_SimpleParseStringFlagsFilename` の *filename* を *NULL*
   に、*flags* を ``0`` にして単純化したイ ンタフェースです。


.. cfunction:: struct _node* PyParser_SimpleParseStringFlags( const char *str, int start, int flags)

   下記の :cfunc:`PyRun_SimpleParseStringFlagsFilename` の *filename* を *NULL*
   にして単純化したインタフェースです。


.. cfunction:: struct _node* PyParser_SimpleParseStringFlagsFilename( const char *str, const char *filename, int start, int flags)

   開始トークン*start*を使って*str*に含まれる Python ソースコード を*flags* 引数に従ってパースします。効率的に評価可能なコードオブジェ
   クトを作成するためにその結果を使うことができます。コード断片を何度も評 価しなければならない場合に役に立ちます。


.. cfunction:: struct _node* PyParser_SimpleParseFile(FILE *fp, const char *filename, int start)

   下記の :cfunc:`PyRun_SimpleParseFileFlags` の*flags* を ``0`` にして単純化したインタフェースです。


.. cfunction:: struct _node* PyParser_SimpleParseFileFlags(FILE *fp, const char *filename, int start, int flags)

   :cfunc:`PyParser_SimpleParseStringFlagsFilename`に似ていますが、
   Pythonソースコードをメモリ内の文字列ではなく*fp*から読み込みます。 *filename*はそのファイルの名前でなけれななりません。


.. cfunction:: PyObject* PyRun_String(const char *str, int start, PyObject *globals, PyObject *locals)

   下記の :cfunc:`PyRun_StringFlags` の*flags* を*NULL*にして単 純化したインタフェースです。


.. cfunction:: PyObject* PyRun_StringFlags(const char *str, int start, PyObject *globals, PyObject *locals, PyCompilerFlags *flags)

   辞書*globals*と*locals*で指定されるコンテキストにおいて、 *str*に含まれるPythonソースコードをコンパイラフラグ *flags* の
   もとで実行します。 パラメータ*start*はソースコードをパースするために使われるべき 開始トークンを指定します。

   コードを実行した結果をPythonオブジェクトとして返します。または、 例外が発生したならば*NULL* を返します。


.. cfunction:: PyObject* PyRun_File(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals)

   下記の :cfunc:`PyRun_FileExFlags` の*closeit* を``0`` にし、 *flags*
   を*NULL*にして単純化したインタフェースです。


.. cfunction:: PyObject* PyRun_FileEx(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals, int closeit)

   下記の :cfunc:`PyRun_FileExFlags` の *flags* を*NULL*にして単純化したインタフェースです。


.. cfunction:: PyObject* PyRun_FileFlags(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals, PyCompilerFlags *flags)

   下記の :cfunc:`PyRun_FileExFlags` の*closeit* を``0`` にし て単純化したインタフェースです。


.. cfunction:: PyObject* PyRun_FileExFlags(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals, int closeit, PyCompilerFlags *flags)

   :cfunc:`PyRun_String`と似ていますが、Pythonソースコードを メモリ内の文字列ではなく*fp*から読み込みます。 *closeit*
   を真にすると、:cfunc:`PyRun_FileExFlags` から処理 を戻す前にファイルを閉じます。
   *filename*はそのファイルの名前でなければなりません。


.. cfunction:: PyObject* Py_CompileString(const char *str, const char *filename, int start)

   下記の:cfunc:`Py_CompileStringFlags` の *flags* を *NULL* に して単純化したインタフェースです。


.. cfunction:: PyObject* Py_CompileStringFlags(const char *str, const char *filename, int start, PyCompilerFlags *flags)

   *str*内のPythonソースコードをパースしてコンパイルし、 作られたコードオブジェクトを返します。開始トークンは
   *start*によって与えられます。これはコンパイル可能なコードを 制限するために使うことができ、:const:`Py_eval_input`、
   :const:`Py_file_input`もしくは:const:`Py_single_input`であるべきです。
   *filename*で指定されるファイル名はコードオブジェクトを構築するために使われ、
   トレースバックあるいは:exc:`SyntaxError`例外メッセージに出てくる可能性があります。
   コードがパースできなかったりコンパイルできなかったりした場合に、 これは*NULL* を返します。


.. cvar:: int Py_eval_input

   .. index:: single: Py_CompileString()

   単独の式に対するPython文法の開始記号で、 :cfunc:`Py_CompileString`と一緒に使います。


.. cvar:: int Py_file_input

   .. index:: single: Py_CompileString()

   ファイルあるいは他のソースから読み込まれた文の並びに対するPython文法の 開始記号で、:cfunc:`Py_CompileString`と
   一緒に使います。これは任意の長さのPythonソースコードをコンパイルするときに 使う記号です。


.. cvar:: int Py_single_input

   .. index:: single: Py_CompileString()

   単一の文に対するPython文法の開始記号で、 :cfunc:`Py_CompileString`と一緒に使います。
   これは対話式のインタプリタループのための記号です。


.. ctype:: struct PyCompilerFlags

   コンパイラフラグを収めておくための構造体です。コードをコンパイルする だけの場合、この構造体が ``int flags`` として渡されます。コードを実
   行する場合には``PyCompilerFlags *flags`` として渡されます。この場合、 ``from __future__  import`` は
   *flags* の内容を変更できます。

   ``PyCompilerFlags *flags`` が*NULL*の場合、 :attr:`cf_flags` は ``0`` として扱われ、``from
   __future__ import`` による変更は 無視されます。 ::

      struct PyCompilerFlags {
          int cf_flags;
      }


.. cvar:: int CO_FUTURE_DIVISION

   このビットを *flags* にセットすると、除算演算子 ``/`` は :pep:`238` による 「真の除算 (true division)」
   として扱われます。

