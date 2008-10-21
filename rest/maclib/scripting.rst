
.. _scripting:

************************
MacPython OSA モジュール
************************

本章では、オープンスクリプティングアーキテクチャ(Open Scripting Architecure、OSA、一般的には AppleScript
と呼ばれる)の現在の Python 用実装について説明します。 Python プログラムからスクリプト可能なアプリケーションを操作したり、 Python
へのインターフェースを備えたものにすることができます。 このモジュール群の開発はすでに終わっており、Python 2.5 では別のものが登場する予定です。

.. % MacPython OSA Modules
.. % % This chapter describes the current implementation of the Open Scripting
.. % % Architecure (OSA, also commonly referred to as AppleScript) for Python, allowing
.. % % you to control scriptable applications from your Python program,
.. % % and with a fairly pythonic interface. Development on this set of modules
.. % % has stopped, and a replacement is expected for Python 2.5.

AppleScript と OSA の様々なコンポーネントの記述のために、また、アーキ テクチャおよび用語についての理解を得るために、アップルの文書を読む必
要があります。"Applescript Language Guide" は概念のモデルおよび用語、Standard Suiteについ
て説明した文書です。"Open Scripting Architecture" 文書は、ア プリケーションプログラマの視点から OSA
を使用する方法について説明 しています。これらの文書はAppleヘルプビューワのDeveloper Documentation 中のCore
Technologiesセクションにあります。

.. % % For a description of the various components of AppleScript and OSA, and
.. % % to get an understanding of the architecture and terminology, you should
.. % % read Apple's documentation. The "Applescript Language Guide" explains
.. % % the conceptual model and the terminology, and documents the standard
.. % % suite. The "Open Scripting Architecture" document explains how to use
.. % % OSA from an application programmers point of view. In the Apple Help
.. % % Viewer these books are located in the Developer Documentation, Core
.. % % Technologies section.

アプリケーションをスクリプトで操作する例として、次の AppleScript  は、 一番前の :program:`Finder`
ウィンドウの名前を取得し、それを印字します。

.. % % As an example of scripting an application, the following piece of
.. % % AppleScript will get the name of the frontmost \program{Finder} window
.. % % and print it:

::

   tell application "Finder"
       get name of window 1
   end tell

Pythonでは以下のコードで同じ事ができます。

.. % % In Python, the following code fragment will do the same:

::

   import Finder

   f = Finder.Finder()
   print f.get(f.window(1).name)

配布されている Python ライブラリは、Standard Suite を実装したパッケー
ジに加えて、いくつかの一般的なアプリケーションへのインターフェースを実 装したパッケージが含まれています。

.. % % As distributed the Python library includes packages that implement the
.. % % standard suites, plus packages that interface to a small number of
.. % % common applications.

アプリケーションに AppleEvent を送るためには、アプリケーションの用語 (:program:`Script
Editor`が「辞書」と呼ぶもの)に接続する Python パッケー ジを最初に作成しなければなりません。これは、:program:`PythonIDE`
の内部 から、あるいは、コマンドラインからのスタンドアロンのプログラムとして  :file:`gensuitemodule.py`
モジュールを実行することにより行うことができ ます。

.. % % To send AppleEvents to an application you must first create the Python
.. % % package interfacing to the terminology of the application (what
.. % % \program{Script Editor} calls the "Dictionary"). This can be done from
.. % % within the \program{PythonIDE} or by running the
.. % % \file{gensuitemodule.py} module as a standalone program from the command
.. % % line.

:file:`gensuitemodule.py` モジュールで生成される出力は多くのモジュール を備えたパッケージのため、全ての Suite
をプログラムの中で 1 つにまとめ て利用できるようにするために :mod:`__init__` モジュールが追加されて います。Python 継承グラフは
AppleScript 継承グラフを理解するので、 Standard Suite をサポートしていて、余分な引数を備えた1つあるいは2つの
変数を拡張する事ができるようにプログラム辞書が書かれていた場合、出力さ れた Suite は、:mod:`StdSuites.Standard_Suite`
からすべてをインポー トして再エクスポートし、さらに拡張機能をもったメソッドをオーバーライド するモジュール :mod:`Standard_Suite`
を含みます。 :mod:`gensuitemodule` の出力は人間に判読可能で、Python docstrings中 にはオリジナルの
AppleScript 辞書にあった文書を含んでいます。したがっ て、それを読むことは有用な情報源となります。

.. % % The generated output is a package with a number of modules, one for
.. % % every suite used in the program plus an \module{__init__} module to glue
.. % % it all together. The Python inheritance graph follows the AppleScript
.. % % inheritance graph, so if a program's dictionary specifies that it
.. % % includes support for the Standard Suite, but extends one or two verbs
.. % % with extra arguments then the output suite will contain a module
.. % % \module{Standard_Suite} that imports and re-exports everything from
.. % % \module{StdSuites.Standard_Suite} but overrides the methods that have
.. % % extra functionality. The output of \module{gensuitemodule} is pretty
.. % % readable, and contains the documentation that was in the original
.. % % AppleScript dictionary in Python docstrings, so reading it is a good
.. % % source of documentation.

出力されたパッケージは、メソッドとして AppleScript 変数をすべて含み、 第1の引数としての直接オブジェクトを含み、キーワード引数としてのすべて
のオプションの引数を含む、パッケージと同じ名前を備えた主要なクラスを実 装しています。また AppleScript クラスは Python
クラス、そして類事物そ の他のもろもろの物として実装されています。

.. % % The output package implements a main class with the same name as the
.. % % package which contains all the AppleScript verbs as methods, with the
.. % % direct object as the first argument and all optional parameters as
.. % % keyword arguments. AppleScript classes are also implemented as Python
.. % % classes, as are comparisons and all the other thingies.

変数を実装する主要な Python クラスは、さらに AppleScriptクラス  "application"
で宣言されたプロパティおよび要素へのアクセスを許可します。 現在のリリースでオブジェクト指向的にやろうとするならば、例えば、より  Python 的な
``f.window(1).name.get()`` の代りに  ``f.get(f.window(1).name)`` を利用する必要があります。

.. % % The main
.. % % Python class implementing the verbs also allows access to the properties
.. % % and elements declared in the AppleScript class "application". In the
.. % % current release that is as far as the object orientation goes, so
.. % % in the example above we need to use
.. % % \code{f.get(f.window(1).name)} in stead of the more Pythonic
.. % % \code{f.window(1).name.get()}.

AppleScript 識別子が Python 識別子と同じでない場合、名前は少数の規則に よって判別します。

.. % % If an AppleScript identifier is not a Python identifier the name is
.. % % mangled according to a small number of rules:

* スペースは下線に置換されます。

* ``_xx_`` が16進法の文字値である場合、他の英数字でない文字は  ``xx`` と置換されます。

* あらゆるPython 予約語には下線を追加します。

Python は、さらに Python でスクリプト対応アプリケーションを作成する事
をサポートしています。次のモジュールはMacPythonのAppleScriptサポートに 適切です。

.. % % Python also has support for creating scriptable applications
.. % % in Python, but
.. % % The following modules are relevant to MacPython AppleScript support:


.. toctree::

   gensuitemodule.rst
   aetools.rst
   aepack.rst
   aetypes.rst
   miniae.rst
さらに、:mod:`Finder`, :mod:`Terminal`, :mod:`Explorer`, :mod:`Netscape`,
:mod:`CodeWarrior`, :mod:`SystemEvents` そして :mod:`StdSuites`
のサポートモジュールは、あらかじめ生成されています。

.. % % In addition, support modules have been pre-generated for
.. % % \module{Finder}, \module{Terminal}, \module{Explorer},
.. % % \module{Netscape}, \module{CodeWarrior}, \module{SystemEvents} and
.. % % \module{StdSuites}.

XXX: input{libgensuitemodule} :XXX
XXX: input{libaetools} :XXX
XXX: input{libaepack} :XXX
XXX: input{libaetypes} :XXX
XXX: input{libminiae} :XXX
