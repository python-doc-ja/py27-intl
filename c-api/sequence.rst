.. highlightlang:: c

.. _sequence:

シーケンス型プロトコル (sequence protocol)
==========================================


.. cfunction:: int PySequence_Check(PyObject *o)

   オブジェクトがシーケンス型プロトコルを提供している場合に ``1`` を返し、そうでないときには ``0`` を返します。この関数呼び出しは常に成功します。


.. cfunction:: Py_ssize_t PySequence_Size(PyObject *o)
               Py_ssize_t PySequence_Length(PyObject *o)

   .. index:: builtin: len

   成功するとシーケンス *o* 中のオブジェクトの数を返し、失敗すると ``-1`` を返します。
   シーケンス型プロトコルをサポートしないオブジェクトに対しては、 Python の式 ``len(o)`` と同じになります。

   .. versionchanged:: 2.5
      これらの関数は以前は :ctype:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: Py_ssize_t PySequence_Length(PyObject *o)

   :cfunc:`PySequence_Size` の別名です。


.. cfunction:: PyObject* PySequence_Concat(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の連結 (concatenation) を返し、失敗すると *NULL* を返します。
   Python の式 ``o1 + o2`` と同じです。


.. cfunction:: PyObject* PySequence_Repeat(PyObject *o, Py_ssize_t count)

   成功するとオブジェクト *o* の *count* 回繰り返しを返し、失敗すると *NULL* を返します。
   Python の式 ``o * count`` と同じです。


.. cfunction:: PyObject* PySequence_InPlaceConcat(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の連結 (concatenation) を返し、失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の式 ``o1 += o2`` と同じです。


.. cfunction:: PyObject* PySequence_InPlaceRepeat(PyObject *o, Py_ssize_t count)

   成功するとオブジェクト *o* の *count* 回繰り返しを返し、失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の式 ``o *= count`` と同じです。

   .. versionchanged:: 2.5
      この関数は以前は *count* の型に :ctype:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. cfunction:: PyObject* PySequence_GetItem(PyObject *o, Py_ssize_t i)

   成功すると *o* の *i* 番目の要素を返し、失敗すると *NULL* を返します。
   Python の式 ``o[i]`` と同じです。

   .. versionchanged:: 2.5
      この関数は以前は *i* の型に :ctype:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. cfunction:: PyObject* PySequence_GetSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2)

   成功すると *o* の *i1* から *i2* までの間のスライスを返し、失敗すると *NULL* を返します。 Python の式 ``o[i1:i2]``
   と同じです。

   .. versionchanged:: 2.5
      この関数は以前は *i1*, *i2* の型に :ctype:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: int PySequence_SetItem(PyObject *o, int Py_ssize_t, PyObject *v)

   *o* の *i* 番目の要素に *v* を代入します。失敗すると ``-1`` を返します。 Python の文 ``o[i] = v`` と同じです。
   この関数は *v* への参照を盗み取り *ません* 。

   .. versionchanged:: 2.5
      この関数は以前は *i* の型に :ctype:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: int PySequence_DelItem(PyObject *o, Py_ssize_t i)

   *o* の *i* 番目の要素を削除します。失敗すると ``-1`` を返します。 Python の文 ``del o[i]`` と同じです。

   .. versionchanged:: 2.5
      この関数は以前は *i* の型に :ctype:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: int PySequence_SetSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2, PyObject *v)

   *o* の *i1* から *i2* までの間のスライスに *v* を代入します。 Python の文 ``o[i1:i2] = v`` と同じです。

   .. versionchanged:: 2.5
      この関数は以前は *i1*, *i2* の型に :ctype:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: int PySequence_DelSlice(PyObject *o, int Py_ssize_t, int Py_ssize_t)

   シーケンスオブジェクト *o* の *i1* から *i2* までの間のスライスを削除します。失敗すると ``-1`` を返します。 Python の文
   ``del o[i1:i2]`` と同じです。

   .. versionchanged:: 2.5
      この関数は以前は *i1*, *i2* の型に :ctype:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: int PySequence_Count(PyObject *o, PyObject *value)

   *o* における *value* の出現回数、すなわち  ``o[key] == value`` となる *key* の個数を返します。失敗すると
   ``-1`` を返します。 Python の式 ``o.count(value)`` と同じです。

   .. versionchanged:: 2.5
      この関数は以前は :ctype:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: int PySequence_Contains(PyObject *o, PyObject *value)

   *o* に *value* が入っているか判定します。 *o* のある要素が *value* と等価 (equal) ならば ``1`` を
   返し、それ以外の場合には ``0`` を返します。エラーが発生すると ``-1`` を返します。 Python の式 ``value in o``
   と同じです。


.. cfunction:: int PySequence_Index(PyObject *o, PyObject *value)

   ``o[i] == value`` となる最初に見つかったインデクス *i* を返します。エラーが発生すると ``-1`` を返します。 Python の式
   ``o.index(value)`` と同じです。

   .. versionchanged:: 2.5
      この関数は以前は :ctype:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: PyObject* PySequence_List(PyObject *o)

   任意のシーケンス *o* と同じ内容を持つリストオブジェクトを返します。返されるリストは必ず新しいリストオブジェクトになります。


.. cfunction:: PyObject* PySequence_Tuple(PyObject *o)

   .. index:: builtin: tuple

   任意のシーケンス *o* と同じ内容を持つタプルオブジェクトを返します。失敗したら *NULL* を返します。 *o* がタプルの場合、新たな参照を返します。
   それ以外の場合、適切な内容が入ったタプルを構築して返します。 Pythonの式 ``tuple(o)`` と同じです。


.. cfunction:: PyObject* PySequence_Fast(PyObject *o, const char *m)

   シーケンス *o* がすでにタプルやリストであれば *o* を返し、そうでなければ *o* をタプルで返します。返されるタプルのメンバにアクセスするには
   :cfunc:`PySequence_Fast_GET_ITEM` を使ってください。失敗すると *NULL* を返します。
   オブジェクトがシーケンスでなければ、 *m* がメッセージテキストになっている :exc:`TypeError` を送出します。


.. cfunction:: PyObject* PySequence_Fast_GET_ITEM(PyObject *o, Py_ssize_t i)

   *o* が *NULL* でなく、 :cfunc:`PySequence_Fast` が返したオブジェクトであり、かつ *i* がインデクスの範囲内にあると
   仮定して、 *o* の *i* 番目の要素を返します。

   .. versionchanged:: 2.5
      この関数は以前は *i* の型に :ctype:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: PyObject** PySequence_Fast_ITEMS(PyObject *o)

   PyObject ポインタの背後にあるアレイを返します．
   この関数では， *o* は :cfunc:`PySequence_Fast` の返したオブジェクトであり，
   *NULL* でないものと仮定しています．

   リストのサイズが変更されるとき、メモリ再確保が要素の配列を再配置するかもしれない
   ことに注意してください。そのため、シーケンスの変更が発生しないコンテキストでのみ
   背後にあるポインターを使ってください。

   .. versionadded:: 2.4


.. cfunction:: PyObject* PySequence_ITEM(PyObject *o, Py_ssize_t i)

   成功すると the *i* th element of *o* を返し、失敗すると *NULL* を返します。
   :cfunc:`PySequence_GetItem` ですが、 :cfunc:`PySequence_Check(o)` が真になるかチェックせず、
   負のインデクスに対する調整を行いません。

   .. versionadded:: 2.3

   .. versionchanged:: 2.5
      この関数は以前は *i* の型に :ctype:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: int PySequence_Fast_GET_SIZE(PyObject *o)

   *o* が *NULL* でなく、 :cfunc:`PySequence_Fast` が返したオブジェクトであると仮定して、 *o* の長さを返します。 *o*
   のサイズは :cfunc:`PySequence_Size` を呼び出しても得られますが、 :cfunc:`PySequence_Fast_GET_SIZE`
   の方が *o* をリストかタプルであると仮定して処理するため、より高速です。
