
:mod:`smtpd` --- SMTP サーバ
============================

.. module:: smtpd


.. moduleauthor:: Barry Warsaw <barry@zope.com>
.. sectionauthor:: Moshe Zadka <moshez@moshez.org>




このモジュールでは、 SMTP サーバを実装するためのクラスをいくつか提供 しています。一つは何も行わない、オーバライドできる汎用のサーバで、
その他の二つでは特定のメール送信ストラテジを提供しています。


SMTPServer オブジェクト
-----------------------


.. class:: SMTPServer(localaddr, remoteaddr)

   新たな:class:`SMTPServer` オブジェクトを作成します。このオブジェクトは ローカルのアドレス*localaddr* に関連づけ (bind)
   されます。 オブジェクトは *remoteaddr* を上流の SMTP リレー先にします。
   このクラスは:class:`asyncore.dispatcher` を継承しており、インスタンス化時に 自身を :mod:`asyncore`
   のイベントループに登録します。


.. method:: SMTPServer.process_message(peer, mailfrom, rcpttos, data)

   このクラスでは:exc:`NotImplementedError`例外を送出します。 受信したメッセージを使って何か意味のある処理をしたい場合にはこのメソッドを
   オーバライドしてください。 コンストラクタの*remoteaddr* に渡した値は:attr:`_remoteaddr` 属性で 参照できます。*peer*
   はリモートホストのアドレスで、*mailfrom* はメッセージエンベロープの発信元 (envelope originator) 、*rcpttos*
   はメッセージエンベロープの受信対象、そして *data* は電子メールの内容 が入った(:rfc:`2822` 形式の)文字列です。


DebuggingServer オブジェクト
----------------------------


.. class:: DebuggingServer(localaddr, remoteaddr)

   新たなデバッグ用サーバを生成します。引数は:class:`SMTPServer` と 同じです。メッセージが届いても無視し、標準出力に出力します。


PureProxy オブジェクト
----------------------


.. class:: PureProxy(localaddr, remoteaddr)

   新たな単純プロキシ (pure proxy) サーバを生成します。引数は:class:`SMTPServer` と同じです。全てのメッセージを
   *remoteaddr* にリレーします。 このオブジェクトを動作させるとオープンリレーを作成してしまう可能性が 多分にあります。注意してください。


MailmanProxy Objects
--------------------


.. class:: MailmanProxy(localaddr, remoteaddr)

   新たな単純プロキシサーバを生成します。引数は:class:`SMTPServer` と同じです。全てのメッセージを *remoteaddr* にリレーしますが、
   ローカルの mailman の設定に*remoteaddr* がある場合には mailman を使って処理します。このオブジェクトを動作させるとオープンリレーを
   作成してしまう可能性が多分にあります。注意してください。

