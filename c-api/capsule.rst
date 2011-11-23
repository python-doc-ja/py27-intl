.. highlightlang:: c

.. _capsules:

カプセル (Capsules)
---------------------

.. index:: object: Capsule

`using-capsules` 以下のオブジェクトを使う方法については :ref:`using-capsules`
を参照してください。


.. ctype:: PyCapsule

   この :ctype:`PyObject` のサブタイプは、任意の値を表し、C拡張モジュールから
   Pythonコードを経由して他のC言語のコードに任意の値を(:ctype:`void\*` ポインタ
   の形で)渡す必要があるときに有用です。
   あるモジュール内で定義されているC言語関数のポインタを、他のモジュールに渡して
   そこから呼び出せるようにするためによく使われます。これにより、動的にロードされる
   モジュールの中の C API に通常の import 機構を通してアクセスすることができます。

.. ctype:: PyCapsule_Destructor

   カプセルに対するデストラクタコールバック型. 次のように定義されます::

      typedef void (*PyCapsule_Destructor)(PyObject *);

   PyCapsule_Destructor コールバックの動作については :cfunc:`PyCapsule_New`
   を参照してください。


.. cfunction:: int PyCapsule_CheckExact(PyObject *p)

   引数が :ctype:`PyCapsule` だったときに true を返します。


.. cfunction:: PyObject* PyCapsule_New(void *pointer, const char *name, PyCapsule_Destructor destructor)

   *pointer* を格納する :ctype:`PyCapsule` を作成します。
   *pointer* 引数は *NULL* であってはなりません。

   失敗した場合、例外を設定して *NULL* を返します。

   *name* 文字列は *NULL* か、有効なC文字列へのポインタです。
   *NULL* で無い場合、この文字列は少なくともカプセルより長く生存する必要があります。
   (*destructor* の中で解放することは許可されています)

   *destructor* が *NULL* で無い場合、カプセルが削除されるときにそのカプセルを
   引数として呼び出されます。

   このカプセルがモジュールの属性として保存される場合、 *name* は
   ``modulename.attributename`` と指定されるべきです。
   こうすると、他のモジュールがそのカプセルを :cfunc:`PyCapsule_Import` で
   インポートすることができます。


.. cfunction:: void* PyCapsule_GetPointer(PyObject *capsule, const char *name)

   カプセルに保存されている *pointer* を取り出します。失敗した場合は
   例外を設定して *NULL* を返します。

   *name* 引数はカプセルに保存されている名前と正確に一致しなければなりません。
   もしカプセルに格納されている name が *NULL* なら、この関数の *name* 引数も
   同じく *NULL* でなければなりません。 Python は C言語の :cfunc:`strcmp`
   を使ってこの name を比較します。


.. cfunction:: PyCapsule_Destructor PyCapsule_GetDestructor(PyObject *capsule)

   カプセルに保存されている現在のデストラクタを返します。
   失敗した場合、例外を設定して *NULL* を返します。

   カプセルは *NULL* をデストラクタとして持つことができます。
   従って、戻り値の *NULL* がエラーを指してない可能性があります。
   :cfunc:`PyCapsule_IsValid` か `PyErr_Occurred` を利用して確認してください。


.. cfunction:: void* PyCapsule_GetContext(PyObject *capsule)

   カプセルに保存されている現在のコンテキスト(context)を返します。
   失敗した場合、例外を設定して *NULL* を返します。

   カプセルは *NULL* をコンテキストとして持つことができます。
   従って、戻り値の *NULL* がエラーを指してない可能性があります。
   :cfunc:`PyCapsule_IsValid` か `PyErr_Occurred` を利用して確認してください。


.. cfunction:: const char* PyCapsule_GetName(PyObject *capsule)

   カプセルに保存されている現在の name を返します。
   失敗した場合、例外を設定して *NULL* を返します。

   カプセルは *NULL* を name として持つことができます。
   従って、戻り値の *NULL* がエラーを指してない可能性があります。
   :cfunc:`PyCapsule_IsValid` か `PyErr_Occurred` を利用して確認してください。


.. cfunction:: void* PyCapsule_Import(const char *name, int no_block)

   モジュールのカプセル属性から Cオブジェクトへのポインタをインポートします。
   *name* 引数はその属性の完全名を ``module.attribute`` のように指定しなければなりません。
   カプセルに格納されている *name* はこの文字列に正確に一致しなければなりません。
   *no_block* が真の時、モジュールを(:cfunc:`PyImport_InportModuleNoBlock` を使って)
   ブロックせずにインポートします。 *no_block* が偽の時、モジュールは (:cfunc:`PyImport_ImportModule`
   を使って) 通常の方法でインポートされます。

   成功した場合、カプセル内部の *pointer* を返します。
   失敗した場合、例外を設定して *NULL* を返します。ただし、 *no_block* が真だった場合は、
   :cfunc:`PyCapsule_Import` はモジュールのインポートに失敗しても例外を設定しません。

.. cfunction:: int PyCapsule_IsValid(PyObject *capsule, const char *name)

   *capsule* が有効なカプセルであるかどうかをチェックします。
   有効な *capsule* は、非 *NULL* で、 :cfunc:`PyCapsule_CheckExact` をパスし、
   非 *NULL* なポインタを格納していて、内部の name が引数 *name* とマッチします。
   (name の比較方法については :cfunc:`PyCapsule_GetPointer` を参照)

   言い換えると、 :cfunc:`PyCapsule_IsValid` が真を返す場合、全てのアクセッサ
   (:cfunc:`PyCapsule_Get` で始まる全ての関数) が成功することが保証されます。

   オブジェクトが有効で name がマッチした場合に非0を、それ以外の場合に 0 を返します。
   この関数は絶対に失敗しません。

.. cfunction:: int PyCapsule_SetContext(PyObject *capsule, void *context)

   *capsule* 内部のコンテキストポインタを *context* に設定します。

   成功したら 0 を、失敗したら例外を設定して 非0 を返します。

.. cfunction:: int PyCapsule_SetDestructor(PyObject *capsule, PyCapsule_Destructor destructor)

   *capsule* 内部のデストラクタを *destructor* に設定します。

   成功したら 0 を、失敗したら例外を設定して 非0 を返します。

.. cfunction:: int PyCapsule_SetName(PyObject *capsule, const char *name)

   *capsule* 内部の name を *name* に設定します。 *name* が非 *NULL* のとき、
   それは *capsule* よりも長い寿命を持つ必要があります。
   もしすでに *capsule* に非 *NULL* の *name* が保存されていた場合、それに対する
   開放は行われません。

   成功したら 0 を、失敗したら例外を設定して 非0 を返します。

.. cfunction:: int PyCapsule_SetPointer(PyObject *capsule, void *pointer)

   *capsule* 内部のポインタを *pointer* に設定します。 *pointer* は *NULL*
   であってはなりません。

   成功したら 0 を、失敗したら例外を設定して 非0 を返します。
