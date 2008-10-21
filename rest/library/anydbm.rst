
:mod:`anydbm` ---  DBM 形式のデータベースへの汎用アクセスインタフェース
=======================================================================

.. module:: anydbm
   :synopsis: DBM 形式のデータベースモジュールに対する汎用インタフェース。


.. index::
   module: bsddb
   module: dbhash
   module: gdbm
   module: dbm
   module: dumbdbm

:mod:`anydbm` は種々の DBM データベース ---  (:mod:`bsddb` を使う)  :mod:`dbhash` 、
:mod:`gdbm`、および :mod:`dbm` --- への汎用インタフェースです。 これらのモジュールがどれもインストールされていない場合、
:mod:`dumbdbm` モジュールの 低速で単純な DBM 実装が使われます。


.. function:: open(filename[, flag[, mode]])

   データベースファイル *filename* を開き、対応するオブジェクトを 返します。

   データベースファイルがすでに存在する場合、:mod:`whichdb` モジュール を使ってファイルタイプが判定され、適切なモジュールが使われます;
   既存のデータベースファイルが存在しなかった場合、上に挙げたモジュール中で 最初にインポートすることができたものが使われます。

   オプションの *flag* は 既存のデータベースを読み込み専用で開く ``'r'``、  既存のデータベースを読み書き用に開く ``'w'``、
   既存のデータベースが存在しない場合には新たに作成する ``'c'``、および 常に新たにデータベースを作成する ``'n'`` をとることができます。
   この引数が指定されない場合、標準の値は ``'r'`` になります。

   オプションの *mode* 引数は、新たにデータベースを作成しなければならない 場合に使われる Unix のファイルモードです。標準の値は 8 進数の
   ``0666`` です (この値は現在有効な umask で修飾されます)。


.. exception:: error

   サポートされているモジュールのどれかによって送出されうる例外が 収められるタプルで、先頭の要素は :exc:`anydbm.error` になって います
   --- :exc:`anydbm.error` が送出された場合、後者が使われます。

:func:`open` によって返されたオブジェクトは辞書とほとんど同じ 同じ機能をサポートします; キーとそれに対応付けられた値を
記憶し、引き出し、削除することができ、:meth:`has_key` および :meth:`keys` メソッドを使うことができます。キーおよび値は
常に文字列です。

以下の例ではホスト名と対応するタイトルがいくつか登録し、データベースの 内容を表示します::

   import anydbm

   # データベースを開く、必要なら作成する
   db = anydbm.open('cache', 'c')

   # いくつかの値を設定する
   db['www.python.org'] = 'Python Website'
   db['www.cnn.com'] = 'Cable News Network'

   # 内容についてループ。
   # .keys(), .values() のような他の辞書メソッドもつかえます。
   for k, v in db.iteritems():
       print k, '\t', v

   # 文字列でないキーまたは値は例外を
   # おこします（ほとんどのばあい TypeErrorです)。
   db['www.yahoo.com'] = 4

   # 終了したらcloseします。
   db.close()


.. seealso::

   Module :mod:`dbhash`
      BSD ``db`` データベースインタフェース。

   Module :mod:`dbm`
      標準の Unix データベースインタフェース。

   Module :mod:`dumbdbm`
      ``dbm`` インタフェースの移植性のある実装。

   Module :mod:`gdbm`
      ``dbm`` インタフェースに基づいた GNU データベースインタフェース。

   Module :mod:`shelve`
      Python ``dbm`` インタフェース上に構築された 汎用オブジェクト永続化機構。

   Module :mod:`whichdb`
      既存のデータベースがどの形式のデータベースか判定する ユーティリティモジュール。

