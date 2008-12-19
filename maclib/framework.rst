
:mod:`FrameWork` --- 対話型アプリケーション・フレームワーク
===========================================================

.. module:: FrameWork
   :platform: Mac
   :synopsis: 対話型アプリケーション・フレームワーク


.. % Interactive application framework
.. % Interactive application framework.

:mod:`FrameWork` モジュールは、対話型 Macintosh アプリケーションのク
ラスで、同時にフレームワークを提供します。プログラマは、サブクラスを作っ て基底クラスの様々なメソッドをオーバーライドし、必要な機能を実装するこ
とでアプリケーションを組み立てられます。機能のオーバーライドは、時によっ て様々な異なるレベルで行われます。つまり、ある一つのダイアログウィンド
ウでクリックの処理を普段と違う方法で行うには、完全なイベント処理をオー バーライドする必要はありません。

.. % % The \module{FrameWork} module contains classes that together provide a
.. % % framework for an interactive Macintosh application. The programmer
.. % % builds an application by creating subclasses that override various
.. % % methods of the bases classes, thereby implementing the functionality
.. % % wanted. Overriding functionality can often be done on various
.. % % different levels, i.e. to handle clicks in a single dialog window in a
.. % % non-standard way it is not necessary to override the complete event
.. % % handling.

:mod:`FrameWork` の開発は事実上停止しています。現在では :mod:`PyObjC`
を使用すればPythonからCocoaの全機能を使用することがで きます。このドキュメントでは最も重要な機能だけしか記述していませんし、
それさえも論理的な形で書かれてもいません。ソースか例題を詳しく見てくだ さい。次にあげるのは、MacPython ニュースグループにポストされたコメントで、
:mod:`FrameWork` の強力さと限界について述べています。

.. % % Work on the \module{FrameWork} has pretty much stopped, now that
.. % % \module{PyObjC} is available for full Cocoa access from Python, and the
.. % % documentation describes only the most important functionality, and not
.. % % in the most logical manner at that. Examine the source or the examples
.. % % for more details.  The following are some comments posted on the
.. % % MacPython newsgroup about the strengths and limitations of
.. % % \module{FrameWork}:


.. epigraph::

   :mod:`FrameWork` の最大の強みは、制御の流れをたくさんの異なる部分に 分割できることです。例えば :mod:`W` を使って、いろいろな方法でメ
   ニューをオン/オフしたり、残りをいじらずにうまくプラグインさせることが できます。:mod:`FrameWork` の弱点は、コマンドインタフェースが抽象化
   されていないこと(といっても難しいわけではないですが)、ダイアログサポー トが最低限しかないこと、それからコントロール/ツールバーサポートが全く ないことです。

   .. % % The strong point of \module{FrameWork} is that it allows you to break
   .. % % into the control-flow at many different places. \refmodule{W}, for
   .. % % instance, uses a different way to enable/disable menus and that plugs
   .. % % right in leaving the rest intact.  The weak points of
   .. % % \module{FrameWork} are that it has no abstract command interface (but
   .. % % that shouldn't be difficult), that its dialog support is minimal and
   .. % % that its control/toolbar support is non-existent.

:mod:`FrameWork` モジュールは次の関数を定義しています。

.. % % The \module{FrameWork} module defines the following functions:


.. function:: Application()

   アプリケーション全体を表現しているオブジェクト。メソッドについての詳細 は以下の記述を参照してください。デフォルト :meth:`__init__` ルーチ
   ンは、空のウィンドウ辞書とアップルメニューつきのメニューバーをを作成し ます。

   .. % % An object representing the complete application. See below for a
   .. % % description of the methods. The default \method{__init__()} routine
   .. % % creates an empty window dictionary and a menu bar with an apple menu.


.. function:: MenuBar()

   メニューバーを表現するオブジェクト。このオブジェクトは普通はユーザは 作成しません。

   .. % % An object representing the menubar. This object is usually not created
   .. % % by the user.


.. function:: Menu(bar, title[, after])

   メニューを表現するオブジェクト。生成時には、メニューが現われる  ``MenuBar`` と、*title* 文字列、メニューが表示されるべき(1から
   始まる)位置 *after* (デフォルトは末尾)を渡します。

   .. % % An object representing a menu. Upon creation you pass the
   .. % % \code{MenuBar} the menu appears in, the \var{title} string and a
   .. % % position (1-based) \var{after} where the menu should appear (default:
   .. % % at the end).


.. function:: MenuItem(menu, title[, shortcut, callback])

   メニューアイテムオブジェクトを作成します。引数は作成するメニューと、ア イテムのタイトル文字列、オプションのキーボードショートカット、コールバッ
   クルーチンです。コールバックは、メニューID、メニュー内のアイテム番号(1 から数える)、現在のフロントウィンドウ、イベントレコードを引数に呼ばれ ます。

   .. % % Create a menu item object. The arguments are the menu to create, the
   .. % % item item title string and optionally the keyboard shortcut
   .. % % and a callback routine. The callback is called with the arguments
   .. % % menu-id, item number within menu (1-based), current front window and
   .. % % the event record.

   呼び出し可能なオブジェクトのかわりに、コールバックは文字列でも良いです。 この場合、メニューの選択は、最前面のウィンドウとアプリケーションの中で
   メソッド探索を引き起こします。メソッド名は、コールバック文字列の前に  ``'domenu_'`` を付けたものです。

   .. % % Instead of a callable object the callback can also be a string. In
   .. % % this case menu selection causes the lookup of a method in the topmost
   .. % % window and the application. The method name is the callback string
   .. % % with \code{'domenu_'} prepended.

   ``MenuBar`` の :meth:`fixmenudimstate`メソッドを呼びだすと、現在
   のフロントウィンドウにもとづいて、適切なディム化を全てのメニューアイテ ムに対してほどこします。

   .. % % Calling the \code{MenuBar} \method{fixmenudimstate()} method sets the
   .. % % correct dimming for all menu items based on the current front window.


.. function:: Separator(menu)

   メニューの最後にセパレータを追加します。

   .. % % Add a separator to the end of a menu.


.. function:: SubMenu(menu, label)

   *label* の名前のサブメニューを、メニュー *menu* の下に作成しま す。メニューオブジェクトが返されます。

   .. % % Create a submenu named \var{label} under menu \var{menu}. The menu
   .. % % object is returned.


.. function:: Window(parent)

   (モードレス)ウィンドウを作成します。*Parent* は、ウィンドウが属す るアプリケーションオブジェクトです。作成されたウィンドウはまだ表示され ません。

   .. % % Creates a (modeless) window. \var{Parent} is the application object to
   .. % % which the window belongs. The window is not displayed until later.


.. function:: DialogWindow(parent)

   モードレスダイアログウィンドウを作成します。

   .. % % Creates a modeless dialog window.


.. function:: windowbounds(width, height)

   与えた幅と高さのウィンドウを作成するのに必要な、``(left, top, right, bottom)`` からなるタプルを返します。ウィ
   ンドウは以前のウィンドウに対して位置をずらして作成され、全体のウィンド ウが画面からなるべく外れないようにします。しかし、ウィンドウはいつでも
   全く同じサイズで、そのため一部は画面から隠れる場合もあります。

   .. % % Return a \code{(\var{left}, \var{top}, \var{right}, \var{bottom})}
   .. % % tuple suitable for creation of a window of given width and height. The
   .. % % window will be staggered with respect to previous windows, and an
   .. % % attempt is made to keep the whole window on-screen. However, the window will
   .. % % however always be the exact size given, so parts may be offscreen.


.. function:: setwatchcursor()

   マウスカーソルを時計型に設定します。

   .. % % Set the mouse cursor to a watch.


.. function:: setarrowcursor()

   マウスカーソルを矢印型に設定します。

   .. % % Set the mouse cursor to an arrow.


.. _application-objects:

アプリケーションオブジェクト
----------------------------

アプリケーションオブジェクトのメソッドは各種ありますが、次のメソッドを あげておきます。

.. % Application Objects
.. % % Application objects have the following methods, among others:


.. method:: Application.makeusermenus()

   アプリケーションでメニューを使う必要がある場合、このメソッドをオーバー ライドします。属性 :attr:`menubar` にメニューを追加します。

   .. % % Override this method if you need menus in your application. Append the
   .. % % menus to the attribute \member{menubar}.


.. method:: Application.getabouttext()

   このメソッドをオーバーライドすることで、アプリケーションの説明を記述す るテキスト文字列を返します。代わりに、:meth:`do_about` メソッドをオー
   バーライドすれば、もっと凝った"アバウト"メッセージを出す事ができます。

   .. % % Override this method to return a text string describing your
   .. % % application.  Alternatively, override the \method{do_about()} method
   .. % % for more elaborate ``about'' messages.


.. method:: Application.mainloop([mask[, wait]])

   このルーチンがメインイベントループで、作成したアプリケーションが動き出 すためにはこれを呼ぶことになります。*Mask* は操作したいイベントを
   選択するマスクです。 *wait* は並行に動作しているアプリケーションに 割り当てたいチック数(1/60秒)です(デフォルトで 0 ですが、あまり良い値で
   はありません)。*self* フラグを立ててメインループを抜ける方法はまだ サポートされていますが、これはお勧めできません。代わりに
   ``self._quit()``を呼んでください。

   .. % % This routine is the main event loop, call it to set your application
   .. % % rolling. \var{Mask} is the mask of events you want to handle,
   .. % % \var{wait} is the number of ticks you want to leave to other
   .. % % concurrent application (default 0, which is probably not a good
   .. % % idea). While raising \var{self} to exit the mainloop is still
   .. % % supported it is not recommended: call \code{self._quit()} instead.

   イベントループは小さなパーツに分割されていて、各々をオーバーライドでき るようになっています。これらのメソッドは、デフォルトでウィンドウとダイ
   アログや、ドラッグとリサイズの操作、 AppleEvent、非FrameWorkのウィンド
   ウに関するウィンドウの操作などに関するイベントを分岐することなどまで面 倒をみてくれます。

   .. % % The event loop is split into many small parts, each of which can be
   .. % % overridden. The default methods take care of dispatching events to
   .. % % windows and dialogs, handling drags and resizes, Apple Events, events
   .. % % for non-FrameWork windows, etc.

   原則として、全てのイベントハンドラは、イベントが完全に取り扱われた場合 は ``1`` を返さなくてはいけませんし、それ以外では ``0`` を返さな
   くてはいけません(例えば、前面のウィンドウは FrameWork ウィンドウではな い場合を考えてください)。こうしなくてはいけない理由は、アップデートイ
   ベントなどが Sioux コンソールウィンドウなどの他のウィンドウにきちんと渡さ れるようにするためです。*our_dispatch*
   やその呼び出し元の内部から  :func:`MacOS.HandleEvent` を呼んではいけません。そうしたコードが Python
   の内部ループのイベントハンドラを経由して呼ばれると、無限ループ になりかねないからです。

   .. % % In general, all event handlers should return \code{1} if the event is fully
   .. % % handled and \code{0} otherwise (because the front window was not a FrameWork
   .. % % window, for instance). This is needed so that update events and such
   .. % % can be passed on to other windows like the Sioux console window.
   .. % % Calling \function{MacOS.HandleEvent()} is not allowed within
   .. % % \var{our_dispatch} or its callees, since this may result in an
   .. % % infinite loop if the code is called through the Python inner-loop
   .. % % event handler.


.. method:: Application.asyncevents(onoff)

   非同期でイベント操作をしたい場合は、非ゼロの引数でこのメソッドを呼んで ください。こうすることで、イベントが生じた時に、内部のインタプリタのルー
   プで、アプリケーションイベントハンドラ *async_dispatch* が呼ばれる
   ことになります。すると、長時間の計算を行っている場合でも、FrameWorkウィ ンドウがアップデートされ、ユーザーインターフェースが動き続けるようにな
   ります。ただし、インタプリタの動作が減速し、非リエントラントのコード  (例えばFrameWork自身など)に奇妙な動作が見られるかもしれません。デフォル
   トでは *async_dispatch* はすぐに *our_dispatch* を呼びますが、
   このメソッドをオーバーライドすると、特定のイベントを非同期で操作しても 良くなります。処理しないイベントは Sioux などに渡されることになります。

   .. % % Call this method with a nonzero parameter to enable
   .. % % asynchronous event handling. This will tell the inner interpreter loop
   .. % % to call the application event handler \var{async_dispatch} whenever events
   .. % % are available. This will cause FrameWork window updates and the user
   .. % % interface to remain working during long computations, but will slow the
   .. % % interpreter down and may cause surprising results in non-reentrant code
   .. % % (such as FrameWork itself). By default \var{async_dispatch} will immediately
   .. % % call \var{our_dispatch} but you may override this to handle only certain
   .. % % events asynchronously. Events you do not handle will be passed to Sioux
   .. % % and such.

   onあるいはoff値が返されます。

   .. % % The old on/off value is returned.


.. method:: Application._quit()

   実行中の :meth:`mainloop` 呼び出しを、次の適当なタイミングで終了さ せます。

   .. % % Terminate the running \method{mainloop()} call at the next convenient
   .. % % moment.


.. method:: Application.do_char(c, event)

   ユーザーが文字 *c* をタイプした時に呼ばれます。イベントの全詳細は event構造体の中にあります。このメソッドはウィンドウオブジェクト内で使
   うためにも提供されています。このオブジェクトのウィンドウが最前面にある 場合は、アプリケーション全般について本ハンドラをオーバーライドします。

   .. % % The user typed character \var{c}. The complete details of the event
   .. % % can be found in the \var{event} structure. This method can also be
   .. % % provided in a \code{Window} object, which overrides the
   .. % % application-wide handler if the window is frontmost.


.. method:: Application.do_dialogevent(event)

   イベントループ内部で最初に呼ばれて、モードレスダイアログイベントを処理 します。デフォルトではメソッドは単にイベントを適切なダイアログに分岐す
   るだけです(関連したダイアログウィンドウオブジェクトを経由してではあり ません)。特別にダイアログイベント(キーボードショートカットなど)を処理す
   る必要がある場合にオーバーライドしてください。

   .. % % Called early in the event loop to handle modeless dialog events. The
   .. % % default method simply dispatches the event to the relevant dialog (not
   .. % % through the the \code{DialogWindow} object involved). Override if you
   .. % % need special handling of dialog events (keyboard shortcuts, etc).


.. method:: Application.idle(event)

   イベントが無い場合にメインイベントループから呼ばれます。 null イベン トも渡されます(つまりマウス位置などを監視することができます)。

   .. % % Called by the main event loop when no events are available. The
   .. % % null-event is passed (so you can look at mouse position, etc).


.. _window-objects:

ウィンドウオブジェクト
----------------------

ウィンドウオブジェクトは特に次のメソッドを持ちます。

.. % Window Objects
.. % % Window objects have the following methods, among others:


.. method:: Window.open()

   ウィンドウを開く時はこのメソッドをオーバーライドします。MacOS ウィンド ウ ID を :attr:`self.wid` に入れて
   :meth:`do_postopen` メソッドを 呼ぶと、親アプリケーションにウィンドウを登録します。

   .. % % Override this method to open a window. Store the MacOS window-id in
   .. % % \member{self.wid} and call the \method{do_postopen()} method to
   .. % % register the window with the parent application.


.. method:: Window.close()

   ウィンドウを閉じるときに特別な処理をする場合はこのメソッドをオーバーラ イドします。親アプリケーションからウィンドウの登録を削除するには、
   :meth:`do_postclose` を呼びます。

   .. % % Override this method to do any special processing on window
   .. % % close. Call the \method{do_postclose()} method to cleanup the parent
   .. % % state.


.. method:: Window.do_postresize(width, height, macoswindowid)

   ウィンドウがリサイズされた後に呼ばれます。``InvalRect`` を呼び出す 以外にもすることがある場合はこれをオーバーライドします。

   .. % % Called after the window is resized. Override if more needs to be done
   .. % % than calling \code{InvalRect}.


.. method:: Window.do_contentclick(local, modifiers, event)

   ウィンドウのコンテント部分をユーザーがクリックすると呼ばれます。引数は 位置座標(ウィンドウを基準)、キーモディファイア、生のイベントです。

   .. % % The user clicked in the content part of a window. The arguments are
   .. % % the coordinates (window-relative), the key modifiers and the raw
   .. % % event.


.. method:: Window.do_update(macoswindowid, event)

   ウィンドウのアップデートイベントが受信された時に呼ばれます。ウィンドウ を再描画します。

   .. % % An update event for the window was received. Redraw the window.


.. method:: Window.do_activate(activate, event)

   ウィンドウがアクティブ化(``activate == 1``)、非アクティブ化 (``activate == 0``)する際に呼ばれます。フォーカスのハイライト
   などを処理します。

   .. % % The window was activated (\code{\var{activate} == 1}) or deactivated
   .. % % (\code{\var{activate} == 0}). Handle things like focus highlighting,
   .. % % etc.


.. _controlswindow-object:

コントロールウィンドウオブジェクト
----------------------------------

コントロールウィンドウオブジェクトには ``Window`` オブジェクトのメ ソッドの他に次のメソッドがあります。

.. % ControlsWindow Object
.. % % ControlsWindow objects have the following methods besides those of
.. % % \code{Window} objects:


.. method:: ControlsWindow.do_controlhit(window, control, pcode, event)

   コントロール *control* のパートコード *pcode* がユーザーにヒットされた 場合に呼ばれます。トラッキングなどは任せておいてかまいません。

   .. % % Part \var{pcode} of control \var{control} was hit by the
   .. % % user. Tracking and such has already been taken care of.


.. _scrolledwindow-object:

スクロールウィンドウオブジェクト
--------------------------------

スクロールウィンドウオブジェクトは、次のメソッドを追加したコントロール ウィンドウオブジェクトです。

.. % ScrolledWindow Object
.. % % ScrolledWindow objects are ControlsWindow objects with the following
.. % % extra methods:


.. method:: ScrolledWindow.scrollbars([wantx[, wanty]])

   水平スクロールバーと垂直スクロールバーを作成します(あるいは破棄します)。 引数はどちらが欲しいか指定します(デフォルトは両方)。スクロールバーは常 に最小値
   ``0`` 、最大値 ``32767`` です。

   .. % % Create (or destroy) horizontal and vertical scrollbars. The arguments
   .. % % specify which you want (default: both). The scrollbars always have
   .. % % minimum \code{0} and maximum \code{32767}.


.. method:: ScrolledWindow.getscrollbarvalues()

   このメソッドは必ず作っておかなくてはいけません。現在のスクロールバーの 位置を与えるタプル ``(x, y)`` を(``0`` の  ``32767``
   間で)返してください。バーの方向について全文書が可視状態で あること知らせるため ``None`` を返す事もできます。

   .. % % You must supply this method. It should return a tuple \code{(\var{x},
   .. % % \var{y})} giving the current position of the scrollbars (between
   .. % % \code{0} and \code{32767}). You can return \code{None} for either to
   .. % % indicate the whole document is visible in that direction.


.. method:: ScrolledWindow.updatescrollbars()

   文書に変更があった場合はこのメソッドを呼びます。このメソッドは :meth:`getscrollbarvalues` を呼んでスクロールバーを更新します。

   .. % % Call this method when the document has changed. It will call
   .. % % \method{getscrollbarvalues()} and update the scrollbars.


.. method:: ScrolledWindow.scrollbar_callback(which, what, value)

   あらかじめ与えておくメソッドで、ユーザーとの対話により呼ばれます。  *which* は ``'x'`` か ``'y'`` 、*what*は ``'-'``,
   ``'--'``, ``'set'``,``'++'``,  ``'+'``のどれかです。 ``'set'``
   の場合は、*value*に新しいスクロールバー位置を入れてお きます。

   .. % % Supplied by you and called after user interaction. \var{which} will
   .. % % be \code{'x'} or \code{'y'}, \var{what} will be \code{'-'},
   .. % % \code{'--'}, \code{'set'}, \code{'++'} or \code{'+'}. For
   .. % % \code{'set'}, \var{value} will contain the new scrollbar position.


.. method:: ScrolledWindow.scalebarvalues(absmin, absmax, curmin, curmax)

   :meth:`getscrollbarvalues` の結果から値を計算するのを助ける補助的な
   メソッドです。文書の最小値と最大値、可視部分に関する最先頭値(最左値)と 最底値(最右値)を渡すと、正しい数か ``None`` を返します。

   .. % % Auxiliary method to help you calculate values to return from
   .. % % \method{getscrollbarvalues()}. You pass document minimum and maximum value
   .. % % and topmost (leftmost) and bottommost (rightmost) visible values and
   .. % % it returns the correct number or \code{None}.


.. method:: ScrolledWindow.do_activate(onoff, event)

   ウィンドウが最前面になった時、スクロールバーのディム(dimming)/ハイライ トの面倒をみます。このメソッドをオーバーライドするなら、オーバーライド
   したメソッドの最後でオリジナルのメソッドを呼んでください。

   .. % % Takes care of dimming/highlighting scrollbars when a window becomes
   .. % % frontmost. If you override this method, call this one at the end of
   .. % % your method.


.. method:: ScrolledWindow.do_postresize(width, height, window)

   スクロールバーを正しい位置に移動させます。オーバーライドする時は、オー バーライドしたメソッドの一番最初でオリジナルのメソッドを呼んでください。

   .. % % Moves scrollbars to the correct position. Call this method initially
   .. % % if you override it.


.. method:: ScrolledWindow.do_controlhit(window, control, pcode, event)

   スクロールバーのインタラクションを処理します。これをオーバーライドする 時は、オリジナルのメソッドを最初に呼び出してください。非ゼロの返り値は
   スクロールバー内がヒットされたことを意味し、実際に処理が進むことになり ます。

   .. % % Handles scrollbar interaction. If you override it call this method
   .. % % first, a nonzero return value indicates the hit was in the scrollbars
   .. % % and has been handled.


.. _dialogwindow-objects:

ダイアログウィンドウオブジェクト
--------------------------------

ダイアログウィンドウオブジェクトには、``Window`` オブジェクトのメソッ ドの他に次のメソッドがあります。

.. % DialogWindow Objects
.. % % DialogWindow objects have the following methods besides those of
.. % % \code{Window} objects:


.. method:: DialogWindow.open(resid)

   ID *resid* の DLOG リソースからダイアログウィンドウを作成します。 ダイアログオブジェクトは :attr:`self.wid` に保存されます。

   .. % % Create the dialog window, from the DLOG resource with id
   .. % % \var{resid}. The dialog object is stored in \member{self.wid}.


.. method:: DialogWindow.do_itemhit(item, event)

   アイテム番号 *item* がヒットされた時に呼ばれます。トグルボタンなど の再描画は自分で処理してください。

   .. % % Item number \var{item} was hit. You are responsible for redrawing
   .. % % toggle buttons, etc.

