
:mod:`fm` --- *Font Manager* インターフェース
=====================================

.. module:: fm
   :platform: IRIX
   :synopsis: SGIワークステーションの Font Manager インターフェース。


.. index::
   single: Font Manager, IRIS
   single: IRIS Font Manager

このモジュールはIRIS *Font Manager*ライブラリへのアクセスを提供しま す。   Silicon Graphics マシン上だけで利用可能です。
次も参照してください：*4Sight User's Guide*, section 1, chapter 5:  "Using the IRIS Font
Manager"。 このモジュールは、まだ IRIS Font Managerへの完全なインターフェースではあ りません。
サポートされていない機能は次のものです： matrix operations; cache operations; character
operations（代わりに string operations を使ってく ださい）; font info のうちのいくつか; individual
glyph metrics; printer  matching。

以下の操作をサポートしています：


.. function:: init()

   関数を初期化します。 :cfunc:`fminit`を呼び出します。 この関数は :mod:`fm`モジュールを最初にインポートすると自動的に呼び出さ
   れるので、普通、呼び出す必要はありません。


.. function:: findfont(fontname)

   フォントハンドルオブジェクトを返します。 ``fmfindfont(fontname)``を呼び出します。


.. function:: enumerate()

   利用可能なフォント名のリストを返します。 この関数は:cfunc:`fmenumerate`へのインターフェースです。


.. function:: prstr(string)

   現在のフォントを使って文字列をレンダリングします（下のフォントハンドルメ ソッド:func:`setfont`を参照）。
   ``fmprstr(string)``を呼び出します。


.. function:: setpath(string)

   フォントの検索パスを設定します。 ``fmsetpath(string)``を呼び出します。 （XXX 機能しない！？！）


.. function:: fontpath()

   現在のフォント検索パスを返します。

フォントハンドルオブジェクトは以下の操作をサポートします：


.. function:: scalefont(factor)

   このフォントを拡大／縮小したハンドルを返します。 ``fmscalefont(fh, factor)``を呼び出します。


.. function:: setfont()

   このフォントを現在のフォントに設定します。 注意：フォントハンドルオブジェクトが削除されると、設定は告知なしに元に戻 ります。
   ``fmsetfont(fh)``を呼び出します。


.. function:: getfontname()

   このフォントの名前を返します。 ``fmgetfontname(fh)``を呼び出します。


.. function:: getcomment()

   このフォントに関連付けられたコメント文字列を返します。 コメント文字列が何もなければ例外を返します。 ``fmgetcomment(fh)``を呼び出します。


.. function:: getfontinfo()

   このフォントに関連したデータを含むタプルを返します。 これは``fmgetfontinfo()``へのインターフェースです。 以下の数値を含むタプルを返します：
   ``(``*printermatched*、*fixed_width*、*xorig*、 *yorig*、*xsize*、*ysize*、*height*、
   *nglyphs*``)``。


.. function:: getstrwidth(string)

   このフォントで*string*を描いたときの幅をピクセル数で返します。 ``fmgetstrwidth(fh, string)``を呼び出します。

