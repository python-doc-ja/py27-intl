
:mod:`pydoc` --- ドキュメント生成とオンラインヘルプシステム
======================================

.. module:: pydoc
   :synopsis: ドキュメント生成とオンラインヘルプシステム
.. moduleauthor:: Ka-Ping Yee <ping@lfw.org>
.. sectionauthor:: Ka-Ping Yee <ping@lfw.org>


.. versionadded:: 2.1

.. index::
   single: documentation; generation
   single: documentation; online
   single: help; online

:mod:`pydoc`モジュールは、Pythonモジュールから自動的にドキュメントを生成します。
生成されたドキュメントをテキスト形式でコンソールに表示したり、 Web browserにサーバとして提供したり、HTMLファイルとして保存したりできます。

組み込み関数の:func:`help`を使うことで、対話型のインタプリタから オンラインヘルプを起動することができます。コンソール用のテキスト形式の
ドキュメントをつくるのにオンラインヘルプでは:mod:`pydoc`を使っています。
:program:`pydoc`をPythonインタプリタからはなく、オペレーティングシステムの
コマンドプロンプトから起動した場合でも、同じテキスト形式のドキュメントを見ることができます。 例えば、以下をshellから実行すると ::

   pydoc sys

:mod:`sys`モジュールのドキュメントを、Unix の:program:`man`コマンドの ような形式で表示させることができます。
:program:`pydoc`の引数として与えることができるのは、関数名・モジュール名・パッケージ名、
また、モジュールやパッケージ内のモジュールに含まれるクラス・メソッド・関数への ドット"."形式での参照です。
:program:`pydoc`への引数がパスと解釈されるような場合で(オペレーティングシステムの パス区切り記号を含む場合です。例えばUnixならば
"/"(スラッシュ)含む場合になります)、 さらに、そのパスがPythonのソースファイルを指しているなら、そのファイルに対する ドキュメントが生成されます。

.. % (訳者注："pydoc"を直接起動できない場合には、"pydoc.py"を明示的にpythonに与えます。
.. % pydoc.pyは、pythonのディレクトリの下のlibのディレクトリにありますので、
.. % begin{verbatim}
.. % python <pythondir>\lib\pydoc.py sys
.. % end{verbatim}
.. % とします。)

引数の前に :option:`-w`フラグを指定すると、コンソールにテキストを表示させる かわりにカレントディレクトリにHTMLドキュメントを生成します。

引数の前に :option:`-k`フラグを指定すると、引数をキーワードとして 利用可能な全てのモジュールの概要を検索します。
検索のやりかたは、Unixの:program:`man`コマンドと同様です。 モジュールの概要というのは、モジュールのドキュメントの一行目のことです。

また、:program:`pydoc`を使うことでローカルマシンに Web browserから
閲覧可能なドキュメントを提供するHTTPサーバーを起動することもできます。 :program:`pydoc` :option:`-p
1234`とすると、HTTPサーバーをポート1234に起動します。 これで、お好きなWeb
browserを使って``http://localhost:1234/``から ドキュメントを見ることができます。

:program:`pydoc`でドキュメントを生成する場合、その時点での環境とパス情報に基づいて モジュールがどこにあるのか決定されます。
そのため、:program:`pydoc` :option:`spam`を実行した場合につくられる
ドキュメントは、Pythonインタプリタを起動して``import spam``と入力したときに 読み込まれるモジュールに対するドキュメントになります。

コアモジュールのドキュメントは `<http://www.python.org/doc/current/lib/>`_ にあると仮定されています。
これは、ライブラリリファレンスマニュアルを置いている異なるURLかローカ ルディレクトリを
環境変数:envvar:`PYTHONDOCS`に設定することでオーバーラ イドすることができます。

