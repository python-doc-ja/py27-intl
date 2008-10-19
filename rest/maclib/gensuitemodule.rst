
:mod:`gensuitemodule` --- OSA スタプ作成パッケージ
========================================

.. module:: gensuitemodule
   :platform: Mac
   :synopsis: OSA辞書からスタブパッケージを作成します。
.. sectionauthor:: Jack Jansen <Jack.Jansen@cwi.nl>


.. % Generate OSA stub packages
.. % \moduleauthor{Jack Jansen?}{email}
.. % Create a stub package from an OSA dictionary

:mod:`gensuitemodule` モジュールは AppleScript 辞書によって特定のア プリケーションに実装されている AppleScript
群のためのスタブコードを実 装した Python パッケージを作成します。

.. % % The \module{gensuitemodule} module creates a Python package implementing
.. % % stub code for the AppleScript suites that are implemented by a specific
.. % % application, according to its AppleScript dictionary.

このモジュールは、通常は :program:`PythonIDE` からユーザによって起動さ
れますが、コマンドラインからスクリプトとして実行する(オプションとして ヘルプに :option:`--help`
を与えてみてください)こともできますし、Python  コードでインポートして利用する事もできます。使用例として、どのようにし
て標準ライブラリに含まれているスタブパッケージを生成するか、  :file:`Mac/scripts/genallsuites.py`
にあるソースを見てください。

.. % % It is usually invoked by the user through the \program{PythonIDE}, but
.. % % it can also be run as a script from the command line (pass \code{--help}
.. % % for help on the options) or imported from Python code. For an example of
.. % % its use see \file{Mac/scripts/genallsuites.py} in a source distribution,
.. % % which generates the stub packages that are included in the standard
.. % % library.

このモジュールは次の関数を定義しています。

.. % % It defines the following public functions:


.. function:: is_scriptable(application)

   ``application`` としてパス名を与えたアプリケーションがスクリプト可 能でありそうな場合、真を返します。返り値はやや不確実な場合があります。
   :program:`Internet Explorer` はスクリプト不可能なように見えてしまいます が、実際はスクリプト可能です。

   .. % % Returns true if \code{application}, which should be passed as a pathname,
   .. % % appears to be scriptable. Take the return value with a grain of salt:
   .. % % \program{Internet Explorer} appears not to be scriptable but definitely is.


.. function:: processfile(application[, output, basepkgname,  edit_modnames, creatorsignature, dump, verbose])

   パス名として渡された ``application`` のためのスタブパッケージを作成 します。:file:`.app`
   として一つのパッケージにまとめてあるプログラム群の ために内部の実行プログラムそのものではなくパッケージへのパス名を渡すだ
   けでよくなっています。パッケージ化されていないCFM アプリケーションでは アプリケーションバイナリのファイル名を渡す事もできます。

   .. % % Create a stub package for \code{application}, which should be passed as
   .. % % a full pathname. For a \file{.app} bundle this is the pathname to the
   .. % % bundle, not to the executable inside the bundle; for an unbundled CFM
   .. % % application you pass the filename of the application binary.

   この関数は、アプリケーションの OSA 用語リソースを捜し、これらのリソー スを読み取り、その結果データをクライアントスタブを実装したPython コー
   ドパッケージを作成するために使用します。

   .. % % This function asks the application for its OSA terminology resources,
   .. % % decodes these resources and uses the resultant data to create the Python
   .. % % code for the package implementing the client stubs.

   ``output`` は作成結果のパッケージを保存するパス名で、指定しない場合 は標準の「別名で保存(save file as)」ダイアログが表示されます。
   ``basepkgname`` はこのパッケージの基盤となるパッケージを指定します。 デフォルトは :mod:`StdSuites`
   になります。:mod:`StdSuites` 自体を 生成する場合だけ、このオプションを指定する必要があります。 ``edit_modnames``
   は自動生成によって作成されてあまり綺麗ではないモ ジュール名を変更するために使用することができる辞書です。 ``creator_signature``
   はパッケージ中の :file:`PkgInfo` ファイル、あ るいは CFM ファイルクリエータ署名から通常得られる4文字クリエータコード
   を無視するために使用することができます。``dump`` にはファイルオブジェ クトを与えます、これを指定するとリソースを読取った後に停止して
   ``processfile`` がコード化した用語リソースの Python 表現をダンプし ます。``verbose``
   にもまたファイルオブジェクトを与え、これを指定する と ``processfile`` の行なっている処理の詳細を出力します。

   .. % % \code{output} is the pathname where the resulting package is stored, if
   .. % % not specified a standard "save file as" dialog is presented to
   .. % % the user. \code{basepkgname} is the base package on which this package
   .. % % will build, and defaults to \module{StdSuites}. Only when generating
   .. % % \module{StdSuites} itself do you need to specify this.
   .. % % \code{edit_modnames} is a dictionary that can be used to change
   .. % % modulenames that are too ugly after name mangling.
   .. % % \code{creator_signature} can be used to override the 4-char creator
   .. % % code, which is normally obtained from the \file{PkgInfo} file in the
   .. % % package or from the CFM file creator signature. When \code{dump} is
   .. % % given it should refer to a file object, and \code{processfile} will stop
   .. % % after decoding the resources and dump the Python representation of the
   .. % % terminology resources to this file. \code{verbose} should also be a file
   .. % % object, and specifying it will cause \code{processfile} to tell you what
   .. % % it is doing.


.. function:: processfile_fromresource(application[, output,  basepkgname, edit_modnames, creatorsignature, dump, verbose])

   この関数は、用語リソースを得るのに異なる方法を使用する以外は、 ``processfile`` と同じです。この関数では、リソースファイルとして
   ``application`` を開き、このファイルから  ``"aete"`` および  ``"aeut"``
   リソースをすべて読み込む事で、AppleScript 用語リソース読み 込みを行ないます。

   .. % % This function does the same as \code{processfile}, except that it uses a
   .. % % different method to get the terminology resources. It opens \code{application}
   .. % % as a resource file and reads all \code{"aete"} and \code{"aeut"} resources
   .. % % from this file.

