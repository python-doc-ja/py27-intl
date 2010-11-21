.. highlightlang:: c

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


.. cfunction:: PyObject* PyFile_FromString(char *filename, char *mode)

   .. index:: single: fopen()

   成功すると、 *filename* に指定した名前のファイルを *mode* に指定したファイルモードで開いて得た新たなファイルオブジェクトを返します。
   *mode* のセマンティクスは標準 C ルーチン :cfunc:`fopen` と同じです。失敗すると *NULL* を返します。


.. cfunction:: PyObject* PyFile_FromFile(FILE *fp, char *name, char *mode, int (*close)(FILE*))

   すでに開かれている標準 C ファイルポインタ *fp* から新たな :ctype:`PyFileObject` を生成します。この関数で生成した
   ファイルオブジェクトは、閉じる際に *close* に指定した関数を呼び出します。失敗すると *NULL* を返します。


.. cfunction:: FILE* PyFile_AsFile(PyObject *p)

   *p* に関連付けられたファイルオブジェクトを :ctype:`FILE\*` で返します。


.. cfunction:: PyObject* PyFile_GetLine(PyObject *p, int n)

   .. index:: single: EOFError (built-in exception)

   ``p.readline([*n*])`` と同じで、この関数はオブジェクト *p* の各行を読み出します。 *p* は
   ファイルオブジェクトか、 :meth:`readline` メソッドを持つ何らかのオブジェクトでかまいません。 *n* が ``0`` の場合、
   行の長さに関係なく正確に 1 行だけ読み出します。 *n* が ``0`` より大きければ、 *n* バイト以上のデータは読み出しません;
   従って、行の一部だけが返される場合があります。どちらの場合でも、読み出し後すぐにファイルの終端に到達した場合には空文字列を返します。 *n* が ``0``
   より小さければ、長さに関わらず 1 行だけを読み出しますが、すぐにファイルの終端に到達した場合には :exc:`EOFError` を送出します。


.. cfunction:: PyObject* PyFile_Name(PyObject *p)

   *p* に指定したファイルの名前を文字列オブジェクトで返します。


.. cfunction:: void PyFile_SetBufSize(PyFileObject *p, int n)

   .. index:: single: setvbuf()

   :cfunc:`setvbuf` があるシステムでのみ利用できます。この関数を呼び出してよいのはファイルオブジェクトの生成直後のみです。


.. cfunction:: int PyFile_SetEncoding(PyFileObject *p, const char *enc)

   Unicode オブジェクトをファイルに出力するときにのエンコード方式を *enc* にします。成功すると ``1`` を、失敗すると ``0`` を返します。

   .. versionadded:: 2.3


.. cfunction:: int PyFile_SoftSpace(PyObject *p, int newflag)

   .. index:: single: softspace (file attribute)

   この関数はインタプリタの内部的な利用のために存在します。この関数は *p* の :attr:`softspace`   属性を *newflag* に
   設定し、以前の設定値を返します。この関数を正しく動作させるために、 *p* がファイルオブジェクトである必然性はありません; 任意の
   オブジェクトをサポートします (:attr:`softspace` 属性が設定されているかどうかのみが問題だと思ってください)。
   この関数は全てのエラーを解消し、属性値が存在しない場合や属性値を取得する際にエラーが生じると、 ``0`` を以前の値として返します。
   この関数からはエラーを検出できませんが、そもそもそういう必要はありません。


.. cfunction:: int PyFile_WriteObject(PyObject *obj, PyObject *p, int flags)

   .. index:: single: Py_PRINT_RAW

   オブジェクト *obj* をファイルオブジェクト *p* に書き込みます。 *flag* がサポートするフラグは :const:`Py_PRINT_RAW`
   だけです; このフラグを指定すると、オブジェクトに :func:`repr` ではなく :func:`str` を適用した結果をファイルに書き出します。
   成功した場合には ``0`` を返し、失敗すると ``-1`` を返して適切な例外をセットします。


.. cfunction:: int PyFile_WriteString(const char *s, PyObject *p)

   文字列 *s* をファイルオブジェクト *p* に書き出します。成功した場合には ``0`` を返し、失敗すると ``-1`` を返して
   適切な例外をセットします。

