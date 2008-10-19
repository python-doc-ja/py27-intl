
:mod:`hashlib` --- セキュアハッシュおよびメッセージダイジェスト
=========================================

.. module:: hashlib
   :synopsis: セキュアハッシュおよびメッセージダイジェストのアルゴリズム
.. moduleauthor:: Gregory P. Smith <greg@users.sourceforge.net>
.. sectionauthor:: Gregory P. Smith <greg@users.sourceforge.net>


.. versionadded:: 2.5

.. index::
   single: message digest, MD5
   single: secure hash algorithm, SHA1, SHA224, SHA256, SHA384, SHA512

このモジュールは、セキュアハッシュやメッセージダイジェスト用のさまざまな アルゴリズムを実装したものです。FIPSのセキュアなハッシュアルゴリズムであ
るSHA1、SHA224、SHA256、SHA384およびSHA512 (FIPS 180-2 で定義されている もの) だけでなくRSAのMD5アルゴリズム
(Internet :rfc:`1321` で定義されてい ます)も実装しています。「セキュアなハッシュ」と「メッセージダイジェスト」
はどちらも同じ意味です。古くからあるアルゴリズムは「メッセージダイジェス ト」と呼ばれていますが、最近は「セキュアハッシュ」という用語が用いられて います。

.. warning::

   中には、ハッシュの衝突の脆弱性をかかえているアルゴリズムもあり ます。最後のFAQをごらんください。

:dfn:`hash` のそれぞれの型の名前をとったコンストラクタメソッドがひとつず つあります。返されるハッシュオブジェクトは、どれも同じシンプルなインター
フェイスを持っています。たとえば :func:`sha1` を使用するとSHA1ハッ
シュオブジェクトが作成されます。このオブジェクトの:meth:`update`メソ ッドに、任意の文字列を渡すことができます。それまでに渡した文字列の
:dfn:`digest`を知りたければ、:meth:`digest`メソッドあるいは :meth:`hexdigest`メソッドを使用します。

.. index:: single: OpenSSL

このモジュールで常に使用できるハッシュアルゴリズムのコンストラクタは :func:`md5`、:func:`sha1`、:func:`sha224`、
:func:`sha256`、:func:`sha384`および:func:`sha512`です。
それ以外のアルゴリズムが使用できるかどうかは、Pythonが使用している OpenSSLライブラリに依存します。

たとえば、``'Nobody inspects the spammish repetition'``という文字列の ダイジェストを取得するには次のようにします。
::

   >>> import hashlib
   >>> m = hashlib.md5()
   >>> m.update("Nobody inspects")
   >>> m.update(" the spammish repetition")
   >>> m.digest()
   '\xbbd\x9c\x83\xdd\x1e\xa5\xc9\xd9\xde\xc9\xa1\x8d\xf0\xff\xe9'

もっと簡潔に書くと、このようになります。 ::

   >>> hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()
   'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'

汎用的なコンストラクタ:func:`new`も用意されています。このコンストラ クタの最初のパラメータとして、使いたいアルゴリズムの名前を指定します。ア
ルゴリズム名として指定できるのは、先ほど説明したアルゴリズムかOpenSSLラ イブラリが提供するアルゴリズムとなります。しかし、アルゴリズム名のコンス
トラクタのほうが:func:`new`よりずっと高速なので、そちらを使うことを お勧めします。

:func:`new`にOpenSSLのアルゴリズムを指定する例です。 ::

   >>> h = hashlib.new('ripemd160')
   >>> h.update("Nobody inspects the spammish repetition")
   >>> h.hexdigest()
   'cc4a5ce1b3df48aec5d22d1f16b894a0b894eccc'

コンストラクタが返すハッシュオブジェクトには、次のような定数属性が用意さ れています。


.. data:: digest_size

   作成されたダイジェストのバイト数。

ハッシュオブジェクトには次のようなメソッドがあります。


.. method:: hash.update(arg)

   ハッシュオブジェクトを文字列*arg*で更新します。繰り返してコールする のは、すべての引数を連結して1回だけコールするのと同じ意味になります。つ
   まり、``m.update(a); m.update(b)``と``m.update(a+b)``は同じ意味だ ということです。


.. method:: hash.digest()

   これまでに:meth:`update`メソッドに渡した文字列のダイジェストを返しま
   す。これは:attr:`digest_size`バイトの文字列であり、非ASCII文字やnull バイトを含むこともあります。


.. method:: hash.hexdigest()

   :meth:`digest`と似ていますが、返される文字列は倍の長さとなり、16進形 式となります。これは、電子メールなどの非バイナリ環境で値を交換する場合に
   便利です。


.. method:: hash.copy()

   ハッシュオブジェクトのコピー ("クローン") を返します。これは、共通部分 を持つ複数の文字列のダイジェストを効率的に計算するために使用します。


.. seealso::

   Module :mod:`hmac`
      ハッシュを用いてメッセージ認証コードを生成するモジュ ールです。

   Module :mod:`base64`
      バイナリハッシュを非バイナリ環境用にエンコードする もうひとつの方法です。

   http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf
      FIPS 180-2 のセキュアハッシュアルゴリズムについての説明。

   http://www.cryptography.com/cnews/hash.html
      Hash Collision FAQ。既知の問題を持つアルゴリズムとその使用上の注意点 に関する情報があります。

