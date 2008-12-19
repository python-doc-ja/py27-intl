
.. _allos:

************************************
汎用オペレーティングシステムサービス
************************************

本章に記述されたモジュールは、ファイルの取り扱いや時間計測のような(ほ ぼ)すべてのオペレーティングシステムで利用可能な機能にインターフェー
スを提供します。これらのインターフェースは、UnixもしくはCのインター フェースを基に作られますが、ほとんどの他のシステムで同様に利用可能です。
概要を以下に記述します。

.. % The modules described in this chapter provide interfaces to operating
.. % system features that are available on (almost) all operating systems,
.. % such as files and a clock.  The interfaces are generally modeled
.. % after the \UNIX{} or C interfaces, but they are available on most
.. % other systems as well.  Here's an overview:


.. toctree::

   os.rst
   time.rst
   optparse.rst
   getopt.rst
   logging.rst
   getpass.rst
   curses.rst
   curses.ascii.rst
   curses.panel.rst
   platform.rst
   errno.rst
   ctypes.rst
