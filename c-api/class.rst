.. highlightlang:: c

.. _classobjects:

Class and Instance Objects
--------------------------

.. index:: object: class

Note that the class objects described here represent old-style classes, which
will go away in Python 3. When creating new types for extension modules, you
will want to work with type objects (section :ref:`typeobjects`).


.. ctype:: PyClassObject

   The C structure of the objects used to describe built-in classes.


.. cvar:: PyObject* PyClass_Type

   .. index:: single: ClassType (in module types)

   This is the type object for class objects; it is the same object as
   ``types.ClassType`` in the Python layer.


.. cfunction:: int PyClass_Check(PyObject *o)

   Return true if the object *o* is a class object, including instances of types
   derived from the standard class object.  Return false in all other cases.


.. cfunction:: int PyClass_IsSubclass(PyObject *klass, PyObject *base)

   Return true if *klass* is a subclass of *base*. Return false in all other cases.


.. index:: object: instance

インスタンスオブジェクト固有の関数はきわめてわずかです。


.. cvar:: PyTypeObject PyInstance_Type

   クラスインスタンスの型オブジェクトです。


.. cfunction:: int PyInstance_Check(PyObject *obj)

   *obj* がインスタンスの場合に真を返します。


.. cfunction:: PyObject* PyInstance_New(PyObject *class, PyObject *arg, PyObject *kw)

   特定クラスの新たなインスタンスを生成します。パラメタ *arg*  および *kw* はそれぞれオブジェクトのコンストラクタに渡す
   実引数およびキーワードパラメタとして使われます。


.. cfunction:: PyObject* PyInstance_NewRaw(PyObject *class, PyObject *dict)

   特定クラスの新たなインスタンスを、コンストラクタを呼ばずに生成します。 *class* は新たに作成するオブジェクトのクラスです。 *dict* パラメタは
   オブジェクトの :attr:`__dict__` に使われます; *dict* が *NULL* なら、インスタンス用に新たな辞書が作成されます。

