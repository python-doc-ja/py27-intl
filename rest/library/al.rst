
:mod:`al` --- SGIのオーディオ機能
=================================

.. module:: al
   :platform: IRIX
   :synopsis: SGIのオーディオ機能。


.. % Audio functions on the SGI}
.. % Audio functions on the SGI.}

このモジュールを使うと、SGI IndyとIndigoワークステーションのオーディオ装 置にアクセスできます。
詳しくはIRIXのmanページのセクション3Aを参照してください。 ここに書かれた関数が何をするかを理解するには、manページを読む必要が あります！
IRIXのリリース4.0.5より前のものでは使えない関数もあります。 お使いのプラットフォームで特定の関数が使えるかどうか、マニュアルで確認し てください。

.. % This module provides access to the audio facilities of the SGI Indy
.. % and Indigo workstations.
.. % See section 3A of the IRIX man pages for
.. % details.
.. % You'll need to read those man pages to understand what these
.. % functions do!
.. % Some of the functions are not available in IRIX
.. % releases before 4.0.5.
.. % Again, see the manual to check whether a
.. % specific function is available on your platform.

このモジュールで定義された関数とメソッドは全て、名前に``AL``の接頭辞 を付けたCの関数と同義です。

.. % All functions and methods defined in this module are equivalent to
.. % the C functions with \samp{AL} prefixed to their name.

.. index:: module: AL

Cのヘッダーファイル``<audio.h>``のシンボル定数は標準モジュール :mod:`AL`に定義されています。 下記を参照してください。

.. % Symbolic constants from the C header file \code{<audio.h>} are
.. % defined in the standard module
.. % \refmodule[al-constants]{AL}\refstmodindex{AL}, see below.

.. warning::

   オーディオライブラリの現在のバージョンは、不正な引数が渡されるとエラース テイタスが返るのではなく、coreを吐き出すことがあります。
   残念ながら、この現象が確実に起こる環境は述べられていないし、確認する ことは難しいので、Pythonインターフェースでこの種の問題に対して防御する
   ことはできません。 （一つの例は過大なキューサイズを特定することです --- 上限については記載 されていません。）

   .. % The current version of the audio library may dump core
   .. % when bad argument values are passed rather than returning an error
   .. % status.
   .. % Unfortunately, since the precise circumstances under which
   .. % this may happen are undocumented and hard to check, the Python
   .. % interface can provide no protection against this kind of problems.
   .. % (One example is specifying an excessive queue size --- there is no
   .. % documented upper limit.)}

このモジュールには、以下の関数が定義されています：

.. % The module defines the following functions:


.. function:: openport(name, direction[, config])

   引数*name*と*direction*は文字列です。 省略可能な引数*config*は、:func:`newconfig`で返されるコンフィ
   ギュレーションオブジェクトです。 返り値は:dfn:`audio port object`です；オーディオポートオブジェクトの メソッドは下に書かれています。

   .. % The name and direction arguments are strings.
   .. % The optional
   .. % \var{config} argument is a configuration object as returned by
   .. % \function{newconfig()}.
   .. % The return value is an \dfn{audio port
   .. % object}; methods of audio port objects are described below.


.. function:: newconfig()

   返り値は新しい:dfn:`audio configuration object`です；オーディオコンフィ
   ギュレーションオブジェクトのメソッドは下に書かれています。

   .. % The return value is a new \dfn{audio configuration object}; methods of
   .. % audio configuration objects are described below.


.. function:: queryparams(device)

   引数*device*は整数です。 返り値は:cfunc:`ALqueryparams`で返されるデータを含む整数のリストで す。

   .. % The device argument is an integer.
   .. % The return value is a list of
   .. % integers containing the data returned by \cfunction{ALqueryparams()}.


.. function:: getparams(device, list)

   引数*device*は整数です。 引数*list*は:func:`queryparams`で返されるようなリストです；
   :func:`queryparams`を適切に（！）修正して使うことができます。

   .. % The \var{device} argument is an integer.
   .. % The list argument is a list
   .. % such as returned by \function{queryparams()}; it is modified in place
   .. % (!).


.. function:: setparams(device, list)

   引数*device*は整数です。 引数*list*は:func:`queryparams`で返されるようなリストです。

   .. % The \var{device} argument is an integer.
   .. % The \var{list} argument is a
   .. % list such as returned by \function{queryparams()}.


.. _al-config-objects:

コンフィギュレーションオブジェクト
----------------------------------

.. % Configuration Objects

:func:`newconfig`で返されるコンフィギュレーションオブジェクト には以下のメソッドがあります：

.. % Configuration objects (returned by \function{newconfig()} have the
.. % following methods:


.. method:: audio configuration.getqueuesize()

   キューサイズを返します。

   .. % Return the queue size.


.. method:: audio configuration.setqueuesize(size)

   キューサイズを設定します。

   .. % Set the queue size.


.. method:: audio configuration.getwidth()

   サンプルサイズを返します。

   .. % Get the sample width.


.. method:: audio configuration.setwidth(width)

   サンプルサイズを設定します。

   .. % Set the sample width.


.. method:: audio configuration.getchannels()

   チャンネル数を返します。

   .. % Get the channel count.


.. method:: audio configuration.setchannels(nchannels)

   チャンネル数を設定します。

   .. % Set the channel count.


.. method:: audio configuration.getsampfmt()

   サンプルのフォーマットを返します。

   .. % Get the sample format.


.. method:: audio configuration.setsampfmt(sampfmt)

   サンプルのフォーマットを設定します。

   .. % Set the sample format.


.. method:: audio configuration.getfloatmax()

   浮動小数点数でサンプルデータの最大値を返します。

   .. % Get the maximum value for floating sample formats.


.. method:: audio configuration.setfloatmax(floatmax)

   浮動小数点数でサンプルデータの最大値を設定します。

   .. % Set the maximum value for floating sample formats.


.. _al-port-objects:

ポートオブジェクト
------------------

.. % Port Objects

:func:`openport`で返されるポートオブジェクトには以下のメソッドがあ ります：

.. % Port objects, as returned by \function{openport()}, have the following
.. % methods:


.. method:: audio port.closeport()

   ポートを閉じます。

   .. % Close the port.


.. method:: audio port.getfd()

   ファイルディスクリプタを整数で返します。

   .. % Return the file descriptor as an int.


.. method:: audio port.getfilled()

   バッファに存在するサンプルの数を返します。

   .. % Return the number of filled samples.


.. method:: audio port.getfillable()

   バッファの空きに入れることのできるサンプルの数を返します。

   .. % Return the number of fillable samples.


.. method:: audio port.readsamps(nsamples)

   必要ならブロックして、キューから指定のサンプル数を読み込みます。 生データを文字列として （例えば、サンプルサイズが2バイトならサンプル当たり2バイトがbig-
   endian （high byte、low byte）で）返します。

   .. % Read a number of samples from the queue, blocking if necessary.
   .. % Return the data as a string containing the raw data, (e.g., 2 bytes per
   .. % sample in big-endian byte order (high byte, low byte) if you have set
   .. % the sample width to 2 bytes).


.. method:: audio port.writesamps(samples)

   必要ならブロックして、キューにサンプルを書き込みます。 サンプルは:meth:`readsamps`で返される値のようにエンコードされていなけ ればなりません。

   .. % Write samples into the queue, blocking if necessary.
   .. % The samples are
   .. % encoded as described for the \method{readsamps()} return value.


.. method:: audio port.getfillpoint()

   'fill point'を返します。

   .. % Return the `fill point'.


.. method:: audio port.setfillpoint(fillpoint)

   'fill point'を設定します。

   .. % Set the `fill point'.


.. method:: audio port.getconfig()

   現在のポートのコンフィギュレーションを含んだコンフィギュレーションオブ ジェクトを返します。

   .. % Return a configuration object containing the current configuration of
   .. % the port.


.. method:: audio port.setconfig(config)

   コンフィギュレーションを引数に取り、そのコンフィギュレーションに設定しま す。

   .. % Set the configuration from the argument, a configuration object.


.. method:: audio port.getstatus(list)

   最後のエラーについてのステイタスの情報を返します。

   .. % Get status information on last error.


:mod:`AL` --- :mod:`al`モジュールで使われる定数
===============================================

.. % Constants used with the \module{al} module}

.. module:: AL
   :platform: IRIX
   :synopsis: alモジュールで使われる定数。


.. % Constants used with the \module{al} module.}

このモジュールには、組み込みモジュール:mod:`al`（上記参照）を使用す るのに必要とされるシンボリック定数が定義されています。
定数の名前はCのincludeファイル``<audioio.h>``で 接頭辞``AL_``を除いたものと同じです。

.. % This module defines symbolic constants needed to use the built-in
.. % module \refmodule{al} (see above);
.. % they are equivalent to those defined
.. % in the C header file \code{<audio.h>} except that the name prefix
.. % \samp{AL_} is omitted.

定義されている名前の完全なリストについてはモジュールのソースを参照してく ださい。 お勧めの使い方は以下の通りです：

.. % Read the module source for a complete list of
.. % the defined names.
.. % Suggested use:

::

   import al
   from AL import *

