
:mod:`filecmp` --- ファイルおよびディレクトリの比較
===================================

.. module:: filecmp
   :synopsis: ファイル群を効率的に比較します。
.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>


:mod:`filecmp` モジュールでは、ファイルおよびディレクトリを 比較するため、様々な時間／正確性のトレードオフに関するオプションを
備えた関数を定義しています。

:mod:`filecmp` モジュールでは以下の関数を定義しています:


.. function:: cmp(f1, f2[, shallow])

   名前が *f1* および *f2* のファイルを比較し、二つのファイルが 同じらしければ ``True`` を返し、そうでなければ ``false`` を
   返します。

   *shallow* が与えられておりかつ偽でなければ、:func:`os.stat` の返すシグネチャが一致するファイルは同じであると見なされます。

   この関数で比較されたファイルは :func:`os.stat` シグネチャが 変更されるまで再び比較されることはありません。*use_statcache*
   を真にすると、キャッシュ無効化機構を失敗させます --- そのため、 :mod:`statcache` のキャッシュから古いファイル stat 値が
   使われます。

   可搬性と効率のために、個の関数は外部プログラムを一切呼び出さないので 注意してください。


.. function:: cmpfiles(dir1, dir2, common[, shallow])

   ファイル名からなる 3つのリスト: *match*、*mismatch*、 *errors* を返します。*match* には双方のディレクトリで
   一致したファイルのリストが含まれ、*mismatch* にはそうでない ファイル名のリストが入ります。そして *errors* は比較されなかった
   ファイルが列挙されます。ファイルによっては、ユーザにそのファイル を読む権限がなかったり、比較を完了することができなかった場合以外 のその他諸々の理由により、
   *errors* に列挙されることがあります。

   引数 *common* は両方のディレクトリにあるファイルのリストです。 引数 *shallow* はその意味も標準 の設定も
   :func:`filecmp.cmp` と同じです。

例::

   >>> import filecmp
   >>> filecmp.cmp('libundoc.tex', 'libundoc.tex')
   True
   >>> filecmp.cmp('libundoc.tex', 'lib.tex')
   False


.. _dircmp-objects:

:class:`dircmp` クラス
-------------------

:class:`dircmp` のインスタンスは以下のコンストラクタで生成されます:


.. class:: dircmp(a, b[, ignore[, hide]])

   ディレクトリ *a* および *b* を比較するための新しいディレクトリ 比較オブジェクトを生成します。*ignore* は比較の際に無視する
   ファイル名のリストで、標準の設定では ``['RCS', 'CVS', 'tags']`` です。*hide* は表示しない名前のリストで、標準の設定では
   ``[os.curdir, os.pardir]`` です。

:class:`dircmp` クラスは以下のメソッドを提供しています:


.. method:: dircmp.report()

   *a* および *b* の間の比較結果を (``sys.stdout`` に) 出力します。


.. method:: dircmp.report_partial_closure()

   *a* および *b* およびそれらの直下にある共通のサブディレクトリ 間での比較結果を出力します。


.. method:: dircmp.report_full_closure()

   *a* および *b* およびそれらの共通のサブディレクトリ間での 比較結果を (再帰的に比較して) 出力します。

:class:`dircmp` は、比較しているディレクトリツリーに関する様々な 種類の情報を取得するために使えるような、多くの興味深い属性を提供 しています。

:meth:`__getattr__` フックを経由すると、全ての属性を のろのろと計算するため、速度上のペナルティを受けないのは
計算処理の軽い属性を使ったときだけなので注意してください。


.. attribute:: dircmp.left_list

   *a* にあるファイルおよびサブディレクトリです。 *hide* および *ignore* でフィルタされています。


.. attribute:: dircmp.right_list

   *b* にあるファイルおよびサブディレクトリです。 *hide* および *ignore* でフィルタされています。


.. attribute:: dircmp.common

   *a* および *b* の両方にあるファイルおよびサブディレクトリです。


.. attribute:: dircmp.left_only

   *a* だけにあるファイルおよびサブディレクトリです。


.. attribute:: dircmp.right_only

   *b* だけにあるファイルおよびサブディレクトリです。


.. attribute:: dircmp.common_dirs

   *a* および *b* の両方にあるサブディレクトリです。


.. attribute:: dircmp.common_files

   *a* および *b* の両方にあるファイルです。


.. attribute:: dircmp.common_funny

   *a* および *b* の両方にあり、ディレクトリ間で タイプが異なるか、:func:`os.stat` がエラーを報告するような 名前です。


.. attribute:: dircmp.same_files

   *a* および *b* 両方にあり、一致するファイルです。


.. attribute:: dircmp.diff_files

   *a* および *b* 両方にあるが、一致しないファイルです。


.. attribute:: dircmp.funny_files

   *a* および *b* 両方にあるが、比較されなかったファイルです。


.. attribute:: dircmp.subdirs

   :attr:`common_dirs` のファイル名を :class:`dircmp` オブジェクトに 対応付けた辞書です。

