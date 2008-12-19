
:mod:`hmac` --- メッセージ認証のための鍵付きハッシュ化
======================================================

.. module:: hmac
   :synopsis: Python で実装された、メッセージ認証のための鍵付き ハッシュ化 (HMAC: Keyed-Hashing for Message
              Authentication) アルゴリズム。
.. moduleauthor:: Gerhard Häring <ghaering@users.sourceforge.net>
.. sectionauthor:: Gerhard Häring <ghaering@users.sourceforge.net>


.. versionadded:: 2.2

このモジュールでは :rfc:`2104` で記述されている HMAC アルゴリズム を実装しています。


.. function:: new(key[, msg[, digestmod]])

   新たな hmac オブジェクトを返します。*msg* が存在すれば、 メソッド呼び出し ``updatemsg`` を行います。 *digestmod* は
   HMAC オブジェクトが使うダイジェストコンストラクタある いはモジュールです。標準では ``hashlib.md5`` コンストラク タになっています。

   .. note::

      md5ハッシュには既知の脆弱性がありますが、後方互 換性を考慮してデフォルトのままにしています。使用するアプリケーションにあ
      わせてよりよいものを選択してください。

HMAC オブジェクトは以下のメソッドを持っています:


.. method:: hmac.update(msg)

   hmac オブジェクトを文字列 *msg* で更新します。繰り返し呼び出し を行うと、それらの引数を全て結合した引数で単一の呼び出しをした
   際と同じに等価になります: すなわち ``m.update(a); m.update(b)``  は ``m.update(a + b)`` と等価です。


.. method:: hmac.digest()

   これまで :meth:`update` メソッドに渡された文字列のダイジェスト値
   を返します。これは:attr:`digest_size`バイトの文字列で、NULL バイトを含む 非 ASCII 文字が含まれることがあります。


.. method:: hmac.hexdigest()

   :meth:`digest`と似ていますが、返される文字列は倍の長さとなり、16進形 式となります。これは、電子メールなどの非バイナリ環境で値を交換する場合に
   便利です。


.. method:: hmac.copy()

   hmac オブジェクトのコピー ("クローン") を返します。このコピー は最初の部分文字列が共通になっている文字列のダイジェスト値を効率
   よく計算するために使うことができます。


.. seealso::

   Module :mod:`hashlib`
      セキュアハッシュ関数を提供するpythonモジュールです。

