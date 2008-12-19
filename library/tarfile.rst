
:mod:`tarfile` --- tar アーカイブファイルを読み書きする
=======================================================

.. module:: tarfile
   :synopsis: tar-形式のアーカイブファイルを読み書きします。


.. versionadded:: 2.3

.. moduleauthor:: Lars Gustäbel <lars@gustaebel.de>
.. sectionauthor:: Lars Gustäbel <lars@gustaebel.de>


:mod:`tarfile` モジュールは、tar アーカイブを読んで作成することができるようにします。 いくつかの事実と外観：

* :mod:`gzip` と :mod:`bzip2` で圧縮されたアーカイブを読み書きします。

* POSIX 1003.1-1990 準拠あるいは GNU tar 互換のアーカイブを作成します。

* GNU tar 拡張機能 *長い名前*、 *longlink* および *sparse* を読みます。

* GNU tar 拡張機能を使って、無制限長さのパス名を保存します。

* ディレクトリ、普通のファイル、ハードリンク、シンボリックリンク、fifo、 キャラクタデバイスおよびブロックデバイスを処理します。また、タイムスタンプ、
  アクセス許可およびオーナーのようなファイル情報の取得および保存が可能です。

* テープデバイスを取り扱うことができます。


.. function:: open([name[, mode [, fileobj[, bufsize]]]])

   パス名 *name*に :class:`TarFile` オブジェクトを返します。 :class:`TarFile` オブジェクトに関する詳細な情報については、
   TarFile オブジェクト (セクション :ref:`tarfile-objects`)を見て下さい。

   *mode* は ``'filemode[:compression]'`` の形式をとる文字列で なければなりません．デフォルトの値は ``'r'``
   です．以下に *mode*のとりうる組み合わせ全てを示します．

   +----------------------+------------------------------------------------------+
   | mode                 | 動作                                                 |
   +======================+======================================================+
   | ``'r' または 'r:*'`` | 透過な圧縮つきで読み込むためにオープンします(推奨)。 |
   +----------------------+------------------------------------------------------+
   | ``'r:'``             | 圧縮なしで排他的に読み込むためにオープンします。     |
   +----------------------+------------------------------------------------------+
   | ``'r:gz'``           | gzip 圧縮で読み込むためにオープンします。            |
   +----------------------+------------------------------------------------------+
   | ``'r:bz2'``          | bzip2 圧縮で読み込むためにオープンします。           |
   +----------------------+------------------------------------------------------+
   | ``'a' または 'a:'``  | 圧縮なしで追加するためにオープンします。             |
   +----------------------+------------------------------------------------------+
   | ``'w' または 'w:'``  | 非圧縮で書き込むためにオープンします。               |
   +----------------------+------------------------------------------------------+
   | ``'w:gz'``           | gzip 圧縮で書き込むためにオープンします。            |
   +----------------------+------------------------------------------------------+
   | ``'w:bz2'``          | bzip2 圧縮で書き込むためにオープンします。           |
   +----------------------+------------------------------------------------------+

   ``'a:gz'`` あるいは ``'a:bz2'``は可能ではないことに注意して下さい。 もし
   *mode*が、ある(圧縮した)ファイルを読み込み用にオープンするのに、 適していないなら、:exc:`ReadError`が発生します。これを防ぐには
   *mode* ``'r'`` を使って下さい。もし圧縮メソッドが サポートされていなければ、 :exc:`CompressionError` が発生します。

   もし *fileobj*が指定されていれば、それは *name*でオープンされた ファイルオブジェクトの代替として使うことができます。

   特別な目的のために、*mode*の2番目の形式: ``'ファイルモード|[圧縮]'`` があります。この形式を使うと，
   ``open``が返すのはデータをブロックからなるストリームとして扱う :class:`TarFile` オブジェクトになります．この場合，ファイルに対して
   ランダムな seek を行えなくなります．*fileobj* を指定する場合， ``read()``および``write()``
   メソッドを持つ任意のオブジェクトに できます． *bufsize* にはブロックサイズを指定します．デフォルトは ``20 * 512``
   バイトです。``sys.stdin`` ，ソケットファイル オブジェクト，テーブデバイスと組み合わせる場合にはこの形式を
   使ってください．ただし，このような:class:`TarFile` オブジェクトには ランダムアクセスを行えないという制限があります． 例 (セクション
   :ref:`tar-examples`)を参照してください。 現在可能なモードは：

   +-------------+-----------------------------------------------------------------+
   | モード      | 動作                                                            |
   +=============+=================================================================+
   | ``'r|*'``   | tar ブロックの *ストリーム* を透過な読み込みにオープンします。  |
   +-------------+-----------------------------------------------------------------+
   | ``'r|'``    | 非圧縮 tar ブロックの *ストリーム* を読み込みにオープンします。 |
   +-------------+-----------------------------------------------------------------+
   | ``'r|gz'``  | gzip 圧縮 *ストリーム*を読み込みにオープンします。              |
   +-------------+-----------------------------------------------------------------+
   | ``'r|bz2'`` | bzip2 圧縮 *ストリーム* を読み込みにオープンします。            |
   +-------------+-----------------------------------------------------------------+
   | ``'w|'``    | 非圧縮 *ストリーム*を書き込みにオープンします。                 |
   +-------------+-----------------------------------------------------------------+
   | ``'w|gz'``  | gzip 圧縮 *ストリーム* を書き込みにオープンします。             |
   +-------------+-----------------------------------------------------------------+
   | ``'w|bz2'`` | bzip2 圧縮 *ストリーム*を書き込みにオープンします。             |
   +-------------+-----------------------------------------------------------------+


.. class:: TarFile

   tar アーカイブを読んだり、書いたりするためのクラスです。このクラスを 直接使わず，代わりに :func:`open` を使ってください．
   :class:`TarFile` オブジェクト (:ref:`tarfile-objects` 節) を参照 してください．


.. function:: is_tarfile(name)

   もし *name*が tar アーカイブファイルであり，:mod:`tarfile` モジュールで読み出せる場合に:const:`True`を返します．


.. class:: TarFileCompat(filename[, mode[, compression]])

   ``zipfile``\ -風なインターフェースを持つ tar アーカイブへの 制限されたアクセスのためのクラスです。詳細は
   ``zipfile``のドキュメントを参照してください． *compression* は、以下の定数のどれかでなければなりません：


   .. data:: TAR_PLAIN

      非圧縮 tar アーカイブのための定数。


   .. data:: TAR_GZIPPED

      :mod:`gzip`圧縮 tar アーカイブのための定数。


.. exception:: TarError

   すべての :mod:`tarfile` 例外のための基本クラスです。


.. exception:: ReadError

   tar アーカイブがオープンされた時、:mod:`tarfile` モジュールで操作 できないか、あるいは何か無効であるとき発生します。


.. exception:: CompressionError

   圧縮方法がサポートされていないか、あるいはデータを正しくデコードできない 時に発生します。


.. exception:: StreamError

   ストリーム風の :class:`TarFile` オブジェクトで典型的な制限の ために発生します。


.. exception:: ExtractError

   :meth:`extract`を使った時、もし:attr:`TarFile.errorlevel`\ ``== 2`` の *フェータルでない*
   エラーに対してだけ発生します。


.. seealso::

   Module :mod:`zipfile`
      :mod:`zipfile` 標準モジュールのドキュメント。

   `GNU tar マニュアル, 基本 Tar 形式 <http://www.gnu.org/software/tar/manual/html_node/tar_134.html#SEC134>`_
      GNU tar 拡張機能を含む、 tar アーカイブファイルのためのドキュメント。

.. % -----------------
.. % TarFile オブジェクト
.. % -----------------


.. _tarfile-objects:

TarFile オブジェクト
--------------------

:class:`TarFile` オブジェクトは、tar アーカイブへのインターフェースを提供します。 tar
アーカイブは一連のブロックです。アーカイブメンバー(保存されたファイル)は、 ヘッダーブロックとそれに続くデータブロックから構成されています。ある tar
アーカイブに ファイルを何回も保存することができます。各アーカイブメンバーは、 :class:`TarInfo`
オブジェクトによって表わされます、詳細については TarInfo オブジェクト (セクション :ref:`tarinfo-objects`)を見て下さい。


.. class:: TarFile([name [, mode[, fileobj]]])

   *(非圧縮の)* tar アーカイブ *name*をオープンします。 *mode* は、既存のアーカイブから読み込むには ``'r'`` 、
   既存のファイルにデータを追加するには ``'a'``、あるいは既存のファイルを 上書きして新しいファイルを作成するには ``'w'``
   のどれかです。*mode* のデフォールトは ``'r'``です。

   もし *fileobj*が与えられていれば、それを使ってデータを読み書きします。 もしそれが決定できれば、*mode*は *fileobj*
   のモードで上書きされます。.

   .. note::

      *fileobj* は、:class:`TarFile`をクローズする時は、クローズされません。


.. method:: TarFile.open(...)

   代替コンストラクタです。モジュールレベルでの :func:`open` 関数は、 実際はこのクラスメソッドへのショートカットです。詳細については セクション
   :ref:`module-tarfile` を見て下さい。


.. method:: TarFile.getmember(name)

   メンバー *name* に対する :class:`TarInfo` オブジェクトを返します。 もし
   *name*がアーカイブに見つからなければ、:exc:`KeyError`が発生します。

   .. note::

      もしメンバーがアーカイブに1つ以上あれば、その最後に出現する ものが、最新のバージョンであるとみなされます。


.. method:: TarFile.getmembers()

   :class:`TarInfo` オブジェクトのリストとしてアーカイブのメンバーを返します。 このリストはアーカイブ内のメンバーと同じ順番です。


.. method:: TarFile.getnames()

   メンバーをその名前のリストとして返します。これは :meth:`getmembers`で返されるリストと同じ順番です。


.. method:: TarFile.list(verbose=True)

   コンテンツの表を ``sys.stdout`` に印刷します。もし *verbose* が :const:`False`
   であれば、メンバー名のみ印刷します。もしそれが :const:`True` であれば、``"ls -l"`` に似た出力を生成します．


.. method:: TarFile.next()

   :class:`TarFile`が読み込み用にオープンされている時、 アーカイブの次のメンバーを
   :class:`TarInfo`オブジェクトとして返します。もしそれ以上利用可能なものがなければ、 ``None`` を返します。


.. method:: TarFile.extractall([path[, members]])

   全てのメンバーをアーカイブから現在の作業ディレクトリーまたは *path* に 抽出します。オプションの *members* が与えられるときには、
   :meth:`getmembers` で返されるリストの一部でなければなりません。
   所有者、変更時刻、許可のようなディレクトリー情報は全てのメンバーが抽出された後に セットされます。これは二つの問題を回避するためです。一つはディレクトリー
   の変更時刻はその中にファイルが作成されるたびにリセットされるということ。 もう一つは、ディレクトリーに書き込み許可がなければその中のファイル抽出は
   失敗してしまうということです。

   .. versionadded:: 2.5


.. method:: TarFile.extract(member[, path])

   メンバーをアーカイブから現在の作業ディレクトリに、そのフル名を使って、 抽出します。そのファイル情報はできるだけ正確に 抽出されます。
   *member*は、ファイル名でも:class:`TarInfo` オブジェクトでも構いません。
   *path*を使って、異なるディレクトリを指定することができます。

   .. note::

      :meth:`extract` メソッドでは tar アーカイブにランダムアクセス することが許されるので、これを使う場合には使用者自身が気をつけな
      ければならない問題があります。上の :meth:`extractall` の説明を 参照してください。


.. method:: TarFile.extractfile(member)

   アーカイブからメンバーをオブジェクトとして抽出します。 *member*は、ファイル名あるいは :class:`TarInfo` オブジェクトです。 もし
   *member*が普通のファイルであれば、ファイル風のオブジェクトを返します。 もし
   *member*がリンクであれば、ファイル風のオブジェクトをリンクのターゲットから 構成します。 もし *member*が上のどれでもなければ、``None``
   が返されます。

   .. note::

      ファイル風のオブジェクトは読み出し専用で以下のメソッドを提供します： :meth:`read`, :meth:`readline`,
      :meth:`readlines`, :meth:`seek`, :meth:`tell`.


.. method:: TarFile.add(name[, arcname[, recursive]])

   ファイル *name*をアーカイブに追加します。*name* は、任意のファイルタイプ (ディレクトリ、fifo、シンボリックリンク等)です。
   もし*arcname* が与えられていれば、それはアーカイブ内のファイルの代替名を 指定します。デフォールトではディレクトリは再帰的に追加されます。
   これは、*recursive* を :const:`False` に設定することで 避けることができます。デフォルトは :const:`True` です．


.. method:: TarFile.addfile(tarinfo[, fileobj])

   :class:`TarInfo`オブジェクト*tarinfo*をアーカイブに追加します。 もし *fileobj*
   が与えられていれば、``tarinfo.size``  バイトがそれから読まれ、 アーカイブに追加されます。:meth:`gettarinfo`を使って
   :class:`TarInfo` オブジェクトを作成することができます。

   .. note::

      Windows プラットフォームでは、*fileobj*は、ファイルサイズに関する問題を避けるために、 常に、モード ``'rb'``
      でオープンされるべきです。


.. method:: TarFile.gettarinfo([name[, arcname [, fileobj]]])

   :class:`TarInfo`オブジェクトをファイル *name* あるいは (そのファイル記述子に ``os.fstat()``を使って)
   ファイルオブジェクト*fileobj*の どちらか用に作成します。 :class:`TarInfo`の属性のいくつかは、
   :meth:`addfile`を使って追加する前に修正することができます。 *arcname*がもし与えられていれば、アーカイブ内のファイルの
   代替名を指定します。


.. method:: TarFile.close()

   :class:`TarFile`をクローズします。書き出しモードでは、完了ゼロブロックが 2つ、アーカイブに追加されます。


.. attribute:: TarFile.posix

   この値が真なら、POSIX 1003.1-1990 準拠のアーカイブを作成します。GNU 拡張機能はは POSIX 標準の一部ではないため使いません．
   POSIX 準拠のアーカイブでは，ファイル名の長さは最大 256 ， リンク名の最大長は100文字に制限されており，ファイルの最大長は 8
   ギガバイト以下です．ファイルがこれらの制限を超えた場合， :exc:`ValueError`を送出します． この値が偽の場合，GNU tar
   互換のアーカイブを作成します． POSIX 仕様には準拠しませんが，上記の制約を受けずにファイルを 保存できます．

   .. versionchanged:: 2.4
      *posix* のデフォルト値が :const:`False` になりました.


.. attribute:: TarFile.dereference

   この値が偽の場合，シンボリックリンクとハードリンクをアーカイブに 追加します。真の場合，ターゲットファイルの内容をアーカイブに追加します。
   この値はリンクをサポートしないシステムには影響しません。


.. attribute:: TarFile.ignore_zeros

   この値が偽の場合，空のブロックをアーカイブの終わりとして処理します。 真の場合，空(で無効な)ブロックを飛ばして、できるだけ多くのメンバを
   取得しようとします。これはアーカイブを連結している場合やアーカイブが 損傷している場合に役に立ちます。


.. attribute:: TarFile.debug=0

   ``0``\ (デバッグメッセージなし、デフォルト)から ``3``\ (すべてのデバッグ メッセージあり)までの値に設定します．メッセージは
   ``sys.stderr`` に出力されます．


.. attribute:: TarFile.errorlevel=0

   この値が``0`` (デフォルトの値です) の場合， :meth:`extract` 実行時の全てのエラーを無視します．ただし，
   デバッグが有効になっている場合には，デバッグ出力にエラーメッセージ として出力します． 値を``1`` にした場合，すべての*致命的な* エラーに対して
   :exc:`OSError`または:exc:`IOError` 例外を送出します． 値を``2`` にした場合、*致命的でない*エラーもまた，全て
   :exc:`TarError` 例外として送出します．

.. % -----------------
.. % TarInfo オブジェクト
.. % -----------------


.. _tarinfo-objects:

TarInfo オブジェクト
--------------------

:class:`TarInfo` オブジェクトは :class:`TarFile` の一つのメンバーを表します。ファイルに
必要な(ファイルタイプ、ファイルサイズ、時刻、許可、所有者等のような)すべての属性を保存する他に、
そのタイプを決定するのに役に立ついくつかのメソッドを提供します。 これにはファイルのデータそのものは含まれま*せん*。

:class:`TarInfo`オブジェクトは ``TarFile``のメソッド ``getmember()``、 ``getmembers()`` および
``gettarinfo()``によって返されます。


.. class:: TarInfo([name])

   :class:`TarInfo` オブジェクトを作成します。


.. method:: TarInfo.frombuf()

   :class:`TarInfo` オブジェクトを文字列バッファから作成して返します。


.. method:: TarInfo.tobuf([posix])

   :class:`TarInfo` オブジェクトから文字列バッファを作成します。 *posix* 引数については :class:`TarFile` の
   :attr:`posix` 属性の 項を参照してください。この引数はデフォルトでは :const:`False` です。

   .. % posixはオプションのようなので\optionalを加えた。2008-06-22 mft.

   .. versionadded:: 2.5
      *posix* 引数.

``TarInfo``オブジェクトには以下の public なデータ属性があります：


.. attribute:: TarInfo.name

   アーカイブメンバーの名前。


.. attribute:: TarInfo.size

   バイト単位でのサイズ。


.. attribute:: TarInfo.mtime

   最終更新時刻。


.. attribute:: TarInfo.mode

   許可ビット。


.. attribute:: TarInfo.type

   ファイルタイプです． *type* は普通、以下の定数: :const:`REGTYPE`, :const:`AREGTYPE`,
   :const:`LNKTYPE`, :const:`SYMTYPE`, :const:`DIRTYPE`, :const:`FIFOTYPE`,
   :const:`CONTTYPE`, :const:`CHRTYPE`, :const:`BLKTYPE`, :const:`GNUTYPE_SPARSE`
   のいずれかです． :class:`TarInfo` オブジェクトのタイプをもっと便利に決定するには、 下記の ``is_*()`` メソッドを使って下さい。


.. attribute:: TarInfo.linkname

   ターゲットファイル名の名前で、これは タイプ:const:`LNKTYPE` と  :const:`SYMTYPE`
   の:class:`TarInfo`オブジェクトにだけ存在します。


.. attribute:: TarInfo.uid

   ファイルメンバを保存した元のユーザのユーザ ID です．


.. attribute:: TarInfo.gid

   ファイルメンバを保存した元のユーザのグループ ID です．


.. attribute:: TarInfo.uname

   ファイルメンバを保存した元のユーザのユーザ名です．


.. attribute:: TarInfo.gname

   ファイルメンバを保存した元のユーザのグループ名です．

:class:`TarInfo`オブジェクトは便利な照会用のメソッドもいくつか提供しています:


.. method:: TarInfo.isfile()

   :class:`Tarinfo` オブジェクトが普通のファイルの場合に、 :const:`True` を返します。


.. method:: TarInfo.isreg()

   :meth:`isfile`と同じです。


.. method:: TarInfo.isdir()

   ディレクトリの場合に:const:`True`を返します。


.. method:: TarInfo.issym()

   シンボリックリンクの場合に:const:`True`を返します。


.. method:: TarInfo.islnk()

   ハードリンクの場合に:const:`True`を返します。


.. method:: TarInfo.ischr()

   キャラクタデバイスの場合に:const:`True`を返します。


.. method:: TarInfo.isblk()

   ブロックデバイスの場合に:const:`True`を返します。


.. method:: TarInfo.isfifo()

   FIFO の場合に:const:`True`を返します。


.. method:: TarInfo.isdev()

   キャラクタデバイス、ブロックデバイスあるいは FIFOの いずれかの場合に :const:`True`を返します。

.. % ------------------------
.. % 例
.. % ------------------------


.. _tar-examples:

例
--

tar アーカイブから現在のディレクトリーに全て抽出する方法：  ::

   import tarfile
   tar = tarfile.open("sample.tar.gz")
   tar.extractall()
   tar.close()

非圧縮 tar アーカイブをファイル名のリストから作成する方法：  ::

   import tarfile
   tar = tarfile.open("sample.tar", "w")
   for name in ["foo", "bar", "quux"]:
       tar.add(name)
   tar.close()

gzip 圧縮 tar アーカイブを作成してメンバー情報のいくつかを表示する方法：  ::

   import tarfile
   tar = tarfile.open("sample.tar.gz", "r:gz")
   for tarinfo in tar:
       print tarinfo.name, " は 大きさが ", tarinfo.size, "バイトで ",
       if tarinfo.isreg():
           print "普通のファイルです。"
       elif tarinfo.isdir():
           print "ディレクトリです。"
       else:
           print "ファイル・ディレクトリ以外のものです。"
   tar.close()

見せかけの情報を持つ tar アーカイブを作成する方法：  ::

   import tarfile
   tar = tarfile.open("sample.tar.gz", "w:gz")
   for name in namelist:
       tarinfo = tar.gettarinfo(name, "fakeproj-1.0/" + name)
       tarinfo.uid = 123
       tarinfo.gid = 456
       tarinfo.uname = "johndoe"
       tarinfo.gname = "fake"
       tar.addfile(tarinfo, file(name))
   tar.close()

非圧縮 tar ストリームを``sys.stdin``から抽出する *唯一の*方法：  ::

   import sys
   import tarfile
   tar = tarfile.open(mode="r|", fileobj=sys.stdin)
   for tarinfo in tar:
       tar.extract(tarinfo)
   tar.close()

