.. highlightlang:: c


.. _newtypes:

********************************************************
オブジェクト実装サポート (object implementation support)
********************************************************

この章では、新しいオブジェクト型 (new object type) を定義する際に 使われる関数、型、およびマクロについて説明します。


.. _allocating-objects:

オブジェクトをヒープ上にメモリ確保する
======================================


.. cfunction:: PyObject* _PyObject_New(PyTypeObject *type)


.. cfunction:: PyVarObject* _PyObject_NewVar(PyTypeObject *type, Py_ssize_t size)


.. cfunction:: void _PyObject_Del(PyObject *op)


.. cfunction:: PyObject* PyObject_Init(PyObject *op, PyTypeObject *type)

   新たにメモリ確保されたオブジェクト *op* に対し、型と初期状態での 参照 (initial reference) を初期化します。
   初期化されたオブジェクトを返します。*type* からそのオブジェクトが 循環参照ガベージ検出の機能を有する場合、検出機構が監視対象とする
   オブジェクトのセットに追加されます。 オブジェクトの他のフィールドには影響を及ぼしません。


.. cfunction:: PyVarObject* PyObject_InitVar(PyVarObject *op, PyTypeObject *type, Py_ssize_t size)

   :cfunc:`PyObject_Init` の全ての処理を行い、可変サイズオブジェクト の場合には長さ情報も初期化します。


.. cfunction:: TYPE* PyObject_New(TYPE, PyTypeObject *type)

   C 構造体型 *TYPE* と Python 型オブジェクト *type* を使って 新たな Python オブジェクトをメモリ確保します。 Python
   オブジェクトヘッダで定義されていないフィールドは初期化されません; オブジェクトの参照カウントは 1 になります。メモリ確保のサイズは 型オブジェクトの
   :attr:`tp_basicsize` で決定します。


.. cfunction:: TYPE* PyObject_NewVar(TYPE, PyTypeObject *type, Py_ssize_t size)

   C 構造体型 *TYPE* と Python 型オブジェクト *type* を使って 新たな Python オブジェクトをメモリ確保します。 Python
   オブジェクトヘッダで定義されていないフィールドは初期化されません。 確保されたメモリは、*TYPE* 構造体に加え、vartype の
   :attr:`tp_itemsize` フィールドで指定されているサイズ中の *size* フィールドを
   収容できます。この関数は、例えばタプルのように生成時にサイズを決定 できるオブジェクトを実装する際に便利です。一連の複数のフィールドに
   対するアロケーション操作を一つにして埋め込むと、アロケーション回数 が減り、メモリ管理の処理効率が向上します。


.. cfunction:: void PyObject_Del(PyObject *op)

   :cfunc:`PyObject_New` や :cfunc:`PyObject_NewVar` で
   確保されたメモリを解放します。この関数は、通常オブジェクトの型に 指定されている :attr:`tp_dealloc` ハンドラ内で呼び出します。
   この関数を呼び出した後では、オブジェクトのメモリ領域はもはや有効な Python オブジェクトを表現してはいないので、オブジェクトのフィールド
   に対してアクセスしてはなりません。


.. cfunction:: PyObject* Py_InitModule(char *name, PyMethodDef *methods)

   *name* と関数のテーブルに基づいて新たなモジュールオブジェクトを 生成し、生成されたモジュールオブジェクトを返します。

   .. versionchanged:: 2.3
      以前のバージョンの Python では、*methods* 引数の 値として*NULL* をサポートしていませんでした.


.. cfunction:: PyObject* Py_InitModule3(char *name, PyMethodDef *methods, char *doc)

   *name* と関数のテーブルに基づいて新たなモジュールオブジェクトを 生成し、生成されたモジュールオブジェクトを返します。 *doc* が
   *NULL*でない場合、モジュールの docstring として 使われます。

   .. versionchanged:: 2.3
      以前のバージョンの Python では、*methods* 引数の 値として*NULL* をサポートしていませんでした.


.. cfunction:: PyObject* Py_InitModule4(char *name, PyMethodDef *methods, char *doc, PyObject *self, int apiver)

   *name* と関数のテーブルに基づいて新たなモジュールオブジェクトを 生成し、生成されたモジュールオブジェクトを返します。 *doc* が
   *NULL*でない場合、モジュールの docstring として 使われます。*self* が*NULL*でない場合、モジュール内の各関数
   の第一引数として渡されます (*NULL*の時には第一引数も *NULL*になります)。 (この関数は実験的な機能のために追加されたもので、現在の Python
   の バージョンで使われてはいないはずです。) *apiver* に渡してよい値は、 :const:`PYTHON_API_VERSION`
   で定義されている定数だけです。

   .. note::

      この関数のほとんどの用途は、代わりに:cfunc:`Py_InitModule3` を使えるはずです; 本当にこの関数を使いたいときにだけ利用してください

   .. versionchanged:: 2.3
      以前のバージョンの Python では、*methods* 引数の 値として*NULL* をサポートしていませんでした.


.. cvar:: PyObject _Py_NoneStruct

   Python からは ``None`` に見えるオブジェクトです。この値への アクセスは、このオブジェクトへのポインタを評価する``Py_None``
   マクロを使わねばなりません。


.. _common-structs:

共通のオブジェクト構造体 (common object structure)
==================================================

Python では、オブジェクト型を定義する上で数多くの構造体が使われます。 この節では三つの構造体とその利用方法について説明します。

全ての Python オブジェクトは、オブジェクトのメモリ内表現の先頭部分に ある少数のフィールドを完全に共有しています。このフィールドは
:ctype:`PyObject` および :ctype:`PyVarObject` 型で表現されます。 :ctype:`PyObject` 型や
:ctype:`PyVarObject` 型もまた、他の全ての Python  オブジェクトを定義する上で直接的・間接的に使われているマクロを
使って定義されています。


.. ctype:: PyObject

   全てのオブジェクト型はこの型を拡張したものです。 この型には、あるオブジェクトに対するオブジェクトとしてのポインタを Python
   から扱う必要がある際に必要な情報が入っています。 通常に "リリースされている" ビルドでは、この構造体にはオブジェクトの
   参照カウントと、オブジェクトに対応する型オブジェクトだけが入っています。

   ``PyObject_HEAD`` マクロ展開で定義されているフィールドに対応します。


.. ctype:: PyVarObject

   :ctype:`PyObject` を拡張して、:attr:`ob_size` フィールドを追加した ものです。この構造体は、*長さ (length)*
   の概念を持つオブジェクト だけに対して使います。この型が Python/C API で使われることは ほとんどありません。
   ``PyObject_VAR_HEAD`` マクロ展開で定義されているフィールドに対応します。

:ctype:`PyObject` および :ctype:`PyVarObject` の定義には以下のマクロが 使われています:


.. cmacro:: PyObject_HEAD

   :ctype:`PyObject` 型のフィールド宣言に展開されるマクロです;  可変でない長さを持つオブジェクトを表現する新たな型を宣言する
   場合に使います。展開によってどのフィールドが宣言されるかは、 :cmacro:`Py_TRACE_REFS` の定義に依存します。
   デフォルトでは、:cmacro:`Py_TRACE_REFS` は定義されておらず、 :cmacro:`PyObject_HEAD`
   は以下のコードに展開されます::

      Py_ssize_t ob_refcnt;
      PyTypeObject *ob_type;

   :cmacro:`Py_TRACE_REFS` が定義されている場合、以下のように展開 されます::

      PyObject *_ob_next, *_ob_prev;
      Py_ssize_t ob_refcnt;
      PyTypeObject *ob_type;


.. cmacro:: PyObject_VAR_HEAD

   マクロです。:ctype:`PyVarObject` 型のフィールド宣言に展開されるマクロです;
   インスタンスによって可変の長さを持つオブジェクトを表現する新たな型を 宣言する場合に使います。マクロは常に以下のように展開されます::

      PyObject_HEAD
      Py_ssize_t ob_size;

   マクロ展開結果の一部に:cmacro:`PyObject_HEAD` が含まれており、 :cmacro:`PyObject_HEAD`
   の展開結果は:cmacro:`Py_TRACE_REFS` の定義に依存します。


.. cmacro:: PyObject_HEAD_INIT


.. ctype:: PyCFunction

   ほとんどの Python の呼び出し可能オブジェクトを C で実装する際に 用いられている関数の型です。 この型の関数は二つの
   :ctype:`PyObject\*` 型パラメタをとり、 :ctype:`PyObject\*` 型の値を返します。戻り値を *NULL*にする場合、
   例外をセットしておかなければなりません。*NULL*でない値を返す場合、 戻り値は Python に関数の戻り値として公開される値として解釈されます。
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

:attr:`ml_meth` は C の関数ポインタです。関数は別の型で定義 されていてもかまいませんが、常に  :ctype:`PyObject\*`
を返します。 関数が :ctype:`PyFunction` でない場合、メソッドテーブル内でキャスト を行うようコンパイラが要求することになるでしょう。
:ctype:`PyCFunction` では最初のパラメタが:ctype:`PyObject\*` 型で あると定義していますが、固有の C 型を
*self* オブジェクトに 使う実装はよく行われています。

:attr:`ml_flags` フィールドはビットフィールドで、以下のフラグが入ります。 個々のフラグは呼び出し規約 (calling convention)
や束縛規約 (binding convention) を表します。 呼び出し規約フラグでは、:const:`METH_VARARGS` および
:const:`METH_KEYWORDS` を組み合わせられます (ただし、 :const:`METH_KEYWORDS` 単体の指定を行っても
``METH_VARARGS | METH_KEYWORDS`` と 同じなので注意してください)。 呼び出し規約フラグは束縛フラグと組み合わせられます。


.. data:: METH_VARARGS

   :ctype:`PyCFunction` 型のメソッドで典型的に使われる呼び出し規約です。 関数は:ctype:`PyObject\*`
   型の引数値を二つ要求します。最初の引数は メソッドの *self* オブジェクトです; モジュール関数の場合、 :cfunc:`Py_InitModule4`
   に与えることになる値が入ります (*NULL* にすると:cfunc:`Py_InitModule` が使われます)。 第二のパラメタ (よく *args*
   と呼ばれます) は、全ての引数を 表現するタプルオブジェクトです。パラメタは通常、 :cfunc:`PyArg_ParseTuple` や
   :cfunc:`PyArg_UnpackTuple` で処理されます。


.. data:: METH_KEYWORDS

   このフラグを持つメソッドは:ctype:`PyCFunctionWithKeywords`
   型でなければなりません。:ctype:`PyCFunctionWithKeywords` は 三つのパラメタ:*self*、 *args*、
   およびキーワード引数 全てからなる辞書、を要求します。このフラグは通常 :const:`METH_VARARGS` と組み合わされ、パラメタは
   :cfunc:`PyArg_ParseTupleAndKeywords` で処理されます。


.. data:: METH_NOARGS

   引数のないメソッドは、:const:`METH_NOARGS` フラグをつけた場合、 必要な引数が指定されているかをチェックしなくなります。 こうしたメソッドは
   :ctype:`PyCFunction` 型でなくてはなりません。 オブジェクトのメソッドに使った場合、第一のパラメタは ``self``
   になり、オブジェクトインスタンスへの参照を保持することになります。 いずれにせよ、第二のパラメタは *NULL*になります。


.. data:: METH_O

   単一のオブジェクト引数だけをとるメソッドは、 :cfunc:`PyArg_ParseTuple` を引数 ``"O"`` にして呼び出す代わりに、
   :const:`METH_O` フラグつきで指定できます。メソッドは :ctype:`PyCFunction` 型で、*self*
   パラメタと単一の引数を表現する :ctype:`PyObject\*` パラメタを伴います。


.. data:: METH_OLDARGS

   この呼び出し規約は撤廃されました。メソッドは:ctype:`PyCFunction` 型で なければなりません。第二引数は、引数がない場合には
   *NULL*、単一の 引数の場合にはその引数オブジェクト、複数個の引数の場合には引数 オブジェクトからなるタプルです。この呼び出し規約を使うと、複数個の
   引数の場合と、単一のタプルが唯一引数の場合を区別できなくなってしまいます。

以下の二つの定数は、呼び出し規約を示すものではなく、 クラスのメソッドとして使う際の束縛方式を示すものです。
モジュールに対して定義された関数で用いてはなりません。 メソッドに対しては、最大で一つしかこのフラグをセットできません。


.. data:: METH_CLASS

   .. index:: builtin: classmethod

   メソッドの最初の引数には、型のインスタンスではなく型オブジェクト が渡されます。このフラグは 組み込み関数 :func:`classmethod`
   を使って生成するのと同じ*クラスメソッド (class method)* を生成するために使われます。

   .. versionadded:: 2.3


.. data:: METH_STATIC

   .. index:: builtin: staticmethod

   メソッドの最初の引数には、型のインスタンスではなく *NULL* が 渡されます。このフラグは、 :func:`staticmethod`
   を使って生成するのと同じ*静的メソッド (static method)* を生成するために使われます。

   .. versionadded:: 2.3

もう一つの定数は、あるメソッドを同名の別のメソッド定義と置き換えるか どうかを制御します。


.. data:: METH_COEXIST

   メソッドを既存の定義を置き換える形でロードします。 *METH_COEXIST* を指定しなければ、デフォルトの設定にしたがって、
   定義が重複しないようスキップします。スロットラッパはメソッドテーブル よりも前にロードされるので、例えば *sq_contains* スロットは
   ラップしているメソッド :meth:`__contains__` を生成し、同名の PyCFunction のロードを阻止します。このフラグを定義すると、
   PyCFunction はラッパオブジェクトを置き換える形でロードされ、 スロットと連立します。 PyCFunctions の呼び出しはラッパオブジェクトの
   呼び出しよりも最適化されているので、こうした仕様が便利になります。

   .. versionadded:: 2.4


.. cfunction:: PyObject* Py_FindMethod(PyMethodDef table[], PyObject *ob, char *name)

   C で実装された拡張型の束縛メソッドオブジェクトを返します。 :cfunc:`PyObject_GenericGetAttr` 関数を使わない
   :attr:`tp_getattro` や :attr:`tp_getattr` ハンドラを実装する際に 便利です。


.. _type-structs:

型オブジェクト
==============

新スタイルの型を定義する構造体: :ctype:`PyTypeObject` 構造体は、おそらく Python
オブジェクトシステムの中で最も重要な構造体の一つでしょう。 型オブジェクトは:cfunc:`PyObject_\*` 系や :cfunc:`PyType_\*`
系の関数で扱えますが、ほとんどの Python アプリケーションにとって、 さして面白みのある機能を提供しません。
とはいえ、型オブジェクトはオブジェクトがどのように振舞うかを決める 基盤ですから、インタプリタ自体や新たな型を定義する拡張モジュールでは 非常に重要な存在です。

型オブジェクトは標準の型 (standard type) に比べるとかなり大きな 構造体です。その理由は、型オブジェクトがある型の様々な機能を実現する
小さな機能単位を実装した C 関数へのポインタが大部分を占めるような 多数の値を保持しているからです。この節では、型オブジェクトの各
フィールドについて詳細を説明します。各フィールドは、構造体内で 出現する順番に説明されています。

Typedefs: unaryfunc, binaryfunc, ternaryfunc, inquiry, coercion, intargfunc,
intintargfunc, intobjargproc, intintobjargproc, objobjargproc, destructor,
freefunc, printfunc, getattrfunc, getattrofunc, setattrfunc, setattrofunc,
cmpfunc, reprfunc, hashfunc

:ctype:`PyTypeObject` の構造体定義は:file:`Include/object.h`
で見つけられるはずです。参照の手間を省くために、ここでは 定義を繰り返します:


.. include:: ../includes/typestruct.h
   :literal:

型オブジェクト構造体は:ctype:`PyVarObject` 構造体を拡張したものです。 :attr:`ob_size` フィールドは、(通常 class
文が呼び出す :func:`type_new` で生成される) 動的な型に使います。 :cdata:`PyType_Type` (メタタイプ)
は:attr:`tp_itemsize` を初期化するので 注意してください。すなわち、インスタンス (つまり型オブジェクト) には
:attr:`ob_size` フィールドがなければ*なりません*。


.. cmember:: PyObject* PyObject._ob_next
             PyObject* PyObject._ob_prev

   これらのフィールドはマクロ  ``Py_TRACE_REFS`` が定義されている 場合のみ存在します。``PyObject_HEAD_INIT``
   マクロを使うと、 フィールドを *NULL* に初期化します。静的にメモリ確保されている オブジェクトでは、これらのフィールドは常に *NULL*のままです。
   動的にメモリ確保されるオブジェクトの場合、これら二つのフィールドは、 ヒープ上の*全ての* 存続中のオブジェクトからなる二重リンクリスト
   でオブジェクトをリンクする際に使われます。 このことは様々なデバッグ目的に利用できます; 現状では、環境変数 :envvar:`PYTHONDUMPREFS`
   が設定されているときに、プログラムの実行 終了時点で存続しているオブジェクトを出力するのが唯一の用例です。

   サブタイプはこのフィールドを継承しません。


.. cmember:: Py_ssize_t PyObject.ob_refcnt

   型オブジェクトの参照カウントで、``PyObject_HEAD_INIT`` は この値を ``1`` に初期化します。静的にメモリ確保された型オブジェクト
   では、型のインスタンス (:attr:`ob_type` が該当する型を指している オブジェクト) は参照をカウントする対象には*なりません*。
   動的にメモリ確保される型オブジェクトの場合、インスタンスは 参照カウントの対象に*なります*。

   サブタイプはこのフィールドを継承しません。


.. cmember:: PyTypeObject* PyObject.ob_type

   型自体の型、別の言い方をするとメタタイプです。 ``PyObject_HEAD_INIT`` マクロで初期化され、通常は ``&PyType_Type``
   になります。しかし、(少なくとも) Windows で 利用できる動的ロード可能な拡張モジュールでは、コンパイラは
   有効な初期化ではないと文句をつけます。そこで、ならわしとして、 ``PyObject_HEAD_INIT`` には *NULL* を渡して初期化しておき、
   他の操作を行う前にモジュールの初期化関数で明示的にこのフィールドを 初期化することになっています。この操作は以下のように行います::

      Foo_Type.ob_type = &PyType_Type;

   上の操作は、該当する型のいかなるインスタンス生成よりも前に しておかねばなりません。:cfunc:`PyType_Ready` は
   :attr:`ob_type` が *NULL*かどうか調べ、*NULL*の場合には 初期化します: Python 2.2
   では、``&PyType_Type`` にセット します; in Python 2.2.1 およびそれ以降では基底クラスの :attr:`ob_type`
   フィールドに初期化します。 :attr:`ob_type` が非ゼロの場合、:cfunc:`PyType_Ready` は このフィールドを変更しません。

   Python 2.2 では、サブタイプはこのフィールドを継承しません。 2.2.1 と 2.3 以降では、サブタイプはこのフィールドを継承します。


.. cmember:: Py_ssize_t PyVarObject.ob_size

   静的にメモリ確保されている型オブジェクトの場合、このフィールドは ゼロに初期化されます。動的にメモリ確保されている型オブジェクトの
   場合、このフィールドは内部使用される特殊な意味を持ちます。

   サブタイプはこのフィールドを継承しません。


.. cmember:: char* PyTypeObject.tp_name

   型の名前が入っている NUL 終端された文字列へのポインタです。 モジュールのグローバル変数としてアクセスできる型の場合、
   この文字列は完全なモジュール名、ドット、そして型の名前と続く 文字列になります; 組み込み型の場合、ただの型の名前です。
   モジュールがあるパッケージのサブモジュールの場合、完全なパッケージ名が 完全なモジュール名の一部になっています。例えば、パッケージ :mod:`P`
   内のサブモジュール :mod:`Q` に入っているモジュール:mod:`M` 内で 定義されている:class:`T` は、:attr:`tp_name` を
   ``"P.Q.M.T"`` に 初期化します。

   動的にメモリ確保される型オブジェクトの場合、このフィールドは 単に型の名前になり、モジュール名は型の辞書内でキー ``'__module__'``
   に対する値として明示的に保存されます。

   静的にメモリ確保される型オブジェクトの場合、:attr:`tp_name` フィールド にはドットが入っているはずです。最後のドットよりも前にある
   部分文字列全体は :attr:`__module__` 属性として、また ドットよりも後ろにある部分は:attr:`__name__`
   属性としてアクセスできます。

   ドットが入っていない場合、:attr:`tp_name` フィールドの内容全てが :attr:`__name__` 属性になり、
   :attr:`__module__` 属性は (前述のように型の辞書内で明示的にセットしないかぎり) 未定義になります。 このため、こうした型オブジェクトは
   pickle 化できないことになります。

   サブタイプはこのフィールドを継承しません。


.. cmember:: Py_ssize_t PyTypeObject.tp_basicsize
             Py_ssize_t PyTypeObject.tp_itemsize

   これらのフィールドは、型インスタンスのバイトサイズを計算できる ようにします。

   型には二つの種類があります: 固定長インスタンスの型は、 :attr:`tp_itemsize` フィールドがゼロで、可変長インスタンスの方は
   :attr:`tp_itemsize` フィールドが非ゼロの値になります。 固定長インスタンスの型の場合、全てのインスタンスは等しく
   :attr:`tp_basicsize` で与えられたサイズになります。

   可変長インスタンスの型の場合、インスタンスには:attr:`ob_size`  フィールドがなくてはならず、インスタンスのサイズは N をオブジェクトの
   "長さ" として、:attr:`tp_basicsize` と N かける :attr:`tp_itemsize` の加算になります。N
   の値は通常、インスタンスの :attr:`ob_size`  フィールドに記憶されます。ただし例外がいくつかあります: 例えば、長整数では負の値を
   :attr:`ob_size` に使って、インスタンスの 表す値が負であることを示し、 N 自体は ``abs(ob_size)``
   になります。また、:attr:`ob_size` フィールドがあるからといって、 必ずしもインスタンスが可変長であることを意味しません (例えば、
   リスト型の構造体は固定長のインスタンスになるにもかかわらず、 インスタンスにはちゃんと意味を持った :attr:`ob_size` フィールドが あります)。

   基本サイズには、:cmacro:`PyObject_HEAD` マクロまたは  :cmacro:`PyObject_VAR_HEAD` マクロ
   (インスタンス構造体を 宣言するのに使ったどちらかのマクロ) で宣言されているフィールド が入っています。さらに、:attr:`_ob_prev` および
   :attr:`_ob_next` フィールドがある場合、これらのフィールドもサイズに加算されます。

   従って、:attr:`tp_basicsize` の正しい初期化パラメタを得るには、 インスタンスデータのレイアウトを宣言するのに使う構造体に対して
   :keyword:`sizeof` 演算子を使うしかありません。 基本サイズには、GC ヘッダサイズは入っていません (これは Python 2.2
   からの新しい仕様です; 2.1 や 2.0 では、GC ヘッダサイズは :attr:`tp_basicsize` に入っていました)。

   バイト整列 (alignment) に関する注釈: 変数の各要素を配置する際に特定の バイト整列が必要となる場合、:attr:`tp_basicsize`
   の値に 気をつけなければなりません。一例: 例えばある型が``double`` の 配列を実装しているとします。:attr:`tp_itemsize` は
   ``sizeof(double)`` です。(``double`` のバイト整列条件に従って) :attr:`tp_basicsize`
   が``sizeof(double)`` の個数分のサイズに なるようにするのはプログラマの責任です。


.. cmember:: destructor PyTypeObject.tp_dealloc

   インスタンスのデストラクタ関数へのポインタです。この関数は (単量子``None`` や``Ellipsis`` の場合のように、インスタンスが
   決してメモリ解放されない型でない限り) 必ず定義しなければなりません。

   デストラクタ関数は、:cfunc:`Py_DECREF` や :cfunc:`Py_XDECREF`
   マクロで、操作後の参照カウントがゼロになった際に呼び出されます。 呼び出された時点では、インスタンスはまだ存在しますが、インスタンスに
   対する参照は全ない状態です。デストラクタ関数はインスタンスが保持している 全ての参照を解放し、インスタンスが確保している全てのメモリバッファを
   (バッファの確保時に使った関数に対応するメモリ解放関数を使って) 解放し、最後に (かならず最後に行う操作として) その型の :attr:`tp_free`
   関数を呼び出します。ある型がサブタイプを作成できない  (:const:`Py_TPFLAGS_BASETYPE` フラグがセットされていない) 場合、
   :attr:`tp_free` の代わりにオブジェクトのメモリ解放関数 (deallocator) を
   直接呼び出してもかまいません。オブジェクトのメモリ解放関数は、 インスタンスのメモリ確保を行う際に使った関数と同じファミリでなければ なりません;
   インスタンスを :cfunc:`PyObject_New` や :cfunc:`PyObject_VarNew` でメモリ確保した場合には、通常
   :cfunc:`PyObject_Del` を使い、:cfunc:`PyObject_GC_New` や :cfunc:`PyObject_GC_VarNew`
   で確保した場合には :cfunc:`PyObject_GC_Del` を使います。

   サブタイプはこのフィールドを継承します。


.. cmember:: printfunc PyTypeObject.tp_print

   オプションのフィールドです。ポインタで、インスタンスの出力 (print) を 行う関数を指します。

   出力関数は、インスタンスが *実体のある (real)* ファイルに出力 される場合にのみ呼び出されます; (:class:`StringIO`
   インスタンスのような) 擬似ファイルに出力される場合には、インスタンスの :attr:`tp_repr` や :attr:`tp_str`
   が指す関数が呼び出され、文字列への変換を行います。 また、:attr:`tp_print` が *NULL*の場合にもこれらの関数が呼び出され ます。
   :attr:`tp_repr` や :attr:`tp_str` と異なる出力を生成するような :attr:`tp_print`
   は、決して型に実装してはなりません。

   出力関数は:cfunc:`PyObject_Print` と同じシグネチャ: ``int tp_print(PyObject *self, FILE
   *file, int flags)`` で呼び出されます。*self* 引数は出力するインスタンスを指します。 *file* 引数は出力先となる標準入出力
   (stdio) ファイルです。 *flags* 引数はフラグビットを組み合わせた値です。 現在定義されているフラグビットは
   :const:`Py_PRINT_RAW` のみです。 :const:`Py_PRINT_RAW` フラグビットがセットされていれば、
   インスタンスは:attr:`tp_str` と同じ書式で出力されます。 :const:`Py_PRINT_RAW` フラグビットがクリアならば、
   インスタンスは:attr:`tp_repr` と同じ書式で出力されます。 この関数は、操作中にエラーが生じた場合、``-1`` を返して例外状態を
   セットしなければなりません。

   :attr:`tp_print` フィールドは撤廃されるかもしれません。いずれにせよ、 :attr:`tp_print`
   は定義せず、代わりに:attr:`tp_repr` や :attr:`tp_str` に頼って出力を行うようにしてください。

   サブタイプはこのフィールドを継承します。


.. cmember:: getattrfunc PyTypeObject.tp_getattr

   オプションのフィールドです。ポインタで、 get-attribute-string を行う関数を指します。

   このフィールドは撤廃されています。このフィールドを定義する場合、 :attr:`tp_getattro` 関数と同じように動作し、属性名は Python 文字列
   オブジェクトではなく C 文字列で指定するような関数を指すように しなければなりません。シグネチャは
   :cfunc:`PyObject_GetAttrString` と同じです。

   このフィールドは:attr:`tp_getattro` と共にサブタイプに継承 されます: すなわち、サブタイプの:attr:`tp_getattr` および
   :attr:`tp_getattro` が共に *NULL*の場合、サブタイプは 基底タイプから:attr:`tp_getattr` と
   :attr:`tp_getattro` を一緒に 継承します。


.. cmember:: setattrfunc PyTypeObject.tp_setattr

   オプションのフィールドです。ポインタで、 set-attribute-string を行う関数を指します。

   このフィールドは撤廃されています。このフィールドを定義する場合、 :attr:`tp_setattro` 関数と同じように動作し、属性名は Python 文字列
   オブジェクトではなく C 文字列で指定するような関数を指すように しなければなりません。シグネチャは
   :cfunc:`PyObject_SetAttrString` と同じです。

   このフィールドは:attr:`tp_setattro` と共にサブタイプに継承 されます: すなわち、サブタイプの:attr:`tp_setattr` および
   :attr:`tp_setattro` が共に *NULL*の場合、サブタイプは 基底タイプから:attr:`tp_setattr` と
   :attr:`tp_setattro` を一緒に 継承します。


.. cmember:: cmpfunc PyTypeObject.tp_compare

   オプションのフィールドです。ポインタで、 三値比較 (three-way comparison) を行う関数を指します。

   シグネチャは:cfunc:`PyObject_Compare` と同じです。 この関数は *self* が *other* よりも大きければ ``1``、
   *self* と *other* の値が等しければ ``0``、 *self* が *other* より小さければ ``-1`` を返します。
   この関数は、比較操作中にエラーが生じた場合、例外状態をセットして ``-1`` を返さねばなりません。

   このフィールドは:attr:`tp_richcompare` および:attr:`tp_hash` と共にサブタイプに継承されます: すなわち、サブタイプの
   :attr:`tp_compare` 、:attr:`tp_richcompare` および :attr:`tp_hash` が共に
   *NULL*の場合、サブタイプは 基底タイプから:attr:`tp_compare`、:attr:`tp_richcompare`、
   :attr:`tp_hash` の三つを一緒に継承します。


.. cmember:: reprfunc PyTypeObject.tp_repr

   .. index:: builtin: repr

   オプションのフィールドです。ポインタで、 組み込み関数:func:`repr` を実装している 関数を指します。

   シグネチャは:cfunc:`PyObject_Repr` と同じです。 この関数は文字列オブジェクトか Unicode オブジェクトを返さねば
   なりません。理想的には、この関数が返す文字列は、適切な環境で :func:`eval` に渡した場合、同じ値を持つオブジェクトになるような
   文字列でなければなりません。不可能な場合には、オブジェクトの型と 値から導出した内容の入った ``'<'``  から始まって ``'>'``
   で終わる文字列を返さねば なりません。

   このフィールドが設定されていない場合、``<%s object at %p>``  の形式をとる文字列が返されます。 ``%s`` は型の名前に、 ``%p``
   はオブジェクトのメモリアドレスに置き換えられます。

   サブタイプはこのフィールドを継承します。

PyNumberMethods \*tp_as_number;

XXX

PySequenceMethods \*tp_as_sequence;

XXX

PyMappingMethods \*tp_as_mapping;

XXX


.. cmember:: hashfunc PyTypeObject.tp_hash

   .. index:: builtin: hash

   オプションのフィールドです。ポインタで、 組み込み関数:func:`hash` を実装している 関数を指します。

   シグネチャは:cfunc:`PyObject_Hash` と同じです。 この関数は C の :ctype:`long` 型の値を返さねばなりません。 通常時には
   ``-1`` を戻り値にしてはなりません; ハッシュ値の 計算中にエラーが生じた場合、関数は例外をセットして``-1`` を 返さねばなりません。

   このフィールドが設定されていない場合、二つの可能性があります: :attr:`tp_compare` および :attr:`tp_richcompare`
   フィールドの 両方が *NULL*の場合、オブジェクトのアドレスに基づいたデフォルトの ハッシュ値が返されます;
   それ以外の場合、:exc:`TypeError`  が送出されます。

   このフィールドは:attr:`tp_compare` および:attr:`tp_richcompare` と共にサブタイプに継承されます:
   すなわち、サブタイプの :attr:`tp_compare` 、:attr:`tp_richcompare` および :attr:`tp_hash` が共に
   *NULL*の場合、サブタイプは 基底タイプから:attr:`tp_compare`、:attr:`tp_richcompare`、
   :attr:`tp_hash` の三つを一緒に継承します。


.. cmember:: ternaryfunc PyTypeObject.tp_call

   オプションのフィールドです。ポインタで、 オブジェクトの呼び出しを実装している 関数を指します。 オブジェクトが呼び出し可能でない場合には *NULL*
   にしなければ なりません。シグネチャは :cfunc:`PyObject_Call` と同じです。

   サブタイプはこのフィールドを継承します。


.. cmember:: reprfunc PyTypeObject.tp_str

   オプションのフィールドです。ポインタで、 組み込みの演算 :func:`str` を実装している 関数を指します。(:class:`str`
   が型の一つになったため、 :func:`str` は :class:`str` のコンストラクタを呼び出す
   ことに注意してください。このコンストラクタは実際の処理を行う 上で:cfunc:`PyObject_Str` を呼び出し、さらに
   :cfunc:`PyObject_Str` がこのハンドラを呼び出すことになります。)

   シグネチャは:cfunc:`PyObject_Str` と同じです; この関数は文字列オブジェクトか Unicode オブジェクトを返さねばなりません。
   また、この関数はオブジェクトを "分かりやすく (friendly)" 表現 した文字列を返さねばなりません。というのは、この文字列は
   :keyword:`print` 文で使われることになる表記だからです。

   このフィールドが設定されていない場合、文字列表現を返すためには :cfunc:`PyObject_Repr` が呼び出されます。

   サブタイプはこのフィールドを継承します。


.. cmember:: getattrofunc PyTypeObject.tp_getattro

   オプションのフィールドです。ポインタで、 get-attribute を実装している関数を指します。

   シグネチャは:cfunc:`PyObject_GetAttr` と同じです。
   対する通常の属性検索を実装している:cfunc:`PyObject_GenericGetAttr`  をこのフィールドに設定しておくと往々にして便利です。

   このフィールドは:attr:`tp_getattr` と共にサブタイプに継承 されます: すなわち、サブタイプの:attr:`tp_getattr` および
   :attr:`tp_getattro` が共に *NULL*の場合、サブタイプは 基底タイプから:attr:`tp_getattr` と
   :attr:`tp_getattro` を一緒に 継承します。


.. cmember:: setattrofunc PyTypeObject.tp_setattro

   オプションのフィールドです。ポインタで、 set-attribute を行う関数を指します。

   シグネチャは:cfunc:`PyObject_SetAttr` と同じです。
   対する通常の属性設定を実装している:cfunc:`PyObject_GenericSetAttr`  をこのフィールドに設定しておくと往々にして便利です。

   このフィールドは:attr:`tp_setattr` と共にサブタイプに継承 されます: すなわち、サブタイプの:attr:`tp_setattr` および
   :attr:`tp_setattro` が共に *NULL*の場合、サブタイプは 基底タイプから:attr:`tp_setattr` と
   :attr:`tp_setattro` を一緒に 継承します。


.. cmember:: PyBufferProcs* PyTypeObject.tp_as_buffer

   バッファインタフェースを実装しているオブジェクトにのみ関連する、 一連のフィールド群が入った別の構造体を指すポインタです。 構造体内の各フィールドは
   "バッファオブジェクト構造体"  (:ref:`buffer-structs` 節) で説明します。

   :attr:`tp_as_buffer` フィールド自体は継承されませんが、フィールド内に 入っているフィールドは個別に継承されます。


.. cmember:: long PyTypeObject.tp_flags

   このフィールドは様々なフラグからなるビットマスクです。 いくつかのフラグは、特定の状況において変則的なセマンティクスが適用 されることを示します;
   その他のフラグは、型オブジェクト (あるいは:attr:`tp_as_number`、:attr:`tp_as_sequence`、
   :attr:`tp_as_mapping`、および:attr:`tp_as_buffer` が参照している 拡張機能構造体: extention
   structure ) の特定のフィールドのうち、 過去から現在までずっと存在しているわけではないもの が有効に なっていることを示すために使われます;
   フラグビットがクリアであれば、フラグが保護しているフィールド にはアクセスしない代わりに、その値はゼロか*NULL* に なっているとみなさなければなりません。

   このフィールドの継承は複雑です。ほとんどのフラグビットは 個別に継承されます。つまり、基底タイプであるフラグビットがセット
   されている場合、サブタイプはそのフラグビットを継承します。 機能拡張のための構造体に関するフラグビットは、その機能拡張構造体
   が継承されるときに限定して継承されます。すなわち、基底タイプの フラグビットの値は、機能拡張構造体へのポインタと一緒にサブタイプに コピーされます。
   :const:`Py_TPFLAGS_HAVE_GC` フラグビットは、:attr:`tp_traverse`  および :attr:`tp_clear`
   フィールドと合わせてコピーされます。 すなわち、サブタイプの :const:`Py_TPFLAGS_HAVE_GC` フラグビットが クリアで、かつ
   (:const:`Py_TPFLAGS_HAVE_RICHCOMPARE` フラグビットの 指定によって)  :attr:`tp_traverse` および
   :attr:`tp_clear`  フィールドがサブタイプ内に存在しており、かつ値が *NULL* の場合に 基底タイプから値を継承します。

   以下のビットマスクは現在定義されているものです; フラグは``|`` 演算子で論理和を取って :attr:`tp_flags` フィールドの値にできます。
   :cfunc:`PyType_HasFeature` マクロは型とフラグ値、 *tp* および *f* をとり、``tp->tp_flags & f``
   が非ゼロかどうか調べます。


   .. data:: Py_TPFLAGS_HAVE_GETCHARBUFFER

      このビットがセットされていれば、:attr:`tp_as_buffer` が参照する :ctype:`PyBufferProcs` 構造体には
      :attr:`bf_getcharbuffer` フィールドが あります。


   .. data:: Py_TPFLAGS_HAVE_SEQUENCE_IN

      このビットがセットされていれば、:attr:`tp_as_sequence` が参照する :ctype:`PySequenceMethods` 構造体には
      :attr:`sq_contains` フィールドが あります。


   .. data:: Py_TPFLAGS_GC

      このビットは旧式のものです。このシンボルが指し示していたビットは もはや使われていません。シンボルの現在の定義はゼロになっています。


   .. data:: Py_TPFLAGS_HAVE_INPLACEOPS

      このビットがセットされていれば、:attr:`tp_as_sequence` が参照する :ctype:`PySequenceMethods`
      構造体、および:attr:`tp_as_number` が参照する :ctype:`PyNumberMethods` 構造体には in-place
      演算に関するフィールドが 入っています。具体的に言うと、 :ctype:`PyNumberMethods` 構造体はフィールド
      :attr:`nb_inplace_add`、 :attr:`nb_inplace_subtract`、
      :attr:`nb_inplace_multiply`、 :attr:`nb_inplace_divide`、
      :attr:`nb_inplace_remainder`、 :attr:`nb_inplace_power`、
      :attr:`nb_inplace_lshift`、 :attr:`nb_inplace_rshift`、 :attr:`nb_inplace_and`、
      :attr:`nb_inplace_xor`、および :attr:`nb_inplace_or` を持つことになります; また、
      :ctype:`PySequenceMethods` 構造体はフィールド :attr:`sq_inplace_concat` および
      :attr:`sq_inplace_repeat` を持つことになります。


   .. data:: Py_TPFLAGS_CHECKTYPES

      このビットがセットされていれば、:attr:`tp_as_number` が参照する :ctype:`PyNumberMethods`
      構造体内で定義されている二項演算子および 三項演算子は任意のオブジェクト型を非演算子にとるようになり、
      必要に応じて引数の型変換を行います。このビットがクリアなら、 演算子は全ての引数が現在のオブジェクト型と同じであるよう要求し、
      演算の呼び出し側は演算に先立って型変換を行うものと想定します。 対象となる演算子は :attr:`nb_add`、 :attr:`nb_subtract`、
      :attr:`nb_multiply`、 :attr:`nb_divide`、 :attr:`nb_remainder`、 :attr:`nb_divmod`、
      :attr:`nb_power`、 :attr:`nb_lshift`、 :attr:`nb_rshift`、 :attr:`nb_and`、
      :attr:`nb_xor`、および :attr:`nb_or` です。


   .. data:: Py_TPFLAGS_HAVE_RICHCOMPARE

      このビットがセットされていれば、型オブジェクトには :attr:`tp_richcompare` フィールド、そして :attr:`tp_traverse`
      および :attr:`tp_clear` フィールドがあります。


   .. data:: Py_TPFLAGS_HAVE_WEAKREFS

      このビットがセットされていれば、構造体には:attr:`tp_weaklistoffset`
      フィールドが定義されています。:attr:`tp_weaklistoffset` フィールドの
      値がゼロより大きければ、この型のインスタンスは弱参照で参照できます。


   .. data:: Py_TPFLAGS_HAVE_ITER

      このビットがセットされていれば、型オブジェクトには:attr:`tp_iter`  および :attr:`tp_iternext` フィールドがあります。


   .. data:: Py_TPFLAGS_HAVE_CLASS

      このビットがセットされていれば、型オブジェクトは Python 2.2 以降で 定義されている新たなフィールド: :attr:`tp_methods`、
      :attr:`tp_members`、 :attr:`tp_getset`、 :attr:`tp_base`、 :attr:`tp_dict`、
      :attr:`tp_descr_get`、 :attr:`tp_descr_set`、 :attr:`tp_dictoffset`、
      :attr:`tp_init`、 :attr:`tp_alloc`、 :attr:`tp_new`、 :attr:`tp_free`、
      :attr:`tp_is_gc`、 :attr:`tp_bases`、 :attr:`tp_mro`、 :attr:`tp_cache`、
      :attr:`tp_subclasses`、 および :attr:`tp_weaklist` が あります。


   .. data:: Py_TPFLAGS_HEAPTYPE

      型オブジェクト自体がヒープにメモリ確保される場合にセットされるビットです。 型オブジェクト自体がヒープにメモリ確保される場合、インスタンスの
      :attr:`ob_type` フィールドは型オブジェクトへの参照とみなされます。 この場合、新たなインスタンスを 生成する度に型オブジェクトを INCREF
      し、インスタンスを解放するたびに DECREF します (サブタイプのインスタンスには適当されません;  インスタンスが :attr:`ob_type`
      で参照している型だけが INCREF および DECREF されます)。


   .. data:: Py_TPFLAGS_BASETYPE

      型を別の型の基底タイプとして使える場合にセットされるビットです。 このビットがクリアならば、この型のサブタイプは生成できません (Java における
      "final" クラスに似たクラスになります)。


   .. data:: Py_TPFLAGS_READY

      型オブジェクトが :cfunc:`PyType_Ready` で完全に初期化される とセットされるビットです。


   .. data:: Py_TPFLAGS_READYING

      :cfunc:`PyType_Ready` による型オブジェクトの初期化処理中にセット されるビットです。


   .. data:: Py_TPFLAGS_HAVE_GC

      オブジェクトがガベージコレクション (GC) をサポートする場合にセットされる ビットです。このビットがセットされている場合、インスタンスは
      :cfunc:`PyObject_GC_New` を使って生成し、 :cfunc:`PyObject_GC_Del` を使って破壊しなければなりません。
      詳しい情報は XXX 節のガベージコレクションに関する説明中にあります。 このビットはまた、GC に関連するフィールド:attr:`tp_traverse`
      および :attr:`tp_clear` が型オブジェクト内に存在することを示します; しかし、これらのフィールドは
      :const:`Py_TPFLAGS_HAVE_GC` がクリア でも:const:`Py_TPFLAGS_HAVE_RICHCOMPARE`
      がセットされている場合には 存在します。


   .. data:: Py_TPFLAGS_DEFAULT

      型オブジェクトおよび拡張機能構造体の特定のフィールドの存在の有無に 関連する全てのビットからなるビットマスクです。 現状では、このビットマスクには以下のビット:
      :const:`Py_TPFLAGS_HAVE_GETCHARBUFFER`、 :const:`Py_TPFLAGS_HAVE_SEQUENCE_IN`、
      :const:`Py_TPFLAGS_HAVE_INPLACEOPS`、 :const:`Py_TPFLAGS_HAVE_RICHCOMPARE`、
      :const:`Py_TPFLAGS_HAVE_WEAKREFS`、 :const:`Py_TPFLAGS_HAVE_ITER`、および
      :const:`Py_TPFLAGS_HAVE_CLASS` が入っています。


.. cmember:: char* PyTypeObject.tp_doc

   オプションのフィールドです。ポインタで、この型オブジェクトの docstring を与える NUL 終端された C の文字列を指します。
   この値は型オブジェクトと型のインスタンスにおける :attr:`__doc__` 属性として公開されます。

   サブタイプはこのフィールドを継承*しません*。

以下の三つのフィールドは、:const:`Py_TPFLAGS_HAVE_RICHCOMPARE`  フラグビットがセットされている場合にのみ存在します。


.. cmember:: traverseproc PyTypeObject.tp_traverse

   オプションのフィールドです。ポインタで、 ガベージコレクタのためのトラバーサル関数 (traversal function)
   を指します。:const:`Py_TPFLAGS_HAVE_GC` がセットされている
   場合にのみ使われます。Pythonのガベージコレクションの枠組みに関する詳細は :ref:`supporting-cycle-detection` にあります。

   :attr:`tp_traverse` ポインタは、ガベージコレクタが循環参照を見つけるために 使われます。 :attr:`tp_traverse`
   関数の典型的な実装は、インスタンスの各メンバのうち Pythonオブジェクトに対して :cfunc:`Py_VISIT` を呼び出します。 例えば、次のコードは
   :mod:`thread` 拡張モジュールの :cfunc:`local_traverse` 関数になります::

      static int
      local_traverse(localobject *self, visitproc visit, void *arg)
      {
          Py_VISIT(self->args);
          Py_VISIT(self->kw);
          Py_VISIT(self->dict);
          return 0;
      }

   :cfunc:`Py_VISIT` が循環参照になる恐れのあるメンバにだけ呼び出されていることに 注目してください。 ``self->key``
   メンバもありますが、それは *NULL* か Python文字列なので、 循環参照の一部になることはありません。

   一方、メンバが循環参照の一部になり得ないと判っていても、デバッグ目的で巡回したい 場合があるかもしれないので、 :mod:`gc` モジュールの
   :cfunc:`get_reference` 関数は 循環参照になり得ないメンバも返します。

   :cfunc:`Py_VISIT` は :cfunc:`local_traverse` が *visit* と *arg*
   という決まった名前の引数を持つことを要求します。

   このフィールドは :attr:`tp_clear` および :const:`Py_TPFLAGS_HAVE_GC` フラグビットと一緒に継承されます:
   フラグビット、:attr:`tp_traverse`、 および :attr:`tp_clear` の値がサブタイプで全てゼロになっており、 *かつ*
   サブタイプで :const:`Py_TPFLAGS_HAVE_RICHCOMPARE`  フラグビットがセットされている場合に、基底タイプから値を継承します。


.. cmember:: inquiry PyTypeObject.tp_clear

   オプションのフィールドです。ポインタで、 ガベージコレクタにおける消去関数 (clear function) を指します。
   :const:`Py_TPFLAGS_HAVE_GC` がセットされている 場合にのみ使われます。

   :attr:`tp_clear` メンバ関数はGCが見つけた循環しているゴミの循環参照を 壊すために用いられます。 システム内の全ての
   :attr:`tp_clear` 関数によって、全ての循環参照を破壊しなければなりません。 (訳注:
   ある型が:attr:`tp_clear`を実装しなくても全ての循環参照が破壊できるのであれば 実装しなくても良い)
   これはとても繊細で、もし少しでも不確かな部分があるのであれば、:attr:`tp_clear` 関数を提供するべきです。
   例えば、タプルは:attr:`tp_clear`を実装しません。なぜなら、 タプルだけで構成された循環参照がみつかることは無いからです。
   したがって、タプル以外の型 :attr:`tp_clear` 関数たちが、タプルを含むどんな循環参照も 破壊できる必要があります。
   これは簡単に判ることでははありません。 :attr:`tp_clear` の実装を避ける良い理由はめったにありません。

   :attr:`tp_clear` の実装は、次の実装のように、インスタンスの
   (Pythonオブジェクト)メンバに対する参照を捨てて、メンバに対するポインタ変数を *NULL* にセットするべきです::

      static int
      local_clear(localobject *self)
      {
          Py_CLEAR(self->key);
          Py_CLEAR(self->args);
          Py_CLEAR(self->kw);
          Py_CLEAR(self->dict);
          return 0;
      }

   参照のクリアはデリケートなので、:cfunc:`Py_CLEAR`マクロを使うべきです:
   ポインタを*NULL*にせっとするまで、そのオブジェクトの参照カウントを デクリメントしてはいけません。
   参照カウントのデクリメントすると、そのオブジェクトが破棄されるかもしれず、 (そのオブジェクトに関連付けられたファイナライザ、弱参照のコールバックにより)
   任意のPythonコードの実行を含む後片付け処理が実行されるかもしれないからです。 もしそういったコードが再び *self* を参照することがあれば、すでに
   持っていたオブジェクトへのポインタは *NULL* になっているので、 *self* は所有していたオブジェクトをもう利用できないことを認識できます。
   :cfunc:`Py_CLEAR`マクロはその手続きを安全な順番で実行します。

   :attr:`tp_clear` 関数の目的は参照カウントを破壊することなので、Python文字列や
   Python整数のような、循環参照になりえないオブジェクトをクリアする必要はありません。 一方、全部の所有オブジェクトをクリアするようにし、
   :attr:`tp_dealloc` 関数が :attr:`tp_clear` 関数を実行するようにすると実相が楽です。

   Pythonのガベージコレクションの仕組みについての詳細は、 :ref:`supporting-cycle-detection` にあります。

   このフィールドは :attr:`tp_traverse` および :const:`Py_TPFLAGS_HAVE_GC` フラグビットと一緒に継承されます:
   フラグビット、:attr:`tp_traverse`、 および :attr:`tp_clear` の値がサブタイプで全てゼロになっており、 *かつ*
   サブタイプで :const:`Py_TPFLAGS_HAVE_RICHCOMPARE`  フラグビットがセットされている場合に、基底タイプから値を継承します。


.. cmember:: richcmpfunc PyTypeObject.tp_richcompare

   オプションのフィールドです。ポインタで、 拡張比較関数 (rich comparison function) を指します。

   シグネチャは:cfunc:`PyObject_RichCompare` と同じです。 この関数は、比較結果を返すべきです。(普通は ``Py_True`` か
   ``Py_False``です。) 比較が未定義の場合は、 ``Py_NotImplemented``を、それ以外のエラーが 発生した場合には例外状態をセットして
   ``NULL`` を返さねばなりません。

   このフィールドは:attr:`tp_compare` および:attr:`tp_hash` と共にサブタイプに継承されます: すなわち、サブタイプの
   :attr:`tp_compare` 、:attr:`tp_richcompare` および :attr:`tp_hash` が共に
   *NULL*の場合、サブタイプは 基底タイプから:attr:`tp_compare`、:attr:`tp_richcompare`、
   :attr:`tp_hash` の三つを一緒に継承します。

   :attr:`tp_richcompare` および:cfunc:`PyObject_RichCompare`
   関数の第三引数に使うための定数としては以下が定義されています:

   +----------------+--------+
   | 定数           | 比較   |
   +================+========+
   | :const:`Py_LT` | ``<``  |
   +----------------+--------+
   | :const:`Py_LE` | ``<=`` |
   +----------------+--------+
   | :const:`Py_EQ` | ``==`` |
   +----------------+--------+
   | :const:`Py_NE` | ``!=`` |
   +----------------+--------+
   | :const:`Py_GT` | ``>``  |
   +----------------+--------+
   | :const:`Py_GE` | ``>=`` |
   +----------------+--------+

次のフィールドは、:const:`Py_TPFLAGS_HAVE_WEAKREFS` フラグビットがセットされている場合にのみ存在します。


.. cmember:: long PyTypeObject.tp_weaklistoffset

   型のインスタンスが弱参照可能な場合、このフィールドはゼロよりも 大きな数になり、インスタンス構造体における弱参照リストの先頭を 示すオフセットが入ります (GC
   ヘッダがある場合には無視します); このオフセット値は :cfunc:`PyObject_ClearWeakRefs` および
   :cfunc:`PyWeakref_\*` 関数が利用します。 インスタンス構造体には、 *NULL*に初期化された:ctype:`PyObject\*` 型の
   フィールドが入っていなければなりません。

   このフィールドを :attr:`tp_weaklist` と混同しないようにしてください; :attr:`tp_weaklist`
   は型オブジェクト自体の弱参照リストの先頭です。

   サブタイプはこのフィールドを継承しますが、以下の規則があるので 読んでください。 サブタイプはこのオフセット値をオーバライドできます; 従って、
   サブタイプでは弱参照リストの先頭が基底タイプとは異なる場合が あります。リストの先頭は常に:attr:`tp_weaklistoffset` で
   分かるはずなので、このことは問題にはならないはずです。

   :keyword:`class` 文で定義された型に :attr:`__slots__` 宣言が 全くなく、かつ基底タイプが弱参照可能でない場合、
   その型を弱参照可能にするには弱参照リストの先頭を表すスロットを インスタンスデータレイアウト構造体に追加し、スロットのオフセットを
   :attr:`tp_weaklistoffset` に設定します。

   型の :attr:`__slots__` 宣言中に :attr:`__weakref__` という名前の
   スロットが入っている場合、スロットはその型のインスタンスにおける 弱参照リストの先頭を表すスロットになり、スロットのオフセットが 型の
   :attr:`tp_weaklistoffset` に入ります。

   型の :attr:`__slots__` 宣言に :attr:`__weakref__` という名のスロット
   が入っていない場合、その型は基底タイプから:attr:`tp_weaklistoffset`  を継承します。

次の二つのフィールドは、:const:`Py_TPFLAGS_HAVE_CLASS` フラグビットがセットされている場合にのみ存在します。


.. cmember:: getiterfunc PyTypeObject.tp_iter

   An optional pointer to a function that returns an iterator for the object.  Its
   presence normally signals that the instances of this type are iterable (although
   sequences may be iterable without this function, and classic instances always
   have this function, even if they don't define an :meth:`__iter__` method).

   This function has the same signature as :cfunc:`PyObject_GetIter`.

   サブタイプはこのフィールドを継承します。


.. cmember:: iternextfunc PyTypeObject.tp_iternext

   オプションのフィールドです。ポインタで、 イテレータにおいて次の要素を返すか、イテレータの要素がなくなると :exc:`StopIteration`
   を送出する関数を指します。このフィールド があると、通常この型のインスタンスがイテレータであることを示します (ただし、旧スタイルのインスタンスでは、たとえ
   :meth:`next` メソッドが 定義されていなくても常にこの関数を持っています)。

   イテレータ型では、 :attr:`tp_iter` 関数も定義していなければならず、 :attr:`tp_iter` は
   (新たなイテレータインスタンスではなく)  イテレータインスタンス自体を返さねばなりません。

   この関数のシグネチャは :cfunc:`PyIter_Next` と同じです。

   サブタイプはこのフィールドを継承します。

次の :attr:`tp_weaklist` までのフィールドは、 :const:`Py_TPFLAGS_HAVE_CLASS`
フラグビットがセットされている場合にのみ存在します。


.. cmember:: struct PyMethodDef* PyTypeObject.tp_methods

   オプションのフィールドです。ポインタで、 この型の正規 (regular) のメソッドを宣言している:ctype:`PyMethodDef`
   構造体からなる、*NULL*で終端された静的な配列を指します。

   配列の各要素ごとに、メソッドデスクリプタの入ったエントリが 型辞書 (下記の :attr:`tp_dict` 参照) に追加されます。

   サブタイプはこのフィールドを継承しません (メソッドは別個の メカニズムで継承されています)。


.. cmember:: struct PyMemberDef* PyTypeObject.tp_members

   オプションのフィールドです。ポインタで、 型の正規 (regular) のデータメンバ (フィールドおよびスロット) を
   宣言している:ctype:`PyMemberDef` 構造体からなる、 *NULL*で終端された静的な配列を指します。

   配列の各要素ごとに、メンバデスクリプタの入ったエントリが 型辞書 (下記の :attr:`tp_dict` 参照) に追加されます。

   サブタイプはこのフィールドを継承しません (メンバは別個の メカニズムで継承されています)。


.. cmember:: struct PyGetSetDef* PyTypeObject.tp_getset

   オプションのフィールドです。ポインタで、 インスタンスの算出属性 (computed attribute) を
   宣言している:ctype:`PyGetSetDef` 構造体からなる、 *NULL*で終端された静的な配列を指します。

   配列の各要素ごとに、getset デスクリプタの入ったエントリが 型辞書 (下記の :attr:`tp_dict` 参照) に追加されます。

   サブタイプはこのフィールドを継承しません (算出属性は別個の メカニズムで継承されています)。

   Docs for PyGetSetDef (XXX belong elsewhere)::

      typedef PyObject *(*getter)(PyObject *, void *);
      typedef int (*setter)(PyObject *, PyObject *, void *);

      typedef struct PyGetSetDef {
          char *name;    /* 属性名 */
          getter get;    /* 属性の get を行う C 関数 */
          setter set;    /* 属性の set を行う C 関数 */
          char *doc;     /* オプションの docstring  */
          void *closure; /* オプションの get/set 関数用追加データ */
      } PyGetSetDef;


.. cmember:: PyTypeObject* PyTypeObject.tp_base

   オプションのフィールドです。ポインタで、型に関するプロパティを 継承する基底タイプへのポインタです。このフィールドのレベルでは、 単継承 (single
   inheritance) だけがサポートされています; 多重継承はメタタイプの呼び出しによる動的な型オブジェクトの生成を 必要とします。

   (当たり前ですが) サブタイプはこのフィールドを継承しません。しかし、 このフィールドのデフォルト値は  (Python
   プログラマは:class:`object` 型として知っている) ``&PyBaseObject_Type`` になります。 .


.. cmember:: PyObject* PyTypeObject.tp_dict

   型の辞書は:cfunc:`PyType_Ready` によってこのフィールドに 収められます。

   このフィールドは通常、:cfunc:`PyType_Ready` を呼び出す前に *NULL* に初期化しておかねばなりません; あるいは、型の初期属性の入った
   辞書で初期化しておいてもかまいません。:cfunc:`PyType_Ready` が 型をひとたび初期化すると、型の新たな属性をこの辞書に追加できるのは、
   属性が (:meth:`__add__` のような) オーバロード用演算でないとき だけです。

   サブタイプはこのフィールドを継承しません (が、この辞書内で 定義されている属性は異なるメカニズムで継承されます)。


.. cmember:: descrgetfunc PyTypeObject.tp_descr_get

   オプションのフィールドです。ポインタで、 "デスクリプタ get" 関数を指します。

   関数のシグネチャは次のとおりです。 ::

      PyObject * tp_descr_get(PyObject *self, PyObject *obj, PyObject *type);

   XXX blah, blah.

   サブタイプはこのフィールドを継承します。


.. cmember:: descrsetfunc PyTypeObject.tp_descr_set

   オプションのフィールドです。ポインタで、 "デスクリプタ set" 関数を指します。

   関数のシグネチャは次のとおりです。 ::

      int tp_descr_set(PyObject *self, PyObject *obj, PyObject *value);

   サブタイプはこのフィールドを継承します。

   XXX blah, blah.


.. cmember:: long PyTypeObject.tp_dictoffset

   型のインスタンスにインスタンス変数の入った辞書がある場合、 このフィールドは非ゼロの値になり、型のインスタンスデータ構造体
   におけるインスタンス変数辞書へのオフセットが入ります; このオフセット値は :cfunc:`PyObject_GenericGetAttr` が 使います。

   このフィールドを :attr:`tp_dict` と混同しないでください; :attr:`tp_dict` は型オブジェクト自体の属性のための辞書です。

   このフィールドの値がゼロより大きければ、値はインスタンス構造体の 先頭からのオフセットを表します。値がゼロより小さければ、 インスタンス構造体の *末尾*
   からのオフセットを表します。 負のオフセットを使うコストは比較的高くつくので、インスタンス構造体に 可変長の部分があるときのみ使うべきです。
   例えば、:class:`str` や :class:`tuple` のサブタイプにインスタンス 辞書を追加する場合には、負のオフセットを使います。
   この場合、たとえ辞書が基本のオブジェクトレイアウトに含まれていなくても、 :attr:`tp_basicsize`
   フィールドは追加された辞書を考慮にいれなければ ならないので注意してください。ポインタサイズが 4 バイトのシステムでは、
   構造体の最後尾に辞書が宣言されていることを示す場合、 :attr:`tp_dictoffset` を``-4`` にしなければなりません。

   :attr:`tp_dictoffset` が負の場合、インスタンスにおける実際の辞書の オフセットは以下のようにして計算されます::

      dictoffset = tp_basicsize + abs(ob_size)*tp_itemsize + tp_dictoffset
      if dictoffset is not aligned on sizeof(void*):
          round up to sizeof(void*)

   ここで、:attr:`tp_basicsize`、 :attr:`tp_itemsize` および :attr:`tp_dictoffset`
   は型オブジェクトから取り出され、 :attr:`ob_size` はインスタンスから取り出されます。 長整数は符号を記憶するのに :attr:`ob_size`
   の符号を使うため、 :attr:`ob_size` は絶対値を使います。(この計算を自分で行う必要は まったくありません;
   :cfunc:`_PyObject_GetDictPtr` が やってくれます。)

   サブタイプはこのフィールドを継承しますが、以下の規則があるので 読んでください。 サブタイプはこのオフセット値をオーバライドできます; 従って、
   サブタイプでは辞書のオフセットが基底タイプとは異なる場合が あります。辞書へのオフセット常に:attr:`tp_dictoffset` で
   分かるはずなので、このことは問題にはならないはずです。

   :keyword:`class` 文で定義された型に :attr:`__slots__` 宣言が
   全くなく、かつ基底タイプの全てにインスタンス変数辞書がない場合、 辞書のスロットをインスタンスデータレイアウト構造体に追加し、
   スロットのオフセットを:attr:`tp_dictoffset` に設定します。

   :keyword:`class` 文で定義された型に :attr:`__slots__` 宣言が ある場合、この型は基底タイプから
   :attr:`tp_dictoffset` を 継承します。

   (:attr:`__dict__` という名前のスロットを :attr:`__slots__` 宣言に
   追加しても、期待どおりの効果は得られず、単に混乱を招くだけに なります。とはいえ、これは将来:attr:`__weakref__` のように
   追加されるはずです。)


.. cmember:: initproc PyTypeObject.tp_init

   オプションのフィールドです。ポインタで、 インスタンス初期化関数を指します。

   この関数はクラスにおける  :meth:`__init__` メソッドに対応 します。:meth:`__init__` と同様、:meth:`__init__`
   を呼び出さず にインスタンスを作成できます。また、:meth:`__init__` を再度 呼び出してインスタンスの再初期化もできます。

   関数のシグネチャは ::

      int tp_init(PyObject *self, PyObject *args, PyObject *kwds)

   です。

   *self* 引数は初期化するインスタンスです; *args* および *kwds* 引数は、:meth:`__init__` を呼び出す際の
   固定引数およびキーワード引数です。

   :attr:`tp_init` 関数のフィールドが *NULL*でない場合、型の呼び出し で普通にインスタンスを生成する際に、型の:attr:`tp_new`
   が インスタンスを返した後に:attr:`tp_init` が呼び出されます。 :attr:`tp_new` が元の型のサブタイプでない別の型を返す場合、
   :attr:`tp_init` は全く呼び出されません; :attr:`tp_new` が 元の型のサブタイプのインスタンスを返す場合、サブタイプの
   :attr:`tp_init` が呼び出されます。 (VERSION NOTE: ここに書かれている 内容は、Python 2.2.1
   以降での実装に関するものです。Python 2.2 では、 :attr:`tp_init` は *NULL*でない限り:attr:`tp_new` が返す全ての
   オブジェクトに対して常に呼び出されます。) not *NULL*.)

   サブタイプはこのフィールドを継承します。


.. cmember:: allocfunc PyTypeObject.tp_alloc

   オプションのフィールドです。ポインタで、 インスタンスのメモリ確保関数を指します。

   関数のシグネチャは ::

      PyObject *tp_alloc(PyTypeObject *self, Py_ssize_t nitems)

   です。

   この関数の目的は、メモリ確保をメモリ初期化から分離することにあります。 この関数は、インスタンス用の的確なサイズを持ち、適切にバイト整列
   され、ゼロで初期化され、ただし:attr:`ob_refcnt` を ``1``  にセットされ、 :attr:`ob_type` が型引数 (type
   argument) にセットされて いるようなメモリブロックを返さねばなりません。 型の :attr:`tp_itemsize`
   がゼロでない場合、オブジェクトの :attr:`ob_size` フィールドは*nitems* に初期化され、 確保されるメモリブロックの長さは
   ``tp_basicsize + nitems*tp_itemsize`` を``sizeof(void*)`` の倍数で 丸めた値になるはずです;
   それ以外の場合、*nitems* の値は使われず、 メモリブロックの長さは :attr:`tp_basicsize` になるはずです。

   この関数をインスタンス初期化の他のどの処理にも、追加でメモリ確保 をする場合でさえ使ってはなりません; そうした処理は :attr:`tp_new`
   で行わねばなりません。

   静的なサブタイプはこのフィールドを継承しますが、動的なサブタイプ (:keyword:`class` 文で生成するサブタイプ) の場合は継承しません;
   後者の場合、このフィールドは常に:cfunc:`PyType_GenericAlloc` にセットされ、標準のヒープ上メモリ確保戦略が強制されます。
   静的に定義する型の場合でも、:cfunc:`PyType_GenericAlloc` を推奨します。


.. cmember:: newfunc PyTypeObject.tp_new

   オプションのフィールドです。ポインタで、 インスタンス生成関数を指します。

   このフィールドが *NULL* を指している型では、型を呼び出して新たな インスタンスを生成できません; こうした型では、おそらくファクトリ
   関数のように、インスタンスを生成する他の方法があるはずです。

   関数のシグネチャは ::

      PyObject *tp_new(PyTypeObject *subtype, PyObject *args, PyObject *kwds)

   です。

   引数 *subtype* は生成するオブジェクトの型です;  *args* および*kwds* 引数は、型を呼び出すときの
   固定引数およびキーワード引数です。サブタイプは :attr:`tp_new` 関数 を呼び出すときに使う型と等価というわけではないので注意してください;
   :attr:`tp_new` 関数を呼び出すときに使う型 (と無関係ではない)  サブタイプのこともあります。

   :attr:`tp_new` 関数は ``subtype->tp_alloc(subtype, nitems)``
   を呼び出してオブジェクトのメモリ領域を確保し、初期化で本当に必要と される処理だけを行います。省略したり繰り返したりしても問題のない
   初期化処理は:attr:`tp_init` ハンドラ内に配置しなければなりません。 経験則からいうと、変更不能な型の場合、初期化は全て
   :attr:`tp_new` で行い、変更可能な型の場合はほとんどの初期化を :attr:`tp_init` に回すべきです。

   サブタイプはこのフィールドを継承します。例外として、 :attr:`tp_base` が*NULL* か``&PyBaseObject_Type``
   になっている静的な型では 継承しません。後者が例外になっているのは、旧式の拡張型が Python 2.2
   でリンクされたときに呼び出し可能オブジェクトにならないように するための予防措置です。


.. cmember:: destructor PyTypeObject.tp_free

   オプションのフィールドです。ポインタで、 インスタンスのメモリ解放関数を指します。

   この関数のシグネチャは少し変更されています; Python 2.2 および 2.2.1 では、シグネチャは:ctype:`destructor` ::

      void tp_free(PyObject *)

   でしたが、 Python 2.3 以降では、シグネチャは :ctype:`freefunc`::

      void tp_free(void *)

   になっています。

   両方のバージョンと互換性のある初期値は ``_PyObject_Del`` です。 ``_PyObject_Del`` の定義は Python 2.3
   で適切に対応できる よう変更されました。

   静的なサブタイプはこのフィールドを継承しますが、動的なサブタイプ (:keyword:`class` 文で生成するサブタイプ) の場合は継承しません;
   後者の場合、このフィールドには:cfunc:`PyType_GenericAlloc` と:const:`Py_TPFLAGS_HAVE_GC`
   フラグビットの値に対応させるのに ふさわしいメモリ解放関数がセットされます。


.. cmember:: inquiry PyTypeObject.tp_is_gc

   オプションのフィールドです。ポインタで、 ガベージコレクタから呼び出される関数を指します。

   ガベージコレクタは、オブジェクトがガベージとして収集可能かどうか を知る必要があります。これを知るには、通常はオブジェクトの型の
   :attr:`tp_flags` フィールドを見て、 :const:`Py_TPFLAGS_HAVE_GC`
   フラグビットを調べるだけで十分です。しかし、静的なメモリ確保と 動的なメモリ確保が混じっているインスタンスを持つような型や、
   静的にメモリ確保されたインスタンスは収集できません。こうした型では、 このフィールドに関数を定義しなければなりません; 関数は インスタンスが収集可能の場合には
   ``1`` を、 収集不能の場合には ``0`` を返さねばなりません。 シグネチャは ::

      int tp_is_gc(PyObject *self)

   です。

   (上記のような型の例は、型オブジェクト自体です。メタタイプ :cdata:`PyType_Type` は、型のメモリ確保が静的か動的かを
   区別するためにこの関数を定義しています。)

   サブタイプはこのフィールドを継承します。 (VERSION NOTE: Python 2.2 では、このフィールドは継承されませんでした。 2.2.1
   以降のバージョンから継承されるようになりました。)


.. cmember:: PyObject* PyTypeObject.tp_bases

   基底型からなるタプルです。

   :keyword:`class` 文で生成されたクラスの場合このフィールドがセット されます。静的に定義されている型の場合には、このフィールドは *NULL*
   になります。

   このフィールドは継承されません。


.. cmember:: PyObject* PyTypeObject.tp_mro

   基底クラス群を展開した集合が入っているタプルです。集合は 該当する型自体からはじまり、:class:`object` で終わります。 メソッド解決順
   (Method Resolution Order) の順に並んでいます。

   このフィールドは継承されません; フィールドの値は :cfunc:`PyType_Ready` で毎回計算されます。


.. cmember:: PyObject* PyTypeObject.tp_cache

   使用されていません。継承されません。 内部で使用するためだけのものです。


.. cmember:: PyObject* PyTypeObject.tp_subclasses

   サブクラスへの弱参照からなるリストです。継承されません。 内部で使用するためだけのものです。


.. cmember:: PyObject* PyTypeObject.tp_weaklist

   この型オブジェクトに対する弱参照からなるリストの先頭です。

残りのフィールドは、機能テスト用のマクロである :const:`COUNT_ALLOCS` が定義されている場合のみ利用でき、内部で使用するためだけのものです。
これらのフィールドについて記述するのは単に完全性のためです。 サブタイプはこれらのフィールドを継承しません。


.. cmember:: Py_ssize_t PyTypeObject.tp_allocs

   メモリ確保の回数です。


.. cmember:: Py_ssize_t PyTypeObject.tp_frees

   メモリ解放の回数です。


.. cmember:: Py_ssize_t PyTypeObject.tp_maxalloc

   同時にメモリ確保できる最大オブジェクト数です。


.. cmember:: PyTypeObject* PyTypeObject.tp_next

   :attr:`tp_allocs` フィールドが非ゼロの、(リンクリストの) 次の型 オブジェクトを指すポインタです。

また、 Python のガベージコレクションでは、*tp_dealloc* を呼び出すのはオブジェクトを生成したスレッドだけではなく、 任意の Python
スレッドかもしれないという点にも注意して下さい。 (オブジェクトが循環参照の一部の場合、任意のスレッドのガベージコレクション
によって解放されてしまうかもしれません)。Python API 側からみれば、 *tp_dealloc* を呼び出すスレッドは グローバルインタプリタロック
(GIL: Global Interpreter Lock) を獲得するので、これは問題ではありません。
しかしながら、削除されようとしているオブジェクトが何らかの C や C++ ライブラリ由来のオブジェクトを削除する場合、 *tp_dealloc* を
呼び出すスレッドのオブジェクトを削除することで、ライブラリの仮定 している何らかの規約に違反しないように気を付ける必要があります。


.. _mapping-structs:

マップ型オブジェクト構造体 (mapping object structure)
=====================================================


.. ctype:: PyMappingMethods

   拡張型でマップ型プロトコルを実装するために使われる関数群へのポインタを 保持するために使われる構造体です。


.. _number-structs:

数値オブジェクト構造体 (number object structure)
================================================


.. ctype:: PyNumberMethods

   拡張型で数値型プロトコルを実装するために使われる関数群へのポインタを 保持するために使われる構造体です。


.. _sequence-structs:

シーケンスオブジェクト構造体 (sequence object structure)
========================================================


.. ctype:: PySequenceMethods

   拡張型でシーケンス型プロトコルを実装するために使われる関数群へのポインタを 保持するために使われる構造体です。


.. _buffer-structs:

バッファオブジェクト構造体 (buffer object structure)
====================================================

.. sectionauthor:: Greg J. Stein <greg@lyra.org>


バッファインタフェースは、あるオブジェクトの内部データを一連の データチャンク (chunk) として見せるモデルを外部から利用できるようにします。
各チャンクはポインタ/データ長からなるペアで指定します。 チャンクはセグメント(:dfn:`segment`) と呼ばれ、
メモリ内に不連続的に配置されるものと想定されています。

バッファインタフェースを利用できるようにしたくないオブジェクト では、:ctype:`PyTypeObject` 構造体の
:attr:`tp_as_buffer` メンバを *NULL*にしなくてはなりません。利用できるようにする場合、 :attr:`tp_as_buffer`
は:ctype:`PyBufferProcs` 構造体を 指さねばなりません。

.. note::

   :ctype:`PyTypeObject` 構造体の :attr:`tp_flags` メンバ の値を ``0`` でなく
   :const:`Py_TPFLAGS_DEFAULT` に しておくことがとても重要です。この設定は、 :ctype:`PyBufferProcs` 構造体に
   :attr:`bf_getcharbuffer`  スロットが入っていることを Python ランタイムに教えます。 Python の古いバージョンには
   :attr:`bf_getcharbuffer` メンバが 存在しないので、古い拡張モジュールを使おうとしている新しいバージョンの Python
   インタプリタは、このメンバがあるかどうかテストしてから 使えるようにする必要があるのです。


.. ctype:: PyBufferProcs

   バッファプロトコルの実装を定義している関数群へのポインタを 保持するのに使われる構造体です。

   最初のスロットは:attr:`bf_getreadbuffer` で、 :ctype:`getreadbufferproc` 型です。 このスロットが
   *NULL*の場合、オブジェクトは内部データの 読み出しをサポートしません。そのような仕様には意味がないので、
   実装を行う側はこのスロットに値を埋めるはずですが、呼び出し側では 非 *NULL* の値かどうかきちんと調べておくべきです。

   次のスロットは :attr:`bf_getwritebuffer` で、 :ctype:`getwritebufferproc`
   型です。オブジェクトが返すバッファに 対して書き込みを許可しない場合はこのスロットを*NULL* にできます。

   第三のスロットは :attr:`bf_getsegcount` で、 :ctype:`getsegcountproc` 型です。このスロットは *NULL*
   であっては ならず、オブジェクトにいくつセグメントが入っているかを呼び出し側に 教えるために使われます。:ctype:`PyString_Type` や
   :ctype:`PyBuffer_Type` オブジェクトのような単純なオブジェクトには単一のセグメントしか入って いません。

   .. index:: single: PyType_HasFeature()

   最後のスロットは :attr:`bf_getcharbuffer` で、 :ctype:`getcharbufferproc` です。オブジェクトの
   :ctype:`PyTypeObject` 構造体における :attr:`tp_flags` フィールドに、
   :const:`Py_TPFLAGS_HAVE_GETCHARBUFFER` ビットフラグがセットされている 場合にのみ、このスロットが存在することになります。
   このスロットの使用に先立って、呼び出し側は :cfunc:`PyType_HasFeature` を使ってスロットが存在するか調べねばなりません。
   フラグが立っていても、:attr:`bf_getcharbuffer`は *NULL*のときもあり、 *NULL*はオブジェクトの内容を *8 ビット文字列*
   として利用できない ことを示します。 このスロットに入る関数も、オブジェクトの内容を 8 ビット文字列に
   変換できない場合に例外を送出することがあります。例えば、 オブジェクトが浮動小数点数を保持するように設定されたアレイの場合、 呼び出し側が
   :attr:`bf_getcharbuffer` を使って 8 ビット文字列 としてデータを取り出そうとすると例外を送出するようにできます。
   この、内部バッファを "テキスト" として取り出すという概念は、 本質的にはバイナリで、文字ベースの内容を持ったオブジェクト間の 区別に使われます。

   .. note::

      現在のポリシでは、文字 (character) はマルチバイト文字 でもかまわないと決めているように思われます。従って、 サイズ *N* のバッファが *N*
      個のキャラクタからなる とはかぎらないことになります。


.. data:: Py_TPFLAGS_HAVE_GETCHARBUFFER

   型構造体中のフラグビットで、:attr:`bf_getcharbuffer` スロットが 既知の値になっていることを示します。このフラグビットがセット
   されていたとしても、オブジェクトがバッファインタフェースをサポート していることや、:attr:`bf_getcharbuffer` スロットが
   *NULL*でない ことを示すわけではありません。


.. ctype:: Py_ssize_t (*getreadbufferproc) (PyObject *self, Py_ssize_t segment, void **ptrptr)

   ``*ptrptr``の中の読み出し可能なバッファセグメントへのポインタを返します。 この関数は例外を送出してもよく、送出する場合には ``-1``
   を返さねばなりません。 *segment* に渡す値はゼロまたは正の値で、:attr:`bf_getsegcount`
   スロット関数が返すセグメント数よりも必ず小さな値でなければなりません。 成功すると、セグメントのサイズを返し、 ``*ptrptr`` を
   そのセグメントを指すポインタ値にセットします。


.. ctype:: Py_ssize_t (*getwritebufferproc) (PyObject *self, Py_ssize_t segment, void **ptrptr)

   読み出し可能なバッファセグメントへのポインタを ``*ptrptr`` に 返し、セグメントの長さを関数の戻り値として返します。エラーによる例外の 場合には
   ``-1`` を``-1`` を返さねばなりません。 オブジェクトが呼び出し専用バッファしかサポートしていない場合には :exc:`TypeError`
   を、*segment* が存在しないセグメントを 指している場合には :exc:`SystemError` を送出しなければなりません。

   .. % Why doesn't it raise ValueError for this one?
   .. % GJS: because you shouldn't be calling it with an invalid
   .. % segment. That indicates a blatant programming error in the C
   .. % code.


.. ctype:: Py_ssize_t (*getsegcountproc) (PyObject *self, Py_ssize_t *lenp)

   バッファを構成するメモリセグメントの数を返します。 *lenp* が *NULL*でない場合、この関数の実装は全てのセグメント のサイズ (バイト単位)
   の合計値を ``*lenp`` を介して 報告しなければなりません。この関数呼び出しは失敗させられません。


.. ctype:: Py_ssize_t (*getcharbufferproc) (PyObject *self, Py_ssize_t segment, const char **ptrptr)

   セグメント *segment* のメモリバッファを *ptrptr* に入れ、 そのサイズを返します。エラーのときに ``-1`` を返します。


.. _supporting-iteration:

イテレータプロトコルをサポートする
==================================


.. _supporting-cycle-detection:

循環参照ガベージコレクションをサポートする
==========================================

Python が循環参照を含むガベージの検出とコレクションをサポートする には、他のオブジェクトに対する "コンテナ" (他のオブジェクトには
他のコンテナも含みます) となるオブジェクト型によるサポートが必要です。 他のオブジェクトに対する参照を記憶しないオブジェクトや、 (数値や文字列のような)
アトム型 (atomic type) への参照だけを 記憶するような型では、ガベージコレクションに際して特別これといった サポートを提供する必要はありません。

ここで説明しているインタフェースの使い方を示した例は、 Python の拡張と埋め込み (XXX reference: ../ext/ext.html) の
"循環参照の収集をサポートする (XXX reference: ../ext/example-cycle-support.html)" にあります。
コンテナ型を作るには、型オブジェクトの :attr:`tp_flags` フィールド に:const:`Py_TPFLAGS_HAVE_GC`
フラグがなくてはならず、 :attr:`tp_traverse` ハンドラの実装を提供しなければなりません。
実装する型のインスタンスを変更可能なオブジェクトにするなら、 :attr:`tp_clear` の実装も提供しなければなりません。


.. data:: Py_TPFLAGS_HAVE_GC

   このフラグをセットした型のオブジェクトは、この節に述べた規則に 適合しなければなりません。簡単のため、このフラグをセットした型の
   オブジェクトをコンテナオブジェクトと呼びます。

コンテナ型のコンストラクタは以下の二つの規則に適合しなければなりません:

#. オブジェクトのメモリは :cfunc:`PyObject_GC_New` または :cfunc:`PyObject_GC_VarNew`
   で確保しなければなりません。

#. 一度他のコンテナへの参照が入るかもしれないフィールドが全て 初期化されたら、:cfunc:`PyObject_GC_Track` を呼び出さねば
   なりません。


.. cfunction:: TYPE* PyObject_GC_New(TYPE, PyTypeObject *type)

   :cfunc:`PyObject_New` に似ていますが、 :const:`Py_TPFLAGS_HAVE_GC` のセットされたコンテナオブジェクト
   用です。


.. cfunction:: TYPE* PyObject_GC_NewVar(TYPE, PyTypeObject *type, Py_ssize_t size)

   :cfunc:`PyObject_NewVar` に似ていますが、 :const:`Py_TPFLAGS_HAVE_GC` のセットされたコンテナオブジェクト
   用です。


.. cfunction:: PyVarObject * PyObject_GC_Resize(PyVarObject *op, Py_ssize_t)

   :cfunc:`PyObject_NewVar` が確保したオブジェクトのメモリを リサイズします。リサイズされたオブジェクトを返します。 失敗すると
   *NULL* を返します。


.. cfunction:: void PyObject_GC_Track(PyObject *op)

   ガベージコレクタが追跡しているコンテナオブジェクトの集合に オブジェクト *op* を追加します。ガベージコレクタの動作する
   回数は予測不能なので、追加対象にするオブジェクトは追跡されている 間ずっと有効なオブジェクトでなければなりません。
   この関数は、通常コンストラクタの最後付近で、:attr:`tp_traverse` ハンドラ以降の全てのフィールドが有効な値になった時点で呼び出さねば
   なりません。


.. cfunction:: void _PyObject_GC_TRACK(PyObject *op)

   :cfunc:`PyObject_GC_Track` のマクロ版です。拡張モジュールに 使ってはなりません。

同様に、オブジェクトのメモリ解放関数も以下の二つの規則に適合しなければ なりません:

#. 他のコンテナを参照しているフィールドを無効化する前に、 :cfunc:`PyObject_GC_UnTrack` を呼び出さねばなりません。

#. オブジェクトのメモリは :cfunc:`PyObject_GC_Del` で解放しなければなりません。


.. cfunction:: void PyObject_GC_Del(void *op)

   :cfunc:`PyObject_GC_New` や :cfunc:`PyObject_GC_NewVar` を使って確保されたメモリを解放します。


.. cfunction:: void PyObject_GC_UnTrack(void *op)

   ガベージコレクタが追跡しているコンテナオブジェクトの集合から オブジェクト *op* を除去します。:cfunc:`PyObject_GC_Track`
   を呼び出して、除去したオブジェクトを再度追跡対象セットに追加 できるので注意してください。メモリ解放関数 (deallocator,
   :attr:`tp_dealloc` ハンドラ) は、:attr:`tp_traverse` ハンドラが 使用しているフィールドのいずれかが無効化されるよりも
   以前にオブジェクトに対して呼び出されていなければなりません。


.. cfunction:: void _PyObject_GC_UNTRACK(PyObject *op)

   :cfunc:`PyObject_GC_UnTrack` のマクロ版です。拡張モジュールに 使ってはなりません。

:attr:`tp_traverse` ハンドラは以下の型を持つ関数を引数の一つとして とります:


.. ctype:: int (*visitproc)(PyObject *object, void *arg)

   :attr:`tp_traverse` ハンドラに渡すビジタ関数 (visitor function)  の型です。この関数は追跡すべきオブジェクトを
   *object* に、 :attr:`tp_traverse` ハンドラの第三引数を *arg* にして呼び出され ます。Python
   のコア部分では、ガベージコレクションの実装に複数の ビジタ関数を使っています。ユーザが独自にビジタ関数を書く必要がある とは想定されていません。

:attr:`tp_traverse` ハンドラは以下の型でなければなりません:


.. ctype:: int (*traverseproc)(PyObject *self, visitproc visit, void *arg)

   コンテナオブジェクトのためのトラバーサル関数 (traversal function) です。 実装では、*self*
   に直接入っている各オブジェクトに対して*visit*  関数を呼び出さねばなりません。このとき、*visit* へのパラメタは
   コンテナに入っている各オブジェクトと、このハンドラに渡された *arg* の値です。*visit* 関数は *NULL* オブジェクトを引数に
   渡して呼び出してはなりません。*visit* が非ゼロの値を返す場合、 エラーが発生し、戻り値をそのまま返すようににしなければなりません。

:attr:`tp_traverse` ハンドラの作成を単純化するため、:cfunc:`Py_VISIT`
マクロが提供されています。このマクロを使うには、:attr:`tp_traverse` の 実装で、引数を *visit* および *arg*
という名前にしておかねば なりません:


.. cfunction:: void Py_VISIT(PyObject *o)

   引数 *o* および *arg* を使って*visit* コールバックを呼び出し ます。*visit* が非ゼロの値を返した場合、その値をそのまま返します。
   このマクロを使えば、:attr:`tp_traverse` ハンドラは以下のようになります::

      static int
      my_traverse(Noddy *self, visitproc visit, void *arg)
      {
          Py_VISIT(self->foo);
          Py_VISIT(self->bar);
          return 0;
      }

   .. versionadded:: 2.4

:attr:`tp_clear` ハンドラは :ctype:`inquiry` 型にするか、 オブジェクトが変更不能の場合には *NULL*
にしなければなりません。 *NULL* if the object is immutable.


.. ctype:: int (*inquiry)(PyObject *self)

   循環参照を形成しているとおぼしき参照群を放棄します。 変更不可能なオブジェクトは循環参照を直接形成することが決してない
   ので、この関数を定義する必要はありません。 このメソッドを呼び出した後でもオブジェクトは有効なままでなければ ならないので注意してください (参照に対して
   :cfunc:`Py_DECREF` を呼ぶだけにしないでください)。ガベージコレクタは、オブジェクトが
   循環参照を形成していることを検出した際にこのメソッドを呼び出します。

