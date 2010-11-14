.. _tut-modules:

**********
モジュール
**********

Python インタプリタを終了させ、再び起動すると、これまでに行ってきた 定義 (関数や変数) は失われています。ですから、より長いプログラムを
書きたいなら、テキストエディタを使ってインタプリタへの入力を用意して おき、手作業の代わりにファイルを入力に使って動作させるとよいでしょう。 この作業を
*スクリプト (script)* の作成と言います; プログラムが 長くなるにつれ、メンテナンスを楽にするために、スクリプトをいくつかの
ファイルに分割したくなるかもしれません。また、いくつかのプログラムで 書いてきた便利な関数について、その定義をコピーすることなく個々の
プログラムで使いたいと思うかもしれません。


こういった要求をサポートするために、Python では定義をファイルに書いて おき、スクリプトの中やインタプリタの対話インスタンス上で使う方法が あります。
このファイルを *モジュール (module)* と呼びます; モジュール にある定義は、他のモジュールや *main* モジュール (実行の
トップレベルや電卓モードでアクセスできる変数の集まりを指します) に *import* (取り込み) することができます。


モジュールは Python の定義や文が入ったファイルです。 ファイル名はモジュール名に接尾語 :file:`.py` がついたものになります。
モジュールの中では、(文字列の) モジュール名をグローバル変数 ``__name__`` で取得できます。例えば、お気に入りのテキストエディタ
を使って、現在のディレクトリに以下の内容のファイル :file:`fibo.py` を 作成してみましょう:


::

   # フィボナッチ数列モジュール

   def fib(n):    # nまで加算されるフィボナッチ級数を印字
       a, b = 0, 1
       while b < n:
           print b,
           a, b = b, a+b

   def fib2(n): # nまで加算されるフィボナッチ級数を返す
       result = []
       a, b = 0, 1
       while b < n:
           result.append(b)
           a, b = b, a+b
       return result

次に Python インタプリタに入り、モジュールを以下のコマンドで import しましょう。


::

   >>> import fibo

この操作では、``fibo`` で定義された関数の名前を直接現在の シンボルテーブルに入力することはありません; 単にモジュール名 ``fibo``
だけをシンボルテーブルに入れます。 関数にはモジュール名を使ってアクセスします:


::

   >>> fibo.fib(1000)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987
   >>> fibo.fib2(100)
   [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
   >>> fibo.__name__
   'fibo'

関数を度々使うのなら、ローカルな名前に代入できます:


::

   >>> fib = fibo.fib
   >>> fib(500)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377


.. _tut-moremodules:

モジュールについてもうすこし
============================

モジュールには、関数定義に加えて実行文を入れることができます。 これらの実行文はモジュールを初期化するためのものです。
これらの実行文は、モジュールがどこかで*最初に* import された 時にだけ実行されます。 [#]_


各々のモジュールは、自前のプライベートなシンボルテーブルを持っていて、 モジュールで定義されている関数はこのテーブルをグローバルな
シンボルテーブルとして使います。 したがって、モジュールの作者は、ユーザのグローバル変数と偶然的な衝突が
起こる心配をせずに、グローバルな変数をモジュールで使うことができます。 一方、自分が行っている操作をきちんと理解していれば、モジュール内の
関数を参照するのと同じ表記法 ``modname.itemname`` で、モジュールの グローバル変数をいじることもできます。


モジュールが他のモジュールを import することもできます。:keyword:`import` 文は全てモジュールの先頭に (さらに言えばスクリプトでも)
置きますが、 これは慣習であって必須ではありません。import されたモジュール名は import
を行っているモジュールのグローバルなシンボルテーブルに置かれます。


:keyword:`import` 文には、あるモジュール内の名前を、import を実行 しているモジュールのシンボルテーブル内に直接取り込むという変型が
あります。例えば:


::

   >>> from fibo import fib, fib2
   >>> fib(500)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377

この操作は、import の対象となるモジュール名をローカルな シンボルテーブル内に取り入れることはありません (従って上の例では、 ``fibo``
は定義されません)。


モジュールで定義されている名前を全て import するという変型もあります:


::

   >>> from fibo import *
   >>> fib(500)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377

上の操作は、アンダースコア (``_``) で開始する名前以外の全ての名前を import します。


.. note::

   実行効率上の理由で、各モジュールはインタープリタの 1 セッションごとに 1 回だけ import されます。従って、モジュールを修正した場合には、インタープリタを再起動させなければなりません -- もしくは、その場で手直ししてテストしたいモジュールが 1 つだった場合には、例えば ``reload(modulename)`` のように :func:`reload` を使ってください。


.. _tut-modulesasscripts:

モジュールをスクリプトとして実行する
====================================

Python モジュールを

::

   python fibo.py <arguments>

と実行すると、 ``__name__`` に ``__main__`` が設定されている点を除いて import したときと同じようにモジュール内のコードが実行されます。つまりモジュールの末尾にこのコード

::
   if __name__ == "__main__":
       import sys
       fib(int(sys.argv[1]))

を追加することで、このファイルが import できるモジュールであると同時にスクリプトとしても使えるようになります、なぜならモジュールが "main" ファイルとして起動されたときだけ、コマンドラインを解釈するコードが実行されるからです:

::

   $ python fibo.py 50
   1 1 2 3 5 8 13 21 34

モジュールが import された場合は、そのコードは実行されません:

::

   >>> import fibo
   >>>

この方法はモジュールに便利なユーザインターフェースを提供したり、テストのために (スクリプトをモジュールとして起動しテストスイートを実行して) 使われます。


.. _tut-searchpath:

モジュール検索パス
------------------

.. index:: triple: module; search; path

:mod:`spam` という名前のモジュールが import されると、インタプリタ は :file:`spam.py`
という名前のファイルを現在のディレクトリ内で探し、 次に環境変数:envvar:`PYTHONPATH` に指定されているディレクトリのリスト
から探します。:envvar:`PYTHONPATH` はシェル変数 :envvar:`PATH` と
同じ構文、すなわちディレクトリ名を並べたものです。:envvar:`PYTHONPATH` が設定されていないか、探しているファイルが見つからなかった場合は、
検索対象をインストール方法に依存するデフォルトのパスにして続けます; Unixでは、このパスは通常
:file:`.:/usr/locall/lib/python` です。


実際には、モジュールは変数 ``sys.path`` で指定されたディレクトリの リストから検索されます。``sys.path`` は、入力とするスクリプトの
入ったディレクトリ (現在のディレクトリ)、:envvar:`PYTHONPATH`、 およびインストール方法依存のデフォルト値を使って初期化されます。
Python プログラマは、自分の行っている操作を理解しているなら、 この変数を使ってモジュール検索パスを修正したり置き換えたりすることが できます。
起動しようとするスクリプトの入ったディレクトリが検索パス上にある ため、スクリプトが標準モジュールと同じ名前をもたないようにすることが
重要です。さもなければ、Python が標準モジュールを import するときに スクリプトをモジュールとして import しようと試みてしまうので注意
してください。このような誤りを犯すと、通常はエラーになります。 詳しくは  :ref:`tut-standardmodules` 節
を参照して ください。



"コンパイル" された Python ファイル
-----------------------------------

たくさんの標準モジュールを使うような短いプログラムで重要となる 起動時間の高速化を行うために、:file:`spam.py` が見つかったディレクトリに
:file:`spam.pyc` という名前のファイルがあった場合には、このファイルを モジュール :mod:`spam` の "バイトコンパイルされた"
バージョン であると仮定します。 :file:`spam.pyc` を生成するのに使われたバージョンの :file:`spam.py` の ファイル修正時刻が
:file:`spam.pyc` に記録されており、この値が 一致しなければ :file:`spam.pyc` ファイルは無視されます。


通常、:file:`spam.pyc` ファイルを生成するために何かをする必要は ありません。:file:`spam.py` が無事コンパイルされると、常に
コンパイルされたバージョンを :file:`spam.pyc` へ書き出すよう 試みます。この試みが失敗してもエラーにはなりません;
何らかの理由でファイルが完全に書き出されなかった場合、作成された :file:`smap.pyc` は無効であるとみなされ、それ以後無視されます。
:file:`spam.pyc` ファイルの内容はプラットフォームに依存しないので、 Python のモジュールのディレクトリは異なるアーキテクチャのマシン間で
共有することができます。


エキスパートへの助言:


* Python インタプリタを :option:`-O` フラグ付きで起動すると、 最適化 (optimize) されたコードが生成されて
  :file:`.pyo` ファイルに 保存されます。最適化機構は今のところあまり役に立っていません; 最適化機構は :keyword:`assert` 文と
  ``SET_LINENO`` 命令を除去 しているだけです。:option:`-O` を使うと、*すべての*  バイトコード (:term:`bytecode`) が最適化されます; ``.pyc``
  ファイルは無視され、 ``.py`` ファイルは最適化されたバイトコードにコンパイルされます。

* 二つの :option:`-O` フラグ (:option:`-OO`) を Python インタプリタへ 渡すと、バイトコードコンパイラは、
  まれにプログラムが正しく動作しなくなるかもしれないような最適化を 実行します。 現状では、ただ ``__doc__`` 文字列をバイトコードから除去して、
  よりコンパクトな :file:`.pyo` ファイルにするだけです。 この文字列が利用できることをあてにしているプログラムがあるかもしれない
  ので、自分の行っている操作が何かわかっているときにだけこのオプションを 使うべきです。

* :file:`.pyc` ファイルや :file:`.pyo` ファイルから 読み出されたとしても、プログラムは何ら高速に動作するわけでは
  ありません。:file:`.pyc` ファイルや :file:`.pyo` ファイルで高速化される のは、読み込まれるときの速度だけです。

* スクリプトの名前をコマンドラインで指定して実行した場合、 そのスクリプトのバイトコードが :file:`.pyc` や :file:`.pyo` に
  書き出されることはありません。従って、スクリプトのほとんどのコードを モジュールに移し、そのモジュールを import する小さなブートストラップ
  スクリプトを作れば、スクリプトの起動時間を短縮できるときがあります。 :file:`.pyc` または :file:`.pyo`
  ファイルの名前を直接コマンドラインに 指定することもできます。

* 一つのモジュールについて、ファイル :file:`spam.py` のない :file:`spam.pyc` (:option:`-O` を使ったときは
  :file:`spam.pyo`)  があってもかまいません。この仕様は、Python コードでできたライブラリを
  リバースエンジニアリングがやや困難な形式で配布するために使えます。

  .. index:: module: compileall

* :mod:`compileall` 
  は、:file:`.pyc` ファイル (または :option:`-O` を使ったときは:file:`.pyo` ファイル) を
  ディレクトリ内の全てのモジュールに対して生成することができます。

  .. % 


.. _tut-standardmodules:

標準モジュール
==============

.. index:: module: sys

Python には標準モジュールのライブラリが付属しています。ライブラリは 独立したドキュメント Python ライブラリ リファレンス (Python
Library Reference) (以降  "ライブラリリファレンス")
で記述されています。 モジュールによってはインタプリタに組み込まれたものがあります;  インタプリタに組み込まれているモジュールが提供しているのは、
言語の中核の部分ではありませんが、効率化のためや、システムコールのような オペレーティングシステムの根本機能へのアクセス手段を提供するための
操作です。これらのモジュールのセットは設定時に選択可能で、また 根底にあるプラットフォームにも依存します。例えば、:mod:`winreg`  モジュールは、
Windows でのみ提供されます。 とりわけ、注目に値するモジュールが一つあります:
:mod:`sys`   はどの Python インタプリタにも
組み込まれています。変数 ``sys.ps1`` と ``sys.ps2`` は、それぞれ 一次プロンプトと二次プロンプトとして使われる文字列を定義しています:


::

   >>> import sys
   >>> sys.ps1
   '>>> '
   >>> sys.ps2
   '... '
   >>> sys.ps1 = 'C> '
   C> print 'Yuck!'
   Yuck!
   C> 

これらの二つの変数は、インタプリタが対話モードにあるときだけ 定義されています。


変数 ``sys.path`` は文字列からなるリストで、インタプリタがモジュール を検索するときのパスを決定します。 ``sys.path`` は環境変数
:envvar:`PYTHONPATH` から得たデフォルトパスに、 :envvar:`PYTHONPATH`
が設定されていなければ組み込みのデフォルト値に設定 されます。標準的なリスト操作で変更することができます:


::

   >>> import sys
   >>> sys.path.append('/ufs/guido/lib/python')


.. _tut-dir:

:func:`dir` 関数
================

組込み関数 :func:`dir` は、あるモジュールがどんな名前を定義して いるか調べるために使われます。 :func:`dir`
はソートされた文字列のリストを返します:


::

   >>> import fibo, sys
   >>> dir(fibo)
   ['__name__', 'fib', 'fib2']
   >>> dir(sys)
   ['__displayhook__', '__doc__', '__excepthook__', '__name__', '__stderr__',
    '__stdin__', '__stdout__', '_getframe', 'api_version', 'argv', 
    'builtin_module_names', 'byteorder', 'callstats', 'copyright',
    'displayhook', 'exc_clear', 'exc_info', 'exc_type', 'excepthook',
    'exec_prefix', 'executable', 'exit', 'getdefaultencoding', 'getdlopenflags',
    'getrecursionlimit', 'getrefcount', 'hexversion', 'maxint', 'maxunicode',
    'meta_path', 'modules', 'path', 'path_hooks', 'path_importer_cache',
    'platform', 'prefix', 'ps1', 'ps2', 'setcheckinterval', 'setdlopenflags',
    'setprofile', 'setrecursionlimit', 'settrace', 'stderr', 'stdin', 'stdout',
    'version', 'version_info', 'warnoptions']

引数がなければ、:func:`dir` は現在定義している名前を列挙します。


::

   >>> a = [1, 2, 3, 4, 5]
   >>> import fibo
   >>> fib = fibo.fib
   >>> dir()
   ['__builtins__', '__doc__', '__file__', '__name__', 'a', 'fib', 'fibo', 'sys']

変数、モジュール、関数、その他の、すべての種類の名前をリストすることに 注意してください。


.. index:: module: __builtin__

:func:`dir` は、組込みの関数や変数の名前はリストしません。 これらの名前からなるリストが必要なら、標準モジュール
:mod:`__builtin__` で定義されています:


::

   >>> import __builtin__
   >>> dir(__builtin__)
   ['ArithmeticError', 'AssertionError', 'AttributeError', 'DeprecationWarning',
    'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False',
    'FloatingPointError', 'FutureWarning', 'IOError', 'ImportError',
    'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt',
    'LookupError', 'MemoryError', 'NameError', 'None', 'NotImplemented',
    'NotImplementedError', 'OSError', 'OverflowError', 
    'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError',
    'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError',
    'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True',
    'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
    'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
    'UserWarning', 'ValueError', 'Warning', 'WindowsError',
    'ZeroDivisionError', '_', '__debug__', '__doc__', '__import__',
    '__name__', 'abs', 'apply', 'basestring', 'bool', 'buffer',
    'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile',
    'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod',
    'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float',
    'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex',
    'id', 'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter',
    'len', 'license', 'list', 'locals', 'long', 'map', 'max', 'min',
    'object', 'oct', 'open', 'ord', 'pow', 'property', 'quit', 'range',
    'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set',
    'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super',
    'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']


.. _tut-packages:

パッケージ
==========

パッケージ (package) は、Python のモジュール名前空間 を "ドット付きモジュール名 (dotted module names)" を使って
構造化する手段です。例えば、モジュール名 :mod:`A.B` は、 ``A`` というパッケージのサブモジュール ``B`` を表します。
ちょうど、モジュールを利用すると、別々のモジュールの著者が互いの グローバル変数名について心配しなくても済むようになるのと同じように、
ドット付きモジュール名を利用すると、 NumPy や Python Imaging Library のように複数モジュールからなる
パッケージの著者が、互いのモジュール名について心配しなくても済むように なります。


音声ファイルや音声データを一様に扱うためのモジュールのコレクション ("パッケージ") を設計したいと仮定しましょう。音声ファイルには 多くの異なった形式がある
(通常は拡張子、例えば :file:`.wav`,  :file:`.aiff`, :file:`.au` などで認識されます) ので、
様々なファイル形式間で変換を行うためのモジュールからなる、 次第に増えていくモジュールのコレクションを作成したりメンテナンス
したりする必要がありかもしれません。また、音声データに対して 実行したい様々な独自の操作 (ミキシング、エコーの追加、
イコライザ関数の適用、人工的なステレオ効果の作成など) があるかも しれません。そうなると、こうした操作を実行するモジュールを果てしなく
書くことになるでしょう。以下に (階層的なファイルシステムで表現した)  パッケージの構造案を示します:


::

   sound/                          トップレベルのパッケージ
         __init__.py               サウンドパッケージを初期化する
         formats/                  ファイルフォーマット変換用の下位パッケージ
                 __init__.py
                 wavread.py
                 wavwrite.py
                 aiffread.py
                 aiffwrite.py
                 auread.py
                 auwrite.py
                 ...
         effects/                  サウンド効果用の下位パッケージ
                 __init__.py
                 echo.py
                 surround.py
                 reverse.py
                 ...
         filters/                  フィルタ用の下位パッケージ
                 __init__.py
                 equalizer.py
                 vocoder.py
                 karaoke.py
                 ...

パッケージを import する際、 Python は ``sys.path`` 上のディレクトリ
を検索して、トップレベルのパッケージの入ったサブディレクトリを探します。


あるディレクトリを、パッケージが入ったディレクトリとしてPython に 扱わせるには、ファイル :file:`__init__.py` が必要です:
このファイルを置かなければならないのは、``string`` のような よくある名前のディレクトリにより、モジュール検索パスの後の方で見つかる
正しいモジュールが意図せず隠蔽されてしまうのを防ぐためです。 最も簡単なケースでは :file:`__init__.py` はただの空ファイルで
構いませんが、:file:`__init__.py` ではパッケージのための初期化コード を実行したり、後述の ``__all__``
変数を設定してもかまいません。


パッケージのユーザは、個々のモジュールをパッケージから import  することができます。例えば:


::

   import sound.effects.echo

この操作はサブモジュール :mod:`sound.effects.echo` をロードします。
このモジュールは、以下のように完全な名前で参照しなければなりません:


::

   sound.effects.echo.echofilter(input, output, delay=0.7, atten=4)

サブモジュールを import するもう一つの方法を示します:


::

   from sound.effects import echo

これもサブモジュール :mod:`echo` をロードし、:mod:`echo` を パッケージ名を表す接頭辞なしで利用できるようにします。従って以下のように
用いることができます:


::

   echo.echofilter(input, output, delay=0.7, atten=4)

さらにもう一つのバリエーションとして、必要な関数や変数を直接 import する 方法があります:


::

   from sound.effects.echo import echofilter

この操作も同様にサブモジュール :mod:`echo` をロードしますが、 :func:`echofilter` を直接利用できるようにします。


::

   echofilter(input, output, delay=0.7, atten=4)

``from package import item`` を使う場合、*item* は パッケージ *package* のサブモジュール
(またはサブパッケージ) でも かまいませんし、関数やクラス、変数のような、*package* で定義されて いる別の名前でもかまわないことに注意してください。
``import`` 文はまず、*item* がパッケージ内で定義されているか どうか調べます; 定義されていなければ、*item* はモジュール
名であると仮定して、モジュールをロードしようと試みます。もし モジュールが見つからなければ、:exc:`ImportError` が送出されます。


反対に、``import item.subitem.subsubitem`` のような構文を 使った場合、最後の ``subsubitem``
を除く各要素はパッケージで なければなりません; 最後の要素はモジュールかパッケージにできますが、
一つ前の要素で定義されているクラスや関数や変数にはできません。



.. _tut-pkg-import-star:

パッケージから \* を import する
--------------------------------

.. index:: single: __all__


それでは、ユーザが ``from sound.effects import *`` と書いたら、 どうなるのでしょうか？
理想的には、何らかの方法でファイルシステムが 調べられ、そのパッケージにどんなサブモジュールがあるかを調べ上げ、 全てを import
する、という処理を望むことでしょう。残念ながら、 この操作は Windows のプラットフォームではうまく動作しません。
これらのプラットフォームでは、ファイルシステムはファイル名の 大小文字の区別について正しい情報をもっているとは限らないからです！
こうしたプラットフォームでは、ファイル :file:`ECHO.PY` を モジュール :mod:`echo` として import
すべきか、:mod:`Echo` と すべきかが分かる確かな方法がないからです (例えば、 Windows 95 は
すべてのファイル名の最初の文字を大文字にして表示するという困った 慣習があります)。また、DOS の 8+3 のファイル名制限のせいで、
長いモジュール名に関して別の奇妙な問題が追加されています。


唯一の解決策は、パッケージの作者にパッケージの索引を明示的に提供 させるというものです。 import 文は次の規約を使います: パッケージの
:file:`__init__.py` コード に ``__all__`` という名前のリストが定義されていれば、 ``from package import
*`` が現れたときに import する リストとして使います。新たなパッケージがリリースされるときに
リストを最新の状態に更新するのはパッケージの作者の責任となります。 自分のパッケージから \* を import するという使い方に同意できなければ、
パッケージの作者は :file:`__init__.py` をサポートしないことにしても かまいません。 例えば、ファイル
``sounds/effects/__init__.py`` には、次のような コードを入れてもよいかもしれません:


::

   __all__ = ["echo", "surround", "reverse"]

このコードは、 ``from sound.effects import *`` とすると、 :mod:`sound` パッケージから指定された 3
つのサブモジュールが  import されることになっている、ということを意味します。


もしも ``__all__`` が定義されていなければ、実行文 ``from sound.effects import *`` は、パッケージ
:mod:`sound.effects`  の全てのサブモジュールを現在の名前空間の中へ import *しません*; この文は単に
(場合によっては初期化コード :file:`__init__.py` を実行して)  パッケージ :mod:`sound.effects` が import
されたということを確認し、 そのパッケージで定義されている名前を全て import するだけです。 import
される名前には、:file:`__init__.py` で定義された名前  (と、明示的にロードされたサブモジュール) が含まれます。
パッケージのサブモジュールで、以前の import 文で明示的にロードされた ものも含みます。以下のコードを考えてください:


::

   import sound.effects.echo
   import sound.effects.surround
   from sound.effects import *

上の例では、echo と surround モジュールが現在の名前空間に import されます。これらのモジュールは ``from...import`` 文が
実行された際に :mod:`sound.effects` 内で定義されているからです (この機構は``__all__`` が定義されているときにも働きます)。


一般的には、モジュールやパッケージから ``*`` を import するという やり方には賛同できません。というのは、この操作を行うとしばしば可読性に
乏しいコードになるからです。しかし、対話セッションでキータイプの量を 減らすために使うのは構わないでしょう。それに、特定のモジュールでは、
特定のパターンに従った名前のみを公開 (export) するように設計されています。


``from package import specific_submodule`` を使っても何も問題は
ないことに留意してください！実際この表記法は、import を行うモジュールが 他のパッケージかと同じ名前を持つサブモジュールを使わなければ
ならない場合を除いて推奨される方式です。



パッケージ内での参照
--------------------

サブモジュール同士で互いに参照を行う必要がしばしば起こります。 例えば、:mod:`surround` モジュールは :mod:`echo` モジュールを
使うかもしれません。実際には、このような参照はよくあることなので、 :keyword:`import` 文を実行すると、まず最初に import 文の入っている
パッケージを検索し、その後になって標準のモジュール検索パスを 見に行きます。こうして、:mod:`surround` モジュールは単に ``import
echo`` や  ``from echo import echofilter`` を使うことができます。 import されたモジュールが現在のパッケージ
(現在のモジュールを サブモジュールにしているパッケージ) 内に見つからなかった場合、 :keyword:`import`
文は指定した名前のトップレベルのモジュールを検索 します。


パッケージが (前述の例の :mod:`sound` パッケージのように)  サブパッケージの集まりに構造化されている場合、絶対 import を使って兄弟関係にある
パッケージを参照できます。例えば、モジュール
:mod:`sound.filters.vocoder` で :mod:`sound.effects` パッケージの :mod:`echo`
モジュールを使いたいとすると、 ``from sound.effects import echo`` を使うことはできます。


Python 2.5 からは、上で説明した暗黙の相対importに加えて、明示的な 相対importを　``from module import name``
の形式のimport文で利用で きます。 この明示的な相対importでは、先頭のドットで現在および親パッケージを指定 して相対importを行います。
:mod:`surround`モジュールの例では、以下の ように記述できます:


::

   from . import echo
   from .. import formats
   from ..filters import equalizer

明示的および暗黙的な相対importのどちらもカレントモジュールの名前をベー スにすることに注意してください。メインモジュールの名前は常に
``"__main__"`` なので、Pythonアプリケーションのメインモジュールとし
て利用されることを意図しているモジュールでは絶対importを利用するべきで す。



複数ディレクトリ中のパッケージ
------------------------------

パッケージのサポートする特殊な属性には、もう一つ :attr:`__path__` が あります。この属性は、パッケージの
:file:`__init__.py` 中のコードが 実行されるよりも前に、:file:`__init__.py` の収められているディレクトリ名
の入ったリストになるよう初期化されます。 この変数は変更することができます; 変更を加えると、以降そのパッケージに
入っているモジュールやサブパッケージの検索に影響します。


この機能はほとんど必要にはならないのですが、パッケージ内に見つかる モジュールのセットを拡張するために使うことができます。



.. rubric:: Footnotes

.. [#] 実際には、関数定義も '実行' される '文' です; モジュールを実行すると、関数名はモジュールのグローバルな シンボルテーブルに入力されます。

