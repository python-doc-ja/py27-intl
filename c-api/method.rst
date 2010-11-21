.. highlightlang:: c

.. _method-objects:

メソッドオブジェクト (method object)
------------------------------------

.. index:: object: method

メソッドオブジェクトを操作する上で便利な関数がいくつかあります。


.. cvar:: PyTypeObject PyMethod_Type

   .. index:: single: MethodType (in module types)

   この :ctype:`PyTypeObject` のインスタンスは Python のメソッドオブジェクト
   型を表現します。このオブジェクトは、 ``types.MethodType``  として Python プログラムに公開されています。


.. cfunction:: int PyMethod_Check(PyObject *o)

   *o* がメソッドオブジェクト (:cdata:`PyMethod_Type` 型である) 場合に真を返します。パラメタは *NULL* にできません。


.. cfunction:: PyObject* PyMethod_New(PyObject *func, PyObject *self, PyObject *class)

   任意の呼び出し可能オブジェクト *func* を使った新たなメソッドオブジェクトを返します; 関数 *func* は、メソッドが呼び出された
   時に呼び出されるオブジェクトです。このメソッドをインスタンスに束縛 (bind) したい場合、 *self* をインスタンス自体にして、 *class*
   を *self* のクラスにしなければなりません。それ以外の場合は *self* を *NULL* に、 *class* を
   非束縛メソッドを提供しているクラスにしなければなりません。


.. cfunction:: PyObject* PyMethod_Class(PyObject *meth)

   メソッドオブジェクト *meth* を生成したクラスオブジェクトを返します; インスタンスがメソッドオブジェクトを生成した場合、戻り値は
   インスタンスのクラスになります。


.. cfunction:: PyObject* PyMethod_GET_CLASS(PyObject *meth)

   :cfunc:`PyMethod_Class` をマクロで実装したバージョンで、エラーチェックを行いません。


.. cfunction:: PyObject* PyMethod_Function(PyObject *meth)

   *meth* に関連付けられている関数オブジェクトを返します。


.. cfunction:: PyObject* PyMethod_GET_FUNCTION(PyObject *meth)

   :cfunc:`PyMethod_Function` のマクロ版で、エラーチェックを行いません。


.. cfunction:: PyObject* PyMethod_Self(PyObject *meth)

   *meth* が束縛メソッドの場合には、メソッドに関連付けられているインスタンスを返します。それ以外の場合には *NULL* を返します。


.. cfunction:: PyObject* PyMethod_GET_SELF(PyObject *meth)

   :cfunc:`PyMethod_Self` のマクロ版で、エラーチェックを行いません。


