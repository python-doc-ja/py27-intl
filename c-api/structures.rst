.. highlightlang:: c

.. _common-structs:

共通のオブジェクト構造体 (common object structure)
==================================================

Python では、オブジェクト型を定義する上で数多くの構造体が使われます。この節では三つの構造体とその利用方法について説明します。

全ての Python オブジェクトは、オブジェクトのメモリ内表現の先頭部分にある少数のフィールドを完全に共有しています。このフィールドは
:ctype:`PyObject` および :ctype:`PyVarObject` 型で表現されます。 :ctype:`PyObject` 型や
:ctype:`PyVarObject` 型もまた、他の全ての Python  オブジェクトを定義する上で直接的・間接的に使われているマクロを
使って定義されています。


.. ctype:: PyObject

   全てのオブジェクト型はこの型を拡張したものです。この型には、あるオブジェクトに対するオブジェクトとしてのポインタを Python
   から扱う必要がある際に必要な情報が入っています。通常に "リリースされている" ビルドでは、この構造体にはオブジェクトの
   参照カウントと、オブジェクトに対応する型オブジェクトだけが入っています。

   ``PyObject_HEAD`` マクロ展開で定義されているフィールドに対応します。


.. ctype:: PyVarObject

   :ctype:`PyObject` を拡張して、 :attr:`ob_size` フィールドを追加したものです。この構造体は、 *長さ (length)*
   の概念を持つオブジェクトだけに対して使います。この型が Python/C API で使われることはほとんどありません。
   ``PyObject_VAR_HEAD`` マクロ展開で定義されているフィールドに対応します。

:ctype:`PyObject` および :ctype:`PyVarObject` の定義には以下のマクロが使われています:


.. cmacro:: PyObject_HEAD

   :ctype:`PyObject` 型のフィールド宣言に展開されるマクロです;  可変でない長さを持つオブジェクトを表現する新たな型を宣言する
   場合に使います。展開によってどのフィールドが宣言されるかは、 :cmacro:`Py_TRACE_REFS` の定義に依存します。
   デフォルトでは、 :cmacro:`Py_TRACE_REFS` は定義されておらず、 :cmacro:`PyObject_HEAD`
   は以下のコードに展開されます::

      Py_ssize_t ob_refcnt;
      PyTypeObject *ob_type;

   :cmacro:`Py_TRACE_REFS` が定義されている場合、以下のように展開されます::

      PyObject *_ob_next, *_ob_prev;
      Py_ssize_t ob_refcnt;
      PyTypeObject *ob_type;


.. cmacro:: PyObject_VAR_HEAD

   マクロです。 :ctype:`PyVarObject` 型のフィールド宣言に展開されるマクロです;
   インスタンスによって可変の長さを持つオブジェクトを表現する新たな型を宣言する場合に使います。マクロは常に以下のように展開されます::

      PyObject_HEAD
      Py_ssize_t ob_size;

   マクロ展開結果の一部に :cmacro:`PyObject_HEAD` が含まれており、 :cmacro:`PyObject_HEAD`
   の展開結果は :cmacro:`Py_TRACE_REFS` の定義に依存します。


.. cmacro:: PyObject_HEAD_INIT


.. ctype:: PyCFunction

   ほとんどの Python の呼び出し可能オブジェクトを C で実装する際に用いられている関数の型です。この型の関数は二つの
   :ctype:`PyObject\*` 型パラメタをとり、 :ctype:`PyObject\*` 型の値を返します。戻り値を *NULL* にする場合、
   例外をセットしておかなければなりません。 *NULL* でない値を返す場合、戻り値は Python に関数の戻り値として公開される値として解釈されます。
   この型の関数は新たな参照を返さなければなりません。


.. ctype:: PyMethodDef

   拡張型のメソッドを記述する際に用いる構造体です。この構造体には 4 つのフィールドがあります:

   +------------------+-------------+----------------------------------------------+
   | フィールド       | C データ型  | 意味                                         |
   +==================+=============+==============================================+
   | :attr:`ml_name`  | char \*     | メソッド名                                   |
   +------------------+-------------+----------------------------------------------+
   | :attr:`ml_meth`  | PyCFunction | C 実装へのポインタ                           |
   +------------------+-------------+----------------------------------------------+
   | :attr:`ml_flags` | int         | 呼び出しをどのように行うかを示すフラグビット |
   +------------------+-------------+----------------------------------------------+
   | :attr:`ml_doc`   | char \*     | docstring の内容を指すポインタ               |
   +------------------+-------------+----------------------------------------------+

:attr:`ml_meth` は C の関数ポインタです。関数は別の型で定義されていてもかまいませんが、常に  :ctype:`PyObject\*`
を返します。関数が :ctype:`PyFunction` でない場合、メソッドテーブル内でキャストを行うようコンパイラが要求することになるでしょう。
:ctype:`PyCFunction` では最初のパラメタが :ctype:`PyObject\*` 型であると定義していますが、固有の C 型を
*self* オブジェクトに使う実装はよく行われています。

:attr:`ml_flags` フィールドはビットフィールドで、以下のフラグが入ります。個々のフラグは呼び出し規約 (calling convention)
や束縛規約 (binding convention) を表します。呼び出し規約フラグでは、 :const:`METH_VARARGS` および
:const:`METH_KEYWORDS` を組み合わせられます (ただし、 :const:`METH_KEYWORDS` 単体の指定を行っても
``METH_VARARGS | METH_KEYWORDS`` と同じなので注意してください)。呼び出し規約フラグは束縛フラグと組み合わせられます。


.. data:: METH_VARARGS

   :ctype:`PyCFunction` 型のメソッドで典型的に使われる呼び出し規約です。関数は :ctype:`PyObject\*`
   型の引数値を二つ要求します。最初の引数はメソッドの *self* オブジェクトです; モジュール関数の場合、 :cfunc:`Py_InitModule4`
   に与えることになる値が入ります (*NULL* にすると :cfunc:`Py_InitModule` が使われます)。第二のパラメタ (よく *args*
   と呼ばれます) は、全ての引数を表現するタプルオブジェクトです。パラメタは通常、 :cfunc:`PyArg_ParseTuple` や
   :cfunc:`PyArg_UnpackTuple` で処理されます。


.. data:: METH_KEYWORDS

   このフラグを持つメソッドは :ctype:`PyCFunctionWithKeywords`
   型でなければなりません。 :ctype:`PyCFunctionWithKeywords` は三つのパラメタ:*self* 、 *args* 、
   およびキーワード引数全てからなる辞書、を要求します。このフラグは通常 :const:`METH_VARARGS` と組み合わされ、パラメタは
   :cfunc:`PyArg_ParseTupleAndKeywords` で処理されます。


.. data:: METH_NOARGS

   引数のないメソッドは、 :const:`METH_NOARGS` フラグをつけた場合、必要な引数が指定されているかをチェックしなくなります。こうしたメソッドは
   :ctype:`PyCFunction` 型でなくてはなりません。オブジェクトのメソッドに使った場合、第一のパラメタは ``self``
   になり、オブジェクトインスタンスへの参照を保持することになります。いずれにせよ、第二のパラメタは *NULL* になります。


.. data:: METH_O

   単一のオブジェクト引数だけをとるメソッドは、 :cfunc:`PyArg_ParseTuple` を引数 ``"O"`` にして呼び出す代わりに、
   :const:`METH_O` フラグつきで指定できます。メソッドは :ctype:`PyCFunction` 型で、 *self*
   パラメタと単一の引数を表現する :ctype:`PyObject\*` パラメタを伴います。


.. data:: METH_OLDARGS

   この呼び出し規約は撤廃されました。メソッドは :ctype:`PyCFunction` 型でなければなりません。第二引数は、引数がない場合には
   *NULL* 、単一の引数の場合にはその引数オブジェクト、複数個の引数の場合には引数オブジェクトからなるタプルです。この呼び出し規約を使うと、複数個の
   引数の場合と、単一のタプルが唯一引数の場合を区別できなくなってしまいます。

以下の二つの定数は、呼び出し規約を示すものではなく、クラスのメソッドとして使う際の束縛方式を示すものです。
モジュールに対して定義された関数で用いてはなりません。メソッドに対しては、最大で一つしかこのフラグをセットできません。


.. data:: METH_CLASS

   .. index:: builtin: classmethod

   メソッドの最初の引数には、型のインスタンスではなく型オブジェクトが渡されます。このフラグは組み込み関数 :func:`classmethod`
   を使って生成するのと同じ *クラスメソッド (class method)* を生成するために使われます。

   .. versionadded:: 2.3


.. data:: METH_STATIC

   .. index:: builtin: staticmethod

   メソッドの最初の引数には、型のインスタンスではなく *NULL* が渡されます。このフラグは、 :func:`staticmethod`
   を使って生成するのと同じ *静的メソッド (static method)* を生成するために使われます。

   .. versionadded:: 2.3

もう一つの定数は、あるメソッドを同名の別のメソッド定義と置き換えるかどうかを制御します。


.. data:: METH_COEXIST

   メソッドを既存の定義を置き換える形でロードします。 *METH_COEXIST* を指定しなければ、デフォルトの設定にしたがって、
   定義が重複しないようスキップします。スロットラッパはメソッドテーブルよりも前にロードされるので、例えば *sq_contains* スロットは
   ラップしているメソッド :meth:`__contains__` を生成し、同名の PyCFunction のロードを阻止します。このフラグを定義すると、
   PyCFunction はラッパオブジェクトを置き換える形でロードされ、スロットと連立します。 PyCFunctions の呼び出しはラッパオブジェクトの
   呼び出しよりも最適化されているので、こうした仕様が便利になります。

   .. versionadded:: 2.4


.. cfunction:: PyObject* Py_FindMethod(PyMethodDef table[], PyObject *ob, char *name)

   C で実装された拡張型の束縛メソッドオブジェクトを返します。 :cfunc:`PyObject_GenericGetAttr` 関数を使わない
   :attr:`tp_getattro` や :attr:`tp_getattr` ハンドラを実装する際に便利です。

