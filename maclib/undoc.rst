
.. _undocumented-modules:

****************************
文書化されていないモジュール
****************************

この章のモジュールは、ほとんど (あるいはまったく) ドキュメント化されていません。これらのモジュールのいずれかについてドキュメントを寄与したいと
考えているなら、`docs@python.org <mailto:docs@python.org>`_ までご連絡ください。

.. % Undocumented Modules
.. % % The modules in this chapter are poorly documented (if at all).  If you
.. % % wish to contribute documentation of any of these modules, please get in
.. % % touch with
.. % % \ulink{\email{python-docs@python.org}}{mailto:python-docs@python.org}.


.. toctree::


:mod:`applesingle` --- AppleSingle デコーダー
=============================================

.. module:: applesingle
   :platform: Mac
   :synopsis: AppleSingle フォーマットファイル用の基本的なデコーダ


.. % AppleSingle decoder
.. % Rudimentary decoder for AppleSingle format files.


:mod:`buildtools` --- BuildAppletとその仲間のヘルパーモジュール
===============================================================

.. module:: buildtools
   :platform: Mac
   :synopsis: BuildAppletとその仲間のヘルパーモジュール


.. % Helper module for BuildApplet and Friends
.. % Helper module for BuildApplet, BuildApplication and macfreeze.

.. deprecated:: 2.4

:mod:`cfmfile` --- コードフラグメントリソースを扱うモジュール
=============================================================

.. module:: cfmfile
   :platform: Mac
   :synopsis: コードフラグメントリソースを扱うモジュール


:mod:`cfmfile` は、コードフラグメントと関連する"cfrg"リソースを処理するモジュールです。このモジュールでコードフラグメントを分解やマージ
できて、全てのプラグインモジュールをまとめて、一つの実行可能ファイルにするため、BuildApplicationによって利用されます。

.. % Code Fragment Resource module
.. % Code Fragment Resource module.
.. % % \module{cfmfile} is a module that understands Code Fragments and the
.. % % accompanying ``cfrg'' resources. It can parse them and merge them, and is
.. % % used by BuildApplication to combine all plugin modules to a single
.. % % executable.

.. deprecated:: 2.4

:mod:`icopen` --- :meth:`open`と Internet Config の置き換え
===========================================================

.. module:: icopen
   :platform: Mac
   :synopsis: open()と Internet Config の置き換え


:mod:`icopen` をインポートすると、組込み :meth:`open` を新しいファイル用にファイルタイプおよびクリエーターを設定するために
Internet Configを使用するバージョンに置き換えます。

.. % Internet Config replacement for \method{open()}
.. % Internet Config replacement for \method{open()}.
.. % % Importing \module{icopen} will replace the builtin \method{open()}
.. % % with a version that uses Internet Config to set file type and creator
.. % % for new files.


:mod:`macerrors` --- MacOSのエラー
==================================

.. module:: macerrors
   :platform: Mac
   :synopsis: 多くの MacOS エラーコード定数定義


:mod:`macerrors` は、MacOS エラーコードを意味する定数定義を含みます。

.. % Mac OS Errors
.. % Constant definitions for many Mac OS error codes.
.. % % \module{macerrors} contains constant definitions for many Mac OS error
.. % % codes.


:mod:`macresource` --- スクリプトのリソースを見つける
=====================================================

.. module:: macresource
   :platform: Mac
   :synopsis: スクリプトのリソースを見つける


:mod:`macresource` はスクリプトが MacPython 上や MacPython アプレットおよび OSX Python
上で起動されている時、特別な処理をせずにダイアログやメニューなどのようなリソースを見つけるためのヘルパースクリプトです。

.. % Locate script resources
.. % Locate script resources.
.. % % \module{macresource} helps scripts finding their resources, such as
.. % % dialogs and menus, without requiring special case code for when the
.. % % script is run under MacPython, as a MacPython applet or under OSX Python.


:mod:`Nav` --- NavServices の呼出し
===================================

.. module:: Nav
   :platform: Mac
   :synopsis: Navigation Services へのインターフェース


Navigation Servicesの低レベルインターフェース。

.. % NavServices calls
.. % Interface to Navigation Services.
.. % % A low-level interface to Navigation Services.


:mod:`PixMapWrapper` --- PixMapオブジェクトのラッパー
=====================================================

.. module:: PixMapWrapper
   :platform: Mac
   :synopsis: PixMapオブジェクトのラッパー


:mod:`PixMapWrapper` はPixMap オブジェクトを Python オブジェクトでラッ
プしたもので、各フィールドに対し名前でアクセスできるようになります。  :mod:`PIL` 画像との相互の変換をするメソッドも用意されています。

.. % Wrapper for PixMap objects
.. % Wrapper for PixMap objects.
.. % % \module{PixMapWrapper} wraps a PixMap object with a Python object that
.. % % allows access to the fields by name. It also has methods to convert
.. % % to and from \module{PIL} images.


:mod:`videoreader` --- QuickTime ムービーの読み込み
===================================================

.. module:: videoreader
   :platform: Mac
   :synopsis: フレームの継続処理のためのQuickTime ムービーのフレーム読み込み


:mod:`videoreader` は QuickTime ムービーを読み込み、デコードし、プロ
グラムへ渡せます。このモジュールはさらにオーディオトラックをサポートしています。

.. % Read QuickTime movies
.. % Read QuickTime movies frame by frame for further processing.
.. % % \module{videoreader} reads and decodes QuickTime movies and passes
.. % % a stream of images to your program. It also provides some support for
.. % % audio tracks.


:mod:`W` --- :mod:`FrameWork` 上に作られたウイジェット
======================================================

.. module:: W
   :platform: Mac
   :synopsis: FrameWork 上に作られた Mac 用ウイジェット


:mod:`W` ウィジェットは、:program:`IDE` で頻繁に使われています。

.. % Widgets built on \module{FrameWork}
.. % Widgets for the Mac, built on top of \refmodule{FrameWork}.
.. % % The \module{W} widgets are used extensively in the \program{IDE}.

