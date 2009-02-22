
.. _toolbox:

******************************
MacOS ツールボックスモジュール
******************************

各種のMacOSツールボックスへのインターフェースを与えるモジュール群があ ります。対応するモジュールがあるなら、そのモジュールではツールボックス
で宣言された各種の構造体のPythonオブジェクトが定義され、操作は定義され たオブジェクトのメソッドとして実装されています。その他の操作はモジュー
ルの関数として実装されています。 Cで可能な操作がすべてPythonで可能なわ けではありませんし(コールバックはよく問題になります)、パラメータが
Pythonだと違ってしまうことはよくあります(特に入力バッファや出力バッファ)。 全てのメソッドと関数は :attr:`__doc__`
文字列があるので、引数と返り値 の説明を得る事ができます。他の情報源としては、 `Inside Macintosh
<http://developer.apple.com/documentation/macos8/mac8.html>`_などを参照してください。

.. % MacOS Toolbox Modules
.. % % There are a set of modules that provide interfaces to various MacOS
.. % % toolboxes.  If applicable the module will define a number of Python
.. % % objects for the various structures declared by the toolbox, and
.. % % operations will be implemented as methods of the object.  Other
.. % % operations will be implemented as functions in the module.  Not all
.. % % operations possible in C will also be possible in Python (callbacks
.. % % are often a problem), and parameters will occasionally be different in
.. % % Python (input and output buffers, especially).  All methods and
.. % % functions have a \member{__doc__} string describing their arguments
.. % % and return values, and for additional description you are referred to
.. % % \citetitle[http://developer.apple.com/documentation/macos8/mac8.html]{Inside
.. % % Macintosh} or similar works.

これらのモジュールは全て :mod:`Carbon` パッケージに含まれています。 この名前にもかかわらずそれら全てが Carbon
フレームワークの一部なわけで はありません。CF は、CoreFoundationフレームワークの中に実際はあります
し、QtはQuickTimeフレームワークにあります。ツールボックスモジュールは普通以下 のようにして利用します。

.. % % These modules all live in a package called \module{Carbon}. Despite that name
.. % % they are not all part of the Carbon framework: CF is really in the CoreFoundation
.. % % framework and Qt is in the QuickTime framework.
.. % % The normal use pattern is

::

   from Carbon import AE

**注意！**これらのモジュールはまだ文書化されていません。これらの モジュールのどれでもよいですが文書化に協力したいという方は、
docs@python.org まで連絡をください。

.. % % \strong{Warning!}  These modules are not yet documented.  If you
.. % % wish to contribute documentation of any of these modules, please get
.. % % in touch with \email{python-docs@python.org}.


.. toctree::

   colorpicker.rst
.. % \section{Argument Handling for Toolbox Modules}


:mod:`Carbon.AE` --- Apple Events
=================================

.. module:: Carbon.AE
   :platform: Mac
   :synopsis: Apple Eventツールボックスへのインタフェース


.. % Interface to the Apple Events toolbox.


:mod:`Carbon.AH` --- Apple ヘルプ
=================================

.. module:: Carbon.AH
   :platform: Mac
   :synopsis: Apple ヘルプマネージャへのインタフェース


.. % Apple Help
.. % Interface to the Apple Help manager.


:mod:`Carbon.App` --- アピアランスマネージャ
============================================

.. module:: Carbon.App
   :platform: Mac
   :synopsis: アピアランスマネージャへのインタフェース


.. % Appearance Manager
.. % Interface to the Appearance Manager.


:mod:`Carbon.CF` --- Core Foundation
====================================

.. module:: Carbon.CF
   :platform: Mac
   :synopsis: Core Foundationへのインタフェース


``CFBase``, ``CFArray``, ``CFData``, ``CFDictionary``, ``CFString`` と ``CFURL``
オブジェクトがいくらか部分的にサポート されています。

.. % Interface to the Core Foundation.
.. % % The
.. % % \code{CFBase}, \code{CFArray}, \code{CFData}, \code{CFDictionary},
.. % % \code{CFString} and \code{CFURL} objects are supported, some
.. % % only partially.


:mod:`Carbon.CG` --- Core Graphics
==================================

.. module:: Carbon.CG
   :platform: Mac
   :synopsis: Component Managerへのインタフェース


.. % Interface to the Component Manager.


:mod:`Carbon.CarbonEvt` --- Carbon Event Manager
================================================

.. module:: Carbon.CaronEvt
   :platform: Mac
   :synopsis: Carbon Event Managerへのインタフェース


.. % Interface to the Carbon Event Manager.


:mod:`Carbon.Cm` --- Component Manager
======================================

.. module:: Carbon.Cm
   :platform: Mac
   :synopsis: Component Managerへのインタフェース


.. % Interface to the Component Manager.


:mod:`Carbon.Ctl` --- Control Manager
=====================================

.. module:: Carbon.Ctl
   :platform: Mac
   :synopsis: Control Managerへのインタフェース


.. % Interface to the Control Manager.


:mod:`Carbon.Dlg` --- Dialog Manager
====================================

.. module:: Carbon.Dlg
   :platform: Mac
   :synopsis: Dialog Managerへのインタフェース


.. % Interface to the Dialog Manager.


:mod:`Carbon.Evt` --- Event Manager
===================================

.. module:: Carbon.Evt
   :platform: Mac
   :synopsis: Event Managerへのインタフェース


.. % Interface to the classic Event Manager.


:mod:`Carbon.Fm` --- Font Manager
=================================

.. module:: Carbon.Fm
   :platform: Mac
   :synopsis: Font Managerへのインタフェース


.. % Interface to the Font Manager.


:mod:`Carbon.Folder` --- Folder Manager
=======================================

.. module:: Carbon.Folder
   :platform: Mac
   :synopsis: Folder Managerへのインタフェース


.. % Interface to the Folder Manager.


:mod:`Carbon.Help` --- Help Manager
===================================

.. module:: Carbon.Help
   :platform: Mac
   :synopsis: Carbon Help Managerへのインタフェース


.. % Interface to the Carbon Help Manager.


:mod:`Carbon.List` --- List Manager
===================================

.. module:: Carbon.List
   :platform: Mac
   :synopsis: List Managerへのインタフェース


.. % Interface to the List Manager.


:mod:`Carbon.Menu` --- Menu Manager
===================================

.. module:: Carbon.Menu
   :platform: Mac
   :synopsis: Menu Managerへのインタフェース


.. % Interface to the Menu Manager.


:mod:`Carbon.Mlte` --- MultiLingual Text Editor
===============================================

.. module:: Carbon.Mlte
   :platform: Mac
   :synopsis: MultiLingual Text Editorへのインタフェース


.. % Interface to the MultiLingual Text Editor.


:mod:`Carbon.Qd` --- QuickDraw
==============================

.. module:: Carbon.Qd
   :platform: Mac
   :synopsis: QuickDrawツールボックスへのインタフェース


.. % Interface to the QuickDraw toolbox.


:mod:`Carbon.Qdoffs` --- QuickDraw Offscreen
============================================

.. module:: Carbon.Qdoffs
   :platform: Mac
   :synopsis: QuickDrawオフスクリーン APIへのインタフェース


.. % Interface to the QuickDraw Offscreen APIs.


:mod:`Carbon.Qt` --- QuickTime
==============================

.. module:: Carbon.Qt
   :platform: Mac
   :synopsis: QuickTime ツールボックスへのインタフェース


.. % Interface to the QuickTime toolbox.


:mod:`Carbon.Res` --- Resource Manager and Handles
==================================================

.. module:: Carbon.Res
   :platform: Mac
   :synopsis: Resource Managerとハンドルへのインタフェース


.. % Interface to the Resource Manager and Handles.


:mod:`Carbon.Scrap` --- スクラップマネージャ
============================================

.. module:: Carbon.Scrap
   :platform: Mac
   :synopsis: スクラップマネージャはカット & ペーストとクリップボードの操作の基本的\
              なサービスを提供します。
   :deprecated:


このモジュールはMacOS9とそれ以前のOS上のClassic PPC MacPythonで完全に利 用可能です。
Carbon版のMacPythonではほんの限られた機能だけが利用可能です。

.. index:: single: Scrap Manager

スクラップマネージャはMacintosh上でのカット & ペースト操作の最もシンプルな形式をサポートします。
アプリケーション間とアプリケーション内での両方のクリップボード操作が可能 です。

:mod:`Scrap`モジュールはスクラップマネージャの関数へのローレベルでのア クセスを提供します。 以下の関数が定義されています：


.. function:: InfoScrap()

   スクラップについて現在の情報を返します。
   この情報は ``(size, handle, count, state, path)``
   を含むタプルでエンコードされます。

   +----------+------------------------------------------------------------------+
   | Field    | Meaning                                                          |
   +==========+==================================================================+
   | *size*   | スクラップのサイズをバイト数で示したもの。                       |
   +----------+------------------------------------------------------------------+
   | *handle* | スクラップを表現するリソースオブジェクト。                       |
   +----------+------------------------------------------------------------------+
   | *count*  | スクラップの内容のシリアルナンバー。                             |
   +----------+------------------------------------------------------------------+
   | *state*  | 整数。メモリー内にあるなら正、ディスク上にあるなら ``0`` 、      |
   |          | 初期化されていないなら負。                                       |
   +----------+------------------------------------------------------------------+
   | *path*   | ディスク上に保存されているなら、そのスクラップのファイルネーム。 |
   +----------+------------------------------------------------------------------+


.. seealso::

   `Scrap Manager <http://developer.apple.com/documentation/mac/MoreToolbox/MoreToolbox-109.html>`_
      Appleのスクラップマネージャに関する文書には、アプリケーションでスクラッ プマネージャを使用する上での便利な情報がたくさんあります。



:mod:`Carbon.Snd` --- Sound Manager
===================================

.. module:: Carbon.Snd
   :platform: Mac
   :synopsis: Sound Managerへのインタフェース


.. % Interface to the Sound Manager.


:mod:`Carbon.TE` --- TextEdit
=============================

.. module:: Carbon.TE
   :platform: Mac
   :synopsis: TextEditへのインタフェース


.. % Interface to TextEdit.


:mod:`Carbon.Win` --- Window Manager
====================================

.. module:: Carbon.Win
   :platform: Mac
   :synopsis: Window Managerへのインタフェース


.. % Interface to the Window Manager.

