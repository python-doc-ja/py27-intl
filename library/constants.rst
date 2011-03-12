
組み込み定数
============

.. A small number of constants live in the built-in namespace.  They are:

組み込み空間には少しだけ定数があります。以下にそれらの定数を示します。:


.. data:: False

   .. The false value of the :class:`bool` type.

   :class:`bool` 型における、偽を表す値です。

   .. versionadded:: 2.3


.. data:: True

   .. The true value of the :class:`bool` type.

   :class:`bool` 型における、真を表す値です。

   .. versionadded:: 2.3


.. data:: None

   .. The sole value of :attr:`types.NoneType`.  ``None`` is frequently used to
   .. represent the absence of a value, as when default arguments are not passed to a
   .. function.

   :attr:`types.NoneType` の唯一の値です。 ``None`` は、例えば関数にデ
   フォルトの値が渡されないときのように、値がないことを表すためにしば
   しば用いられます。


   .. .. versionchanged:: 2.4
   ..    Assignments to ``None`` are illegal and raise a :exc:`SyntaxError`.

   .. versionchanged:: 2.4
      ``None`` に対する割り当ては不正であり、 :exc:`SyntaxError` を送
      出します。


.. data:: NotImplemented

   .. Special value which can be returned by the "rich comparison" special methods
   .. (:meth:`__eq__`, :meth:`__lt__`, and friends), to indicate that the comparison
   .. is not implemented with respect to the other type.

   "特殊な比較 (rich comparison)" を行う特殊メソッド (:meth:`__eq__`,
   :meth:`__lt__`, およびその仲間) に対して、他の型に対しては比較が実
   装されていないことを示すために返される値です。


.. data:: Ellipsis

   .. Special value used in conjunction with extended slicing syntax.

   拡張スライス文と同時に用いられる特殊な値です。


.. data:: __debug__

   .. This constant is true if Python was not started with an :option:`-O` option.
   .. It cannot be reassigned.  See also the :keyword:`assert` statement.

   この定数は Python が :option:`-O` オプションを付して開始されていな
   いときに真となります。
   :const:`__debug__` に対して再代入はできません。
   :keyword:`assert` ステートメントも参照下さい。


.. note::

   .. The name :data:`None` cannot be reassigned (assignments to it, even as an
   .. attribute name, raise :exc:`SyntaxError`), so it can be considered a "true"
   .. constant.

   :data:`None` という名前は再代入できないので (``None`` に対する代入は、たとえ属性名としてであっても
   :exc:`SyntaxError` が送出されます)、 ``None`` は「真の」定数であると考えることができます。


.. Constants added by the :mod:`site` module

:mod:`site` モジュールで追加される定数
-----------------------------------------

.. The :mod:`site` module (which is imported automatically during startup, except
.. if the :option:`-S` command-line option is given) adds several constants to the
.. built-in namespace.  They are useful for the interactive interpreter shell and
.. should not be used in programs.

:mod:`site` モジュール (コマンドラインオプションとして :option:`-S` が
指定されない限り、開始時に自動的にインポートされます) はいくつかの定数
を組み込みの名前空間に追加します。それらは対話的インタープリタシェルに
とって有用であり、プログラムから使うべきではありません。


.. data:: quit([code=None])
          exit([code=None])

   .. Objects that when printed, print a message like "Use quit() or Ctrl-D
   .. (i.e. EOF) to exit", and when called, raise :exc:`SystemExit` with the
   .. specified exit code.

   オブジェクトは、画面出力されたとき、 "Use quit() or Ctrl-D
   (i.e. EOF) to exit" のような画面出力をだします。呼び出されたときには、
   :exc:`SystemExit` を送出し、特定の終了コードで終了します。


.. data:: copyright
          license
          credits

   .. Objects that when printed, print a message like "Type license() to see the
   .. full license text", and when called, display the corresponding text in a
   .. pager-like fashion (one screen at a time).

   オブジェクトは、画面出力されたとき、 "Type license() to see the
   full license text" のような画面出力をだします。呼び出されたときには、
   それぞれのテキストをページャのような形式 (1画面分づつ) で表示します。
