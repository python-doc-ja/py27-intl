.. highlightlang:: c

.. _gen-objects:

ジェネレータオブジェクト
------------------------

ジェネレータ (generator) オブジェクトは、 Python がジェネレータ型イテレータを実装するために使っているオブジェクトです。
ジェネレータオブジェクトは、通常、 :cfunc:`PyGen_New` で明示的に生成されることはなく、値を逐次生成するような関数に対してイテレーションを
行うときに生成されます。

.. % Generator Objects


.. ctype:: PyGenObject

   ジェネレータオブジェクトに使われている C 構造体です。


.. cvar:: PyTypeObject PyGen_Type

   ジェネレータオブジェクトに対応する型オブジェクトです。


.. cfunction:: int PyGen_Check(ob)

   *ob* がジェネレータオブジェクトの場合に真を返します。 *ob* が *NULL* であってはなりません。


.. cfunction:: int PyGen_CheckExact(ob)

   *ob* の型が *PyGen_Type* の場合に真を返します。 *ob* が *NULL* であってはなりません。


.. cfunction:: PyObject* PyGen_New(PyFrameObject *frame)

   *frame* オブジェクトに基づいて新たなジェネレータオブジェクトを生成して返します。この関数は *frame* への参照を盗みます。パラメタが
   *NULL* であってはなりません。

