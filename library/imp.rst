
:mod:`imp` --- :keyword:`import` 内部へアクセスする
===================================================

.. module:: imp
   :synopsis: import文の実装へアクセスする。


.. index:: statement: import

このモジュールは :keyword:`import` 文を実装するために使われているメカニズムへのインターフェイスを提供します。次の定数と関数が定義されています:


.. function:: get_magic()

   .. index:: pair: file; byte-code

   バイトコンパイルされたコードファイル(:file:`.pyc` ファイル)を認識するために使われるマジック文字列値を返します。(この値は Python の各バージョンで異なります。)


.. function:: get_suffixes()

   三つ組みのリストを返します。それぞれはモジュールの特定の型を説明しています。各三つ組みは形式 ``(suffix, mode, type)`` を持ちます。
   ここで、 *suffix* は探すファイル名を作るためにモジュール名に追加する文字列です。
   そのファイルをオープンするために、 *mode* は組み込み :func:`open` 関数へ渡されるモード文字列です(これはテキストファイル対しては ``'r'`` 、バイナリファイルに対しては ``'rb'`` となります)。
   *type* はファイル型で、以下で説明する値 :const:`PY_SOURCE`, :const:`PY_COMPILED` あるいは、 :const:`C_EXTENSION` の一つを取ります。


.. function:: find_module(name[, path])

   検索パス *path* 上でモジュール *name* を見つけようとします。 *path* がディレクトリ名のリストならば、上の :func:`get_suffixes` が返す拡張子のいずれかを伴ったファイルを各ディレクトリの中で検索します。リスト内の有効でない名前は黙って無視されます(しかし、すべてのリスト項目は文字列でなければならない)。 *path* が省略されるか ``None`` ならば、 ``sys.path`` のディレクトリ名のリストが検索されます。しかし、最初にいくつか特別な場所を検索します。所定の名前(:const:`C_BUILTIN`)をもつ組み込みモジュールを見つけようとします。それから、フリーズされたモジュール(:const:`PY_FROZEN`)、同様にいくつかのシステムと他の場所がみられます(Windowsでは、特定のファイルを指すレジストリの中を見ます)。

   検索が成功すれば、戻り値は三要素のタプル ``(file, pathname, description)`` です:

   *file* は先頭に位置を合わされたオープンファイルオブジェクトで、 *pathname* は見つかったファイルのパス名です。そして、 *description* は :func:`get_suffixes` が返すリストに含まれているような三つ組みで、見つかったモジュールの種類を説明しています。

   モジュールがファイルの中にあるならば、返された *file* は ``None`` で、 *pathname* は空文字列、 *description* タプルはその拡張子とモードに対して空文字列を含みます。モジュール型は上の括弧の中に示されます。検索が失敗すれば、 :exc:`ImportError` が発生します。他の例外は引数または環境に問題があることを示唆します。

   モジュールがパッケージならば、 *file* は ``None`` で、 *pathname* はパッケージのパスで *description* タプルの最後の項目は :const:`PKG_DIRECTORY` です。

   この関数は階層的なモジュール名(ドットを含んだ名前)を扱いません。 *P.M* 、すなわち、パッケージ *P* のサブモジュール *M* を見つけるためには、パッケージ *P* を見つけてロードするために :func:`find_module` と :func:`load_module` を使い、それから ``P.__path__`` に設定された *path* 引数とともに :func:`find_module` を使ってください。 *P* 自身がドット名のときは、このレシピを再帰的に適用してください。


.. function:: load_module(name, file, pathname, description)

   .. index:: builtin: reload

   :func:`find_module` を使って(あるいは、互換性のある結果を作り出す検索を行って)以前見つけたモジュールをロードします。この関数はモジュールをインポートするという以上のことを行います:
   モジュールが既にインポートされているならば、 :func:`reload` と同じです! *name* 引数は(これがパッケージのサブモジュールならばパッケージ名を含む)完全なモジュール名を示します。 *file* 引数はオープンしたファイルで、 *pathname* は対応するファイル名です。モジュールがパッケージであるかファイルからロードされようとしていないとき、これらはそれぞれ ``None`` と ``''`` であっても構いません。 :func:`get_suffixes` が返すように *description* 引数はタプルで、どの種類のモジュールがロードされなければならないかを説明するものです。

   ロードが成功したならば、戻り値はモジュールオブジェクトです。そうでなければ、例外(たいていは :exc:`ImportError`)が発生します。

   **重要:** *file* 引数が ``None`` でなければ、例外が発生した時でさえ呼び出し側にはそれを閉じる責任があります。これを行うには、 :keyword:`try` ... :keyword:`finally` 文をつかうことが最も良いです。


.. function:: new_module(name)

   *name* という名前の新しい空モジュールオブジェクトを返します。このオブジェクトは ``sys.modules`` に挿入され *ません* 。


.. function:: lock_held()

   現在インポートロックが維持されているならば、 ``True`` を返します。そうでなければ、 ``False`` を返します。スレッドのないプラットホームでは、常に ``False`` を返します。

   スレッドのあるプラットホームでは、インポートが完了するまでインポートを実行するスレッドは内部ロックを維持します。このロックは元のインポートが完了するまで他のスレッドがインポートすることを阻止します。言い換えると、元のスレッドがそのインポート(および、もしあるならば、それによって引き起こされるインポート)の途中で構築した不完全なモジュールオブジェクトを、他のスレッドが見られないようにします。


.. function:: acquire_lock()

   実行中のスレッドでインタープリタのインポートロックを取得します。スレッドセーフなインポートフックでは、インポート時にこのロックを取得します。

   一旦スレッドが インポートロックを取得したら、その同じスレッドはブロックされることなくそのロックを再度取得できます。スレッドはロックを取得するのと同じだけ解放しなければなりません。

   スレッドのないプラットホームではこの関数は何もしません。

   .. versionadded:: 2.3


.. function:: release_lock()

   インタープリタのインポートロックを解放します。スレッドのないプラットホームではこの関数は何もしません。

   .. versionadded:: 2.3

整数値をもつ次の定数はこのモジュールの中で定義されており、 :func:`find_module` の検索結果を表すために使われます。


.. data:: PY_SOURCE

   ソースファイルとしてモジュールが発見された。


.. data:: PY_COMPILED

   コンパイルされたコードオブジェクトファイルとしてモジュールが発見された。


.. data:: C_EXTENSION

   動的にロード可能な共有ライブラリとしてモジュールが発見された。


.. data:: PKG_DIRECTORY

   パッケージディレクトリとしてモジュールが発見された。


.. data:: C_BUILTIN

   モジュールが組み込みモジュールとして発見された。


.. data:: PY_FROZEN

   モジュールがフリーズされたモジュールとして発見された(:func:`init_frozen` を参照)。

次の定数と関数は旧式のものです。それらの機能は :func:`find_module` や :func:`load_module` を使って利用できます。後方互換性のために残されています:


.. data:: SEARCH_ERROR

   使われていません。


.. function:: init_builtin(name)

   *name* という名前の組み込みモジュールを初期化し、そのモジュールオブジェクトを ``sys.modules`` に格納しておいて返します。モジュールが既に初期化されている場合は、 *再度* 初期化されます。再初期化はビルトインモジュールの ``__dict__`` を ``sys.modules`` のエントリーに結びつけられたキャッシュモジュールからコピーする過程を含みます。 *name* という名前の組み込みモジュールがない場合は、 ``None`` を返します。


.. function:: init_frozen(name)

   *name* という名前のフリーズされたモジュールを初期化し、モジュールオブジェクトを返します。モジュールが既に初期化されている場合は、 *再度* 初期化されます。 *name* という名前のフリーズされたモジュールがない場合は、 ``None`` を返します。(フリーズされたモジュールは Python で書かれたモジュールで、そのコンパイルされたバイトコードオブジェクトが Python の :program:`freeze` ユーティリティを使ってカスタムビルト Python インタープリタへ組み込まれています。差し当たり、 :file:`Tools/freeze/` を参照してください。)


.. function:: is_builtin(name)

   *name* という名前の再度初期化できる組み込みモジュールがある場合は、 ``1`` を返します。 *name* という名前の再度初期化できない組み込みモジュールがある場合は、 ``-1`` を返します(:func:`init_builtin` を参照してください)。 *name* という名前の組み込みモジュールがない場合は、 ``0`` を返します。


.. function:: is_frozen(name)

   *name* という名前のフリーズされたモジュール(:func:`init_frozen` を参照)がある場合は、 ``True`` を返します。または、そのようなモジュールがない場合は、 ``False`` を返します。


.. function:: load_compiled(name, pathname[, file])

   .. index:: pair: file; byte-code

   バイトコンパイルされたコードファイルとして実装されているモジュールをロードして初期化し、そのモジュールオブジェクトを返します。モジュールが既に初期化されている場合は、 *再度* 初期化されます。 *name* 引数はモジュールオブジェクトを作ったり、アクセスするために使います。 *pathname* 引数はバイトコンパイルされたコードファイルを指します。 *file* 引数はバイトコンパイルされたコードファイルで、バイナリモードでオープンされ、先頭からアクセスされます。現在は、ユーザ定義のファイルをエミュレートするクラスではなく、実際のファイルオブジェクトでなければなりません。


.. function:: load_dynamic(name, pathname[, file])

   動的ロード可能な共有ライブラリとして実装されているモジュールをロードして初期化します。モジュールが既に初期化されている場合は、 *再度* 初期化します。
   再初期化はモジュールのキャッシュされたインスタンスの ``__dict__`` 属性を ``sys.modules`` にキャッシュされたモジュールの中で使われた値の上にコピーする過程を含みます。
   *pathname* 引数は共有ライブラリを指していなければなりません。 *name* 引数は初期化関数の名前を作るために使われます。共有ライブラリの ``initname()`` という名前の外部C関数が呼び出されます。オプションの *file* 引数は無視されます。(注意:
   共有ライブラリはシステムに大きく依存します。また、すべてのシステムがそれをサポートしているわけではありません。)


.. function:: load_source(name, pathname[, file])

   Python ソースファイルとして実装されているモジュールをロードして初期化し、モジュールオブジェクトを返します。モジュールが既に初期化されている場合は、 *再度* 初期化します。 *name* 引数はモジュールオブジェクトを作成したり、アクセスしたりするために使われます。 *pathname* 引数はソースファイルを指します。 *file* 引数はソースファイルで、テキストとして読み込むためにオープンされ、先頭からアクセスされます。現在は、ユーザ定義のファイルをエミュレートするクラスではなく、実際のファイルオブジェクトでなければなりません。(拡張子 :file:`.pyc` または :file:`.pyo` をもつ)正しく対応するバイトコンパイルされたファイルが存在する場合は、与えられたソースファイルを構文解析する代わりにそれが使われることに注意してください。


.. class:: NullImporter(path_string)

   :class:`NullImporter` 型は :pep:`302` インポートフックで、何もモジュールが見つからなかったときの非ディレクトリパス文字列を処理します。この型を既存のディレクトリや空文字列に対してコールすると :exc:`ImportError` が発生します。それ以外の場合は :class:`NullImporter` のインスタンスが返されます。

   Python は、ディレクトリでなく ``sys.path_hooks`` のどのパスフックでも処理されていないすべてのパスエントリに対して、この型のインスタンスを ``sys.path_importer_cache`` に追加します。このインスタンスが持つメソッドは次のひとつです。


   .. method:: NullImporter.find_module(fullname [, path])

      このメソッドは常に ``None`` を返し、要求されたモジュールが見つからなかったことを表します。

   .. versionadded:: 2.5


.. _examples-imp:

例
--

次の関数は Python
1.4 までの標準 import 文(階層的なモジュール名がない)をエミュレートします。(この *実装* はそのバージョンでは動作しないでしょう。なぜなら、 :func:`find_module` は拡張されており、また :func:`load_module` が 1.4 で追加されているからです。)
::

   import imp
   import sys

   def __import__(name, globals=None, locals=None, fromlist=None):
       # Fast path: see if the module has already been imported.
       try:
           return sys.modules[name]
       except KeyError:
           pass

       # If any of the following calls raises an exception,
       # there's a problem we can't handle -- let the caller handle it.

       fp, pathname, description = imp.find_module(name)

       try:
           return imp.load_module(name, fp, pathname, description)
       finally:
           # Since we may exit via an exception, close fp explicitly.
           if fp:
               fp.close()

.. index::
   builtin: reload
   module: knee

階層的なモジュール名を実装し、 :func:`reload` 関数を含むより完全な例はモジュール :mod:`knee` にあります。 :mod:`knee` モジュールは Python のソースディストリビューションの中の :file:`Demo/imputil/` にあります。

