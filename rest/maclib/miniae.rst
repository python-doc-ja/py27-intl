
:mod:`MiniAEFrame` --- オープンスクリプティングアーキテクチャサーバのサポート
==================================================

.. module:: MiniAEFrame
   :platform: Mac
   :synopsis: オープンスクリプティングアーキテクチャ(OSA)サーバ("Apple Events")のサポート。


.. index::
   single: Open Scripting Architecture
   single: AppleEvents
   module: FrameWork

:mod:`MiniAEFrame`モジュールは、アプリケーションにオープンスクリプ ティングアーキテクチャ(OSA)サーバ機
能を持たせるためのフレームワークを提供します。つまり、 AppleEventsの受信と処理を行わせます。
:mod:`FrameWork`と連携させても良いし、単独 でも使えます。
実例として、このモジュールは:program:`PythonCGISlave`の中で使われていま す。

:mod:`MiniAEFrame`には以下のクラスが定義されています。


.. class:: AEServer()

   AppleEventの分岐を処理するクラス。作成するアプリケーションはこのクラス
   と、:class:`MiniApplication`あるいは:class:`FrameWork.Application`のサブク
   ラスでなければなりません。サブクラス化したクラスでは:meth:`__init__`
   メソッドで、継承した両方のクラスの:meth:`__init__`メソッドを呼びださ なければなりません。


.. class:: MiniApplication()

   :class:`FrameWork.Application`とある程度互換なクラスですが、機能は少ない
   です。このクラスのイベントループはアップルメニュー、Cmd-.(コマンドキーを押しながらピリオド.を押す)、
   AppleEventをサポートします。他のイベントはPythonインタープリタかSioux（CodeWarriorの
   コンソールシステム）に渡されます。作成するアプリケーションで :class:`AEServer`を使いたいが、独自のウィンドウなどを持たない場合に便利で す。


.. _aeserver-objects:

AEServer オブジェクト
---------------


.. method:: AEServer.installaehandler(classe, type, callback)

   AppleEventハンドラをインストールします。*classe*と*type*は4文字
   のOSAクラスとタイプの指定子で、ワイルドカード``'****'``も使えます。対
   応するAppleEventを受けるとパラメータがデコードされ、与えたコールバックが 呼び出されます。


.. method:: AEServer.callback(_object, **kwargs)

   与えたコールバックは、OSAダイレクトオブジェクトを1番目のパラメータとして 呼び出されます。他のパラメータは4文字の指定子を名前にしたキーワード引数
   として渡されます。他に3つのキーワード・パラメータが渡されます。つまり、
   ``_class``と``_type``はクラスとタイプ指定子で、``_attributes`` はAppleEvent属性を持つ辞書です。

   与えたメソッドの返り値は:func:`aetools.packevent`でパックされ、リプ ライとして送られます。

現在のクラス設計にはいくつか重大な問題があることに注意してください。引数 に名前ではない4文字の指定子を持つAppleEventはまだ実装されていないし、イ
ベントの送信側にエラーを返すこともできません。この問題は将来のリリースま で先送りにされています。

