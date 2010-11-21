.. highlightlang:: c


.. _concrete:

*****************************************
具象オブジェクト (concrete object) レイヤ
*****************************************

この章ではは、特定の Python オブジェクト型固有の関数について述べています。これらの関数に間違った方のオブジェクトを渡すのは良い考えであありません;
Python プログラムから何らかのオブジェクトを受け取ったとき、そのオブジェクトが正しい型になっているか確信をもてないの
なら、まず型チェックを行わなければなりません; 例えば、あるオブジェクトが辞書型か調べるには、 :cfunc:`PyDict_Check` を使います。
この章は Python のオブジェクト型における "家計図" に従って構成されています。

.. warning::

   この章で述べている関数は、渡されたオブジェクトの型を注意深くチェックしはするものの、多くの関数は渡されたオブジェクトが有効な *NULL*
   なのか有効なオブジェクトなのかをチェックしません。これらの関数に *NULL* を渡させてしまうと、関数はメモリアクセス
   違反を起こして、インタプリタを即座に終了させてしまうはずです。


.. _fundamental:

基本オブジェクト (fundamental object)
=====================================

この節では、Python の型オブジェクトと単量子 (singleton)  オブジェクト ``None`` について述べます。


.. _typeobjects:

型オブジェクト (type object)
----------------------------

.. index:: object: type


.. ctype:: PyTypeObject

   組み込み型を記述する際に用いられる、オブジェクトを表す C 構造体です。


.. cvar:: PyObject* PyType_Type

   .. index:: single: TypeType (in module types)

   型オブジェクト自身の型オブジェクトです; Python レイヤにおける ``type`` や ``types.TypeType`` と同じオブジェクトです。


.. cfunction:: int PyType_Check(PyObject *o)

   オブジェクト *o* が型オブジェクトの場合に真を返します。標準型オブジェクトから導出されたサブタイプ (subtype) のインスタンスも
   含みます。その他の場合には偽を返します。


.. cfunction:: int PyType_CheckExact(PyObject *o)

   オブジェクト *o* が型オブジェクトの場合に真を返します。標準型のサブタイプの場合は含みません。その他の場合には偽を返します。

   .. versionadded:: 2.2


.. cfunction:: int PyType_HasFeature(PyObject *o, int feature)

   型オブジェクト *o* に、型機能 *feature* が設定されている場合に真を返します。型機能は各々単一ビットのフラグで表されます。


.. cfunction:: int PyType_IS_GC(PyObject *o)

   型オブジェクトが *o* が循環参照検出をサポートしている場合に真を返します; この関数は型機能フラグ :const:`Py_TPFLAGS_HAVE_GC`
   の設定状態をチェックします。

   .. versionadded:: 2.0


.. cfunction:: int PyType_IsSubtype(PyTypeObject *a, PyTypeObject * b)

   *a* が *b* のサブタイプの場合に真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyType_GenericAlloc(PyTypeObject * type, Py_ssize_t nitems)

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyType_GenericNew(PyTypeObject * type, PyObject *args, PyObject * kwds)

   .. versionadded:: 2.2


.. cfunction:: int PyType_Ready(PyTypeObject *type)

   型オブジェクトの後始末処理 (finalize) を行います。この関数は全てのオブジェクトで初期化を完了するために呼び出されなくてはなりません。
   この関数は、基底クラス型から継承したスロットを型オブジェクトに追加する役割があります。成功した場合には ``0`` を返し、エラーの場合には ``-1``
   を返して例外情報を設定します。

   .. versionadded:: 2.2


.. _noneobject:

None オブジェクト
-----------------

.. index:: object: None

``None`` に対する :ctype:`PyTypeObject` は、 Python/C API では直接公開されていないので注意してください。
``None`` は単量子 (singleton) なので、オブジェクトのアイデンティティテスト (C では ``==``) を使うだけで十分だからです。
同じ理由から、 :cfunc:`PyNone_Check` 関数はありません。


.. cvar:: PyObject* Py_None

   Python における ``None`` オブジェクトで、値がないことを表します。このオブジェクトにはメソッドがありません。リファレンスカウントに
   ついては、このオブジェクトも他のオブジェクトと同様に扱う必要があります。


.. cmacro:: Py_RETURN_NONE

   C 関数から :cdata:`Py_None` を戻す操作を適切に行うためのマクロです。


.. _numericobjects:

数値型オブジェクト (numeric object)
===================================

.. index:: object: numeric


.. _intobjects:

(通常)整数型オブジェクト (plain integer object)
-----------------------------------------------

.. index:: object: integer


.. ctype:: PyIntObject

   この :ctype:`PyObject` のサブタイプは Python の整数型オブジェクトを表現します。


.. cvar:: PyTypeObject PyInt_Type

   .. index:: single: IntType (in modules types)

   この :ctype:`PyTypeObject` のインスタンスは Python の (長整数でない)整数型を表現します。これは
   ``int`` や ``types.IntType`` と同じオブジェクトです。


.. cfunction:: int PyInt_Check(PyObject *o)

   *o* が :cdata:`PyInt_Type` 型か :cdata:`PyInt_Type` 型のサブタイプであるときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. cfunction:: int PyInt_CheckExact(PyObject *o)

   *o* が :cdata:`PyInt_Type` 型で、かつ :cdata:`PyInt_Type` 型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyInt_FromString(char * str, char **pend, int base)

   *str* の文字列値に基づいて、新たな :ctype:`PyIntObject` または :ctype:`PyLongObject` を返します。このとき
   *base* を基数として文字列を解釈します。 *pend* が *NULL* でなければ、 `` *pend`` は * str* 中で
   数が表現されている部分以後の先頭の文字のアドレスを指しています。 *base* が ``0`` ならば、 *str* の先頭の文字列に基づいて基数を決定します:
   もし *str* が ``'0x'`` または ``'0X'`` で始まっていれば、基数に 16 を使います; *str* が ``'0'``
   で始まっていれば、基数に 8 を使います; その他の場合には基数に 10 を使います。 *base* が ``0`` でなければ、 *base* は ``2``
   以上 ``36`` 以下の数でなければなりません。先頭に空白がある場合は無視されます。数字が全くない場合、 :exc:`ValueError` が送出
   されます。使用しているマシンの :ctype:`long int` 型で表現し切れないくらい大きな数が文字列に入っており、オーバフロー警告が抑制されていれば、
   :ctype:`PyLongObject` を返します。オーバフロー警告が抑制されていなければ、 *NULL* を返します。


.. cfunction:: PyObject* PyInt_FromLong(long ival)

   *ival* の値を使って新たな整数オブジェクトを生成します。

   現在の実装では、 ``-5`` から ``256`` までの全ての整数に対する整数オブジェクトの配列を保持するようにしており、
   この範囲の数を生成すると、実際には既存のオブジェクトに対する参照が返るようになっています。従って、 ``1`` の
   値を変えることすら可能です。変えてしまった場合の Python の挙動は未定義です :-)


.. cfunction:: PyObject* PyInt_FromSsize_t(Py_ssize_t ival)

   *ival* の値を使って新たな整数オブジェクトを生成します。値が ``LONG_MAX`` を超えている場合、長整数オブジェクトを返します。

   .. versionadded:: 2.5


.. cfunction:: long PyInt_AsLong(PyObject *io)

   オブジェクトがまだ :ctype:`PyIntObject` でなければまず型キャストを試み、次にその値を返します。
   エラーが発生した場合、 ``-1`` が返されます。その時呼び出し側は、 ``PyErr_Occurred()`` を使って、エラーが発生したのか、
   単に値が-1だったのかを判断するべきです。


.. cfunction:: long PyInt_AS_LONG(PyObject *io)

   オブジェクト *io* の値を返します。エラーチェックを行いません。


.. cfunction:: unsigned long PyInt_AsUnsignedLongMask(PyObject *io)

   オブジェクトがまだ :ctype:`PyIntObject` または :ctype:`PyLongObject` で
   なければまず型キャストを試み、次にその値を :ctype:`unsigned long` 型で返します。この関数はオーバフローをチェックしません。

   .. versionadded:: 2.3


.. cfunction:: unsigned PY_LONG_LONG PyInt_AsUnsignedLongLongMask(PyObject *io)

   オブジェクトがまだ :ctype:`PyIntObject` または :ctype:`PyLongObject` で
   なければまず型キャストを試み、次にその値を :ctype:`unsigned long long` 型で返します。オーバフローをチェックしません。

   .. versionadded:: 2.3


.. cfunction:: Py_ssize_t PyInt_AsSsize_t(PyObject *io)

   オブジェクトがまだ :ctype:`PyIntObject` でなければまず型キャストを試み、次にその値を :ctype:`Py_ssize_t` 型で返します。

   .. versionadded:: 2.5


.. cfunction:: long PyInt_GetMax()

   .. index:: single: LONG_MAX

   システムの知識に基づく、扱える最大の整数値 (システムのヘッダファイルに定義されている :const:`LONG_MAX`) を返します。


.. _boolobjects:

Bool 型オブジェクト
-------------------

Python の Bool 型は整数のサブクラスとして実装されています。ブール型の値は、 :const:`Py_False` と
:const:`Py_True` の 2 つしかありません。従って、通常の生成／削除関数はブール型にはあてはまりません。
とはいえ、以下のマクロが利用できます。

.. % Boolean Objects


.. cfunction:: int PyBool_Check(PyObject *o)

   *o* が :cdata:`PyBool_Type` の場合に真を返します。

   .. versionadded:: 2.3


.. cvar:: PyObject* Py_False

   Python における ``False`` オブジェクトです。このオブジェクトはメソッドを持ちません。参照カウントの点では、他のオブジェクトと同様に扱う必要が
   あります。


.. cvar:: PyObject* Py_True

   Python における ``True`` オブジェクトです。このオブジェクトはメソッドを持ちません。参照カウントの点では、他のオブジェクトと同様に扱う必要が
   あります。


.. cmacro:: Py_RETURN_FALSE

   :const:`Py_False` に適切な参照カウントのインクリメントを行って、関数から返すためのマクロです。

   .. versionadded:: 2.4


.. cmacro:: Py_RETURN_TRUE

   :const:`Py_True` に適切な参照カウントのインクリメントを行って、関数から返すためのマクロです。

   .. versionadded:: 2.4


.. cfunction:: int PyBool_FromLong(long v)

   *v* の値に応じて :const:`Py_True` または :const:`Py_False` への新しい参照を返します。

   .. versionadded:: 2.3


.. _longobjects:

長整数型オブジェクト (long integer object)
------------------------------------------

.. index:: object: long integer


.. ctype:: PyLongObject

   この :ctype:`PyObject` のサブタイプは長整数型を表現します。


.. cvar:: PyTypeObject PyLong_Type

   .. index:: single: LongType (in modules types)

   この :ctype:`PyTypeObject` のインスタンスは Python 長整数型を表現します。これは
   ``long`` や ``types.LongType`` と同じオブジェクトです。


.. cfunction:: int PyLong_Check(PyObject *p)

   引数が :ctype:`PyLongObject` か :ctype:`PyLongObject` のサブタイプのときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. cfunction:: int PyLong_CheckExact(PyObject *p)

   引数が :ctype:`PyLongObject` 型で、かつ :ctype:`PyLongObject` 型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyLong_FromLong(long v)

   *v* から新たな :ctype:`PyLongObject` オブジェクトを生成して返します。失敗のときには *NULL* を返します。


.. cfunction:: PyObject* PyLong_FromUnsignedLong(unsigned long v)

   C の :ctype:`unsigned long` 型から新たな :ctype:`PyLongObject` オブジェクトを生成して返します。
   失敗のときには *NULL* を返します。


.. cfunction:: PyObject* PyLong_FromLongLong(PY_LONG_LONG v)

   C の :ctype:`long long` 型から新たな :ctype:`PyLongObject` オブジェクトを生成して返します。失敗のときには
   *NULL* を返します。


.. cfunction:: PyObject* PyLong_FromUnsignedLongLong(unsigned PY_LONG_LONG v)

   C の :ctype:`unsigned long long` 型から新たな :ctype:`PyLongObject`
   オブジェクトを生成して返します。失敗のときには *NULL* を返します。


.. cfunction:: PyObject* PyLong_FromDouble(double v)

   *v* の整数部から新たな :ctype:`PyLongObject` オブジェクトを生成して返します。失敗のときには *NULL* を返します。


.. cfunction:: PyObject * PyLong_FromString(char * str, char **pend, int base)

   *str* の文字列値に基づいて、新たな :ctype:`PyLongObject` を返します。このとき *base* を基数として文字列を解釈します。
   *pend* が *NULL* でなければ、 `` *pend`` は * str* 中で数が表現されている部分以後の先頭の文字のアドレスを指しています。
   *base* が ``0`` ならば、 *str* の先頭の文字列に基づいて基数を決定します: もし *str* が ``'0x'`` または ``'0X'``
   で始まっていれば、基数に 16 を使います; *str* が ``'0'`` で始まっていれば、基数に 8 を使います; その他の場合には基数に 10 を
   使います。 *base* が ``0`` でなければ、 *base* は ``2`` 以上 ``36`` 以下の数でなければなりません。先頭に空白がある場合は
   無視されます。数字が全くない場合、 :exc:`ValueError` が送出されます。


.. cfunction:: PyObject * PyLong_FromUnicode(Py_UNICODE * u, Py_ssize_t length, int base)

   Unicode の数字配列を Python の長整数型に変換します。最初のパラメタ *u* は、 Unicode 文字列の最初の文字を指し、 *length*
   には文字数を指定し、 *base* には変換時の基数を指定します。基数は範囲 [2, 36] になければなりません; 範囲外の基数を指定すると、
   :exc:`ValueError` を送出します。

   .. versionadded:: 1.6


.. cfunction:: PyObject * PyLong_FromVoidPtr(void * p)

   Python 整数型または長整数型をポインタ *p* から生成します。ポインタに入れる値は :cfunc:`PyLong_AsVoidPtr` を使って
   得られるような値です。

   .. versionadded:: 1.5.2

   .. versionchanged:: 2.5
      整数値がLONG_MAXより大きい場合は、正の長整数を返します.


.. cfunction:: long PyLong_AsLong(PyObject *pylong)

   .. index::
      single: LONG_MAX
      single: OverflowError (built-in exception)

   *pylong* の指す長整数値を、 C の :ctype:`long` 型表現で返します。 *pylong* が :const:`LONG_MAX` よりも
   大きい場合、 :exc:`OverflowError` を送出します。


.. cfunction:: unsigned long PyLong_AsUnsignedLong(PyObject *pylong)

   .. index::
      single: ULONG_MAX
      single: OverflowError (built-in exception)

   *pylong* の指す長整数値を、 C の :ctype:`unsigned long` 型表現で返します。 *pylong* が
   :const:`ULONG_MAX` よりも大きい場合、 :exc:`OverflowError` を送出します。


.. cfunction:: PY_LONG_LONG PyLong_AsLongLong(PyObject *pylong)

   *pylong* の指す長整数値を、 C の :ctype:`long long` 型表現で返します。 *pylong* が :ctype:`long
   long` で表せない場合、 :exc:`OverflowError` を送出します。

   .. versionadded:: 2.2


.. cfunction:: unsigned PY_LONG_LONG PyLong_AsUnsignedLongLong(PyObject *pylong)

   *pylong* の指す値を、 C の :ctype:`unsigned long long` 型表現で返します。 *pylong* が
   :ctype:`unsigned long long` で表せない場合、正の値なら :exc:`OverflowError` を、負の値なら
   :exc:`TypeError` を送出します。

   .. versionadded:: 2.2


.. cfunction:: unsigned long PyLong_AsUnsignedLongMask(PyObject *io)

   Python 長整数値を、オーバフローチェックを行わずに C の :ctype:`unsigned long` 型表現で返します。

   .. versionadded:: 2.3


.. cfunction:: unsigned PY_LONG_LONG PyLong_AsUnsignedLongLongMask(PyObject *io)

   Python 長整数値を、オーバフローチェックを行わずに C の :ctype:`unsigned long long` 型表現で返します。

   .. versionadded:: 2.3


.. cfunction:: double PyLong_AsDouble(PyObject *pylong)

   *pylong* の指す値を、 C の :ctype:`double` 型表現で返します。 *pylong* が :ctype:`double`
   を使って近似表現できない場合、 :exc:`OverflowError` 例外を送出して ``-1.0`` を返します。


.. cfunction:: void * PyLong_AsVoidPtr(PyObject * pylong)

   Python の整数型か長整数型を指す *pylong* を、 C の :ctype:`void` ポインタに変換します。 *pylong* を変換できなければ、
   :exc:`OverflowError` を送出します。この関数は :cfunc:`PyLong_FromVoidPtr` で値を生成するときに使うような
   :ctype:`void` ポインタ型を生成できるだけです。

   .. versionadded:: 1.5.2

   .. versionchanged:: 2.5
      値が0..LONG_MAXの範囲の外だった場合、符号付き整数と符号無し整数の両方とも利用可能です.


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


.. cfunction:: PyObject * PyFloat_FromString(PyObject * str, char **pend)

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


.. _complexobjects:

浮動小数点オブジェクト (complex number object)
----------------------------------------------

.. index:: object: complex number

Python の複素数オブジェクトは、 C API 側から見ると二つの別個の型として実装されています: 一方は Python プログラムに対して公開
されている Python のオブジェクトで、他方は実際の複素数値を表現する C の構造体です。 API では、これら双方を扱う関数を提供しています。


C 構造体としての複素数
^^^^^^^^^^^^^^^^^^^^^^

複素数の C 構造体を引数として受理したり、戻り値として返したりする関数は、ポインタ渡しを行うのではなく *値渡し* を行うので注意してください。これは
API 全体を通して一貫しています。


.. ctype:: Py_complex

   Python 複素数オブジェクトの値の部分に対応する C の構造体です。複素数オブジェクトを扱うほとんどの関数は、この型の構造体を
   場合に応じて入力や出力として使います。構造体は以下のように定義されています::

      typedef struct {
         double real;
         double imag;
      } Py_complex;


.. cfunction:: Py_complex _Py_c_sum(Py_complex left, Py_complex right)

   二つの複素数の和を C の :ctype:`Py_complex` 型で返します。


.. cfunction:: Py_complex _Py_c_diff(Py_complex left, Py_complex right)

   二つの複素数の差を C の :ctype:`Py_complex` 型で返します。


.. cfunction:: Py_complex _Py_c_neg(Py_complex complex)

   複素数 *complex* の符号反転 C の :ctype:`Py_complex` 型で返します。


.. cfunction:: Py_complex _Py_c_prod(Py_complex left, Py_complex right)

   二つの複素数の積を C の :ctype:`Py_complex` 型で返します。


.. cfunction:: Py_complex _Py_c_quot(Py_complex dividend, Py_complex divisor)

   二つの複素数の商を C の :ctype:`Py_complex` 型で返します。


.. cfunction:: Py_complex _Py_c_pow(Py_complex num, Py_complex exp)

   指数 *exp* の *num* 乗を C の :ctype:`Py_complex` 型で返します。


Python オブジェクトとしての複素数型
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. ctype:: PyComplexObject

   この :ctype:`PyObject` のサブタイプは Python の複素数オブジェクトを表現します。


.. cvar:: PyTypeObject PyComplex_Type

   この :ctype:`PyTypeObject` のインスタンスは Python の複素数型を表現します。
   Pythonの ``complex`` や ``types.ComplexType`` と同じオブジェクトです。


.. cfunction:: int PyComplex_Check(PyObject *p)

   引数が :ctype:`PyComplexObject` 型か :ctype:`PyComplexObject` 型のサブタイプのときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. cfunction:: int PyComplex_CheckExact(PyObject *p)

   引数が :ctype:`PyComplexObject` 型で、かつ :ctype:`PyComplexObject` 型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyComplex_FromCComplex(Py_complex v)

   C の :ctype:`Py_complex` 型から Python の複素数値を生成します。


.. cfunction:: PyObject* PyComplex_FromDoubles(double real, double imag)

   新たな :ctype:`PyComplexObject` オブジェクトを *real* と *imag* から生成します。


.. cfunction:: double PyComplex_RealAsDouble(PyObject *op)

   *op* の実数部分を C の :ctype:`double` 型で返します。


.. cfunction:: double PyComplex_ImagAsDouble(PyObject *op)

   *op* の虚数部分を C の :ctype:`double` 型で返します。


.. cfunction:: Py_complex PyComplex_AsCComplex(PyObject *op)

   複素数値 *op* から :ctype:`Py_complex` 型を生成します。


.. _sequenceobjects:

シーケンスオブジェクト (sequence object)
========================================

.. index:: object: sequence

シーケンスオブジェクトに対する一般的な操作については前の章ですでに述べました; この節では、Python 言語にもともと備わっている
特定のシーケンスオブジェクトについて扱います。


.. _stringobjects:

文字列オブジェクト (string object)
----------------------------------

以下の関数では、文字列が渡されるはずのパラメタに非文字列が渡された場合に :exc:`TypeError` を送出します。

.. index:: object: string


.. ctype:: PyStringObject

   この :ctype:`PyObject` のサブタイプは Python の文字列オブジェクトを表現します。


.. cvar:: PyTypeObject PyString_Type

   .. index:: single: StringType (in module types)

   この :ctype:`PyTypeObject` のインスタンスは Python の文字列型を表現します; このオブジェクトは Python レイヤにおける
   ``str`` や ``types.TypeType`` と同じです。 .


.. cfunction:: int PyString_Check(PyObject *o)

   *o* が文字列型か文字列型のサブタイプであるときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. cfunction:: int PyString_CheckExact(PyObject *o)

   *o* が文字列型で、かつ文字列型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyString_FromString(const char * v)

   *v* を値に持つ文字列オブジェクトを返します。失敗すると *NULL* を返します。パラメタ *v* は *NULL* であってはなりません;
   *NULL* かどうかはチェックしません。


.. cfunction:: PyObject * PyString_FromStringAndSize(const char * v, Py_ssize_t len)

   値が *v* で長さが *len* の新たな文字列オブジェクトを返します。失敗すると *NULL* を返します。 *v* が *NULL*
   の場合、文字列の中身は未初期化の状態になります。


.. cfunction:: PyObject * PyString_FromFormat(const char * format, ...)

   C 関数 :cfunc:`printf` 形式の *format* 文字列と可変個の引数をとり、書式化済みの文字列長を計算した上で、書式化を行った結果を
   値とする Python 文字列にして返します。可変個の引数部は C のデータ型でなくてはならず、かつ *format* 文字列内の書式指定文字 (format
   character) に一致する型でなくてはなりません。利用できる書式化文字は以下の通りです:

   .. % This should be exactly the same as the table in PyErr_Format.
   .. % One should just refer to the other.
   .. % The descriptions for %zd and %zu are wrong, but the truth is complicated
   .. % because not all compilers support the %z width modifier -- we fake it
   .. % when necessary via interpolating PY_FORMAT_SIZE_T.
   .. % %u, %lu, %zu should have "new in Python 2.5" blurbs.

   +--------------+---------------+----------------------------------------------+
   | 書式指定文字 | 型            | コメント                                     |
   +==============+===============+==============================================+
   | :attr:`%%`   | *n/a*         | 文字 % のリテラル。                          |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%c`   | int           | C の整数型で表現される単一の文字。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%d`   | int           | C の ``printf("%d")`` と全く同じ。            |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%u`   | unsigned int  | C の ``printf("%u")`` と全く同じ。            |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%ld`  | long          | C の ``printf("%ld")`` と全く同じ。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%lu`  | unsigned long | C の ``printf("%lu")`` と全く同じ。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%zd`  | Py_ssize_t    | C の ``printf("%zd")`` と全く同じ。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%zu`  | size_t        | C の ``printf("%zu")`` と全く同じ。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%i`   | int           | C の ``printf("%i")`` と全く同じ。            |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%x`   | int           | C の ``printf("%x")`` と全く同じ。            |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%s`   | char\*        | null で終端された C の文字列。               |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%p`   | void\*        | C ポインタの 16                              |
   |              |               | 進表記。 ``printf("%p")``                     |
   |              |               | とほとんど同じだが、プラットフォームにおける |
   |              |               | ``printf`` の定義に関わりなく先頭にリテラル |
   |              |               | ``0x`` が付きます。                          |
   +--------------+---------------+----------------------------------------------+

   識別できない書式指定文字があった場合、残りの書式文字列はそのまま出力文字列にコピーされ、残りの引数は無視されます。


.. cfunction:: PyObject * PyString_FromFormatV(const char * format, va_list vargs)

   :func:`PyString_FromFormat` と同じです。ただし、こちらの関数は二つしか引数をとりません。


.. cfunction:: Py_ssize_t PyString_Size(PyObject *string)

   文字列オブジェクト *string* 内の文字列値の長さを返します。


.. cfunction:: Py_ssize_t PyString_GET_SIZE(PyObject *string)

   :cfunc:`PyString_Size` をマクロで実装したもので、エラーチェックを行いません。


.. cfunction:: char * PyString_AsString(PyObject * string)

   *string* の中身を NUL 文字終端された表現で返します。ポインタは *string* オブジェクトの内部バッファを指し、
   バッファのコピーを指すわけではありません。 ``PyString_FromStringAndSize(NULL, size)`` を使って
   生成した文字列でない限り、バッファ内のデータはいかなる変更もしてはなりません。この文字列をデアロケートしてはなりません。 *string* が Unicode
   オブジェクトの場合、この関数は *string* のデフォルトエンコーディング版を計算し、デフォルトエンコーディング版に対して操作を行います。
   *string* が文字列オブジェクトですらない場合、 :cfunc:`PyString_AsString` は *NULL* を返して
   :exc:`TypeError` を送出します。


.. cfunction:: char * PyString_AS_STRING(PyObject * string)

   :cfunc:`PyString_AsString` をマクロで実装したもので、エラーチェックを行いません。文字列オブジェクトだけをサポートします;
   Unicode オブジェクトを渡してはなりません。


.. cfunction:: int PyString_AsStringAndSize(PyObject *obj, char **buffer, Py_ssize_t * length)

   *obj* の中身を NUL 文字終端された表現にして、出力用の変数 *buffer* と *length* を使って返します。

   この関数は文字列オブジェクトと Unicode オブジェクトのどちらも入力として受理します。 Unicode オブジェクトの場合、オブジェクトを
   デフォルトエンコーディングでエンコードしたバージョン (default encoded version) を返します。 *length* が *NULL* の
   場合、値を返させるバッファには NUL 文字を入れてはなりません; NUL 文字が入っている場合、関数は ``-1`` を返し、
   :exc:`TypeError` を送出します。

   *buffer* は *obj* の内部文字列バッファを参照し、バッファのコピーを参照するわけではありません。
   ``PyString_FromStringAndSize(NULL, size)`` を使って生成した文字列でない限り、バッファ内のデータはいかなる変更も
   してはなりません。この文字列をデアロケートしてはなりません。

   *string* が Unicode オブジェクトの場合、この関数は *string* のデフォルトエンコーディング版を計算し、
   デフォルトエンコーディング版に対して操作を行います。 *string* が文字列オブジェクトですらない場合、
   :cfunc:`PyString_AsStringAndSize` は ``-1`` を返して :exc:`TypeError` を送出します。


.. cfunction:: void PyString_Concat(PyObject **string, PyObject * newpart)

   新しい文字列オブジェクトを *\* string * に作成し、 * newpart * の内容を * string* に追加します; 呼び出し側は新たな参照を所有
   することになります。 *string* の以前の値に対する参照は盗み取られます。新たな文字列を生成できなければ、 *string* に対する古い参照は無視され、
   *\* string * の値は * NULL* に設定されます; その際、適切な例外情報が設定されます。


.. cfunction:: void PyString_ConcatAndDel(PyObject **string, PyObject * newpart)

   新しい文字列オブジェクトを *\* string * に作成し、 * newpart * の内容を * string* に追加します。こちらのバージョンの関数は
   *newpart* への参照をデクリメントします。


.. cfunction:: int _PyString_Resize(PyObject **string, Py_ssize_t newsize)

   "変更不能" である文字列オブジェクトをサイズ変更する手段です。新たな文字列オブジェクトを作成するときにのみ使用してください;
   文字列がすでにコードの他の部分で使われているかもしれない場合には、この関数を使ってはなりません。入力する文字列オブジェクトの参照カウントが 1
   でない場合、この関数を呼び出すとエラーになります。左側値には、既存の文字列オブジェクトのアドレスを渡し (このアドレスには
   書き込み操作が起きるかもしれません)、新たなサイズを指定します。成功した場合、 *\* string* はサイズ変更された文字列オブジェクトを
   保持し、 ``0`` が返されます; *\* string* の値は、入力したときの値と異なっているかもしれません。文字列の再アロケーションに失敗した場合、
   *\* string * に入っていた元の文字列オブジェクトを解放し、 * \ *string* を *NULL* にセットし、メモリ例外をセットし、 ``-1``
   を返します。


.. cfunction:: PyObject * PyString_Format(PyObject * format, PyObject *args)

   新たな文字列オブジェクトを  *format* と *args* から生成します。 ``format % args`` と似た働きです。引数 *args*
   はタプルでなければなりません。


.. cfunction:: void PyString_InternInPlace(PyObject **string)

   引数 *\* string* をインプレースで隔離 (intern) します。引数は Python 文字列オブジェクトを指すポインタへのアドレスで
   なくてはなりません。 *\* string * と等しい、すでに隔離済みの文字列が存在する場合、そのオブジェクトを * \ *string* に設定します
   (かつ、元の文字列オブジェクトの参照カウントをデクリメントし、すでに隔離済みの文字列オブジェクトの参照カウントをインクリメントします)。 (補足:
   参照カウントについては沢山説明して来ましtが、この関数は参照カウント中立 (reference-count-neutral) と考えてください;
   この関数では、関数の呼び出し後にオブジェクトに対して参照の所有権を持てるのは、関数を呼び出す前にすでに所有権を持っていた場合に限ります。)


.. cfunction:: PyObject * PyString_InternFromString(const char * v)

   :cfunc:`PyString_FromString` と  :cfunc:`PyString_InternInPlace` を組み合わせたもので、
   隔離済みの新たな文字列オブジェクトを返すか、同じ値を持つすでに隔離済みの文字列オブジェクトに対する新たな ("所有権を得た") 参照を返します。


.. cfunction:: PyObject * PyString_Decode(const char * s, Py_ssize_t size, const char *encoding, const char * errors)

   *size* からなるエンコード済みのバッファ *s* を *encoding* の名前で登録されている codec に
   渡してデコードし、オブジェクトを生成します。 *encoding* および *errors* は組み込み関数 :func:`unicode`
   に与える同名のパラメタと同じ意味を持ちます。使用する codec の検索は、 Python の codec レジストリを使って行います。codec
   が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyString_AsDecodedObject(PyObject * str, const char *encoding, const char * errors)

   文字列オブジェクトを *encoding* の名前で登録されている codec に渡してデコードし、Python オブジェクトを返します。 *encoding*
   および *errors* は文字列型の :meth:`encode` メソッドに与える同名のパラメタと同じ意味を持ちます。使用する codec の検索は、
   Python の codec レジストリを使って行います。codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyString_Encode(const char * s, Py_ssize_t size, const char *encoding, const char * errors)

   *size* で指定されたサイズの :ctype:`char` バッファを *encoding* の名前で登録されている codec に渡してエンコードし、
   Python オブジェクトを返します。 *encoding* および *errors* は文字列型の :meth:`encode`
   メソッドに与える同名のパラメタと同じ意味を持ちます。使用する codec の検索は、 Python の codec レジストリを使って行います。codec
   が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyString_AsEncodedObject(PyObject * str, const char *encoding, const char * errors)

   エンコード名 *encoding* で登録された codec を使って文字列オブジェクトをエンコードし、その結果を Python オブジェクト
   として返します。 *encoding* および *errors* は文字列型の :meth:`encode` メソッドに与える同名のパラメタと
   同じ意味を持ちます。使用する codec の検索は、 Python の codec レジストリを使って行います。codec が例外を送出した場合には
   *NULL* を返します。


.. _unicodeobjects:

Unicode オブジェクト (Unicode object)
-------------------------------------

.. sectionauthor:: Marc-Andre Lemburg <mal@lemburg.com>


以下は Python の Unicode 実装に用いられている基本 Unicode  オブジェクト型です:

.. % --- Unicode Type -------------------------------------------------------


.. ctype:: Py_UNICODE

   この型はUnicode序数(Unicode ordinal)を保持するための基礎単位として、 Pythonが内部的に使います。
   Pythonのデフォルトのビルドでは、 :ctype:`Py_UNICODE` として16-bit型を利用し、 Unicodeの値を内部ではUCS-2で保持します。
   UCS4版のPythonをビルドすることもできます。(最近の多くのLinuxディストリビューションでは UCS4版のPythonがついてきます)
   UCS4版ビルドでは :ctype:`Py_UNICODE` に32-bit型を利用し、内部ではUnicode データをUCS4で保持します。
   :ctype:`wchar_t` が利用できて、PythonのUnicodeに関するビルドオプションと
   一致するときは、 :ctype:`Py_UNICODE` は :ctype:`wchar_t` をtypedefでエイリアス
   され、ネイティブプラットフォームに対する互換性を高めます。それ以外のすべてのプラットフォームでは、 :ctype:`Py_UNICODE` は
   :ctype:`unsigned short` (UCS2) か :ctype:`unsigned long` (UCS4) の
   typedefによるエイリアスになります。

UCS2とUCS4のPythonビルドの間にはバイナリ互換性がないことに注意してください。拡張やインタフェースを書くときには、このことを覚えておいてください。


.. ctype:: PyUnicodeObject

   この :ctype:`PyObject` のサブタイプは Unicode オブジェクトを表現します。


.. cvar:: PyTypeObject PyUnicode_Type

   この :ctype:`PyTypeObject` のインスタンスは Python の Unicode 型を表現します。
   Pythonレイヤにおける ``unicode`` や ``types.UnicodeType`` と同じオブジェクトです。

以下の API は実際には C マクロで、Unicode オブジェクト内部の読み出し専用データに対するチェックやアクセスを高速に行います:


.. cfunction:: int PyUnicode_Check(PyObject *o)

   *o* が Unicode 文字列型か Unicode 文字列型のサブタイプであるときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. cfunction:: int PyUnicode_CheckExact(PyObject *o)

   *o* が Unicode 文字列型で、かつ Unicode 文字列型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. cfunction:: Py_ssize_t PyUnicode_GET_SIZE(PyObject *o)

   オブジェクトのサイズを返します。 *o* は :ctype:`PyUnicodeObject` でなければなりません (チェックはしません)。


.. cfunction:: Py_ssize_t PyUnicode_GET_DATA_SIZE(PyObject *o)

   オブジェクトの内部バッファのサイズをバイト数で返します。 *o* は :ctype:`PyUnicodeObject` でなければなりません
   (チェックはしません)。


.. cfunction:: Py_UNICODE * PyUnicode_AS_UNICODE(PyObject * o)

   オブジェクト内部の :ctype:`Py_UNICODE` バッファへのポインタを返します。  *o* は :ctype:`PyUnicodeObject`
   でなければなりません (チェックはしません)。


.. cfunction:: const char * PyUnicode_AS_DATA(PyObject * o)

   オブジェクト内部バッファへのポインタを返します。  *o* は :ctype:`PyUnicodeObject` でなければなりません
   (チェックはしません)。

Unicode は数多くの異なる文字プロパティ (character property) を提供しています。よく使われる文字プロパティは、以下のマクロ
で利用できます。これらのマクロは Python の設定に応じて、各々 C の関数に対応付けられています。

.. % --- Unicode character properties ---------------------------------------


.. cfunction:: int Py_UNICODE_ISSPACE(Py_UNICODE ch)

   *ch* が空白文字かどうかに応じて 1 または 0 を返します。


.. cfunction:: int Py_UNICODE_ISLOWER(Py_UNICODE ch)

   *ch* が小文字かどうかに応じて 1 または 0 を返します。


.. cfunction:: int Py_UNICODE_ISUPPER(Py_UNICODE ch)

   *ch* が大文字かどうかに応じて 1 または 0 を返します。


.. cfunction:: int Py_UNICODE_ISTITLE(Py_UNICODE ch)

   *ch* がタイトルケース文字 (titlecase character) かどうかに応じて 1 または 0 を返します。


.. cfunction:: int Py_UNICODE_ISLINEBREAK(Py_UNICODE ch)

   *ch* が改行文字かどうかに応じて 1 または 0 を返します。


.. cfunction:: int Py_UNICODE_ISDECIMAL(Py_UNICODE ch)

   *ch* が 10 進の数字文字かどうかに応じて 1 または 0 を返します。


.. cfunction:: int Py_UNICODE_ISDIGIT(Py_UNICODE ch)

   *ch* が 2 進の数字文字かどうかに応じて 1 または 0 を返します。


.. cfunction:: int Py_UNICODE_ISNUMERIC(Py_UNICODE ch)

   *ch* が数字文字かどうかに応じて 1 または 0 を返します。


.. cfunction:: int Py_UNICODE_ISALPHA(Py_UNICODE ch)

   *ch* がアルファベット文字かどうかに応じて 1 または 0 を返します。


.. cfunction:: int Py_UNICODE_ISALNUM(Py_UNICODE ch)

   *ch* が英数文字かどうかに応じて 1 または 0 を返します。

以下の API は、高速に直接文字変換を行うために使われます:


.. cfunction:: Py_UNICODE Py_UNICODE_TOLOWER(Py_UNICODE ch)

   *ch* を小文字に変換したものを返します。


.. cfunction:: Py_UNICODE Py_UNICODE_TOUPPER(Py_UNICODE ch)

   *ch* を大文字に変換したものを返します。


.. cfunction:: Py_UNICODE Py_UNICODE_TOTITLE(Py_UNICODE ch)

   *ch* をタイトルケース文字に変換したものを返します。


.. cfunction:: int Py_UNICODE_TODECIMAL(Py_UNICODE ch)

   *ch* を 10 進の正の整数に変換したものを返します。不可能ならば ``-1`` を返します。このマクロは例外を送出しません。


.. cfunction:: int Py_UNICODE_TODIGIT(Py_UNICODE ch)

   *ch* を一桁の 2 進整数に変換したものを返します。不可能ならば ``-1`` を返します。このマクロは例外を送出しません。


.. cfunction:: double Py_UNICODE_TONUMERIC(Py_UNICODE ch)

   *ch* を :ctype:`double` に変換したものを返します。不可能ならば ``-1.0`` を返します。このマクロは例外を送出しません。

Unicode オブジェクトを生成したり、Unicode のシーケンスとしての基本的なプロパティにアクセスしたりするには、以下の API を使ってください:

.. % --- Plain Py_UNICODE ---------------------------------------------------


.. cfunction:: PyObject * PyUnicode_FromUnicode(const Py_UNICODE * u, Py_ssize_t size)

   *size* で指定された長さを持つ Py_UNICODE 型バッファ *u*  から Unicode オブジェクトを生成します。 *u* を *NULL*
   にしてもよく、その場合オブジェクトの内容は未定義です。バッファに必要な情報を埋めるのはユーザの責任です。バッファの内容は新たなオブジェクトに
   コピーされます。バッファが *NULL* でない場合、戻り値は共有されたオブジェクトになることがあります。従って、この関数が返す Unicode
   オブジェクトを変更してよいのは *u* が *NULL* のときだけです。


.. cfunction:: Py_UNICODE * PyUnicode_AsUnicode(PyObject * unicode)

   Unicode オブジェクトの内部バッファ :ctype:`Py_UNICODE` に対する読み出し専用のポインタを返します。 *unicode* が
   Unicode オブジェクトでなければ *NULL* を返します。


.. cfunction:: Py_ssize_t PyUnicode_GetSize(PyObject *unicode)

   Unicode オブジェクトの長さを返します。


.. cfunction:: PyObject * PyUnicode_FromEncodedObject(PyObject * obj, const char *encoding, const char * errors)

   あるエンコード方式でエンコードされたオブジェクト *obj* を Unicode オブジェクトに型強制して、参照カウントをインクリメントして返します。

   型強制は以下のようにして行われます:

   文字列やその他の char バッファ互換オブジェクトの場合、オブジェクトは *encoding* に従ってデコードされます。このとき *error* で
   定義されたエラー処理を用います。これら二つの引数は *NULL* にでき、その場合デフォルト値が使われます (詳細は次の節を参照してください)

   その他のUnicodeオブジェクトを含むオブジェクトは :exc:`TypeError` 例外を引き起こします。

   この API は、エラーが生じたときには *NULL* を返します。呼び出し側は返されたオブジェクトを decref する責任があります。


.. cfunction:: PyObject * PyUnicode_FromObject(PyObject * obj)

   ``PyUnicode_FromEncodedObject(obj, NULL, "strict")`` を行うショートカットで、インタプリタは Unicode
   への型強制が必要な際に常にこの関数を使います。

プラットフォームで :ctype:`wchar_t` がサポートされていて、かつ wchar.h が提供されている場合、Python は以下の関数を使って
:ctype:`wchar_t` に対するインタフェースを確立することがあります。このサポートは、Python 自体の :ctype:`Py_UNICODE`
型がシステムの :ctype:`wchar_t` と同一の場合に最適化をもたらします。

.. % --- wchar_t support for platforms which support it ---------------------


.. cfunction:: PyObject * PyUnicode_FromWideChar(const wchar_t * w, Py_ssize_t size)

   *size* の :ctype:`wchar_t` バッファ *w* から Unicode オブジェクトを生成します。失敗すると *NULL* を返します。


.. cfunction:: Py_ssize_t PyUnicode_AsWideChar(PyUnicodeObject *unicode, wchar_t * w, Py_ssize_t size)

   Unicode オブジェクトの内容を :ctype:`wchar_t` バッファ *w* にコピーします。最大で *size* 個の
   :ctype:`wchar_t` 文字を (末尾の 0-終端文字を除いて) コピーします。コピーした :ctype:`wchar_t`
   文字の個数を返します。エラーの時には -1 を返します。 :ctype:`wchar_t` 文字列は 0-終端されている場合も、されていない場合も
   あります。関数の呼び出し手の責任で、アプリケーションの必要に応じて :ctype:`wchar_t` 文字列を 0-終端してください。


.. _builtincodecs:

組み込み codec (built-in codec)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python では、処理速度を高めるために C で書かれた一そろいの codec を提供しています。これらの codec は全て以下の関数を介して
直接利用できます。

以下の API の多くが、 *encoding* と *errors* という二つの引数をとります。これらのパラメタは、組み込みの Unicode
オブジェクトコンストラクタである :func:`unicode` における同名のパラメタと同じセマンティクスになっています。

*encoding* を *NULL* にすると、デフォルトエンコーディングである ASCIIを使います。ファイルシステムに関する関数の呼び出し
では、ファイル名に対するエンコーディングとして :cdata:`Py_FileSystemDefaultEncoding` を使わねばなりません。
この変数は読み出し専用の変数として扱わねばなりません: この変数は、あるシステムによっては静的な文字列に対するポインタで
あったり、また別のシステムでは、(アプリケーションが setlocale を読んだときなどに) 変わったりもします。

*errors* で指定するエラー処理もまた、 *NULL* を指定できます。 *NULL* を指定すると、codec で定義されているデフォルト処理の使用を
意味します。全ての組み込み codec で、デフォルトのエラー処理は "strict" (:exc:`ValueError` を送出する) になっています。

個々の codec は全て同様のインタフェースを使っています。個別の codec の説明では、説明を簡単にするために以下の汎用のインタフェースとの
違いだけを説明しています。

以下は汎用 codec の API です:

.. % --- Generic Codecs -----------------------------------------------------


.. cfunction:: PyObject * PyUnicode_Decode(const char * s, Py_ssize_t size, const char *encoding, const char * errors)

   何らかのエンコード方式でエンコードされた、 *size* バイトの文字列 *s* をデコードして Unicode オブジェクトを生成します。
   *encoding* と *errors* は、組み込み関数 unicode() の同名のパラメタと同じ意味を持ちます。使用する codec の検索は、
   Python の codec レジストリを使って行います。codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_Encode(const Py_UNICODE * s, Py_ssize_t size, const char *encoding, const char * errors)

   *size* で指定されたサイズの :ctype:`Py_UNICODE` バッファをエンコードした Python 文字列オブジェクトを返します。
   *encoding* および *errors* は Unicode 型の :meth:`encode` メソッドに与える同名のパラメタと
   同じ意味を持ちます。使用する codec の検索は、 Python の codec レジストリを使って行います。codec が例外を送出した場合には
   *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_AsEncodedString(PyObject * unicode, const char *encoding, const char * errors)

   Unicode オブジェクトをエンコードし、その結果を Python 文字列オブジェクトとして返します。 *encoding* および *errors* は
   Unicode 型の :meth:`encode` メソッドに与える同名のパラメタと同じ意味を持ちます。使用する codec の検索は、 Python の
   codec レジストリを使って行います。codec が例外を送出した場合には *NULL* を返します。

以下は UTF-8 codec の APIです:

.. % --- UTF-8 Codecs -------------------------------------------------------


.. cfunction:: PyObject * PyUnicode_DecodeUTF8(const char * s, Py_ssize_t size, const char *errors)

   UTF-8 でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec が例外を送出した場合には
   *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_DecodeUTF8Stateful(const char * s, Py_ssize_t size, const char *errors, Py_ssize_t * consumed)

   *consumed* が *NULL* の場合、 :cfunc:`PyUnicode_DecodeUTF8` と同じように動作します。 *consumed* が
   *NULL* でない場合、 :cfunc:`PyUnicode_DecodeUTF8Stateful` は末尾の不完全な UTF-8 バイト列
   をエラーとみなしません。これらのバイト列はデコードされず、デコードされたバイト数を *consumed* に返します。

   .. versionadded:: 2.4


.. cfunction:: PyObject * PyUnicode_EncodeUTF8(const Py_UNICODE * s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :ctype:`Py_UNICODE` 型バッファを UTF-8 でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_AsUTF8String(PyObject * unicode)

   UTF-8 で Unicode オブジェクトをエンコードし、結果を Python 文字列オブジェクトとして返します。エラー処理は "strict" です。
   codec が例外を送出した場合には *NULL* を返します。

以下は UTF-16 codec の APIです:

.. % --- UTF-16 Codecs ------------------------------------------------------ */


.. cfunction:: PyObject * PyUnicode_DecodeUTF16(const char * s, Py_ssize_t size, const char *errors, int * byteorder)

   UTF-16 でエンコードされたバッファ *s* から *size* バイトデコードして、結果を Unicode オブジェクトで返します。 *errors*
   は (*NULL* でない場合) エラー処理方法を定義します。デフォルト値は "strict" です。

   *byteorder* が *NULL* でない場合、デコード機構は以下のように指定されたバイト整列 (byte order) に従ってデコードを開始
   します::

      *byteorder == -1: リトルエンディアン
      *byteorder == 0:  ネイティブ
      *byteorder == 1:  ビッグエンディアン

   その後、入力データ中に見つかった全てのバイト整列マーカ  (byte order mark, BOM) に従って、バイト整列を切り替えます。 BOM
   はデコード結果の Unicode 文字列中にはコピーされません。デコードを完結した後、 *\* byteorder* は入力データの終点現在に
   おけるバイト整列に設定されます。

   *byteorder* が *NULL* の場合、 codec はネイティブバイト整列のモードで開始します。

   codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_DecodeUTF16Stateful(const char * s, Py_ssize_t size, const char *errors, int * byteorder, Py_ssize_t *consumed)

   *consumed* が *NULL* の場合、 :cfunc:`PyUnicode_DecodeUTF16` と同じように動作します。 *consumed* が
   *NULL* でない場合、 :cfunc:`PyUnicode_DecodeUTF16Stateful` は末尾の不完全な UTF-16 バイト列
   (奇数長のバイト列や分割されたサロゲートペア) をエラーとみなしません。これらのバイト列はデコードされず、デコードされたバイト数を *consumed*
   に返します。

   .. versionadded:: 2.4


.. cfunction:: PyObject * PyUnicode_EncodeUTF16(const Py_UNICODE * s, Py_ssize_t size, const char *errors, int byteorder)

   *s* 中の Unicode データを UTF-16 でエンコードした結果が入っている Python 文字列オブジェクトを返します。 *byteorder* が
   ``0`` でない場合、出力は以下のバイト整列指定に従って書き出されます::

      byteorder == -1: リトルエンディアン
      byteorder == 0:  ネイティブ (BOM マーカを書き出します)
      byteorder == 1:  ビッグエンディアン

   バイトオーダが ``0`` の場合、出力結果となる文字列は常に Unicode BOM マーカ (U+FEFF) で始まります。それ以外のモードでは、 BOM
   マーカを頭につけません。

   *Py_UNICODE_WIDE* が定義されている場合、単一の :ctype:`Py_UNICODE` 値はサロゲートペアとして表現されることがあります。
   *Py_UNICODE_WIDE* が定義されていなければ、各 :ctype:`Py_UNICODE` 値は UCS-2 文字として表現されます。

   codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_AsUTF16String(PyObject * unicode)

   ネイティブバイトオーダの UTF-16 でエンコードされた Python 文字列を返します。文字列は常に BOM マーカから始まります。エラー処理は
   "strict" です。 codec が例外を送出した場合には *NULL* を返します。

以下は "Unicode Escape" codec の APIです:

.. % --- Unicode-Escape Codecs ----------------------------------------------


.. cfunction:: PyObject * PyUnicode_DecodeUnicodeEscape(const char * s, Py_ssize_t size, const char *errors)

   Unicode-Escape でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec
   が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_EncodeUnicodeEscape(const Py_UNICODE * s, Py_ssize_t size)

   *size* で指定された長さを持つ :ctype:`Py_UNICODE` 型バッファを Unicode-Escape でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_AsUnicodeEscapeString(PyObject * unicode)

   Unicode-Escape で Unicode オブジェクトをエンコードし、結果を  Python 文字列オブジェクトとして返します。エラー処理は
   "strict" です。 codec が例外を送出した場合には *NULL* を返します。

以下は "Raw Unicode Escape" codec の APIです:

.. % --- Raw-Unicode-Escape Codecs ------------------------------------------


.. cfunction:: PyObject * PyUnicode_DecodeRawUnicodeEscape(const char * s, Py_ssize_t size, const char *errors)

   Raw-Unicode-Escape でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec
   が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_EncodeRawUnicodeEscape(const Py_UNICODE * s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :ctype:`Py_UNICODE` 型バッファを Raw-Unicode-Escape でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_AsRawUnicodeEscapeString(PyObject * unicode)

   Raw-Unicode-Escape で Unicode オブジェクトをエンコードし、結果を  Python 文字列オブジェクトとして返します。エラー処理は
   "strict" です。 codec が例外を送出した場合には *NULL* を返します。

以下は Latin-1 codec の APIです: Latin-1 は、 Unicode 序数の最初の 256 個に対応し、エンコード時にはこの 256
個だけを受理します。

.. % --- Latin-1 Codecs -----------------------------------------------------


.. cfunction:: PyObject * PyUnicode_DecodeLatin1(const char * s, Py_ssize_t size, const char *errors)

   Latin-1 でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec が例外を送出した場合には
   *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_EncodeLatin1(const Py_UNICODE * s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :ctype:`Py_UNICODE` 型バッファを Latin-1 でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_AsLatin1String(PyObject * unicode)

   Latin-1 で Unicode オブジェクトをエンコードし、結果を Python 文字列オブジェクトとして返します。エラー処理は "strict" です。
   codec が例外を送出した場合には *NULL* を返します。

以下は ASCII codec の APIです: 7 ビットの ASCII データだけを受理します。その他のコードはエラーになります。

.. % --- ASCII Codecs -------------------------------------------------------


.. cfunction:: PyObject * PyUnicode_DecodeASCII(const char * s, Py_ssize_t size, const char *errors)

   ASCII でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec が例外を送出した場合には
   *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_EncodeASCII(const Py_UNICODE * s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :ctype:`Py_UNICODE` 型バッファを ASCII でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_AsASCIIString(PyObject * unicode)

   ASCII で Unicode オブジェクトをエンコードし、結果を Python 文字列オブジェクトとして返します。エラー処理は "strict" です。
   codec が例外を送出した場合には *NULL* を返します。

以下は mapping codec の APIです:

.. % --- Character Map Codecs -----------------------------------------------

この codec は、多くの様々な codec を実装する際に使われるという点で特殊な codec です (実際、 :mod:`encodings`
パッケージに入っている標準 codecs のほとんどは、この codec を使っています)。この codec は、文字のエンコードやデコードにマップ型
(mapping) を使います。

デコード用のマップ型は、文字列型の字列一組みを、 Unicode 型の字列一組、整数 (Unicode 序数として解釈されます) または ``None``
("定義されていない対応付け(undefined mapping)" を意味し、エラーを引き起こします) のいずれかに対応付けなければなりません。

デコード用のマップ型は、Unicode 型の字列一組みを、 string 型の字列一組、整数 (Latin-1 序数として解釈されます) または
``None`` ("定義されていない対応付け(undefined mapping)" を意味し、エラーを引き起こします) の
いずれかに対応付けなければなりません。

マップ型オブジェクトは、 :meth:`__getitem__` マップ型インタフェースをサポートしなければなりません。

ある文字の検索が LookupError によって失敗すると、その文字はそのままコピーされます。すなわち、その文字の序数値がそれぞれ  Unicode または
Latin-1 として解釈されます。このため、codec を実現するマップ型に入れる必要がある対応付け関係は、ある文字を別の
コード点に対応付けるものだけです。


.. cfunction:: PyObject * PyUnicode_DecodeCharmap(const char * s, Py_ssize_t size, PyObject *mapping, const char * errors)

   エンコードされた *size* バイトの文字列 *s* から  *mapping* に指定されたオブジェクトを使って Unicode オブジェクトを
   生成します。codec が例外を送出した場合には *NULL* を返します。
   もし、 *mapping* が *NULL* だった場合、latin-1でデコーディングされます。それ以外の場合では、 *mapping* はbyteに対する辞書マップ
   (訳注: sに含まれる文字のunsignedな値をint型でキーとして、値として変換対象の Unicode文字を表すUnicode文字列になっているような辞書)
   か、ルックアップテーブルとして扱われるunicode文字列です。

   文字列(訳注: mappingがunicode文字列として渡された場合)の長さより大きい byte値や、(訳注: mappingにしたがって変換した結果が)
   U+FFFE "characters" になる Byte値は、"undefined mapping" として扱われます。

   .. versionchanged:: 2.4
      mapping引数としてunicodeが使えるようになりました.


.. cfunction:: PyObject * PyUnicode_EncodeCharmap(const Py_UNICODE * s, Py_ssize_t size, PyObject *mapping, const char * errors)

   *size* で指定された長さを持つ :ctype:`Py_UNICODE` 型バッファを *mapping* に指定されたオブジェクトを使ってエンコードし、
   Python 文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_AsCharmapString(PyObject * unicode, PyObject *mapping)

   Unicode オブジェクトを *mapping* に指定されたオブジェクトを使ってエンコードし、結果を Python 文字列オブジェクトとして返します。
   エラー処理は "strict" です。 codec が例外を送出した場合には *NULL* を返します。

以下の codec API は Unicode から Unicode への対応付けを行う特殊なものです。


.. cfunction:: PyObject * PyUnicode_TranslateCharmap(const Py_UNICODE * s, Py_ssize_t size, PyObject *table, const char * errors)

   *で* 指定された長さを持つ :ctype:`Py_UNICODE` バッファを、文字変換マップ *table* を適用して変換し、変換結果を Unicode
   オブジェクトで返します。codec が例外を発行した場合には *NULL* を返します。

   対応付けを行う *table* は、 Unicode 序数を表す整数を Unicode 序数を表す整数または ``None`` に対応付けます。
   (``None`` の場合にはその文字を削除します)

   対応付けテーブルが提供する必要があるメソッドは :meth:`__getitem__` インタフェースだけです; 従って、辞書や
   シーケンス型を使ってもうまく動作します。対応付けを行っていない (:exc:`LookupError` を起こすような) 文字序数に対しては、
   変換は行わず、そのままコピーします。

以下は MBCS codec の API です。この codec は現在のところ、 Windows 上だけで利用でき、変換の実装には Win32 MBCS
変換機構 (Win32 MBCS converter) を使っています。 MBCS (または DBCS) はエンコード方式の種類 (class)
を表す言葉で、単一のエンコード方式を表すわけでなないので注意してください。利用されるエンコード方式 (target encoding) は、 codec
を動作させているマシン上のユーザ設定で定義されています。

.. % --- MBCS codecs for Windows --------------------------------------------


.. cfunction:: PyObject * PyUnicode_DecodeMBCS(const char * s, Py_ssize_t size, const char *errors)

   MBCS でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec が例外を送出した場合には
   *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_DecodeMBCSStateful(const char * s, int size, const char *errors, int * consumed)

   *consumed* が *NULL* のとき、 :cfunc:`PyUnicode_DecodeMBCS` と同じ動作をします。
   *consumed* が *NULL* でないとき、 :cfunc:`PyUnicode_DecodeMBCSStateful` は
   文字列の最後にあるマルチバイト文字の前半バイトをデコードせず、 *consumed* にデコードしたバイト数を格納します。

   .. versionadded:: 2.5


.. cfunction:: PyObject * PyUnicode_EncodeMBCS(const Py_UNICODE * s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :ctype:`Py_UNICODE` 型バッファを MBCS でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。


.. cfunction:: PyObject * PyUnicode_AsMBCSString(PyObject * unicode)

   MBCS で Unicode オブジェクトをエンコードし、結果を Python 文字列オブジェクトとして返します。エラー処理は "strict" です。
   codec が例外を送出した場合には *NULL* を返します。

.. % --- Methods & Slots ----------------------------------------------------


.. _unicodemethodsandslots:

メソッドおよびスロット関数 (slot function)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下の API は Unicode オブジェクトおよび文字列を入力に取り (説明では、どちらも文字列と表記しています)、場合に応じて Unicode
オブジェクトか整数を返す機能を持っています。

これらの関数は全て、例外が発生した場合には *NULL* または ``-1`` を返します。


.. cfunction:: PyObject * PyUnicode_Concat(PyObject * left, PyObject *right)

   二つの文字列を結合して、新たな Unicode 文字列を生成します。


.. cfunction:: PyObject * PyUnicode_Split(PyObject * s, PyObject *sep, Py_ssize_t maxsplit)

   Unicode 文字列のリストを分割して、 Unicode 文字列からなるリストを返します。 *sep* が *NULL* の場合、全ての空白文字を使って
   分割を行います。それ以外の場合、指定された文字を使って分割を行います。最大で *maxsplit* 個までの分割を行います。 *maxsplit*
   が負ならば分割数に制限を設けません。分割結果のリスト内には分割文字は含みません。


.. cfunction:: PyObject * PyUnicode_Splitlines(PyObject * s, int keepend)

   Unicode 文字列を改行文字で区切り、Unicode 文字列からなるリストを返します。CRLF は一個の改行文字とみなします。 *keepend* が 0
   の場合、分割結果のリスト内に改行文字を含めません。


.. cfunction:: PyObject * PyUnicode_Translate(PyObject * str, PyObject *table, const char * errors)

   文字列に文字変換マップ *table* を適用して変換し、変換結果を  Unicode オブジェクトで返します。

   対応付けを行う *table* は、 Unicode 序数を表す整数を Unicode 序数を表す整数または ``None`` に対応付けます。
   (``None`` の場合にはその文字を削除します)

   対応付けテーブルが提供する必要があるメソッドは :meth:`__getitem__` インタフェースだけです; 従って、辞書や
   シーケンス型を使ってもうまく動作します。対応付けを行っていない (:exc:`LookupError` を起こすような) 文字序数に対しては、
   変換は行わず、そのままコピーします。

   *errors* は codecs で通常使われるのと同じ意味を持ちます。 *errors* は *NULL* にしてもよく、デフォルトエラー処理の
   使用を意味します。


.. cfunction:: PyObject * PyUnicode_Join(PyObject * separator, PyObject *seq)

   指定した *separator* で文字列からなるシーケンスを連結 (join) し、連結結果を Unicode 文字列で返します。


.. cfunction:: int PyUnicode_Tailmatch(PyObject *str, PyObject * substr, Py_ssize_t start, Py_ssize_t end, int direction)

   *substr* が指定された末尾条件 (*direction* == -1 は前方一致、 *direction* ==1 は後方一致) で
   *str*[*start*:*end*] とマッチする場合に 1 を返し、それ以外の場合には 0 を返します。エラーが発生した時は ``-1``
   を返します。


.. cfunction:: Py_ssize_t PyUnicode_Find(PyObject *str, PyObject * substr, Py_ssize_t start, Py_ssize_t end, int direction)

   *str*[*start*:*end*] 中に *substr* が最初に出現する場所を返します。このとき指定された検索方向 *direction*
   (*direction* == 1 は順方向検索、 *direction* == -1 は逆方向検索) で検索します。戻り値は最初にマッチが見つかった場所の
   インデクスです; 戻り値 ``-1`` はマッチが見つからなかったことを表し、 ``-2`` はエラーが発生して例外情報が設定されていることを表します。


.. cfunction:: Py_ssize_t PyUnicode_Count(PyObject *str, PyObject * substr, Py_ssize_t start, Py_ssize_t end)

   ``str[start:end]`` に *substr* が重複することなく出現する回数を返します。エラーが発生した場合には ``-1`` を返します。


.. cfunction:: PyObject * PyUnicode_Replace(PyObject * str, PyObject *substr, PyObject * replstr, Py_ssize_t maxcount)

   *str* 中に出現する *substr* を最大で *maxcount* 個 *replstr* に置換し、置換結果を Unicode オブジェクトにして
   返します。 *maxcount* == -1 にすると、全ての *substr* を置換します。


.. cfunction:: int PyUnicode_Compare(PyObject *left, PyObject * right)

   二つの文字列を比較して、左引数が右引数より小さい場合、左右引数が等価の場合、左引数が右引数より大きい場合、について、それぞれ -1, 0, 1 を返します。


.. cfunction:: int PyUnicode_RichCompare(PyObject *left,  PyObject * right,  int op)

   二つのunicode文字列を比較して、下のうちの一つを返します:

* ``NULL`` を、例外が発生したときに返します。

* :const:`Py_True` もしくは :const:`Py_False` を、正しく比較できた時に返します。

* :const:`Py_NotImplemented` を、leftとrightがのどちらかに対する
     :cfunc:`PyUnicode_FromObject` が失敗したときに返します。(原文: in case the type combination is
     unknown)

     .. % 訳注: 原文が分かりにくいので翻訳者が解説しました。

   :const:`Py_EQ` と :const:`Py_NE` の比較は、引数からUnicodeへの変換が :exc:`UnicodeDecodeError`
   で失敗した時に、 :exc:`UnicodeWarning` を発生する可能性があることに注意してください。

   *op* に入れられる値は、 :const:`Py_GT`, :const:`Py_GE`, :const:`Py_EQ`, :const:`Py_NE`,
   :const:`Py_LT`, and :const:`Py_LE` のどれかです。


.. cfunction:: PyObject * PyUnicode_Format(PyObject * format, PyObject *args)

   新たな文字列オブジェクトを *format* および *args* から生成して返します; このメソッドは ``format % args``
   のようなものです。引数 *args* はタプルでなくてはなりません。


.. cfunction:: int PyUnicode_Contains(PyObject *container, PyObject * element)

   *element* が *container* 内にあるか調べ、その結果に応じて真または偽を返します。

   *element* は単要素の Unicode 文字に型強制できなければなりません。エラーが生じた場合には ``-1`` を返します。


.. _bufferobjects:

Buffer Objects
--------------

.. sectionauthor:: Greg Stein <gstein@lyra.org>


.. index::
   object: buffer
   single: buffer interface

C で実装された Python オブジェクトは、"バッファインタフェース (buffer interface)" と呼ばれる一連の
関数を公開していることがあります。これらの関数は、あるオブジェクトのデータを生 (raw) のバイト列形式で公開するために使います。
このオブジェクトの使い手は、バッファインタフェースを使うことで、オブジェクトをあらかじめコピーしておく必要なしに、オブジェクトの
データに直接アクセスできます。

バッファインタフェースをサポートするオブジェクトの例として、文字列型とアレイ (array) 型の二つがあります。文字列オブジェクトは、
その内容をバッファインタフェースのバイト単位形式で公開しています。アレイもその内容を公開していますが、注意する必要が
あるのはアレイの要素は複数バイトの値になりうる、ということです。

バッファインタフェースの使い手の一例として、ファイルオブジェクトの :meth:`write` メソッドがあります。バッファインタフェースを
介してバイト列を公開しているオブジェクトは全て、ファイルへの書き出しができます。オブジェクトのバッファインタフェースを操作し、
対象となるオブジェクトからデータを返させる  :cfunc:`PyArg_ParseTuple` には数多くのデータ書式化コードがあります。

.. index:: single: PyBufferProcs

バッファインタフェースに関するより詳しい情報は、 "バッファオブジェクト構造体" 節 ( :ref:`buffer-structs` 節) の、
:ctype:`PyBufferProcs` の説明のところにあります。

"バッファオブジェクト" はヘッダファイル :file:`bufferobject.h`  の中で定義されています (このファイルは
:file:`Python.h` がインクルードしています)。バッファオブジェクトは、 Python プログラミングの
レベルからは文字列オブジェクトと非常によく似ているように見えます: スライス、インデクス指定、結合、その他標準の文字列操作をサポート
しています。しかし、バッファオブジェクトのデータは二つのデータソース: 何らかのメモリブロックか、バッファインタフェースを公開している
別のオブジェクト、のいずれかに由来しています。

バッファオブジェクトは、他のオブジェクトのバッファインタフェースから Python プログラマにデータを公開する方法として便利です。
バッファオブジェクトはゼロコピーなスライス機構 (zero-copy slicing  mechanism) としても使われます。ブロックメモリを参照するという
バッファオブジェクトの機能を使うことで、任意のデータをきわめて簡単に Python プログラマに公開できます。メモリブロックは巨大でもかまいませんし、C
拡張モジュール内の定数配列でもかまいません。また、オペレーティングシステムライブラリ側に渡す前の、操作用の生のブロックメモリでもかまいませんし、
構造化されたデータをネイティブのメモリ配置形式でやりとりするためにも使えます。


.. ctype:: PyBufferObject

   この :ctype:`PyObject` のサブタイプはバッファオブジェクトを表現します。


.. cvar:: PyTypeObject PyBuffer_Type

   .. index:: single: BufferType (in module types)

   Python バッファ型 (buffer type) を表現する :ctype:`PyTypeObject` です; Python レイヤにおける
   ``buffer`` や ``types.BufferType`` と同じオブジェクトです。


.. cvar:: int Py_END_OF_BUFFER

   この定数は、 :cfunc:`PyBuffer_FromObject` またはの :cfunc:`PyBuffer_FromReadWriteObject`
   *size* パラメタに渡します。このパラメタを渡すと、 :ctype:`PyBufferObject` は指定された *offset*
   からバッファの終わりまでを *base* オブジェクトとして参照します。このパラメタを使うことで、関数の呼び出し側が *base* オブジェクト
   のサイズを調べる必要がなくなります。


.. cfunction:: int PyBuffer_Check(PyObject *p)

   引数が :cdata:`PyBuffer_Type` 型のときに真を返します。


.. cfunction:: PyObject * PyBuffer_FromObject(PyObject * base, Py_ssize_t offset, Py_ssize_t size)

   新たな読み出し専用バッファオブジェクトを返します。 *base* が読み出し専用バッファに必要なバッファプロトコルをサポートしていない
   場合や、厳密に一つのバッファセグメントを提供していない場合には :exc:`TypeError` を送出し、 *offset* がゼロ以下の場合には
   :exc:`ValueError` を送出します。バッファオブジェクトはは *base* オブジェクトに対する参照を保持し、バッファオブジェクトのの内容は
   *base* オブジェクトの *offset* から *size* バイトのバッファインタフェースへの参照になります。 *size* が
   :const:`Py_END_OF_BUFFER` の場合、新たに作成するバッファオブジェクトの内容は *base* から公開されているバッファの
   末尾までにわたります。


.. cfunction:: PyObject * PyBuffer_FromReadWriteObject(PyObject * base, Py_ssize_t offset, Py_ssize_t size)

   新たな書き込み可能バッファオブジェクトを返します。パラメタおよび例外は :cfunc:`PyBuffer_FromObject` と同じです。 *base*
   オブジェクトが書き込み可能バッファに必要なバッファプロトコルを公開していない場合、 :exc:`TypeError` を送出します。


.. cfunction:: PyObject * PyBuffer_FromMemory(void * ptr, Py_ssize_t size)

   メモリ上の指定された場所から指定されたサイズのデータを読み出せる、新たな読み出し専用バッファオブジェクトを返します。
   この関数が返すバッファオブジェクトが存続する間、 *ptr* で与えられたメモリバッファがデアロケートされないようにするのは呼び出し側の責任です。 *size*
   がゼロ以下の場合には :exc:`ValueError` を送出します。 *size* には :const:`Py_END_OF_BUFFER` を指定しては
   *なりません* ; 指定すると、 :exc:`ValueError` を送出します。


.. cfunction:: PyObject * PyBuffer_FromReadWriteMemory(void * ptr, Py_ssize_t size)

   :cfunc:`PyBuffer_FromMemory` に似ていますが、書き込み可能なバッファを返します。


.. cfunction:: PyObject* PyBuffer_New(Py_ssize_t size)

   *size* バイトのメモリバッファを独自に維持する新たな書き込み可能バッファオブジェクトを返します。 *size*
   がゼロまたは正の値でない場合、 :exc:`ValueError` を送出します。(:cfunc:`PyObject_AsWriteBuffer`
   が返すような) メモリバッファは特に整列されていないので注意して下さい。


.. _tupleobjects:

タプルオブジェクト (tuple object)
---------------------------------

.. index:: object: tuple


.. ctype:: PyTupleObject

   この :ctype:`PyObject` のサブタイプは Python のタプルオブジェクトを表現します。


.. cvar:: PyTypeObject PyTuple_Type

   .. index:: single: TupleType (in module types)

   この :ctype:`PyTypeObject` のインスタンスは Python のタプル型を表現します; Python レイヤにおける ``tuple``
   や ``types.TupleType``  と同じオブジェクトです。


.. cfunction:: int PyTuple_Check(PyObject *p)

   *p* がタプルオブジェクトか、タプル型のサブタイプのインスタンスである場合に真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. cfunction:: int PyTuple_CheckExact(PyObject *p)

   *p* がタプルオブジェクトで、かつタプル型のサブタイプのインスタンスでない場合に真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyTuple_New(Py_ssize_t len)

   サイズが *len* 新たなタプルオブジェクトを返します。失敗すると *NULL* を返します。


.. cfunction:: PyObject* PyTuple_Pack(Py_ssize_t n, ...)

   サイズ *n* 新たなタプルオブジェクトを返します。失敗すると *NULL* を返します。タプルの値は後続の *n* 個の Python オブジェクトを指す C
   引数になります。 ``PyTuple_Pack(2, a, b)`` は ``Py_BuildValue("(OO)", a, b)`` と同じです。

   .. versionadded:: 2.4


.. cfunction:: int PyTuple_Size(PyObject *p)

   タプルオブジェクトへのポインタを引数にとり、そのタプルのサイズを返します。


.. cfunction:: int PyTuple_GET_SIZE(PyObject *p)

   タプル *p* のサイズを返しますが、 *p* は非 *NULL* でなくてはならず、タプルオブジェクトを指していなければなりません;
   エラーチェックを行いません。


.. cfunction:: PyObject * PyTuple_GetItem(PyObject * p, Py_ssize_t pos)

   *p* の指すタプルオブジェクト内の、位置 *pos* にあるオブジェクトを返します。 *pos* が範囲を超えている場合、 *NULL* を返して
   :exc:`IndexError` 例外をセットします。


.. cfunction:: PyObject * PyTuple_GET_ITEM(PyObject * p, Py_ssize_t pos)

   :cfunc:`PyTuple_GetItem` に似ていますが、引数に対するエラーチェックを行いません。


.. cfunction:: PyObject * PyTuple_GetSlice(PyObject * p, Py_ssize_t low, Py_ssize_t high)

   *p* の指すタプルオブジェクト内の、位置 *low* から *high* までのスライスを取り出して、タプルオブジェクトとして返します。


.. cfunction:: int PyTuple_SetItem(PyObject *p, Py_ssize_t pos, PyObject * o)

   *p* の指すタプルオブジェクト内の位置 *pos* に、オブジェクト *o* への参照を挿入します。成功した場合には ``0`` を返します。

   .. note::

      この関数は *o* への参照を "盗み取り" ます。


.. cfunction:: void PyTuple_SET_ITEM(PyObject *p, Py_ssize_t pos, PyObject * o)

   :cfunc:`PyTuple_SetItem` に似ていますが、エラーチェックを行わず、新たなタプルに値を入れるとき *以外には使ってはなりません* 。

   .. note::

      この関数は *o* への参照を "盗み取り" ます。


.. cfunction:: int _PyTuple_Resize(PyObject **p, Py_ssize_t newsize)

   タプルをリサイズする際に使えます。 *newsize* はタプルの新たな長さです。タプルは変更不能なオブジェクト *ということになっている*
   ので、この関数は対象のオブジェクトに対してただ一つしか参照がない時以外には使ってはなりません。タプルがコード中の他の部分ですでに参照
   されている場合には、この関数を *使ってはなりません* 。タプルは常に指定サイズの末尾まで伸縮します。成功した場合には ``0`` を返します。
   クライアントコードは、 `` *p`` の値が呼び出し前と同じになると気体してはなりません。 ``* p`` が置き換えられた場合、オリジナルの ``*p``
   は破壊されます。失敗すると ``-1`` を返し、 `` *p`` を * NULL* に設定して、  :exc:`MemoryError` または
   :exc:`SystemError` を送出します。

   .. versionchanged:: 2.2
      使われていなかった三つ目のパラメタ、 *last_is_sticky* を削除しました.


.. _listobjects:

List Objects
------------

.. index:: object: list


.. ctype:: PyListObject

   この :ctype:`PyObject` のサブタイプは Python のリストオブジェクトを表現します。


.. cvar:: PyTypeObject PyList_Type

   .. index:: single: ListType (in module types)

   この :ctype:`PyTypeObject` のインスタンスは Python のタプル型を表現します。これは Python レイヤにおける
   ``list`` や ``types.ListType`` と同じオブジェクトです。


.. cfunction:: int PyList_Check(PyObject *p)

   引数が :ctype:`PyListObject` である場合に真を返します。


.. cfunction:: PyObject* PyList_New(Py_ssize_t len)

   サイズが *len* 新たなリストオブジェクトを返します。失敗すると *NULL* を返します。

   .. note::

      *len* が0より大きいとき、返されるリストオブジェクトの要素には ``NULL`` がセットされています。
      なので、 :cfunc:`PyList_SetItem` で本当にオブジェクトをセットする
      までは、Pythonコードにこのオブジェクトを渡したり、 :cfunc:`PySequence_SetItem` のような抽象APIを利用してはいけません。


.. cfunction:: Py_ssize_t PyList_Size(PyObject *list)

   .. index:: builtin: len

   リストオブジェクト *list* の長さを返します;  リストオブジェクトにおける ``len(list)`` と同じです。


.. cfunction:: Py_ssize_t PyList_GET_SIZE(PyObject *list)

   マクロ形式でできた :cfunc:`PyList_Size` で、エラーチェックをしません。


.. cfunction:: PyObject * PyList_GetItem(PyObject * list, Py_ssize_t index)

   *p* の指すリストオブジェクト内の、位置 *pos* にあるオブジェクトを返します。位置は正である必要があり、リスとの終端からのインデックスは
   サポートされていません。 *pos* が範囲を超えている場合、 *NULL* を返して :exc:`IndexError` 例外をセットします。


.. cfunction:: PyObject * PyList_GET_ITEM(PyObject * list, Py_ssize_t i)

   マクロ形式でできた :cfunc:`PyList_GetItem` で、エラーチェックをしません。


.. cfunction:: int PyList_SetItem(PyObject *list, Py_ssize_t index, PyObject * item)

   リストオブジェクト内の位置 *index* に、オブジェクト *item*  を挿入します。成功した場合には ``0`` を返し、失敗すると ``-1``
   を返します。

   .. note::

      この関数は *item* への参照を "盗み取り" ます。また、変更先のインデクスにすでに別の要素が入っている場合、その要素に対する参照を放棄します。


.. cfunction:: void PyList_SET_ITEM(PyObject *list, Py_ssize_t i, PyObject * o)

   :cfunc:`PyList_SetItem` をマクロによる実装で、エラーチェックを行いません。この関数は、新たなリストのまだ要素を入れたことのない
   位置に要素を入れるときにのみ使います。

   .. note::

      この関数は *item* への参照を "盗み取り" ます。また、 :cfunc:`PyList_SetItem` と違って、要素の置き換えが生じても
      置き換えられるオブジェクトへの参照を放棄 *しません* ; その結果、 *list* 中の位置 *i* で参照されていたオブジェクト
      がメモリリークを引き起こします。


.. cfunction:: int PyList_Insert(PyObject *list, Py_ssize_t index, PyObject * item)

   要素 *item* をインデクス *index* の前に挿入します。成功すると ``0`` を返します。失敗すると ``-1`` を返し、
   例外をセットします。 ``list.insert(index, item)`` に類似した機能です。


.. cfunction:: int PyList_Append(PyObject *list, PyObject * item)

   オブジェクト *item* を *list* の末尾に追加します。成功すると ``0`` を返します; 失敗すると ``-1`` を返し、
   例外をセットします。 ``list.append(item)``  に類似した機能です。


.. cfunction:: PyObject * PyList_GetSlice(PyObject * list, Py_ssize_t low, Py_ssize_t high)

   *list* 内の、 *low* から *high* の *間の* オブジェクトからなるリストを返します。失敗すると *NULL* を返し、
   例外をセットします。 ``list[low:high]`` に類似した機能です。


.. cfunction:: int PyList_SetSlice(PyObject *list, Py_ssize_t low, Py_ssize_t high, PyObject * itemlist)

   *list* 内の、 *low* から *high* の間のオブジェクトを、 *itemlist* の内容にします。 ``list[low:high] =
   itemlist`` と類似の機能です。 *itemlist* は *NULL* でもよく、空リストの代入 (指定スライスの削除) になります。
   成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。


.. cfunction:: int PyList_Sort(PyObject *list)

   *list* の内容をインプレースでソートします。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。 success, ``-1``
   on failure.   ``list.sort()`` と同じです。


.. cfunction:: int PyList_Reverse(PyObject *list)

   *list* の要素をインプレースで反転します。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。
   ``list.reverse()`` と同じです。


.. cfunction:: PyObject * PyList_AsTuple(PyObject * list)

   .. index:: builtin: tuple

   *list* の内容が入った新たなタプルオブジェクトを返します; ``tuple(list)``. と同じです。


.. _mapobjects:

マップ型オブジェクト (mapping object)
=====================================

.. index:: object: mapping


.. _dictobjects:

辞書オブジェクト (dictionary object)
------------------------------------

.. index:: object: dictionary


.. ctype:: PyDictObject

   この :ctype:`PyObject` のサブタイプは Python の辞書オブジェクトを表現します。


.. cvar:: PyTypeObject PyDict_Type

   .. index::
      single: DictType (in module types)
      single: DictionaryType (in module types)

   この :ctype:`PyTypeObject` のインスタンスは Python の辞書を表現します。このオブジェクトは、Python プログラムには
   ``dict`` および ``types.DictType`` として公開されています。


.. cfunction:: int PyDict_Check(PyObject *p)

   引数が :ctype:`PyDictObject` のときに真を返します。


.. cfunction:: int PyDict_CheckExact(PyObject *p)

   *p* が辞書型オブジェクトであり、かつ辞書型のサブクラスのインスタンスでない場合に真を返します。

   .. versionadded:: 2.4


.. cfunction:: PyObject* PyDict_New()

   *p* が辞書型オブジェクトで、かつ辞書型のサブタイプのインスタンスでない場合に真を返します。


.. cfunction:: PyObject * PyDictProxy_New(PyObject * dict)

   あるマップ型オブジェクトに対して、読み出し専用に制限されたプロキシオブジェクト (proxy object) を返します。通常、この関数は動的でないクラス型
   (non-dynamic class type) のクラス辞書を変更させないためにプロキシを作成するために使われます。

   .. versionadded:: 2.2


.. cfunction:: void PyDict_Clear(PyObject *p)

   現在辞書に入っている全てのキーと値のペアを除去して空にします。


.. cfunction:: int PyDict_Contains(PyObject *p, PyObject * key)

   辞書 *p* に *key* が入っているか判定します。 *p* の要素が *key* に一致した場合は ``1`` を返し、それ以外の場合には ``0``
   を返します。エラーの場合 ``-1`` を返します。この関数は Python の式 ``key in p`` と等価です。

   .. versionadded:: 2.4


.. cfunction:: PyObject * PyDict_Copy(PyObject * p)

   *p* と同じキーと値のペアが入った新たな辞書を返します。

   .. versionadded:: 1.6


.. cfunction:: int PyDict_SetItem(PyObject *p, PyObject * key, PyObject *val)

   辞書 *p* に、 *key* をキーとして値 *value* を挿入します。 *key* はハッシュ可能でなければなりません; ハッシュ可能でない場合、
   :exc:`TypeError` を送出します。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。


.. cfunction:: int PyDict_SetItemString(PyObject *p, const char * key, PyObject *val)

   .. index:: single: PyString_FromString()

   辞書 *p* に、 *key* をキーとして値 *value* を挿入します。 *key* は :ctype:`char\*` 型でなければなりません。
   キーオブジェクトは ``PyString_FromString(key)`` で生成されます。成功した場合には ``0`` を、失敗した場合には ``-1``
   を返します。


.. cfunction:: int PyDict_DelItem(PyObject *p, PyObject * key)

   辞書 *p* から *key* をキーとするエントリを除去します。 *key* はハッシュ可能でなければなりません;  ハッシュ可能でない場合、
   :exc:`TypeError` を送出します。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。


.. cfunction:: int PyDict_DelItemString(PyObject *p, char * key)

   辞書 *p* から文字列 *key* をキーとするエントリを除去します。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。


.. cfunction:: PyObject * PyDict_GetItem(PyObject * p, PyObject *key)

   辞書 *p* 内で *key* をキーとするオブジェクトを返します。キー *key* が存在しない場合には *NULL* を返しますが、例外をセット
   *しません* 。


.. cfunction:: PyObject * PyDict_GetItemString(PyObject * p, const char *key)

   :cfunc:`PyDict_GetItem` と同じですが、 *key* は :ctype:`PyObject\ *` ではなく :ctype:`char\* `
   で指定します。


.. cfunction:: PyObject * PyDict_Items(PyObject * p)

   辞書オブジェクトのメソッド :meth:`item` のように、辞書内の全ての要素対が入った :ctype:`PyListObject` を返します。
   (:meth:`items` については Python ライブラリリファレンス (XXX reference: ../lib/lib.html) を
   参照してください。)


.. cfunction:: PyObject * PyDict_Keys(PyObject * p)

   辞書オブジェクトのメソッド :meth:`keys` のように、辞書内の全てのキーが入った :ctype:`PyListObject` を返します。
   (:meth:`keys` については Python ライブラリリファレンス (XXX reference: ../lib/lib.html) を
   参照してください。)


.. cfunction:: PyObject * PyDict_Values(PyObject * p)

   辞書オブジェクトのメソッド :meth:`values` のように、辞書内の全ての値が入った :ctype:`PyListObject` を返します。
   (:meth:`values` については Python ライブラリリファレンス (XXX reference: ../lib/lib.html) を
   参照してください。)


.. cfunction:: Py_ssize_t PyDict_Size(PyObject *p)

   .. index:: builtin: len

   辞書内の要素の数を返します。辞書に対して ``len(p)`` を実行するのと同じです。


.. cfunction:: int PyDict_Next(PyObject *p, Py_ssize_t * ppos, PyObject **pkey, PyObject ** pvalue)

   辞書 *p* 内の全てのキー/値のペアにわたる反復処理を行います。 *ppos* が参照している :ctype:`int` 型は、この関数で反復処理
   を開始する際に、最初に関数を呼び出すよりも前に ``0`` に初期化しておかなければなりません; この関数は辞書内の各ペアを
   取り上げるごとに真を返し、全てのペアを取り上げたことが分かると偽を返します。パラメタ *pkey* および *pvalue* には、
   それぞれ辞書の各々のキーと値を指すポインタか、または *NULL* が入ります。この関数から返される参照はすべて借りた参照になります。反復処理中に
   *ppos* を変更してはなりません。この値は内部的な辞書構造体のオフセットを表現しており、構造体はスパースなので、オフセットの値に一貫性がないためです。

   以下に例を示します::

      PyObject *key, * value;
      int pos = 0;

      while (PyDict_Next(self->dict, &pos, &key, &value)) {
          / * 取り出した値で何らかの処理を行う... * /
          ...
      }

   反復処理中に辞書 *p* を変更してはなりません。 (Python 2.1 からは) 辞書を反復処理する際に、キーに対応する値を
   変更しても大丈夫になりましたが、キーの集合を変更しないことが前提です。以下に例を示します::

      PyObject *key, * value;
      int pos = 0;

      while (PyDict_Next(self->dict, &pos, &key, &value)) {
          int i = PyInt_AS_LONG(value) + 1;
          PyObject *o = PyInt_FromLong(i);
          if (o == NULL)
              return -1;
          if (PyDict_SetItem(self->dict, key, o) < 0) {
              Py_DECREF(o);
              return -1;
          }
          Py_DECREF(o);
      }


.. cfunction:: int PyDict_Merge(PyObject *a, PyObject * b, int override)

   マップ型オブジェクト *b* の全ての要素にわたって、反復的にキー/値のペアを辞書 *a* に追加します。 *b*
   は辞書か、 :func:`PyMapping_Keys` または :func:`PyObject_GetItem` をサポートする何らかのオブジェクト
   にできます。 *override* が真ならば、 *a* のキーと一致するキーが *b* にある際に、既存のペアを置き換えます。それ以外の場合は、 *b*
   のキーに一致するキーが *a* にないときのみ追加を行います。成功した場合には ``0`` を返し、例外が送出された場合には ``-1`` を返します。

   .. versionadded:: 2.2


.. cfunction:: int PyDict_Update(PyObject *a, PyObject * b)

   C で表せば ``PyDict_Merge(a, b, 1)`` と同じ、 Python で表せば ``a.update(b)`` と同じです。成功した場合には
   ``0`` を返し、例外が送出された場合には ``-1`` を返します。

   .. versionadded:: 2.2


.. cfunction:: int PyDict_MergeFromSeq2(PyObject *a, PyObject * seq2, int override)

   *seq2* 内のキー/値ペアを使って、辞書 *a* の内容を更新したり統合したりします。 *seq2* は、キー/値のペアとみなせる長さ 2 の
   反復可能オブジェクト(iterable object) を生成する反復可能オブジェクトでなければなりません。重複するキーが存在する場合、 *override*
   が真ならば先に出現したキーを使い、そうでない場合は後に出現したキーを使います。成功した場合には ``0`` を返し、例外が送出された場合には ``-1``
   を返します。

   (戻り値以外は) 等価な Python コードを書くと、以下のようになります::

      def PyDict_MergeFromSeq2(a, seq2, override):
          for key, value in seq2:
              if override or key not in a:
                  a[key] = value

   .. versionadded:: 2.2


.. _otherobjects:

その他のオブジェクト
====================


.. _fileobjects:

ファイルオブジェクト (file object)
----------------------------------

.. index:: object: file

Python の組み込みファイルオブジェクトは、全て標準 C ライブラリの :ctype:`FILE\*` サポートの上に実装されています。以下の詳細説明は
一実装に関するもので、将来の Python のリリースで変更されるかもしれません。


.. ctype:: PyFileObject

   この :ctype:`PyObject` のサブタイプは Python のファイル型オブジェクトを表現します。


.. cvar:: PyTypeObject PyFile_Type

   .. index:: single: FileType (in module types)

   この :ctype:`PyTypeObject` のインスタンスは Python のファイル型を表現します。このオブジェクトは ``file`` および
   ``types.FileType`` として Python プログラムで公開されています。


.. cfunction:: int PyFile_Check(PyObject *p)

   引数が :ctype:`PyFileObject` か :ctype:`PyFileObject` のサブタイプのときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. cfunction:: int PyFile_CheckExact(PyObject *p)

   引数が :ctype:`PyFileObject` 型で、かつ :ctype:`PyFileObject` 型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyFile_FromString(char * filename, char *mode)

   .. index:: single: fopen()

   成功すると、 *filename* に指定した名前のファイルを *mode* に指定したファイルモードで開いて得た新たなファイルオブジェクトを返します。
   *mode* のセマンティクスは標準 C ルーチン :cfunc:`fopen` と同じです。失敗すると *NULL* を返します。


.. cfunction:: PyObject * PyFile_FromFile(FILE * fp, char *name, char * mode, int (*close)(FILE*))

   すでに開かれている標準 C ファイルポインタ *fp* から新たな :ctype:`PyFileObject` を生成します。この関数で生成した
   ファイルオブジェクトは、閉じる際に *close* に指定した関数を呼び出します。失敗すると *NULL* を返します。


.. cfunction:: FILE * PyFile_AsFile(PyObject * p)

   *p* に関連付けられたファイルオブジェクトを :ctype:`FILE\*` で返します。


.. cfunction:: PyObject * PyFile_GetLine(PyObject * p, int n)

   .. index:: single: EOFError (built-in exception)

   ``p.readline([*n*])`` と同じで、この関数はオブジェクト *p* の各行を読み出します。 *p* は
   ファイルオブジェクトか、 :meth:`readline` メソッドを持つ何らかのオブジェクトでかまいません。 *n* が ``0`` の場合、
   行の長さに関係なく正確に 1 行だけ読み出します。 *n* が ``0`` より大きければ、 *n* バイト以上のデータは読み出しません;
   従って、行の一部だけが返される場合があります。どちらの場合でも、読み出し後すぐにファイルの終端に到達した場合には空文字列を返します。 *n* が ``0``
   より小さければ、長さに関わらず 1 行だけを読み出しますが、すぐにファイルの終端に到達した場合には :exc:`EOFError` を送出します。


.. cfunction:: PyObject * PyFile_Name(PyObject * p)

   *p* に指定したファイルの名前を文字列オブジェクトで返します。


.. cfunction:: void PyFile_SetBufSize(PyFileObject *p, int n)

   .. index:: single: setvbuf()

   :cfunc:`setvbuf` があるシステムでのみ利用できます。この関数を呼び出してよいのはファイルオブジェクトの生成直後のみです。


.. cfunction:: int PyFile_Encoding(PyFileObject *p, char * enc)

   Unicode オブジェクトをファイルに出力するときにのエンコード方式を *enc* にします。成功すると ``1`` を、失敗すると ``0`` を返します。

   .. versionadded:: 2.3


.. cfunction:: int PyFile_SoftSpace(PyObject *p, int newflag)

   .. index:: single: softspace (file attribute)

   この関数はインタプリタの内部的な利用のために存在します。この関数は *p* の :attr:`softspace`   属性を *newflag* に
   設定し、以前の設定値を返します。この関数を正しく動作させるために、 *p* がファイルオブジェクトである必然性はありません; 任意の
   オブジェクトをサポートします (:attr:`softspace` 属性が設定されているかどうかのみが問題だと思ってください)。
   この関数は全てのエラーを解消し、属性値が存在しない場合や属性値を取得する際にエラーが生じると、 ``0`` を以前の値として返します。
   この関数からはエラーを検出できませんが、そもそもそういう必要はありません。


.. cfunction:: int PyFile_WriteObject(PyObject *obj, PyObject * p, int flags)

   .. index:: single: Py_PRINT_RAW

   オブジェクト *obj* をファイルオブジェクト *p* に書き込みます。 *flag* がサポートするフラグは :const:`Py_PRINT_RAW`
   だけです; このフラグを指定すると、オブジェクトに :func:`repr` ではなく :func:`str` を適用した結果をファイルに書き出します。
   成功した場合には ``0`` を返し、失敗すると ``-1`` を返して適切な例外をセットします。


.. cfunction:: int PyFile_WriteString(const char *s, PyObject * p)

   文字列 *s* をファイルオブジェクト *p* に書き出します。成功した場合には ``0`` を返し、失敗すると ``-1`` を返して
   適切な例外をセットします。


.. _instanceobjects:

インスタンスオブジェクト (instance object)
------------------------------------------

.. index:: object: instance

インスタンスオブジェクト固有の関数はきわめてわずかです。


.. cvar:: PyTypeObject PyInstance_Type

   クラスインスタンスの型オブジェクトです。


.. cfunction:: int PyInstance_Check(PyObject *obj)

   *obj* がインスタンスの場合に真を返します。


.. cfunction:: PyObject * PyInstance_New(PyObject * class, PyObject *arg, PyObject * kw)

   特定クラスの新たなインスタンスを生成します。パラメタ *arg*  および *kw* はそれぞれオブジェクトのコンストラクタに渡す
   実引数およびキーワードパラメタとして使われます。


.. cfunction:: PyObject * PyInstance_NewRaw(PyObject * class, PyObject *dict)

   特定クラスの新たなインスタンスを、コンストラクタを呼ばずに生成します。 *class* は新たに作成するオブジェクトのクラスです。 *dict* パラメタは
   オブジェクトの :attr:`__dict__` に使われます; *dict* が *NULL* なら、インスタンス用に新たな辞書が作成されます。


.. _function-objects:

関数オブジェクト (Function Objects)
-----------------------------------

.. index:: object: function

Pythonの関数にはいくつかの種類があります。


.. ctype:: PyFunctionObject

   関数に使われるCの構造体


.. cvar:: PyTypeObject PyFunction_Type

   .. index:: single: MethodType (in module types)

   :ctype:`PyTypeObject` 型のインスタンスで、 Python の関数型を表します。これは Python プログラムに
   ``types.FunctionType`` として公開されます。


.. cfunction:: int PyFunction_Check(PyObject *o)

   *o* が関数オブジェクト (:cdata:`PyFunction_Type` を持っている) なら true を返します。引数は *NULL*
   であってはいけません。


.. cfunction:: PyObject * PyFunction_New(PyObject * code, PyObject *globals)

   コードオブジェクト *code* に関連付けられた新しい関数オブジェクトを返します。 *globals*
   はこの関数からアクセスできるグローバル変数の辞書でなければなりません。

   関数のドキュメント文字列、名前および *__module__* はコードオブジェクトから取得されます。引数のデフォルト値やクロージャは *NULL*
   にセットされます。


.. cfunction:: PyObject * PyFunction_GetCode(PyObject * op)

   関数オブジェクト *op* に関連付けられたコードオブジェクトを返します。


.. cfunction:: PyObject * PyFunction_GetGlobals(PyObject * op)

   関数オブジェクト *op* に関連付けられたglobals辞書を返します。


.. cfunction:: PyObject * PyFunction_GetModule(PyObject * op)

   関数オブジェクト *op* の *__module__* 属性を返します。　これは普通はモジュール名の文字列が入っていますが、Python コードから
   他のオブジェクトをセットされることもあります。


.. cfunction:: PyObject * PyFunction_GetDefaults(PyObject * op)

   関数オブジェクト *op* の引数のデフォルト値を返します。引数のタプルか *NULL* になります。


.. cfunction:: int PyFunction_SetDefaults(PyObject *op, PyObject * defaults)

   関数オブジェクト *op* の引数のデフォルト値を設定します。 *defaults* は *Py_None* かタプルでなければいけません。

   失敗した時は、 :exc:`SystemError` を発生し、 ``-1`` を返します。


.. cfunction:: PyObject * PyFunction_GetClosure(PyObject * op)

   関数オブジェクト *op* に設定されたクロージャを返します。 *NULL* か cell オブジェクトのタプルです。


.. cfunction:: int PyFunction_SetClosure(PyObject *op, PyObject * closure)

   関数オブジェクト *op* にクロージャを設定します。 *closure* は、 *Py_None* もしくは cell
   オブジェクトのタプルでなければなりません。

   失敗した時は、 :exc:`SystemError` を送出し、 ``-1`` を返します。


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


.. cfunction:: PyObject * PyMethod_New(PyObject * func, PyObject *self, PyObject * class)

   任意の呼び出し可能オブジェクト *func* を使った新たなメソッドオブジェクトを返します; 関数 *func* は、メソッドが呼び出された
   時に呼び出されるオブジェクトです。このメソッドをインスタンスに束縛 (bind) したい場合、 *self* をインスタンス自体にして、 *class*
   を *self* のクラスにしなければなりません。それ以外の場合は *self* を *NULL* に、 *class* を
   非束縛メソッドを提供しているクラスにしなければなりません。


.. cfunction:: PyObject * PyMethod_Class(PyObject * meth)

   メソッドオブジェクト *meth* を生成したクラスオブジェクトを返します; インスタンスがメソッドオブジェクトを生成した場合、戻り値は
   インスタンスのクラスになります。


.. cfunction:: PyObject * PyMethod_GET_CLASS(PyObject * meth)

   :cfunc:`PyMethod_Class` をマクロで実装したバージョンで、エラーチェックを行いません。


.. cfunction:: PyObject * PyMethod_Function(PyObject * meth)

   *meth* に関連付けられている関数オブジェクトを返します。


.. cfunction:: PyObject * PyMethod_GET_FUNCTION(PyObject * meth)

   :cfunc:`PyMethod_Function` のマクロ版で、エラーチェックを行いません。


.. cfunction:: PyObject * PyMethod_Self(PyObject * meth)

   *meth* が束縛メソッドの場合には、メソッドに関連付けられているインスタンスを返します。それ以外の場合には *NULL* を返します。


.. cfunction:: PyObject * PyMethod_GET_SELF(PyObject * meth)

   :cfunc:`PyMethod_Self` のマクロ版で、エラーチェックを行いません。


.. _moduleobjects:

モジュールオブジェクト (module object)
--------------------------------------

.. index:: object: module

モジュールオブジェクト固有の関数は数個しかありません。


.. cvar:: PyTypeObject PyModule_Type

   .. index:: single: ModuleType (in module types)

   この :ctype:`PyTypeObject` のインスタンスは Python のモジュールオブジェクト型を表現します。このオブジェクトは、Python
   プログラムには ``types.ModuleType``  として公開されています。


.. cfunction:: int PyModule_Check(PyObject *p)

   *o* がモジュールオブジェクトかモジュールオブジェクトのサブタイプであるときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. cfunction:: int PyModule_CheckExact(PyObject *p)

   *o* がモジュールオブジェクトで、かつモジュールオブジェクトのサブタイプでないときに真を返します。  :cdata:`PyModule_Type`.

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyModule_New(const char * name)

   .. index::
      single: __name__ (module attribute)
      single: __doc__ (module attribute)
      single: __file__ (module attribute)

   :attr:`__name__` 属性が *name* に設定された新たなモジュールオブジェクトを返します。モジュールの :attr:`__doc__`
   および :attr:`__name__` 属性だけに値が入っています; :attr:`__file__` 属性に値を入れるのは呼び出し側の責任です。


.. cfunction:: PyObject * PyModule_GetDict(PyObject * module)

   .. index:: single: __dict__ (module attribute)

   *module* の名前空間を実現する辞書オブジェクトを返します; このオブジェクトはモジュールオブジェクトの :attr:`__dict__`
   と同じです。この関数が失敗することはありません。  拡張モジュールでは、この関数で得たモジュールの :attr:`__dict__`
   を直接いじるより、他の :cfunc:`PyModule_\ *` および :cfunc:`PyObject_\* ` 関数を使うよう勧めます。


.. cfunction:: char * PyModule_GetName(PyObject * module)

   .. index::
      single: __name__ (module attribute)
      single: SystemError (built-in exception)

   *module* の :attr:`__name__` の値を返します。モジュールがこの属性を提供していない場合や文字列型でない場合、
   :exc:`SystemError` を送出して *NULL* を返します。


.. cfunction:: char * PyModule_GetFilename(PyObject * module)

   .. index::
      single: __file__ (module attribute)
      single: SystemError (built-in exception)

   *module* をロードするために使ったファイルの名前を、 *module* の :attr:`__file__`
   属性から調べて返します。 :attr:`__file__` が定義されていない場合や文字列型でない場合、 :exc:`SystemError` を送出して
   *NULL* を返します。


.. cfunction:: int PyModule_AddObject(PyObject *module, const char * name, PyObject *value)

   *module* にオブジェクトを *name* として追加します。この関数はモジュールの初期化関数から利用される便宜関数です。エラーのときには ``-1``
   を、成功したときには ``0`` を返します。

   .. versionadded:: 2.0


.. cfunction:: int PyModule_AddIntConstant(PyObject *module, const char * name, long value)

   *module* に整数定数を *name* として追加します。この便宜関数はモジュールの初期化関数から利用されています。エラーのときには ``-1``
   を、成功したときには ``0`` を返します。

   .. versionadded:: 2.0


.. cfunction:: int PyModule_AddStringConstant(PyObject *module, const char * name, char *value)

   *module* に文字列定数を *name* として追加します。この便宜関数はモジュールの初期化関数から利用されています。文字列 *value* は
   null 終端されていなければなりません。エラーのときには ``-1`` を、成功したときには ``0`` を返します。

   .. versionadded:: 2.0


.. _iterator-objects:

イテレータオブジェクト (iterator object)
----------------------------------------

Python では二種類のイテレータオブジェクトを提供しています。一つ目はシーケンスイテレータで、 :meth:`__getitem__` メソッドを
サポートする任意のシーケンスを取り扱います。二つ目は呼び出し可能オブジェクトとセンチネル値 (sentinel value) を扱い、
シーケンス内の要素ごとに呼び出し可能オブジェクトを呼び出して、センチネル値が返されたときに反復処理を終了します。


.. cvar:: PyTypeObject PySeqIter_Type

   :cfunc:`PySeqIter_New` や、組み込みシーケンス型に対して 1 引数形式の組み込み関数 :func:`iter` を呼び出したときに
   返される、イテレータオブジェクトの型オブジェクトです。

   .. versionadded:: 2.2


.. cfunction:: int PySeqIter_Check(op)

   :cdata:`PySeqIter_Type` の型が *op* のときに真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PySeqIter_New(PyObject * seq)

   一般的なシーケンスオブジェクト *seq* を扱うイテレータを返します。反復処理は、シーケンスが添字指定操作の際に :exc:`IndexError` を
   返したときに終了します。

   .. versionadded:: 2.2


.. cvar:: PyTypeObject PyCallIter_Type

   :cfunc:`PyCallIter_New` や、組み込み関数 :func:`iter` の 2 引数形式が返すイテレータオブジェクトの型オブジェクトです。
   :func:`iter` built-in function.

   .. versionadded:: 2.2


.. cfunction:: int PyCallIter_Check(op)

   :cdata:`PyCallIter_Type` の型が *op* のときに真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyCallIter_New(PyObject * callable, PyObject *sentinel)

   新たなイテレータを返します。最初のパラメタ *callable* は引数なしで呼び出せる Python の呼び出し可能オブジェクトならなんでもかまいません;
   *callable* は、呼び出されるたびに次の反復処理対象オブジェクトを返さなければなりません。生成されたイテレータは、 *callable* が
   *sentinel* に等しい値を返すと反復処理を終了します。

   .. versionadded:: 2.2


.. _descriptor-objects:

デスクリプタオブジェクト (descriptor object)
--------------------------------------------

"デスクリプタ (descriptor)" は、あるオブジェクトのいくつかの属性について記述したオブジェクトです。デスクリプタオブジェクトは
型オブジェクトの辞書内にあります。


.. cvar:: PyTypeObject PyProperty_Type

   組み込みデスクリプタ型の型オブジェクトです。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyDescr_NewGetSet(PyTypeObject * type, struct PyGetSetDef *getset)

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyDescr_NewMember(PyTypeObject * type, struct PyMemberDef *meth)

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyDescr_NewMethod(PyTypeObject * type, struct PyMethodDef *meth)

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyDescr_NewWrapper(PyTypeObject * type, struct wrapperbase *wrapper, void * wrapped)

   .. versionadded:: 2.2


.. cfunction:: int PyDescr_IsData(PyObject *descr)

   デスクリプタオブジェクト *descr* がデータ属性のデスクリプタの場合には真を、メソッドデスクリプタの場合には偽を返します。 *descr*
   はデスクリプタオブジェクトでなければなりません; エラーチェックは行いません。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyWrapper_New(PyObject *, PyObject *)

   .. versionadded:: 2.2


.. _slice-objects:

スライスオブジェクト (slice object)
-----------------------------------


.. cvar:: PyTypeObject PySlice_Type

   .. index:: single: SliceType (in module types)

   スライスオブジェクトの型オブジェクトです。 ``slice`` や ``types.SliceType`` と同じです。


.. cfunction:: int PySlice_Check(PyObject *ob)

   *ob* がスライスオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。


.. cfunction:: PyObject * PySlice_New(PyObject * start, PyObject *stop, PyObject * step)

   指定した値から新たなスライスオブジェクトを返します。パラメタ *start*, *stop*, および *step* はスライスオブジェクトに
   おける同名の属性として用いられます。これらの値はいずれも *NULL* にでき、対応する値には ``None`` が使われます。新たな
   オブジェクトをアロケーションできない場合には *NULL* を返します。


.. cfunction:: int PySlice_GetIndices(PySliceObject *slice, Py_ssize_t length, Py_ssize_t * start, Py_ssize_t *stop, Py_ssize_t * step)

   スライスオブジェクト *slice* における *start*, *stop*,  および *step* のインデクス値を取得します。このときシーケンスの
   長さを *length* と仮定します。 *length* よりも大きなインデクスになるとエラーとして扱います。

   成功のときには ``0`` を、エラーのときには例外をセットせずに ``-1`` を返します (ただし、指定インデクスのいずれか一つが
   :const:`None` ではなく、かつ整数に変換できなかった場合を除きます。この場合、 ``-1`` を返して例外をセットします)。

   おそらくこの関数を使う気にはならないでしょう。バージョン 2.3 以前の Python でスライスオブジェクトを使いたいのなら、
   :cfunc:`PySlice_GetIndicesEx` のソースを適切に名前変更して自分の拡張モジュールのソースコード内に組み込むとよいでしょう。


.. cfunction:: int PySlice_GetIndicesEx(PySliceObject *slice, Py_ssize_t length, Py_ssize_t * start, Py_ssize_t *stop, Py_ssize_t * step, Py_ssize_t *slicelength)

   :cfunc:`PySlice_GetIndices` の置き換えとして使える関数です。

   スライスオブジェクト *slice* における *start*, *stop*,  および *step* のインデクス値を取得します。このときシーケンスの
   長さを *length* と仮定します。スライスの長さを *slicelength* に記憶します。境界をはみだしたインデクスは、通常のスライスを扱うのと
   同じ一貫したやり方でクリップされます。

   成功のときには ``0`` を、エラーのときには例外をセットして ``-1`` を返します。

   .. versionadded:: 2.3


.. _weakref-objects:

弱参照オブジェクト (weak reference object)
------------------------------------------

Python は *弱参照* を第一級オブジェクト (first-class object)
としてサポートします。弱参照を直接実装する二種類の固有のオブジェクト型があります。第一は単純な参照オブジェクトで、第二はオリジナルの
オブジェクトに対して可能な限りプロキシとして振舞うオブジェクトです。


.. cfunction:: int PyWeakref_Check(ob)

   *ob* が参照オブジェクトかプロキシオブジェクトの場合に真を返します。

   .. versionadded:: 2.2


.. cfunction:: int PyWeakref_CheckRef(ob)

   *ob* が参照オブジェクトの場合に真を返します。

   .. versionadded:: 2.2


.. cfunction:: int PyWeakref_CheckProxy(ob)

   *ob* がプロキシオブジェクトの場合に真を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyWeakref_NewRef(PyObject * ob, PyObject *callback)

   *ob* に対する弱参照オブジェクトを返します。この関数は常に新たな参照を返しますが、必ずしも新たなオブジェクトを作る保証はありません;
   既存の参照オブジェクトが返されることもあります。第二のパラメタ *callback* は呼び出し可能オブジェクトで、 *ob*
   がガーベジコレクションされた際に通知を受け取ります; *callback* は弱参照オブジェクト自体を単一のパラメタとして受け取ります。 *callback*
   は ``None`` や *NULL* にしてもかまいません。 *ob* が弱参照できないオブジェクトの場合や、 *callback*
   が呼び出し可能オブジェクト、 ``None`` 、 *NULL* のいずれでもない場合は、 *NULL* を返して :exc:`TypeError` を送出します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyWeakref_NewProxy(PyObject * ob, PyObject *callback)

   *ob* に対する弱参照プロキシオブジェクトを返します。この関数は常に新たな参照を返しますが、必ずしも新たなオブジェクトを作る保証はありません;
   既存の参照オブジェクトが返されることもあります。第二のパラメタ *callback* は呼び出し可能オブジェクトで、 *ob*
   がガーベジコレクションされた際に通知を受け取ります; *callback* は弱参照オブジェクト自体を単一のパラメタとして受け取ります。 *callback*
   は ``None`` や *NULL* にしてもかまいません。 *ob* が弱参照できないオブジェクトの場合や、 *callback*
   が呼び出し可能オブジェクト、 ``None`` 、 *NULL* のいずれでもない場合は、 *NULL* を返して :exc:`TypeError` を送出します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyWeakref_GetObject(PyObject * ref)

   弱参照 *ref* が参照しているオブジェクトを返します。被参照オブジェクトがすでに存続していない場合、 ``None`` を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject * PyWeakref_GET_OBJECT(PyObject * ref)

   :cfunc:`PyWeakref_GetObject` に似ていますが、マクロで実装されていて、エラーチェックを行いません。

   .. versionadded:: 2.2


.. _cobjects:

Cオブジェクト (CObject)
-----------------------

.. index:: object: CObject

このオブジェクトの使用法に関する情報は、 *Python インタプリタの拡張と埋め込み* 1.12 節、 "Providing a C API for an
Extension Module," を参照してください。


.. ctype:: PyCObject

   この :ctype:`PyObject` のサブタイプは不透明型値 (opaque value) を表現します。C 拡張モジュールが Python
   コードから不透明型値を  (:ctype:`void\*` ポインタで) 他の C コードに渡す必要があるときに便利です。正規の import
   機構を使って動的にロードされるモジュール内で定義されている C API にアクセスするために、あるモジュール内で定義されている C
   関数ポインタを別のモジュールでも利用できるようにするためによく使われます。


.. cfunction:: int PyCObject_Check(PyObject *p)

   引数が :ctype:`PyCObject` の場合に真を返します。


.. cfunction:: PyObject * PyCObject_FromVoidPtr(void* cobj, void (*destr)(void *))

   ``void *``* cobj * から :ctype:`PyCObject` を生成します。関数 * destr * が * NULL*
   でない場合、オブジェクトを再利用する際に呼び出します。


.. cfunction:: PyObject * PyCObject_FromVoidPtrAndDesc(void* cobj, void * desc, void (* destr)(void *, void *))

   ``void *``* cobj * から :ctype:`PyCObject` を生成します。関数 * destr * が * NULL*
   でない場合、オブジェクトを再利用する際に呼び出します。引数 *desc* を使って、デストラクタ関数に追加のコールバックデータを渡せます。


.. cfunction:: void * PyCObject_AsVoidPtr(PyObject* self)

   :ctype:`PyCObject` オブジェクト *self* を生成するのに用いたオブジェクト :ctype:`void \*` を返します。


.. cfunction:: void * PyCObject_GetDesc(PyObject* self)

   :ctype:`PyCObject` オブジェクト *self* を生成するのに用いたコールバックデータ :ctype:`void \*` を返します。


.. cfunction:: int PyCObject_SetVoidPtr(PyObject * self, void* cobj)

   *self* 内の void ポインタ *cobj* に設定します。 :ctype:`PyCObject` にデストラクタが関連づけられていてはなりません。
   成功すると真値を返し、失敗すると偽値を返します。


.. _cell-objects:

セルオブジェクト (cell object)
------------------------------

"セル (cell)" オブジェクトは、複数のスコープから参照される変数群を実装するために使われます。セルは各変数について作成され、各々の値を記憶します;
この値を参照する各スタックフレームにおけるローカル変数には、そのスタックフレームの外側で同じ値を参照している
セルに対する参照が入ります。セルで表現された値にアクセスすると、セルオブジェクト自体の代わりにセル内の値が使われます。このセルオブジェクトを使った間接参照
(dereference) は、インタプリタによって生成されたバイトコード内でサポートされている必要があります;
セルオブジェクトにアクセスした際に、自動的に間接参照は起こりません。上記以外の状況では、セルオブジェクトは役に立たないはずです。


.. ctype:: PyCellObject

   セルオブジェクトに使われる C 構造体です。


.. cvar:: PyTypeObject PyCell_Type

   セルオブジェクトに対応する型オブジェクトです。


.. cfunction:: int PyCell_Check(ob)

   *ob* がセルオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。


.. cfunction:: PyObject * PyCell_New(PyObject * ob)

   値 *ob* の入った新たなセルオブジェクトを生成して返します。引数を *NULL* にしてもかまいません。


.. cfunction:: PyObject * PyCell_Get(PyObject * cell)

   *cell* の内容を返します。


.. cfunction:: PyObject * PyCell_GET(PyObject * cell)

   *cell* の内容を返しますが、 *cell* が非 *NULL* でかつセルオブジェクトであるかどうかチェックしません。


.. cfunction:: int PyCell_Set(PyObject *cell, PyObject * value)

   セルオブジェクト *cell* の内容を *value* に設定します。この関数は現在のセルの全ての内容に対する参照を解放します。 *value* は
   *NULL* でもかまいません。 *cell* は非 *NULL* でなければなりません; もし *cell* がセルオブジェクトでない場合、 ``-1``
   を返します。成功すると ``0`` を返します。


.. cfunction:: void PyCell_SET(PyObject *cell, PyObject * value)

   セルオブジェクト *cell* の値を *value* に設定します。参照カウントに対する変更はなく、安全のためのチェックは何も行いません; *cell*
   は非 *NULL* でなければならず、かつセルオブジェクトでなければなりません。


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


.. cfunction:: PyObject * PyGen_New(PyFrameObject * frame)

   *frame* オブジェクトに基づいて新たなジェネレータオブジェクトを生成して返します。この関数は *frame* への参照を盗みます。パラメタが
   *NULL* であってはなりません。


.. _datetime-objects:

DateTime オブジェクト
---------------------

:mod:`datetime` モジュールでは、様々な日付オブジェクトや時刻オブジェクト
を提供しています。以下に示す関数を使う場合には、あらかじめヘッダファイル :file:`datetime.h` をソースに include し
(:file:`Python.h` はこのファイルを  include しません)、 :cfunc:`PyDateTime_IMPORT` マクロを起動しておく
必要があります。このマクロは以下のマクロで使われる静的変数 ``PyDateTimeAPI`` に C 構造体へのポインタを入れます。

.. % DateTime Objects

以下は型チェックマクロです:


.. cfunction:: int PyDate_Check(PyObject *ob)

   *ob* が :cdata:`PyDateTime_DateType` 型か :cdata:`PyDateTime_DateType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. cfunction:: int PyDate_CheckExact(PyObject *ob)

   *ob* が :cdata:`PyDateTime_DateType` 型のオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_Check(PyObject *ob)

   *ob* が :cdata:`PyDateTime_DateTimeType` 型か :cdata:`PyDateTime_DateTimeType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_CheckExact(PyObject *ob)

   *ob* が :cdata:`PyDateTime_DateTimeType` 型のオブジェクトの場合に真を返します; *ob* は *NULL*
   であってはなりません。

   .. versionadded:: 2.4


.. cfunction:: int PyTime_Check(PyObject *ob)

   *ob* が :cdata:`PyDateTime_TimeType` 型か :cdata:`PyDateTime_TimeType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. cfunction:: int PyTime_CheckExact(PyObject *ob)

   *ob* が :cdata:`PyDateTime_TimeType` 型のオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. cfunction:: int PyDelta_Check(PyObject *ob)

   *ob* が :cdata:`PyDateTime_DeltaType` 型か :cdata:`PyDateTime_DeltaType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. cfunction:: int PyDelta_CheckExact(PyObject *ob)

   *ob* が :cdata:`PyDateTime_DeltaType` 型のオブジェクトの場合に真を返します; *ob* は *NULL*
   であってはなりません。

   .. versionadded:: 2.4


.. cfunction:: int PyTZInfo_Check(PyObject *ob)

   *ob* が :cdata:`PyDateTime_TZInfoType` 型か :cdata:`PyDateTime_TZInfoType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. cfunction:: int PyTZInfo_CheckExact(PyObject *ob)

   *ob* が :cdata:`PyDateTime_TZInfoType` 型のオブジェクトの場合に真を返します; *ob* は *NULL*
   であってはなりません。

   .. versionadded:: 2.4

以下はオブジェクトを作成するためのマクロです:


.. cfunction:: PyObject* PyDate_FromDate(int year, int month, int day)

   指定された年、月、日の ``datetime.date`` オブジェクトを返します。

   .. versionadded:: 2.4


.. cfunction:: PyObject* PyDateTime_FromDateAndTime(int year, int month, int day, int hour, int minute, int second, int usecond)

   指定された年、月、日、時、分、秒、マイクロ秒の ``datetime.datetime``  オブジェクトを返します。

   .. versionadded:: 2.4


.. cfunction:: PyObject* PyTime_FromTime(int hour, int minute, int second, int usecond)

   指定された時、分、秒、マイクロ秒の ``datetime.time``  オブジェクトを返します。

   .. versionadded:: 2.4


.. cfunction:: PyObject* PyDelta_FromDSU(int days, int seconds, int useconds)

   指定された日、秒、マイクロ秒の ``datetime.timedelta`` オブジェクトを返します。マイクロ秒と秒が
   ``datetime.timedelta`` オブジェクトで定義されている範囲に入るように正規化を行います。

   .. versionadded:: 2.4

以下のマクロは date オブジェクトからフィールド値を取り出すためのものです。引数は :cdata:`PyDateTime_Date` またはそのサブクラス
(例えば :cdata:`PyDateTime_DateTime`)の  インスタンスでなければなりません。引数を *NULL* にしてはならず、
型チェックは行いません:


.. cfunction:: int PyDateTime_GET_YEAR(PyDateTime_Date *o)

   年を正の整数で返します。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_GET_MONTH(PyDateTime_Date *o)

   月を 1 から 12 の間の整数で返します。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_GET_DAY(PyDateTime_Date *o)

   日を 1 から 31 の間の整数で返します。

   .. versionadded:: 2.4

以下のマクロは datetime オブジェクトからフィールド値を取り出すためのものです。引数は :cdata:`PyDateTime_DateTime`
またはそのサブクラスのインスタンスでなければなりません。引数を *NULL* にしてはならず、型チェックは行いません:


.. cfunction:: int PyDateTime_DATE_GET_HOUR(PyDateTime_DateTime *o)

   時を 0 から 23 の間の整数で返します。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_DATE_GET_MINUTE(PyDateTime_DateTime *o)

   分を 0 から 59 の間の整数で返します。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_DATE_GET_SECOND(PyDateTime_DateTime *o)

   秒を 0 から 59 の間の整数で返します。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_DATE_GET_MICROSECOND(PyDateTime_DateTime *o)

   マイクロ秒を 0 から 999999 の間の整数で返します。

   .. versionadded:: 2.4

以下のマクロは time オブジェクトからフィールド値を取り出すためのものです。引数は :cdata:`PyDateTime_Time` またはそのサブクラスの
インスタンスでなければなりません。引数を *NULL* にしてはならず、型チェックは行いません:


.. cfunction:: int PyDateTime_TIME_GET_HOUR(PyDateTime_Time *o)

   時を 0 から 23 の間の整数で返します。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_TIME_GET_MINUTE(PyDateTime_Time *o)

   分を 0 から 59 の間の整数で返します。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_TIME_GET_SECOND(PyDateTime_Time *o)

   秒を 0 から 59 の間の整数で返します。

   .. versionadded:: 2.4


.. cfunction:: int PyDateTime_TIME_GET_MICROSECOND(PyDateTime_Time *o)

   マイクロ秒を 0 から 999999 の間の整数で返します。

   .. versionadded:: 2.4

以下のマクロは DB API を実装する上での便宜用です:


.. cfunction:: PyObject * PyDateTime_FromTimestamp(PyObject * args)

   ``dateitme.datetime.fromtimestamp()`` に渡すのに適した引数タプルから新たな ``datetime.datetime``
   オブジェクトを生成して返します。

   .. versionadded:: 2.4


.. cfunction:: PyObject * PyDate_FromTimestamp(PyObject * args)

   ``dateitme.date.fromtimestamp()`` に渡すのに適した引数タプルから新たな ``datetime.date``
   オブジェクトを生成して返します。

   .. versionadded:: 2.4


.. _setobjects:

集合オブジェクト (Set Objects)
------------------------------

.. sectionauthor:: Raymond D. Hettinger <python@rcn.com>


.. index::
   object: set
   object: frozenset

.. versionadded:: 2.5

このセクションでは :class:`set` と :class:`frozenset` の公開APIについて詳しく述べます。
以降で説明していない機能は、抽象オブジェクトプロトコル ( :cfunc:`PyObject_CallMethod`,
:cfunc:`PyObject_RichCompareBool`, :cfunc:`PyObject_Hash`,
:cfunc:`PyObject_Repr`, :cfunc:`PyObject_IsTrue`, :cfunc:`PyObject_Print`,
:cfunc:`PyObject_GetIter` を含む) か抽象数値プロトコル ( :cfunc:`PyNumber_Add`,
:cfunc:`PyNumber_Subtract`, :cfunc:`PyNumber_Or`, :cfunc:`PyNumber_Xor`,
:cfunc:`PyNumber_InPlaceAdd`, :cfunc:`PyNumber_InPlaceSubtract`,
:cfunc:`PyNumber_InPlaceOr`, :cfunc:`PyNumber_InPlaceXor` を含む) を使って利用できます。


.. ctype:: PySetObject

   この :ctype:`PyObject` を継承した型は、 :class:`set` と :class:`frozenset` 両方の
   内部データを保存するのに用いられます。 :ctype:`PyDictObject`
   と同じように、小さい集合(set)に対しては(タプルのように)固定サイズであり、
   そうでない集合に対しては(リストと同じように)可変長のメモリブロックを用います。この構造体のどのフィールドも、非公開で変更される可能性があると考えて下さい。
   すべてのアクセスは、構造体の中の値を直接操作するのではなく、ドキュメントされた APIを用いて行うべきです。


.. cvar:: PyTypeObject PySet_Type

   この :ctype:`PyTypeObject` のインスタンスは、Pythonの :class:`set` 型を表します。


.. cvar:: PyTypeObject PyFrozenSet_Type

   この :ctype:`PyTypeObject` のインスタンスは、Pythonの :class:`frozenset` 型を表します。

以降の型チェックマクロはすべてのPythonオブジェクトに対するポインタに対して動作します。
同様に、コンストラクタはすべてのイテレート可能なPythonオブジェクトに対して動作します。


.. cfunction:: int PyAnySet_Check(PyObject *p)

   *p* が :class:`set` か :class:`frozenset` 、あるいはそのサブタイプのオブジェクトであれば、trueを返します。


.. cfunction:: int PyAnySet_CheckExact(PyObject *p)

   *p* が :class:`set` か :class:`frozenset` のどちらかのオブジェクトであるときに true を返します。
   サブタイプのオブジェクトは含みません。


.. cfunction:: int PyFrozenSet_CheckExact(PyObject *p)

   *p* が :class:`frozenset` のオブジェクトであるときに true を返します。サブタイプのオブジェクトは含みません。


.. cfunction:: PyObject * PySet_New(PyObject * iterable)

   *iterable* が返すオブジェクトを含む新しい :class:`set` を返します。 *iterable* が *NULL*
   のときは、空のsetを返します。成功したら新しいsetを、失敗したら *NULL* を返します。 *iterable* がイテレート可能で無い場合は、
   :exc:`TypeError` を送出します。このコンストラクタは set をコピーするときにも使えます。 (``c=set(s)``)


.. cfunction:: PyObject * PyFrozenSet_New(PyObject * iterable)

   *iterable* が返すオブジェクトを含む新しい :class:`frozenset` を返します。 *iterable* が *NULL*
   のときは、空のfrozensetを返します。 *iterable* がイテレート可能で無い場合は、 :exc:`TypeError` を送出します。

以降の関数やマクロは、 :class:`set` と :class:`frozenset` とそのサブタイプのインスタンスに対して利用できます。


.. cfunction:: int PySet_Size(PyObject *anyset)

   .. index:: builtin: len

   :class:`set` や :class:`frozenset` のオブジェクトの長さを返します。 ``len(anyset)`` と同じです。
   *anyset* が :class:`set` 、 :class:`frozenset` 及びそのサブタイプのオブジェクトで
   無い場合は、 :exc:`PyExc_SystemError` を送出します。


.. cfunction:: int PySet_GET_SIZE(PyObject *anyset)

   エラーチェックを行わない、 :cfunc:`PySet_Size` のマクロ形式。


.. cfunction:: int PySet_Contains(PyObject *anyset, PyObject * key)

   見つかったら１を、見つからなかったら0を、エラーが発生したときは-1を返します。 Pythonの :meth:`__contains__`
   メソッドと違って、この関数は非ハッシュsetを一時frozensetに自動で変換しません。
   *key* がハッシュ可能で無い場合、 :exc:`TypeError` を送出します。 *anyset* が :class:`set`,
   :class:`frozenset` 及びそのサブタイプのオブジェクトで無い場合は :exc:`PyExc_SystemError` を送出します。

以降の関数は、 :class:`set` とそのサブタイプに対して利用可能です。 :class:`frozenset` とそのサブタイプには利用できません。


.. cfunction:: int PySet_Add(PyObject *set, PyObject * key)

   :class:`set` のインスタンスに *key* を追加します。 :class:`frozenset` のインスタンスに使わないで下さい。
   成功したら0を、失敗したら-1を返します。 *key* がハッシュ可能でないなら、 :exc:`TypeError` を送出します。
   setを大きくする余裕が無い場合は、 :exc:`MemoryError` を送出します。
   *set* が :class:`set` とそのサブタイプのインスタンスで無い場合は、 :exc:`SystemError` を送出します。


.. cfunction:: int PySet_Discard(PyObject *set, PyObject * key)

   見つかって削除したら1を返します。見つからなかったら何もせずに0を返します。エラーが発生したら-1を返します。
   keyが無くても :exc:`KeyError` を送出しません。 *key* がハッシュ不可能であれば :exc:`TypeError` を送出します。
   Pythonの :meth:`discard` メソッドと違って、この関数は非ハッシュsetsを一時frozensetに変換しません。
   *set* が :class:`set` とそのサブタイプのインスタンスで無いときは、 :exc:`PyExc_SystemError` を送出します。


.. cfunction:: PyObject * PySet_Pop(PyObject * set)

   *set* の中の要素のどれかに対する新しい参照を返し、そのオブジェクトを *set* から削除します。失敗したら *NULL* を返します。
   setが空の場合には :exc:`KeyError` を送出します。 *set* が :class:`set` とそのサブタイプのインスタンスで無い場合は、
   :exc:`SystemError` を送出します。


.. cfunction:: int PySet_Clear(PyObject *set)

   setを空にします。

