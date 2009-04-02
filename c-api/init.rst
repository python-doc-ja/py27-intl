.. highlightlang:: c


.. _initialization:

**********************************************************
初期化 (initialization)、終了処理 (finalization)、スレッド
**********************************************************


.. cfunction:: void Py_Initialize()

   .. index::
      single: Py_SetProgramName()
      single: PyEval_InitThreads()
      single: PyEval_ReleaseLock()
      single: PyEval_AcquireLock()
      single: modules (in module sys)
      single: path (in module sys)
      module: __builtin__
      module: __main__
      module: sys
      triple: module; search; path
      single: PySys_SetArgv()
      single: Py_Finalize()

   Python インタプリタを初期化します。Python の埋め込みを行う アプリケーションでは、他のあらゆる Python/C API を使用するよりも
   前にこの関数を呼び出さねばなりません; ただし、 :cfunc:`Py_SetProgramName`,
   :cfunc:`PyEval_InitThreads`, :cfunc:`PyEval_ReleaseLock`, および
   :cfunc:`PyEval_AcquireLock` は例外です。 この関数はロード済みモジュールのテーブル (``sys.modules``) を初期化
   し、基盤となるモジュール群、 :mod:`__builtin__`, :mod:`__main__` および :mod:`sys` を生成します。
   また、モジュール検索パス   (``sys.path``) も初期化します。 ``sys.argv`` の設定は行いません; 設定するには、
   :cfunc:`PySys_SetArgv` を使ってください。 この関数を (:cfunc:`Py_Finalize` を 呼ばずに)
   再度呼び出しても何も行いません。 戻り値はありません; 初期化が失敗すれば、それは致命的なエラーです。


.. cfunction:: void Py_InitializeEx(int initsigs)

   *initsigs* に1を指定すれば:cfunc:`Py_Initialize` と同じ処理を実
   行しますが、Python埋め込みアプリケーションでは *initsigs* を0として
   初期化時にシグナルハンドラの登録をスキップすることができます。

   .. versionadded:: 2.4


.. cfunction:: int Py_IsInitialized()

   Python インタプリタがすでに初期化済みの場合に真 (非ゼロ) を返し、 そうでない場合には偽 (ゼロ)
   を返します。:cfunc:`Py_Finalize` を呼び出すと、次に:cfunc:`Py_Initialize` を呼び出すまで この関数は偽を返します。


.. cfunction:: void Py_Finalize()

   :cfunc:`Py_Initialize` とそれ以後の Python/C API 関数で行った 全ての初期化処理を取り消し、最後の
   :cfunc:`Py_Initialize`  呼び出し以後に Python インタプリタが生成した全てのサブインタプリタ  (sub-interpreter,
   下記の :cfunc:`Py_NewInterpreter` を参照) を 消去します。 理想的な状況では、この関数によって Python
   インタプリタが確保した メモリは全て解放されます。 この関数を (:cfunc:`Py_Initialize` を呼ばずに) 再度呼び出しても 何も行いません。
   戻り値はありません; 終了処理中のエラーは無視されます。

   この関数が提供されている理由はいくつかあります。Python の埋め込みを 行っているアプリケーションでは、アプリケーションを再起動することなく Python
   を再起動したいことがあります。また、動的ロード可能イブラリ (あるいは DLL) から Python インタプリタをロードするアプリケーション では、DLL
   をアンロードする前に Python が確保したメモリを解放したい と考えるかもしれません。アプリケーション内で起きているメモリリークを 追跡する際に、開発者は
   Python が確保したメモリをアプリケーションの 終了前に解放させたいと思う場合もあります。

   **バグおよび注意事項:** モジュールやモジュール内のオブジェクト はランダムな順番で削除されます; このため、他のオブジェクト
   (関数オブジェクトも含みます) やモジュールに依存するデストラクタ  (:meth:`__del__` メソッド) が失敗してしまうことがあります。
   動的にロードされるようになっている拡張モジュールが Python によって ロードされていた場合、アンロードされません。Python が確保した
   メモリがわずかながら解放されないかもしれません (メモリリークを 発見したら、どうか報告してください)。オブジェクト間の循環参照に
   捕捉されているメモリは解放されないことがあります。拡張モジュール が確保したメモリは解放されないことがあります。拡張モジュールに よっては、初期化ルーチンを 2
   度以上呼び出すと正しく動作 しないことがあります; こうした状況は、:cfunc:`Py_Initialize`  や:cfunc:`Py_Finalize`
   を 2 度以上呼び出すと起こり得ます。


.. cfunction:: PyThreadState* Py_NewInterpreter()

   .. index::
      module: __builtin__
      module: __main__
      module: sys
      single: stdout (in module sys)
      single: stderr (in module sys)
      single: stdin (in module sys)

   新しいサブインタプリタ (sub-interpreter) を生成します。 サブインタプリタとは、(ほぼ完全に) 個別に分割された Python
   コードの実行環境です。特に、新しいサブインタプリタは、 import されるモジュール全てについて個別のバージョンを持ち、 これには基盤となるモジュール
   :mod:`__builtin__`, :mod:`__main__` および :mod:`sys` も含まれます。 ロード済みのモジュールからなるテーブル
   (``sys.modules``)  およびモジュール検索パス (``sys.path``) もサブインタプリタ
   毎に別個のものになります。新たなサブインタプリタ環境には ``sys.argv`` 変数がありません。また、サブインタプリタは 新たな標準 I/O ストリーム
   ``sys.stdin``, ``sys.stdout`` および ``sys.stderr`` を持ちます (とはいえ、これらのストリームは 根底にある C
   ライブラリの同じ :ctype:`FILE` 構造体を参照しています)。

   戻り値は、新たなサブインタプリタが生成したスレッド状態 (thread state) オブジェクトのうち、最初のものを指しています。
   このスレッド状態が現在のスレッド状態 (current thread state) になります。 実際のスレッドが生成されるわけではないので注意してください;
   下記のスレッド状態に関する議論を参照してください。 新たなインタプリタの生成に失敗すると、*NULL* を返します;
   例外状態はセットされませんが、これは例外状態が現在のスレッド状態に 保存されることになっていて、現在のスレッド状態なるものが 存在しないことがあるからです。
   (他の Python/C API 関数のように、 この関数を呼び出す前にはグローバルインタプリタロック (global interpreter lock)
   が保持されていなければならず、関数が 処理を戻した際にも保持されたままになります; しかし、 他の Python/C API
   関数とは違い、関数から戻ったときの現在のスレッド状態 が関数に入るときと同じとは限らないので注意してください)。

   .. index::
      single: Py_Finalize()
      single: Py_Initialize()

   拡張モジュールは以下のような形で (サブ) インタプリタ間で共有 されます: ある特定の拡張モジュールを最初に import すると、
   モジュールを通常通りに初期化し、そのモジュールの辞書の (浅い) コピーをしまい込んでおきます。他の (サブ) インタプリタが 同じ拡張モジュールを
   import すると、新たなモジュールを初期化し、 先ほどのコピーの内容で辞書の値を埋めます; 拡張モジュールの ``init``
   関数は呼び出されません。この挙動は、 :cfunc:`Py_Finalize` および :cfunc:`Py_Initialize` を呼び出して
   インタプリタを完全に再初期化した後に拡張モジュールを import した 際の挙動とは異なるので注意してください; 再初期化後に import を
   行うと、拡張モジュールの ``initmodule`` は再度 *呼び出され* ます。

   .. index:: single: close() (in module os)

   **バグと注意事項:** サブインタプリタ (とメインインタプリタ) は同じプロセスの一部分なので、インタプリタ間の絶縁性は完璧では ありません ---
   例えば、 :func:`os.close` のような低レベルのファイル操作を使うと、 (偶然なり故意なりに) 互いのインタプリタ下にある開かれたファイルに
   影響を及ぼせてしまいます。 拡張モジュールを (サブ) インタプリタ間で共有する方法のために、 拡張モジュールによっては正しく動作しないかもしれません;
   拡張モジュールが (静的な) グローバル変数を利用している 場合や、拡張モジュールが初期化後に自身のモジュール辞書を操作 する場合には特にそうです。
   一つのサブインタプリタで生成されたオブジェクトは他のサブインタプリタ の名前空間への挿入が可能です; ユーザ定義関数、メソッド、インスタンス
   およびクラスをサブインタプリタをサブインタプリタ間で共有しないように 十分注意してください。というのは、これらの共有オブジェクトが 実行した import
   文は間違った (サブ) インタプリタのロード済み モジュール辞書に影響を及ぼす場合があるからです (XXX この問題は
   修正が難しいバグで、将来のリリースで解決される予定です)

   この機能は PyObjC や ctypes のような、:cfunc:`PyGILState_\*` API を利用する
   タイプの拡張モジュールと相性が悪いことにも注意してください。 (これは、:cfunc:`PyGILState_\*` 関数の動作特有の問題です)
   シンプルなことなら上手くいくかもしれませんが、いつ混乱させる動作をするかわかりません。


.. cfunction:: void Py_EndInterpreter(PyThreadState *tstate)

   .. index:: single: Py_Finalize()

   指定されたスレッド状態 *tstate* で表現される (サブ) インタプリタを 抹消します。*tstate* は現在のスレッド状態でなければなりません。
   下記のスレッド状態に関する議論を参照してください。関数呼び出しが 戻ったとき、現在のスレッド状態は *NULL*になっています。
   このインタプリタに関連付けられた全てのスレッド状態は抹消されます。 (この関数を呼び出す前にはグローバルインタプリタロックを保持して
   おかねばならず、ロックは関数が戻ったときも保持されています。) :cfunc:`Py_Finalize` は、その時点で
   明示的に抹消されていない全てのサブインタプリタを抹消します。


.. cfunction:: void Py_SetProgramName(char *name)

   .. index::
      single: Py_Initialize()
      single: main()
      single: Py_GetPath()

   この関数を呼び出すなら、最初に :cfunc:`Py_Initialize` を呼び出す よりも前に呼び出さねばなりません。この関数はインタプリタに
   プログラムの:cfunc:`main` 関数に 指定した``argv[0]`` 引数の値を教えます。 この引数値は、:cfunc:`Py_GetPath` や、
   以下に示すその他の関数が、インタプリタの実行可能形式から Python ランタイムライブラリへの相対パスを取得するために使われます。
   デフォルトの値は``'python'`` です。引数はゼロ終端された キャラクタ文字列で、静的な記憶領域に入っていなければならず、
   その内容はプログラムの実行中に変更してはなりません。 Python インタプリタ内のコードで、この記憶領域の内容を変更するものは 一切ありません。


.. cfunction:: char* Py_GetProgramName()

   .. index:: single: Py_SetProgramName()

   :cfunc:`Py_SetProgramName` で 設定されたプログラム名か、デフォルトのプログラム名を返します。
   関数が返す文字列ポインタは静的な記憶領域を返します; 関数の 呼び出し側はこの値を変更できません。


.. cfunction:: char* Py_GetPrefix()

   プラットフォーム非依存のファイル群がインストールされている場所である *prefix* を返します。この値は
   :cfunc:`Py_SetProgramName` でセットされたプログラム名や いくつかの環境変数をもとに、数々の複雑な規則から導出されます;
   例えば、プログラム名が``'/usr/local/bin/python'`` の場合、prefix は ``'/usr/local'`` になります。
   関数が返す文字列ポインタは静的な記憶領域を返します; 関数の 呼び出し側はこの値を変更できません。 この値はトップレベルの :file:`Makefile`
   に指定されている変数 :makevar:`prefix` や、ビルド値に :program:`configure` スクリプト に指定した
   :option:`--prefix` 引数に対応しています。 この値は Python コードからは ``sys.prefix`` として利用できます。 Unix
   でも有用です。次に説明する関数も参照してください。


.. cfunction:: char* Py_GetExecPrefix()

   プラットフォーム*依存* のファイルがインストールされている場所 である*exec-prefix* を返します。
   この値は:cfunc:`Py_SetProgramName` でセットされたプログラム名や いくつかの環境変数をもとに、数々の複雑な規則から導出されます;
   例えば、プログラム名が``'/usr/local/bin/python'`` の場合、exec-prefix は ``'/usr/local'`` になります。
   関数が返す文字列ポインタは静的な記憶領域を返します; 関数の 呼び出し側はこの値を変更できません。 この値はトップレベルの :file:`Makefile`
   に指定されている変数 :makevar:`exec_prefix` や、ビルド値に :program:`configure` スクリプト に指定した
   :option:`--exec-prefix` 引数に対応しています。 この値は Python コードからは ``sys.exec_prefix``
   として利用できます。 Unixのみで有用です。

   背景: プラットフォーム依存のファイル (実行形式や共有ライブラリ) が、 別個のディレクトリツリー内にインストールされている場合、 exec-prefix は
   prefix と異なります。典型的なインストール形態では、 プラットフォーム非依存のファイルが:file:`/usr/local` に収められる一方、
   プラットフォーム依存のファイルは:file:`/usr/local/plat` サブツリーに 収められます。

   概して、プラットフォームとは、ハードウェアとソフトウェアファミリの 組み合わせを指します。例えば、 Solaris 2.x を動作させている Sparc
   マシンは全て同じプラットフォームであるとみなしますが、Solaris 2.x を動作させている Intel マシンは違うプラットフォームになりますし、 同じ
   Intel マシンでも Linux を動作させているならまた別の プラットフォームです。一般的には、同じオペレーティングシステムでも、
   メジャーリビジョンの違うものは異なるプラットフォームです。 非 Unix のオペレーティングシステムの場合は話はまた別です; 非 Unix
   のシステムでは、インストール方法はとても異なっていて、 prefix や exec-prefix には意味がなく、空文字列が設定されている
   ことがあります。コンパイル済みの Python バイトコードは プラットフォームに依存しないので注意してください (ただし、 どのバージョンの Python
   でコンパイルされたかには依存します!)。

   システム管理者は、:program:`mount` や :program:`automount` プログラムを
   使って、各プラットフォーム用の:file:`/usr/local/plat` を異なった ファイルシステムに置き、プラットフォーム間で
   :file:`/usr/local` を 共有するための設定方法を知っているはずです。


.. cfunction:: char* Py_GetProgramFullPath()

   .. index::
      single: Py_SetProgramName()
      single: executable (in module sys)

   Python 実行可能形式の完全なプログラム名を返します; この値は デフォルトのモジュール検索パスを
   (前述の:cfunc:`Py_SetProgramName`  で設定された) プログラム名から導出する際に 副作用的に計算されます。
   関数が返す文字列ポインタは静的な記憶領域を返します; 関数の 呼び出し側はこの値を変更できません。 この値は Python コードからは
   ``sys.executable`` として利用できます。 Unixのみで有用です。


.. cfunction:: char* Py_GetPath()

   .. index::
      triple: module; search; path
      single: path (in module sys)

   デフォルトモジュール検索パスを返します; パスは (上の :cfunc:`Py_SetProgramName` で設定された) プログラム名と、
   いくつかの環境変数から計算されます。戻り値となる文字列は、 プラットフォーム依存のパスデリミタ文字で分割された一連の ディレクトリ名からなります。デリミタ文字は
   Unixと Mac OS X では``':'``、 Windows では``';'`` です。 関数が返す文字列ポインタは静的な記憶領域を返します;
   関数の呼び出し側はこの値を変更できません。 この値は Python コードからはリスト ``sys.path`` として
   利用できます。このリストは、値を修正して将来モジュールをロードする際に 使う検索パスを変更できます。

   .. % XXX should give the exact rules


.. cfunction:: const char* Py_GetVersion()

   Python インタプリタのバージョンを返します。バージョンは、 ::

      "1.5 (#67, Dec 31 1997, 22:34:28) [GCC 2.7.2.2]"

   ような形式の文字列です。

   .. index:: single: version (in module sys)

   第一ワード (最初のスペース文字まで) は、現在の Python のバージョン です; 最初の三文字は、メジャーバージョンとマイナーバージョン、そして
   それを分割しているピリオドです。関数が返す文字列ポインタは静的な 記憶領域を返します; 関数の呼び出し側はこの値を変更できません。 この値は Python
   コードからは``sys.version``として利用できます。


.. cfunction:: const char* Py_GetBuildNumber()

   このPython実行ファイルが、Subversionのどのリビジョンからビルドされたかを表す 文字列を返します。
   リビジョンを混ぜて作られたPythonでは末尾に 'M' をつけるので、 この番号は文字列になっています。

   .. versionadded:: 2.5


.. cfunction:: const char* Py_GetPlatform()

   .. index:: single: platform (in module sys)

   現在のプラットフォームのプラットフォーム識別文字列を返します。 Unixでは、オペレーティングシステムの "公式の" 名前を小文字に
   変換し、後ろにメジャーリビジョン番号を付けた構成になっています; 例えば Solaris 2.x は、SunOS 5.x, としても知られていますが、
   ``'sunos5'`` になります。Mac OS X では ``'darwin'`` です。 Windows では``'win'`` です。
   関数が返す文字列ポインタは静的な 記憶領域を返します; 関数の呼び出し側はこの値を変更できません。 この値は Python
   コードからは``sys.platform``として利用できます。


.. cfunction:: const char* Py_GetCopyright()

   .. index:: single: copyright (in module sys)

   現在の Python バージョンに対する公式の著作権表示文字列、例えば ``'Copyright 1991-1995 Stichting
   Mathematisch Centrum, Amsterdam'`` を返します。 関数が返す文字列ポインタは静的な 記憶領域を返します;
   関数の呼び出し側はこの値を変更できません。 この値は Python コードからは``sys.copyright``として利用できます。


.. cfunction:: const char* Py_GetCompiler()

   現在使っているバージョンの Python をビルドする際に用いたコンパイラ を示す文字列を、各括弧で囲った文字列を返します。例えば::

      "[GCC 2.7.2.2]"

   になります。

   .. index:: single: version (in module sys)

   関数が返す文字列ポインタは静的な 記憶領域を返します; 関数の呼び出し側はこの値を変更できません。 この値は Python
   コードからは``sys.version`` の一部として 取り出せます。


.. cfunction:: const char* Py_GetBuildInfo()

   現在使っている Python インタプリタインスタンスの、シーケンス番号と ビルド日時に関する情報を返します。例えば ::

      "#67, Aug  1 1997, 22:34:28"

   になります。

   .. index:: single: version (in module sys)

   関数が返す文字列ポインタは静的な 記憶領域を返します; 関数の呼び出し側はこの値を変更できません。 この値は Python
   コードからは``sys.version`` の一部として 取り出せます。


.. cfunction:: void PySys_SetArgv(int argc, char **argv)

   .. index::
      single: main()
      single: Py_FatalError()
      single: argv (in module sys)

   *argc* および *argv* に基づいて ``sys.argv`` を設定 します。このパラメタはプログラムの :cfunc:`main`
   に渡したパラメタに似ていますが、最初の要素が Python インタプリタ の宿主となっている実行形式の名前ではなく、実行されるスクリプト名を
   参照しなければならない点が違います。実行するスクリプトがない場合、 *argv* の最初の要素は空文字列にしてもかまいません。 この関数が
   ``sys.argv`` の初期化に失敗した場合、致命的 エラー条件を:cfunc:`Py_FatalError` でシグナルします。

   .. % XXX impl. doesn't seem consistent in allowing 0/NULL for the params;
   .. % check w/ Guido.

.. % XXX Other PySys thingies (doesn't really belong in this chapter)


.. _threads:

スレッド状態 (thread state) とグローバルインタプリタロック (global interpreter lock)
====================================================================================

.. index::
   single: global interpreter lock
   single: interpreter lock
   single: lock, interpreter

Python インタプリタは完全にスレッド安全 (thread safe) ではありません。 マルチスレッドの Python
プログラムをサポートするために、グローバルな ロックが存在していて、現在のスレッドが Python オブジェクトに安全に
アクセスする前に必ずロックを獲得しなければならなくなっています。 ロック機構がなければ、単純な操作でさえ、マルチスレッドプログラムの
実行に問題を引き起こす可能性があります: たとえば、二つのスレッドが 同じオブジェクトの参照カウントを同時にインクリメントすると、
結果的に参照カウントは二回でなく一回だけしかインクリメントされない かもしれません。

.. index:: single: setcheckinterval() (in module sys)

このため、グローバルインタプリタロックを獲得したスレッドだけが Python オブジェクトを操作したり、 Python/C API 関数を呼び出したり
できるというルールがあります。マルチスレッドの Python プログラムを サポートするため、インタプリタは定期的に --- デフォルトの設定では バイトコード
100 命令ごとに (この値は :func:`sys.setcheckinterval` で 変更できます) --- ロックを解放したり獲得したりします。
このロックはブロックが起こりうる I/O 操作の付近でも解放・獲得 され、I/O を要求するスレッドが I/O 操作の完了を待つ間、他の
スレッドが動作できるようにしています。

.. index::
   single: PyThreadState
   single: PyThreadState

Python インタプリタはスレッドごとに何らかの予約情報を持っておかねば なりません --- このため、Python は
:ctype:`PyThreadState` と呼ばれるデータ構造 を用います。 とはいえ、グローバル変数はまだ一つだけ残っています: それは現在の
:ctype:`PyThreadState` 構造体を指すポインタです。 ほとんどのスレッドパッケージが "スレッドごとのグローバルデータ"
を保存する手段を持っている一方で、Python の内部的なプラットフォーム 非依存のスレッド抽象層はこれをサポートしていません。従って、
現在のスレッド状態を明示的に操作するようにしなければなりません。

ほとんどのケースで、このような操作は十分簡単にできます。 グローバルインタプリタロックを操作数ほとんどのコードは、以下のような 単純な構造を持ちます::

   スレッド状態をローカル変数に保存する。
   インタプリタロックを解放する。
   ...ブロックが起きるような何らかの I/O 操作...
   インタプリタロックを獲得する。
   ローカル変数からスレッド状態を回復する。

このやりかたは非常に一般的なので、作業を単純にするために二つの マクロが用意されています::

   Py_BEGIN_ALLOW_THREADS
   ...ブロックが起きるような何らかの I/O 操作...
   Py_END_ALLOW_THREADS

.. index::
   single: Py_BEGIN_ALLOW_THREADS
   single: Py_END_ALLOW_THREADS

:cmacro:`Py_BEGIN_ALLOW_THREADS` マクロは新たなブロック文を開始し、隠しローカル変数を宣言します;
:cmacro:`Py_END_ALLOW_THREADS` はブロック文を終了します。これらの二つのマクロを使うもうひとつの 利点は、Python
をスレッドサポートなしでコンパイルしたとき、 マクロの内容、すなわちスレッド状態の退避とロック操作が空になると いう点です。

スレッドサポートが有効になっている場合、上記のブロックは 以下のようなコードに展開されます::

   PyThreadState *_save;

   _save = PyEval_SaveThread();
   ...ブロックが起きるような何らかの I/O 操作...
   PyEval_RestoreThread(_save);

より低水準のプリミティブを使うと、以下のようにしてほぼ同じ効果を 得られます::

   PyThreadState *_save;

   _save = PyThreadState_Swap(NULL);
   PyEval_ReleaseLock();
   ...ブロックが起きるような何らかの I/O 操作...
   PyEval_AcquireLock();
   PyThreadState_Swap(_save);

.. index::
   single: PyEval_RestoreThread()
   single: errno
   single: PyEval_SaveThread()
   single: PyEval_ReleaseLock()
   single: PyEval_AcquireLock()

上の二つには微妙な違いがあります; とりわけ、 :cfunc:`PyEval_RestoreThread`  はグローバル変数 :cdata:`errno`
の値を保存しておいて 元に戻す点が異なります。というのは、ロック操作が :cdata:`errno` に
何もしないという保証がないからです。また、スレッドサポートが無効化 されている場合、 :cfunc:`PyEval_SaveThread` および
:cfunc:`PyEval_RestoreThread` はロックを操作しません; この場合、 :cfunc:`PyEval_ReleaseLock` および
:cfunc:`PyEval_AcquireLock` は 利用できません。この仕様は、スレッドサポートを無効化してコンパイル
されているインタプリタが、スレッドサポートが有効化された状態で コンパイルされている動的ロード拡張モジュールをロードできる ようにするためのものです。

グローバルインタプリタロックは、現在のスレッド状態を指すポインタを 保護するために使われます。ロックを解放してスレッド状態を退避する際、
ロックを解放する前に現在のスレッド状態ポインタを取得しておかなければ なりません (他のスレッドがすぐさまロックを獲得して、自らの
スレッド状態をグローバル変数に保存してしまうかもしれないからです)。 逆に、ロックを獲得してスレッド状態を復帰する際には、
グローバル変数にスレッド状態ポインタを保存する前にロックを獲得して おかなければなりません。

なぜここまで詳しく説明しようとするかおわかりでしょうか? それは、 C でスレッドを生成した場合、そのスレッドにはグローバルインタプリタ
ロックがなく、スレッド状態データ構造体もないからです。このような スレッドが Python/C API を利用するには、まずスレッド状態データ構造体を
生成し、次にロックを獲得し、そしてスレッド状態ポインタを保存すると いったように、自分自身をブートストラップして生成しなければ
なりません。スレッドが作業を終えたら、スレッド状態ポインタを リセットして、ロックを解放し、最後にスレッド状態データ構造体を メモリ解放しなければなりません。

スレッドデータ構造体を生成する際には、インタプリタ状態データ構造体を 指定する必要があります。インタプリタ状態データ構造体は、
インタプリタ内の全てのスレッド間で共有されているグローバルなデータ、 例えばモジュール管理データ (codesys.modules) を保持しています。
必要に応じて、新たなインタプリタ状態データ構造体を作成するなり、 Python メインスレッドが使っているインタプリタ状態データ構造体 を共有するなりできます
(後者のデータにアクセスするためには、 スレッド状態データ構造体を獲得して、その :attr:`interp` メンバ にアクセスしなければなりません;
この処理は、Python が作成した スレッドから行うか、Python を初期化した後で主スレッドから行わねば なりません)。

インタプリタオブジェクトにアクセスできるという仮定の下では、C の スレッドから Python を呼び出す際の典型的な常套句は以下のようになります。

バージョン 2.3 からは、上記の事を全て自動で行われて、 スレッドは :cfunc:`PyGILState_\*` の恩恵に預かることができます。 C
のスレッドから Python を呼び出す典型的な方法は以下のとおりです。 ::

   PyGILState_STATE gstate;
   gstate = PyGILState_Ensure();

   /* Perform Python actions here.  */
   result = CallSomeFunction();
   /* evaluate result */

   /* Release the thread. No Python API allowed beyond this point. */
   PyGILState_Release(gstate);

:cfunc:`PyGILState_\*`関数は、(:cfunc:`Py_Initialize`によって自動的に作られる)
グローバルインタプリタ一つだけが存在すると仮定する事に気をつけて下さい。 Python は (:cfunc:`Py_NewInterpreter`を使って)
追加のインタプリタを作成できることに 変わりはありませんが、複数インタプリタと :cfunc:`PyGILState_\*` API を混ぜて
使うことはサポートされていません。


.. ctype:: PyInterpreterState

   このデータ構造体は、協調動作する多数のスレッド間で共有されている 状態 (state) を表現します。同じインタプリタに属するスレッドは
   モジュール管理情報やその他いくつかの内部的な情報を共有しています。 この構造体には公開 (public) のメンバはありません。

   異なるインタプリタに属するスレッド間では、利用可能なメモリ、 開かれているファイルデスクリプタなどといったプロセス状態を除き、
   初期状態では何も共有されていません。グローバルインタプリタロック もまた、スレッドがどのインタプリタに属しているかに関わらず
   すべてのスレッドで共有されています。


.. ctype:: PyThreadState

   単一のスレッドの状態を表現する表現するデータ構造体です。 データメンバ :ctype:`PyInterpreterState \*`:attr:`interp`
   だけが公開されていて、スレッドのインタプリタ状態を指すポインタに なっています。


.. cfunction:: void PyEval_InitThreads()

   .. index::
      single: PyEval_ReleaseLock()
      single: PyEval_ReleaseThread()

   グローバルインタプリタロックを初期化し、獲得します。 この関数は、主スレッドが第二のスレッドを生成する以前や、
   :cfunc:`PyEval_ReleaseLock` や ``PyEval_ReleaseThread(tstate)``
   といった他のスレッド操作に入るよりも前に呼び出されるようにして おかなければなりません。

   .. index:: single: Py_Initialize()

   二度目に呼び出すと何も行いません。この関数を :cfunc:`Py_Initialize` の前に呼び出しても 安全です。

   .. index:: module: thread

   主スレッドしか存在しないのであれば、ロック操作は必要ありません。 これはよくある状況ですし (ほとんどの Python プログラムはスレッドを
   使いません)、ロック操作はインタプリタをごくわずかに低速化します。 従って、初期状態ではロックは生成されません。ロックを使わない状況は、
   すでにロックを獲得している状況と同じです: 単一のスレッドしか なければ、オブジェクトへのアクセスは全て安全です。従って、
   この関数がロックを初期化すると、同時にロックを獲得するようになって います。Python の :mod:`thread` モジュールは、
   新たなスレッドを作成する前に、ロックが存在するか、あるいはまだ 作成されていないかを調べ、:cfunc:`PyEval_InitThreads` を
   呼び出します。この関数から処理が戻った場合、ロックが作成作成され、呼び出 し元スレッドがそのロックを獲得している事が保証されています。

   どのスレッドが現在グローバルインタプリタロックを (存在する場合)  持っているか分からない時にこの関数を使うのは安全では **ありません** 。

   この関数はコンパイル時にスレッドサポートを無効化すると利用できません。


.. cfunction:: int PyEval_ThreadsInitialized()

   :cfunc:`PyEval_InitThreads`をすでに呼び出している場合は真 (非ゼロ)
   を返します。この関数は、ロックを獲得せずに呼び出すことができますので、シ ングルスレッドで実行している場合にはロック関連のAPI呼び出しを避けるため
   に使うことができます。 この関数はコンパイル時にスレッドサポートを無効化すると利用できません。

   .. versionadded:: 2.4


.. cfunction:: void PyEval_AcquireLock()

   グローバルインタプリタロックを獲得します。 ロックは前もって作成されていなければなりません。 この関数を呼び出したスレッドがすでにロックを獲得している場合、
   デッドロックに陥ります。 この関数はコンパイル時にスレッドサポートを無効化すると利用できません。


.. cfunction:: void PyEval_ReleaseLock()

   グローバルインタプリタロックを解放します。 ロックは前もって作成されていなければなりません。
   この関数はコンパイル時にスレッドサポートを無効化すると利用できません。


.. cfunction:: void PyEval_AcquireThread(PyThreadState *tstate)

   グローバルインタプリタロックを獲得し、現在のスレッド状態を *tstate* に設定します。*tstate* は *NULL*であっては
   なりません。ロックはあらかじめ作成されていなければなりません。 この関数を呼び出したスレッドがすでにロックを獲得している場合、 デッドロックに陥ります。
   この関数はコンパイル時にスレッドサポートを無効化すると利用できません。


.. cfunction:: void PyEval_ReleaseThread(PyThreadState *tstate)

   現在のスレッド状態をリセットして *NULL* にし、グローバルインタプリタ ロックを解放します。ロックはあらかじめ作成されていなければならず、
   かつ現在のスレッドが保持していなければなりません。*tstate* は *NULL*であってはなりませんが、その値が現在のスレッド状態を
   表現しているかどうかを調べるためにだけ使われます --- もしそうで なければ、致命的エラーが報告されます。
   この関数はコンパイル時にスレッドサポートを無効化すると利用できません。


.. cfunction:: PyThreadState* PyEval_SaveThread()

   (インタプリタロックが生成されていて、スレッドサポートが有効の 場合) インタプリタロックを解放して、スレッド状態を *NULL*にし、 以前のスレッド状態
   (*NULL*にはなりません) を返します。 ロックがすでに生成されている場合、現在のスレッドがロックを獲得 していなければなりません。


.. cfunction:: void PyEval_RestoreThread(PyThreadState *tstate)

   (インタプリタロックが生成されていて、スレッドサポートが有効の 場合) インタプリタロックを獲得して、現在のスレッド状態を *tstate*
   に設定します。*tstate* は *NULL*であっては なりません。 この関数を呼び出したスレッドがすでにロックを獲得している場合、
   デッドロックに陥ります。 (この関数はコンパイル時にスレッドサポートを無効化すると利用できません。)

以下のマクロは、通常末尾にセミコロンを付けずに使います; Python ソース配布物内の使用例を見てください。


.. cmacro:: Py_BEGIN_ALLOW_THREADS

   このマクロを展開すると ``{ PyThreadState *_save; _save = PyEval_SaveThread();`` になります。
   マクロに開き波括弧が入っていることに注意してください; この波括弧は 後で :cmacro:`Py_END_ALLOW_THREADS`
   マクロと対応させなければ なりません。 マクロについての詳しい議論は上記を参照してください。 コンパイル時にスレッドサポートが無効化されていると何も行いません。


.. cmacro:: Py_END_ALLOW_THREADS

   このマクロを展開すると ``PyEval_RestoreThread(_save); }`` になります。
   マクロに開き波括弧が入っていることに注意してください; この波括弧は 事前の :cmacro:`Py_BEGIN_ALLOW_THREADS` マクロと対応して
   いなければなりません。 マクロについての詳しい議論は上記を参照してください。 コンパイル時にスレッドサポートが無効化されていると何も行いません。


.. cmacro:: Py_BLOCK_THREADS

   このマクロを展開すると ``PyEval_RestoreThread(_save);`` になります:
   閉じ波括弧のない:cmacro:`Py_END_ALLOW_THREADS` と同じです。 コンパイル時にスレッドサポートが無効化されていると何も行いません。


.. cmacro:: Py_UNBLOCK_THREADS

   このマクロを展開すると ``_save = PyEval_SaveThread();`` になります:
   閉じ波括弧のない:cmacro:`Py_BEGIN_ALLOW_THREADS` と同じです。
   コンパイル時にスレッドサポートが無効化されていると何も行いません。

以下の全ての関数はコンパイル時にスレッドサポートが有効になっている 時だけ利用でき、呼び出すのはインタプリタロックがすでに作成されている
場合だけにしなくてはなりません。


.. cfunction:: PyInterpreterState* PyInterpreterState_New()

   新しいインタプリタ状態オブジェクトを生成します。 インタプリタロックを保持しておく必要はありませんが、この関数を次々に
   呼び出す必要がある場合には保持しておいたほうがよいでしょう。


.. cfunction:: void PyInterpreterState_Clear(PyInterpreterState *interp)

   インタプリタ状態オブジェクト内の全ての情報をリセットします。 インタプリタロックを保持していなければなりません。


.. cfunction:: void PyInterpreterState_Delete(PyInterpreterState *interp)

   インタプリタ状態オブジェクトを破壊します。 インタプリタロックを保持しておく必要はありません。
   インタプリタ状態は:cfunc:`PyInterpreterState_Clear` であらかじめ リセットしておかなければなりません。


.. cfunction:: PyThreadState* PyThreadState_New(PyInterpreterState *interp)

   指定したインタプリタオブジェクトに属する新たなスレッド状態オブジェクトを 生成します。 インタプリタロックを保持しておく必要はありませんが、この関数を次々に
   呼び出す必要がある場合には保持しておいたほうがよいでしょう。


.. cfunction:: void PyThreadState_Clear(PyThreadState *tstate)

   スレッド状態オブジェクト内の全ての情報をリセットします。 インタプリタロックを保持していなければなりません。


.. cfunction:: void PyThreadState_Delete(PyThreadState *tstate)

   スレッド状態オブジェクトを破壊します。 インタプリタロックを保持していなければなりません。
   スレッド状態は:cfunc:`PyThreadState_Clear` であらかじめ リセットしておかなければなりません。


.. cfunction:: PyThreadState* PyThreadState_Get()

   現在のスレッド状態を返します。 インタプリタロックを保持していなければなりません。 現在のスレッド状態が *NULL*なら、(呼び出し側が
   *NULL*チェックを しなくてすむように) この関数は致命的エラーを起こすようになっています。


.. cfunction:: PyThreadState* PyThreadState_Swap(PyThreadState *tstate)

   現在のスレッド状態を *tstate* に指定したスレッド状態と入れ変えます。 *tstate* は*NULL*であってはなりません。
   インタプリタロックを保持していなければなりません。


.. cfunction:: PyObject* PyThreadState_GetDict()

   拡張モジュールがスレッド固有の状態情報を保存できるような辞書を返します。 各々の拡張モジュールが辞書に状態情報を保存するためには唯一のキーを
   使わねばなりません。 現在のスレッド状態がない時にこの関数を呼び出してもかまいません。 この関数が
   *NULL*を返す場合、例外はまったく送出されず、呼び出し側は 現在のスレッド状態が利用できないと考えねばなりません。

   .. versionchanged:: 2.3
      以前は、現在のスレッドがアクティブなときのみ呼び出せる ようになっており、 *NULL* は例外が送出されたことを意味していました.


.. cfunction:: int PyThreadState_SetAsyncExc(long id, PyObject *exc)

   スレッド内で非同期的に例外を送出します。 *id* 引数はターゲットとなるスレッドのスレッド id です; *exc* は送出する例外オブジェクトです。
   この関数は *exc* に対する参照を一切盗み取りません。 素朴な間違いを防ぐため、この関数を呼び出すには独自に C 拡張モジュール を書かねばなりません。
   グローバルインタプリタロックを保持した状態で呼び出さなければなりません。

   変更を受けたスレッド状態の数を返します; これは普通は1ですが、スレッドidが 見つからなかった場合は0になります。 もし *exc* が
   :const:`NULL` であれば、そのスレッドで保留されている 例外があればクリアします。 この関数自体は例外を送出しません。

   .. versionadded:: 2.3


.. cfunction:: PyGILState_STATE PyGILState_Ensure()

   Pythonの状態やスレッドロックに関わらず、実行中スレッドでPython C APIの呼
   び出しが可能となるようにします。この関数はスレッド内で何度でも呼び出すこ とができますが、必ず全ての呼び出しに対応して
   :cfunc:`PyGILState_Release`を呼び出す必要があります。

   通常、:cfunc:`PyGILState_Ensure`呼び出しと
   :cfunc:`PyGILState_Release`呼び出しの間でこれ以外のスレッド関連API
   を使用することができますが、Release()の前にスレッド状態は復元されていな
   ければなりません。通常の:cmacro:`Py_BEGIN_ALLOW_THREADS`マクロと
   :cmacro:`Py_END_ALLOW_THREADS`も使用することができます。

   戻り値は:cfunc:`PyGILState_Acquire`呼び出し時のスレッド状態を隠蔽し
   た"ハンドル"で、:cfunc:`PyGILState_Release`に渡してPythonを同じ状態
   に保たなければなりません。再起呼び出しも可能ですが、ハンドルを共有するこ とは*できません* -
   それぞれの:cfunc:`PyGILState_Ensure`呼び出し
   でハンドルを保存し、対応する:cfunc:`PyGILState_Release`呼び出しで渡し てください。

   関数から復帰したとき、実行中のスレッドはGILを所有しています。処理の失敗 は致命的なエラーです。

   .. versionadded:: 2.3


.. cfunction:: void PyGILState_Release(PyGILState_STATE)

   獲得したすべてのリソースを開放します。この関数を呼び出すと、Pythonの状態
   は対応する:cfunc:`PyGILState_Ensure`を呼び出す前と同じとなります。(通
   常、この状態は呼び出し元でははわかりませんので、GILState APIを利用するよ うにしてください。）

   :cfunc:`PyGILState_Ensure`を呼び出す場合は、必ず同一スレッド内で対
   応する:cfunc:`PyGILState_Release`を呼び出してください。

   .. versionadded:: 2.3


.. _profiling:

プロファイルとトレース (profiling and tracing)
==============================================

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


Python インタプリタは、プロファイル: 分析 (profile) や実行の トレース: 追跡 (trace) といった機能を組み込むために低水準の
サポートを提供しています。このサポートは、プロファイルや デバッグ、適用範囲分析 (coverage analysis) ツールなどに使われます。

Python 2.2 になってから、この機能の実装は実質的に作り直され、 C から呼び出すためのインタフェースが追加されました。 この C
インタフェースは、プロファイルやトレース作業時に、 Python レベルの呼び出し可能オブジェクトが呼び出されることによる オーバヘッドを避け、直接 C
関数呼び出しが行えるようにしています。 プロファイルやトレース機能の本質的な特性は変わっていません;
インタフェースではとレース関数をスレッドごとにインストールでき、 トレース関数に報告される基本イベント (basic event) は以前の バージョンにおいて
Python レベルのトレース関数で報告されていた ものと同じです。


.. ctype:: int (*Py_tracefunc)(PyObject *obj, PyFrameObject *frame, int what, PyObject *arg)

   :cfunc:`PyEval_SetProfile` および :cfunc:`PyEval_SetTrace`
   を使って登録できるトレース関数の形式です。最初のパラメタは オブジェクトで、登録関数に *obj* として渡されます。 *frame*
   はイベントが属している実行フレームオブジェクトで、 *what* は定数 :const:`PyTrace_CALL`,
   :const:`PyTrace_EXCEPTION`, :const:`PyTrace_LINE`, :const:`PyTrace_RETURN`,
   :const:`PyTrace_C_CALL`, :const:`PyTrace_C_EXCEPTION`,
   あるいは:const:`PyTrace_C_RETURN` のいずれかで、*arg* は *what* の値によって以下のように 異なります:

   +------------------------------+-------------------------------------------+
   | *what* の値                  | *arg* の意味                              |
   +==============================+===========================================+
   | :const:`PyTrace_CALL`        | 常に *NULL*です。                         |
   +------------------------------+-------------------------------------------+
   | :const:`PyTrace_EXCEPTION`   | :func:`sys.exc_info` の返す例外情報です。 |
   +------------------------------+-------------------------------------------+
   | :const:`PyTrace_LINE`        | 常に *NULL*です。                         |
   +------------------------------+-------------------------------------------+
   | :const:`PyTrace_RETURN`      | 呼び出し側に返される予定の値です。        |
   +------------------------------+-------------------------------------------+
   | :const:`PyTrace_C_CALL`      | 呼び出している関数の名前です。            |
   +------------------------------+-------------------------------------------+
   | :const:`PyTrace_C_EXCEPTION` | 常に *NULL*です。                         |
   +------------------------------+-------------------------------------------+
   | :const:`PyTrace_C_RETURN`    | 常に *NULL*です。                         |
   +------------------------------+-------------------------------------------+


.. cvar:: int PyTrace_CALL

   関数やメソッドが新たに呼び出されたり、ジェネレータが新たなエントリの 処理に入ったことを報告する際の、:ctype:`Py_tracefunc` の*what*
   の 値です。イテレータやジェネレータ関数の生成は、対応するフレーム内の Python バイトコードに制御の委譲 (control transfer)
   が起こらない ため報告されないので注意してください。


.. cvar:: int PyTrace_EXCEPTION

   例外が送出された際の:ctype:`Py_tracefunc` の*what* の値です。 現在実行されているフレームで例外がセットされ、何らかのバイトコードが
   処理された後に、*what* にこの値がセットされた状態でコールバック 関数が呼び出されます。

   この結果、例外の伝播によって Python が呼び出しスタックを逆戻りする 際に、各フレームから処理が戻るごとにコールバック関数が呼び出されます。
   トレース関数だけがこれらのイベントを受け取ります; プロファイラは この種のイベントを必要としません。


.. cvar:: int PyTrace_LINE

   行番号イベントを報告するときに (プロファイル関数ではなく) トレース関数の*what* パラメタとして渡す値です。


.. cvar:: int PyTrace_RETURN

   関数呼び出しが例外の伝播なしに返るときに :ctype:`Py_tracefunc` 関数の*what* パラメタとして渡す値です。


.. cvar:: int PyTrace_C_CALL

   C関数を呼び出す直前に :ctype:`Py_tracefunc` 関数の*what* パラメタとして渡す値です。


.. cvar:: int PyTrace_C_EXCEPTION

   C関数が例外を送出したときに :ctype:`Py_tracefunc` 関数の*what* パラメタとして渡す値です。


.. cvar:: int PyTrace_C_RETURN

   C関数から戻るときに :ctype:`Py_tracefunc` 関数の*what* パラメタとして渡す値です。


.. cfunction:: void PyEval_SetProfile(Py_tracefunc func, PyObject *obj)

   プロファイル関数を *func* に設定します。*obj* パラメタは 関数の第一パラメタとして渡され、何らかの Python オブジェクトかまたは
   *NULL*になります。プロファイル関数がスレッド状態を維持する必要が あるなら、各々のスレッドに異なる *obj* を使うことで、状態を
   記憶しておく便利でスレッドセーフな場所を提供できます。プロファイル 関数は、モニタされているイベントのうち、行番号イベントを除く全ての
   イベントに対して呼び出されます。


.. cfunction:: void PyEval_SetTrace(Py_tracefunc func, PyObject *obj)

   トレース関数を *func* にセットします。 :cfunc:`PyEval_SetProfile` に似ていますが、トレース関数は
   行番号イベントを受け取る点が違います。


.. _advanced-debugging:

高度なデバッガサポート (advanced debugger support)
==================================================

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


以下の関数は高度なデバッグツールでの使用のためだけのものです。


.. cfunction:: PyInterpreterState* PyInterpreterState_Head()

   インタプリタ状態オブジェクトからなるリストのうち、先頭にあるもの を返します。

   .. versionadded:: 2.2


.. cfunction:: PyInterpreterState* PyInterpreterState_Next(PyInterpreterState *interp)

   インタプリタ状態オブジェクトからなるリストのうち、*interp* の 次にあるものを返します。

   .. versionadded:: 2.2


.. cfunction:: PyThreadState * PyInterpreterState_ThreadHead(PyInterpreterState *interp)

   インタプリタ *interp* に関連付けられているスレッドからなるリストの うち、先頭にある :ctype:`PyThreadState`
   オブジェクトを返します。

   .. versionadded:: 2.2


.. cfunction:: PyThreadState* PyThreadState_Next(PyThreadState *tstate)

   *tstate* と同じ:ctype:`PyInterpreterState` オブジェクトに属している スレッド状態オブジェクトのうち、*tstate*
   の次にあるものを返します。

   .. versionadded:: 2.2

