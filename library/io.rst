:mod:`io` --- ストリームを扱うコアツール
=================================================

.. module:: io
   :synopsis: Core tools for working with streams.
.. moduleauthor:: Guido van Rossum <guido@python.org>
.. moduleauthor:: Mike Verdone <mike.verdone@gmail.com>
.. moduleauthor:: Mark Russell <mark.russell@zen.co.uk>
.. sectionauthor:: Benjamin Peterson <benjamin@python.org>
.. versionadded:: 2.6

.. The :mod:`io` module provides the Python interfaces to stream handling.  The
.. built-in :func:`open` function is defined in this module.

:mod:`io` モジュールはストリーム処理をする Python インタフェースを提供します。
組み込み関数 :func:`open` はこのモジュールで定義されています。


.. At the top of the I/O hierarchy is the abstract base class :class:`IOBase`.  It
.. defines the basic interface to a stream.  Note, however, that there is no
.. separation between reading and writing to streams; implementations are allowed
.. to throw an :exc:`IOError` if they do not support a given operation.

I/O 階層の最上位には抽象基底クラスの :class:`IOBase` があります。
:class:`IOBase` ではストリームに対して基本的なインタフェースを定義しています。
しかしながら、ストリームの読みと書きの間に違いがないことに留意してください。
実装においては与えられた操作をサポートしない場合は :exc:`IOError` を投げることが許されています。


.. Extending :class:`IOBase` is :class:`RawIOBase` which deals simply with the
.. reading and writing of raw bytes to a stream.  :class:`FileIO` subclasses
.. :class:`RawIOBase` to provide an interface to files in the machine's
.. file system.

:class:`IOBase` の拡張は生のバイト列の読み書きをしてストリームに落とす処理を単純に扱う :class:`RawIOBase` です。
:class:`FileIO` は :class:`RawIOBase` を継承してマシンのファイルシステム中のファイルへのインタフェースを提供します。


.. :class:`BufferedIOBase` deals with buffering on a raw byte stream
.. (:class:`RawIOBase`).  Its subclasses, :class:`BufferedWriter`,
.. :class:`BufferedReader`, and :class:`BufferedRWPair` buffer streams that are
.. readable, writable, and both readable and writable.
.. :class:`BufferedRandom` provides a buffered interface to random access
.. streams.  :class:`BytesIO` is a simple stream of in-memory bytes.

:class:`BufferedIOBase` では生のバイトストリーム (:class:`RawIOBase`) の上にバッファ処理を追加します。
そのサブクラスの :class:`BufferedWriter`, :class:`BufferedReader`, :class:`BufferedRWPair` ではそれぞれ読み込み専用、書き込み専用、読み書き可能なストリームをバッファします。
:class:`BufferedRandom` ではランダムアクセスストリームに対してバッファされたインタフェースを提供します。
:class:`BytesIO` はインメモリバイトへのシンプルなストリームです。


.. Another :class:`IOBase` subclass, :class:`TextIOBase`, deals with
.. streams whose bytes represent text, and handles encoding and decoding
.. from and to strings. :class:`TextIOWrapper`, which extends it, is a
.. buffered text interface to a buffered raw stream
.. (:class:`BufferedIOBase`). Finally, :class:`StringIO` is an in-memory
.. stream for text.

もう一つの :class:`IOBase` のサブクラスである、 :class:`TextIOBase` は文字列を表すバイトストリームやその文字列に対するエンコーディングやデコーディングといった処理を行います。
:class:`TextIOWrapper` はその拡張で、バッファされた生ストリーム (:class:`BufferedIOBase`) へのバッファされた文字列インタフェースです。
最後に :class:`StringIO` は文字列に対するインメモリストリームです。


.. Argument names are not part of the specification, and only the arguments of
.. :func:`.open` are intended to be used as keyword arguments.

引数名は規約に含まれていません。
また :func:`.open` の引数はキーワード引数として用いられることが意図されています。


モジュールインタフェース
------------------------

.. data:: DEFAULT_BUFFER_SIZE

   .. An int containing the default buffer size used by the module's buffered I/O
   .. classes.  :func:`.open` uses the file's blksize (as obtained by
   .. :func:`os.stat`) if possible.

   モジュールのバッファ I/O クラスに使用されるデフォルトのバッファサイズを指定する整数値です。
   :func:`.open` は可能であればファイル全体のサイズを使用します。（ファイル全体のサイズは :func:`os.stat` で取得されます)


.. function:: open(file[, mode[, buffering[, encoding[, errors[, newline[, closefd=True]]]]]])

   .. Open *file* and return a stream.  If the file cannot be opened, an
   .. :exc:`IOError` is raised.

   *file* を開きストリームを返します。
   もしファイルを開くことが出来なかった場合、 :exc:`IOError` が発生します。


   .. *file* is either a string giving the name (and the path if the file isn't in
   .. the current working directory) of the file to be opened or a file
   .. descriptor of the file to be opened.  (If a file descriptor is given,
   .. for example, from :func:`os.fdopen`, it is closed when the returned
   .. I/O object is closed, unless *closefd* is set to ``False``.)

   *file* は開きたいファイルの名前(とカレントディレクトリにない場合はそのパス)を示す文字列であるか、開きたいファイルのファイルディスクリプタです。
   (たとえば :func:`os.fdopen` から得られるようなファイルディスクリプタが与えられた場合、 *closefd* が ``False`` に設定されていなければ、返されたI/Oオブジェクトが閉じられたときにそのファイルディスクリプタは閉じられます)


   .. *mode* is an optional string that specifies the mode in which the file is
   .. opened.  It defaults to ``'r'`` which means open for reading in text mode.
   .. Other common values are ``'w'`` for writing (truncating the file if it
   .. already exists), and ``'a'`` for appending (which on *some* Unix systems,
   .. means that *all* writes append to the end of the file regardless of the
   .. current seek position).  In text mode, if *encoding* is not specified the
   .. encoding used is platform dependent. (For reading and writing raw bytes use
   .. binary mode and leave *encoding* unspecified.)  The available modes are:

   *mode* はオプションの文字列です。これによってファイルをどのようなモードで開くか明示することができます。
   デフォルトは ``'r'`` でテキストモードで読み取り専用で開くことを指します。
   他にも ``'w'`` は書き込み専用(もしファイルが存在していた場合は上書きになります)となり、 ``'a'`` では追記モードとなります。
   (``'a'`` は *いくつかの* Unixシステムでは *すべての* 書き込みがシーク位置がどこにあろうともファイルの末尾に追記されることを意味します)
   テキストモードではもし *encoding* が指定されていなかった場合、エンコーディングはプラットフォーム依存となります。
   (生のバイトデータの読み込みと書き込みはバイナリモードを用いて、 *encoding* は未指定のままとします)
   指定可能なモードは次の表の通りです。


   .. ========= ===============================================================
   .. Character Meaning
   .. --------- ---------------------------------------------------------------
   .. ``'r'``   open for reading (default)
   .. ``'w'``   open for writing, truncating the file first
   .. ``'a'``   open for writing, appending to the end of the file if it exists
   .. ``'b'``   binary mode
   .. ``'t'``   text mode (default)
   .. ``'+'``   open a disk file for updating (reading and writing)
   .. ``'U'``   universal newline mode (for backwards compatibility; should
   ..           not be used in new code)
   .. ========= ===============================================================

   ========= ===============================================================
   文字       意味
   --------- ---------------------------------------------------------------
   ``'r'``   読み込み専用で開く(デフォルト)
   ``'w'``   書き込み専用で開く。ファイルの内容をまず初期化する。
   ``'a'``   書き込み専用で開く。ファイルが存在する場合は末尾に追記する。
   ``'b'``   バイナリモード
   ``'t'``   テキストモード(デフォルト)
   ``'+'``     ファイルを更新用に開く(読み込み／書き込み)
   ``'U'``   ユニバーサルニューラインモード
             (後方互換性のためのモードであり、新規コードでは使用すべきではありません)
   ========= ===============================================================


   .. The default mode is ``'rt'`` (open for reading text).  For binary random
   .. access, the mode ``'w+b'`` opens and truncates the file to 0 bytes, while
   .. ``'r+b'`` opens the file without truncation.

   デフォルトモードは ``'rt'`` です。(テキストを読み込み専用で開ます)
   バイナリのランダムアクセスでは ``'w+b'`` でファイルを開き、0バイトに初期化します。
   一方で ``'r+b'`` でファイルを開くと初期化は行われません。


   .. Python distinguishes between files opened in binary and text modes, even when
   .. the underlying operating system doesn't.  Files opened in binary mode
   .. (including ``'b'`` in the *mode* argument) return contents as ``bytes``
   .. objects without any decoding.  In text mode (the default, or when ``'t'`` is
   .. included in the *mode* argument), the contents of the file are returned as
   .. strings, the bytes having been first decoded using a platform-dependent
   .. encoding or using the specified *encoding* if given.

   Pythonではバイナリモードで開かれたファイルとテキストモードで開かれたファイルを区別します。
   オペレーティングシステムが区別しない場合でもそれは適用されます。
   バイナリモードで開かれたファイル(つまり *mode* 引数に ``'b'`` が含まれるとき)では中身を ``bytes`` オブジェクトとして返し、一切のデコードを行いません。
   テキストモード(デフォルトか *mode* 引数に ``'t'`` が含まれている場合)ではファイルの中身は文字列として返され、バイト列はプラットフォーム依存のエンコーディングをされるか、 *encoding* が指定された場合は指定されたエンコーディングを行います。


   .. *buffering* is an optional integer used to set the buffering policy.
   .. Pass 0 to switch buffering off (only allowed in binary mode), 1 to select
   .. line buffering (only usable in text mode), and an integer > 1 to indicate
   .. the size of a fixed-size chunk buffer.  When no *buffering* argument is
   .. given, the default buffering policy works as follows:

   オプションである *buffering* はバッファ用の設定を行う整数値です。
   0を設定することでバッファがオフになります。(バイナリモードでのみ有効です)
   1の場合は１行ごとのバッファリングを行い (テキストモードでのみ利用可能です)、
   1より大きい場合は固定サイズチャンクバッファのサイズを表します。
   *buffering* 引数が与えられなければ、デフォルトのバッファリングポリシーは以下のように働きます:


   .. * Binary files are buffered in fixed-size chunks; the size of the buffer
   ..   is chosen using a heuristic trying to determine the underlying device's
   ..   "block size" and falling back on :attr:`DEFAULT_BUFFER_SIZE`.
   ..   On many systems, the buffer will typically be 4096 or 8192 bytes long.

   * バイナリファイルは固定サイズのチャンクでバッファリングされます。
     バッファサイズは、背後のデバイスの「ブロックサイズ」を決定するヒューリスティックを用いて選択され、
     それが不可能な場合は代わりに :attr:`DEFAULT_BUFFER_SIZE` が使われます。
     多くのシステムでは、典型的なバッファサイズは 4096 か 8192 バイト長になるでしょう。


   .. * "Interactive" text files (files for which :meth:`isatty` returns True)
   ..   use line buffering.  Other text files use the policy described above
   ..   for binary files.

   * 「対話的な」テキストファイル (:meth:`isatty` が True を返すファイル) は行バッファリングを使用します。
     その他のテキストファイルは、上で説明されたバイナリファイルのためのポリシーを使用します。


   .. *encoding* is the name of the encoding used to decode or encode the file.
   .. This should only be used in text mode.  The default encoding is platform
   .. dependent, but any encoding supported by Python can be used.  See the
   .. :mod:`codecs` module for the list of supported encodings.

   *encoding* はファイルをエンコードあるいはデコードするために使われるエンコーディング名です。
   このオプションはテキストモードでのみ使用されるべきです。
   デフォルトエンコーディングはプラットフォーム依存ですが、Pythonでサポートされているエンコーディングはどれでも使えます。
   詳しくは :mod:`codecs` モジュール内のサポートしているエンコーディングのリストを参照してください。


   .. *errors* is an optional string that specifies how encoding and decoding
   .. errors are to be handled.  Pass ``'strict'`` to raise a :exc:`ValueError`
   .. exception if there is an encoding error (the default of ``None`` has the same
   .. effect), or pass ``'ignore'`` to ignore errors.  (Note that ignoring encoding
   .. errors can lead to data loss.)  ``'replace'`` causes a replacement marker
   .. (such as ``'?'``) to be inserted where there is malformed data.  When
   .. writing, ``'xmlcharrefreplace'`` (replace with the appropriate XML character
   .. reference) or ``'backslashreplace'`` (replace with backslashed escape
   .. sequences) can be used.  Any other error handling name that has been
   .. registered with :func:`codecs.register_error` is also valid.

   *errors* はエンコードやデコードの際のエラーをどのように扱うかを指定する文字列です。
   ``'strict'`` を指定するとエンコードエラーがあった場合 :exc:`ValueError` 例外を発生させます。
   (デフォルトである ``None`` は同様の処理を行います)
   ``'ignore'`` を指定した場合はエラーを無視します。 ``'replace'`` を指定した場合は正常に変換されなかった文字の代わりにマーカ(例えば ``'?'`` のような文字)を挿入します。
   書き込みの際に ``'xmlcharrefreplace'`` (適切なXML文字参照に置き換える)か ``'backslashreplace'`` (バックスラッシュによるエスケープシーケンスに置き換える)のどちらかが使用出来ます。
   :func:`codecs.register_error` に登録されている他のエラー処理名も指定出来ます。


   .. *newline* controls how universal newlines works (it only applies to text
   .. mode).  It can be ``None``, ``''``, ``'\n'``, ``'\r'``, and ``'\r\n'``.  It
   .. works as follows:

   *newline* ではユニバーサルニューラインの挙動を制御しています。(テキストモードのみ有効です)
   ``None``, ``''``, ``'\n'``, ``'\r'``, ``'\r\n'`` が指定出来ます。
   以下のように動作します：


   .. * On input, if *newline* is ``None``, universal newlines mode is enabled.
   ..   Lines in the input can end in ``'\n'``, ``'\r'``, or ``'\r\n'``, and these
   ..   are translated into ``'\n'`` before being returned to the caller.  If it is
   ..   ``''``, universal newline mode is enabled, but line endings are returned to
   ..   the caller untranslated.  If it has any of the other legal values, input
   ..   lines are only terminated by the given string, and the line ending is
   ..   returned to the caller untranslated.

   * 入力時、 *newline* が ``None`` の場合はユニバーサルニューラインモードが有効になります。
     入力行は ``'\n'``, ``'\r'``, ``'\r\n'`` のどれかで終わると思いますが、それらは呼び出し元に戻される前に ``'\n'`` に変換されます。
     もし ``''`` だった場合はユニバーサルニューラインモードは有効になりますが、行末は変換されずに呼び出し元に戻されます。
     もし他の適切な値が指定された場合は、入力行は与えられた文字列で中断され、行末は変換されずに呼び出し元に戻されます。


   .. * On output, if *newline* is ``None``, any ``'\n'`` characters written are
   ..   translated to the system default line separator, :data:`os.linesep`.  If
   ..   *newline* is ``''``, no translation takes place.  If *newline* is any of
   ..   the other legal values, any ``'\n'`` characters written are translated to
   ..   the given string.

   * 出力時、 *newline* が ``None`` の場合は、すべての ``'\n'`` 文字はシステムのデフォルト行区切り文字 :data:`os.linesep` に変換されます。
     もし *newline* が ``''`` の場合、変換は起きません。
     もし *newline* に他の適切な値が指定された場合は、 ``'\n'`` 文字は与えられた文字に変換されます。


   .. If *closefd* is ``False`` and a file descriptor rather than a
   .. filename was given, the underlying file descriptor will be kept open
   .. when the file is closed.  If a filename is given *closefd* has no
   .. effect but must be ``True`` (the default).

   もし *closefd* が ``False`` で、ファイル名ではなくてファイルディスクリプタが与えられていた場合、処理中のファイルディスクリプタはファイルが閉じられた後も開いたままとなります。
   もしファイル名が与えられていた場合は、 *closefd* は関係ありません。しかし ``True`` でなければいけません。(デフォルト値)


   .. The type of file object returned by the :func:`.open` function depends
   .. on the mode.  When :func:`.open` is used to open a file in a text mode
   .. (``'w'``, ``'r'``, ``'wt'``, ``'rt'``, etc.), it returns a
   .. :class:`TextIOWrapper`. When used to open a file in a binary mode,
   .. the returned class varies: in read binary mode, it returns a
   .. :class:`BufferedReader`; in write binary and append binary modes, it
   .. returns a :class:`BufferedWriter`, and in read/write mode, it returns
   .. a :class:`BufferedRandom`.

   :func:`.open` によって返されるファイルオブジェクトのタイプの話をすると、 :func:`.open` がテキストモードでファイルを開くときに使われた場合( ``'w'``, ``'r'``, ``'wt'``, ``'rt'`` など)、 :class:`TextIOWrapper` が返されます。
   バイナリモードでファイルを開くときに使われた場合、返される値は変わってきます。もし読み取り専用のバイナリモードだった場合は :class:`BufferedReader` が返されます。
   書き込み専用のバイナリモードだった場合は :class:`BufferedWriter` が返されます。
   読み書き可能なバイナリモードの場合は :class:`BufferedRandom` が返されます。


   .. It is also possible to use a string or bytearray as a file for both reading
   .. and writing.  For strings :class:`StringIO` can be used like a file opened in
   .. a text mode, and for bytearrays a :class:`BytesIO` can be used like a
   .. file opened in a binary mode.

   もし文字列やバイト列をファイルとして読み書きすることも可能です。
   文字列では :class:`StringIO` を使えばテキストモードで開いたファイルのように扱えます。
   バイト列では :class:`BytesIO` を使えばバイナリモードで開いたファイルのように扱えます。


.. exception:: BlockingIOError

   .. Error raised when blocking would occur on a non-blocking stream.  It inherits
   .. :exc:`IOError`.

   非ブロッキングストリームでブロック処理が起きた場合に発生するエラーです。
   :exc:`IOError` を継承しています。


   .. In addition to those of :exc:`IOError`, :exc:`BlockingIOError` has one
   .. attribute:

   :exc:`IOError` で持っている属性以外に :exc:`BlockingIOError` では次の属性を持っています。


   .. attribute:: characters_written

      .. An integer containing the number of characters written to the stream
      .. before it blocked.

      ブロック前にストリームに書き込まれる文字数を保持する整数値です。


.. exception:: UnsupportedOperation

   .. An exception inheriting :exc:`IOError` and :exc:`ValueError` that is raised
   .. when an unsupported operation is called on a stream.

   :exc:`IOError` と :exc:`ValueError` を継承した例外でストリームに予想外の操作が行われた場合に発生します。


I/O ベースクラス
----------------

.. class:: IOBase

   .. The abstract base class for all I/O classes, acting on streams of bytes.
   .. There is no public constructor.

   すべてのI/Oクラスの抽象ベースクラスです。バイトストリームへの操作を行います。
   パブリックなコンストラクタはありません。


   .. This class provides empty abstract implementations for many methods
   .. that derived classes can override selectively; the default
   .. implementations represent a file that cannot be read, written or
   .. seeked.

   このクラスでは継承先のクラスがオーバライドするかの選択の余地を残すためにたくさんの
   空の抽象実装を持っています。デフォルトの実装では読み込み、書き込み、シークができない
   ファイルとなっています。


   .. Even though :class:`IOBase` does not declare :meth:`read`, :meth:`readinto`,
   .. or :meth:`write` because their signatures will vary, implementations and
   .. clients should consider those methods part of the interface.  Also,
   .. implementations may raise a :exc:`IOError` when operations they do not
   .. support are called.

   :class:`IOBase` がそのシグナチャーが変化するため :meth:`read`, :meth:`readinto`,
   :meth:`write` を宣言していなくても、実装やクライアントはインタフェースの一部として
   これらのメソッドを考慮するべきです。
   また実装はサポートしていない操作を呼び出されたときは :exc:`IOError` を発生させるかもしれません。


   .. The basic type used for binary data read from or written to a file is
   .. :class:`bytes`.  :class:`bytearray`\s are accepted too, and in some cases
   .. (such as :class:`readinto`) required.  Text I/O classes work with
   .. :class:`str` data.

   ファイル等への読み書きに用いられるバイナリデータに使われるバイナリ型は :class:`bytes` です。
   :class:`bytearray` も許可されています。ほかにもいくつかのクラス(たとえば :class:`readinto`)
   が必要です。文字列のI/Oクラスは :class:`str` のデータを扱っています。


   .. Note that calling any method (even inquiries) on a closed stream is
   .. undefined.  Implementations may raise :exc:`IOError` in this case.

   閉じたストリームでメソッドを呼び出し(問い合わせでさえ)は定義されていません。
   この場合実装は :exc:`IOError` を発生させます。


   .. IOBase (and its subclasses) support the iterator protocol, meaning that an
   .. :class:`IOBase` object can be iterated over yielding the lines in a stream.

   IOBase(とそのサブクラス)はイテレータプロトコルをサポートします。
   それはつまり :class:`IOBase` オブジェクトはストリーム内の行をyieldを使って
   イテレートすることが出来ます。


   .. IOBase is also a context manager and therefore supports the
   .. :keyword:`with` statement.  In this example, *file* is closed after the
   .. :keyword:`with` statement's suite is finished---even if an exception occurs:

   IOBaseはコンテキストマネージャでもあります。そのため :keyword:`with` 構文を
   サポートします。次の例では *file* は :keyword:`with` 構文が終わった後、
   閉じられます。--それがたとえ例外が発生したあとでさえです。


   ::

      with open('spam.txt', 'w') as file:
          file.write('Spam and eggs!')


   .. :class:`IOBase` provides these data attributes and methods:

   :class:`IOBase` データ属性とメソッドを提供します:


   .. method:: close()

      .. Flush and close this stream. This method has no effect if the file is
      .. already closed. Once the file is closed, any operation on the file
      .. (e.g. reading or writing) will raise an :exc:`ValueError`.

      このストリームをフラッシュして閉じます。このメソッドはファイルが既に閉じられていた場合
      特になにも影響を与えません。
      いったんファイルが閉じられると、すべてのファイルに対する操作 (例えば読み込みや書き込み) で :exc:`ValueError` が発生します。


      .. As a convenience, it is allowed to call this method more than once;
      .. only the first call, however, will have an effect.

      利便性のために、このメソッドを複数回呼ぶことは許可されています。
      しかし、効果があるのは最初の1回だけです。


   .. attribute:: closed

      .. True if the stream is closed.

      ストリームが閉じられていた場合Trueになります。


   .. method:: fileno()

      .. Return the underlying file descriptor (an integer) of the stream if it
      .. exists.  An :exc:`IOError` is raised if the IO object does not use a file
      .. descriptor.

      ストリームが保持しているファイルディスクリプタ(整数値)が存在する場合はそれを返します。
      もしIOオブジェクトがファイルディスクリプタを使っていない場合は :exc:`IOError` が発生します。


   .. method:: flush()

      .. Flush the write buffers of the stream if applicable.  This does nothing
      .. for read-only and non-blocking streams.

      適用可能であればストリームの書き込みバッファをフラッシュします。
      読み込み専用や非ブロッキングストリームには影響を与えません。


   .. method:: isatty()

      .. Return ``True`` if the stream is interactive (i.e., connected to
      .. a terminal/tty device).

      ストリームが相互作用的であれば(つまりターミナルやttyデバイスにつながっている場合)
      ``True`` を返します。


   .. method:: readable()

      .. Return ``True`` if the stream can be read from.  If False, :meth:`read`
      .. will raise :exc:`IOError`.

      ストリームが読み込める場合 ``True`` を返します。
      Falseの場合は :meth:`read` は :exc:`IOError` を発生させます。


   .. method:: readline([limit])

      .. Read and return one line from the stream.  If *limit* is specified, at
      .. most *limit* bytes will be read.

      ストリームから1行読み込んで返します。
      もし *limit* が指定された場合、最大で *limit* バイトが読み込まれます。


      .. The line terminator is always ``b'\n'`` for binary files; for text files,
      .. the *newlines* argument to :func:`.open` can be used to select the line
      .. terminator(s) recognized.

      バイナリファイルでは行末文字は常に ``b'\n'`` となります。テキストファイルでは
      :func:`.open` への *newlines* 引数は行末文字が認識されたときに使われます。


   .. method:: readlines([hint])

      .. Read and return a list of lines from the stream.  *hint* can be specified
      .. to control the number of lines read: no more lines will be read if the
      .. total size (in bytes/characters) of all lines so far exceeds *hint*.

      ストリームから行のリストを読み込んで返します。
      *hint* を指定することで、何行読み込むかを指定出来ます。
      もし読み込んだすべての行のサイズ(バイト数、もしくは文字数)が
      *hint* の値を超えた場合読み込みをそこで終了します。


   .. method:: seek(offset[, whence])

      .. Change the stream position to the given byte *offset*.  *offset* is
      .. interpreted relative to the position indicated by *whence*.  Values for
      .. *whence* are:

      ストリーム位置を指定された *offset* バイトに変更します。
      *offset* は *whence* で指定された位置からの相対位置として解釈されます。
      *whence* に入力できる値は：


      .. * ``0`` -- start of the stream (the default); *offset* should be zero or positive
      .. * ``1`` -- current stream position; *offset* may be negative
      .. * ``2`` -- end of the stream; *offset* is usually negative

      * ``0`` -- ストリームの最初(デフォルト)です。 *offset* はゼロもしくは正の値です。
      * ``1`` -- 現在のストリーム位置です。 *offset* は負の値です。
      * ``2`` -- ストリームの最後です。 *offset* は通常負の値です。


      .. Return the new absolute position.

      新しい絶対位置を返します。


   .. method:: seekable()

      .. Return ``True`` if the stream supports random access.  If ``False``,
      .. :meth:`seek`, :meth:`tell` and :meth:`truncate` will raise :exc:`IOError`.

      もしストリームがランダムアクセスをサポートしていた場合 ``True`` を返します。
      ``False`` の場合は :meth:`seek`, :meth:`tell`, :meth:`truncate` は :exc:`IOError` を発生させます。


   .. method:: tell()

      .. Return the current stream position.

      現在のストリーム位置を返します。


   .. method:: truncate([size])

      .. Resize the stream to the given *size* in bytes (or the current position
      .. if *size* is not specified).  The current stream position isn't changed.
      .. This resizing can extend or reduce the current file size.  In case of
      .. extension, the contents of the new file area depend on the platform
      .. (on most systems, additional bytes are zero-filled, on Windows they're
      .. undetermined).  The new file size is returned.

      指定された *size* バイト (または *size* が指定されなければ現在の位置) にストリームをリサイズします。
      現在のストリーム位置は変更されません。
      このリサイズは、現在のファイルサイズを拡大または縮小させることができます。
      拡大の場合には、新しいファイル領域の内容はプラットホームに依存します
      (ほとんどのシステムでは、追加のバイトがゼロで埋められます。 Windowsでは不定です)。
      新しいファイルサイズが返されます。


   .. method:: writable()

      .. Return ``True`` if the stream supports writing.  If ``False``,
      .. :meth:`write` and :meth:`truncate` will raise :exc:`IOError`.

      ストリームが書き込みをサポートしていた場合 ``True`` を返します。
      ``False`` の場合は :meth:`write`, :meth:`truncate` は :exc:`IOError` を返します。


   .. method:: writelines(lines)

      .. Write a list of lines to the stream.  Line separators are not added, so it
      .. is usual for each of the lines provided to have a line separator at the
      .. end.

      ストリームに複数行書き込みます。
      行区切り文字は付与されないので、書き込む各行の行末には行区切り文字があります。


.. class:: RawIOBase

   .. Base class for raw binary I/O.  It inherits :class:`IOBase`.  There is no
   .. public constructor.

   生バイナリI/Oへのベースクラスです。 :class:`IOBase` を継承しています。
   パブリックコンストラクタはありません。


   .. In addition to the attributes and methods from :class:`IOBase`,
   .. RawIOBase provides the following methods:

   :class:`IOBase` の属性やメソッドに加えて、 RawIOBase は次のメソッドを提供します：


   .. method:: read([n])

      .. Read and return all the bytes from the stream until EOF, or if *n* is
      .. specified, up to *n* bytes.  Only one system call is ever made.  An empty
      .. bytes object is returned on EOF; ``None`` is returned if the object is set
      .. not to block and has no data to read.

      EOF まで、あるいは *n* が指定された場合 *n* バイトまでストリームから\
      すべてのバイトを読み込んで返します。たった1つのシステムコールが呼ばれます。
      既に EOF に達していたら空のバイトオブジェクトが返されます。
      もしオブジェクトがブロックされず読み込むべきデータがない場合は ``None`` が返されます。


   .. method:: readall()

      .. Read and return all the bytes from the stream until EOF, using multiple
      .. calls to the stream if necessary.

      EOF までストリームからすべてのバイトを読み込みます。
      必要な場合はストリームに対して複数の呼び出しをします。


   .. method:: readinto(b)

      .. Read up to len(b) bytes into bytearray *b* and return the number of bytes
      .. read.

      バイト列 *b* に len(b) バイト分読み込み、読み込んだバイト数を返します。


   .. method:: write(b)

      .. Write the given bytes or bytearray object, *b*, to the underlying raw
      .. stream and return the number of bytes written (This is never less than
      .. ``len(b)``, since if the write fails, an :exc:`IOError` will be raised).

      与えられたバイトあるいはバイト列オブジェクト *b* を生のストリームに書き込んで、
      書き込んだバイト数を返します。
      (決して ``len(b)`` よりも小さくなることはありません。
      なぜならはもし書き込みに失敗した場合は :exc:`IOError` が発生するからです)


.. class:: BufferedIOBase

   .. Base class for streams that support buffering.  It inherits :class:`IOBase`.
   .. There is no public constructor.

   バッファリングをサポートするストリームの基底クラスです。
   :class:`IOBase` を継承します。
   パブリックなコンストラクタはありません。


   .. The main difference with :class:`RawIOBase` is that the :meth:`read` method
   .. supports omitting the *size* argument, and does not have a default
   .. implementation that defers to :meth:`readinto`.

   :class:`RawIOBase` との主な違いは :meth:`read` メソッドが *size*
   引数の省略を許し、 :meth:`readinto` と異なるデフォルト実装を持たないことです。


   .. In addition, :meth:`read`, :meth:`readinto`, and :meth:`write` may raise
   .. :exc:`BlockingIOError` if the underlying raw stream is in non-blocking mode
   .. and not ready; unlike their raw counterparts, they will never return
   .. ``None``.

   さらに、 :meth:`read`, :meth:`readinto`, :meth:`write` が、
   元になる生ストリームが非ブロッキングモードでかつ準備ができていない場合に、
   :exc:`BlockingIOError` を送出するかもしれません。
   対応する"生"バージョンと違って、 ``None`` を返すことはありません。


   .. A typical implementation should not inherit from a :class:`RawIOBase`
   .. implementation, but wrap one like :class:`BufferedWriter` and
   .. :class:`BufferedReader`.

   通常の実装では :class:`RawIOBase` 実装を継承して実装せず、
   :class:`BufferedWriter` と :class:`BufferedReader` のようにラップすべきです。


   .. :class:`BufferedIOBase` provides or overrides these methods in addition to
   .. those from :class:`IOBase`:

   :class:`BufferedIOBase` は :class:`IOBase` からのメソッドに加えて、
   以下のメソッドを提供するかもしくはオーバーライドします:


   .. method:: read([n])

      .. Read and return up to *n* bytes.  If the argument is omitted, ``None``, or
      .. negative, data is read and returned until EOF is reached.  An empty bytes
      .. object is returned if the stream is already at EOF.

      最大で *n* バイト読み込み、返します。
      引数が省略されるか、 ``None`` か、または負の値であった場合、
      データは EOF に到達するまで読み込まれます。
      ストリームが既に EOF に到達していた場合空の bytes オブジェクトが返されます。


      .. If the argument is positive, and the underlying raw stream is not
      .. interactive, multiple raw reads may be issued to satisfy the byte count
      .. (unless EOF is reached first).  But for interactive raw streams, at most
      .. one raw read will be issued, and a short result does not imply that EOF is
      .. imminent.

      引数が正で、元になる生ストリームが対話的でなければ、
      複数回の生 read が必要なバイト数を満たすように発行されるかもしれません
      (先に EOF に到達しない限りは)。
      対話的である場合には、最大で一回の raw read しか発行されず、
      短い結果でも EOF に達したことを意味しません。


      .. A :exc:`BlockingIOError` is raised if the underlying raw stream has no
      .. data at the moment.

      元になる生ストリームが呼び出された時点でデータを持っていなければ、
      :exc:`BlockingIOError` が送出されます。


   .. method:: readinto(b)

      .. Read up to len(b) bytes into bytearray *b* and return the number of bytes
      .. read.

      len(b) バイトを上限に bytearray *b* に読み込み、何バイト読んだかを返します。


      .. Like :meth:`read`, multiple reads may be issued to the underlying raw
      .. stream, unless the latter is 'interactive.'

      :meth:`read` と同様、元になる生ストリームに、それが対話的でない限り、
      複数回の read が発行されるかもしれません。


      .. A :exc:`BlockingIOError` is raised if the underlying raw stream has no
      .. data at the moment.

      元になる生ストリームが呼び出された時点でデータを持っていなければ、
      :exc:`BlockingIOError` が送出されます。


   .. method:: write(b)

      .. Write the given bytes or bytearray object, *b*, to the underlying raw
      .. stream and return the number of bytes written (never less than ``len(b)``,
      .. since if the write fails an :exc:`IOError` will be raised).

      与えられた bytes または bytearray オブジェクト *b* を、
      元になる生ストリームに書き込み、書き込まれたバイト数を返します
      (決して ``len(b)`` よりも小さくなることはありません。
      なぜならはもし書き込みに失敗した場合は :exc:`IOError` が発生するからです)


      .. A :exc:`BlockingIOError` is raised if the buffer is full, and the
      .. underlying raw stream cannot accept more data at the moment.

      バッファが満杯で元になる生ストリームが書き込み時点でさらなるデータを受け付けられない場合
      :exc:`BlockingIOError` が送出されます。


生ファイルI/O
--------------

.. class:: FileIO(name[, mode])

   .. :class:`FileIO` represents a file containing bytes data.  It implements
   .. the :class:`RawIOBase` interface (and therefore the :class:`IOBase`
   .. interface, too).

   :class:`FileIO` はバイトデータを含むファイルを表します。
   :class:`RawIOBase` インタフェースを (そしてしたがって
   :class:`IOBase` インタフェースも) 実装しています。


   .. The *mode* can be ``'r'``, ``'w'`` or ``'a'`` for reading (default), writing,
   .. or appending.  The file will be created if it doesn't exist when opened for
   .. writing or appending; it will be truncated when opened for writing.  Add a
   .. ``'+'`` to the mode to allow simultaneous reading and writing.

   *mode* はそれぞれ読み込み(デフォルト)、書き込み、追記を表す
   ``'r'``, ``'w'``, ``'a'`` にすることができます。
   ファイルは書き込みまたは追記モードで開かれたときに存在しなければ作成されます。
   書き込みモードでは存在したファイル内容は消されます。
   読み込みと書き込みを同時に行いたければ ``'+'`` をモードに加えて下さい。


   .. In addition to the attributes and methods from :class:`IOBase` and
   .. :class:`RawIOBase`, :class:`FileIO` provides the following data
   .. attributes and methods:

   :class:`IOBase` および :class:`RawIOBase` から継承した属性とメソッドに加えて、
   :class:`FileIO` は以下のデータ属性とメソッドを提供しています:


   .. attribute:: mode

      .. The mode as given in the constructor.

      コンストラクタに渡されたモードです。


   .. attribute:: name

      .. The file name.  This is the file descriptor of the file when no name is
      .. given in the constructor.

      ファイル名。
      コンストラクタに名前が渡されなかったときはファイルディスクリプタになります。


   .. method:: read([n])

      .. Read and return at most *n* bytes.  Only one system call is made, so it is
      .. possible that less data than was requested is returned.  Use :func:`len`
      .. on the returned bytes object to see how many bytes were actually returned.
      .. (In non-blocking mode, ``None`` is returned when no data is available.)

      最大で *n* バイト読み込み、返します。
      システムコールを一度呼び出すだけなので、要求されたより少ないデータが返されることもあります。
      実際に返されたバイト数を得たければ :func:`len` を返されたバイトオブジェクトに対して使って下さい。
      (非ブロッキングモードでは、データが取れなければ ``None`` が返されます。)


   .. method:: readall()

      .. Read and return the entire file's contents in a single bytes object.  As
      .. much as immediately available is returned in non-blocking mode.  If the
      .. EOF has been reached, ``b''`` is returned.

      ファイルの全内容を読み込み、単一のバイトオブジェクトに入れて返します。
      非ブロッキングモードでは直ちに取得できる限りのものが返されます。
      EOF に到達すると、 ``b''`` が返されます。


   .. method:: write(b)

      .. Write the bytes or bytearray object, *b*, to the file, and return
      .. the number actually written. Only one system call is made, so it
      .. is possible that only some of the data is written.

      与えられたバイトあるいはバイト列オブジェクト *b* をファイルに書き込み、
      実際に書き込まれた(バイト)数を返します。
      システムコールを一度呼び出すだけなので、データの一部だけが書き込まれることもあり得ます。


   .. Note that the inherited ``readinto()`` method should not be used on
   .. :class:`FileIO` objects.

   :class:`FileIO` オブジェクトでは継承された ``readinto()`` メソッドを使うべきではないということを忘れないで下さい。


バッファ付きストリーム
----------------------

.. class:: BytesIO([initial_bytes])

   .. A stream implementation using an in-memory bytes buffer.  It inherits
   .. :class:`BufferedIOBase`.

   インメモリの bytes バッファを利用したストリームの実装。
   :class:`BufferedIOBase` を継承します。


   .. The argument *initial_bytes* is an optional initial bytearray.

   引数 *initial_bytes* は省略可能な bytearray の初期値です。


   .. :class:`BytesIO` provides or overrides these methods in addition to those
   .. from :class:`BufferedIOBase` and :class:`IOBase`:

   :class:`BytesIO` は :class:`BufferedIOBase` または :class:`IOBase`
   からのメソッドに加えて、以下のメソッドを提供するかもしくはオーバーライドします:


   .. method:: getvalue()

      .. Return ``bytes`` containing the entire contents of the buffer.

      バッファの全内容を保持した ``bytes`` を返します。


   .. method:: read1()

      .. In :class:`BytesIO`, this is the same as :meth:`read`.

      :class:`BytesIO` においては、このメソッドは :meth:`read` と同じです。


.. class:: BufferedReader(raw[, buffer_size])

   .. A buffer for a readable, sequential :class:`RawIOBase` object.  It inherits
   .. :class:`BufferedIOBase`.

   読み込み可能でシーケンシャルな :class:`RawIOBase` オブジェクトのバッファです。
   :class:`BufferedIOBase` を継承します。


   .. The constructor creates a :class:`BufferedReader` for the given readable
   .. *raw* stream and *buffer_size*.  If *buffer_size* is omitted,
   .. :data:`DEFAULT_BUFFER_SIZE` is used.

   このコンストラクタは与えられた *raw* ストリームと *buffer_size* に対し
   :class:`BufferedReader` を生成します。
   *buffer_size* が省略された場合 :data:`DEFAULT_BUFFER_SIZE` が代わりに使われます。


   .. :class:`BufferedReader` provides or overrides these methods in addition to
   .. those from :class:`BufferedIOBase` and :class:`IOBase`:

   :class:`BufferedReader` は :class:`BufferedIOBase` または :class:`IOBase`
   からのメソッドに加えて、以下のメソッドを提供するかもしくはオーバーライドします:


   .. method:: peek([n])

      .. Return 1 (or *n* if specified) bytes from a buffer without advancing the
      .. position.  Only a single read on the raw stream is done to satisfy the
      .. call. The number of bytes returned may be less than requested since at
      .. most all the buffer's bytes from the current position to the end are
      .. returned.

      1 (または指定されれば *n*) バイトをバッファから位置を変更せずに読んで返します。
      これを果たすために生ストリームに対して行われる read はただ一度だけです。
      返されるバイト数は、
      最大でもバッファの現在の位置から最後までのバイト列なので、
      要求されたより少なくなるかもしれません。


   .. method:: read([n])

      .. Read and return *n* bytes, or if *n* is not given or negative, until EOF
      .. or if the read call would block in non-blocking mode.

      *n* バイトを読み込んで返します。
      *n* が与えられないかまたは負の値ならば、EOF まで、
      または非ブロッキングモード中で read 呼び出しがブロックされるまでを返します。


   .. method:: read1(n)

      .. Read and return up to *n* bytes with only one call on the raw stream.  If
      .. at least one byte is buffered, only buffered bytes are returned.
      .. Otherwise, one raw stream read call is made.

      生ストリームに対しただ一度の呼び出しで最大 *n* バイトを読み込んで返します。
      少なくとも 1 バイトがバッファされていれば、バッファされているバイト列だけが返されます。
      それ以外の場合にはちょうど一回生ストリームに read 呼び出しが行われます。


.. class:: BufferedWriter(raw[, buffer_size[, max_buffer_size]])

   .. A buffer for a writeable sequential RawIO object.  It inherits
   .. :class:`BufferedIOBase`.

   書き込み可能でシーケンシャルな :class:`RawIOBase` オブジェクトのバッファです。
   :class:`BufferedIOBase` を継承します。


   .. The constructor creates a :class:`BufferedWriter` for the given writeable
   .. *raw* stream.  If the *buffer_size* is not given, it defaults to
   .. :data:`DEAFULT_BUFFER_SIZE`.  If *max_buffer_size* is omitted, it defaults to
   .. twice the buffer size.

   このコンストラクタは与えられた書き込み可能な *raw* ストリームに対し
   :class:`BufferedWriter` を生成します。
   *buffer_size* が省略された場合 :data:`DEFAULT_BUFFER_SIZE` がデフォルトになります。
   *max_buffer_size* が省略された場合、バッファサイズの 2 倍がデフォルトになります。


   .. :class:`BufferedWriter` provides or overrides these methods in addition to
   .. those from :class:`BufferedIOBase` and :class:`IOBase`:

   :class:`BufferedWriter` は :class:`BufferedIOBase` または :class:`IOBase`
   からのメソッドに加えて、以下のメソッドを提供するかもしくはオーバーライドします:


   .. method:: flush()

      .. Force bytes held in the buffer into the raw stream.  A
      .. :exc:`BlockingIOError` should be raised if the raw stream blocks.

      バッファに保持されたバイト列を生ストリームに流し込みます。
      生ストリームがブロックした場合 :exc:`BlockingIOError` が送出されます。


   .. method:: write(b)

      .. Write the bytes or bytearray object, *b*, onto the raw stream and return
      .. the number of bytes written.  A :exc:`BlockingIOError` is raised when the
      .. raw stream blocks.

      bytes または bytearray オブジェクト *b* を生ストリームに書き込み、
      書き込んだバイト数を返します。
      生ストリームがブロックした場合 :exc:`BlockingIOError` が送出されます。


.. class:: BufferedRWPair(reader, writer[, buffer_size[, max_buffer_size]])

   .. A combined buffered writer and reader object for a raw stream that can be
   .. written to and read from.  It has and supports both :meth:`read`, :meth:`write`,
   .. and their variants.  This is useful for sockets and two-way pipes.
   .. It inherits :class:`BufferedIOBase`.

   読み書きできる生ストリームのための組み合わされたバッファ付きライターとリーダーです。
   :meth:`read` 系、 :meth:`write` 系メソッド両方ともサポートされます。
   ソケットや両方向パイプに便利です。
   :class:`BufferedIOBase` を継承しています。


   .. *reader* and *writer* are :class:`RawIOBase` objects that are readable and
   .. writeable respectively.  If the *buffer_size* is omitted it defaults to
   .. :data:`DEFAULT_BUFFER_SIZE`.  The *max_buffer_size* (for the buffered writer)
   .. defaults to twice the buffer size.

   *reader* と *writer* はそれぞれ読み込み可能、書き込み可能な :class:`RawIOBase`
   オブジェクトです。
   *buffer_size* が省略された場合 :data:`DEFAULT_BUFFER_SIZE` がデフォルトになります。
   (バッファ付きライターのための) *max_buffer_size* が省略された場合、バッファサイズの 2 倍がデフォルトになります。


   .. :class:`BufferedRWPair` implements all of :class:`BufferedIOBase`\'s methods.

   :class:`BufferedRWPair` は :class:`BufferedIOBase` の全てのメソッドを実装します。


.. class:: BufferedRandom(raw[, buffer_size[, max_buffer_size]])

   .. A buffered interface to random access streams.  It inherits
   .. :class:`BufferedReader` and :class:`BufferedWriter`.

   ランダムアクセスストリームへのバッファ付きインタフェース。
   :class:`BufferedReader` および :class:`BufferedWriter` を継承しています。


   .. The constructor creates a reader and writer for a seekable raw stream, given
   .. in the first argument.  If the *buffer_size* is omitted it defaults to
   .. :data:`DEFAULT_BUFFER_SIZE`.  The *max_buffer_size* (for the buffered writer)
   .. defaults to twice the buffer size.

   このコンストラクタは第一引数として与えられるシーク可能な生ストリームに対し、
   リーダーおよびライターを作成します。
   *buffer_size* が省略された場合 :data:`DEFAULT_BUFFER_SIZE` がデフォルトになります。
   (バッファ付きライターのための) *max_buffer_size* が省略された場合、バッファサイズの 2 倍がデフォルトになります。


   .. :class:`BufferedRandom` is capable of anything :class:`BufferedReader` or
   .. :class:`BufferedWriter` can do.

   :class:`BufferedRandom` は :class:`BufferedReader` や :class:`BufferedWriter`
   にできることは何でもできます。


文字列 I/O
------------

.. class:: TextIOBase

   .. Base class for text streams.  This class provides a character and line based
   .. interface to stream I/O.  There is no :meth:`readinto` method because
   .. Python's character strings are immutable.  It inherits :class:`IOBase`.
   .. There is no public constructor.

   テキストストリームの基底クラスです。
   このクラスはストリーム I/O への文字と行に基づいたインタフェースを提供します。
   :meth:`readinto` メソッドは Python の文字列が変更不可能なので存在しません。
   :class:`IOBase` を継承します。
   パブリックなコンストラクタはありません。


   .. :class:`TextIOBase` provides or overrides these data attributes and
   .. methods in addition to those from :class:`IOBase`:

   :class:`IOBase` から継承した属性とメソッドに加えて、
   :class:`TextIOBase` は以下のデータ属性とメソッドを提供しています:


   .. attribute:: encoding

      .. The name of the encoding used to decode the stream's bytes into
      .. strings, and to encode strings into bytes.

      エンコーディング名で、ストリームのバイト列を文字列にデコードするとき、
      また文字列をバイト列にエンコードするときに使われます。


   .. attribute:: newlines

      .. A string, a tuple of strings, or ``None``, indicating the newlines
      .. translated so far.

      文字列、文字列のタプル、または ``None`` で、改行がどのように読み換えられるかを指定します。


   .. method:: read(n)

      .. Read and return at most *n* characters from the stream as a single
      .. :class:`str`.  If *n* is negative or ``None``, reads to EOF.

      最大 *n* 文字をストリームから読み込み、一つの文字列にして返します。
      *n* が負の値または ``None`` ならば、 EOF まで読みます。


   .. method:: readline()

      .. Read until newline or EOF and return a single ``str``.  If the stream is
      .. already at EOF, an empty string is returned.

      改行または EOF まで読み込み、一つの ``str`` を返します。
      ストリームが既に EOF に到達している場合、空文字列が返されます。


   .. method:: write(s)

      .. Write the string *s* to the stream and return the number of characters
      .. written.

      文字列 *s* をストリームに書き込み、書き込まれた文字数を返します。


.. class:: TextIOWrapper(buffer[, encoding[, errors[, newline[, line_buffering]]]])

   .. A buffered text stream over a :class:`BufferedIOBase` raw stream, *buffer*.
   .. It inherits :class:`TextIOBase`.

   :class:`BufferedIOBase` 生ストリーム *buffer* 上のバッファ付きテキストストリーム。
   :class:`TextIOBase` を継承します。


   .. *encoding* gives the name of the encoding that the stream will be decoded or
   .. encoded with.  It defaults to :func:`locale.getpreferredencoding`.

   *encoding* にはストリームをデコードしたりそれを使ってエンコードしたりするエンコーディング名を渡します。
   デフォルトは :func:`locale.getpreferredencoding` です。


   .. *errors* is an optional string that specifies how encoding and decoding
   .. errors are to be handled.  Pass ``'strict'`` to raise a :exc:`ValueError`
   .. exception if there is an encoding error (the default of ``None`` has the same
   .. effect), or pass ``'ignore'`` to ignore errors.  (Note that ignoring encoding
   .. errors can lead to data loss.)  ``'replace'`` causes a replacement marker
   .. (such as ``'?'``) to be inserted where there is malformed data.  When
   .. writing, ``'xmlcharrefreplace'`` (replace with the appropriate XML character
   .. reference) or ``'backslashreplace'`` (replace with backslashed escape
   .. sequences) can be used.  Any other error handling name that has been
   .. registered with :func:`codecs.register_error` is also valid.

   *errors* はオプションの文字列でエンコードやデコードの際のエラーをどのように扱うかを指定します。
   エンコードエラーがあったら :exc:`ValueError` 例外を送出させるには
   ``'strict'`` を渡します(デフォルトの ``None`` でも同じです)。
   エラーを無視させるには ``'ignore'`` です。
   (注意しなければならないのはエンコーディングエラーを無視するとデータ喪失につながる可能性があるということです。)
   ``'replace'`` は正常に変換されなかった文字の代わりにマーカ
   (たとえば ``'?'``) を挿入させます。
   書き込み時には ``'xmlcharrefreplace'`` (適切な XML 文字参照に置き換え) や、
   ``'backslashreplace'`` (バックスラッシュによるエスケープシーケンスに置き換え)
   も使えます。
   他にも :func:`codecs.register_error` で登録されたエラー処理名が有効です。


   .. *newline* can be ``None``, ``''``, ``'\n'``, ``'\r'``, or ``'\r\n'``.  It
   .. controls the handling of line endings.  If it is ``None``, universal newlines
   .. is enabled.  With this enabled, on input, the lines endings ``'\n'``,
   .. ``'\r'``, or ``'\r\n'`` are translated to ``'\n'`` before being returned to
   .. the caller.  Conversely, on output, ``'\n'`` is translated to the system
   .. default line separator, :data:`os.linesep`.  If *newline* is any other of its
   .. legal values, that newline becomes the newline when the file is read and it
   .. is returned untranslated.  On output, ``'\n'`` is converted to the *newline*.

   *newline* は ``None``, ``''``, ``'\n'``, ``'\r'``, ``'\r\n'`` のいずれかです。
   行末の扱いを制御します。
   ``None`` では、ユニバーサルニューラインが有効になります。
   これが有効になると、入力時、行末の ``'\n'``, ``'\r'``, ``'\r\n'`` は ``'\n'``
   に変換されて呼び出し側に返されます。
   逆に出力時は ``'\n'`` がシステムのデフォルト行区切り文字 (:data:`os.linesep`)
   に変換されます。
   *newline* が他の適切な値の場合には、ファイル読み込みの際にその改行で改行されるようになり、
   変換は行われません。
   出力時には ``'\n'`` が *newline* に変換されます。


   .. If *line_buffering* is ``True``, :meth:`flush` is implied when a call to
   .. write contains a newline character.

   *line_buffering* が ``True`` の場合、write への呼び出しが改行文字を含んでいれば
   :meth:`flush` がそれに伴って呼び出されます。


   .. :class:`TextIOWrapper` provides these data attributes in addition to those of
   .. :class:`TextIOBase` and its parents:

   :class:`TextIOBase` およびその親クラスの属性に加えて、
   :class:`TextIOWrapper` は以下のデータ属性を提供しています:


   .. attribute:: errors

      .. The encoding and decoding error setting.

      エンコーディングおよびデコーディングエラーの設定。


   .. attribute:: line_buffering

      .. Whether line buffering is enabled.

      行バッファリングが有効かどうか。


.. class:: StringIO([initial_value[, encoding[, errors[, newline]]]])

   .. An in-memory stream for text.  It inherits :class:`TextIOWrapper`.

   テキストのためのインメモリストリーム。
   :class:`TextIOWrapper` を継承します。


   .. Create a new StringIO stream with an inital value, encoding, error handling,
   .. and newline setting.  See :class:`TextIOWrapper`\'s constructor for more
   .. information.

   新しい StringIO ストリームを初期値、エンコーディング、エラーの扱い、改行設定から作成します。
   より詳しい情報は :class:`TextIOWrapper` のコンストラクタを参照して下さい。


   .. :class:`StringIO` provides this method in addition to those from
   .. :class:`TextIOWrapper` and its parents:

   :class:`TextIOWrapper` およびその親クラスから継承したメソッドに加えて
   :class:`StringIO` は以下のメソッドを提供しています:


   .. method:: getvalue()

      .. Return a ``str`` containing the entire contents of the buffer.

      バッファの全内容を保持した ``str`` を返します。


.. class:: IncrementalNewlineDecoder

   .. A helper codec that decodes newlines for universal newlines mode.  It
   .. inherits :class:`codecs.IncrementalDecoder`.

   ユニバーサルニューラインモード向けに改行をデコードする補助コーデック。
   :class:`codecs.IncrementalDecoder` を継承します。

