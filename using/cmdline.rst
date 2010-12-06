.. highlightlang:: none

.. _using-on-general:

コマンドラインと環境
=====================

CPython インタプリタはコマンドラインと環境を読み取って様々な設定を行ないます。

.. impl-detail::

   他の実装のコマンドラインスキームは CPython とは異なります。
   さらなる情報は :ref:`implementations` を参照してください。


.. _using-on-cmdline:

コマンドライン
---------------

Python を起動するとき、以下のうち任意のオプションを指定できます。 ::

    python [-BdEiOQsStuUvVWxX3?] [-c command | -m module-name | script | - ] [args]

もちろん、もっとも一般的な利用方法は、シンプルにスクリプトを実行するものです。 ::

    python myscript.py


.. _using-on-interface-options:

インターフェイスオプション
~~~~~~~~~~~~~~~~~~~~~~~~~~~

インタプリタのインターフェイスは UNIX シェルに似ていますが、
より多くのの実行方法を提供しています。

* tty デバイスに接続された標準入力とともに起動された場合、 EOF (end-of-file
  文字。 UNIX では *Ctrl-D* で、Windows では *Ctrl-Z, Enter* で入力可能)
  を受け取るまで、コマンドを受け取り、それを実行します。
* ファイル名引数を指定されるか、ファイルを標準入力に渡された場合は、
  そのファイルから読み込んだスクリプトを実行します。
* ディレクトリ名を引数に受け取ったときは、そのディレクトリから適切な
  名前のスクリプトファイルを読み込んで実行します。
* ``-c コマンド`` オプションを利用して起動された場合、 *コマンド* として渡された
  Python の文を実行します。 *コマンド* の部分には改行で区切られた複数行を指定する
  こともできます。行の先頭の空白文字は Python 文の重要要素です！
* ``-m モジュール名`` として Python モジュールパスにあるモジュールを指定された場合、
  そのモジュールをスクリプトとして実行します。

非インタラクティブモードでは、入力の全体が実行前にパースされます。

インタプリタによって消費されるオプションリストが終了したあと、継続する全ての
引数は :data:`sys.argv` に渡ります。 -- ただし、添字 0 の先頭要素(``sys.argv[0]``)
はプログラムのソース自体を示す文字列です。

.. cmdoption:: -c <command>

   *command* 内の Python コードを実行します。
   *command* は改行によって区切られた1行以上の文です。
   通常のモジュールのコードと同じく、行頭の空白文字は意味を持ちます。

   このオプションが指定された場合、 :data:`sys.argv` の先頭要素は ``"-c"`` になり、
   カレントディレクトリが :data:`sys.path` の先頭に追加されます。
   (そのディレクトリにあるモジュールをトップレベルモジュールとして import
   することが可能になります。)


.. cmdoption:: -m <module-name>

   :data:`sys.path` から指定されたモジュール名のモジュールを探し、その内容を
   :mod:`__main__` モジュールとして実行します。

   引数は *module* 名なので、拡張子 (``.py``) を含めてはいけません。
   ``module-name`` は有効な Python のモジュール名であるべきですが、実装がそれを
   矯正しているとは限りません。 (例えば、ハイフンを名前に含める事を許可するかも
   しれません。)

   .. note::

      このオプションはビルトインモジュールや C で書かれた拡張モジュールには
      利用できません。 Python モジュールファイルを持っていないからです。
      しかし、コンパイル済みのモジュールは、たとえ元のソースファイルがなくても
      利用可能です。

   このオプションが指定された場合、 :data:`sys.argv` の先頭要素はモジュールファイルの
   フルパスになります。
   :option:`-c` オプションのように、カレントディレクトリが :data:`sys.path`
   の先頭に追加されます。

   Many standard library modules contain code that is invoked on their execution
   as a script.  An example is the :mod:`timeit` module::
   多くの標準ライブラリモジュールが、スクリプトとして実行された時のコードを持っています。
   例えば、 :mod:`timeit` モジュールは次のように実行可能です。 ::

       python -mtimeit -s 'setup here' 'benchmarked code here'
       python -mtimeit -h # for details

   .. seealso::
      :func:`runpy.run_module`
         この機能の実際の実装

      :pep:`338` -- Executing modules as scripts

   .. versionadded:: 2.4

   .. versionchanged:: 2.5
      パッケージ内のモジュールを指定できるようになりました。


.. describe:: -

   標準入力 (:data:`sys.stdin`) からコマンドを読み込みます。
   標準入力がターミナルだった場合、 :option:`-i` オプションを含みます。

   このオプションが指定された場合、 :data:`sys.argv` の最初の要素は
   ``"-"`` で、カレントディレクトリが :data:`sys.path` の先頭に追加されます。


.. describe:: <script>

   *script* 内の Python コードを実行します。
   *script* は、 Python ファイル、 ``__main__.py`` ファイルを含むディレクトリ、
   ``__main__.py`` ファイルを含む zip ファイルのいづれかの、ファイルシステム上の
   (絶対あるいは相対)パスでなければなりません。

   このオプションが指定された場合、 :data:`sys.argv` の先頭要素は、
   コマンドラインで指定されたスクリプト名になります。

   スクリプト名が Python ファイルを直接指定していた場合、そのファイルを
   含むディレクトリが :data:`sys.path` の先頭に追加され、そのファイルは
   :mod:`__main__` モジュールとして実行されます。

   スクリプト名がディレクトリか zip ファイルを指定していた場合、
   スクリプト名が :data:`sys.path` に追加され、その中の ``__main__.py``
   ファイルが :mod:`__main__` モジュールとして実行されます。

   .. versionchanged:: 2.5
      トップレベルに ``__main__.py`` ファイルを持つディレクトリや zip ファイルが
      有効な Python スクリプトとなりました。

インターフェイスオプションが与えられなかった場合、 :option:`-i` が暗黙的に指定され、
``sys.argv[0]`` は空白文字列 (``""``)で、カレントディレクトリが :data:`sys.path`
の先頭に追加されます。

.. seealso::  :ref:`tut-invoking`


一般オプション
~~~~~~~~~~~~~~~

.. cmdoption:: -?
               -h
               --help

   全てのコマンドラインオプションの短い説明を表示します。

   .. versionchanged:: 2.5
      ``--help`` 形式


.. cmdoption:: -V
               --version

   Python のバージョン番号を表示して終了します。出力の例::

       Python 2.5.1

   .. versionchanged:: 2.5
      ``--version`` 形式


その他のオプション
~~~~~~~~~~~~~~~~~~~~~

.. cmdoption:: -B

   Python は import したソースモジュールの ``.pyc`` や ``.pyo`` ファイルの
   作成を試みません。
   :envvar:`PYTHONDONTWRITEBYTECODE` 環境変数も参照してください。

   .. versionadded:: 2.6


.. cmdoption:: -d

   パーサーのデバッグ出力を有効にします。(魔法使い専用です。コンパイルオプションに
   依存します)。
   :envvar:`PYTHONDEBUG` も参照してください。


.. cmdoption:: -E

   全ての :envvar:`PYTHON*` 環境変数を無視します。
   例えば、 :envvar:`PYTHONPATH` と :envvar:`PYTHONHOME` などです。

   .. versionadded:: 2.2


.. cmdoption:: -i

   最初の引数にスクリプトが指定された場合や :option:`-c` オプションが利用された場合、
   :data:`sys.stdin` がターミナルに出力されない場合も含めて、
   スクリプトかコマンドを実行した後にインタラクティブモードに入ります。
   :envvar:`PYTHONSTARTUP` ファイルは読み込みません。

   このオプションはグローバル変数や、スクリプトが例外を発生させるときにその
   スタックトレースを調べるのに便利です。 :envvar:`PYTHONINSPECT` も参照してください。


.. cmdoption:: -O

   基本的な最適化を有効にします。
   コンパイル済み (:term:`bytecode`) ファイルの拡張子を ``.pyc`` から ``.pyo``
   に変更します。 :envvar:`PYTHONOPTIMIZE` も参照してください。


.. cmdoption:: -OO

   :option:`-O` の最適化に加えて、ドキュメンテーション文字列の除去も行ないます。


.. cmdoption:: -Q <arg>

   除算制御。引数は以下のうち1つでなければなりません:

   ``old``
     int/int と long/long の除算は、 int か long を返します。 (*デフォルト*)
   ``new``
     新しい除算方式。 int/int や long/long の除算が float を返します。
   ``warn``
     古い除算方式で、 int/int や long/long 除算に警告を表示します。
   ``warnall``
     古い除算方式で、全ての除算演算子に対して警告を表示します。

   .. seealso::
      :file:`Tools/scripts/fixdiv.py`
         ``warnall`` を使っています.

      :pep:`238` -- Changing the division operator


.. cmdoption:: -s

   sys.path にユーザー site ディレクトリを追加しません。

   .. versionadded:: 2.6

   .. seealso::

      :pep:`370` -- Per user site-packages directory


.. cmdoption:: -S

   :mod:`site` モジュールのインポートを無効にし、そのモジュールで行われている
   場所独自の :data:`sys.path` 操作を無効にします。


.. cmdoption:: -t

   ソースファイルが、タブ幅に依存して意味が変わるような方法でタブ文字とスペースを
   混ぜて含んでいる場合に警告を発生させます。このオプションを2重にする (:option:`-tt`)
   とエラーになります。


.. cmdoption:: -u

   stdin, stdout, stderr のバッファを強制的に無効にします。
   関係するシステムでは、 stdin, stdout, stderr をバイナリモードにします。

   :meth:`file.readlines` や :ref:`bltin-file-objects` (``for line in sys.stdin``)
   はこのオプションに影響されない内部バッファリングをしています。
   これを回避したい場合は、 ``while 1:`` ループの中で :meth:`file.readline` します。

   :envvar:`PYTHONUNBUFFERED` も参照してください。


.. cmdoption:: -v

   モジュールが初期化されるたびに、それがどこ(ファイル名やビルトインモジュール)
   からロードされたのかを示すメッセージを表示します。
   2重に指定された場合(:option:`-vv`)は、モジュールを検索するときにチェックされた
   各ファイルに対してメッセージを表示します。また、終了時のモジュールクリーンアップに
   関する情報も提供します。 :envvar:`PYTHONVERBOSE` も参照してください。


.. cmdoption:: -W arg

   警告制御。 Python の警告機構はデフォルトでは警告メッセージを :data:`sys.stderr`
   に表示します。典型的な警告メッセージは次の形をしています::

       file:line: category: message

   デフォルトでは、各警告は発生したソース業ごとに一度だけ表示されます。
   このオプションは、警告をどれくらいの頻度で表示するかを制御します。

   複数の :option:`-W` オプションを指定することができます。警告が1つ以上の
   オプションとマッチしたときは、最後にマッチしたオプションのアクションが有効になります。
   不正な :option:`-W` オプションは無視されます。(最初の警告が発生したときに、
   不正なオプションに対する警告メッセージが表示されます。)

   警告は Python プログラムの中から :mod:`warnings` モジュールを利用して
   制御することができます。

   引数の一番シンプルな形は、以下のアクション文字列(かそのユニークな短縮形)
   を単体で利用するものです。

   ``ignore``
      全ての警告を無視する。
   ``default``
      明示的にデフォルトの動作(ソース行ごとに1度警告を表示する)を要求する。
   ``all``
      警告が発生するたびに表示する (これは、ループの中などで同じソース行により
      繰り返し警告が発生された場合に、大量のメッセージを表示します。)
   ``module``
      各モジュールで最初に発生した警告を表示する。
   ``once``
      プログラムで最初に発生した警告だけを表示する。
   ``error``
      警告メッセージを表示する代わりに例外を発生させる。

   引数の完全形は次のようになります::

       action:message:category:module:line

   ここで、 *action* は上で説明されたものですが、残りのフィールドにマッチした
   メッセージにだけ適用されます。空のフィールドは全ての値にマッチします。
   空のフィールドの後ろは除外されます。 *message* フィールドは表示される
   警告メッセージの先頭に、大文字小文字を無視してマッチします。 *category*
   フィールドは警告カテゴリにマッチします。これはクラス名でなければなりません。
   *category* のマッチは、メッセージの実際の警告カテゴリーが指定された警告
   カテゴリーのサブクラスかどうかをチェックします。完全なクラス名を指定しなければ
   なりません。
   *module* フィールドは、(完全正規形(fully-qualified)の) モジュール名に対して
   マッチします。このマッチは大文字小文字を区別します。
   *line* フィールドは行番号にマッチします。 0 は全ての行番号にマッチし、
   省略した時と同じです。

   .. seealso::
      :mod:`warnings` -- the warnings module

      :pep:`230` -- Warning framework


.. cmdoption:: -x

   Unix 以外の形式の ``#!cmd`` を使うために、ソースの最初の行をスキップします。
   これは、DOS専用のハックのみを目的としています。

   .. note:: エラーメッセージ内の行番号は -1 されます。

.. cmdoption:: -3

   Warn about Python 3.x incompatibilities which cannot be fixed trivially by
   :ref:`2to3 <2to3-reference>`. Among these are:

   * :meth:`dict.has_key`
   * :func:`apply`
   * :func:`callable`
   * :func:`coerce`
   * :func:`execfile`
   * :func:`reduce`
   * :func:`reload`

   Using these will emit a :exc:`DeprecationWarning`.

   .. versionadded:: 2.6

Options you shouldn't use
~~~~~~~~~~~~~~~~~~~~~~~~~

.. cmdoption:: -J

   Reserved for use by Jython_.

.. _Jython: http://jython.org

.. cmdoption:: -U

   Turns all string literals into unicodes globally.  Do not be tempted to use
   this option as it will probably break your world.  It also produces
   ``.pyc`` files with a different magic number than normal.  Instead, you can
   enable unicode literals on a per-module basis by using::

        from __future__ import unicode_literals

   at the top of the file.  See :mod:`__future__` for details.

.. cmdoption:: -X

    Reserved for alternative implementations of Python to use for their own
    purposes.

.. _using-on-envvars:

Environment variables
---------------------

These environment variables influence Python's behavior.

.. envvar:: PYTHONHOME

   Change the location of the standard Python libraries.  By default, the
   libraries are searched in :file:`{prefix}/lib/python{version}` and
   :file:`{exec_prefix}/lib/python{version}`, where :file:`{prefix}` and
   :file:`{exec_prefix}` are installation-dependent directories, both defaulting
   to :file:`/usr/local`.

   When :envvar:`PYTHONHOME` is set to a single directory, its value replaces
   both :file:`{prefix}` and :file:`{exec_prefix}`.  To specify different values
   for these, set :envvar:`PYTHONHOME` to :file:`{prefix}:{exec_prefix}`.


.. envvar:: PYTHONPATH

   Augment the default search path for module files.  The format is the same as
   the shell's :envvar:`PATH`: one or more directory pathnames separated by
   :data:`os.pathsep` (e.g. colons on Unix or semicolons on Windows).
   Non-existent directories are silently ignored.

   In addition to normal directories, individual :envvar:`PYTHONPATH` entries
   may refer to zipfiles containing pure Python modules (in either source or
   compiled form). Extension modules cannot be imported from zipfiles.

   The default search path is installation dependent, but generally begins with
   :file:`{prefix}/lib/python{version}` (see :envvar:`PYTHONHOME` above).  It
   is *always* appended to :envvar:`PYTHONPATH`.

   An additional directory will be inserted in the search path in front of
   :envvar:`PYTHONPATH` as described above under
   :ref:`using-on-interface-options`. The search path can be manipulated from
   within a Python program as the variable :data:`sys.path`.


.. envvar:: PYTHONSTARTUP

   If this is the name of a readable file, the Python commands in that file are
   executed before the first prompt is displayed in interactive mode.  The file
   is executed in the same namespace where interactive commands are executed so
   that objects defined or imported in it can be used without qualification in
   the interactive session.  You can also change the prompts :data:`sys.ps1` and
   :data:`sys.ps2` in this file.


.. envvar:: PYTHONY2K

   Set this to a non-empty string to cause the :mod:`time` module to require
   dates specified as strings to include 4-digit years, otherwise 2-digit years
   are converted based on rules described in the :mod:`time` module
   documentation.


.. envvar:: PYTHONOPTIMIZE

   If this is set to a non-empty string it is equivalent to specifying the
   :option:`-O` option.  If set to an integer, it is equivalent to specifying
   :option:`-O` multiple times.


.. envvar:: PYTHONDEBUG

   If this is set to a non-empty string it is equivalent to specifying the
   :option:`-d` option.  If set to an integer, it is equivalent to specifying
   :option:`-d` multiple times.


.. envvar:: PYTHONINSPECT

   If this is set to a non-empty string it is equivalent to specifying the
   :option:`-i` option.

   This variable can also be modified by Python code using :data:`os.environ`
   to force inspect mode on program termination.


.. envvar:: PYTHONUNBUFFERED

   If this is set to a non-empty string it is equivalent to specifying the
   :option:`-u` option.


.. envvar:: PYTHONVERBOSE

   If this is set to a non-empty string it is equivalent to specifying the
   :option:`-v` option.  If set to an integer, it is equivalent to specifying
   :option:`-v` multiple times.


.. envvar:: PYTHONCASEOK

   If this is set, Python ignores case in :keyword:`import` statements.  This
   only works on Windows.


.. envvar:: PYTHONDONTWRITEBYTECODE

   If this is set, Python won't try to write ``.pyc`` or ``.pyo`` files on the
   import of source modules.

   .. versionadded:: 2.6

.. envvar:: PYTHONIOENCODING

   Overrides the encoding used for stdin/stdout/stderr, in the syntax
   ``encodingname:errorhandler``.  The ``:errorhandler`` part is optional and
   has the same meaning as in :func:`str.encode`.

   .. versionadded:: 2.6


.. envvar:: PYTHONNOUSERSITE

   If this is set, Python won't add the user site directory to sys.path

   .. versionadded:: 2.6

   .. seealso::

      :pep:`370` -- Per user site-packages directory


.. envvar:: PYTHONUSERBASE

   Sets the base directory for the user site directory

   .. versionadded:: 2.6

   .. seealso::

      :pep:`370` -- Per user site-packages directory


.. envvar:: PYTHONEXECUTABLE

   If this environment variable is set, ``sys.argv[0]`` will be set to its
   value instead of the value got through the C runtime.  Only works on
   Mac OS X.


Debug-mode variables
~~~~~~~~~~~~~~~~~~~~

Setting these variables only has an effect in a debug build of Python, that is,
if Python was configured with the :option:`--with-pydebug` build option.

.. envvar:: PYTHONTHREADDEBUG

   If set, Python will print threading debug info.

   .. versionchanged:: 2.6
      Previously, this variable was called ``THREADDEBUG``.

.. envvar:: PYTHONDUMPREFS

   If set, Python will dump objects and reference counts still alive after
   shutting down the interpreter.


.. envvar:: PYTHONMALLOCSTATS

   If set, Python will print memory allocation statistics every time a new
   object arena is created, and on shutdown.

