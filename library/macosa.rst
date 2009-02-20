
.. _mac-scripting:

************************
MacPython OSA モジュール
************************

この章では Python 用の Open Scripting Architecture (OSA, 一般には
AppleScript として知られている) の現在の実装について説明しています。
これを使うとスクリプト制御可能なアプリケーションを Python プログラムから
実に pythonic なインタフェースとともに制御することができます。
このモジュール群の開発は停止しましたが、Python 2.5 用には代わりのものが期待できるでしょう。

AppleScript や OSA の様々なコンポーネントの説明、
およびそのアーキテクチャや用語法の理解のために、
Apple のドキュメントを読んでおく方がよいでしょう。
"Applescript Language Guide" は概念モデルと用語法を説明し、
標準スイートについて文書にまとめてあります。
"Open Scripting Architecture" はアプリケーションプログラマの視点から、
どのように OSA を使用するかについて説明しています。
Apple Help Viewer においてこれらは Developer Documentation, Core Technologies
節で見つかります。

アプリケーションでスクリプト制御する例として、以下の AppleScript コードの断片は、
もっとも手前にある :program:`Finder` のウィンドウの名前を取得して表示させます::

   tell application "Finder"
       get name of window 1
   end tell

Python では、以下のコード片が同じことをします::

   import Finder

   f = Finder.Finder()
   print f.get(f.window(1).name)

配布されている Python ライブラリには、標準スイートを実装したパッケージに、
いくつかのよくあるアプリケーションへのインタフェースをプラスしたものが含まれています。

AppleEvent をアプリケーションに送るためには、最初にアプリケーションの用語
(:program:`Script Editor` が "Dictionary" と呼んでいるもの)
とインタフェースを取る Python パッケージを作らなければなりません。
この作業は :program:`PythonIDE` の中から行うこともできますし、
コマンドラインから :file:`gensuitemodule.py` モジュールを独立のプログラムとして実行することでもできます。

作成されるのはいくつものモジュールからなるパッケージで、
それぞれのモジュールはプログラムで使われるスイートであり 
:mod:`__init__` モジュールがそれらを取りまとめています。
Python の継承グラフは AppleScript の継承グラフに従っていますので、
プログラムの辞書が標準スイートのサポートを含みつつ、
一つ二つ動詞を追加の引数で拡張するように指定しているならば、
出力されるスイートは :mod:`Standard_Suite` という
 :mod:`StdSuites.Standard_Suite` からすべてをインポートしてエクスポートし直しつつ
追加された機能を持つようにメソッドをオーバーライドしたモジュールを含みます。
:mod:`gensuitemodule` の出力は非常に読み易く、
また元々の AppleScript 辞書にあったドキュメントを Python 文書化文字列 (docstring)
中に含みますので、それを読むことはドキュメントの良い手本となります。

出力されたパッケージにはパッケージと同じ名前のメインクラスを実装しており、
これは全ての AppleScript 動詞を直接のオブジェクトは第1引数でオプションのパラメータはキーワード引数で受けるメソッドとして含みます。
AppleScript クラスも Python クラスとして実装されたり、その他諸々も同様です。

動詞を実装しているメインの Python クラスはまた AppleScript の "application"
クラスで宣言されたプロパティおよび要素へのアクセスも許します。
現在のリリースではこれはオブジェクト指向的というには程遠く、
上の例で見たように ``f.get(f.window(1).name)`` と書かねばならず、
より Pythonic な ``f.window(1).name.get()`` という書き方はできません。

AppleScript の識別子が Python の識別子として扱えない場合以下の少数のルールで変換します:

* 空白はアンダースコアに置き換えられます

* その他の英数字以外の文字は ``_xx_`` に置き換えられます。ここで ``xx``
  はその文字の16進値です。

* Python の予約語にはアンダースコアが後ろに付けられます

Python はスクリプト可能なアプリケーションを Python で作成することもサポートしていますが、
以下のモジュールは MacPython の AppleScript サポートに関係するモジュールのみです:

.. toctree::

   gensuitemodule.rst
   aetools.rst
   aepack.rst
   aetypes.rst
   miniaeframe.rst


他に、以下のサポートモジュールが事前に生成されています:
:mod:`Finder`, :mod:`Terminal`, :mod:`Explorer`, :mod:`Netscape`,
:mod:`CodeWarrior`, :mod:`SystemEvents`, :mod:`StdSuites` 。
