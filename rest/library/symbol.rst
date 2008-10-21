
:mod:`symbol` --- Python解析木と共に使われる定数
================================================

.. module:: symbol
   :synopsis: Constants representing internal nodes of the parse tree.
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


このモジュールは解析木の内部ノードの数値を表す定数を提供します。ほとんどのPython定数とは違い、これらは小文字の名前を使います。言語の文法のコンテキストにおける名前の定義については、Pythonディストリビューションのファイル:file:`Grammar/Grammar`を参照してください。名前がマップする特定の数値はPythonのバージョン間で変わります。

このモジュールには、データオブジェクトも一つ付け加えられています:


.. data:: sym_name

   ディクショナリはこのモジュールで定義されている定数の数値を名前の文字列へマップし、より人が読みやすいように解析木を表現します。


.. seealso::

   Module :mod:`parser`
      :mod:`parser`モジュールの二番目の例で、:mod:`symbol`モジュールの使い方を示しています。

