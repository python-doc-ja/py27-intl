
:mod:`token` --- Python解析木と共に使われる定数
===================================

.. module:: token
   :synopsis: Constants representing terminal nodes of the parse tree.
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


このモジュールは解析木の葉ノード(終端記号)の数値を表す定数を提供します。言語の文法のコンテキストにおける名前の定義については、Pythonディストリビューションのファイル:file:`Grammar/Grammar`を参照してください。名前がマップする特定の数値は、Pythonのバージョン間で変わります。

このモジュールは一つのデータオブジェクトといくつかの関数も提供します。関数はPythonのCヘッダファイルの定義を反映します。


.. data:: tok_name

   辞書はこのモジュールで定義されている定数の数値を名前の文字列へマップし、より人が読みやすいように解析木を表現します。


.. function:: ISTERMINAL(x)

   終端トークンの値に対して真を返します。


.. function:: ISNONTERMINAL(x)

   非終端トークンの値に対して真を返します。


.. function:: ISEOF(x)

   *x*が入力の終わりを示すマーカーならば、真を返します。


.. seealso::

   Module :mod:`parser`
      :mod:`parser`モジュールの二番目の例で、:mod:`symbol`モジュールの使い方を示しています。

