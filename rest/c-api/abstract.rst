.. highlightlang:: c


.. _abstract:

***********************************************
抽象オブジェクトレイヤ (abstract objects layer)
***********************************************

この章で説明する関数は、Python オブジェクトとのやりとりを型や (数値型全て、シーケンス型全てといった) 大まかなオブジェクト型の種類に
関係なく行います。関数を適用対象でないオブジェクトに対して 使った場合、 Python の例外が送出されることになります。

これらの関数は、:cfunc:`PyList_New`で作成された後に``NULL``以外の値を
設定されていないリストのような、適切に初期化されていないオブジェクトに対して 使うことはできません。


.. _object:

オブジェクトプロトコル (object protocol)
========================================


.. cfunction:: int PyObject_Print(PyObject *o, FILE *fp, int flags)

   オブジェクト *o* をファイル *fp* に出力します。 失敗すると``-1`` を返します。 *flags*
   引数は何らかの出力オプションを有効にする際に使います。 現在サポートされている唯一のオプションは:const:`Py_PRINT_RAW` です;
   このオプションを指定すると、:func:`repr` の代わりに :func:`str` を使ってオブジェクトを書き込みます。


.. cfunction:: int PyObject_HasAttrString(PyObject *o, const char *attr_name)

   *o* が属性 *attr_name* を持つときに ``1`` を、それ以外の ときに ``0`` を返します。この関数は Python の式
   ``hasattr(o, attr_name)`` と同じです。 この関数は常に成功します。


.. cfunction:: PyObject* PyObject_GetAttrString(PyObject *o, const char *attr_name)

   オブジェクト *o* から、名前 *attr_name* の属性を取得します。 成功すると属性値を返し失敗すると *NULL* を返します。 この関数は
   Python の式 ``o.attr_name`` と同じです。


.. cfunction:: int PyObject_HasAttr(PyObject *o, PyObject *attr_name)

   *o* が属性 *attr_name* を持つときに ``1`` を、それ以外の ときに ``0`` を返します。この関数は Python の式
   ``hasattr(o, attr_name)`` と同じです。 この関数は常に成功します。


.. cfunction:: PyObject* PyObject_GetAttr(PyObject *o, PyObject *attr_name)

   オブジェクト *o* から、名前 *attr_name* の属性を取得します。 成功すると属性値を返し失敗すると *NULL* を返します。 この関数は
   Python の式 ``o.attr_name`` と同じです。


.. cfunction:: int PyObject_SetAttrString(PyObject *o, const char *attr_name, PyObject *v)

   オブジェクト *o* の*attr_name* という名の属性に、値 *v* を設定します。失敗すると ``-1`` を返します。 この関数は Python
   の式 ``o.attr_name = v`` と同じです。


.. cfunction:: int PyObject_SetAttr(PyObject *o, PyObject *attr_name, PyObject *v)

   オブジェクト *o* の*attr_name* という名の属性に、値 *v* を設定します。失敗すると ``-1`` を返します。 この関数は Python
   の式 ``o.attr_name = v`` と同じです。


.. cfunction:: int PyObject_DelAttrString(PyObject *o, const char *attr_name)

   オブジェクト *o* の*attr_name* という名の属性を削除します。 失敗すると ``-1`` を返します。 この関数は Python の文 ``del
   o.attr_name`` と同じです。


.. cfunction:: int PyObject_DelAttr(PyObject *o, PyObject *attr_name)

   オブジェクト *o* の*attr_name* という名の属性を削除します。 失敗すると ``-1`` を返します。 この関数は Python の文 ``del
   o.attr_name`` と同じです。


.. cfunction:: PyObject* PyObject_RichCompare(PyObject *o1, PyObject *o2, int opid)

   *o1* と *o2* を *opid* に指定した演算によって比較します。 *opid* は :const:`Py_LT`, :const:`Py_LE`,
   :const:`Py_EQ`, :const:`Py_NE`, :const:`Py_GT`, または :const:`Py_GE`,
   のいずれかでなければならず、それぞれ ``<``, ``<=``, ``==``, ``!=``, ``>``, および ``>=`` に対応します。
   この関数は Python の式 ``o1 op o2`` と同じで、 ``op`` が *opid* に対応する演算子です。
   成功すると比較結果の値を返し失敗すると *NULL* を返します。


.. cfunction:: int PyObject_RichCompareBool(PyObject *o1, PyObject *o2, int opid)

   *o1* と *o2* を *opid* に指定した演算によって比較します。 *opid* は :const:`Py_LT`, :const:`Py_LE`,
   :const:`Py_EQ`, :const:`Py_NE`, :const:`Py_GT`, または :const:`Py_GE`,
   のいずれかでなければならず、それぞれ ``<``, ``<=``, ``==``, ``!=``, ``>``, および ``>=`` に対応します。
   比較結果が真ならば ``1`` を、偽ならば ``0`` を、 エラーが発生すると ``-1`` を返します。 この関数は Python の式 ``o1 op
   o2`` と同じで、 ``op`` が *opid* に対応する演算子です。


.. cfunction:: int PyObject_Cmp(PyObject *o1, PyObject *o2, int *result)

   .. index:: builtin: cmp

   *o1* と *o2* の値を比較します。このとき*o1* が比較ルーチンを 持っていればそれを使い、なければ *o2* のルーチンを使います。 比較結果は
   *result* に返されます。失敗すると ``-1`` を返します。 Python 文 ``result = cmp(o1, o2)`` と同じです。


.. cfunction:: int PyObject_Compare(PyObject *o1, PyObject *o2)

   .. index::
      builtin: cmp
      builtin: cmp

   *o1* と *o2* の値を比較します。このとき*o1* が比較ルーチンを 持っていればそれを使い、なければ *o2* のルーチンを使います。 比較結果は
   *result* に返されます。失敗すると ``-1`` を返します。 Python 文 ``result = cmp(o1, o2)``
   と同じです。成功すると比較結果を返します。エラーが生じた場合の 戻り値は未定義です; :cfunc:`PyErr_Occurred` を使ってエラー検出を
   行って下さい。Python 式 ``cmp(o1,  o2)`` と同じです。


.. cfunction:: PyObject* PyObject_Repr(PyObject *o)

   .. index:: builtin: repr

   *o* の文字列表現を計算します。成功すると文字列表現を返し、 失敗すると *NULL* を返します。Python 式``repr(o)``
   と同じです。この関数は組み込み関数 :func:`repr` や逆クオート表記の処理で 呼び出されます。


.. cfunction:: PyObject* PyObject_Str(PyObject *o)

   .. index:: builtin: str

   *o* の文字列表現を計算します。成功すると文字列表現を返し、 失敗すると *NULL* を返します。Python 式``str(o)``
   と同じです。この関数は組み込み関数 :func:`str` や:keyword:`print` 文の処理で 呼び出されます。


.. cfunction:: PyObject* PyObject_Unicode(PyObject *o)

   .. index:: builtin: unicode

   *o* の Unicode 文字列表現を計算します。成功すると Unicode 文字列表現を返し失敗すると *NULL* を返します。 Python
   式``unicode(o)`` と同じです。この関数は組み込み関数 :func:`unicode` の処理で呼び出されます。


.. cfunction:: int PyObject_IsInstance(PyObject *inst, PyObject *cls)

   *inst* が *cls* のインスタンスか、 *cls* のサブクラスの インスタンスの場合に ``-1`` を返し、そうでなければ ``0`` を
   返します。エラーの時には ``-1`` を返し、例外をセットします。 *cls* がクラスオブジェクトではなく型オブジェクトの場合、
   :cfunc:`PyObject_IsInstance` は *inst* が*cls* で あるときに ``1`` を返します。*cls*
   をタプルで指定した場合、 *cls* に指定した全てのエントリについてチェックを行います。 少なくとも一つのエントリに対するチェックが ``1``
   を返せば結果は ``1`` になり、そうでなければ ``0`` になります。 *inst* がクラスインスタンスでなく、かつ *cls* が
   型オブジェクトでもクラスオブジェクトでもタプルでもない場合、 *inst* には :attr:`__class__` 属性がなくてはなりません ---
   この場合、:attr:`__class__` 属性の値と、*cls* の値の間の クラス関係を、関数の戻り値を決定するのに使います。

   .. versionadded:: 2.1

   .. versionchanged:: 2.2
      二つ目の引数にタプルのサポートを追加しました。.

サブクラスの決定はかなり正攻法で行いますが、クラスシステムの拡張を 実装する人たちに知っておいて欲しいちょっとした問題点があります。 :class:`A` と
:class:`B` がクラスオブジェクトの場合、 :class:`B` が :class:`A` のサブクラスとなるのは、:class:`B` が
:class:`A` を 直接的あるいは間接的に継承 (inherit) している場合です。 両方がクラスオブジェクトでない場合、二つのオブジェクト間の
クラス関係を決めるには、より汎用の機構を使います。 *B* が *A* のサブクラスであるか調べたとき、*A* が *B*
と等しければ、:cfunc:`PyObject_IsSubclass` は真を返します。 *A* および *B* が異なるオブジェクトなら、*B* の
:attr:`__bases__` 属性から深さ優先探索 (depth-first search)で *A* を探索します ---
オブジェクトに:attr:`__bases__` があるだけで、 この決定法を適用する条件を満たしているとみなされます。


.. cfunction:: int PyObject_IsSubclass(PyObject *derived, PyObject *cls)

   クラス *derived* が *cls* と同じクラスか、*cls* の導出 クラスの場合に ``1`` を返し、それ以外の場合には ``0`` を
   返します。エラーが生じると ``-1`` を返します。  *cls* をタプルで指定した場合、*cls* に指定した全てのエントリに ついてチェックを行います。
   少なくとも一つのエントリに対するチェックが ``1`` を返せば結果は ``1`` になり、そうでなければ ``0`` になります。 *derived* または
   *cls* のいずれかが実際のクラスオブジェクト (あるいはタプル) でない場合、上で述べた汎用アルゴリズムを使います。

   .. versionadded:: 2.1

   .. versionchanged:: 2.3
      以前の Python のバージョンは、二つ目の引数に タプルをサポートしていませんでした.


.. cfunction:: int PyCallable_Check(PyObject *o)

   オブジェクト *o* が呼び出し可能オブジェクトかどうか調べます。 オブジェクトが呼び出し可能であるときに ``1`` を返し、 そうでないときには ``0``
   を返します。 この関数呼び出しは常に成功します。


.. cfunction:: PyObject* PyObject_Call(PyObject *callable_object, PyObject *args, PyObject *kw)

   .. index:: builtin: apply

   呼び出し可能な Python オブジェクト *callable_object* を タプルで指定された引数 *args* および辞書で指定された名前つき 引数
   (named argument) *kw* とともに呼び出します。名前つき引数を 必要としない場合、 *kw* を *NULL* にしてもかまいません。
   *args* は *NULL* であってはなりません。引数が全く必要ない場合には 空のタプルを使ってください。
   成功すると呼び出し結果として得られたオブジェクトを返し、 失敗すると *NULL* を返します。 Python の式
   ``apply(callable_object, args, kw)`` あるいは ``callable_object(*args, **kw)``
   と同じです。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyObject_CallObject(PyObject *callable_object, PyObject *args)

   .. index:: builtin: apply

   呼び出し可能な Python オブジェクト *callable_object* を タプルで指定された引数 *args* とともに呼び出します。  引数を
   必要としない場合、 *args* を *NULL* にしてもかまいません。 成功すると呼び出し結果として得られたオブジェクトを返し、 失敗すると *NULL*
   を返します。 Python の式 ``apply(callable_object, args)``  あるいは
   ``callable_object(*args)`` と同じです。


.. cfunction:: PyObject* PyObject_CallFunction(PyObject *callable, char *format, ...)

   .. index:: builtin: apply

   呼び出し可能な Python オブジェクト *callable_object* を 可変数個の C 引数とともに呼び出します。C 引数は
   :cfunc:`Py_BuildValue` 形式のフォーマット文字列を使って記述します。 *format*
   は*NULL*にしてもよく、与える引数がないことを表します。 成功すると呼び出し結果として得られたオブジェクトを返し、 失敗すると *NULL* を返します。
   Python の式 ``apply(callable, args)`` あるいは ``callable(*args)`` と同じです。
   もしも、:ctype:`PyObject \*` args だけを引数に渡す場合は、:cfunc:`PyObject_CallFunctionObjArgs`
   がより速い方法であることを覚えておいてください。


.. cfunction:: PyObject* PyObject_CallMethod(PyObject *o, char *method, char *format, ...)

   オブジェクト *o* の *method* という名前のメソッドを、 可変数個の C 引数とともに呼び出します。C 引数はタプルを生成するような
   :cfunc:`Py_BuildValue` 形式のフォーマット文字列を使って記述します。 *format*
   は*NULL*にしてもよく、与える引数がないことを表します。 成功すると呼び出し結果として得られたオブジェクトを返し、 失敗すると *NULL* を返します。
   Python の式 ``o.method(args)`` と同じです。 もしも、:ctype:`PyObject \*` args
   だけを引数に渡す場合は、:cfunc:`PyObject_CallMethodObjArgs` がより速い方法であることを覚えておいてください。


.. cfunction:: PyObject* PyObject_CallFunctionObjArgs(PyObject *callable, ..., NULL)

   呼び出し可能な Python オブジェクト *callable_object* を 可変数個の :ctype:`PyObject\*`
   引数とともに呼び出します。 引数列は末尾に *NULL*がついた可変数個のパラメタとして与えます。 成功すると呼び出し結果として得られたオブジェクトを返し
   失敗すると *NULL* を返します。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyObject_CallMethodObjArgs(PyObject *o, PyObject *name, ..., NULL)

   オブジェクト *o* のメソッドを呼び出します、メソッド名は Python 文字列オブジェクト*name* で与えます。可変数個の
   :ctype:`PyObject\*` 引数と共に呼び出されます. 引数列は末尾に *NULL*がついた可変数個のパラメタとして与えます。
   成功すると呼び出し結果として得られたオブジェクトを返し 失敗すると *NULL* を返します。

   .. versionadded:: 2.2


.. cfunction:: long PyObject_Hash(PyObject *o)

   .. index:: builtin: hash

   オブジェクト *o* のハッシュ値を計算して返します。 失敗すると ``-1`` を返します。 Python の式 ``hash(o)`` と同じです。


.. cfunction:: int PyObject_IsTrue(PyObject *o)

   *o* が真を表すとみなせる場合には ``1`` を、 そうでないときには ``0`` を返します。   Python の式 ``not not o``
   と同じです。 失敗すると ``-1`` を返します。


.. cfunction:: int PyObject_Not(PyObject *o)

   *o* が真を表すとみなせる場合には ``0`` を、 そうでないときには ``1`` を返します。   Python の式 ``not o`` と同じです。
   失敗すると ``-1`` を返します。


.. cfunction:: PyObject* PyObject_Type(PyObject *o)

   .. index:: builtin: type

   *o* が *NULL*でない場合、オブジェクト*o* のオブジェクト型に 相当する型オブジェクトを返します。失敗すると :exc:`SystemError`
   を送出して *NULL*を返します。 Python の式 ``type(o)``と同じです。  この関数は戻り値の参照カウントをインクリメントします。
   参照カウントのインクリメントが必要でない限り、広く使われていて :ctype:`PyTypeObject\*` 型のポインタを返す表記法
   ``o->ob_type`` の代わりに使う理由は全くありません。


.. cfunction:: int PyObject_TypeCheck(PyObject *o, PyTypeObject *type)

   オブジェクト *o* が、 *type* か *type* のサブタイプで あるときに真を返します。どちらのパラメタも *NULL*であってはなりません。

   .. versionadded:: 2.2


.. cfunction:: Py_ssize_t PyObject_Length(PyObject *o)
               Py_ssize_t PyObject_Size(PyObject *o)

   .. index:: builtin: len

   *o* の長さを返します。オブジェクト*o* がシーケンス型プロトコルと マップ型プロトコルの両方を提供している場合、シーケンスとしての長さを
   返します。エラーが生じると ``-1`` を返します。 Python の式 ``len(o)``と同じです。


.. cfunction:: PyObject* PyObject_GetItem(PyObject *o, PyObject *key)

   成功するとオブジェクト *key* に対応する *o* の要素を返し、 失敗すると *NULL* を返します。  Python の式 ``o[key]``
   と同じです。


.. cfunction:: int PyObject_SetItem(PyObject *o, PyObject *key, PyObject *v)

   オブジェクト *key* を値 *v* に対応付けます。 失敗すると ``-1`` を返します。 Python の文 ``o[key] = v`` と同じです。


.. cfunction:: int PyObject_DelItem(PyObject *o, PyObject *key)

   オブジェクト *o* から *key* に対する対応付けを削除します。 失敗すると ``-1`` を返します。 Python の文 ``del o[key]``
   と同じです。


.. cfunction:: int PyObject_AsFileDescriptor(PyObject *o)

   Python オブジェクトからファイル記述子を取り出します。 オブジェクトが整数か長整数なら、その値を返します。 (長)整数でない場合、オブジェクトに
   :meth:`fileno` メソッドがあれば 呼び出します; この場合、 :meth:`fileno` メソッドは
   整数または長整数をファイル記述子の値として返さなければなりません。 失敗すると ``-1`` を返します。


.. cfunction:: PyObject* PyObject_Dir(PyObject *o)

   この関数は Python の式 ``dir(o)`` と同じで、 オブジェクトの変数名に割り当てている文字列からなるリスト (空の場合もあります)
   を返します。エラーの場合には *NULL* を返します。引数を *NULL*にすると、Python における``dir()``
   と同様に、現在のローカルな名前を返します; この場合、 アクティブな実行フレームがなければ *NULL* を返しますが、
   :cfunc:`PyErr_Occurred` は偽を返します。


.. cfunction:: PyObject* PyObject_GetIter(PyObject *o)

   Python の式 ``iter(o)`` と同じです。 引数にとったオブジェクトに対する新たなイテレータか、
   オブジェクトがすでにイテレータの場合にはオブジェクト自身を 返します。オブジェクトが反復処理不可能であった場合には :exc:`TypeError` を送出して
   *NULL* を返します。


.. _number:

数値型プロトコル (number protocol)
==================================


.. cfunction:: int PyNumber_Check(PyObject *o)

   オブジェクト *o* が数値型プロトコルを提供している場合に ``1`` を返し、そうでないときには偽を返します。 この関数呼び出しは常に成功します。


.. cfunction:: PyObject* PyNumber_Add(PyObject *o1, PyObject *o2)

   成功すると*o1* と *o2* を加算した結果を返し、 失敗すると *NULL* を返します。 Python の式 ``o1 + o2`` と同じです。


.. cfunction:: PyObject* PyNumber_Subtract(PyObject *o1, PyObject *o2)

   成功すると*o1* から *o2* を減算した結果を返し、 失敗すると *NULL* を返します。 Python の式 ``o1 - o2`` と同じです。


.. cfunction:: PyObject* PyNumber_Multiply(PyObject *o1, PyObject *o2)

   成功すると*o1* と *o2* を乗算した結果を返し、失敗すると *NULL* を返します。 Python の式 ``o1 * o2`` と同じです。


.. cfunction:: PyObject* PyNumber_Divide(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した結果を返し, 失敗すると *NULL* を返します。  Python の式 ``o1 / o2`` と同じです。


.. cfunction:: PyObject* PyNumber_FloorDivide(PyObject *o1, PyObject *o2)

   成功すると*o1* を *o2* で除算した切捨て値を返し、 失敗すると *NULL* を返します。  "旧仕様の" 整数間での除算と同じです。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyNumber_TrueDivide(PyObject *o1, PyObject *o2)

   成功すると、数学的な *o1* の *o2* による除算値に対する 妥当な近似 (reasonable approximation) を返し、 失敗すると
   *NULL* を返します。 全ての実数を 2 を基数として表現するのは不可能なため、二進の浮動小数点数は "近似値"
   しか表現できません。このため、戻り値も近似になります。 この関数に二つの整数を渡した際、浮動小数点の値を返すことがあります。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyNumber_Remainder(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した剰余を返し、 失敗すると *NULL* を返します。 Python の式 ``o1 % o2`` と同じです。


.. cfunction:: PyObject* PyNumber_Divmod(PyObject *o1, PyObject *o2)

   .. index:: builtin: divmod

   組み込み関数 :func:`divmod` を参照してください。 失敗すると *NULL* を返します。 Python の式 ``divmod(o1,
   o2)`` と同じです。


.. cfunction:: PyObject* PyNumber_Power(PyObject *o1, PyObject *o2, PyObject *o3)

   .. index:: builtin: pow

   組み込み関数:func:`pow` を参照してください。 失敗すると *NULL* を返します。 Python の式 ``pow(o1, o2,
   o3)``と同じです。 *o3* はオプションです。 *o3* を無視させたいなら、 :cdata:`Py_None` を入れてください (*o3*
   に*NULL* を渡すと、不正なメモリアクセスを引き起こすことが あります)。


.. cfunction:: PyObject* PyNumber_Negative(PyObject *o)

   成功すると*o* の符号反転を返し、失敗すると *NULL* を返します。 Python の式 ``-o`` と同じです。


.. cfunction:: PyObject* PyNumber_Positive(PyObject *o)

   成功すると *o* を返し、失敗すると *NULL* を返します。 Python の式 ``+o`` と同じです。


.. cfunction:: PyObject* PyNumber_Absolute(PyObject *o)

   .. index:: builtin: abs

   成功すると *o* の絶対値を返し、失敗すると *NULL* を返します。 Python の式 ``abs(o)`` と同じです。


.. cfunction:: PyObject* PyNumber_Invert(PyObject *o)

   成功すると *o* のビット単位反転 (bitwise negation) を返し、 失敗すると *NULL* を返します。Python の式 ``~o``
   と同じです。


.. cfunction:: PyObject* PyNumber_Lshift(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* だけ左シフトした結果を返し、 失敗すると *NULL* を返します。 Python の式 ``o1 << o2``
   と同じです。


.. cfunction:: PyObject* PyNumber_Rshift(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* だけ右シフトした結果を返し、 失敗すると *NULL* を返します。 Python の式 ``o1 >> o2``
   と同じです。


.. cfunction:: PyObject* PyNumber_And(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位論理積 (bitwise and)" を返し、 失敗すると *NULL* を返します。 Python の式
   ``o1 & o2`` と同じです。


.. cfunction:: PyObject* PyNumber_Xor(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の  "ビット単位排他的論理和 (bitwise exclusive or)" を返し、 失敗すると *NULL*
   を返します。 Python の式 ``o1 ^ o2`` と同じです。


.. cfunction:: PyObject* PyNumber_Or(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位論理和 (bitwise or)" を返し 失敗すると *NULL* を返します。 Python の式
   ``o1 | o2`` と同じです。


.. cfunction:: PyObject* PyNumber_InPlaceAdd(PyObject *o1, PyObject *o2)

   成功すると*o1* と *o2* を加算した結果を返し、 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 += o2`` と同じです。


.. cfunction:: PyObject* PyNumber_InPlaceSubtract(PyObject *o1, PyObject *o2)

   成功すると*o1* から *o2* を減算した結果を返し、 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 -= o2`` と同じです。


.. cfunction:: PyObject* PyNumber_InPlaceMultiply(PyObject *o1, PyObject *o2)

   成功すると*o1* と *o2* を乗算した結果を返し、 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 *= o2`` と同じです。


.. cfunction:: PyObject* PyNumber_InPlaceDivide(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した結果を返し, 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 /= o2`` と同じです。


.. cfunction:: PyObject* PyNumber_InPlaceFloorDivide(PyObject *o1, PyObject *o2)

   成功すると*o1* を *o2* で除算した切捨て値を返し、 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 //= o2`` と同じです。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyNumber_InPlaceTrueDivide(PyObject *o1, PyObject *o2)

   成功すると、数学的な *o1* の *o2* による除算値に対する 妥当な近似 (reasonable approximation) を返し、 失敗すると
   *NULL* を返します。 全ての実数を 2 を基数として表現するのは不可能なため、二進の浮動小数点数は "近似値"
   しか表現できません。このため、戻り値も近似になります。 この関数に二つの整数を渡した際、浮動小数点の値を返すことがあります。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。

   .. versionadded:: 2.2


.. cfunction:: PyObject* PyNumber_InPlaceRemainder(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した剰余を返し、 , 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 %= o2`` と同じです。


.. cfunction:: PyObject* PyNumber_InPlacePower(PyObject *o1, PyObject *o2, PyObject *o3)

   .. index:: builtin: pow

   組み込み関数:func:`pow` を参照してください。 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 この関数は *o3* が :cdata:`Py_None` の場合は Python 文 ``o1
   **= o2`` と同じで、それ以外の場合は ``pow(o1, o2, o3)`` の in-place 版です。 *o3* を無視させたいなら、
   :cdata:`Py_None` を入れてください (*o3* に*NULL* を渡すと、不正なメモリアクセスを引き起こすことが あります)。


.. cfunction:: PyObject* PyNumber_InPlaceLshift(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* だけ左シフトした結果を返し、 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 <<= o2`` と同じです。


.. cfunction:: PyObject* PyNumber_InPlaceRshift(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* だけ右シフトした結果を返し、 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 >>= o2`` と同じです。


.. cfunction:: PyObject* PyNumber_InPlaceAnd(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位論理積 (bitwise and)" を返し、 失敗すると *NULL* を返します。  *o1* が
   *in-place* 演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 &= o2`` と同じです。


.. cfunction:: PyObject* PyNumber_InPlaceXor(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位排他的論理和  (bitwise exclusive or)" を返し、失敗すると *NULL*
   を返します。  *o1* が *in-place* 演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 ^= o2``
   と同じです。


.. cfunction:: PyObject* PyNumber_InPlaceOr(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位論理和 (bitwise or)" を返し 失敗すると *NULL* を返します。 *o1* が *in-
   place* 演算をサポートする場合、in-place 演算を 行います。 Python の文 ``o1 |= o2`` と同じです。


.. cfunction:: int PyNumber_Coerce(PyObject **p1, PyObject **p2)

   .. index:: builtin: coerce

   この関数は:ctype:`PyObject\*` 型の二つの変数のアドレスを引数にとります。 ``*p1`` と``*p2``
   が指すオブジェクトが同じ型の場合、 それぞれの参照カウントをインクリメントして ``0`` (成功) を返します。
   オブジェクトを変換して共通の数値型にできる場合、 ``*p1`` と ``*p2`` を変換後の値に置き換えて (参照カウントを '新しく' して)
   、``0`` を返します。 変換が不可能な場合や、その他何らかのエラーが生じた場合、``-1`` (失敗) を返し、参照カウントをインクリメントしません。
   ``PyNumber_Coerce(&o1, &o2)`` の呼び出しは Python 文 ``o1, o2 = coerce(o1, o2)`` と同じです。


.. cfunction:: PyObject* PyNumber_Int(PyObject *o)

   .. index:: builtin: int

   成功すると*o* を整数に変換したものを返し、 失敗すると *NULL* を返します。  引数の値が整数の範囲外の場合、長整数を代わりに返します。 Python
   の式 ``int(o)`` と同じです。


.. cfunction:: PyObject* PyNumber_Long(PyObject *o)

   .. index:: builtin: long

   成功すると*o* を長整数に変換したものを返し、 失敗すると *NULL* を返します。   Python の式 ``long(o)`` と同じです。


.. cfunction:: PyObject* PyNumber_Float(PyObject *o)

   .. index:: builtin: float

   成功すると*o* を浮動小数点数に変換したものを返し、 失敗すると *NULL* を返します。   Python の式 ``float(o)`` と同じです。


.. cfunction:: PyObject* PyNumber_Index(PyObject *o)

   *o*をPythonのintもしくはlong型に変換し、成功したらその値を、失敗したら *NULL*が返され、TypeError例外が送出されます。

   .. versionadded:: 2.5


.. cfunction:: Py_ssize_t PyNumber_AsSsize_t(PyObject *o, PyObject *exc)

   *o*を整数として解釈可能だった場合、Py_ssize_t型の値に変換して返します。
   もし*o*がPythonのintもしくはlongに変換できたのに、Py_ssize_tへの変換が
   :exc:`OverflowError`になる場合は、*exc*引数で渡された型
   (普通は:exc:`IndexError`か:exc:`OverflowError`) の例外を送出します。
   もし、*exc*が*NULL*なら、例外はクリアされて、値が負の場合は*PY_SSIZE_T_MIN*へ、
   正の場合は*PY_SSIZE_T_MAX*へと制限されます。

   .. versionadded:: 2.5


.. cfunction:: int PyIndex_Check(PyObject *o)

   *o*がインデックス整数であるときにTrueを返します。 (tp_as_number構造体のnb_indexスロットが埋まっている場合)

   .. versionadded:: 2.5


.. _sequence:

シーケンス型プロトコル (sequence protocol)
==========================================


.. cfunction:: int PySequence_Check(PyObject *o)

   オブジェクトがシーケンス型プロトコルを提供している場合に ``1`` を返し、 そうでないときには ``0`` を返します。 この関数呼び出しは常に成功します。


.. cfunction:: Py_ssize_t PySequence_Size(PyObject *o)

   .. index:: builtin: len

   成功するとシーケンス *o* 中のオブジェクトの数を返し、 失敗すると ``-1`` を返します。
   シーケンス型プロトコルをサポートしないオブジェクトに対しては、 Python の式 ``len(o)`` と同じ になります。


.. cfunction:: Py_ssize_t PySequence_Length(PyObject *o)

   :cfunc:`PySequence_Size` の別名です。


.. cfunction:: PyObject* PySequence_Concat(PyObject *o1, PyObject *o2)

   成功すると*o1* と *o2* の連結 (concatenation) を返し、 失敗すると *NULL* を返します。 Python の式 ``o1 +
   o2`` と同じです。


.. cfunction:: PyObject* PySequence_Repeat(PyObject *o, Py_ssize_t count)

   成功するとオブジェクト*o* の *count* 回繰り返しを返し、 失敗すると *NULL* を返します。 Python の式 ``o * count``
   と同じです。


.. cfunction:: PyObject* PySequence_InPlaceConcat(PyObject *o1, PyObject *o2)

   成功すると*o1* と *o2* の連結 (concatenation) を返し、 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の式 ``o1 += o2`` と同じです。


.. cfunction:: PyObject* PySequence_InPlaceRepeat(PyObject *o, Py_ssize_t count)

   成功するとオブジェクト*o* の *count* 回繰り返しを返し、 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を 行います。 Python の式 ``o *= count`` と同じです。


.. cfunction:: PyObject* PySequence_GetItem(PyObject *o, Py_ssize_t i)

   成功すると *o* の *i* 番目の要素を返し、 失敗すると *NULL* を返します。 Python の式 ``o[i]`` と同じです。


.. cfunction:: PyObject* PySequence_GetSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2)

   成功すると*o* の *i1* から *i2* までの間のスライスを返し、 失敗すると *NULL* を返します。 Python の式 ``o[i1:i2]``
   と同じです。


.. cfunction:: int PySequence_SetItem(PyObject *o, int Py_ssize_t, PyObject *v)

   *o* の *i* 番目の要素に *v* を代入します。 失敗すると ``-1`` を返します。 Python の文 ``o[i] = v`` と同じです。
   この関数は *v* への参照を盗み取り*ません*。


.. cfunction:: int PySequence_DelItem(PyObject *o, Py_ssize_t i)

   *o* の *i* 番目の要素を削除します。 失敗すると ``-1`` を返します。 Python の文 ``del o[i]`` と同じです。


.. cfunction:: int PySequence_SetSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2, PyObject *v)

   *o* の *i1* から *i2* までの間のスライスに *v* を代入します。 Python の文 ``o[i1:i2] = v`` と同じです。


.. cfunction:: int PySequence_DelSlice(PyObject *o, int Py_ssize_t, int Py_ssize_t)

   シーケンスオブジェクト *o* の *i1* から *i2* までの間の スライスを削除します。失敗すると ``-1`` を返します。 Python の文
   ``del o[i1:i2]`` と同じです。


.. cfunction:: int PySequence_Count(PyObject *o, PyObject *value)

   *o* における *value* の出現回数、すなわち  ``o[key] == value`` となる *key* の個数を 返します。失敗すると
   ``-1`` を返します。 Python の式 ``o.count(value)`` と同じです。


.. cfunction:: int PySequence_Contains(PyObject *o, PyObject *value)

   *o* に*value* が入っているか判定します。 *o* のある要素が *value* と等価 (equal) ならば``1`` を
   返し、それ以外の場合には ``0`` を返します。 エラーが発生すると ``-1`` を返します。 Python の式 ``value in o``
   と同じです。


.. cfunction:: int PySequence_Index(PyObject *o, PyObject *value)

   ``o[i] == value`` となる最初に見つかったインデクス *i* を返します。 エラーが発生すると ``-1`` を返します。 Python の式
   ``o.index(value)`` と同じです。


.. cfunction:: PyObject* PySequence_List(PyObject *o)

   任意のシーケンス *o* と同じ内容を持つリストオブジェクトを返します。 返されるリストは必ず新しいリストオブジェクトになります。


.. cfunction:: PyObject* PySequence_Tuple(PyObject *o)

   .. index:: builtin: tuple

   任意のシーケンス *o* と同じ内容を持つタプルオブジェクトを返します。 失敗したら*NULL*を返します。 *o* がタプルの場合、新たな参照を返します。
   それ以外の場合、適切な内容が入ったタプルを構築して返します。 Pythonの式 ``tuple(o)`` と同じです。


.. cfunction:: PyObject* PySequence_Fast(PyObject *o, const char *m)

   シーケンス *o* がすでにタプルやリストであれば *o* を返し、 そうでなければ *o* をタプルで返します。 返されるタプルのメンバにアクセスするには
   :cfunc:`PySequence_Fast_GET_ITEM` を使ってください。 失敗すると *NULL* を返します。
   オブジェクトがシーケンスでなければ、*m* がメッセージテキストに なっている:exc:`TypeError` を送出します。


.. cfunction:: PyObject* PySequence_Fast_GET_ITEM(PyObject *o, Py_ssize_t i)

   *o* が*NULL*でなく、:cfunc:`PySequence_Fast` が返した オブジェクトであり、かつ*i* がインデクスの範囲内にあると
   仮定して、*o* の *i* 番目の要素を返します。


.. cfunction:: PyObject** PySequence_Fast_ITEMS(PyObject *o)

   PyObject ポインタの背後にあるアレイを返します．この関数では，*o* は :cfunc:`PySequence_Fast` の返したオブジェクトであり，
   *NULL*でないものと仮定しています．

   .. versionadded:: 2.4


.. cfunction:: PyObject* PySequence_ITEM(PyObject *o, Py_ssize_t i)

   成功すると the *i*th element of *o* を返し、 失敗すると *NULL* を返します。
   :cfunc:`PySequence_GetItem` ですが、 :cfunc:`PySequence_Check(o)` が真になるかチェックせず、
   負のインデクスに対する調整を行いません。

   .. versionadded:: 2.3


.. cfunction:: int PySequence_Fast_GET_SIZE(PyObject *o)

   *o* が*NULL*でなく、:cfunc:`PySequence_Fast` が返した オブジェクトであると仮定して、*o* の長さを返します。 *o*
   のサイズは:cfunc:`PySequence_Size` を呼び出しても 得られますが、:cfunc:`PySequence_Fast_GET_SIZE`
   の方が *o* をリストかタプルであると仮定して処理するため、より高速です。


.. _mapping:

マップ型プロトコル (mapping protocol)
=====================================


.. cfunction:: int PyMapping_Check(PyObject *o)

   オブジェクトがマップ型プロトコルを提供している場合に ``1`` を返し、 そうでないときには ``0`` を返します。 この関数呼び出しは常に成功します。


.. cfunction:: Py_ssize_t PyMapping_Length(PyObject *o)

   .. index:: builtin: len

   成功するとオブジェクト *o* 中のキーの数を返し、 失敗すると ``-1`` を返します。 マップ型プロトコルを提供していないオブジェクトに対しては、
   Python の式 ``len(o)`` と同じ になります。


.. cfunction:: int PyMapping_DelItemString(PyObject *o, char *key)

   オブジェクト *o* から *key* に関する対応付けを削除します。 失敗すると ``-1`` を返します。 Python の文 ``del o[key]``
   と同じです。


.. cfunction:: int PyMapping_DelItem(PyObject *o, PyObject *key)

   オブジェクト *o* から *key* に対する対応付けを削除します。 失敗すると ``-1`` を返します。 Python の文 ``del o[key]``
   と同じです。


.. cfunction:: int PyMapping_HasKeyString(PyObject *o, char *key)

   成功すると、マップ型オブジェクトがキー *key* を持つ場合に ``1`` を返し、そうでないときには ``0`` を返します。 Python の式
   ``o.has_key(key)`` と同じです。 この関数呼び出しは常に成功します。


.. cfunction:: int PyMapping_HasKey(PyObject *o, PyObject *key)

   マップ型オブジェクトがキー *key* を持つ場合に ``1`` を返し、 そうでないときには ``0`` を返します。 Python の式
   ``o.has_key(key)`` と同じです。 この関数呼び出しは常に成功します。


.. cfunction:: PyObject* PyMapping_Keys(PyObject *o)

   成功するとオブジェクト *o* のキーからなるリストを返します。 失敗すると *NULL*を返します。 Python の式 ``o.keys()``
   と同じです。


.. cfunction:: PyObject* PyMapping_Values(PyObject *o)

   成功するとオブジェクト *o* のキーに対応する値からなるリストを返します。 失敗すると *NULL*を返します。 Python の式
   ``o.values()`` と同じです。


.. cfunction:: PyObject* PyMapping_Items(PyObject *o)

   成功するとオブジェクト *o* の要素対、すなわちキーと値のペアが 入ったタプルからなるリストを返します。 失敗すると *NULL*を返します。 Python
   の式 ``o.items()`` と同じです。


.. cfunction:: PyObject* PyMapping_GetItemString(PyObject *o, char *key)

   オブジェクト *key* に対応する*o* の要素を返します。 失敗すると *NULL*を返します。 Python の式 ``o[key]`` と同じです。


.. cfunction:: int PyMapping_SetItemString(PyObject *o, char *key, PyObject *v)

   オブジェクト*o* で *key* を値 *v* に対応付けます。 失敗すると ``-1`` を返します。 Python の文 ``o[key] = v``
   と同じです。


.. _iterator:

イテレータプロトコル (iterator protocol)
========================================

.. versionadded:: 2.2

イテレータを扱うための固有の関数は二つしかありません。


.. cfunction:: int PyIter_Check(PyObject *o)

   *o* がイテレータプロトコルをサポートする場合に真を返します。


.. cfunction:: PyObject* PyIter_Next(PyObject *o)

   反復処理 *o* における次の値を返します。オブジェクトが イテレータの場合、この関数は反復処理における次の値を取り出します。
   要素が何も残っていない場合には例外がセットされていない状態で *NULL* を 返します。オブジェクトがイテレータでない場合には
   :exc:`TypeError` を送出します。要素を取り出す際にエラーが生じると *NULL* を返し、 発生した例外を送出します。

イテレータの返す要素にわたって反復処理を行うループを書くと、 C のコードは以下のようになるはずです::

   PyObject *iterator = PyObject_GetIter(obj);
   PyObject *item;

   if (iterator == NULL) {
       /* エラーの伝播処理をここに書く */
   }

   while (item = PyIter_Next(iterator)) {
       /* 取り出した要素で何らかの処理を行う */
       ...
       /* 終わったら参照を放棄する */
       Py_DECREF(item);
   }

   Py_DECREF(iterator);

   if (PyErr_Occurred()) {
       /* エラーの伝播処理をここに書く */
   }
   else {
       /* 別の処理を続ける */
   }


.. _abstract-buffer:

バッファプロトコル (buffer protocol)
====================================


.. cfunction:: int PyObject_AsCharBuffer(PyObject *obj, const char **buffer, Py_ssize_t *buffer_len)

   文字ベースの入力として使える読み出し専用メモリ上の位置へのポインタを 返します。*obj* 引数は単一セグメントからなる
   文字バッファインタフェースをサポートしていなければなりません。 成功すると ``0``を返し、*buffer* をメモリの位置に、  *buffer_len*
   をバッファの長さに設定します。エラーの際には  ``-1`` を返し、:exc:`TypeError` をセットします。

   .. versionadded:: 1.6


.. cfunction:: int PyObject_AsReadBuffer(PyObject *obj, const void **buffer, Py_ssize_t *buffer_len)

   任意のデータを収めた読み出し専用のメモリ上の位置へのポインタを 返します。*obj* 引数は単一セグメントからなる読み出し可能
   バッファインタフェースをサポートしていなければなりません。 成功すると ``0``を返し、*buffer* をメモリの位置に、  *buffer_len*
   をバッファの長さに設定します。エラーの際には  ``-1`` を返し、:exc:`TypeError` をセットします。

   .. versionadded:: 1.6


.. cfunction:: int PyObject_CheckReadBuffer(PyObject *o)

   *o* が単一セグメントからなる読み出し可能バッファインタフェース をサポートしている場合に ``1`` を返します。それ以外の場合には ``0``
   を返します。

   .. versionadded:: 2.2


.. cfunction:: int PyObject_AsWriteBuffer(PyObject *obj, void **buffer, Py_ssize_t *buffer_len)

   書き込み可能なメモリ上の位置へのポインタを返します。*obj*  引数は単一セグメントからなる文字バッファインタフェース
   をサポートしていなければなりません。成功すると ``0``を返し、 *buffer* をメモリの位置に、 *buffer_len* をバッファの
   長さに設定します。エラーの際には ``-1`` を返し、 :exc:`TypeError` をセットします。

   .. versionadded:: 1.6

