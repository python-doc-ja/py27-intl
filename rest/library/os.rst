
:mod:`os` --- 雑多なオペレーティングシステムインタフェース
==========================================================

.. module:: os
   :synopsis: 雑多なオペレーティングシステムインタフェース。


このモジュールでは、オペレーティングシステム依存の機能を利用する方法 として、:mod:`posix` や :mod:`nt` といったオペレーティング
システム依存の組み込みモジュールを import するよりも可搬性の高い 手段を提供しています。

.. % 様々なオペレーティングシステムインターフェース

このモジュールは、:mod:`mac` や :mod:`posix` のような、 オペレーティングシステム依存の組み込みモジュールから関数やデータを
検索して、見つかったものを取り出し (export) ます。Python における 組み込みのオペレーティングシステム依存モジュールは、同じ機能を
利用することができる限り、同じインタフェースを使います; たとえば、 ``os.stat(path)`` は *path* についての stat 情報を
(たまたま POSIX インタフェースに起源する) 同じ書式で返します。

特定のオペレーティングシステム固有の拡張も :mod:`os` を介して 利用することができますが、これらの利用はもちろん、可搬性を脅かします！

最初の :mod:`os` の import 以後、:mod:`os` を介した関数の 利用は、オペレーティングシステム依存組み込みモジュールにおける関数の
直接利用に比べてパフォーマンス上のペナルティは *全くありません*。 従って、:mod:`os`を利用しない理由は *存在しません* !

:mod:`os` モジュールには多くの関数とデータ値が入っています。 以下の項目と、その後に続くサブセクションは :mod:`os` モジュールから
直接利用できます。

.. % % Frank Stajano <fstajano@uk.research.att.com> complained that it
.. % % wasn't clear that the entries described in the subsections were all
.. % % available at the module level (most uses of subsections are
.. % % different); I think this is only a problem for the HTML version,
.. % % where the relationship may not be as clear.
.. % %


.. exception:: error

   .. index:: module: errno

   関数がシステム関連のエラー(引数の型違いや他のありがちなエラーではない) を返した場合この例外が発生します。これは :exc:`OSError` とし
   て知られる組み込み例外でもあります。付属する値は :cdata:`errno` から とった数値のエラーコードと、エラーコードに対応する、C 関数
   :cfunc:`perror` により出力されるのと同じ文字列からなるペアです。 背後のオペレーティングシステムで定義されているエラーコード名が収め られている
   :mod:`errno` を参照してください。

   例外がクラスの場合、この例外は二つの属性、:attr:`errno` と :attr:`strerror` を持ちます。前者の属性は C の
   :cdata:`errno` 変数 の値、後者は :cfunc:`strerror` による対応するエラーメッセージ
   の値を持ちます。(:func:`chdir` や :func:`unlink` のような) ファイルシステム上のパスを含む例外に対しては、この例外インスタンス
   は 3 つめの属性、:attr:`filename` を持ち、関数に渡されたファイル名 となります。


.. data:: name

   import されているオペレーティング・システム依存モジュールの名前です。 現在次の名前が登録されています: ``'posix'``, ``'nt'`` 、
   ``'dos'`` 、 ``'mac'`` 、 ``'os2'`` 、 ``'ce'`` 、 ``'java'`` 、 ``'riscos'`` 。


.. data:: path

   :mod:`posixpath` や :mod:`macpath` のように、システムごとに対応
   付けられているパス名操作のためのシステム依存の標準モジュールです。 すなわち、正しく import が行われるかぎり、
   ``os.path.split(file)`` は ``posixpath.split(file)``
   と等価でありながらより汎用性があります。このモジュール自体が import 可能なモジュールでもあるので注意してください。: :mod:`os.path`
   として直接 import してもかまいません。


.. _os-procinfo:

プロセスのパラメタ
------------------

これらの関数とデータ要素は、現在のプロセスおよびユーザに対する情報 提供および操作のための機能を提供しています。


.. data:: environ

   環境変数の値を表すマップ型オブジェクトです。例えば、 ``environ['HOME']`` は( いくつかのプラットフォーム上での) あなたの
   ホームディレクトリへのパスです。これは C の ``getenv("HOME")`` と 等価です。

   このマップ型の内容は、:mod:`os` モジュールの最初の import の時点、 通常は Python の起動時に :file:`site.py`
   が処理される中で取り込まれます。 それ以後に変更された環境変数は ``os.environ`` を直接変更しない限り 反映されません。

   プラットフォーム上で :func:`putenv` がサポートされている場合、この マップ型オブジェクトは環境変数に対するクエリと同様に変更するために使うこ
   ともできます。:func:`putenv` はマップ型オブジェクトが修正される時に、 自動的に呼ばれることになります。

   .. note::

      :func:`putenv` を直接呼び出しても``os.environ`` の
      内容は変わらないので、``os.environ``を直接変更する方がベターです。

   .. note::

      FreeBSD と Mac OS X を含むいつくかのプラットフォームでは、 ``environ`` の値を変更するとメモリリークの原因になる場合があります。
      システムの :cfunc:`putenv` に関するドキュメントを参照してください。

   :func:`putenv` が提供されていない場合、このマッピングオブジェクト
   に変更を加えたコピーを適切なプロセス生成機能に渡して、子プロセスが修正された環境変数 を利用するようにできます。

   プラットフォームが :func:`unsetenv` 関数をサポートしているならば、 このマッピングからアイテムを取り除いて環境変数を取り消すことができます。
   :func:`unsetenv` は ``os.environ`` からアイテムが取り除かれた時に 自動的に呼ばれます。


.. function:: chdir(path)
              getcwd()
   :noindex:

   これらの関数は、"ファイルとディレクトリ" (:ref:`os-file-dir` 節) で 説明されています。


.. function:: ctermid()

   プロセスの制御端末に対応するファイル名を返します。 利用できる環境: Unix。


.. function:: getegid()

   現在のプロセスの実行グループ id を返します。この id は 現在のプロセスで実行されているファイルの 'set id' ビットに 対応します。
   利用できる環境: Unix。


.. function:: geteuid()

   .. index:: single: user; effective id

   現在のプロセスの実行ユーザ id を返します。 利用できる環境: Unix。


.. function:: getgid()

   .. index:: single: process; group

   現在のプロセスの実際のグループ id を返します。 利用できる環境: Unix。


.. function:: getgroups()

   現在のプロセスに関連づけられた従属グループ id のリストを返します。 利用できる環境: Unix。


.. function:: getlogin()

   現在のプロセスの制御端末にログインしているユーザ名を返します。ほとんどの 場合、ユーザが誰かを知りたいときには環境変数 :envvar:`LOGNAME`
   を、現在有 効になっているユーザ名を知りたいときには  ``pwd.getpwuid(os.getuid())[0]`` を使うほうが便利です。
   利用できる環境: Unix。


.. function:: getpgrp()

   .. index:: single: process; group

   現在のプロセス・グループの id を返します。 利用できる環境: Unix。


.. function:: getpid()

   .. index:: single: process; id

   現在のプロセス id を返します。 利用できる環境: Unix、 Windows。


.. function:: getppid()

   .. index:: single: process; id of parent

   親プロセスの id を返します。 利用できる環境: Unix。


.. function:: getuid()

   .. index:: single: user; id

   現在のプロセスのユーザ id を返します。 利用できる環境: Unix。


.. function:: getenv(varname[, value])

   環境変数 *varname* が存在する場合にはその値を返し、存在しない 場合には *value* を返します。*value* のデフォルト値は
   ``None`` です。 利用できる環境: Unix互換環境、Windows。


.. function:: putenv(varname, value)

   .. index:: single: environment variables; setting

   *varname* と名づけられた環境変数の値を文字列 *value* に 設定します。このような環境変数への変更は、:func:`os.system` 、
   :func:`popen`  、 :func:`fork` および :func:`execv`  により起動された子プロセスに影響します。 利用できる環境:
   主な Unix互換環境、Windows。

   .. note::

      FreeBSD と Mac OS X を含むいつくかのプラットフォームでは、 ``environ`` の値を変更するとメモリリークの原因になる場合があります。
      システムの putenv に関するドキュメントを参照してください。

   :func:`putenv` がサポートされている場合、 ``os.environ``  の要素に対する代入を行うと自動的に :func:`putenv`
   を呼び出します;  しかし、:func:`putenv` の呼び出しは ``os.environ`` を更新しない ので、実際には ``os.environ``
   の要素に代入する方が望ましい操作です。


.. function:: setegid(egid)

   現在のプロセスに有効なグループIDをセットします。 利用できる環境: Unix。


.. function:: seteuid(euid)

   現在のプロセスに有効なユーザIDをセットします。 利用できる環境: Unix。


.. function:: setgid(gid)

   現在のプロセスにグループ id をセットします。 利用できる環境: Unix。


.. function:: setgroups(groups)

   現在のグループに関連付けられた従属グループ id のリストを *groups* に設定します。*groups* はシーケンス型でなくてはならず、
   各要素はグループを特定する整数でなくてはなりません。この操作は 通常、スーパユーザしか利用できません。 利用できる環境: Unix。

   .. versionadded:: 2.2


.. function:: setpgrp()

   システムコール :cfunc:`setpgrp` または :cfunc:`setpgrp(0, 0)` のどちらかのバージョンのうち、 (実装されていれば)
   実装されている方を呼び出します。 機能については Unix マニュアルを参照してください。 利用できる環境: Unix


.. function:: setpgid(pid, pgrp)

   システムコール :cfunc:`setpgid` を呼び出して、 *pid* の id をもつプロセスのプロセスグループ id を *pgrp* に設定します。
   利用できる環境: Unix


.. function:: setreuid(ruid, euid)

   現在のプロセスに対して実際のユーザ id および実行ユーザ id を 設定します。 利用できる環境: Unix


.. function:: setregid(rgid, egid)

   現在のプロセスに対して実際のグループ id および実行ユーザ id を 設定します。 利用できる環境: Unix


.. function:: getsid(pid)

   システムコール :cfunc:`getsid` を呼び出します。機能については Unix マニュアルを参照してください。 利用できる環境: Unix。

   .. versionadded:: 2.4


.. function:: setsid()

   システムコール :cfunc:`setsid` を呼び出します。機能については Unix マニュアルを参照してください。 利用できる環境: Unix


.. function:: setuid(uid)

   .. index:: single: user; id, setting

   現在のプロセスのユーザ id を設定します。 利用できる環境: Unix

.. % % placed in this section since it relates to errno.... a little weak ;-(


.. function:: strerror(code)

   エラーコード *code* に対応するエラーメッセージを返します。 利用できる環境: Unix、Windows


.. function:: umask(mask)

   現在の数値 umask を設定し、以前の umask 値を返します。 利用できる環境: Unix、Windows


.. function:: uname()

   .. index::
      single: gethostname() (in module socket)
      single: gethostbyaddr() (in module socket)

   現在のオペレーティングシステムを特定する情報の入った 5 要素のタプル を返します。このタプルには 5 つの文字列: ``(sysname, nodename,
   release, version, machine)`` が入っています。 システムによっては、ノード名を 8 文字、または先頭の要素だけに 切り詰めます;
   ホスト名を取得する方法としては、 :func:`socket.gethostname`   を使う方がよいでしょう、あるいは
   ``socket.gethostbyaddr(socket.gethostname())`` でもかまいません。 利用できる環境: Unix互換環境


.. function:: unsetenv(varname)

   .. index:: single: environment variables; deleting

   *varname* という名前の環境変数を取り消します。 このような環境の変化は :func:`os.system`、 :func:`popen` または
   :func:`fork` と :func:`execv` で開始されるサブプロセスに影響を与えます。 利用できる環境:  ほとんどの
   Unix互換環境、Windows

   :func:`unsetenv` がサポートされている時には ``os.environ`` のアイテムの 削除が対応する :func:`unsetenv`
   の呼び出しに自動的に翻訳されます。しかし、 :func:`unsetenv` の呼び出しは ``os.environ`` を更新しませんので、 むしろ
   ``os.environ`` のアイテムを削除する方が好ましい方法です。


.. _os-newstreams:

ファイルオブジェクトの生成
--------------------------

以下の関数は新しいファイルオブジェクトを作成します。


.. function:: fdopen(fd[, mode[, bufsize]])

   .. index:: single: I/O control; buffering

   ファイル記述子 *fd* に接続している、開かれた ファイルオブジェクトを返します。 引数 *mode* および *bufsize* は、組み込み関数
   :func:`open`  における対応する引数と同じ意味を持ちます。 利用できる環境: Macintosh、 Unix、Windows

   .. versionchanged:: 2.3
      引数 *mode* は、指定されるならば、 ``'r'``、 ``'w'``、 ``'a'`` のいずれかの文字で始まらなければなりません。 そうでなければ
      :exc:`ValueError` が送出されます.

   .. versionchanged:: 2.5
      Unixでは、引数 *mode* が ``'a'`` で始まる時には *O_APPEND* フラグがファイル記述子に設定されます。
      (ほとんどのプラットフォームで :cfunc:`fdopen` 実装が既に行なっていることです).


.. function:: popen(command[, mode[, bufsize]])

   *command* への、または *command* からのパイプ入出力を開きます。 戻り値はパイプに接続されている開かれたファイルオブジェクトで、
   *mode* が ``'r'`` (標準の設定です) または ``'w'`` かに よって読み出しまたは書き込みを行うことができます。 引数 *bufsize*
   は、組み込み関数 :func:`open`  における対応する引数と同じ意味を持ちます。 *command* の終了ステータス (:func:`wait`
   で指定された書式でコード化 されています) は、:meth:`close` メソッドの戻り値として取得することが できます。例外は終了ステータスがゼロ
   (すなわちエラーなしで終了) の 場合で、このときには ``None`` を返します。 利用できる環境: Macintosh、Unix、Windows

   .. versionchanged:: 2.0
      この関数は、Pythonの初期のバージョンでは、 Windows環境下で信頼できない動作をしていました。これはWindowsに付属 して提供されるライブラリの
      :cfunc:`_popen` 関数を利用したことに よるものです。新しいバージョンの Python では、Windows 付属のライブラリ
      にある壊れた実装を利用しません.


.. function:: tmpfile()

   更新モード(``w+b``)で開かれた新しいファイルオブジェクトを返します。 このファイルはディレクトリエントリ登録に関連付けられておらず、
   このファイルに対するファイル記述子がなくなると自動的に削除されます。 利用できる環境: Macintosh、Unix、Windows

以下の :func:`popen` の変種はどれも、*bufsize* が指定されている場合には I/O パイプのバッファサイズを表します。 *mode*
を指定する場合には、文字列 ``'b'`` または ``'t'`` でなければなりません; これは、Windows でファイルをバイナリモードで開くか
テキストモードで開くかを決めるために必要です。 *mode* の標準の 設定値は``'t'`` です。

またUnixではこれらの変種はいずれも *cmd* をシーケンスにできます。その場合、 引数はシェルの介在なしに直接 (:func:`os.spawnv`
のように) 渡されます。 *cmd* が文字列の場合、引数は( :func:`os.system` のように) シェルに渡されます。

以下のメソッドは子プロセスから終了ステータスを取得できるようには していません。入出力ストリームを制御し、かつ終了コードの取得も 行える唯一の方法は、
:mod:`popen2` モジュールの  :class:`Popen3` と  :class:`Popen4`  クラスを利用する事です。これらは
Unix上でのみ利用可能です。

これらの関数の利用に関係して起きうるデッドロック状態についての議論は、 "フロー制御問題 (XXX reference: popen2-flow-
control.html)" (section :ref:`popen2-flow-control`) を参照してください。


.. function:: popen2(cmd[, mode[, bufsize]])

   *cmd* を子プロセスとして実行します。ファイル・オブジェクト ``(child_stdin, child_stdout)`` を返します。 利用できる環境:
   Macintosh、Unix、Windows

   .. versionadded:: 2.0


.. function:: popen3(cmd[, mode[, bufsize]])

   *cmd* を子プロセスとして実行します。ファイルオブジェクト  ``(child_stdin, child_stdout, child_stderr)`` を
   返します。 利用できる環境: Macintosh、Unix、Windows

   .. versionadded:: 2.0


.. function:: popen4(cmd[, mode[, bufsize]])

   *cmd* を子プロセスとして実行します。ファイルオブジェクト ``(child_stdin, child_stdout_and_stderr)``
   を返します。 利用できる環境: Macintosh、Unix、Windows

   .. versionadded:: 2.0

(``child_stdin, child_stdout, および child_stderr`` は子プロセスの視点で名付けられているので注意してください。
すなわち、*child_stdin* とは子プロセスの標準入力を意味します。)

この機能は :mod:`popen2` モジュール内の同じ名前の関数 を使っても実現できますが、これらの関数の戻り値は異なる順序を持ってい ます。


.. _os-fd-ops:

ファイル記述子の操作
--------------------

これらの関数は、ファイル記述子を使って参照されている I/Oストリームを操作します。

ファイル記述子とは現在のプロセスから開かれたファイルに対応する小さな整数です。 例えば、標準入力のファイル記述子はいつでも 0 で、標準出力は 1、標準エラーは
2 です。 その他にさらにプロセスから開かれたファイルには 3、4、5、などが割り振られます。
「ファイル記述子」という名前は少し誤解を与えるものかもしれませんが、 Unixプラットフォームにおいて、ソケットやパイプもファイル記述子によって参照されます。


.. function:: close(fd)

   ファイルディスクリプタ *fd* を閉じます。 利用できる環境: Macintosh、 Unix、 Windows

   .. note::

      注:この関数は低レベルの I/O のためのもので、:func:`open` や  :func:`pipe` が返すファイル記述子に対して適用しなければ
      なりません。組み込み関数 :func:`open` や :func:`popen` 、 :func:`fdopen` の返す "ファイルオブジェクト"
      を閉じるには、 オブジェクトの :meth:`close` メソッドを使ってください。


.. function:: dup(fd)

   ファイル記述子 *fd* の複製を返します。 利用できる環境: Macintosh、 Unix、 Windows.


.. function:: dup2(fd, fd2)

   ファイル記述子を *fd* から *fd2* に複製し、必要なら後者の 記述子を前もって閉じておきます。 利用できる環境:
   Macintosh、Unix、Windows


.. function:: fdatasync(fd)

   ファイル記述子 *fd* を持つファイルのディスクへの書き込みを 強制します。メタデータの更新は強制しません。 利用できる環境: Unix


.. function:: fpathconf(fd, name)

   開いているファイルに関連したシステム設定情報 (system configuration information) を返します。 *name*
   には取得したい設定名を指定します;  これは定義済みのシステム固有値名の文字列で、多くの標準 (POSIX.1、 Unix 95、 Unix 98 その他)
   で定義されています。 プラットフォームによっては別の名前も定義しています。 ホストオペレーティングシステムの関知する名前は ``pathconf_names``
   辞書で与えられています。このマップオブジェクトに入っていない設定 変数については、 *name* に整数を渡してもかまいません。 利用できる環境:
   Macintosh、Unix

   もし *name* が文字列でかつ不明である場合、 :exc:`ValueError`  を送出します。*name*
   の指定値がホストシステムでサポートされておらず、 ``pathconf_names`` にも入っていない場合、:const:`errno.EINVAL`
   をエラー番号として :exc:`OSError` を送出します。


.. function:: fstat(fd)

   :func:`stat` のようにファイル記述子 *fd* の状態を返します。 利用できる環境: Macintosh、Unix、Windows


.. function:: fstatvfs(fd)

   :func:`statvfs` のように、ファイル記述子 *fd* に関連 づけられたファイルが入っているファイルシステムに関する情報を返します。
   利用できる環境: Unix


.. function:: fsync(fd)

   ファイル記述子 *fd* を持つファイルのディスクへの書き込みを強制します。 Unixでは、ネイティブの :cfunc:`fsync` 関数を、Windows
   では MS  :cfunc:`_commit` 関数を呼び出します。

   Python のファイルオブジェクト *f* を使う場合、*f* の内部バッファ を確実にディスクに書き込むために、まず ``f.flush()`` を実行し、
   それから ``os.fsync(f.fileno())`` してください。 利用できる環境: Macintosh、Unix、2.2.3 以降では Windows
   も


.. function:: ftruncate(fd, length)

   ファイル記述子 *fd* に対応するファイルを、サイズが最大で  *length* バイトになるように切り詰めます。 利用できる環境:
   Macintosh、Unix


.. function:: isatty(fd)

   ファイル記述子 *fd* が開いていて、tty(のような)装置に接 続されている場合、``1`` を返します。そうでない場合は ``0`` を返 します。
   利用できる環境: Macintosh、Unix


.. function:: lseek(fd, pos, how)

   ファイル記述子 *fd* の現在の位置を *pos* に設定します。 *pos* の意味は *how* で修飾されます:  ファイルの先頭からの相対には
   ``0`` を設定します;  現在の位置からの相対には``1`` を設定します;  ファイルの末尾からの相対には ``2`` を設定します。
   利用できる環境:Macintosh、 Unix、Windows。


.. function:: open(file, flags[, mode])

   ファイル *file* を開き、*flag* に従って様々なフラグを 設定し、可能なら *mode* に従ってファイルモードを設定します。 *mode*
   の標準の設定値は ``0777`` (8進表現) で、先に 現在の umask を使ってマスクを掛けます。新たに開かれたファイルの
   のファイル記述子を返します。利用できる環境:Macintosh、Unix、Windows。 フラグとファイルモードの値についての詳細は C
   ランタイムのドキュメントを 参照してください; (:const:`O_RDONLY` や :const:`O_WRONLY` のような)
   フラグ定数はこのモジュールでも定義されています (以下を参照してください)。

   .. note::

      この関数は低レベルの I/O のためのものです。通常の利用では、 :meth:`read` や :meth:`write` (やその他多くの) メソッドを持つ
      「ファイルオブジェクト」 を返す、組み込み関数 :func:`open` を 使ってください。 ファイル記述子を「ファイルオブジェクト」でラップするには
      :func:`fdopen` を使ってください。


.. function:: openpty()

   .. index:: module: pty

   新しい擬似端末のペアを開きます。ファイル記述子のペア ``(master, slave)`` を返し、それぞれ pty および tty を表します。(少しだけ)
   より可搬性のあるアプローチとしては、 :mod:`pty` モジュールを使ってください。 利用できる環境: Macintosh、いくつかの Unix系システム


.. function:: pipe()

   パイプを作成します。ファイル記述子のペア ``(r, w)``  を返し、それぞれ読み出し、書き込み用に使うことができます。 利用できる環境:
   Macintosh、Unix、Windows


.. function:: read(fd, n)

   ファイル記述子 *fd* から最大で *n* バイト読み出します。 読み出されたバイト列の入った文字列を返します。*fd* が参照して
   いるファイルの終端に達した場合、空の文字列が返されます。 利用できる環境: Macintosh、Unix、Windows。

   .. note::

      この関数は低レベルの I/O のためのもので、:func:`open` や  :func:`pipe` が返すファイル記述子に対して適用しなければ
      なりません。組み込み関数 :func:`open` や :func:`popen` 、 :func:`fdopen` の返す "ファイルオブジェクト"
      、あるいは ``sys.stdin`` から読み出すには、オブジェクトの :meth:`read`  メソッドを使ってください。


.. function:: tcgetpgrp(fd)

   *fd* (:func:`open` が返す開かれたファイル記述子)  で与えられる端末に関連付けられたプロセスグループを返します。 利用できる環境:
   Macintosh、Unix


.. function:: tcsetpgrp(fd, pg)

   *fd* (:func:`open` が返す開かれたファイル記述子)  で与えられる端末に関連付けられたプロセスグループを *pg* に設定します。
   利用できる環境: Macintosh、Unix


.. function:: ttyname(fd)

   ファイル記述子 *fd* に関連付けられている端末デバイスを特定する 文字列を返します。*fd* が端末に関連付けられていない場合、 例外が送出されます。
   利用できる環境: Macintosh、Unix


.. function:: write(fd, str)

   ファイル記述子 *fd* に文字列 *str* を書き込みます。 実際に書き込まれたバイト数を返します。 利用できる環境:Macintosh、
   Unix、Windows。

   .. note::

      この関数は低レベルの I/O のためのもので、:func:`open` や  :func:`pipe` が返すファイル記述子に対して適用しなければ
      なりません。組み込み関数 :func:`open` や :func:`popen` 、 :func:`fdopen` の返す "ファイルオブジェクト"
      、あるいは ``sys.stdout``、``sys.stderr`` に書き込むには、オブジェクトの :meth:`write`  メソッドを使ってください。

以下のデータ要素は :func:`open` 関数の *flags* 引数を 構築するために利用することができます。いくつかのアイテムは
全てのプラットフォームで使えるわけではありません。 何が使えるか、また何に使うのかといった説明は :manpage:`open(2)` を参照してください。


.. data:: O_RDONLY
          O_WRONLY
          O_RDWR
          O_APPEND
          O_CREAT
          O_EXCL
          O_TRUNC

   :func:`open` 関数の *flag* 引数のためのオプションフラグです。 これらの値はビット単位 OR を取れます。 利用できる環境:
   Macintosh、 Unix、Windows。


.. data:: O_DSYNC
          O_RSYNC
          O_SYNC
          O_NDELAY
          O_NONBLOCK
          O_NOCTTY
          O_SHLOCK
          O_EXLOCK

   上のフラグと同様、:func:`open` 関数の *flag* 引数のための オプションフラグです。これらの値はビット単位 OR を取れます。
   利用できる環境: Macintosh、 Unix。


.. data:: O_BINARY

   :func:`open` 関数の *flag* 引数のためのオプションフラグです。 この値は上に列挙したフラグとビット単位 OR を取ることができます。
   利用できる環境: Windows。

   .. % % XXX need to check on the availability of this one.


.. data:: O_NOINHERIT
          O_SHORT_LIVED
          O_TEMPORARY
          O_RANDOM
          O_SEQUENTIAL
          O_TEXT

   :func:`open` 関数の *flag* 引数のためのオプションフラグです。 これらの値はビット単位 OR を取ることができます。 利用できる環境:
   Windows


.. data:: SEEK_SET
          SEEK_CUR
          SEEK_END

   :func:`lseek` 関数のパラメータです。 値はそれぞれ 0、 1、 2 です。 利用できる環境: Windows、 Macintosh、 Unix

   .. versionadded:: 2.5


.. _os-file-dir:

ファイルとディレクトリ
----------------------


.. function:: access(path, mode)

   実 uid/gid を使って *path* に対するアクセスが可能か調べます。 ほとんどのオペレーティングシステムは実行 uid/gid を使うため、
   このルーチンは suid/sgid 環境において、プログラムを起動した ユーザが *path* に対するアクセス権をもっているかを調べる
   ために使われます。*path* が存在するかどうかを調べるには  *mode* を :const:`F_OK` にします。ファイル操作許可
   (permission) を調べるために :const:`R_OK`、 :const:`W_OK`、:const:`X_OK`
   から一つまたはそれ以上のフラグと OR をとることもできます。 アクセスが許可されている場合 ``True`` を、そうでない場合 ``False``
   を返します。詳細は :manpage:`access(2)` のマニュアルページを参照して ください。 利用できる環境: Macintosh、 Unix、
   Windows

   .. note::

      :func:`access` を使ってユーザーが例えばファイルを開く権限を持っているか :func:`open`
      を使って実際にそうする前に調べることはセキュリティ・ホールを 作り出してしまいます。というのは、調べる時点と開く時点の時間差を利用して
      そのユーザーがファイルを操作してしまうかもしれないからです。

   .. note::

      I/O 操作は :func:`access` が成功を思わせるときにも失敗することがありえます。 特にネットワーク・ファイルシステムにおける操作が 通常の
      POSIX 許可ビット・モデルをはみ出す意味論を備える場合には そのようなことが起こりえます。


.. data:: F_OK

   :func:`access` の *mode* に渡すための値で、 *path* が存在するかどうかを調べます。


.. data:: R_OK

   :func:`access` の *mode* に渡すための値で、 *path* が読み出し可能かどうかを調べます。


.. data:: W_OK

   :func:`access` の *mode* に渡すための値で、 *path* が書き込み可能かどうかを調べます。


.. data:: X_OK

   :func:`access` の *mode* に渡すための値で、 *path* が実行可能かどうかを調べます。


.. function:: chdir(path)

   .. index:: single: directory; changing

   現在の作業ディレクトリ (current working directory) を *path* に 設定します。利用できる環境: Macintosh、
   Unix、Windows。


.. function:: getcwd()

   現在の作業ディレクトリを表現する文字列を返します。 利用できる環境: Macintosh、 Unix、Windows。


.. function:: getcwdu()

   現在の作業ディレクトリを表現するユニコードオブジェクトを返します。 利用できる環境: Macintosh、 Unix、 Windows

   .. versionadded:: 2.3


.. function:: chroot(path)

   現在のプロセスに対してルートディレクトリを *path* に変更します。 利用できる環境: Macintosh、Unix。

   .. versionadded:: 2.2


.. function:: chmod(path, mode)

   *path* のモードを数値 *mode* に変更します。 *mode* は、(:mod:`stat` モジュールで定義されている)
   以下の値のいずれかまたはビット単位の OR で組み合わせた値を取り得ます:

* ``S_ISUID``

* ``S_ISGID``

* ``S_ENFMT``

* ``S_ISVTX``

* ``S_IREAD``

* ``S_IWRITE``

* ``S_IEXEC``

* ``S_IRWXU``

* ``S_IRUSR``

* ``S_IWUSR``

* ``S_IXUSR``

* ``S_IRWXG``

* ``S_IRGRP``

* ``S_IWGRP``

* ``S_IXGRP``

* ``S_IRWXO``

* ``S_IROTH``

* ``S_IWOTH``

* ``S_IXOTH``

   利用できる環境: Macintosh、 Unix、 Windows。

   .. note::

      Windows でも :func:`chmod` はサポートされていますが、 ファイルの読み込み専用フラグを (定数 ``S_IWRITE`` と
      ``S_IREAD``、または対応する整数値を通して) 設定できるだけです。 他のビットは全て無視されます。


.. function:: chown(path, uid, gid)

   *path* の所有者 (owner) id とグループ id を、数値 *uid* および *gid* に変更します。いずれかの id を変更せずにおくには、
   その値として -1 をセットします。 利用できる環境: Macintosh、 Unix。


.. function:: lchown(path, uid, gid)

   Change the owner and group id of *path* to the numeric *uid* and gid. This
   function will not follow symbolic links. *path* の所有者 (owner) id とグループ id を、数値
   *uid* および *gid* に変更します。この関数はシンボリックリンクをたどりません。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. function:: link(src, dst)

   *src* を指しているハードリンク *dst* を作成します。 利用できる環境: Macintosh、 Unix。


.. function:: listdir(path)

   ディレクトリ内のエントリ名が入ったリストを返します。 リスト内の順番は不定です。特殊エントリ ``'.'`` および ``'..'``
   は、それらがディレクトリに入っていてもリストには含められません。 利用できる環境: Macintosh、 Unix、 Windows。

   .. versionchanged:: 2.3
      Windows NT/2k/XP と Unixでは、*path* が Unicode オ ブジェクトの場合、Unicode オブジェクトのリストが返されます。.


.. function:: lstat(path)

   :func:`stat` に似ていますが、シンボリックリンクをたどりません。 利用できる環境: Macintosh、 Unix。


.. function:: mkfifo(path[, mode])

   数値で指定されたモード *mode* を持つ FIFO (名前付きパイプ) を *path* に作成します。*mode* の標準の値は ``0666``
   (8進) です。現在の umask 値が前もって *mode* からマスクされます。 利用できる環境: Macintosh、 Unix。

   FIFO は通常のファイルのようにアクセスできるパイプです。FIFO は (例えば :func:`os.unlink` を使って) 削除されるまで
   存在しつづけます。一般的に、FIFO は "クライアント" と "サーバ" 形式のプロセス間でランデブーを行うために使われます: このとき、 サーバは FIFO
   を読み出し用に開き、クライアントは書き込み用に 開きます。:func:`mkfifo` は FIFO を開かない --- 単にランデブー ポイントを作成するだけ
   --- なので注意してください。


.. function:: mknod(filename[, mode=0600, device])

   *filename* という名前で、ファイルシステム・ノード (ファイル、デバイス特殊 ファイル、または、名前つきパイプ) を作ります 。*mode*
   は、作ろうとす るノードの使用権限とタイプを、S_IFREG、S_IFCHR、S_IFBLK、S_IFIFO (これら の定数は :mod:`stat`
   で使用可能) のいずれかと（ビット OR で）組み合わ せて指定します。S_IFCHR と S_IFBLK を指定すると、*device* は新しく作
   られたデバイス特殊ファイルを (おそらく :func:`os.makedev` を使って)  定義し、指定しなかった場合には無視します。

   .. versionadded:: 2.3


.. function:: major(device)

   生のデバイス番号から、デバイスのメジャー番号を取り出します。(たいてい :ctype:`stat` の :attr:`st_dev` フィールドか
   :attr:`st_rdev`　 フィールドです)

   .. versionadded:: 2.3


.. function:: minor(device)

   生のデバイス番号から、デバイスのマイナー番号を取り出します。(たいてい :ctype:`stat` の :attr:`st_dev` フィールドか
   :attr:`st_rdev`　 フィールドです)

   .. versionadded:: 2.3


.. function:: makedev(major, minor)

   major と minor から、新しく生のデバイス番号を作ります。

   .. versionadded:: 2.3


.. function:: mkdir(path[, mode])

   数値で指定されたモード *mode* をもつディレクトリ *path*  を作成します。*mode* の標準の値は ``0777`` (8進)です。
   システムによっては、 *mode* は無視されます。利用の際には、 現在の umask 値が前もってマスクされます。 利用できる環境: Macintosh、
   Unix、Windows。


.. function:: makedirs(path[, mode])

   .. index::
      single: directory; creating
      single: UNC paths; and os.makedirs()

   再帰的なディレクトリ作成関数です。   :func:`mkdir` に似て いますが、末端 (leaf) となるディレクトリを作成するために必要な
   中間の全てのディレクトリを作成します。末端ディレクトリが すでに存在する場合や、作成ができなかった場合には :exc:`error`
   例外を送出します。*mode* の標準の値は ``0777`` (8進)です。 システムによっては、 *mode* は無視されます。利用の際には、 現在の
   umask 値が前もってマスクされます。

   .. note::

      :func:`makedirs` は作り出すパス要素が *os.pardir* を 含むと混乱することになります。

   .. versionadded:: 1.5.2

   .. versionchanged:: 2.3
      この関数は UNC パスを正しく扱えるようになりました.


.. function:: pathconf(path, name)

   指定されたファイルに関係するシステム設定情報を返します。 varname には取得したい設定名を指定します;
   これは定義済みのシステム固有値名の文字列で、多くの標準 (POSIX.1、 Unix 95、 Unix 98 その他) で定義されています。
   プラットフォームによっては別の名前も定義しています。 ホストオペレーティングシステムの関知する名前は ``pathconf_names``
   辞書で与えられています。このマップ型オブジェクトに入っていない設定 変数については、 *name* に整数を渡してもかまいません。 利用できる環境:
   Macintosh、Unix

   もし *name* が文字列でかつ不明である場合、 :exc:`ValueError`  を送出します。*name*
   の指定値がホストシステムでサポートされておらず、 ``pathconf_names`` にも入っていない場合、:const:`errno.EINVAL`
   をエラー番号として :exc:`OSError` を送出します。


.. data:: pathconf_names

   :func:`pathconf` および :func:`fpathconf` が受理する システム設定名を、ホストオペレーティングシステムで定義されている
   整数値に対応付けている辞書です。この辞書はシステムでどの 設定名が定義されているかを決定するために利用できます。 利用できる環境: Macintosh、
   Unix。


.. function:: readlink(path)

   シンボリックリンクが指しているパスを表す文字列を返します。 返される値は絶対パスにも、相対パスにもなり得ます; 相対 パスの場合、
   ``os.path.join(os.path.dirname(path), result)`` を使って絶対パスに変換することができます。 利用できる環境:
   Macintosh、 Unix。


.. function:: remove(path)

   ファイル *path* を削除します。*path* がディレクトリの 場合、:exc:`OSError` が送出されます; ディレクトリの削除については
   :func:`rmdir` を参照してください。この関数は下で述べられている :func:`unlink` 関数と同一です。Windows
   では、使用中のファイル を削除しようと試みると例外を送出します; Unixでは、ディレクトリ
   エントリは削除されますが、記憶装置上にアロケーションされたファイル領域は 元のファイルが使われなくなるまで残されます。 利用できる環境: Macintosh、
   Unix、Windows。


.. function:: removedirs(path)

   .. index:: single: directory; deleting

   再帰的なディレクトリ削除関数です。:func:`rmdir` と同じように 動作しますが、末端ディレクトリがうまく削除できるかぎり、
   :func:`removedirs` は *path* に現れる親ディレクトリをエラー が送出されるまで (このエラーは通常、
   指定したディレクトリの親ディレクトリが空でないことを意味するだけ なので無視されます) 順に削除することを試みます。
   例えば、``os.removedirs('foo/bar/baz')`` では最初にディレクトリ ``'foo/bar/baz'`` を削除し、次に
   ``'foo/bar'``、さらに ``'foo'`` をそれらが空ならば削除します。 末端のディレクトリが削除できなかった場合には
   :exc:`OSError` が送出されます。

   .. versionadded:: 1.5.2


.. function:: rename(src, dst)

   ファイルまたはディレクトリ *src* を *dst* に名前変更します。 *dst* がディレクトリの場合、:exc:`OSError` が送出 されます。
   Unixでは、 *dst* が存在し、かつファイルの場合、 ユーザの権限があるかぎり暗黙のうちに元のファイルが削除されます。 この操作はいくつかの Unix
   系において、*src* と *dst* が異なるファイルシステム上にあると失敗することがあります。 ファイル名の変更が成功する場合、この操作は原子的
   (atomic) 操作 となります (これは POSIX 要求仕様です) Windows では、 *dst* が既に存在する場合には、たとえファイルの場合でも
   :exc:`OSError` が送出されます; これは *dst* が既に 存在するファイル名の場合、名前変更の原子的操作を実装する手段が ないからです。
   利用できる環境: Macintosh、 Unix、Windows。


.. function:: renames(old, new)

   再帰的にディレクトリやファイル名を変更する関数です。 :func:`rename` のように動作しますが、新たなパス名を持つ
   ファイルを配置するために必要な途中のディレクトリ構造をまず作成 しようと試みます。 名前変更の後、元のファイル名のパス要素は
   :func:`removedirs` を使って右側から順に枝刈りされてゆきます。

   .. versionadded:: 1.5.2

   .. note::

      この関数はコピー元の末端のディレクトリまたはファイルを削除する 権限がない場合には失敗します。


.. function:: rmdir(path)

   ディレクトリ *path* を削除します。 利用できる環境: Macintosh、 Unix、Windows。


.. function:: stat(path)

   与えられた *path* に対して :cfunc:`stat` システムコールを 実行します。戻り値はオブジェクトで、その属性が :ctype:`stat`
   構造体の 以下に挙げる各メンバ: :attr:`st_mode` (保護モードビット)、 :attr:`st_ino` (i ノード番号)、
   :attr:`st_dev` (デバイス)、 :attr:`st_nlink` (ハードリンク数)、 :attr:`st_uid` (所有者のユーザ ID)、
   :attr:`st_gid` (所有者のグループ  ID)、 :attr:`st_size` (ファイルのバイトサイズ)、 :attr:`st_atime`
   (最終アクセス時刻)、 :attr:`st_mtime` (最終更新時刻)、 :attr:`st_ctime`
   (プラットフォーム依存：Unixでは最終メタデータ変更時刻、 Windowsでは作成時刻) となっています。 ::

      >>> import os
      >>> statinfo = os.stat('somefile.txt')
      >>> statinfo
      (33188, 422511L, 769L, 1, 1032, 100, 926L, 1105022698,1105022732, 1105022732)
      >>> statinfo.st_size
      926L
      >>>

   .. versionchanged:: 2.3
      もし :func:`stat_float_times`
      が真を返す場合、時間値は浮動小数点で秒を計ります。ファイルシステムがサポートしていれば、秒の小数点以下の桁も含めて返されます。 Mac OS
      では、時間は常に浮動小数点です。詳細な説明は :func:`stat_float_times` を参照してください.

   (Linux のような) Unix システムでは、以下の属性: :attr:`st_blocks` (ファイル用にアロケーションされているブロック数)、
   :attr:`st_blksize` (ファイルシステムのブロックサイズ)、 :attr:`st_rdev` (i ノードデバイスの場合、デバイスの形式)、
   :attr:`st_flags` (ファイルに対するユーザー定義のフラグ) も利用可能なときがあります。

   他の (FreeBSD のような) Unix システムでは、以下の属性: :attr:`st_gen` (ファイル生成番号)、
   :attr:`st_birthtime` (ファイル生成時刻) も利用可能なときがあります (ただし root
   がそれらを使うことにした場合以外は値が入っていないでしょう)。

   Mac OS システムでは、以下の属性: :attr:`st_rsize`、 :attr:`st_creator`、 :attr:`st_type`、
   も利用可能なときがあります。

   RISCOS システムでは、以下の属性: :attr:`st_ftype` (file type)、 :attr:`st_attrs`
   (attributes)、 :attr:`st_obtype` (object type)、 も利用可能なときがあります。

   後方互換性のために、:func:`stat` の戻り値は少なくとも 10 個の 整数からなるタプルとしてアクセスすることができます。このタプルは もっとも重要な
   (かつ可搬性のある) :ctype:`stat` 構造体のメンバを 与えており、以下の順番、 :attr:`st_mode`、 :attr:`st_ino`、
   :attr:`st_dev`、 :attr:`st_nlink`、 :attr:`st_uid`、 :attr:`st_gid`、
   :attr:`st_size`、 :attr:`st_atime`、 :attr:`st_mtime`、 :attr:`st_ctime`、 に並んでいます。

   .. index:: module: stat

   実装によっては、この後ろにさらに値が付け加えられていることもあります。 Mac OS では、時刻の値は Mac OS の他の時刻表現値と同じように浮動小数点数
   なので注意してください。 標準モジュール :mod:`stat` では、 :ctype:`stat` 構造体から情報を引き出す上で便利な関数や定数を定義して
   います。(Windows では、いくつかのデータ要素はダミーの値が埋められて います。)

   .. note::

      :attr:`st_atime`, :attr:`st_mtime`, および :attr:`st_ctime`
      メンバの厳密な意味や精度はオペレーティングシステムやファイルシステムによって 変わります。例えば、FAT や FAT32
      ファイルシステムを使っているWindows システム では、:attr:`st_atime` の精度は 1 日に過ぎません。詳しくはお使いのオペレーティング
      システムのドキュメントを参照してください。

   利用できる環境: Macintosh、 Unix、Windows。

   .. versionchanged:: 2.2
      返されたオブジェクトの属性としてのアクセス機能を追加しました.

   .. versionchanged:: 2.5
      st_gen、 st_birthtime を追加しました.


.. function:: stat_float_times([newvalue])

   :class:`stat_result` がタイムスタンプに浮動小数点オブジェクトを使うかどう かを決定します。*newvalue* が ``True``
   の場合、 以後の :func:`stat` 呼び出しは浮動小数点を返し、 ``False`` の場合には以後整数を返します。*newvalue*
   が省略された場合、現在の設 定どおりの戻り値になります。

   古いバージョンの Python と互換性を保つため、:class:`stat_result` にタプル としてアクセスすると、常に整数が返されます。

   .. versionchanged:: 2.5
      Python はデフォルトで浮動小数点数を返すようになりました。 浮動小数点数のタイムスタンプではうまく動かないアプリケーションはこの機能を利用して
      昔ながらの振る舞いを取り戻すことができます。.

   タイムスタンプの精度 (すなわち最小の小数部分) はシステム依存です。 システムによっては秒単位の精度しかサポートしません。
   そういったシステムでは小数部分は常に 0 です。

   この設定の変更は、プログラムの起動時に、 *__main__* モジュールの中でのみ行うことを推奨します。
   ライブラリは決して、この設定を変更するべきではありません。 浮動小数点型のタイムスタンプを処理すると、不正確な動作をするようなライブ
   ラリを使う場合、ライブラリが修正されるまで、浮動小数点型を返す機能を停止 させておくべきです。


.. function:: statvfs(path)

   与えられた *path* に対して :cfunc:`statvfs` システムコールを 実行します。戻り値はオブジェクトで、その属性は与えられたパスが収め
   られているファイルシステムについて記述したものです。かく属性は :ctype:`statvfs` 構造体のメンバ: :attr:`f_bsize`、
   :attr:`f_frsize`、 :attr:`f_blocks`、 :attr:`f_bfree`、 :attr:`f_bavail`、
   :attr:`f_files`、 :attr:`f_ffree`、 :attr:`f_favail`、 :attr:`f_flag`、
   :attr:`f_namemax`、 に対応します。 利用できる環境: Unix。

   .. index:: module: statvfs

   後方互換性のために、戻り値は上の順にそれぞれ対応する属性値が並んだ タプルとしてアクセスすることもできます。 標準モジュール :mod:`statvfs`
   では、 シーケンスとしてアクセスする場合に、:ctype:`statvfs` 構造体から情報を 引き出す上便利な関数や定数を定義しています; これは
   属性として各フィールドにアクセスできないバージョンの Python で 動作する必要のあるコードを書く際に便利です。

   .. versionchanged:: 2.2
      返されたオブジェクトの属性としてのアクセス機能を追加しました.


.. function:: symlink(src, dst)

   *src* を指しているシンボリックリンクを *dst* に作成します。 利用できる環境: Unix。


.. function:: tempnam([dir[, prefix]])

   一時ファイル (temporary file) を生成する上でファイル名として相応しい 一意なパス名を返します。この値は一時的なディレクトリエントリ
   を表す絶対パスで、*dir* ディレクトリの下か、*dir* が省略 されたり ``None`` の場合には一時ファイルを置くための共通の
   ディレクトリの下になります。*prefix* が与えられており、かつ ``None`` でない場合、ファイル名の先頭につけられる短い
   接頭辞になります。アプリケーションは :func:`tempnam` が返したパス名を使って正しくファイルを生成し、生成したファイルを 管理する責任があります;
   一時ファイルの自動消去機能は提供されて いません。

   .. warning::

      :func:`tempnam` を使うと、symlink 攻撃に対して脆弱 になります; 代りに:func:`tmpfile` (第:ref:`os-
      newstreams`節) を使うよう検討してください。

   利用できる環境: Macintosh、 Unix、 Windows。


.. function:: tmpnam()

   一時ファイル (temporary file) を生成する上でファイル名として相応しい 一意なパス名を返します。この値は一時ファイルを置くための共通の
   ディレクトリ下の一時的なディレクトリエントリを表す絶対パスです。 アプリケーションは :func:`tmpnam`
   が返したパス名を使って正しくファイルを生成し、生成したファイルを 管理する責任があります; 一時ファイルの自動消去機能は提供されて いません。

   .. warning::

      :func:`tmpnam` を使うと、symlink 攻撃に対して脆弱 になります; 代りに:func:`tmpfile`  (第:ref:`os-
      newstreams`節) を使うよう検討してください。

   利用できる環境: Unix、Windows。 この関数はおそらく Windows では使うべきではないでしょう; Micorosoft の
   :func:`tmpnam` 実装では、常に現在のドライブの ルートディレクトリ下のファイル名を生成しますが、これは一般的には
   テンポラリファイルを置く場所としてはひどい場所です  (アクセス権限によっては、この名前をつかってファイルを開くことすら できないかもしれません)。


.. data:: TMP_MAX

   :func:`tmpnam` がテンポラリ名を再利用し始めるまでに生成できる 一意な名前の最大数です。


.. function:: unlink(path)

   ファイル *path* を削除します。:func:`remove` と同じです;  :func:`unlink` の名前は伝統的な Unix の関数名です。
   利用できる環境: Macintosh、 Unix、Windows。


.. function:: utime(path, times)

   *path* で指定されたファイルに最終アクセス時刻および最終修正時刻 を設定します。*times* が ``None`` の場合、ファイルの最終
   アクセス時刻および最終更新時刻は現在の時刻になります。そうでない 場合、 *times* は 2 要素のタプルで、``(atime, mtime)``
   の形式をとらなくてはなりません。これらはそれぞれアクセス時刻および修正時刻 を設定するために使われます。 *path*
   にディレクトリを指定できるかどうかは、オペレーティングシステム がディレクトリをファイルの一種として実装しているかどうかに依存します (例えば、 Windows
   はそうではありません)。ここで設定した時刻の値は、オペレーティング システムがアクセス時刻や更新時刻を記録する際の精度によっては、後で:func:`stat`
   呼び出したときの値と同じにならないかも知れないので注意してください。 :func:`stat` も参照してください。

   .. versionchanged:: 2.0
      *times* として ``None`` をサポートするように しました.

   利用できる環境: Macintosh、 Unix、Windows。


.. function:: walk(top[, topdown\ ``=True`` [, onerror\ ``=None``]])

   .. index::
      single: directory; walking
      single: directory; traversal

   :func:`walk` は、ディレクトリツリー以下のファイル名を、ツリーを トップダウンとボトムアップの両方向に歩行することで生成します。 ディレクトリ
   *top* を根に持つディレクトリツリーに含まれる、 各ディレクトリ(*top* 自身を含む) から、タプル ``(dirpath,  dirnames,
   filenames)`` を生成します。

   *dirpath* は文字列で、ディレクトリへのパスです。*dirnames* は  *dirpath* 内のサブディレクトリ名のリスト (``'.'`` と
   ``'..'``  は除く）です。*filenames* は *dirpath* 内の非ディレクトリ・ファ
   イル名のリストです。このリスト内の名前には、ファイル名までのパスが含まれ ないことに、注意してください。*dirpath* 内のファイルやディレクトリへ の
   (*top* からたどった) フルパスを得るには、 ``os.path.join(dirpath, name)`` してください。

   オプション引数 *topdown* が真であるか、指定されなかった場合、各ディ レクトリからタプルを生成した後で、サブディレクトリからタプルを生成します。
   (ディレクトリはトップダウンで生成)。*topdown* が偽の場合、ディレクト リに対応するタプルは、そのディレクトリ以下の全てのサブディレクトリに対応
   するタプルの後で (ボトムアップで) 生成されます

   *topdown* が真のとき、呼び出し側は *dirnames* リストを、インプレ ースで (たとえば、:keyword:`del`
   やスライスを使った代入で) 変更でき、 :func:`walk` は*dirnames* に残っているサブディレクトリ内のみを
   再帰します。これにより、検索を省略したり、特定の訪問順序を強制したり、呼 び出し側が :func:`walk` を再開する前に、呼び出し側が作った、または
   名前を変更したディレクトリを、:func:`walk` に知らせたりすることがで きます。*topdown* が偽のときに *dirnames*
   を変更しても効果はあり ません。ボトムアップモードでは  *dirpath* 自身が生成される前に *dirnames*
   内のディレクトリの情報が生成されるからです。

   デフォルトでは、``os.listdir()`` 呼び出しから送出されたエラーは 無視されます。オプションの引数 *onerror* を指定するなら、
   この値は関数でなければなりません; この関数は単一の引数として、 :exc:`OSError` インスタンスを伴って呼び出されます。この関数では
   エラーを報告して歩行を続けたり、例外を送出して歩行を中断したり できます。ファイル名は例外オブジェクトの ``filename`` 属性として
   取得できることに注意してください。

   .. note::

      相対パスを渡した場合、:func:`walk` の回復の間でカレント作業ディレク トリを変更しないでください。:func:`walk`
      はカレントディレクトリを変 更しませんし、呼び出し側もカレントディレクトリを変更しないと仮定していま す。

   .. note::

      シンボリックリンクをサポートするシステムでは、サブディレクトリへのリンク が *dirnames* リストに含まれますが、:func:`walk`
      はそのリンクを たどりません (シンボリックリンクをたどると、無限ループに陥りやすくなりま す)。リンクされたディレクトリをたどるには、
      ``os.path.islink(path)`` でリンク先ディレクトリを確認し、各ディ レクトリに対して ``walk(path)``
      を実行するとよいでしょう。

   以下の例では、最初のディレクトリ以下にある各ディレクトリに含まれる、非ディレクトリファイルのバイト数を表示します。ただし、CVS
   サブディレクトリより下を見に行きません。 ::

      import os
      from os.path import join, getsize
      for root, dirs, files in os.walk('python/Lib/email'):
          print root, "consumes",
          print sum(getsize(join(root, name)) for name in files),
          print "bytes in", len(files), "non-directory files"
          if 'CVS' in dirs:
              dirs.remove('CVS')  # don't visit CVS directories

   次の例では、ツリーをボトムアップで歩行することが不可欠になります; :func:`rmdir` はディレクトリが空になる前に削除させないからです::

      # Delete everything reachable from the directory named in 'top',
      # assuming there are no symbolic links.
      # CAUTION:  This is dangerous!  For example, if top == '/', it
      # could delete all your disk files.
      import os
      for root, dirs, files in os.walk(top, topdown=False):
          for name in files:
              os.remove(os.path.join(root, name))
          for name in dirs:
              os.rmdir(os.path.join(root, name))

   .. versionadded:: 2.3


.. _os-process:

プロセス管理
------------

プロセスを生成したり管理するために、以下の関数を利用することができます。

様々な :func:`exec\*` 関数が、プロセス内にロードされた新たな プログラムに与えるための引数からなるリストをとります。どの場合でも、
新たなプログラムに渡されるリストの最初の引数は、ユーザがコマンドライン で入力する引数ではなく、プログラム自身の名前になります。 C
プログラマにとっては、これはプログラムの :cfunc:`main` に 渡される ``argv[0]`` になります。例えば、
``os.execv('/bin/echo', ['foo', 'bar'])`` は、標準出力に ``bar`` を出力します; ``foo``
は無視されたかのように見える ことでしょう。


.. function:: abort()

   :const:`SIGABRT` シグナルを現在のプロセスに対して生成します。 Unixでは、標準設定の動作はコアダンプの生成です; Windows では、
   プロセスは即座に終了コード ``3`` を返します。 :func:`signal.signal` を使って :const:`SIGABRT` に対する
   シグナルハンドラを設定しているプログラムは異なる挙動を示すので 注意してください。 利用できる環境: Macintosh、 Unix、 Windows。


.. function:: execl(path, arg0, arg1, ...)
              execle(path, arg0, arg1, ..., env)
              execlp(file, arg0, arg1, ...)
              execlpe(file, arg0, arg1, ..., env)
              execv(path, args)
              execve(path, args, env)
              execvp(file, args)
              execvpe(file, args, env)

   これらの関数はすべて、現在のプロセスを置き換える形で新たな プログラムを実行します; 現在のプロセスは戻り値を返しません。
   Unixでは、新たに実行される実行コードは現在のプロセス内に ロードされ、呼び出し側と同じプロセス ID を持つことになります。 エラーは
   :exc:`OSError` 例外として報告されます。

   ``'l'`` および ``'v'`` のついた :func:`exec\*`  関数は、コマンドライン引数をどのように渡すかが異なります。 ``'l'``
   型は、コードを書くときにパラメタ数が決まっている場合 に、おそらくもっとも簡単に利用できます。個々のパラメタは単に :func:`execl\*`
   関数の追加パラメタとなります。``'v'`` 型は、 パラメタの数が可変の時に便利で、リストかタプルの引数が *args*
   パラメタとして渡されます。どちらの場合も、子プロセスに渡す引数は 動作させようとしているコマンドの名前から始めるべきですが、これは 強制ではありません。

   末尾近くに ``'p'`` をもつ型 (:func:`execlp`、 :func:`execlpe`、 :func:`execvp`、 および
   :func:`execvpe`) は、プログラム *file* を探すために 環境変数 :envvar:`PATH` を利用します。環境変数が (次の段で述べる
   :func:`exec\*e` 型関数で) 置き換えられる場合、環境変数は :envvar:`PATH` を決定する上の情報源として使われます。
   その他の型、:func:`execl`、 :func:`execle`、 :func:`execv`、 および :func:`execve` では、実行
   コードを探すために :envvar:`PATH` を使いません。 *path* には適切に設定された絶対パスまたは相対パスが 入っていなくてはなりません。

   :func:`execle`、 :func:`execlpe`、 :func:`execve`、 および :func:`execvpe`
   (全て末尾に``'e'`` がついていること に注意してください) では、*env* パラメタは新たなプロセスで利用
   される環境変数を定義するためのマップ型でなくてはなりません; :func:`execl`、:func:`execlp`、 :func:`execv`、 および
   :func:`execvp` では、全て新たなプロセスは現在のプロセス の環境を引き継ぎます。 利用できる環境: Macintosh、 Unix、
   Windows。


.. function:: _exit(n)

   終了ステータス *n* でシステムを終了します。このとき クリーンアップハンドラの呼び出しや、標準入出力バッファの フラッシュなどは行いません。
   利用できる環境: Macintosh、 Unix、 Windows。

   .. note::

      システムを終了する標準的な方法は ``sys.exit(n)`` です。:func:`_exit` は通常、 :func:`fork` された後の子プロセス
      でのみ使われます。

以下の終了コードは必須ではありませんが :func:`_exit` と共に使うこと ができます。一般に、 メールサーバの外部コマンド配送プログラムのような、
Python で書かれたシステムプログラムに使います。

.. note::

   いくらかの違いがあって、これらの全てが全ての Unix プラットフォームで 使えるわけではありません。以下の定数は基礎にあるプラットフォームで
   定義されていれば定義されます。


.. data:: EX_OK

   エラーが起きなかったことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_USAGE

   誤った個数の引数が渡されたときなど、コマンドが間違って使われたことを表す 終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_DATAERR

   入力データが間違っていたことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_NOINPUT

   入力ファイルが存在しなかった、または、読み込み不可だったことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_NOUSER

   指定されたユーザが存在しなかったことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_NOHOST

   指定されたホストが存在しなかったことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_UNAVAILABLE

   要求されたサービスが利用できないことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_SOFTWARE

   内部ソフトウェアエラーが検出されたことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_OSERR

   fork できない、pipe の作成ができないなど、オペレーティング・システム・エ ラーが検出されたことを表す終了コード。 利用できる環境:
   Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_OSFILE

   システムファイルが存在しなかった、開けなかった、あるいはその他のエラーが 起きたことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_CANTCREAT

   ユーザには作成できない出力ファイルを指定したことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_IOERR

   ファイルの I/O を行っている途中にエラーが発生したときの終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_TEMPFAIL

   一時的な失敗が発生したことを表す終了コード。これは、再試行可能な操作の途 中に、ネットワークに接続できないというような、実際にはエラーではないかも
   知れないことを意味します。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_PROTOCOL

   プロトコル交換が不正、不適切、または理解不能なことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_NOPERM

   操作を行うために十分な許可がなかった（ファイルシステムの問題を除く）こと を表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_CONFIG

   設定エラーが起こったことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. data:: EX_NOTFOUND

   "an entry was not found" のようなことを表す終了コード。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. function:: fork()

   子プロセスを fork します。子プロセスでは ``0`` が返り、 親プロセスでは子プロセスの id が返ります。 利用できる環境: Macintosh、
   Unix。


.. function:: forkpty()

   子プロセスを fork します。このとき新しい擬似端末 (psheudo-terminal)  を子プロセスの制御端末として使います。 親プロセスでは
   ``(pid, fd)`` からなるペアが返り、*fd* は擬似端末の マスタ側 (master end) のファイル記述子となります。可搬性のある
   アプローチを取るためには、:mod:`pty` モジュールを利用してください。 利用できる環境: Macintosh、 いくつかの Unix系。


.. function:: kill(pid, sig)

   .. index::
      single: process; killing
      single: process; signalling

   プロセス *pid* にシグナル *sig* を送ります。 ホストプラットフォームで利用可能なシグナルを特定する定数は :mod:`signal`
   モジュールで定義されています。 利用できる環境: Macintosh、 Unix。


.. function:: killpg(pgid, sig)

   .. index::
      single: process; killing
      single: process; signalling

   プロセスグループ *pgid* にシグナル *sig* を送ります。 利用できる環境: Macintosh、 Unix。

   .. versionadded:: 2.3


.. function:: nice(increment)

   プロセスの "nice 値" に *increment* を加えます。新たな nice 値を返します。 利用できる環境: Macintosh、 Unix。


.. function:: plock(op)

   プログラムのセグメント (program segment) をメモリ内でロックします。 *op* (``<sys/lock.h>`` で定義されています)
   にはどのセグメントを ロックするかを指定します。 利用できる環境: Macintosh、 Unix。


.. function:: popen(...)
              popen2(...)
              popen3(...)
              popen4(...)
   :noindex:

   子プロセスを起動し、子プロセスとの通信のために開かれたパイプを返します。 これらの関数は :ref:`os-newstreams` 節で記述されています。


.. function:: spawnl(mode, path, ...)
              spawnle(mode, path, ..., env)
              spawnlp(mode, file, ...)
              spawnlpe(mode, file, ..., env)
              spawnv(mode, path, args)
              spawnve(mode, path, args, env)
              spawnvp(mode, file, args)
              spawnvpe(mode, file, args, env)

   新たなプロセス内でプログラム *path* を実行します。 *mode* が :const:`P_NOWAIT` の場合、この関数は 新たなプロセスのプロセス
   ID となります。; *mode* が :const:`P_WAIT` の場合、子プロセスが正常に終了するとその終了コードが返ります。そうでない
   場合にはプロセスを kill したシグナル *signal* に対して ``-signal`` が返ります。Windows では、プロセス ID は
   実際にはプロセスハンドル値になります。

   ``'l'`` および ``'v'`` のついた :func:`spawn\*`  関数は、コマンドライン引数をどのように渡すかが異なります。 ``'l'``
   型は、コードを書くときにパラメタ数が決まっている場合 に、おそらくもっとも簡単に利用できます。個々のパラメタは単に :func:`spawnl\*`
   関数の追加パラメタとなります。``'v'`` 型は、 パラメタの数が可変の時に便利で、リストかタプルの引数が *args*
   パラメタとして渡されます。どちらの場合も、子プロセスに渡す引数は 動作させようとしているコマンドの名前から始まらなくてはなりません。

   末尾近くに ``'p'`` をもつ型 (:func:`spawnlp`、 :func:`spawnlpe`、 :func:`spawnvp`、 および
   :func:`spawnvpe`) は、プログラム *file* を探すために 環境変数 :envvar:`PATH` を利用します。環境変数が
   (次の段で述べる :func:`spawn\*e` 型関数で) 置き換えられる場合、環境変数は :envvar:`PATH`
   を決定する上の情報源として使われます。 その他の型、:func:`spawnl`、 :func:`spawnle`、 :func:`spawnv`、 および
   :func:`spawnve` では、実行 コードを探すために :envvar:`PATH` を使いません。 *path*
   には適切に設定された絶対パスまたは相対パスが 入っていなくてはなりません。

   :func:`spawnle`、 :func:`spawnlpe`、 :func:`spawnve`、 および :func:`spawnvpe`
   (全て末尾に``'e'`` がついていること に注意してください) では、*env* パラメタは新たなプロセスで利用
   される環境変数を定義するためのマップ型でなくてはなりません; :func:`spawnl`、:func:`spawnlp`、 :func:`spawnv`、
   および :func:`spawnvp` では、全て新たなプロセスは現在のプロセス の環境を引き継ぎます。

   例えば、以下の :func:`spawnlp` および :func:`spawnvpe`  呼び出し::

      import os
      os.spawnlp(os.P_WAIT, 'cp', 'cp', 'index.html', '/dev/null')

      L = ['cp', 'index.html', '/dev/null']
      os.spawnvpe(os.P_WAIT, 'cp', L, os.environ)

   は等価です。利用できる環境: Unix、Windows。

   :func:`spawnlp`、:func:`spawnlpe`、 :func:`spawnvp`  および :func:`spawnvpe` は
   Windows では利用できません。

   .. versionadded:: 1.6


.. data:: P_NOWAIT
          P_NOWAITO

   :func:`spawn\*` 関数ファミリに対する *mode* パラメタ として取れる値です。この値のいずれかを *mode* として与えた場合、
   :func:`spawn\*` 関数は新たなプロセスが生成されるとすぐに、 プロセスの ID を戻り値として返ります。 利用できる環境: Macintosh、
   Unix、Windows。

   .. versionadded:: 1.6


.. data:: P_WAIT

   :func:`spawn\*` 関数ファミリに対する *mode* パラメタ として取れる値です。この値を *mode* として与えた場合、
   :func:`spawn\*` 関数は新たなプロセスを起動して完了するまで返らず、 プロセスがうまく終了した場合には終了コードを、シグナルによってプロセス が
   kill された場合には ``-signal`` を返します。 利用できる環境: Macintosh、 Unix、Windows。

   .. versionadded:: 1.6


.. data:: P_DETACH
          P_OVERLAY

   :func:`spawn\*` 関数ファミリに対する *mode* パラメタ として取れる値です。これらの値は上の値よりもやや可搬性において劣って
   います。:const:`P_DETACH` は :const:`P_NOWAIT` に似ていますが、 新たなプロセスは呼び出しプロセスのコンソールから切り離され
   (detach) ます。:const:`P_OVERLAY` が使われた場合、現在のプロセスは 置き換えられます; 従って:func:`spawn\*`
   は返りません。 利用できる環境: Windows。

   .. versionadded:: 1.6


.. function:: startfile(path[, operation])

   ファイルを関連付けられたアプリケーションを使って「スタート」します。

   *operation* が指定されないかまたは ``'open'`` であるとき、 この動作は、 Windows の Explorer
   上でのファイルをダブルクリックや、 コマンドプロンプト (interactive command shell) 上での ファイル名を
   :program:`start` 命令の引数としての実行と同様です: ファイルは拡張子が関連付けされているアプリケーション (が存在する場合)
   を使って開かれます。

   他の *operation* が与えられる場合、それはファイルに対して何がなされるべきかを 表す "command verb" (コマンドを表す動詞)
   でなければなりません。 Microsoft が文書化している動詞は、``'print'`` と ``'edit'`` (ファイルに対して) および
   ``'explore'`` と ``'find'`` (ディレクトリに対して) です。

   :func:`startfile` は関連付けされたアプリケーションが起動すると 同時に返ります。アプリケーションが閉じるまで待機させるためのオプション
   はなく、アプリケーションの終了状態を取得する方法もありません。 *path* 引数は現在のディレクトリからの相対で表します。
   絶対パスを利用したいなら、最初の文字はスラッシュ  (``'/'``) ではないので注意してください; もし最初の文字がスラッシュ なら、システムの背後にある
   Win32 :cfunc:`ShellExecute` 関数は 動作しません。:func:`os.path.normpath` 関数を使って、Win32 用に
   正しくコード化されたパスになるようにしてください。 利用できる環境: Windows。

   .. versionadded:: 2.0

   .. versionadded:: 2.5
      *operation* パラメータ.


.. function:: system(command)

   サブシェル内でコマンド (文字列) を実行します。この関数は 標準 C 関数 :cfunc:`system` を使って実装されており、
   :cfunc:`system` と同じ制限があります。 ``posix.environ``、 ``sys.stdin`` 等に対する変更を行っても、
   実行されるコマンドの環境には反映されません。

   Unixでは、戻り値はプロセスの終了ステータスで、:func:`wait`  で定義されている書式にコード化されています。 POSIX は
   :cfunc:`system` 関数の戻り値の意味について定義して いないので、Python の :func:`system` における戻り値はシステム依存と
   なることに注意してください。

   Windows では、戻り値は *command* を実行した後にシステムシェルから 返される値で、Windows の環境変数
   :envvar:`COMSPEC` となります: :program:`command.com` ベースのシステム (Windows 95, 98 および ME)
   では、この値は常に ``0`` です; :program:`cmd.exe` ベースのシステム (Windows NT, 2000 および XP)
   では、この値は実行したコマンドの終了 ステータスです; ネイティブでないシェルを使っているシステムについては、
   使っているシェルのドキュメントを参照してください。

   利用できる環境: Macintosh、 Unix、 Windows。


.. function:: times()

   (プロセスまたはその他の) 積算時間を秒で表す浮動小数点数からなる、 5 要素のタプルを返します。タプルの要素は、ユーザ時間 (user time)、
   システム時間 (system time)、子プロセスのユーザ時間、子プロセスの システム時間、そして過去のある固定時点からの経過時間で、この順に
   並んでいます。Unix マニュアルページ :manpage:`times(2)` または 対応する Windows プラットフォーム API
   ドキュメントを参照してください。 利用できる環境: Macintosh、Unix、Windows。


.. function:: wait()

   子プロセスの実行完了を待機し、子プロセスの pid と終了コードインジケータ --- 16 ビットの数で、下位バイトがプロセスを kill
   したシグナル番号、上位バイト が終了ステータス (シグナル番号がゼロの場合) --- の入ったタプルを 返します;
   コアダンプファイルが生成された場合、下位バイトの最上桁ビットが 立てられます。 利用できる環境: Macintosh、Unix。


.. function:: waitpid(pid, options)

   プロセス id *pid* で与えられた子プロセスの完了を待機し、 子プロセスのプロセス id と(:func:`wait` と同様にコード化された)
   終了ステータスインジケータからなるタプルを返します。 この関数の動作は *options* によって影響されます。通常の操作では ``0`` にします。
   利用できる環境: Unix。

   *pid* が ``0`` よりも大きい場合、 :func:`waitpid` は特定のプロセスのステータス情報を要求します。*pid* が ``0``
   の場合、現在のプロセスグループ内の任意の子プロセスの状態 に対する要求です。*pid* が ``-1`` の場合、現在のプロセス
   の任意の子プロセスに対する要求です。*pid* が ``-1`` よりも 小さい場合、プロセスグループ ``-pid`` (すなわち *pid* の 絶対値)
   内の任意のプロセスに対する要求です。


.. function:: wait3([options])

   :func:`waitpid` に似ていますが、プロセス id を引数に取らず、 子プロセス
   id、終了ステータスインジケータ、リソース使用情報の3要素からなるタプルを返します。 リソース使用情報の詳しい情報は :mod:`resource`.\
   :func:`getrusage` を参照してください。 *options* は :func:`waitpid` および :func:`wait4`
   と同様です。 利用できる環境: Unix。

   .. versionadded:: 2.5


.. function:: wait4(pid, options)

   :func:`waitpid` に似ていますが、 子プロセス id、終了ステータスインジケータ、リソース使用情報の3要素からなるタプルを返します。
   リソース使用情報の詳しい情報は :mod:`resource`.\ :func:`getrusage` を参照してください。 :func:`wait4`
   の引数は :func:`waitpid` に与えられるものと同じです。 利用できる環境: Unix。

   .. versionadded:: 2.5


.. data:: WNOHANG

   子プロセス状態がすぐに取得できなかった場合に直ちに終了する ようにするための :func:`waitpid` のオプションです。 この場合、関数は ``(0,
   0)`` を返します。 利用できる環境: Macintosh、Unix。


.. data:: WCONTINUED

   このオプションによって子プロセスは前回状態が報告された後にジョブ制御による停止状態から実行を継続された場合に報告されるようになります。 利用できる環境:
   ある種の Unix システム。

   .. versionadded:: 2.3


.. data:: WUNTRACED

   このオプションによって子プロセスは停止されていながら停止されてから状態が報告されていない場合に報告されるようになります。 利用できる環境: Macintosh、
   Unix。

   .. versionadded:: 2.3

以下の関数は:func:`system`、 :func:`wait`、 あるいは:func:`waitpid` が返すプロセス状態コード
を引数にとります。これらの関数はプロセスの配置を決めるために 利用することができます。


.. function:: WCOREDUMP(status)

   プロセスに対してコアダンプが生成されていた場合には ``True`` を、 それ以外の場合は ``False`` を返します。 利用できる環境:
   Macintosh、 Unix。

   .. versionadded:: 2.3


.. function:: WIFCONTINUED(status)

   プロセスがジョブ制御による停止状態から実行を継続された (continue) 場合に ``True`` を、 それ以外の場合は ``False`` を返します。
   利用できる環境: Unix。

   .. versionadded:: 2.3


.. function:: WIFSTOPPED(status)

   プロセスが停止された (stop) 場合に ``True`` を、 それ以外の場合は ``False`` を返します。 利用できる環境: Unix。


.. function:: WIFSIGNALED(status)

   プロセスがシグナルによって終了した (exit) 場合に ``True`` を、 それ以外の場合は ``False`` を返します。 利用できる環境:
   Macintosh、 Unix。


.. function:: WIFEXITED(status)

   プロセスが :manpage:`exit(2)` システムコールで終了した場合に ``True`` を、 それ以外の場合は ``False`` を返します。
   利用できる環境: Macintosh、Unix。


.. function:: WEXITSTATUS(status)

   ``WIFEXITED(status)`` が真の場合、:manpage:`exit(2)` システム コールに渡された整数パラメタを返します。そうでない場合、
   返される値には意味がありません。 利用できる環境: Macintosh、Unix。


.. function:: WSTOPSIG(status)

   プロセスを停止させたシグナル番号を返します。 利用できる環境: Macintosh、Unix。


.. function:: WTERMSIG(status)

   プロセスを終了させたシグナル番号を返します。 利用できる環境: Macintosh、Unix


.. _os-path:

雑多なシステム情報
------------------


.. function:: confstr(name)

   文字列形式によるシステム設定値 (system configuration value)を返します。 *name* には取得したい設定名を指定します; この値は
   定義済みのシステム値名を表す文字列にすることができます; 名前は 多くの標準 (POSIX.1、 Unix 95、 Unix 98 その他)
   で定義されています。 ホストオペレーティングシステムの関知する名前は ``confstr_names`` 辞書のキーとして与えられています。
   このマップ型オブジェクトに入っていない設定 変数については、 *name* に整数を渡してもかまいません。 利用できる環境: Macintosh、Unix。

   *name* に指定された設定値が定義されていない場合、``None`` を返します。

   もし *name* が文字列でかつ不明である場合、 :exc:`ValueError`  を送出します。*name*
   の指定値がホストシステムでサポートされておらず、 ``confstr_names`` にも入っていない場合、:const:`errno.EINVAL`
   をエラー番号として :exc:`OSError` を送出します。


.. data:: confstr_names

   :func:`confstr` が受理する名前を、ホストオペレーティングシステムで 定義されている整数値に対応付けている辞書です。 この辞書はシステムでどの
   設定名が定義されているかを決定するために利用できます。 利用できる環境: Macintosh、Unix。


.. function:: getloadavg()

   過去 1 分、5 分、15分間で、システムで走っているキューの平均プロセス数を 返します。平均負荷が得られない場合には :exc:`OSError`
   を送出します。

   .. versionadded:: 2.3


.. function:: sysconf(name)

   整数値のシステム設定値を返します。 *name* で指定された設定値が定義されていない場合、``-1``  が返されます。*name*
   に関するコメントとしては、:func:`confstr` で述べた内容が同様に当てはまります; 既知の設定名についての情報を 与える辞書は
   ``sysconf_names`` で与えられています。 利用できる環境: Macintosh、Unix。


.. data:: sysconf_names

   :func:`sysconf` が受理する名前を、ホストオペレーティングシステムで 定義されている整数値に対応付けている辞書です。
   この辞書はシステムでどの設定名が定義されているかを決定するために 利用できます。 利用できる環境: Macintosh、Unix。

以下のデータ値はパス名編集操作をサポートするために利用されます。 これらの値は全てのプラットフォームで定義されています。

パス名に対する高レベルの操作は :mod:`os.path` モジュールで 定義されています。


.. data:: curdir

   現在のディレクトリ参照するためにオペレーティングシステムで使われる 文字列定数です。 例: POSIX では ``'.'`` 、Mac OS 9
   では``':'`` 。 :mod:`os.path` からも利用できます。


.. data:: pardir

   親ディレクトリを参照するためにオペレーティングシステムで使われる 文字列定数です。 例: POSIX では ``'..'`` 、Mac OS 9
   では``'::'`` 。 :mod:`os.path` からも利用できます。


.. data:: sep

   パス名を要素に分割するためにオペレーティングシステムで利用されている 文字で、例えば POSIX では ``'/'`` で、Mac OS 9 では
   ``':'`` です。しかし、このことを知っているだけではパス名を 解析したり、パス名同士を結合したりするには不十分です ---  こうした操作には
   :func:`os.path.split` や :func:`os.path.join`  を使ってください--- が、たまに便利なこともあります。
   :mod:`os.path` からも利用できます。


.. data:: altsep

   文字パス名を要素に分割する際にオペレーティングシステムで利用されるもう 一つの文字で、分割文字が一つしかない場合には ``None`` になります。 この値は
   ``sep`` がバックスラッシュとなっている DOS や Windows  システムでは ``'/'`` に設定されています。 :mod:`os.path`
   からも利用できます。


.. data:: extsep

   ベースのファイル名と拡張子を分ける文字。 たとえば、:file:`os.py` では ``'.'`` です。 :mod:`os.path` からも利用できます。

   .. versionadded:: 2.2


.. data:: pathsep

   (:envvar:`PATH` のような) サーチパス内の要素を分割するために オペレーティングシステムが慣習的に用いる文字で、POSIX における
   ``':'`` や DOS および Windows における ``';'`` に相当します。 :mod:`os.path` からも利用できます。


.. data:: defpath

   :func:`exec\*p\*` や :func:`spawn\*p\*` において、環境変数辞書内に ``'PATH'``
   キーがない場合に使われる標準設定のサーチパスです。 :mod:`os.path` からも利用できます。


.. data:: linesep

   現在のプラットフォーム上で行を分割 (あるいは終端) するために用いられ ている文字列です。この値は例えば POSIX での``'\n'`` や Mac OS
   での ``'\r'`` のように、単一の文字にもなりますし、例えば DOS や Windows での ``'\r\n'`` のように複数の文字列にもなります。


.. data:: devnull

   ヌルデバイス (null device) のファイルパスです。例えばPOSIX では ``'/dev/null'``、Mac OS 9
   では``'Dev:Nul'`` です。 この値は:mod:`os.path` からも利用できます。

   .. versionadded:: 2.4


.. _os-miscfunc:

雑多な関数
----------


.. function:: urandom(n)

   暗号に関する用途に適した*n* バイトからなるランダムな文字列を返します。

   この関数は OS 固有の乱数発生源からランダムなバイト列を生成して返します。 この関数の返すデータは暗号を用いたアプリケーションで十分利用できる程度に
   予測不能ですが、実際のクオリティは OS の実装によって異なります。 Unix系のシステムでは :file:`/dev/urandom` への問い合わせを行い、
   Windows では :cfunc:`CryptGenRandom` を使います。乱数発生源
   が見つからない場合、:exc:`NotImplementedError` を送出します。

   .. versionadded:: 2.4

