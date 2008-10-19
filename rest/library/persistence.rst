
.. _persistence:

*******
データの永続化
*******

この章で解説されるモジュール群は Python データをディスクに永続的な形式 で保存します。 モジュール :mod:`pickle` と モジュール
:mod:`marshal` は 多くの Python データ型をバイト列に変換し、バイト列から再生成します。 様々な
DBM関連モジュールはハッシュを基にした、文字列から他の文字列へのマッ プを保存するファイルフォーマット群をサポートします。 モジュール
:mod:`bsddb` はディスクベースの文字列から文字列へのマッピ ングを、ハッシュ、B-Tree, レコードを基にしたフォーマットで提供します。

この章で説明されるモジュールは:


.. toctree::

   pickle.rst
   copy_reg.rst
   shelve.rst
   marshal.rst
   anydbm.rst
   whichdb.rst
   dbm.rst
   gdbm.rst
   dbhash.rst
   bsddb.rst
   dumbdbm.rst
   sqlite3.rst
