
:mod:`uu` --- uuencode形式のエンコードとデコード
===================================

.. module:: uu
   :synopsis: uuencode形式のエンコードとデコードを行う。
.. moduleauthor:: Lance Ellinghouse


このモジュールではファイルをuuencode形式(任意のバイナリデータをASCII文字列 に変換したもの)にエンコード、デコードする機能を提供します。
引数としてファイルが仮定されている所では、ファイルのようなオブジェクトが 利用できます。後方互換性のために、パス名を含む文字列も利用できるようにし
ていて、対応するファイルを開いて読み書きします。しかし、このインターフェー スは利用しないでください。呼び出し側でファイルを開いて(Windowsでは
``'rb'``か``'wb'``のモードで)利用する方法が推奨されます。

.. % This module encodes and decodes files in uuencode format, allowing
.. % arbitrary binary data to be transferred over ASCII-only connections.
.. % Wherever a file argument is expected, the methods accept a file-like
.. % object.  For backwards compatibility, a string containing a pathname
.. % is also accepted, and the corresponding file will be opened for
.. % reading and writing; the pathname \code{'-'} is understood to mean the
.. % standard input or output.  However, this interface is deprecated; it's
.. % better for the caller to open the file itself, and be sure that, when
.. % required, the mode is \code{'rb'} or \code{'wb'} on Windows.

.. index::
   single: Jansen, Jack
   single: Ellinghouse, Lance

このコードはLance Ellinghouseによって提供され、Jack Jansenによって更新さ れました。

.. % This code was contributed by Lance Ellinghouse, and modified by Jack
.. % Jansen.

:mod:`uu`モジュールでは以下の関数を定義しています。


.. function:: encode(in_file, out_file[, name[, mode]])

   *in_file*を*out_file*にエンコードします。 エンコードされたファイルには、デフォルトでデコード時に利用される
   *name*と*mode*を含んだヘッダがつきます。省略された場合には、 *in_file*から取得された名前か``'-'`` という文字と、``0666``
   がそれぞれデフォルト値として与えられます。

   .. % Uuencode file \var{in_file} into file \var{out_file}.  The uuencoded
   .. % file will have the header specifying \var{name} and \var{mode} as
   .. % the defaults for the results of decoding the file. The default
   .. % defaults are taken from \var{in_file}, or \code{'-'} and \code{0666}
   .. % respectively.


.. function:: decode(in_file[, out_file[, mode]])

   uuencode形式でエンコードされた*in_file*をデコードして varout_fileに書き出します。もし*out_file*がパス名でかつファイルを
   作る必要があるときには、 *mode*がパーミッションの設定に使われます。 *out_file*と*mode*のデフォルト値は*in_file*のヘッダから取得
   されます。しかし、ヘッダで指定されたファイルが既に存在していた場合は、 :exc:`uu.Error`が起きます。

   .. % This call decodes uuencoded file \var{in_file} placing the result on
   .. % file \var{out_file}. If \var{out_file} is a pathname, \var{mode} is
   .. % used to set the permission bits if the file must be
   .. % created. Defaults for \var{out_file} and \var{mode} are taken from
   .. % the uuencode header.  However, if the file specified in the header
   .. % already exists, a \exception{uu.Error} is raised.

   誤った実装のuuencoderによる入力で、エラーから復旧できた場合、 :func:`decode`は標準エラー出力に警告を表示するかもしれません。
   *quiet*を真にすることでこの警告を抑制することができます。


.. exception:: Error()

   :exc:`Exception`のサブクラスで、:func:`uu.decode`によって、さ
   まざまな状況で起きる可能性があります。上で紹介された場合以外にも、ヘッダ のフォーマットが間違っている場合や、入力ファイルが途中で区切れた場合に も起きます。

   .. % Subclass of \exception{Exception}, this can be raised by
   .. % \function{uu.decode()} under various situations, such as described
   .. % above, but also including a badly formated header, or truncated
   .. % input file.


.. seealso::

   Module :mod:`binascii`
      ASCII からバイナリへ、バイナリからASCIIへの 変換をサポートするモジュール。

