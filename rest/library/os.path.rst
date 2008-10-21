
:mod:`os.path` --- 共通のパス名操作
===================================

.. module:: os.path




このモジュールには、パス名を操作する便利な関数が定義されています。

.. index:: single: path; operations

.. warning::

   これらの関数の多くはWindowsの一律命名規則（UNCパス名）を正しく
   サポートしていません。:func:`splitunc`と:func:`ismount`は正し くUNCパス名を操作できます。


.. function:: abspath(path)

   *path*の標準化された絶対パスを返します。 たいていのプラットフォームでは、 ``normpath(join(os.getcwd(),
   path))``と同じ結果になります。

   .. versionadded:: 1.5.2


.. function:: basename(path)

   パス名*path*の末尾のファイル名を返します。 これは``split(path)``で返されるペアの２番目の要素です。 この関数が返す値はUnixの
   :program:`basename`とは異なります； Unixの:program:`basename`は``'/foo/bar/'``に対して
   ``'bar'``を返しますが、:func:`basename`は空文字列(``''``) を返します。


.. function:: commonprefix(list)

   パスの*list*の中の共通する最長のプレフィックスを（パス名の１文字１文 字を判断して）返します。
   もし*list*が空なら、空文字列(``''``)を返します。 これは一度に１文字を扱うため、不正なパスを返すことがあるかもしれませんの で注意して下さい。


.. function:: dirname(path)

   パス*path*のディレクトリ名を返します。 これは``split(path)``で返されるペアの最初の要素です。


.. function:: exists(path)

   *path*が存在するなら、``True``を返します。 壊れたシンボリッックリンクについては``False``を返します。 いくつかのプラットフォームでは、
   たとえ *path* が物理的に存在していたとしても、 リクエストされたファイルに対する :func:`os.stat` の実行が許可されなければ この関数が
   ``False`` を返すことがあります。


.. function:: lexists(path)

   *path* が存在するパスなら``True`` を返す。 壊れたシンボリッックリンクについては``True``を返します。
   :func:`os.lstat`がない環境では:func:`exists`と同じです。

   .. versionadded:: 2.4


.. function:: expanduser(path)

   .. index:: module: pwd

   Unixでは、 与えられた引数の先頭のパス要素``~``または``~user``を、 *user*のホームディレクトリのパスに置き換えて返します。
   先頭の``~``は、環境変数:envvar:`HOME`が設定されているならその値に置き換えられます。
   そうでなければ、現在のユーザのホームディレクトリをビルトインモジュール :mod:`pwd`を使ってパスワードディレクトリ から探して置き換えます。
   先頭の``~user``については、直接パスワードディレクトリから探します。

   Windows では``~``だけがサポートされ、環境変数:envvar:`HOME`または
   :envvar:`HOMEDRIVE`と:envvar:`HOMEPATH`の組み合わせで置き換えられます。

   もし置き換えに失敗したり、引数のパスがチルダで始まっていなかったら、パス をそのまま返します。


.. function:: expandvars(path)

   引数のパスを環境変数に展開して返します。 引数の中の``$name``または``${name}``の文字列が 環境変数の*name*に置き換えられます。
   不正な変数名や存在しない変数名の場合には変換されず、そのまま返します。


.. function:: getatime(path)

   *path*に最後にアクセスした時刻を、エポック（:mod:`time`モジュール を参照）からの経過時間を示す秒数で返します。
   ファイルが存在しなかったりアクセスできない場合は:exc:`os.error`を発 生します。

   .. versionchanged:: 2.3
      :func:`os.stat_float_times`がTrueを返す場合、戻り値は 浮動小数点値となります。.

   .. versionadded:: 1.5.2


.. function:: getmtime(path)

   *path*の最終更新時刻を、エポック（:mod:`time`モジュールを参照） からの経過時間を示す秒数で返します。
   ファイルが存在しなかったりアクセスできない場合は:exc:`os.error`を発 生します。

   .. versionchanged:: 2.3
      :func:`os.stat_float_times`がTrueを返す場合、戻り値は 浮動小数点値となります。.

   .. versionadded:: 1.5.2


.. function:: getctime(path)

   システムによって、ファイルの最終変更時刻 (Unix のような システム) や 作成時刻 (Windows のようなシステム) をシステムの ctime
   で返します。 戻り値はエポック（:mod:`time`モジュールを参照）からの経過秒数を 示す数値です。
   ファイルが存在しなかったりアクセスできない場合は:exc:`os.error`を発 生します。

   .. versionadded:: 2.3


.. function:: getsize(path)

   ファイル*path*のサイズをバイト数で返します。 ファイルが存在しなかったりアクセスできない場合は:exc:`os.error`を発 生します。

   .. versionadded:: 1.5.2


.. function:: isabs(path)

   *path*が絶対パス（スラッシュで始まる）なら、``True``を返します。


.. function:: isfile(path)

   *path*が存在する正しいファイルなら、*True*を返します。 シンボリックリンクの場合にはその実体をチェックするので、同じパスに対して
   :func:`islink`と:func:`isfile`の両方が*True*を返すことがあ ります。


.. function:: isdir(path)

   *path*が存在するなら、``True``を返します。 シンボリックリンクの場合にはその実体をチェックするので、同じパスに対して
   :func:`islink`と:func:`isfile`の両方が*True*を返すことがあ ります。


.. function:: islink(path)

   *path*がシンボリックリンクなら、``True``を返します。 シンボリックリンクがサポートされていないプラットフォームでは、常に
   ``False``を返します。


.. function:: ismount(path)

   パス名*path*がマウントポイント:dfn:`mount point`（ファイルシステムの
   中で異なるファイルシステムがマウントされているところ）なら、``True`` を返します：
   この関数は*path*の親ディレクトリである:file:`path/..`が *path*と異なるデバイス上にあるか、あるいは:file:`path/..`と
   *path*が同じデバイス上の同じi-nodeを指しているかをチェックします--- これによって全てのUnixとPOSIX標準でマウントポイントが検出できま
   す。


.. function:: join(path1[, path2[, ...]])

   １つあるいはそれ以上のパスの要素をうまく結合します。 付け加える要素に絶対パスがあれば、それより前の要素は(Windows ではドライブ名
   があればそれも含めて)全て破棄され、以降の要素を結合します。 戻り値は*path1*と省略可能な*path2*以降を結合したもので、
   *path2*が空文字列でないなら、ディレクトリの区切り文字(``os.sep``) が各要素の間に挿入されます。
   Windowsでは各ドライブに対してカレントディレクトリがあるので、 :func:`os.path.join("c:", "foo")`によって、
   :file:`c:\\\\foo`ではなく、ドライブ:file:`C:`上の カレントディレクトリからの相対パス（:file:`c:foo`）が返されます。


.. function:: normcase(path)

   パス名の大文字、小文字をシステムの標準にします。 Unixではそのまま返します。大文字、小文字を区別しないファイルシステム ではパス名を小文字に変換します。
   Windowsでは、スラッシュをバックスラッシュに変換します。


.. function:: normpath(path)

   パス名を標準化します。 余分な区切り文字や上位レベル参照を削除し、``A//B``、
   ``A/./B``、``A/foo/../B``が全て``A/B``になるようにします。
   大文字、小文字は標準化しません（それには:func:`normcase`を使って下 さい）。 Windowsでは、スラッシュをバックスラッシュに変換します。
   パスがシンボリックリンクを含んでいるかによって意味が変わることに注意し てください。


.. function:: realpath(path)

   パスの中のシンボリックリンク(もしそれが当該オペレーティングシステムで サポートされていれば)を取り除いて、標準化したパスを返します。

   .. versionadded:: 2.2


.. function:: samefile(path1, path2)

   ２つの引数であるパス名が同じファイルあるいはディレクトリを指していれば（ 同じデバイスナンバーとi-nodeナンバーで示されていれば）、``True``を返
   します。 どちらかのパス名で:func:`os.stat`の呼び出しに失敗した場合には、例外 が発生します。 利用可能：Macintosh、Unix


.. function:: sameopenfile(fp1, fp2)

   ファイルディスクリプタ*fp1*と*fp2*が同じファイルを指していたら、 ``True``を返します。 利用可能：Macintosh、Unix


.. function:: samestat(stat1, stat2)

   statタプル*stat1*と*stat2*が同じファイルを指していたら、 ``True``を返します。
   これらのタプルは:func:`fstat`、:func:`lstat`や :func:`stat`で返されたものでかまいません。
   この関数は、:func:`samefile`と:func:`sameopenfile`で使われるの と同様なものを背後に実装しています。
   利用可能：Macintosh、Unix


.. function:: split(path)

   パス名*path*を``(headとtail)``のペアに分割します。 *tail*はパスの構成要素の末尾で、*head*はそれより前の部分です。
   *tail*はスラッシュを含みません；もし*path*の最後にスラッシュがあ れば、*tail*は空文字列になります。
   もし*path*にスラッシュがなければ、*head*は空文字列になります。 *path*が空文字列なら、*head*と*tail*のどちらも空文字列になり
   ます。 *head*の末尾のスラッシュは、*head*がルートディレクトリ（１つ以上 のスラッシュのみ）でない限り、取り除かれます。
   ほとんど全ての場合、``join(head, tail)``の結果が *path*と等しくなります（ただ１つの例外は、複数のスラッシュが
   *head*と*tail*を分けている時です）。


.. function:: splitdrive(path)

   パス名*path*を``(drive,tail)``のペアに分割します。 *drive*はドライブ名か、空文字列です。
   ドライブ名を使用しないシステムでは、*drive*は常に空文字列です。 全ての場合に``drive + tail``は*path*と等しくなりま す。

   .. versionadded:: 1.3


.. function:: splitext(path)

   パス名*path*を``(root, ext)``のペアにします。 ``root + ext == path``になります。
   *ext*は空文字列か１つのピリオドで始まり、多くても１つのピリオドを含 みます。


.. function:: splitunc(path)

   パス名*path*をペア ``(unc, rest)`` に分割します。
   ここで*unc*は(``r'\\host\mount'``のような)UNCマウントポイント、
   そして*rest*は(``r'\path\file.ext'``のような)パスの残りの部分です。 ドライブ名を含むパスでは常に*unc*が空文字列になります。
   利用可能:  Windows。


.. function:: walk(path, visit, arg)

   *path*をルートとする各ディレクトリに対して（もし*path*がディレク トリなら*path*も含みます）、``(arg, dirname,
   names)``を引数として関数*visit*を呼び出します。 引数*dirname*は訪れたディレクトリを示し、引数*names*はそのディレ
   クトリ内のファイルのリスト（``os.listdir(dirname)``で得られる） です。
   関数*visit*によって*names*を変更して、*dirname*以下の対象と なるディレクトリのセットを変更することもできます。例えば、あるディレクト
   リツリーだけ関数を適用しないなど。 （*names*で参照されるオブジェクトは、:keyword:`del`あるいはスライスを
   使って正しく変更しなければなりません。）

   .. note::

      ディレクトリへのシンボリックリンクはサブディレクトリとして扱われないの で、:func:`walk`による操作対象とはされません。
      ディレクトリへのシンボリックリンクを操作対象とするには、 ``os.path.islink(file)``と``os.path.isdir(file)``
      で識別して、:func:`walk`で必要な操作を実行しなければなりません。

   .. note::

      新たに追加された:func:`os.walk` ジェネレータを 使用すれば、同じ処理をより簡単に行う事ができます。


.. data:: supports_unicode_filenames

   任意のユニコード文字列を（ファイルシステムの制限内で） ファイルネームに使うことが可能で、:func:`os.listdir`がユニコード文字列の
   引数に対してユニコードを返すなら、真を返します。

   .. versionadded:: 2.3

