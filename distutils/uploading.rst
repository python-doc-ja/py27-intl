.. _package-upload:

***************************************
Uploading Packages to the Package Index
***************************************

.. versionadded:: 2.5

Python Package Index (PyPI) は、パッケージ情報に加えて、作者が望むのであれば パッケージデータを置くこともできます。
distutils の :command:`upload` コマンドは配布物をPyPIにアップロードします。

このコマンドは一つ以上の配布物ファイルをビルドした直後に呼び出されます。 例えば、次のコマンド ::

   python setup.py sdist bdist_wininst upload

は、ソース配布物とWindowsのインストーラをPyPIにアップロードします。 以前に :file:`setup.py`
を実行してビルドした配布物もアップロード対象に なるけれども、アップロードされるのは :command:`upload` コマンドと同時に
指定された配布物だけだということに注意してください。

:command:`upload` コマンドは、:file:`$HOME/.pypirc` ファイル (詳しくは:ref:`pypirc` セクションを
ご覧下さい) の、ユーザー名、パスワードとリポジトリURLを利用します。

:option:`--sign` オプションで、 アップロードする各ファイルにGPG (GNU Privacy Guard) を使うことができます。
:program:`gpg` プログラムが 環境変数:envvar:`PATH` から実行可能である必要があります。
署名にどの鍵を使うかを、:option:`--identity=*name*` で指定することもできます。

他の :command:`upload` のオプションには、 :option:`--repository=*url*`
(:file:`$HOME/.pypirc` で設定されたリポジトリを 上書きします)、 :option:`--show-response`
(アップロードの問題をデバッグするために、PyPI サーバー からの全てのレスポンスを表示します)　があります。


