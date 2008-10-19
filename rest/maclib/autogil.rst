
:mod:`autoGIL` --- イベントループ中のグローバルインタープリタの取り扱い
=============================================

.. module:: autoGIL
   :platform: Mac
   :synopsis: イベントループ中のグローバルインタープリタの取り扱い
.. moduleauthor:: Just van Rossum <just@letterror.com>


.. % Global Interpreter Lock handling in event loops
.. % Global Interpreter Lock handling in event loops.

:mod:`autoGIL`モジュールは、自動的にイベントループを実行する場合 、 Python のグローバルインタープリタをロックしたり、ロックの解除をした
りするための関数 :func:`installAutoGIL` を提供します。

.. % % The \module{autoGIL} module provides a function \function{installAutoGIL} that
.. % % automatically locks and unlocks Python's Global Interpreter Lock
.. % % when running an event loop.


.. exception:: AutoGILError

   例えば現在のスレッドがループしていないなど、オブザーバにコールバックが できない場合に発生します。

   .. % % Raised if the observer callback cannot be installed, for example because
   .. % % the current thread does not have a run loop.


.. function:: installAutoGIL()

   現在のスレッドのイベントループ(CFRunLoop)中のオブザーバにコールバッ クを行ない、適切な時にグローバルインタープリタロック(GIL)を、イ
   ベントループが使用されていない間、他の Python スレッドの起動がで きるようにロックしたり、ロックの解除をしたりします。

   .. % %     Install an observer callback in the event loop (CFRunLoop) for the
   .. % %     current thread, that will lock and unlock the Global Interpreter Lock
   .. % %     (GIL) at appropriate times, allowing other Python threads to run while
   .. % %     the event loop is idle.

   有効性：OSX 10.1以降

   .. % % Availability: OSX 10.1 or later.

