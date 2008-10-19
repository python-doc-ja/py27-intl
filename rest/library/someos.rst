.. % \chapter{Optional Operating System Services}


.. _someos:

**********************
オプションのオペレーティングシステムサービス
**********************

この章で説明するモジュールでは、 特定のオペレーティングシステムでだけ利用できる オペレーティングシステム機能へのインターフェースを提供します。
このインターフェースは、 おおむね Unix や C のインターフェースにならってモデル化してありますが、
他のシステム上（WindowsやNTなど）でも利用できることがあります。 次に概要を示します。

.. % The modules described in this chapter provide interfaces to operating
.. % system features that are available on selected operating systems only.
.. % The interfaces are generally modeled after the \UNIX{} or \C{}
.. % interfaces but they are available on some other systems as well
.. % (e.g. Windows or NT).  Here's an overview:


.. toctree::

   select.rst
   thread.rst
   threading.rst
   dummy_thread.rst
   dummy_threading.rst
   mmap.rst
   readline.rst
   rlcompleter.rst
