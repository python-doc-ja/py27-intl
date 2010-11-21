.. highlightlang:: c

.. _abstract-buffer:

バッファプロトコル (buffer protocol)
====================================


.. cfunction:: int PyObject_AsCharBuffer(PyObject *obj, const char **buffer, Py_ssize_t *buffer_len)

   文字ベースの入力として使える読み出し専用メモリ上の位置へのポインタを返します。 *obj* 引数は単一セグメントからなる
   文字バッファインタフェースをサポートしていなければなりません。成功すると ``0`` を返し、 *buffer* をメモリの位置に、  *buffer_len*
   をバッファの長さに設定します。エラーの際には  ``-1`` を返し、 :exc:`TypeError` をセットします。

   .. versionadded:: 1.6


.. cfunction:: int PyObject_AsReadBuffer(PyObject *obj, const void **buffer, Py_ssize_t *buffer_len)

   任意のデータを収めた読み出し専用のメモリ上の位置へのポインタを返します。 *obj* 引数は単一セグメントからなる読み出し可能
   バッファインタフェースをサポートしていなければなりません。成功すると ``0`` を返し、 *buffer* をメモリの位置に、  *buffer_len*
   をバッファの長さに設定します。エラーの際には  ``-1`` を返し、 :exc:`TypeError` をセットします。

   .. versionadded:: 1.6


.. cfunction:: int PyObject_CheckReadBuffer(PyObject *o)

   *o* が単一セグメントからなる読み出し可能バッファインタフェースをサポートしている場合に ``1`` を返します。それ以外の場合には ``0``
   を返します。

   .. versionadded:: 2.2


.. cfunction:: int PyObject_AsWriteBuffer(PyObject *obj, void **buffer, Py_ssize_t *buffer_len)

   書き込み可能なメモリ上の位置へのポインタを返します。 *obj*  引数は単一セグメントからなる文字バッファインタフェース
   をサポートしていなければなりません。成功すると ``0`` を返し、 *buffer* をメモリの位置に、 *buffer_len* をバッファの
   長さに設定します。エラーの際には ``-1`` を返し、 :exc:`TypeError` をセットします。

   .. versionadded:: 1.6

