
:mod:`Queue` --- 同期キュークラス
=================================

.. module:: Queue
   :synopsis: 同期キュークラス


:mod:`Queue`モジュールは、多生産者-多消費者FIFOキューを実装します。 これは、複数のスレッドの間で情報を安全に交換しなければならないときの
スレッドプログラミングで特に有益です。 このモジュールの:class:`Queue`クラスは、 必要なすべてのロックセマンティクスを実装しています。
これはPythonのスレッドサポートの状況に依存します。

:mod:`Queue`モジュールは以下のクラスと例外を定義します:


.. class:: Queue(maxsize)

   クラスのコンストラクタです。 *maxsize*はキューに置くことのできる要素数の上限を設定する整数です。
   いったんこの大きさに達したら、挿入はキューの要素が消費されるまでブロック されます。 もし*maxsize*が0以下であるならば、キューの大きさは無限です。


.. exception:: Empty

   空な:class:`Queue`オブジェクトで、 非ブロックメソッドとして:meth:`get`\ (または:meth:`get_nowait`)
   が呼ばれたとき、送出される例外です。


.. exception:: Full

   満杯な:class:`Queue`オブジェクトで、 非ブロックメソッドとして:meth:`put`\ (または:meth:`put_nowait`)
   が呼ばれたとき、送出される例外です。


.. _queueobjects:

キューオブジェクト
------------------

クラス:class:`Queue`はキューオブジェクトを実装しており、 以下のメソッドを持っています。
このクラスは、他のキュー構造(例えばスタック)を実装するために 派生させられるますが、継承可能なインタフェースはここでは説明しません。
詳しいことはソースコードを見てください。 公開メソッドは次のものです:


.. method:: Queue.qsize()

   キューの大まかなサイズを返します。 マルチスレッドセマンティクスにおいて、この値は信頼できません。


.. method:: Queue.empty()

   キューが空なら``True``を返し、そうでないなら``False``を返します。 マルチスレッドセマンティクスにおいて、この値は信頼できません。


.. method:: Queue.full()

   キューが満杯なら``True``を返し、そうでないなら``False``を返します。 マルチスレッドセマンティクスにおいて、この値は信頼できません。


.. method:: Queue.put(item[, block[, timeout]])

   *item*をキューに入れます。 もしオプション引数*block*がTrueで*timeout*がNone(デフォルト)ならば、
   フリースロットが利用可能になるまでブロックします。 *timeout*が正の値の場合、最大で*timeout*秒間ブロックし、
   その時間内に空きスロットが利用可能にならなければ、 例外:exc:`Full`を送出します。
   他方(*block*がFalse)、直ちにフリースロットが利用できるならば、 キューにアイテムを置きます。できないならば、例外:exc:`Full`を送出します
   (この場合*timeout*は無視されます)。

   .. versionadded:: 2.3
      the timeout parameter.


.. method:: Queue.put_nowait(item)

   ``put(item, False)``と同じ意味です。


.. method:: Queue.get([block[, timeout]])

   キューからアイテムを取り除き、それを返します。 もしオプション引数*block*がTrueで*timeout*がNone(デフォルト)ならば、
   アイテムが利用可能になるまでブロックします。 もし*timeout*が正の値の場合、最大で*timeout*秒間ブロックし、
   その時間内でアイテムが利用可能にならなければ、 例外:exc:`Empty`を送出します。
   他方(*block*がFalse)、直ちにアイテムが利用できるならば、 それを返します。できないならば、例外:exc:`Empty`を送出します
   (この場合*timeout*は無視されます)。

   .. versionadded:: 2.3
      the timeout parameter.


.. method:: Queue.get_nowait()

   ``get(False)``と同じ意味です。

キューに入れられたタスクが全て消費者スレッドに処理されたかどうかを追跡するために 2つのメソッドが提供されます。


.. method:: Queue.task_done()

   過去にキューに入れられたタスクが完了した事を示します。 キューの消費者スレッドに利用されます。 タスクの取り出しに使われた、各 :meth:`get`
   に対して、それに続く :meth:`task_done` の 呼び出しは、取り出したタスクに対する処理が完了した事をキューに教えます。

   :meth:`join` がブロックされていた場合、全itemが処理された (キューに:meth:`put`された全てのitemに対して
   :meth:`task_done` が呼び出されたことを 意味します) 時に復帰します。

   キューにあるよりitemの個数よりも多く呼び出された場合、 :exc:`ValueError` が送出されます。

   .. versionadded:: 2.5


.. method:: Queue.join()

   キューの中の全アイテムが処理される間でブロックします。

   キューにitemが追加される度に、未完了タスクカウントが増やされます。 消費者スレッドが :meth:`task_done`
   を呼び出して、itemを受け取ってそれに 対する処理が完了した事を知らせる度に、未完了タスクカウントが減らされます。
   未完了タスクカウントが0になったときに、join() のブロックが解除されます。

   .. versionadded:: 2.5

キューに入れたタスクが完了するのを待つ例::

   def worker(): 
       while True: 
           item = q.get() 
           do_work(item) 
           q.task_done() 

   q = Queue() 
   for i in range(num_worker_threads): 
        t = Thread(target=worker)
        t.setDaemon(True)
        t.start() 

   for item in source():
       q.put(item) 

   q.join()       # 全タスクが完了するまでブロック

