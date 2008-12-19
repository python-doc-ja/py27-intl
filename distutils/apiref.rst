.. _api-reference:

****************
API リファレンス
****************


:mod:`distutils.core` --- Distutils のコア機能
==============================================

.. module:: distutils.core
   :synopsis: Distutils のコア機能


Distutilsを使うためにインストールする必要がある唯一のモジュールが
:mod:`distutils.core`モジュールです。:func:`setup`関数 (セットアップスクリプトから呼び出されます)を提供します。間接的に
:class:`distutils.dist.Distribution`クラスと :class:`distutils.cmd.Command`
クラスを提供します。


.. function:: setup(arguments)

   全てを実行する基本的な関数で、Distutilsでできるほとんどのことを実行し ます。 XXXXを参照してください。

   setup関数はたくさんの引数をとります。以下のテーブルにまとめます。

   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | argument name      | value                                                      | type                                                            |
   +====================+============================================================+=================================================================+
   | *name*             | パッケージの名前                                           | 文字列                                                          |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *version*          | パッケージのバージョン番号                                 | :mod:`distutils.version`を参照してください                      |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *description*      | 1行で書いたパッケージ解説                                  | 文字列                                                          |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *long_description* | パッケージの長い解説                                       | 文字列                                                          |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *author*           | パッケージ作者の名前                                       | 文字列                                                          |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *author_email*     | パッケージ作者のemailアドレス                              | 文字列                                                          |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *maintainer*       | 現在のメンテナの名前(パッケージ作者と異なる場合)           | 文字列                                                          |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *maintainer_email* | 現在のメンテナのemailアドレス(パッケージ作者と異なる場合)  |                                                                 |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *url*              | パッケージのURL(ホームページ)                              | URL                                                             |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *download_url*     | パッケージダウンロード用URL                                | URL                                                             |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *packages*         | distutilsが操作するPythonパッケージのリスト                | 文字列のリスト                                                  |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *py_modules*       | distutilsが操作するPythonモジュールのリスト                | 文字列のリスト                                                  |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *scripts*          | ビルドおよびインストールする単体スクリプトファイルのリスト | 文字列のリスト                                                  |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *ext_modules*      | ビルドする拡張モジュール                                   | :class:`distutils.core.Extension`インスタンスのリスト           |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *classifiers*      | パッケージのカテゴリのリスト                               | 利用可能なカテゴリ一覧は                                        |
   |                    |                                                            | `<http://cheeseshop.python.org/pypi?:action=list_classifiers>`_ |
   |                    |                                                            | にあります。                                                    |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *distclass*        | 使用する :class:`Distribution`クラス                       | :class:`distutils.core.Distribution`のサブクラス                |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *script_name*      | setup.pyスクリプトの名前 -                                 | 文字列                                                          |
   |                    | デフォルトでは``sys.argv[0]``                              |                                                                 |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *script_args*      | セットアップスクリプトの引数                               | 文字列のリスト                                                  |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *options*          | セットアップスクリプトのデフォルト引数                     | 文字列                                                          |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *license*          | パッケージのライセンス                                     |                                                                 |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *keywords*         | 説明用メタデータ。 :pep:`314`を参照してください            |                                                                 |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *platforms*        |                                                            |                                                                 |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+
   | *cmdclass*         | コマンド名から :class:`Command`                            | 辞書                                                            |
   |                    | サブクラスへのマッピング                                   |                                                                 |
   +--------------------+------------------------------------------------------------+-----------------------------------------------------------------+

   利用可能なカテゴリ一覧は `<http://cheeseshop.python.org/pypi?:action=list_classifiers>`_
   にあります。


.. function:: run_setup(script_name[, script_args=``None``, stop_after=``'run'``])

   制御された環境でセットアップスクリプトを実行し、いろいろなものを操作する
   :class:`distutils.dist.Distribution`クラスのインスタンスを返します。
   これはディストリビューションのメタデータ(キーワード引数*script*と して 関数:func:`setup`に渡される)を参照したり、設定ファイルやコマ
   ンドラインの内容を調べる時に便利です。

   *script_name* は :func:`execfile`で実行されるファイルです。 ``sys.argv[0]`` は、
   呼び出しのために*script_name*と置換されます。  *script_args* は文字列のリストです。もし提供されていた場合、
   ``sys.argv[1:]`` は、呼び出しのために*script_args* で置換されます。

   *stop_after* は いつ動作を停止するか関数:func:`setup` に伝えます。 とりうる値は:

   +---------------+-----------------------------------------------------------------+
   | 値            | 説明                                                            |
   +===============+=================================================================+
   | *init*        | :class:`Distribution`インスタンスを作成し、キーワード引数を     |
   |               | :func:`setup`に渡したあとに停止する。                           |
   +---------------+-----------------------------------------------------------------+
   | *config*      | 設定ファイルをパーズしたあと停止する(そしてそのデータは         |
   |               | :class:`Distribution`インスタンスに保存される)。                |
   +---------------+-----------------------------------------------------------------+
   | *commandline* | コマンドライン (``sys.argv[1:]`` または                         |
   |               | *script_args*) がパーズされたあとに停止する (そしてそのデータは |
   |               | :class:`Distribution`インスタンスに保存される)。                |
   +---------------+-----------------------------------------------------------------+
   | *run*         | 全てのコマンドを実行したあとに停止する(関数 :func:`setup`       |
   |               | を通常の方法で呼び出した場合と同じ)。 デフォルト値。            |
   +---------------+-----------------------------------------------------------------+

これに加えて、:mod:`distutils.core`モジュールは他のモジュールにある いくつかのクラスを公開しています。

* :class:`Extension` は :mod:`distutils.extension` から。

* :class:`Command` は :mod:`distutils.cmd` から。

* :class:`Distribution` は :mod:`distutils.dist` から。

それぞれの簡単な説明を以下に記します。完全な説明についてはそれぞれの モジュールをごらんください。


.. class:: Extension

   Extension クラスは、セットアップスクリプト中で C または C++拡張モジュー ルを表します。コンストラクタで以下のキーワード引数をとります。

   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | argument name          | value                                                                            | type                     |
   +========================+==================================================================================+==========================+
   | *name*                 | 拡張のフルネーム(パッケージを含む) ---                                           | string                   |
   |                        | ファイル名やパス                                                                 |                          |
   |                        | 名では*なく*、Pythonのピリオド区切りの名前                                       |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *sources*              | ソースファイル名のリスト。配布物ルートディレクトリ                               | string                   |
   |                        | (setupスクリプトのある場所)                                                      |                          |
   |                        | からの相対パス、プラットフォーム独立のた め Unix                                 |                          |
   |                        | 形式(スラッシュで区切る)で記述します。ソースファイルは                           |                          |
   |                        | C, C++, SWIG                                                                     |                          |
   |                        | (.i)、特定プラットフォーム用のリソースファイル、その他                           |                          |
   |                        | :command:`build_ext`コマンドがソースファイルだと認識するどの形式でもありえます。 |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *include_dirs*         | C/C++ヘッダファイルを検索するディレクトリのリ                                    | string                   |
   |                        | スト(プラットフォーム独立のため Unix 形式で記述する)                             |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *define_macros*        | 定義するマクロのリスト; それぞれのマクロは                                       | (string,string)  または  |
   |                        | 2要素のタプルで定義されます。'値'には定義しようとしている文字列、                | (name,``None``) のタプル |
   |                        | または内容なしで定義する場合は``None``\                                          |                          |
   |                        | (ソースコード中で ``#define                                                      |                          |
   |                        | FOO``と書く、または Unix                                                         |                          |
   |                        | Cコンパイラのコマンドラインで                                                    |                          |
   |                        | :option:`-DFOO`                                                                  |                          |
   |                        | を指定するのと等価です)を指定します。                                            |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *undef_macros*         | 定義を消すマクロのリスト                                                         | string                   |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *library_dirs*         | リンク時にC/C++ライブラリを検索するディレクトリのリスト                          | string                   |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *libraries*            | リンクするライブラリ名のリスト (ファイル名やパスではない)                        | string                   |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *runtime_library_dirs* | 実行時(shared extensionでは、拡張が読み                                          | string                   |
   |                        | 込まれる時)に                                                                    |                          |
   |                        | C/C++ライブラリを探索するディレクトリのリスト                                    |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *extra_objects*        | 追加でリンクするファイル('sources'に対応するコー                                 | string                   |
   |                        | ドが含まれていないファイル、バイナリ形式のリソースファイルなど)のリスト          |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *extra_compile_args*   | 'sources'のソースをコンパイルする時に                                            | string                   |
   |                        | 追加するプラットフォーム特有またはコンパイラ特有の情報                           |                          |
   |                        | コマンドラインを利用できるプラットホームとコンパイラでは、これは通常             |                          |
   |                        | コマンドライン引数のリストですが、他のプラットホームでも、それは何か             |                          |
   |                        | に使えます。                                                                     |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *extra_link_args*      | オブジェクトファイルをリンクして拡張(または新しいPythonインタプ                  | string                   |
   |                        | リタ)を作る時に                                                                  |                          |
   |                        | 追加するプラットフォーム特有またはコンパイラ特有の情報                           |                          |
   |                        | 'extra_compile_args'に似た実装です。                                             |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *export_symbols*       | shared                                                                           | string                   |
   |                        | extensionからエクスポートされるシンボルのリスト。                                |                          |
   |                        | 全てのプラットフォームでは使われず、                                             |                          |
   |                        | Python拡張(典型的には ``init`` +                                                 |                          |
   |                        | extension_name という1つのシンボル                                               |                          |
   |                        | だけエクスポートする)に一般的に必要なものでもない。                              |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *depends*              | 拡張が依存するファイルのリスト                                                   | string                   |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+
   | *language*             | 拡張の言語 (例: ``'c'``, ``'c++'``,                                              | string                   |
   |                        | ``'objc'``)。指定しなければソースの拡張子で検出される。                          |                          |
   +------------------------+----------------------------------------------------------------------------------+--------------------------+


.. class:: Distribution

   :class:`Distribution`はPythonソフトウェアパッケージをどのようにビルド、 インストール、パッケージするかを定義する。

   :class:`Distribution`のコンストラクタが取りうる キーワード引数のリストに関しては、:func:`setup`関数を見てください。
   :func:`setup`は:class:`Distribution`のインスタンスを作ります。


.. class:: Command

   :class:`Command`クラス(そのサブクラスのインスタンス)はdistutilsのあるコマン ドを実装します。


:mod:`distutils.ccompiler` --- CCompiler ベースクラス
=====================================================

.. module:: distutils.ccompiler
   :synopsis: 抽象 CCompiler class


このモジュールは :class:`CCompiler`クラスの抽象ベースクラスを提供します。
:class:`CCompiler`のインスタンスはプロジェクトにおける全てのコンパイルお よびリンクに使われます。
コンパイラのオプションを設定するためのメソッドが提供されます --- マク ロ定義、includeディレクトリ、リンクパス、ライブラリなど。

このモジュールは以下の関数を提供します。


.. function:: gen_lib_options(compiler, library_dirs, runtime_library_dirs, libraries)

   ライブラリを探索するディレクトリ、特定のライブラリとのリンクをするための リンカオプションを生成します。 *libraries* と
   *library_dirs* はそれぞれライブラリ名(ファイル 名ではありません!)のリストと、探索ディレクトリのリストです。
   compilerで利用できるコマンドラインオプションのリスト(指定されたフォーマット文字列に依存します)を返します。


.. function:: gen_preprocess_options(macros, include_dirs)

   Cプリプロセッサオプション(:option:`-D`, :option:`-U`,
   :option:`-I`)を生成します。これらは少なくとも2つのコンパイラで利用可能です。 典型的な Unix のコンパイラと、VisualC++です。
   *macros*は1または2要素のタプルで``(name,)``は*name*マクロの削除 (-U)を意味し、
   *(name,value)*は*name*マクロを*value*として
   定義(:option:`-D`)します。*include_dirs*はディレクトリ名のリストで、ヘッダファ
   イルのサーチパスに追加されます(:option:`-I`)。 Unix のコンパイラと、Visual C++で利用できるコマンドラインオプショ
   ンのリストを返します。


.. function:: get_default_compiler(osname, platform)

   指定されたプラットフォームのデフォルトコンパイラを返します。

   問い合わせの*osname*はPython標準のOS名(``os.name``で返されるもの)のひとつであるべき
   で、*platform*は``sys.platform``で返される共通の値です。

   パラメータが指定されていない場合のデフォルト値は``os.name``と ``sys.platform``です。


.. function:: new_compiler(plat=None, compiler=None, verbose=0, dry_run=0, force=0)

   指定されたプラットフォーム/コンパイラの組み合わせ向けに、 CCompilerサブクラスのインスタンスを生成するファクトリ関数です。 *plat*
   のデフォルト値は ``os.name`` (例: ``'posix'``, ``'nt'``), *compiler*)、
   *compiler*のデフォルト値はプラトフォームのデフォルトコンパイラです。 現在は
   ``'posix'``と``'nt'``だけがサポートされています、デフォルトのコンパイラは "traditional Unix
   interface"(:class:`UnixCCompiler`クラス) と、 Visual C++(:class:`MSVCCompiler` クラス)
   です。 WindowsでUnixコンパイラオブジェクトを要求することも、UnixでMicrosoft
   コンパイラオブジェクトを要求することも可能です。*compiler*引数を与えると *plat*は無視されます。

   .. % Is the posix/nt only thing still true? Mac OS X seems to work, and
   .. % returns a UnixCCompiler instance. How to document this... hmm.


.. function:: show_compilers()

   利用可能なコンパイラのリストを表示します(:command:`build`, :command:`build_ext`,
   :command:`build_clib`の、:option:`--help-compiler`オプションで使われます。)


.. class:: CCompiler([verbose=``0``, dry_run=``0``, force=``0``])

   抽象ベースクラス :class:`CCompiler`は実際のコンパイラクラスで実装される必要のある
   インタフェースを定義しています。このクラスはコンパイラクラスで利用されるユーティリティメソッドも定義しています。

   コンパイラ抽象クラスの基本的な前提は、各インスタンスはあるプロジェクトを ビルドするときの全コンパイル/リンクで利用できるということです。
   そこで、コンパイルとリンクステップで共通する属性 ---  インクルードディレクトリ、マクロ定義、リンクするライブラリ など --- はコンパイラインスタンスの
   属性になります。 どのように各ファイルが扱われるかを変更できるように、ほとんどの 属性はコンパイルごと、またはリンクごとに与えることができます。

   各サブクラスのコンストラクタは Compiler クラスのインスタンスを作ります。 フラグは *verbose*(冗長な出力を表示します)、
   *dry_run*(実際にはそのステップを実行しません)、 そして*force*(依存関係を無視して全て再ビルドします)です。
   これらのフラグは全てデフォルト値が``0``\ (無効)になっています。
   :class:`CCompiler`またはサブクラスを直接インスタンス化したくない場合には、
   かわりに:func:`distutils.CCompiler.new_compiler`ファクトリ関数を利用してください。

   以下のメソッドで、Compilerクラスのインスタンスが使うコンパイラオプションを手動で変更できます。


   .. method:: CCompiler.add_include_dir(dir)

      *dir*をヘッダファイル探索ディレクトリのリストに追加します。 コンパイラは:meth:`add_include_dir`を呼び出した順にディレクトリを
      探索するよう指定されます。


   .. method:: CCompiler.set_include_dirs(dirs)

      探索されるディレクトリのリストを *dirs* (文字列のリスト)に設定します。 先に実行された
      :meth:`add_include_dir`は上書きされます。
      後で実行する:meth:`add_include_dir`は:meth:`set_include_dirs`の
      リストにディレクトリを追加します。これはコンパイラがデフォルトで探索する 標準インクルードディレクトリには影響しません。


   .. method:: CCompiler.add_library(libname)

      *libname*をコンパイラオブジェクトによるリンク時に使われる ライブラリのリストに追加します。*libname*はライブラリを含むファイル名ではなく、
      ライブラリそのものの名前です: 実際のファイル名はリンカ、コンパイラ、または コンパイラクラス(プラットフォームに依存します)から推測されます。

      リンカは:meth:`add_library`と:meth:`set_library`
      で渡された順にライブラリをリンクしようとします。ライブラリ名が重なることは 問題ありません。リンカは指定された回数だけライブラリとリンクしようとします。


   .. method:: CCompiler.set_libraries(libnames)

      コンパイラオブジェクトによるリンク時に使われるライブラリのリストを  *libnames*(文字列のリスト)に設定します。
      これはリンカがデフォルトでリンクする標準のシステムライブラリには影響しません。


   .. method:: CCompiler.add_library_dir(dir)

      :meth:`add_library` と :meth:`set_libraries`で指定された
      ライブラリを探索するディレクトリのリストに*dir*を追加します。 リンカは:meth:`add_library_dir`と
      :meth:`set_library_dirs`で 指定された順にディレクトリを探索されます。


   .. method:: CCompiler.set_library_dirs(dirs)

      ライブラリを探索するディレクトリを *dirs*(文字列のリスト)に設定します。 これはリンカがデフォルトで探索する標準ライブラリ探索パスには影響しません。


   .. method:: CCompiler.add_runtime_library_dir(dir)

      実行時に共有ライブラリを探索するディレクトリのリストに*dir*を追加します。


   .. method:: CCompiler.set_runtime_library_dirs(dirs)

      実行時に共有ライブラリを探索するディレクトリのリストを*dir*に設定します。 これはランタイムリンカがデフォルトで利用する標準探索パスには影響しません。


   .. method:: CCompiler.define_macro(name[, value=``None``])

      このコンパイラオブジェクトで実行される全てのコンパイルで利用される プリプロセッサのマクロを定義します。省略可能なパラメータ*value*は
      文字列であるべきです。省略された場合は、マクロは特定の値をとらずに定義され、 具体的な結果は利用されるコンパイラに依存します。 (XXX 本当に?
      これについてANSIで言及されている?)


   .. method:: CCompiler.undefine_macro(name)

      このコンパイラオブジェクトで実行される全てのコンパイルで利用される プリプロセッサのマクロ定義を消します。同じマクロを:meth:`define_macro`で
      定義し、:meth:`undefine_macro`で定義を削除した場合、後で呼び出されたものが 優先される(複数の再定義と削除を含みます)。
      もしコンパイルごと(すなわち:meth:`compile`の呼び出しごと)にマクロが再定義/削除 される場合も後で呼び出されたものが優先されます。


   .. method:: CCompiler.add_link_object(object)

      このコンパイラオブジェクトによる全てのリンクで利用される オブジェクトファイル(または類似のライブラリファイルや
      "リソースコンパイラ"の出力)のリストに*object*を追加します。


   .. method:: CCompiler.set_link_objects(objects)

      このコンパイラオブジェクトによる全てのリンクで利用される オブジェクトファイル(または類似のもの)のリストを*objects*に設定します。
      これはリンカがデフォルト利用する標準オブジェクトファイル(システムライブラリ など)には影響しません。

   以下のメソッドはコンパイラオプションの自動検出を実装しており、 GNU :program:`autoconf`に似たいくつかの機能を提供します。


   .. method:: CCompiler.detect_language(sources)

      与えられたファイルまたはファイルのリストの言語を検出します。 インスタンス属性:attr:`language_map`\ (辞書)と、
      :attr:`language_order` (リスト)を仕事に使います。


   .. method:: CCompiler.find_library_file(dirs, lib[, debug=``0``])

      指定されたディレクトリのリストから、スタティックまたは共有ライブラリファイル *lib*を探し、そのファイルのフルパスを返します。
      もし*debug*が真なら、(現在のプラットフォームで意味があれば)デバッグ版を探します。 指定されたどのディレクトリでも *lib* が見つからなければ
      ``None``を返します。


   .. method:: CCompiler.has_function(funcname [, includes=``None``, include_dirs=``None``, libraries=``None``, library_dirs=``None``])

      *funcname*が現在のプラットフォームでサポートされているかどうかをブール値で返します。 省略可能引数は追加のインクルードファイルやパス、
      ライブラリやパスを与えることでコンパイル環境を指定します。


   .. method:: CCompiler.library_dir_option(dir)

      *dir*をライブラリ探索ディレクトリに追加する コンパイラオプションを返します。


   .. method:: CCompiler.library_option(lib)

      共有ライブラリまたは実行ファイルにリンクされるライブラリ一覧に*lib*を追加する コンパイラオプションを返します。


   .. method:: CCompiler.runtime_library_dir_option(dir)

      ランタイムライブラリを検索するディレクトリのリストに  *dir*を追加するコンパイラオプションを返します。


   .. method:: CCompiler.set_executables(**args)

      コンパイルのいろいろなステージで実行される実行ファイル(とその引数)を定 義します。コンパイラクラス(の 'executables' 属性)によって実行ファイル
      のセットは変わる可能性がありますが、ほとんどは以下のものを持っています:

      +--------------+-----------------------------------------------------------+
      | attribute    | description                                               |
      +==============+===========================================================+
      | *compiler*   | C/C++ コンパイラ                                          |
      +--------------+-----------------------------------------------------------+
      | *linker_so*  | シェアードオブジェクト、ライブラリを作るために使う リンカ |
      +--------------+-----------------------------------------------------------+
      | *linker_exe* | バイナリ実行可能ファイルを作るために使うリンカ            |
      +--------------+-----------------------------------------------------------+
      | *archiver*   | 静的ライブラリを作るアーカイバ                            |
      +--------------+-----------------------------------------------------------+

      コマンドラインをもつプラットフォーム(Unix, DOS/Windows)では、それぞれ
      の文字列は実行ファイル名と(省略可能な)引数リストに分割されます。(文字 列の分割は Unix のシェルが行うものに似ています: 単語はスペースで区
      切られますが、クォートとバックスラッシュでオーバーライドできます。  :func:`distutils.util.split_quoted`をごらんください。)

   以下のメソッドはビルドプロセスのステージを呼び出します。


   .. method:: CCompiler.compile(sources[, output_dir=``None``, macros=``None``, include_dirs=``None``, debug=``0``, extra_preargs=``None``, extra_postargs=``None``, depends=``None``])

      1つ以上のソースファイルをコンパイルします。オブジェクトファイルを生成 (たとえば :file:`.c` ファイルを
      :file:`.o`ファイルに変換)します。

      *sources* はファイル名のリストである必要があります。おそらく C/C++ ファイルですが、実際にはコンパイラとコンパイラクラスで扱えるもの(例:
      :class:`MSVCCompiler`はリソースファイルを *sources*にとることができ ます)なら何でも指定できます。
      *sources*のソースファイルひとつずつ に対応するオブジェクトファイル名のリストを返します。実装に依存しますが、
      全てのソースファイルがコンパイルされる必要はありません。しかし全ての対 応するオブジェクトファイル名が返ります。

      もし *output_dir*が指定されていれば、オブジェクトファイルはその下 に、オリジナルのパスを維持した状態で置かれます。 つまり、
      :file:`foo/bar.c`は通常コンパイルされて:file:`foo/bar.o`になります (Unix実装の場合)が、もし*output_dir*が
      *build*であれば、 :file:`build/foo/bar.o`になります。

      *macros*は(もし指定されていれば)マクロ定義のリストである必要があり ます。 マクロ定義は``(name,
      value)``という形式の2要素のタプル、または ``(name,)``という形式の1要素のタプルのどちらかです。前者はマクロを定
      義します。もしvalueが``None``であれば、マクロは特定の値をもたないで 定義されます。1要素のタプルはマクロ定義を削除します。後で実行された定
      義/再定義/削除が優先されます。

      *include_dirs*は(もし指定されていれば)文字列のリストである必要があ ります。このコンパイルだけで有効な、デフォルトのインクルードファイル
      の検索ディレクトリに追加するディレクトリ群を指定します。

      *debug*はブーリアン値です。もし真なら、コンパイラはデバッグシンボ ルをオブジェクトファイルに(または別ファイルに)出力します。

      *extra_postargs*と*extra_postargs*は実装依存です。 コマンドラインをもっているプラットフォーム(例 Unix,
      DOS/Windows)では、 おそらく文字列のリスト: コンパイラのコマンドライン引数の前/後に追加す
      るコマンドライン引数です。他のプラットフォームでは、実装クラスのドキュ メントを参照してください。どの場合でも、これらの引数は抽象コンパイラフ
      レームワークが期待に沿わない時の脱出口として意図されています。

      *depends*は(もし指定されていれば)ターゲットが依存しているファイル 名のリストです。ソースファイルが依存しているファイルのどれかより古けれ
      ば、ソースファイルは再コンパイルされます。これは依存関係のトラッキング をサポートしていますが、荒い粒度でしか行われません。

      失敗すると:exc:`CompileError`を起こします。


   .. method:: CCompiler.create_static_lib(objects, output_libname[, output_dir=``None``, debug=``0``, target_lang=``None``])

      静的ライブラリファイルを作るために元ファイル群をリンクします。 「元ファイル群」は*objects*で指定されたオブジェクトファイルのリス
      トを基礎にしています。追加のオブジェクトファイルを :meth:`add_link_object` および/または
      :meth:`set_link_objects` で指定し、追加のライブラリを:meth:`add_library` および/または
      :meth:`set_libraries`で指定します。そして*libraries*で指定され たライブラリです。

      *output_libname*はライブラリ名で、ファイル名ではありません; ファイ
      ル名はライブラリ名から作られます。*output_dir*はライブラリファイル が起かれるディレクトリです。
      *debug*はブール値です。真なら、デバッグ情報がライブラリに含まれま す(ほとんどのプラットフォームではコンパイルステップで意味をもちます:
      *debug*フラグは一貫性のためにここにもあります。)。

      .. % XXX デフォルトは何?

      *target_lang* はオブジェクトがコンパイルされる対象になる言語です。 これはその言語特有のリンク時の処理を可能にします。

      失敗すると :exc:`LibError` を起こします。


   .. method:: CCompiler.link(target_desc, objects, output_filename[, output_dir=``None``, libraries=``None``, library_dirs=``None``, runtime_library_dirs=``None``, export_symbols=``None``, debug=``0``, extra_preargs=``None``, extra_postargs=``None``, build_temp=``None``, target_lang=``None``])

      実行ファイルまたは共有ライブラリファイルを作るために元ファイル群をリンクします。

      「元ファイル群」は*objects*で指定されたオブジェクトファイルのリス トを基礎にしています。*output_filename* はファイル名です。もし
      *output_dir*が指定されていれば、それに対する相対パスとして
      *output_filename*は扱われます(必要ならば*output_filename* はディ レクトリ名を含むことができます。)。

      *libraries*はリンクするライブラリのリストです。 これはファイル名ではなくライブラリ名で指定します。プラットフォーム依存
      の方式でファイル名に変換されます(例: *foo* はUnix では :file:`libfoo.a` に、DOS/Windowsでは
      :file:`foo.lib` になります。 )。ただしこれらはディレクト リ名を含むことができ、その場合はリンカは通常の場所全体を探すのではなく
      特定のディレクトリを参照します。

      *library_dirs*はもし指定されるならば、修飾されていない(ディレクト リ名を含んでいない)ライブラリ名で指定されたライブラリを探索する
      ディレクトリのリストです。これはシステムのデフォルトより優先され、 :meth:`add_library_dir` と/または
      :meth:`set_library_dirs`に渡さ れます。*runtime_library_dirs*は共有ライブラリに埋め込まれるディレ
      クトリのリストで、実行時にそれが依存する共有ライブラリのパスを指定しま す(これはUnixでだけ意味があるかもしれません。)。

      *export_symbols*は共有ライブラリがエクスポートするシンボルのリストです。 (これはWindowsだけで意味があるようです。)

      *debug*は :meth:`compile` や :meth:`create_static_lib`と同じですが、
      少しだけ違いがあり、(:meth:`create_static_lib`では*debug*フラグ
      は形式をあわせるために存在していたのに対して)ほとんどのプラットフォー ムで意識されます。

      *extra_preargs* と *extra_postargs* は :meth:`compile`
      と同じですが、コンパイラではなくリンカへの引数として扱われます。

      *target_lang*は指定されたオブジェクトがコンパイルされた対象言語で す。リンク時に言語特有の処理を行えるようにします。

      失敗すると :exc:`LinkError` が起きます。


   .. method:: CCompiler.link_executable(objects, output_progname[, output_dir=``None``, libraries=``None``, library_dirs=``None``, runtime_library_dirs=``None``, debug=``0``, extra_preargs=``None``, extra_postargs=``None``, target_lang=``None``])

      実行ファイルをリンクします。 *output_progname*は実行ファイルの名前です。*objects*はリンクさ
      れるオブジェクトのファイル名のリストです。他の引数は:meth:`link`メソッドと同 じです。


   .. method:: CCompiler.link_shared_lib(objects, output_libname[, output_dir=``None``, libraries=``None``, library_dirs=``None``, runtime_library_dirs=``None``, export_symbols=``None``, debug=``0``, extra_preargs=``None``, extra_postargs=``None``, build_temp=``None``, target_lang=``None``])

      共有ライブラリをリンクします。*output_libname*は出力先のライブラリ 名です。*objects*はリンクされるオブジェクトのファイル名のリストで
      す。他の引数は:meth:`link`メソッドと同じです。


   .. method:: CCompiler.link_shared_object(objects, output_filename[, output_dir=``None``, libraries=``None``, library_dirs=``None``, runtime_library_dirs=``None``, export_symbols=``None``, debug=``0``, extra_preargs=``None``, extra_postargs=``None``, build_temp=``None``, target_lang=``None``])

      共有オブジェクトをリンクします。*output_filename*は出力先の共有オ
      ブジェクト名です。*objects*はリンクされるオブジェクトのファイル名のリストで す。他の引数は:meth:`link`メソッドと同じです。


   .. method:: CCompiler.preprocess(source[, output_file=``None``, macros=``None``, include_dirs=``None``, extra_preargs=``None``, extra_postargs=``None``])

      *source*で指定されたひとつの C/C++ソースファイルをプリプロセスします。 出力先のファイルは *output_file*か、もし
      *output_file*が指定さ れていなければ *stdout* になります。 *macro*は:meth:`compile`と同様にマクロ定義のリストで、
      :meth:`define_macro` や :meth:`undefine_macro`によって引数になります。
      *include_dirs*はデフォルトのリストに追加されるディレクトリ名のリス トで、:meth:`add_include_dir`と同じ方法で扱われます。

      失敗すると :exc:`PreprocessError` が起きます。

   以下のユーティリティメソッドは具体的なサブクラスで使うために、 :class:`CCompiler`クラスで定義されています。


   .. method:: CCompiler.executable_filename(basename[, strip_dir=``0``, output_dir=``''``])

      *basename*で指定された実行ファイルのファイル名を返します。
      Windows以外の典型的なプラットフォームではbasenameそのままが、Windowsで は :file:`.exe`が追加されたものが返ります。


   .. method:: CCompiler.library_filename(libname[, lib_type=``'static'``, strip_dir=``0``, output_dir=``''``])

      現在のプラットフォームでのライブラリファイル名を返します。
      Unixで*lib_type*が``'static'``の場合、:file:`liblibname.a`の 形式を返し、*lib_type* が
      ``'dynamic'`` の場合は :file:`liblibname.so`の形式を返します。


   .. method:: CCompiler.object_filenames(source_filenames[, strip_dir=``0``, output_dir=``''``])

      指定されたソースファイルに対応するオブジェクトファイル名を返します。 *source_filenames* はファイル名のリストです。


   .. method:: CCompiler.shared_object_filename(basename[, strip_dir=``0``, output_dir=``''``])

      *basename*に対応する共有オブジェクトファイルのファイル名を返します。


   .. method:: CCompiler.execute(func, args[, msg=``None``, level=``1``])

      :func:`distutils.util.execute`を呼びだします。このメソッドは ログを取り、*dry_run*フラグを考慮にいれて、
      Python関数*func*に引数*args*を与えて呼びだします。

      .. % XXX see also


   .. method:: CCompiler.spawn(cmd)

      :func:`distutils.util.spawn`を呼び出します。これは指定したコマン ドを実行する外部プロセスを呼び出します。

      .. % XXX see also


   .. method:: CCompiler.mkpath(name[, mode=``511``])

      :func:`distutils.dir_util.mkpath`を呼び出します。これは 親ディレクトリ込みでディレクトリを作成します。

      .. % XXX see also


   .. method:: CCompiler.move_file(src, dst)

      :meth:`distutils.file_util.move_file`を呼び出します。 *src* を*dst*にリネームします。

      .. % XXX see also


   .. method:: CCompiler.announce(msg[, level=``1``])

      :func:`distutils.log.debug`関数を使ってメッセージを書き出します。

      .. % XXX see also


   .. method:: CCompiler.warn(msg)

      警告メッセージ*msg*を標準エラー出力に書き出します。


   .. method:: CCompiler.debug_print(msg)

      もしこの :class:`CCompiler`インスタンスで *debug*フラグが指定されて
      いれば*msg*を標準出力に出力し、そうでなければ何も出力しません。

.. % \subsection{Compiler-specific modules}
.. % 
.. % The following modules implement concrete subclasses of the abstract
.. % \class{CCompiler} class. They should not be instantiated directly, but should
.. % be created using \function{distutils.ccompiler.new_compiler()} factory
.. % function.


:mod:`distutils.unixccompiler` --- Unix C コンパイラ
====================================================

.. module:: distutils.unixccompiler
   :synopsis: UNIX C Compiler


このモジュールは:class:`UnixCCompiler`クラスを提供します。
:class:`CCompiler`クラスのサブクラスで、典型的なUnixスタイルのコマン ドラインCコンパイラを扱います:

* マクロは :option:`-Dname[=value]` で定義されます。

* マクロは :option:`-Uname` で削除されます。

* インクルードファイルの探索ディレクトリは :option:`-Idir`で指定されます。

* ライブラリは :option:`-llib` で指定されます。

* ライブラリの探索ディレクトリは :option:`-Ldir` で指定されます。

* コンパイルは :program:`cc` (またはそれに似た) 実行ファイルに、 :option:`-c` オプションをつけて実行します:
  :file:`.c` を :file:`.o`にコンパイルします。

* 静的ライブラリは :program:`ar`コマンドで処理されます (:program:`ranlib`を使うかもしれません)

* 共有ライブラリのリンクは :program:`cc` :option:`-shared` で処 理されます。


:mod:`distutils.msvccompiler` --- Microsoft コンパイラ
======================================================

.. module:: distutils.msvccompiler
   :synopsis: Microsoft Compiler


このモジュールは :class:`MSVCCompiler`クラスを提供します。 抽象クラス:class:`CCompiler`の具象クラスでMicrosoft
Visual Studio向けの ものです。 一般的に、拡張モジュールはPythonをコンパイルしたのと同じコンパイラでコンパイルする
必要があります。Python 2.3 やそれ以前では、コンパイラはVisual Studio 6でした。 Python 2.4 と Python 2.5
では、コンパイラは Visual Studio .NET 2003 です。 AMD64 と Itanium バイナリは Platform SDK
を利用して作成されました。

:class:`MSVCCompiler` は大体正しいコンパイラ、リンカその他を選びます。 この選択を上書きするためには、環境変数
*DISTUTILS_USE_SDK* と *MSSdk* の 両方を設定する必要があります。 *MSSdk* は現在の環境をセットアップした
``SetEnv.Cmd`` スクリプト、もしくは 環境変数がSDKをインストールした時に登録されたものであることを示します。
*DISTUTILS_USE_SDK* はdistutilsのユーザーが明示的に :class:`MSVCCompiler` が選んだ
コンパイラを上書きすることを示します。


:mod:`distutils.bcppcompiler` --- Borland コンパイラ
====================================================

.. module:: distutils.bcppcompiler


このモジュールは:class:`BorlandCCompiler`クラスを提供します。
抽象クラス:class:`CCompiler`の具象クラスでBorland C++ コンパイラ向けです。


:mod:`distutils.cygwincompiler` --- Cygwin コンパイラ
=====================================================

.. module:: distutils.cygwinccompiler


このモジュールは:class:`CygwinCCompiler`クラスを提供します。 :class:`UnixCCompiler`のサブクラスで
Cygwinに移植されたWindows用の GNU C コンパイラ向けです。 さらに :class:`Mingw32CCompiler`
クラスを含んでおり、これは mingw32 向けに移植された GCC (cygwinの no-cygwin モードと同じ)向けです。

.. % % 訳者コメント: (same as cygwin in no-cygwin mode) cygwin知らないので訳が変かもしれません


:mod:`distutils.emxccompiler` --- OS/2 EMX コンパイラ
=====================================================

.. module:: distutils.emxccompiler
   :synopsis: OS/2 EMX Compiler support


このモジュールは:class:`EMXCCompiler`クラスを提供します。 :class:`UnixCCompiler`のサブクラスで GNU C
コンパイラの  OS/2 向け EMX ポートを扱います。


:mod:`distutils.mwerkscompiler` --- Metrowerks CodeWarrior サポート
===================================================================

.. module:: distutils.mwerkscompiler
   :synopsis: Metrowerks CodeWarrior support


:class:`MWerksCompiler`クラスを提供します。抽象クラス:class:`CCompiler` の具象クラスで Mac OS X 以前の
Macintosh の MetroWerks CodeWarrior向けです。 WindowsやMac OS XのCWをサポートするには作業が必要です。

.. % \subsection{Utility modules}
.. % 
.. % The following modules all provide general utility functions. They haven't
.. % all been documented yet.


:mod:`distutils.archive_util` ---  アーカイブユーティリティ
===========================================================

.. module:: distutils.archive_util
   :synopsis: Utility functions for creating archive files (tarballs, zip files, ...)


このモジュールはアーカイブファイル(tarやzip)を作成する関数を提供します。


.. function:: make_archive(base_name, format[, root_dir=``None``, base_dir=``None``, verbose=``0``, dry_run=``0``])

   アーカイブファイル(例: ``zip``や``tar``)を作成します。 *base_name*は作成するファイル名からフォーマットの拡張子を除いたものです。
   *format*はアーカイブのフォーマットで``zip``、``tar``、``ztar``、``gztar``の いずれかです。
   *root_dir*はアーカイブのルートディレクトリになるディレクトリです: つまり アーカイブを作成する前に*root_dir*に*chdir*します。
   *base_dir*はアーカイブの起点となるディレクトリです: つまり*base_dir*は
   アーカイブ中の全ファイルおよびディレクトリの前につくディレクトリ名です。 *root_dir* と
   *base_dir*はともにカレントディレクトリがデフォルト値です。 アーカイブファイル名を返します。

   .. warning::

      この関数はbz2ファイルを扱えるように変更されるべきです


.. function:: make_tarball(base_name, base_dir[, compress=``'gzip'``, verbose=``0``, dry_run=``0``])

   *base_dir*以下の全ファイルから、tarファイルを作成(オプションで圧縮)します。
   *compress*は``'gzip'``、``'compress'``、``'bzip2'``、 または
   ``None``である必要があります。:program:`tar`と*compress*で指定された
   圧縮ユーティリティにはパスが通っている必要があるので、これはおそらくUnix だけで有効です。 出力tarファイルは
   :file:`base_dir.tar`という名前になり、 圧縮によって拡張子がつきます(:file:`.gz`、 :file:`.bz2` または
   :file:`.Z`)。出力ファイル名が返ります。

   .. warning::

      これは:mod:`tarfile`モジュールの呼び出しに置換されるべきです。


.. function:: make_zipfile(base_name, base_dir[, verbose=``0``, dry_run=``0``])

   *base_dir*以下の全ファイルから、zipファイルを作成します。 出力されるzipファイルは*base_dir* +
   :file:`.zip`という名前になります。 :mod:`zipfile`\ Pythonモジュール(利用可能なら)またはInfoZIP
   :file:`zip` ユーティリティ(インストールされていてパスが通っているなら)を使います。
   もしどちらも利用できなければ、:exc:`DistutilsExecError`が起きます。 出力zipファイル名が返ります。


:mod:`distutils.dep_util` --- 依存関係のチェック
================================================

.. module:: distutils.dep_util
   :synopsis: Utility functions for simple dependency checking


このモジュールはシンプルなタイムスタンプを元にしたファイルやファイル群の依存関係を処理する関数を提供します。さらに、それらの依存関係解析を元にした関数を提供します。


.. function:: newer(source, target)

   *source*が存在して、*target*より最近変更されている、または *source*が存在して、*target*が存在していない場合は真を返します。
   両方が存在していて、*target*のほうが*source*より新しいか同じ場合には 偽を返します。 *source*が存在しない場合には
   :exc:`DistutilsFileError`を起こします。


.. function:: newer_pairwise(sources, targets)

   ふたつのファイル名リストを並列に探索して、それぞれのソースが対応するターゲットより
   新しいかをテストします。:func:`newer`の意味でターゲットよりソースが新しい ペアのリスト(*sources*,*targets*)を返します。

   .. % % equivalent to a listcomp...


.. function:: newer_group(sources, target[, missing=``'error'``])

   *target*が*source*にリストアップされたどれかのファイル より古ければ真を返します。言い換えれば、*target*が存在して
   *sources*の全てより新しいなら偽を返し、そうでなければ真を返します。 *missing*はソースファイルが存在しなかった時の振る舞いを決定します。
   デフォルト(``'error'``)は :func:`os.stat` で :exc:`OSError`
   例外を起こします。もし``'ignore'``なら、単に存在しないソースファイルを無視します。
   もし``'newer'``なら、存在しないソースファイルについては*target*が古いと みなします(これは"dry-tun"モードで便利です:
   入力がないのでコマンドは実行できませんが 実際に実行しようとしていないので問題になりません)。


:mod:`distutils.dir_util` --- ディレクトリツリーの操作
======================================================

.. module:: distutils.dir_util
   :synopsis: Utility functions for operating on directories and directory trees


このモジュールはディレクトリとディレクトリツリーを操作する関数を提供します。


.. function:: mkpath(name[, mode=``0777``, verbose=``0``, dry_run=``0``])

   ディレクトリと、必要な親ディレクトリを作成します。もしディレクトリが既 に存在している(*name*が空文字列の場合、カレントディレクトリ
   を示すのでもちろん存在しています)場合、何もしません。 ディレクトリを作成できなかった場合(例: ディレクトリと同じ名前のファイルが
   既に存在していた)、:exc:`DistutilsFileError`を起こします。 もし
   *verbose*が真なら、それぞれのmkdirについて1行、標準出力に出力 します。 実際に作成されたディレクトリのリストを返します。


.. function:: create_tree(base_dir, files[, mode=``0777``, verbose=``0``, dry_run=``0``])

   *files*を置くために必要な空ディレクトリを*base_dir*以下に作成 します。 *base_dir*ディレクトリは存在している必要はありません。
   *files*はファイル名のリストで*base_dir*からの相対パスとして扱 われます。*base_dir* + *files*のディレクトリ部分
   が(既に存在し ていなければ)作成されます。*mode*, *verbose*と*dry_run*フ ラグは:func:`mkpath`と同じです。


.. function:: copy_tree(src, dst[preserve_mode=``1``, preserve_times=``1``, preserve_symlinks=``0``, update=``0``, verbose=``0``, dry_run=``0``])

   *src*ディレクトリツリー全体を*dst*にコピーします。 *src*と *dst*はどちらもディレクトリ名である必要があります。
   もし*src*がディレクトリでなければ、:exc:`DistutilsFileError`
   を起こします。もし*dst*が存在しなければ、:func:`mkpath`で作成され ます。実行結果は、*src*以下の全てのファイルが*dst*にコピーされ、
   *src*以下の全てのディレクトリが*dst*に再帰的にコピーされます。 コピーされた(またはされるはず)のファイルのリストを返します。返り値は
   *update*または*dry_run*に影響されません: *src* 以下の全ファイルを単に*dst*以下に改名したリストが返されます。

   *preserve_mode* と *preserve_times* は
   :mod:`distutils.file_util`の:func:`copy_file` と同じです:
   通常のファイルには適用されますが、ディレクトリには適用されません。  もし*preserve_symlinks* が真なら、シンボリックリンクは(サポートさ
   れているシステムでは)シンボリックリンクとしてコピーされます。そうでな ければ(デフォルト)シンボリックリンクは参照されている実体ファイルがコピーされます。
   *update* と*verbose* は:func:`copy_file`と同じです。


.. function:: remove_tree(directory[verbose=``0``, dry_run=``0``])

   再帰的に *directory*とその下の全ファイルを削除します。エラーは無視
   されます(*verbose*が真の時は``sys.stdout``に出力されます)

**\*\*** Some of this could be replaced with the shutil module? **\*\***


:mod:`distutils.file_util` --- 1ファイルの操作
==============================================

.. module:: distutils.file_util
   :synopsis: 1ファイルを操作するユーティリティ関数


このモジュールはそれぞれのファイルを操作するユーティリティ関数を提供します。


.. function:: copy_file(src, dst[preserve_mode=``1``, preserve_times=``1``, update=``0``, link=``None``, verbose=``0``, dry_run=``0``])

   ファイル*src*を*dst*にコピーします。もし*dst*がディレクト リなら、*src*はそこへ同じ名前でコピーされます; そうでなければ、
   ファイル名として扱われます。 (もしファイルが存在するなら、上書きされま す。)
   mosil*preserve_mode*が真(デフォルト)なら、ファイルのモード (タイプやパーミッション、その他プラットフォームがサポートするもの)もコ
   ピーされます。もし *preserve_times*が真(デフォルト)なら、最終更新、
   最終アクセス時刻もコピーされます。もし*update*が真なら、*src* は*dst*が存在しない場合か、*dst*が*src*より古い時にだけコ
   ピーします。

   *link*は値を``'hard'``または``'sym'``に設定することでコピーのかわりに ハードリンク(:func:`os.link`を使います)ま
   たはシンボリックリンク(:func:`os.symlink`を使います)を許可します。 ``None``\
   (デフォルト)の時には、ファイルはコピーされます。*link* をサポートしていないシステムで有効にしないでください。
   :func:`copy_file`はハードリンク、シンボリックリンクが可能かチェッ クしていません。ファイルの内容をコピーするために
   :func:`_copy_file_contents`を利用しています。

   ``(dest_name, copied)``のタプルを返します: *dest_name*は出力ファ
   イルの実際の名前、*copied*はファイルがコピーされた(*dry_run*が 真の時にはコピーされることになった)場合には真です。

   .. % XXX if the destination file already exists, we clobber it if
   .. % copying, but blow up if linking.  Hmmm.  And I don't know what
   .. % macostools.copyfile() does.  Should definitely be consistent, and
   .. % should probably blow up if destination exists and we would be
   .. % changing it (ie. it's not already a hard/soft link to src OR
   .. % (not update) and (src newer than dst)).


.. function:: move_file(src, dst[verbose, dry_run])

   ファイル*src*を*dst*に移動します。もし*dst*がディレクトリ なら、ファイルはそのディレクトリに同じ名前で移動されます。そうでなけれ
   ば、*src*は*dst*に単にリネームされます。新しいファイルの名前を 返します。

   .. warning::

      Unix では デバイスをまたがる移動は:func:`copy_file`を利用して扱っています。 他のシステムではどうなっている ???


.. function:: write_file(filename, contents)

   *filename* を作成し、*contents*(行末文字がない文 字列のシーケンス)を書き込みます。


:mod:`distutils.util` --- その他のユーティリティ関数
====================================================

.. module:: distutils.util
   :synopsis: その他のユーティリティ関数


このモジュールは他のユーティリティモジュールにあわないものを提供しています。


.. function:: get_platform()

   現在のプラットフォームを示す文字列を返します。 これはプラットフォーム依存のビルドディレクトリやプラットフォーム依存の 配布物を区別するために使われます。
   典型的には、('os.uname()'のように)OSの名前とバージョン、アーキテクチャ を含みますが、厳密にはOSに依存します。たとえば
   IRIXではアーキテクチャ はそれほど重要ではありません(IRIXはSGIのハードウェアだけで動作する)が、
   Linuxではカーネルのバージョンはそれほど重要ではありません。

   返り値の例:

* ``linux-i586``

* ``linux-alpha``

* ``solaris-2.6-sun4u``

* ``irix-5.3``

* ``irix64-6.2``

   POSIX でないプラットフォームでは、今のところ単に``sys.platform`` が返されます。

   .. % XXX isn't this also provided by some other non-distutils module?


.. function:: convert_path(pathname)

   'pathname' をファイルシステムで利用できる名前にして返します。 すなわち、'/'で分割し、現在のディレクトリセパレータで接続しなおします。
   セットアップスクリプト中のファイル名はUnixスタイルで提供され、実 際に利用する前に変換する必要があるため、この関数が必要になります。 もし
   *pathname* の最初または最後が スラッシュの場合、Unix的でな いシステムでは:exc:`ValueError`が起きます。


.. function:: change_root(new_root, pathname)

   *pathname*の前に*new_root*を追加したものを返します。 もし*pathname*が相対パスなら、
   ``os.path.join(new_root,pathname)``と等価です。そうでなければ、
   *pathname*を相対パスに変換したあと接続します。これはDOS/Windows ではトリッキーな作業になります。


.. function:: check_environ()

   'os.environ'に、ユーザがconfigファイル、コマンドラインオプションなどで 利用できることを保証している環境変数があることを確認します。
   現在は以下のものが含まれています:

* :envvar:`HOME` - ユーザのホームディレクトリ (Unix のみ)

* :envvar:`PLAT` - ハードウェアとOSを含む現在のプラットフォームの説 明。 ( :func:`get_platform`を参照)


.. function:: subst_vars(s, local_vars)

   shell/Perlスタイルの変数置換を*s*について行います。 全ての``$``に名前が続いたものは変数とみなされ、辞書*local_vars*で
   みつかった値に置換されます。*local_vars*で見つからなかった場合には ``os.environ``で置換されます。
   *os.environ*は最初にある値を含んでいることをチェックされます: :func:`check_environ`を参照。  *local_vars* or
   ``os.environ``のどちらにも値が見つからなかった 場合、:exc:`ValueError`を起こします。

   これは完全な文字列挿入関数ではないことに注意してください。 ``$variable``の名前には大小英字、数字、アンダーバーだけを含むこと ができます。 { }
   や ( ) を使った引用形式は利用できません。


.. function:: grok_environment_error(exc[, prefix=``'error: '``])

   例外オブジェクト :exc:`EnvironmentError` (:exc:`IOError` ま たは :exc:`OSError`)
   から、エラーメッセージを生成します。 Python 1.5.1 またはそれ以降の形式を扱い、ファイル名を含んでいない例外
   オブジェクトも扱います。このような状況はエラーが2つのファイルに関係す る操作、たとえば:func:`rename`や:func:`link`で発生します。
   *prefix*をプレフィクスに持つエラーメッセージを返します。


.. function:: split_quoted(s)

   文字列をUnixのシェルのようなルール(引用符やバックスラッシュの扱い)で分 割します。つまり、バックスラッシュでエスケープされるか、引用符で囲まれ
   ていなければ各語はスペースで区切られます。一重引用符と二重引用符は同じ 意味です。引用符もバックスラッシュでエスケープできます。
   2文字でのエスケープシーケンスに使われているバックスラッシュは削除され、 エスケープされていた文字だけが残ります。引用符は文字列から削除されます。
   語のリストが返ります。

   .. % Should probably be moved into the standard library.


.. function:: execute(func, args[, msg=``None``, verbose=``0``, dry_run=``0``])

   外部に影響するいくつかのアクション(たとえば、ファイルシステムへの書き 込み)を実行します。そのようなアクションは*dry_run*フラグで無効にす
   る必要があるので特別です。この関数はその繁雑な処理を行います。 関数と引数のタプル、(実行する「アクション」をはっきりさせるための)表示
   に使われる任意のメッセージを渡してください。


.. function:: strtobool(val)

   真偽値をあらわす文字列を真(1)または偽(0)に変換します。

   真の値は ``y``, ``yes``, ``t``, ``true``, ``on``  そして ``1``です。偽の値は ``n``, ``no``,
   ``f``, ``false``,  ``off`` そして ``0``です。 *val*が上のどれでもない時は
   :exc:`ValueError`を起こします。


.. function:: byte_compile(py_files[, optimize=``0``, force=``0``, prefix=``None``, base_dir=``None``, verbose=``1``, dry_run=``0``, direct=``None``])

   Pythonソースファイル群をバイトコンパイルして:file:`.pyc`または
   :file:`.pyo`ファイルを同じディレクトリに作成します。*py_files*はコ
   ンパイルされるファイルのリストです。:file:`.py`でおわっていないファイル はスキップされます。*optimize*は以下のどれかです:

* ``0`` - 最適化しない (:file:`.pyc`ファイルを作成します)

* ``1`` - 通常の最適化 (``python -O``のように)

* ``2`` - さらに最適化 (``python -OO``のように)

   もし*force*が真なら、全てのファイルがタイムスタンプに関係なく再コ ンパイルされます。

   バイトコードファイルにエンコードされるソースファイル名は、デフォルトでは *py_files*が使われます。これを*prefix*と*base_dir*で変更す
   ることができます。 *prefix*はそれぞれのソースファイル名から削除される文字列で、
   *base_dir*は(*prefix*を削除したあと)先頭に追加されるディレクト リ名です。
   任意に*prefix*と*base_dir*のどちらか、両方を与える(与えない)こ とができます。

   もし*dry_run*が真なら、ファイルシステムに影響することは何もされません。

   バイトコンパイルは現在のインタプリタプロセスによって標準の :mod:`py_compile`モジュールを使って直接行われるか、テンポラリスクリ
   プトを書いて間接的に行われます。 通常は:func:`byte_compile`に直接かそうでないかをまかせます (詳細についてはソースをごらんください)。
   *direct*フラグは関節モードで作成されたスクリプトで使用されます。 何をやっているか理解していない時は``None``のままにしておいてください。


.. function:: rfc822_escape(header)

   :rfc:`822`ヘッダに含められるよう加工した*header*を返します。 改行のあとには8つのスペースが追加されます。この関数は文字列に他の変更
   はしません。

   .. % this _can_ be replaced

.. % \subsection{Distutils objects}


:mod:`distutils.dist` --- Distribution クラス
=============================================

.. module:: distutils.dist
   :synopsis: 構築/インストール/配布 される配布物を表す Distribution クラスを提供します。


このモジュールは:class:`Distribution`クラスを提供します。これは 構築/インストール/配布される配布物をあらわします。


:mod:`distutils.extension` --- Extension クラス
===============================================

.. module:: distutils.extension
   :synopsis: セットアップスクリプトでC/C++ 拡張モジュール をあら わす Extension クラスを提供します。


このモジュールは:class:`Extension`クラスを提供します。 C/C++拡張モジュールをセットアップスクリプトで表すために使われます。

.. % \subsection{Ungrouped modules}
.. % The following haven't been moved into a more appropriate section yet.


:mod:`distutils.debug` --- Distutils デバッグモード
===================================================

.. module:: distutils.debug
   :synopsis: distutilsのデバッグフラグを提供します。


このモジュールはDEBUGフラグを提供します。


:mod:`distutils.errors` --- Distutils 例外
==========================================

.. module:: distutils.errors
   :synopsis: distutils の標準的な例外を提供します。


distutilsのモジュールで使用される例外を提供します。 distutilsのモジュールは標準的な例外を起こします。特に、 SystemExit は
エンドユーザによる失敗(コマンドライン引数の間違いなど)で起きます。

このモジュールは``from ... import *``で安全に使用することができます。
このモジュールは``Distutils``ではじまり、``Error``で終わるシンボ ルしかexportしません。


:mod:`distutils.fancy_getopt` --- 標準 getopt モジュールのラッパ
================================================================

.. module:: distutils.fancy_getopt
   :synopsis: getopt 追加機能


このモジュールは以下の機能を標準の:mod:`getopt`モジュールに追加する ラッパを提供します:

* 短いオプションと長いオプションを関連づけます

* オプションはヘルプ文字列を持ちます。可能性としては :func:`fancy_getopt`に完全な利用方法サマリを作らせることができま す。

* オプションは渡されたオブジェクトの属性を設定します。

* 真偽値をとるオプションは "負のエイリアス" を持ちます。--- たと えば :option:`--quiet` の "負のエイリアス" が
  :option:`--verbose`の場合、コマンドラインで :option:`--quiet`を 指定すると*verbose*は偽になります。

**\*\*** Should be replaced with :mod:`optik` (which is also now known as
:mod:`optparse` in Python 2.3 and later). **\*\***


.. function:: fancy_getopt(options, negative_opt, object, args)

   ラッパ関数。*options*は:class:`FancyGetopt`のコンストラ クタで説明されている``(long_option,
   short_option, help_string)`` の3要素タプルのリストです。 *negative_opt*
   はオプション名からオプション名のマッピングになって いる辞書で、キー、値のどちらも*options*リストに含まれている必要が あります。
   *object*は値を保存するオブジェクト(:class:`FancyGetopt`クラスの :meth:`getopt`メソッドを参照してください)です。
   *args*は引数のリストです。*args*として``None``を渡すと、 ``sys.argv[1:]``が使われます。


.. function:: wrap_text(text, width)

   *text*を*width*以下の幅で折り返します。

   .. warning::

      :mod:`textwrap` で置き換えられるべき ( Python 2.3 以降で利 用可能)。


.. class:: FancyGetopt([option_table=``None``])

   option_table は 3つ組タプルのリストです。``(long_option, short_option, help_string)``

   もしオプションが引数を持つなら、*long_option*に``'='``を追加する
   必要があります。*short_option*は一文字のみで、``':'``はどの場合 にも不要です。*long_option*
   に対応する*short_option*がない場合、 *short_option*は``None``にしてください。
   全てのオプションタプルは長い形式のオプションを持つ必要があります。

:class:`FancyGetopt`クラスは以下のメソッドを提供します:


.. method:: FancyGetopt.getopt([args=``None``, object=``None``])

   argsのコマンドラインオプションを解析します。*object*に属性として保 存します。

   もし*args*が``None``もしくは与えられない場合には、 ``sys.argv[1:]``を使います。
   もし*object*が``None``もしくは与えられない場合には、 新しく
   :class:`OptionDummy`インスタンスを作成し、オプションの値を保存したのち ``(args, object)``のタプルを返します。
   もし*object*が提供されていれば、その場で変更され、 :func:`getopt`は*args*のみを返します。どちらのケースでも、
   返された*args*は渡された*args*リスト(これは変更されません)の変 更されたコピーです。

   .. % and args returned are?


.. method:: FancyGetopt.get_option_order()

   直前に実行された:meth:`getopt`が処理した``(option, value)``タプ
   ルのリストを返します。:meth:`getopt`がまだ呼ばれていない場合には :exc:`RuntimeError`を起こします。


.. method:: FancyGetopt.generate_help([header=``None``])

   この :class:`FancyGetopt`オブジェクトのオプションテーブルから ヘルプテキスト(出力の一行に対応する文字列のリスト)を生成します。

   もし与えられていれば、*header*をヘルプの先頭に出力します。


:mod:`distutils.filelist` ---  FileList クラス
==============================================

.. module:: distutils.filelist
   :synopsis: ファイルシステムを見て、ファイルのリストを構築するために使われる FileList クラス


このモジュールはファイルシステムを見て、ファイルのリストを構築するために使われる :class:`FileList` クラスを提供します。


:mod:`distutils.log` --- シンプルな PEP 282 スタイルのロギ ング
===============================================================

.. module:: distutils.log
   :synopsis: シンプルな282スタイルのロギングメカニズム


.. warning::

   標準の:mod:`logging` モジュールに置き換えられるべき

.. % \subsubsection{\module{} --- }
.. % \declaremodule{standard}{distutils.magic}
.. % \modulesynopsis{ }


:mod:`distutils.spawn` --- サブプロセスの生成
=============================================

.. module:: distutils.spawn
   :synopsis: spawn() 関数を提供


このモジュールは:func:`spawn`関数を提供します。これは様々なプラッ トフォーム依存の他プログラムをサブプロセスとして実行する関数に対するフ
ロントエンドになっています。 与えられた実行ファイルの名前からパスを探索する :func:`find_executable`関数も提供しています。

XXX: input{sysconfig} :XXX

:mod:`distutils.text_file` --- TextFile クラス
==============================================

.. module:: distutils.text_file
   :synopsis: テキストファイルへのシンプルなインタフェース TextFile クラスを提供します。


このモジュールは :class:`TextFile`クラスを提供します。これはテキストファイル
へのインタフェースを提供し、コメントの削除、空行の無視、バックスラッシュ での行の連結を任意に行えます。


.. class:: TextFile([filename=``None``, file=``None``, **options])

   このクラスはファイルのようなオブジェクトを提供します。 これは行指向のテキストファイルを処理する時に共通して必要となる処理を行 います:
   (``#``がコメント文字なら)コメントの削除、空行のスキップ、 (行末のバックスラッシュでの)改行のエスケープによる行の連結、 先頭/末尾の空白文字の削除。
   これらは全て独立して任意に設定できます。

   クラスは:meth:`warn`メソッドを提供しており、物理行つきの警告メッセー ジを生成することができます。この物理行は論理行が複数の物理行にまたがっ
   ていても大丈夫です。 また:meth:`unreadline`メソッドが一行先読みを実装するために提供されています。

   :class:`TextFile`のインスタンスは*filename*、*file*、またはその 両方をとって作成されます。 両方が ``None`` の場合
   :exc:`RuntimeError` が起きます。 *filename*は文字列、*file*はファイルオブジェク
   ト(または:meth:`readline`と:meth:`close`のメソッドを提供する何か) である必要があります。
   :class:`TextFile`が生成する警告メッセージに含めることができるので、 *filename*を与えることが推奨されます、
   もし*file*が提供されなければ、 :class:`TextFile` は組み込みの :func:`open` を利用して自分で作成します。

   オプションは全て真偽値で、:meth:`readline`で返される値に影響します。

   .. % \begin{tableiii}{c|l|l}{オプション名}{オプション名}{説明}{デフォルト値}

   +------------------+------------------------------------------------------------------------+--------------+
   | option name      | 説明                                                                   | デフォルト値 |
   +==================+========================================================================+==============+
   | *strip_comments* | バックスラッシュでエスケープされていない限り、``'#'``から行末          | true         |
   |                  | までと、``'#'``の先にある空白文字の並びを削除します。                  |              |
   +------------------+------------------------------------------------------------------------+--------------+
   | *lstrip_ws*      | 行を返す前に先頭の空白文字の並びを削除します。                         | false        |
   +------------------+------------------------------------------------------------------------+--------------+
   | *rstrip_ws*      | 行を返す前に行末の空白文字(改行文字を含みます!)の並びを削除します。    | true         |
   +------------------+------------------------------------------------------------------------+--------------+
   | *skip_blanks*    | コメントと空白を除いた\*あとで\*内容がない行をスキップします。         | true         |
   |                  | (もし lstrip_ws と rstrip_ws                                           |              |
   |                  | がともに偽なら、空白文字だけの行があるか                               |              |
   |                  | もしれません。これは*skip_blanks*が真でない限りスキップされません。)   |              |
   +------------------+------------------------------------------------------------------------+--------------+
   | *join_lines*     | もしコメントと空白文字を削除したあとで、バックスラッシュが最後の改行文 | false        |
   |                  | 字でない文字なら、次の行を接続して一つの論理行とします:                |              |
   |                  | N行の連続した行がバックスラッシュで終わる場合、N+1                     |              |
   |                  | 行の物理行が1行の論 理行として扱われます。                             |              |
   +------------------+------------------------------------------------------------------------+--------------+
   | *collapse_join*  | 前の行と接続するとき、行頭の空白文字を削除します。``(join_lines        | false        |
   |                  | and not lstrip_ws)``                                                   |              |
   |                  | の時だけ意味をもちます。                                               |              |
   +------------------+------------------------------------------------------------------------+--------------+

   *rstrip_ws*は行末の改行を削除するので、:meth:`readline`のセマン
   ティクスが組み込みファイルオブジェクトの:meth:`readline`メソッドと は変わってしまいます! 特に、 *rstrip_ws* が真で
   *skip_blanks* が偽のとき、 :meth:`readline` はファイルの終端で``None``を返し、空文字
   列を返したときは空行(または全て空白文字の行)です。


   .. method:: TextFile.open(filename)

      新しいファイル*filename*を開きます。これはコンストラクタ引数の *file*と*filename*を上書きします。


   .. method:: TextFile.close()

      現在のファイルを閉じ、(ファイル名や現在の行番号を含め)現在のファイルに ついての情報を全て消します。


   .. method:: TextFile.warn(msg[,line=``None``])

      標準エラー出力に現在のファイルの論理行に結びついた警告メッセージを出力 します。 もし現在の論理行が複数の物理行に対応するなら、警告メッセージは以下のように全体
      を参照します: ``"lines 3-5"``。 もし *line* が与えられていれば、 現在の行番号を上書きします;
      物理行のレンジをあらわすリストまたはタプル、 もしくはある物理行をあらわす整数のどれでも与えられます。


   .. method:: TextFile.readline()

      現在のファイル(または:meth:`unreadline`で"unread"を直前に行ってい
      ればバッファ)から論理行を1行読み込んで返します。もし*join_lines*オ プションが真なら、このメソッドは複数の物理行を読み込んで接続した文字列
      を返します。 現在の行番号を更新します。そのため:meth:`readline`のあとに :meth:`warn`を呼ぶと丁度読んだ行についての警告を出します。
      *rstrip_ws*が真で、*strip_blanks*が偽のとき空文字列が返るので、 ファイルの終端では``None``を返します。


   .. method:: TextFile.readlines()

      現在のファイルで残っている全ての論理行のリストを読み込んで返します。 行番号を、ファイルの最後の行に更新します。


   .. method:: TextFile.unreadline(line)

      *line*(文字列)を次の:meth:`readline`用に、内部バッファにpushし ます。行の先読みを必要とするパーサを実装する時に便利です。
      :meth:`unreadline`で"unread"された行は:meth:`readline`で読み込む際 に再度処理(空白の除去など)されません。
      もし:meth:`unreadlinee`を、:meth:`readline`を呼ぶ前に複数回実行する と、最後にunreadした行から返されます。


:mod:`distutils.version` --- バージョン番号クラス
=================================================

.. module:: distutils.version
   :synopsis: モジュールのバージョン番号を表すクラスの実装


.. % todo
.. % \section{Distutils Commands}
.. % 
.. % This part of Distutils implements the various Distutils commands, such
.. % as \code{build}, \code{install} \&c. Each command is implemented as a
.. % separate module, with the command name as the name of the module.


:mod:`distutils.cmd` --- Distutils コマンドの抽象クラス
=======================================================

.. module:: distutils.cmd
   :synopsis: このモジュールは Command 抽象ベースクラスを提供します。このクラスは distutils.commandサブパッケージ中のモジュールでサブクラス
              を作るために利用されます。


このモジュールは抽象ベースクラス :class:`Command` を提供します。


.. class:: Command(dist)

   コマンドクラスを定義するための抽象ベースクラス --- distutilsの「働きバチ」 --- です。 コマンドクラスは *options*
   とよばれるローカル変数を持ったサブルー チンと考えることができます。オプションは:meth:`initialize_options`で宣
   言され、:meth:`finalize_options` で定義さ(最終的な値を与えら)れます。
   どちらも全てのコマンドクラスで実装する必要があります。この2つの区別は 必要です。なぜならオプションの値は外部(コマンドライン、設定ファイルな
   ど)から来るかもしれず、他のオプションに依存しているオプションは 外部の影響を処理した後で計算される必要があるからです。そのため
   :meth:`finalize_options`が存在します。 サブルーチンの本体は全ての処理をオプションの値にもとづいて行う
   :meth:`run`メソッドで、これも全てのコマンドクラスで実装される必要があります。

   クラスのコンストラクタは:class:`Distribution`のインスタンスである単一の 引数*dist*をとります。


:mod:`distutils.command` ---  Distutils 各コマンド
==================================================

.. module:: distutils.command
   :synopsis: このサブパッケージは標準のdistutilsコマンドを提供します。


.. % \subsubsection{Individual Distutils commands}
.. % todo


:mod:`distutils.command.bdist` --- バイナリインストーラの構築
=============================================================

.. module:: distutils.command.bdist
   :synopsis: パッケージのバイナリインストラーを構築します


.. % todo


:mod:`distutils.command.bdist_packager` --- パッケージの抽象ベースクラス
========================================================================

.. module:: distutils.command.bdist_packager
   :synopsis: パッケージの抽象ベースクラス


.. % todo


:mod:`distutils.command.bdist_dumb` --- "ダム"インストー ラを構築
=================================================================

.. module:: distutils.command.bdist_dumb
   :synopsis: "ダム"インストーラ(単純なファイルのアーカイブ)を構築します


.. % todo


:mod:`distutils.command.bdist_rpm` --- Redhat RPMとSRPM形式 のバイナリディストリビューションを構築
==================================================================================================

.. module:: distutils.command.bdist_rpm
   :synopsis: Redhat RPMとSRPM形式のバイナリディストリビューションを構築


.. % todo


:mod:`distutils.command.bdist_wininst` --- Windowsインストー ラの構築
=====================================================================

.. module:: distutils.command.bdist_wininst
   :synopsis: Windows インストーラの構築


.. % todo


:mod:`distutils.command.sdist` --- ソース配布物の構築
=====================================================

.. module:: distutils.command.sdist
   :synopsis: ソース配布物の構築


.. % todo


:mod:`distutils.command.build` --- パッケージ中の全ファイルを 構築
==================================================================

.. module:: distutils.command.build
   :synopsis: パッケージ中の全ファイルのビルド


.. % todo


:mod:`distutils.command.build_clib` --- パッケージ中のCライブラリを構築
=======================================================================

.. module:: distutils.command.build_clib
   :synopsis: パッケージ中のCライブラリを構築


.. % todo


:mod:`distutils.command.build_ext` --- パッケージ中の拡張を構築
===============================================================

.. module:: distutils.command.build_ext
   :synopsis: パッケージ中の拡張を構築


.. % todo


:mod:`distutils.command.build_py` --- パッケージ中の.py/.pyc ファイルを構築
===========================================================================

.. module:: distutils.command.build_py
   :synopsis: パッケージ中の.py/.pyc ファイルを構築


.. % todo


:mod:`distutils.command.build_scripts` --- パッケージ中のスクリプトを構築
=========================================================================

.. module:: distutils.command.build_scripts
   :synopsis: パッケージ中のスクリプトを構築


.. % todo


:mod:`distutils.command.clean` --- パッケージのビルドエリアを消去
=================================================================

.. module:: distutils.command.clean
   :synopsis: パッケージのビルドエリアを消去


.. % todo


:mod:`distutils.command.config` --- パッケージの設定
====================================================

.. module:: distutils.command.config
   :synopsis: パッケージの設定


.. % todo


:mod:`distutils.command.install` --- パッケージのインストー ル
==============================================================

.. module:: distutils.command.install
   :synopsis: パッケージのインストール


.. % todo


:mod:`distutils.command.install_data` --- パッケージ中のデータファイルをインストール
====================================================================================

.. module:: distutils.command.install_data
   :synopsis: パッケージ中のデータファイルをインストール


.. % todo


:mod:`distutils.command.install_headers` --- パッケージから C/C++ ヘッダファイルをインストール
==============================================================================================

.. module:: distutils.command.install_headers
   :synopsis: パッケージから C/C++ ヘッダファイルをインストール


.. % todo


:mod:`distutils.command.install_lib` --- パッケージから ライブラリファイルをインストール
========================================================================================

.. module:: distutils.command.install_lib
   :synopsis: パッケージから ライブラリファイルをインストール


.. % todo


:mod:`distutils.command.install_scripts` --- パッケージから スクリプトファイルをインストール
============================================================================================

.. module:: distutils.command.install_scripts
   :synopsis: パッケージから スクリプトファイルをインストール


.. % todo


:mod:`distutils.command.register` --- モジュールをPython Package Indexに登録する
================================================================================

.. module:: distutils.command.register
   :synopsis: モジュールをPython Package Indexに登録する


``register``コマンドはパッケージをPython Package Index に登録します。 この詳細は :pep:`301` に記述されています。

.. % todo


新しいDistutilsコマンドの作成
=============================

このセクションではDistutilsの新しいコマンドを作成する手順の概要をしめします。

新しいコマンドは :mod:`distutils.command`パッケージ中のモジュールに
作られます。:file:`command_template`というディレクトリにサンプルのテン
プレートがあります。このファイルを実装しようとしているコマンドと同名の 新しいモジュールにコピーしてください。
このモジュールはモジュール(とコマンド)と同じ名前のクラスを実装する必要があります。 そのため、``peel_banana``コマンド(ユーザは
``setup.py peel_banana``と実行できます)を実装する際には、 :file:`command_template`を
:file:`distutils/command/peel_banana.py`にコ
ピーし、:class:`distutils.cmd.Command`のサブクラス :class:`peel_banana`
クラスを実装するように編集してください。

:class:`Command`のサブクラスは以下のメソッドを実装する必要があります。


.. method:: Command.initialize_options()(こ)

   のコマンドがサポートする全てのオプションのデフォルト値を設定します。 これらのデフォルトは他のコマンドやセットアップスクリプト、設定ファイル
   、コマンドラインによって上書きされるかもしれません。 そのためオプション間の依存関係を記述するには適切な場所ではありません。
   一般的に:meth:`initialize_options`は単に``self.foo = None`` のよ うな定義だけを行います。


.. method:: Command.finalize_options()

   このコマンドがサポートする全てのオプションの最終的な値を設定します。 これは可能な限り遅く呼び出されます。つまりコマンドラインや他のコマンド
   によるオプションの代入のあとに呼び出されます。 そのため、オプション間の依存関係を記述するのに適した場所です。 もし *foo* が *bar*
   に依存しており、かつ まだ*foo*が :meth:`initialize_options`で定義された値のままなら、 *foo*
   を*bar*から代入しても安全です。


.. method:: Command.run()

   コマンドの本体です。実行するべきアクションを実装しています。 :meth:`initialize_options` で初期化され、他のコマンド
   され、セットアップスクリプト、コマンドライン、設定ファイルでカスタマイ
   ズされ、:meth:`finalize_options`で設定されたオプションがアクションを制御します。
   端末への出力とファイルシステムとのやりとりは全て:meth:`run`が行います。

*sub_commands*は コマンドの"ファミリー"を定式化したものです。 たとえば ``install`` は サブコマンド
``install_lib``、``install_headers``などの親です。 コマンドファミリーの親は
*sub_commands*をクラス属性として持ちます。 2要素のタプル``(command_name, predicate)``のリストで、
*command_name*には文字列、*predicate*には親コマンドのメソッドで、
現在の状況がコマンド実行にふさわしいかどうか判断するものを指定します。 (例えば ``install_headers`` はインストールするべき
Cヘッダファイル がある時だけ有効です。) もし *predicate* が None なら、そのコマン ドは常に有効になります。

*sub_commands* は 通常クラスの最後で定義されます。  これはpredicate は
boundされていないメソッドになるので、全て先に定義されてい る必要があるためです。

標準的な例は:command:`install` コマンドです。

.. % 
.. % The ugly "%begin{latexonly}" pseudo-environments are really just to
.. % keep LaTeX2HTML quiet during the \renewcommand{} macros; they're
.. % not really valuable.
.. % 
.. % begin{latexonly}
.. % end{latexonly}

XXX: input{moddist.ind} :XXX
.. % Module Index
.. % begin{latexonly}
.. % end{latexonly}

XXX: input{dist.ind} :XXX
.. % Index


