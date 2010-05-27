.. _tarfile-mod:

:mod:`tarfile` --- tar アーカイブファイルを読み書きする
=======================================================

.. module:: tarfile
   :synopsis: tar-形式のアーカイブファイルを読み書きします。


.. versionadded:: 2.3

.. moduleauthor:: Lars Gustabel <lars@gustaebel.de>
.. sectionauthor:: Lars Gustabel <lars@gustaebel.de>


:mod:`tarfile` モジュールは、gzipやbz2圧縮されたものも含めて、tarアーカイブの読み書きができます。
(:file:`.zip` ファイルの読み書きは :mod:`zipfile` モジュールで可能です。)

いくつかの事実と外観：

* :mod:`gzip` と :mod:`bz2` で圧縮されたアーカイブを読み書きします。

* POSIX.1-1988 (ustar) フォーマットの読み書きをサポートしています。

* *longname*, *longlink* 拡張を含めた、GNU tarフォーマットの読み書きをサポートしています。
  *sparse* 拡張は読み込みのみサポートしています。

* POSIX.1-2001 (pax) フォーマットの読み書きをサポートしています。

  .. versionadded:: 2.6

* ディレクトリ、普通のファイル、ハードリンク、シンボリックリンク、fifo、キャラクタデバイスおよびブロックデバイスを処理します。また、タイムスタンプ、
  アクセス許可およびオーナーのようなファイル情報の取得および保存が可能です。


.. function:: open(name=None, mode='r', fileobj=None, bufsize=10240, \*\*kwargs)

   パス名 *name* の :class:`TarFile` オブジェクトを返します。
   :class:`TarFile` オブジェクトと、利用出来るキーワード引数に関する詳細な情報については、
   :ref:`tarfile-objects` 節を参照してください。

   *mode* は ``'filemode[:compression]'`` の形式をとる文字列でなければなりません。デフォルトの値は ``'r'``
   です。以下に *mode* のとりうる組み合わせ全てを示します。

   +----------------------+-----------------------------------------------------------------+
   | mode                 | 動作                                                            |
   +======================+=================================================================+
   | ``'r' または 'r:*'`` | 透過な圧縮つきで読み込むためにオープンします(推奨)。            |
   +----------------------+-----------------------------------------------------------------+
   | ``'r:'``             | 圧縮なしで排他的に読み込むためにオープンします。                |
   +----------------------+-----------------------------------------------------------------+
   | ``'r:gz'``           | gzip 圧縮で読み込むためにオープンします。                       |
   +----------------------+-----------------------------------------------------------------+
   | ``'r:bz2'``          | bzip2 圧縮で読み込むためにオープンします。                      |
   +----------------------+-----------------------------------------------------------------+
   | ``'a' または 'a:'``  | 圧縮なしで追加するためにオープンします。ファイルが存在しない    |
   |                      | 場合は新たに作成されます。                                      |
   +----------------------+-----------------------------------------------------------------+
   | ``'w' または 'w:'``  | 非圧縮で書き込むためにオープンします。                          |
   +----------------------+-----------------------------------------------------------------+
   | ``'w:gz'``           | gzip 圧縮で書き込むためにオープンします。                       |
   +----------------------+-----------------------------------------------------------------+
   | ``'w:bz2'``          | bzip2 圧縮で書き込むためにオープンします。                      |
   +----------------------+-----------------------------------------------------------------+

   ``'a:gz'`` あるいは ``'a:bz2'`` は可能ではないことに注意して下さい。もし
   *mode* が、ある(圧縮した)ファイルを読み込み用にオープンするのに、適していないなら、 :exc:`ReadError` が発生します。これを防ぐには
   *mode* ``'r'`` を使って下さい。もし圧縮メソッドがサポートされていなければ、 :exc:`CompressionError` が発生します。

   もし *fileobj* が指定されていれば、それは *name* でオープンされたファイルオブジェクトの代替として使うことができます。
   そのファイルオブジェクトの、ファイルポジションが0であることを前提に動作します。

   特別な目的のために、 *mode* の2番目の形式: ``'ファイルモード|[圧縮]'`` があります。この形式を使うと、
   :func:`tarfile.open` が返すのはデータをブロックからなるストリームとして扱う :class:`TarFile` オブジェクトになります。この場合、ファイルに対して
   ランダムな seek を行えなくなります。 *fileobj* を指定する場合、 ``read()`` および ``write()``
   メソッドを持つ任意のオブジェクトにできます。 *bufsize* にはブロックサイズを指定します。デフォルトは ``20 * 512``
   バイトです。 ``sys.stdin`` 、ソケットファイルオブジェクト、テープデバイスと組み合わせる場合にはこの形式を
   使ってください。ただし、このような :class:`TarFile` オブジェクトにはランダムアクセスを行えないという制限があります。
   :ref:`tar-examples` 節を参照してください。現在可能なモードは：

   +-------------+-----------------------------------------------------------------+
   | モード      | 動作                                                            |
   +=============+=================================================================+
   | ``'r| *'``   | tar ブロックの *ストリーム* を透過な読み込みにオープンします。 |
   +-------------+-----------------------------------------------------------------+
   | ``'r|'``    | 非圧縮 tar ブロックの *ストリーム* を読み込みにオープンします。 |
   +-------------+-----------------------------------------------------------------+
   | ``'r|gz'``  | gzip 圧縮 *ストリーム* を読み込みにオープンします。             |
   +-------------+-----------------------------------------------------------------+
   | ``'r|bz2'`` | bzip2 圧縮 *ストリーム* を読み込みにオープンします。            |
   +-------------+-----------------------------------------------------------------+
   | ``'w|'``    | 非圧縮 *ストリーム* を書き込みにオープンします。                |
   +-------------+-----------------------------------------------------------------+
   | ``'w|gz'``  | gzip 圧縮 *ストリーム* を書き込みにオープンします。             |
   +-------------+-----------------------------------------------------------------+
   | ``'w|bz2'`` | bzip2 圧縮 *ストリーム* を書き込みにオープンします。            |
   +-------------+-----------------------------------------------------------------+


.. class:: TarFile

   tar アーカイブを読んだり、書いたりするためのクラスです。このクラスを直接使わず、代わりに :func:`tarfile.open` を使ってください。
   :ref:`tarfile-objects` を参照してください。


.. function:: is_tarfile(name)

   もし *name* が tar アーカイブファイルであり、 :mod:`tarfile` モジュールで読み出せる場合に :const:`True` を返します。


.. class:: TarFileCompat(filename, mode='r', compression=TAR_PLAIN)

   ``zipfile`` \ -風なインターフェースを持つ tar アーカイブへの制限されたアクセスのためのクラスです。詳細は
   ``zipfile`` のドキュメントを参照してください。 *compression* は、以下の定数のどれかでなければなりません：


   .. data:: TAR_PLAIN

      非圧縮 tar アーカイブのための定数。


   .. data:: TAR_GZIPPED

      :mod:`gzip` 圧縮 tar アーカイブのための定数。

   .. deprecated:: 2.6
      :class:`TarFileCompat` クラスは、 Python 3.0 で削除されるので、非推奨になりました。


.. exception:: TarError

   すべての :mod:`tarfile` 例外のための基本クラスです。


.. exception:: ReadError

   tar アーカイブがオープンされた時、 :mod:`tarfile` モジュールで操作できないか、あるいは何か無効であるとき発生します。


.. exception:: CompressionError

   圧縮方法がサポートされていないか、あるいはデータを正しくデコードできない時に発生します。


.. exception:: StreamError

   ストリーム風の :class:`TarFile` オブジェクトで典型的な制限のために発生します。


.. exception:: ExtractError

   :meth:`TarFile.extract` を使った時、もし :attr:`TarFile.errorlevel`\ ``== 2`` の *フェータルでない*
   エラーに対してだけ発生します。


.. exception:: HeaderError

   .. Is raised by :meth:`TarInfo.frombuf` if the buffer it gets is invalid.

   :meth:`TarInfo.frombuf` メソッドが、バッファが不正だったときに送出します。

   .. versionadded:: 2.6


.. Each of the following constants defines a tar archive format that the
   :mod:`tarfile` module is able to create. See section :ref:`tar-formats` for
   details.

以下の各定数は、 :mod:`tarfile` モジュールが作成できるtarアーカイブフォーマットを定義しています。
詳細は、 :ref:`tar-formats` を参照してください。


.. data:: USTAR_FORMAT

   POSIX.1-1988 (ustar) フォーマット


.. data:: GNU_FORMAT

   GNU tar フォーマット


.. data:: PAX_FORMAT

   POSIX.1-2001 (pax) フォーマット


.. data:: DEFAULT_FORMAT

   .. The default format for creating archives. This is currently :const:`GNU_FORMAT`.

   アーカイブを作成する際のデフォルトのフォーマット。
   現在は :const:`GNU_FORMAT`


.. The following variables are available on module level:

以下のモジュールレベル変数が利用できます。


.. data:: ENCODING

   .. The default character encoding i.e. the value from either
      :func:`sys.getfilesystemencoding` or :func:`sys.getdefaultencoding`.

   デフォルト文字エンコーディング。
   :func:`sys.getfilesystemencoding` か :func:`sys.getdefaultencoding`
   のどちらかの値。


.. seealso::

   Module :mod:`zipfile`
      :mod:`zipfile` 標準モジュールのドキュメント。

   `GNU tar マニュアル, 基本 Tar 形式 <http://www.gnu.org/software/tar/manual/html_node/Standard.html>`_
      GNU tar 拡張機能を含む、 tar アーカイブファイルのためのドキュメント。


.. _tarfile-objects:

TarFile オブジェクト
--------------------

:class:`TarFile` オブジェクトは、tar アーカイブへのインターフェースを提供します。 tar
アーカイブは一連のブロックです。アーカイブメンバー(保存されたファイル)は、ヘッダーブロックとそれに続くデータブロックから構成されています。ある tar
アーカイブにファイルを何回も保存することができます。各アーカイブメンバーは、 :class:`TarInfo`
オブジェクトによって表わされます、詳細については :ref:`tarinfo-objects` を参照してください。


.. class:: TarFile(name=None, mode='r', fileobj=None, format=DEFAULT_FORMAT, tarinfo=TarInfo, dereference=False, ignore_zeros=False, encoding=ENCODING, errors=None, pax_headers=None, debug=0, errorlevel=0)

   以下の全ての引数はオプションで、インスタンス属性としてもアクセスすることができます。

   .. *name* is the pathname of the archive. It can be omitted if *fileobj* is given.
      In this case, the file object's :attr:`name` attribute is used if it exists.

   *name* はアーカイブのパス名。 *fileobj* が渡された場合は省略可能。
   その場合、ファイルオブジェクトの :attr:`name` 属性があれば、それを利用します。

   .. *mode* is either ``'r'`` to read from an existing archive, ``'a'`` to append
      data to an existing file or ``'w'`` to create a new file overwriting an existing
      one.

   *mode* は、既存のアーカイブファールから読み込むための ``'r'``,
   既存のアーカイブファイルに追記するための ``'a'``,
   既存のファイルがあれば上書きし、新しいファイルを作成する ``'w'``
   のいずれかです。

   もし *fileobj* が与えられていれば、それを使ってデータを読み書きします。もしそれが決定できれば、 *mode* は *fileobj*
   のモードで上書きされます。
   *fileobj* はポジション0から利用されます。

   .. note::

      *fileobj* は、 :class:`TarFile` をクローズする時にクローズされません。

   .. *format* controls the archive format. It must be one of the constants
      :const:`USTAR_FORMAT`, :const:`GNU_FORMAT` or :const:`PAX_FORMAT` that are
      defined at module level.

   *format* はアーカイブのフォーマットを制御します。
   モジュールレベルで定義されている、 :const:`USTAR_FORMAT`, :const:`GNU_FORMAT`, :const:`PAX_FORMAT` 
   のいずれかである必要があります。

   .. versionadded:: 2.6

   .. The *tarinfo* argument can be used to replace the default :class:`TarInfo` class
      with a different one.

   *tarinfo* 引数を利用して、デフォルトの :class:`TarInfo` クラスを別のクラスで置き換えられます。

   .. versionadded:: 2.6

   .. If *dereference* is :const:`False`, add symbolic and hard links to the archive. If it
      is :const:`True`, add the content of the target files to the archive. This has no
      effect on systems that do not support symbolic links.

   *dereference* が :const:`False` だった場合、シンボリックリンクやハードリンクがアーカイブに追加されます。
   :const:`True` だった場合、リンクのターゲットとなるファイルの内容がアーカイブに追加されます。
   シンボリックリンクをサポートしていないシステムでは効果がありません。

   .. todo::
      訳者note: ハードリンクにまで対応している？原文が間違っている可能性があるので要確認。

   .. If *ignore_zeros* is :const:`False`, treat an empty block as the end of the archive.
      If it is :const:`True`, skip empty (and invalid) blocks and try to get as many members
      as possible. This is only useful for reading concatenated or damaged archives.

   *ignore_zeros* が :const:`False` だった場合、空ブロックをアーカイブの終端だと扱います。
   :const:`True` だった場合、空の(無効な)ブロックをスキップして、可能な限り多くのメンバを取得しようとします。
   このオプションは、連結(concatenate)されたり、壊れたアーカイブファイルを扱うときにのみ、意味があります。

   .. *debug* can be set from ``0`` (no debug messages) up to ``3`` (all debug
      messages). The messages are written to ``sys.stderr``.

   *debug* は ``0`` (デバッグメッセージ無し)から ``3`` (全デバッグメッセージ)
   まで設定できます。このメッセージは ``sys.stderr`` に書き込まれます。

   .. If *errorlevel* is ``0``, all errors are ignored when using :meth:`TarFile.extract`.
      Nevertheless, they appear as error messages in the debug output, when debugging
      is enabled.  If ``1``, all *fatal* errors are raised as :exc:`OSError` or
      :exc:`IOError` exceptions. If ``2``, all *non-fatal* errors are raised as
      :exc:`TarError` exceptions as well.

   *errorlevel* が ``0`` の場合、 :meth:`TarFile.extract` 使用時に全てのエラーが無視されます。
   エラーが無視された場合でも、 *debug* が有効であれば、エラーメッセージは出力されます。
   ``1`` の場合、全ての *致命的な(fatal)* エラーは :exc:`OSError` か :exc:`IOError` を送出します。
   ``2`` の場合、全ての *致命的でない(non-fatal)* エラーも :exc:`TarError` 例外として送出されます。

   .. The *encoding* and *errors* arguments control the way strings are converted to
      unicode objects and vice versa. The default settings will work for most users.
      See section :ref:`tar-unicode` for in-depth information.

   *encoding* と *errors* 引数は、文字列と unicode オブジェクトとの間の相互変換方法を指定します。
   デフォルトの設定で、ほとんどのユーザーでうまく動作するでしょう。
   詳しい情報は、 :ref:`tar-unicode` 節を参照してください。

   .. versionadded:: 2.6

   .. The *pax_headers* argument is an optional dictionary of unicode strings which
      will be added as a pax global header if *format* is :const:`PAX_FORMAT`.

   *pax_headers* 引数は、オプションの、 unicode 文字列の辞書で、 *format* が :const:`PAX_FORMAT`
   だった場合に pax グローバルヘッダに追加されます。

   .. versionadded:: 2.6


.. method:: TarFile.open(...)

   代替コンストラクタです。モジュールレベルでの :func:`tarfile.open`
   関数は、実際はこのクラスメソッドへのショートカットです。


.. method:: TarFile.getmember(name)

   メンバー *name* に対する :class:`TarInfo` オブジェクトを返します。もし
   *name* がアーカイブに見つからなければ、 :exc:`KeyError` が発生します。

   .. note::

      もしメンバーがアーカイブに1つ以上あれば、その最後に出現するものが、最新のバージョンであるとみなされます。


.. method:: TarFile.getmembers()

   :class:`TarInfo` オブジェクトのリストとしてアーカイブのメンバーを返します。このリストはアーカイブ内のメンバーと同じ順番です。


.. method:: TarFile.getnames()

   メンバーをその名前のリストとして返します。これは :meth:`getmembers` で返されるリストと同じ順番です。


.. method:: TarFile.list(verbose=True)

   コンテンツの表を ``sys.stdout`` に印刷します。もし *verbose* が :const:`False`
   であれば、メンバー名のみ印刷します。もしそれが :const:`True` であれば、 ``"ls -l"`` に似た出力を生成します。


.. method:: TarFile.next()

   :class:`TarFile` が読み込み用にオープンされている時、アーカイブの次のメンバーを
   :class:`TarInfo` オブジェクトとして返します。もしそれ以上利用可能なものがなければ、 :const:`None` を返します。


.. method:: TarFile.extractall(path=".", members=None)

   全てのメンバーをアーカイブから現在の作業ディレクトリーまたは *path* に抽出します。オプションの *members* が与えられるときには、
   :meth:`getmembers` で返されるリストの一部でなければなりません。
   所有者、変更時刻、許可のようなディレクトリー情報は全てのメンバーが抽出された後にセットされます。これは二つの問題を回避するためです。一つはディレクトリー
   の変更時刻はその中にファイルが作成されるたびにリセットされるということ。もう一つは、ディレクトリーに書き込み許可がなければその中のファイル抽出は
   失敗してしまうということです。

   .. warning::

      .. Never extract archives from untrusted sources without prior inspection.
         It is possible that files are created outside of *path*, e.g. members
         that have absolute filenames starting with ``"/"`` or filenames with two
         dots ``".."``.

      内容を信頼できないtarアーカイブを、事前の内部チェック前に展開してはいけません。
      ファイルが *path* の外側に作られる可能性があります。
      例えば、 ``"/"`` で始まる絶対パスのファイル名や、2重ドット ``".."``
      で始まるパスのファイル名です。

   .. versionadded:: 2.5


.. method:: TarFile.extract(member, path="")

   メンバーをアーカイブから現在の作業ディレクトリに、そのフル名を使って、抽出します。そのファイル情報はできるだけ正確に抽出されます。
   *member* は、ファイル名でも :class:`TarInfo` オブジェクトでも構いません。
   *path* を使って、異なるディレクトリを指定することができます。

   .. note::

      .. The :meth:`extract` method does not take care of several extraction issues.
         In most cases you should consider using the :meth:`extractall` method.

      :meth:`extract` メソッドは幾つかの展開に関する問題を扱いません。
      殆どの場合、 :meth:`extractall` メソッドの利用を考慮するべきです。

   .. warning::

      :meth:`extractall` の警告(warning)を参照


.. method:: TarFile.extractfile(member)

   アーカイブからメンバーをオブジェクトとして抽出します。 *member* は、ファイル名あるいは :class:`TarInfo` オブジェクトです。もし
   *member* が普通のファイルであれば、ファイル風のオブジェクトを返します。もし
   *member* がリンクであれば、ファイル風のオブジェクトをリンクのターゲットから構成します。もし *member* が上のどれでもなければ、
   :const:``None`` が返されます。

   .. note::

      ファイル風のオブジェクトは読み出し専用で以下のメソッドを提供します： :meth:`read`, :meth:`readline`,
      :meth:`readlines`, :meth:`seek`, :meth:`tell`.


.. method:: TarFile.add(name, arcname=None, recursive=True, exclude=None)

   ファイル *name* をアーカイブに追加します。 *name* は、任意のファイルタイプ (ディレクトリ、fifo、シンボリックリンク等)です。
   もし *arcname* が与えられていれば、それはアーカイブ内のファイルの代替名を指定します。デフォールトではディレクトリは再帰的に追加されます。
   これは、 *recursive* を :const:`False` に設定することで避けることができます。
   *exclude* を指定する場合、それは1つのファイル名を引数にとって、ブール値を返す関数である必要があります。
   この関数の戻り値が :const:`True` の場合、そのファイルが除外されます。 :const:`False` の場合、そのファイルは追加されます。

   .. versionchanged:: 2.6
      *exclude* 引数が追加されました。


.. method:: TarFile.addfile(tarinfo, fileobj=None)

   :class:`TarInfo` オブジェクト *tarinfo* をアーカイブに追加します。もし *fileobj*
   が与えられていれば、 ``tarinfo.size``  バイトがそれから読まれ、アーカイブに追加されます。 :meth:`gettarinfo` を使って
   :class:`TarInfo` オブジェクトを作成することができます。

   .. note::

      Windows プラットフォームでは、 *fileobj* は、ファイルサイズに関する問題を避けるために、常に、モード ``'rb'``
      でオープンされるべきです。


.. method:: TarFile.gettarinfo(name=None, arcname=None, fileobj=None)

   :class:`TarInfo` オブジェクトをファイル *name* あるいは (そのファイル記述子に ``os.fstat()`` を使って)
   ファイルオブジェクト *fileobj* のどちらか用に作成します。 :class:`TarInfo` の属性のいくつかは、
   :meth:`addfile` を使って追加する前に修正することができます。 *arcname* がもし与えられていれば、アーカイブ内のファイルの
   代替名を指定します。


.. method:: TarFile.close()

   :class:`TarFile` をクローズします。書き出しモードでは、完了ゼロブロックが 2つ、アーカイブに追加されます。


.. attribute:: TarFile.posix

   .. Setting this to :const:`True` is equivalent to setting the :attr:`format`
      attribute to :const:`USTAR_FORMAT`, :const:`False` is equivalent to
      :const:`GNU_FORMAT`.

   この値を :const:`True` にすることは、 :attr:`format` を :const:`USTAR_FORMAT` にすることと同じです。
   この値を :const:`False` にすることは、 :attr:`format` を :const:`GNU_FORMAT` にすることと同じです。

   .. versionchanged:: 2.4
      *posix* のデフォルト値が :const:`False` になりました.

   .. deprecated:: 2.6
      .. Use the :attr:`format` attribute instead.
      代わりに :attr:`format` 属性を利用してください。


.. attribute:: TarFile.pax_headers

   .. A dictionary containing key-value pairs of pax global headers.

   pax グローバルヘッダに含まれる key-value ペアの辞書

   .. versionadded:: 2.6

.. _tarinfo-objects:

TarInfo オブジェクト
--------------------

:class:`TarInfo` オブジェクトは :class:`TarFile` の一つのメンバーを表します。ファイルに
必要な(ファイルタイプ、ファイルサイズ、時刻、許可、所有者等のような)すべての属性を保存する他に、
そのタイプを決定するのに役に立ついくつかのメソッドを提供します。これにはファイルのデータそのものは含まれま *せん* 。

:class:`TarInfo` オブジェクトは ``TarFile`` のメソッド ``getmember()`` 、 ``getmembers()`` および
``gettarinfo()`` によって返されます。


.. class:: TarInfo(name="")

   :class:`TarInfo` オブジェクトを作成します。


.. method:: TarInfo.frombuf(buf)

   :class:`TarInfo` オブジェクトを文字列バッファ *buf* から作成して返します。

   .. versionadded:: 2.6
      バッファが不正な場合は、 :exc:`HeaderError` を送出します。

.. method:: TarInfo.fromtarfile(tarfile)

   .. Read the next member from the :class:`TarFile` object *tarfile* and return it as
      a :class:`TarInfo` object.

   :class:`TarFile` オブジェクトの *tarfile* から、次のメンバを読み込んで、それを
   :class:`TarInfo` オブジェクトとして返します。

   .. versionadded:: 2.6

.. method:: TarInfo.tobuf(format=DEFAULT_FORMAT, encoding=ENCODING, errors='strict')

   .. Create a string buffer from a :class:`TarInfo` object. For information on the
      arguments see the constructor of the :class:`TarFile` class.

   :class:`TarInfo` オブジェクトから文字列バッファを作成します。
   引数についての情報は、 :class:`TarFile` クラスのコンストラクタを参照してください。

   .. versionchanged:: 2.6
      引数が追加されました。


``TarInfo`` オブジェクトには以下の public なデータ属性があります：


.. attribute:: TarInfo.name

   アーカイブメンバーの名前。


.. attribute:: TarInfo.size

   バイト単位でのサイズ。


.. attribute:: TarInfo.mtime

   最終更新時刻。


.. attribute:: TarInfo.mode

   許可ビット。


.. attribute:: TarInfo.type

   ファイルタイプです。 *type* は普通、以下の定数: :const:`REGTYPE`, :const:`AREGTYPE`,
   :const:`LNKTYPE`, :const:`SYMTYPE`, :const:`DIRTYPE`, :const:`FIFOTYPE`,
   :const:`CONTTYPE`, :const:`CHRTYPE`, :const:`BLKTYPE`, :const:`GNUTYPE_SPARSE`
   のいずれかです。 :class:`TarInfo` オブジェクトのタイプをもっと便利に決定するには、下記の ``is_*()`` メソッドを使って下さい。


.. attribute:: TarInfo.linkname

   ターゲットファイル名の名前で、これはタイプ :const:`LNKTYPE` と  :const:`SYMTYPE`
   の :class:`TarInfo` オブジェクトにだけ存在します。


.. attribute:: TarInfo.uid

   ファイルメンバを保存した元のユーザのユーザ ID です。


.. attribute:: TarInfo.gid

   ファイルメンバを保存した元のユーザのグループ ID です。


.. attribute:: TarInfo.uname

   ファイルメンバを保存した元のユーザのユーザ名です。


.. attribute:: TarInfo.gname

   ファイルメンバを保存した元のユーザのグループ名です。

.. attribute:: TarInfo.pax_headers

   .. A dictionary containing key-value pairs of an associated pax extended header.

   pax 拡張ヘッダに関連付けられた、 key-value ペアの辞書。

   .. versionadded:: 2.6


:class:`TarInfo` オブジェクトは便利な照会用のメソッドもいくつか提供しています:


.. method:: TarInfo.isfile()

   :class:`Tarinfo` オブジェクトが普通のファイルの場合に、 :const:`True` を返します。


.. method:: TarInfo.isreg()

   :meth:`isfile` と同じです。


.. method:: TarInfo.isdir()

   ディレクトリの場合に :const:`True` を返します。


.. method:: TarInfo.issym()

   シンボリックリンクの場合に :const:`True` を返します。


.. method:: TarInfo.islnk()

   ハードリンクの場合に :const:`True` を返します。


.. method:: TarInfo.ischr()

   キャラクタデバイスの場合に :const:`True` を返します。


.. method:: TarInfo.isblk()

   ブロックデバイスの場合に :const:`True` を返します。


.. method:: TarInfo.isfifo()

   FIFO の場合に :const:`True` を返します。


.. method:: TarInfo.isdev()

   キャラクタデバイス、ブロックデバイスあるいは FIFOのいずれかの場合に :const:`True` を返します。


.. _tar-examples:

例
--

tar アーカイブから現在のディレクトリーに全て抽出する方法::

   import tarfile
   tar = tarfile.open("sample.tar.gz")
   tar.extractall()
   tar.close()

.. How to extract a subset of a tar archive with :meth:`TarFile.extractall` using
   a generator function instead of a list::

tarアーカイブの一部を、リストの代わりにジェネレータ関数を利用して、
:meth:`TarFile.extractall` で展開する方法::

   import os
   import tarfile

   def py_files(members):
       for tarinfo in members:
           if os.path.splitext(tarinfo.name)[1] == ".py":
               yield tarinfo

   tar = tarfile.open("sample.tar.gz")
   tar.extractall(members=py_files(tar))
   tar.close()

非圧縮 tar アーカイブをファイル名のリストから作成する方法::

   import tarfile
   tar = tarfile.open("sample.tar", "w")
   for name in ["foo", "bar", "quux"]:
       tar.add(name)
   tar.close()

gzip 圧縮 tar アーカイブを作成してメンバー情報のいくつかを表示する方法：  ::

   import tarfile
   tar = tarfile.open("sample.tar.gz", "r:gz")
   for tarinfo in tar:
       print tarinfo.name, " は大きさが ", tarinfo.size, "バイトで ",
       if tarinfo.isreg():
           print "普通のファイルです。"
       elif tarinfo.isdir():
           print "ディレクトリです。"
       else:
           print "ファイル・ディレクトリ以外のものです。"
   tar.close()

.. _tar-formats:

.. Supported tar formats

サポートされる tar のフォーマット
----------------------------------
..
   There are three tar formats that can be created with the :mod:`tarfile` module:

:mod:`tarfile` モジュールは、3つの tar フォーマットを作成することができます。

.. * The POSIX.1-1988 ustar format (:const:`USTAR_FORMAT`). It supports filenames
     up to a length of at best 256 characters and linknames up to 100 characters. The
     maximum file size is 8 gigabytes. This is an old and limited but widely
     supported format.

* POSIX.1-1988 ustar format (:const:`USTAR_FORMAT`). ファイル名の長さは256文字までで、
  リンク名の長さは100文字までです。最大のファイルサイズは8GBです。
  このフォーマットは古くて制限が多いですが、広くサポートされています。

.. * The GNU tar format (:const:`GNU_FORMAT`). It supports long filenames and
     linknames, files bigger than 8 gigabytes and sparse files. It is the de facto
     standard on GNU/Linux systems. :mod:`tarfile` fully supports the GNU tar
     extensions for long names, sparse file support is read-only.

* GNU tar format (:const:`GNU_FORMAT`). 長いファイル名とリンク名、8GBを超えるファイルや\
  スパース(sparse)ファイルをサポートしています。
  これは GNU/Linux システムにおいて、デ・ファクト・スタンダードになっています。
  :mod:`tarfile` モジュールは長いファイル名を完全にサポートしています。
  スパースファイルは読み込みのみサポートしています。

.. * The POSIX.1-2001 pax format (:const:`PAX_FORMAT`). It is the most flexible
     format with virtually no limits. It supports long filenames and linknames, large
     files and stores pathnames in a portable way. However, not all tar
     implementations today are able to handle pax archives properly.
   
     The *pax* format is an extension to the existing *ustar* format. It uses extra
     headers for information that cannot be stored otherwise. There are two flavours
     of pax headers: Extended headers only affect the subsequent file header, global
     headers are valid for the complete archive and affect all following files. All
     the data in a pax header is encoded in *UTF-8* for portability reasons.

* The POSIX.1-2001 pax format (:const:`PAX_FORMAT`).
  一番柔軟性があり、ほぼ制限が無いフォーマットです。
  長いファイル名やリンク名、大きいファイルをサポートし、パス名をポータブルな方法で保存します。
  しかし、現在のところ、全ての tar の実装が pax フォーマットを正しく扱えるわけではありません。

  *pax* フォーマットは既存の *ustar* フォーマットの拡張です。
  *ustar* では保存できない情報を追加のヘッダを利用して保存します。
  *pax* には2種類のヘッダがあります。
  1つ目は拡張ヘッダで、その次のファイルヘッダに影響します。
  2つ目はグローバルヘッダで、アーカイブ全体に対して有効で、それ以降の全てのファイルに影響します。
  全ての pax ヘッダの内容は、ポータブル性のために *UTF-8* で保存されます。

.. There are some more variants of the tar format which can be read, but not
   created:

他にも、読み込みのみサポートしている tar フォーマットが幾つかあります。

.. * The ancient V7 format. This is the first tar format from Unix Seventh Edition,
     storing only regular files and directories. Names must not be longer than 100
     characters, there is no user/group name information. Some archives have
     miscalculated header checksums in case of fields with non-ASCII characters.

* ancient V7 format. 
  これは Unix 7th Edition から存在する、最初の tar フォーマットです。
  通常のファイルとディレクトリのみ保存します。
  名前は100文字を超えてはならず、ユーザー/グループ名に関する情報は保存されません。
  幾つかのアーカイブは、フィールドがASCIIでない文字を含む場合に、
  ヘッダのチェックサムの計算を誤っています。

.. * The SunOS tar extended format. This format is a variant of the POSIX.1-2001
     pax format, but is not compatible.

* The SunOS tar extended format.
  POSIX.1-2001 pax フォーマットの亜流ですが、互換性がありません。

.. _tar-unicode:

Unicode に関する問題
--------------------

.. The tar format was originally conceived to make backups on tape drives with the
   main focus on preserving file system information. Nowadays tar archives are
   commonly used for file distribution and exchanging archives over networks. One
   problem of the original format (that all other formats are merely variants of)
   is that there is no concept of supporting different character encodings. For
   example, an ordinary tar archive created on a *UTF-8* system cannot be read
   correctly on a *Latin-1* system if it contains non-ASCII characters. Names (i.e.
   filenames, linknames, user/group names) containing these characters will appear
   damaged.  Unfortunately, there is no way to autodetect the encoding of an
   archive.

tarフォーマットはもともと、テープドライブにファイルシステムのバックアップを取る目的で設計されました。
現在、tarアーカイブはファイルを配布する場合に一般的に用いられ、ネットワークごしに送受信されます。
オリジナルのフォーマットの抱える1つの問題(ほか多くのフォーマットも同じですが)は、
文字エンコーディングが異なる環境を考慮していないことです。
例えば、通常の *UTF-8* の環境で作成されたアーカイブは、非ASCII文字を含んでいた場合
*Latin-1* のシステムでは正しく読み込むことができません。
非ASCII文字を含む名前(ファイル名、リンク名、ユーザー/グループ名)が破壊されます。
不幸なことに、アーカイブのエンコーディングを自動検出する方法はありません。

.. The pax format was designed to solve this problem. It stores non-ASCII names
   using the universal character encoding *UTF-8*. When a pax archive is read,
   these *UTF-8* names are converted to the encoding of the local file system.

pax フォーマットはこの問題を解決するように設計されました。
このフォーマットは、非ASCII文字の名前を *UTF-8* で保存します。
pax アーカイブを読み込むときに、この *UTF-8* の名前がローカルのファイルシステムの\
エンコーディングに変換されます。

.. The details of unicode conversion are controlled by the *encoding* and *errors*
   keyword arguments of the :class:`TarFile` class.

unicode 変換の動作は、 :class:`TarFile` クラスの *encoding* と *errors*
キーワード引数によって制御されます。

.. The default value for *encoding* is the local character encoding. It is deduced
   from :func:`sys.getfilesystemencoding` and :func:`sys.getdefaultencoding`. In
   read mode, *encoding* is used exclusively to convert unicode names from a pax
   archive to strings in the local character encoding. In write mode, the use of
   *encoding* depends on the chosen archive format. In case of :const:`PAX_FORMAT`,
   input names that contain non-ASCII characters need to be decoded before being
   stored as *UTF-8* strings. The other formats do not make use of *encoding*
   unless unicode objects are used as input names. These are converted to 8-bit
   character strings before they are added to the archive.

*encoding* のデフォルト値はローカルの文字エンコーディングです。
これは :func:`sys.getfilesystemencoding` と :func:`sys.getdefaultencoding`
から取得されます。
読み込みモードでは、 *encoding* は pax フォーマット内の unicode
の名前をローカルの文字エンコーディングに変換するために利用されます。
書き込みモードでは、 *encoding* の扱いは選択されたアーカイブフォーマットに依存します。
:const:`PAX_FORMAT` の場合、入力された非ASCII文字を含む文字は *UTF-8*
文字列として保存する前に一旦デコードする必要があるので、そこで *encoding* が利用されます。
それ以外のフォーマットでは、 *encoding* は、入力された名前に unicode が含まれない限りは\
利用されません。unicodeが含まれている場合、アーカイブに保存する前に *encoding*
でエンコードされます。

.. The *errors* argument defines how characters are treated that cannot be
   converted to or from *encoding*. Possible values are listed in section
   :ref:`codec-base-classes`. In read mode, there is an additional scheme
   ``'utf-8'`` which means that bad characters are replaced by their *UTF-8*
   representation. This is the default scheme. In write mode the default value for
   *errors* is ``'strict'`` to ensure that name information is not altered
   unnoticed.

*errors* 引数は、 *encoding* を利用して変換できない文字の扱いを指定します。
利用可能な値は、 :ref:`codec-base-classes` 節でリストアップされています。
読み込みモードでは、追加の値として ``'utf-8'`` を選択することができ、\
エラーが発生したときは *UTF-8* を利用することができます。(これがデフォルトです)
書き込みモードでは、 *errors* のデフォルト値は ``'strict'`` になっていて、\
名前が気づかないうちに変化することが無いようにしています。
