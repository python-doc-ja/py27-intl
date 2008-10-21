
:mod:`shutil` --- 高レベルなファイル操作
========================================

.. module:: shutil
   :synopsis: コピーを含む高レベルなファイル操作。
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


.. % partly based on the docstrings

:mod:`shutil`モジュールはファイルやファイルの収集に関する多くの高レベ ルな操作方法を提供します。特にファイルのコピーや削除のための関数が用意さ
れています。

.. index::
   single: file; copying
   single: copying files

**注意:** MacOSにおいてはリソースフォークや他のメタデータは取り扱う ことができません。

つまり、ファイルをコピーする際にこれらのリソースは失われたり、ファイルタ イプや作成者コードは正しく認識されないことを意味します。


.. function:: copyfile(src, dst)

   *src*で指定されたファイル内容を*dst*で指定されたファイルへとコ ピーします。 コピー先は書き込み可能である必要があります。そうでなければ
   :exc:`IOError`を発生します。 もし*dst*が存在したら、置き換えられます。
   キャラクタやブロックデバイス、パイプ等の特別なファイルはこの関数ではコ ピーできません。 *src*と*dst*にはパス名を文字列で与えられます。


.. function:: copyfileobj(fsrc, fdst[, length])

   ファイル形式のオブジェクト*fsrc*の内容を*fdst*へコピーします。 整数値*length*はバッファサイズを表します。特に負の*length*は
   チャンク内のソースデータを繰り返し操作することなくコピーします。 つまり標準ではデータは制御不能なメモリ消費を避けるためにチャンク内 に読み込まれます。


.. function:: copymode(src, dst)

   *src*から*dst*へパーミッションをコピーします。ファイル内容や所 有者、グループは影響を受けません。
   *src*と*dst*には文字列としてパス名を与えられます。


.. function:: copystat(src, dst)

   *src*から*dst*へパーミッション最終アクセス時間、最終更新時間を コピーします。ファイル内容や所有者、グループは影響を受けません。
   *src*と*dst*には文字列としてパス名を与えられます。


.. function:: copy(src, dst)

   ファイル*src*をファイルまたはディレクトリ*dist*へコピーします。 もし、*dst*がディレクトリであればファイル名は*src*と同じものが
   指定されたディレクトリ内に作成（または上書き）されます。 パーミッションはコピーされます。 *src*と*dst*には文字列としてパス名を与えられます。


.. function:: copy2(src, dst)

   :func:`copy`と類似していますが、最終アクセス時間や最終更新時間も同 様にコピーされます。これは  Unix コマンドの :program:`cp`
   :option:`-p`と同様の働きをします。


.. function:: copytree(src, dst[, symlinks])

   *src*を起点としてディレクトリーに既存のものは使えません。 存在しない親ディレクトリも含めて作成されます。 パーミッションと時刻は
   :func:`copystat`関数でコピーされます。 個々のファイルは:func:`copy2`によってコピー されます。If
   *symlinks*が真であれば、元のディレクトリ内の シンボリックリンクはコピー先のディレクトリ内へシンボリックリンクとして
   コピーされます。偽が与えられたり省略された場合は元のディレクトリ内のリ ンクの対象となっているファイルがコピー先のディレクトリ内へコピーされま
   す。エラーが発生したときはエラー理由のリストを持った:exc:`Error`を起こします。

   この関数のソースコードは道具としてよりも使用例として捉えられるべきでしょう。

   .. versionchanged:: 2.3
      コピー中にエラーが発生した場合、メッセージを出力するのではなく :exc:`Error`を起こす。.

   .. versionchanged:: 2.5
      *dst*を作成する際に中間のディレクトリ作成が必要な場合、 エラーを起こすのではなく作成する。 ディレクトリのパーミッションと時刻を
      :func:`copystat` を利用してコピーする。 .


.. function:: rmtree(path[, ignore_errors[, onerror]])

   .. index:: single: directory; deleting

   ディレクトリツリー全体を削除します。もし*ignore_errors*が真であれば 削除に失敗したことによるエラーは無視され、偽が与えられたり省略された場
   合はこれらのエラーは*onerror*で与えられたハンドラを呼び出して処理 され、これが省略された場合は例外を引き起こします。

   *onerror*が与えられた場合、それは3つのパラメータ*function*, *path*および*excinfo*を受け入れて呼び出し可能のものでなくてはな
   りません。最初のパラメータ*function*は例外を引き起こす関数で :func:`os.listdir`、:func:`os.remove`または
   :func:`os.rmdir`が用いられるでしょう。 二番目のパラメータは*path*は*function*へ渡らせるパス名です。
   三番目のパラメータ*excinfo*は:func:`sys.exc_info`で返されるよ
   うな例外情報になるでしょう。*onerror*が引き起こす例外はキャッチでき ません。


.. function:: move(src, dst)

   再帰的にファイルやディレクトリを別の場所へ移動します。

   もし移動先が現在のファイルシステム上であれば単純に名前を変更します。 そうでない場合はコピーを行い、その後コピー元は削除されます。

   .. versionadded:: 2.3


.. exception:: Error

   この例外は複数ファイルの操作を行っているときに生じる例外をまとめたもの
   です。:func:`copytree`に対しては例外の引数は3つのタプル(*srcname*, *dstname*,
   *exception*)からなるリストです。

   .. versionadded:: 2.3


.. _shutil-example:

使用例
------

以下は前述の:func:`copytree`関数のドキュメント文字列を省略した実装 例です。 本モジュールで提供される他の関数の使い方を示しています。 ::

   def copytree(src, dst, symlinks=0):
       names = os.listdir(src)
       os.mkdir(dst)
       for name in names:
           srcname = os.path.join(src, name)
           dstname = os.path.join(dst, name)
           try:
               if symlinks and os.path.islink(srcname):
                   linkto = os.readlink(srcname)
                   os.symlink(linkto, dstname)
               elif os.path.isdir(srcname):
                   copytree(srcname, dstname, symlinks)
               else:
                   copy2(srcname, dstname)
           except (IOError, os.error), why:
               print "Can't copy %s to %s: %s" % (`srcname`, `dstname`, str(why))

