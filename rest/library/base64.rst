
:mod:`base64` --- RFC 3548: Base16, Base32, Base64 テータの符号化
==========================================================

.. module:: base64
   :synopsis: RFC 3548: Base16, Base32, Base64 テータの符号化


.. index::
   pair: base64; encoding
   single: MIME; base64 encoding

このモジュールは任意のバイナリ文字列を(eメールやHTTPのPOSTリクエストの一
部としてで安全に送ることのできるテキスト文字列に変換する)base64形式へエンコー ドおよびデコードする機能を提供します。
エンコードの概要は:rfc:`1521`\ (*MIME(Multipurpose Internet Mail Extensions)Part One:
Mechanisms for Specifying and Describing the Format of Internet Message Bodies*,
section 5.2, "Base64 Content-Transfer-Encoding")で定義されていて、
MIME形式のeメールやインターネットのさまざまな場面で利用されています。
この形式は:program:`uuencode`プログラムによる出力とは違うものです。 たとえば、``'www.python.org'``は、
``'d3d3LnB5dGhvbi5vcmc=\n'``とエンコードされます。

.. % This module performs base64 encoding and decoding of arbitrary binary
.. % strings into text strings that can be safely sent by email or included
.. % as part of an HTTP POST request.  The
.. % encoding scheme is defined in \rfc{1521} (\emph{MIME
.. % (Multipurpose Internet Mail Extensions) Part One: Mechanisms for
.. % Specifying and Describing the Format of Internet Message Bodies},
.. % section 5.2, ``Base64 Content-Transfer-Encoding'') and is used for
.. % MIME email and various other Internet-related applications; it is not
.. % the same as the output produced by the \program{uuencode} program.
.. % For example, the string \code{'www.python.org'} is encoded as the
.. % string \code{'d3d3LnB5dGhvbi5vcmc=\e n'}.

このモジュールは、 :rfc:`3548` で定められた仕様による データの符号化 (エンコード、encoding) および復元 (デコード、decoding)
を 提供します。この RFC 標準では Base16, Base32 および Base64 が
定義されており、これはバイナリ文字列とテキスト文字列とをエンコードあるいは デコードするためのアルゴリズムです。変換されたテキスト文字列は email で確実に
送信したり、URL の一部として使用したり、HTTP POST リクエストの一部に 含めることができます。これらの符号化アルゴリズムは
:program:`uuencode` で 使われているものとは別物です。

このモジュールでは 2つのインターフェイスが提供されています。 現代的なインターフェイスは、これら 3種類のアルファベット集合を使った
文字列オブジェクトのエンコードおよびデコードをすべてサポートします。 一方、レガシーなインターフェイスは、文字列とともにファイル風のオブジェクトに対する
エンコード / デコードを提供しますが、Base64 標準のアルファベット集合しか 使いません。

現代的なインターフェイスは以下のものを提供します:


.. function:: b64encode(s[, altchars])

   Base64 をつかって、文字列を エンコード (符号化) します。

   *s* はエンコードする文字列です。オプション引数 *altchars* は 最低でも 2 の長さをもつ文字列で (これ以降の文字は無視されます)、 これは
   ``+`` と ``/`` の代わりに使われる代替アルファベットを指定します。 これにより、アプリケーションはたとえば URL
   やファイルシステムの影響をうけない Base64 文字列を生成することができます。デフォルトの値は ``None`` で、 これは標準の Base64
   アルファベット集合が使われることを意味します。

   エンコードされた文字列が返されます。


.. function:: b64decode(s[, altchars])

   Base64 文字列をデコード (復元) します。

   *s* にはデコードする文字列を渡します。オプション引数の *altchars* は 最低でも 2 の長さをもつ文字列で (これ以降の文字は無視されます)、
   これは ``+`` と ``/`` の代わりに使われる代替アルファベットを指定します。

   デコードされた文字列が返されます。*s* が正しくパディングされていなかったり、 規定のアルファベット以外の文字が含まれていた場合には
   :exc:`TypeError` が発生します。


.. function:: standard_b64encode(s)

   標準の Base64 アルファベット集合をもちいて文字列 *s* をエンコード (符号化) します。


.. function:: standard_b64decode(s)

   標準の Base64 アルファベット集合をもちいて文字列 *s* をデコード (復元) します。


.. function:: urlsafe_b64encode(s)

   URL 用に安全なアルファベット集合をもちいて文字列 *s* をエンコード (符号化) します。 これは、標準の Base64 アルファベット集合にある
   ``+`` のかわりに ``-`` を使い、 ``/`` のかわりに ``_`` を使用します。


.. function:: urlsafe_b64decode(s)

   URL 用に安全なアルファベット集合をもちいて文字列 *s* をデコード (復元) します。 これは、標準の Base64 アルファベット集合にある ``+``
   のかわりに ``-`` を使い、 ``/`` のかわりに ``_`` を使用します。


.. function:: b32encode(s)

   Base32 をつかって、文字列をエンコード (符号化) します。 *s* にはエンコードする文字列を渡し、エンコードされた文字列が返されます。


.. function:: b32decode(s[, casefold[, map01]])

   Base32 をつかって、文字列をデコード (復元) します。

   *s* にはエンコードする文字列を渡します。オプション引数 *casefold* は 小文字のアルファベットを受けつけるかどうかを指定します。
   セキュリティ上の理由により、デフォルトではこれは ``False`` になっています。

   :rfc:`3548` は付加的なマッピングとして、数字の 0 (零) を アルファベットの O (オー) に、数字の 1 (壱) をアルファベットの I
   (アイ) または L (エル) に 対応させることを許しています。オプション引数は *map01* は、 ``None`` でないときは、数字の 1
   をどの文字に対応づけるかを指定します (map01 が ``None`` でないとき、数字の 0 はつねにアルファベットの O (オー) に対応づけられます)。
   セキュリティ上の理由により、これはデフォルトでは ``None`` になっているため、 0 および 1 は入力として許可されていません。

   デコードされた文字列が返されます。*s* が正しくパディングされていなかったり、 規定のアルファベット以外の文字が含まれていた場合には
   :exc:`TypeError` が発生します。


.. function:: b16encode(s)

   Base16 をつかって、文字列をエンコード (符号化) します。

   *s* にはエンコードする文字列を渡し、エンコードされた文字列が返されます。


.. function:: b16decode(s[, casefold])

   Base16 をつかって、文字列をデコード (復元) します。

   *s* にはエンコードする文字列を渡します。オプション引数 *casefold* は 小文字のアルファベットを受けつけるかどうかを指定します。
   セキュリティ上の理由により、デフォルトではこれは ``False`` になっています。

   デコードされた文字列が返されます。*s* が正しくパディングされていなかったり、 規定のアルファベット以外の文字が含まれていた場合には
   :exc:`TypeError` が発生します。

レガシーなインターフェイスは以下のものを提供します:


.. function:: decode(input, output)

   *input*の中身をデコードした結果を*output*に出力します。 *input*、*output*ともにファイルオブジェクトか、ファイルオブジェ
   クトと同じインターフェースを持ったオブジェクトである必要があります。 *input*は``input.read()``が空文字列を返すまで読まれます。

   .. % Decode the contents of the \var{input} file and write the resulting
   .. % binary data to the \var{output} file.
   .. % \var{input} and \var{output} must either be file objects or objects that
   .. % mimic the file object interface. \var{input} will be read until
   .. % \code{\var{input}.read()} returns an empty string.


.. function:: decodestring(s)

   文字列*s*をデコードして結果のバイナリデータを返します。 *s*には一行以上のbase64形式でエンコードされたデータが含まれている必 要があります。

   .. % Decode the string \var{s}, which must contain one or more lines of
   .. % base64 encoded data, and return a string containing the resulting
   .. % binary data.


.. function:: encode(input, output)

   *input*の中身をbase64形式でエンコードした結果を*output*に出力します。
   *input*、*output*ともにファイルオブジェクトか、ファイルオブジェ クトと同じインターフェースを持ったオブジェクトである必要があります。
   *input*は``input.read()``が空文字列を返すまで読まれます。
   :func:`encode`はエンコードされたデータと改行文字(``'\n'``)を出 力します。

   .. % Encode the contents of the \var{input} file and write the resulting
   .. % base64 encoded data to the \var{output} file.
   .. % \var{input} and \var{output} must either be file objects or objects that
   .. % mimic the file object interface. \var{input} will be read until
   .. % \code{\var{input}.read()} returns an empty string.  \function{encode()}
   .. % returns the encoded data plus a trailing newline character
   .. % (\code{'\e n'}).


.. function:: encodestring(s)

   文字列*s*(任意のバイナリデータを含むことができます)を base64形式でエンコードした結果の(1行以上の文字列)データを返します。
   :func:`encodestring`はエンコードされた一行以上のデータと改行文字 (``'\n'``)を出力します。

   .. % Encode the string \var{s}, which can contain arbitrary binary data,
   .. % and return a string containing one or more lines of
   .. % base64-encoded data.  \function{encodestring()} returns a
   .. % string containing one or more lines of base64-encoded data
   .. % always including an extra trailing newline (\code{'\e n'}).

モジュールの使用例::

   >>> import base64
   >>> encoded = base64.b64encode('data to be encoded')
   >>> encoded
   'ZGF0YSB0byBiZSBlbmNvZGVk'
   >>> data = base64.b64decode(encoded)
   >>> data
   'data to be encoded'


.. seealso::

   Module :mod:`binascii`
      ASCII からバイナリへ、バイナリからASCIIへの 変換をサポートするモジュール。

   :rfc:`1521` - MIME (Multipurpose Internet Mail Extensions) Part One: Mechanisms for Specifying and Describing the Format of Internet Message Bodies
      Section 5.2, "Base64 Content-Transfer-Encoding," provides the definition of the
      base64 encoding.

