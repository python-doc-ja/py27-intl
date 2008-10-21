.. % \chapter{Built-in Functions, Types, and Exceptions \label{builtin}}


.. _builtin:

********************
組み込みオブジェクト
********************

組み込み例外名、関数名、各種定数名は専用のシンボルテーブル中に存在しています。 シンボル名を参照するときこのシンボルテーブルは最後に参照されるので、
ユーザーが設定したローカルな名前やグローバルな名前によってオーバーライド することができます。 組み込み型については参照しやすいようにここで説明されています。
[#]_

.. % Names for built-in exceptions and functions are found in a separate
.. % symbol table.  This table is searched last when the interpreter looks
.. % up the meaning of a name, so local and global
.. % user-defined names can override built-in names.  Built-in types are
.. % described together here for easy reference.\footnote{
.. % Most descriptions sorely lack explanations of the exceptions
.. % that may be raised --- this will be fixed in a future version of
.. % this manual.}

.. index::
   pair: built-in; types
   pair: built-in; exceptions
   pair: built-in; functions
   pair: built-in; constants
   single: symbol table

この章にある表では、オペレータの優先度を昇順に並べて表わしていて、 同じ優先度のオペレータは同じ箱に入れています。同じ優先度の二項演算子は左
から右への結合順序を持っています。(単項演算子は右から左へ結合しますが選択 の余地はないでしょう。)  [#]_
オペレータの優先順位についての詳細はPython Reference Manual (XXX reference:
../ref/ref.html)の5章をごらんください。

.. % The tables in this chapter document the priorities of operators by
.. % listing them in order of ascending priority (within a table) and
.. % grouping operators that have the same priority in the same box.
.. % Binary operators of the same priority group from left to right.
.. % (Unary operators group from right to left, but there you have no real
.. % choice.)  See chapter 5 of the \citetitle[../ref/ref.html]{Python
.. % Reference Manual} for the complete picture on operator priorities.

.. rubric:: Footnotes

.. [#] ほとんどの説明ではそこで発生しうる例外については説明されていません。この マニュアルの将来の版で訂正される予定です。

.. [#] 訳者註: HTML版では、変換の過程で 表の区切り情報が消えてしまっているので、PS版やPDF版をごらんください。

