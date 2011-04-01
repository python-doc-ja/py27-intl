.. highlightlang:: c

.. _setobjects:

集合オブジェクト (Set Objects)
------------------------------

.. sectionauthor:: Raymond D. Hettinger <python@rcn.com>


.. index::
   object: set
   object: frozenset

.. versionadded:: 2.5

このセクションでは :class:`set` と :class:`frozenset` の公開APIについて詳しく述べます。
以降で説明していない機能は、抽象オブジェクトプロトコル ( :c:func:`PyObject_CallMethod`,
:c:func:`PyObject_RichCompareBool`, :c:func:`PyObject_Hash`,
:c:func:`PyObject_Repr`, :c:func:`PyObject_IsTrue`, :c:func:`PyObject_Print`,
:c:func:`PyObject_GetIter` を含む) か抽象数値プロトコル ( :c:func:`PyNumber_Add`,
:c:func:`PyNumber_Subtract`, :c:func:`PyNumber_Or`, :c:func:`PyNumber_Xor`,
:c:func:`PyNumber_InPlaceAdd`, :c:func:`PyNumber_InPlaceSubtract`,
:c:func:`PyNumber_InPlaceOr`, :c:func:`PyNumber_InPlaceXor` を含む) を使って利用できます。


.. ctype:: PySetObject

   この :c:type:`PyObject` を継承した型は、 :class:`set` と :class:`frozenset` 両方の
   内部データを保存するのに用いられます。 :c:type:`PyDictObject`
   と同じように、小さい集合(set)に対しては(タプルのように)固定サイズであり、
   そうでない集合に対しては(リストと同じように)可変長のメモリブロックを用います。この構造体のどのフィールドも、非公開で変更される可能性があると考えて下さい。
   すべてのアクセスは、構造体の中の値を直接操作するのではなく、ドキュメントされた APIを用いて行うべきです。


.. cvar:: PyTypeObject PySet_Type

   この :c:type:`PyTypeObject` のインスタンスは、Pythonの :class:`set` 型を表します。


.. cvar:: PyTypeObject PyFrozenSet_Type

   この :c:type:`PyTypeObject` のインスタンスは、Pythonの :class:`frozenset` 型を表します。

以降の型チェックマクロはすべてのPythonオブジェクトに対するポインタに対して動作します。
同様に、コンストラクタはすべてのイテレート可能なPythonオブジェクトに対して動作します。


.. c:function:: int PySet_Check(PyObject *p)

   *p* が :class:`set` かそのサブタイプのオブジェクトであるときに真を返します。

   .. versionadded:: 2.6

.. c:function:: int PyFrozenSet_Check(PyObject *p)

   *p* が :class:`frozenset` かそのサブタイプのオブジェクトであるときに
   真を返します。

   .. versionadded:: 2.6

.. c:function:: int PyAnySet_Check(PyObject *p)

   *p* が :class:`set` か :class:`frozenset` 、あるいはそのサブタイプの
   オブジェクトであれば、trueを返します。


.. c:function:: int PyAnySet_CheckExact(PyObject *p)

   *p* が :class:`set` か :class:`frozenset` のどちらかのオブジェクトであるときに true を返します。
   サブタイプのオブジェクトは含みません。


.. c:function:: int PyFrozenSet_CheckExact(PyObject *p)

   *p* が :class:`frozenset` のオブジェクトであるときに true を返します。サブタイプのオブジェクトは含みません。


.. c:function:: PyObject* PySet_New(PyObject *iterable)

   *iterable* が返すオブジェクトを含む新しい :class:`set` を返します。 *iterable* が *NULL*
   のときは、空のsetを返します。成功したら新しいsetを、失敗したら *NULL* を返します。 *iterable* がイテレート可能で無い場合は、
   :exc:`TypeError` を送出します。このコンストラクタは set をコピーするときにも使えます。 (``c=set(s)``)


.. c:function:: PyObject* PyFrozenSet_New(PyObject *iterable)

   *iterable* が返すオブジェクトを含む新しい :class:`frozenset` を返します。 *iterable* が *NULL*
   のときは、空のfrozensetを返します。 *iterable* がイテレート可能で無い場合は、 :exc:`TypeError` を送出します。

   .. versionchanged:: 2.6
      完全に新しい :class:`frozenset` オブジェクトを返すことが保証されるように
      なりました。以前は、大きさがゼロの frozenset はシングルトンでした。
      これは新しい frozenset を :meth:`PySet_Add` を使って作成するためです。

以降の関数やマクロは、 :class:`set` と :class:`frozenset` とそのサブタイプのインスタンスに対して利用できます。


.. c:function:: Py_ssize_t PySet_Size(PyObject *anyset)

   .. index:: builtin: len

   :class:`set` や :class:`frozenset` のオブジェクトの長さを返します。 ``len(anyset)`` と同じです。
   *anyset* が :class:`set` 、 :class:`frozenset` 及びそのサブタイプのオブジェクトで
   無い場合は、 :exc:`PyExc_SystemError` を送出します。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: Py_ssize_t PySet_GET_SIZE(PyObject *anyset)

   エラーチェックを行わない、 :c:func:`PySet_Size` のマクロ形式。


.. c:function:: int PySet_Contains(PyObject *anyset, PyObject *key)

   見つかったら１を、見つからなかったら0を、エラーが発生したときは-1を返します。 Pythonの :meth:`__contains__`
   メソッドと違って、この関数は非ハッシュsetを一時frozensetに自動で変換しません。
   *key* がハッシュ可能で無い場合、 :exc:`TypeError` を送出します。 *anyset* が :class:`set`,
   :class:`frozenset` 及びそのサブタイプのオブジェクトで無い場合は :exc:`PyExc_SystemError` を送出します。


.. c:function:: int PySet_Add(PyObject *set, PyObject *key)

   :class:`set` のインスタンスに *key* を追加します。 :class:`frozenset` のインスタンスに使わないで下さい。
   成功したら0を、失敗したら-1を返します。 *key* がハッシュ可能でないなら、 :exc:`TypeError` を送出します。
   setを大きくする余裕が無い場合は、 :exc:`MemoryError` を送出します。
   *set* が :class:`set` とそのサブタイプのインスタンスで無い場合は、 :exc:`SystemError` を送出します。

   .. versionchanged:: 2.6
      :class:`frozenset` やそのサブタイプのインスタンスに対して利用できる
      ようになりました。
      :c:func:`PyTuple_SetItem` のように、新しい frozenset を他のコードに渡す
      まえに内容を追加するためのに使うことができます。

以降の関数は、 :class:`set` とそのサブタイプに対して利用可能です。
:class:`frozenset` とそのサブタイプには利用できません。

.. c:function:: int PySet_Discard(PyObject *set, PyObject *key)

   見つかって削除したら1を返します。見つからなかったら何もせずに0を返します。エラーが発生したら-1を返します。
   keyが無くても :exc:`KeyError` を送出しません。 *key* がハッシュ不可能であれば :exc:`TypeError` を送出します。
   Pythonの :meth:`discard` メソッドと違って、この関数は非ハッシュsetsを一時frozensetに変換しません。
   *set* が :class:`set` とそのサブタイプのインスタンスで無いときは、 :exc:`PyExc_SystemError` を送出します。


.. c:function:: PyObject* PySet_Pop(PyObject *set)

   *set* の中の要素のどれかに対する新しい参照を返し、そのオブジェクトを *set* から削除します。失敗したら *NULL* を返します。
   setが空の場合には :exc:`KeyError` を送出します。 *set* が :class:`set` とそのサブタイプのインスタンスで無い場合は、
   :exc:`SystemError` を送出します。


.. c:function:: int PySet_Clear(PyObject *set)

   setを空にします。

