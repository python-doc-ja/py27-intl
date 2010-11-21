.. highlightlang:: c

.. _floatobjects:

浮動小数点型オブジェクト (floating point object)
------------------------------------------------

.. index:: object: floating point


.. ctype:: PyFloatObject

   この :ctype:`PyObject` のサブタイプは Python 浮動小数点型オブジェクトを表現します。


.. cvar:: PyTypeObject PyFloat_Type

   .. index:: single: FloatType (in modules types)

   この :ctype:`PyTypeObject` のインスタンスは Python 浮動小数点型を表現します。これは
   ``float`` や ``types.FloatType`` と同じオブジェクトです。


.. cfunction:: int PyFloat_Check(PyObject *p)

   引数が :ctype:`PyFloatObject` か :ctype:`PyFloatObject` のサブタイプのときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. cfunction:: int PyFloat_CheckExact(PyObject *p)

   引数が :ctype:`PyFloatObject` 型で、かつ :ctype:`PyFloatObject` 型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyFloat_FromString(PyObject *str, char **pend)

   *str* の文字列値をもとに :ctype:`PyFloatObject` オブジェクトを生成します。失敗すると *NULL* を返します。引数
   *pend* は無視されます。この引数は後方互換性のためだけに残されています。


.. cfunction:: PyObject* PyFloat_FromDouble(double v)

   *v* から :ctype:`PyFloatObject` オブジェクトを生成して返します。失敗すると *NULL* を返します。


.. cfunction:: double PyFloat_AsDouble(PyObject *pyfloat)

   *pyfloat* の指す値を、 C の :ctype:`double` 型表現で返します。


.. cfunction:: double PyFloat_AS_DOUBLE(PyObject *pyfloat)

   *pyfloat* の指す値を、 C の :ctype:`double` 型表現で返しますが、エラーチェックを行いません。


.. cfunction:: PyObject* PyFloat_GetInfo(void)

   Return a structseq instance which contains information about the
   precision, minimum and maximum values of a float. It's a thin wrapper
   around the header file :file:`float.h`.

   .. versionadded:: 2.6


.. cfunction:: double PyFloat_GetMax(void)

   Return the maximum representable finite float *DBL_MAX* as C :ctype:`double`.

   .. versionadded:: 2.6


.. cfunction:: double PyFloat_GetMin(void)

   Return the minimum normalized positive float *DBL_MIN* as C :ctype:`double`.

   .. versionadded:: 2.6

