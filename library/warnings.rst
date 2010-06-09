
:mod:`warnings` --- 警告の制御
==============================

.. index:: single: warnings

.. module:: warnings
   :synopsis: 警告メッセージを送出したり、その処理方法を制御したりします。


.. versionadded:: 2.1

警告メッセージは一般に、ユーザに警告しておいた方がよいような状況下にプログラムが置かれているが、その状況は (通常は) 例外を送出したり
そのプログラムを終了させるほどの正当な理由がないといった状況で発されます。例えば、プログラムが古いモジュールを使っている場合
には警告を発したくなるかもしれません。

Python プログラマは、このモジュールの :func:`warn` 関数を使うことで警告を発することができます。(C 言語のプログラマは
:cfunc:`PyErr_WarnEx` を使います; 詳細は :ref:`exceptionhandling` を参照してください)。

警告メッセージは通常 ``sys.stderr`` に出力されますが、その処理方法は、全ての警告に対する無視する処理から警告を例外に変更する
処理まで、柔軟に変更することができます。警告の処理方法は警告カテゴリ (以下参照)、警告メッセージテキスト、そして警告を
発したソースコード上の場所に基づいて変更することができます。ソースコード上の同じ場所に対して特定の警告が繰り返された場合、通常は抑制されます。

警告制御には 2 つの段階 (stage) があります: 第一に、警告が発されるたびに、メッセージを出力すべきかどうか決定が行われます; 次に、
メッセージを出力するなら、メッセージはユーザによって設定が可能なフックを使って書式化され印字されます。

警告メッセージを出力するかどうかの決定は、警告フィルタによって制御されます。警告フィルタは一致規則 (matching
rule)と動作からなるシーケンスです。 :func:`filterwarnings` を呼び出して一致規則をフィルタに追加する
ことができ、 :func:`resetwarnings` を呼び出してフィルタを標準設定の状態にリセットすることができます。

警告メッセージの印字は :func:`showwarning` を呼び出して行うことができ、この関数は上書きすることができます; この関数の標準の実装では、
:func:`formatwarning` を呼び出して警告メッセージを書式化しますが、この関数についても自作の実装を使うことができます。


.. _warning-categories:

警告カテゴリ
------------

警告カテゴリを表現する組み込み例外は数多くあります。このカテゴリ化は警告をグループごとフィルタする上で便利です。現在以下の警告カテゴリ
クラスが定義されています:

+----------------------------------+---------------------------------------------------------------------------------------+
| クラス                           | 記述                                                                                  |
+==================================+=======================================================================================+
| :exc:`Warning`                   | 全ての警告カテゴリクラスの基底クラスです。 :exc:`Exception`                           |
|                                  | のサブクラスです。                                                                    |
+----------------------------------+---------------------------------------------------------------------------------------+
| :exc:`UserWarning`               | :func:`warn` の標準のカテゴリです。                                                   |
+----------------------------------+---------------------------------------------------------------------------------------+
| :exc:`DeprecationWarning`        | その機能が廃用化されていることを示す警告カテゴリの基底クラスです。                    |
+----------------------------------+---------------------------------------------------------------------------------------+
| :exc:`SyntaxWarning`             | その文法機能があいまいであることを示す警告カテゴリの基底クラスです。                  |
+----------------------------------+---------------------------------------------------------------------------------------+
| :exc:`RuntimeWarning`            | その実行時システム機能があいまいであることを示す警告カテゴリの基底クラスです。        |
+----------------------------------+---------------------------------------------------------------------------------------+
| :exc:`FutureWarning`             | その構文の意味付けが将来変更される予定であることを示す警告カテゴリの基底クラスです。  |
+----------------------------------+---------------------------------------------------------------------------------------+
| :exc:`PendingDeprecationWarning` | 将来その機能が廃用化されることを示す                                                  |
|                                  | 警告カテゴリの基底クラスです(デフォルトでは無視されます)。                            |
+----------------------------------+---------------------------------------------------------------------------------------+
| :exc:`ImportWarning`             | モジュールのインポート処理中に引き起こされる                                          |
|                                  | 警告カテゴリの基底クラスです(デフォルトでは無視されます)。                            |
+----------------------------------+---------------------------------------------------------------------------------------+
| :exc:`UnicodeWarning`            | Unicode に関係した警告カテゴリの基底クラスです。                                      |
+----------------------------------+---------------------------------------------------------------------------------------+

これらは技術的には組み込み例外ですが、概念的には警告メカニズムに属しているのでここで記述されています。

標準の警告カテゴリをユーザの作成したコード上でサブクラス化することで、さらに別の警告カテゴリを定義することができます。警告カテゴリは常に
:exc:`Warning` クラスのサブクラスでなければなりません。


.. _warning-filter:

警告フィルタ
------------

警告フィルタは、ある警告を無視すべきか、表示すべきか、あるいは (例外を送出する) エラーにするべきかを制御します。

概念的には、警告フィルタは複数のフィルタ仕様からなる順番付けられたリストを維持しています; 何らかの特定の警告が生じると、フィルタ仕様の
一致するものが見つかるまで、リスト中の各フィルタとの照合が行われます; 一致したフィルタ仕様がその警告の処理方法を決定します。フィルタの各エントリは
(*action*, *message*, *category*, *module*, *lineno*) からなるタプルです。ここで:

* *action* は以下の文字列のうちの一つです:

  +---------------+-------------------------------------------------------------------------------------+
  | 値            | 処理方法                                                                            |
  +===============+=====================================================================================+
  | ``"error"``   | 一致した警告を例外に変えます                                                        |
  +---------------+-------------------------------------------------------------------------------------+
  | ``"ignore"``  | 一致した警告を決して出力しません                                                    |
  +---------------+-------------------------------------------------------------------------------------+
  | ``"always"``  | 一致した警告を常に出力します                                                        |
  +---------------+-------------------------------------------------------------------------------------+
  | ``"default"`` | 一致した警告のうち、警告の原因になった                                              |
  |               | ソースコード上の場所ごとに、最初の警告のみ出力します。                              |
  +---------------+-------------------------------------------------------------------------------------+
  | ``"module"``  | 一致した警告のうち、警告の原因になったモジュールごとに、最初の警告のみ出力します。  |
  +---------------+-------------------------------------------------------------------------------------+
  | ``"once"``    | 一致した警告のうち、警告の原因になった場所にかかわらず最初の警告のみ出力します。    |
  +---------------+-------------------------------------------------------------------------------------+

* *message* は正規表現を含む文字列で、メッセージはこのパタンに一致しなければなりません (照合時には常に大小文字の区別を
  しないようにコンパイルされます)。

* *category* はクラス (:exc:`Warning` のサブクラス) です。警告クラスはこのクラスのサブクラスに一致しなければなりません。

* *module* は正規表現を含む文字列で、モジュール名はこのパタンに一致しなければなりません (照合時には常に大小文字の区別を
  しないようにコンパイルされます)。

* *lineno* 整数で、警告が発生した場所の行番号に一致しなければなりません、すべての行に一致する場合には ``0`` になります。

:exc:`Warning` クラスは組み込みの :exc:`Exception` クラスから導出されているので、警告をエラーに変えるには単に
``category(message)`` を ``raise`` します。

警告フィルタは Python インタプリタのコマンドラインに渡される :option:`-W` オプションで初期化されます。インタプリタは
:option:`-W` オプションに渡される全ての引数を ``sys.warnoptions`` ; に変換せずに保存します; :mod:`warnings`
モジュールは最初に ``import`` された際にこれらの引数を解釈します (無効なオプションは ``sys.stderr`` にメッセージを出力した後
無視されます)。

デフォルトでは無視される警告を :option:`-Wd` をインタプリタに渡すことで有効にすることができます。このオプションは通常はデフォルトで無視さ
れるようなものを含む全ての警告のデフォルトでの扱いを有効化します。このような振る舞いは開発中のパッケージをインポートする問題をデバッグする時
にImportWarning を有効化するために使えます。ImportWarning は次のような Python
コードを使って明示的に有効化することもできます。 ::

   warnings.simplefilter('default', ImportWarning)

.. _warning-suppress:

一時的にwarningを抑制する
--------------------------------

.. If you are using code that you know will raise a warning, such as a deprecated
   function, but do not want to see the warning, then it is possible to suppress
   the warning using the :class:`catch_warnings` context manager::

廃止予定の関数など、warning を発生させる事を知っているコードを利用する場合に、
warningを表示したくないのであれば、 :class:`catch_warnings` コンテキストマネージャーを
使ってwarningを抑制することができます。 ::

    import warnings

    def fxn():
        warnings.warn("deprecated", DeprecationWarning)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()

.. While within the context manager all warnings will simply be ignored. This
   allows you to use known-deprecated code without having to see the warning while
   not suppressing the warning for other code that might not be aware of its use
   of deprecated code.

このサンプルのコンテキストマネージャーの中では、全てのwarningが無視されています。
これで、他の廃止予定のコードを含まない(つもりの)部分までwarningを抑止せずに、
廃止予定だと分かっているコードだけwarningを表示させないようにすることができます。


.. _warning-testing:

.. Testing Warnings

warning のテスト
----------------

.. To test warnings raised by code, use the :class:`catch_warnings` context
   manager. With it you can temporarily mutate the warnings filter to facilitate
   your testing. For instance, do the following to capture all raised warnings to
   check::

コードがwarningを発生させることをテストするには、 :class:`catch_warnings`
コンテキストマネージャーを利用します。
このくr巣を使うと、一時的にwarningフィルターを操作してテストに利用できます。
例えば、次のコードでは、全ての発生したwarningを取得してチェックしています。 ::

    import warnings

    def fxn():
        warnings.warn("deprecated", DeprecationWarning)

    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        # Trigger a warning.
        fxn()
        # Verify some things
        assert len(w) == 1
        assert isinstance(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)

.. One can also cause all warnings to be exceptions by using ``error`` instead of
   ``always``. One thing to be aware of is that if a warning has already been
   raised because of a ``once``/``default`` rule, then no matter what filters are
   set the warning will not be seen again unless the warnings registry related to
   the warning has been cleared.

``always`` の代わりに ``error`` を利用することで、全てのwarningで例外を発生させることができます。
1つ気をつけないといけないのは、1度 ``once``/``default`` ルールによって発生したwarningは、
フィルターに何をセットしているかにかかわらず、warnings registryをクリアしない限りは
2度と発生しません。

.. Once the context manager exits, the warnings filter is restored to its state
   when the context was entered. This prevents tests from changing the warnings
   filter in unexpected ways between tests and leading to indeterminate test
   results. The :func:`showwarning` function in the module is also restored to
   its original value.

コンテキストマネージャーが終了したら、warningフィルターはコンテキストマネージャーに\
入る前のものに戻されます。これは、テスト中に予期しない方法でwarningフィルターが変更され、
テスト結果が中途半端になる事を予防します。
このモジュールの :func:`showwarning` 関数も元の値に戻されます。

.. When testing multiple operations that raise the same kind of warning, it
   is important to test them in a manner that confirms each operation is raising
   a new warning (e.g. set warnings to be raised as exceptions and check the
   operations raise exceptions, check that the length of the warning list
   continues to increase after each operation, or else delete the previous
   entries from the warnings list before each new operation).

同じ種類のwarningを発生させる複数の操作をテストする場合、
各操作が新しいwarningを発生させている事を確認するのは大切な事です。
(例えば、warningを例外として発生させて各操作が例外を発生させることを確認したり、
warningリストの長さが各操作で増加していることを確認したり、
warningリストを各操作の前に毎回クリアする事ができます。)


.. _warning-functions:

利用可能な関数
--------------


.. function:: warn(message[, category[, stacklevel]])

   警告を発するか、無視するか、あるいは例外を送出します。 *category* 引数が与えられた場合、警告カテゴリクラスでなければなりません
   (上を参照してください); 標準の値は :exc:`UserWarning` です。 *message* を :exc:`Warning` インスタンスで代用する
   こともできますが、この場合 *category* は無視され、 ``message.__class__`` が使われ、メッセージ文は
   ``str(message)`` になります。発された例外が前述した警告フィルタによってエラーに変更された場合、この関数は例外を送出します。引数
   *stacklevel* は Python でラッパ関数を書く際に利用することができます。例えば::

      def deprecation(message):
          warnings.warn(message, DeprecationWarning, stacklevel=2)

   こうすることで、警告が参照するソースコード部分を、 :func:`deprecation` 自身ではなく :func:`deprecation` を
   呼び出した側にできます (というのも、前者の場合は警告メッセージの目的を台無しにしてしまうからです)。


.. function:: warn_explicit(message, category, filename, lineno[, module[, registry[, module_globals]]])

   :func:`warn` の機能に対する低レベルのインタフェースで、メッセージ、警告カテゴリ、ファイル名および行番号、そしてオプションの
   モジュール名およびレジストリ情報 (モジュールの  ``__warningregistry__`` 辞書) を明示的に渡します。モジュール名は標準で
   ``.py`` が取り去られたファイル名になります; レジストリが渡されなかった場合、警告が抑制されることはありません。 *message*
   は文字列のとき、 *category* は :exc:`Warning` のサブクラスでなければなりません。また *message* は
   :exc:`Warning` のインスタンスであってもよく、この場合 *category* は無視されます。

   *module_globals* は、もし与えられるならば、警告が発せられるコードが使っているグローバル名前空間でなければなりません。(この引数は
   zipfile やその他の非ファイルシステムのインポート元の中にあるモジュールのソースを表示することをサポートするためのものです)
   
   .. versionchanged:: 2.5
      *module_globals* 引数が追加されました


.. function:: warnpy3k(message[, category[, stacklevel]])

   .. Issue a warning related to Python 3.x deprecation. Warnings are only shown
      when Python is started with the -3 option. Like :func:`warn` *message* must
      be a string and *category* a subclass of :exc:`Warning`. :func:`warnpy3k`
      is using :exc:`DeprecationWarning` as default warning class.

   Python 3.x で廃止予定についてのwarningを発生させます。
   Pythonが -3 オプション付きで実行されているときのみwarningが表示されます。
   :func:`warn` と同じく、 *message* は文字列で、 *category* は :exc:`Warninp`
   のサブクラスである必要があります。
   :func:`warnpy3k` は :exc:`DeprecationWarning` をデフォルトのwarningクラスとして利用しています。


.. function:: showwarning(message, category, filename, lineno[, file[, line]])

   警告をファイルに書き込みます。標準の実装では、 ``formatwarning(message, category, filename, lineno, line)``
   を呼び出し、返された文字列を *file* に書き込みます。 *file* は標準では ``sys.stderr`` です。この関数は
   ``warnings.showwarning`` に別の実装を代入して置き換えることができます。
   *line* はwarningメッセージに含めるソースコードの1行です。
   *line* が与えられない場合、 :func:`showwarning` は *filename* と *lineno*
   から行を取得することを試みます。

   .. versionchanged:: 2.6
      .. Added the *line* argument. Implementations that lack the new argument
         will trigger a :exc:`DeprecationWarning`.
      *line* 引数が追加されました。
      新しい引数を使わない ``showwarning`` の実装は :exc:`DeprecationWarning` を発生させます。


.. function:: formatwarning(message, category, filename, lineno)

   警告を通常の方法で書式化します。返される文字列内には改行が埋め込まれている可能性があり、かつ文字列は改行で終端されています。
   *line* はwarningメッセージに含まれるソースコードの1行です。
   *line* が渡されない場合、 :func:`formatwarning` は *filename* と *fileno*
   から行の取得を試みます。

   .. versionchanged:: 2.6
      *line* 引数を追加しました。


.. function:: filterwarnings(action[, message[, category[, module[, lineno[, append]]]]])

   警告フィルタのリストにエントリを一つ挿入します。標準ではエントリは先頭に挿入されます; *append* が真ならば、末尾に挿入されます。
   この関数は引数の型をチェックし、 *message* および *module* の正規表現をコンパイルしてから、これらをタプルにして警告フィルタ
   のリストに挿入します。二つのエントリが特定の警告に合致した場合、リストの先頭に近い方のエントリが後方にあるエントリに優先します。
   引数が省略されると、標準では全てにマッチする値に設定されます。


.. function:: simplefilter(action[, category[, lineno[, append]]])

   単純なエントリを警告フィルタのリストに挿入します。引数の意味は :func:`filterwarnings` と同じですが、この関数により挿入されるフィ
   ルタはカテゴリと行番号が一致していれば全てのモジュールの全てのメッセージに合致しますので、正規表現は必要ありません。


.. function:: resetwarnings()

   警告フィルタをリセットします。これにより、 :option:`-W` コマンドラインオプションによるもの :func:`simplefilter`
   呼び出しによるものを含め、 :func:`filterwarnings` の呼び出しによる影響はすべて無効化されます。


.. Available Context Managers

利用可能なコンテキストマネージャー
------------------------------------

.. class:: catch_warnings([\*, record=False, module=None])

   .. A context manager that copies and, upon exit, restores the warnings filter
      and the :func:`showwarning` function.
      If the *record* argument is :const:`False` (the default) the context manager
      returns :class:`None` on entry. If *record* is :const:`True`, a list is
      returned that is progressively populated with objects as seen by a custom
      :func:`showwarning` function (which also suppresses output to ``sys.stdout``).
      Each object in the list has attributes with the same names as the arguments to
      :func:`showwarning`.

   コンテキストマネージャーで、warningフィルターと :func:`showwarning` 関数をコピーし、
   終了時にリストアします。
   *record* 引数が :const:`False` (デフォルト値)だった場合、エントリー時には :const:`None`
   を返します。もし *record* が :const:`True` だった場合、カスタムの :func:`showwarning`
   関数(この関数は同時に ``sys.stdout`` への出力を抑制します)によってオブジェクトが
   継続的に追加されるリストを返します。
   リストの中の各オブジェクトは、 :func:`showwarning` 関数の引数と同じ名前の属性を持っています。

   .. The *module* argument takes a module that will be used instead of the
      module returned when you import :mod:`warnings` whose filter will be
      protected. This argument exists primarily for testing the :mod:`warnings`
      module itself.

   *module* 引数は :mod:`warnings` を import して得られるオブジェクトの代わりに利用されます。
   このモジュールのフィルターは保護されます。
   この引数は、主に :mod:`warnings` モジュール自体をテストする目的で追加されました。

   .. note::
      .. In Python 3.0, the arguments to the constructor for
         :class:`catch_warnings` are keyword-only arguments.

      Python 3.0 では、 :class:`catch_warnings` コンストラクタの引数は keyword-only 引数です。

   .. versionadded:: 2.6

