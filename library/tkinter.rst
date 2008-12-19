
.. _tkinter:

********************************************
Tkを用いたグラフィカルユーザインターフェイス
********************************************

.. index::
   single: GUI
   single: Graphical User Interface
   single: Tkinter
   single: Tk

Tk/Tcl は長きにわたり Python の不可欠な一部でありつづけています。 Tk/Tcl は頑健でプラットホームに依存しないウィンドウ構築
ツールキットであり、 Python プログラマは:mod:`Tkinter`モジュールや その拡張の:mod:`Tix`モジュールを使って利用できます。

:mod:`Tkinter` モジュールは、 Tcl/Tk 上に作られた軽量な オブジェクト指向のレイヤです。 :mod:`Tkinter` を使うために
Tcl コードを書く必要はありませんが、 Tk のドキュメントや、場合によって は Tcl のドキュメントを調べる必要があるでしょう。
:mod:`Tkinter` は Tk のウィジェットを Python のクラスとして 実装しているラッパをまとめたものです。加えて、内部モジュール
:mod:`_tkinter` では、 Python と Tcl がやり取りできるような スレッド安全なメカニズムを提供しています。

Tk は Python にとって唯一の GUI というわけではありません。 Python 用の他の GUI ツールキットに 関する詳しい情報は、:ref
:`other-gui-packages`章、「他のユーザ インタフェースモジュールとパッケージ」を参照してください。

.. % Other sections I have in mind are
.. % Tkinter internals
.. % Freezing Tkinter applications


.. toctree::


:mod:`Tkinter` --- Tcl/Tk への Python インタフェース
====================================================

.. module:: Tkinter
   :synopsis: グラフィカルユーザインタフェースを実現する Tcl/Tk への インタフェース
.. moduleauthor:: Guido van Rossum <guido@Python.org>


:mod:`Tkinter` モジュール ("Tk インタフェース") は、 Tk GUI ツールキットに対する標準の Python インタフェースです。 Tk
と :mod:`Tkinter` はほとんどの Unix プラットフォーム の他、 Windows や Macintosh システム上でも利用できます。 (Tk
自体は Python の一部ではありません。 Tk は ActiveState で保守されて います。)


.. seealso::

   `Python Tkinter Resources <http://www.python.org/topics/tkinter/>`_
      Python Tkinter Topic Guide では、Tk を Python から利用する上 での情報と、その他の Tk
      にまつわる情報源を数多く提供していま す。

   `An Introduction to Tkinter <http://www.pythonware.com/library/an-introduction-to-tkinter.htm>`_
      Fredrik Lundh のオンラインリファレンス資料です。

   `Tkinter reference: a GUI for Python <http://www.nmt.edu/tcc/help/pubs/lang.html>`_
      オンラインリファレンス資料です。

   `Tkinter for JPython <http://jtkinter.sourceforge.net>`_
      Jython から Tkinter へのインタフェースです。

   `Python and Tkinter Programming <http://www.amazon.com/exec/obidos/ASIN/1884777813>`_
      John Graysonによる解説書 (ISBN 1-884777-81-3) です。


Tkinter モジュール
------------------

ほとんどの場合、本当に必要となるのは :mod:`Tkinter` モジュールだけ ですが、他にもいくつかの追加モジュールを利用できます。 Tk
インタフェース自体は :mod:`_tkinter` と言う名前の バイナリモジュール内にあります。 このモジュールに入っているのは Tk
への低水準のインタフェースであり、 プリケーションプログラマが直接使ってはなりません。 :mod:`_tkinter` は通常共有ライブラリ (や DLL)
になっていますが、 Python インタプリタに静的にリンクされていることもあります。

Tk インタフェースモジュールの他にも、:mod:`Tkinter` には Python モジュールが数多く入っています。最も重要なモジュールは、
:mod:`Tkinter` 自体と :mod:`Tkconstants` と呼ばれるモジュール の二つです。前者は自動的に後者を import
するので、以下のように 一方のモジュールを import するだけで Tkinter を使えるようになります::

   import Tkinter

あるいは、よく使うやり方で::

   from Tkinter import *

のようにします。


.. class:: Tk(screenName=None, baseName=None, className='Tk', useTk=1)

   :class:`Tk` クラスは引数なしでインスタンス化します。 これは Tk のトップレベルウィジェットを生成します。
   通常、トップレベルウィジェットはアプリケーションのメインウィンドウに なります。それぞれのインスタンスごとに固有の Tcl インタプリタが関連 づけられます。

   .. % FIXME: The following keyword arguments are currently recognized:

   .. versionchanged:: 2.4
      *useTk* パラメタが追加されました.


.. function:: Tcl(screenName=None, baseName=None, className='Tk', useTk=0)

   :func:`Tcl` はファクトリ関数で、:class:`Tk` クラスで生成するオブジェクト とよく似たオブジェクトを生成します。ただし Tk
   サブシステムを初期化 しません。この関数は、余分なトップレベルウィンドウを作る必要がなかったり、 (X サーバを持たない Unix/Linux
   システムなどのように) 作成できない環境に おいて Tcl インタプリタを駆動したい場合に便利です。 :func:`Tcl`
   で生成したオブジェクトに対して:meth:`loadtk` メソッドを 呼び出せば、トップレベルウィンドウを作成 (して、Tk サブシステムを 初期化)
   します。

   .. versionadded:: 2.4

Tk をサポートしているモジュールには、他にも以下のようなモジュールが あります:

:mod:`ScrolledText`
   垂直スクロールバー付きのテキストウィジェットです。

:mod:`tkColorChooser`
   ユーザに色を選択させるためのダイアログです。

:mod:`tkCommonDialog`
   このリストの他のモジュールが定義しているダイアログの基底クラスです。

:mod:`tkFileDialog`
   ユーザが開きたいファイルや保存したいファイルを指定できるようにする 共通のダイアログです。

:mod:`tkFont`
   フォントの扱いを補助するためのユーティリティです。

:mod:`tkMessageBox`
   標準的な Tk のダイアログボックスにアクセスします。

:mod:`tkSimpleDialog`
   基本的なダイアログと便宜関数 (convenience function) です。

:mod:`Tkdnd`
   :mod:`Tkinter` 用のドラッグアンドドロップのサポートです。 実験的なサポートで、Tk DND に置き替わった時点で撤廃されるはずです。

:mod:`turtle`
   Tk ウィンドウ上でタートルグラフィックスを実現します。


Tkinter お助け手帳 (life preserver)
-----------------------------------

.. sectionauthor:: Matt Conway


この節は、 Tk や Tkinter を全て網羅したチュートリアルを目指している わけではありません。むしろ、Tkinter のシステムを学ぶ上での指針を
示すための、その場しのぎ的なマニュアルです。

.. % Converted to LaTeX by Mike Clarkson.

謝辞:

* Tkinter は Steen Lumholt と Guido van Rossum が作成しました。

* Tk は John Ousterhout が Berkeley の在籍中に作成しました。

* この Life Preserver は Virginia 大学の Matt Conway 他が書きました。

* html へのレンダリングやたくさんの編集は、Ken Manheimer が FrameMaker 版から行いました。

* Fredrik Lundh はクラスインタフェース詳細な説明を書いたり 内容を改訂したりして、現行の Tk 4.2 に合うようにしました。

* Mike Clarkson はドキュメントをLaTeX 形式に変換し、 リファレンスマニュアルのユーザインタフェースの章をコンパイルしました。


この節の使い方
^^^^^^^^^^^^^^

この節は二つの部分で構成されています: 前半では、背景となることがらを (大雑把に) 網羅しています。後半は、キーボードの横に置けるような手軽な
リファレンスになっています。

「ホゲホゲ (blah) するにはどうしたらよいですか」 という形の問いに答えよう と思うなら、まず Tk で「ホゲホゲ」する方法を調べてから、この
ドキュメントに戻ってきてその方法に対応する:mod:`Tkinter` の 関数呼び出しに変換するのが多くの場合最善の方法になります。 Python
プログラマが Tk ドキュメンテーションを見れば、たいてい 正しい Python コマンドの見当をつけられます。従って、 Tkinter を使うには Tk
についてほんの少しだけ知っていればよいと いうことになります。 このドキュメントではその役割を果たせないので、次善の策として、
すでにある最良のドキュメントについていくつかヒントを示しておく ことにしましょう:

* Tk の man マニュアルのコピーを手に入れるよう強く勧めます。 とりわけ最も役立つのは:file:`mann` ディレクトリ内にあるマニュアルです。
  ``man3`` のマニュアルページは Tk ライブラリに対する C インタフェー スについての説明なので、スクリプト書きにとって取り立てて役に立つ内容
  ではありません。

* Addison-Wesley は John Ousterhout の書いた Tcl and the Tk Toolkit (ISBN
  0-201-63337-X) という名前の本 を出版しています。この本は初心者向けの Tcl と Tk の良い入門書です。 内容は網羅的ではなく、詳細の多くは
  man マニュアル任せにしています。

* たいていの場合、:file:`Tkinter.py` は参照先としては最後の地 (last resort)
  ですが、それ以外の手段で調べても分からない場合には 救いの地 (good place) になるかもしれません。


.. seealso::

   `ActiveState Tclホームページ <http://tcl.activestate.com/>`_
      Tk/Tcl の開発は ActiveState で大々的に行われています。

   `Tcl and the Tk Toolkit <http://www.amazon.com/exec/obidos/ASIN/020163337X>`_
      Tcl を考案した John Ousterhout による本です。

   `Practical Programming in Tcl and Tk <http://www.amazon.com/exec/obidos/ASIN/0130220280>`_
      Brent Welch の百科事典のような本です。


簡単なHello Worldプログラム
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. % HelloWorld.html
.. % begin{latexonly}
.. % \begin{figure}[hbtp]
.. % \centerline{\epsfig{file=HelloWorld.gif,width=.9\textwidth}}
.. % \vspace{.5cm}
.. % \caption{HelloWorld gadget image}
.. % \end{figure}
.. % See also the hello-world \ulink{notes}{classes/HelloWorld-notes.html} and
.. % \ulink{summary}{classes/HelloWorld-summary.html}.
.. % end{latexonly}

::

   from Tkinter import *

   class Application(Frame):
       def say_hi(self):
           print "hi there, everyone!"

       def createWidgets(self):
           self.QUIT = Button(self)
           self.QUIT["text"] = "QUIT"
           self.QUIT["fg"]   = "red"
           self.QUIT["command"] =  self.quit

           self.QUIT.pack({"side": "left"})

           self.hi_there = Button(self)
           self.hi_there["text"] = "Hello",
           self.hi_there["command"] = self.say_hi

           self.hi_there.pack({"side": "left"})


       def __init__(self, master=None):
           Frame.__init__(self, master)
           self.pack()
           self.createWidgets()

   root = Tk()
   app = Application(master=root)
   app.mainloop()
   root.destroy()


Tcl/Tk を (本当に少しだけ) 見渡してみる
---------------------------------------

クラス階層は複雑に見えますが、実際にプログラムを書く際には、 アプリケーションプログラマはほとんど常にクラス階層の最底辺に あるクラスしか参照しません。

.. % BriefTclTk.html

注意:

* クラスのいくつかは、特定の関数を一つの名前空間下にまとめるために 提供されています。こうしたクラスは個別にインスタンス化するためのもの ではありません。

* :class:`Tk` クラスはアプリケーション内で一度だけインスタンス化 するようになっています。アプリケーションプログラマが明示的に
  インスタンス化する必要はなく、他のクラスがインスタンス化されると 常にシステムが作成します。

* :class:`Widget` クラスもまた、インスタンス化して使うようには なっていません。このクラスはサブクラス化して「実際の」ウィジェットを
  作成するためのものです。(C++ で言うところの、'抽象クラス  (abstract class)' です)。

このリファレンス資料を活用するには、Tk の短いプログラムを読んだり、 Tk コマンドの様々な側面を知っておく必要がままあるでしょう。
(下の説明の:mod:`Tkinter` 版は、 :ref:`tkinter-basic-mapping` 節を参照してください。)

Tk スクリプトは Tcl プログラムです。全ての Tcl プログラムに同じく、 Tk スクリプトはトークンをスペースで区切って並べます。 Tk
ウィジェットとは、ウィジェットの*クラス*、 ウィジェットの設定を行う*オプション*、そしてウィジェットに 役立つことをさせる*アクション*
をあわせたものに過ぎません。

Tk でウィジェットを作るには、常に次のような形式のコマンドを使います::

   classCommand newPathname options

*classCommand*
   どの種類のウィジェット (ボタン、ラベル、メニュー、...) を作るかを表します。

*newPathname*
   作成するウィジェットにつける新たな名前です。Tk 内の全ての名前は一意 になっていなければなりません。一意性を持たせる助けとして、 Tk 内の
   ウィジェットは、ファイルシステムにおけるファイルと同様、  *パス名 (pathname)* を使って名づけられます。 トップレベルのウィジェット、すなわち
   *ルート* は ``.``  (ピリオド) という名前になり、その子ウィジェット階層もピリオドで 区切ってゆきます。ウィジェットの名前は、例えば
   ``.myApp.controlPanel.okButton`` のようになります。

*options*
   ウィジェットの見た目を設定します。場合によってはウィジェットの挙動も 設定します。オプションはフラグと値がリストになった形式をとります。 Unix
   のシェルコマンドのフラグと同じように、フラグの前には '-' がつ き、複数の単語からなる値はクオートで囲まれます。

以下に例を示します::

   button   .fred   -fg red -text "hi there"
      ^       ^     \_____________________/
      |       |                |
    class    new            options
   command  widget  (-opt val -opt val ...)

ウィジェットを作成すると、ウィジェットへのパス名は新しいコマンドに なります。この新たな*widget command* は、プログラマが新たに作成した
ウィジェットに*action* を実行させる際のハンドル (handle) に なります。Cでは someAction(fred,
someOptions)と表し、 C++ではfred.someAction(someOptions)と表すでしょう。Tkでは::

   .fred someAction someOptions 

のようにします。 オブジェクト名 ``.fred`` はドットから始まっているので注意してください。

読者の想像の通り、*someAction* に指定できる値はウィジェット のクラスに依存しています: fred がボタンなら ``.fred disable``
は うまくいきます (fred はグレーになります) が、fred がラベルならうまく いきません (Tkではラベルの無効化をサポートしていないからです)。

*someOptions* に指定できる値はアクションの内容に依存しています。 ``disable`` のようなアクションは引数を必要としませんが、
テキストエントリボックスの ``delete``コマンドのようなアクションには テキストを削除する範囲を指定するための引数が必要になります。


.. _tkinter-basic-mapping:

基本的な Tk プログラムと Tkinter との対応関係
---------------------------------------------

Tkのクラスコマンドは、Tkinterのクラスコンストラクタに対応しています。 ::

   button .fred                =====>  fred = Button()

オブジェクトの親 (master) は、オブジェクトの作成時に指定した新たな名前から 非明示的に決定されます。Tkinter では親を明示的に指定します。 ::

   button .panel.fred          =====>  fred = Button(panel)

Tk の設定オプションは、ハイフンをつけたタグと値の組からなるリストで 指定します。Tkinter では、オプションはキーワード引数にして
インスタンスのコンストラクタに指定したり、:meth:`config` に キーワード引数を指定して呼び出したり、インデクス指定を使って
インスタンスに代入したりして設定します。オプションの設定については :ref:`tkinter-setting-options` 節を参照してください。　 ::

   button .fred -fg red        =====>  fred = Button(panel, fg = "red")
   .fred configure -fg red     =====>  fred["fg"] = red
                               OR ==>  fred.config(fg = "red")

Tk でウィジェットにアクションを実行させるには、ウィジェット名を コマンドにして、その後にアクション名を続け、必要に応じて引数 (オプション) を続けます。
Tkinter では、クラスインスタンスの メソッドを呼び出して、ウィジェットのアクションを呼び出します。 あるウィジェットがどんなアクション (メソッド)
を実行できるかは、 Tkinter.py モジュール内にリストされています。 ::

   .fred invoke                =====>  fred.invoke()

Tk でウィジェットを packer (ジオメトリマネジャ) に渡すには、 pack コマンドをオプション引数付きで呼び出します。 Tkinter では
Pack クラスがこの機能すべてを握っていて、 様々な pack の形式がメソッドとして実装されています。 :mod:`Tkinter` のウィジェットは全て
Packer からサブクラス化 されているため、pack 操作にまつわる全てのメソッドを継承しています。 Form
ジオメトリマネジャに関する詳しい情報については :mod:`Tix` モジュールのドキュメントを参照してください。 ::

   pack .fred -side left       =====>  fred.pack(side = "left")


Tk と Tkinter はどのように関わっているのか
------------------------------------------

.. % Relationship.html

.. note::

   以下の構図は図版をもとに書き下ろしたものです。このドキュメントの 今後のバージョンでは、図版をもっと直接的に利用する予定です。

上から下に、呼び出しの階層構造を説明してゆきます:

あなたのアプリケーション (Python)
   まず、 Python アプリケーションが:mod:`Tkinter`を呼び出します。

Tkinter ( Python モジュール)
   上記の呼び出し (例えば、ボタンウィジェットの作成) は、 *Tkinter* モジュール内で実現されており、Python で書かれています。 この
   Python で書かれた関数は、コマンドと引数を解析して変換し、あたかも コマンドが Python スクリプトではなく Tk スクリプトから来たように
   みせかけます。

tkinter (C)
   上記のコマンドと引数は *tkinter*  (小文字です。注意してください) 拡張モジュール内の C 関数に渡されます 。　

Tk Widgets (C and Tcl)
   上記の C 関数は、Tk ライブラリを構成する C 関数の入った別の C  モジュールへの呼び出しを行えるようになっています。 Tk は C と Tcl
   を少し使って実装されています。 Tk ウィジェットの Tcl 部分は、ウィジェットのデフォルト動作をバインド するために使われ、Python
   で書かれた:mod:`Tkinter` モジュールが import される時点で一度だけ実行されます。(ユーザがこの過程を目にする ことはありません。

Tk (C)
   Tkウィジェットの Tk 部分で実装されている最終的な対応付け操作によって...

Xlib (C)
   Xlib ライブラリがスクリーン上にグラフィックスを描きます。


簡単なリファレンス
------------------


.. _tkinter-setting-options:

オプションの設定
^^^^^^^^^^^^^^^^

オプションは、色やウィジェットの境界線幅などを制御します。 オプションの設定には三通りの方法があります:

オブジェクトを作成する時にキーワード引数を使う
   ::

      fred = Button(self, fg = "red", bg = "blue")

オブジェクトを作成した後、オプション名を辞書インデックスのように扱う
   ::

      fred["fg"] = "red"
      fred["bg"] = "blue"

オブジェクトを生成した後、config()メソッドを使って複数の属性を更新する
   ::

      fred.config(fg = "red", bg = "blue")

オプションとその振る舞いに関する詳細な説明は、該当するウィジェットの Tk の man マニュアルを参照してください。

man マニュアルには、各ウィジェットの  "STANDARD OPTIONS(標準オプション)" と "WIDGET SPECIFIC OPTIONS
(ウィジェット固有のオプション)" がリストされていることに注意しましょう。 前者は多くのウィジェットに共通のオプションのリストで、
後者は特定のウィジェットに特有のオプションです。標準オプションの 説明は man マニュアルの:manpage:`options(3)` にあります。

このドキュメントでは、標準オプションとウィジェット固有のオプションを 区別していません。オプションによっては、ある種のウィジェットに
適用できません。あるウィジェットがあるオプションに対応しているか どうかは、ウィジェットのクラスによります。例えばボタンには ``command``
オプションがありますが、ラベルにはありません。

あるウィジェットがどんなオプションをサポートしているかは、ウィジェット の man マニュアルにリストされています。また、実行時にウィジェットの
:meth:`config` メソッドを引数なしで呼び出したり、:meth:`keys` メソッドを呼び出したりして問い合わせることもできます。
メソッド呼び出しを行うと辞書型の値を返します。この辞書は、オプション の名前がキー (例えば ``'relief'``) になっていて、値が 5
要素のタプルになっています。

``bg`` のように、いくつかのオプションはより長い名前を持つ共通の オプションに対する同義語になっています (``bg``は "background" を
短縮したものです)。短縮形のオプション名を ``config()`` に渡すと、 5 要素ではなく 2 要素のタプルを返します。このタプルには、同義語の 名前と
「本当の」オプション名が入っています (例えば ``('bg', 'background')``)。

+--------------+--------------------------------------+--------------+
| インデックス | 意味                                 | 例           |
+==============+======================================+==============+
| 0            | オプション名                         | ``'relief'`` |
+--------------+--------------------------------------+--------------+
| 1            | データベース検索用のオプション名     | ``'relief'`` |
+--------------+--------------------------------------+--------------+
| 2            | データベース検索用のオプションクラス | ``'Relief'`` |
+--------------+--------------------------------------+--------------+
| 3            | デフォルト値                         | ``'raised'`` |
+--------------+--------------------------------------+--------------+
| 4            | 現在の値                             | ``'groove'`` |
+--------------+--------------------------------------+--------------+

例::

   >>> print fred.config()
   {'relief' : ('relief', 'relief', 'Relief', 'raised', 'groove')}

もちろん、実際に出力される辞書には利用可能なオプションが全て 表示されます。上の表示例は単なる例にすぎません。


Packer
^^^^^^

.. index:: single: packing (widgets)

.. % Packer.html

packer はTkのジオメトリ管理メカニズムの一つです。  ジオメトリマネジャは、複数のウィジェットの位置を、それぞれの ウィジェットを含むコンテナ -
共通の*マスタ (master)* からの 相対で指定するために使います。 やや扱いにくい *placer* (あまり使われないのでここでは取り上げ ません)
と違い、packer は定性的な関係を表す指定子 - *上 (above)*、 *〜の左 (to the left of)*、*引き延ばし (filling)*
など - を受け取り、厳密な配置座標の決定を全て行ってくれます。

.. % \citetitle[classes/ClassPacker.html]{the Packer class interface}も参照してくだい。

どんな*マスタ* ウィジェットでも、大きさは内部の "スレイブ (slave) ウィジェット" の大きさで決まります。packer は、スレイブウィジェットを
pack 先のマスタウィジェット中のどこに配置するかを制御するために使われ ます。 望みのレイアウトを達成するには、ウィジェットをフレームにパックし、
そのフレームをまた別のフレームにパックできます。 さらに、一度パックを行うと、それ以後の設定変更に合わせて動的に 並べ方を調整します。

ジオメトリマネジャがウィジェットのジオメトリを確定するまで、 ウィジェットは表示されないので注意してください。
初心者のころにはよくジオメトリの確定を忘れてしまい、 ウィジェットを生成したのに何も表示されず驚くことになります。
ウィジェットは、(例えばpackerの:meth:`pack`メソッドを適用して) ジオメトリを確定した後で初めて表示されます。

pack() メソッドは、キーワード引数つきで呼び出せます。キーワード引数 は、ウィジェットをコンテナ内のどこに表示するか、メインの
アプリケーションウィンドウをリサイズしたときにウィジェットがどう 振舞うかを制御します。以下に例を示します::

   fred.pack()                     # デフォルトでは、side = "top"
   fred.pack(side = "left")
   fred.pack(expand = 1)


Packer のオプション
^^^^^^^^^^^^^^^^^^^

packer と packer の取りえるオプションについての詳細は、man マニュアル や John Ousterhout の本の 183
ページを参照してください。

anchor 
   アンカーの型です。 packer が区画内に各スレイブを配置する位置を示します。

expand
   ブール値で、``0``または``1`` になります。

fill
   指定できる値は ``'x'``、``'y'``、``'both'``、``'none'`` です。

ipadxとipady
   スレイブウィジェットの各側面の内側に行うパディング幅を表す長さを 指定します。

padxとpady
   スレイブウィジェットの各側面の外側に行うパディング幅を表す長さを 指定します。

side
   指定できる値は ``'left'``, ``'right'``, ``'top'``,  ``'bottom'`` です。


ウィジェット変数を関連付ける
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ウィジェットによっては、(テキスト入力ウィジェットのように)  特殊なオプションを使って、現在設定されている値をアプリケーション内の
変数に直接関連付けできます。このようなオプションには``variable``、
``textvariable``、``onvalue``、``offvalue``および``value`` があります。この関連付けは双方向に働きます:
変数の値が何らかの理由で 変更されると、関連付けされているウィジェットも更新され、新しい値を 反映します。

.. % VarCouplings.html

残念ながら、現在の:mod:`Tkinter` の実装では、 ``variable`` や``textvariable`` オプションでは 任意の Python
の値をウィジェットに渡せません。 この関連付け機能がうまく働くのは、 :mod:`Tkinter` モジュール内で Variable というクラスから
サブクラス化されている変数によるオプションだけです。

Variable には、:class:`StringVar`、:class:`IntVar`、:class:`DoubleVar`および
:class:`BooleanVar` といった便利なサブクラスがすでにすでに数多く定義 されています。こうした変数の現在の値を読み出したければ、
:meth:`get` メソッドを呼び出します。また、値を変更したければ :meth:`set` メソッドを呼び出します。
このプロトコルに従っている限り、それ以上なにも手を加えなくても ウィジェットは常に現在値に追従します。

例えば::

   class App(Frame):
       def __init__(self, master=None):
           Frame.__init__(self, master)
           self.pack()

           self.entrythingy = Entry()
           self.entrythingy.pack()

           # アプリケーション変数です
           self.contents = StringVar()
           # 変数の値を設定します
           self.contents.set("this is a variable")
           # エントリウィジェットに変数の値を監視させます
           self.entrythingy["textvariable"] = self.contents

           # ユーザがリターンキーを押した時にコールバックを呼び出させます
           # これで、このプログラムは、ユーザがリターンキーを押すと
           # アプリケーション変数の値を出力するようになります。
           self.entrythingy.bind('<Key-Return>',
                                 self.print_contents)

       def print_contents(self, event):
           print "hi. contents of entry is now ---->", \
                 self.contents.get()


ウィンドウマネジャ
^^^^^^^^^^^^^^^^^^

.. index:: single: window manager (widgets)

.. % WindowMgr.html

Tk には、ウィンドウマネジャとやり取りするための ``wm`` という ユーティリティコマンドがあります。``wm`` コマンドにオプション
を指定すると、タイトルや配置、アイコンビットマップなどを操作 できます。:mod:`Tkinter` では、こうしたコマンドは :class:`Wm`
クラスのメソッドとして実装されています。 トップレベルウィジェットは :class:`Wm` クラスからサブクラス化 されているので、:class:`Wm`
のメソッドを直接呼び出せます。

あるウィジェットの入っているトップレベルウィンドウを取得したい場合、 大抵は単にウィジェットのマスタを参照するだけですみます。とはいえ、
ウィジェットがフレーム内にパックされている場合、マスタはトップレベル ウィンドウではありません。任意のウィジェットの入っている
トップレベルウィンドウを知りたければ :meth:`_root` メソッド を呼び出してください。このメソッドはアンダースコアがついていますが、
これはこの関数が :mod:`Tkinter` の実装の一部であり、Tk の機能 に対するインタフェースではないことを示しています。

.. % See also \citetitle[classes/ClassWm.html]{the Wm class interface}.

以下に典型的な使い方の例をいくつか挙げます::

   from Tkinter import *
   class App(Frame):
       def __init__(self, master=None):
           Frame.__init__(self, master)
           self.pack()


   # アプリケーションを作成します
   myapp = App()

   #
   # ウィンドウマネジャクラスのメソッドを呼び出します。
   #
   myapp.master.title("My Do-Nothing Application")
   myapp.master.maxsize(1000, 400)

   # プログラムを開始します
   myapp.mainloop()


Tk オプションデータ型
^^^^^^^^^^^^^^^^^^^^^

.. index:: single: Tk Option Data Types

.. % OptionTypes.html

anchor
   指定できる値はコンパスの方位です:
   ``"n"``、``"ne"``、``"e"``、``"se"``、``"s"``、``"sw"``、``"w"``、``"nw"``、および``"center"``。

bitmap
   八つの組み込み、名前付きビットマップ:
   ``'error'``、``'gray25'``、``'gray50'``、``'hourglass'``、``'info'``、``'questhead'``、``'question'``、``'warning'``。
   Xビットマップファイル名を指定するために、``"@/usr/contrib/bitmap/gumby.bit"``のような``@``を先頭に付けたファイルへの完全なパスを与えてください。

boolean
   整数0または1、あるいは、文字列``"yes"``または``"no"``を渡すことができます。

callback
   これは引数を取らない Python 関数ならどれでも構いません。例えば::

      def print_it():
              print "hi there"
      fred["command"] = print_it

color
   色はrgb.txtファイルのXカラーの名前か、またはRGB値を表す文字列として与えられます。RGB値を表す文字列は、4ビット: ``"#RGB"``, 8
   bit: ``"#RRGGBB"``, 12 bit" ``"#RRRGGGBBB"``, あるいは、16 bit
   ``"#RRRRGGGGBBBB"``の範囲を取ります。ここでは、R,G,Bは適切な十六進数ならどんなものでも表します。詳細は、Ousterhoutの本の160ページを参照してください。

cursor
   :file:`cursorfont.h`の標準Xカーソル名を、接頭語``XC_``無しで使うことができます。例えば、handカーソル(:const:`XC_hand2`)を得るには、文字列``"hand2"``を使ってください。あなた自身のビットマップとマスクファイルを指定することもできます。Ousterhoutの本の179ページを参照してください。

distance
   スクリーン上の距離をピクセルか絶対距離のどちらかで指定できます。ピクセルは数として与えられ、絶対距離は文字列として与えられます。絶対距離を表す文字列は、単位を表す終了文字(センチメートルには``c``、インチには``i``、ミリメートルには``m``、プリンタのポイントには``p``)を伴います。例えば、3.5インチは``"3.5i"``と表現します。

font
   Tkは``{courier 10
   bold}``のようなリストフォント名形式を使います。正の数のフォントサイズはポイント単位で表され。負の数のサイズはピクセル単位で表されます。

geometry
   これは``widthxheight``形式の文字列です。ここでは、ほとんどのウィジェットに対して幅と高さピクセル単位で(テキストを表示するウィジェットに対しては文字単位で)表されます。例えば:
   ``fred["geometry"] = "200x100"``。

justify
   指定できる値は文字列です: ``"left"``、``"center"``、``"right"``、and ``"fill"``。

region
   これは空白で区切られた四つの要素をもつ文字列です。各要素は指定可能な距離です(以下を参照)。例えば: ``"2 3 4 5"``と``"3i 2i 4.5i
   2i"``と``"3c 2c 4c 10.43c"``は、すべて指定可能な範囲です。

relief
   ウィジェットのボーダのスタイルが何かを決めます。指定できる値は:
   ``"raised"``、``"sunken"``、``"flat"``、``"groove"``、and ``"ridge"``。

scrollcommand
   これはほとんど常にスクロールバー・ウィジェットの:meth:`set`メソッドですが、一引数を取るどんなウィジェットメソッドでもあり得ます。例えば、
   Python ソース配布の:file:`Demo/tkinter/matt/canvas-with-scrollbars.py`ファイルを参照してください。

wrap:
   次の中の一つでなければならない: ``"none"``、``"char"``、あるいは``"word"``。


バインドとイベント
^^^^^^^^^^^^^^^^^^

.. index::
   single: bind (widgets)
   single: events (widgets)

.. % Bindings.html

ウィジェットコマンドからのbindメソッドによって、あるイベントを待つことと、そのイベント型が起きたときにコールバック関数を呼び出すことができるようになります。bindメソッドの形式は::

   def bind(self, sequence, func, add=''):

ここでは:

sequence
   は対象とするイベントの型を示す文字列です。(詳細については、bindのmanページとJohn Ousterhoutの本の201ページをを参照してください。)

func
   は一引数を取り、イベントが起きるときに呼び出される Python
   関数です。イベント・インスタンスが引数として渡されます。(このように実施される関数は、一般に*callbacks*として知られています。)

add
   はオプションで、````か``\ +``のどちらかです。
   空文字列を渡すことは、このイベントが関係する他のどんなバインドをもこのバインドが置き換えることを意味します。``\
   +``を使う仕方は、この関数がこのイベント型にバインドされる関数のリストに追加されることを意味しています。

例えば::

   def turnRed(self, event):
       event.widget["activeforeground"] = "red"

   self.button.bind("<Enter>", self.turnRed)

イベントのウィジェットフィールドが:meth:`turnRed`コールバック内でどのようにアクセスされているかに注意してください。
このフィールドはXイベントを捕らえるウィジェットを含んでいます。
以下の表はあなたがアクセスできる他のイベントフィールドとそれらのTkでの表現方法の一覧です。Tk manページを参照するときに役に立つでしょう。 ::

   Tk      Tkinterイベントフィールド       Tk      Tkinterイベントフィールド
   --      -------------------------       --      -------------------------
   %f      focus                           %A      char
   %h      height                          %E      send_event
   %k      keycode                         %K      keysym
   %s      state                           %N      keysym_num
   %t      time                            %T      type
   %w      width                           %W      widget
   %x      x                               %X      x_root
   %y      y                               %Y      y_root


index パラメータ
^^^^^^^^^^^^^^^^

たくさんのウィジェットが渡される"index"パラメータを必要とします。これらはテキストウィジェットでの特定の場所や、エントリウィジェットでの特定の文字、あるいは、メニューウィジェットでの特定のメニュー項目を指定するために使われます。

.. % Index.html

エントリウィジェットのインデックス(インデックス、ビューインデックスなど)
   エントリウィジェットは表示されているテキスト内の文字位置を参照するオプションを持っています。
   テキストウィジェットにおけるこれらの特別な位置にアクセスするために、これらの:mod:`Tkinter`関数を使うことができます:

   AtEnd()
      テキストの最後の位置を参照します

   AtInsert()
      テキストカーソルの位置を参照します

   AtSelFirst()
      選択されたテキストの先頭の位置を指します

   AtSelLast()
      選択されているテキストおよび最終的に選択されたテキストの末尾の位置を示します。

   At(x[, y])
      ピクセル位置*x*, *y*(テキストを一行だけ含むテキストエントリウィジェットの場合には*y*は使われない)の文字を参照します。

テキストウィジェットのインデックス
   テキストウィジェットに対するインデックス記法はとても機能が豊富で、Tk manページでよく説明されています。

メニューのインデックス(menu.invoke()、menu.entryconfig()など)
   メニューに対するいくつかのオプションとメソッドは特定のメニュー項目を操作します。メニューインデックスはオプションまたはパラメータのために必要とされるときはいつでも、以下のものを渡すことができます:

* 頭から数えられ、0で始まるウィジェットの数字の位置を指す整数。

* 文字列``'active'``、現在カーソルがあるメニューの位置を指します。

* 最後のメニューを指す文字列``"last"``。

* ``@6``のような``@``が前に来る整数。ここでは、整数がメニューの座標系におけるyピクセル座標として解釈されます。

*
     文字列``"none"``、どんなメニューエントリもまったく指しておらず、ほとんどの場合、すべてのエントリの動作を停止させるためにmenu.activate()と一緒に使われます。そして、最後に、

*
     メニューの先頭から一番下までスキャンしたときに、メニューエントリのラベルに一致したパターンであるテキスト文字列。このインデックス型は他すべての後に考慮されることに注意してください。その代わりに、それは``last``、``active``または``none``とラベル付けされたメニュー項目への一致は上のリテラルとして解釈されることを意味します。


画像
^^^^

Bitmap/Pixelmap画像を:class:`Tkinter.Image`のサブクラスを使って作ることができます:

* :class:`BitmapImage`はX11ビットマップデータに対して使えます。

* :class:`PhotoImage`はGIFとPPM/PGMカラービットマップに対して使えます。

画像のどちらの型でも``file``または``data``オプションを使って作られます(その上、他のオプションも利用できます)。

``image``オプションがウィジェットにサポートされるところならどこでも、画像オブジェクトを使うことができます(例えば、ラベル、ボタン、メニュー)。これらの場合では、Tkは画像への参照を保持しないでしょう。画像オブジェクトへの最後の
Python の参照が削除されたときに、おまけに画像データが削除されます。そして、どこで画像が使われていようとも、Tkは空の箱を表示します。


:mod:`Tix` --- Tkの拡張ウィジェット
===================================

.. module:: Tix
   :synopsis: Tkinter用のTk拡張ウィジェット
.. sectionauthor:: Mike Clarkson <mikeclarkson@users.sourceforge.net>


.. index:: single: Tix

:mod:`Tix` (Tk Interface
Extension)モジュールは豊富な追加ウィジェットを提供します。標準Tkライブラリには多くの有用なウィジェットがありますが、完全では決してありません。:mod:`Tix`ライブラリは標準Tkに欠けている一般的に必要とされるウィジェットの大部分を提供します:
:class:`HList`、:class:`ComboBox`、:class:`Control`
(別名SpinBox)および各種のスクロール可能なウィジェット。:mod:`Tix`には、一般的に幅広い用途に役に立つたくさんのウィジェットも含まれています:
:class:`NoteBook`、:class:`FileEntry`、:class:`PanedWindow`など。それらは40以上あります。

これら全ての新しいウィジェットと使うと、より便利でより直感的なユーザインタフェース作成し、あなたは新しい相互作用テクニックをアプリケーションに導入することができます。アプリケーションとユーザに特有の要求に合うように、大部分のアプリケーションウィジェットを選ぶことによって、アプリケーションを設計できます。


.. seealso::

   `Tix Homepage <http://tix.sourceforge.net/>`_
      :mod:`Tix`のホームページ。  ここには追加ドキュメントとダウンロードへのリンクがあります。

   `Tix Man Pages <http://tix.sourceforge.net/dist/current/man/>`_
      manページと参考資料のオンライン版。

   `Tix Programming Guide <http://tix.sourceforge.net/dist/current/docs/tix-book/tix.book.html>`_
      プログラマ用参考資料のオンライン版。

   `Tix Development Applications <http://tix.sourceforge.net/Tide/>`_
      TixとTkinterプログラムの開発のためのTixアプリケーション。TideアプリケーションはTkまたはTkinterに基づいて動作します。また、リモートでTix/Tk/Tkinterアプリケーションを変更やデバグするためのインスペクタ:program:`TixInspect`が含まれます。


Tixを使う
---------


.. class:: Tix(screenName[, baseName[, className]])

   たいていはアプリケーションのメインウィンドウを表すTixのトップレベルウィジェット。それにはTclインタープリタが付随します。

   :mod:`Tix`モジュールのクラスは:mod:`Tkinter`モジュールのクラスをサブクラス化します。前者は後者をインポートします。だから、Tkinterと一緒に:mod:`Tix`を使うためにやらなければならないのは、モジュールを一つインポートすることだけです。一般的に、:mod:`Tix`をインポートし、トップレベルでの:class:`Tkinter.Tk`の呼び出しを:class:`Tix.Tk`に置き換えるだけでよいのです::

      import Tix
      from Tkconstants import *
      root = Tix.Tk()

:mod:`Tix`を使うためには、通常Tkウィジェットのインストールと平行して、:mod:`Tix`ウィジェットをインストールしなければなりません。インストールをテストするために、次のことを試してください::

   import Tix
   root = Tix.Tk()
   root.tk.eval('package require Tix')

これが失敗した場合は、先に進む前に解決しなければならない問題がTkのインストールにあることになります。インストールされた:mod:`Tix`ライブラリを指定するためには環境変数:envvar:`TIX_LIBRARY`を使ってください。Tk動的オブジェクトライブラリ(:file:`tk8183.dll`または:file:`libtk8183.so`)を含むディレクトリと同じディレクトリに、動的オブジェクトライブラリ(:file:`tix8183.dll`または:file:`libtix8183.so`)があるかどうかを確かめてください。動的オブジェクトライブラリのあるディレクトリには、:file:`pkgIndex.tcl`
(大文字、小文字を区別します)という名前のファイルも含まれているべきで、それには次の一行が含まれます::

   package ifneeded Tix 8.1 [list load "[file join $dir tix8183.dll]" Tix]

.. % $ <-- bow to font-lock


Tixウィジェット
---------------

`Tix <http://tix.sourceforge.net/dist/current/man/html/TixCmd/TixIntro.htm>`_
は40個以上のウィジェットクラスを:mod:`Tkinter`のレパートリーに導入します。
標準配布の:file:`Demo/tix`ディレクトリには、:mod:`Tix`ウィジェットのデモがあります。

.. % The  Python  sample code is still being added to  Python , hence commented out


基本ウィジェット
^^^^^^^^^^^^^^^^


.. class:: Balloon()

   ヘルプを提示するためにウィジェット上にポップアップする`Balloon
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixBalloon.htm>`_。ユーザがカーソルをBalloonウィジェットが束縛されているウィジェット内部へ移動させたとき、説明のメッセージが付いた小さなポップアップウィンドウがスクリーン上に表示されます。

.. % Python  Demo of:
.. % \ulink{Balloon}{http://tix.sourceforge.net/dist/current/demos/samples/Balloon.tcl}


.. class:: ButtonBox()

   `ButtonBox
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixButtonBox.htm>`_ウィジェットは、``Ok
   Cancel``のためだけに普通は使われるようなボタンボックスを作成します。

.. % Python  Demo of:
.. % \ulink{ButtonBox}{http://tix.sourceforge.net/dist/current/demos/samples/BtnBox.tcl}


.. class:: ComboBox()

   `ComboBox
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixComboBox.htm>`_ウィジェットはMS
   Windowsのコンボボックスコントロールに似ています。ユーザはエントリ・サブウィジェットでタイプするか、リストボックス・サブウィジェットから選択するかのどちらかで選択肢を選びます。

.. % Python  Demo of:
.. % \ulink{ComboBox}{http://tix.sourceforge.net/dist/current/demos/samples/ComboBox.tcl}


.. class:: Control()

   `Control
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixControl.htm>`_ウィジェットは:class:`SpinBox`ウィジェットとしても知られています。ユーザは二つの矢印ボタンを押すか、またはエントリに直接値を入力して値を調整します。新しい値をユーザが定義した上限と下限に対してチェックします。

.. % Python  Demo of:
.. % \ulink{Control}{http://tix.sourceforge.net/dist/current/demos/samples/Control.tcl}


.. class:: LabelEntry()

   `LabelEntry
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixLabelEntry.htm>`_ウィジェットはエントリウィジェットとラベルを一つのメガウィジェットにまとめたものです。"記入形式"型のインタフェースの作成を簡単に行うために使うことができます。

.. % Python  Demo of:
.. % \ulink{LabelEntry}{http://tix.sourceforge.net/dist/current/demos/samples/LabEntry.tcl}


.. class:: LabelFrame()

   `LabelFrame
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixLabelFrame.htm>`_ウィジェットはフレームウィジェットとラベルを一つのメガウィジェットにまとめたものです。LabelFrameウィジェット内部にウィジェットを作成するためには、:attr:`frame`サブウィジェットに対して新しいウィジェットを作成し、それらを:attr:`frame`サブウィジェット内部で取り扱います。

.. % Python  Demo of:
.. % \ulink{LabelFrame}{http://tix.sourceforge.net/dist/current/demos/samples/LabFrame.tcl}


.. class:: Meter()

   `Meter
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixMeter.htm>`_ウィジェットは実行に時間のかかるバックグラウンド・ジョブの進み具合を表示するために使用できます。

.. % Python  Demo of:
.. % \ulink{Meter}{http://tix.sourceforge.net/dist/current/demos/samples/Meter.tcl}


.. class:: OptionMenu()

   `OptionMenu
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixOptionMenu.htm>`_はオプションのメニューボタンを作成します。

.. % Python  Demo of:
.. % \ulink{OptionMenu}{http://tix.sourceforge.net/dist/current/demos/samples/OptMenu.tcl}


.. class:: PopupMenu()

   `PopupMenu
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixPopupMenu.htm>`_ウィジェットは``tk_popup``コマンドの代替品として使用できます。:mod:`Tix`
   :class:`PopupMenu`ウィジェットの利点は、操作するためにより少ないアプリケーション・コードしか必要としないことです。

.. % Python  Demo of:
.. % \ulink{PopupMenu}{http://tix.sourceforge.net/dist/current/demos/samples/PopMenu.tcl}


.. class:: Select()

   `Select
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixSelect.htm>`_ウィジェットはボタン・サブウィジェットのコンテナです。ユーザに対する選択オプションのラジオボックスまたはチェックボックス形式を提供するために利用することができます。

.. % Python  Demo of:
.. % \ulink{Select}{http://tix.sourceforge.net/dist/current/demos/samples/Select.tcl}


.. class:: StdButtonBox()

   `StdButtonBox
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixStdButtonBox.htm>`_ウィジェットは、Motifに似たダイアログボックスのための標準的なボタンのグループです。

.. % Python  Demo of:
.. % \ulink{StdButtonBox}{http://tix.sourceforge.net/dist/current/demos/samples/StdBBox.tcl}


ファイルセレクタ
^^^^^^^^^^^^^^^^


.. class:: DirList()

   `DirList
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixDirList.htm>`_ウィジェットは、ディレクトリのリストビュー(その前のディレクトリとサブディレクトリ)を表示します。ユーザはリスト内の表示されたディレクトリの一つを選択したり、あるいは他のディレクトリへ変更したりできます。

.. % Python  Demo of:
.. % \ulink{DirList}{http://tix.sourceforge.net/dist/current/demos/samples/DirList.tcl}


.. class:: DirTree()

   `DirTree
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixDirTree.htm>`_ウィジェットはディレクトリのツリービュー(その前のディレクトリとそのサブディレクトリ)を表示します。ユーザはリスト内に表示されたディレクトリの一つを選択したり、あるいは他のディレクトリに変更したりできます。

.. % Python  Demo of:
.. % \ulink{DirTree}{http://tix.sourceforge.net/dist/current/demos/samples/DirTree.tcl}


.. class:: DirSelectDialog()

   `DirSelectDialog
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixDirSelectDialog.htm>`_ウィジェットは、ダイアログウィンドウにファイルシステム内のディレクトリを提示します。望みのディレクトリを選択するために、ユーザはファイルシステムを介して操作するこのダイアログウィンドウを利用できます。

.. % Python  Demo of:
.. % \ulink{DirSelectDialog}{http://tix.sourceforge.net/dist/current/demos/samples/DirDlg.tcl}


.. class:: DirSelectBox()

   :class:`DirSelectBox`は標準Motif(TM)ディレクトリ選択ボックスに似ています。ユーザがディレクトリを選択するために一般的に使われます。DirSelectBoxは主に最近ComboBoxウィジェットに選択されたディレクトリを保存し、すばやく再選択できるようにします。


.. class:: ExFileSelectBox()

   `ExFileSelectBox
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixExFileSelectBox.htm>`_ウィジェットは、たいていtixExFileSelectDialogウィジェット内に組み込まれます。ユーザがファイルを選択するのに便利なメソッドを提供します。:class:`ExFileSelectBox`ウィジェットのスタイルは、MS
   Windows 3.1の標準ファイルダイアログにとてもよく似ています。

.. % Python  Demo of:
.. % \ulink{ExFileSelectDialog}{http://tix.sourceforge.net/dist/current/demos/samples/EFileDlg.tcl}


.. class:: FileSelectBox()

   `FileSelectBox
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixFileSelectBox.htm>`_は標準的なMotif(TM)ファイル選択ボックスに似ています。ユーザがファイルを選択するために一般的に使われます。FileSelectBoxは主に最近:class:`ComboBox`ウィジェットに選択されたファイルを保存し、素早く再選択できるようにします。

.. % Python  Demo of:
.. % \ulink{FileSelectDialog}{http://tix.sourceforge.net/dist/current/demos/samples/FileDlg.tcl}


.. class:: FileEntry()

   `FileEntry
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixFileEntry.htm>`_ウィジェットはファイル名を入力するために使うことができます。ユーザは手でファイル名をタイプできます。その代わりに、ユーザはエントリの横に並んでいるボタンウィジェットを押すことができます。それはファイル選択ダイアログを表示します。

.. % Python  Demo of:
.. % \ulink{FileEntry}{http://tix.sourceforge.net/dist/current/demos/samples/FileEnt.tcl}


ハイアラキカルリストボックス
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: HList()

   `HList
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixHList.htm>`_ウィジェットは階層構造をもつどんなデータ(例えば、ファイルシステムディレクトリツリー)でも表示するために使用できます。リストエントリは字下げされ、階層のそれぞれの場所に応じて分岐線で接続されます。

.. % Python  Demo of:
.. % \ulink{HList}{http://tix.sourceforge.net/dist/current/demos/samples/HList1.tcl}


.. class:: CheckList()

   `CheckList
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixCheckList.htm>`_ウィジェットは、ユーザが選ぶ項目のリストを表示します。CheckListはTkのチェックリストやラジオボタンより多くの項目を扱うことができることを除いて、チェックボタンあるいはラジオボタンウィジェットと同じように動作します。

.. % Python  Demo of:
.. % \ulink{ CheckList}{http://tix.sourceforge.net/dist/current/demos/samples/ChkList.tcl}
.. % Python  Demo of:
.. % \ulink{ScrolledHList (1)}{http://tix.sourceforge.net/dist/current/demos/samples/SHList.tcl}
.. % Python  Demo of:
.. % \ulink{ScrolledHList (2)}{http://tix.sourceforge.net/dist/current/demos/samples/SHList2.tcl}


.. class:: Tree()

   `Tree
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixTree.htm>`_ウィジェットは階層的なデータをツリー形式で表示するために使うことができます。ユーザはツリーの一部を開いたり閉じたりすることによって、ツリーの見えを調整できます。

.. % Python  Demo of:
.. % \ulink{Tree}{http://tix.sourceforge.net/dist/current/demos/samples/Tree.tcl}
.. % Python  Demo of:
.. % \ulink{Tree (Dynamic)}{http://tix.sourceforge.net/dist/current/demos/samples/DynTree.tcl}


タビュラーリストボックス
^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: TList()

   `TList
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixTList.htm>`_ウィジェットは、表形式でデータを表示するために使うことができます。:class:`TList`ウィジェットのリスト・エントリは、Tkのリストボックス・ウィジェットのエントリに似ています。主な差は、(1)
   :class:`TList`ウィジェットはリスト・エントリを二次元形式で表示でき、(2)
   リスト・エントリに対して複数の色やフォントだけでなく画像も使うことができるということです。

.. % Python  Demo of:
.. % \ulink{ScrolledTList (1)}{http://tix.sourceforge.net/dist/current/demos/samples/STList1.tcl}
.. % Python  Demo of:
.. % \ulink{ScrolledTList (2)}{http://tix.sourceforge.net/dist/current/demos/samples/STList2.tcl}
.. % Grid has yet to be added to  Python
.. % \subsubsection{Grid Widget}
.. % Python  Demo of:
.. % \ulink{Simple Grid}{http://tix.sourceforge.net/dist/current/demos/samples/SGrid0.tcl}
.. % Python  Demo of:
.. % \ulink{ScrolledGrid}{http://tix.sourceforge.net/dist/current/demos/samples/SGrid1.tcl}
.. % Python  Demo of:
.. % \ulink{Editable Grid}{http://tix.sourceforge.net/dist/current/demos/samples/EditGrid.tcl}


管理ウィジェット
^^^^^^^^^^^^^^^^


.. class:: PanedWindow()

   `PanedWindow
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixPanedWindow.htm>`_ウィジェットは、ユーザがいくつかのペインのサイズを対話的に操作できるようにします。ペインは垂直または水平のどちらかに配置されます。ユーザは二つのペインの間でリサイズ・ハンドルをドラッグしてペインの大きさを変更します。

.. % Python  Demo of:
.. % \ulink{PanedWindow}{http://tix.sourceforge.net/dist/current/demos/samples/PanedWin.tcl}


.. class:: ListNoteBook()

   `ListNoteBook
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixListNoteBook.htm>`_ウィジェットは、:class:`TixNoteBook`ウィジェットにとてもよく似ています。ノートのメタファを使って限られた空間をに多くのウィンドウを表示するために使われます。ノートはたくさんのページ(ウィンドウ)に分けられています。ある時には、これらのページの一つしか表示できません。ユーザは:attr:`hlist`サブウィジェットの中の望みのページの名前を選択することによって、これらのページを切り替えることができます。

.. % Python  Demo of:
.. % \ulink{ListNoteBook}{http://tix.sourceforge.net/dist/current/demos/samples/ListNBK.tcl}


.. class:: NoteBook()

   `NoteBook
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixNoteBook.htm>`_ウィジェットは、ノートのメタファを多くのウィンドウを表示することができます。ノートはたくさんのページに分けられています。ある時には、これらのページの一つしか表示できません。ユーザはNoteBookウィジェットの一番上にある目に見える"タブ"を選択することで、これらのページを切り替えることができます。

.. % Python  Demo of:
.. % \ulink{NoteBook}{http://tix.sourceforge.net/dist/current/demos/samples/NoteBook.tcl}

.. % \subsubsection{Scrolled Widgets}
.. % Python  Demo of:
.. % \ulink{ScrolledListBox}{http://tix.sourceforge.net/dist/current/demos/samples/SListBox.tcl}
.. % Python  Demo of:
.. % \ulink{ScrolledText}{http://tix.sourceforge.net/dist/current/demos/samples/SText.tcl}
.. % Python  Demo of:
.. % \ulink{ScrolledWindow}{http://tix.sourceforge.net/dist/current/demos/samples/SWindow.tcl}
.. % Python  Demo of:
.. % \ulink{Canvas Object View}{http://tix.sourceforge.net/dist/current/demos/samples/CObjView.tcl}


画像タイプ
^^^^^^^^^^

:mod:`Tix`モジュールは次のものを追加します:

* 全ての:mod:`Tix`と:mod:`Tkinter`ウィジェットに対してXPMファイルからカラー画像を作成する`pixmap
  <http://tix.sourceforge.net/dist/current/man/html/TixCmd/pixmap.htm>`_機能。

  .. % Python  Demo of:
  .. % \ulink{XPM Image In Button}{http://tix.sourceforge.net/dist/current/demos/samples/Xpm.tcl}
  .. % Python  Demo of:
  .. % \ulink{XPM Image In Menu}{http://tix.sourceforge.net/dist/current/demos/samples/Xpm1.tcl}

* `Compound
  <http://tix.sourceforge.net/dist/current/man/html/TixCmd/compound.htm>`_
  画像タイプは複数の水平方向の線から構成される画像を作成するために使うこ とができます。それぞれの線は左から右に並べられた一連のアイテム(テキスト、
  ビットマップ、画像あるいは空白)から作られます。例え ば、Tkの:class:`Button`ウィジェットの中にビットマップとテキスト文字列を
  同時に表示するためにcompound画像は使われます。

  .. % Python  Demo of:
  .. % \ulink{Compound Image In Buttons}{http://tix.sourceforge.net/dist/current/demos/samples/CmpImg.tcl}
  .. % Python  Demo of:
  .. % \ulink{Compound Image In NoteBook}{http://tix.sourceforge.net/dist/current/demos/samples/CmpImg2.tcl}
  .. % Python  Demo of:
  .. % \ulink{Compound Image Notebook Color Tabs}{http://tix.sourceforge.net/dist/current/demos/samples/CmpImg4.tcl}
  .. % Python  Demo of:
  .. % \ulink{Compound Image Icons}{http://tix.sourceforge.net/dist/current/demos/samples/CmpImg3.tcl}


その他のウィジェット
^^^^^^^^^^^^^^^^^^^^


.. class:: InputOnly()

   `InputOnly
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixInputOnly.htm>`_ウィジェットは、ユーザから入力を受け付けます。それは、``bind``コマンドを使って行われます(Unixのみ)。


ジオメトリマネジャを作る
^^^^^^^^^^^^^^^^^^^^^^^^

加えて、:mod:`Tix`は次のものを提供することで:mod:`Tkinter`を補強します:


.. class:: Form()

   Tkウィジェットに対する接続ルールに基づいたジオメトリマネジャを`作成(Form)します
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tixForm.htm>`_。

.. % begin{latexonly}
.. % \subsection{Tix Class Structure}
.. % 
.. % \begin{figure}[hbtp]
.. % \centerline{\epsfig{file=hierarchy.png,width=.9\textwidth}}
.. % \vspace{.5cm}
.. % \caption{The Class Hierarchy of Tix Widgets}
.. % \end{figure}
.. % end{latexonly}


Tixコマンド
-----------


.. class:: tixCommand()

   `tixコマンド
   <http://tix.sourceforge.net/dist/current/man/html/TixCmd/tix.htm>`_は:mod:`Tix`の内部状態と:mod:`Tix`アプリケーション・コンテキストのいろいろな要素へのアクセスを提供します。これらのメソッドによって操作される情報の大部分は、特定のウィンドウというよりむしろアプリケーション全体かスクリーンあるいはディスプレイに関するものです。

   現在の設定を見るための一般的な方法は、  ::

      import Tix
      root = Tix.Tk()
      print root.tix_configure()


.. method:: tixCommand.tix_configure([cnf,] **kw)

   Tixアプリケーション・コンテキストの設定オプションを問い合わせたり、変更したりします。オプションが指定されなければ、利用可能なオプションすべてのディクショナリを返します。オプションが値なしで指定された場合は、メソッドは指定されたオプションを説明するリストを返します(このリストはオプションが指定されていない場合に返される値に含まれている、指定されたオプションに対応するサブリストと同一です)。一つ以上のオプション-値のペアが指定された場合は、メソッドは与えられたオプションが与えられた値を持つように変更します。この場合は、メソッドは空文字列を返します。オプションは設定オプションのどれでも構いません。


.. method:: tixCommand.tix_cget(option)

   *option*によって与えられた設定オプションの現在の値を返します。オプションは設定オプションのどれでも構いません。


.. method:: tixCommand.tix_getbitmap(name)

   ビットマップディレクトリの一つの中の``name.xpm``または``name``と言う名前のビットマップファイルの場所を見つけ出します(:meth:`tix_addbitmapdir`メソッドを参照してください)。:meth:`tix_getbitmap`を使うことで、アプリケーションにビットマップファイルのパス名をハードコーディングすることを避けることができます。成功すれば、文字``@``を先頭に付けたビットマップファイルの完全なパス名を返します。戻り値をTkとTixウィジェットの``bitmap``オプションを設定するために使うことができます。


.. method:: tixCommand.tix_addbitmapdir(directory)

   Tixは:meth:`tix_getimage`と:meth:`tix_getbitmap`メソッドが画像ファイルを検索するディレクトリのリストを保持しています。標準ビットマップディレクトリは:file:`$TIX_LIBRARY/bitmaps`です。:meth:`tix_addbitmapdir`メソッドは*directory*をこのリストに追加します。そのメソッドを使うことによって、アプリケーションの画像ファイルを:meth:`tix_getimage`または:meth:`tix_getbitmap`メソッドを使って見つけることができます。


.. method:: tixCommand.tix_filedialog([dlgclass])

   このアプリケーションからの異なる呼び出しの間で共有される可能性があるファイル選択ダイアログを返します。最初に呼ばれた時に、このメソッドはファイル選択ダイアログ・ウィジェットを作成します。このダイアログはその後のすべての:meth:`tix_filedialog`への呼び出しで返されます。オプションのdlgclassパラメータは、要求されているファイル選択ダイアログ・ウィジェットの型を指定するために文字列として渡されます。指定可能なオプションは``tix``、``FileSelectDialog``あるいは``tixExFileSelectDialog``です。


.. method:: tixCommand.tix_getimage(self, name)

   ビットマップディレクトリの一つの中の:file:`name.xpm`、:file:`name.xbm`または:file:`name.ppm`という名前の画像ファイルの場所を見つけ出します(上の:meth:`tix_addbitmapdir`メソッドを参照してください)。同じ名前(だが異なる拡張子)のファイルが一つ以上ある場合は、画像のタイプがXディスプレイの深さに応じて選択されます。xbm画像はモノクロディスプレイの場合に選択され、カラー画像はカラーディスプレイの場合に選択されます。:meth:`tix_getimage`を使うことによって、アプリケーションに画像ファイルのパス名をハードコーディングすることを避けられます。成功すれば、このメソッドは新たに作成した画像の名前を返し、TkとTixウィジェットの``image``オプションを設定するためにそれを使うことができます。


.. method:: tixCommand.tix_option_get(name)

   Tixのスキーム・メカニズムによって保持されているオプションを得ます。


.. method:: tixCommand.tix_resetoptions(newScheme, newFontSet[, newScmPrio])

   Tixアプリケーションのスキームとフォントセットを*newScheme*と*newFontSet*それぞれへと再設定します。これはこの呼び出し後に作成されたそれらのウィジェットだけに影響します。そのため、Tixアプリケーションのどんなウィジェットを作成する前にresetoptionsメソッドを呼び出すのが最も良いのです。

   オプション・パラメータ*newScmPrio*を、Tixスキームによって設定されるTkオプションの優先度レベルを再設定するために与えることができます。

   TkがXオプションデータベースを扱う方法のため、Tixがインポートされ初期化された後に、カラースキームとフォントセットを:meth:`tix_config`メソッドを使って再設定することができません。その代わりに、:meth:`tix_resetoptions`メソッドを使わなければならないのです。


:mod:`ScrolledText` --- スクロールするテキストウィジェット
==========================================================

.. module:: ScrolledText
   :platform: Tk
   :synopsis: 垂直スクロールバーを持つテキストウィジェット。
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


:mod:`ScrolledText`モジュールは"正しい動作"をするように設定された垂直スクロールバーをもつ基本的なテキストウィジェットを実装する同じ名前のクラスを提供します。:class:`ScrolledText`クラスを使うことは、テキストウィジェットとスクロールバーを直接設定するより簡単です。コンストラクタは:class:`Tkinter.Text`クラスのものを同じです。

テキストウィジェットとスクロールバーは:class:`Frame`の中に一緒にpackされ、:class:`Grid`と:class:`Pack`ジオメトリマネジャのメソッドは:class:`Frame`オブジェクトから得られます。これによって、もっとも標準的なジオメトリマネジャの振る舞いにするために、直接:class:`ScrolledText`ウィジェットを使えるようになります。

特定の制御が必要ならば、以下の属性が利用できます:


.. attribute:: ScrolledText.frame

   テキストとスクロールバーウィジェットを取り囲むフレーム。


.. attribute:: ScrolledText.vbar

   スクロールバーウィジェット。

XXX: input{libturtle} :XXX

.. _idle:

Idle
====

.. moduleauthor:: Guido van Rossum <guido@ Python .org>


.. % \declaremodule{standard}{idle}
.. % \modulesynopsis{A  Python  Integrated Development Environment}

.. index::
   single: Idle
   single: Python  Editor
   single: Integrated Development Environment

Idleは:mod:`Tkinter` GUIツールキットをつかって作られた Python  IDEです。

IDLEは次のような特徴があります:

* :mod:`Tkinter` GUIツールキットを使って、100% ピュア  Python でコーディングされています

* クロス-プラットホーム: WindowsとUnixで動作します (Mac OSでは、現在Tcl/Tkに問題があります)

* 多段Undo、 Python 対応の色づけや他にもたくさんの機能(例えば、自動的な字下げや呼び出し情報の表示)をもつマルチ-ウィンドウ・テキストエディタ

* Python シェルウィンドウ(別名、対話インタープリタ)

* デバッガ(完全ではりませんが、ブレークポイントの設定や値の表示、ステップ実行ができます)


メニュー
--------


Fileメニュー
^^^^^^^^^^^^

New window
   新しい編集ウィンドウを作成します

Open...
   既存のファイルをオープンします

Open module...
   既存のモジュールをオープンします(sys.pathを検索します)

Class browser
   現在のファイルの中のクラスとモジュールを示します

Path browser
   sys.pathディレクトリ、モジュール、クラスおよびメソッドを示します

.. index::
   single: Class browser
   single: Path browser

Save
   現在のウィンドウを対応するファイルにセーブします(未セーブのウィンドウには、ウィンドウタイトルの前後に\*があります)

Save As...
   現在のウィンドウを新しいファイルへセーブします。そのファイルが対応するファイルになります

Save Copy As...
   現在のウィンドウを対応するファイルを変えずに異なるファイルにセーブします。

Close
   現在のウィンドウを閉じます(未セーブの場合はセーブするか質問します)

Exit
   すべてのウィンドウを閉じてIDLEを終了します(未セーブの場合はセーブするか質問します)


Editメニュー
^^^^^^^^^^^^

Undo
   現在のウィンドウに対する最後の変更をUndo(取り消し)します(最大で1000個の変更)

Redo
   現在のウィンドウに対する最後にundoされた変更をRedo(再実行)します

Cut
   システムのクリップボードへ選択された部分をコピーします。それから選択された部分を削除します

Copy
   選択された部分をシステムのクリップボードへコピーします

Paste
   システムのクリップボードをウィンドウへ挿入します

Select All
   編集バッファの内容全体を選択します

Find...
   たくさんのオプションをもつ検索ダイアログボックスを開きます

Find again
   最後の検索を繰り返します

Find selection
   選択された文字列を検索します

Find in Files...
   検索するファイルに対する検索ダイアログボックスを開きます

Replace...
   検索と置換ダイアログボックスを開きます

Go to line
   行番号を尋ね、その行を表示します

Indent region
   選択された行を右へ空白4個分シフトします

Dedent region
   選択された行を左へ空白4個分シフトします

Comment out region
   選択された行の先頭に##を挿入します

Uncomment region
   選択された行から先頭の#あるいは##を取り除きます

Tabify region
   *先頭*の一続きの空白をタブに置き換えます

Untabify region
   *すべての*タブを適切な数の空白に置き換えます

Expand word
   あなたがタイプした語を同じバッファの別の語に一致するように展開します。そして、異なる展開が得るために繰り返します

Format Paragraph
   現在の空行で区切られた段落を再フォーマットします

Import module
   現在のモジュールをインポートまたはリロードします

Run script
   現在のファイルを__main__名前空間内で実行します

.. index::
   single: Import module
   single: Run script


Windowsメニュー
^^^^^^^^^^^^^^^

Zoom Height
   ウィンドウを標準サイズ(24x80)と最大の高さの間で切り替えます

このメニューの残りはすべての開いたウィンドウの名前の一覧になっています。一つを選ぶとそれを最前面に持ってくることができます(必要ならばアイコン化をやめさせます)


Debugメニュー( Python シェルウィンドウ内のみ)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to file/line
   挿入ポイントの周りからファイル名と行番号を探し、ファイルをオープンし、その行を表示します

Open stack viewer
   最後の例外のスタックトレースバックを表示します

Debugger toggle
   デバッガの下、シェル内でコマンドを実行します

JIT Stack viewer toggle
   トレースバック上のスタックビューアをオープンします

.. index::
   single: stack viewer
   single: debugger


基本的な編集とナビゲーション
----------------------------

* :kbd:`Backspace`は左側を削除し、:kbd:`Del`は右側を削除します

* 矢印キーと:kbd:`Page Up`/:kbd:`Page Down`はそれぞれ移動します

* :kbd:`Home`/:kbd:`End`は行の始め/終わりへ移動します

* :kbd:`C-Home`/:kbd:`C-End`はファイルの始め/終わりへ移動します

*
  :kbd:`C-B`、:kbd:`C-P`、:kbd:`C-A`、:kbd:`C-E`、:kbd:`C-D`、:kbd:`C-L`を含む、いくつかの:program:`Emacs`バインディングも動作します


自動的な字下げ
^^^^^^^^^^^^^^

ブロックの始まりの文の後、次の行は4つの空白( Python
Shellウィンドウでは、一つのタブ)で字下げされます。あるキーワード(break、returnなど)の後では、次の行は字下げが解除(dedent)されます。先頭の字下げでは、:kbd:`Backspace`は4つの空白があれば削除します。:kbd:`Tab`は1-4つの空白(
Python  Shellウィンドウでは一つのタブ)を挿入します。editメニューのindent/dedent regionコマンドも参照してください。


Python  Shellウィンドウ
^^^^^^^^^^^^^^^^^^^^^^^

* :kbd:`C-C` 実行中のコマンドを中断します

* :kbd:`C-D` ファイル終端(end-of-file)を送り、``>>>``プロンプトでタイプしていた場合はウィンドウを閉じます

* :kbd:`Alt-p` あなたがタイプしたことに一致する以前のコマンドを取り出します

* :kbd:`Alt-n` 次を取り出します

* :kbd:`Return` 以前のコマンドを取り出しているときは、そのコマンド

* :kbd:`Alt-/` (語を展開します)ここでも便利です

.. index:: single: indentation


構文の色づけ
------------

色づけはバックグランド"スレッド"で適用され、そのため時折色付けされないテキストが見えます。カラースキームを変えるには、:file:`config.txt`の``[Colors]``節を編集してください。

Python の構文の色:
   キーワード
      オレンジ

   文字列
      緑

   コメント
      赤

   定義
      青

シェルの色:
   コンソールの出力
      茶色

   stdout
      青

   stderr
      暗い緑

   stdin
      黒


コマンドラインの使い方
^^^^^^^^^^^^^^^^^^^^^^

::

   idle.py [-c command] [-d] [-e] [-s] [-t title] [arg] ...

   -c コマンド このコマンドを実行します
   -d          デバッガを有効にします
   -e          編集モード、引数は編集するファイルです
   -s          $IDLESTARTUPまたは$PYTHONSTARTUPを最初に実行します
   -t タイトル シェルウィンドウのタイトルを設定します

引数がある場合:

#. :option:`-e`が使われる場合は、引数は編集のためにオープンされるファイルで、``sys.argv``はIDLE自体へ渡される引数を反映します。

#.
   そうではなく、:option:`-c`が使われる場合には、すべての引数が``sys.argv[1:...]``の中に置かれ、``sys.argv[0]``が``'-c'``に設定されます。

#.
   そうではなく、:option:`-e`でも:option:`-c`でも使われない場合は、最初の引数は``sys.argv[1:...]``にある残りの引数とスクリプト名に設定される``sys.argv[0]``と一緒に実行されるスクリプトです。スクリプト名が'-'のときは、実行されるスクリプトはありませんが、対話的な
   Python セッションが始まります。引数はまだ``sys.argv``にあり利用できます。


.. _other-gui-packages:

他のグラフィカルユーザインタフェースパッケージ
==============================================

:mod:`Tkinter`へ付け加えられるたくさんの拡張ウィジェットがあります。


.. seealso::

   ` Python メガウィジェット <http://pmw.sourceforge.net/>`_
      :mod:`Tkinter`モジュールを使い Python で高レベルの複合 ウィジェットを構築するためのツールキットです。基本クラスと
      この基礎の上に構築された柔軟で拡張可能なメガウィジェットか ら構成されています。これらのメガウィジェットはノートブック、
      コンボボックス、選択ウィジェット、ペインウィジェット、スク ロールするウィジェット、ダイアログウィンドウなどを含みます。
      BLTに対するPmw.Bltインタフェースを持ち、busy、graph、 stripchart、tabsetおよびvectorコマンドが利用できます。

      Pmwの最初のアイディアは、Michael McLennanによるTk ``itcl``拡張 ``[incr Tk]``とMark
      Ulfertsによる``[incr Widgets]``から得ました。 メガウィジェットのいくつかはitclから Python へ直接変換したものです。
      ``[incr Widgets]``が提供するウィジェットとほぼ同等のものを提供しま す。そして、Tixと同様にほぼ完成しています。しかしながら、ツリーを描く
      ためのTixの高速な:class:`HList`ウィジェットが欠けています。

   `Tkinter3000 Widget Construction Kit (WCK) <http://tkinter.effbot.org/>`_
      は、新しい Tkinter ウィジェットを、 Python  で書けるようにするライブラリで す。WCK
      フレームワークは、ウィジェットの生成、設定、スクリーンの外観、イ ベント操作における、完全な制御を提供します。Tk/Tcl レイヤーを通してデー
      タ転送する必要がなく、直接  Python  のデータ構造を操作することができるので、 WCK ウィジェットは非常に高速で軽量になり得ます。

      .. % 

他にも Python で使える GUI パッケージがあります。


.. seealso::

   `wxPython <http://www.wxpython.org>`_
      wxPython はクロスプラットフォームの Python 用 GUI ツールキットで、 人気のある `wxWidgets
      <http://www.wxwidgets.org/>`_ C++ ツールキットに基づいて作られています。このツールキットは Windows, Mac OS X
      および Unix システムのアプリケーションに、 それぞれのプラットフォームのネイティブなウィジェットを可能ならば利用して (Unix系のシステムでは
      GTK+)、ネイティブなルック＆フィールを提供します。 多彩なウィジェットの他に、オンラインドキュメントや場面に応じたヘルプ、 印刷、HTML
      表示、低級デバイスコンテキスト描画、ドラッグ＆ドロップ、 システムクリップボードへのアクセス、XML に基づいたリソースフォーマット、
      さらにユーザ寄贈のモジュールからなる成長し続けているライブラリ等々を wxPython は提供しています。wxWidget も wxPython
      もどちらのプロジェクトも 活発に開発が続けられ改良が進められており、活動的で親切なユーザと開発者の コミュニティがあります。

   `wxPython in Action <http://www.amazon.com/exec/obidos/ASIN/1932394621>`_
      Noel Rappin と Robin Dunn による wxPython の本。

   PyQt
      PyQtは:program:`sip`でラップされたQtツールキットへの バインディングです。QtはUnix、WindowsおよびMac OS Xで利用できる大
      規模なC++ GUIツールキットです。:program:`sip`は Python クラスとし
      てC++ライブラリに対するバインディングを生成するためのツールキット で、特に Python 用に設計されています。オンライン・マニュアルは
      `<http://www.opendocspublishing.com/pyqt/>`_ (正誤表は
      `<http://www.valdyas.org/python/book.html>`_にあります)で手に入りま す。

   `PyKDE <http://www.riverbankcomputing.co.uk/pykde/index.php>`_
      PyKDEは:program:`sip`でラップされたKDEデスクトップライブラリに対するイ
      ンタフェースです。KDEはUnixコンピュータ用のデスクトップ環境です。グ ラフィカル・コンポーネントはQtに基づいています。

   `FXPy <http://fxpy.sourceforge.net/>`_
      `FOX <http://www.cfdrc.com/FOX/fox.html>`_ GUIへのインタフェースを提供する Python
      拡張モジュールです。FOXは、グ ラフィカルユーザインタフェースを簡単かつ効率良く開発するためのC++
      ベースのツールキットです。それは幅広く、成長しているコントロール・コ レクションで、3Dグラフィックスの操作のためのOpenGLウィジェットと同様
      に、ドラッグアンドドロップ、選択のような最新の機能を提供します。FOX はアイコン、画像およびステータスライン・ヘルプやツールチップのような
      ユーザにとって便利な機能も実装しています。

      FOXはすでに大規模なコントロール・コレクションを提供していますが、単に 既存のコントロールを使って望みの振る舞いを追加または再定義する派生クラ
      スを作成することによってプログラマが簡単に追加コントロールとGUI要素を 構築できるようにするために、FOXはC++を利用しています。

   `PyGTK <http://www.daa.com.au/~ james/software/pygtk/>`_
      `GTK <http://www.gtk.org/>`_ウィ ジェットセットのための一連のバインディングです。Cのものより少しだけ
      高レベルなオブジェクト指向インタフェースを提供します。普通はC APIを 使ってやらなければならない型キャストとリファレンス・カウントをすべて
      自動的に行います。`GNOME <http://www.gnome.org>`_に対しても、 `バインディング <http://www.daa.com.au/~
      james/gnome/>`_があります。`チュートリアル <http://laguna.fmedic.unam.mx/~
      daniel/pygtutorial/pygtutorial/index.html>`_が手に入ります。

.. % XXX Reference URLs that compare the different UI packages

