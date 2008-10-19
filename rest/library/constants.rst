
組み込み定数
======

組み込み空間には少しだけ定数があります。以下にそれらの定数を示します:


.. data:: False

   :class:`bool` 型における、偽を表す値です。

   .. versionadded:: 2.3


.. data:: True

   :class:`bool` 型における、真を表す値です。

   .. versionadded:: 2.3


.. data:: None

   ``types.NoneType`` の唯一の値です。 ``None`` は、例えば関数にデフォルトの値が渡されないときのように、
   値がないことを表すためにしばしば用いられます。


.. data:: NotImplemented

   "特殊な比較 (rich comparison)" を行う特殊メソッド  (:meth:`__eq__`、:meth:`__lt__`、およびその仲間)
   に対して、 他の型に対しては比較が実装されていないことを示すために返される値です。


.. data:: Ellipsis

   拡張スライス文と同時に用いられる特殊な値です。

   .. % XXX Someone who understands extended slicing should fill in here.

