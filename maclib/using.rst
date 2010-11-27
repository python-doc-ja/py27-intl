
.. _using:

***************************
MacintoshでPythonを利用する
***************************

.. sectionauthor:: Bob Savage <bobsavage@mac.com>


.. % Using Python on a Macintosh

Python を Mac OS X が稼動する Macintosh 上で動作させる方法は、原則的にその他の
Unixプラットフォームと同じです。ただ、IDEやパッケージマネージャなどの追加機能については一言説明しておく価値があるでしょう。

.. % % Python on a Macintosh running Mac OS X is in principle very similar to
.. % % Python on any other \UNIX platform, but there are a number of additional
.. % % features such as the IDE and the Package Manager that are worth pointing out.

Mac OS 9 以前のバージョン上での Python は、Unix や Windows 上の  Python
とはかなり異なります。しかしこのマニュアルでは取り扱いません。というのも、Python 2.4 以降ではこのプラットフォームがサポート対象外となっ
ているからです。Mac OS 9 用の最新の 2.3 系リリースのインストーラやドキュメントが
`<http://www.cwi.nl/~jack/macpython>`_ にあります。

.. % % Python on Mac OS 9 or earlier can be quite different from Python on
.. % % \UNIX{} or Windows, but is beyond the scope of this manual, as that platform
.. % % is no longer supported, starting with Python 2.4. See
.. % % \url{http://www.cwi.nl/\textasciitilde jack/macpython} for installers
.. % % for the latest 2.3 release for Mac OS 9 and related documentation.


.. _getting-osx:

MacPythonの入手とインストール
=============================

Mac OS X 10.3 には、Apple によってPython 2.3 が既にインストールされています。
しかし、ここにはIDEやその他の追加機能が含まれていません。それらが必要な場合は、MacPythonのウェブサイト
`<http://www.cwi.nl/~jack/macpython>`_ から :program:`MacPython for Panther
additions` をインストールしなければなりません。

.. % Getting and Installing MacPython
.. % % Mac OS X 10.3 comes with Python 2.3 pre-installed by Apple.
.. % % This installation does not come with the IDE and other additions, however,
.. % % so to get these you need to install the \program{MacPython for Panther additions}
.. % % from the MacPython website, \url{http://www.cwi.nl/\textasciitilde jack/macpython}.

インストールを行うと、様々なものが入ります:

.. % % What you get after installing is a number of things:

* :file:`Applications` フォルダ下の :file:`MacPython-2.3` フォルダ。このフォルダの中には、 PythonIDE
  統合開発環境、ファインダからダブルクリックして Python スクリプトを起動するための PythonLauncher、 Package Manager
  が入っています。

* ほぼ標準の Unix 版のコマンドライン Python インタプリタ。 :file:`/usr/local/bin/python`
  にインストールされます。ただし、通常作成される:file:`/usr/local/lib/python` はできません。

* フレームワーク :file:`/Library/Frameworks/Python.framework` 。
  実際の処理にかかわる部分ですが、たいていの場合それを気にする必要はありません。

単に上の 3 つを削除すれば、MacPython をアンインストールできます。

.. % % To uninstall MacPython you can simply remove these three things.

"additions" のインストーラで既存の Apple-Python に上書きインストールを
した場合、フレームワークやコマンドラインインタプリタは見えないでしょう。というのもこれらはAppleが事前にインストール済みだからです。それぞれ
:file:`/System/Library/Frameworks/Python.framework` と :file:`/usr/bin/python`
にインストールされています。原則として、これらを変更したり削除したりしてはいけません。というのもこれらはAppleの管理下に
あるものであり、Appleやサードパーティのソフトウェアがそれを利用している可能性があるからです。

.. % % If you use the ``additions'' installer to install on top of an existing
.. % % Apple-Python you will not get the framework and the commandline interpreter,
.. % % as they have been installed by Apple already, in
.. % % \file{/System/Library/Frameworks/Python.framework} and
.. % % \file{/usr/bin/python}, respectively. You should in principle never modify
.. % % or delete these, as they are Apple-controlled and may be used by Apple- or
.. % % third-party software.

PythonIDE には "MacPython Help" という名前の Apple Help Viewer ブックが
入っています。このヘルプはヘルプメニューからアクセスできます。まったくの Python の初心者は、このドキュメントの IDE の説明から
読み始めるとよいでしょう。

.. % % PythonIDE contains an Apple Help Viewer book called "MacPython Help"
.. % % which you can access through its help menu. If you are completely new to
.. % % Python you should start reading the IDE introduction in that document.

他の Unix プラットフォーム上で動作する Python について詳しいなら、 Unix シェルからの Python
スクリプトの実行を説明している節を読むのがよいでしょう。

.. % % If you are familiar with Python on other \UNIX{} platforms you should
.. % % read the section on running Python scripts from the \UNIX{} shell.


Python スクリプトの実行方法
---------------------------

Mac OS X 上で Python を始めるには PythonIDE 統合開発環境に触れてみるのが最良の方法です。章 :ref:`ide` を見るか、IDE
が起動しているならヘルプメニューから呼び出せる Apple ヘルプビューア書類の IDE 入門を読みながら  IDE に触れてみてください。

.. % How to run a Python script
.. % % Your best way to get started with Python on Mac OS X is through the PythonIDE
.. % % integrated development environment, see section \ref{IDE} and use the Help
.. % % menu when the IDE is running.

Python を Terminal ウィンドウのコマンドラインや Finder から起動したいなら、まずはスクリプトを書くエディタが必要になります。 Mac
OS X には、:program:`vim` や :program:`emacs` のような、様々な標準の Unix
コマンドラインエディタがついてきます。もっと Mac らしいエディタを使いたければ、 Bare Bones Software
(`<http://www.barebones.com/products/bbedit/index.shtml>`_) の  :program:`BBEdit`
か :program:`TextWrangler` を選ぶと良いでしょう。 :program:`AppleWorks` や、ASCII
形式でファイルを保存できるその他のワードプロセッサ、あるいは OS X に同梱されている :program:`TextEdit` でもかまいません。

.. % % If you want to run Python scripts from the Terminal window command line
.. % % or from the Finder you first need an editor to create your script.
.. % % Mac OS X comes with a number of standard \UNIX{} command line editors,
.. % % \program{vim} and \program{emacs} among them. If you want a more Mac-like
.. % % editor \program{BBEdit} or \program{TextWrangler} from Bare Bones Software
.. % % (see \url{http://www.barebones.com/products/bbedit/index.shtml}) are
.. % % good choices.  \program{AppleWorks} or any other
.. % % word processor that can save files in ASCII is also a possibility, including
.. % % \program{TextEdit} which is included with OS X.

Terminal のウィンドウから自作のスクリプトを起動するには、シェルの検索パスに :file:`/usr/local/bin`
含まれるようにしておかなければなりません。

.. % % To run your script from the Terminal window you must make sure that
.. % % \file{/usr/local/bin} is in your shell search path.

Finder から自作スクリプトを実行するには、2 つのやり方があります:

.. % % To run your script from the Finder you have two options:

* プログラムを :program:`PythonLauncher` にドラッグします。

* Finder の情報ウィンドウで、作成したスクリプト (又はその他の  :file:`.py` スクリプト) を開くためのデフォルトのアプリケーション
  として :program:`PythonLauncher` を選択して、スクリプトをダブルクリックします。

PythonLauncher には様々な設定があり、スクリプトの起動方法を制御できるようになっています。オプションキーを押しながらドラッグすると、起動時に
設定を変更できます。全体的な設定を変えたければ Perferences メニューを使ってください。

.. % % PythonLauncher has various preferences to control how your script is launched.
.. % % Option-dragging allows you to change these for one invocation, or use its
.. % % Preferences menu to change things globally.


.. _osx-gui-scripts:

GUI つきのスクリプトの実行
--------------------------

Mac OS X には、一つだけ知っておかねばならないクセがあります:  Aqua ウィンドウマネージャとやり取りするような (すなわち、何らかの GUI
を持つような) プログラムは、特殊な方法で起動せねばならないのです。 GUIを持ったスクリプトを実行するには :program:`python` の代わりに
:program:`pythonw` を使ってください。

.. % Running scripts with a GUI
.. % % There is one Mac OS X quirk that you need to be aware of: programs
.. % % that talk to the Aqua window manager (in other words, anything that has a GUI)
.. % % need to be run in a special way. Use \program{pythonw} in stead of \program{python}
.. % % to start such scripts.


設定
----

MacPython では、標準的な Unix の Python が使う:envvar:`PYTHONPATH`
のような環境変数全てに従います。しかし、Finder から起動したプログラムでは、こうした変数に対して標準的でない振る舞いを見せます。これは、 Finder
が起動時に :file:`.profile` や :file:`.cshrc` を読まないためです。 Finder
から起動するプログラム向けに環境変数を設定したければ、 :file:`~/.MacOSX/environment.plist` ファイルを作成して
ください。詳しくは Apple Technical Document QA1067 を参照してください。

.. % configuration
.. % % MacPython honours all standard \UNIX{} environment variables such as
.. % % \envvar{PYTHONPATH}, but setting these variables for programs started
.. % % from the Finder is non-standard
.. % % as the Finder does not read your \file{.profile} or \file{.cshrc} at startup.
.. % % You need to create a file \file{\textasciitilde /.MacOSX/environment.plist}.
.. % % See Apple's Technical Document QA1067 for details.

Package Manager を使うと、追加の Python パッケージをとても簡単にインストールできます。詳しくは MacPython
ヘルプを参照してください。

.. % % Installing additional Python packages is most easily done through the
.. % % Package Manager, see the MacPython Help Book for details.


.. _ide:

統合開発環境
============

:program:`Python IDE`\ (統合開発環境) は独立したアプリケーションで、Python
コードのテキストエディタや、クラスブラウザ、グラフィカルデバッガなどとして動作します。

.. % The IDE
.. % % The \program{Python IDE} (Integrated Development Environment) is a
.. % % separate application that acts as a text editor for your Python code,
.. % % a class browser, a graphical debugger, and more.

Python のオンラインヘルプには IDE の簡単な使い方が含まれています。これを見れば主要な機能やその使用法がわかることでしょう。

.. % % The online Python Help contains a quick walkthrough of the IDE that
.. % % shows the major features and how to use them.


"Python Interactive"ウィンドウを使う
------------------------------------

このウィンドウは、通常の Unix のコマンドラインインタプリタと同じように使います。

.. % Using the ``Python Interactive'' window
.. % % Use this window like you would use a normal \UNIX{} command line
.. % % interpreter.


.. _idewrite:

Pythonスクリプトを書く
----------------------

:program:`Python IDE` は、対話的に使うだけでなく、Python プログラムを書
き上げたり、順次保存したりでき、全体や一部分の実行もできます。

.. % Writing a Python Script
.. % % In addition to using the \program{Python IDE} interactively, you can
.. % % also type out a complete Python program, saving it incrementally, and
.. % % execute it or smaller selections of it.

「File」メニューの適当なメニューアイテムを選択すれば新たにスクリプトを作成したり、前に保存したスクリプトを開いたり、
現在開いているスクリプトを保存したりできます。 Python スクリプトを  :program:`Python IDE`
の上にドロップすると、ファイルを編集用に開きます。

.. % % You can create a new script, open a previously saved script, and save
.. % % your currently open script by selecting the appropriate item in the
.. % % ``File'' menu. Dropping a Python script onto the
.. % % \program{Python IDE} will open it for editting.

:program:`Python IDE` はスクリプトを保存する際にクリエータコードの設定を
使います。この設定は、ドキュメントウィンドウの一番右上の小さな黒い三角形をクリックし、「save options」を選べば操作できます。
デフォルトでは、ファイルの:program:`Python IDE` をクリエータコードにして保存します。従って、ファイルのアイコンをダブルクリックすると
ファイルを編集用に開きます。この動作を変更して、 :program:`PythonLauncher` で開いて実行するようしたいと思う場合も
あるでしょう。そうするには、単に「save options」から「PythonLauncher」を選ぶだけです。このオプションは
アプリケーションではなく*ファイル* に関連付けられているので注意してください。

.. % % When the \program{Python IDE} saves a script, it uses the creator code
.. % % settings which are available by clicking on the small black triangle
.. % % on the top right of the document window, and selecting ``save
.. % % options''. The default is to save the file with the \program{Python
.. % % IDE} as the creator, this means that you can open the file for editing
.. % % by simply double-clicking on its icon. You might want to change this
.. % % behaviour so that it will be opened by the
.. % % \program{PythonLauncher}, and run. To do this simply choose
.. % % ``PythonLauncher'' from the ``save options''. Note that these
.. % % options are associated with the \emph{file} not the application.


.. _ideexecution:

統合開発環境の中からスクリプトを実行する
----------------------------------------

:program:`Python IDE`の最前面のウィンドウで全部実行(run all)ボタンを押
すと、そのウィンドウのスクリプトを実行できます。しかし、仮に Python の習慣通りに ``if __name__ == "__main__":``
と書いても、スクリプトはデフォルトでは「__main__」に *ならない* ことに注意しておきましょう。
そういう風に動作させるには、ドキュメントウィンドウの一番右上の小さな黒い三角形から、"Run as __main__"オプションを選ばねばなりません。
このオプションはアプリケーションではなく*ファイル* に関連付けられているので注意してください。とはいえ、このオプションは保存後もそのまま
*残ります*。止めたければ、再度このオプションを選んでください。

.. % Executing a script from within the IDE
.. % % You can run the script in the frontmost window of the \program{Python
.. % % IDE} by hitting the run all button.  You should be aware, however that
.. % % if you use the Python convention \samp{if __name__ == "__main__":} the
.. % % script will \emph{not} be ``__main__'' by default. To get that
.. % % behaviour you must select the ``Run as __main__'' option from the
.. % % small black triangle on the top right of the document window.  Note
.. % % that this option is associated with the \emph{file} not the
.. % % application. It \emph{will} stay active after a save, however; to shut
.. % % this feature off simply select it again.


.. _ideapplet:

"Save as" と "Save as Applet" の違い
------------------------------------

Python スクリプトを書いたら、ファイルを「アプレット」としても保存できます ("File"メニューの"Save as applet"を選びます) 。
アプレットとして保存すると、ファイルやフォルダをスクリプトにドロップすることで、コマンドライン引数で渡すのと同じようにスクリプトにファイル
やフォルダを渡せるという、大きな利点があります。ただし、アプレットを今までのファイルに上書きせず、別のファイルとして
保存するように気をつけてください。アプレットとして保存したファイルは二度と編集できないからです。

.. % ``Save as'' versus ``Save as Applet''
.. % % When you are done writing your Python script you have the option of
.. % % saving it as an ``applet'' (by selecting ``Save as applet'' from the
.. % % ``File'' menu). This has a significant advantage in that you can drop
.. % % files or folders onto it, to pass them to the applet the way
.. % % command-line users would type them onto the command-line to pass them
.. % % as arguments to the script. However, you should make sure to save the
.. % % applet as a separate file, do not overwrite the script you are
.. % % writing, because you will not be able to edit it again.

「ドラッグ＆ドロップ」でアプレットに渡した項目にアクセスするには、標準的な :attr:`sys.argv` の動作を使います。詳しくは
Pythonの標準ドキュメントを参照してください。

.. % % Accessing the items passed to the applet via ``drag-and-drop'' is done
.. % % using the standard \member{sys.argv} mechanism. See the general
.. % % documentation for more
.. % need to link to the appropriate place in non-Mac docs

スクリプトをアプレットとして保存しても、 Python がインストールされていないシステムでは実行できないので注意してください。

.. % % Note that saving a script as an applet will not make it runnable on a
.. % % system without a Python installation.

.. % \subsection{Debugger}
.. % **NEED INFO HERE**
.. % \subsection{Module Browser}
.. % **NEED INFO HERE**
.. % \subsection{Profiler}
.. % **NEED INFO HERE**
.. % end IDE
.. % \subsection{The ``Scripts'' menu}
.. % **NEED INFO HERE**


パッケージマネージャ
====================

歴史的に、MacPython には便利な拡張パッケージが多数同梱されてきました。というのも、対打数の Macintosh ユーザは開発環境や C
コンパイラを持っていなかったからです。Mac OS X 用のものについては、拡張パッケージは同梱されて
いません。しかし、新たな仕組みによって拡張パッケージに簡単にアクセスできるようになりました。

.. % The Package Manager
.. % % Historically MacPython came with a number of useful extension packages
.. % % included, because most Macintosh users do not have access to a development
.. % % environment and C compiler. For Mac OS X that bundling is no longer done,
.. % % but a new mechanism has been made available to allow easy access to
.. % % extension packages.

Python パッケージマネージャを使用すると、追加パッケージをインストールして Python の機能を強化できるようになります。パッケージマネージャは、
MacOS のバージョンと Python のバージョンを調べ、それと同じ組み合わせでテストしたパッケージのデータベースをダウンロードします。つまり、パッケージ
マネージャに表示されているのにもかかわらず動作しないパッケージが万一あった場合は、気兼ねなくデータベースの管理者に文句を言っていいということです。

.. % % The Python Package Manager helps you installing additional packages
.. % % that enhance Python. It determines the exact MacOS version  and Python
.. % % version you have and uses that information to download  a database that
.. % % has packages that are tested and tried on that combination. In other
.. % % words: if something is in your Package Manager  window but does not work
.. % % you are free to blame the database maintainer.

次に、パッケージマネージャはどのパッケージがインストールされていてどのパッケージがインストールされていないのかを調べます。パッケージマネージャを
使わずにインストールしたパッケージも検出します。パッケージを選択してインストールすると、もし別のパッケージが必要な場合も自動的にそれをインストールします。

.. % % PackageManager then checks which of the packages you have installed  and
.. % % which ones are not. This should also work when you have installed packages
.. % % outside of PackageManager.  You can select packages and install them,
.. % % and PackageManager will work out the requirements and install these too.

パッケージマネージャは、ひとつのパッケージをバイナリとソースの二通りで表示することがあります。バイナリ版は常に使用できますが、ソース版を使うには Apple
Developer Tools をインストールしておく必要があります。このツールやその他の依存ファイルがインストールされていない場合は、パッケージマネージ
ャは警告を発します。

.. % % Often PackageManager will list a package in two flavors: binary  and
.. % % source. Binary should always work, source will only work if  you have
.. % % installed the Apple Developer Tools. PackageManager will warn  you about
.. % % this, and also about other external dependencies.

パッケージマネージャは、単体のアプリケーションとして使用する以外にもIDE の機能として使うこともできます。この場合はメニューから File->Package
Manager を選択します。

.. % % PackageManager is available as a separate application and also  as a
.. % % function of the IDE, through the File->Package Manager menu  entry.

