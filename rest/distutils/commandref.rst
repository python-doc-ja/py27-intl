.. _reference:

***********
リファレンスマニュアル
***********

.. % \section{Building modules: the \protect\command{build} command family}
.. % \label{build-cmds}
.. % \subsection{\protect\command{build}}
.. % \label{build-cmd}
.. % \subsection{\protect\command{build\_py}}
.. % \label{build-py-cmd}
.. % \subsection{\protect\command{build\_ext}}
.. % \label{build-ext-cmd}
.. % \subsection{\protect\command{build\_clib}}
.. % \label{build-clib-cmd}


.. _install-cmd:

モジュールをインストールする:  :command:`install` コマンド群
=========================================

:command:`install` コマンドは最初にビルドコマンドを実行済みに しておいてから、サブコマンド :command:`install_lib`
を実行します。 :command:`install_data` and :command:`install_scripts`.

.. % \subsection{\protect\command{install\_lib}}
.. % \label{install-lib-cmd}


.. _install-data-cmd:

:command:`install_data`
-----------------------

このコマンドは配布物中に提供されている全てのデータファイルを インストールします。


.. _install-scripts-cmd:

:command:`install_scripts`
--------------------------

このコマンドは配布物中の全ての (Python) スクリプトをインストール します。

.. % \section{Cleaning up: the \protect\command{clean} command}
.. % \label{clean-cmd}


.. _sdist-cmd:

ソースコード配布物を作成する:  :command:`sdist` command
=========================================

**\*\*** これは上から断片的に移動した文章です: 脈絡を与える必要あり！ **\*\***

マニフェストテンプレート関連のコマンドを以下に示します:

+-------------------------------------------+----------------------------------------+
| コマンド                                      | 説明                                     |
+===========================================+========================================+
| :command:`include pat1 pat2 ...`          | 列挙されたパターンのいずれかにマッチする全てのファイルを 対象に含めます   |
+-------------------------------------------+----------------------------------------+
| :command:`exclude pat1 pat2 ...`          | 列挙されたパターンのいずれかにマッチする全てのファイルを 対象から除外します |
+-------------------------------------------+----------------------------------------+
| :command:`recursive-include dir pat1 pat2 | *dir* 下にある、列挙されたパターンのいずれかにマッチ          |
| ...`                                      | する全てのファイルを対象に含めます                      |
+-------------------------------------------+----------------------------------------+
| :command:`recursive-exclude dir pat1 pat2 | *dir* 下にある、列挙されたパターンのいずれかにマッチ          |
| ...`                                      | する全てのファイルを対象から除外します                    |
+-------------------------------------------+----------------------------------------+
| :command:`global-include pat1 pat2 ...`   | ソースツリー下にある、列挙されたパターンのいずれかにマッチ          |
|                                           | する全てのファイルを対象に含めます                      |
+-------------------------------------------+----------------------------------------+
| :command:`global-exclude pat1 pat2 ...`   | ソースツリー下にある、列挙されたパターンのいずれかにマッチ          |
|                                           | する全てのファイルを対象から除外します                    |
+-------------------------------------------+----------------------------------------+
| :command:`prune dir`                      | *dir* 下の全てのファイルを除外します                  |
+-------------------------------------------+----------------------------------------+
| :command:`graft dir`                      | *dir* 下の全てのファイルを含めます                   |
+-------------------------------------------+----------------------------------------+

ここでいうパターンとは、Unix式の "glob" パターンです: ``*`` は全ての正規なファイル名文字列に一致し、``?`` は
正規なファイル名文字一字に一致します。また、 ``[range]`` は、*range* の範囲 (例えば、 ``a=z``、``a-zA-Z``、
``a-f0-9_.``) 内にある、任意の文字にマッチします。 "正規なファイル名文字" の定義は、プラットフォームごとに特有の ものです: Unix
ではスラッシュ以外の全ての文字です; Windows  では、バックラッシュとコロン以外です; Mac OS 9 ではコロン以外です。

**\*\*** Windows はまだサポートされていません **\*\***

.. % \section{Creating a built distribution: the
.. % \protect\command{bdist} command family}
.. % \label{bdist-cmds}

.. % \subsection{\protect\command{bdist}}
.. % \subsection{\protect\command{bdist\_dumb}}
.. % \subsection{\protect\command{bdist\_rpm}}
.. % \subsection{\protect\command{bdist\_wininst}}


