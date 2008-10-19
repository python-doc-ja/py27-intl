
:mod:`ftplib` --- FTPプロトコルクライアント
================================

.. module:: ftplib
   :synopsis: FTPプロトコルクライアント(ソケットを必要とします)。


.. index::
   pair: FTP; protocol
   single: FTP; ftplib (standard module)

このモジュールでは:class:`FTP`クラスと、それに関連するいくつかの項目を定 義しています。
:class:`FTP`クラスは、FTPプロトコルのクライアント側の機能を備えています。
このクラスを使うとFTPのいろいろな機能の自動化、例えば他のFTPサーバのミ ラーリングといったことを実行するPythonプログラムを書くことができます。
また、:mod:`urllib`モジュールもFTPを使うURLを操作するのにこのクラス を使っています。 FTP (File Transfer
Protocol)についての詳しい情報はInternet :rfc:`959`を参 照して下さい。

:mod:`ftplib`モジュールを使ったサンプルを以下に示します： ::

   >>> from ftplib import FTP
   >>> ftp = FTP('ftp.cwi.nl')   # ホストのデフォルトポートへ接続
   >>> ftp.login()               # ユーザ名 anonymous、パスワード anonyumou
   s@
   >>> ftp.retrlines('LIST')     # ディレクトリの内容をリストアップ
   total 24418
   drwxrwsr-x   5 ftp-usr  pdmaint     1536 Mar 20 09:48 .
   dr-xr-srwt 105 ftp-usr  pdmaint     1536 Mar 21 14:32 ..
   -rw-r--r--   1 ftp-usr  pdmaint     5305 Mar 20 09:48 INDEX
    .
    .
    .
   >>> ftp.retrbinary('RETR README', open('README', 'wb').write)
   '226 Transfer complete.'
   >>> ftp.quit()

このモジュールは以下の項目を定義しています：


.. class:: FTP([host[, user[, passwd[, acct]]]])

   :class:`FTP`クラスの新しいインスタンスを返します。 *host*が与えられると、``connect(host)``メソッドが実行されま す。
   *user*が与えられると、さらに``login(user, passwd, acct)``メソッドが実行されます（この*passwd*と*acct*は指定され
   なければデフォルトでは空文字列です）。


.. data:: all_errors

   :class:`FTP`インスタンスのメソッドの結果、FTP接続で（プログラミングのエ ラーと考えられるメソッドの実行によって）発生する全ての例外（タプル形
   式）。 この例外には以下の４つのエラーはもちろん、:exc:`socket.error`と :exc:`IOError`も含まれます。


.. exception:: error_reply

   サーバから想定外の応答があった時に発生する例外。


.. exception:: error_temp

   400--499の範囲のエラー応答コードを受け取った時に発生する例外。


.. exception:: error_perm

   500--599の範囲のエラー応答コードを受け取った時に発生する例外。


.. exception:: error_proto

   1--5の数字で始まらない応答コードをサーバから受け取った時に発生する例外。


.. seealso::

   Module :mod:`netrc`
      :file:`.netrc`ファイルフォーマットのパーザ。 :file:`.netrc`ファイルは、FTPクライアントがユーザにプロンプトを出す前に、
      ユーザ認証情報をロードするのによく使われます。

   .. index:: single: ftpmirror.py

   Pythonのソースディストリビューションの:file:`Tools/scripts/ftpmi rror.py`ファイルは、FTPサイトあるいはその一部をミ
   ラーリングするスクリプトで、:mod:`ftplib`モジュールを使っています。こ のモジュールを適用した応用例として使うことができます。


.. _ftp-objects:

FTP オブジェクト
----------

いくつかのコマンドは２つのタイプについて実行します：１つはテキストファイ ルで、もう１つはバイナリファイルを扱います。
これらのメソッドのテキストバージョンでは``lines``、バイナリバージョン では``binary``の語がメソッド名の終わりについています。

:class:`FTP`インスタンスには以下のメソッドがあります：


.. method:: FTP.set_debuglevel(level)

   インスタンスのデバッグレベルを設定します。 この設定によってデバッグ時に出力される量を調節します。 デフォルトは``0``で、何も出力されません。
   ``1``なら、一般的に１つのコマンドあたり１行の適当な量のデバッグ出力を 行います。
   ``2``以上なら、コントロール接続で受信した各行を出力して、最大のデバッ グ出力をします。


.. method:: FTP.connect(host[, port[, timeout]])

   指定されたホストとポートに接続します。 ポート番号のデフォルト値はFTPプロトコルの仕様で定められた``21``です。
   他のポート番号を指定する必要はめったにありません。 この関数はひとつのインスタンスに対して一度だけ実行すべきです；
   インスタンスが作られた時にホスト名が与えられていたら、呼び出すべきではあ りません。 これ以外の他の全てのメソッドは接続された後で実行可能となります。


.. method:: FTP.getwelcome()

   接続して最初にサーバから送られてくるウェルカムメッセージを返します。 （このメッセージには、ユーザにとって適切な注意書きやヘルプ情報が含まれる
   ことがあります。）


.. method:: FTP.login([user[, passwd[, acct]]])

   ct 与えられた*user*でログインします。 *passwd*と*acct*のパラメータは省略可能で、デフォルトでは空文字列 です。
   もし*user*が指定されないなら、デフォルトで``'anonymous'``になりま す。
   もし*user*が``'anonymous'``なら、デフォルトの*passwd*は``'anonymous@'``になります。
   このfunctionは各インスタンスについて一度だけ、接続が確立した後に呼び出さ なければなりません；
   インスタンスが作られた時にホスト名とユーザ名が与えられていたら、このメ ソッドを実行すべきではありません。
   ほとんどのFTPコマンドはクライアントがログインした後に実行可能になりま す。


.. method:: FTP.abort()

   実行中のファイル転送を中止します。 これはいつも機能するわけではありませんが、やってみる価値はあります。


.. method:: FTP.sendcmd(command)

   シンプルなコマンド文字列をサーバに送信して、受信した文字列を返します。


.. method:: FTP.voidcmd(command)

   シンプルなコマンド文字列をサーバに送信して、その応答を扱います。 応答コードが200--299の範囲にあれば何も返しません。 それ以外は例外を発生します。


.. method:: FTP.retrbinary(command, callback[, maxblocksize[, rest]])

   バイナリ転送モードでファイルを受信します。 *command*は適切な``RETR``コマンド： ``'RETR filename'``でなければなりません。
   関数*callback*は、受信したデータブロックのそれぞれに対して、データブ ロックを１つの文字列の引数として呼び出されます。
   省略可能な引数*maxblocksize*は、実際の転送を行うのに作られた低レベル のソケットオブジェクトから読み込む最大のチャンクサイズを指定します（これ
   は*callback*に与えられるデータブロックの最大サイズにもなります）。 妥当なデフォルト値が設定されます。
   *rest*は、:meth:`transfercmd`メソッドと同じものです。


.. method:: FTP.retrlines(command[, callback])

   ASCII転送モードでファイルとディレクトリのリストを受信します。
   *command*は、適切な``RETR``コマンド（:meth:`retrbinary`を参
   照）あるいは``LIST``コマンド（通常は文字列``'LIST'``）でなければな りません。
   関数*callback*は末尾のCRLFを取り除いた各行に対して実行されます。
   デフォルトでは*callback*は``sys.stdout``に各行を印字します。


.. method:: FTP.set_pasv(boolean)

   *boolean*がtrueなら"パッシブモード"をオンにし、そうでないならパッ シブモードをオフにします。 （Python
   2.0以前ではデフォルトでパッシブモードはオフにされていましたが、 Python 2.1以後ではデフォルトでオンになっています。）


.. method:: FTP.storbinary(command, file[, blocksize])

   バイナリ転送モードでファイルを転送します。 *command*は適切な``STOR``コマンド：``"STOR filename"``で なければなりません。
   *file*は開かれたファイルオブジェクトで、:meth:`read`メソッドで EOFまで読み込まれ、ブロックサイズ*blocksize*でデータが転送されま
   す。 引数*blocksize*のデフォルト値は8192です。

   .. versionchanged:: 2.1
      *blocksize*のデフォルト値が追加されました.


.. method:: FTP.storlines(command, file)

   ASCII転送モードでファイルを転送します。 *command*は適切な``STOR``コマンドでなければなりません（:meth:`st
   orbinary`を参照）。 *file*は開かれたファイルオブジェクトで、:meth:`readline`メソッド
   でEOFまで読み込まれ、各行がデータが転送されます。


.. method:: FTP.transfercmd(cmd[, rest])

   データ接続中に転送を初期化します。 もし転送中なら、``EPRT``あるいは``PORT``コマンドと、*cmd*で指 定したコマンドを送信し、接続を続けます。
   サーバがパッシブなら、``EPSV``あるいは``PASV``コマンドを送信して接 続し、転送コマンドを開始します。
   どちらの場合も、接続のためのソケットを返します。

   省略可能な*rest*が与えられたら、``REST``コマンドがサーバに送信さ れ、*rest*を引数として与えます。
   *rest*は普通、要求したファイルのバイトオフセット値で、最初のバイトを とばして指定したオフセット値からファイルのバイト転送を再開するよう伝えま す。
   しかし、RFC 959では*rest*が印字可能なASCIIコード33から126の範囲の文 字列からなることを要求していることに注意して下さい。
   したがって、:meth:`transfercmd`メソッドは*rest*を文字列に変換しま すが、文字列の内容についてチェックしません。
   もし``REST``コマンドをサーバが認識しないなら、例外:exc:`error_re ply`が発生します。
   この例外が発生したら、引数*rest*なしに:meth:`transfercmd`を実行し ます。


.. method:: FTP.ntransfercmd(cmd[, rest])

   :meth:`transfercmd`と同様ですが、データと予想されるサイズとのタプルを 返します。
   もしサイズが計算できないなら、サイズの代わりに``None``が返されます。 *cmd*と*rest*は:meth:`transfercmd`のものと同じです。


.. method:: FTP.nlst(argument[, ...])

   ``NLST``コマンドで返されるファイルのリストを返します。 省略可能な*argument*は、リストアップするディレクトリです（デフォルト
   ではサーバのカレントディレクトリです）。 ``NLST``コマンドに非標準である複数の引数を渡すことができます。


.. method:: FTP.dir(argument[, ...])

   ``LIST``コマンドで返されるディレクトリ内のリストを作り、標準出力へ出 力します。
   省略可能な*argument*は、リストアップするディレクトリです（デフォルト ではサーバのカレントディレクトリです）。
   ``LIST``コマンドに非標準である複数の引数を渡すことができます。
   もし最後の引数が関数なら、:meth:`retrlines`のように*callback*とし
   て使われます；デフォルトでは``sys.stdout``に印字します。 このメソッドは``None``を返します。


.. method:: FTP.rename(fromname, toname)

   サーバ上のファイルのファイル名*fromname*を*toname*へ変更します。


.. method:: FTP.delete(filename)

   サーバからファイル*filename*を削除します。 成功したら応答のテキストを返し、そうでないならパーミッションエラーでは
   :exc:`error_perm`を、他のエラーでは:exc:`error_reply`を返しま す。


.. method:: FTP.cwd(pathname)

   サーバのカレントディレクトリを設定します。


.. method:: FTP.mkd(pathname)

   サーバ上に新たにディレクトリを作ります。


.. method:: FTP.pwd()

   サーバ上のカレントディレクトリのパスを返します。


.. method:: FTP.rmd(dirname)

   サーバ上のディレクトリ*dirname*を削除します。


.. method:: FTP.size(filename)

   サーバ上のファイル*filename*のサイズを尋ねます。 成功したらファイルサイズが整数で返され、そうでないなら``None``が返さ れます。
   ``SIZE``コマンドは標準化されていませんが、多くの普通のサーバで実装さ れていることに注意して下さい。


.. method:: FTP.quit()

   サーバに``QUIT``コマンドを送信し、接続を閉じます。 これは接続を閉じるのに"礼儀正しい"方法ですが、``QUIT``コマンドに反
   応してサーバの例外が発生するかもしれません。 この例外は、:meth:`close`メソッドによって:class:`FTP`インスタンスに対
   するその後のコマンド使用が不可になっていることを示しています（下記参 照）。


.. method:: FTP.close()

   接続を一方的に閉じます。 既に閉じた接続に対して実行すべきではありません（例えば:meth:`quit`を 呼び出して成功した後など）。
   この実行の後、:class:`FTP`インスタンスはもう使用すべきではありません （:meth:`close`あるいは:meth:`quit`を呼び出した後で、
   :meth:`login`メソッドをもう一度実行して再び接続を開くことはできませ ん）。

