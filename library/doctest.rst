:mod:`doctest` --- 対話モードを使った使用例の内容をテストする
=============================================================

.. module:: doctest
   :synopsis: docstring の中のテストコード.
.. moduleauthor:: Tim Peters <tim@python.org>
.. sectionauthor:: Tim Peters <tim@python.org>
.. sectionauthor:: Moshe Zadka <moshez@debian.org>
.. sectionauthor:: Edward Loper <edloper@users.sourceforge.net>


.. The :mod:`doctest` module searches for pieces of text that look like interactive
.. Python sessions, and then executes those sessions to verify that they work
.. exactly as shown.  There are several common ways to use doctest:

:mod:`doctest` モジュールは、対話的 Python セッションのように見えるテキストを探し出し、
セッションの内容を実行して、そこに書かれている通りに振舞うかを調べます。
:mod:`doctest` は以下のような用途によく使われています:


.. * To check that a module's docstrings are up-to-date by verifying that all
..   interactive examples still work as documented.

* モジュールの docstring (ドキュメンテーション文字列) 中にある対話モードでの使用例全てが書かれている通りに動作するかを検証することで、
  docstring の内容が最新のものになるよう保ちます。


.. * To perform regression testing by verifying that interactive examples from a
..   test file or a test object work as expected.

* テストファイルやテストオブジェクト中の対話モードにおける使用例が期待通りに動作するかを検証することで、
  回帰テストを実現します。


.. * To write tutorial documentation for a package, liberally illustrated with
..   input-output examples.  Depending on whether the examples or the expository text
..   are emphasized, this has the flavor of "literate testing" or "executable
..   documentation".

* 入出力例をふんだんに使ったパッケージのチュートリアルドキュメントを書けます。
  入出力例と解説文のどちらに注目するかによって、ドキュメントは「読めるテスト」にも「実行できるドキュメント」にもなります。


.. Here's a complete but small example module:

以下にちょっとした、それでいて完全な例を示します。


::

   """
   This is the "example" module.

   The example module supplies one function, factorial().  For example,

   >>> factorial(5)
   120
   """

   def factorial(n):
       """Return the factorial of n, an exact integer >= 0.

       If the result is small enough to fit in an int, return an int.
       Else return a long.

       >>> [factorial(n) for n in range(6)]
       [1, 1, 2, 6, 24, 120]
       >>> [factorial(long(n)) for n in range(6)]
       [1, 1, 2, 6, 24, 120]
       >>> factorial(30)
       265252859812191058636308480000000L
       >>> factorial(30L)
       265252859812191058636308480000000L
       >>> factorial(-1)
       Traceback (most recent call last):
           ...
       ValueError: n must be >= 0

       Factorials of floats are OK, but the float must be an exact integer:
       >>> factorial(30.1)
       Traceback (most recent call last):
           ...
       ValueError: n must be exact integer
       >>> factorial(30.0)
       265252859812191058636308480000000L

       It must also not be ridiculously large:
       >>> factorial(1e100)
       Traceback (most recent call last):
           ...
       OverflowError: n too large
       """

       import math
       if not n >= 0:
           raise ValueError("n must be >= 0")
       if math.floor(n) != n:
           raise ValueError("n must be exact integer")
       if n+1 == n:  # catch a value like 1e300
           raise OverflowError("n too large")
       result = 1
       factor = 2
       while factor <= n:
           result *= factor
           factor += 1
       return result


   if __name__ == "__main__":
       import doctest
       doctest.testmod()


.. If you run :file:`example.py` directly from the command line, :mod:`doctest`
.. works its magic:

:file:`example.py` をコマンドラインから直接実行すると、 :mod:`doctest` はその魔法を働かせます。


::

   $ python example.py
   $


.. There's no output!  That's normal, and it means all the examples worked.  Pass
.. :option:`-v` to the script, and :mod:`doctest` prints a detailed log of what
.. it's trying, and prints a summary at the end:

出力は何もありません！しかしこれが正常で、全ての例が正しく動作することを意味しています。
スクリプトに :option:`-v` を与えると、 :mod:`doctest`  は何を行おうとしているのかを記録した詳細なログを出力し、
最後にまとめを出力します。


::

   $ python example.py -v
   Trying:
       factorial(5)
   Expecting:
       120
   ok
   Trying:
       [factorial(n) for n in range(6)]
   Expecting:
       [1, 1, 2, 6, 24, 120]
   ok
   Trying:
       [factorial(long(n)) for n in range(6)]
   Expecting:
       [1, 1, 2, 6, 24, 120]
   ok


.. And so on, eventually ending with:

といった具合で、最後には


::

   Trying:
       factorial(1e100)
   Expecting:
       Traceback (most recent call last):
           ...
       OverflowError: n too large
   ok
   2 items passed all tests:
      1 tests in __main__
      8 tests in __main__.factorial
   9 tests in 2 items.
   9 passed and 0 failed.
   Test passed.
   $


.. That's all you need to know to start making productive use of :mod:`doctest`!
.. Jump in.  The following sections provide full details.  Note that there are many
.. examples of doctests in the standard Python test suite and libraries.
.. Especially useful examples can be found in the standard test file
.. :file:`Lib/test/test_doctest.py`.

これが、 :mod:`doctest` を使って生産性の向上を目指す上で知っておく必要があることの全てです！
さあやってみましょう。詳細な事柄は後続の各節で全て説明しています。
doctest の例は、標準の Python テストスイートやライブラリ中に沢山あります。
標準のテストファイル :file:`Lib/test/test_doctest.py`  には、特に便利な例題があります。


.. _doctest-simple-testmod:

簡単な利用法: docstring 中の例題をチェックする
----------------------------------------------

.. The simplest way to start using doctest (but not necessarily the way you'll
.. continue to do it) is to end each module :mod:`M` with:

doctest を試す簡単な方法、(とはいえ、いつもそうする必要はないのですが) は、
各モジュール :mod:`M` の最後を、以下のようにして締めくくるやりかたです。


::

   if __name__ == "__main__":
       import doctest
       doctest.testmod()


.. :mod:`doctest` then examines docstrings in module :mod:`M`.

こうすると、 :mod:`doctest` は :mod:`M` 中の docstring を検査します。


.. Running the module as a script causes the examples in the docstrings to get
.. executed and verified:

モジュールをスクリプトとして実行すると、docstring 中の例題が実行され、検証されます。


::

   python M.py


.. This won't display anything unless an example fails, in which case the failing
.. example(s) and the cause(s) of the failure(s) are printed to stdout, and the
.. final line of output is ``***Test Failed*** N failures.``, where *N* is the
.. number of examples that failed.

ドキュメンテーション文字列に書かれた例の実行が失敗しない限り、何も表示されません。
失敗すると、失敗した例と、その原因が (場合によっては複数) 標準出力に印字され、
最後に ``***Test Failed*** N failures.`` という行を出力します。ここで、 *N* は失敗した例題の数です。


.. Run it with the :option:`-v` switch instead:

一方、 :option:`-v` スイッチをつけて走らせると


::

   python M.py -v


.. and a detailed report of all examples tried is printed to standard output, along
.. with assorted summaries at the end.

実行を試みた全ての例について詳細に報告し、最後に各種まとめをおこなった内容が標準出力に印字されます。


.. You can force verbose mode by passing ``verbose=True`` to :func:`testmod`, or
.. prohibit it by passing ``verbose=False``.  In either of those cases,
.. ``sys.argv`` is not examined by :func:`testmod` (so passing :option:`-v` or not
.. has no effect).

``verbose=True`` を :func:`testmod` に渡せば、詳細報告 (verbose) モードを強制できます。また、
``verbose=False`` にすれば禁止できます。どちらの場合にも、 :func:`testmod` は ``sys.argv`` 上のスイッチ
を調べません。(従って、 :option:`-v` をつけても効果はありません)。


.. Since Python 2.6, there is also a command line shortcut for running
.. :func:`testmod`.  You can instruct the Python interpreter to run the doctest
.. module directly from the standard library and pass the module name(s) on the
.. command line:

Python 2.6 からは :func:`testmod` を実行するコマンドラインショートカットがあります。
Python インタプリタに doctest モジュールを標準ライブラリから直接実行して、テストする
モジュール名をコマンドライン引数に与えます。


::

   python -m doctest -v example.py


.. This will import :file:`example.py` as a standalone module and run
.. :func:`testmod` on it.  Note that this may not work correctly if the file is
.. part of a package and imports other submodules from that package.

こうすると :file:`example.py` を単体モジュールとしてインポートして、
それに対して :func:`testmod` を実行します。
このファイルがパッケージの一部で他のサブモジュールをそのパッケージからインポートしている場合は
うまく動かないことに注意してください。


.. For more information on :func:`testmod`, see section :ref:`doctest-basic-api`.

:func:`testmod` の詳しい情報は :ref:`doctest-basic-api` 節を参照してください。


.. _doctest-simple-testfile:

簡単な利用法: テキストファイル中の例題をチェックする
----------------------------------------------------

.. Another simple application of doctest is testing interactive examples in a text
.. file.  This can be done with the :func:`testfile` function:

doctest のもう一つの簡単な用途は、テキストファイル中にある対話操作の例に対するテストです。
これには :func:`testfile` 関数を使います。


::

   import doctest
   doctest.testfile("example.txt")


.. That short script executes and verifies any interactive Python examples
.. contained in the file :file:`example.txt`.  The file content is treated as if it
.. were a single giant docstring; the file doesn't need to contain a Python
.. program!   For example, perhaps :file:`example.txt` contains this:

この短いスクリプトは、 :file:`example.txt` というファイルの中に入っている対話モードの Python
操作例全てを実行して、その内容を検証します。
ファイルの内容は一つの巨大な docstring であるかのように扱われます; ファイルが Python
プログラムでなくてもよいのです！
例えば、 :file:`example.txt` には以下のような内容が入っているかもしれません。


::

   The ``example`` module
   ======================

   Using ``factorial``
   -------------------

   This is an example text file in reStructuredText format.  First import
   ``factorial`` from the ``example`` module:

       >>> from example import factorial

   Now use it:

       >>> factorial(6)
       120


.. Running ``doctest.testfile("example.txt")`` then finds the error in this
.. documentation:

``doctest.testfile("example.txt")`` を実行すると、このドキュメント内のエラーを見つけ出します。


::

   File "./example.txt", line 14, in example.txt
   Failed example:
       factorial(6)
   Expected:
       120
   Got:
       720


.. As with :func:`testmod`, :func:`testfile` won't display anything unless an
.. example fails.  If an example does fail, then the failing example(s) and the
.. cause(s) of the failure(s) are printed to stdout, using the same format as
.. :func:`testmod`.

:func:`testmod` と同じく、 :func:`testfile` は例題が失敗しない限り何も表示しません。
例題が失敗すると、失敗した例題とその原因が (場合によっては複数) :func:`testmod`
と同じ書式で標準出力に書き出されます。


.. By default, :func:`testfile` looks for files in the calling module's directory.
.. See section :ref:`doctest-basic-api` for a description of the optional arguments
.. that can be used to tell it to look for files in other locations.

デフォルトでは、 :func:`testfile` は自分自身を呼び出したモジュールのあるディレクトリを探します。
その他の場所にあるファイルを見に行くように :func:`testfile`
に指示するためのオプション引数についての説明は :ref:`doctest-basic-api`
節を参照してください。


.. Like :func:`testmod`, :func:`testfile`'s verbosity can be set with the
.. :option:`-v` command-line switch or with the optional keyword argument
.. *verbose*.

:func:`testmod` と同様に :func:`testfile` の冗長性 (verbosity) はコマンドラインスイッチ
:option:`-v` またはオプションのキーワード引数 *verbose* によって指定できます。


.. Since Python 2.6, there is also a command line shortcut for running
.. :func:`testfile`.  You can instruct the Python interpreter to run the doctest
.. module directly from the standard library and pass the file name(s) on the
.. command line:

Python 2.6 からは :func:`testfile` を実行するコマンドラインショートカットがあります。
Python インタプリタに doctest モジュールを標準ライブラリから直接実行して、テストする
モジュール名をコマンドライン引数に与えます。


::

   python -m doctest -v example.txt


.. Because the file name does not end with :file:`.py`, :mod:`doctest` infers that
.. it must be run with :func:`testfile`, not :func:`testmod`.

ファイル名が :file:`.py` で終っていないので、 :mod:`doctest` は :func:`testmod` ではなく
:func:`testfile` を使って実行するのだと判断します。


.. For more information on :func:`testfile`, see section :ref:`doctest-basic-api`.

:func:`testfile` の詳細は :ref:`doctest-basic-api` 節を参照してください。


.. _doctest-how-it-works:

doctest のからくり
------------------

.. This section examines in detail how doctest works: which docstrings it looks at,
.. how it finds interactive examples, what execution context it uses, how it
.. handles exceptions, and how option flags can be used to control its behavior.
.. This is the information that you need to know to write doctest examples; for
.. information about actually running doctest on these examples, see the following
.. sections.

この節では、doctest のからくり: どの docstring を見に行くのか、
どうやって対話操作例を見つけ出すのか、どんな実行コンテキストを使うのか、
例外をどう扱うか、上記の振る舞いを制御するためにどのようなオプションフラグを使うか、について詳しく吟味します。
こうした情報は、 doctest に対応した例題を書くために必要な知識です;
書いた例題に対して実際に doctest を実行する上で必要な情報については後続の節を参照してください。


.. _doctest-which-docstrings:

どのドキュメンテーション文字列が検証されるのか?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. The module docstring, and all function, class and method docstrings are
.. searched.  Objects imported into the module are not searched.

モジュールのドキュメンテーション文字列、全ての関数、クラスおよびメソッドのドキュメンテーション文字列が検索されます。
モジュールに import されたオブジェクトは検索されません。


.. In addition, if ``M.__test__`` exists and "is true", it must be a dict, and each
.. entry maps a (string) name to a function object, class object, or string.
.. Function and class object docstrings found from ``M.__test__`` are searched, and
.. strings are treated as if they were docstrings.  In output, a key ``K`` in
.. ``M.__test__`` appears with name :

加えて、 ``M.__test__`` が存在し、 "真の値を持つ" 場合、この値は辞書で、辞書の各エントリは (文字列の) 名前を
関数オブジェクト、クラスオブジェクト、または文字列に対応付けていなくてはなりません。
``M.__test__``  から得られた関数およびクラスオブジェクトのドキュメンテーション文字列は、
その名前がプライベートなものでも検索され、
文字列の場合にはそれがドキュメンテーション文字列であるかのように直接検索を行います。
出力においては、 ``M.__test__``  におけるキー ``K`` は、


::

   <name of M>.__test__.K


のように表示されます。


.. Any classes found are recursively searched similarly, to test docstrings in
.. their contained methods and nested classes.

検索中に見つかったクラスも同様に再帰的に検索が行われ、
クラスに含まれているメソッドおよびネストされたクラスについて
ドキュメンテーション文字列のテストが行われます。


.. .. versionchanged:: 2.4
..    A "private name" concept is deprecated and no longer documented.

.. versionchanged:: 2.4
   "プライベート名" の概念は撤廃されたため、今後はドキュメントにしません.


.. _doctest-finding-examples:

ドキュメンテーション文字列内の例をどうやって認識するのか?
---------------------------------------------------------

.. In most cases a copy-and-paste of an interactive console session works fine, but
.. doctest isn't trying to do an exact emulation of any specific Python shell.  All
.. hard tab characters are expanded to spaces, using 8-column tab stops.  If you
.. don't believe tabs should mean that, too bad:  don't use hard tabs, or write
.. your own :class:`DocTestParser` class.

ほとんどの場合、対話コンソールセッション上でのコピー／ペーストはうまく動作します。
とはいえ、 :mod:`doctest` は特定の Python シェルの振る舞いを正確にエミュレーションしようとするわけではありません。
ハードタブは全て 8 カラムのタブストップを使ってスペースに展開されます。
従って、タブがそのように表現されると考えておかないととまずいことになります:
その場合は、ハードタブを使わないか、自前で :class:`DocTestParser` クラスを書いてください。


.. .. versionchanged:: 2.4
..    Expanding tabs to spaces is new; previous versions tried to preserve hard tabs,
..    with confusing results.

.. versionchanged:: 2.4
   新たにタブをスペースに展開するようになりました; 以前のバージョンはハードタブを保存しようとしていたので、
   混乱させるようなテスト結果になってしまっていました.


::

   >>> # comments are ignored
   >>> x = 12
   >>> x
   12
   >>> if x == 13:
   ...     print "yes"
   ... else:
   ...     print "no"
   ...     print "NO"
   ...     print "NO!!!"
   ...
   no
   NO
   NO!!!
   >>>


.. Any expected output must immediately follow the final ``'>>> '`` or ``'... '``
.. line containing the code, and the expected output (if any) extends to the next
.. ``'>>> '`` or all-whitespace line.

出力結果例  (expected output) は、コードを含む最後の ``'>>> '`` or ``'... '`` 行の直下に続きます。
また、出力結果例 (がある場合) は、次の ``'>>> '`` 行か、全て空白文字の行まで続きます。


.. The fine print:

細かな注意:


.. * Expected output cannot contain an all-whitespace line, since such a line is
..   taken to signal the end of expected output.  If expected output does contain a
..   blank line, put ``<BLANKLINE>`` in your doctest example each place a blank line
..   is expected.

* 出力結果例には、全て空白の行が入っていてはなりません。
  そのような行は出力結果例の終了を表すと見なされるからです。
  もし予想出力結果の内容に空白行が入っている場合には、空白行が入るべき場所全てに ``<BLANKLINE>`` を入れてください。


  .. .. versionchanged:: 2.4
  ..    ``<BLANKLINE>`` was added; there was no way to use expected output containing
  ..    empty lines in previous versions.

  .. versionchanged:: 2.4
     ``<BLANKLINE>`` を追加しました; 以前のバージョンでは、空白行の入った予想出力結果を扱う方法がありませんでした.


.. * Output to stdout is captured, but not output to stderr (exception tracebacks
..   are captured via a different means).

* stdout への出力は取り込まれますが、stderr は取り込まれません (例外発生時のトレースバックは別の方法で取り込まれます)。


.. * If you continue a line via backslashing in an interactive session, or for any
..   other reason use a backslash, you should use a raw docstring, which will
..   preserve your backslashes exactly as you type them:

* 対話セッションにおいて、バックスラッシュを用いて次の行に続ける場合や、
  その他の理由でバックスラッシュを用いる場合、raw docstring を使って
  バックスラッシュを入力どおりに扱わせるようにせねばなりません。


  ::

     >>> def f(x):
     ...     r'''Backslashes in a raw docstring: m\n'''
     >>> print f.__doc__
     Backslashes in a raw docstring: m\n


  .. Otherwise, the backslash will be interpreted as part of the string. For example,
  .. the "\\" above would be interpreted as a newline character.  Alternatively, you
  .. can double each backslash in the doctest version (and not use a raw string):

  こうしなければ、バックスラッシュは文字列の一部として解釈されてしまいます。
  例えば、上の例の "\\" は改行文字として認識されてしまうでしょう。
  こうする代わりに、(raw docstring を使わずに) doctest 版の中ではバックスラッシュを全て二重にしてもかまいません。


  ::

     >>> def f(x):
     ...     '''Backslashes in a raw docstring: m\\n'''
     >>> print f.__doc__
     Backslashes in a raw docstring: m\n


.. * The starting column doesn't matter:

* 開始カラムはどこでもかまいません。


  ::

     >>> assert "Easy!"
           >>> import math
               >>> math.floor(1.9)
               1.0


  .. and as many leading whitespace characters are stripped from the expected output
  .. as appeared in the initial ``'>>> '`` line that started the example.

  出力結果例の先頭部にある空白文字列は、例題の開始部分にあたる ``'>>> '`` 行の先頭にある空白文字列と同じだけはぎとられます。


.. _doctest-execution-context:

実行コンテキストとは何か?
-------------------------

.. By default, each time :mod:`doctest` finds a docstring to test, it uses a
.. *shallow copy* of :mod:`M`'s globals, so that running tests doesn't change the
.. module's real globals, and so that one test in :mod:`M` can't leave behind
.. crumbs that accidentally allow another test to work.  This means examples can
.. freely use any names defined at top-level in :mod:`M`, and names defined earlier
.. in the docstring being run. Examples cannot see names defined in other
.. docstrings.

デフォルトでは、 :mod:`doctest` はテストを行うべき docstring を見つけるたびに
:mod:`M` のグローバル名前空間の *浅いコピー* を使い、
テストの実行によってモジュールの実際のグローバル名前空間を変更しないようにし、
かつ :mod:`M` 内で行ったテストが痕跡を残して偶発的に別のテストを誤って動作させないようにしています。
従って、例題中では :mod:`M` 内のトップレベルで定義されたすべての名前と、
docstring ドキュメンテーション文字列が動作する以前に定義された名前を自由に使えます。
個々の例題は他の docstring 中で定義された名前を参照できません。


.. You can force use of your own dict as the execution context by passing
.. ``globs=your_dict`` to :func:`testmod` or :func:`testfile` instead.

:func:`testmod` や :func:`testfile` に ``globs=your_dict`` を渡し、
自前の辞書を実行コンテキストとして使うこともできます。


.. _doctest-exceptions:

例外はどう扱えばよいのですか?
-----------------------------

.. No problem, provided that the traceback is the only output produced by the
.. example:  just paste in the traceback. [#]_ Since tracebacks contain details
.. that are likely to change rapidly (for example, exact file paths and line
.. numbers), this is one case where doctest works hard to be flexible in what it
.. accepts.

例で生成される出力がトレースバックのみである限り問題ありません:
単にトレースバックを貼り付けてください。 [#]_
トレースバックには、頻繁に変更されがちな情報が入っている (例えばファイルパスや行番号など) ものなので、
受け入れるべきテスト結果に柔軟性を持たせようと doctest が苦労している部分の一つです。


.. Simple example:

簡単な例を示しましょう。


::

   >>> [1, 2, 3].remove(42)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: list.remove(x): x not in list


.. That doctest succeeds if :exc:`ValueError` is raised, with the ``list.remove(x):
.. x not in list`` detail as shown.

この doctest は :exc:`ValueError` が送出され、かつ詳細情報に ``list.remove(x): x not in list``
が入っている場合にのみ成功します。


.. The expected output for an exception must start with a traceback header, which
.. may be either of the following two lines, indented the same as the first line of
.. the example:

例外が発生したときの予想出力はトレースバックヘッダから始まっていなければなりません。
トレースバックの形式は以下の二通りの行のいずれかでよく、
例題の最初の行と同じインデントでなければりません。


::

   Traceback (most recent call last):
   Traceback (innermost last):


.. The traceback header is followed by an optional traceback stack, whose contents
.. are ignored by doctest.  The traceback stack is typically omitted, or copied
.. verbatim from an interactive session.

トレースバックヘッダの後ろにトレースバックスタックを続けてもかまいませんが、
doctest はその内容を無視します。
普通はトレースバックスタックを無視するか、対話セッションからそのままコピーしてきます。


.. The traceback stack is followed by the most interesting part: the line(s)
.. containing the exception type and detail.  This is usually the last line of a
.. traceback, but can extend across multiple lines if the exception has a
.. multi-line detail:

トレースバックスタックの後ろにはもっとも有意義な部分、例外の型と詳細情報の入った行があります。
通常、この行はトレースバックの末尾にあるのですが、例外が複数行の詳細情報を持っている場合、
複数の行にわたることもあります。


::

   >>> raise ValueError('multi\n    line\ndetail')
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: multi
       line
   detail


.. The last three lines (starting with :exc:`ValueError`) are compared against the
.. exception's type and detail, and the rest are ignored.

上の例では、最後の 3 行 (:exc:`ValueError` から始まる行) における例外の型と詳細情報だけが比較され、
それ以外の部分は無視されます。


.. Best practice is to omit the traceback stack, unless it adds significant
.. documentation value to the example.  So the last example is probably better as:

例外を扱うコツは、例題をドキュメントとして読む上で明らかに価値のある情報でない限り、
トレースバックスタックは無視する、ということです。従って、先ほどの例は以下のように書くべきでしょう。


::

   >>> raise ValueError('multi\n    line\ndetail')
   Traceback (most recent call last):
       ...
   ValueError: multi
       line
   detail


.. Note that tracebacks are treated very specially.  In particular, in the
.. rewritten example, the use of ``...`` is independent of doctest's
.. :const:`ELLIPSIS` option.  The ellipsis in that example could be left out, or
.. could just as well be three (or three hundred) commas or digits, or an indented
.. transcript of a Monty Python skit.

トレースバックの扱いは非常に特殊なので注意してください。
特に、上の書き直した例題では、 ``...`` の扱いが doctest の
:const:`ELLIPSIS` オプションによって変わります。
この例での省略記号は何かの省略を表しているかもしれませんし、
コンマや数字が 3 個 (または 300 個) かもしれませんし、
Monty Python のスキットをインデントして書き写したものかもしれません。


.. Some details you should read once, but won't need to remember:

以下の詳細はずっと覚えておく必要はないのですが、一度目を通しておいてください:


.. * Doctest can't guess whether your expected output came from an exception
..   traceback or from ordinary printing.  So, e.g., an example that expects
..   ``ValueError: 42 is prime`` will pass whether :exc:`ValueError` is actually
..   raised or if the example merely prints that traceback text.  In practice,
..   ordinary output rarely begins with a traceback header line, so this doesn't
..   create real problems.

* doctest は予想出力の出所が print 文なのか例外なのかを推測できません。
  従って、例えば予想出力が ``ValueError: 42 is prime``  であるような例題は、
  :exc:`ValueError` が実際に送出された場合と、万が一予想出力と同じ文字列を
  print した場合の両方でパスしてしまいます。
  現実的には、通常の出力がトレースバックヘッダから始まることはないので、
  さしたる問題にはなりません。


.. * Each line of the traceback stack (if present) must be indented further than
..   the first line of the example, *or* start with a non-alphanumeric character.
..   The first line following the traceback header indented the same and starting
..   with an alphanumeric is taken to be the start of the exception detail.  Of
..   course this does the right thing for genuine tracebacks.

* トレースバックスタック (がある場合) の各行は、例題の最初の行よりも深くインデントされているか、
  *または* 英数文字以外で始まっていなければなりません。
  トレースバックヘッダ以後に現れる行のうち、インデントが等しく英数文字で始まる最初の行は
  例外の詳細情報が書かれた行とみなされるからです。
  もちろん、通常のトレースバックでは全く正しく動作します。


.. * When the :const:`IGNORE_EXCEPTION_DETAIL` doctest option is is specified,
..   everything following the leftmost colon is ignored.

* doctest のオプション :const:`IGNORE_EXCEPTION_DETAIL` を指定した場合、
  最も左端のコロン以後の内容が無視されます。


.. * The interactive shell omits the traceback header line for some
..   :exc:`SyntaxError`\ s.  But doctest uses the traceback header line to
..   distinguish exceptions from non-exceptions.  So in the rare case where you need
..   to test a :exc:`SyntaxError` that omits the traceback header, you will need to
..   manually add the traceback header line to your test example.

* 対話シェルでは、 :exc:`SyntaxError` の場合にトレースバックヘッダを無視することがあります。
  しかし doctest にとっては、例外を例外でないものと区別するためにトレースバックヘッダが必要です。
  そこで、トレースバックヘッダを省略するような :exc:`SyntaxError`
  をテストする必要があるというごく稀なケースでは、
  例題に自分で作ったトレースバックヘッダを追加する必要があるでしょう。


.. * For some :exc:`SyntaxError`\ s, Python displays the character position of the
..   syntax error, using a ``^`` marker:

* :exc:`SyntaxError` の場合、 Python は構文エラーの起きた場所を ``^`` マーカで表示します。


  ::

     >>> 1 1
       File "<stdin>", line 1
         1 1
           ^
     SyntaxError: invalid syntax


  .. Since the lines showing the position of the error come before the exception type
  .. and detail, they are not checked by doctest.  For example, the following test
  .. would pass, even though it puts the ``^`` marker in the wrong location:

  例外の型と詳細情報の前にエラー位置を示す行がくるため、 doctest はこの行を調べません。
  例えば、以下の例では、間違った場所に ``^`` マーカを入れてもパスしてしまいます。


  ::

     >>> 1 1
     Traceback (most recent call last):
       File "<stdin>", line 1
         1 1
         ^
     SyntaxError: invalid syntax


.. .. versionchanged:: 2.4
..    The ability to handle a multi-line exception detail, and the
..    :const:`IGNORE_EXCEPTION_DETAIL` doctest option, were added.

.. versionchanged:: 2.4
   複数行からなる例外の詳細情報を扱えるようにし、 doctest オプション :const:`IGNORE_EXCEPTION_DETAIL` を追加しました.


.. _doctest-options:

オプションフラグとディレクティブ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. A number of option flags control various aspects of doctest's behavior.
.. Symbolic names for the flags are supplied as module constants, which can be
.. or'ed together and passed to various functions.  The names can also be used in
.. doctest directives (see below).

doctest では、その挙動の様々な側面をたくさんのオプションフラグで制御しています。各フラグのシンボル名はモジュールの定数として提供されて
おり、論理和で組み合わせて様々な関数に渡せるようになっています。シンボル名は doctest のディレクティブ (directive, 下記参照) としても
使えます。


.. The first group of options define test semantics, controlling aspects of how
.. doctest decides whether actual output matches an example's expected output:

最初に説明するオプション群は、テストのセマンティクスを決めます。すなわち、実際にテストを実行したときの出力と例題中の予想出力とが一致しているかどうかを
doctest がどうやって判断するかを制御します:


.. data:: DONT_ACCEPT_TRUE_FOR_1

   .. By default, if an expected output block contains just ``1``, an actual output
   .. block containing just ``1`` or just ``True`` is considered to be a match, and
   .. similarly for ``0`` versus ``False``.  When :const:`DONT_ACCEPT_TRUE_FOR_1` is
   .. specified, neither substitution is allowed.  The default behavior caters to that
   .. Python changed the return type of many functions from integer to boolean;
   .. doctests expecting "little integer" output still work in these cases.  This
   .. option will probably go away, but not for several years.

   デフォルトでは、予想出力ブロックに単に ``1`` だけが入っており、実際の出力ブロックに ``1`` または ``True``
   だけが入っていた場合、これらの出力は一致しているとみなされます。
   ``0`` と ``False`` の場合も同様です。
   :const:`DONT_ACCEPT_TRUE_FOR_1` を指定すると、こうした値の読み替えを行いません。
   デフォルトの挙動で読み替えを行うのは、最近の Python で多くの関数の戻り値型が整数型からブール型に
   変更されたことに対応するためです; 読み替えを行う場合、"通常の整数" の出力を予想出力とするような
   doctest も動作します。このオプションはそのうち無くなるでしょうが、ここ数年はそのままでしょう。


.. data:: DONT_ACCEPT_BLANKLINE

   .. By default, if an expected output block contains a line containing only the
   .. string ``<BLANKLINE>``, then that line will match a blank line in the actual
   .. output.  Because a genuinely blank line delimits the expected output, this is
   .. the only way to communicate that a blank line is expected.  When
   .. :const:`DONT_ACCEPT_BLANKLINE` is specified, this substitution is not allowed.

   デフォルトでは、予想出力ブロックに ``<BLANKLINE>`` だけの入った行がある場合、
   その行は実際の出力における空行に一致するようになります。
   完全な空行を入れてしまうと予想出力がそこで終わっているとみなされてしまうため、
   空行を予想出力に入れたい場合にはこの方法を使わねばなりません。
   :const:`DONT_ACCEPT_BLANKLINE` を指定すると、 ``<BLANKLINE>`` の読み替えを行わなくなります。


.. data:: NORMALIZE_WHITESPACE

   .. When specified, all sequences of whitespace (blanks and newlines) are treated as
   .. equal.  Any sequence of whitespace within the expected output will match any
   .. sequence of whitespace within the actual output. By default, whitespace must
   .. match exactly. :const:`NORMALIZE_WHITESPACE` is especially useful when a line of
   .. expected output is very long, and you want to wrap it across multiple lines in
   .. your source.

   このフラグを指定すると、空白 (空白と改行文字) の列は互いに等価であるとみなします。
   予想出力における任意の空白列は実際の出力における任意の空白と一致します。
   デフォルトでは、空白は厳密に一致せねばなりません。
   :const:`NORMALIZE_WHITESPACE` は、予想出力の内容が非常に長いために、
   ソースコード中でその内容を複数行に折り返して書きたい場合に特に便利です。


.. data:: ELLIPSIS

   .. When specified, an ellipsis marker (``...``) in the expected output can match
   .. any substring in the actual output.  This includes substrings that span line
   .. boundaries, and empty substrings, so it's best to keep usage of this simple.
   .. Complicated uses can lead to the same kinds of "oops, it matched too much!"
   .. surprises that ``.*`` is prone to in regular expressions.

   このフラグを指定すると、予想出力中の省略記号マーカ (``...``)
   を実際の出力中の任意の部分文字列に一致させられます。
   部分文字列は行境界にわたるものや空文字列を含みます。
   従って、このフラグを使うのは単純な内容を対象にする場合にとどめましょう。
   複雑な使い方をすると、正規表現に ``.*`` を使ったときのように
   "あらら、省略部分をマッチがえてる (match too much) ！"  と驚くことになりかねません。


.. data:: IGNORE_EXCEPTION_DETAIL

   .. When specified, an example that expects an exception passes if an exception of
   .. the expected type is raised, even if the exception detail does not match.  For
   .. example, an example expecting ``ValueError: 42`` will pass if the actual
   .. exception raised is ``ValueError: 3*14``, but will fail, e.g., if
   .. :exc:`TypeError` is raised.

   このフラグを指定すると、予想される実行結果に例外が入るような例題で、
   予想通りの型の例外が送出された場合に、例外の詳細情報が一致していなくてもテストをパスさせます。
   例えば、予想出力が ``ValueError: 42`` であるような例題は、
   実際に送出された例外が ``ValueError: 3*14``  でもパスしますが、
   :exc:`TypeError` が送出されるといった場合にはパスしません。


   .. Note that a similar effect can be obtained using :const:`ELLIPSIS`, and
   .. :const:`IGNORE_EXCEPTION_DETAIL` may go away when Python releases prior to 2.4
   .. become uninteresting.  Until then, :const:`IGNORE_EXCEPTION_DETAIL` is the only
   .. clear way to write a doctest that doesn't care about the exception detail yet
   .. continues to pass under Python releases prior to 2.4 (doctest directives appear
   .. to be comments to them).  For example,

   :const:`ELLIPSIS` を使っても同様のことができ、 :const:`IGNORE_EXCEPTION_DETAIL`
   はリリース 2.4 以前の Python を使う人がほとんどいなくなった時期を見計らって
   撤廃するかもしれないので気をつけてください。
   それまでは、 :const:`IGNORE_EXCEPTION_DETAIL` は 2.4 以前の Python で
   例外の詳細については気にせずテストをパスさせるように
   doctest を書くための唯一の明確な方法です。例えば、


   ::

      >>> (1, 2)[3] = 'moo' #doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
        File "<stdin>", line 1, in ?
      TypeError: object doesn't support item assignment


   .. passes under Python 2.4 and Python 2.3.  The detail changed in 2.4, to say "does
   .. not" instead of "doesn't".

   にすると、 Python 2.4 と Python 2.3 の両方でテストをパスさせられます。
   というのは、例外の詳細情報は 2.4 で変更され、 "doesn't" から "does not" と書くようになったからです。


.. data:: SKIP

   .. When specified, do not run the example at all.  This can be useful in contexts
   .. where doctest examples serve as both documentation and test cases, and an
   .. example should be included for documentation purposes, but should not be
   .. checked.  E.g., the example's output might be random; or the example might
   .. depend on resources which would be unavailable to the test driver.

   このフラグを指定すると、例題は一切実行されません。
   こうした機能は doctest の実行例がドキュメントとテストを兼ねていて、
   ドキュメントのためには含めておかなければならないけれどチェックされなくても良い、
   というような文脈で役に立ちます。
   例えば、実行例の出力がランダムであるとか、
   テスト機構には手が届かない資源に依存している場合などです。


   .. The SKIP flag can also be used for temporarily "commenting out" examples.

   SKIP フラグは一時的に例題を"コメントアウト"するのにも使えます。


.. data:: COMPARISON_FLAGS

   .. A bitmask or'ing together all the comparison flags above.

   上記の比較フラグ全ての論理和をとったビットマスクです。


.. The second group of options controls how test failures are reported:

二つ目のオプション群は、テストの失敗を報告する方法を制御します:


.. data:: REPORT_UDIFF

   .. When specified, failures that involve multi-line expected and actual outputs are
   .. displayed using a unified diff.

   このオプションを指定すると、複数行にわたる予想出力や実際の出力を、一元化 (unified) diff を使って表示します。


.. data:: REPORT_CDIFF

   .. When specified, failures that involve multi-line expected and actual outputs
   .. will be displayed using a context diff.

   このオプションを指定すると、複数行にわたる予想出力や実際の出力を、コンテキスト diff を使って表示します。


.. data:: REPORT_NDIFF

   .. When specified, differences are computed by ``difflib.Differ``, using the same
   .. algorithm as the popular :file:`ndiff.py` utility. This is the only method that
   .. marks differences within lines as well as across lines.  For example, if a line
   .. of expected output contains digit ``1`` where actual output contains letter
   .. ``l``, a line is inserted with a caret marking the mismatching column positions.

   このオプションを指定すると、予想出力と実際の出力との間の差分をよく知られている :file:`ndiff.py`
   ユーティリティと同じアルゴリズムを使っている ``difflib.Differ`` で分析します。
   これは、行単位の差分と同じように行内の差分にマーカをつけられるようにする唯一の手段です。
   例えば、予想出力のある行に数字の ``1`` が入っていて、実際の出力には ``l`` が入っている場合、
   不一致のおきているカラム位置を示すキャレットの入った行が一行挿入されます。


.. data:: REPORT_ONLY_FIRST_FAILURE

   .. When specified, display the first failing example in each doctest, but suppress
   .. output for all remaining examples.  This will prevent doctest from reporting
   .. correct examples that break because of earlier failures; but it might also hide
   .. incorrect examples that fail independently of the first failure.  When
   .. :const:`REPORT_ONLY_FIRST_FAILURE` is specified, the remaining examples are
   .. still run, and still count towards the total number of failures reported; only
   .. the output is suppressed.

   このオプションを指定すると、各 doctest で最初にエラーの起きた例題だけを表示し、
   それ以後の例題の出力を抑制します。これにより、正しく書かれた例題が、
   それ以前の例題の失敗によっておかしくなってしまった場合に、
   doctest がそれを報告しないようになります。
   とはいえ、最初に失敗を引き起こした例題とは関係なく誤って書かれた例題の報告も抑制してしまいます。
   :const:`REPORT_ONLY_FIRST_FAILURE` を指定した場合、例題がどこかで失敗しても、
   それ以後の例題を続けて実行し、失敗したテストの総数を報告します; 出力が抑制されるだけです。


.. data:: REPORTING_FLAGS

   .. A bitmask or'ing together all the reporting flags above.

   上記のエラー報告に関するフラグ全ての論理和をとったビットマスクです。


.. "Doctest directives" may be used to modify the option flags for individual
.. examples.  Doctest directives are expressed as a special Python comment
.. following an example's source code:

「doctest ディレクティブ」を使うと、個々の例題に対してオプションフラグの設定を変更できます。 doctest ディレクティブは特殊な Python
コメント文として表現され、例題のソースコードの後に続けます:


.. productionlist:: doctest
   directive: "#" "doctest:" `directive_options`
   directive_options: `directive_option` ("," `directive_option`)\*
   directive_option: `on_or_off` `directive_option_name`
   on_or_off: "+" \| "-"
   directive_option_name: "DONT_ACCEPT_BLANKLINE" \| "NORMALIZE_WHITESPACE" \| ...


.. Whitespace is not allowed between the ``+`` or ``-`` and the directive option
.. name.  The directive option name can be any of the option flag names explained
.. above.

``+`` や ``-`` とディレクティブオプション名の間に空白を入れてはなりません。
ディレクティブオプション名は上で説明したオプションフラグ名のいずれかです。


.. An example's doctest directives modify doctest's behavior for that single
.. example.  Use ``+`` to enable the named behavior, or ``-`` to disable it.

ある例題の doctest ディレクティブは、その例題だけの doctest の振る舞いを変えます。
ある特定の挙動を有効にしたければ ``+`` を、無効にしたければ ``-`` を使います。


.. For example, this test passes:

例えば、以下のテストはパスします。


::

   >>> print range(20) #doctest: +NORMALIZE_WHITESPACE
   [0,   1,  2,  3,  4,  5,  6,  7,  8,  9,
   10,  11, 12, 13, 14, 15, 16, 17, 18, 19]


.. Without the directive it would fail, both because the actual output doesn't have
.. two blanks before the single-digit list elements, and because the actual output
.. is on a single line.  This test also passes, and also requires a directive to do
.. so:

ディレクティブがない場合、実際の出力には一桁の数字の間に二つスペースが入っていないこと、
実際の出力は 1 行になることから、テストはパスしないはずです。
別のディレクティブを使って、このテストをパスさせることもできます。


::

   >>> print range(20) # doctest:+ELLIPSIS
   [0, 1, ..., 18, 19]


.. Multiple directives can be used on a single physical line, separated by commas:

複数のディレクティブは、一つの物理行の中にコンマで区切って指定できます。


::

   >>> print range(20) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
   [0,    1, ...,   18,    19]


.. If multiple directive comments are used for a single example, then they are
.. combined:

一つの例題中で複数のディレクティブコメントを使った場合、それらは組み合わされます。


::

   >>> print range(20) # doctest: +ELLIPSIS
   ...                 # doctest: +NORMALIZE_WHITESPACE
   [0,    1, ...,   18,    19]


.. As the previous example shows, you can add ``...`` lines to your example
.. containing only directives.  This can be useful when an example is too long for
.. a directive to comfortably fit on the same line:

前の例題で示したように、 ``...`` の後ろにディレクティブだけの入った行を例題のうしろに追加して書けます。
この書きかたは、例題が長すぎるためにディレクティブを同じ行に入れると収まりが悪い場合に便利です。


::

   >>> print range(5) + range(10,20) + range(30,40) + range(50,60)
   ... # doctest: +ELLIPSIS
   [0, ..., 4, 10, ..., 19, 30, ..., 39, 50, ..., 59]


.. Note that since all options are disabled by default, and directives apply only
.. to the example they appear in, enabling options (via ``+`` in a directive) is
.. usually the only meaningful choice.  However, option flags can also be passed to
.. functions that run doctests, establishing different defaults.  In such cases,
.. disabling an option via ``-`` in a directive can be useful.

デフォルトでは全てのオプションが無効になっており、ディレクティブは特定の例題だけに影響を及ぼすので、
通常意味があるのは有効にするためのオプション(``+`` のついたディレクティブ) だけです。
とはいえ、 doctest を実行する関数はオプションフラグを指定してデフォルトとは異なった挙動を実現できるので、
そのような場合には ``-`` を使った無効化オプションも意味を持ちます。


.. .. versionchanged:: 2.4
..    Constants :const:`DONT_ACCEPT_BLANKLINE`, :const:`NORMALIZE_WHITESPACE`,
..    :const:`ELLIPSIS`, :const:`IGNORE_EXCEPTION_DETAIL`, :const:`REPORT_UDIFF`,
..    :const:`REPORT_CDIFF`, :const:`REPORT_NDIFF`,
..    :const:`REPORT_ONLY_FIRST_FAILURE`, :const:`COMPARISON_FLAGS` and
..    :const:`REPORTING_FLAGS` were added; by default ``<BLANKLINE>`` in expected
..    output matches an empty line in actual output; and doctest directives were
..    added.

.. versionchanged:: 2.4
   定数 :const:`DONT_ACCEPT_BLANKLINE`, :const:`NORMALIZE_WHITESPACE`,
   :const:`ELLIPSIS`, :const:`IGNORE_EXCEPTION_DETAIL`, :const:`REPORT_UDIFF`,
   :const:`REPORT_CDIFF`, :const:`REPORT_NDIFF`,
   :const:`REPORT_ONLY_FIRST_FAILURE`, :const:`COMPARISON_FLAGS`,
   :const:`REPORTING_FLAGS` を追加しました。予想出力中の ``<BLANKLINE>`` がデフォルトで
   実際の出力中の空行にマッチするようになりました。また、 doctest ディレクティブが追加されました.


.. .. versionchanged:: 2.5
..    Constant :const:`SKIP` was added.

.. versionchanged:: 2.5
   定数 :const:`SKIP` が追加されました.


.. There's also a way to register new option flag names, although this isn't useful
.. unless you intend to extend :mod:`doctest` internals via subclassing:

新たなオプションフラグ名を登録する方法もありますが、 :mod:`doctest` の内部をサブクラスで拡張しない限り、意味はないでしょう:


.. function:: register_optionflag(name)

   .. Create a new option flag with a given name, and return the new flag's integer
   .. value.  :func:`register_optionflag` can be used when subclassing
   .. :class:`OutputChecker` or :class:`DocTestRunner` to create new options that are
   .. supported by your subclasses.  :func:`register_optionflag` should always be
   .. called using the following idiom:

   名前 *name* の新たなオプションフラグを作成し、作成されたフラグの整数値を返します。
   :func:`register_optionflag` は :class:`OutputChecker` や  :class:`DocTestRunner` をサブクラス化して、
   その中で新たに作成したオプションをサポートさせる際に使います。
   :func:`register_optionflag` は以下のような定形文で呼び出さねばなりません。


   ::

      MY_FLAG = register_optionflag('MY_FLAG')

   .. versionadded:: 2.4


.. _doctest-warnings:

注意
^^^^

.. :mod:`doctest` is serious about requiring exact matches in expected output.  If
.. even a single character doesn't match, the test fails.  This will probably
.. surprise you a few times, as you learn exactly what Python does and doesn't
.. guarantee about output.  For example, when printing a dict, Python doesn't
.. guarantee that the key-value pairs will be printed in any particular order, so a
.. test like :

:mod:`doctest` では、予想出力に対する厳密な一致を厳しく求めています。
一致しない文字が一文字でもあると、テストは失敗してしまいます。
このため、Python が出力に関して何を保証していて、何を保証していないかを正確に知っていないと幾度か混乱させられることでしょう。
例えば、辞書を出力する際、Python はキーと値のペアが常に特定の順番で並ぶよう保証してはいません。従って、以下のようなテスト


::

   >>> foo()
   {"Hermione": "hippogryph", "Harry": "broomstick"}


.. is vulnerable!  One workaround is to do :

は失敗するかもしれないのです! 回避するには


::

   >>> foo() == {"Hermione": "hippogryph", "Harry": "broomstick"}
   True


.. instead.  Another is to do :

とするのが一つのやり方です。別のやり方は、


::

   >>> d = foo().items()
   >>> d.sort()
   >>> d
   [('Harry', 'broomstick'), ('Hermione', 'hippogryph')]


です。


.. There are others, but you get the idea.

他にもありますが、自分で考えてみてください。


.. Another bad idea is to print things that embed an object address, like :

以下のように、オブジェクトアドレスを埋め込むような結果を print するのもよくありません。


::

   >>> id(1.0) # certain to fail some of the time
   7948648
   >>> class C: pass
   >>> C()   # the default repr() for instances embeds an address
   <__main__.C instance at 0x00AC18F0>


.. The :const:`ELLIPSIS` directive gives a nice approach for the last example:

:const:`ELLIPSIS` ディレクティブを使うと、上のような例をうまく解決できます。


::

   >>> C() #doctest: +ELLIPSIS
   <__main__.C instance at 0x...>


.. Floating-point numbers are also subject to small output variations across
.. platforms, because Python defers to the platform C library for float formatting,
.. and C libraries vary widely in quality here. :

浮動小数点数もまた、プラットフォーム間での微妙な出力の違いの原因となります。
というのも、Python は浮動小数点の書式化をプラットフォームの  C ライブラリにゆだねており、
この点では、C ライブラリはプラットフォーム間で非常に大きく異なっているからです。


::

   >>> 1./7  # risky
   0.14285714285714285
   >>> print 1./7 # safer
   0.142857142857
   >>> print round(1./7, 6) # much safer
   0.142857


.. Numbers of the form ``I/2.**J`` are safe across all platforms, and I often
.. contrive doctest examples to produce numbers of that form:

``I/2.**J`` の形式になる数値はどのプラットフォームでもうまく動作するので、
私はこの形式の数値を生成するように doctest の例題を工夫しています。


::

   >>> 3./4  # utterly safe
   0.75


.. Simple fractions are also easier for people to understand, and that makes for
.. better documentation.

このように、単分数 (simple fraction) を使えば、人間にとっても理解しやすくよいドキュメントになります。


.. _doctest-basic-api:

基本 API
--------

.. The functions :func:`testmod` and :func:`testfile` provide a simple interface to
.. doctest that should be sufficient for most basic uses.  For a less formal
.. introduction to these two functions, see sections :ref:`doctest-simple-testmod`
.. and :ref:`doctest-simple-testfile`.

関数 :func:`testmod` および :func:`testfile` は、基本的なほとんどの用途に十分な doctest
インタフェースを提供しています。これら二つの関数についてもっとくだけた説明を読みたければ、
:ref:`doctest-simple-testmod` 節および :ref:`doctest-simple-testfile` 節を参照してください。


.. function:: testfile(filename[, module_relative][, name][, package][, globs][, verbose][, report][, optionflags][, extraglobs][, raise_on_error][, parser][, encoding])

   .. All arguments except *filename* are optional, and should be specified in keyword
   .. form.

   *filename* 以外の引数は全てオプションで、キーワード引数形式で指定せねばなりません。


   .. Test examples in the file named *filename*.  Return ``(failure_count,
   .. test_count)``.

   *filename* に指定したファイル内にある例題をテストします。 ``(failure_count, test_count)`` を返します。


   .. Optional argument *module_relative* specifies how the filename should be
   .. interpreted:

   オプション引数の *module_relative* は、ファイル名をどのように解釈するかを指定します:


   .. * If *module_relative* is ``True`` (the default), then *filename* specifies an
   ..   OS-independent module-relative path.  By default, this path is relative to the
   ..   calling module's directory; but if the *package* argument is specified, then it
   ..   is relative to that package.  To ensure OS-independence, *filename* should use
   ..   ``/`` characters to separate path segments, and may not be an absolute path
   ..   (i.e., it may not begin with ``/``).

   * *module_relative* が ``True`` (デフォルト) の場合、 *filename* は OS
     に依存しないモジュールの相対パスになります。デフォルトでは、このパスは関数 :func:`testfile` を呼び出して
     いるモジュールからの相対パスになります; ただし、 *package* 引数を指定した場合には、パッケージからの相対になります。
     OS への依存性を除くため、 *filename*  ではパスを分割する文字に ``/`` を使わねばならず、
     絶対パスにしてはなりません (パス文字列を ``/`` で始めてはなりません)。


   .. * If *module_relative* is ``False``, then *filename* specifies an OS-specific
   ..   path.  The path may be absolute or relative; relative paths are resolved with
   ..   respect to the current working directory.

   * *module_relative* が ``False`` の場合、 *filename* は OS 依存のパスを示します。
     パスは絶対パスでも相対パスでもかまいません; 相対パスにした場合、現在の作業ディレクトリを基準に解決します。


   .. Optional argument *name* gives the name of the test; by default, or if ``None``,
   .. ``os.path.basename(filename)`` is used.

   オプション引数 *name* には、テストの名前を指定します; デフォルトの場合や ``None`` を指定した場合、
   ``os.path.basename(filename)`` になります。


   .. Optional argument *package* is a Python package or the name of a Python package
   .. whose directory should be used as the base directory for a module-relative
   .. filename.  If no package is specified, then the calling module's directory is
   .. used as the base directory for module-relative filenames.  It is an error to
   .. specify *package* if *module_relative* is ``False``.

   オプション引数 *package* には、 Python パッケージを指定するか、モジュール相対のファイル名の場合には
   相対の基準ディレクトリとなる Python パッケージの名前を指定します。
   パッケージを指定しない場合、関数を呼び出しているモジュールのディレクトリを相対の基準ディレクトリとして使います。
   *module_relative* を ``False`` に指定している場合、 *package* を指定するとエラーになります。


   .. Optional argument *globs* gives a dict to be used as the globals when executing
   .. examples.  A new shallow copy of this dict is created for the doctest, so its
   .. examples start with a clean slate. By default, or if ``None``, a new empty dict
   .. is used.

   オプション引数 *globs* には辞書を指定します。この辞書は、例題を実行する際のグローバル変数として用いられます。
   doctest はこの辞書の浅いコピーを生成するので、例題は白紙の状態からスタートします。
   デフォルトの場合や ``None`` を指定した場合、新たな空の辞書になります。


   .. Optional argument *extraglobs* gives a dict merged into the globals used to
   .. execute examples.  This works like :meth:`dict.update`:  if *globs* and
   .. *extraglobs* have a common key, the associated value in *extraglobs* appears in
   .. the combined dict.  By default, or if ``None``, no extra globals are used.  This
   .. is an advanced feature that allows parameterization of doctests.  For example, a
   .. doctest can be written for a base class, using a generic name for the class,
   .. then reused to test any number of subclasses by passing an *extraglobs* dict
   .. mapping the generic name to the subclass to be tested.

   オプション引数 *extraglobs* には辞書を指定します。この辞書は、例題を実行する際にグローバル変数にマージされます。
   マージは :meth:`dict.update` のように振舞います: *globs* と *extraglobs* との間に同じキー値がある場合、両者を合わせた
   辞書中には *extraglobs* の方の値が入ります。この仕様は、パラメタ付きで doctest を実行するという、やや進んだ機能です。
   例えば、一般的な名前を使って基底クラス向けに doctest を書いておき、
   その後で辞書で一般的な名前からテストしたいサブクラスへの対応付けを行う辞書を *extraglobs* に渡して、
   様々なサブクラスをテストできます。


   .. Optional argument *verbose* prints lots of stuff if true, and prints only
   .. failures if false; by default, or if ``None``, it's true if and only if ``'-v'``
   .. is in ``sys.argv``.

   オプション引数 *verbose* が真の場合、様々な情報を出力します。偽の場合にはテストの失敗だけを報告します。
   デフォルトの場合や ``None`` を指定した場合、 ``sys.argv`` に ``-v`` を指定しない限りこの値は真になりません。


   .. Optional argument *report* prints a summary at the end when true, else prints
   .. nothing at the end.  In verbose mode, the summary is detailed, else the summary
   .. is very brief (in fact, empty if all tests passed).

   オプション引数 *report* が真の場合、テストの最後にサマリを出力します。
   それ以外の場合には何も出力しません。
   verbose モードの場合、サマリには詳細な情報を出力しますが、
   そうでない場合にはサマリはとても簡潔になります (実際には、全てのテストが成功した場合には何も出力しません)。


   .. Optional argument *optionflags* or's together option flags.  See section
   .. :ref:`doctest-options`.

   オプション引数 *optionflags* は、各オプションフラグの論理和をとった値を指定します。 :ref:`doctest-options`
   節を参照してください。


   .. Optional argument *raise_on_error* defaults to false.  If true, an exception is
   .. raised upon the first failure or unexpected exception in an example.  This
   .. allows failures to be post-mortem debugged. Default behavior is to continue
   .. running examples.

   オプション引数 *raise_on_error* の値はデフォルトでは偽です。
   真にすると、最初のテスト失敗や予期しない例外が起きたときに例外を送出します。
   このオプションを使うと、失敗の原因を検死デバッグ (post-mortem debug) できます。
   デフォルトの動作では、例題の実行を継続します。


   .. Optional argument *parser* specifies a :class:`DocTestParser` (or subclass) that
   .. should be used to extract tests from the files.  It defaults to a normal parser
   .. (i.e., ``DocTestParser()``).

   オプション引数 *parser* には、 :class:`DocTestParser` (またはそのサブクラス) を指定します。
   このクラスはファイルから例題を抽出するために使われます。デフォルトでは通常のパーザ  (``DocTestParser()``) です。


   .. Optional argument *encoding* specifies an encoding that should be used to
   .. convert the file to unicode.

   オプション引数 *encoding* にはファイルをユニコードに変換する際に使われるエンコーディングを指定します。


   .. versionadded:: 2.4


   .. .. versionchanged:: 2.5
   ..    The parameter *encoding* was added.

   .. versionchanged:: 2.5
      *encoding* パラメタが追加されました.


.. function:: testmod([m][, name][, globs][, verbose][, report][, optionflags][, extraglobs][, raise_on_error][, exclude_empty])

   .. All arguments are optional, and all except for *m* should be specified in
   .. keyword form.

   引数は全てオプションで、 *m* 以外の引数はキーワード引数として指定せねばなりません。


   .. Test examples in docstrings in functions and classes reachable from module *m*
   .. (or module :mod:`__main__` if *m* is not supplied or is ``None``), starting with
   .. ``m.__doc__``.

   モジュール *m* (*m* を指定しないか ``None`` にした場合には :mod:`__main__`) から到達可能な関数およびクラスの
   docstring 内にある例題をテストします。 ``m.__doc__`` 内の例題からテストを開始します。


   .. Also test examples reachable from dict ``m.__test__``, if it exists and is not
   .. ``None``.  ``m.__test__`` maps names (strings) to functions, classes and
   .. strings; function and class docstrings are searched for examples; strings are
   .. searched directly, as if they were docstrings.

   また、辞書 ``m.__test__`` が存在し、 ``None``  でない場合、この辞書から到達できる例題もテストします。
   ``m.__test__`` は、(文字列の) 名前から関数、クラスおよび文字列への対応付けを行っています。
   関数およびクラスの場合には、その docstring 内から例題を検索します。
   文字列の場合には、docstring と同じようにして例題の検索を直接実行します。


   .. Only docstrings attached to objects belonging to module *m* are searched.

   モジュール *m* に属するオブジェクトにつけられた docstrings のみを検索します。


   .. Return ``(failure_count, test_count)``.

   ``(failure_count, test_count)`` を返します。


   .. Optional argument *name* gives the name of the module; by default, or if
   .. ``None``, ``m.__name__`` is used.

   オプション引数 *name* には、モジュールの名前を指定します。デフォルトの場合や ``None`` を指定した場合には、
   ``m.__name__`` を使います。


   .. Optional argument *exclude_empty* defaults to false.  If true, objects for which
   .. no doctests are found are excluded from consideration. The default is a backward
   .. compatibility hack, so that code still using :meth:`doctest.master.summarize` in
   .. conjunction with :func:`testmod` continues to get output for objects with no
   .. tests. The *exclude_empty* argument to the newer :class:`DocTestFinder`
   .. constructor defaults to true.

   オプション引数 *exclude_empty* はデフォルトでは偽になっています。
   この値を真にすると、doctest を持たないオブジェクトを考慮から外します。
   デフォルトの設定は依存のバージョンとの互換性を考えたハックであり、 :meth:`doctest.master.summarize` と
   :func:`testmod` を合わせて利用しているようなコードでも、
   テスト例題を持たないオブジェクトから出力を得るようにしています。
   新たに追加された :class:`DocTestFinder` のコンストラクタの *exclude_empty* はデフォルトで真になります。


   .. Optional arguments *extraglobs*, *verbose*, *report*, *optionflags*,
   .. *raise_on_error*, and *globs* are the same as for function :func:`testfile`
   .. above, except that *globs* defaults to ``m.__dict__``.

   オプション引数 *extraglobs*, *verbose*, *report*, *optionflags*, *raise_on_error*, および
   *globs* は上で説明した :func:`testfile` の引数と同じです。ただし、 *globs* のデフォルト値は ``m.__dict__``
   になります。


   .. .. versionchanged:: 2.3
   ..    The parameter *optionflags* was added.

   .. versionchanged:: 2.3
      *optionflags* パラメタを追加しました.


   .. .. versionchanged:: 2.4
   ..    The parameters *extraglobs*, *raise_on_error* and *exclude_empty* were added.

   .. versionchanged:: 2.4
      *extraglobs*, *raise_on_error* および *exclude_empty* パラメタを追加しました.


   .. .. versionchanged:: 2.5
   ..    The optional argument *isprivate*, deprecated in 2.4, was removed.

   .. versionchanged:: 2.5
      オプション引数 *isprivate* は、2.4 では非推奨でしたが、廃止されました.


.. There's also a function to run the doctests associated with a single object.
.. This function is provided for backward compatibility.  There are no plans to
.. deprecate it, but it's rarely useful:

単一のオブジェクトに関連付けられた doctest を実行するための関数もあります。
この関数は以前のバージョンとの互換性のために提供されています。
この関数を撤廃する予定はありませんが、役に立つことはほとんどありません:


.. function:: run_docstring_examples(f, globs[, verbose][, name][, compileflags][, optionflags])

   .. Test examples associated with object *f*; for example, *f* may be a module,
   .. function, or class object.

   オブジェクト *f* に関連付けられた例題をテストします。 *f* はモジュール、関数、またはクラスオブジェクトです。


   .. A shallow copy of dictionary argument *globs* is used for the execution context.

   引数 *globs* に辞書を指定すると、その浅いコピーを実行コンテキストに使います。


   .. Optional argument *name* is used in failure messages, and defaults to
   .. ``"NoName"``.

   オプション引数 *name* はテスト失敗時のメッセージに使われます。デフォルトの値は ``NoName`` です。


   .. If optional argument *verbose* is true, output is generated even if there are no
   .. failures.  By default, output is generated only in case of an example failure.

   オプション引数 *verbose* の値を真にすると、テストが失敗しなくても出力を生成します。
   デフォルトでは、例題のテストに失敗したときのみ出力を生成します。


   .. Optional argument *compileflags* gives the set of flags that should be used by
   .. the Python compiler when running the examples.  By default, or if ``None``,
   .. flags are deduced corresponding to the set of future features found in *globs*.

   オプション引数 *compileflags* には、例題を実行するときに Python バイトコードコンパイラが使うフラグを指定します。
   デフォルトの場合や ``None`` を指定した場合、フラグは *globs* 内にある future 機能セットに対応したものになります。


   .. Optional argument *optionflags* works as for function :func:`testfile` above.

   オプション引数 *optionflags* は、上で述べた :func:`testfile` と同様の働きをします。


.. _doctest-unittest-api:

単位テスト API
--------------

.. As your collection of doctest'ed modules grows, you'll want a way to run all
.. their doctests systematically.  Prior to Python 2.4, :mod:`doctest` had a barely
.. documented :class:`Tester` class that supplied a rudimentary way to combine
.. doctests from multiple modules. :class:`Tester` was feeble, and in practice most
.. serious Python testing frameworks build on the :mod:`unittest` module, which
.. supplies many flexible ways to combine tests from multiple sources.  So, in
.. Python 2.4, :mod:`doctest`'s :class:`Tester` class is deprecated, and
.. :mod:`doctest` provides two functions that can be used to create :mod:`unittest`
.. test suites from modules and text files containing doctests.  These test suites
.. can then be run using :mod:`unittest` test runners:

doctest 化したモジュールのコレクションが増えるにつれ、全ての doctest
をシステマティックに実行したいと思うようになるはずです。
Python 2.4  以前の :mod:`doctest` には :class:`Tester`
というほとんどドキュメント化されていないクラスがあり、
複数のモジュールの doctest を統合する初歩的な手段を提供していました。
:class:`Tester` は非力であり、実際のところ、もっときちんとした Python
のテストフレームワークが :mod:`unittest` モジュールで構築されており、
複数のソースコードからのテストを統合する柔軟な方法を提供しています。
そこで Python 2.4 では :mod:`doctest` の :class:`Tester` クラスを撤廃し、
モジュールや doctest の入ったテキストファイルから :mod:`unittest`
テストスイートを作成できるような二つの関数を :mod:`doctest` 側で提供するようにしました。
こうしたテストスイートは、 :mod:`unittest` のテストランナを使って実行できます。


::

   import unittest
   import doctest
   import my_module_with_doctests, and_another

   suite = unittest.TestSuite()
   for mod in my_module_with_doctests, and_another:
       suite.addTest(doctest.DocTestSuite(mod))
   runner = unittest.TextTestRunner()
   runner.run(suite)


.. There are two main functions for creating :class:`unittest.TestSuite` instances
.. from text files and modules with doctests:

doctest の入ったテキストファイルやモジュールから :class:`unittest.TestSuite` インスタンスを生成するための
主な関数は二つあります:


.. function:: DocFileSuite(*paths, [module_relative][, package][, setUp][, tearDown][, globs][, optionflags][, parser][, encoding])

   .. Convert doctest tests from one or more text files to a
   .. :class:`unittest.TestSuite`.

   単一または複数のテキストファイルに入っている doctest 形式のテストを、 :class:`unittest.TestSuite`
   インスタンスに変換します。


   .. The returned :class:`unittest.TestSuite` is to be run by the unittest framework
   .. and runs the interactive examples in each file.  If an example in any file
   .. fails, then the synthesized unit test fails, and a :exc:`failureException`
   .. exception is raised showing the name of the file containing the test and a
   .. (sometimes approximate) line number.

   この関数の返す :class:`unittest.TestSuite` インスタンスは、 unittest
   フレームワークで動作させ、各ファイルの例題を対話的に実行するためのものです。
   ファイル内の何らかの例題の実行に失敗すると、この関数で生成した単位テストは失敗し、
   該当するテストの入っているファイルの名前と、 (場合によりだいたいの) 行番号の入った :exc:`failureException`
   例外を送出します。


   .. Pass one or more paths (as strings) to text files to be examined.

   関数には、テストを行いたい一つまたは複数のファイルへのパスを (文字列で) 渡します。


   .. Options may be provided as keyword arguments:

   :func:`DocFileSuite` には、キーワード引数でオプションを指定できます:


   .. Optional argument *module_relative* specifies how the filenames in *paths*
   .. should be interpreted:

   オプション引数 *module_relative* は *paths* に指定したファイル名をどのように解釈するかを指定します:


   .. * If *module_relative* is ``True`` (the default), then each filename in
   ..   *paths* specifies an OS-independent module-relative path.  By default, this
   ..   path is relative to the calling module's directory; but if the *package*
   ..   argument is specified, then it is relative to that package.  To ensure
   ..   OS-independence, each filename should use ``/`` characters to separate path
   ..   segments, and may not be an absolute path (i.e., it may not begin with
   ..   ``/``).

   * *module_relative* が ``True`` (デフォルト) の場合、 *filename* は OS
     に依存しないモジュールの相対パスになります。デフォルトでは、このパスは関数 :func:`testfile` を呼び出して
     いるモジュールからの相対パスになります; ただし、 *package* 引数を指定した場合には、
     パッケージからの相対になります。 OS への依存性を除くため、 *filename* ではパスを分割する文字に
     ``/`` を使わねばならず、絶対パスにしてはなりません (パス文字列を ``/`` で始めてはなりません)。


   .. * If *module_relative* is ``False``, then each filename in *paths* specifies
   ..   an OS-specific path.  The path may be absolute or relative; relative paths
   ..   are resolved with respect to the current working directory.

   * *module_relative* が ``False`` の場合、 *filename* は OS 依存のパスを示します。パスは絶対パスでも相対パスでも
     かまいません; 相対パスにした場合、現在の作業ディレクトリを基準に解決します。


   .. Optional argument *package* is a Python package or the name of a Python
   .. package whose directory should be used as the base directory for
   .. module-relative filenames in *paths*.  If no package is specified, then the
   .. calling module's directory is used as the base directory for module-relative
   .. filenames.  It is an error to specify *package* if *module_relative* is
   .. ``False``.

   オプション引数 *package* には、 Python パッケージを指定するか、
   モジュール相対のファイル名の場合には相対の基準ディレクトリとなる Python パッケージの名前を指定します。
   パッケージを指定しない倍、関数を呼び出しているモジュールのディレクトリを相対の基準ディレクトリとして使います。
   *module_relative* を ``False`` に指定している場合、 *package* を指定するとエラーになります。


   .. Optional argument *setUp* specifies a set-up function for the test suite.
   .. This is called before running the tests in each file.  The *setUp* function
   .. will be passed a :class:`DocTest` object.  The setUp function can access the
   .. test globals as the *globs* attribute of the test passed.

   オプション引数 *setUp* には、テストスイートのセットアップに使う関数を指定します。
   この関数は、各ファイルのテストを実行する前に呼び出されます。
   *setUp* 関数は :class:`DocTest` オブジェクトに引き渡されます。
   *setUp* は *globs* 属性を介してテストのグローバル変数にアクセスできます。


   .. Optional argument *tearDown* specifies a tear-down function for the test
   .. suite.  This is called after running the tests in each file.  The *tearDown*
   .. function will be passed a :class:`DocTest` object.  The setUp function can
   .. access the test globals as the *globs* attribute of the test passed.

   オプション引数 *tearDown* には、テストを解体 (tear-down) するための関数を指定します。
   この関数は、各ファイルのテストの実行を終了するたびに呼び出されます。
   *tearDown* 関数は :class:`DocTest`  オブジェクトに引き渡されます。
   *tearDown* は *globs* 属性を介してテストのグローバル変数にアクセスできます。


   .. Optional argument *globs* is a dictionary containing the initial global
   .. variables for the tests.  A new copy of this dictionary is created for each
   .. test.  By default, *globs* is a new empty dictionary.

   オプション引数 *globs* は辞書で、テストのグローバル変数の初期値が入ります。
   この辞書は各テストごとに新たにコピーして使われます。
   デフォルトでは *globs* は空の新たな辞書です。


   .. Optional argument *optionflags* specifies the default doctest options for the
   .. tests, created by or-ing together individual option flags.  See section
   .. :ref:`doctest-options`. See function :func:`set_unittest_reportflags` below
   .. for a better way to set reporting options.

   オプション引数 *optionflags* には、テストを実行する際にデフォルトで適用される
   doctest オプションを OR で結合して指定します。
   :ref:`doctest-options` 節を参照してください。
   結果レポートに関するオプションの指定する上手いやり方は下記の :func:`set_unittest_reportflags`
   の説明を参照してください。


   .. Optional argument *parser* specifies a :class:`DocTestParser` (or subclass)
   .. that should be used to extract tests from the files.  It defaults to a normal
   .. parser (i.e., ``DocTestParser()``).

   オプション引数 *parser* には、ファイルからテストを抽出するために使う :class:`DocTestParser` (またはサブクラス)
   を指定します。デフォルトは通常のパーザ (``DocTestParser()``) です。


   .. Optional argument *encoding* specifies an encoding that should be used to
   .. convert the file to unicode.

   オプション引数 *encoding* にはファイルをユニコードに変換する際に使われるエンコーディングを指定します。


   .. versionadded:: 2.4


   .. .. versionchanged:: 2.5
   ..    The global ``__file__`` was added to the globals provided to doctests
   ..    loaded from a text file using :func:`DocFileSuite`.

   .. versionchanged:: 2.5
      グローバル変数 ``__file__`` が追加され :func:`DocFileSuite` を使ってテキストファイルから読み込まれた doctest
      に提供されます.


   .. .. versionchanged:: 2.5
   ..    The parameter *encoding* was added.

   .. versionchanged:: 2.5
      *encoding* パラメタが追加されました.


.. function:: DocTestSuite([module][, globs][, extraglobs][, test_finder][, setUp][, tearDown][, checker])

   .. Convert doctest tests for a module to a :class:`unittest.TestSuite`.

   doctest のテストを :class:`unittest.TestSuite` に変換します。


   .. The returned :class:`unittest.TestSuite` is to be run by the unittest framework
   .. and runs each doctest in the module.  If any of the doctests fail, then the
   .. synthesized unit test fails, and a :exc:`failureException` exception is raised
   .. showing the name of the file containing the test and a (sometimes approximate)
   .. line number.

   この関数の返す :class:`unittest.TestSuite` インスタンスは、 unittest フレームワークで動作させ、モジュール内の各
   doctest を実行するためのものです。何らかの doctest の実行に失敗すると、この関数で
   生成した単位テストは失敗し、該当するテストの入っているファイルの名前と、 (場合によりだいたいの) 行番号の入った :exc:`failureException`
   例外を送出します。


   .. Optional argument *module* provides the module to be tested.  It can be a module
   .. object or a (possibly dotted) module name.  If not specified, the module calling
   .. this function is used.

   オプション引数 *module* には、テストしたいモジュールの名前を指定します。 *module* にはモジュールオブジェクトまたは (ドット表記の)
   モジュール名を指定できます。 *module* を指定しない場合、この関数を呼び出しているモジュールになります。


   .. Optional argument *globs* is a dictionary containing the initial global
   .. variables for the tests.  A new copy of this dictionary is created for each
   .. test.  By default, *globs* is a new empty dictionary.

   オプション引数 *globs* は辞書で、テストのグローバル変数の初期値が入ります。この辞書は各テストごとに新たにコピーして使われ
   ます。デフォルトでは *glob* は空の新たな辞書です。


   .. Optional argument *extraglobs* specifies an extra set of global variables, which
   .. is merged into *globs*.  By default, no extra globals are used.

   オプション引数 *extraglobs* には追加のグローバル変数セットを指定します。この変数セットは *globs* に統合されます。
   デフォルトでは、追加のグローバル変数はありません。


   .. Optional argument *test_finder* is the :class:`DocTestFinder` object (or a
   .. drop-in replacement) that is used to extract doctests from the module.

   オプション引数 *test_finder* は、モジュールから doctest を抽出するための :class:`DocTestFinder` オブジェクト
   (またはその代用となるオブジェクト) です。


   .. Optional arguments *setUp*, *tearDown*, and *optionflags* are the same as for
   .. function :func:`DocFileSuite` above.

   オプション引数 *setUp* 、 *tearDown* 、および *optionflags* は上の :func:`DocFileSuite` と同じです。


   .. versionadded:: 2.3


   .. .. versionchanged:: 2.4
   ..    The parameters *globs*, *extraglobs*, *test_finder*, *setUp*, *tearDown*, and
   ..    *optionflags* were added; this function now uses the same search technique as
   ..    :func:`testmod`.

   .. versionchanged:: 2.4
      *globs*, *extraglobs*, *test_finder*, *setUp*, *tearDown*, および *optionflags*
      パラメタを追加しました。また、この関数は doctest の検索に :func:`testmod` と同じテクニックを使うようになりました.


.. Under the covers, :func:`DocTestSuite` creates a :class:`unittest.TestSuite` out
.. of :class:`doctest.DocTestCase` instances, and :class:`DocTestCase` is a
.. subclass of :class:`unittest.TestCase`. :class:`DocTestCase` isn't documented
.. here (it's an internal detail), but studying its code can answer questions about
.. the exact details of :mod:`unittest` integration.

:func:`DocTestSuite` は水面下では :class:`doctest.DocTestCase`
インスタンスから :class:`unittest.TestSuite` を作成しており、 :class:`DocTestCase`
は :class:`unittest.TestCase` のサブクラスになっています。 :class:`DocTestCase` についてはここでは説明しません
(これは内部実装上の詳細だからです) が、そのコードを調べてみれば、 :mod:`unittest` の組み込みの詳細に関する疑問を解決できるはずです。


.. Similarly, :func:`DocFileSuite` creates a :class:`unittest.TestSuite` out of
.. :class:`doctest.DocFileCase` instances, and :class:`DocFileCase` is a subclass
.. of :class:`DocTestCase`.

同様に、 :func:`DocFileSuite` は :class:`doctest.DocFileCase`
インスタンスから :class:`unittest.TestSuite` を作成し、 :class:`DocFileCase` は
:class:`DocTestCase` のサブクラスになっています。


.. So both ways of creating a :class:`unittest.TestSuite` run instances of
.. :class:`DocTestCase`.  This is important for a subtle reason: when you run
.. :mod:`doctest` functions yourself, you can control the :mod:`doctest` options in
.. use directly, by passing option flags to :mod:`doctest` functions.  However, if
.. you're writing a :mod:`unittest` framework, :mod:`unittest` ultimately controls
.. when and how tests get run.  The framework author typically wants to control
.. :mod:`doctest` reporting options (perhaps, e.g., specified by command line
.. options), but there's no way to pass options through :mod:`unittest` to
.. :mod:`doctest` test runners.

これにははっきりとした訳があります: :mod:`doctest`
関数を自分で実行する場合、オプションフラグを :mod:`doctest` 関数に渡すことで、 :mod:`doctest`
のオプションを直接操作できます。しかしながら、 :mod:`unittest` フレームワークを書いている場合には、いつどのようにテストを動作させるかを
:mod:`unittest` が完全に制御してしまいます。フレームワークの作者はたいてい、 :mod:`doctest` のレポートオプションを
(コマンドラインオプションで指定するなどして) 操作したいと考えますが、 :mod:`unittest` を介して :mod:`doctest`
のテストランナにオプションを渡す方法は存在しないのです。


.. For this reason, :mod:`doctest` also supports a notion of :mod:`doctest`
.. reporting flags specific to :mod:`unittest` support, via this function:

このため、 :mod:`doctest` では、以下の関数を使って、 :mod:`unittest` サポート
に特化したレポートフラグ表記方法もサポートしています:


.. function:: set_unittest_reportflags(flags)

   .. Set the :mod:`doctest` reporting flags to use.

   :mod:`doctest` のレポートフラグをセットします。


   .. Argument *flags* or's together option flags.  See section
   .. :ref:`doctest-options`.  Only "reporting flags" can be used.

   引数 *flags* にはオプションフラグを OR で結合して渡します。
   :ref:`doctest-options` 節を参照してください。「レポートフラグ」しか使えません。


   .. This is a module-global setting, and affects all future doctests run by module
   .. :mod:`unittest`:  the :meth:`runTest` method of :class:`DocTestCase` looks at
   .. the option flags specified for the test case when the :class:`DocTestCase`
   .. instance was constructed.  If no reporting flags were specified (which is the
   .. typical and expected case), :mod:`doctest`'s :mod:`unittest` reporting flags are
   .. or'ed into the option flags, and the option flags so augmented are passed to the
   .. :class:`DocTestRunner` instance created to run the doctest.  If any reporting
   .. flags were specified when the :class:`DocTestCase` instance was constructed,
   .. :mod:`doctest`'s :mod:`unittest` reporting flags are ignored.

   この関数で設定した内容はモジュール全体にわたる物であり、関数呼び出し以後に :mod:`unittest` モジュールから実行される全ての doctest
   に影響します: :class:`DocTestCase` の :meth:`runTest` メソッドは、 :class:`DocTestCase`
   インスタンスが作成された際に、現在のテストケースに指定されたオプションフラグを見に行きます。レポートフラグが指定されていない場合
   (通常の場合で、望ましいケースです)、 :mod:`doctest` の :mod:`unittest` レポートフラグが OR で結合され、doctest
   を実行するために作成される :class:`DocTestRunner`  インスタンスに渡されます。 :class:`DocTestCase`
   インスタンスを構築する際に何らかのレポートフラグが指定されていた場合、 :mod:`doctest` の :mod:`unittest`
   レポートフラグは無視されます。


   .. The value of the :mod:`unittest` reporting flags in effect before the function
   .. was called is returned by the function.

   この関数は、関数を呼び出す前に有効になっていた :mod:`unittest`  レポートフラグの値を返します。


   .. versionadded:: 2.4


.. _doctest-advanced-api:

拡張 API
--------

.. The basic API is a simple wrapper that's intended to make doctest easy to use.
.. It is fairly flexible, and should meet most users' needs; however, if you
.. require more fine-grained control over testing, or wish to extend doctest's
.. capabilities, then you should use the advanced API.

基本 API は、 doctest を使いやすくするための簡単なラッパであり、柔軟性があってほとんどのユーザの必要を満たしています; とはいえ、
もっとテストをきめ細かに制御したい場合や、 doctest の機能を拡張したい場合、拡張 API (advanced API) を使わねばなりません。


.. The advanced API revolves around two container classes, which are used to store
.. the interactive examples extracted from doctest cases:

拡張 API は、doctest ケースから抽出した対話モードでの例題を記憶するための二つのコンテナクラスを中心に構成されています:


.. * :class:`Example`: A single python :term:`statement`, paired with its expected
..   output.

* :class:`Example`: 1つの Python 文(:term:`statement`)と、その予想出力をペアにしたもの。


.. * :class:`DocTest`: A collection of :class:`Example`\ s, typically extracted
..   from a single docstring or text file.

* :class:`DocTest`: :class:`Example` の集まり。通常一つの docstring やテキストファイルから抽出されます。


.. Additional processing classes are defined to find, parse, and run, and check
.. doctest examples:

その他に、 doctest の例題を検索、パーズ、実行、チェックするための処理クラスが以下のように定義されています:


.. * :class:`DocTestFinder`: Finds all docstrings in a given module, and uses a
..   :class:`DocTestParser` to create a :class:`DocTest` from every docstring that
..   contains interactive examples.

* :class:`DocTestFinder`: 与えられたモジュールから全ての docstring を検索し、対話モードでの例題が入った各
  docstring から :class:`DocTestParser` を使って :class:`DocTest` を生成します。


.. * :class:`DocTestParser`: Creates a :class:`DocTest` object from a string (such
..   as an object's docstring).

* :class:`DocTestParser`: (オブジェクトにつけられた docstring のような) 文字列から :class:`DocTest`
  オブジェクトを生成します。


.. * :class:`DocTestRunner`: Executes the examples in a :class:`DocTest`, and uses
..   an :class:`OutputChecker` to verify their output.

* :class:`DocTestRunner`: :class:`DocTest` 内の例題を実行し、 :class:`OutputChecker`
  を使って出力を検証します。


.. * :class:`OutputChecker`: Compares the actual output from a doctest example with
..   the expected output, and decides whether they match.

* :class:`OutputChecker`: doctest 例題から実際に出力された結果を予想出力と比較し、両者が一致するか判別します。


.. The relationships among these processing classes are summarized in the following
.. diagram:

これらの処理クラスの関係を図にまとめると、以下のようになります。


::

                               list of:
   +------+                   +---------+
   |module| --DocTestFinder-> | DocTest | --DocTestRunner-> results
   +------+    |        ^     +---------+     |       ^    (printed)
               |        |     | Example |     |       |
               v        |     |   ...   |     v       |
              DocTestParser   | Example |   OutputChecker
                              +---------+


.. _doctest-doctest:

DocTest オブジェクト
^^^^^^^^^^^^^^^^^^^^


.. class:: DocTest(examples, globs, name, filename, lineno, docstring)

   .. A collection of doctest examples that should be run in a single namespace.  The
   .. constructor arguments are used to initialize the member variables of the same
   .. names.

   単一の名前空間内で実行される doctest 例題の集まりです。   コンストラクタの引数は :class:`DocTest` インスタンス中の同名の
   メンバ変数の初期化に使われます。


   .. versionadded:: 2.4


   .. :class:`DocTest` defines the following member variables.  They are initialized by
   .. the constructor, and should not be modified directly.

   :class:`DocTest` では、以下のメンバ変数を定義しています。
   これらの変数はコンストラクタで初期化されます。直接変更してはなりません。


   .. attribute:: examples

      .. A list of :class:`Example` objects encoding the individual interactive Python
      .. examples that should be run by this test.

      対話モードにおける例題それぞれをエンコードしていて、テストで実行される、 :class:`Example` オブジェクトからなるリストです。


   .. attribute:: globs

      .. The namespace (aka globals) that the examples should be run in. This is a
      .. dictionary mapping names to values.  Any changes to the namespace made by the
      .. examples (such as binding new variables) will be reflected in :attr:`globs`
      .. after the test is run.

      例題を実行する名前空間 (いわゆるグローバル変数) です。このメンバは、名前から値への対応付けを行っている辞書です。例題が名前空間に対して
      (新たな変数をバインドするなど) 何らかの変更を行った場合、 :attr:`globs` への反映はテストの実行後に起こります。


   .. attribute:: name

      .. A string name identifying the :class:`DocTest`.  Typically, this is the name
      .. of the object or file that the test was extracted from.

      :class:`DocTest` を識別する名前の文字列です。通常、この値はテストを取り出したオブジェクトかファイルの名前になります。


   .. attribute:: filename

      .. The name of the file that this :class:`DocTest` was extracted from; or
      .. ``None`` if the filename is unknown, or if the :class:`DocTest` was not
      .. extracted from a file.

      :class:`DocTest` を取り出したファイルの名前です; ファイル名が未知の場合や :class:`DocTest` をファイルから取り出したので
      ない場合には ``None`` になります。


   .. attribute:: lineno

      .. The line number within :attr:`filename` where this :class:`DocTest` begins, or
      .. ``None`` if the line number is unavailable.  This line number is zero-based
      .. with respect to the beginning of the file.

      :attr:`filename` 中で :class:`DocTest` のテスト例題が始まっている行の
      行番号です。行番号は、ファイルの先頭をゼロとして数えます。


   .. attribute:: docstring

      .. The string that the test was extracted from, or 'None' if the string is
      .. unavailable, or if the test was not extracted from a string.

      テストを取り出した docstring 自体を現す文字列です。 docstring 文字列を得られない場合や、文字列からテスト例題を取り出したのでない場合には
      ``None`` になります。


.. _doctest-example:

Example オブジェクト
^^^^^^^^^^^^^^^^^^^^


.. class:: Example(source, want[, exc_msg][, lineno][, indent][, options])

   .. A single interactive example, consisting of a Python statement and its expected
   .. output.  The constructor arguments are used to initialize the member variables
   .. of the same names.

   ひとつの Python 文と、それに対する予想出力からなる、単一の対話的モードの例題です。コンストラクタの引数は :class:`Example`
   インスタンス中の同名のメンバ変数の初期化に使われます。


   .. versionadded:: 2.4


   .. :class:`Example` defines the following member variables.  They are initialized by
   .. the constructor, and should not be modified directly.

   :class:`Example` では、以下のメンバ変数を定義しています。これらの変数はコンストラクタで初期化されます。直接変更してはなりません。


   .. attribute:: source

      .. A string containing the example's source code.  This source code consists of a
      .. single Python statement, and always ends with a newline; the constructor adds
      .. a newline when necessary.

      例題のソースコードが入った文字列です。ソースコードは単一の Python で、末尾は常に改行です。コンストラクタは必要に応じて改行を追加します。


   .. attribute:: want

      .. The expected output from running the example's source code (either from
      .. stdout, or a traceback in case of exception).  :attr:`want` ends with a
      .. newline unless no output is expected, in which case it's an empty string.  The
      .. constructor adds a newline when necessary.

      例題のソースコードを実行した際の予想出力 (標準出力と、例外が生じた場合にはトレースバック) です。 :attr:`want` の末尾は、予想出力が全く
      ない場合を除いて常に改行になります。予想出力がない場合には空文字列になります。コンストラクタは必要に応じて改行を追加します。


   .. attribute:: exc_msg

      .. The exception message generated by the example, if the example is expected to
      .. generate an exception; or ``None`` if it is not expected to generate an
      .. exception.  This exception message is compared against the return value of
      .. :func:`traceback.format_exception_only`.  :attr:`exc_msg` ends with a newline
      .. unless it's ``None``.  The constructor adds a newline if needed.

      例題が例外を生成すると予想される場合の例外メッセージです。例外を送出しない場合には ``None`` です。
      この例外メッセージは、 :func:`traceback.format_exception_only` の戻り値と比較されます。値が ``None``
      でない限り、 :attr:`exc_msg` は改行で終わっていなければなりません; コンストラクタは必要に応じて改行を追加します。


   .. attribute:: lineno

      .. The line number within the string containing this example where the example
      .. begins.  This line number is zero-based with respect to the beginning of the
      .. containing string.

      この例題の入っている文字列中における、例題の実行文のある行のの行番号です。行番号は文字列の先頭をゼロとして数えます。


   .. attribute:: indent

      .. The example's indentation in the containing string, i.e., the number of space
      .. characters that precede the example's first prompt.

      例題の入っている文字列のインデント、すなわち例題の最初のプロンプトより前にある空白文字の数です。


   .. attribute:: options

      .. A dictionary mapping from option flags to ``True`` or ``False``, which is used
      .. to override default options for this example.  Any option flags not contained
      .. in this dictionary are left at their default value (as specified by the
      .. :class:`DocTestRunner`'s :attr:`optionflags`). By default, no options are set.

      オプションフラグを ``True`` または ``False`` に対応付けている辞書です。例題に対するデフォルトオプションを上書きするために
      用いられます。この辞書に入っていないオプションフラグはデフォルトの状態 (:class:`DocTestrunner` の
      :attr:`optionflags` の内容) のままになります。


.. _doctest-doctestfinder:

DocTestFinder オブジェクト
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: DocTestFinder([verbose][, parser][, recurse][, exclude_empty])

   .. A processing class used to extract the :class:`DocTest`\ s that are relevant to
   .. a given object, from its docstring and the docstrings of its contained objects.
   .. :class:`DocTest`\ s can currently be extracted from the following object types:
   .. modules, functions, classes, methods, staticmethods, classmethods, and
   .. properties.

   与えられたオブジェクトについて、その docstring か、そのオブジェクトに入っているオブジェクトの docstring
   から :class:`DocTest` を抽出する処理クラスです。現在のところ、モジュール、関数、クラス、メソッド、静的メソッド、
   クラスメソッド、プロパティから :class:`DocTest` を抽出できます。


   .. The optional argument *verbose* can be used to display the objects searched by
   .. the finder.  It defaults to ``False`` (no output).

   オプション引数 *verbose* を使うと、抽出処理の対象となるオブジェクトを表示できます。デフォルトは ``False`` (出力をおこなわない) です。


   .. The optional argument *parser* specifies the :class:`DocTestParser` object (or a
   .. drop-in replacement) that is used to extract doctests from docstrings.

   オプション引数 *parser* には、 docstring から :class:`DocTest` を
   抽出するのに使う :class:`DocTestParser` オブジェクト (またはその代替となるオブジェクト) を指定します。


   .. If the optional argument *recurse* is false, then :meth:`DocTestFinder.find`
   .. will only examine the given object, and not any contained objects.

   オプション引数 *recurse* が偽の場合、 :meth:`DocTestFinder.find`
   は与えられたオブジェクトだけを調べ、そのオブジェクトに入っている他のオブジェクトを調べません。


   .. If the optional argument *exclude_empty* is false, then
   .. :meth:`DocTestFinder.find` will include tests for objects with empty docstrings.

   オプション引数 *exclude_empty* が偽の場合、 :meth:`DocTestFinder.find` は空の docstring
   を持つオブジェクトもテスト対象に含めます。


   .. versionadded:: 2.4


   .. :class:`DocTestFinder` defines the following method:

   :class:`DocTestFinder` では以下のメソッドを定義しています:


   .. method:: find(obj[, name][, module][, globs][, extraglobs])

      .. Return a list of the :class:`DocTest`\ s that are defined by *obj*'s
      .. docstring, or by any of its contained objects' docstrings.

      *obj* または *obj* 内に入っているオブジェクトの docstring 中で定義されている
      :class:`DocTest` のリストを返します。


      .. The optional argument *name* specifies the object's name; this name will be
      .. used to construct names for the returned :class:`DocTest`\ s.  If *name* is
      .. not specified, then ``obj.__name__`` is used.

      オプション引数 *name* には、オブジェクトの名前を指定します。
      この名前は、関数が返す :class:`DocTest` の名前になります。
      *name* を指定しない場合、 ``obj.__name__`` を使います。


      .. The optional parameter *module* is the module that contains the given object.
      .. If the module is not specified or is None, then the test finder will attempt
      .. to automatically determine the correct module.  The object's module is used:

      オプションのパラメタ *module* は、指定したオブジェクトを収めているモジュールを指定します。
      *module* を指定しないか、 :const:`None` を指定した場合には、
      正しいモジュールを自動的に決定しようと試みます。
      オブジェクトのモジュールは以下のような役割を果たします:


      .. * As a default namespace, if *globs* is not specified.

      * *globs* を指定していない場合、オブジェクトのモジュールはデフォルトの名前空間になります。


      .. * To prevent the DocTestFinder from extracting DocTests from objects that are
      ..   imported from other modules.  (Contained objects with modules other than
      ..   *module* are ignored.)

      * 他のモジュールから import されたオブジェクトに対して :class:`DocTestFinder` が :class:`DocTest`
        を抽出するのを避けるために使います (*module* 由来でないオブジェクトを無視します)。


      .. * To find the name of the file containing the object.

      * オブジェクトの入っているファイル名を調べるために使います。


      .. * To help find the line number of the object within its file.

      * オブジェクトがファイル内の何行目にあるかを調べる手助けにします。


      .. If *module* is ``False``, no attempt to find the module will be made.  This is
      .. obscure, of use mostly in testing doctest itself: if *module* is ``False``, or
      .. is ``None`` but cannot be found automatically, then all objects are considered
      .. to belong to the (non-existent) module, so all contained objects will
      .. (recursively) be searched for doctests.

      *module* が ``False`` の場合には、モジュールの検索を試みません。
      これは正確さを欠くような使い方で、通常 doctest 自体のテストにしかつかいません。
      *module* が ``False`` の場合、または *module* が ``None`` で自動的に的確な
      モジュールを見つけ出せない場合には、全てのオブジェクトは ``(non-existent)``
      モジュールに属するとみなされ、そのオブジェクト内の全てのオブジェクトに対して
      (再帰的に) doctest の検索をおこないます。


      .. The globals for each :class:`DocTest` is formed by combining *globs* and
      .. *extraglobs* (bindings in *extraglobs* override bindings in *globs*).  A new
      .. shallow copy of the globals dictionary is created for each :class:`DocTest`.
      .. If *globs* is not specified, then it defaults to the module's *__dict__*, if
      .. specified, or ``{}`` otherwise.  If *extraglobs* is not specified, then it
      .. defaults to ``{}``.

      各 :class:`DocTest` のグローバル変数は、 *globs* と *extraglobs* を合わせたもの (*extraglobs*
      内のバインドが *globs* 内のバインドを上書きする) になります。
      各々の :class:`DocTest` に対して、グローバル変数を表す辞書の新たな浅いコピーを生成します。
      *globs* を指定しない場合に使われるのデフォルト値は、モジュールを指定していればそのモジュールの
      *__dict__* になり、指定していなければ ``{}`` になります。
      *extraglobs* を指定しない場合、デフォルトの値は ``{}`` になります。


.. _doctest-doctestparser:

DocTestParser オブジェクト
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: DocTestParser()

   .. A processing class used to extract interactive examples from a string, and use
   .. them to create a :class:`DocTest` object.

   対話モードの例題を文字列から抽出し、それを使って :class:`DocTest`  オブジェクトを生成するために使われる処理クラスです。


   .. versionadded:: 2.4


   .. :class:`DocTestParser` defines the following methods:

   :class:`DocTestParser` では以下のメソッドを定義しています:


   .. method:: get_doctest(string, globs, name, filename, lineno)

      .. Extract all doctest examples from the given string, and collect them into a
      .. :class:`DocTest` object.

      指定した文字列から全ての doctest 例題を抽出し、 :class:`DocTest` オブジェクト内に集めます。


      .. *globs*, *name*, *filename*, and *lineno* are attributes for the new
      .. :class:`DocTest` object.  See the documentation for :class:`DocTest` for more
      .. information.

      *globs*, *name*, *filename*, および *lineno* は新たに作成される :class:`DocTest`
      オブジェクトの属性になります。詳しくは :class:`DocTest` のドキュメントを参照してください。


   .. method:: get_examples(string[, name])

      .. Extract all doctest examples from the given string, and return them as a list
      .. of :class:`Example` objects.  Line numbers are 0-based.  The optional argument
      .. *name* is a name identifying this string, and is only used for error messages.

      指定した文字列から全ての doctest 例題を抽出し、 :class:`Example`
      オブジェクトからなるリストにして返します。
      各 :class:`Example` の行番号はゼロから数えます。
      オプション引数 *name* はこの文字列につける名前で、エラーメッセージにしか使われません。


   .. method:: parse(string[, name])

      .. Divide the given string into examples and intervening text, and return them as
      .. a list of alternating :class:`Example`\ s and strings. Line numbers for the
      .. :class:`Example`\ s are 0-based.  The optional argument *name* is a name
      .. identifying this string, and is only used for error messages.

      指定した文字列を、例題とその間のテキストに分割し、
      例題を :class:`Example` オブジェクトに変換し、
      :class:`Example` と文字列からなるリストにして返します。
      各 :class:`Example` の行番号はゼロから数えます。オプション引数 *name*
      はこの文字列につける名前で、エラーメッセージにしか使われません。


.. _doctest-doctestrunner:

DocTestRunner オブジェクト
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: DocTestRunner([checker][, verbose][, optionflags])

   .. A processing class used to execute and verify the interactive examples in a
   .. :class:`DocTest`.

   :class:`DocTest` 内の対話モード例題を実行し、検証する際に用いられる処理クラスです。


   .. The comparison between expected outputs and actual outputs is done by an
   .. :class:`OutputChecker`.  This comparison may be customized with a number of
   .. option flags; see section :ref:`doctest-options` for more information.  If the
   .. option flags are insufficient, then the comparison may also be customized by
   .. passing a subclass of :class:`OutputChecker` to the constructor.

   予想出力と実際の出力との比較は :class:`OutputChecker` で行います。
   比較は様々なオプションフラグを使ってカスタマイズできます;
   詳しくは :ref:`doctest-options` を参照してください。
   オプションフラグでは不十分な場合、コンストラクタに
   :class:`OutputChecker` のサブクラスを渡して比較方法をカスタマイズできます。


   .. The test runner's display output can be controlled in two ways. First, an output
   .. function can be passed to :meth:`TestRunner.run`; this function will be called
   .. with strings that should be displayed.  It defaults to ``sys.stdout.write``.  If
   .. capturing the output is not sufficient, then the display output can be also
   .. customized by subclassing DocTestRunner, and overriding the methods
   .. :meth:`report_start`, :meth:`report_success`,
   .. :meth:`report_unexpected_exception`, and :meth:`report_failure`.

   テストランナの表示出力の制御には二つの方法があります。
   一つ目は、 :meth:`TestRunner.run` に出力用の関数を渡すというものです。
   この関数は、表示すべき文字列を引数にして呼び出されます。
   デフォルトは ``sys.stdout.write`` です。出力を取り込んで処理するだけでは不十分な場合、
   :class:`DocTestRunner` をサブクラス化し、 :meth:`report_start`,
   :meth:`report_success`, :meth:`report_unexpected_exception`, および
   :meth:`report_failure` をオーバライドすればカスタマイズできます。


   .. The optional keyword argument *checker* specifies the :class:`OutputChecker`
   .. object (or drop-in replacement) that should be used to compare the expected
   .. outputs to the actual outputs of doctest examples.

   オプションのキーワード引数 *checker* には、 :class:`OutputChecker` オブジェクト (またはその代用品)
   を指定します。このオブジェクトは doctest 例題の予想出力と実際の出力との比較を行う際に使われます。


   .. The optional keyword argument *verbose* controls the :class:`DocTestRunner`'s
   .. verbosity.  If *verbose* is ``True``, then information is printed about each
   .. example, as it is run.  If *verbose* is ``False``, then only failures are
   .. printed.  If *verbose* is unspecified, or ``None``, then verbose output is used
   .. iff the command-line switch :option:`-v` is used.

   オプションのキーワード引数 *verbose* は、 :class:`DocTestRunner` の出すメッセージの冗長性を制御します。
   *verbose* が ``True`` の場合、各例題を実行するつど、その例題についての情報を出力します。
   *verbose* が ``False`` の場合、テストの失敗だけを出力します。
   *verbose* を指定しない場合や ``None`` を指定した場合、コマンドラインスイッチ
   :option:`-v` を使った場合にのみ *verbose* 出力を適用します。


   .. The optional keyword argument *optionflags* can be used to control how the test
   .. runner compares expected output to actual output, and how it displays failures.
   .. For more information, see section :ref:`doctest-options`.

   オプションのキーワード引数  *optionflags* を使うと、
   テストランナが予想出力と実際の出力を比較する方法や、
   テストの失敗を表示する方法を制御できます。
   詳しくは :ref:`doctest-options` 節を参照してください。


   .. versionadded:: 2.4


   .. :class:`DocTestParser` defines the following methods:

   :class:`DocTestRunner` では、以下のメソッドを定義しています:


   .. method:: report_start(out, test, example)

      .. Report that the test runner is about to process the given example. This method
      .. is provided to allow subclasses of :class:`DocTestRunner` to customize their
      .. output; it should not be called directly.

      テストランナが例題を処理しようとしているときにレポートを出力します。
      :class:`DocTestRunner` の出力をサブクラスでカスタマイズできるように
      するためのメソッドです。直接呼び出してはなりません。


      .. *example* is the example about to be processed.  *test* is the test
      .. *containing example*.  *out* is the output function that was passed to
      .. :meth:`DocTestRunner.run`.

      *example* は処理する例題です。 *test* は *example* の入っているテストです。
      *out* は出力用の関数で、 :meth:`DocTestRunner.run` に渡されます。


   .. method:: report_success(out, test, example, got)

      .. Report that the given example ran successfully.  This method is provided to
      .. allow subclasses of :class:`DocTestRunner` to customize their output; it
      .. should not be called directly.

      与えられた例題が正しく動作したことを報告します。
      このメソッドは :class:`DocTestRunner` のサブクラスで出力を
      カスタマイズできるようにするために提供されています; 直接呼び出してはなりません。


      .. *example* is the example about to be processed.  *got* is the actual output
      .. from the example.  *test* is the test containing *example*.  *out* is the
      .. output function that was passed to :meth:`DocTestRunner.run`.

      *example* は処理する例題です。 *got* は例題から実際に得られた出力です。
      *test* は *example* の入っているテストです。
      *out* は出力用の関数で、 :meth:`DocTestRunner.run` に渡されます。


   .. method:: report_failure(out, test, example, got)

      .. Report that the given example failed.  This method is provided to allow
      .. subclasses of :class:`DocTestRunner` to customize their output; it should not
      .. be called directly.

      与えられた例題が正しく動作しなかったことを報告します。
      このメソッドは :class:`DocTestRunner` のサブクラスで出力を
      カスタマイズできるようにするために提供されています; 直接呼び出してはなりません。


      .. *example* is the example about to be processed.  *got* is the actual output
      .. from the example.  *test* is the test containing *example*.  *out* is the
      .. output function that was passed to :meth:`DocTestRunner.run`.

      *example* は処理する例題です。 *got* は例題から実際に得られた出力です。
      *test* は *example* の入っているテストです。
      *out* は出力用の関数で、 :meth:`DocTestRunner.run` に渡されます。


   .. method:: report_unexpected_exception(out, test, example, exc_info)

      .. Report that the given example raised an unexpected exception. This method is
      .. provided to allow subclasses of :class:`DocTestRunner` to customize their
      .. output; it should not be called directly.

      与えられた例題が予想とは違う例外を送出したことを報告します。
      このメソッドは :class:`DocTestRunner` のサブクラスで出力をカスタマイズ
      できるようにするために提供されています; 直接呼び出してはなりません。


      .. *example* is the example about to be processed. *exc_info* is a tuple
      .. containing information about the unexpected exception (as returned by
      .. :func:`sys.exc_info`). *test* is the test containing *example*.  *out* is the
      .. output function that was passed to :meth:`DocTestRunner.run`.

      *example* は処理する例題です。 *exc_info* には予期せず送出された
      例外の情報を入れたタプル (:func:`sys.exc_info` の返す内容) になります。
      *test* は *example* の入っているテストです。
      *out* は出力用の関数で、 :meth:`DocTestRunner.run` に渡されます。


   .. method:: run(test[, compileflags][, out][, clear_globs])

      .. Run the examples in *test* (a :class:`DocTest` object), and display the
      .. results using the writer function *out*.

      *test* 内の例題 (:class:`DocTest` オブジェクト) を実行し、
      その結果を出力用の関数 *out* を使って表示します。


      .. The examples are run in the namespace ``test.globs``.  If *clear_globs* is
      .. true (the default), then this namespace will be cleared after the test runs,
      .. to help with garbage collection. If you would like to examine the namespace
      .. after the test completes, then use *clear_globs=False*.

      例題は名前空間 ``test.globs`` の下で実行されます。
      *clear_globs* が真 (デフォルト) の場合、名前空間はテストの実行後に消去され、
      ガベージコレクションをうながします。
      テストの実行完了後にその内容を調べたければ、 *clear_globs* を
      :const:`False` にしてください。


      .. *compileflags* gives the set of flags that should be used by the Python
      .. compiler when running the examples.  If not specified, then it will default to
      .. the set of future-import flags that apply to *globs*.

      *compileflags* には、例題を実行する際に Python コンパイラに適用するフラグセットを指定します。
      *compileflags* を指定しない場合、デフォルト値は *globs* で適用されている
      future-import フラグセットになります。


      .. The output of each example is checked using the :class:`DocTestRunner`'s
      .. output checker, and the results are formatted by the
      .. :meth:`DocTestRunner.report_\*` methods.

      各例題の出力は :class:`DocTestRunner` の出力チェッカで検査され、その結果は
      :meth:`DocTestRunner.report_\*` メソッドで書式化されます。


   .. method:: summarize([verbose])

      .. Print a summary of all the test cases that have been run by this DocTestRunner,
      .. and return a :term:`named tuple` ``TestResults(failed, attempted)``.

      この DocTestRunner が実行した全てのテストケースのサマリを出力し、
      名前付きタプル (:term:`named tuple`) ``TestResults(failed, attempted)`` を返します。


      .. The optional *verbose* argument controls how detailed the summary is.  If the
      .. verbosity is not specified, then the :class:`DocTestRunner`'s verbosity is
      .. used.

      オプションの *verbose* 引数を使うと、どのくらいサマリを詳しくするかを制御できます。
      冗長度を指定しない場合、 :class:`DocTestRunner` 自体の冗長度を使います。


      .. .. versionchanged:: 2.6
      ..    Use a named tuple.

      .. versionchanged:: 2.6
         名前付きタプル (named tuple) を使うようになりました。


.. _doctest-outputchecker:

OutputChecker オブジェクト
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: OutputChecker()

   .. A class used to check the whether the actual output from a doctest example
   .. matches the expected output.  :class:`OutputChecker` defines two methods:
   .. :meth:`check_output`, which compares a given pair of outputs, and returns true
   .. if they match; and :meth:`output_difference`, which returns a string describing
   .. the differences between two outputs.

   doctest 例題を実際に実行したときの出力が予想出力と一致するかどうかを
   チェックするために使われるクラスです。
   :class:`OutputChecker` では、与えられた二つの出力を比較して、
   一致する場合には真を返す :meth:`check_output` と、
   二つの出力間の違いを説明する文字列を返す :meth:`output_difference`
   の、二つのメソッドがあります。


   .. versionadded:: 2.4


   .. :class:`OutputChecker` defines the following methods:

   :class:`OutputChecker` では以下のメソッドを定義しています:


   .. method:: check_output(want, got, optionflags)

      .. Return ``True`` iff the actual output from an example (*got*) matches the
      .. expected output (*want*).  These strings are always considered to match if
      .. they are identical; but depending on what option flags the test runner is
      .. using, several non-exact match types are also possible.  See section
      .. :ref:`doctest-options` for more information about option flags.

      例題から実際に得られた出力 (*got*) と、予想出力 (*want*)
      が一致する場合にのみ ``True`` を返します。
      二つの文字列が全く同一の場合には常に一致するとみなしますが、
      テストランナの使っているオプションフラグにより、
      厳密には同じ内容になっていなくても一致するとみなす場合もあります。
      オプションフラグについての詳しい情報は :ref:`doctest-options` 節を参照してください。


   .. method:: output_difference(example, got, optionflags)

      .. Return a string describing the differences between the expected output for a
      .. given example (*example*) and the actual output (*got*).  *optionflags* is the
      .. set of option flags used to compare *want* and *got*.

      与えられた例題の予想出力 (*want*)と、実際に得られた出力 (*got*)
      の間の差異を解説している文字列を返します。
      *optionflags* は *want* と *got* を比較する際に使われる
      オプションフラグのセットです。


.. _doctest-debugging:

デバッグ
--------

.. Doctest provides several mechanisms for debugging doctest examples:

:mod:`doctest` では、doctest 例題をデバッグするメカニズムをいくつか提供しています:


.. * Several functions convert doctests to executable Python programs, which can be
..   run under the Python debugger, :mod:`pdb`.

* doctest を実行可能な Python プログラムに変換し、 Python デバッガ :mod:`pdb`
  で実行できるようにするための関数がいくつかあります。


.. * The :class:`DebugRunner` class is a subclass of :class:`DocTestRunner` that
..   raises an exception for the first failing example, containing information about
..   that example. This information can be used to perform post-mortem debugging on
..   the example.

* :class:`DocTestRunner` のサブクラス :class:`DebugRunner` クラスが
  あります。このクラスは、最初に失敗した例題に対して例外を送出します。
  例外には例題に関する情報が入っています。この情報は例題の検視デバッグに利用できます。


.. * The :mod:`unittest` cases generated by :func:`DocTestSuite` support the
..   :meth:`debug` method defined by :class:`unittest.TestCase`.

* :func:`DocTestSuite` の生成する :mod:`unittest` テストケースは、 :meth:`debug`
  メソッドをサポートしています。 :meth:`debug` は :class:`unittest.TestCase` で定義されています。


.. * You can add a call to :func:`pdb.set_trace` in a doctest example, and you'll
..   drop into the Python debugger when that line is executed.  Then you can inspect
..   current values of variables, and so on.  For example, suppose :file:`a.py`
..   contains just this module docstring:

* :func:`pdb.set_trace` を doctest 例題の中で呼び出しておけば、その行が実行されたときに Python
  デバッガが組み込まれます。
  デバッガを組み込んだあとは、変数の現在の値などを調べられます。
  たとえば、以下のようなモジュールレベルの docstring
  の入ったファイル :file:`a.py` があるとします。


  ::

     """
     >>> def f(x):
     ...     g(x*2)
     >>> def g(x):
     ...     print x+3
     ...     import pdb; pdb.set_trace()
     >>> f(3)
     9
     """


  .. Then an interactive Python session may look like this:

  対話セッションは以下のようになるでしょう。


  ::

     >>> import a, doctest
     >>> doctest.testmod(a)
     --Return--
     > <doctest a[1]>(3)g()->None
     -> import pdb; pdb.set_trace()
     (Pdb) list
       1     def g(x):
       2         print x+3
       3  ->     import pdb; pdb.set_trace()
     [EOF]
     (Pdb) print x
     6
     (Pdb) step
     --Return--
     > <doctest a[0]>(2)f()->None
     -> g(x*2)
     (Pdb) list
       1     def f(x):
       2  ->     g(x*2)
     [EOF]
     (Pdb) print x
     3
     (Pdb) step
     --Return--
     > <doctest a[2]>(1)?()->None
     -> f(3)
     (Pdb) cont
     (0, 3)
     >>>


  .. .. versionchanged:: 2.4
  ..    The ability to use :func:`pdb.set_trace` usefully inside doctests was added.

  .. versionchanged:: 2.4
     :func:`pdb.set_trace` を doctest の中で有効に使えるようになりました.


.. Functions that convert doctests to Python code, and possibly run the synthesized
.. code under the debugger:

以下は、doctest を Python コードに変換して、できたコードをデバッガ下で実行できるようにするための関数です:


.. function:: script_from_examples(s)

   .. Convert text with examples to a script.

   例題の入ったテキストをスクリプトに変換します。


   .. Argument *s* is a string containing doctest examples.  The string is converted
   .. to a Python script, where doctest examples in *s* are converted to regular code,
   .. and everything else is converted to Python comments.  The generated script is
   .. returned as a string. For example,

   引数 *s* は doctest 例題の入った文字列です。
   この文字列は Python スクリプトに変換され、その中では *s* の doctest 例題が
   通常のコードに、それ以外は Python のコメント文になります。
   生成したスクリプトを文字列で返します。例えば、


   ::

      import doctest
      print doctest.script_from_examples(r"""
          Set x and y to 1 and 2.
          >>> x, y = 1, 2

          Print their sum:
          >>> print x+y
          3
      """)


   .. displays:

   は、


   ::

      # Set x and y to 1 and 2.
      x, y = 1, 2
      #
      # Print their sum:
      print x+y
      # Expected:
      ## 3


   になります。


   .. This function is used internally by other functions (see below), but can also be
   .. useful when you want to transform an interactive Python session into a Python
   .. script.

   この関数は他の関数 (下記参照) から使われていまるが、対話セッションを
   Python スクリプトに変換したいような場合にも便利でしょう。


   .. versionadded:: 2.4


.. function:: testsource(module, name)

   .. Convert the doctest for an object to a script.

   あるオブジェクトの doctest をスクリプトに変換します。


   .. Argument *module* is a module object, or dotted name of a module, containing the
   .. object whose doctests are of interest.  Argument *name* is the name (within the
   .. module) of the object with the doctests of interest.  The result is a string,
   .. containing the object's docstring converted to a Python script, as described for
   .. :func:`script_from_examples` above.  For example, if module :file:`a.py`
   .. contains a top-level function :func:`f`, then

   引数 *module* はモジュールオブジェクトか、対象の doctest を持つ
   オブジェクトの入ったモジュールのドット表記名です。
   引数 *name* は対象の doctest を持つオブジェクトの (モジュール内の) 名前です。
   対象オブジェクトの docstring を上の :func:`script_from_examples`
   で説明した方法で Python スクリプトに変換してできた文字列を返しますます。
   例えば、 :file:`a.py` モジュールのトップレベルに関数 :func:`f` がある場合、以下のコード


   ::

      import a, doctest
      print doctest.testsource(a, "a.f")


   .. prints a script version of function :func:`f`'s docstring, with doctests
   .. converted to code, and the rest placed in comments.

   を実行すると、 :func:`f` の docstring から doctest をコードに変換し、
   それ以外をコメントにしたスクリプトを出力します。


   .. versionadded:: 2.3


.. function:: debug(module, name[, pm])

   .. Debug the doctests for an object.

   オブジェクトの持つ doctest をデバッグします。


   .. The *module* and *name* arguments are the same as for function
   .. :func:`testsource` above.  The synthesized Python script for the named object's
   .. docstring is written to a temporary file, and then that file is run under the
   .. control of the Python debugger, :mod:`pdb`.

   *module* および *name* 引数は上の :func:`testsource` と同じです。
   指定したオブジェクトの docstring から合成された Python
   スクリプトは一時ファイルに書き出され、その後 Python デバッガ :mod:`pdb` の制御下で実行されます。


   .. A shallow copy of ``module.__dict__`` is used for both local and global
   .. execution context.

   ローカルおよびグローバルの実行コンテキストには、 ``module.__dict__`` の浅いコピーが使われます。


   .. Optional argument *pm* controls whether post-mortem debugging is used.  If *pm*
   .. has a true value, the script file is run directly, and the debugger gets
   .. involved only if the script terminates via raising an unhandled exception.  If
   .. it does, then post-mortem debugging is invoked, via :func:`pdb.post_mortem`,
   .. passing the traceback object from the unhandled exception.  If *pm* is not
   .. specified, or is false, the script is run under the debugger from the start, via
   .. passing an appropriate :func:`execfile` call to :func:`pdb.run`.

   オプション引数 *pm* は、検死デバッグを行うかどうかを指定します。
   *pm* が真の場合、スクリプトファイルは直接実行され、
   スクリプトが送出した例外が処理されないまま終了した場合にのみデバッガが立ち入ります。
   その場合、 :func:`pdb.post_mortem` によって検死デバッグを起動し、
   処理されなかった例外から得られたトレースバックオブジェクトを渡します。
   *pm* を指定しないか値を偽にした場合、 :func:`pdb.run` に適切な :func:`execfile`
   呼び出しを渡して、最初からデバッガの下でスクリプトを実行します。


   .. versionadded:: 2.3


   .. .. versionchanged:: 2.4
   ..    The *pm* argument was added.

   .. versionchanged:: 2.4
      引数 *pm* を追加しました.


.. function:: debug_src(src[, pm][, globs])

   .. Debug the doctests in a string.

   文字列中の doctest をデバッグします。


   .. This is like function :func:`debug` above, except that a string containing
   .. doctest examples is specified directly, via the *src* argument.

   上の :func:`debug` に似ていますが、doctest の入った文字列は *src* 引数で直接指定します。


   .. Optional argument *pm* has the same meaning as in function :func:`debug` above.

   オプション引数 *pm* は上の :func:`debug` と同じ意味です。


   .. Optional argument *globs* gives a dictionary to use as both local and global
   .. execution context.  If not specified, or ``None``, an empty dictionary is used.
   .. If specified, a shallow copy of the dictionary is used.

   オプション引数 *globs* には、ローカルおよびグローバルな実行コンテキストの
   両方に使われる辞書を指定します。
   *globs* を指定しない場合や ``None`` にした場合、空の辞書を使います。
   辞書を指定した場合、実際の実行コンテキストには浅いコピーが使われます。


   .. versionadded:: 2.4


.. The :class:`DebugRunner` class, and the special exceptions it may raise, are of
.. most interest to testing framework authors, and will only be sketched here.  See
.. the source code, and especially :class:`DebugRunner`'s docstring (which is a
.. doctest!) for more details:

:class:`DebugRunner` クラス自体や :class:`DebugRunner` クラスが送出する特殊な例外は、
テストフレームワークの作者にとって非常に興味のあるところですが、
ここでは概要しか述べられません。
詳しくはソースコード、とりわけ :class:`DebugRunner` の docstring (それ自体 doctest ですよ!)
を参照してください。


.. class:: DebugRunner([checker][, verbose][, optionflags])

   .. A subclass of :class:`DocTestRunner` that raises an exception as soon as a
   .. failure is encountered.  If an unexpected exception occurs, an
   .. :exc:`UnexpectedException` exception is raised, containing the test, the
   .. example, and the original exception.  If the output doesn't match, then a
   .. :exc:`DocTestFailure` exception is raised, containing the test, the example, and
   .. the actual output.

   テストの失敗に遭遇するとすぐに例外を送出するようになっている
   :class:`DocTestRunner` のサブクラスです。予期しない例外が生じると、
   :exc:`UnexpectedException` 例外を送出します。
   この例外には、テスト、例題、もともと送出された例外が入っています。
   予想出力と実際出力が一致しないために失敗した場合には、
   :exc:`DocTestFailure` 例外を送出します。
   この例外には、テスト、例題、実際の出力が入っています。


   .. For information about the constructor parameters and methods, see the
   .. documentation for :class:`DocTestRunner` in section :ref:`doctest-advanced-api`.

   コンストラクタのパラメタやメソッドについては、 :ref:`doctest-advanced-api` 節の
   :class:`DocTestRunner` のドキュメントを参照してください。


.. There are two exceptions that may be raised by :class:`DebugRunner` instances:

:class:`DebugRunner` インスタンスの送出する例外には以下の二つがあります:


.. exception:: DocTestFailure(test, example, got)

   .. An exception thrown by :class:`DocTestRunner` to signal that a doctest example's
   .. actual output did not match its expected output. The constructor arguments are
   .. used to initialize the member variables of the same names.

   doctest 例題の実際の出力が予想出力と一致しなかったことを示すために
   :class:`DocTestRunner` が送出する例外です。
   コンストラクタの引数は、インスタンスの同名のメンバ変数を初期化するために使われます。


.. :exc:`DocTestFailure` defines the following member variables:

:exc:`DocTestFailure` では以下のメンバ変数を定義しています:


.. attribute:: DocTestFailure.test

   .. The :class:`DocTest` object that was being run when the example failed.

   例題が失敗した時に実行されていた :class:`DocTest` オブジェクトです。


.. attribute:: DocTestFailure.example

   .. The :class:`Example` that failed.

   失敗した :class:`Example` オブジェクトです。


.. attribute:: DocTestFailure.got

   .. The example's actual output.

   例題の実際の出力です。


.. exception:: UnexpectedException(test, example, exc_info)

   .. An exception thrown by :class:`DocTestRunner` to signal that a doctest example
   .. raised an unexpected exception.  The constructor arguments are used to
   .. initialize the member variables of the same names.

   doctest 例題が予期しない例外を送出したことを示すために :class:`DocTestRunner` が送出する例外です。
   コンストラクタの引数は、インスタンスの同名のメンバ変数を初期化するために使われます。


.. :exc:`UnexpectedException` defines the following member variables:

:exc:`UnexpectedException` では以下のメンバ変数を定義しています:


.. attribute:: UnexpectedException.test

   .. The :class:`DocTest` object that was being run when the example failed.

   例題が失敗した時に実行されていた :class:`DocTest` オブジェクトです。


.. attribute:: UnexpectedException.example

   .. The :class:`Example` that failed.

   失敗した :class:`Example` オブジェクトです。


.. attribute:: UnexpectedException.exc_info

   .. A tuple containing information about the unexpected exception, as returned by
   .. :func:`sys.exc_info`.

   予期しない例外についての情報の入ったタプルで、 :func:`sys.exc_info`  が返すのと同じものです。


.. _doctest-soapbox:

提言
----

.. As mentioned in the introduction, :mod:`doctest` has grown to have three primary
.. uses:

冒頭でも触れたように、 :mod:`doctest` は、


.. #. Checking examples in docstrings.

.. #. Regression testing.

.. #. Executable documentation / literate testing.

#. docstring 内の例題をチェックする、

#. 回帰テストを行う、

#. 実行可能なドキュメント/読めるテストの実現、


という三つの主な用途を持つようになりました。


.. These uses have different requirements, and it is important to distinguish them.
.. In particular, filling your docstrings with obscure test cases makes for bad
.. documentation.

これらの用途にはそれぞれ違った要求があるので、区別して考えるのが重要です。
特に、 docstring を曖昧なテストケースに埋もれさせてしまうとドキュメントとしては最悪です。


.. When writing a docstring, choose docstring examples with care. There's an art to
.. this that needs to be learned---it may not be natural at first.  Examples should
.. add genuine value to the documentation.  A good example can often be worth many
.. words. If done with care, the examples will be invaluable for your users, and
.. will pay back the time it takes to collect them many times over as the years go
.. by and things change.  I'm still amazed at how often one of my :mod:`doctest`
.. examples stops working after a "harmless" change.

docstring の例は注意深く作成してください。
doctest の作成にはコツがあり、きちんと学ぶ必要があります --- 最初はすんなりできないでしょう。
例題は、ドキュメントに紛れ無しの価値を与えます。
よい例がたくさんの言葉に値することは多々あります。
注意深くやれば、例はユーザにとってはあまり意味のないものになるかもしれませんが、
歳を経るにつれて、あるいは "状況が変わった" 際に何度も何度も正しく動作させるために
かかることになる時間を節約するという形で、きっと見返りを得るでしょう。
私は今でも、自分の :mod:`doctest` で処理した例が "たいした事のない"
変更を行った際にうまく動作しなくなることに驚いています。


.. Doctest also makes an excellent tool for regression testing, especially if you
.. don't skimp on explanatory text.  By interleaving prose and examples, it becomes
.. much easier to keep track of what's actually being tested, and why.  When a test
.. fails, good prose can make it much easier to figure out what the problem is, and
.. how it should be fixed.  It's true that you could write extensive comments in
.. code-based testing, but few programmers do. Many have found that using doctest
.. approaches instead leads to much clearer tests.  Perhaps this is simply because
.. doctest makes writing prose a little easier than writing code, while writing
.. comments in code is a little harder.  I think it goes deeper than just that:
.. the natural attitude when writing a doctest-based test is that you want to
.. explain the fine points of your software, and illustrate them with examples.
.. This in turn naturally leads to test files that start with the simplest
.. features, and logically progress to complications and edge cases.  A coherent
.. narrative is the result, instead of a collection of isolated functions that test
.. isolated bits of functionality seemingly at random.  It's a different attitude,
.. and produces different results, blurring the distinction between testing and
.. explaining.

説明テキストの作成をけちらなければ、 :mod:`doctest` は回帰テストの優れたツールにもなり得ます。
説明文と例題を交互に記述していけば、
実際に何をどうしてテストしているのかもっと簡単に把握できるようになるでしょう。
もちろん、コードベースのテストに詳しくコメントを入れるのも手ですが、
そんなことをするプログラマはほとんどいません。
多くの人々が、 :mod:`doctest` のアプローチをとった方がきれいにテストを書けると気づいています。
おそらく、これは単にコード中にコメントを書くのが少し面倒だからという理由でしょう。
私はもう少しうがった見方もしています:
doctest ベースのテストを書くときの自然な態度は、
自分のソフトウェアのよい点を説明しようとして、
例題を使って説明しようとするときの態度そのものだからだ、という理由です。
それゆえに、テストファイルは自然と単純な機能の解説から始め、
論理的により複雑で境界条件的なケースに進むような形になります。
結果的に、一見ランダムに見えるような個別の機能をテストしている個別の関数の集まりではなく、
首尾一貫した説明ができるようになるのです。
:mod:`doctest` によるテストの作成は全く別の取り組み方であり、
テストと説明の区別をなくして、全く違う結果を生み出すのです。


.. Regression testing is best confined to dedicated objects or files.  There are
.. several options for organizing tests:

回帰テストは特定のオブジェクトやファイルにまとめておくのがよいでしょう。
回帰テストの組み方にはいくつか選択肢があります:


.. * Write text files containing test cases as interactive examples, and test the
..   files using :func:`testfile` or :func:`DocFileSuite`.  This is recommended,
..   although is easiest to do for new projects, designed from the start to use
..   doctest.

* テストケースを対話モードの例題にして入れたテキストファイルを書き、
  :func:`testifle` や :func:`DocFileSuite` を使ってそのファイルをテストします。
  この方法をお勧めします。
  最初から doctest を使うようにしている新たなプロジェクトでは、この方法が一番簡単です。


.. * Define functions named ``_regrtest_topic`` that consist of single docstrings,
..   containing test cases for the named topics.  These functions can be included in
..   the same file as the module, or separated out into a separate test file.

* ``_regrtest_topic`` という名前の関数を定義します。
  この関数には、あるトピックに対応するテストケースの入った docstring が一つだけ入っています。
  この関数はモジュールと同じファイルの中にも置けますし、別のテストファイルに分けてもかまいません。


.. * Define a ``__test__`` dictionary mapping from regression test topics to
..   docstrings containing test cases.

* 回帰テストのトピックをテストケースの入った docstring
  に対応付けた辞書 ``__test__`` 辞書を定義します。


.. rubric:: Footnotes

.. .. [#] Examples containing both expected output and an exception are not supported.
..    Trying to guess where one ends and the other begins is too error-prone, and that
..    also makes for a confusing test.

.. [#] 予想出力結果と例外の両方を含んだ例はサポートされていません。
   一方の終わりと他方の始まりを見分けようとするのはエラーの元になりがちですし、
   解りにくいテストになってしまいます。

