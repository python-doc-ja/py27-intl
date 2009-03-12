
.. _toolbox:

*******************************
Mac OS ツールボックスモジュール
*******************************

各種の Mac OS ツールボックスへのインターフェースを与えるモジュール群が\
あります。対応するモジュールがあるなら、そのモジュールではツールボックス\
で宣言された各種の構造体の Python オブジェクトが定義され、操作は定義され\
たオブジェクトのメソッドとして実装されています。その他の操作はモジュー\
ルの関数として実装されています。 C で可能な操作がすべて Python で可能な\
わけではありませんし(コールバックはよく問題になります)、パラメータが\
Python だと違ってしまうことはよくあります(特に入力バッファや出力バッファ)。
全てのメソッドと関数は :attr:`__doc__` 文字列があるので、引数と返り値\
の説明を得る事ができます。他の情報源としては、 `Inside Macintosh
<http://developer.apple.com/documentation/macos8/mac8.html>`_
などを参照してください。

これらのモジュールは全て :mod:`Carbon` パッケージに含まれています。
この名前にもかかわらずそれら全てが Carbon フレームワークの一部なわけで\
はありません。CF は、CoreFoundation フレームワークの中に実際はあります\
し、Qt は QuickTime フレームワークにあります。ツールボックスモジュール\
は普通以下のようにして利用します。

::

   from Carbon import AE

.. warning::

   Carbon モジュール群は 3.0 で削除されます。


:mod:`Carbon.AE` --- Apple Events
=================================

.. module:: Carbon.AE
   :platform: Mac
   :synopsis: Apple Eventツールボックスへのインタフェース
   :deprecated:


:mod:`Carbon.AH` --- Apple ヘルプ
=================================

.. module:: Carbon.AH
   :platform: Mac
   :synopsis: Apple ヘルプマネージャへのインタフェース
   :deprecated:


:mod:`Carbon.App` --- アピアランスマネージャ
============================================

.. module:: Carbon.App
   :platform: Mac
   :synopsis: アピアランスマネージャへのインタフェース
   :deprecated:


:mod:`Carbon.CF` --- Core Foundation
====================================

.. module:: Carbon.CF
   :platform: Mac
   :synopsis: Core Foundationへのインタフェース
   :deprecated:

``CFBase``, ``CFArray``, ``CFData``, ``CFDictionary``, ``CFString`` と
``CFURL`` オブジェクトがいくらか部分的にサポートされています。


:mod:`Carbon.CG` --- Core Graphics
==================================

.. module:: Carbon.CG
   :platform: Mac
   :synopsis: コア・グラフィックスへのインタフェース
   :deprecated:


:mod:`Carbon.CarbonEvt` --- Carbon Event Manager
================================================

.. module:: Carbon.CaronEvt
   :platform: Mac
   :synopsis: Carbon Event Managerへのインタフェース
   :deprecated:


:mod:`Carbon.Cm` --- Component Manager
======================================

.. module:: Carbon.Cm
   :platform: Mac
   :synopsis: Component Managerへのインタフェース
   :deprecated:


:mod:`Carbon.Ctl` --- Control Manager
=====================================

.. module:: Carbon.Ctl
   :platform: Mac
   :synopsis: Control Managerへのインタフェース
   :deprecated:


:mod:`Carbon.Dlg` --- Dialog Manager
====================================

.. module:: Carbon.Dlg
   :platform: Mac
   :synopsis: Dialog Managerへのインタフェース
   :deprecated:


:mod:`Carbon.Evt` --- Event Manager
===================================

.. module:: Carbon.Evt
   :platform: Mac
   :synopsis: Event Managerへのインタフェース
   :deprecated:


:mod:`Carbon.Fm` --- Font Manager
=================================

.. module:: Carbon.Fm
   :platform: Mac
   :synopsis: Font Managerへのインタフェース
   :deprecated:


:mod:`Carbon.Folder` --- Folder Manager
=======================================

.. module:: Carbon.Folder
   :platform: Mac
   :synopsis: Folder Managerへのインタフェース
   :deprecated:


:mod:`Carbon.Help` --- Help Manager
===================================

.. module:: Carbon.Help
   :platform: Mac
   :synopsis: Carbon Help Managerへのインタフェース
   :deprecated:


:mod:`Carbon.List` --- List Manager
===================================

.. module:: Carbon.List
   :platform: Mac
   :synopsis: List Managerへのインタフェース
   :deprecated:


:mod:`Carbon.Menu` --- Menu Manager
===================================

.. module:: Carbon.Menu
   :platform: Mac
   :synopsis: Menu Managerへのインタフェース
   :deprecated:


:mod:`Carbon.Mlte` --- MultiLingual Text Editor
===============================================

.. module:: Carbon.Mlte
   :platform: Mac
   :synopsis: MultiLingual Text Editorへのインタフェース
   :deprecated:


:mod:`Carbon.Qd` --- QuickDraw
==============================

.. module:: Carbon.Qd
   :platform: Mac
   :synopsis: QuickDrawツールボックスへのインタフェース
   :deprecated:


:mod:`Carbon.Qdoffs` --- QuickDraw Offscreen
============================================

.. module:: Carbon.Qdoffs
   :platform: Mac
   :synopsis: QuickDrawオフスクリーン APIへのインタフェース
   :deprecated:


:mod:`Carbon.Qt` --- QuickTime
==============================

.. module:: Carbon.Qt
   :platform: Mac
   :synopsis: QuickTime ツールボックスへのインタフェース
   :deprecated:


:mod:`Carbon.Res` --- Resource Manager and Handles
==================================================

.. module:: Carbon.Res
   :platform: Mac
   :synopsis: Resource Managerとハンドルへのインタフェース
   :deprecated:


:mod:`Carbon.Scrap` --- スクラップマネージャ
============================================

.. module:: Carbon.Scrap
   :platform: Mac
   :synopsis: スクラップマネージャはカット & ペーストとクリップボードの操作の基本的\
              なサービスを提供します。
   :deprecated:


このモジュールは Mac OS 9 とそれ以前の OS 上の Classic PPC MacPython
で完全に利用可能です。
Carbon 版の MacPython ではほんの限られた機能だけが利用可能です。

.. index:: single: Scrap Manager

スクラップマネージャは Macintosh 上でのカット & ペースト操作の最も\
シンプルな形式をサポートします。
アプリケーション間とアプリケーション内での両方のクリップボード操作が可能\
です。

:mod:`Scrap` モジュールはスクラップマネージャの関数へのローレベルでのア\
クセスを提供します。
以下の関数が定義されています：


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
      Appleのスクラップマネージャに関する文書には、アプリケーションでスクラッ\
      プマネージャを使用する上での便利な情報がたくさんあります。



:mod:`Carbon.Snd` --- Sound Manager
===================================

.. module:: Carbon.Snd
   :platform: Mac
   :synopsis: Sound Managerへのインタフェース
   :deprecated:


:mod:`Carbon.TE` --- TextEdit
=============================

.. module:: Carbon.TE
   :platform: Mac
   :synopsis: TextEditへのインタフェース
   :deprecated:


:mod:`Carbon.Win` --- Window Manager
====================================

.. module:: Carbon.Win
   :platform: Mac
   :synopsis: Window Managerへのインタフェース
   :deprecated:
