
:mod:`distutils.sysconfig` --- システム設定情報
=======================================

.. module:: distutils.sysconfig
   :synopsis: Python インタプリタの設定情報に対する低水準の アクセス手段。
.. moduleauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. moduleauthor:: Greg Ward <gward@python.net>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


:mod:`distutils.sysconfig` モジュールでは、 Python の低水準の 設定情報へのアクセス手段を提供しています。
どの設定情報変数にアクセスできるかは、プラットフォームと設定自体に 大きく左右されます。また、特定の変数は、使っている Python の
バージョンに対するビルドプロセスに左右されます; こうした変数は、 Unix システムでは、:file:`Makefile` や Python
と一緒にインストール される設定ヘッダから探し出されます。 設定ファイルのヘッダは、2.2 以降のバージョンでは :file:`pyconfig.h`
、それ以前のバージョンでは :file:`config.h`  です。

他にも、:mod:`distutils` パッケージの別の部分を操作 する上で便利な関数がいくつか提供されています。


.. data:: PREFIX

   ``os.path.normpath(sys.prefix)`` の結果です。


.. data:: EXEC_PREFIX

   ``os.path.normpath(sys.exec_prefix)`` の結果です。


.. function:: get_config_var(name)

   ある一つの設定変数に対する値を返します。 ``get_config_vars().get(name)`` と同じです。


.. function:: get_config_vars(...)

   定義されている変数のセットを返します。引数を指定しなければ、 設定変数名を変数の値に対応付けるマップ型を返します。
   引数を指定する場合、引数の各値は文字列でなければならず、戻り値は 引数に関連付けられた各設定変数の値からなるシーケンスになります。
   引数に指定した名前の設定変数に値がない場合、その変数値には ``None`` が入ります。


.. function:: get_config_h_filename()

   設定ヘッダのフルパス名を返します。 Unixの場合、このヘッダファイルは :program:`configure`
   スクリプトによって生成されるヘッダファイル名です; 他のプラットフォームでは、ヘッダは Python ソース配布物中で直接
   与えられています。ファイルはプラットフォーム固有のテキストファイル です。


.. function:: get_makefile_filename()

   Python をビルドする際に用いる :file:`Makefile` のフルパスを返します。 Unixの場合、このファイルは
   :program:`configure` スクリプトによって 生成されます; 他のプラットフォームでは、この関数の返す値の
   意味は様々です。有意なファイル名を返す場合、ファイルは プラットフォーム固有のテキストファイル形式です。 この関数は POSIX
   プラットフォームでのみ有用です。


.. function:: get_python_inc([plat_specific[, prefix]])

   C インクルードファイルディレクトリについて、一般的なディレクトリ名か、 プラットフォーム依存のディレクトリ名のいずれかを返します。
   *plat_specific* が真であれば、プラットフォーム依存の インクルードディレクトリ名を返します; *plat_specific* が偽か、
   省略された場合には、プラットフォームに依存しないディレクトリを 返します。 *prefix* が指定されていれば、:const:`PREFIX`
   の代わりに用いられます。また、 *plat_specific* が真の場合、 :const:`EXEC_PREFIX` の代わりに用いられます。


.. function:: get_python_lib([plat_specific[, standard_lib[, prefix]]])

   ライブラリディレクトリについて、一般的なディレクトリ名か、 プラットフォーム依存のディレクトリ名のいずれかを返します。 *plat_specific*
   が真であれば、プラットフォーム依存の ライブラリディレクトリ名を返します; *plat_specific* が偽か、
   省略された場合には、プラットフォームに依存しないディレクトリを 返します。*prefix* が指定されていれば、:const:`PREFIX`
   の代わりに用いられます。また、 *plat_specific* が真の場合、 :const:`EXEC_PREFIX` の代わりに用いられます。
   *standard_lib* が真であれば、サードパーティ製の拡張モジュール をインストールするディレクトリの代わりに、標準ライブラリのディレクトリ
   を返します。

以下の関数は、:mod:`distutils` パッケージ内の使用だけを 前提にしています。


.. function:: customize_compiler(compiler)

   :class:`distutils.ccompiler.CCompiler` インスタンスに対して、 プラットフォーム固有のカスタマイズを行います。

   この関数は現在のところ、Unix だけで必要ですが、将来の互換性を 考慮して一貫して常に呼び出されます。この関数は様々な Unix の
   変種ごとに異なる情報や、Python の:file:`Makefile` に書かれた情報 をインスタンスに挿入します。この情報には、選択されたコンパイラや
   コンパイラ/リンカのオプション、そして共有オブジェクトを扱うために リンカに指定する拡張子が含まれます。

この関数はもっと特殊用途向けで、Python 自体のビルドプロセスで しか使われません。


.. function:: set_python_build()

   :mod:`distutils.sysconfig` モジュールに、モジュールが Python の
   ビルドプロセスの一部として使われることを知らせます。これによって、 ファイルコピー先を示す相対位置が大幅に変更され、インストール済みの Python
   ではなく、ビルド作業領域にファイルが置かれるようになります。

