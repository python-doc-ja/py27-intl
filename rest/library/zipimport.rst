
:mod:`zipimport` --- Zip アーカイブからモジュールを import する
===============================================================

.. module:: zipimport
   :synopsis: Python モジュール を ZIP アーカイブから import する機能のサポート
.. moduleauthor:: Just van Rossum <just@letterror.com>


.. versionadded:: 2.3

このモジュールは， Python モジュール (:file:`\*.py`，:file:`\*.py[co]` やパッケージを ZIP 形式のアーカイブから
import できるように します。通常，:mod:`zipimport` を明示的に使う必要はありません; 組み込みの :keyword:`import`
は，``sys.path`` の要素が ZIP  アーカイブへのパスを指している場合にこのモジュールを自動的に 使います。

普通，``sys.path`` はディレクトリ名の文字列からなるリストです。 このモジュールを使うと，``sys.path`` の要素に ZIP ファイル
アーカイブを示す文字列を使えるようになります。ZIP アーカイブには サブディレクトリ構造を含めることができ，パッケージの import を
サポートさせしたり，アーカイブ内のパスを指定してサブディレクトリ 下から import を行わせたりできます。例えば，
:file:`/tmp/example.zip/lib/` のように指定すると，アーカイブ中の :file:`lib/` サブディレクトリ下だけから
import を行います。

ZIP アーカイブ内にはどんなファイルを置いてもかまいませんが， import できるのは:file:`.py` および :file:`.py[co]`
だけです。 動的モジュール (:file:`.pyd`，:file:`.so`) の ZIP import は行えません。 アーカイブ内に
:file:`.py` ファイルしか入っていない場合， Python がアーカイブを変更して， :file:`.py` ファイルに対応する
:file:`.pyc` や:file:`.pyo` ファイルを追加したりはしません。 つまり，ZIP アーカイブ中に :file:`.pyc` が入っていない
場合， import はやや低速になるかもしれないので注意してください。

ZIP アーカイブからロードしたモジュールに対して組み込み関数 :func:`reload` を呼び出すと失敗します; :func:`reload` が
必要になるということは，実行時に ZIPファイルが置き換えられてしまう ことになり，あまり起こりそうにない状況だからです。

このモジュールで使える属性を以下に示します:


.. exception:: ZipImporterError

   zipimporter オブジェクトが送出する例外です。 :exc:`ImportError` のサブクラスなので，:exc:`ImportError`
   としても捕捉できます。


.. class:: zipimporter

   ZIP ファイルを import するためのクラスです。 コンストラクタの詳細は "zipimporter オブジェクト" (:ref
   :`zipimporter-objects` 節) を参照してください。


.. seealso::

   `PKZIP Application Note <http://www.pkware.com/appnote.html>`_
      ZIP ファイル形式の作者であり，ZIP で使われて いるアルゴリズムの作者でもある Phil Katz による，ZIP ファイル形式
      についてのドキュメントです。

   :pep:`0273` - Import Modules from Zip Archives
      このモジュールの実装も行った、James C. Ahlstrom による PEP です。 Python 2.3 は PEP 273 の仕様に従っていますが、
      Just van Rossum の書いた import フックによる実装を使っています。 import フックは PEP 302 で解説されています。

   :pep:`0302` - New Import Hooks
      このモジュールを動作させる助けに なっている import フックの追加を提案している PEP です。


.. _zipimporter-objects:

zipimporter オブジェクト
------------------------


.. class:: zipimporter(archivepath)

   新たな zipimporter インスタンスを生成します。*archivepath* は ZIP ファイルへのパスでなければなりません。
   *archivepath* が 有効な ZIP アーカイブを指していない場合、:exc:`ZipImportError` を送出します。


.. method:: zipimporter.find_module(fullname[, path])

   *fullname* に指定したモジュールを検索します。*fullname* は 完全指定の (ドット表記の) モジュール名でなければなりません。
   モジュールが見つかった場合には zipimporter インスタンス自体を返し、 そうでない場合には :const:`None` を返します。 *path*
   引数は無視されます --- この引数は importer プロトコルとの 互換性を保つためのものです。


.. method:: zipimporter.get_code(fullname)

   *fullname* に指定したモジュールのコードオブジェクトを返します。 モジュールがない場合には:class:`ZipImportError`
   を送出します。


.. method:: zipimporter.get_data(pathname)

   *pathname* に関連付けられたデータを返します。該当するファイルが 見つからなかった場合には :exc:`IOError` を送出します。


.. method:: zipimporter.get_source(fullname)

   *fullname* に指定したモジュールのソースコードを返します。 モジュールが見つからなかった場合には :exc:`ZipImportError`
   を送出します。モジュールは存在するが、ソースコードがない場合には :const:`None` を返します。


.. method:: zipimporter.is_package(fullname)

   *fullname* で指定されたモジュールがパッケージの場合に :const:`True` を返します。モジュールが見つからなかった場合には
   :exc:`ZipImportError` を送出します。


.. method:: zipimporter.load_module(fullname)

   *fullname* に指定したモジュールをロードします。*fullname* は完全指定の (ドット表記の) モジュール名でなくてはなりません。 import
   済みのモジュールを返します。モジュールがない場合には :exc:`ZipImportError` を送出します。


使用例
------

.. _zipimport examples:

モジュールを ZIP アーカイブから import する例を以下に示します -  :mod:`zipimport` モジュールが明示的に使われていないことに注意
してください。 ::

   $ unzip -l /tmp/example.zip
   Archive:  /tmp/example.zip
     Length     Date   Time    Name
    --------    ----   ----    ----
        8467  11-26-02 22:30   jwzthreading.py
    --------                   -------
        8467                   1 file
   $ ./python
   Python 2.3 (#1, Aug 1 2003, 19:54:32) 
   >>> import sys
   >>> sys.path.insert(0, '/tmp/example.zip')  # パス先頭に .zip ファイル追加
   >>> import jwzthreading
   >>> jwzthreading.__file__
   '/tmp/example.zip/jwzthreading.py'

