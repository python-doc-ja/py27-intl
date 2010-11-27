
:mod:`MacOS` --- Mac OS インタプリタ機能へのアクセス
====================================================

.. module:: MacOS
   :platform: Mac
   :synopsis: Mac OS 固有のインタープリタ機能へのアクセス。


.. % Access to Mac OS interpreter features
.. % Access to Mac OS-specific interpreter features.

このモジュールは、Python インタプリタ内の MacOS 固有の機能に対するアクセスを提供します。例えば、インタプリタのイベントループ関数などです。十
分注意して利用してください。

.. % % This module provides access to MacOS specific functionality in the
.. % % Python interpreter, such as how the interpreter eventloop functions
.. % % and the like. Use with care.

モジュール名が大文字で始まることに注意してください。これは昔からの約束です。

.. % % Note the capitalization of the module name; this is a historical
.. % % artifact.


.. data:: runtimemodel

   Python 2.4 以降は常に ``'macho'`` です。それより前のバージョンの Python では、古い Mac OS 8 ランタイムモデルの場合は
   ``'ppc'``、 Mac OS 9 ランタイムモデルの場合は ``'carbon'`` となります。

   .. % % Always \code{'macho'}, from Python 2.4 on.
   .. % % In earlier versions of Python the value could
   .. % % also be \code{'ppc'} for the classic Mac OS 8 runtime model or
   .. % % \code{'carbon'} for the Mac OS 9 runtime model.


.. data:: linkmodel

   インタープリタがどのような方法でリンクされているかを返します。拡張モジュールがリンクモデル間で非互換性かもしれない場合、パッケージはより多
   くの適切なエラーメッセージを伝えるためにこの情報を使用することができます。値は静的リンクした Python は ``'static'``、Mac OS X
   framework  で構築した Python は ``'framework'``、標準の Unix 共有ライブラリ (shared
   library)で構築された Python は ``'shared'`` となります。古いバージョンの Python の場合、Mac OS 9 互換の
   Python では ``'cfm'`` となります。

   .. % % The way the interpreter has been linked. As extension modules may be
   .. % % incompatible between linking models, packages could use this information to give
   .. % % more decent error messages. The value is one of \code{'static'} for a
   .. % % statically linked Python, \code{'framework'} for Python in a Mac OS X framework,
   .. % % \code{'shared'} for Python in a standard \UNIX{} shared library.
   .. % % Older Pythons could also have the value
   .. % % \code{'cfm'} for Mac OS 9-compatible Python.


.. exception:: Error

   .. index:: module: macerrors

   MacOS でエラーがあると、このモジュールの関数か、Mac 固有なツールボックスインターフェースモジュールから、この例外が生成されます。引数は、整数
   エラーコード(:cdata:`OSErr` 値)とテキストで記述されたエラーコードです。分かっている全てのエラーコードのシンボル名は、標準モジュール
   :mod:`macerrors` で定義されています。

   .. % % This exception is raised on MacOS generated errors, either from
   .. % % functions in this module or from other mac-specific modules like the
   .. % % toolbox interfaces. The arguments are the integer error code (the
   .. % % \cdata{OSErr} value) and a textual description of the error code.
   .. % % Symbolic names for all known error codes are defined in the standard
   .. % % module \refmodule{macerrors}.\refstmodindex{macerrors}


.. function:: GetErrorString(errno)

   MacOSのエラーコード *errno* のテキスト表現を返します。

   .. % % Return the textual description of MacOS error code \var{errno}.


.. function:: DebugStr(message [, object])

   Mac OS X上では、文字列を単純に標準出力に送ります (古いバージョンの Mac OSでは、より複雑な機能が使用できました)。しかし、低水準のデバッガ
   (:program:`gdb`など) 用にブレークポイントを設定する場所も適切に用意しています。

   .. % % On Mac OS X the string is simply printed to stderr (on older
   .. % % Mac OS systems more elaborate functionality was available),
   .. % % but it provides a convenient location to attach a breakpoint
   .. % % in a low-level debugger like \program{gdb}.


.. function:: SysBeep()

   ベルを鳴らします。

   .. % % Ring the bell.


.. function:: GetTicks()

   システム起動時からのチック数(clock ticks、1/60秒)を得ます。

   .. % % Get the number of clock ticks (1/60th of a second) since system boot.


.. function:: GetCreatorAndType(file)

   2つの4文字の文字列としてファイルクリエータおよびファイルタイプを返します。*file* 引数はパスもしくは、``FSSpec``、``FSRef``
   オブジェクトを与える事ができます。

   .. % % Return the file creator and file type as two four-character strings.
   .. % % The \var{file} parameter can be a pathname or an \code{FSSpec} or
   .. % % \code{FSRef} object.


.. function:: SetCreatorAndType(file, creator, type)

   ファイルクリエータおよびファイルタイプを設定します。*file* 引数はパスもしくは、``FSSpec``、``FSRef`` オブジェクトを与える事ができ
   ます。*creator* と *type* は4文字の文字列が必要です。

   .. % % Set the file creator and file type.
   .. % % The \var{file} parameter can be a pathname or an \code{FSSpec} or
   .. % % \code{FSRef} object. \var{creator} and \var{type} must be four character
   .. % % strings.


.. function:: openrf(name [, mode])

   ファイルのリソースフォークを開きます。引数は組み込み関数  :func:`open` と同じです。返されたオブジェクトはファイルのように
   見えるかもしれませんが、これは Python のファイルオブジェクトではありませんので扱いに微妙な違いがあります。

   .. % % Open the resource fork of a file. Arguments are the same as for the
   .. % % built-in function \function{open()}. The object returned has file-like
   .. % % semantics, but it is not a Python file object, so there may be subtle
   .. % % differences.


.. function:: WMAvailable()

   現在のプロセスが動作しているウィンドウマネージャにアクセスします。例えば、Mac OS X サーバー上、あるいは SSH でログインしている、もしくは現在
   のインタープリタがフルブローンアプリケーションバンドル(fullblown application
   bundle)から起動されていない場合などのような、ウィンドウマネージャが存在しない場合は ``False`` を返します。

   .. % % Checks wether the current process has access to the window manager.
   .. % % The method will return \code{False} if the window manager is not available,
   .. % % for instance when running on Mac OS X Server or when logged in via ssh,
   .. % % or when the current interpreter is not running from a fullblown application
   .. % % bundle. A script runs from an application bundle either when it has been
   .. % % started with \program{pythonw} in stead of \program{python} or when running
   .. % % as an applet.

