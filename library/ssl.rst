..
   以下は、socket モジュールから削除された節です。このモジュールの翻訳時に参考にできるかもしれません。
   .. _ssl-objects:

   SSL オブジェクト
   ----------------

   SSLオブジェクトには、以下のメソッドがあります。


   .. method:: SSL.write(s)

      文字列 *s* をSSL接続で出力します。戻り値として、送信したバイト数を返します。


   .. method:: SSL.read([n])

      SSL接続からデータを受信します。 *n* を指定した場合は指定したバイト数のデータを受信し、省略時はEOFまで読み込みます。戻り値として、受信したバイ
      ト列の文字列を返します。


   .. method:: SSL.server()

      サーバの証明書を特定するための ASN.1 識別名(distinguished name)を含む文字列を
      返します。(下の例を見ると識別名がどう見えるものか判ります。)


   .. method:: SSL.issuer()

      サーバの証明書の発行者を特定するための ASN.1 識別名(distinguished name)を含む文字列を返します。


.. :mod:`ssl` --- SSL wrapper for socket objects

:mod:`ssl` --- ソケットオブジェクトに対するSSLラッパー
=======================================================

.. module:: ssl
   :synopsis: ソケットオブジェクトに対するSSLラッパー

.. moduleauthor:: Bill Janssen <bill.janssen@gmail.com>

.. versionadded:: 2.6

.. sectionauthor::  Bill Janssen <bill.janssen@gmail.com>


.. index:: single: OpenSSL; (use in module ssl)

.. index:: TLS, SSL, Transport Layer Security, Secure Sockets Layer

This module provides access to Transport Layer Security (often known as "Secure
Sockets Layer") encryption and peer authentication facilities for network
sockets, both client-side and server-side.  This module uses the OpenSSL
library. It is available on all modern Unix systems, Windows, Mac OS X, and
probably additional platforms, as long as OpenSSL is installed on that platform.

このモジュールは Transport Layer Security (よく "Secure Sockets Layer"
という名前で知られています) 暗号化と、クライアントサイド、サーバーサイド
両方のネットワークソケットのためのピア認証の仕組みを提供しています。
このモジュールはOpenSSLライブラリを利用しています。
OpenSSLは、全てのモダンなUnixシステム、Windows、Mac OS X、その他幾つかの
OpenSSLがインストールされているプラットフォームで利用できます。

.. note::

   Some behavior may be platform dependent, since calls are made to the
   operating system socket APIs.  The installed version of OpenSSL may also
   cause variations in behavior.

   OSのソケットAPIに対して実装されているので、幾つかの挙動はプラットフォーム依存に
   なるかもしれません。
   インストールされているOpenSSLのバージョンの違いも挙動の違いの原因になるかもしれません。


This section documents the objects and functions in the ``ssl`` module; for more
general information about TLS, SSL, and certificates, the reader is referred to
the documents in the "See Also" section at the bottom.


このセクションでは、 ``ssl`` モジュールのオブジェクトと関数の解説します。
TLS, SSL, certificates に関するより一般的な情報は、末尾にある "See Also"
のセクションを参照してください。

This module provides a class, :class:`ssl.SSLSocket`, which is derived from the
:class:`socket.socket` type, and provides a socket-like wrapper that also
encrypts and decrypts the data going over the socket with SSL.  It supports
additional :meth:`read` and :meth:`write` methods, along with a method,
:meth:`getpeercert`, to retrieve the certificate of the other side of the
connection, and a method, :meth:`cipher`, to retrieve the cipher being used for
the secure connection.

このモジュールは1つのクラス、 :class:`ssl.SSLSocket` を提供します。
このクラスは :class:`socket.socket` クラスを継承していて、ソケットで
通信されるデータをSSLで暗号化・復号するソケットに似たラッパーになります。
また、このクラスは追加で、 :meth:`read` と :meth:`write` メソッド、
接続の相手側から certificate を受信する :meth:`getpeercert` メソッド、
セキュア接続で使うための cipher を受信する :meth:`cipher` メソッドをサポートしています。


Functions, Constants, and Exceptions

関数、定数、例外
----------------

.. exception:: SSLError

   Raised to signal an error from the underlying SSL implementation.  This
   signifies some problem in the higher-level encryption and authentication
   layer that's superimposed on the underlying network connection.  This error
   is a subtype of :exc:`socket.error`, which in turn is a subtype of
   :exc:`IOError`.

   下層のSSL実装からのエラーを伝えるための例外です。
   このエラーは、低レベルなネットワークの上に載っている、高レベルな暗号化と認証レイヤーでの
   問題を通知します。
   このエラーは :exc:`socket.error` のサブタイプで、 :exc:`socket.error` は
   :exc:`IOError` のサブタイプです。


.. function:: wrap_socket (sock, keyfile=None, certfile=None, server_side=False, cert_reqs=CERT_NONE, ssl_version={see docs}, ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True)

   Takes an instance ``sock`` of :class:`socket.socket`, and returns an instance
   of :class:`ssl.SSLSocket`, a subtype of :class:`socket.socket`, which wraps
   the underlying socket in an SSL context.  For client-side sockets, the
   context construction is lazy; if the underlying socket isn't connected yet,
   the context construction will be performed after :meth:`connect` is called on
   the socket.  For server-side sockets, if the socket has no remote peer, it is
   assumed to be a listening socket, and the server-side SSL wrapping is
   automatically performed on client connections accepted via the :meth:`accept`
   method.  :func:`wrap_socket` may raise :exc:`SSLError`.

   :class:`socket.socket` のインスタンス ``sock`` を受け取り、 :class:`socket.socket`` のサブタイプである
   :class:`ssl.SSLSocket` のインスタンスを返します。 :class:`ssl.SSLSocket` は低レイヤの
   ソケットをSSLコンテキストでラップします。
   クライアントサイドソケットにおいて、コンテキストの生成は遅延されます。
   つまり、低レイヤのソケットがまだ接続されていない場合、コンテキストの生成はそのソケットの
   :meth:`connect` メソッドが呼ばれた後に行われます。
   サーバーサイドソケットの場合、そのソケットに接続先が居なければそれは listen 用ソケットだと
   判断されます。 :meth:`accept` メソッドで生成されるクライアント接続に対してのサーバーサイド
   SSLラップは自動的に行われます。そのクライアント接続に対して :func:`wrap_socket` を実行すると
   :exc:`SSLError` が発生します。

   The ``keyfile`` and ``certfile`` parameters specify optional files which
   contain a certificate to be used to identify the local side of the
   connection.  See the discussion of :ref:`ssl-certificates` for more
   information on how the certificate is stored in the ``certfile``.

   オプションの ``keyfile`` と ``certfile`` 引数は、接続のローカル側を識別するために利用される
   証明書を含むファイルを指定します。
   証明書がどのように ``certfile`` に格納されるかについてのより詳しい情報は、 :ref:`ssl-certificates` 
   を参照してください。

   Often the private key is stored in the same file as the certificate; in this
   case, only the ``certfile`` parameter need be passed.  If the private key is
   stored in a separate file, both parameters must be used.  If the private key
   is stored in the ``certfile``, it should come before the first certificate in
   the certificate chain.

   多くの場合、証明書と同じファイルに秘密鍵も格納されています。この場合、 ``certfile``
   引数だけが必要とされます。
   秘密鍵が証明書と別のファイルに格納されている場合、両方の引数を指定しなければなりません。
   秘密鍵が ``certfile`` に格納されている場合、秘密鍵は証明書チェインの最初の証明書よりも先に
   ないといけません。 ::

      -----BEGIN RSA PRIVATE KEY-----
      ... (private key in base64 encoding) ...
      -----END RSA PRIVATE KEY-----
      -----BEGIN CERTIFICATE-----
      ... (certificate in base64 PEM encoding) ...
      -----END CERTIFICATE-----

   The parameter ``server_side`` is a boolean which identifies whether server-side or client-side
   behavior is desired from this socket.

   ``server_side`` 引数は真偽値で、このソケットがサーバーサイドとクライアントサイドのどちらの
   動作をするのかを指定します。

   The parameter ``cert_reqs`` specifies whether a certificate is
   required from the other side of the connection, and whether it will
   be validated if provided.  It must be one of the three values
   :const:`CERT_NONE` (certificates ignored), :const:`CERT_OPTIONAL` (not required,
   but validated if provided), or :const:`CERT_REQUIRED` (required and
   validated).  If the value of this parameter is not :const:`CERT_NONE`, then
   the ``ca_certs`` parameter must point to a file of CA certificates.

   ``cert_reqs`` 引数は、接続の相手側がどの証明書を要求しているのかと、
   それを検証(validate)するかどうかを指定します。これは次の3つの定数のどれかで無ければなりません:
   :const:`CERT_NONE` (証明書は無視されます), :const:`CERT_OPTIONAL`
   (要求はされないが、提供された場合は検証する), :const:`CERT_REQUIRED`
   (証明書を要求するし、検証する)。
   もしこの引数が :const:`CERT_NONE` 以外だった場合、 ``ca_certs`` 引数はCA証明書ファイルを
   指定していなければなりません。

   The ``ca_certs`` file contains a set of concatenated "certification authority" certificates,
   which are used to validate certificates passed from the other end of the connection.
   See the discussion of :ref:`ssl-certificates` for more information about how to arrange
   the certificates in this file.

   ``ca_certs`` ファイルは、接続の相手側から渡された証明書を検証するために使う、
   一連のCA証明書を結合したものを含んでいます。
   このファイル内にどう証明書を並べるかについての詳しい情報は :ref:`ssl-certificates`
   を参照してください。

   The parameter ``ssl_version`` specifies which version of the SSL protocol to use.
   Typically, the server chooses a particular protocol version, and the client
   must adapt to the server's choice.  Most of the versions are not interoperable
   with the other versions.  If not specified, for client-side operation, the
   default SSL version is SSLv3; for server-side operation, SSLv23.  These
   version selections provide the most compatibility with other versions.

   ``ssl_version`` 引数は、使用するSSLプロトコルのバージョンを指定します。
   通常、サーバー側が特定のプロトコルバージョンを選び、クライアント側は
   サーバーの選んだプロトコルを受け入れなければなりません。
   ほとんどのバージョンは他のバージョンと互換性がありません。
   もしこの引数が指定されなかった場合、クライアントサイドでは、デフォルトの
   SSLバージョンは SSLv3 になります。サーバーサイドでは SSLv23 です。
   これらのバージョンは、できるだけの互換性を確保するように選ばれています。

   Here's a table showing which versions in a client (down the side)
   can connect to which versions in a server (along the top):

   次のテーブルは、どのクライアント側のバージョンがどのサーバー側のバージョンに
   接続できるかを示しています。

     .. table::

       ========================  =========  =========  ==========  =========
        *client* / **server**    **SSLv2**  **SSLv3**  **SSLv23**  **TLSv1**
       ------------------------  ---------  ---------  ----------  ---------
        *SSLv2*                    yes        no         yes*        no
        *SSLv3*                    yes        yes        yes         no
        *SSLv23*                   yes        no         yes         no
        *TLSv1*                    no         no         yes         yes
       ========================  =========  =========  ==========  =========

.. vimのシンタックスハイライトエラー対策用コメント.

   In some older versions of OpenSSL (for instance, 0.9.7l on OS X 10.4),
   an SSLv2 client could not connect to an SSLv23 server.

   幾つかの古いバージョンのOpenSSL(例えば、OS X 10.4 の 0.9.7l)では、
   SSLv2クライアントが SSLv23 サーバーに接続できません。

   The parameter ``do_handshake_on_connect`` specifies whether to do the SSL
   handshake automatically after doing a :meth:`socket.connect`, or whether the
   application program will call it explicitly, by invoking the
   :meth:`SSLSocket.do_handshake` method.  Calling
   :meth:`SSLSocket.do_handshake` explicitly gives the program control over the
   blocking behavior of the socket I/O involved in the handshake.

   ``do_handshake_on_connect`` 引数は、 :meth:`socket.connect` の後に自動的に
   SSLハンドシェイクを行うか、それともアプリケーションが明示的に :meth:`SSLSocket.do_handshake`
   メソッドを実行するかを指定します。
   :meth:`SSLSocket.do_handshake` を明示的に呼びだすことで、ハンドシェイクによる
   ソケットI/Oのブロッキング動作を制御できます。

   The parameter ``suppress_ragged_eofs`` specifies how the :meth:`SSLSocket.read`
   method should signal unexpected EOF from the other end of the connection.  If specified
   as :const:`True` (the default), it returns a normal EOF in response to unexpected
   EOF errors raised from the underlying socket; if :const:`False`, it will raise
   the exceptions back to the caller.

   ``suppress_ragged_eofs`` 引数は、 :meth:`SSLSocket.read`` メソッドが、接続先から
   予期しないEOFを受け取った時に通知する方法を指定します。
   :const:`True` (デフォルト) の場合、下位のソケットレイヤーから予期せぬEOFエラーが来た場合、
   通常のEOFを返します。 :const:`False` の場合、呼び出し元に例外を投げて通知します。

.. function:: RAND_status()

   Returns True if the SSL pseudo-random number generator has been seeded with
   'enough' randomness, and False otherwise.  You can use :func:`ssl.RAND_egd`
   and :func:`ssl.RAND_add` to increase the randomness of the pseudo-random
   number generator.

   SSL 擬似乱数生成器が十分なランダム性(randomness)を受け取っている時に真を、
   それ以外の場合は偽を返します。
   :func:`ssl.RAND_egd` と :func:`ssl.RAND_add` を使って擬似乱数生成機に
   ランダム性を渡すことができます。

.. function:: RAND_egd(path)

   If you are running an entropy-gathering daemon (EGD) somewhere, and ``path``
   is the pathname of a socket connection open to it, this will read 256 bytes
   of randomness from the socket, and add it to the SSL pseudo-random number
   generator to increase the security of generated secret keys.  This is
   typically only necessary on systems without better sources of randomness.

   もしエントロピー収集デーモン(EGD=entropy-gathering daemon)が動いていて、
   ``path`` がEGDへのソケットのパスだった場合、この関数はそのソケットから
   256バイトのランダム性を読み込み、SSL擬似乱数生成器にそれを渡すことで、
   生成される暗号鍵のセキュリティを向上させることができます。
   これは、より良いランダム性のソースが内システムでのみ必要です。

   See http://egd.sourceforge.net/ or http://prngd.sourceforge.net/ for
   sources of entropy-gathering daemons.

   エントロピー収集デーモンについては、
   http://egd.sourceforge.net/ や http://prngd.sourceforge.net/
   を参照してください。

.. function:: RAND_add(bytes, entropy)

   Mixes the given ``bytes`` into the SSL pseudo-random number generator.  The
   parameter ``entropy`` (a float) is a lower bound on the entropy contained in
   string (so you can always use :const:`0.0`).  See :rfc:`1750` for more
   information on sources of entropy.

   与えられた ``bytes`` をSSL擬似乱数生成器に混ぜます。
   ``entropy`` 引数(float値)は、その文字列に含まれるエントロピーの下限です。
   (なので、いつでも :const:`0.0` を使うことができます。)
   エントロピーのソースについてのより詳しい情報は、 :rfc:`1750` を参照してください。

.. function:: cert_time_to_seconds(timestring)

   Returns a floating-point value containing a normal seconds-after-the-epoch
   time value, given the time-string representing the "notBefore" or "notAfter"
   date from a certificate.

   証明書内の "notBefore" や "notAfter" で使われている日時の文字列表現 *timestring*
   から、通常のエポック秒を含むfloat値にして返します。

   Here's an example

   例です。 ::

     >>> import ssl
     >>> ssl.cert_time_to_seconds("May  9 00:00:00 2007 GMT")
     1178694000.0
     >>> import time
     >>> time.ctime(ssl.cert_time_to_seconds("May  9 00:00:00 2007 GMT"))
     'Wed May  9 00:00:00 2007'
     >>>

.. function:: get_server_certificate (addr, ssl_version=PROTOCOL_SSLv3, ca_certs=None)

   Given the address ``addr`` of an SSL-protected server, as a (*hostname*,
   *port-number*) pair, fetches the server's certificate, and returns it as a
   PEM-encoded string.  If ``ssl_version`` is specified, uses that version of
   the SSL protocol to attempt to connect to the server.  If ``ca_certs`` is
   specified, it should be a file containing a list of root certificates, the
   same format as used for the same parameter in :func:`wrap_socket`.  The call
   will attempt to validate the server certificate against that set of root
   certificates, and will fail if the validation attempt fails.

   SSLで保護されたサーバーのアドレス ``addr`` を (*hostname*, *port-number*)
   の形で受け取り、そのサーバーから証明書を取得し、それを PEMエンコードされた
   文字列として返します。
   ``ssl_version`` が指定された場合は、サーバーに接続を試みるときに
   そのバージョンのSSLプロトコルを利用します。
   ``ca_certs`` が指定された場合、それは :func:`wrap_socket` の同名の引数と同じフォーマットで、
   ルート証明書のリストを含むファイルでなければなりません。
   この関数はサーバー証明書をルート証明書リストに対して認証し、認証が失敗した
   場合にこの関数も失敗します。

.. function:: DER_cert_to_PEM_cert (DER_cert_bytes)

   Given a certificate as a DER-encoded blob of bytes, returns a PEM-encoded
   string version of the same certificate.

   DERエンコードされたバイト列として与えられた証明書から、
   PEMエンコードされたバージョンの同じ証明書を返します。

.. function:: PEM_cert_to_DER_cert (PEM_cert_string)

   Given a certificate as an ASCII PEM string, returns a DER-encoded sequence of
   bytes for that same certificate.

   PEM 形式のASCII文字列として与えられた証明書から、
   同じ証明書をDERエンコードしたバイト列を返します。

.. data:: CERT_NONE

   Value to pass to the ``cert_reqs`` parameter to :func:`sslobject` when no
   certificates will be required or validated from the other side of the socket
   connection.

   ソケット接続先からの証明書やその認証を必要としないときに、 :func:`sslobject`
   の ``cert_reqs`` 引数に指定する値。

.. data:: CERT_OPTIONAL

   Value to pass to the ``cert_reqs`` parameter to :func:`sslobject` when no
   certificates will be required from the other side of the socket connection,
   but if they are provided, will be validated.  Note that use of this setting
   requires a valid certificate validation file also be passed as a value of the
   ``ca_certs`` parameter.

   ソケット接続先からの証明書を必要としないが、もし証明書があればそれを認証する
   場合に :func:`sslobject` の ``cert_reqs`` 引数に指定する値。
   この設定を利用するときは、 ``ca_certs`` 引数に有効な証明書認証ファイルが渡される
   必要があることに注意してください。

.. data:: CERT_REQUIRED

   Value to pass to the ``cert_reqs`` parameter to :func:`sslobject` when
   certificates will be required from the other side of the socket connection.
   Note that use of this setting requires a valid certificate validation file
   also be passed as a value of the ``ca_certs`` parameter.

   ソケット接続先からの証明書とその認証が必要なときに :func:`sslobject` の
   ``cert_reqs`` 引数に指定する値。
   この設定を利用するときは、 ``ca_certs`` 引数に有効な証明書認証ファイルが渡される
   必要があることに注意してください。

.. data:: PROTOCOL_SSLv2

   Selects SSL version 2 as the channel encryption protocol.

   .. warning::

      SSL version 2 is insecure.  Its use is highly discouraged.

      SSL version 2 は非セキュアです。
      このプロトコルは強く非推奨です。

.. data:: PROTOCOL_SSLv23

   Selects SSL version 2 or 3 as the channel encryption protocol.  This is a
   setting to use with servers for maximum compatibility with the other end of
   an SSL connection, but it may cause the specific ciphers chosen for the
   encryption to be of fairly low quality.

   チャンネル暗号化プロトコルとしてSSLバージョン2か3を選択します。
   これはサーバー側が相手側への最大限の互換性を確保するための設定です。
   しかし、この設定では非常に低い品質の暗号化が選ばれる可能性があります。

   .. todo::
      だれかチェックお願い。

.. data:: PROTOCOL_SSLv3

   Selects SSL version 3 as the channel encryption protocol.  For clients, this
   is the maximally compatible SSL variant.

   チャンネル暗号化プロトコルとしてSSLバージョン3をを選択します。
   クライアントにとって、これは最大限に互換性の高いSSLの種類です。

.. data:: PROTOCOL_TLSv1

   Selects TLS version 1 as the channel encryption protocol.  This is the most
   modern version, and probably the best choice for maximum protection, if both
   sides can speak it.

   チャンネル暗号化プロトコルとしてTLSバージョン1を選択します。
   これは最も現代的で、接続の両サイドが利用できる場合は、たぶん最も安全な選択肢です。


SSLSocket オブジェクト
----------------------

.. method:: SSLSocket.read([nbytes=1024])

   Reads up to ``nbytes`` bytes from the SSL-encrypted channel and returns them.

   ``nbytes`` 以下のバイト列を SSL暗号化されたチャンネルから受信してそれを返します。

.. method:: SSLSocket.write(data)

   Writes the ``data`` to the other side of the connection, using the SSL
   channel to encrypt.  Returns the number of bytes written.

   ``data`` をSSLチャンネルを使って暗号化した上で接続の相手側へ送ります。
   書き込めたバイト数を返します。

.. method:: SSLSocket.getpeercert(binary_form=False)

   If there is no certificate for the peer on the other end of the connection,
   returns ``None``.

   接続先に証明書が無い場合、 ``None`` を返します。

   If the parameter ``binary_form`` is :const:`False`, and a certificate was
   received from the peer, this method returns a :class:`dict` instance.  If the
   certificate was not validated, the dict is empty.  If the certificate was
   validated, it returns a dict with the keys ``subject`` (the principal for
   which the certificate was issued), and ``notAfter`` (the time after which the
   certificate should not be trusted).  The certificate was already validated,
   so the ``notBefore`` and ``issuer`` fields are not returned.  If a
   certificate contains an instance of the *Subject Alternative Name* extension
   (see :rfc:`3280`), there will also be a ``subjectAltName`` key in the
   dictionary.

   ``binary_form`` が :const:`False` で接続先から証明書を取得した場合、
   このメソッドは :class:`dict` のインスタンスを返します。
   証明書が認証されていない場合、辞書は空です。
   証明書が認証されていた場合、 ``subject`` (証明書が発行された principal),
   ``notafter`` (その証明書がそれ以降信頼できなくなる時間) が格納された辞書を返します。
   証明書は既に認証されているので、 ``notBefore`` と ``issuer`` フィールドは返されません。
   証明書が *Subject Alternative Name* 拡張(:rfc:`3280` を参照)のインスタンスを
   格納していた場合、 ``subjectAltName`` キーも辞書に含まれます。

   The "subject" field is a tuple containing the sequence of relative
   distinguished names (RDNs) given in the certificate's data structure for the
   principal, and each RDN is a sequence of name-value pairs.

   "subject" フィールドは、証明書の principal に格納されているRDN
   (relative distinguishued name)のシーケンスを格納したタプルで、各RDNは
   name-value ペアのシーケンスです。 ::

      {'notAfter': 'Feb 16 16:54:50 2013 GMT',
       'subject': ((('countryName', u'US'),),
                   (('stateOrProvinceName', u'Delaware'),),
                   (('localityName', u'Wilmington'),),
                   (('organizationName', u'Python Software Foundation'),),
                   (('organizationalUnitName', u'SSL'),),
                   (('commonName', u'somemachine.python.org'),))}

   If the ``binary_form`` parameter is :const:`True`, and a certificate was
   provided, this method returns the DER-encoded form of the entire certificate
   as a sequence of bytes, or :const:`None` if the peer did not provide a
   certificate.  This return value is independent of validation; if validation
   was required (:const:`CERT_OPTIONAL` or :const:`CERT_REQUIRED`), it will have
   been validated, but if :const:`CERT_NONE` was used to establish the
   connection, the certificate, if present, will not have been validated.

   ``binary_form`` 引数が :const:`True` だった場合、証明書が渡されていれば
   このメソッドはDERエンコードされた証明書全体をバイト列として返し、
   接続先が証明書を提示しなかった場合は :const:`None` を返します。
   この戻り値は認証とは独立しています。認証が要求されていた場合 (:const:`CERT_OPTIONAL`
   か :const:`CERT_REQUIRED`) その証明書は認証されますが、 :const:`CERT_NONE`
   が接続時に利用された場合、証明書があったとしても、それは認証されません。

.. method:: SSLSocket.cipher()

   Returns a three-value tuple containing the name of the cipher being used, the
   version of the SSL protocol that defines its use, and the number of secret
   bits being used.  If no connection has been established, returns ``None``.

   利用されている暗号の名前、その暗号の利用を定義しているSSLプロトコルのバージョン、
   利用されている鍵のbit長の3つの値を含むタプルを返します。
   もし接続が確立されていない場合、 ``None`` を返します。

.. method:: SSLSocket.do_handshake()

   Perform a TLS/SSL handshake.  If this is used with a non-blocking socket, it
   may raise :exc:`SSLError` with an ``arg[0]`` of :const:`SSL_ERROR_WANT_READ`
   or :const:`SSL_ERROR_WANT_WRITE`, in which case it must be called again until
   it completes successfully.  For example, to simulate the behavior of a
   blocking socket, one might write.

   TLS/SSL ハンドシェイクを実施します。
   ノンブロッキングソケットで利用された場合、ハンドシェイクが完了するまでは
   :exc:`SSLError` の ``arg[0]`` に :const:`SSL_ERROR_WANT_READ` か
   :const:`SSL_ERROR_WANT_WRITE` が設定された例外が発生し、このメソッドを繰り返し
   実行しなければなりません。
   例えば、ブロッキングソケットを真似する場合は次のようになります。 ::

        while True:
            try:
                s.do_handshake()
                break
            except ssl.SSLError, err:
                if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                    select.select([s], [], [])
                elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                    select.select([], [s], [])
                else:
                    raise

.. method:: SSLSocket.unwrap()

   Performs the SSL shutdown handshake, which removes the TLS layer from the
   underlying socket, and returns the underlying socket object.  This can be
   used to go from encrypted operation over a connection to unencrypted.  The
   socket instance returned should always be used for further communication with
   the other side of the connection, rather than the original socket instance
   (which may not function properly after the unwrap).

   SSLシャットダウンハンドシェイクを実行します。
   これは下位レイヤーのソケットからTLSレイヤーを取り除き、下位レイヤーの
   ソケットオブジェクトを返します。
   これは暗号化されたオペレーションから暗号化されていない接続に移行するときに利用されます。
   以降の通信には、このメソッドが返したソケットインスタンスを利用するべきです。
   元のソケットインスタンスは unwrap 後に正しく機能しないかもしれません。

.. index:: single: certificates

.. index:: single: X509 certificate

.. _ssl-certificates:

Certificates

証明書
-------

Certificates in general are part of a public-key / private-key system.  In this
system, each *principal*, (which may be a machine, or a person, or an
organization) is assigned a unique two-part encryption key.  One part of the key
is public, and is called the *public key*; the other part is kept secret, and is
called the *private key*.  The two parts are related, in that if you encrypt a
message with one of the parts, you can decrypt it with the other part, and
**only** with the other part.

証明書を大まかに言うと、公開鍵/秘密鍵システムの一種です。
このシステムでは、各 *principal* (これは マシン、人、組織などです) は、
ユニークな2部の暗号鍵を割り当てられます。1部は公開され、 *公開鍵(public key)*
と呼ばれます。もう一方は秘密にされ、 *秘密鍵(private key)* と呼ばれます。
2つの鍵は関連しており、片方の鍵で暗号化したメッセージは、もう片方の鍵 **のみ**
で復号できます。

A certificate contains information about two principals.  It contains the name
of a *subject*, and the subject's public key.  It also contains a statement by a
second principal, the *issuer*, that the subject is who he claims to be, and
that this is indeed the subject's public key.  The issuer's statement is signed
with the issuer's private key, which only the issuer knows.  However, anyone can
verify the issuer's statement by finding the issuer's public key, decrypting the
statement with it, and comparing it to the other information in the certificate.
The certificate also contains information about the time period over which it is
valid.  This is expressed as two fields, called "notBefore" and "notAfter".

証明書は2つの principal の情報を含んでいます。
証明書は *subject* 名とその公開鍵を含んでいます。
また、もう一つの principal である *発行者(issuer)* からの、 subject が本人であることと、
その公開鍵が正しいことの宣言を含んでいます。
発行者からの宣言は、その発行者の秘密鍵で署名されています。発行者の秘密鍵は発行者しか
知りませんが、誰もがその発行者の公開鍵を利用して宣言を復号し、証明書内の別の情報と
比較することで認証することができます。
証明書はまた、その証明書が有効である期限に関する情報も含んでいます。
この期限は "notBefore" と "notAfter" と呼ばれる2つのフィールドで表現されています。

In the Python use of certificates, a client or server can use a certificate to
prove who they are.  The other side of a network connection can also be required
to produce a certificate, and that certificate can be validated to the
satisfaction of the client or server that requires such validation.  The
connection attempt can be set to raise an exception if the validation fails.
Validation is done automatically, by the underlying OpenSSL framework; the
application need not concern itself with its mechanics.  But the application
does usually need to provide sets of certificates to allow this process to take
place.

Python において証明書を利用する場合、クライアントもサーバーも自分を証明するために
証明書を利用することができます。ネットワーク接続の相手側に証明書の提示を要求する事ができ、
そのクライアントやサーバーが認証を必要とするならその証明書を認証することができます。
認証が失敗した場合、接続は例外を発生させます。
認証は下位層のOpenSSLフレームワークが自動的に行います。
アプリケーションは認証機構について意識する必要はありません。
しかし、アプリケーションは認証プロセスのために幾つかの証明書を提供する必要があるかもしれません。

Python uses files to contain certificates.  They should be formatted as "PEM"
(see :rfc:`1422`), which is a base-64 encoded form wrapped with a header line
and a footer line:

Python は証明書を格納したファイルを利用します。そのファイルは "PEM" (:rfc:`1422` 参照)
フォーマットという、ヘッダー行とフッター行の間にbase-64エンコードされた形をとっている
必要があります。 ::

      -----BEGIN CERTIFICATE-----
      ... (certificate in base64 PEM encoding) ...
      -----END CERTIFICATE-----

The Python files which contain certificates can contain a sequence of
certificates, sometimes called a *certificate chain*.  This chain should start
with the specific certificate for the principal who "is" the client or server,
and then the certificate for the issuer of that certificate, and then the
certificate for the issuer of *that* certificate, and so on up the chain till
you get to a certificate which is *self-signed*, that is, a certificate which
has the same subject and issuer, sometimes called a *root certificate*.  The
certificates should just be concatenated together in the certificate file.  For
example, suppose we had a three certificate chain, from our server certificate
to the certificate of the certification authority that signed our server
certificate, to the root certificate of the agency which issued the
certification authority's certificate:

Pythonが利用する証明書を格納したファイルは、ときには *証明書チェイン(certificate chain)*
と呼ばれる証明書のシーケンスを格納します。
このチェインは、まずクライアントやサーバー自体の principal の証明書で始まらなければなりません。
それ以降に続く証明書は、手前の証明書の発行者(issuer)の証明書になり、最後にsubject と発行者が
同じ *自己署名(self-signed)* 証明書で終わります。この最後の証明書は *ルート証明書(root certificate*
と呼ばれます。
これらの証明書チェインは1つの証明書ファイルに結合されなければなりません。
例えば、3つの証明書からなる証明書チェインがあるとします。私たちのサーバーの証明書から、
私たちのサーバーに署名した認証局の証明書、そして認証局の証明書を発行した機関のルート証明書です。 ::

      -----BEGIN CERTIFICATE-----
      ... (certificate for your server)...
      -----END CERTIFICATE-----
      -----BEGIN CERTIFICATE-----
      ... (the certificate for the CA)...
      -----END CERTIFICATE-----
      -----BEGIN CERTIFICATE-----
      ... (the root certificate for the CA's issuer)...
      -----END CERTIFICATE-----

If you are going to require validation of the other side of the connection's
certificate, you need to provide a "CA certs" file, filled with the certificate
chains for each issuer you are willing to trust.  Again, this file just contains
these chains concatenated together.  For validation, Python will use the first
chain it finds in the file which matches.

もし相手から送られてきた証明書の認証をしたい場合、信頼している各発行者の
証明書チェインが入った "CA certs" ファイルを提供する必要があります。
繰り返しますが、このファイルは単純に、各チェインを結合しただけのものです。
認証のために、Pythonはそのファイルの中の最初にマッチしたチェインを利用します。

Some "standard" root certificates are available from various certification
authorities: `CACert.org <http://www.cacert.org/index.php?id=3>`_, `Thawte
<http://www.thawte.com/roots/>`_, `Verisign
<http://www.verisign.com/support/roots.html>`_, `Positive SSL
<http://www.PositiveSSL.com/ssl-certificate-support/cert_installation/UTN-USERFirst-Hardware.crt>`_
(used by python.org), `Equifax and GeoTrust
<http://www.geotrust.com/resources/root_certificates/index.asp>`_.

幾つかの "standard" ルート証明書が、幾つかの認証機関から入手できます:
`CACert.org <http://www.cacert.org/index.php?id=3>`_, `Thawte
<http://www.thawte.com/roots/>`_, `Verisign
<http://www.verisign.com/support/roots.html>`_, `Positive SSL
<http://www.PositiveSSL.com/ssl-certificate-support/cert_installation/UTN-USERFirst-Hardware.crt>`_
(python.org が利用しています), `Equifax and GeoTrust
<http://www.geotrust.com/resources/root_certificates/index.asp>`_.

In general, if you are using SSL3 or TLS1, you don't need to put the full chain
in your "CA certs" file; you only need the root certificates, and the remote
peer is supposed to furnish the other certificates necessary to chain from its
certificate to a root certificate.  See :rfc:`4158` for more discussion of the
way in which certification chains can be built.

一般的に、 SSL3 か TLS1 を利用している場合、"CA certs" ファイルに全てのチェインを
保存する必要はありません。接続先はそれ自身の証明書からルート証明書までの証明書チェインを
送ってくるはずで、"CA certs" にはルート証明書だけあれば充分なはずです。
証明書チェインを組み立てる方法についてのより詳しい情報は、 :rfc:`4158` を参照してください。

If you are going to create a server that provides SSL-encrypted connection
services, you will need to acquire a certificate for that service.  There are
many ways of acquiring appropriate certificates, such as buying one from a
certification authority.  Another common practice is to generate a self-signed
certificate.  The simplest way to do this is with the OpenSSL package, using
something like the following:

SSL暗号化接続サービスを提供するサーバーを建てる場合、適切な証明書を取得するには、
認証局から買うなどの幾つかの方法があります。また、自己署名証明書を作るケースもあります。
OpenSSLを使って自己署名証明書を作るには、次のようにします。 ::

  % openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
  Generating a 1024 bit RSA private key
  .......++++++
  .............................++++++
  writing new private key to 'cert.pem'
  -----
  You are about to be asked to enter information that will be incorporated
  into your certificate request.
  What you are about to enter is what is called a Distinguished Name or a DN.
  There are quite a few fields but you can leave some blank
  For some fields there will be a default value,
  If you enter '.', the field will be left blank.
  -----
  Country Name (2 letter code) [AU]:US
  State or Province Name (full name) [Some-State]:MyState
  Locality Name (eg, city) []:Some City
  Organization Name (eg, company) [Internet Widgits Pty Ltd]:My Organization, Inc.
  Organizational Unit Name (eg, section) []:My Group
  Common Name (eg, YOUR name) []:myserver.mygroup.myorganization.com
  Email Address []:ops@myserver.mygroup.myorganization.com
  %

The disadvantage of a self-signed certificate is that it is its own root
certificate, and no one else will have it in their cache of known (and trusted)
root certificates.

自己署名証明書の欠点は、それ自身がルート証明書であり、他の人はその証明書を持っていない
(そして信頼しない)ことです。

Examples

例
----

Testing for SSL support

SSLサポートをテストする
^^^^^^^^^^^^^^^^^^^^^^^

To test for the presence of SSL support in a Python installation, user code
should use the following idiom:

インストールされているPythonがSSLをサポートしているかどうかをテストするために、
ユーザーコードは次のイディオムを利用することができます。 ::

   try:
      import ssl
   except ImportError:
      pass
   else:
      [ do something that requires SSL support ]

Client-side operation

クライアントサイドの処理
^^^^^^^^^^^^^^^^^^^^^^^^^

This example connects to an SSL server, prints the server's address and
certificate, sends some bytes, and reads part of the response:

次の例では、SSLサーバーに接続し、サーバーのアドレスと証明書を表示し、
数バイト送信し、レスポンスの一部を読み込みます。 ::

   import socket, ssl, pprint

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   # サーバーからの証明書を要求する
   ssl_sock = ssl.wrap_socket(s,
                              ca_certs="/etc/ca_certs_file",
                              cert_reqs=ssl.CERT_REQUIRED)

   ssl_sock.connect(('www.verisign.com', 443))

   print repr(ssl_sock.getpeername())
   print ssl_sock.cipher()
   print pprint.pformat(ssl_sock.getpeercert())

   # シンプルなHTTPリクエストを送信する。 -- 実際のコードではhttplibを利用してください。
   ssl_sock.write("""GET / HTTP/1.0\r
   Host: www.verisign.com\r\n\r\n""")

   # 1チャンクのデータを読む。
   # サーバーから返されたデータの全てを読み込むとは限らない。
   data = ssl_sock.read()

   # SSLSocketを閉じると下位レイヤーのソケットも閉じられることに注目してください。
   ssl_sock.close()

As of September 6, 2007, the certificate printed by this program looked like
this:

2007年9月時点で、このプログラムによって表示される証明書は次のようになります。 ::

      {'notAfter': 'May  8 23:59:59 2009 GMT',
       'subject': ((('serialNumber', u'2497886'),),
                   (('1.3.6.1.4.1.311.60.2.1.3', u'US'),),
                   (('1.3.6.1.4.1.311.60.2.1.2', u'Delaware'),),
                   (('countryName', u'US'),),
                   (('postalCode', u'94043'),),
                   (('stateOrProvinceName', u'California'),),
                   (('localityName', u'Mountain View'),),
                   (('streetAddress', u'487 East Middlefield Road'),),
                   (('organizationName', u'VeriSign, Inc.'),),
                   (('organizationalUnitName',
                     u'Production Security Services'),),
                   (('organizationalUnitName',
                     u'Terms of use at www.verisign.com/rpa (c)06'),),
                   (('commonName', u'www.verisign.com'),))}

which is a fairly poorly-formed ``subject`` field.

これは不完全な形の ``subject`` フィールドです。

Server-side operation

サーバーサイドの処理
^^^^^^^^^^^^^^^^^^^^^

For server operation, typically you'd need to have a server certificate, and
private key, each in a file.  You'd open a socket, bind it to a port, call
:meth:`listen` on it, then start waiting for clients to connect:

サーバーサイドの処理では、通常、サーバー証明書と秘密鍵がそれぞれファイルに格納された形で必要です。
ソケットを開き、ポートにバインドし、そのソケットの :meth:`listen` を呼び、クライアントからの
接続を待ちます。 ::

   import socket, ssl

   bindsocket = socket.socket()
   bindsocket.bind(('myaddr.mydomain.com', 10023))
   bindsocket.listen(5)

When one did, you'd call :meth:`accept` on the socket to get the new socket from
the other end, and use :func:`wrap_socket` to create a server-side SSL context
for it:

誰かが接続してきた場合、 :meth:`accept` を呼んで新しいソケットを作成し、
:func:`wrap_socket` を利用してサーバーサイドSSLコンテキストを生成します。 ::

   while True:
      newsocket, fromaddr = bindsocket.accept()
      connstream = ssl.wrap_socket(newsocket,
                                   server_side=True,
                                   certfile="mycertfile",
                                   keyfile="mykeyfile",
                                   ssl_version=ssl.PROTOCOL_TLSv1)
      deal_with_client(connstream)

Then you'd read data from the ``connstream`` and do something with it till you
are finished with the client (or the client is finished with you):

そして、 ``connstream`` からデータを読み、クライアントと切断する(あるいはクライアントが
切断してくる)まで何か処理をします。 ::

   def deal_with_client(connstream):

      data = connstream.read()
      # 空のデータは、クライアントが接続を切ってきた事を意味します。
      while data:
         if not do_something(connstream, data):
            # 処理が終了したときに do_something が False
            # を返すと仮定します。
            break
         data = connstream.read()
      # クライアントを切断します。
      connstream.close()

And go back to listening for new client connections.

そして新しいクライアント接続のために listen に戻ります。

.. seealso::

   Class :class:`socket.socket`
            下位レイヤーの :mod:`socket` クラスのドキュメント

   `Introducing SSL and Certificates using OpenSSL <http://old.pseudonym.org/ssl/wwwj-index.html>`_
       Frederick J. Hirsch

   `RFC 1422: Privacy Enhancement for Internet Electronic Mail: Part II: Certificate-Based Key Management <http://www.ietf.org/rfc/rfc1422>`_
       Steve Kent

   `RFC 1750: Randomness Recommendations for Security <http://www.ietf.org/rfc/rfc1750>`_
       D. Eastlake et. al.

   `RFC 3280: Internet X.509 Public Key Infrastructure Certificate and CRL Profile <http://www.ietf.org/rfc/rfc3280>`_
       Housley et. al.
