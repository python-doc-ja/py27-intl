
:mod:`compileall` --- Pythonライブラリをバイトコンパイル
==========================================

.. module:: compileall
   :synopsis: ディレクトリに含まれるPythonソースファイルを、一括してバイトコンパイルします。


このモジュールは、指定したディレクトリに含まれるPythonソースをコンパイル する関数を定義しています。Pythonライブラリをインストールする時、ソースフ
ァイルを事前にコンパイルしておく事により、ライブラリのインストール先ディ レクトリに書き込み権限をもたないユーザでもキャッシュされたバイトコードフ
ァイルを利用する事ができるようになります。

このモジュールのソースコードは、Pytonソースファイルをコンパイルするスク リプトとしても利用する事ができます。コンパイルするディレクトリは、
``sys.path``で指定されたディレクトリ、またはコマンドラインで指定され たディレクトリとなります。


.. function:: compile_dir(dir[, maxlevels[, ddir[, force[,  rx[, quiet]]]]])

   *dir*で指定されたディレクトリを再帰的に下降し、見つかった :file:`.py`を全てコンパイルします。*maxlevels*は、下降する最大の深
   さ（デフォルトは``10``）を指定します。*ddir*には、エラーメッ セージで使用されるファイル名の、親ディレクトリ名を指定する事ができま
   す。*force*が真の場合、モジュールはファイルの更新日付に関わりなく 再コンパイルされます。

   *rx*には、検索対象から除外するファイル名の正規表現式を指定します。 絶対パス名をこの正規表現で``search``し、一致した場合にはコンパイル
   対象から除外します。

   *quiet*が真の場合、通常処理では標準出力に何も表示しません。


.. function:: compile_path([skip_curdir[, maxlevels[, force]]])

   ``sys.path``に含まれる、全ての:file:`.py`ファイルをバイトコンパイル
   します。*skip_curdir*が真（デフォルト）の時、カレントディレクトリ
   は検索されません。*maxlevels*と*force*はデフォルトでは``0`` で、:func:`compile_dir`に渡されます。

:file:`Lib/`ディレクトリ以下にある全ての:file:`.py`ファイルを強制的にリコンパイル するには、以下のようにします::

   import compileall

   compileall.compile_dir('Lib/', force=True)

   # .svnディレクトリにあるファイルをのぞいて同じことをするにはこのようにします。
   import re
   compileall.compile_dir('Lib/', rx=re.compile('/[.]svn'), force=True)


.. seealso::

   Module :mod:`py_compile`
      Byte-compile a single source file.

