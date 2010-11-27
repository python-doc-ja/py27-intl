.. highlightlang:: rest

.. Style Guide
.. ===========

スタイルガイド
==============

.. The Python documentation should follow the `Apple Publications Style Guide`_
.. wherever possible. This particular style guide was selected mostly because it
.. seems reasonable and is easy to get online.

Python ドキュメントは、可能な限り `Apple Publications Style Guide`_ に
準拠することになっています。内容の合理性と、オンラインで容易に取得できることから、
このスタイルガイドが選ばれました。

.. _Apple Publications Style Guide: http://developer.apple.com/documentation/UserExperience/Conceptual/APStyleGuide/APSG_2008.pdf

.. Topics which are not covered in the Apple's style guide will be discussed in
.. this document if necessary.

Apple のスタイルガイドがカバーしていないトピックについては、この
ドキュメントで必要に応じて議論していきます。

.. Footnotes are generally discouraged, though they may be used when they are the
.. best way to present specific information. When a footnote reference is added at
.. the end of the sentence, it should follow the sentence-ending punctuation. The
.. reST markup should appear something like this::

脚注は、何かの情報を提供するのにもっとも適した方法である場合は利用されますが、
普通はお勧めできません。
脚注への参照を文の最後に追加する場合は、句点の後に追加しなければなりません。
reST 記法は次のようになります ::

    この文には脚注への参照があります。 [#]_ ここは次の文になります。

.. Footnotes should be gathered at the end of a file, or if the file is very long,
.. at the end of a section. The docutils will automatically create backlinks to the
.. footnote reference.

脚注はファイルの終端か、ファイルが非常に大きい場合は節の終わりに集められます。
docutils は自動的に、脚注の参照への逆リンクを作成します。

.. Footnotes may appear in the middle of sentences where appropriate.

脚注は、文の途中でも適切な場所で使用することができます。

.. Many special names are used in the Python documentation, including the names of
.. operating systems, programming languages, standards bodies, and the like. Most
.. of these entities are not assigned any special markup, but the preferred
.. spellings are given here to aid authors in maintaining the consistency of
.. presentation in the Python documentation.

Python ドキュメントの中では、オペレーティングシステムやプログラミング言語、
標準機関、その他の名前を含む沢山の特殊な名前を使っています。
それらの名前のほとんどには特別なマークアップを割り当てていませんが、推奨される
表記法をここで提供して、ドキュメント作者が Python ドキュメント内の表現の一貫性を
維持しやすくします。

.. Other terms and words deserve special mention as well; these conventions should
.. be used to ensure consistency throughout the documentation:

その他の用語や単語についても特に説明しておく必要があるでしょう;
ドキュメントの作者はこれらの規約に従い、ドキュメント全体を通して
一貫性を保証しなければなりません。

.. CPU
..     For "central processing unit." Many style guides say this should be spelled
..     out on the first use (and if you must use it, do so!). For the Python
..     documentation, this abbreviation should be avoided since there's no
..     reasonable way to predict which occurrence will be the first seen by the
..     reader. It is better to use the word "processor" instead.

CPU
    "central processing unit" (中央処理装置) のことです。多くのスタイルガイドが、
    この語を最初に利用するときには略さずに書かねばならないとしています
    (ですから、どうしてもこの語を使う必要があるなら、必ずそうしてください!)。
    Python ドキュメントでは、読者が最初にどこを読むのか合理的に予測する方法がないので、
    略語の使用を避けねばなりません。
    代わりに "processor (プロセッサ)" を使う方がよいでしょう。

.. POSIX
..     The name assigned to a particular group of standards. This is always
..     uppercase.

POSIX
    ある一連の標準仕様につけられた名前です。常に大文字だけからなります。

.. Python
..     The name of our favorite programming language is always capitalized.

Python
    私たちの大好きなプログラミング言語の名前は、常に大文字で始めます。

.. Unicode
..     The name of a character set and matching encoding. This is always written
..     capitalized.

Unicode
    ある文字セットと、それに対応する符号化方式の名前です。
    常に大文字で始めます。

.. Unix
..     The name of the operating system developed at AT&T Bell Labs in the early
..     1970s.

Unix
    1970年代初頭に AT&T ベル研究所で開発されたオペレーティングシステムの名前です。
