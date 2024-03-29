#######################################
 Python 2.6 ドキュメント翻訳について
#######################################

:author: 稲田 直哉  <inada-n@klab.jp>
:date: 2008-10-21


reStructuredText について
=========================

LatexからreStructuredTextへ
---------------------------
Python 2.6 から、ドキュメントシステムが latex から sphinx に変更されました。
sphinxでは、各文章を reStructuredText (略称: reST、拡張子は決まっていませんが、
Pythonドキュメントでは rst) という記法で記述します。

ドキュメント記法についての詳細は、Python 2.6 ドキュメントの中の、
Documenting Python をみてください。

preconvツールについて
-----------------------

未翻訳のドキュメントは、Latexから自動的にreStructuredTextに変換されたものです。
これは本家がLatexからreSTに移行したときに使った変換ツールを少しカスタマイズして
利用しているのですが、英語と日本語の違いの為に、変換結果は多くの箇所であまりよくありません。
例えば、 ::

   この値が``True``のとき

のような場合、 reST ではバッククオートの前後にスペースが無いためにマークアップだと認識されません。
次のように修正しなければなりません。 ::

   この値が ``True`` のとき

``refs/jptool/preconv.py`` は、こういった問題をヒューリスティックに修正する為のツールです。
このツールをどこかパスの通った場所に置くなり、翻訳しているドキュメントの場所にコピーするなりして、
簡単に使えるようにしてください。ここでは、 ``library/`` ディレクトリ以下にコピーしたとします。
たとえば ``tarfile.rst`` の翻訳をする前に、 ::

   $ python preconv.py tarfile.rst

を実行すると、tarfile.rst が tarfile.rst.orig にリネームされ、修正後のファイルが tarfile.rst
という名前で保存されます。preconv.pyは完璧なツールでは無いので、 orig ファイルと比較して
修正結果を確認してください。その後、差分翻訳を始めてください。


日本語とreStructuredText
------------------------
reStructuredTextのコンセプトの一つに、そのまま（変換前）での読みやすさが
あります。そのために、見出し記法ではアンダーラインを、table記法では罫線を
書く必要があります。(読みやすさのための少しの書きにくさは許容するのは、
なんとなくPythonicな気がします)

ここで、文字幅の問題が出てきます。初期のreSTは、文字幅のことを考慮されて
いないため、いわゆる「全角・倍角」の文字も「半角」の文字も一文字は一文字として
扱われていました。これは、特にtable(表)において問題になりました ::

    == == ==
    あい うえ おか
    == == ==
    きく けこ さし
    == == ==

現在のreStructuredTextでは、文字幅が考慮されるようになりました。
上の例のテーブルでは、罫線が一カラムあたり4文字で書けます ::

    ==== ==== ====
    あい うえ おか
    ==== ==== ====
    きく けこ さし
    ==== ==== ====

文字幅の判定には、 ``unicodedata`` の ``east_asian_width()`` が利用されます。
ここで、ターミナルの設定等でおなじみの、Ambiguous 文字の文字幅の扱いに関する
問題が起こります。この文字は、地域やフォントによって文字幅が異なる文字です。

ターミナル等の設定では単に見え方の問題なので、日本では Ambiguous 文字のすべてを
倍幅で扱うことでほとんど問題が起こりません。しかし、文書記法のreSTで、ユーザー
が文字幅を「環境設定」できてしまうと、ある文書が環境によって正常に parse でき
たりできなかったりしてしまいます。これは好ましくないので、Python ドキュメント
翻訳プロジェクトではdocutilsを改造せずにそのまま利用することにします。

docutils での文字幅は、 ``docutils.utils.east_asian_widths`` で設定されています。
Ambiguous 文字の文字幅は1になっています。なので、お使いの環境で倍角に見える
文字であっても、 Ambiguous 文字であれば、半角だと思って table を書くように
してください。（見出しの下線については、見出しの文字列より長くても問題ないので、
見た目の長さと一致するように書いてかまいません）

Ambiguous 文字には、たとえば以下のような文字が含まれます ::

 Д○③Ⅲ←⇔⇧

これらの文字は、特にtableの中では、避けた方が無難です。


ディレクトリの解説
===================
/
   翻訳していくターゲットとなるディレクトリ.

/refs/rest262
   Python 2.6.2 リリースパッケージの中のDocディレクトリを取り出したもの。お手本。

