
:mod:`subprocess` --- サブプロセス管理
==============================

.. module:: subprocess
   :synopsis: サブプロセス管理
.. moduleauthor:: Peter Åstrand <astrand@lysator.liu.se>
.. sectionauthor:: Peter Åstrand <astrand@lysator.liu.se>


.. versionadded:: 2.4

:mod:`subprocess` モジュールは、新しくプロセスを開始したり、 それらの標準入出力/エラー出力に対してパイプで接続したり、
それらの終了ステータスを取得したりします。このモジュールは以下のような 古いいくつかのモジュールを置き換えることを目的としています:

.. % XXX このモジュールに popen2 とそのコマンド・セクションの
.. % ポインタを追加すること。

::

   os.system
   os.spawn*
   os.popen*
   popen2.*
   commands.*

これらのモジュールや関数の代わりに、:mod:`subprocess` モジュールを どのように使うかについては以下の節で説明します。


subprocess モジュールを使う
-------------------

このモジュールでは :class:`Popen` と呼ばれるクラスを定義しています:


.. class:: Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)

   各引数の説明は以下のとおりです:

   *args* は文字列か、あるいはプログラムへの引数のシーケンスである 必要があります。実行するプログラムは通常 args シーケンスあるいは文字列の
   最初の要素ですが、executable 引数を使うことにより明示的に指定することもできます。

   Unix で *shell=False* の場合 (デフォルト): この場合、 Popen クラスは子プログラムを実行するのに
   :meth:`os.execvp` を使います。 *args* は通常シーケンスでなければなりません。文字列の場合は ひとつだけの文字列要素 (=
   実行するプログラム名) をもったシーケンスとして 扱われます。

   Unix で *shell=True* の場合: args が文字列の場合、これは シェルを介して実行されるコマンドライン文字列を指定します。*args* が
   シーケンスの場合、その最初の要素はコマンドライン文字列となり、 それ以降の要素はすべてシェルへの追加の引数として扱われます。

   Windows の場合: :class:`Popen` クラスは子プログラムを実行するのに 文字列の扱える CreateProcess()
   を使います。*args* が シーケンスの場合、これは :meth:`list2cmdline` メソッドをつかって コマンドライン文字列に変換されます。注意:
   すべての MS Windows アプリケーションがコマンドライン引数を同じやりかたで 解釈するとは限りません。:meth:`list2cmdline` は MS
   C ランタイムと 同じやりかたで文字列を解釈するアプリケーション用に設計されています。

   *bufsize* は、もしこれが与えられた場合、ビルトインの open() 関数の該当する引数と同じ意味をもちます: :const:`0`
   はバッファされないことを意味し、 :const:`1` は行ごとにバッファされることを、それ以外の正の値は (ほぼ)
   その大きさのバッファが使われることを意味します。 負の *bufsize* はシステムのデフォルト値が使われることを意味し、
   通常これはバッファがすべて有効となります。*bufsize* のデフォルト値は :const:`0` (バッファされない) です。

   *executable* 引数には実行するプログラムを指定します。 これはほとんど必要ありません: ふつう、実行するプログラムは *args*
   引数で指定されるからです。``shell=True`` の場合、 *executable* 引数は使用するシェルを指定します。 Unix
   では、デフォルトのシェルは :file:`/bin/sh` です。Windows では、デフォルトのシェルは :envvar:`COMSPEC`
   環境変数で指定されます。

   *stdin*、 *stdout* および *stderr* には、 実行するプログラムの標準入力、標準出力、および標準エラー出力の
   ファイルハンドルをそれぞれ指定します。とりうる値は ``PIPE`` 、既存のファイル記述子 (正の整数) 、 既存のファイルオブジェクト、そして
   ``None`` です。 ``PIPE`` を指定すると新しいパイプが子プロセスに向けて作られます。 ``None``
   を指定するとリダイレクトは起こりません。子プロセスの ファイルハンドルはすべて親から受け継がれます。 加えて、*stderr* を ``STDOUT``
   にすると、アプリケーションの stderr からの出力は stdout と同じファイルハンドルに出力されます。

   *preexec_fn* に callable オブジェクトが指定されている場合、 このオブジェクトは子プロセスが起動されてから、プログラムが exec
   される直前に呼ばれます。(Unixのみ)

   *close_fds* が真の場合、子プロセスが実行される前に :const:`0`、 :const:`1` および :const:`2`
   をのぞくすべてのファイル記述子が 閉じられます。(Unixのみ)

   *shell* が :const:`True` の場合、 指定されたコマンドはシェルを介して実行されます。

   *cwd* が ``None`` 以外の場合、子プロセスの カレントディレクトリが実行される前に *cwd* に変更されます。
   このディレクトリは実行ファイルを探す段階では考慮されませんので、 プログラムのパスを *cwd* に対する相対パスで指定することはできない、
   ということに注意してください。

   *env* が ``None`` 以外の場合、これは新しいプロセスでの 環境変数を定義します。

   *universal_newlines* が :const:`True` の場合、 stdout および stderr
   のファイルオブジェクトはテキストファイルとして open されますが、行の終端は Unix形式の行末 ``'\n'`` か、 Macintosh 形式の行末
   ``'\r'`` か、あるいは Windows 形式の行末 ``'\r\n'`` のいずれも許されます。これらすべての外部表現は Python プログラムには
   ``'\n'`` として認識されます。

   .. note::

      この機能は Python に universal newline がサポートされている場合 (デフォルト) にのみ 有効です。また、
      :attr:`stdout`, :attr:`stdin` および :attr:`stderr` の ファイルオブジェクトの newlines 属性は
      communicate() メソッドでは 更新されません。

   *startupinfo* および *creationflags* が与えられた場合、 これらは内部で呼びだされる CreateProcess()
   関数に渡されます。 これらはメインウインドウの形状や新しいプロセスの優先度などを 指定することができます。  (Windows のみ)


便利な関数
^^^^^

このモジュールは二つのショートカット関数も定義しています:


.. function:: call(*popenargs, **kwargs)

   コマンドを指定された引数で実行し、そのコマンドが完了するのを待って、 :attr:`returncode` 属性を返します。

   この引数は Popen コンストラクタの引数と同じです。 使用例::

      retcode = call(["ls", "-l"])


.. function:: check_call(*popenargs, **kwargs)

   コマンドを引数付きで実行します。コマンドが完了するのを待ちます。終了コードがゼロ ならば終わりますが、そうでなければ
   :exc:`CalledProcessError` 例外を送出します。 :exc:`CalledProcessError` オブジェクトにはリターンコードが
   :attr:`returncode` 属性として収められています。

   引数は Popen のコンストラクタと一緒です。使用例::

      check_call(["ls", "-l"])


例外
^^

子プロセス内で raise した例外は、新しいプログラムが実行される前であれば、 親プロセスでも raise されます。さらに、この例外オブジェクトには
:attr:`child_traceback` という属性が追加されており、これには 子プロセスの視点からの traceback 情報が格納されています。

もっとも一般的に起こる例外は :exc:`OSError` です。 これは、たとえば存在しないファイルを実行しようとしたときなどに
発生します。アプリケーションは :exc:`OSError` 例外には あらかじめ準備しておく必要があります。

不適当な引数で :class:`Popen` が呼ばれた場合は、 :exc:`ValueError` が発生します。

:func:`check_call` は もし呼び出されたプロセスがゼロでないリターンコードを返したならば :exc:`CalledProcessError`
を送出します。


セキュリティ
^^^^^^

ほかの popen 関数とは異なり、この実装は決して暗黙のうちに /bin/sh を 実行しません。これはシェルのメタ文字をふくむすべての文字が
安全に子プロセスに渡されるということを意味しています。


Popen オブジェクト
------------

:class:`Popen` クラスのインスタンスには、以下のようなメソッドがあります:


.. method:: Popen.poll()

   子プロセスが終了しているかどうかを検査します。 returncode 属性を返します。


.. method:: Popen.wait()

   子プロセスが終了するまで待ちます。 returncode 属性を返します。


.. method:: Popen.communicate(input=None)

   プロセスと通信します: end-of-file に到達するまで データを stdin に送信し、stdout および stderr からデータを受信します。
   プロセスが終了するまで待ちます。オプション引数 *input* には 子プロセスに送られる文字列か、あるいはデータを送らない場合は ``None``
   を指定します。

   communicate() はタプル (stdout, stderr) を返します。

   .. note::

      受信したデータはメモリ中にバッファされます。 そのため、返されるデータが大きいかあるいは制限がないような場合は このメソッドを使うべきではありません。

以下の属性も利用できます:


.. attribute:: Popen.stdin

   *stdin* 引数が ``PIPE`` の場合、この属性には 子プロセスの入力に使われるファイルオブジェクトになります。 そうでない場合は ``None``
   です。


.. attribute:: Popen.stdout

   *stdout* 引数が ``PIPE`` の場合、この属性には 子プロセスの出力に使われるファイルオブジェクトになります。 そうでない場合は ``None``
   です。


.. attribute:: Popen.stderr

   *stderr* 引数が ``PIPE`` の場合、この属性には 子プロセスのエラー出力に使われるファイルオブジェクトになります。 そうでない場合は
   ``None`` です。


.. attribute:: Popen.pid

   子プロセスのプロセス ID が入ります。


.. attribute:: Popen.returncode

   子プロセスの終了ステータスが入ります。 ``None`` はまだその子プロセスが終了していないことを示し、 負の値 -N は子プロセスがシグナル N
   により中止させられたことを示します (Unix のみ)。


古い関数を subprocess モジュールで置き換える
----------------------------

以下、この節では、"a ==> b" と書かれているものは a の代替として b が使えるということを表します。

.. note::

   この節で紹介されている関数はすべて、実行するプログラムが 見つからないときは (いくぶん) 静かに終了します。このモジュールは :exc:`OSError`
   例外を発生させます。

以下の例では、 subprocess モジュールは "from subprocess import \*" で インポートされたと仮定しています。


/bin/sh シェルのバッククォートを置き換える
^^^^^^^^^^^^^^^^^^^^^^^^^

::

   output=`mycmd myarg`
   ==>
   output = Popen(["mycmd", "myarg"], stdout=PIPE).communicate()[0]


シェルのパイプラインを置き換える
^^^^^^^^^^^^^^^^

::

   output=`dmesg | grep hda`
   ==>
   p1 = Popen(["dmesg"], stdout=PIPE)
   p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
   output = p2.communicate()[0]


os.system() を置き換える
^^^^^^^^^^^^^^^^^^

::

   sts = os.system("mycmd" + " myarg")
   ==>
   p = Popen("mycmd" + " myarg", shell=True)
   sts = os.waitpid(p.pid, 0)

注意:

* このプログラムは普通シェル経由で呼び出す必要はありません。

* 終了状態を見るよりも :attr:`returncode` 属性を見るほうが簡単です。

より現実的な例ではこうなるでしょう::

   try:
       retcode = call("mycmd" + " myarg", shell=True)
       if retcode < 0:
           print >>sys.stderr, "子プロセスがシグナルによって中止されました", -retcode
       else:
           print >>sys.stderr, "子プロセスが終了コードを返しました", retcode
   except OSError, e:
       print >>sys.stderr, "実行に失敗しました:", e


os.spawn\* を置き換える
^^^^^^^^^^^^^^^^^

P_NOWAIT の例::

   pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
   ==>
   pid = Popen(["/bin/mycmd", "myarg"]).pid

P_WAIT の例::

   retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
   ==>
   retcode = call(["/bin/mycmd", "myarg"])

シーケンスを使った例::

   os.spawnvp(os.P_NOWAIT, path, args)
   ==>
   Popen([path] + args[1:])

環境変数を使った例::

   os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)
   ==>
   Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})


os.popen\* を置き換える
^^^^^^^^^^^^^^^^^

::

   pipe = os.popen(cmd, mode='r', bufsize)
   ==>
   pipe = Popen(cmd, shell=True, bufsize=bufsize, stdout=PIPE).stdout

::

   pipe = os.popen(cmd, mode='w', bufsize)
   ==>
   pipe = Popen(cmd, shell=True, bufsize=bufsize, stdin=PIPE).stdin

::

   (child_stdin, child_stdout) = os.popen2(cmd, mode, bufsize)
   ==>
   p = Popen(cmd, shell=True, bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, close_fds=True)
   (child_stdin, child_stdout) = (p.stdin, p.stdout)

::

   (child_stdin,
    child_stdout,
    child_stderr) = os.popen3(cmd, mode, bufsize)
   ==>
   p = Popen(cmd, shell=True, bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
   (child_stdin,
    child_stdout,
    child_stderr) = (p.stdin, p.stdout, p.stderr)

::

   (child_stdin, child_stdout_and_stderr) = os.popen4(cmd, mode, bufsize)
   ==>
   p = Popen(cmd, shell=True, bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
   (child_stdin, child_stdout_and_stderr) = (p.stdin, p.stdout)


popen2.\* を置き換える
^^^^^^^^^^^^^^^^

.. note::

   popen2 に対するコマンド引数が文字列の場合、 そのコマンドは /bin/sh 経由で実行されます。いっぽうこれが
   リストの場合、そのコマンドは直接実行されます。

::

   (child_stdout, child_stdin) = popen2.popen2("somestring", bufsize, mode)
   ==>
   p = Popen(["somestring"], shell=True, bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, close_fds=True)
   (child_stdout, child_stdin) = (p.stdout, p.stdin)

::

   (child_stdout, child_stdin) = popen2.popen2(["mycmd", "myarg"], bufsize, mode)
   ==>
   p = Popen(["mycmd", "myarg"], bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, close_fds=True)
   (child_stdout, child_stdin) = (p.stdout, p.stdin)

popen2.Popen3 および popen2.Popen4 は基本的には subprocess.Popen と同様です。 ただし、違う点は:

* subprocess.Popen は実行できなかった場合に例外を発生させます。

* *capturestderr* 引数は *stderr* 引数に代わりました。

* stdin=PIPE および stdout=PIPE を指定する必要があります。

* popen2 はデフォルトですべてのファイル記述子を閉じますが、subprocess.Popen では 明示的に close_fds=True
  を指定する必要があります。

