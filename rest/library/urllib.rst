
:mod:`urllib` --- URL による任意のリソースへのアクセス
======================================

.. module:: urllib
   :synopsis: URL による任意のネットワークリソースへのアクセス (socket が必要です)。


.. index::
   single: WWW
   single: World Wide Web
   single: URL

このモジュールはワールドワイドウェブ (World Wide Web) を介してデータを 取り寄せるための高レベルのインタフェースを提供する。特に、関数
:func:`urlopen` は組み込み関数 :func:`open` と同様に動作し、 ファイル名の代わりにファイルユニバーサルリソースロケータ (URL)
を 指定することができます。いくつかの制限はあります --- URL は読み出し 専用でしか開けませんし、seek 操作を行うことはできません。

このモジュールでは、以下の public な関数を定義します。


.. function:: urlopen(url[, data[, proxies]])

   URL で表されるネットワーク上のオブジェクトを読み込み用に開きます。 URL がスキーム識別子を持たないか、スキーム識別子が :file:`file:`
   である場合、ローカルシステムのファイルが (広範囲の改行サポート なしで) 開かれます。それ以外の場合は
   ネットワーク上のどこかにあるサーバへのソケットを開きます。 接続を作ることができない場合、 例外 :exc:`IOError`
   が送出されます。全ての処理がうまくいけば、 ファイル類似のオブジェクトが返されます。このオブジェクトは以下の メソッド:  :meth:`read` 、
   :meth:`readline` 、 :meth:`readlines` 、 :meth:`fileno` 、 :meth:`close` 、
   :meth:`info` そして :meth:`geturl` をサポートします。 また、イテレータプロトコルも正しくサポートしています。 注意:
   :meth:`read`の引数を省略または負の値を指定しても、データスト リームの最後まで読みこむ訳ではありません。ソケットからすべてのストリーム
   を読み込んだことを決定する一般的な方法は存在しません。

   :meth:`info` および :meth:`geturl` メソッドを除き、 これらのメソッドはファイルオブジェクトと同じインタフェースを持って います
   --- このマニュアルの :ref:`bltin-file-objects` セクションを 参照してください。 (ですが、このオブジェクトは組み込みのファイル
   オブジェクトではないので、まれに真の組み込みファイルオブジェクトが 必要な場所では使うことができません)

   .. index:: module: mimetools

   :meth:`info` メソッドは開いた URL に関連付けられたメタ情報 を含む :class:`mimetools.Message`
   クラスのインスタンスを返します。 URL へのアクセスメソッドが HTTP である場合、メタ情報中の ヘッダ情報はサーバが HTML
   ページを返すときに先頭に付加するヘッダ 情報です (Content-Length および Content-Type を含みます) 。 アクセスメソッドが FTP
   の場合、ファイル取得リクエストに応答 してサーバがファイルの長さを返したときには (これは現在では普通に なりましたが) Content-Length
   ヘッダがメタ情報に含められます。 Content-type ヘッダは MIME タイプが推測可能なときにメタ情報に
   含められます。アクセスメソッドがローカルファイルの場合、 返されるヘッダ情報にはファイルの最終更新日時を表す Date エントリ、 ファイルのサイズを示す
   Content-Length エントリ、そして推測される ファイル形式の Content-Type エントリが含まれます。 :mod:`mimetools`
   モジュールを 参照してください。

   .. index:: single: redirect

   :meth:`geturl` メソッドはページの実際の URL を返します。場合に よっては、HTTP サーバはクライアントの要求を他の URL に振り向け
   (redirect 、リダイレクト ) します。 関数 :func:`urlopen` はユーザに対してリダイレクトを透過的に
   行いますが、呼び出し側にとってクライアントがどの URL にリダイレクト されたかを知りたいときがあります。:meth:`geturl` メソッドを
   使うと、このリダイレクトされた URL を取得できます。

   *url* に :file:`http:` スキーム識別子を使う場合、*data* 引数を 与えて ``POST`` 形式のリクエストを行うことができます
   (通常リクエストの 形式は ``GET`` です)。引数 *data* は標準の
   :mimetype:`application/x-www-form-urlencoded` 形式でなければなりません; 以下の
   :func:`urlencode` 関数を参照してください。

   :func:`urlopen` 関数は認証を必要としないプロキシ (proxy) に対して 透過的に動作します。Unix または Windows 環境では、
   Python を起動 する前に、環境変数 :envvar:`http_proxy`、 :envvar:`ftp_proxy` 、および
   :envvar:`gopher_proxy` にそれぞれのプロキシサーバを指定する URL を 設定してください。 例えば (``'%'``
   はコマンドプロンプトです)::

      % http_proxy="http://www.someproxy.com:3128"
      % export http_proxy
      % python
      ...

   Windows 環境では、プロキシを指定する環境変数が設定されていない場合、 プロキシの設定値はレジストリの Internet Settings
   セクションから取得 されます。

   .. index:: single: Internet Config

   Macintosh 環境では、:func:`urlopen` は 「インターネットの設定」 (Internet Config) からプロキシ情報を取得します。

   別の方法として、オプション引数 *proxies* を使って明示的にプロキシを 設定することができます。この引数はスキーム名をプロキシの URL にマップする
   辞書型のオブジェクトでなくてはなりません。空の辞書を指定するとプロキシを 使いません。``None`` (デフォルトの値です) を指定すると、上で述べた
   ように環境変数で指定されたプロキシ設定を使います。例えば::

      # http://www.someproxy.com:3128 を http プロキシに使う
      proxies = {'http': 'http://www.someproxy.com:3128'}
      filehandle = urllib.urlopen(some_url, proxies=proxies)
      # プロキシを使わない
      filehandle = urllib.urlopen(some_url, proxies={})
      # 環境変数からプロキシを使う - 両方の表記とも同じ意味です。
      filehandle = urllib.urlopen(some_url, proxies=None)
      filehandle = urllib.urlopen(some_url)

   (訳注: 上記と矛盾する内容です。おそらく旧バージョンのドキュメントです) 関数 :func:`urlopen` は明示的なプロキシ指定をサポートしていません。
   環境変数のプロキシ設定を上書きしたい場合には :class:`URLopener` を使う か、:class:`FancyURLopener`
   などのサブクラスを使ってください。

   認証を必要とするプロキシは現在のところサポートされていません。 これは実装上の制限 (implementation limitation) と考えています。

   .. versionchanged:: 2.3
      *proxies* のサポートを追加しました。.


.. function:: urlretrieve(url[, filename[, reporthook[, data]]])

   URL で表されるネットワーク上のオブジェクトを、必要に応じてローカルな ファイルにコピーします。URL がローカルなファイルを指定していたり、
   オブジェクトのコピーが正しくキャッシュされていれば、そのオブジェクトは コピーされません。タプル ``(filename, headers)`` を
   返し、*filename* はローカルで見つかったオブジェクトに対する ファイル名で、*headers* は :func:`urlopen` が返した
   (おそらくキャッシュされているリモートの) オブジェクトに :meth:`info` を適用して得られるものになります。 :func:`urlopen`
   と同じ例外を送出します。

   2 つめの引数がある場合、オブジェクトのコピー先となるファイルの位置を 指定します (もしなければ、ファイルの場所は一時ファイル (tmpfile) の
   置き場になり、名前は適当につけられます)。 3 つめの引数がある場合、ネットワークとの接続が確立された際に一度
   呼び出され、以降データのブロックが読み出されるたびに呼び出されるフック 関数 (hook function) を指定します。フック関数には 3 つの引数が渡され
   ます; これまで転送されたブロック数のカウント、バイト単位で表された ブロックサイズ、ファイルの総サイズです。3 つ目のファイルの総サイズ
   は、ファイル取得の際の応答時にファイルサイズを返さない古い FTP サーバ では ``-1`` になります。

   *url* が :file:`http:` スキーム識別子を使っていた場合、オプション 引数 *data* を与えることで ``POST``
   リクエストを行うよう 指定することができます (通常リクエストの形式は ``GET`` です)。 *data* 引数は標準の
   :mimetype:`application/x-www-form-urlencoded` 形式でなくてはなりません; 以下の
   :func:`urlencode` 関数を参照して ください。

   .. versionchanged:: 2.5
      :func:`'urlretrieve()'` は、予想 (これは *Content-Length* ヘッダにより 通知されるサイズです)
      よりも取得できるデータ量が少ないことを検知した場合、 :exc:`ContentTooShortError` を発生します。これは、例えば、ダウンロードが
      中断された場合などに発生します。

      *Content-Length* は下限として扱われます: より多いデータがある場合、 urlretrieve
      はそのデータを読みますが、より少ないデータしか取得できない場合、 これは exception を発生します。

      このような場合にもダウンロードされたデータを取得することは可能で、これは  exception インスタンスの :attr:`content`
      属性に保存されています。

      *Content-Length* ヘッダが無い場合、urlretrieve はダウンロードされた
      データのサイズをチェックできず、単にそれを返します。この場合は、 ダウンロードは成功したと見なす必要があります。.


.. data:: _urlopener

   パブリック関数 :func:`urlopen` および :func:`urlretrieve`  は :class:`FancyURLopener`
   クラスのインスタンスを生成します。 インスタンスは要求された動作に応じて使用されます。 この機能をオーバライドするために、プログラマは
   :class:`URLopener`  または :class:`FancyURLopener` のサブクラスを作り、そのクラスから 生成したインスタンスを変数
   ``urllib._urlopener`` に代入した 後、呼び出したい関数を呼ぶことができます。 例えば、アプリケーションが
   :class:`URLopener` が定義しているのとは 異なった :mailheader:`User-Agent` ヘッダを指定したい場合があるかも
   しれません。この機能は以下のコードで実現できます::

      import urllib

      class AppURLopener(urllib.FancyURLopener):
          version = "App/1.7"

      urllib._urlopener = AppURLopener()


.. function:: urlcleanup()

   以前の :func:`urlretrieve` で生成された可能性のあるキャッシュを 消去します。


.. function:: quote(string[, safe])

   *string* に含まれる特殊文字を ``%xx`` エスケープで置換 （quote）します。 アルファベット、数字、および文字 ``'_.-'`` は
   quote 処理 を行いません。オプションのパラメタ *safe* は quote 処理しない 追加の文字を指定します --- デフォルトの値は ``'/'``
   です。

   例: ``quote('/~connolly/')`` は ``'/%7econnolly/'`` になります。


.. function:: quote_plus(string[, safe])

   :func:`quote` と似ていますが、加えて空白文字をプラス記号 ("+") に 置き換えます。これは HTML フォームの値を quote 処理する際に
   必要な機能です。もとの文字列におけるプラス記号は *safe* に含まれて いない限りエスケープ置換されます。上と同様に、*safe* の デフォルトの値は
   ``'/'`` です。


.. function:: unquote(string)

   ``%xx`` エスケープをエスケープが表す 1 文字に置き換えます。

   例: ``unquote('/%7Econnolly/')`` は ``'/~connolly/'`` になります。


.. function:: unquote_plus(string)

   :func:`unquote` と似ていますが、加えてプラス記号を空白文字に置き換 えます。これは quote 処理された HTML
   フォームの値を元に戻すのに必要な 機能です。


.. function:: urlencode(query[, doseq])

   マップ型オブジェクト、または 2 つの要素をもったタプルからなるシーケンス を、 "URL にエンコードされた (url-encoded)" に変換して、
   上述の :func:`urlopen` のオプション引数 *data* に適した 形式にします。この関数はフォームのフィールド値でできた辞書を ``POST``
   型のリクエストに渡すときに便利です。 返される文字列は ``key=value`` のペアを ``'&'`` で区切ったシーケンスで、*key* と
   *value* の双方は上の :func:`quote_plus` で quote 処理されます。 オプションのパラメタ *doseq*
   が与えられていて、その評価結果が真 であった場合、シーケンス *doseq* の個々の要素について ``key=value`` のペアが生成されます。 2
   つの要素をもったタプルからなるシーケンスが引数 *query* として使われた 場合、各タプルの最初の値が key で、2 番目の値が value になります。
   このときエンコードされた文字列中のパラメタの順番はシーケンス中のタプルの順番 と同じになります。 :mod:`cgi` モジュールでは、関数
   :func:`parse_qs` および :func:`parse_qsl` を提供しており、クエリ文字列を解析して Python
   のデータ構造にするのに利用できます。


.. function:: pathname2url(path)

   ローカルシステムにおける記法で表されたパス名 *path* を、URL に おけるパス部分の形式に変換します。この関数は完全な URL を生成するわけ
   ではありません。返される値は常に :func:`quote` を使って quote 処理 されたものになります。


.. function:: url2pathname(path)

   URL のパスの部分 *path* をエンコードされた URL の形式からローカル システムにおけるパス記法に変換します。この関数は *path* をデコード
   するために :func:`unquote` を使います。


.. class:: URLopener([proxies[, **x509]])

   URL をオープンし、読み出すためのクラスの基礎クラス (base class)です。 :file:`http:` 、 :file:`ftp:`
   、:file:`gopher:` または :file:`file:`  以外のスキームを使ったオブジェクトのオープンをサポートしたいのでない
   かぎり、:class:`FancyURLopener` を使おうと思うことになるでしょう。

   デフォルトでは、 :class:`URLopener` クラスは :mailheader:`User-Agent` ヘッダとして ``urllib/VVV``
   を送信します。ここで *VVV* は :mod:`urllib` のバージョン番号です。アプリケーションで独自の
   :mailheader:`User-Agent` ヘッダを送信したい場合は、:class:`URLopener`  かまたは
   :class:`FancyURLopener` のサブクラスを作成し、 サブクラス定義においてクラス属性 :attr:`version` を適切な
   文字列値に設定することで行うことができます。

   オプションのパラメタ *proxies* はスキーム名をプロキシの URL に マップする辞書でなくてはなりません。空の辞書はプロキシ機能を完全に
   オフにします。デフォルトの値は ``None`` で、この場合、 :func:`urlopen` の定義で述べたように、プロキシを設定する環境変数が
   存在するならそれを使います。

   追加のキーワードパラメタは *x509* に集められますが、これは :file:`https:` スキームを使った際のクライアント認証に使われることがあります。
   キーワード引数 *key_file* および *cert_file* が SSL 鍵と証明書を 設定するためにサポートされています;
   クライアント認証をするには両方が必要です。

   :class:`URLopener` オブジェクトは、サーバがエラーコードを 返した時には :exc:`IOError` を発生します。


.. class:: FancyURLopener(...)

   :class:`FancyURLopener` は :class:`URLopener` のサブクラスで、 以下の HTTP レスポンスコード:
   301、302、303、 307、および 401 を取り扱う機能を提供します。 レスポンスコード 30x に対しては、
   :mailheader:`Location` ヘッダを使って実際の URL を取得します。 レスポンスコード 401 (認証が要求されていることを示す)
   に対しては、 ベーシック認証 (basic HTTP authintication) が行われます。 レスポンスコード 30x に対しては、最大で
   *maxtries* 属性に指定された数だけ再帰呼び出しを行うように なっています。この値はデフォルトで 10 です。

   その他のレスポンスコードについては、:meth:`http_error_default` が 呼ばれます。これはサブクラスでエラーを適切に処理するように
   オーバーライドすることができます。

   .. note::

      :rfc:`2616` によると、 POST 要求に対する 301 および 302  応答はユーザの承認無しに自動的にリダイレクトしてはなりません。
      実際は、これらの応答に対して自動リダイレクトを許すブラウザでは POST を GET に変更しており、:mod:`urllib` でもこの動作を 再現します。

   コンストラクタに与えるパラメタは :class:`URLopener` と同じです。

   .. note::

      基本的な HTTP 認証を行う際、 :class:`FancyURLopener` インスタンスは :meth:`prompt_user_passwd`
      メソッドを呼び出します。このメソッドは デフォルトでは実行を制御している端末上で認証に必要な情報を要求する
      ように実装されています。必要ならば、このクラスのサブクラスにおいて より適切な動作をサポートするために :meth:`prompt_user_passwd`
      メソッドをオーバライドしてもかまいません。


.. exception:: ContentTooShortError(msg[, content])

   この例外は :func:`urlretrieve` 関数が、ダウンロードされたデータの 量が予期した量 (*Content-Length* ヘッダで与えられる)
   よりも少ない ことを検知した際に発生します。:attr:`content` 属性には (恐らく途中までの)  ダウンロードされたデータが格納されています。

   .. versionadded:: 2.5

制限:

  .. index::
     pair: HTTP; protocol
     pair: Gopher; protocol
     pair: FTP; protocol

* 現在のところ、以下のプロトコルだけがサポートされています: HTTP、 (バージョン 0.9 および 1.0)、 Gopher (Gopher-+
  を除く)、 FTP、 およびローカルファイル。

* :func:`urlretrieve` のキャッシュ機能は、有効期限ヘッダ (Expiration time header)
  を正しく処理できるようにハックするための 時間を取れるまで、無効にしてあります。

* ある URL がキャッシュにあるかどうか調べるような関数があればと思って います。。

* 後方互換性のため、 URL がローカルシステム上のファイルを指している ように見えるにも関わらずファイルを開くことができなければ、 URL は FTP
  プロトコルを使って再解釈されます。この機能は時として混乱を招く エラーメッセージを引き起こします。

* 関数 :func:`urlopen` および :func:`urlretrieve` は、
  ネットワーク接続が確立されるまでの間、一定でない長さの遅延を引き起こす ことがあります。このことは、これらの関数を使ってインタラクティブな Web
  クライアントを構築するのはスレッドなしには難しいことを意味します。

  .. index::
     single: HTML
     pair: HTTP; protocol

* :func:`urlopen` または :func:`urlretrieve` が返すデータは サーバが返す生のデータです。このデータはバイナリデータ
  (画像データ等) 、 生テキスト (plain text)、または (例えば) HTML でもかまいません。HTTP プロトコルはリプライ ヘッダ (reply
  header) にデータのタイプに関する情報を返します。 タイプは :mailheader:`Content-Type` ヘッダを見ることで推測できます。

  .. index::
     pair: Gopher; protocol
     module: htmllib

  Gopher プロトコルでは、データのタイプに 関する情報は URL にエンコードされます; これを展開することは簡単 ではありません。返されたデータが
  HTML であれば、 :mod:`htmllib` を使ってパースすることが できます。

  .. index:: single: FTP

  FTP プロトコルを扱うコードでは、ファイルとディレクトリ を区別できません。このことから、アクセスできないファイルを指している URL
  からデータを読み出そうとすると、予期しない動作を引き起こす 場合があります。 URL が``/`` で終わっていれば、ディレクトリを
  指しているものとみなして、それに適した処理を行います。 しかし、ファイルの読み出し操作が 550 エラー (URL が存在しないか、
  主にパーミッションの理由でアクセスできない) になった場合、 URL がディレクトリを指していて、末尾の ``/`` を忘れたケース
  を処理するため、パスをディレクトリとして扱います。 このために、パーミッションのためにアクセスできないファイルを fetch しようとすると、FTP
  コードはそのファイルを開こうとして 550  エラーに陥り、次にディレクトリ一覧を表示しようとするため、 誤解を生むような結果を引き起こす可能性があるのです。
  よく調整された制御が必要なら、:mod:`ftplib` モジュールを使うか、 :class:`FancyURLOpener` をサブクラス化するか、
  *_urlopener* を変更して目的に合わせるよう検討してください。

* このモジュールは認証を必要とするプロキシをサポートしません。 将来実装されるかもしれません。

  .. index:: module: urlparse

* :mod:`urllib` モジュールは URL 文字列を解釈したり構築したりする (ドキュメント化されていない) ルーチンを含んでいますが、URL
  を操作するためのインタフェースとしては、 :mod:`urlparse` モジュールをお勧めします。


.. _urlopener-objs:

URLopener オブジェクト
----------------

.. sectionauthor:: Skip Montanaro <skip@mojam.com>


:class:`URLopener` および :class:`FancyURLopener` クラスのオブジェクトは 以下の属性を持っています。


.. method:: URLopener.open(fullurl[, data])

   適切なプロトコルを使って *fullurl* を開きます。このメソッドは キャッシュとプロキシ情報を設定し、その後適切な open メソッドを入力引数
   つきで呼び出します。認識できないスキームが与えられた場合、 :meth:`open_unknown` が呼び出されます。 *data* 引数は
   :func:`urlopen` の引数 *data* と同じ意味を持っています。


.. method:: URLopener.open_unknown(fullurl[, data])

   オーバライド可能な、未知のタイプの URL を開くためのインタフェースです。


.. method:: URLopener.retrieve(url[, filename[, reporthook[, data]]])

   *url* のコンテンツを取得し、*filename* に書き込みます。 返り値はタプルで、ローカルシステムにおけるファイル名と、 応答ヘッダ (URL
   がリモートを指している場合)  または ``None``  (URL がローカルを指している場合) からなります。呼び出し側の処理は その後
   *filename* を開いて内容を読み出さなくてはなりません。 *filename* が与えられており、かつ URL がローカルシステム上の
   ファイルを示しているばあい、入力ファイル名が返されます。URL が ローカルのファイルを示しておらず、かつ *filename* が与えられて
   いない場合、ファイル名は入力 URL の最後のパス構成要素につけられた拡張子と 同じ拡張子を :func:`tempfile.mktemp`
   につけたものになります。 *reporthook* を与える場合、この変数は 3 つの数値パラメタを受け取る 関数でなくてはなりません。この関数はデータの塊
   (chunk) がネットワークから 読み込まれるたびに呼び出されます。ローカルの URL を与えた場合 *reporthook* は無視されます。

   *url* が :file:`http:` スキーム識別子を使っている場合、オプションの 引数  *data* を与えて ``POST``
   リクエストを行うよう指定できます (通常のリクエストの形式は ``GET`` です) 。   引数 *data* は標準の
   :mimetype:`application/x-www-form-urlencoded`  形式でなくてはなりません; 上の
   :func:`urlencode` を参照して下さい。


.. attribute:: URLopener.version

   URL をオープンするオブジェクトのユーザエージェントを指定する 変数です。:mod:`urllib` を特定のユーザエージェントであると
   サーバに通知するには、サブクラスの中でこの値をクラス変数として 値を設定するか、コンストラクタの中でベースクラスを呼び出す前に 値を設定してください。

:class:`FancyURLopener` クラスはオーバライド可能な追加のメソッドを提供 しており、適切な振る舞いをさせることができます:


.. method:: FancyURLopener.prompt_user_passwd(host, realm)

   指定されたセキュリティ領域 (security realm) 下にある与えられたホスト において、ユーザ認証に必要な情報を返すための関数です。この関数が
   返す値は ``(user, password)`` 、からなるタプルなくて はなりません。値はベーシック認証 (basic authentication)
   で使われます。

   このクラスでの実装では、端末に情報を入力するようプロンプトを出します; ローカルの環境において適切な形で対話型モデルを使うには、このメソッドを
   オーバライドしなければなりません。


使用例
---

.. _urllib examples:

以下は ``GET`` メソッドを使ってパラメタを含む URL を取得するセッション の例です::

   >>> import urllib
   >>> params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
   >>> f = urllib.urlopen("http://www.musi-cal.com/cgi-bin/query?%s" % params)
   >>> print f.read()

以下は ``POST`` メソッドを代わりに使った例です::

   >>> import urllib
   >>> params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
   >>> f = urllib.urlopen("http://www.musi-cal.com/cgi-bin/query", params)
   >>> print f.read()

以下の例では、環境変数による設定内容に対して上書きする形で HTTP プロキシを 明示的に設定しています::

   >>> import urllib
   >>> proxies = {'http': 'http://proxy.example.com:8080/'}
   >>> opener = urllib.FancyURLopener(proxies)
   >>> f = opener.open("http://www.python.org")
   >>> f.read()

以下の例では、環境変数による設定内容に対して上書きする形で、まったく プロキシを使わないよう設定しています::

   >>> import urllib
   >>> opener = urllib.FancyURLopener({})
   >>> f = opener.open("http://www.python.org/")
   >>> f.read()

