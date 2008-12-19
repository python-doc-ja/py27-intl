
:mod:`zipfile` --- ZIP アーカイブの処理
=======================================

.. module:: zipfile
   :synopsis: ZIP-フォーマットのアーカイブファイルを読み書きする
.. moduleauthor:: James C. Ahlstrom <jim@interet.com>
.. sectionauthor:: James C. Ahlstrom <jim@interet.com>


.. % LaTeX markup by Fred L. Drake, Jr. <fdrake@acm.org>
.. % Japanese translation by Yasushi Mausda <y.masuda@acm.org>

.. versionadded:: 1.6

ZIP は一般によく知られているアーカイブ （書庫化）および圧縮の標準ファイルフォーマットです。 このモジュールでは ZIP
形式のファイルの作成、読み書き、追記、 書庫内のファイル一覧の作成を行うためのツールを提供します。 より高度な使い方でこのモジュールを利用したいなら、
`PKZIP Application Note
<http://www.pkware.com/business_and_developers/developer/appnote/>`_. に定義されている
ZIP ファイルフォーマットを理解することが必要に なるでしょう。

このモジュールは現在のところ、コメントを追記した ZIP ファイルや マルチディスク ZIP ファイルを扱うことはできません。 ZIP64 拡張を利用する
ZIP ファイル(サイズが 4GB を超えるような ZIP ファイル) は扱えます。

このモジュールで利用できる属性を以下に示します:

.. % raise error エラーの送出


.. exception:: error

   不備のある ZIP ファイル操作の際に送出されるエラー


.. exception:: LargeZipFile

   ZIP ファイルが ZIP64 の機能を必要とするとき、 その機能が有効にされていないと送出されるエラー


.. class:: ZipFile

   ZIP ファイルの読み書きのためのクラスです。 コンストラクタの詳細については、 "ZipFile オブジェクト" (:ref:`zipfile-
   objects` 節)  を参照してください。


.. class:: PyZipFile

   Python ライブラリを含む ZIP アーカイブを生成するためのクラスです。


.. class:: ZipInfo([filename[, date_time]])

   アーカイブ中のメンバに関する情報を提供するために用いられるクラスです。 このクラスのインスタンスは :class:`ZipFile` オブジェクトの
   :meth:`getinfo` および :meth:`infolist` メソッドによって返され ます。:mod:`zipfile`
   モジュールを利用するほとんどのユーザはこの オブジェクトを自ら生成する必要はなく、モジュールが生成して返す オブジェクトを利用するだけでしょう。
   *filename* はアーカイブメンバの完全な名前で、 *date_time* は ファイルの最終更新時刻を記述する、 6 つの
   フィールドからなるタプルでなくてはなりません。各フィールドについては :ref:`zipinfo-objects`, "ZipInfo オブジェクト"
   節を参照してください。


.. function:: is_zipfile(filename)

   *filename* が正しいマジックナンバをもつ ZIP ファイルのときに ``True`` を返し、そうでない場合 ``False`` を返します。この
   モジュールは現在のところ、コメントを追記した ZIP ファイルを扱うこと ができません。


.. data:: ZIP_STORED

   アーカイブメンバが圧縮されていないことを表す数値定数です。


.. data:: ZIP_DEFLATED

   通常の ZIP 圧縮手法を表す数値定数。ZIP 圧縮は zlib モジュールを必要 とします。現在のところ他の圧縮手法はサポートされていません。


.. seealso::

   `PKZIP Application Note <http://www.pkware.com/business_and_developers/developer/appnote/>`_
      ZIP ファイル形式およびアルゴリズムを作成した  Phil Katz によるドキュメント。

   `Info-ZIP Home Page <http://www.info-zip.org/pub/infozip/>`_
      Info-ZIP プロジェクトによる ZIP アーカイブプログラム及びプログラム開発ライブラリに関する情報。


.. _zipfile-objects:

ZipFile オブジェクト
--------------------


.. class:: ZipFile(file[, mode[, compression[, allowZip64]]])

   ZIP ファイルを開きます。*file* はファイルへのパス名 (文字列) またはファイルのように振舞うオブジェクトのどちらでもかまいません。 *mode*
   パラメタは、既存のファイルを読むためには     ``'r'``、 既存のファイルを切り詰めたり新しいファイルに書き込むためには ``'w'``、
   追記を行うためには ``'a'`` でなくてはなりません。 *mode* が ``'a'`` で *file* が既存の ZIP ファイルを
   参照している場合、追加するファイルは既存のファイル中の ZIP アーカイブ に追加されます。*file* が ZIP を参照していない場合、新しい ZIP
   アーカイブが生成され、既存のファイルの末尾に追加されます。このことは、 ある ZIP ファイルを他のファイル、例えば
   :file:`python.exe` に ::

      cat myzip.zip >> python.exe

   として追加することができ、少なくとも :program:`WinZip` がこのような ファイルを読めることを意味します。 *compression*
   はアーカイブを書き出すときの ZIP 圧縮法で、 :const:`ZIP_STORED` または :const:`ZIP_DEFLATED` でなくては
   なりません。不正な値を指定すると :exc:`RuntimeError` が送出 されます。また、:const:`ZIP_DEFLATED`
   定数が指定されているのに :mod:`zlib` を利用することができない場合、 :exc:`RuntimeError` が送出されます。デフォルト値は
   :const:`ZIP_STORED` です。 *allowZip64* が ``True`` ならば 2GB より大きな ZIP ファイルの作成時に
   ZIP64 拡張を使用します。これが ``False`` ならば、:mod:`zipfile` モジュールは ZIP64
   拡張が必要になる場面で例外を送出します。 ZIP64 拡張はデフォルトでは無効にされていますが、これは Unix の :program:`zip` 　および
   :program:`unzip` (InfoZIP ユーティリティ) コマンドがこの拡張をサポートしていないからです。


.. method:: ZipFile.close()

   アーカイブファイルを閉じます。:meth:`close` は プログラムを終了する前に必ず呼び出さなければなりません。
   さもないとアーカイブ上の重要なレコードが書き込まれません。


.. method:: ZipFile.getinfo(name)

   アーカイブメンバ *name* に関する情報を持つ :class:`ZipInfo`  オブジェクトを返します。


.. method:: ZipFile.infolist()

   アーカイブに含まれる各メンバの :class:`ZipInfo` オブジェクトからなる リストを返します。既存のアーカイブファイルを開いている場合、
   リストの順番は実際の ZIP ファイル中のメンバの順番と同じになります。


.. method:: ZipFile.namelist()

   アーカイブメンバの名前のリストを返します。


.. method:: ZipFile.printdir()

   アーカイブの目次を ``sys.stdout`` に出力します。


.. method:: ZipFile.read(name)

   アーカイブ中のファイルの内容をバイト列にして返します。アーカイブは 読み込みまたは追記モードで開かれていなくてはなりません。


.. method:: ZipFile.testzip()

   アーカイブ中の全てのファイルを読み、CRC チェックサムとヘッダが正常か調べます。 最初に見つかった不正なファイルの名前を返します。 不正なファイルがなければ
   ``None`` を返します。


.. method:: ZipFile.write(filename[, arcname[, compress_type]])

   *filename* に指定したファイル名を持つファイルを、アーカイブ名を *arcname* (デフォルトでは *filename* と同じですが
   ドライブレターと先頭にあるパスセパレータは取り除かれます) にしてアーカイブに収録します。 *compress_type*
   を指定した場合、コンストラクタを使って新たなアーカイブエントリ を生成した際に使った*compression* パラメタを上書きします。アーカイブのモードは
   ``'w'`` または ``'a'`` でなくてはなりません。

   .. note::

      ZIP ファイル中のファイル名に関する公式なエンコーディング方式はありません。 もしユニコードのファイル名が付けられているならば、それを
      :meth:`write` に渡す前に望ましいエンコーディングでバイト列に変換しておいてください。 WinZip は全てのファイル名を DOS Latin
      としても知られる CP437 で解釈します。

   .. note::

      アーカイブ名はアーカイブルートに対する相対的なものでなければなりません。 言い換えると、アーカイブ名はパスセパレータで始まってはいけません。


.. method:: ZipFile.writestr(zinfo_or_arcname, bytes)

   文字列 *bytes*をアーカイブに書き込みます。*zinfo_or_arcname*
   はアーカイブ中で指定するファイル名か、または:class:`ZipInfo` インスタンス
   を指定します。*zinfo_or_arcname*に:class:`ZipInfo` インスタンスを指定
   する場合、*zinfo*インスタンスには少なくともファイル名、日付および時刻 を指定しなければなりません。ファイル名を指定した場合、日付と時刻には現在の
   日付と時間が設定されます。アーカイブはモード ``'w'`` または ``'a'`` で開かれていなければなりません。

以下のデータ属性も利用することができます。


.. attribute:: ZipFile.debug

   使用するデバッグ出力レベル。この属性は ``0`` (デフォルト、何も出力しない) から ``3`` (最も多くデバッグ情報を 出力する)
   までの値に設定することができます。デバッグ情報は  ``sys.stdout`` に出力されます。


.. _pyzipfile-objects:

PyZipFile オブジェクト
----------------------

:class:`PyZipFile` コンストラクタは :class:`ZipFile` コンストラクタ と同じパラメタを必要とします。インスタンスは
:class:`ZipFile` の メソッドの他に、追加のメソッドを一つ持ちます。


.. method:: PyZipFile.writepy(pathname[, basename])

   :file:`\*.py` ファイルを探し、:file:`\*.py` ファイルに対応するファイルを アーカイブに追加します。 対応するファイルとは、もしあれば
   :file:`\*.pyo` であり、そうでなければ :file:`\*.pyc` で、必要に応じて :file:`\*.py` からコンパイルします。 もし
   pathname がファイルなら、ファイル名は :file:`.py` で終わっていな ければなりません。また、(:file:`\*.py` に対応する
   :file:`\*.py[co]`) ファイルはアーカイブのトップレベルに (パス情報なしで) 追加されます。 もし pathname
   がディレクトリで、ディレクトリがパッケージディレクトリ でないなら、全ての :file:`\*.py[co]` ファイルはトップレベルに追加され
   ます。もしディレクトリがパッケージディレクトリなら、全ての :file:`\*.py[co]` ファイルはパッケージ名の名前をもつファイルパスの
   下に追加されます。サブディレクトリがパッケージディレクトリなら、 それらは再帰的に追加されます *basename* はクラス内部での呼び出し
   に使用するためのものです。

   :meth:`writepy` メソッドは以下のようなファイル名を持ったアーカイブ を生成します。 ::

      string.pyc                    # トップレベル名
      test/__init__.pyc             # パッケージディレクトリ
      test/testall.pyc              # test.testall モジュール
      test/bogus/__init__.pyc       # サブパッケージディレクトリ
      test/bogus/myfile.pyc         # test.bogus.myfile サブモジュール


.. _zipinfo-objects:

ZipInfo オブジェクト
--------------------

:class:`ZipFile` オブジェクトの :meth:`getinfo` および :meth:`infolist` メソッドは
:class:`ZipInfo` クラスのインスタンス を返します。それぞれのインスタンスオブジェクトは ZIP アーカイブの
一個のメンバについての情報を保持しています。

インスタンスは以下の属性を持ちます:


.. attribute:: ZipInfo.filename

   アーカイブ中のファイルの名前。


.. attribute:: ZipInfo.date_time

   アーカイブメンバの最終更新日時。この属性は6つの値からなるタプルです。:

   +-------+-------------------+
   | Index | Value             |
   +=======+===================+
   | ``0`` | 西暦年            |
   +-------+-------------------+
   | ``1`` | 月 (1 から始まる) |
   +-------+-------------------+
   | ``2`` | 日 (1 から始まる) |
   +-------+-------------------+
   | ``3`` | 時 (0 から始まる) |
   +-------+-------------------+
   | ``4`` | 分 (0 から始まる) |
   +-------+-------------------+
   | ``5`` | 秒 (0 から始まる) |
   +-------+-------------------+


.. attribute:: ZipInfo.compress_type

   アーカイブメンバの圧縮形式。


.. attribute:: ZipInfo.comment

   各アーカイブメンバに対するコメント。


.. attribute:: ZipInfo.extra

   拡張フィールドデータ。 この文字列データに含まれているデータの内部構成については、 `PKZIP Application Note
   <http://www.pkware.com/business_and_developers/developer/appnote/>`_
   でコメントされています。


.. attribute:: ZipInfo.create_system

   ZIP アーカイブを作成したシステムを記述する文字列。


.. attribute:: ZipInfo.create_version

   このアーカイブを作成した PKZIP のバージョン。


.. attribute:: ZipInfo.extract_version

   このアーカイブを展開する際に必要な PKZIP のバージョン。


.. attribute:: ZipInfo.reserved

   予約領域。ゼロでなくてはなりません。


.. attribute:: ZipInfo.flag_bits

   ZIP フラグビット列。


.. attribute:: ZipInfo.volume

   ファイルヘッダのボリュームナンバ。


.. attribute:: ZipInfo.internal_attr

   内部属性。


.. attribute:: ZipInfo.external_attr

   外部ファイル属性。


.. attribute:: ZipInfo.header_offset

   ファイルヘッダへのバイト数で表したオフセット。


.. attribute:: ZipInfo.CRC

   圧縮前のファイルの CRC-32 チェックサム。


.. attribute:: ZipInfo.compress_size

   圧縮後のデータのサイズ。


.. attribute:: ZipInfo.file_size

   圧縮前のファイルのサイズ。

