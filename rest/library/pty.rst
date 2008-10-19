
:mod:`pty` --- 擬似端末ユーティリティ
==========================

.. module:: pty
   :platform: IRIX, Linux
   :synopsis: SGIとLinux用の擬似端末を制御する
.. moduleauthor:: Steen Lumholt
.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>


.. % \modulesynopsis{Pseudo-Terminal Handling for SGI and Linux.}

:mod:`pty`モジュールは擬似端末(他のプロセスを実行してその制御をしてい る端末をプログラムで読み書きする)を制御する操作を定義しています。

.. % The \module{pty} module defines operations for handling the
.. % pseudo-terminal concept: starting another process and being able to
.. % write to and read from its controlling terminal programmatically.

擬似端末の制御はプラットフォームに強く依存するので、SGIとLinux用のコード
しか存在していません。(Linux用のコードは他のプラットフォームでも動作するよ うに作られていますがテストされていません。)

.. % Because pseudo-terminal handling is highly platform dependant, there
.. % is code to do it only for SGI and Linux. (The Linux code is supposed
.. % to work on other platforms, but hasn't been tested yet.)

:mod:`pty`モジュールでは以下の関数を定義しています:

.. % The \module{pty} module defines the following functions:


.. function:: fork()

   forkします。子プロセスの制御端末を擬似端末に接続します。 返り値は``(pid, fd)``です。子プロセスは*pid*として0、
   、*fd*として*invalid* をそれぞれ受けとります。親プロセスは *pid*として子プロセスのPID、*fd*として子プロセスの制御端末(子プ
   ロセスの標準入出力に接続されている)のファイルディスクリプタを受けとります。

   .. % Fork. Connect the child's controlling terminal to a pseudo-terminal.
   .. % Return value is \code{(\var{pid}, \var{fd})}. Note that the child
   .. % gets \var{pid} 0, and the \var{fd} is \emph{invalid}. The parent's
   .. % return value is the \var{pid} of the child, and \var{fd} is a file
   .. % descriptor connected to the child's controlling terminal (and also
   .. % to the child's standard input and output).


.. function:: openpty()

   新しい擬似端末のペアを開きます。 利用できるなら:func:`os.openpty`を使い、 利用できなければSGIと一般的なUnixシステム用の
   エミュレーションコードを使います。 マスター、スレーブそれぞれのためのファイルディスクリプタ、 ``(master, slave)``のタプルを返します。

   .. % Open a new pseudo-terminal pair, using \function{os.openpty()} if
   .. % possible, or emulation code for SGI and generic \UNIX{} systems.
   .. % Return a pair of file descriptors \code{(\var{master}, \var{slave})},
   .. % for the master and the slave end, respectively.


.. function:: spawn(argv[, master_read[, stdin_read]])

   プロセスを生成して制御端末を現在のプロセスの標準入出力に接続します。 これは制御端末を読もうとするプログラムをごまかすために利用されます。

   .. % Spawn a process, and connect its controlling terminal with the current
   .. % process's standard io. This is often used to baffle programs which
   .. % insist on reading from the controlling terminal.

   *master_read*と*stdin_read*にはファイルディスクリプタから読み込む
   関数を指定してください。デフォルトでは呼ばれるたびに1024バイトずつ読み 込もうとします。

   .. % The functions \var{master_read} and \var{stdin_read} should be
   .. % functions which read from a file-descriptor. The defaults try to read
   .. % 1024 bytes each time they are called.

