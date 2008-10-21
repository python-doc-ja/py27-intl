.. _package-index:

******************************
パッケージインデクスに登録する
******************************

Python パッケージインデクス (Python Package Index, PyPI) は、 distutils
でパッケージ化された配布物に関するメタデータを保持 しています。配布物のメタデータをインデクスに提出するには、  Distutils のコマンド
:command:`register` を使います。 :command:`register` は以下のように起動します::

   python setup.py register

Distutils は以下のようなプロンプトを出します::

   running register
   We need to know who you are, so please choose either:
    1. use your existing login,
    2. register as a new user,
    3. have the server generate a new password for you (and email it to you), or
    4. quit
   Your selection [default 1]:

注意: ユーザ名とパスワードをローカルの計算機に保存しておくと、 このメニューは表示されません。

まだ PyPI に登録したことがなければ、まず登録する必要があります。 この場合選択肢 2 番を選び、リクエストされた詳細情報を入力して
ゆきます。詳細情報を提出し終えると、登録情報の承認を行うための メールを受け取るはずです。

すでに登録を行ったことがあれば、選択肢 1 を選べます。この選択肢を 選ぶと、PyPI ユーザ名とパスワードを入力するよう促され、
:command:`register` がメタデータをインデクスに自動的に提出します。

配布物の様々なバージョンについて、好きなだけインデクスへの提出 を行ってかまいません。特定のバージョンに関するメタデータを
入れ替えたければ、再度提出を行えば、インデクス上のデータが 更新されます。

PyPI は提出された配布物の (名前、バージョン) の各組み合わせについて 記録を保持しています。ある配布物名について最初に情報を提出したユーザが、
その配布物名のオーナ (owner) になります。オーナは :command:`register` コマンドか、web
インタフェースを介して変更を提出できます。 オーナは他のユーザをオーナやメンテナとして指名できます。
メンテナはパッケージ情報を編集できますが、他の人をオーナやメンテナに 指名することはできません。

デフォルトでは、 PyPI はあるパッケージについて全てのバージョンを 表示します。特定のバージョンを非表示にしたければ、パッケージの Hidden
プロパティを yes に設定します。この値は web インタフェース で編集しなければなりません。


.. _pypirc:

.pypircファイル (The .pypirc file)
==================================

:file:`.pypirc`ファイルのフォーマットを示します。 ::

   [server-login]
   repository: <repository-url>
   username: <username>
   password: <password>

*repository* は省略可能で、デフォルトでは ``http://www.python.org/pypi`` になります。


