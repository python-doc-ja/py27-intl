
:mod:`getpass` --- 可搬性のあるパスワード入力機構
=================================================

.. module:: getpass
   :synopsis: ポータブルなパスワードとユーザーIDの検索


.. moduleauthor:: Piers Lauder <piers@cs.su.oz.au>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


.. % Windows (& Mac?) support by Guido van Rossum.

The :mod:`getpass` module provides two functions: getpassモジュールは二つの機能を提供します:


.. function:: getpass([prompt[, stream]])

   エコーなしでユーザーにパスワードを入力させるプロンプト。 ユーザーは*prompt*の文字列をプロンプトに使えます、
   デフォルトは``'Password:'``です。 Unixではプロンプトはファイルに似たオブジェクト*stream*へ
   出力されます。デフォルトは``sys.stdout``です(この引数は Windowsでは無視されます。)。

   利用できるシステム: Macintosh, Unix, Windows

   .. versionchanged:: 2.5
      パラメータ *stream* の追加.


.. function:: getuser()

   ユーザーの "ログイン名"を返します。 　有効性:Unix、Windows

   この関数は環境変数:envvar:`LOGNAME` :envvar:`USER` :envvar:`LNAME`
   :envvar:`USERNAME`の順序でチェックして、最初の空ではない文字列が設定された値を返します。
   もし、なにも設定されていない場合はpwdモジュールが提供するシステム上のパスワードデータベースから返します。それ以外は、例外が上がります。

