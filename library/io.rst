.. -*- coding: utf-8; -*-
:mod:`io` --- ストリームを扱うコアツール
=================================================

.. module:: io
   :synopsis: Core tools for working with streams.
.. moduleauthor:: Guido van Rossum <guido@python.org>
.. moduleauthor:: Mike Verdone <mike.verdone@gmail.com>
.. moduleauthor:: Mark Russell <mark.russell@zen.co.uk>
.. sectionauthor:: Benjamin Peterson
.. versionadded:: 2.6

:mod:`io` モジュールはストリーム処理をするPythonインタフェースを提供します。組み込み関数 :func:`open` はこのモジュールで定義されています。

I/O階層の最上位には抽象基底クラスの :class:`IOBase` があります。
:class:`IOBase` ではストリームに対して基本的なインタフェースを定義しています。
しかしながら、ストリームの読みと書きの間に違いがないことに留意してください。
実装においては与えられた操作をサポートしない場合は :exc:`IOError` を投げることが許されています。

:class:`IOBase` の拡張は生のバイト列の読み書きをしてストリームに落とす処理を単純に扱う :class:`RawIOBase` です。
:class:`FileIO` は :class:`RawIOBase` を継承してマシンのファイルシステム中のファイルへのインタフェースを提供します。

:class:`BufferedIOBase` では生のバイトストリーム処理を扱います。（ :class:`RawIOBase` ）
そのサブクラスの :class:`BufferdWriter` :class:`BufferedReader` :class:`BufferedRWPair` ではそれぞれ読み込み専用、書き込み専用、読み書き可能なストリームをバッファします。
:class:`BufferedRandom` ではランダムアクセスストリームに対してバッファされたインタフェースを提供します。
:class:`BytesIO` はインメモリバイトへのシンプルなストリームです。

もう一つの :class:`IOBase` のサブクラスである、 :class:`TextIOBase` は文字列を表すバイトストリームやその文字列に対するエンコーディングやデコーディングといった処理を行います。
:class:`TextIOWrapper` はその拡張で、バッファされた生ストリーム（ :class:`BufferedIOBase` ）へのバッファされた文字列インタフェースです。
最後に :class:`StringIO` は文字列に対するインメモリストリームです。

引数名は規約に含まれていません。また :func:`open` の引数はキーワード引数として用いられることが意図されています。


モジュールインタフェース
--------------------

.. data:: DEFAULT_BUFFER_SIZE

   モジュールのバッファI/Oクラスに使用されるデフォルトのバッファサイズを指定する整数値です。
   :func:`open` は可能であればファイル全体のサイズを使用します。（ファイル全体のサイズは :func:`os.stat` で取得されます）

.. function:: open(file[, mode[, buffering[, encoding[, errors[, newline[, closefd=True]]]]]])

   *file* を開きストリームを返します。もしファイルを開くことが出来なかった場合、 :exc:`IOError` が発生します。

   *file* は開きたいファイルの名前（とカレントディレクトリにない場合はそのパス）を示す文字列であるか、開きたいファイルのファイルディスクリプタです。
   （たとえば :func:`os.fdopen` から得られるようなファイルディスクリプタが与えられた場合、 *closefd* が ``False`` に設定されていなければ、返されたI/Oオブジェクトが閉じられたときにそのファイルディスクリプタは閉じられます）

   *mode* はオプションの文字列です。これによってファイルをどのようなモードで開くか明示することができます。
   デフォルトは ``'r'`` でテキストモードで読み取り専用で開くことを指します。
   他にも ``'w'`` は書き込み専用（もしファイルが存在していた場合は上書きになります）となり、 ``'a'`` では追記モードとなります。（ ``'a'`` は *いくつかの* Unixシステムでは *すべての* 書き込みがシーク位置がどこにあろうともファイルの末尾に追記されることを意味します）
   テキストモードではもし *encoding* が指定されていなかった場合、エンコーディングはプラットフォーム依存となります。（生のバイトデータの読み込みと書き込みはバイナリモードを用いて、 *encoding* は未指定のままとします）
   指定可能なモードは次の表の通りです。

   ========= ===============================================================
   文字       意味
   --------- ---------------------------------------------------------------
   ``'r'``   読み込み専用で開く（デフォルト）
   ``'w'``   書き込み専用で開く。ファイルの内容をまず初期化する。
   ``'a'``   書き込み専用で開く。ファイルが存在する場合は末尾に追記する。
   ``'b'``   バイナリモード
   ``'t'``   テキストモード（デフォルト）
   ``'+'``	 ファイルを更新用に開く（読み込み／書き込み）
   ``'U'``   ユニバーサルニューラインモード
             （後方互換性のためのモードであり、新規コードでは使用すべきではありません）
   ========= ===============================================================


   デフォルトモードは ``'rt'`` です。（テキストを読み込み専用で開ます）
   バイナリのランダムアクセスでは ``'w+b'`` でファイルを開き、0バイトに初期化します。
   一方で ``'r+b'`` でファイルを開くと初期化は行われません。

   Pythonではバイナリモードで開かれたファイルとテキストモードで開かれたファイルを区別します。
   オペレーティングシステムが区別しない場合でもそれは適用されます。
   バイナリモードで開かれたファイル（つまり *mode* 引数に ``'b'`` が含まれるとき）では中身を ``bytes`` オブジェクトとして返し、一切のデコードを行いません。
   テキストモード（デフォルトか *mode* 引数に ``'t'`` が含まれている場合）ではファイルの中身は文字列として返され、バイト列はプラットフォーム依存のエンコーディングをされるか、 *encoding* が指定された場合は指定されたエンコーディングを行います。

   オプションである *buffering* はバッファ用の設定を行う整数値です。
   デフォルトではフルバッファがオンに設定されています。
   0を設定することでバッファがオフになります。（バイナリモードでのみ有効です）
   1の場合は１行ごとのバッファリングを行い、1より大きい場合はフルバッファが行われます。

   *encoding* はファイルをエンコードあるいはデコードするために使われるエンコーディング名です。
   このオプションはテキストモードでのみ使用されるべきです。
   デフォルトエンコーディングはプラットフォーム依存ですが、Pythonでサポートされているエンコーディングはどれでも使えます。
   詳しくは :mod:`codecs` モジュール内のサポートしているエンコーディングのリストを参照してください。

   *errors* はエンコードやデコードの際のエラーをどのように扱うかを指定する文字列です。
   ``'strict'`` を指定するとエンコードエラーがあった場合 :exc:`ValueError` 例外を発生させます。
   （ デフォルトである ``None`` は同様の処理を行います）
   ``'ignore'`` を指定した場合はエラーを無視します。 ``'replace'`` を指定した場合は正常に変換されなかった文字の代わりにマーカ（例えば ``'?'`` のような文字）を挿入します。
   書き込みの際に ``'xmlcharrefreplace'`` （適切なXML文字リファレンスに置き換える）か ``'backslashreplace'`` （バックスラッシュによるエスケープシーケンスに置き換える）のどちらかが使用出来ます。
   :func:`codecs.register_error` に登録されている他のエラー処理名も指定出来ます。

   *newline* ではユニバーサルニューラインの挙動を制御しています。（テキストモードのみ有効です）
   ``None``, ``''``, ``'\n'``, ``'\r'``, ``'\r\n'`` が指定出来ます。
   以下のように動作します：

   * 入力時、 *newline* が ``None`` の場合はユニバーサルニューラインモードが有効になります。
     入力行は ``'\n'``, ``'\r'``, ``'\r\n'`` のどれかで終わると思いますが、それらは呼び出し元に戻される前に ``'\n'`` に変換されます。
     もし ``''`` だった場合はユニバーサルニューラインモードは有効になりますが、行末は変換されずに呼び出し元に戻されます。
     もし他の適切な値が指定された場合は、入力行は与えられた文字列で中断され、行末は変換されずに呼び出し元に戻されます。

   * 出力時、 *newline* が ``None`` の場合は、すべての ``'\n'`` 文字はシステムのデフォルト行区切り文字 :data:`os.linesep` に変換されます。
     もし *newline* が ``''`` の場合、変換は起きません。
     もし *newline* に他の適切な値が指定された場合は、 ``'\n'`` 文字は与えられた文字に変換されます。

   もし *closefd* が ``False`` で、ファイル名ではなくてファイルディスクリプタが与えられていた場合、処理中のファイルディスクリプタはファイルが閉じられた後も開いたままとなります。
   もしファイル名が与えられていた場合は、 *closefd* は関係ありません。しかし ``True`` でなければいけません。（デフォルト値）

   :func:`open` によって返されるファイルオブジェクトのタイプの話をすると、 :func:`open` がテキストモードでファイルを開くときに使われた場合（ ``'w'``, ``'r'``, ``'wt'``, ``'rt'`` など）、 :class:`TextIOWrapper` が返されます。
   バイナリモードでファイルを開くときに使われた場合、返される値は変わってきます。もし読み取り専用のバイナリモードだった場合は :class:`BufferedReader` が返されます。
   書き込み専用のバイナリモードだった場合は :class:`BufferdWriter` が返されます。
   読み書き可能なバイナリモードの場合は :class:`BufferedRandom` が返されます。

   もし文字列やバイト列をファイルとして読み書きすることも可能です。
   文字列では :class:`StringIO` を使えばテキストモードで開いたファイルのように扱えます。
   バイト列では :class:`BytesIO` を使えばバイナリモードで開いたファイルのように扱えます。


.. exception:: BlockingIOError

   .. :exc:`IOError`.
   非ブロッキングストリームでブロック処理が起きた場合に発生するエラーです。 :exc:`IOError` を継承しています。

   :exc:`IOError` で持っている属性以外に :exc:`BlockingIOError` では次の属性を持っています。

   .. attribute:: characters_written

	  ブロック前にストリームに書き込まれる文字数を保持する整数値です。


.. exception:: UnsupportedOperation

   :exc:`IOError` と :exc:`ValueError` を継承した例外でストリームに予想外の操作が行われた場合に発生します。


I/O ベースクラス
----------------

.. class:: IOBase

   すべてのI/Oクラスの抽象ベースクラスです。バイトストリームへの操作を行います。
   パブリックなコンストラクタはありません。

   このクラスでは継承先のクラスがオーバライドするかの選択の余地を残すためにたくさんの
   空の抽象実装を持っています。デフォルトの実装では読み込み、書き込み、シークができない
   ファイルとなっています。

   :class:`IOBase` がそのシグナチャーが変化するため :meth:`read`, :meth:`readinto`, 
   :meth:`write` を宣言していなくても、実装やクライアントはインタフェースの一部として
   これらのメソッドを考慮するべきです。
   また実装はサポートしていない操作を呼び出されたときは :exc:`IOError` を発生させるかもしれません。
   

   ファイル等への読み書きに用いられるバイナリデータに使われるバイナリ型は :class:`bytes` です。
   :class:`bytearray` も許可されています。ほかにもいくつかのクラス（たとえば :class:`readinto` ）
   が必要です。文字列のI/Oクラスは :class:`str` のデータを扱っています。

   閉じたストリームでメソッドを呼び出し（問い合わせでさえ）は定義されていません。
   この場合実装は :exc:`IOError` を発生させます。

   IOBase（とそのサブクラス）はイテレータプロトコルをサポートします。
   それはつまり :class:`IOBase` オブジェクトはストリーム内の行をyieldを使って
   イテレートすることが出来ます。

   IOBaseはコンテキストマネージャでもあります。そのため :keyword:`with` 構文を
   サポートします。次の例では *file* は :keyword:`with` 構文が終わった後、
   閉じられます。--それがたとえ例外が発生したあとでさえです。
   
      with open('spam.txt', 'w') as file:
          file.write('Spam and eggs!')

   :class:`IOBase` データ属性とメソッドを提供します:

   .. method:: close()

   	  このストリームをフラッシュして閉じます。このメソッドはファイルが既に閉じられていた場合
	  特になにも影響を与えません。

   .. attribute:: closed

   	  ストリームが閉じられていた場合Trueになります。

   .. method:: fileno()
   
      ストリームが保持しているファイルディスクリプタ（整数値）が存在する場合はそれを返します。
	  もしIOオブジェクトがファイルディスクリプタを使っていない場合は :exc:`IOError` が発生します。

   .. method:: flush()

      適用可能であればストリームの書き込みバッファをフラッシュします。
	  読み込み専用や非ブロッキングストリームには影響を与えません。

   .. method:: isatty()

      ストリームが相互作用的であれば（つまりターミナルやttyデバイスにつながっている場合）
	  ``True`` を返します。

   .. method:: readable()

      ストリームが読み込める場合 ``True`` を返します。
	  Falseの場合は :meth:`read` は :exc:`IOError` を発生させます。

   .. method:: readline([limit])

	  ストリームから1行読み込んで返します。
	  もし *limit* が指定された場合、最大で *limit* バイトが読み込まれます。

	  バイナリファイルでは行末文字は常に ``b'\n'`` となります。テキストファイルでは
	  :func:`open` への *newlines* 引数は行末文字が認識されたときに使われます。

   .. method:: readlines([hint])

      ストリームから行のリストを読み込んで返します。
	  *hint* を指定することで、何行読み込むかを指定出来ます。
      もし読み込んだすべての行のサイズ（バイト数、もしくは文字数）が *hint* の値を超えた場合
      読み込みをそこで終了します。

   .. method:: seek(offset[, whence])

      ストリーム位置を指定された *offset* バイトに変更します。
      *offset* は *whence* で指定された位置からの相対位置として解釈されます。
      *whence* に入力できる値は：

      * ``0`` -- ストリームの最初（デフォルト）です。 *offset* はゼロもしくは正の値です。
      * ``1`` -- 現在のストリーム位置です。 *offset* は負の値です。
      * ``2`` -- ストリームの最後です。 *offset* は通常負の値です。

      新しい絶対位置を返します。

   .. method:: seekable()

      もしストリームがランダムアクセスをサポートしていた場合 ``True`` を返します。
      ``False`` の場合は :meth:`seek`, :meth:`tell`, :meth:`truncate` は :exc:`IOError` を発生させます。

   .. method:: tell()

      現在のストリーム位置を返します。

   .. method:: truncate([size])

      最大 *size* バイト分ファイルを切り捨てます。
      *size* のデフォルト値は現在のファイルの位置で、 :meth:`tell` が返す値と同値です。

   .. method:: writable()

      ストリームが書き込みをサポートしていた場合 ``True`` を返します。
      ``False`` の場合は :meth:`write`, :meth:`truncate` は :exc:`IOError` を返します。

   .. method:: writelines(lines)

      ストリームに複数行書き込みます。
      行区切り文字は付与されないので、書き込む各行の行末には行区切り文字があります。


.. class:: RawIOBase

   生バイナリI/Oへのベースクラスです。 :class:`IOBase` を継承しています。
   パブリックコンストラクタはありません。

   :class:`IOBase` の属性やメソッドに加えて、 RawIOBase は次のメソッドを提供します：

   .. method:: read([n])

      EOFまで、あるいは *n* が指定された場合 *n* バイトまでストリームから
      すべてのバイトを読み込んで返します。たった1つのシステムコールが呼ばれます。
      空のバイトオブジェクトはEOFの上に返されます。
      もしオブジェクトがブロックされず読み込むべきデータがない場合は ``None`` が返されます。
      
   .. method:: readall()

      EOFまでストリームからすべてのバイトを読み込みます。必要な場合はストリームに対して
      複数の呼び出しをします。

   .. method:: readinto(b)

      バイト列 *b* に len(b) バイト分読み込み、読み込んだバイト数を返します。

   .. method:: write(b)

      与えられたバイトあるいはバイト列オブジェクト *b* を生のストリームに書き込んで、
      書き込んだバイト数を返します。（決して ``len(b)`` よりも小さくなることはありません。
      なぜならはもし書き込みに失敗した場合は :exc:`IOError` が発生するからです）


生ファイルI/O
--------------

.. class:: FileIO(name[, mode])

   :class:`FileIO` represents a file containing bytes data.  It implements
   the :class:`RawIOBase` interface (and therefore the :class:`IOBase`
   interface, too).

   The *mode* can be ``'r'``, ``'w'`` or ``'a'`` for reading (default), writing,
   or appending.  The file will be created if it doesn't exist when opened for
   writing or appending; it will be truncated when opened for writing.  Add a
   ``'+'`` to the mode to allow simultaneous reading and writing.

   In addition to the attributes and methods from :class:`IOBase` and
   :class:`RawIOBase`, :class:`FileIO` provides the following data
   attributes and methods:

   .. attribute:: mode

      The mode as given in the constructor.

   .. attribute:: name

      The file name.  This is the file descriptor of the file when no name is
      given in the constructor.

   .. method:: read([n])

      Read and return at most *n* bytes.  Only one system call is made, so it is
      possible that less data than was requested is returned.  Use :func:`len`
      on the returned bytes object to see how many bytes were actually returned.
      (In non-blocking mode, ``None`` is returned when no data is available.)

   .. method:: readall()

      Read and return the entire file's contents in a single bytes object.  As
      much as immediately available is returned in non-blocking mode.  If the
      EOF has been reached, ``b''`` is returned.

   .. method:: write(b)

      Write the bytes or bytearray object, *b*, to the file, and return
      the number actually written. Only one system call is made, so it
      is possible that only some of the data is written.

   Note that the inherited ``readinto()`` method should not be used on
   :class:`FileIO` objects.


バッファドストリーム
------------------

.. class:: BufferedIOBase

   Base class for streams that support buffering.  It inherits :class:`IOBase`.
   There is no public constructor.

   The main difference with :class:`RawIOBase` is that the :meth:`read` method
   supports omitting the *size* argument, and does not have a default
   implementation that defers to :meth:`readinto`.

   In addition, :meth:`read`, :meth:`readinto`, and :meth:`write` may raise
   :exc:`BlockingIOError` if the underlying raw stream is in non-blocking mode
   and not ready; unlike their raw counterparts, they will never return
   ``None``.

   A typical implementation should not inherit from a :class:`RawIOBase`
   implementation, but wrap one like :class:`BufferedWriter` and
   :class:`BufferedReader`.

   :class:`BufferedIOBase` provides or overrides these methods in addition to
   those from :class:`IOBase`:

   .. method:: read([n])

      Read and return up to *n* bytes.  If the argument is omitted, ``None``, or
      negative, data is read and returned until EOF is reached.  An empty bytes
      object is returned if the stream is already at EOF.

      If the argument is positive, and the underlying raw stream is not
      interactive, multiple raw reads may be issued to satisfy the byte count
      (unless EOF is reached first).  But for interactive raw streams, at most
      one raw read will be issued, and a short result does not imply that EOF is
      imminent.

      A :exc:`BlockingIOError` is raised if the underlying raw stream has no
      data at the moment.

   .. method:: readinto(b)

      Read up to len(b) bytes into bytearray *b* and return the number of bytes
      read.

      Like :meth:`read`, multiple reads may be issued to the underlying raw
      stream, unless the latter is 'interactive.'

      A :exc:`BlockingIOError` is raised if the underlying raw stream has no
      data at the moment.

   .. method:: write(b)

      Write the given bytes or bytearray object, *b*, to the underlying raw
      stream and return the number of bytes written (never less than ``len(b)``,
      since if the write fails an :exc:`IOError` will be raised).

      A :exc:`BlockingIOError` is raised if the buffer is full, and the
      underlying raw stream cannot accept more data at the moment.


.. class:: BytesIO([initial_bytes])

   A stream implementation using an in-memory bytes buffer.  It inherits
   :class:`BufferedIOBase`.

   The argument *initial_bytes* is an optional initial bytearray.

   :class:`BytesIO` provides or overrides these methods in addition to those
   from :class:`BufferedIOBase` and :class:`IOBase`:

   .. method:: getvalue()

      Return ``bytes`` containing the entire contents of the buffer.

   .. method:: read1()

      In :class:`BytesIO`, this is the same as :meth:`read`.

   .. method:: truncate([size])

      Truncate the buffer to at most *size* bytes.  *size* defaults to the
      current stream position, as returned by :meth:`tell`.


.. class:: BufferedReader(raw[, buffer_size])

   A buffer for a readable, sequential :class:`RawIOBase` object.  It inherits
   :class:`BufferedIOBase`.

   The constructor creates a :class:`BufferedReader` for the given readable
   *raw* stream and *buffer_size*.  If *buffer_size* is omitted,
   :data:`DEFAULT_BUFFER_SIZE` is used.

   :class:`BufferedReader` provides or overrides these methods in addition to
   those from :class:`BufferedIOBase` and :class:`IOBase`:

   .. method:: peek([n])

      Return 1 (or *n* if specified) bytes from a buffer without advancing the
      position.  Only a single read on the raw stream is done to satisfy the
      call. The number of bytes returned may be less than requested since at
      most all the buffer's bytes from the current position to the end are
      returned.

   .. method:: read([n])

      Read and return *n* bytes, or if *n* is not given or negative, until EOF
      or if the read call would block in non-blocking mode.

   .. method:: read1(n)

      Read and return up to *n* bytes with only one call on the raw stream.  If
      at least one byte is buffered, only buffered bytes are returned.
      Otherwise, one raw stream read call is made.


.. class:: BufferedWriter(raw[, buffer_size[, max_buffer_size]])

   A buffer for a writeable sequential RawIO object.  It inherits
   :class:`BufferedIOBase`.

   The constructor creates a :class:`BufferedWriter` for the given writeable
   *raw* stream.  If the *buffer_size* is not given, it defaults to
   :data:`DEAFULT_BUFFER_SIZE`.  If *max_buffer_size* is omitted, it defaults to
   twice the buffer size.

   :class:`BufferedWriter` provides or overrides these methods in addition to
   those from :class:`BufferedIOBase` and :class:`IOBase`:

   .. method:: flush()

      Force bytes held in the buffer into the raw stream.  A
      :exc:`BlockingIOError` should be raised if the raw stream blocks.

   .. method:: write(b)

      Write the bytes or bytearray object, *b*, onto the raw stream and return
      the number of bytes written.  A :exc:`BlockingIOError` is raised when the
      raw stream blocks.


.. class:: BufferedRWPair(reader, writer[, buffer_size[, max_buffer_size]])

   A combined buffered writer and reader object for a raw stream that can be
   written to and read from.  It has and supports both :meth:`read`, :meth:`write`,
   and their variants.  This is useful for sockets and two-way pipes.
   It inherits :class:`BufferedIOBase`.

   *reader* and *writer* are :class:`RawIOBase` objects that are readable and
   writeable respectively.  If the *buffer_size* is omitted it defaults to
   :data:`DEFAULT_BUFFER_SIZE`.  The *max_buffer_size* (for the buffered writer)
   defaults to twice the buffer size.

   :class:`BufferedRWPair` implements all of :class:`BufferedIOBase`\'s methods.


.. class:: BufferedRandom(raw[, buffer_size[, max_buffer_size]])

   A buffered interface to random access streams.  It inherits
   :class:`BufferedReader` and :class:`BufferedWriter`.

   The constructor creates a reader and writer for a seekable raw stream, given
   in the first argument.  If the *buffer_size* is omitted it defaults to
   :data:`DEFAULT_BUFFER_SIZE`.  The *max_buffer_size* (for the buffered writer)
   defaults to twice the buffer size.

   :class:`BufferedRandom` is capable of anything :class:`BufferedReader` or
   :class:`BufferedWriter` can do.


文字列 I/O
------------

.. class:: TextIOBase

   Base class for text streams.  This class provides a character and line based
   interface to stream I/O.  There is no :meth:`readinto` method because
   Python's character strings are immutable.  It inherits :class:`IOBase`.
   There is no public constructor.

   :class:`TextIOBase` provides or overrides these data attributes and
   methods in addition to those from :class:`IOBase`:

   .. attribute:: encoding

      The name of the encoding used to decode the stream's bytes into
      strings, and to encode strings into bytes.

   .. attribute:: newlines

      A string, a tuple of strings, or ``None``, indicating the newlines
      translated so far.

   .. method:: read(n)

      Read and return at most *n* characters from the stream as a single
      :class:`str`.  If *n* is negative or ``None``, reads to EOF.

   .. method:: readline()

      Read until newline or EOF and return a single ``str``.  If the stream is
      already at EOF, an empty string is returned.

   .. method:: write(s)

      Write the string *s* to the stream and return the number of characters
      written.


.. class:: TextIOWrapper(buffer[, encoding[, errors[, newline[, line_buffering]]]])

   A buffered text stream over a :class:`BufferedIOBase` raw stream, *buffer*.
   It inherits :class:`TextIOBase`.

   *encoding* gives the name of the encoding that the stream will be decoded or
   encoded with.  It defaults to :func:`locale.getpreferredencoding`.

   *errors* is an optional string that specifies how encoding and decoding
   errors are to be handled.  Pass ``'strict'`` to raise a :exc:`ValueError`
   exception if there is an encoding error (the default of ``None`` has the same
   effect), or pass ``'ignore'`` to ignore errors.  (Note that ignoring encoding
   errors can lead to data loss.)  ``'replace'`` causes a replacement marker
   (such as ``'?'``) to be inserted where there is malformed data.  When
   writing, ``'xmlcharrefreplace'`` (replace with the appropriate XML character
   reference) or ``'backslashreplace'`` (replace with backslashed escape
   sequences) can be used.  Any other error handling name that has been
   registered with :func:`codecs.register_error` is also valid.

   *newline* can be ``None``, ``''``, ``'\n'``, ``'\r'``, or ``'\r\n'``.  It
   controls the handling of line endings.  If it is ``None``, universal newlines
   is enabled.  With this enabled, on input, the lines endings ``'\n'``,
   ``'\r'``, or ``'\r\n'`` are translated to ``'\n'`` before being returned to
   the caller.  Conversely, on output, ``'\n'`` is translated to the system
   default line seperator, :data:`os.linesep`.  If *newline* is any other of its
   legal values, that newline becomes the newline when the file is read and it
   is returned untranslated.  On output, ``'\n'`` is converted to the *newline*.

   If *line_buffering* is ``True``, :meth:`flush` is implied when a call to
   write contains a newline character.

   :class:`TextIOWrapper` provides these data attributes in addition to those of
   :class:`TextIOBase` and its parents:

   .. attribute:: errors

      The encoding and decoding error setting.

   .. attribute:: line_buffering

      Whether line buffering is enabled.
   

.. class:: StringIO([initial_value[, encoding[, errors[, newline]]]])

   An in-memory stream for text.  It in inherits :class:`TextIOWrapper`.

   Create a new StringIO stream with an inital value, encoding, error handling,
   and newline setting.  See :class:`TextIOWrapper`\'s constructor for more
   information.

   :class:`StringIO` provides this method in addition to those from
   :class:`TextIOWrapper` and its parents:

   .. method:: getvalue()

      Return a ``str`` containing the entire contents of the buffer.


.. class:: IncrementalNewlineDecoder

   A helper codec that decodes newlines for universal newlines mode.  It
   inherits :class:`codecs.IncrementalDecoder`.

