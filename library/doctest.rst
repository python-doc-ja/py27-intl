:mod:`doctest` --- 対話モードを使った使用例の内容をテストする
=============================================================

.. module:: doctest
   :synopsis: docstring の中のテストコード.
.. moduleauthor:: Tim Peters <tim@python.org>
.. sectionauthor:: Tim Peters <tim@python.org>
.. sectionauthor:: Moshe Zadka <moshez@debian.org>
.. sectionauthor:: Edward Loper <edloper@users.sourceforge.net>


:mod:`doctest` モジュールは、対話的 Python セッションのように見えるテキストを探し出し、
セッションの内容を実行して、そこに書かれている通りに振舞うかを調べます。
:mod:`doctest` は以下のような用途によく使われています:

* モジュールの docstring (ドキュメンテーション文字列) 中にある対話モードでの使用例全てが書かれている通りに動作するかを検証することで、
  docstring の内容が最新のものになるよう保ちます。

* テストファイルやテストオブジェクト中の対話モードにおける使用例が期待通りに動作するかを検証することで、
  回帰テストを実現します。

* 入出力例をふんだんに使ったパッケージのチュートリアルドキュメントを書けます。
  入出力例と解説文のどちらに注目するかによって、ドキュメントは「読めるテスト」にも「実行できるドキュメント」にもなります。

以下にちょっとした、それでいて完全な例を示します:

:mod:`doctest` モジュールは、モジュールの docstring から、これらのセッションを実際に実行して、
そこに書かれている通りに動作するか検証します。 ::

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

:file:`example.py` をコマンドラインから直接実行すると、 :mod:`doctest` はその魔法を働かせます::

   $ python example.py
   $

出力は何もありません！しかしこれが正常で、全ての例が正しく動作することを意味しています。
スクリプトに :option:`-v` を与えると、 :mod:`doctest`  は何を行おうとしているのかを記録した詳細なログを出力し、
最後にまとめを出力します::

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

といった具合で、最後には::

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

これが、 :mod:`doctest` を使って生産性の向上を目指す上で知っておく必要があることの全てです！
さあやってみましょう。詳細な事柄は後続の各節で全て説明しています。
doctest の例は、標準の Python テストスイートやライブラリ中に沢山あります。
標準のテストファイル :file:`Lib/test/test_doctest.py`  には、特に便利な例題があります。


.. _doctest-simple-testmod:

簡単な利用法: docstring 中の例題をチェックする
----------------------------------------------

doctest を試す簡単な方法、(とはいえ、いつもそうする必要はないのですが) は、
各モジュール :mod:`M` の最後を、以下のようにして締めくくるやりかたです。::

   if __name__ == "__main__":
       import doctest, M
       doctest.testmod()


こうすると、 :mod:`doctest` は :mod:`M` 中の docstring を検査します。
モジュールをスクリプトとして実行すると、docstring 中の例題が実行され、検証されます::

   python M.py

ドキュメンテーション文字列に書かれた例の実行が失敗しない限り、何も表示されません。
失敗すると、失敗した例と、その原因が (場合によっては複数) 標準出力に印字され、
最後に ``***Test Failed*** N failures.`` という行を出力します。ここで、 *N* は失敗した例題の数です。

一方、 :option:`-v` スイッチをつけて走らせると::

   python M.py -v

実行を試みた全ての例について詳細に報告し、最後に各種まとめをおこなった内容が標準出力に印字されます。

``verbose=True`` を :func:`testmod` に渡せば、詳細報告 (verbose) モードを強制できます。また、
``verbose=False`` にすれば禁止できます。どちらの場合にも、 :func:`testmod` は ``sys.argv`` 上のスイッチ
を調べません。(従って、 :option:`-v` をつけても効果はありません)。

Python 2.6 からは :func:`testmod` を実行するコマンドラインショートカットがあります。
Python インタプリタに doctest モジュールを標準ライブラリから直接実行して、テストする
モジュール名をコマンドライン引数に与えます。::

   python -m doctest -v example.py

こうすると :file:`example.py` を単体モジュールとしてインポートして、
それに対して :func:`testmod` を実行します。
このファイルがパッケージの一部で他のサブモジュールをそのパッケージからインポートしている場合は
うまく動かないことに注意してください。

:func:`testmod` の詳しい情報は :ref:`doctest-basic-api` 節を参照してください。

.. _doctest-simple-testfile:

簡単な利用法: テキストファイル中の例題をチェックする
----------------------------------------------------

doctest のもう一つの簡単な用途は、テキストファイル中にある対話操作の例に対するテストです。
これには :func:`testfile` 関数を使います::

   import doctest
   doctest.testfile("example.txt")

この短いスクリプトは、 :file:`example.txt` というファイルの中に入っている対話モードの Python
操作例全てを実行して、その内容を検証します。
ファイルの内容は一つの巨大な docstring であるかのように扱われます; ファイルが Python
プログラムでなくてもよいのです！
例えば、 :file:`example.txt` には以下のような内容が入っているかもしれません::

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

``doctest.testfile("example.txt")`` を実行すると、このドキュメント内のエラーを見つけ出します::

   File "./example.txt", line 14, in example.txt
   Failed example:
       factorial(6)
   Expected:
       120
   Got:
       720

:func:`testmod` と同じく、 :func:`testfile` は例題が失敗しない限り何も表示しません。
例題が失敗すると、失敗した例題とその原因が (場合によっては複数) :func:`testmod`
と同じ書式で標準出力に書き出されます。

デフォルトでは、 :func:`testfile` は自分自身を呼び出したモジュールのあるディレクトリを探します。
その他の場所にあるファイルを見に行くように :func:`testfile`
に指示するためのオプション引数についての説明は :ref:`doctest-basic-api`
節を参照してください。

Python 2.6 からは :func:`testfile` を実行するコマンドラインショートカットがあります。
Python インタプリタに doctest モジュールを標準ライブラリから直接実行して、テストする
モジュール名をコマンドライン引数に与えます。::

   python -m doctest -v example.txt

ファイル名が :file:`.py` で終っていないので、 :mod:`doctest` は :func:`testmod` ではなく
:func:`testfile` を使って実行するのだと判断します。

:func:`testfile` の詳細は :ref:`doctest-basic-api` 節を参照してください。


.. _doctest-how-it-works:

doctest のからくり
------------------

この節では、doctest のからくり: どの docstring を見に行くのか、
どうやって対話操作例を見つけ出すのか、どんな実行コンテキストを使うのか、
例外をどう扱うか、上記の振る舞いを制御するためにどのようなオプションフラグを使うか、について詳しく吟味します。
こうした情報は、 doctest に対応した例題を書くために必要な知識です;
書いた例題に対して実際に doctest を実行する上で必要な情報については後続の節を参照してください。


.. _doctest-which-docstrings:

どのドキュメンテーション文字列が検証されるのか?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

モジュールのドキュメンテーション文字列、全ての関数、クラスおよびメソッドのドキュメンテーション文字列が検索されます。
モジュールに import されたオブジェクトは検索されません。

加えて、 ``M.__test__`` が存在し、 "真の値を持つ" 場合、この値は辞書で、辞書の各エントリは (文字列の) 名前を
関数オブジェクト、クラスオブジェクト、または文字列に対応付けていなくてはなりません。
``M.__test__``  から得られた関数およびクラスオブジェクトのドキュメンテーション文字列は、
その名前がプライベートなものでも検索され、
文字列の場合にはそれがドキュメンテーション文字列であるかのように直接検索を行います。
出力においては、 ``M.__test__``  におけるキー ``K`` は、 ::

   <name of M>.__test__.K

のように表示されます。

検索中に見つかったクラスも同様に再帰的に検索が行われ、
クラスに含まれているメソッドおよびネストされたクラスについて
ドキュメンテーション文字列のテストが行われます。

.. versionchanged:: 2.4
   "プライベート名" の概念は撤廃されたため、今後はドキュメントにしません.


.. _doctest-finding-examples:

ドキュメンテーション文字列内の例をどうやって認識するのか?
---------------------------------------------------------

ほとんどの場合、対話コンソールセッション上でのコピー／ペーストはうまく動作します。
とはいえ、 :mod:`doctest` は特定の Python シェルの振る舞いを正確にエミュレーションしようとするわけではありません。
ハードタブは全て 8 カラムのタブストップを使ってスペースに展開されます。
従って、タブがそのように表現されると考えておかないととまずいことになります:
その場合は、ハードタブを使わないか、自前で :class:`DocTestParser` クラスを書いてください。

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

出力結果例  (expected output) は、コードを含む最後の ``'>>> '`` or ``'... '`` 行の直下に続きます。
また、出力結果例 (がある場合) は、次の ``'>>> '`` 行か、全て空白文字の行まで続きます。

細かな注意:

* 出力結果例には、全て空白の行が入っていてはなりません。
  そのような行は出力結果例の終了を表すと見なされるからです。
  もし予想出力結果の内容に空白行が入っている場合には、空白行が入るべき場所全てに ``<BLANKLINE>`` を入れてください。

  .. versionchanged:: 2.4
     ``<BLANKLINE>`` を追加しました; 以前のバージョンでは、空白行の入った予想出力結果を扱う方法がありませんでした.

* stdout への出力は取り込まれますが、stderr は取り込まれません (例外発生時のトレースバックは別の方法で取り込まれます)。

* 対話セッションにおいて、バックスラッシュを用いて次の行に続ける場合や、
  その他の理由でバックスラッシュを用いる場合、raw docstring を使って
  バックスラッシュを入力どおりに扱わせるようにせねばなりません::

     >>> def f(x):
     ...     r'''Backslashes in a raw docstring: m\n'''
     >>> print f.__doc__
     Backslashes in a raw docstring: m\n

  こうしなければ、バックスラッシュは文字列の一部として解釈されてしまいます。
  例えば、上の例の "\\" は改行文字として認識されてしまうでしょう。
  こうする代わりに、(raw docstring を使わずに) doctest 版の中ではバックスラッシュを全て二重にしてもかまいません::

     >>> def f(x):
     ...     '''Backslashes in a raw docstring: m\\n'''
     >>> print f.__doc__
     Backslashes in a raw docstring: m\n

* 開始カラムはどこでもかまいません::

     >>> assert "Easy!"
           >>> import math
               >>> math.floor(1.9)
               1.0

  出力結果例の先頭部にある空白文字列は、例題の開始部分にあたる ``'>>> '`` 行の先頭にある空白文字列と同じだけはぎとられます。


実行コンテキストとは何か?
-------------------------

デフォルトでは、 :mod:`doctest` はテストを行うべき docstring を見つけるたびに
:mod:`M` のグローバル名前空間の *浅いコピー* を使い、
テストの実行によってモジュールの実際のグローバル名前空間を変更しないようにし、
かつ :mod:`M` 内で行ったテストが痕跡を残して偶発的に別のテストを誤って動作させないようにしています。
従って、例題中では :mod:`M` 内のトップレベルで定義されたすべての名前と、
docstring ドキュメンテーション文字列が動作する以前に定義された名前を自由に使えます。
個々の例題は他の docstring 中で定義された名前を参照できません。

:func:`testmod` や :func:`testfile` に ``globs=your_dict`` を渡し、
自前の辞書を実行コンテキストとして使うこともできます。


例外はどう扱えばよいのですか?
-----------------------------

例で生成される出力がトレースバックのみである限り問題ありません:
単にトレースバックを貼り付けてください。 [#]_
トレースバックには、頻繁に変更されがちな情報が入っている (例えばファイルパスや行番号など) ものなので、
受け入れるべきテスト結果に柔軟性を持たせようと doctest が苦労している部分の一つです。

簡単な例を示しましょう::

   >>> [1, 2, 3].remove(42)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: list.remove(x): x not in list
   >>>

この doctest は :exc:`ValueError` が送出され、かつ詳細情報に ``list.remove(x): x not in list``
が入っている場合にのみ成功します。

例外が発生したときの予想出力はトレースバックヘッダから始まっていなければなりません。
トレースバックの形式は以下の二通りの行のいずれかでよく、
例題の最初の行と同じインデントでなければりません::

   Traceback (most recent call last):
   Traceback (innermost last):

トレースバックヘッダの後ろにトレースバックスタックを続けてもかまいませんが、
doctest はその内容を無視します。
普通はトレースバックスタックを無視するか、対話セッションからそのままコピーしてきます。

トレースバックスタックの後ろにはもっとも有意義な部分、例外の型と詳細情報の入った行があります。
通常、この行はトレースバックの末尾にあるのですが、例外が複数行の詳細情報を持っている場合、
複数の行にわたることもあります::

   >>> raise ValueError('multi\n    line\ndetail')
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: multi
       line
   detail

上の例では、最後の 3 行 (:exc:`ValueError` から始まる行) における例外の型と詳細情報だけが比較され、
それ以外の部分は無視されます。

例外を扱うコツは、例題をドキュメントとして読む上で明らかに価値のある情報でない限り、
トレースバックスタックは無視する、ということです。従って、先ほどの例は以下のように書くべきでしょう::

   >>> raise ValueError('multi\n    line\ndetail')
   Traceback (most recent call last):
       ...
   ValueError: multi
       line
   detail

トレースバックの扱いは非常に特殊なので注意してください。
特に、上の書き直した例題では、 ``...`` の扱いが doctest の
:const:`ELLIPSIS` オプションによって変わります。
この例での省略記号は何かの省略を表しているかもしれませんし、
コンマや数字が 3 個 (または 300 個) かもしれませんし、
Monty Python のスキットをインデントして書き写したものかもしれません。

以下の詳細はずっと覚えておく必要はないのですが、一度目を通しておいてください:

* doctest は予想出力の出所が print 文なのか例外なのかを推測できません。
  従って、例えば予想出力が ``ValueError: 42 is prime``  であるような例題は、
  :exc:`ValueError` が実際に送出された場合と、万が一予想出力と同じ文字列を
  print した場合の両方でパスしてしまいます。
  現実的には、通常の出力がトレースバックヘッダから始まることはないので、
  さしたる問題にはなりません。

* トレースバックスタック (がある場合) の各行は、例題の最初の行よりも深くインデントされているか、
  *または* 英数文字以外で始まっていなければなりません。
  トレースバックヘッダ以後に現れる行のうち、インデントが等しく英数文字で始まる最初の行は
  例外の詳細情報が書かれた行とみなされるからです。
  もちろん、通常のトレースバックでは全く正しく動作します。

* doctest のオプション :const:`IGNORE_EXCEPTION_DETAIL` を指定した場合、
  最も左端のコロン以後の内容が無視されます。

* 対話シェルでは、 :exc:`SyntaxError` の場合にトレースバックヘッダを無視することがあります。
  しかし doctest にとっては、例外を例外でないものと区別するためにトレースバックヘッダが必要です。
  そこで、トレースバックヘッダを省略するような :exc:`SyntaxError` 
  をテストする必要があるというごく稀なケースでは、
  例題に自分で作ったトレースバックヘッダを追加する必要があるでしょう。

* :exc:`SyntaxError` の場合、 Python は構文エラーの起きた場所を ``^`` マーカで表示します::

     >>> 1 1
       File "<stdin>", line 1
         1 1
           ^
     SyntaxError: invalid syntax

  例外の型と詳細情報の前にエラー位置を示す行がくるため、 doctest はこの行を調べません。
  例えば、以下の例では、間違った場所に ``^`` マーカを入れてもパスしてしまいます::

     >>> 1 1
     Traceback (most recent call last):
       File "<stdin>", line 1
         1 1
         ^
     SyntaxError: invalid syntax

.. versionchanged:: 2.4
   複数行からなる例外の詳細情報を扱えるようにし、 doctest オプション :const:`IGNORE_EXCEPTION_DETAIL` を追加しました.


.. _doctest-options:

オプションフラグとディレクティブ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

doctest では、その挙動の様々な側面をたくさんのオプションフラグで制御しています。各フラグのシンボル名はモジュールの定数として提供されて
おり、論理和で組み合わせて様々な関数に渡せるようになっています。シンボル名は doctest のディレクティブ (directive, 下記参照) としても
使えます。

最初に説明するオプション群は、テストのセマンティクスを決めます。すなわち、実際にテストを実行したときの出力と例題中の予想出力とが一致しているかどうかを
doctest がどうやって判断するかを制御します:


.. data:: DONT_ACCEPT_TRUE_FOR_1

   デフォルトでは、予想出力ブロックに単に ``1`` だけが入っており、実際の出力ブロックに ``1`` または ``True``
   だけが入っていた場合、これらの出力は一致しているとみなされます。
   ``0`` と ``False`` の場合も同様です。
   :const:`DONT_ACCEPT_TRUE_FOR_1` を指定すると、こうした値の読み替えを行いません。
   デフォルトの挙動で読み替えを行うのは、最近の Python で多くの関数の戻り値型が整数型からブール型に
   変更されたことに対応するためです; 読み替えを行う場合、"通常の整数" の出力を予想出力とするような
   doctest も動作します。このオプションはそのうち無くなるでしょうが、ここ数年はそのままでしょう。


.. data:: DONT_ACCEPT_BLANKLINE

   デフォルトでは、予想出力ブロックに ``<BLANKLINE>`` だけの入った行がある場合、
   その行は実際の出力における空行に一致するようになります。
   完全な空行を入れてしまうと予想出力がそこで終わっているとみなされてしまうため、
   空行を予想出力に入れたい場合にはこの方法を使わねばなりません。
   :const:`DONT_ACCEPT_BLANKLINE` を指定すると、 ``<BLANKLINE>`` の読み替えを行わなくなります。


.. data:: NORMALIZE_WHITESPACE

   このフラグを指定すると、空白 (空白と改行文字) の列は互いに等価であるとみなします。
   予想出力における任意の空白列は実際の出力における任意の空白と一致します。
   デフォルトでは、空白は厳密に一致せねばなりません。
   :const:`NORMALIZE_WHITESPACE` は、予想出力の内容が非常に長いために、
   ソースコード中でその内容を複数行に折り返して書きたい場合に特に便利です。


.. data:: ELLIPSIS

   このフラグを指定すると、予想出力中の省略記号マーカ (``...``) 
   を実際の出力中の任意の部分文字列に一致させられます。
   部分文字列は行境界にわたるものや空文字列を含みます。
   従って、このフラグを使うのは単純な内容を対象にする場合にとどめましょう。
   複雑な使い方をすると、正規表現に ``.*`` を使ったときのように
   "あらら、省略部分をマッチがえてる (match too much) ！"  と驚くことになりかねません。


.. data:: IGNORE_EXCEPTION_DETAIL

   このフラグを指定すると、予想される実行結果に例外が入るような例題で、
   予想通りの型の例外が送出された場合に、例外の詳細情報が一致していなくてもテストをパスさせます。
   例えば、予想出力が ``ValueError: 42`` であるような例題は、
   実際に送出された例外が ``ValueError: 3*14``  でもパスしますが、
   :exc:`TypeError` が送出されるといった場合にはパスしません。

   :const:`ELLIPSIS` を使っても同様のことができ、 :const:`IGNORE_EXCEPTION_DETAIL`
   はリリース 2.4 以前の Python を使う人がほとんどいなくなった時期を見計らって
   撤廃するかもしれないので気をつけてください。
   それまでは、 :const:`IGNORE_EXCEPTION_DETAIL` は 2.4 以前の Python で
   例外の詳細については気にせずテストをパスさせるように
   doctest を書くための唯一の明確な方法です。例えば、 ::

      >>> (1, 2)[3] = 'moo' #doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
        File "<stdin>", line 1, in ?
      TypeError: object doesn't support item assignment

   にすると、 Python 2.4 と Python 2.3 の両方でテストをパスさせられます。
   というのは、例外の詳細情報は 2.4 で変更され、 "doesn't" から "does not" と書くようになったからです。


.. data:: SKIP

   このフラグを指定すると、例題は一切実行されません。
   こうした機能は doctest の実行例がドキュメントとテストを兼ねていて、
   ドキュメントのためには含めておかなければならないけれどチェックされなくても良い、
   というような文脈で役に立ちます。
   例えば、実行例の出力がランダムであるとか、
   テスト機構には手が届かない資源に依存している場合などです。

   SKIP フラグは一時的に例題を"コメントアウト"するのにも使えます。


.. data:: COMPARISON_FLAGS

   上記の比較フラグ全ての論理和をとったビットマスクです。

二つ目のオプション群は、テストの失敗を報告する方法を制御します:


.. data:: REPORT_UDIFF

   このオプションを指定すると、複数行にわたる予想出力や実際の出力を、一元化 (unified) diff を使って表示します。


.. data:: REPORT_CDIFF

   このオプションを指定すると、複数行にわたる予想出力や実際の出力を、コンテキスト diff を使って表示します。


.. data:: REPORT_NDIFF

   このオプションを指定すると、予想出力と実際の出力との間の差分をよく知られている :file:`ndiff.py`
   ユーティリティと同じアルゴリズムを使っている ``difflib.Differ`` で分析します。
   これは、行単位の差分と同じように行内の差分にマーカをつけられるようにする唯一の手段です。
   例えば、予想出力のある行に数字の ``1`` が入っていて、実際の出力には ``l`` が入っている場合、
   不一致のおきているカラム位置を示すキャレットの入った行が一行挿入されます。


.. data:: REPORT_ONLY_FIRST_FAILURE

   このオプションを指定すると、各 doctest で最初にエラーの起きた例題だけを表示し、
   それ以後の例題の出力を抑制します。これにより、正しく書かれた例題が、
   それ以前の例題の失敗によっておかしくなってしまった場合に、
   doctest がそれを報告しないようになります。
   とはいえ、最初に失敗を引き起こした例題とは関係なく誤って書かれた例題の報告も抑制してしまいます。
   :const:`REPORT_ONLY_FIRST_FAILURE` を指定した場合、例題がどこかで失敗しても、
   それ以後の例題を続けて実行し、失敗したテストの総数を報告します; 出力が抑制されるだけです。


.. data:: REPORTING_FLAGS

   上記のエラー報告に関するフラグ全ての論理和をとったビットマスクです。

「doctest ディレクティブ」を使うと、個々の例題に対してオプションフラグの設定を変更できます。 doctest ディレクティブは特殊な Python
コメント文として表現され、例題のソースコードの後に続けます:

.. productionlist:: doctest
   directive: "#" "doctest:" `directive_options`
   directive_options: `directive_option` ("," `directive_option`)\*
   directive_option: `on_or_off` `directive_option_name`
   on_or_off: "+" \| "-"
   directive_option_name: "DONT_ACCEPT_BLANKLINE" \| "NORMALIZE_WHITESPACE" \| ...

``+`` や ``-`` とディレクティブオプション名の間に空白を入れてはなりません。
ディレクティブオプション名は上で説明したオプションフラグ名のいずれかです。

ある例題の doctest ディレクティブは、その例題だけの doctest の振る舞いを変えます。
ある特定の挙動を有効にしたければ ``+`` を、無効にしたければ ``-`` を使います。

例えば、以下のテストはパスします::

   >>> print range(20) #doctest: +NORMALIZE_WHITESPACE
   [0,   1,  2,  3,  4,  5,  6,  7,  8,  9,
   10,  11, 12, 13, 14, 15, 16, 17, 18, 19]

ディレクティブがない場合、実際の出力には一桁の数字の間に二つスペースが入っていないこと、
実際の出力は 1 行になることから、テストはパスしないはずです。
別のディレクティブを使って、このテストをパスさせることもできます::

   >>> print range(20) # doctest:+ELLIPSIS
   [0, 1, ..., 18, 19]

複数のディレクティブは、一つの物理行の中にコンマで区切って指定できます::

   >>> print range(20) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
   [0,    1, ...,   18,    19]

一つの例題中で複数のディレクティブコメントを使った場合、それらは組み合わされます::

   >>> print range(20) # doctest: +ELLIPSIS
   ...                 # doctest: +NORMALIZE_WHITESPACE
   [0,    1, ...,   18,    19]

前の例題で示したように、 ``...`` の後ろにディレクティブだけの入った行を例題のうしろに追加して書けます。
この書きかたは、例題が長すぎるためにディレクティブを同じ行に入れると収まりが悪い場合に便利です::

   >>> print range(5) + range(10,20) + range(30,40) + range(50,60)
   ... # doctest: +ELLIPSIS
   [0, ..., 4, 10, ..., 19, 30, ..., 39, 50, ..., 59]

デフォルトでは全てのオプションが無効になっており、ディレクティブは特定の例題だけに影響を及ぼすので、
通常意味があるのは有効にするためのオプション(``+`` のついたディレクティブ) だけです。
とはいえ、 doctest を実行する関数はオプションフラグを指定してデフォルトとは異なった挙動を実現できるので、
そのような場合には ``-`` を使った無効化オプションも意味を持ちます。

.. versionchanged:: 2.4
   定数 :const:`DONT_ACCEPT_BLANKLINE`, :const:`NORMALIZE_WHITESPACE`,
   :const:`ELLIPSIS`, :const:`IGNORE_EXCEPTION_DETAIL`, :const:`REPORT_UDIFF`,
   :const:`REPORT_CDIFF`, :const:`REPORT_NDIFF`,
   :const:`REPORT_ONLY_FIRST_FAILURE`, :const:`COMPARISON_FLAGS`,
   :const:`REPORTING_FLAGS` を追加しました。予想出力中の ``<BLANKLINE>`` がデフォルトで
   実際の出力中の空行にマッチするようになりました。また、 doctest ディレクティブが追加されました.

.. versionchanged:: 2.5
   定数 :const:`SKIP` が追加されました.

新たなオプションフラグ名を登録する方法もありますが、 :mod:`doctest` の内部をサブクラスで拡張しない限り、意味はないでしょう:


.. function:: register_optionflag(name)

   名前 *name* の新たなオプションフラグを作成し、作成されたフラグの整数値を返します。
   :func:`register_optionflag` は :class:`OutputChecker` や  :class:`DocTestRunner` をサブクラス化して、
   その中で新たに作成したオプションをサポートさせる際に使います。
   :func:`register_optionflag` は以下のような定形文で呼び出さねばなりません::

      MY_FLAG = register_optionflag('MY_FLAG')

   .. versionadded:: 2.4


.. _doctest-warnings:

注意
^^^^

:mod:`doctest` では、予想出力に対する厳密な一致を厳しく求めています。
一致しない文字が一文字でもあると、テストは失敗してしまいます。
このため、Python が出力に関して何を保証していて、何を保証していないかを正確に知っていないと幾度か混乱させられることでしょう。
例えば、辞書を出力する際、Python はキーと値のペアが常に特定の順番で並ぶよう保証してはいません。従って、以下のようなテスト ::

   >>> foo()
   {"Hermione": "hippogryph", "Harry": "broomstick"}

は失敗するかもしれないのです! 回避するには ::

   >>> foo() == {"Hermione": "hippogryph", "Harry": "broomstick"}
   True

とするのが一つのやり方です。別のやり方は、 ::

   >>> d = foo().items()
   >>> d.sort()
   >>> d
   [('Harry', 'broomstick'), ('Hermione', 'hippogryph')]

です。

他にもありますが、自分で考えてみてください。

以下のように、オブジェクトアドレスを埋め込むような結果を print するのもよくありません::

   >>> id(1.0) # certain to fail some of the time
   7948648
   >>> class C: pass
   >>> C()   # the default repr() for instances embeds an address
   <__main__.C instance at 0x00AC18F0>

:const:`ELLIPSIS` ディレクティブを使うと、上のような例をうまく解決できます::

   >>> C() #doctest: +ELLIPSIS
   <__main__.C instance at 0x...>

浮動小数点数もまた、プラットフォーム間での微妙な出力の違いの原因となります。
というのも、Python は浮動小数点の書式化をプラットフォームの  C ライブラリにゆだねており、
この点では、C ライブラリはプラットフォーム間で非常に大きく異なっているからです。 ::

   >>> 1./7  # risky
   0.14285714285714285
   >>> print 1./7 # safer
   0.142857142857
   >>> print round(1./7, 6) # much safer
   0.142857

``I/2.**J`` の形式になる数値はどのプラットフォームでもうまく動作するので、
私はこの形式の数値を生成するように doctest の例題を工夫しています::

   >>> 3./4  # utterly safe
   0.75

このように、単分数 (simple fraction) を使えば、人間にとっても理解しやすくよいドキュメントになります。


.. _doctest-basic-api:

基本 API
--------

関数 :func:`testmod` および :func:`testfile` は、基本的なほとんどの用途に十分な doctest
インタフェースを提供しています。これら二つの関数についてもっとくだけた説明を読みたければ、
:ref:`doctest-simple-testmod` 節および :ref:`doctest-simple-testfile` 節を参照してください。


.. function:: testfile(filename[, module_relative][, name][, package][, globs][, verbose][, report][, optionflags][, extraglobs][, raise_on_error][, parser][, encoding])

   *filename* 以外の引数は全てオプションで、キーワード引数形式で指定せねばなりません。

   *filename* に指定したファイル内にある例題をテストします。 ``(failure_count, test_count)`` を返します。

   オプション引数の *module_relative* は、ファイル名をどのように解釈するかを指定します:

   * *module_relative* が ``True`` (デフォルト) の場合、 *filename* は OS
     に依存しないモジュールの相対パスになります。デフォルトでは、このパスは関数 :func:`testfile` を呼び出して
     いるモジュールからの相対パスになります; ただし、 *package* 引数を指定した場合には、パッケージからの相対になります。
     OS への依存性を除くため、 *filename*  ではパスを分割する文字に ``/`` を使わねばならず、
     絶対パスにしてはなりません (パス文字列を ``/`` で始めてはなりません)。

   * *module_relative* が ``False`` の場合、 *filename* は OS 依存のパスを示します。
     パスは絶対パスでも相対パスでもかまいません; 相対パスにした場合、現在の作業ディレクトリを基準に解決します。

   オプション引数 *name* には、テストの名前を指定します; デフォルトの場合や ``None`` を指定した場合、
   ``os.path.basename(filename)`` になります。

   オプション引数 *package* には、 Python パッケージを指定するか、モジュール相対のファイル名の場合には
   相対の基準ディレクトリとなる Python パッケージの名前を指定します。
   パッケージを指定しない場合、関数を呼び出しているモジュールのディレクトリを相対の基準ディレクトリとして使います。
   *module_relative* を ``False`` に指定している場合、 *package* を指定するとエラーになります。

   オプション引数 *globs* には辞書を指定します。この辞書は、例題を実行する際のグローバル変数として用いられます。
   doctest はこの辞書の浅いコピーを生成するので、例題は白紙の状態からスタートします。
   デフォルトの場合や ``None`` を指定した場合、新たな空の辞書になります。

   オプション引数 *extraglobs* には辞書を指定します。この辞書は、例題を実行する際にグローバル変数にマージされます。
   マージは :meth:`dict.update` のように振舞います: *globs* と *extraglobs* との間に同じキー値がある場合、両者を合わせた
   辞書中には *extraglobs* の方の値が入ります。この仕様は、パラメタ付きで doctest を実行するという、やや進んだ機能です。
   例えば、一般的な名前を使って基底クラス向けに doctest を書いておき、
   その後で辞書で一般的な名前からテストしたいサブクラスへの対応付けを行う辞書を *extraglobs* に渡して、
   様々なサブクラスをテストできます。

   オプション引数 *verbose* が真の場合、様々な情報を出力します。偽の場合にはテストの失敗だけを報告します。
   デフォルトの場合や ``None`` を指定した場合、 ``sys.argv`` に ``-v`` を指定しない限りこの値は真になりません。

   オプション引数 *report* が真の場合、テストの最後にサマリを出力します。
   それ以外の場合には何も出力しません。
   verbose モードの場合、サマリには詳細な情報を出力しますが、
   そうでない場合にはサマリはとても簡潔になります (実際には、全てのテストが成功した場合には何も出力しません)。

   オプション引数 *optionflags* は、各オプションフラグの論理和をとった値を指定します。 :ref:`doctest-options`
   節を参照してください。

   オプション引数 *raise_on_error* の値はデフォルトでは偽です。
   真にすると、最初のテスト失敗や予期しない例外が起きたときに例外を送出します。
   このオプションを使うと、失敗の原因を検死デバッグ (post-mortem debug) できます。
   デフォルトの動作では、例題の実行を継続します。

   オプション引数 *parser* には、 :class:`DocTestParser` (またはそのサブクラス) を指定します。
   このクラスはファイルから例題を抽出するために使われます。デフォルトでは通常のパーザ  (``DocTestParser()``) です。

   オプション引数 *encoding* にはファイルをユニコードに変換する際に使われるエンコーディングを指定します。

   .. versionadded:: 2.4

   .. versionchanged:: 2.5
      *encoding* パラメタが追加されました.


.. function:: testmod([m][, name][, globs][, verbose][, report][, optionflags][, extraglobs][, raise_on_error][, exclude_empty])

   引数は全てオプションで、 *m* 以外の引数はキーワード引数として指定せねばなりません。

   モジュール *m* (*m* を指定しないか ``None`` にした場合には :mod:`__main__`) から到達可能な関数およびクラスの
   docstring 内にある例題をテストします。 ``m.__doc__`` 内の例題からテストを開始します。

   また、辞書 ``m.__test__`` が存在し、 ``None``  でない場合、この辞書から到達できる例題もテストします。
   ``m.__test__`` は、(文字列の) 名前から関数、クラスおよび文字列への対応付けを行っています。
   関数およびクラスの場合には、その docstring 内から例題を検索します。
   文字列の場合には、docstring と同じようにして例題の検索を直接実行します。

   モジュール *m* に属するオブジェクトにつけられた docstrings のみを検索します。

   ``(failure_count, test_count)`` を返します。

   オプション引数 *name* には、モジュールの名前を指定します。デフォルトの場合や ``None`` を指定した場合には、
   ``m.__name__`` を使います。

   オプション引数 *exclude_empty* はデフォルトでは偽になっています。
   この値を真にすると、doctest を持たないオブジェクトを考慮から外します。
   デフォルトの設定は依存のバージョンとの互換性を考えたハックであり、 :meth:`doctest.master.summarize` と
   :func:`testmod` を合わせて利用しているようなコードでも、
   テスト例題を持たないオブジェクトから出力を得るようにしています。
   新たに追加された :class:`DocTestFinder` のコンストラクタの *exclude_empty* はデフォルトで真になります。

   オプション引数 *extraglobs*, *verbose*, *report*, *optionflags*, *raise_on_error*, および
   *globs* は上で説明した :func:`testfile` の引数と同じです。ただし、 *globs* のデフォルト値は ``m.__dict__``
    になります。

   .. versionchanged:: 2.3
      *optionflags* パラメタを追加しました.

   .. versionchanged:: 2.4
      *extraglobs*, *raise_on_error* および *exclude_empty* パラメタを追加しました.

   .. versionchanged:: 2.5
      オプション引数 *isprivate* は、2.4 では非推奨でしたが、廃止されました.

単一のオブジェクトに関連付けられた doctest を実行するための関数もあります。
この関数は以前のバージョンとの互換性のために提供されています。
この関数を撤廃する予定はありませんが、役に立つことはほとんどありません:


.. function:: run_docstring_examples(f, globs[, verbose][, name][, compileflags][, optionflags])

   オブジェクト *f* に関連付けられた例題をテストします。 *f* はモジュール、関数、またはクラスオブジェクトです。

   引数 *globs* に辞書を指定すると、その浅いコピーを実行コンテキストに使います。

   オプション引数 *name* はテスト失敗時のメッセージに使われます。デフォルトの値は ``NoName`` です。

   オプション引数 *verbose* の値を真にすると、テストが失敗しなくても出力を生成します。
   デフォルトでは、例題のテストに失敗したときのみ出力を生成します。

   オプション引数 *compileflags* には、例題を実行するときに Python バイトコードコンパイラが使うフラグを指定します。
   デフォルトの場合や ``None`` を指定した場合、フラグは *globs* 内にある future 機能セットに対応したものになります。

   オプション引数 *optionflags* は、上で述べた :func:`testfile` と同様の働きをします。


.. _doctest-unittest-api:

単位テスト API
--------------

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
こうしたテストスイートは、 :mod:`unittest` のテストランナを使って実行できます::

   import unittest
   import doctest
   import my_module_with_doctests, and_another

   suite = unittest.TestSuite()
   for mod in my_module_with_doctests, and_another:
       suite.addTest(doctest.DocTestSuite(mod))
   runner = unittest.TextTestRunner()
   runner.run(suite)

doctest の入ったテキストファイルやモジュールから :class:`unittest.TestSuite` インスタンスを生成するための
主な関数は二つあります:


.. function:: DocFileSuite([module_relative][, package][, setUp][, tearDown][, globs][, optionflags][, parser][, encoding])

   単一または複数のテキストファイルに入っている doctest 形式のテストを、 :class:`unittest.TestSuite`
   インスタンスに変換します。

   この関数の返す :class:`unittest.TestSuite` インスタンスは、 unittest
   フレームワークで動作させ、各ファイルの例題を対話的に実行するためのものです。
   ファイル内の何らかの例題の実行に失敗すると、この関数で生成した単位テストは失敗し、
   該当するテストの入っているファイルの名前と、 (場合によりだいたいの) 行番号の入った :exc:`failureException`
   例外を送出します。

   関数には、テストを行いたい一つまたは複数のファイルへのパスを (文字列で) 渡します。

   :func:`DocFileSuite` には、キーワード引数でオプションを指定できます:

   オプション引数 *module_relative* は *paths* に指定したファイル名をどのように解釈するかを指定します:

   * *module_relative* が ``True`` (デフォルト) の場合、 *filename* は OS
     に依存しないモジュールの相対パスになります。デフォルトでは、このパスは関数 :func:`testfile` を呼び出して
     いるモジュールからの相対パスになります; ただし、 *package* 引数を指定した場合には、
     パッケージからの相対になります。 OS への依存性を除くため、 *filename* ではパスを分割する文字に
     ``/`` を使わねばならず、絶対パスにしてはなりません (パス文字列を ``/`` で始めてはなりません)。

   * *module_relative* が ``False`` の場合、 *filename* は OS 依存のパスを示します。パスは絶対パスでも相対パスでも
     かまいません; 相対パスにした場合、現在の作業ディレクトリを基準に解決します。

   オプション引数 *package* には、 Python パッケージを指定するか、
   モジュール相対のファイル名の場合には相対の基準ディレクトリとなる Python パッケージの名前を指定します。
   パッケージを指定しない倍、関数を呼び出しているモジュールのディレクトリを相対の基準ディレクトリとして使います。
   *module_relative* を ``False`` に指定している場合、 *package* を指定するとエラーになります。

   オプション引数 *setUp* には、テストスイートのセットアップに使う関数を指定します。
   この関数は、各ファイルのテストを実行する前に呼び出されます。
   *setUp* 関数は :class:`DocTest` オブジェクトに引き渡されます。
   *setUp* は *globs* 属性を介してテストのグローバル変数にアクセスできます。

   オプション引数 *tearDown* には、テストを解体 (tear-down) するための関数を指定します。
   この関数は、各ファイルのテストの実行を終了するたびに呼び出されます。
   *tearDown* 関数は :class:`DocTest`  オブジェクトに引き渡されます。
   *tearDown* は *globs* 属性を介してテストのグローバル変数にアクセスできます。

   オプション引数 *globs* は辞書で、テストのグローバル変数の初期値が入ります。
   この辞書は各テストごとに新たにコピーして使われます。
   デフォルトでは *globs* は空の新たな辞書です。

   オプション引数 *optionflags* には、テストを実行する際にデフォルトで適用される
   doctest オプションを OR で結合して指定します。
   :ref:`doctest-options` 節を参照してください。
   結果レポートに関するオプションの指定する上手いやり方は下記の :func:`set_unittest_reportflags`
   の説明を参照してください。

   オプション引数 *parser* には、ファイルからテストを抽出するために使う :class:`DocTestParser` (またはサブクラス)
   を指定します。デフォルトは通常のパーザ (``DocTestParser()``) です。

   オプション引数 *encoding* にはファイルをユニコードに変換する際に使われるエンコーディングを指定します。

   .. versionadded:: 2.4

   .. versionchanged:: 2.5
      グローバル変数 ``__file__`` が追加され :func:`DocFileSuite` を使ってテキストファイルから読み込まれた doctest
      に提供されます.

   .. versionchanged:: 2.5
      *encoding* パラメタが追加されました.


.. function:: DocTestSuite([module][, globs][, extraglobs][, test_finder][, setUp][, tearDown][, checker])

   doctest のテストを :class:`unittest.TestSuite` に変換します。

   この関数の返す :class:`unittest.TestSuite` インスタンスは、 unittest フレームワークで動作させ、モジュール内の各
   doctest を実行するためのものです。何らかの doctest の実行に失敗すると、この関数で
   生成した単位テストは失敗し、該当するテストの入っているファイルの名前と、 (場合によりだいたいの) 行番号の入った :exc:`failureException`
   例外を送出します。

   オプション引数 *module* には、テストしたいモジュールの名前を指定します。 *module* にはモジュールオブジェクトまたは (ドット表記の)
   モジュール名を指定できます。 *module* を指定しない場合、この関数を呼び出しているモジュールになります。

   オプション引数 *globs* は辞書で、テストのグローバル変数の初期値が入ります。この辞書は各テストごとに新たにコピーして使われ
   ます。デフォルトでは *glob* は空の新たな辞書です。

   オプション引数 *extraglobs* には追加のグローバル変数セットを指定します。この変数セットは *globs* に統合されます。
   デフォルトでは、追加のグローバル変数はありません。

   オプション引数 *test_finder* は、モジュールから doctest を抽出するための :class:`DocTestFinder` オブジェクト
   (またはその代用となるオブジェクト) です。

   オプション引数 *setUp* 、 *tearDown* 、および *optionflags* は上の :func:`DocFileSuite` と同じです。

   .. versionadded:: 2.3

   .. versionchanged:: 2.4
      *globs*, *extraglobs*, *test_finder*, *setUp*, *tearDown*, および *optionflags*
      パラメタを追加しました。また、この関数は doctest の検索に :func:`testmod` と同じテクニックを使うようになりました.

:func:`DocTestSuite` は水面下では :class:`doctest.DocTestCase`
インスタンスから :class:`unittest.TestSuite` を作成しており、 :class:`DocTestCase`
は :class:`unittest.TestCase` のサブクラスになっています。 :class:`DocTestCase` についてはここでは説明しません
(これは内部実装上の詳細だからです) が、そのコードを調べてみれば、 :mod:`unittest` の組み込みの詳細に関する疑問を解決できるはずです。

同様に、 :func:`DocFileSuite` は :class:`doctest.DocFileCase`
インスタンスから :class:`unittest.TestSuite` を作成し、 :class:`DocFileCase` は
:class:`DocTestCase` のサブクラスになっています。これにははっきりとした訳があります: :mod:`doctest`
関数を自分で実行する場合、オプションフラグを :mod:`doctest` 関数に渡すことで、 :mod:`doctest`
のオプションを直接操作できます。しかしながら、 :mod:`unittest` フレームワークを書いている場合には、いつどのようにテストを動作させるかを
:mod:`unittest` が完全に制御してしまいます。フレームワークの作者はたいてい、 :mod:`doctest` のレポートオプションを
(コマンドラインオプションで指定するなどして) 操作したいと考えますが、 :mod:`unittest` を介して :mod:`doctest`
のテストランナにオプションを渡す方法は存在しないのです。

このため、 :mod:`doctest` では、以下の関数を使って、 :mod:`unittest` サポート
に特化したレポートフラグ表記方法もサポートしています:


.. function:: set_unittest_reportflags(flags)

   :mod:`doctest` のレポートフラグをセットします。

   引数 *flags* にはオプションフラグを OR で結合して渡します。
   :ref:`doctest-options` 節を参照してください。「レポートフラグ」しか使えません。

   この関数で設定した内容はモジュール全体にわたる物であり、関数呼び出し以後に :mod:`unittest` モジュールから実行される全ての doctest
   に影響します: :class:`DocTestCase` の :meth:`runTest` メソッドは、 :class:`DocTestCase`
   インスタンスが作成された際に、現在のテストケースに指定されたオプションフラグを見に行きます。レポートフラグが指定されていない場合
   (通常の場合で、望ましいケースです)、 :mod:`doctest` の :mod:`unittest` レポートフラグが OR で結合され、doctest
   を実行するために作成される :class:`DocTestRunner`  インスタンスに渡されます。 :class:`DocTestCase`
   インスタンスを構築する際に何らかのレポートフラグが指定されていた場合、 :mod:`doctest` の :mod:`unittest`
   レポートフラグは無視されます。

   この関数は、関数を呼び出す前に有効になっていた :mod:`unittest`  レポートフラグの値を返します。

   .. versionadded:: 2.4


.. _doctest-advanced-api:

拡張 API
--------

基本 API は、 doctest を使いやすくするための簡単なラッパであり、柔軟性があってほとんどのユーザの必要を満たしています; とはいえ、
もっとテストをきめ細かに制御したい場合や、 doctest の機能を拡張したい場合、拡張 API (advanced API) を使わねばなりません。

拡張 API は、doctest ケースから抽出した対話モードでの例題を記憶するための二つのコンテナクラスを中心に構成されています:

* :class:`Example`: 1つの Python 文(:term:`statement`)と、その予想出力をペアにしたもの。

* :class:`DocTest`: :class:`Example` の集まり。通常一つの docstring や テキストファイルから抽出されます。

その他に、 doctest の例題を検索、パーズ、実行、チェックするための処理クラスが以下のように定義されています:

* :class:`DocTestFinder`: 与えられたモジュールから全ての docstring を検索し、対話モードでの例題が入った各
  docstring から :class:`DocTestParser` を使って:class:`DocTest` を生成します。

* :class:`DocTestParser`: (オブジェクトにつけられた docstring のような) 文字列から :class:`DocTest`
  オブジェクトを生成します。

* :class:`DocTestRunner`: :class:`DocTest` 内の例題を実行し、 :class:`OutputChecker`
  を使って出力を検証します。

* :class:`OutputChecker`: doctest 例題から実際に出力された結果を予想出力と比較し、両者が一致するか判別します。

これらの処理クラスの関係を図にまとめると、以下のようになります::

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

   単一の名前空間内で実行される doctest 例題の集まりです。   コンストラクタの引数は :class:`DocTest` インスタンス中の同名の
   メンバ変数の初期化に使われます。

   .. versionadded:: 2.4

   :class:`DocTest` では、以下のメンバ変数を定義しています。
   これらの変数はコンストラクタで初期化されます。直接変更してはなりません。


   .. attribute:: examples

      対話モードにおける例題それぞれをエンコードしていて、テストで実行される、 :class:`Example` オブジェクトからなるリストです。


   .. attribute:: globs

      例題を実行する名前空間 (いわゆるグローバル変数) です。このメンバは、名前から値への対応付けを行っている辞書です。例題が名前空間に対して
      (新たな変数をバインドするなど) 何らかの変更を行った場合、 :attr:`globs` への反映はテストの実行後に起こります。


   .. attribute:: name

      :class:`DocTest` を識別する名前の文字列です。通常、この値はテストを取り出したオブジェクトかファイルの名前になります。


   .. attribute:: filename

      :class:`DocTest` を取り出したファイルの名前です; ファイル名が未知の場合や :class:`DocTest` をファイルから取り出したので
      ない場合には ``None`` になります。


   .. attribute:: lineno

      :attr:`filename` 中で :class:`DocTest` のテスト例題が始まっている行の
      行番号です。行番号は、ファイルの先頭をゼロとして数えます。


   .. attribute:: docstring

      テストを取り出した docstring 自体を現す文字列です。 docstring 文字列を得られない場合や、文字列からテスト例題を取り出したのでない場合には
      ``None`` になります。


.. _doctest-example:

Example オブジェクト
^^^^^^^^^^^^^^^^^^^^


.. class:: Example(source, want[, exc_msg][, lineno][, indent][, options])

   ひとつの Python 文と、それに対する予想出力からなる、単一の対話的モードの例題です。コンストラクタの引数は :class:`Example`
   インスタンス中の同名のメンバ変数の初期化に使われます。

   .. versionadded:: 2.4

   :class:`Example` では、以下のメンバ変数を定義しています。これらの変数はコンストラクタで初期化されます。直接変更してはなりません。


   .. attribute:: source

      例題のソースコードが入った文字列です。ソースコードは単一の Python で、末尾は常に改行です。コンストラクタは必要に応じて改行を追加します。


   .. attribute:: want

      例題のソースコードを実行した際の予想出力 (標準出力と、例外が生じた場合にはトレースバック) です。 :attr:`want` の末尾は、予想出力が全く
      ない場合を除いて常に改行になります。予想出力がない場合には空文字列になります。コンストラクタは必要に応じて改行を追加します。


   .. attribute:: exc_msg

      例題が例外を生成すると予想される場合の例外メッセージです。例外を送出しない場合には ``None`` です。
      この例外メッセージは、 :func:`traceback.format_exception_only` の戻り値と比較されます。値が ``None``
      でない限り、 :attr:`exc_msg` は改行で終わっていなければなりません; コンストラクタは必要に応じて改行を追加します。


   .. attribute:: lineno

      この例題の入っている文字列中における、例題の実行文のある行のの行番号です。行番号は文字列の先頭をゼロとして数えます。


   .. attribute:: indent

      例題の入っている文字列のインデント、すなわち例題の最初のプロンプトより前にある空白文字の数です。


   .. attribute:: options

      オプションフラグを ``True`` または ``False`` に対応付けている辞書です。例題に対するデフォルトオプションを上書きするために
      用いられます。この辞書に入っていないオプションフラグはデフォルトの状態 (:class:`DocTestrunner` の
      :attr:`optionflags` の内容) のままになります。


.. _doctest-doctestfinder:

DocTestFinder オブジェクト
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: DocTestFinder([verbose][, parser][, recurse][, exclude_empty])

   与えられたオブジェクトについて、その docstring か、そのオブジェクトに入っているオブジェクトの docstring
   から :class:`DocTest` を抽出する処理クラスです。現在のところ、モジュール、関数、クラス、メソッド、静的メソッド、
   クラスメソッド、プロパティから :class:`DocTest` を抽出できます。

   オプション引数 *verbose* を使うと、抽出処理の対象となるオブジェクトを表示できます。デフォルトは ``False`` (出力をおこなわない) です。

   オプション引数 *parser* には、 docstring から :class:`DocTest` を
   抽出するのに使う :class:`DocTestParser` オブジェクト (またはその代替となるオブジェクト) を指定します。

   オプション引数 *recurse* が偽の場合、 :meth:`DocTestFinder.find`
   は与えられたオブジェクトだけを調べ、そのオブジェクトに入っている他のオブジェクトを調べません。

   オプション引数 *exclude_empty* が偽の場合、 :meth:`DocTestFinder.find` は空の docstring
   を持つオブジェクトもテスト対象に含めます。

   .. versionadded:: 2.4

   :class:`DocTestFinder` では以下のメソッドを定義しています:


   .. method:: find(obj[, name][, module][, globs][, extraglobs])

      *obj* または *obj* 内に入っているオブジェクトの docstring 中で定義されている
      :class:`DocTest` のリストを返します。

      オプション引数 *name* には、オブジェクトの名前を指定します。
      この名前は、関数が返す :class:`DocTest` の名前になります。
      *name* を指定しない場合、 ``obj.__name__`` を使います。

      オプションのパラメタ *module* は、指定したオブジェクトを収めているモジュールを指定します。
      *module* を指定しないか、 :const:`None` を指定した場合には、
      正しいモジュールを自動的に決定しようと試みます。
      オブジェクトのモジュールは以下のような役割を果たします:

      * *globs* を指定していない場合、オブジェクトのモジュールはデフォルトの名前空間になります。

      * 他のモジュールから import されたオブジェクトに対して :class:`DocTestFinder` が :class:`DocTest`
        を抽出するのを避けるために使います (*module* 由来でないオブジェクトを無視します)。

      * オブジェクトの入っているファイル名を調べるために使います。

      * オブジェクトがファイル内の何行目にあるかを調べる手助けにします。

      *module* が ``False`` の場合には、モジュールの検索を試みません。
      これは正確さを欠くような使い方で、通常 doctest 自体のテストにしかつかいません。
      *module* が ``False`` の場合、または *module* が ``None`` で自動的に的確な
      モジュールを見つけ出せない場合には、全てのオブジェクトは ``(non-existent)``
      モジュールに属するとみなされ、そのオブジェクト内の全てのオブジェクトに対して
      (再帰的に) doctest の検索をおこないます。

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

   対話モードの例題を文字列から抽出し、それを使って :class:`DocTest`  オブジェクトを生成するために使われる処理クラスです。

   .. versionadded:: 2.4

   :class:`DocTestParser` では以下のメソッドを定義しています:


   .. method:: get_doctest(string, globs, name, filename, lineno)

      指定した文字列から全ての doctest 例題を抽出し、 :class:`DocTest` オブジェクト内に集めます。

      *globs*, *name*, *filename*, および *lineno* は新たに作成される :class:`DocTest`
      オブジェクトの属性になります。詳しくは :class:`DocTest` のドキュメントを参照してください。


   .. method:: get_examples(string[, name])

      指定した文字列から全ての doctest 例題を抽出し、 :class:`Example`
      オブジェクトからなるリストにして返します。
      各 :class:`Example` の行番号はゼロから数えます。
      オプション引数 *name* はこの文字列につける名前で、エラーメッセージにしか使われません。


   .. method:: parse(string[, name])

      指定した文字列を、例題とその間のテキストに分割し、
      例題を :class:`Example` オブジェクトに変換し、
      :class:`Example` と文字列からなるリストにして返します。
      各 :class:`Example` の行番号はゼロから数えます。オプション引数 *name*
      はこの文字列につける名前で、エラーメッセージにしか使われません。


.. _doctest-doctestrunner:

DocTestRunner オブジェクト
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: DocTestRunner([checker][, verbose][, optionflags])

   :class:`DocTest` 内の対話モード例題を実行し、検証する際に用いられる処理クラスです。

   予想出力と実際の出力との比較は :class:`OutputChecker` で行います。
   比較は様々なオプションフラグを使ってカスタマイズできます;
   詳しくは :ref:`doctest-options` を参照してください。
   オプションフラグでは不十分な場合、コンストラクタに
   :class:`OutputChecker` のサブクラスを渡して比較方法をカスタマイズできます。

   テストランナの表示出力の制御には二つの方法があります。
   一つ目は、 :meth:`TestRunner.run` に出力用の関数を渡すというものです。
   この関数は、表示すべき文字列を引数にして呼び出されます。
   デフォルトは ``sys.stdout.write`` です。出力を取り込んで処理するだけでは不十分な場合、
   :class:`DocTestRunner` をサブクラス化し、 :meth:`report_start`,
   :meth:`report_success`, :meth:`report_unexpected_exception`, および
   :meth:`report_failure` をオーバライドすればカスタマイズできます。

   オプションのキーワード引数 *checker* には、 :class:`OutputChecker` オブジェクト (またはその代用品)
   を指定します。このオブジェクトは doctest 例題の予想出力と実際の出力との比較を行う際に使われます。

   オプションのキーワード引数 *verbose* は、 :class:`DocTestRunner` の出すメッセージの冗長性を制御します。
   *verbose* が ``True`` の場合、各例題を実行するつど、その例題についての情報を出力します。
   *verbose* が ``False`` の場合、テストの失敗だけを出力します。
   *verbose* を指定しない場合や ``None`` を指定した場合、コマンドラインスイッチ
   :option:`-v` を使った場合にのみ *verbose* 出力を適用します。

   オプションのキーワード引数  *optionflags* を使うと、
   テストランナが予想出力と実際の出力を比較する方法や、
   テストの失敗を表示する方法を制御できます。
   詳しくは :ref:`doctest-options` 節を参照してください。

   .. versionadded:: 2.4

   :class:`DocTestRunner` では、以下のメソッドを定義しています:


   .. method:: report_start(out, test, example)

      テストランナが例題を処理しようとしているときにレポートを出力します。
      :class:`DocTestRunner` の出力をサブクラスでカスタマイズできるように
      するためのメソッドです。直接呼び出してはなりません。

      *example* は処理する例題です。 *test* は *example* の入っているテストです。
      *out* は出力用の関数で、 :meth:`DocTestRunner.run` に渡されます。


   .. method:: report_success(out, test, example, got)

      与えられた例題が正しく動作したことを報告します。
      このメソッドは :class:`DocTestRunner` のサブクラスで出力を
      カスタマイズできるようにするために提供されています; 直接呼び出してはなりません。

      *example* は処理する例題です。 *got* は例題から実際に得られた出力です。
      *test* は *example* の入っているテストです。
      *out* は出力用の関数で、 :meth:`DocTestRunner.run` に渡されます。


   .. method:: report_failure(out, test, example, got)

      与えられた例題が正しく動作しなかったことを報告します。
      このメソッドは :class:`DocTestRunner` のサブクラスで出力を
      カスタマイズできるようにするために提供されています; 直接呼び出してはなりません。

      *example* は処理する例題です。 *got* は例題から実際に得られた出力です。
      *test* は *example* の入っているテストです。
      *out* は出力用の関数で、 :meth:`DocTestRunner.run` に渡されます。


   .. method:: report_unexpected_exception(out, test, example, exc_info)

      与えられた例題が予想とは違う例外を送出したことを報告します。
      このメソッドは :class:`DocTestRunner` のサブクラスで出力をカスタマイズ
      できるようにするために提供されています; 直接呼び出してはなりません。

      *example* は処理する例題です。 *exc_info* には予期せず送出された
      例外の情報を入れたタプル (:func:`sys.exc_info` の返す内容) になります。
      *test* は *example* の入っているテストです。
      *out* は出力用の関数で、 :meth:`DocTestRunner.run` に渡されます。

   .. method:: run(test[, compileflags][, out][, clear_globs])

      *test* 内の例題 (:class:`DocTest` オブジェクト) を実行し、
      その結果を出力用の関数 *out* を使って表示します。

      例題は名前空間 ``test.globs`` の下で実行されます。
      *clear_globs* が真 (デフォルト) の場合、名前空間はテストの実行後に消去され、
      ガベージコレクションをうながします。
      テストの実行完了後にその内容を調べたければ、 *clear_globs* を
      :const:`False` にしてください。

      *compileflags* には、例題を実行する際に Python コンパイラに適用するフラグセットを指定します。 
      *compileflags* を指定しない場合、デフォルト値は *globs* で適用されている
      future-import フラグセットになります。

      各例題の出力は :class:`DocTestRunner` の出力チェッカで検査され、その結果は
      :meth:`DocTestRunner.report_\*`. メソッドで書式化されます。

   .. method:: summarize([verbose])

      この DocTestRunner が実行した全てのテストケースのサマリを出力し、
      :tuple:`名前付きタプル` (named tuple) ``TestResults(failed, attempted)`` を返します。

      オプションの *verbose* 引数を使うと、どのくらいサマリを詳しくするかを制御できます。
      冗長度を指定しない場合、 :class:`DocTestRunner` 自体の冗長度を使います。

      .. versionchanged:: 2.6
         名前付きタプル (named tuple) を使うようになりました。


.. _doctest-outputchecker:

OutputChecker オブジェクト
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: OutputChecker()

   doctest 例題を実際に実行したときの出力が予想出力と一致するかどうかを
   チェックするために使われるクラスです。
   :class:`OutputChecker` では、与えられた二つの出力を比較して、
   一致する場合には真を返す :meth:`check_output` と、
   二つの出力間の違いを説明する文字列を返す :meth:`output_difference`
   の、二つのメソッドがあります。

   .. versionadded:: 2.4

:class:`OutputChecker` では以下のメソッドを定義しています:

    .. method:: check_output(want, got, optionflags)

       例題から実際に得られた出力 (*got*) と、予想出力 (*want*)
       が一致する場合にのみ ``True`` を返します。
       二つの文字列が全く同一の場合には常に一致するとみなしますが、
       テストランナの使っているオプションフラグにより、
       厳密には同じ内容になっていなくても一致するとみなす場合もあります。
       オプションフラグについての詳しい情報は :ref:`doctest-options` 節を参照してください。


    .. method:: output_difference(want, got, optionflags)

       与えられた例題の予想出力 (*want*)と、実際に得られた出力 (*got*)
       の間の差異を解説している文字列を返します。
       *optionflags* は *want* と *got* を比較する際に使われる
       オプションフラグのセットです。


.. _doctest-debugging:

デバッグ
--------

:mod:`doctest` では、doctest 例題をデバッグするメカニズムをいくつか提供しています:

* doctest を実行可能な Python プログラムに変換し、 Python デバッガ :mod:`pdb`
  で実行できるようにするための関数がいくつかあります。

* :class:`DocTestRunner` のサブクラス :class:`DebugRunner` クラスが
  あります。このクラスは、最初に失敗した例題に対して例外を送出します。
  例外には例題に関する情報が入っています。この情報は例題の検視デバッグに利用できます。

* :func:`DocTestSuite` の生成する :mod:`unittest` テストケースは、 :meth:`debug`
  メソッドをサポートしています。 :meth:`debug` は :class:`unittest.TestCase` で定義されています。

* :func:`pdb.set_trace` を doctest 例題の中で呼び出しておけば、その行が実行されたときに Python
  デバッガが組み込まれます。
  デバッガを組み込んだあとは、変数の現在の値などを調べられます。
  たとえば、以下のようなモジュールレベルの docstring
  の入ったファイル :file:`a.py` があるとします::

     """
     >>> def f(x):
     ...     g(x*2)
     >>> def g(x):
     ...     print x+3
     ...     import pdb; pdb.set_trace()
     >>> f(3)
     9
     """

  対話セッションは以下のようになるでしょう::

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

  .. versionchanged:: 2.4
     :func:`pdb.set_trace` を doctest の中で有効に使えるようになりました.

以下は、doctest を Python コードに変換して、できたコードをデバッガ下で実行できるようにするための関数です:


.. function:: script_from_examples(s)

   例題の入ったテキストをスクリプトに変換します。

   引数 *s* は doctest 例題の入った文字列です。
   この文字列は Python スクリプトに変換され、その中では *s* の doctest 例題が
   通常のコードに、それ以外は Python のコメント文になります。
   生成したスクリプトを文字列で返します。例えば、 ::

      import doctest
      print doctest.script_from_examples(r"""
          Set x and y to 1 and 2.
          >>> x, y = 1, 2

          Print their sum:
          >>> print x+y
          3
      """)

   は、 ::

      # Set x and y to 1 and 2.
      x, y = 1, 2
      #
      # Print their sum:
      print x+y
      # Expected:
      ## 3

   になります。

   この関数は他の関数 (下記参照) から使われていまるが、対話セッションを
   Python スクリプトに変換したいような場合にも便利でしょう。

   .. versionadded:: 2.4


.. function:: testsource(module, name)

   あるオブジェクトの doctest をスクリプトに変換します。

   引数 *module* はモジュールオブジェクトか、対象の doctest を持つ
   オブジェクトの入ったモジュールのドット表記名です。
   引数 *name* は対象の doctest を持つオブジェクトの (モジュール内の) 名前です。
   対象オブジェクトの docstring を上の :func:`script_from_examples`
   で説明した方法で Python スクリプトに変換してできた文字列を返しますます。
   例えば、 :file:`a.py` モジュールのトップレベルに関数 :func:`f` がある場合、以下のコード ::

      import a, doctest
      print doctest.testsource(a, "a.f")

   を実行すると、 :func:`f` の docstring から doctest をコードに変換し、
   それ以外をコメントにしたスクリプトを出力します。

   .. versionadded:: 2.3


.. function:: debug(module, name[, pm])

   オブジェクトの持つ doctest をデバッグします。

   *module* および *name* 引数は上の :func:`testsource` と同じです。
   指定したオブジェクトの docstring から合成された Python
   スクリプトは一時ファイルに書き出され、その後 Python デバッガ :mod:`pdb` の制御下で実行されます。

   ローカルおよびグローバルの実行コンテキストには、 ``module.__dict__`` の浅いコピーが使われます。

   オプション引数 *pm* は、検死デバッグを行うかどうかを指定します。
   *pm* が真の場合、スクリプトファイルは直接実行され、
   スクリプトが送出した例外が処理されないまま終了した場合にのみデバッガが立ち入ります。
   その場合、 :func:`pdb.post_mortem` によって検死デバッグを起動し、
   処理されなかった例外から得られたトレースバックオブジェクトを渡します。
   *pm* を指定しないか値を偽にした場合、 :func:`pdb.run` に適切な :func:`execfile`
   呼び出しを渡して、最初からデバッガの下でスクリプトを実行します。

   .. versionadded:: 2.3

   .. versionchanged:: 2.4
      引数 *pm* を追加しました.


.. function:: debug_src(src[, pm][, globs])

   文字列中の doctest をデバッグします。

   上の :func:`debug` に似ていますが、doctest の入った文字列は *src* 引数で直接指定します。

   オプション引数 *pm* は上の :func:`debug` と同じ意味です。

   オプション引数 *globs* には、ローカルおよびグローバルな実行コンテキストの
   両方に使われる辞書を指定します。
   *globs* を指定しない場合や ``None`` にした場合、空の辞書を使います。
   辞書を指定した場合、実際の実行コンテキストには浅いコピーが使われます。

   .. versionadded:: 2.4

:class:`DebugRunner` クラス自体や :class:`DebugRunner` クラスが送出する特殊な例外は、
テストフレームワークの作者にとって非常に興味のあるところですが、
ここでは概要しか述べられません。
詳しくはソースコード、とりわけ :class:`DebugRunner` の docstring (それ自体 doctest ですよ!)
を参照してください。


.. class:: DebugRunner([checker][, verbose][, optionflags])

   テストの失敗に遭遇するとすぐに例外を送出するようになっている
   :class:`DocTestRunner` のサブクラスです。予期しない例外が生じると、
   :exc:`UnexpectedException` 例外を送出します。
   この例外には、テスト、例題、もともと送出された例外が入っています。
   予想出力と実際出力が一致しないために失敗した場合には、
   :exc:`DocTestFailure` 例外を送出します。
   この例外には、テスト、例題、実際の出力が入っています。

   コンストラクタのパラメタやメソッドについては、 :ref:`doctest-advanced-api` 節の
   :class:`DocTestRunner` のドキュメントを参照してください。

:class:`DebugRunner` インスタンスの送出する例外には以下の二つがあります:


.. exception:: DocTestFailure(test, example, got)

   doctest 例題の実際の出力が予想出力と一致しなかったことを示すために
   :class:`DocTestRunner` が送出する例外です。
   コンストラクタの引数は、インスタンスの同名のメンバ変数を初期化するために使われます。

:exc:`DocTestFailure` では以下のメンバ変数を定義しています:


.. attribute:: DocTestFailure.test

   例題が失敗した時に実行されていた :class:`DocTest` オブジェクトです。


.. attribute:: DocTestFailure.example

   失敗した :class:`Example` オブジェクトです。


.. attribute:: DocTestFailure.got

   例題の実際の出力です。


.. exception:: UnexpectedException(test, example, exc_info)

   doctest 例題が予期しない例外を送出したことを示すために :class:`DocTestRunner` が送出する例外です。
   コンストラクタの引数は、インスタンスの同名のメンバ変数を初期化するために使われます。

:exc:`UnexpectedException` では以下のメンバ変数を定義しています:


.. attribute:: UnexpectedException.test

   例題が失敗した時に実行されていた :class:`DocTest` オブジェクトです。


.. attribute:: UnexpectedException.example

   失敗した :class:`Example` オブジェクトです。


.. attribute:: UnexpectedException.exc_info

   予期しない例外についての情報の入ったタプルで、 :func:`sys.exc_info`  が返すのと同じものです。


.. _doctest-soapbox:

提言
----

冒頭でも触れたように、 :mod:`doctest` は、

#. docstring 内の例題をチェックする、

#. 回帰テストを行う、

#. 実行可能なドキュメント/読めるテストの実現、

という三つの主な用途を持つようになりました。
これらの用途にはそれぞれ違った要求があるので、区別して考えるのが重要です。
特に、 docstring を曖昧なテストケースに埋もれさせてしまうとドキュメントとしては最悪です。

docstring の例は注意深く作成してください。
doctest の作成にはコツがあり、きちんと学ぶ必要があります --- 最初はすんなりできないでしょう。
例題は、ドキュメントに紛れ無しの価値を与えます。
よい例がたくさんの言葉に値することは多々あります。
注意深くやれば、例はユーザにとってはあまり意味のないものになるかもしれませんが、
歳を経るにつれて、あるいは "状況が変わった" 際に何度も何度も正しく動作させるために
かかることになる時間を節約するという形で、きっと見返りを得るでしょう。
私は今でも、自分の :mod:`doctest` で処理した例が "たいした事のない" 
変更を行った際にうまく動作しなくなることに驚いています。

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

回帰テストは特定のオブジェクトやファイルにまとめておくのがよいでしょう。
回帰テストの組み方にはいくつか選択肢があります:

* テストケースを対話モードの例題にして入れたテキストファイルを書き、
  :func:`testifle` や :func:`DocFileSuite` を使ってそのファイルをテストします。
  この方法をお勧めします。
  最初から doctest を使うようにしている新たなプロジェクトでは、この方法が一番簡単です。

* ``_regrtest_topic`` という名前の関数を定義します。
  この関数には、あるトピックに対応するテストケースの入った docstring が一つだけ入っています。
  この関数はモジュールと同じファイルの中にも置けますし、別のテストファイルに分けてもかまいません。

* 回帰テストのトピックをテストケースの入った docstring
  に対応付けた辞書 ``__test__`` 辞書を定義します。


進んだ使い方
------------

doctest をどのように動作させるかを制御する、いくつかのモジュールレベルの関数が利用できます。


.. function:: debug(module, name)

   doctest を含む単一のドキュメンテーション文字列をデバッグします。

   デバッグしたいドキュメンテーション文字列の入った *module* 
   (またはドットで区切ったモジュール名) と、(モジュール内の)
   デバッグしたいドキュメンテーション文字列を持つオブジェクトの
   *name* を指定してください。

   doctest の例が展開され (:func:`testsource` 関数を参照してください)、
   一次ファイルに書き込まれます。次に Python デバッガ
   :mod:`pdb` がこのファイルに対して起動されます。

   .. versionadded:: 2.3


.. function:: testmod()

   この関数は doctest への基本的なインタフェース提供します。
   この関数は  :class:`Tester` のローカルなインスタンスを生成し、
   このクラスの適切なメソッドを動作させ、結果をグローバルな
   :class:`Tester` インスタンスである ``master`` に統合します。

   :func:`testmod` が提供するよりも細かい制御を行うには、
   :class:`Tester` のインスタンスを自作のポリシで作成するか、
   ``master`` のメソッドを直接呼び出します。
   詳細は ``Tester.__doc__`` を参照してください。


.. function:: testsource(module, name)

   doctest の例をドキュメンテーション文字列から展開します。

   展開したいテストの入った *module*  (またはドットで区切られたモジュールの名前)
   と、展開したいテストの入った docstring を持つオブジェクトの
   (モジュール内の) *name* を与えます。

   doctest 内の例は Python コードの入った文字列として返されます。
   例中での予想される出力のブロックは Python のコメントに変換されます。

   .. versionadded:: 2.3


.. function:: DocTestSuite([module])

   モジュールにおける doctest のテストプログラムを :class:`unittest.TestSuite` に変換します。

   返される :class:`TestSuite` は unittest フレームワークで動作するためのもので、
   モジュール内の各 doctest を走らせます。
   doctest のいずれかが失敗すると、生成された unittest が失敗し、
   該当するテストを含むファイルと (時に近似の) 行番号を表示する
   :exc:`DocTestTestFailure` 例外が送出されます。

   オプションの *module* 引数はテストするモジュールを与えます。
   この値はモジュールオブジェクトか (場合によってはドットで区切られた)
   モジュール名となります。
   指定されていなければ、この関数を呼び出しているモジュールが使われます。

   :mod:`unittest` モジュールが :class:`TestSuite` を利用する数多くの方法のうちの一つを使った例を以下に示します::

      import unittest
      import doctest
      import my_module_with_doctests

      suite = doctest.DocTestSuite(my_module_with_doctests)
      runner = unittest.TextTestRunner()
      runner.run(suite)

   .. versionadded:: 2.3

   .. warning::

      この関数は現在のところ ``M.__test__`` を検索せず、その検索テクニックはあらゆる点で :func:`testmod` と合致しません。
      将来のバージョンではこれら二つを収斂させる予定です。

.. rubric:: Footnotes

.. [#] 予想出力結果と例外の両方を含んだ例はサポートされていません。
   一方の終わりと他方の始まりを見分けようとするのはエラーの元になりがちですし、
   解りにくいテストになってしまいます。

