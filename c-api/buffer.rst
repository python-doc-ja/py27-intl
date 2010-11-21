.. highlightlang:: c

.. _bufferobjects:

バッファーオブジェクト
----------------------

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


.. cfunction:: PyObject* PyBuffer_FromObject(PyObject *base, Py_ssize_t offset, Py_ssize_t size)

   新たな読み出し専用バッファオブジェクトを返します。 *base* が読み出し専用バッファに必要なバッファプロトコルをサポートしていない
   場合や、厳密に一つのバッファセグメントを提供していない場合には :exc:`TypeError` を送出し、 *offset* がゼロ以下の場合には
   :exc:`ValueError` を送出します。バッファオブジェクトはは *base* オブジェクトに対する参照を保持し、バッファオブジェクトのの内容は
   *base* オブジェクトの *offset* から *size* バイトのバッファインタフェースへの参照になります。 *size* が
   :const:`Py_END_OF_BUFFER` の場合、新たに作成するバッファオブジェクトの内容は *base* から公開されているバッファの
   末尾までにわたります。


.. cfunction:: PyObject* PyBuffer_FromReadWriteObject(PyObject *base, Py_ssize_t offset, Py_ssize_t size)

   新たな書き込み可能バッファオブジェクトを返します。パラメタおよび例外は :cfunc:`PyBuffer_FromObject` と同じです。 *base*
   オブジェクトが書き込み可能バッファに必要なバッファプロトコルを公開していない場合、 :exc:`TypeError` を送出します。


.. cfunction:: PyObject* PyBuffer_FromMemory(void *ptr, Py_ssize_t size)

   メモリ上の指定された場所から指定されたサイズのデータを読み出せる、新たな読み出し専用バッファオブジェクトを返します。
   この関数が返すバッファオブジェクトが存続する間、 *ptr* で与えられたメモリバッファがデアロケートされないようにするのは呼び出し側の責任です。 *size*
   がゼロ以下の場合には :exc:`ValueError` を送出します。 *size* には :const:`Py_END_OF_BUFFER` を指定しては
   *なりません* ; 指定すると、 :exc:`ValueError` を送出します。


.. cfunction:: PyObject* PyBuffer_FromReadWriteMemory(void *ptr, Py_ssize_t size)

   :cfunc:`PyBuffer_FromMemory` に似ていますが、書き込み可能なバッファを返します。


.. cfunction:: PyObject* PyBuffer_New(Py_ssize_t size)

   *size* バイトのメモリバッファを独自に維持する新たな書き込み可能バッファオブジェクトを返します。 *size*
   がゼロまたは正の値でない場合、 :exc:`ValueError` を送出します。(:cfunc:`PyObject_AsWriteBuffer`
   が返すような) メモリバッファは特に整列されていないので注意して下さい。


