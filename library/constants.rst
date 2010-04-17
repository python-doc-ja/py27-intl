
組み込み定数
============

組み込み空間には少しだけ定数があります。以下にそれらの定数を示します。:


.. data:: False

   :class:`bool` 型における、偽を表す値です。

   .. versionadded:: 2.3


.. data:: True

   :class:`bool` 型における、真を表す値です。

   .. versionadded:: 2.3


.. data:: None

   :attr:`types.NoneType` の唯一の値です。 ``None`` は、例えば関数にデ
   フォルトの値が渡されないときのように、値がないことを表すためにしば
   しば用いられます。

   .. versionchanged:: 2.4
      ``None`` に対する割り当ては不正であり、 :exc:`SyntaxError` を送
      出します。


.. data:: NotImplemented

   "特殊な比較 (rich comparison)" を行う特殊メソッド (:meth:`__eq__`,
   :meth:`__lt__`, およびその仲間) に対して、他の型に対しては比較が実
   装されていないことを示すために返される値です。

matsue
.. data:: Ellipsis

   拡張スライス文と同時に用いられる特殊な値です。

   .. XXX Someone who understands extended slicing should fill in here.


.. data:: __debug__

   この定数は Python が :option:`-O` オプションを付して開始されていな
   いときに真となります。
   :const:`__debug__` に対しての代入は不正であり、 :exc:`SyntaxError`
   を送出します。
   :keyword:`assert` ステートメントも参照下さい。


Constants added by the :mod:`site` module
-----------------------------------------

:mod:`site` モジュール (コマンドラインオプションとして :option:`-S` が
指定されない限り、開始時に自動的にインポートされます) はいくつかの定数
を組み込みの名前空間に追加します。それらは対話的インタープリタシェルに
とって有用であり、プログラムから使うべきではありません。

.. data:: quit([code=None])
          exit([code=None])

   オブジェクトは、画面出力されたとき、 "Use quit() or Ctrl-D
   (i.e. EOF) to exit" のような画面出力をだします。呼び出されたときには、
   :exc:`SystemExit` を送出し、特定の終了コードで終了します。

.. data:: copyright
          license
          credits

   オブジェクトは、画面出力されたとき、 "Type license() to see the
   full license text" のような画面出力をだします。呼び出されたときには、
   それぞれのテキストをページャのような形式 (1画面分づつ) で表示します。
