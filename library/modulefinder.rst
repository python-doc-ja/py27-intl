
:mod:`modulefinder` --- スクリプト中で使われているモジュールを 検索する
=======================================================================

.. sectionauthor:: A.M. Kuchling <amk@amk.ca>


.. module:: modulefinder
   :synopsis: スクリプト中で使われているモジュールを検索します。


.. versionadded:: 2.3

このモジュールでは、スクリプト中で import されているモジュールセットを 調べるために使える :class:`ModuleFinder`
クラスを提供しています。 ``modulefinder.py`` はまた、Python スクリプトのファイル名を引数に 指定してスクリプトとして実行し、
import されているモジュールの レポートを出力させることもできます。


.. function:: AddPackagePath(pkg_name, path)

   *pkg_name* という名前のパッケージの在り処が*path* である ことを記録します。


.. function:: ReplacePackage(oldname, newname)

   実際にはパッケージ内で*oldname* という名前になっているモジュール を *newname* という名前で指定できるようにします。この関数の
   主な用途は、:mod:`_xmlplus` パッケージが :mod:`xml` パッケージ に置き換わっている場合の処理でしょう。


.. class:: ModuleFinder([path=None, debug=0, excludes=[], replace_paths=[]])

   このクラスでは:meth:`run_script` および:meth:`report`  メソッドを提供しています。これらのメソッドは何らかのスクリプト中で
   import されているモジュールの集合を調べます。 *path* はモジュールを検索する先のディレクトリ名からなるリストです。 *path*
   を指定しない場合、``sys.path`` を使います。 *debug* にはデバッグレベルを設定します; 値を大きくすると、
   実行している内容を表すデバッグメッセージを出力します。 *excludes* は検索から除外するモジュール名です。 *replace_paths*
   には、モジュールパス内で置き換えられるパスを タプル``(oldpath, newpath)`` からなるリストで 指定します。


.. method:: ModuleFinder.report()

   スクリプトで import しているモジュールと、そのパスからなるリストを列挙 したレポートを標準出力に出力します。モジュールを見つけられなかったり、
   モジュールがないように見える場合にも報告します。


.. method:: ModuleFinder.run_script(pathname)

   *pathname* に指定したファイルの内容を解析します。ファイルには Python コードが入っていなければなりません。

