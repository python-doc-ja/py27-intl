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
対象となるオブジェクトからデータを返させる  :c:func:`PyArg_ParseTuple` には数多くのデータ書式化コードがあります。

バージョン 1.6 から、Python は Python レベルのバッファオブジェクトと、
C 言語レベルのバッファAPIを提供しており、任意のビルトイン型やユーザー定義型は
その文字列表現を公開することができます。
しかし、両方共、幾つかの欠点のために廃止予定扱いされていて、
Python 3.0 では公式に削除され、新しい C 言語レベルのバッファAPIと
新しい Python レベルの :class:`memoryview` という名前のオブジェクトに
置き換えられています。

新しいバッファAPIは Python 2.6 に逆移植されており、 :class:`memoryviews`
オブジェクトは Python 2.7 に逆移植されています。
古いバージョンとの互換性が必要なければ、古いAPIの代わりにこれらを使うことをおすすめします。


新スタイル Py_buffer 構造体
==============================


.. ctype:: Py_buffer

   .. cmember:: void *buf

      オブジェクトのメモリの開始位置へのポインタ

   .. cmember:: Py_ssize_t len
      :noindex:

      メモリのトータルサイズ[byte]

   .. cmember:: int readonly

      バッファが読み込み専用かどうかを示す

   .. cmember:: const char *format
      :noindex:

      バッファを通してアクセスできる要素の形式を指定する、 :mod:`struct`
      モジュールスタイル文法の、 *NULL* 終端文字列。
      このポインタの値が *NULL* なら、 ``"B"`` (符号無しバイト) として扱われます。

   .. cmember:: int ndim

      メモリが多次元配列を表している時の次元数。 0 の場合、 :c:data:`strides`
      と :c:data:`suboffsets` は *NULL* でなければなりません。

   .. cmember:: Py_ssize_t *shape

      メモリが多次元配列を表しているとき、その形を示す長さ :c:data:`ndim` の
      :c:type:`Py_ssize_t` の配列。
      ``((*shape)[0] * ... * (*shape)[ndims-1])*itemsize`` は :c:data:`len`
      と等しくなければならないことに気をつけてください。

   .. cmember:: Py_ssize_t *strides

      各次元で次の要素を得るためにスキップするバイト数を示す、長さ :c:data:`ndim`
      の :c:type:`Py_ssize_t` の配列。

   .. cmember:: Py_ssize_t *suboffsets

      長さ :c:data:`ndim` の、 :c:type:`Py_ssize_t` の配列。
      suboffset の各数値が0以上であるとき、その次元に格納されているのはポインタで、
      suboffset の値はそのポインタの参照を解決するときに何バイトのオフセットを足すかを
      示しています。
      suboffset に負の数が格納されているときは、参照解決が不要であること
      (連続したメモリブロック内に直接配置されていること)を意味しています。

      次の例は、 strides も suboffsets も非NULL の時に、N次元配列からN次元インデックスで
      示される要素のポインタを返す関数です。 ::

          void *get_item_pointer(int ndim, void *buf, Py_ssize_t *strides,
              Py_ssize_t *suboffsets, Py_ssize_t *indices) {
              char *pointer = (char*)buf;
              int i;
              for (i = 0; i < ndim; i++) {
                  pointer += strides[i] * indices[i];
                  if (suboffsets[i] >=0 ) {
                      pointer = *((char**)pointer) + suboffsets[i];
                  }
              }
              return (void*)pointer;
           }


   .. cmember:: Py_ssize_t itemsize

      これは共有メモリ上の各要素のbyte単位のサイズを格納する変数です。
      これは :c:func:`PyBuffer_SizeFromFormat` を使って計算できる値なので
      技術的には不要なのですが、バッファを提供する側はフォーマット文字列を
      解析しなくてもこの情報を知っているでしょうし、バッファを受け取る側に
      とっては正しく解釈するのに必要な情報です。なので、要素サイズを格納する
      ほうが便利ですし高速です。

   .. cmember:: void *internal

      バッファを提供する側のオブジェクトが内部的に利用するための変数です。
      例えば、提供側はこの変数に整数型をキャストして、 shape, strides, suboffsets
      といった配列をバッファを開放するときに同時に開放するべきかどうかを
      管理するフラグに使うことができるでしょう。
      バッファを受け取る側は、この値を変更してはなりません。


バッファ関連関数
========================


.. cfunction:: int PyObject_CheckBuffer(PyObject *obj)

   *obj* がバッファインタフェースをサポートしている場合に 1 を、
   それ以外の場合に 0 を返します。


.. cfunction:: int PyObject_GetBuffer(PyObject *obj, Py_buffer *view, int flags)

      *obj* を :c:type:`Py_buffer` *view* へエクスポートします。
      これらの引数は *NULL* であってはなりません。
      *flag* 引数は呼び出し側がどんなバッファを扱おうとしているのか、
      バッファ提供側がどんなバッファを返すことが許されているのかを示す、
      ビットフィールドです。
      バッファインタフェースは複雑なメモリ共有を可能にしていますが、呼び出し元は
      すべての複雑なバッファを扱えるとは限らず、バッファ提供側がシンプルなビューを
      提供できるならそれを利用したいとかもしれません。

      バッファ提供側はすべての方法でメモリを共有できるとは限らず、呼び出し側に
      何かが不可能であることを伝えるためにエラーを発生させる必要があるかもしれません。
      その場合のエラーは、もしその問題を実際に引き起こしているのが別のエラーだったとしても、
      :exc:`BufferError` でなければなりません。
      バッファ提供側は flag の情報を使って :c:data:`Py_buffer` 構造体のどのフィールドへの
      非デフォルト値の設定を省略したり、要求されたシンプルな view を提供できない場合は
      エラーを発生させたりすることができます。

      成功したら 0 が、エラー時には -1 が返されます。

      次のテーブルは、 *flags* 引数が取りうる値です。

      +-----------------------------------+--------------------------------------------------------------+
      | Flag                              | 説明                                                         |
      +===================================+==============================================================+
      | :c:macro:`PyBUF_SIMPLE`           | これはデフォルトの flag の状態です。                         |
      |                                   | 結果のバッファは書き込み可能かもしれませんし、不可能かも     |
      |                                   | しれません。データのフォーマットは unsigned byte とします。  |
      |                                   | これは "スタンドアロン" のフラグ定数です。他の定数と '|'     |
      |                                   | する必要はありません。                                       |
      |                                   | 提供側はこのような連続したバイト列のバッファを提供できない   |
      |                                   | 場合に、エラーを発生させるかもしれません。                   |
      |                                   |                                                              |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_WRITABLE`         | 結果のバッファは書込み可能でなければなりません。             |
      |                                   | 書き込み不可能な場合はエラーを発生させます。                 |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_STRIDES`          | この値は :c:macro:`PyBUF_ND` を含みます。                    |
      |                                   | バッファは strides 情報を提供しなければなりません。          |
      |                                   | (言い換えると、 strides は NULL ではなりません。)            |
      |                                   | このフラグは、呼び出し元が、要素間に隙間のある不連続な       |
      |                                   | 配列を扱えるときに使われます。 strides を扱うことは、        |
      |                                   | 自動的に shape も扱えることを要求されます。                  |
      |                                   | 提供側は stride 形式のバッファを提供できないとき(例えば、    |
      |                                   | suboffset が必要な場合)はエラーを発生させます。              |
      |                                   |                                                              |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_ND`               | バッファは shape 情報を提供しなければなりません。            |
      |                                   | メモリは C スタイルの並び (最後の次元が一番高速) だと仮定    |
      |                                   | されます。提供側はこの種類の連続バッファを提供できない場合は |
      |                                   | エラーを発生させます。このフラグが指定されていな場合は shape |
      |                                   | は *NULL* になります。                                       |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_C_CONTIGUOUS`     | これらのフラグは、返されるバッファの並びを指定します。       |
      | :c:macro:`PyBUF_F_CONTIGUOUS`     | それぞれ、C並び(最後の次元が一番高速)、Fortran並び(最初の    |
      | :c:macro:`PyBUF_ANY_CONTIGUOUS`   | 次元が一番高速), そのどちらでも、を意味します。              |
      |                                   | これらのフラグは :c:macro:`PyBUF_STRIDES` を含んでおり、     |
      |                                   | strides 情報が正しく格納されていることを保証します。         |
      |                                   |                                                              |
      |                                   |                                                              |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_INDIRECT`         | このフラグは、返されるバッファが suboffsets 情報を含んで     |
      |                                   | いることを示します。(suboffsets が必要無いときは NULL でも   |
      |                                   | かまいません。) このフラグは、バッファ利用側が suboffsets    |
      |                                   | を使って参照されている間接配列を扱えるときに利用されます。   |
      |                                   | このフラグは :c:macro:`PyBUF_STRIDES` を含みます。           |
      |                                   |                                                              |
      |                                   |                                                              |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_FORMAT`           | 返されるバッファは正しい format 情報を持っていなければ       |
      |                                   | なりません。このフラグは、バッファ利用側が実際に格納されて   |
      |                                   | いるデータの '種類' をチェックするときに利用します。         |
      |                                   | バッファ提供側は、要求された場合は常にこの情報を提供できる   |
      |                                   | べきです。 format が明示的に要求されていない場合は format は |
      |                                   | *NULL* (``'B'``, unsigned byte を意味する)であるべきです。   |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_STRIDED`          | ``(PyBUF_STRIDES | PyBUF_WRITABLE)`` と同じ                  |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_STRIDED_RO`       | ``(PyBUF_STRIDES)`` と同じ                                   |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_RECORDS`          | ``(PyBUF_STRIDES | PyBUF_FORMAT | PyBUF_WRITABLE)`` と同じ   |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_RECORDS_RO`       | ``(PyBUF_STRIDES | PyBUF_FORMAT)`` と同じ                    |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_FULL`             | ``(PyBUF_INDIRECT | PyBUF_FORMAT | PyBUF_WRITABLE)`` と同じ  |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_FULL_RO`          | ``(PyBUF_INDIRECT | PyBUF_FORMAT)`` と同じ                   |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_CONTIG`           | ``(PyBUF_ND | PyBUF_WRITABLE)`` と同じ                       |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_CONTIG_RO`        | ``(PyBUF_ND)`` と同じ                                        |
      +-----------------------------------+--------------------------------------------------------------+


.. cfunction:: void PyBuffer_Release(Py_buffer *view)

   *view* バッファを開放します。
   バッファが利用されなくなったときに、そのメモリを開放できるようにこの関数を呼び出すべきです。

.. todo::
   以下の2つの関数は実装が存在しない。問い合わせ中。

   .. cfunction:: Py_ssize_t PyBuffer_SizeFromFormat(const char *)

      :c:data:`~Py_buffer.itemsize` の値を :c:data:`~PyBuffer.format` から返します。

   .. cfunction:: int PyObject_CopyToObject(PyObject *obj, void *buf, Py_ssize_t len, char fortran)

      Copy *len* bytes of data pointed to by the contiguous chunk of memory
      pointed to by *buf* into the buffer exported by obj.  The buffer must of
      course be writable.  Return 0 on success and return -1 and raise an error
      on failure.  If the object does not have a writable buffer, then an error
      is raised.  If *fortran* is ``'F'``, then if the object is
      multi-dimensional, then the data will be copied into the array in
      Fortran-style (first dimension varies the fastest).  If *fortran* is
      ``'C'``, then the data will be copied into the array in C-style (last
      dimension varies the fastest).  If *fortran* is ``'A'``, then it does not
      matter and the copy will be made in whatever way is more efficient.


.. cfunction:: int PyBuffer_IsContiguous(Py_buffer *view, char fortran)

   *view* で定義されているメモリが、(*fortran* == ``'C'`` のとき) C-styleか、
   (*fortran* == ``'F'`` のとき) Fortran-style か、 (*fortran* == ``'A'``
   のとき) そのいずれかであれば 1 を返します。
   それ以外の場合は 0 を返します。


.. cfunction:: void PyBuffer_FillContiguousStrides(int ndim, Py_ssize_t *shape, Py_ssize_t *strides, Py_ssize_t itemsize, char fortran)

   *strides* 配列を、 *itemsize* の大きさの要素がバイト単位で連続した、
   *shape* の形をした (*fortran* が ``'C'`` なら C-style, *fortran* が ``'F'``
   なら Fortran-style の) 多次元配列として埋める。


.. cfunction:: int PyBuffer_FillInfo(Py_buffer *view, PyObject *obj, void *buf, Py_ssize_t len, int readonly, int infoflags)

   Fill in a buffer-info structure, *view*, correctly for an exporter that can
   only share a contiguous chunk of memory of "unsigned bytes" of the given
   length.  Return 0 on success and -1 (with raising an error) on error.
   バッファ提供側が与えられた長さの "unsigned bytes" の連続した1つのメモリブロックしか
   提供できないものとして、 *view* バッファ情報構造体を正しく埋める。
   成功したら 0 を、エラー時には(例外を発生させつつ) -1 を返す。


旧スタイルバッファオブジェクト
=================================

.. index:: single: PyBufferProcs

バッファインタフェースに関するより詳しい情報は、 "バッファオブジェクト構造体" 節 ( :ref:`buffer-structs` 節) の、
:c:type:`PyBufferProcs` の説明のところにあります。

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

   この :c:type:`PyObject` のサブタイプはバッファオブジェクトを表現します。


.. cvar:: PyTypeObject PyBuffer_Type

   .. index:: single: BufferType (in module types)

   Python バッファ型 (buffer type) を表現する :c:type:`PyTypeObject` です; Python レイヤにおける
   ``buffer`` や ``types.BufferType`` と同じオブジェクトです。


.. cvar:: int Py_END_OF_BUFFER

   この定数は、 :c:func:`PyBuffer_FromObject` またはの :c:func:`PyBuffer_FromReadWriteObject`
   *size* パラメタに渡します。このパラメタを渡すと、 :c:type:`PyBufferObject` は指定された *offset*
   からバッファの終わりまでを *base* オブジェクトとして参照します。このパラメタを使うことで、関数の呼び出し側が *base* オブジェクト
   のサイズを調べる必要がなくなります。


.. cfunction:: int PyBuffer_Check(PyObject *p)

   引数が :c:data:`PyBuffer_Type` 型のときに真を返します。


.. cfunction:: PyObject* PyBuffer_FromObject(PyObject *base, Py_ssize_t offset, Py_ssize_t size)

   新たな読み出し専用バッファオブジェクトを返します。 *base* が読み出し専用バッファに必要なバッファプロトコルをサポートしていない
   場合や、厳密に一つのバッファセグメントを提供していない場合には :exc:`TypeError` を送出し、 *offset* がゼロ以下の場合には
   :exc:`ValueError` を送出します。バッファオブジェクトはは *base* オブジェクトに対する参照を保持し、バッファオブジェクトのの内容は
   *base* オブジェクトの *offset* から *size* バイトのバッファインタフェースへの参照になります。 *size* が
   :const:`Py_END_OF_BUFFER` の場合、新たに作成するバッファオブジェクトの内容は *base* から公開されているバッファの
   末尾までにわたります。

   .. versionchanged:: 2.5
      この関数は以前は *offset*, *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: PyObject* PyBuffer_FromReadWriteObject(PyObject *base, Py_ssize_t offset, Py_ssize_t size)

   新たな書き込み可能バッファオブジェクトを返します。パラメタおよび例外は :c:func:`PyBuffer_FromObject` と同じです。 *base*
   オブジェクトが書き込み可能バッファに必要なバッファプロトコルを公開していない場合、 :exc:`TypeError` を送出します。

   .. versionchanged:: 2.5
      この関数は以前は *offset*, *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. cfunction:: PyObject* PyBuffer_FromMemory(void *ptr, Py_ssize_t size)

   メモリ上の指定された場所から指定されたサイズのデータを読み出せる、新たな読み出し専用バッファオブジェクトを返します。
   この関数が返すバッファオブジェクトが存続する間、 *ptr* で与えられたメモリバッファがデアロケートされないようにするのは呼び出し側の責任です。 *size*
   がゼロ以下の場合には :exc:`ValueError` を送出します。 *size* には :const:`Py_END_OF_BUFFER` を指定しては
   *なりません* ; 指定すると、 :exc:`ValueError` を送出します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. cfunction:: PyObject* PyBuffer_FromReadWriteMemory(void *ptr, Py_ssize_t size)

   :c:func:`PyBuffer_FromMemory` に似ていますが、書き込み可能なバッファを返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. cfunction:: PyObject* PyBuffer_New(Py_ssize_t size)

   *size* バイトのメモリバッファを独自に維持する新たな書き込み可能バッファオブジェクトを返します。 *size*
   がゼロまたは正の値でない場合、 :exc:`ValueError` を送出します。(:c:func:`PyObject_AsWriteBuffer`
   が返すような) メモリバッファは特に整列されていないので注意して下さい。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

