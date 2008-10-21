
:mod:`fpformat` --- 浮動小数点の変換
====================================

.. module:: fpformat
   :synopsis: 浮動小数点をフォーマットする汎用関数。
.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>


.. note::

   This module is unneeded: everything here could be done via the ``%`` string
   interpolation operator.

:mod:`fpformat` モジュールは浮動小数点数の表示を 100% 純粋に Python だけで 行うための関数を定義しています。

.. % interpolation operator:補間演算?

.. note::

   このモジュールは必要ありません: このモジュールのすべてのことは、 ``%`` を使って、文字列の補間演算により可能です。

:mod:`fpformat` モジュールは次にあげる関数と例外を定義しています。


.. function:: fix(x, digs)

   *x* を ``[-]ddd.ddd`` の形にフォーマットします。 小数点の後ろに *digs* 桁と、小数点の前に少なくとも1桁です。 ``vardigs
   <= 0`` の場合、小数点以下は切り捨てられます。  *x* は数字か数字を表した文字列です。

   .. % fix(4.5, 0) --> '4'

   *digs* は整数です。

   返り値は文字列です。


.. function:: sci(x, digs)

   *x* を ``[-]d.dddE[+-]ddd`` の形にフォーマットします。 小数点の後ろに *digs* 桁と、小数点の前に1桁だけです。

   ``vardigs <= 0`` の場合、1桁だけ残され、小数点以下は切り捨てられます。  *x* は実数か実数を表した文字列です。

   .. % fix(4.5, 0) --> '5e+000'

   *digs* は整数です。

   返り値は文字列です。


.. exception:: NotANumber

   :func:`fix` や :func:`sci` にパラメータとして渡された文字列 *x* が 数字として認識できなかった場合、例外が発生します。
   標準の例外が文字列の場合、この例外は :exc:`ValueError` のサブクラスです。 例外値は、例外を発生させた不適切にフォーマットされた文字列です。

例::

   >>> import fpformat
   >>> fpformat.fix(1.23, 1)
   '1.2'

