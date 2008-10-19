
:mod:`pwd` --- パスワードデータベースへのアクセスを提供する
=====================================

.. module:: pwd
   :platform: Unix
   :synopsis: パスワードデータベースへのアクセスを提供する (getpwnam() など)。


このモジュールはUnixのユーザアカウントとパスワードのデータベースへ のアクセスを提供します。全てのUnix系OSで利用できます。

.. % This module provides access to the \UNIX{} user account and password
.. % database.  It is available on all \UNIX{} versions.

パスワードデータベースの各エントリはタプルのようなオブジェクトで提供され、 それぞれの属性は``passwd``構造体のメンバに対応しています(下
の属性欄については、``<pwd.h>``を見てください)。

.. % Password database entries are reported as a tuple-like object, whose
.. % attributes correspond to the members of the \code{passwd} structure
.. % (Attribute field below, see \code{<pwd.h>}):

+--------+---------------+------------------------+
| インデックス | 属性            | 意味                     |
+========+===============+========================+
| 0      | ``pw_name``   | ログイン名                  |
+--------+---------------+------------------------+
| 1      | ``pw_passwd`` | 暗号化されたパスワード(optional)) |
+--------+---------------+------------------------+
| 2      | ``pw_uid``    | ユーザID(UID)             |
+--------+---------------+------------------------+
| 3      | ``pw_gid``    | グループID(GID)            |
+--------+---------------+------------------------+
| 4      | ``pw_gecos``  | 実名またはコメント              |
+--------+---------------+------------------------+
| 5      | ``pw_dir``    | ホームディレクトリ              |
+--------+---------------+------------------------+
| 6      | ``pw_shell``  | シェル                    |
+--------+---------------+------------------------+

UIDとGIDは整数で、それ以外は全て文字列です。 検索したエントリが見つからないと:exc:`KeyError`が発生します。

.. % The uid and gid items are integers, all others are strings.
.. % \exception{KeyError} is raised if the entry asked for cannot be found.

.. % \note{In traditional \UNIX{} the field \code{pw_passwd} usually
.. % contains a password encrypted with a DES derived algorithm (see module
.. % \refmodule{crypt}\refbimodindex{crypt}).  However most modern unices
.. % use a so-called \emph{shadow password} system.  On those unices the
.. % field \code{pw_passwd} only contains a asterisk (\code{'*'}) or the
.. % letter \character{x} where the encrypted password is stored in a file
.. % \file{/etc/shadow} which is not world readable.}

.. note::

   .. index:: module: crypt

   伝統的なUnixでは、``pw_passwd``フィールドはDES由来のアルゴリ ズムで暗号化されたパスワード(:mod:`crypy`モジュー
   ルをごらんください)が含まれています。しかし、近代的なUNIX系OSでは*シャドウパスワード*とよばれる仕組みを利用しています。この場合には
   *pw_passwd*フィールドにはアスタリスク(``'*'``)か、``'x'``と いう一文字だけが含まれており、暗号化されたパスワードは、一般には見えない
   :file:`/etc/shadow`というファイルに入っています。*pw_passwd*フィールド に有用な値が入っているかはシステムに依存します。
   利用可能なら、暗号化されたパスワードへのアクセスが必要なときには  :mod:`spwd`モジュールを利用してください。

このモジュールでは以下のものが定義されています:

.. % It defines the following items:


.. function:: getpwuid(uid)

   与えられたUIDに対応するパスワードデータベースのエントリを返します。


.. function:: getpwnam(name)

   与えられたユーザ名に対応するパスワードデータベースのエントリを返します。


.. function:: getpwall()

   パスワードデータベースの全てのエントリを、任意の順番で並べたリストを返し ます。


.. seealso::

   Module :mod:`grp`
      このモジュールに似た、グループデータベースへのアクセス を提供するモジュール。

   Module :mod:`spwd`
      このモジュールに似た、シャドウパスワードデータベースへのアクセス を提供するモジュール。

