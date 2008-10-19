
:mod:`socket` --- 低レベルネットワークインターフェース
====================================

.. module:: socket
   :synopsis: 低レベルネットワークインターフェース。


このモジュールは、PythonでBSD *ソケット* インターフェースを利用する ために使用します。最近のUnixシステム、Windows, MacOS,
BeOS, OS/2な ど、多くのプラットフォームで利用可能です。

.. note::

   いくつかの振る舞いはプラットフォームに依存します。これはオペレーティングシステム のソケットAPIを呼び出しているためです。

C言語によるソケットプログラミングの基礎については、以下の資料を参照して ください。 An Introductory 4.3BSD Interprocess
Communication Tutorial (Stuart Sechrest), An Advanced 4.3BSD Interprocess
Communication Tutorial (Samuel J. Leffler他), UNIX Programmer's Manual,
Supplementary Documents 1(PS1:7章 PS1:8章)。ソケットの詳細については、
各プラットフォームのソケット関連システムコールに関するドキュメント(Unix では
マニュアルページ、WindowsではWinSock(またはWinSock2)仕様書)も参照し てください。IPv6対応のAPIについては、:rfc:`2553`
Basic Socket Interface Extensions for IPv6を参照してくださ い。

.. index:: object: socket

Pythonインターフェースは、Unixのソケット用システムコールとライブラリ を、そのままPythonのオブジェクト指向スタイルに変換したものです。各種ソケ
ット関連のシステムコールは、:func:`socket`関数で生成する :dfn:`ソケット オブジェクト`のメソッドとして実装されてい
ます。メソッドのパラメータはCのインターフェースよりも多少高水準で、例え
ば:meth:`read`や:meth:`write`メソッドではファイルオブジェクトと同
様、受信時のバッファ確保や送信時の出力サイズなどは自動的に処理されます。

ソケットのアドレスは以下のように指定します:単一の文字列は、 :const:`AF_UNIX`アドレスファミリを示します。``(host,
port)``のペアは:const:`AF_INET`アドレスファミリを示し、*host*
は``'daring.cwi.nl'``のようなインターネットドメイン形式または
``'100.50.200.5'``のようなIPv4アドレスを文字列で、*port*はポート
番号を整数で指定します。:const:`AF_INET6`アドレスファミリは ``(host, port, flowinfo, scopeid)``の長さ4の
タプルで示し、*flowinfo*と*scopeid*にはそれぞれCの :const:`struct
sockaddr_in6`における``sin6_flowinfo``と
``sin6_scope_id``の値を指定します。後方互換性のため、:mod:`socket`
モジュールのメソッドでは``sin6_flowinfo``と``sin6_scope_id``を省略
する事ができますが、*scopeid*を省略するとスコープを持ったIPv6アドレ スの処理で問題が発生する場合があります。現在サポートされているアドレスフ
ァミリは以上です。ソケットオブジェクトで利用する事のできるアドレス形式 は、ソケットオブジェクトの作成時に指定したアドレスファミリで決まります。

IPv4アドレスのホストアドレスが空文字列の場合、:const:`INADDR_ANY`とし て処理されます。また、``'<broadcast>'``の場合は
:const:`INADDR_BROADCAST`として処理されます。IPv6では後方互換性のため
この機能は用意されていませんので、IPv6をサポートするPythonプログラムでは 利用しないで下さい。

IPv4/v6ソケットの*host*部にホスト名を指定すると、処理結果が一定では
ない場合があります。これはPythonはDNSから取得したアドレスのうち最初のア
ドレスを使用するので、DNSの処理やホストの設定によって異なるIPv4/6アドレ スを取得する場合があるためです。常に同じ結果が必要であれば、*host*に
数値のアドレスを指定してください。

.. versionadded:: 2.5
   AF_NETLINK ソケットが ``pid, groups`` のペアで表現されます.

エラー時には例外が発生します。引数型のエラーやメモリ不足の場合には通常の 例外が発生し、ソケットやアドレス関連のエラーの場合は
:exc:`socket.error`が発生します。

:meth:`setblocking`メソッドで、非ブロッキングモードを使用することがで
きます。また、より汎用的に:meth:`settimeout`メソッドでタイムアウトを 指定する事ができます。

:mod:`socket`モジュールでは、以下の定数と関数を提供しています。


.. exception:: error

   .. index:: module: errno

   この例外は、ソケット関連のエラーが発生した場合に送出されます。例外の値は 障害の内容を示す文字列か、または:exc:`os.error`と同様な
   ``(errno, string)``のペアとなります。オペレーティングシス テムで定義されているエラーコードについては:mod:`errno`
   を参照してください。


.. exception:: herror

   この例外は、C APIの:func:`gethostbyname_ex`や
   :func:`gethostbyaddr`などで、*h_errno*のようなアドレス関連のエ ラーが発生した場合に送出されます。

   例外の値は``(h_errno, string)``のペアで、ライブラリの呼び
   出し結果を返します。*string*はC関数:cfunc:`hstrerror`で取得し た、*h_errno*の意味を示す文字列です。


.. exception:: gaierror

   この例外は:func:`getaddrinfo`と:func:`getnameinfo`でアドレス関 連のエラーが発生した場合に送出されます。

   例外の値は``(error, string)``のペアで、ライブラリの呼び出
   し結果を返します。*string*はC関数:cfunc:`gai_strerror`で取得し た、*h_errno*の意味を示す文字列です。
   *error*の値は、このモジュールで定義される :const:`EAI_\*` 定数の何れか となります。


.. exception:: timeout

   この例外は、あらかじめ :meth:`settimeout` を呼び出してタイムアウトを 有効にしてあるソケットでタイムアウトが生じた際に送出されます。
   例外に付属する値は文字列で、その内容は現状では常に "timed out" となります。

   .. versionadded:: 2.3


.. data:: AF_UNIX
          AF_INET
          AF_INET6

   アドレス（およびプロトコル）ファミリを示す定数で、:func:`socket`の
   最初の引数に指定することができます。:const:`AF_UNIX`ファミリをサポート
   しないプラットフォームでは、:const:`AF_UNIX`は未定義となります。


.. data:: SOCK_STREAM
          SOCK_DGRAM
          SOCK_RAW
          SOCK_RDM
          SOCK_SEQPACKET

   ソケットタイプを示す定数で、:func:`socket`の2番目の引数に指定するこ とができます。(ほとんどの場合、:const:`SOCK_STREAM`と
   :const:`SOCK_DGRAM`以外は必要ありません。)


.. data:: SO_*
          SOMAXCONN
          MSG_*
          SOL_*
          IPPROTO_*
          IPPORT_*
          INADDR_*
          IP_*
          IPV6_*
          EAI_*
          AI_*
          NI_*
          TCP_*

   Unixのソケット・IPプロトコルのドキュメントで定義されている各種定数。
   ソケットオブジェクトの:meth:`setsockopt`や:meth:`getsockopt`で使用
   します。ほとんどのシンボルはUnixのヘッダファイルに従っています。一部 のシンボルには、デフォルト値を定義してあります。


.. data:: has_ipv6

   現在のプラットフォームでIPv6がサポートされているか否かを示す真偽値。

   .. versionadded:: 2.3


.. function:: getaddrinfo(host, port[, family[, socktype[, proto[, flags]]]])

   *host*/*port* 引数の指すアドレス情報を解決して、 ソケット操作に必要な全ての引数が入った 5 要素のタプルを返します。
   *host*はドメイン名、IPv4/v6アドレスの文字列、または``None`` です。*port* は``'http'``のようなサービス名文字列、ポート番号
   を表す数値、または``None`` です。

   これ以外の引数は省略可能で、指定する場合には数値でなければなりません。 *host*と*port* に空文字列か``None`` を指定すると C APIに
   ``NULL``を渡せます。 :func:`getattrinfo` 関数は以下の構造をとる 5 要素のタプルを返します:

   ``(family, socktype, proto, canonname, sockaddr)``

   *family*・*socktype*・*proto*は、:func:`socket`関数を呼
   び出す際に指定する値と同じ整数です。*canonname*は*host*の規準名
   を示す文字列です。:const:`AI_CANONNAME`を指定した場合、数値によるIPv4/
   v6アドレスを返します。*sockaddr*は、ソケットアドレスを上述の形式で表
   すタプルです。この関数の使い方については、:mod:`httplib`モジュール などのソースを参考にしてください。

   .. versionadded:: 2.2


.. function:: getfqdn([name])

   *name*の完全修飾ドメイン名を返します。*name*が空または省略された 場合、ローカルホストを指定したとみなします。完全修飾ドメイン名の取得には
   まず:func:`gethostbyaddr`でチェックし、次に可能であればエイリアスを 調べ、名前にピリオドを含む最初の名前を値として返します。完全修飾ドメイ
   ン名を取得できない場合、:func:`gethostname`で返されるホスト名を返します。

   .. versionadded:: 2.0


.. function:: gethostbyname(hostname)

   ホスト名を``'100.50.200.5'``のようなIPv4形式のアドレスに変換します。
   ホスト名としてIPv4アドレスを指定した場合、その値は変換せずにそのまま返り ます。:func:`gethostbyname`
   APIへのより完全なインターフェースが必要 であれば、:func:`gethostbyname_ex`を参照してください。
   :func:`gethostbyname`は、IPv6名前解決をサポートしていません。IPv4/
   v6のデュアルスタックをサポートする場合は:func:`getaddrinfo`を使用し ます。


.. function:: gethostbyname_ex(hostname)

   ホスト名から、IPv4形式の各種アドレス情報を取得します。戻り値は ``(hostname, aliaslist,
   ipaddrlist)``のタプルで、*hostname*は *ip_address*で指定したホストの正式名、*aliaslist*は同じアドレス
   の別名のリスト(空の場合もある)、*ipaddrlist*は同じホスト上の同一イ ンターフェースのIPv4アドレスのリスト(ほとんどの場合は単一のアドレスのみ)
   を示します。:func:`gethostbyname`は、IPv6名前解決をサポートしていま せん。IPv4/v6のデュアルスタックをサポートする場合は
   :func:`getaddrinfo`を使用します。


.. function:: gethostname()

   Pythonインタープリタを現在実行中のマシンのホスト名を示す文字列を取得しま す。実行中マシンのIPアドレスが必要であれば、
   ``gethostbyname(gethostname())``を使用してください。この処理は実行中
   ホストのアドレス-ホスト名変換が可能であることを前提としていますが、常に 変換可能であるとは限りません。注意:
   :func:`gethostname`は完全修飾ド メイン名を返すとは限りません。完全修飾ドメイン名が必要であれば、
   ``gethostbyaddr(gethostname())``としてください(下記参照)。


.. function:: gethostbyaddr(ip_address)

   ``(hostname, aliaslist, ipaddrlist)``のタプルを返
   し、*hostname*は*ip_address*で指定したホストの正式名、 ``aliaslist``は同じアドレスの別名のリスト(空の場合もある)、
   ``ipaddrlist``は同じホスト上の同一インターフェースのIPv4アドレスのリ
   スト(ほとんどの場合は単一のアドレスのみ)を示します。完全修飾ドメイン名が 必要であれば、:func:`getfqdn`を使用してください。
   :func:`gethostbyaddr`は、IPv4/IPv6の両方をサポートしています。


.. function:: getnameinfo(sockaddr, flags)

   ソケットアドレス*sockaddr*から、``(host, port)``のタ プルを取得します。*flags*の設定に従い、*host*は完全修飾ドメイン
   名または数値形式アドレスとなります。同様に、*port*は文字列のポート名 または数値のポート番号となります。

   .. versionadded:: 2.2


.. function:: getprotobyname(protocolname)

   ``'icmp'``のようなインターネットプロトコル名を、:func:`socket`の
   第三引数として指定する事ができる定数に変換します。これは主にソケットを"
   raw"モード(:const:`SOCK_RAW`)でオープンする場合には必要ですが、通常の
   ソケットモードでは第三引数に0を指定するか省略すれば正しいプロトコルが自 動的に選択されます。


.. function:: getservbyname(servicename[, protocolname])

   インターネットサービス名とプロトコルから、そのサービスのポート番号を取得 します。省略可能なプロトコル名として、``'tcp'``か``'udp'``のどちら
   かを指定することができます。指定がなければどちらのプロトコルにもマッチ します。


.. function:: getservbyport(port[, protocolname])

   インターネットポート番号とプロトコル名から、サービス名を取得します。 省略可能なプロトコル名として、``'tcp'``か``'udp'``のどちら
   かを指定することができます。指定がなければどちらのプロトコルにもマッチ します。


.. function:: socket([family[, type[, proto]]])

   アドレスファミリ、ソケットタイプ、プロトコル番号を指定してソケットを作成 します。アドレスファミリには:const:`AF_INET`\
   (デフォルト値)・:const:`AF_INET6`・ :const:`AF_UNIX`を指定することができます。ソケットタイプには
   :const:`SOCK_STREAM`\ (デフォルト値)・:const:`SOCK_DGRAM`・または他の
   ``SOCK_``定数の何れかを指定します。プロトコル番号は通常省略するか、 または0を指定します。


.. function:: ssl(sock[, keyfile, certfile])

   ソケット*sock*によるSSL接続を初期化します。*keyfile*には、PEMフ
   ォーマットのプライベートキーファイル名を指定します。*certfile*には、 PEMフォーマットの認証チェーンファイル名を指定します。処理が成功すると、
   新しい:class:`SSLObject`が返ります。

   .. warning::

      証明書の認証は全く行いません。


.. function:: socketpair([family[, type[, proto]]])

   指定されたアドレスファミリ、ソケットタイプ、プロトコル番号から、 接続されたソケットのペアを作成します。  アドレスファミリ、ソケットタイプ、プロトコル番号は
   :func:`socket`関 数と同様に指定します。 デフォルトのアドレスファミリは、プラットフォームで定義されていれば
   :const:`AF_UNIX`、そうでなければ:const:`AF_INET`が使われます。

   利用可能: Unix.

   .. versionadded:: 2.4


.. function:: fromfd(fd, family, type[, proto])

   ファイルディスクリプタ (ファイルオブジェクトの:meth:`fileno`で返る 整数) *fd* を複製して、ソケットオブジェクトを構築します。アドレス
   ファミリとプロトコル番号は:func:`socket`と同様に指定します。 ファイルディスクリプタ
   はソケットを指していなければなりませんが、実際にソケットであるかどうかの チェックは行っていません。このため、ソケット以外のファイルディスクリプタ
   を指定するとその後の処理が失敗する場合があります。この関数が必要な事はあ まりありませんが、Unixのinetデーモンのようにソケットを標準入力や標準
   出力として使用するプログラムで使われます。この関数で使用するソケットは、 ブロッキングモードと想定しています。 利用可能:Unix


.. function:: ntohl(x)

   32ビット整数のバイトオーダを、ネットワークバイトオーダからホストバイト オーダに変換します。ホストバイトオーダとネットワークバイトオーダが一致す
   るマシンでは、この関数は何もしません。それ以外の場合は4バイトのスワップ を行います。


.. function:: ntohs(x)

   16ビット整数のバイトオーダを、ネットワークバイトオーダからホストバイト オーダに変換します。ホストバイトオーダとネットワークバイトオーダが一致す
   るマシンでは、この関数は何もしません。それ以外の場合は2バイトのスワップ を行います。


.. function:: htonl(x)

   32ビット整数のバイトオーダを、ホストバイトオーダからネットワークバイト オーダに変換します。ホストバイトオーダとネットワークバイトオーダが一致す
   るマシンでは、この関数は何もしません。それ以外の場合は4バイトのスワップ を行います。


.. function:: htons(x)

   16ビット整数のバイトオーダを、ホストバイトオーダからネットワークバイト オーダに変換します。ホストバイトオーダとネットワークバイトオーダが一致す
   るマシンでは、この関数は何もしません。それ以外の場合は2バイトのスワップ を行います。


.. function:: inet_aton(ip_string)

   ドット記法によるIPv4アドレス(``'123.45.67.89'``など)を32ビットにパッ
   クしたバイナリ形式に変換し、長さ4の文字列として返します。この関数が返す 値は、標準Cライブラリの:ctype:`struct
   in_addr`型を使用する関数に渡す事がで きます。

   IPv4アドレス文字列が不正であれば、:exc:`socket.error`が発生します。 このチェックは、この関数で使用しているCの実装
   :cfunc:`inet_aton`で 行われます。

   :func:`inet_aton`は、IPv6をサポートしません。IPv4/v6のデュアルスタ
   ックをサポートする場合は:func:`getnameinfo`を使用します。


.. function:: inet_ntoa(packed_ip)

   32ビットにパックしたバイナリ形式のIPv4アドレスを、ドット記法による文字列
   (``'123.45.67.89'``など)に変換します。この関数が返す値は、標準Cライブ ラリの:ctype:`struct
   in_addr`型を使用する関数に渡す事ができます。

   この関数に渡す文字列の長さが4バイト以外であれば、 :exc:`socket.error`が発生します。
   :func:`inet_ntoa`は、IPv6をサポートしません。IPv4/v6のデュアルスタ
   ックをサポートする場合は:func:`getnameinfo`を使用します。


.. function:: inet_pton(address_family, ip_string)

   IPアドレスを、アドレスファミリ固有の文字列からパックしたバイナリ形式に変 換します。:func:`inet_pton`は、:ctype:`struct
   in_addr`型 (:func:`inet_aton`と同様)や:ctype:`struct in6_addr`を使用するライブ
   ラリやネットワークプロトコルを呼び出す際に使用することができます。

   現在サポートされている*address_family*は、:const:`AF_INET`と
   :const:`AF_INET6`です。*ip_string*に不正なIPアドレス文字列を指定す
   ると、:exc:`socket.error`が発生します。有効な*ip_string*は、
   *address_family*と:cfunc:`inet_pton`の実装によって異なります。

   利用可能: Unix (サポートしていないプラットフォームもあります)

   .. versionadded:: 2.3


.. function:: inet_ntop(address_family, packed_ip)

   パックしたIPアドレス(数文字の文字列)を、``'7.10.0.5'``や ``'5aef:2b::8'``などの標準的な、アドレスファミリ固有の文字列形式に変
   換します。:func:`inet_ntop`は(:func:`inet_ntoa`と同様に) :ctype:`struct
   in_addr`型や:ctype:`struct in6_addr`型のオブジェクトを返す ライブラリやネットワークプロトコル等で使用することができます。

   現在サポートされている*address_family*は、:const:`AF_INET`と
   :const:`AF_INET6`です。*packed_ip*の長さが指定したアドレスファミリ
   で適切な長さでなければ、:exc:`ValueError`が発生します。
   :func:`inet_ntop`でエラーとなると、:exc:`socket.error`が発生し ます。

   利用可能: Unix (サポートしていないプラットフォームもあります)

   .. versionadded:: 2.3


.. function:: getdefaulttimeout()

   新規に生成されたソケットオブジェクトの、デフォルトのタイムアウト値を浮動 小数点形式の秒数で返します。タイプアウトを使用しない場合には``None``
   を返します。最初にsocketモジュールがインポートされた時の初期値は ``None``です。

   .. versionadded:: 2.3


.. function:: setdefaulttimeout(timeout)

   新規に生成されたソケットオブジェクトの、デフォルトのタイムアウト値を浮動 小数点形式の秒数で指定します。タイムアウトを使用しない場合には
   ``None``を指定します。最初にsocketモジュールがインポートされた時の初 期値は``None``です。

   .. versionadded:: 2.3


.. data:: SocketType

   ソケットオブジェクトの型を示す型オブジェクト。``type(socket(...))``と 同じです。


.. seealso::

   Module :mod:`SocketServer`
      ネットワークサーバの開発を省力化するためのク ラス群。


.. _socket-objects:

socket オブジェクト
-------------

ソケットオブジェクトは以下のメソッドを持ちます。:meth:`makefile`以外 のメソッドは、Unixのソケット用システムコールに対応しています。


.. method:: socket.accept()

   接続を受け付けます。ソケットはアドレスにbind済みで、listen中である必要が あります。戻り値は``(conn,
   address)``のペアで、*conn* は接続を通じてデータの送受信を行うための*新しい*ソケットオブジェク
   ト、*address*は接続先でソケットにbindしているアドレスを示します。


.. method:: socket.bind(address)

   ソケットを*address*にbindします。bind済みのソケットを再バインドする
   事はできません。*address*のフォーマットはアドレスファミリによって異 なります(前述)。

   .. note::

      本来、このメソッドは単一のタプルのみを引数として受け付けますが、 以前は:const:`AF_INET`アドレスを示す二つの値を指定する事ができました。
      これは本来の仕様ではなく、Python 2.0以降では使用することはできません。


.. method:: socket.close()

   ソケットをクローズします。以降、このソケットでは全ての操作が失敗します。 リモート端点ではキューに溜まったデータがフラッシュされた後はそれ以上の
   データを受信しません。ソケットはガベージコレクション時に自動的にクローズ されます。


.. method:: socket.connect(address)

   *address*で示されるリモートソケットに接続します。*address*のフ ォーマットはアドレスファミリによって異なります(前述)。

   .. note::

      本来、このメソッドは単一のタプルのみを引数として受け付けますが、 以前は:const:`AF_INET`アドレスを示す二つの値を指定する事ができました。
      これは本来の仕様ではなく、Python 2.0以降では使用することはできません。


.. method:: socket.connect_ex(address)

   ``connect(address)``と同様ですが、C言語の:cfunc:`connect`
   関数の呼び出しでエラーが発生した場合には例外を送出せずにエラーを戻り値と して返します。(これ以外の、"host not
   found,"等のエラーの場合には例外が 発生します。)処理が正常に終了した場合には``0``を返し、エラー時には
   :cdata:`errno`の値を返します。この関数は、非同期接続をサポートする場合な どに使用することができます。

   .. note::

      本来、このメソッドは単一のタプルのみを引数として受け付けますが、 以前は:const:`AF_INET`アドレスを示す二つの値を指定する事ができました。
      これは本来の仕様ではなく、Python 2.0以降では使用することはできません。


.. method:: socket.fileno()

   ソケットのファイルディスクリプタを整数型で返します。ファイルディスクリプ タは、:func:`select.select`などで使用します。

   Windowsではこのメソッドで返された小整数をファイルディスクリプタを扱う箇 所(:func:`os.fdopen`など)で利用できません。 Unix
   にはこの制限はありません。


.. method:: socket.getpeername()

   ソケットが接続しているリモートアドレスを返します。この関数は、リモート IPv4/v6ソケットのポート番号を調べる場合などに使用します。*address*の
   フォーマットはアドレスファミリによって異なります(前述)。この関数をサポー トしていないシステムも存在します。


.. method:: socket.getsockname()

   ソケット自身のアドレスを返します。この関数は、IPv4/v6ソケットのポート番 号を調べる場合などに使用します。*address*のフォーマットはアドレスフ
   ァミリによって異なります(前述)。


.. method:: socket.getsockopt(level, optname[, buflen])

   .. index:: module: struct

   ソケットに指定されたオプションを返します(Unixのマニュアルページ
   :manpage:`getsockopt(2)`を参照)。:const:`SO_\*`等のシンボルは、このモジ
   ュールで定義しています。*buflen*を省略した場合、取得するオブションは 整数とみなし、整数型の値を戻り値とします。*buflen*を指定した場合、長
   さ*buflen*のバッファでオプションを受け取り、このバッファを文字列とし て返します。このバッファは、呼び出し元プログラムで:mod:`struct`
   モジュール等を利用して内容を読み取ることができま す。


.. method:: socket.listen(backlog)

   ソケットをListenし、接続を待ちます。引数*backlog*には接続キューの最
   大の長さ(1以上)を指定します。*backlog*の最大数はシステムに依存します (通常は5)。


.. method:: socket.makefile([mode[, bufsize]])

   .. index:: single: I/O control; buffering

   ソケットに関連付けられた:dfn:`ファイルオブジェクト`を返します(ファイルオ ブジェクトについては:ref:`bltin-file-
   objects`の"ファイルオブジェクト"を 参照)。ファイルオブジェクトはソケットを:cfunc:`dup`したファイルディ
   スクリプタを使用しており、ソケットオブジェクトとファイルオブジェクトは 別々にクローズしたりガベージコレクションで破棄したりする事ができます。ソ
   ケットはブロッキングモードでなければなりません。 オプション引数の*mode*と*bufsize*
   には、:func:`file`組み込み関数と同じ値を指定します。 :ref:`built-in-funcs`の"組み込み関数"を参照してください。


.. method:: socket.recv(bufsize[, flags])

   ソケットからデータを受信し、文字列として返します。受信する最大バイト数 は、*bufsize*で指定します。*flags*のデフォルト値は0です。値の意
   味についてはUnixマニュアルページの:manpage:`recv(2)`を参照してくださ い。

   .. note::

      ハードウェアおよびネットワークの現実に最大限マッチするように、 *bufsize*の値は比較的小さい2の累乗、たとえば 4096、にすべきです。


.. method:: socket.recvfrom(bufsize[, flags])

   ソケットからデータを受信し、結果をタプル``(string, address)``として返します。*string*は受信データの文字列で、
   *address*は送信元のアドレスを示します。オプション引数*flags*の意
   味は、上記:meth:`recv`と同じです。*address*のフォーマットはアドレ スファミリによって異なります(前述)。


.. method:: socket.send(string[, flags])

   ソケットにデータを送信します。ソケットはリモートソケットに接続済みでなけ ればなりません。オプション引数*flags*の意味は、上記:meth:`recv`と
   同じです。戻り値として、送信したバイト数を返します。アプリケーションで は、必ず戻り値をチェックし、全てのデータが送られた事を確認する必要があり
   ます。データの一部だけが送信された場合、アプリケーションで残りのデータを 再送信してください。


.. method:: socket.sendall(string[, flags])

   ソケットにデータを送信します。ソケットはリモートソケットに接続済みでなけ ればなりません。オプション引数*flags*の意味は、上記:meth:`recv`と
   同じです。:meth:`send`と異なり、このメソッドは*string*の全データ を送信するか、エラーが発生するまで処理を継続します。正常終了の場合は
   ``None``を返し、エラー発生時には例外が発生します。エラー発生時、送信 されたバイト数を調べる事はできません。


.. method:: socket.sendto(string[, flags], address)

   ソケットにデータを送信します。このメソッドでは接続先を*address*で指 定するので、接続済みではいけません。オプション引数*flags*の意味は、
   上記:meth:`recv`と同じです。戻り値として、送信したバイト数を返しま す。*address*のフォーマットはアドレスファミリによって異なります(前
   述)。


.. method:: socket.setblocking(flag)

   ソケットのブロッキング・非ブロッキングモードを指定します。*flag*が0 の場合は非ブロッキングモード、0以外の場合はブロッキングモードとなりま
   す。全てのソケットは、初期状態ではブロッキングモードです。非ブロッキング モードでは、:meth:`recv`メソッド呼び出し時に読み込みデータが無かった
   り:meth:`send`メソッド呼び出し時にデータを処理する事ができないような 場合に:exc:`error`例外が発生します。しかし、ブロッキングモードでは
   呼び出しは処理が行われるまでブロックされます。``s.setblocking(0)``は
   ``s.settimeout(0)``と、``s.setblocking(1)``は ``s.settimeout(None)``とそれぞれ同じ意味を持ちます。


.. method:: socket.settimeout(value)

   ソケットのブロッキング処理のタイムアウト値を指定します。*value*に は、正の浮動小数点で秒数を指定するか、もしくは``None``を指定します。
   浮動小数点値を指定した場合、操作が完了する前に*value*で指定した秒数
   が経過すると:exc:`timeout`が発生します。タイムアウト値に``None``を 指定すると、ソケットのタイムアウトを無効にします。
   ``s.settimeout(0.0)``は``s.setblocking(0)``と、
   ``s.settimeout(None)``は``s.setblocking(1)``とそれぞれ同じ意味を持 ちます。

   .. versionadded:: 2.3


.. method:: socket.gettimeout()

   ソケットに指定されたタイムアウト値を取得します。タイムアウト値が設定され ている場合には浮動小数点型で秒数が、設定されていなければ``None``が返
   ります。この値は、最後に呼び出された:meth:`setblocking`または :meth:`settimeout`によって設定されます。

   .. versionadded:: 2.3

ソケットのブロッキングとタイムアウトについて:ソケットオブジェクトのモー ドは、ブロッキング・非ブロッキング・タイムアウトの何れかとなります。初期
状態では常にブロッキングモードです。ブロッキングモードでは、処理が完了す るまでブロックされます。非ブロッキングモードでは、処理を行う事ができなけ
れば(不幸にもシステムによって異なる値の)エラーとなります。タイムアウト モードでは、ソケットに指定したタイムアウトまでに完了しなければ処理は失敗
となります。:meth:`setblocking`メソッドは、:meth:`settimeout`の省 略形式です。

内部的には、タイムアウトモードではソケットを非ブロッキングモードに設定し ます。ブロッキングとタイムアウトの設定は、ソケットと同じネットワーク端点
へ接続するファイルディスクリプタにも反映されます。この結果、 :meth:`makefile`で作成したファイルオブジェクトはブロッキングモードで
のみ使用することができます。これは非ブロッキングモードとタイムアウトモー ドでは、即座に完了しないファイル操作はエラーとなるためです。

註: :meth:`connect`はタイムアウト設定に従います。一般的に、
:meth:`settimeout`を:meth:`connect`の前に呼ぶことをおすすめします。


.. method:: socket.setsockopt(level, optname, value)

   .. index:: module: struct

   ソケットのオプションを設定します(Unixのマニュアルページ
   :manpage:`setsockopt(2)`を参照)。:const:`SO_\*`等のシンボルは、このモジ
   ュールで定義しています。``value``には、整数または文字列をバッファとし て指定する事ができます。文字列を指定する場合、文字列には適切なビットを設
   定するようにします。(:mod:`struct`モジュール を利用すれば、Cの構造体を文字列にエンコードする事ができます。)


.. method:: socket.shutdown(how)

   接続の片方向、または両方向を切断します。*how*が:const:`SHUT_RD`の場合、以降
   は受信を行えません。*how*が:const:`SHUT_WR`の場合、以降は送信を行えません。
   *how*が``SHUT_RDWR``の場合、以降は送受信を行えません。

:meth:`read`メソッドと:meth:`write`メソッドは存在しませんので注意
してください。代わりに*flags*を省略した:meth:`recv`と :meth:`send`を使うことができます。

ソケットオブジェクトには以下の :class:`socket` コンストラクタに 渡された値に対応した(読み出し専用)属性があります。


.. attribute:: socket.family

   ソケットファミリー。

   .. versionadded:: 2.5


.. attribute:: socket.type

   ソケットタイプ。

   .. versionadded:: 2.5


.. attribute:: socket.proto

   ソケットプロトコル。

   .. versionadded:: 2.5


.. _ssl-objects:

SSL オブジェクト
----------

SSLオブジェクトには、以下のメソッドがあります。


.. method:: SSL.write(s)

   文字列*s*をSSL接続で出力します。戻り値として、送信したバイト数を返し ます。


.. method:: SSL.read([n])

   SSL接続からデータを受信します。*n*を指定した場合は指定したバイト数の データを受信し、省略時はEOFまで読み込みます。戻り値として、受信したバイ
   ト列の文字列を返します。


.. method:: SSL.server()

   サーバの証明書を特定するための ASN.1 識別名(distinguished name)を含む文字列を
   返します。(下の例を見ると識別名がどう見えるものか判ります。)


.. method:: SSL.issuer()

   サーバの証明書の発行者を特定するための ASN.1 識別名(distinguished name)を含む文字列を返します。


.. _socket-example:

例
-

以下はTCP/IPプロトコルの簡単なサンプルとして、受信したデータをクライアン トにそのまま返送するサーバ(接続可能なクライアントは一件のみ)と、サーバに
接続するクライアントの例を示します。サーバでは、:func:`socket`・
:meth:`bind`・:meth:`listen`・:meth:`accept`を実行し(複数のクラ
イアントからの接続を受け付ける場合、:meth:`accept`を複数回呼び出しま
す)、クライアントでは:func:`socket`と:meth:`connect`だけを呼び出
しています。サーバでは:meth:`send`/:meth:`recv`メソッドはlisten中
のソケットで実行するのではなく、:meth:`accept`で取得したソケットに対 して実行している点にも注意してください。

次のクライアントとサーバは、IPv4のみをサポートしています。 ::

   # Echo server program
   import socket

   HOST = ''                 # Symbolic name meaning the local host
   PORT = 50007              # Arbitrary non-privileged port
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind((HOST, PORT))
   s.listen(1)
   conn, addr = s.accept()
   print 'Connected by', addr
   while 1:
       data = conn.recv(1024)
       if not data: break
       conn.send(data)
   conn.close()

::

   # Echo client program
   import socket

   HOST = 'daring.cwi.nl'    # The remote host
   PORT = 50007              # The same port as used by the server
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((HOST, PORT))
   s.send('Hello, world')
   data = s.recv(1024)
   s.close()
   print 'Received', repr(data)

The next two examples are identical to the above two, but support both IPv4 and
IPv6. The server side will listen to the first address family available (it
should listen to both instead). On most of IPv6-ready systems, IPv6 will take
precedence and the server may not accept IPv4 traffic. The client side will try
to connect to the all addresses returned as a result of the name resolution, and
sends traffic to the first one connected successfully.

次のサンプルは上記のサンプルとほとんど同じですが、IPv4とIPv6の両方をサ ポートしています。サーバでは、IPv4/v6の両方ではなく、利用可能な最初のア
ドレスファミリだけをlistenしています。ほとんどのIPv6対応システムではIPv6
が先に現れるため、サーバはIPv4には応答しません。クライアントでは名前解決 の結果として取得したアドレスに順次接続を試み、最初に接続に成功したソケッ
トにデータを送信しています。 ::

   # Echo server program
   import socket
   import sys

   HOST = ''                 # Symbolic name meaning the local host
   PORT = 50007              # Arbitrary non-privileged port
   s = None
   for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
       af, socktype, proto, canonname, sa = res
       try:
   	s = socket.socket(af, socktype, proto)
       except socket.error, msg:
   	s = None
   	continue
       try:
   	s.bind(sa)
   	s.listen(1)
       except socket.error, msg:
   	s.close()
   	s = None
   	continue
       break
   if s is None:
       print 'could not open socket'
       sys.exit(1)
   conn, addr = s.accept()
   print 'Connected by', addr
   while 1:
       data = conn.recv(1024)
       if not data: break
       conn.send(data)
   conn.close()

::

   # Echo client program
   import socket
   import sys

   HOST = 'daring.cwi.nl'    # The remote host
   PORT = 50007              # The same port as used by the server
   s = None
   for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
       af, socktype, proto, canonname, sa = res
       try:
   	s = socket.socket(af, socktype, proto)
       except socket.error, msg:
   	s = None
   	continue
       try:
   	s.connect(sa)
       except socket.error, msg:
   	s.close()
   	s = None
   	continue
       break
   if s is None:
       print 'could not open socket'
       sys.exit(1)
   s.send('Hello, world')
   data = s.recv(1024)
   s.close()
   print 'Received', repr(data)

次の例ではSSLサーバに接続し、サーバおよび発行者の識別名(distinguished name)
を表示し、いくらかのバイトを送り、レスポンスの一部を読みます::

   import socket

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect(('www.verisign.com', 443))

   ssl_sock = socket.ssl(s)

   print repr(ssl_sock.server())
   print repr(ssl_sock.issuer())

   # Set a simple HTTP request -- use httplib in actual code.
   ssl_sock.write("""GET / HTTP/1.0\r
   Host: www.verisign.com\r\n\r\n""")

   # Read a chunk of data.  Will not necessarily
   # read all the data returned by the server.
   data = ssl_sock.read()

   # Note that you need to close the underlying socket, not the SSL object.
   del ssl_sock
   s.close()

執筆時点で、このSSL実行例は次のような出力を表示しました (読み易いように改行は入れてあります)::

   '/C=US/ST=California/L=Mountain View/
    O=VeriSign, Inc./OU=Production Services/
    OU=Terms of use at www.verisign.com/rpa (c)00/
    CN=www.verisign.com'
   '/O=VeriSign Trust Network/OU=VeriSign, Inc./
    OU=VeriSign International Server CA - Class 3/
    OU=www.verisign.com/CPS Incorp.by Ref. LIABILITY LTD.(c)97 VeriSign'

