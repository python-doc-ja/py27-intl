
:mod:`dummy_thread` --- :mod:`thread` の代替モジュール
==============================================

.. module:: dummy_thread
   :synopsis: thread の代替モジュール。


このモジュールは :mod:`thread` モジュールのインターフェースをそっ くりまねるものです。:mod:`thread` モジュールがサポートされていな
いプラットフォームで import することを意図して作られたものです。

使用例::

   try:
       import thread as _thread
   except ImportError:
       import dummy_thread as _thread

生成するスレッドが、他のブロックしたスレッドを待ち、デッドロック発生の 可能性がある場合には、このモジュールを使わないようにしてください。ブロッ キング I/O
を使っている場合によく起きます。

