
:mod:`stat` --- :func:`stat` の返す内容を解釈する
=================================================

.. module:: stat
   :synopsis: os.stat()、os.lstat() および os.fstat() の返す内容を解釈するためのユーティリティ群。
.. sectionauthor:: Skip Montanaro <skip@automatrix.com>


:mod:`stat` モジュールでは、 :func:`os.stat` 、 :func:`os.lstat` および :func:`os.fstat`
(存在すれば) の返す内容を解釈するための定数や関数を定義しています。
:cfunc:`stat` 、 :cfunc:`fstat` 、および :cfunc:`lstat`
の関数呼び出しについての完全な記述はシステムのドキュメントを参照してください。

:mod:`stat` モジュールでは、特殊なファイル型を判別するための以下の関数を定義しています:


.. function:: S_ISDIR(mode)

   ファイルのモードがディレクトリの場合にゼロでない値を返します。


.. function:: S_ISCHR(mode)

   ファイルのモードがキャラクタ型の特殊デバイスファイルの場合にゼロでない値を返します。


.. function:: S_ISBLK(mode)

   ファイルのモードがブロック型の特殊デバイスファイルの場合にゼロでない値を返します。


.. function:: S_ISREG(mode)

   ファイルのモードが通常ファイルの場合にゼロでない値を返します。


.. function:: S_ISFIFO(mode)

   ファイルのモードが FIFO (名前つきパイプ) の場合にゼロでない値を返します。


.. function:: S_ISLNK(mode)

   ファイルのモードがシンボリックリンクの場合にゼロでない値を返します。


.. function:: S_ISSOCK(mode)

   ファイルのモードがソケットの場合にゼロでない値を返します。

より一般的なファイルのモードを操作するための二つの関数が定義されています:


.. function:: S_IMODE(mode)

   :func:`os.chmod` で設定することのできる一部のファイルモード ---
   すなわち、ファイルの許可ビット (permission bits) に加え、 (サポートされているシステムでは)
   スティッキービット (sticky bit)、実行グループ ID 設定 (set-group-id) および
   実行ユーザ ID 設定  (set-user-id) ビット --- を返します。


.. function:: S_IFMT(mode)

   ファイルの形式を記述しているファイルモードの一部 (上記の  :func:`S_IS\*` 関数で使われます) を返します。

通常、ファイルの形式を調べる場合には :func:`os.path.is\*` 関数を使うことになります; ここで挙げた関数は同じファイルに対して
複数のテストを同時に行いたいが、 :cfunc:`stat` システムコールを何度も呼び出してオーバヘッドが生じるのを避けたい場合に便利です。
これらはまた、ブロック型およびキャラクタ型デバイスに対するテストのように、 :mod:`os.path` で扱うことのできないファイルの
情報を調べる際にも便利です。

以下の全ての変数は、 :func:`os.stat` 、 :func:`os.fstat` 、または :func:`os.lstat` が返す 10
要素のタプルにおけるインデクスを単にシンボル定数化したものです。


.. data:: ST_MODE

   Iノードの保護モード。


.. data:: ST_INO

   Iノード番号。


.. data:: ST_DEV

   Iノードが存在するデバイス。


.. data:: ST_NLINK

   該当する Iノードへのリンク数。


.. data:: ST_UID

   ファイルの所持者のユーザ ID。


.. data:: ST_GID

   ファイルの所持者のグループ ID。


.. data:: ST_SIZE

   通常ファイルではバイトサイズ; いくつかの特殊ファイルでは処理待ちのデータ量。


.. data:: ST_ATIME

   最後にアクセスした時刻。


.. data:: ST_MTIME

   最後に変更された時刻。


.. data:: ST_CTIME

   オペレーティングシステムから返される"ctime"。あるOS(Unixなど)では最
   後にメタデータが更新された時間となり、別のOS(Windowsなど)では作成時間と
   なります(詳細については各プラットフォームのドキュメントを参照してください)。

"ファイルサイズ" の解釈はファイルの型によって異なります。通常のファイルの場合、サイズはファイルの大きさをバイトで表したものです。ほとんどの Unix 系
(特に Linux) における FIFO やソケットの場合、"サイズ" は :func:`os.stat` 、 :func:`os.fstat` 、あるいは
:func:`os.lstat` を呼び出した時点で読み出し待ちであったデータのバイト数になります; この値は時に有用で、特に上記の特殊なファイル
を非ブロックモードで開いた後にポーリングを行いたいといった場合に便利です。他のキャラクタ型およびブロック型デバイスにおけるサイズ
フィールドの意味はさらに異なっていて、背後のシステムコールの実装によります。

例を以下に示します::

   import os, sys
   from stat import *

   def walktree(top, callback):
       '''recursively descend the directory tree rooted at top,
          calling the callback function for each regular file'''

       for f in os.listdir(top):
           pathname = os.path.join(top, f)
           mode = os.stat(pathname)[ST_MODE]
           if S_ISDIR(mode):
               # It's a directory, recurse into it
               walktree(pathname, callback)
           elif S_ISREG(mode):
               # It's a file, call the callback function
               callback(pathname)
           else:
               # Unknown file type, print a message
               print 'Skipping %s' % pathname

   def visitfile(file):
       print 'visiting', file

   if __name__ == '__main__':
       walktree(sys.argv[1], visitfile)

