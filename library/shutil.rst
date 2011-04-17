
:mod:`shutil` --- 高レベルなファイル操作
========================================

.. module:: shutil
   :synopsis: コピーを含む高レベルなファイル操作。
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


.. partly based on the docstrings

:mod:`shutil` モジュールはファイルやファイルの収集に関する多くの高レベルな操作方法を提供します。
特にファイルのコピーや削除のための関数が用意されています。
個別のファイルに対する操作については、 :mod:`os` モジュールを参照してください。

.. index::
   single: file; copying
   single: copying files

.. warning::
   .. Even the higher-level file copying functions (:func:`copy`, :func:`copy2`)
      can't copy all file metadata.

   高レベルなファイルコピー関数(:func:`copy`, :func:`copy2`)でも、全てのファイルの
   メタデータをコピーできるわけではありません。

   .. On POSIX platforms, this means that file owner and group are lost as well
      as ACLs.  On Mac OS, the resource fork and other metadata are not used.
      This means that resources will be lost and file type and creator codes will
      not be correct. On Windows, file owners, ACLs and alternate data streams
      are not copied.

   POSIXプラットフォームでは、これはACLやファイルのオーナー、グループが失われることを意味しています。
   Mac OSでは、リソースフォーク(resource fork)やその他のメタデータが利用されません。
   これは、リソースが失われ、ファイルタイプや生成者コード(creator code)が正しくなくなることを意味しています。
   Windowsでは、ファイルオーナー、ACL、代替データストリームがコピーされません。


.. function:: copyfileobj(fsrc, fdst[, length])

   ファイル形式のオブジェクト *fsrc* の内容を *fdst* へコピーします。整数値 *length* はバッファサイズを表します。特に負の *length* は
   チャンク内のソースデータを繰り返し操作することなくコピーします。つまり標準ではデータは制御不能なメモリ消費を避けるためにチャンク内に読み込まれます。
   *fsrc* オブジェクトのファイルポジションが0でない場合、現在のポジションから後ろの\
   部分だけがコピーされることに注意してください。


.. function:: copyfile(src, dst)

   .. Copy the contents (no metadata) of the file named *src* to a file named *dst*.
      *dst* must be the complete target file name; look at :func:`copy` for a copy that
      accepts a target directory path.  If *src* and *dst* are the same files,
      :exc:`Error` is raised.
      The destination location must be writable; otherwise,  an :exc:`IOError` exception
      will be raised. If *dst* already exists, it will be replaced.   Special files
      such as character or block devices and pipes cannot be copied with this
      function.  *src* and *dst* are path names given as strings.

   *src* で指定されたファイルの内容を *dst* で指定されたファイルへとコピーします。(メタデータはコピーされません)
   *dst* は完全なターゲットファイル名である必要があります。
   コピー先にディレクトリ名を使用したい場合は、 :func:`copy` を参照してください。
   もし、 *src* と *dst* が同じファイルであれば、 :exc:`Error` 例外が発生します。

   コピー先は書き込み可能である必要があります。そうでなければ
   :exc:`IOError` を発生します。もし *dst* が存在したら、置き換えられます。
   キャラクタやブロックデバイス、パイプ等の特別なファイルはこの関数ではコピーできません。
   *src* と *dst* にはパス名を文字列で与えられます。


.. function:: copymode(src, dst)

   *src* から *dst* へパーミッションをコピーします。ファイル内容や所有者、グループは影響を受けません。
   *src* と *dst* には文字列としてパス名を与えられます。


.. function:: copystat(src, dst)

   *src* から *dst* へ、パーミッション、最終アクセス時間、最終更新時間、フラグをコピーします。
   ファイル内容や所有者、グループは影響を受けません。
   *src* と *dst* には文字列としてパス名を与えられます。


.. function:: copy(src, dst)

   ファイル *src* をファイルまたはディレクトリ *dist* へコピーします。もし、 *dst* がディレクトリであればファイル名は *src* と同じものが
   指定されたディレクトリ内に作成（または上書き）されます。パーミッションはコピーされます。 *src* と *dst* には文字列としてパス名を与えられます。


.. function:: copy2(src, dst)

   :func:`copy` と類似していますが、メタデータも同様にコピーされます。
   実際のところ、この関数は :func:`copy` の後に :func:`copystat` しています。
   Unix コマンドの :program:`cp -p` と同様の働きをします。


.. function:: ignore_patterns(\*patterns)

   ..
      This factory function creates a function that can be used as a callable for
      :func:`copytree` \'s *ignore* argument, ignoring files and directories that
      match one of the glob-style *patterns* provided.  See the example below.

   このファクトリ関数は、 :func:`copytree` 関数の *ignore* 引数に渡すための呼び出し可能
   オブジェクトを作成します。
   glob形式の *patterns* にマッチするファイルやディレクトリが無視されます。
   下の例を参照してください。

   .. versionadded:: 2.6


.. function:: copytree(src, dst[, symlinks])

   .. Recursively copy an entire directory tree rooted at *src*.  The destination
      directory, named by *dst*, must not already exist; it will be created as well
      as missing parent directories.  Permissions and times of directories are
      copied with :func:`copystat`, individual files are copied using
      :func:`copy2`.

   *src* を起点としたディレクトリツリーをコピーします。
   *dst* で指定されたターゲットディレクトリは、既存のもので無い必要があります。
   存在しない親ディレクトリも含めて作成されます。パーミッションと時刻は
   :func:`copystat` 関数でコピーされます。個々のファイルは :func:`copy2` によってコピーされます。

   .. If *symlinks* is true, symbolic links in the source tree are represented as
      symbolic links in the new tree; if false or omitted, the contents of the
      linked files are copied to the new tree.

   *symlinks* が真であれば、元のディレクトリ内のシンボリックリンクはコピー先のディレクトリ内へシンボリックリンクとして
   コピーされます。偽が与えられたり省略された場合は元のディレクトリ内のリンクの対象となっているファイルがコピー先のディレクトリ内へコピーされま
   す。

   .. If *ignore* is given, it must be a callable that will receive as its
      arguments the directory being visited by :func:`copytree`, and a list of its
      contents, as returned by :func:`os.listdir`.  Since :func:`copytree` is
      called recursively, the *ignore* callable will be called once for each
      directory that is copied.  The callable must return a sequence of directory
      and file names relative to the current directory (i.e. a subset of the items
      in its second argument); these names will then be ignored in the copy
      process.  :func:`ignore_patterns` can be used to create such a callable that
      ignores names based on glob-style patterns.

   *ignore* 引数を利用する場合、その呼び出し可能オブジェクトは、引数として、
   :func:`copytree` が走査するディレクトリと、 :func:`os.listdir` が返すそのディレクトリの内容を
   受け取ります。
   :func:`copytree` は再帰的に呼び出されるので、 *ignore* はコピーされる各ディレクトリ\
   毎に呼び出されます。 *ignore* の戻り値は、ファイルやディレクトリに対する\
   カレントディレクトリからの相対パスのシーケンスである必要があります。
   (例えば、第二引数のサブセット)
   返された名前は、無視され、コピーされません。
   :func:`ignore_patterns` を使って、glob形式のパターンからこの引数のための
   呼び出し可能オブジェクトを作成することができます。

   エラーが発生したときはエラー理由のリストを持った :exc:`Error` を起こします。

   この関数は、究極の道具としてではなく、ソースコードが利用例になっていると捉えるべきでしょう。

   .. versionchanged:: 2.3
      コピー中にエラーが発生した場合、メッセージを出力するのではなく :exc:`Error` を起こす。

   .. versionchanged:: 2.5
      *dst* を作成する際に中間のディレクトリ作成が必要な場合、エラーを起こすのではなく作成する。ディレクトリのパーミッションと時刻を
      :func:`copystat` を利用してコピーする。

   .. versionchanged:: 2.6
      何がコピーされるかを制御するための *ignore* 引数

.. function:: rmtree(path[, ignore_errors[, onerror]])

   .. index:: single: directory; deleting

   ディレクトリツリー全体を削除します。
   *path* はディレクトリを指している必要があります。（ディレクトリに対するシンボリックリンクではいけません）
   もし *ignore_errors* が真であれば削除に失敗したことによるエラーは無視されます。
   偽が与えられたり省略された場合はこれらのエラーは *onerror* で与えられたハンドラを呼び出して処理され、\
   *onerror* が省略された場合は例外を引き起こします。

   *onerror* が与えられた場合、それは3つのパラメータ *function*, *path* および *excinfo* を受け入れて呼び出し可能のものでなくてはな
   りません。最初のパラメータ *function* は例外を引き起こした関数で
   :func:`os.listdir`, :func:`os.remove`, :func:`os.rmdir` のいずれかでしょう。
   2番目のパラメータ *path* は *function* へ渡されたパス名です。
   3番目のパラメータ *excinfo* は :func:`sys.exc_info` で返されるよ
   うな例外情報になるでしょう。 *onerror* が引き起こす例外はキャッチできません。

   .. .. versionchanged:: 2.6
   ..    Explicitly check for *path* being a symbolic link and raise :exc:`OSError`
         in that case.

   .. versionchanged:: 2.6
      *path* を明示的にチェックして、シンボリックリンクだった場合は :exc:`OSError`
      を返すようになりました。

.. function:: move(src, dst)

   再帰的にファイルやディレクトリを別の場所へ移動します。

   もし移動先が現在のファイルシステム上であれば単純に名前を変更します。
   そうでない場合は(:func:`copy2` で)コピーを行い、その後コピー元は削除されます。

   .. versionadded:: 2.3


.. exception:: Error

   この例外は複数ファイルの操作を行っているときに生じる例外をまとめたもの
   です。 :func:`copytree` に対しては例外の引数は3つのタプル(*srcname*, *dstname*,
   *exception*)からなるリストです。

   .. versionadded:: 2.3


.. _shutil-example:

使用例
------

以下は前述の :func:`copytree` 関数のドキュメント文字列を省略した実装例です。本モジュールで提供される他の関数の使い方を示しています。 ::

   def copytree(src, dst, symlinks=False, ignore=None):
       names = os.listdir(src)
       if ignore is not None:
           ignored_names = ignore(src, names)
       else:
           ignored_names = set()

       os.makedirs(dst)
       errors = []
       for name in names:
           if name in ignored_names:
               continue
           srcname = os.path.join(src, name)
           dstname = os.path.join(dst, name)
           try:
               if symlinks and os.path.islink(srcname):
                   linkto = os.readlink(srcname)
                   os.symlink(linkto, dstname)
               elif os.path.isdir(srcname):
                   copytree(srcname, dstname, symlinks, ignore)
               else:
                   copy2(srcname, dstname)
               # XXX What about devices, sockets etc.?
           except (IOError, os.error), why:
               errors.append((srcname, dstname, str(why)))
           # catch the Error from the recursive copytree so that we can
           # continue with other files
           except Error, err:
               errors.extend(err.args[0])
       try:
           copystat(src, dst)
       except WindowsError:
           # can't copy file access times on Windows
           pass
       except OSError, why:
           errors.extend((src, dst, str(why)))
       if errors:
           raise Error(errors)

:func:`ignore_patterns` ヘルパ関数を利用する、もう1つの例です。 ::

   from shutil import copytree, ignore_patterns

   copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))

この例では、 ``.pyc`` ファイルと、 ``tmp`` で始まる全てのファイルやディレクトリを除いて、
全てをコピーします。

*ignore* 引数にロギングさせる別の例です。 ::

   from shutil import copytree
   import logging

   def _logpath(path, names):
       logging.info('Working in %s' % path)
       return []   # nothing will be ignored

   copytree(source, destination, ignore=_logpath)

