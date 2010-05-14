
:mod:`popen2` --- アクセス可能な I/O ストリームを持つ子プロセス生成
===================================================================

.. module:: popen2
   :platform: Unix, Windows
   :synopsis: アクセス可能な I/O ストリームを持つ子プロセス生成。
.. sectionauthor:: Drew Csillag <drew_csillag@geocities.com>


このモジュールにより、Unix および Windows でプロセスを起動し、 その入力／出力／エラー出力パイプに接続し、そのリターンコード
を取得することができます。

Python 2.0 から、この機能は :mod:`os` モジュールにある 関数を使って得ることができるので注意してください。 :mod:`os`
にある関数はこのモジュールにおけるファクトリ関数 と同じ名前を持ちますが、戻り値に関する取り決めは :mod:`os` の関数の方がより直感的です。

このモジュールで提供されている第一のインタフェースは 3 つの ファクトリ関数です。これらの関数のいずれも、*bufsize* を 指定した場合、 I/O
パイプのバッファサイズを決定します。 *mode* を指定する場合、文字列``'b'`` または ``'t'``  でなければなりません; Windows
では、ファイルオブジェクトを バイナリあるいはテキストモードのどちらで開くかを決めなければ なりません。*mode* の標準の値は ``'t'`` です。

Unixでは*cmd*はシーケンスでもよく、その場合には (:func:`os.spawnv`のように)引数はプログラムシェルを経由せず直接渡 されます。
*cmd*が文字列の場合、(:func:`os.system`のように)シェルに渡されます。

子プロセスからのリターンコードを取得するには、:class:`Popen3` および :class:`Popen4` クラスの :meth:`poll`
あるいは :meth:`wait` メソッドを使うしかありません; これらの機能は Unixでしか利用できません。この情報は :func:`popen2`、
:func:`popen3`、および :func:`popen4` 関数、 あるいは :mod:`os` モジュールにおける同等の関数の
使用によっては得ることができません。 (:mod:`os`モジュールの関数から返されるタプルは:mod:`popen2`モ
ジュールの関数から返されるものとは違う順序です。)


.. function:: popen2(cmd[, bufsize[, mode]])

   *cmd* をサブプロセスとして実行します。ファイルオブジェクト ``(child_stdout, child_stdin)`` を返します。


.. function:: popen3(cmd[, bufsize[, mode]])

   *cmd* をサブプロセスとして実行します。ファイルオブジェクト ``(child_stdout, child_stdin, child_stderr)``
   を返します。


.. function:: popen4(cmd[, bufsize[, mode]])

   *cmd* をサブプロセスとして実行します。ファイルオブジェクト ``(child_stdout_and_stderr, child_stdin)``.

   .. versionadded:: 2.0

Unixでは、ファクトリ関数によって返されるオブジェクトを定義している クラスも利用することができます。これらのオブジェクトは Windows 実装
で使われていないため、そのプラットフォーム上で使うことはできません。


.. class:: Popen3(cmd[, capturestderr[, bufsize]])

   このクラスは子プロセスを表現します。通常、 :class:`Popen3` インスタンスは上で述べた :func:`popen2` および
   :func:`popen3`  ファクトリ関数を使って生成されます。

   :class:`Popen3` オブジェクトを生成するためにいずれかのヘルパー関数を 使っていないのなら、*cmd* パラメタは子プロセスで実行する
   シェルコマンドになります。*capturestderr* フラグが真であれば、 このオブジェクトが子プロセスの標準エラー出力を捕獲しなければならない
   ことを意味します。標準の値は偽です。*bufsize* パラメタが存在 する場合、子プロセスへの／からの I/O バッファのサイズを指定します。


.. class:: Popen4(cmd[, bufsize])

   :class:`Popen3` に似ていますが、標準エラー出力を標準出力と同じファイル オブジェクトで捕獲します。このオブジェクトは通常
   :func:`popen4` で 生成されます。

   .. versionadded:: 2.0


.. _popen3-objects:

Popen3 および Popen4 オブジェクト
---------------------------------

:class:`Popen3` および :class:`Popen4` クラスのインスタンスは以下の メソッドを持ちます:


.. method:: Popen3.poll()

   子プロセスがまだ終了していない際には ``-1`` を、そうでない場合には リターンコードを返します。


.. method:: Popen3.wait()

   子プロセスの状態コード出力を待機して返します。状態コードでは 子プロセスのリターンコードと、プロセスが :cfunc:`exit` によって
   終了したか、あるいはシグナルによって死んだかについての情報を 符号化しています。状態コードの解釈を助けるための関数は :mod:`os`
   モジュールで定義されています;  :ref:`os-process` 節の :func:`W\*` 関数ファミリを 参照してください。

以下の属性も利用可能です:


.. attribute:: Popen3.fromchild

   子プロセスからの出力を提供するファイルオブジェクトです。 :class:`Poepn4` インスタンスの場合、この値は標準出力と標準
   エラー出力の両方を提供するオブジェクトになります。


.. attribute:: Popen3.tochild

   子プロセスへの入力を提供するファイルオブジェクトです。


.. attribute:: Popen3.childerr

   コンストラクタに *capturestderr* を渡した際には子プロセスからの 標準エラー出力を提供するファイルオブジェクトで、そうでない場合
   ``None`` になります。 :class:`Popen4` インスタンスでは、この値は常に ``None`` になります。


.. attribute:: Popen3.pid

   子プロセスのプロセス番号です。


.. _popen2-flow-control:

フロー制御の問題
----------------

何らかの形式でプロセス間通信を利用している際には常に、制御フローに ついて注意深く考える必要があります。これはこのモジュール (あるいは :mod:`os`
モジュールにおける等価な機能) で生成される ファイルオブジェクトの場合にもあてはまります。

親プロセスが子プロセスの標準出力を読み出している一方で、子プロセスが 大量のデータを標準エラー出力に書き込んでいる場合、この子プロセスから
出力を読み出そうとするとデッドロックが発生します。 同様の状況は読み書きの他の組み合わせでも生じます。本質的な要因は、 一方のプロセスが別の
プロセスでブロック型の読み出しをしている際に、:const:`_PC_PIPE_BUF`
バイトを超えるデータがブロック型の入出力を行うプロセスによって書き込ま れることにあります。

.. % Example explanation and suggested work-arounds substantially stolen
.. % from Martin von Loewis:
.. % http://mail.python.org/pipermail/python-dev/2000-September/009460.html

こうした状況を扱うには幾つかのやりかたがあります。

多くの場合、もっとも単純なアプリケーションに対する変更は、 親プロセスで以下のようなモデル::

   import popen2

   r, w, e = popen2.popen3('python slave.py')
   e.readlines()
   r.readlines()
   r.close()
   e.close()
   w.close()

に従うようにし、子プロセスで以下::

   import os
   import sys

   # note that each of these print statements
   # writes a single long string

   print >>sys.stderr, 400 * 'this is a test\n'
   os.close(sys.stderr.fileno())
   print >>sys.stdout, 400 * 'this is another test\n'

のようなコードにすることでしょう。

とりわけ、``sys.stderr`` は全てのデータを書き込んた後に閉じ られなければならないということに注意してください。さもなければ、
:meth:`readlines` は返ってきません。また、 ``sys.stderr.close()`` が ``stderr`` を閉じないように
:func:`os.close` を使わなければならないことにも注意してください。 (そうでなく、``sys.stderr``
に関連付けると、暗黙のうちに閉じられて しまうので、それ以降のエラーが出力されません)。

より一般的なアプローチをサポートする必要があるアプリケーションでは、 パイプ経由の I/O を :func:`select` ループでまとめるか、 個々の
:func:`popen\*` 関数や :class:`Popen\*` クラスが提供する各々のファイルに対して、個別のスレッドを使って 読み出しを行います。

