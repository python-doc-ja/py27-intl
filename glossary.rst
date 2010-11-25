.. _glossary:

********
用語集
********

.. if you add new entries, keep the alphabetical sorting!

.. glossary::

   ``>>>``
      .. The default Python prompt of the interactive shell.  Often seen for code
         examples which can be executed interactively in the interpreter.

      インタラクティブシェルにおける、デフォルトのPythonプロンプト。
      インタラクティブに実行されるコードサンプルとしてよく出てきます。

   ``...``
      .. The default Python prompt of the interactive shell when entering code for
         an indented code block or within a pair of matching left and right
         delimiters (parentheses, square brackets or curly braces).

      インタラクティブシェルにおける、インデントされたコードブロックや対応する括弧(丸括弧()、
      角括弧[]、curly brace{})の内側で表示されるデフォルトのプロンプト。

   2to3
      .. A tool that tries to convert Python 2.x code to Python 3.x code by
         handling most of the incompatibilites which can be detected by parsing the
         source and traversing the parse tree.

      Python 2.x のコードを Python 3.x のコードに変換するツール。
      ソースコードを解析して、その解析木を巡回(traverse)して、非互換なコードの大部分を処理する。

      .. 2to3 is available in the standard library as :mod:`lib2to3`; a standalone
         entry point is provided as :file:`Tools/scripts/2to3`.  See
         :ref:`2to3-reference`.

      2to3 は、 :mod:`lib2to3` モジュールとして標準ライブラリに含まれています。
      スタンドアローンのツールとして使うときのコマンドは :file:`Tools/scripts/2to3`
      として提供されています。 :ref:`2to3-reference` を参照してください。

   abstract base class
      .. Abstract Base Classes (abbreviated ABCs) complement :term:`duck-typing` by
         providing a way to define interfaces when other techniques like :func:`hasattr`
         would be clumsy. Python comes with many builtin ABCs for data structures
         (in the :mod:`collections` module), numbers (in the :mod:`numbers`
         module), and streams (in the :mod:`io` module). You can create your own
         ABC with the :mod:`abc` module.

      (抽象基底クラス) Abstract Base Classes (ABCs と略されます)は :term:`duck-typing`
      を補完するもので、 :func:`hasattr` などの別のテクニックでは不恰好になる場合に
      インタフェースを定義する方法を提供します。
      Pythonは沢山のビルトインABCsを、(:mod:`collections` モジュールで)データ構造、
      (:mod:`numbers` モジュールで)数値型、(:mod:`io` モジュールで)ストリーム型で
      提供いています。
      :mod:`abc` モジュールを利用して独自のABCを作成することもできます。

   argument
      (引数)
      関数やメソッドに渡された値。関数の中では、名前の付いたローカル変数に代入されます。

      関数やメソッドは、その定義中に位置指定引数(positional arguments, 訳注: ``f(1, 2)``
      のように呼び出し側で名前を指定せず、引数の位置に引数の値を対応付けるもの)
      とキーワード引数(keyword arguments, 訳注: ``f(a=1, b=2)`` のように、引数名に
      引数の値を対応付けるもの)の両方を持つことができます。
      位置指定引数とキーワード引数は可変長です。
      関数定義や呼び出しは、 ``*`` を使って、不定数個の位置指定引数をシーケンス型に入れて
      受け取ったり渡したりすることができます。
      同じく、キーワード引数は ``**`` を使って、辞書に入れて受け取ったり渡したりできます。

      引数リスト内では任意の式を使うことができ、その式を評価した値が渡されます。

      .. todo::
         キーワード引数？名前付き引数？
         順序付き引数？順序引数？位置指定引数？

   attribute
      (属性)
      オブジェクトに関連付けられ、ドット演算子を利用して名前で参照される値。
      例えば、オブジェクト *o* が属性 *a* を持っているとき、その属性は
      *o.a* で参照されます。

   BDFL
      慈悲ぶかき独裁者 (Benevolent Dictator For Life) の略です。
      Python の作者、 `Guido van Rossum <http://www.python.org/~guido/>`_
      のことです。

      .. Benevolent Dictator For Life, a.k.a. `Guido van Rossum
         <http://www.python.org/~guido/>`_, Python's creator.

   bytecode
      (バイトコード)
      Pythonのソースコードはバイトコードへとコンパイルされます。
      バイトコードはPythonプログラムのインタプリタ内部での形です。
      バイトコードはまた、 ``.pyc`` や ``.pyo`` ファイルにキャッシュされ、
      同じファイルを二度目に実行した際により高速に実行できるようにします
      (ソースコードからバイトコードへの再度のコンパイルは回避されます)。
      このバイトコードは、各々のバイトコードに対応するサブルーチンを呼び出すような
      "仮想計算機(:term:`virtual machine`)" で動作する "中間言語 (intermediate language)" といえます。

      .. Python source code is compiled into bytecode, the internal representation
         of a Python program in the interpreter.  The bytecode is also cached in
         ``.pyc`` and ``.pyo`` files so that executing the same file is faster the
         second time (recompilation from source to bytecode can be avoided).  This
         "intermediate language" is said to run on a :term:`virtual machine`
         that executes the machine code corresponding to each bytecode.

   class
      (クラス)
      ユーザー定義オブジェクトを作成するためのテンプレート。
      クラス定義は普通、そのクラスのインスタンス上の操作をするメソッドの定義を含みます。

   classic class
      (旧スタイルクラス)
      :class:`object` を継承していないクラス全てを指します。
      新スタイルクラス(:term:`new-style class`) も参照してください。
      旧スタイルクラスはPython 3.0で削除されます。

      .. Any class which does not inherit from :class:`object`.  See
         :term:`new-style class`.  Classic classes will be removed in Python 3.0.

   coercion
      (型強制)
      同じ型の2つの引数を要する演算の最中に、ある型のインスタンスを別の型に暗黙のうちに変換することです。
      例えば、 ``int(3.15)`` は浮動小数点数を整数の ``3`` にします。
      しかし、 ``3+4.5`` の場合、各引数は型が異なっていて(一つは整数、一つは浮動小数点数)、
      加算をする前に同じ型に変換しなければいけません。 そうでないと、 ``TypeError`` 例外が投げられます。
      2つの被演算子間の型強制は組み込み関数の ``coerce`` を使って行えます。 
      従って、 ``3+4.5`` は ``operator.add(*coerce(3, 4.5))`` を呼び出すことに等しく、
      ``operator.add(3.0, 4.5)`` という結果になります。
      型強制を行わない場合、たとえ互換性のある型であっても、すべての引数はプログラマーが、
      単に ``3+4.5`` とするのではなく、
      ``float(3)+4.5`` というように、同じ型に正規化しなければいけません。

      .. The implicit conversion of an instance of one type to another during an
         operation which involves two arguments of the same type.  For example,
         ``int(3.15)`` converts the floating point number to the integer ``3``, but
         in ``3+4.5``, each argument is of a different type (one int, one float),
         and both must be converted to the same type before they can be added or it
         will raise a ``TypeError``.  Coercion between two operands can be
         performed with the ``coerce`` builtin function; thus, ``3+4.5`` is
         equivalent to calling ``operator.add(*coerce(3, 4.5))`` and results in
         ``operator.add(3.0, 4.5)``.  Without coercion, all arguments of even
         compatible types would have to be normalized to the same value by the
         programmer, e.g., ``float(3)+4.5`` rather than just ``3+4.5``.

   complex number
      (複素数)
      よく知られている実数系を拡張したもので、すべての数は実部と虚部の和として表されます。
      虚数は虚数単位元(``-1`` の平方根)に実数を掛けたもので、一般に数学では ``i``
      と書かれ、工業では ``j`` と書かれます。

      Pythonは複素数に組込みで対応し、後者の表記を取っています。
      虚部は末尾に ``j`` をつけて書きます。例えば、 ``3+1j`` となります。
      :mod:`math` モジュールの複素数版を利用するには、 :mod:`cmath` を使います。

      複素数の使用はかなり高度な数学の機能です。
      必要性を感じなければ、ほぼ間違いなく無視してしまってよいでしょう。

      .. An extension of the familiar real number system in which all numbers are
         expressed as a sum of a real part and an imaginary part.  Imaginary
         numbers are real multiples of the imaginary unit (the square root of
         ``-1``), often written ``i`` in mathematics or ``j`` in
         engineering. Python has builtin support for complex numbers, which are
         written with this latter notation; the imaginary part is written with a
         ``j`` suffix, e.g., ``3+1j``.  To get access to complex equivalents of the
         :mod:`math` module, use :mod:`cmath`.  Use of complex numbers is a fairly
         advanced mathematical feature.  If you're not aware of a need for them,
         it's almost certain you can safely ignore them.

   context manager
      (コンテキストマネージャー)
      :keyword:`with` 文で扱われる、環境を制御するオブジェクト。
      :meth:`__enter__` と :meth:`__exit__` メソッドを定義することで作られる。

      :pep:`343` を参照。

   CPython
      Pythonプログラミング言語の基準となる実装。
      CPython という単語は、この実装を Jython や IronPython といった他の実装と
      区別する必要が有る文脈で利用されます。

   decorator
      (デコレータ)
      関数を返す関数。
      通常、 ``@wrapper`` という文法によって関数を変換するのに利用されます。
      デコレータの一般的な利用レとして、 :func:`classmethod` と
      :func:`staticmethod` があります。

      デコレータの文法はシンタックスシュガーです。
      次の2つの関数定義は意味的に同じものです。 ::

         def f(...):
             ...
         f = staticmethod(f)

         @staticmethod
         def f(...):
             ...

      デコレータについてのより詳しい情報は、
      :ref:`the documentation for function definition <function>`
      を参照してください。

   descriptor
      (デスクリプタ)
      メソッド :meth:`__get__`, :meth:`__set__`, あるいは :meth:`__delete__`
      が定義されている *新スタイル (new-style)* のオブジェクトです。
      あるクラス属性がデスクリプタである場合、その属性を参照するときに、
      そのデスクリプタに束縛されている特別な動作を呼び出します。
      通常、get,set,deleteのために *a.b* と書くと、 *a* のクラス辞書内でオブジェクト
      *b* を検索しますが、 *b* がデスクリプタの場合にはデスクリプタで定義された
      メソッドを呼び出します。
      デスクリプタの理解は、 Python を深く理解する上で鍵となります。
      というのは、デスクリプタこそが、関数、メソッド、プロパティ、
      クラスメソッド、静的メソッド、そしてスーパクラスの参照といった多くの機能の基盤だからです。

      .. todo::
         デスクリプタとディスクリプタのどちらかに統一する。

      .. Any *new-style* object which defines the methods :meth:`__get__`,
         :meth:`__set__`, or :meth:`__delete__`.  When a class attribute is a
         descriptor, its special binding behavior is triggered upon attribute
         lookup.  Normally, using *a.b* to get, set or delete an attribute looks up
         the object named *b* in the class dictionary for *a*, but if *b* is a
         descriptor, the respective descriptor method gets called.  Understanding
         descriptors is a key to a deep understanding of Python because they are
         the basis for many features including functions, methods, properties,
         class methods, static methods, and reference to super classes.

         For more information about descriptors' methods, see :ref:`descriptors`.

   dictionary
      (辞書)
      任意のキーを値に対応付ける連想配列です。
      :class:`dict` の使い方は :class:`list` に似ていますが、ゼロから始まる整数に限らず、
      :meth:`__hash__` 関数を実装している全てのオブジェクトをキーにできます。
      Perl ではハッシュ (hash) と呼ばれています。

      .. An associative array, where arbitrary keys are mapped to values.  The use
         of :class:`dict` closely resembles that for :class:`list`, but the keys can
         be any object with a :meth:`__hash__` function, not just integers.
         Called a hash in Perl.

   docstring
      クラス、関数、モジュールの最初の式となっている文字列リテラルです。
      実行時には無視されますが、コンパイラによって識別され、そのクラス、
      関数、モジュールの :attr:`__doc__` 属性として保存されます。
      イントロスペクションできる（訳注: 属性として参照できる）ので、
      オブジェクトのドキュメントを書く正しい場所です。

      .. todo::
         ドキュメンテーション文字列？？　統一した訳語を定義する。

   duck-typing
      Python 的なプログラムスタイルではオブジェクトの型を（型オブジェクトとの関係ではなく）
      メソッドや属性といったシグネチャを見ることで判断します。
      （「もしそれがガチョウのようにみえて、ガチョウのように鳴けば、それはガチョウである」）
      インタフェースを型より重視することで、上手くデザインされたコードは
      (polymorphicな置換を許可することによって)柔軟性を増すことができます。
      duck-typing は :func:`type` や :func:`isinstance` を避けます。
      (ただし、duck-typing を抽象ベースクラス(abstract base classes)で補完することもできます。)
      その代わりに :func:`hasattr` テストや *EAFP* プログラミング を利用します。

      .. A pythonic programming style which determines an object's type by inspection
         of its method or attribute signature rather than by explicit relationship
         to some type object ("If it looks like a duck and quacks like a duck, it
         must be a duck.")  By emphasizing interfaces rather than specific types,
         well-designed code improves its flexibility by allowing polymorphic
         substitution.  Duck-typing avoids tests using :func:`type` or
         :func:`isinstance`. (Note, however, that duck-typing can be complemented
         with abstract base classes.) Instead, it typically employs :func:`hasattr`
         tests or :term:`EAFP` programming.

   EAFP
      「認可をとるより許しを請う方が容易  (easier to ask for forgiveness than permission、マーフィーの法則)」
      の略です。 Python で広く使われているコーディングスタイルでは、通常は有効なキーや
      属性が存在するものと仮定し、その仮定が誤っていた場合に例外を捕捉します。
      この簡潔で手早く書けるコーディングスタイルには、 :keyword:`try` 文および
      :keyword:`except` 文がたくさんあるのが特徴です。
      このテクニックは、C のような言語でよく使われている :term:`LBYL` スタイルと対照的なものです。

      .. Easier to ask for forgiveness than permission.  This common Python coding
         style assumes the existence of valid keys or attributes and catches
         exceptions if the assumption proves false.  This clean and fast style is
         characterized by the presence of many :keyword:`try` and :keyword:`except`
         statements.  The technique contrasts with the :term:`LBYL` style
         common to many other languages such as C.

   expression
      (式)
      何かの値に評価される、一つづきの構文(a piece of syntax).
      言い換えると、リテラル、名前、属性アクセス、演算子や関数呼び出しといった、
      値を返す式の要素の組み合わせ。
      他の多くの言語と違い、Pythonは言語の全ての構成要素が式というわけではありません。
      :keyword:`print` や :keyword:`if` のように、式にはならない、文(:term:`statement`)
      もあります。代入も式ではなく文です。

   extension module
      (拡張モジュール)
      CやC++で書かれたモジュール。ユーザーコードやPythonのコアとやりとりするために、
      PythonのC APIを利用します。

   finder
      モジュールの :term:`loader` を探すオブジェクト。
      :meth:`find_module` という名前のメソッドを実装していなければなりません。
      詳細については :pep:`302` を参照してください。

   function
      (関数)
      呼び出し側に値を返す、一連の文。
      ゼロ個以上の引数を受け取り、それを関数の本体を実行するときに諒できます。
      :term:`argument` や :term:`method` も参照してください。

   __future__
      互換性のない新たな機能を現在のインタプリタで有効にするためにプログラマが
      利用できる擬似モジュールです。例えば、式 ``11/4`` は現状では ``2``
      になります。この式を実行しているモジュールで ::

         from __future__ import division

      を行って *真の除算操作 (true division)* を有効にすると、式 ``11/4`` は
      ``2.75`` になります。実際に :mod:`__future__` モジュールを import
      してその変数を評価すれば、新たな機能が初めて追加されたのがいつで、
      いつデフォルトの機能になる予定かわかります。 ::

         >>> import __future__
         >>> __future__.division
         _Feature((2, 2, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0), 8192)

   garbage collection
      (ガベージコレクション)
      もう使われなくなったメモリを開放する処理。
      Pythonは、Pythonは参照カウントと循環参照を見つけて破壊する循環参照コレクタ
      を使ってガベージコレクションを行います。

      .. index:: single: generator

   generator
      (ジェネレータ)
      イテレータを返す関数です。 :keyword:`return` 文の代わりに :keyword:`yield`
      文を使って呼び出し側に要素を返す他は、通常の関数と同じに見えます。

      よくあるジェネレータ関数は一つまたはそれ以上の :keyword:`for` ループや :keyword:`while` ループ
      を含んでおり、ループの呼び出し側に要素を返す(:keyword:`yield`)ようになっています。
      ジェネレータが返すイテレータを使って関数を実行すると、関数は
      :keyword:`yield` キーワードで (値を返して) 一旦停止し、 :meth:`next`
      を呼んで次の要素を要求するたびに実行を再開します。

      .. A function which returns an iterator.  It looks like a normal function
         except that values are returned to the caller using a :keyword:`yield`
         statement instead of a :keyword:`return` statement.  Generator functions
         often contain one or more :keyword:`for` or :keyword:`while` loops which
         :keyword:`yield` elements back to the caller.  The function execution is
         stopped at the :keyword:`yield` keyword (returning the result) and is
         resumed there when the next element is requested by calling the
         :meth:`next` method of the returned iterator.

      .. index:: single: generator expression

   generator expression
      (ジェネレータ式)
      ジェネレータを返す式です。
      普通の式に、ループ変を定義している :keyword:`for` 式、範囲、そしてオプショナルな
      :keyword:`if` 式がつづいているように見えます。
      こうして構成された式は、外側の関数に対して値を生成します。::

         >>> sum(i*i for i in range(10))         # sum of squares 0, 1, 4, ... 81
         285

      .. An expression that returns a generator.  It looks like a normal expression
         followed by a :keyword:`for` expression defining a loop variable, range,
         and an optional :keyword:`if` expression.  The combined expression
         generates values for an enclosing function::


   GIL
      グローバルインタプリタロック(:term:`global interpreter lock`)を参照してください。

   global interpreter lock
      (グローバルインタプリタロック)
      :term:`CPython` のVM(:term:`virtual machine`)の中で一度に1つのスレッドだけが
      動作することを保証するために使われているロックです。
      このロックによって、同時に同じメモリにアクセスする2つのプロセスは存在しないと保証されているので、
      CPython を単純な構造にできるのです。
      インタプリタ全体にロックをかけると、多重プロセサ計算機における並列性の恩恵と引き換えにインタプリタの
      多重スレッド化を簡単に行えます。かつて "スレッド自由な (free-threaded)"
      インタプリタを作ろうと 努力したことがありましたが、広く使われている単一プロセッサの場合には
      パフォーマンスが低下するという事態に悩まされました。

      .. The lock used by Python threads to assure that only one thread
         executes in the :term:`CPython` :term:`virtual machine` at a time.
         This simplifies the CPython implementation by assuring that no two
         processes can access the same memory at the same time.  Locking the
         entire interpreter makes it easier for the interpreter to be
         multi-threaded, at the expense of much of the parallelism afforded by
         multi-processor machines.  Efforts have been made in the past to
         create a "free-threaded" interpreter (one which locks shared data at a
         much finer granularity), but so far none have been successful because
         performance suffered in the common single-processor case.

   hashable
      (ハッシュ可能)
      *ハッシュ可能* なオブジェクトとは、生存期間中変わらないハッシュ値を持ち
      (:meth:`__hash__` メソッドが必要)、他のオブジェクトと比較ができる
      (:meth:`__eq__` か :meth:`__cmp__` メソッドが必要) オブジェクトです。
      同値なハッシュ可能オブジェクトは必ず同じハッシュ値を持つ必要があります。

      辞書のキーや集合型のメンバーは、内部でハッシュ値を使っているので、
      ハッシュ可能オブジェクトである必要があります。

      Python の全ての不変(:term:`immutable`)なビルドインオブジェクトはハッシュ可能です。
      リストや辞書といった変更可能なコンテナ型はハッシュ可能ではありません。

      ユーザー定義クラスのインスタンスはデフォルトでハッシュ可能です。
      それらは、比較すると常に不等で、ハッシュ値は :func:`id` になります。

   IDLE
      Python の組み込み開発環境 (Integrated DeveLopment Environment) です。
      IDLE は Pythonの標準的な配布物についてくる基本的な機能のエディタとインタプリタ環境です。
      初心者に向いている点として、 IDLEはよく洗練され、複数プラットフォームで動作する GUI
      アプリケーションを実装したい人むけの明解なコード例にもなっています。

      .. An Integrated Development Environment for Python.  IDLE is a basic editor
         and interpreter environment which ships with the standard distribution of
         Python.  Good for beginners, it also serves as clear example code for
         those wanting to implement a moderately sophisticated, multi-platform GUI
         application.

   immutable
      (不変オブジェクト)
      固定の値を持ったオブジェクトです。
      変更不能なオブジェクトには、 数値、文字列、およびタプルなどがあります。
      これらのオブジェクトは値を変えられません。
      別の値を記憶させる際には、 新たなオブジェクトを作成しなければなりません。
      不変オブジェクトは、固定のハッシュ値が必要となる状況で重要な役割を果たします。
      辞書におけるキーがその例です。

      .. An object with a fixed value.  Immutable objects include numbers, strings and
         tuples.  Such an object cannot be altered.  A new object has to
         be created if a different value has to be stored.  They play an important
         role in places where a constant hash value is needed, for example as a key
         in a dictionary.

   integer division
      (整数除算)
      剰余を考慮しない数学的除算です。例えば、式 ``11/4`` は現状では ``2.75`` ではなく
      ``2`` になります。これは *切り捨て除算 (floor division)* とも呼ばれます。
      二つの整数間で除算を行うと、結果は (端数切捨て関数が適用されて)  常に整数になります。
      しかし、被演算子の一方が (:class:`float` のような) 別の数値型の場合、
      演算の結果は共通の型に型強制されます (型強制(:term:`coercion`)参照)。
      例えば、浮動小数点数で整数を除算すると結果は浮動小数点になり、
      場合によっては端数部分を伴います。 ``//`` 演算子を
      ``/`` の代わりに使うと、整数除算を強制できます。
      :term:`__future__` も参照してください。

      .. Mathematical division discarding any remainder.  For example, the
         expression ``11/4`` currently evaluates to ``2`` in contrast to the
         ``2.75`` returned by float division.  Also called *floor division*.
         When dividing two integers the outcome will always be another integer
         (having the floor function applied to it). However, if one of the operands
         is another numeric type (such as a :class:`float`), the result will be
         coerced (see :term:`coercion`) to a common type.  For example, an integer
         divided by a float will result in a float value, possibly with a decimal
         fraction.  Integer division can be forced by using the ``//`` operator
         instead of the ``/`` operator.  See also :term:`__future__`.

   importer
      モジュールを探してロードするオブジェクト。 :term:`finder` と :term:`loader`
      のどちらでもあるオブジェクト。

   interactive
      (対話的)
      Python には対話的インタプリタがあり、文や式をインタプリタのプロンプトに
      入力すると即座に実行されて結果を見ることができます。
      ``python`` と何も引数を与えずに実行してください。(コンピュータのメインメニューから
      Pythonの対話的インタプリタを起動できるかもしれません。)
      対話的インタプリタは、新しいあアイデアを試してみたり、モジュールや
      パッケージの中を覗いてみる(``help(x)`` を覚えておいてください)
      のに非常に便利なツールです。

   interpreted
      Python はインタプリタ形式の言語であり、コンパイラ言語の対極に位置します。
      (バイトコードコンパイラがあるために、この区別は曖昧ですが。)
      ここでのインタプリタ言語とは、ソースコードのファイルを、
      まず実行可能形式にしてから実行させるといった操作なしに、直接実行できることを意味します。
      インタプリタ形式の言語は通常、
      コンパイラ形式の言語よりも開発／デバッグのサイクルは短いものの、プログラムの実行は一般に遅いです。
      対話的(:term:`interactive`)も参照してください。

      .. Python is an interpreted language, as opposed to a compiled one,
         though the distinction can be blurry because of the presence of the
         bytecode compiler.  This means that source files can be run directly
         without explicitly creating an executable which is then run.
         Interpreted languages typically have a shorter development/debug cycle
         than compiled ones, though their programs generally also run more
         slowly.  See also :term:`interactive`.

   iterable
      (反復可能オブジェクト)
      要素を一つずつ返せるオブジェクトです。

      反復可能オブジェクトの例には、(:class:`list`, :class:`str`, :class:`tuple` といった)
      全てのシーケンス型や、 :class:`dict` や :class:`file` といった幾つかの非シーケンス型、
      あるいは :meth:`__iter__` か :meth:`__getitem__` メソッドを実装したクラスのインスタンスが含まれます。

      反復可能オブジェクトは :keyword:`for` ループ内やその他多くのシーケンス
      (訳注: ここでのシーケンスとは、シーケンス型ではなくただの列という意味)が必要となる状況
      (:func:`zip`, :func:`map`, ...) で利用できます。

      反復可能オブジェクトを組み込み関数 :func:`iter` の引数として渡すと、
      オブジェクトに対するイテレータを返します。
      このイテレータは一連の値を引き渡す際に便利です。
      反復可能オブジェクトを使う際には、通常 :func:`iter` を呼んだり、
      イテレータオブジェクトを自分で扱う必要はありません。
      ``for`` 文ではこの操作を自動的に行い、無名の変数を作成してループの間イテレータを記憶します。
      イテレータ(:term:`iterator`) シーケンス(:term:`sequence`),
      およびジェネレータ(:term:`generator`)も参照してください。

   iterator
      一連のデータ列 (stream) を表現するオブジェクトです。
      イテレータの :meth:`next` メソッドを繰り返し呼び出すと、
      データ列中の要素を一つずつ返します。
      後続のデータがなくなると、 データの代わりに :exc:`StopIteration` 例外を送出します。
      その時点で、イテレータオブジェクトは全てのオブジェクトを出し尽くしており、
      それ以降は :meth:`next` を何度呼んでも :exc:`StopIteration` を送出します。
      イテレータは、そのイテレータオブジェクト自体を返す :meth:`__iter__`
      メソッドを実装しなければならなくなっており、そのため全てのイテレータは他の
      反復可能オブジェクトを受理できるほとんどの場所で利用できます。
      著しい例外は複数の反復を行うようなコードです。
      (:class:`list` のような) コンテナオブジェクトでは、 :func:`iter`
      関数にオブジェクトを渡したり、 :keyword:`for` ループ内で使うたびに、
      新たな未使用のイテレータを生成します。
      このイテレータをさらに別の場所でイテレータとして使おうとすると、
      前回のイテレーションパスで使用された同じイテレータオブジェクトを返すため、
      空のコンテナのように見えます。

      より詳細な情報は :ref:`typeiter` にあります。

      .. An object representing a stream of data.  Repeated calls to the iterator's
         :meth:`next` method return successive items in the stream.  When no more
         data are available a :exc:`StopIteration` exception is raised instead.  At
         this point, the iterator object is exhausted and any further calls to its
         :meth:`next` method just raise :exc:`StopIteration` again.  Iterators are
         required to have an :meth:`__iter__` method that returns the iterator
         object itself so every iterator is also iterable and may be used in most
         places where other iterables are accepted.  One notable exception is code
         which attempts multiple iteration passes.  A container object (such as a
         :class:`list`) produces a fresh new iterator each time you pass it to the
         :func:`iter` function or use it in a :keyword:`for` loop.  Attempting this
         with an iterator will just return the same exhausted iterator object used
         in the previous iteration pass, making it appear like an empty container.

         More information can be found in :ref:`typeiter`.

   keyword argument
      (キーワード引数)
      呼び出し時に、 ``variable_name=`` が手前にある引数。
      変数名は、その値が関数内のどのローカル変数に渡されるかを指定します。
      キーワード引数として辞書を受け取ったり渡したりするために ``**``
      を使うことができます。 :term:`argument` も参照してください。

   lambda
      (ラムダ)
      無名のインライン関数で、関数が呼び出されたときに評価される1つの式
      (:term:`expression`) を持ちます。
      ラムダ関数を作る構文は、 ``lambda [arguments]: expression`` です。


   LBYL
      「ころばぬ先の杖」 (look before you leap) の略です。
      このコーディングスタイルでは、呼び出しや検索を行う前に、明示的に前提条件
      (pre-condition) 判定を行います。
      *EAFP* アプローチと対照的で、:keyword:`if` 文がたくさん使われるのが特徴的です。

      .. Look before you leap.  This coding style explicitly tests for
         pre-conditions before making calls or lookups.  This style contrasts with
         the :term:`EAFP` approach and is characterized by the presence of many
         :keyword:`if` statements.

   list
      (リスト)
      Python のビルトインのシーケンス型(:term:`sequence`)です。
      リストという名前ですが、リンクリストではなく、他の言語で言う配列(array)と
      同種のもので、要素へのアクセスは O(1) です。

   list comprehension
      (リスト内包表記)
      シーケンス内の全てあるいは一部の要素を処理して、その結果からなるリストを返す、
      コンパクトな書き方です。
      ``result = ["0x%02x" % x for x in range(256) if x % 2 == 0]``
      とすると、 0 から 255 までの偶数を 16進数表記 (0x..) した文字列からなるリストを生成します。
      :keyword:`if` 節はオプションです。 :keyword:`if` 節がない場合、
      ``range(256)`` の全ての要素が処理されます。

      .. A compact way to process all or part of the elements in a sequence and
         return a list with the results.  ``result = ["0x%02x" % x for x in
         range(256) if x % 2 == 0]`` generates a list of strings containing
         even hex numbers (0x..) in the range from 0 to 255. The :keyword:`if`
         clause is optional.  If omitted, all elements in ``range(256)`` are
         processed.

   loader
      モジュールをロードするオブジェクト。
      :meth:`load_module` という名前のメソッドを定義していなければなりません。
      詳細は :pep:`302` を参照してください。

   mapping
      (マップ)
      特殊メソッド :meth:`__getitem__` を使って、任意のキーに対する検索をサポートする
      (:class:`dict` のような)コンテナオブジェクトです。

      .. A container object (such as :class:`dict`) which supports arbitrary key
         lookups using the special method :meth:`__getitem__`.

   metaclass
      (メタクラス)
      クラスのクラスです。
      クラス定義は、クラス名、クラスの辞書と、基底クラスのリストを作ります。
      メタクラスは、それら3つを引数として受け取り、クラスを作る責任を負います。
      ほとんどのオブジェクト指向言語は(訳注:メタクラスの)デフォルトの実装を提供しています。
      Pythonはカスタムのメタクラスを作成できる点が特別です。
      ほとんどのユーザーに取って、メタクラスは全く必要のないものです。
      しかし、一部の場面では、メタクラスは強力でエレガントな方法を提供します。
      たとえば属性アクセスのログを取ったり、スレッドセーフ性を追加したり、オブジェクトの
      生成を追跡したり、シングルトンを実装するなど、多くの場面で利用されます。

      .. The class of a class.  Class definitions create a class name, a class
         dictionary, and a list of base classes.  The metaclass is responsible for
         taking those three arguments and creating the class.  Most object oriented
         programming languages provide a default implementation.  What makes Python
         special is that it is possible to create custom metaclasses.  Most users
         never need this tool, but when the need arises, metaclasses can provide
         powerful, elegant solutions.  They have been used for logging attribute
         access, adding thread-safety, tracking object creation, implementing
         singletons, and many other tasks.

         More information can be found in :ref:`metaclasses`.

   method
      クラス内で定義された関数。
      クラス属性として呼び出された場合、メソッドはインスタンスオブジェクトを
      第一引数(:term:`argument`) として受け取ります(この第一引数は普段
      ``self`` と呼ばれます)。
      :term:`function` と :term:`nested scope` も参照してください。

   mutable
      (変更可能オブジェクト)
      変更可能なオブジェクトは、 :func:`id` を変えることなく値を変更できます。
      変更不能 (:term:`immutable`) も参照してください。

      .. Mutable objects can change their value but keep their :func:`id`.  See
         also :term:`immutable`.

   named tuple
      (名前付きタプル)
      タプルに似ていて、インデックスによりアクセスする要素に名前付き属性としても
      アクセス出来るクラス。
      (例えば、 :func:`time.localtime` はタプルに似たオブジェクトを返し、
      その *year* には ``t[0]`` のようなインデックスによるアクセスと、
      ``t.tm_year`` のような名前付き要素としてのアクセスが可能です。)

      名前付きタプルには、 :class:`time.struct_time` のようなビルトイン型もありますし、
      通常のクラス定義によって作成することもできます。
      名前付きタプルを :func:`collections.namedtuple` ファクトリ関数で作成することもできます。
      最後の方法で作った名前付きタプルには自動的に、
      ``Employee(name='jones', title='programmer')`` のような自己ドキュメント表現(self-documenting
      representation) 機能が付いてきます。

   namespace
      (名前空間)
      変数を記憶している場所です。
      名前空間は辞書を用いて実装されています。
      名前空間には、ローカル、グローバル、組み込み名前空間、そして (メソッド内の)
      オブジェクトのネストされた名前空間があります。
      例えば、関数 :func:`__builtin__.open` と :func:`os.open`
      は名前空間で区別されます。
      名前空間はまた、ある関数をどのモジュールが実装しているかをはっきりさせることで、
      可読性やメンテナンス性に寄与します。
      例えば、 :func:`random.seed`, :func:`itertools.izip` と書くことで、これらの関数がそれぞれ
      :mod:`random` モジュールや :mod:`itertools`
      モジュールで実装されていることがはっきりします。

      .. The place where a variable is stored.  Namespaces are implemented as
         dictionaries.  There are the local, global and builtin namespaces as well
         as nested namespaces in objects (in methods).  Namespaces support
         modularity by preventing naming conflicts.  For instance, the functions
         :func:`__builtin__.open` and :func:`os.open` are distinguished by their
         namespaces.  Namespaces also aid readability and maintainability by making
         it clear which module implements a function.  For instance, writing
         :func:`random.seed` or :func:`itertools.izip` makes it clear that those
         functions are implemented by the :mod:`random` and :mod:`itertools`
         modules, respectively.

   nested scope
      (ネストされたスコープ)
      外側で定義されている変数を参照する機能。
      具体的に言えば、ある関数が別の関数の中で定義されている場合、内側の関数は外側の関数中の変数を参照できます。
      ネストされたスコープは変数の参照だけができ、変数の代入はできないので注意してください。
      変数の代入は、常に最も内側のスコープにある変数に対する書き込みになります。
      同様に、グローバル変数を使うとグローバル名前空間の値を読み書きします。

      .. The ability to refer to a variable in an enclosing definition.  For
         instance, a function defined inside another function can refer to
         variables in the outer function.  Note that nested scopes work only for
         reference and not for assignment which will always write to the innermost
         scope.  In contrast, local variables both read and write in the innermost
         scope.  Likewise, global variables read and write to the global namespace.

   new-style class
      (新スタイルクラス)
      :class:`object` から継承したクラス全てを指します。これには :class:`list` や :class:`dict`
      のような全ての組み込み型が含まれます。 :meth:`__slots__`, デスクリプタ、プロパティ、
      :meth:`__getattribute__` といった、
      Python の新しい機能を使えるのは新スタイルクラスだけです。

      より詳しい情報は :ref:`newstyle` を参照してください。

      .. Any class which inherits from :class:`object`.  This includes all built-in
         types like :class:`list` and :class:`dict`.  Only new-style classes can
         use Python's newer, versatile features like :attr:`__slots__`,
         descriptors, properties, and :meth:`__getattribute__`.

         More information can be found in :ref:`newstyle`.

   object
      状態(属性や値)と定義された振る舞い(メソッド)をもつ全てのデータ。
      もしくは、全ての新スタイルクラス(:term:`new-style class`)
      の基底クラスのこと。

   positional argument
      (位置指定引数)
      引数のうち、呼び出すときの順序で、関数やメソッドの中のどの名前に
      代入されるかが決定されるもの。
      複数の位置指定引数を、関数定義側が受け取ったり、渡したりするために、
      ``*`` を使うことができます。
      :term:`argument` も参照してください。

   Python 3000
      Pythonの次のメジャーバージョンである Python 3.0 のニックネームです。
      (Python 3 が遠い将来の話だった頃に作られた言葉です。)
      "Py3k" と略されることもあります。

      .. Nickname for the next major Python version, 3.0 (coined long ago
         when the release of version 3 was something in the distant future.)  This
         is also abbreviated "Py3k".

   Pythonic
      他の言語で一般的な考え方で書かれたコードではなく、Python の特に一般的な
      イディオムに繋がる、考え方やコード。
      例えば、Python の一般的なイディオムに iterable の要素を :keyword:`for`
      文を使って巡回することです。この仕組を持たない言語も多くあるので、Python
      に慣れ親しんでいない人は数値のカウンターを使うかもしれません。 ::

          for i in range(len(food)):
              print food[i]

      これと対照的な、よりきれいな Pythonic な方法はこうなります。 ::

         for piece in food:
             print piece

   reference count
      (参照カウント)
      あるオブジェクトに対する参照の数。
      参照カウントが0になったとき、そのオブジェクトは破棄されます。
      参照カウントは通常は Python のコード上には現れませんが、
      :term:`CPython` 実装の重要な要素です。
      :mod:`sys` モジュールは、プログラマーが任意のオブジェクトの参照カウントを
      知るための :func:`getrefcount` 関数を提供しています。

   __slots__
      新スタイルクラス(:term:`new-style class`)内で、インスタンス属性の記憶に
      必要な領域をあらかじめ定義しておき、それとひきかえにインスタンス辞書を排除して
      メモリの節約を行うための宣言です。
      これはよく使われるテクニックですが、正しく動作させるのには少々手際を要するので、
      例えばメモリが死活問題となるようなアプリケーション内にインスタンスが大量に
      存在するといった稀なケースを除き、使わないのがベストです。

      .. A declaration inside a :term:`new-style class` that saves memory by
         pre-declaring space for instance attributes and eliminating instance
         dictionaries.  Though popular, the technique is somewhat tricky to get
         right and is best reserved for rare cases where there are large numbers of
         instances in a memory-critical application.

   sequence
      (シーケンス)
      特殊メソッド :meth:`__getitem__` で整数インデックスによる効率的な要素へのアクセスを
      サポートし、 :meth:`len` で長さを返すような反復可能オブジェクト(:term:`iterable`)です。
      組み込みシーケンス型には、 :class:`list`, :class:`str`, :class:`tuple`, :class:`unicode`
      などがあります。
      :class:`dict` は :meth:`__getitem__` と :meth:`__len__` もサポートしますが、
      検索の際に任意の変更不能(:term:`immutable`)なキーを使うため、シーケンスではなく
      マップ (mapping) とみなされて いるので注意してください。

      .. An :term:`iterable` which supports efficient element access using integer
         indices via the :meth:`__getitem__` special method and defines a
         :meth:`len` method that returns the length of the sequence.
         Some built-in sequence types are :class:`list`, :class:`str`,
         :class:`tuple`, and :class:`unicode`. Note that :class:`dict` also
         supports :meth:`__getitem__` and :meth:`__len__`, but is considered a
         mapping rather than a sequence because the lookups use arbitrary
         :term:`immutable` keys rather than integers.

   slice
      (スライス)
      多くの場合、シーケンス(:term:`sequence`)の一部を含むオブジェクト。
      スライスは、添字記号 ``[]`` で数字の間にコロンを書いたときに作られます。
      例えば、 ``variable_name[1:3:5]`` です。
      添字記号は :class:`slice` オブジェクトを内部で利用しています。
      (もしくは、古いバージョンの、 :meth:`__getslice__` と :meth:`__setslice__`
      を利用します。)

   special method
      (特殊メソッド)
      ある型に対する特定の動作をするために、 Python から暗黙的に呼ばれるメソッド。
      この種類のメソッドは、メソッド名の最初と最後にアンダースコア2つを持ちます。
      特殊メソッドについては :ref:`specialnames` で解説されています。

   statement
      (文)
      文は一種のコードブロックです。
      文は :term:`expression` か、それ以外のキーワードにより構成されます。
      例えば :keyword:`if`, :keyword:`while`, :keyword:`print` は文です。

   triple-quoted string
      (三重クォート文字列)
      3つの連続したクォート記号(")かアポストロフィー(')で囲まれた文字列。
      通常の(一重)クォート文字列に比べて表現できる文字列に違いはありませんが、
      幾つかの理由で有用です。
      1つか2つの連続したクォート記号をエスケープ無しに書くことができますし、
      行継続文字(\\)を使わなくても複数行にまたがることができるので、
      ドキュメンテーション文字列を書く時に特に便利です。

   type
      (型)
      Python のオブジェクトの型は、そのオブジェクトの種類を決定します。
      全てのオブジェクトは型を持っています。
      オブジェクトの型は、 :attr:`__class__` 属性からアクセスしたり、
      ``type(obj)`` で取得することができます。

   virtual machine
      (仮想マシン)
      ソフトウェアにより定義されたコンピュータ。
      Python の仮想マシンは、バイトコードコンパイラが出力したバイトコード
      (:term:`bytecode`)を実行します。

   Zen of Python
      (Pythonの悟り)
      Python を理解し利用する上での導きとなる、Python の設計原則と哲学をリストにしたものです。
      対話プロンプトで "``import this``" とするとこのリストを読めます。

      .. Listing of Python design principles and philosophies that are helpful in
         understanding and using the language.  The listing can be found by typing
         "``import this``" at the interactive prompt.
