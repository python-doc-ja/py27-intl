.. _tut-classes:

******
クラス
******

Python では、最小限の構文と意味付けを使ってクラス (class) のメカニズム を言語に追加しています。Python のクラスは、C++ と
Modula-3 で 見られるクラスメカニズムを混合したものです。モジュールがそうであるように、 Python
におけるクラスでは、クラス定義とユーザとの間に絶対的な障壁を おかず、ユーザが礼儀正しく、 "定義に首を突っ込む" ことはないと
あてにしています。とはいえ、クラスにおける最も重要な機能はそのままに、 完全な力を持っています: クラスの継承 (inheritance) メカニズムでは、
複数の基底クラスを持つことができ、導出されたクラスでは基底クラスの 任意のメソッドをオーバライド (override, 上書き) することができます。
メソッドでは、基底クラスのメソッドを同じ名前で呼び出すことができます。 オブジェクトには任意のプライベートなデータを入れることができます。

.. % Classes
.. % % Python's class mechanism adds classes to the language with a minimum
.. % % of new syntax and semantics.  It is a mixture of the class mechanisms
.. % % found in \Cpp{} and Modula-3.  As is true for modules, classes in Python
.. % % do not put an absolute barrier between definition and user, but rather
.. % % rely on the politeness of the user not to ``break into the
.. % % definition.''  The most important features of classes are retained
.. % % with full power, however: the class inheritance mechanism allows
.. % % multiple base classes, a derived class can override any methods of its
.. % % base class or classes, and a method can call the method of a base class with the
.. % % same name.  Objects can contain an arbitrary amount of private data.

C++ の用語では、全てのクラスメンバ (データメンバも含む) は *public* (公開されたデータ) であり、メンバ関数はすべて *仮想関数
(virtual)* です。特別なコンストラクタ (constructor: 生成関数) やデストラクタ (destructor: 破壊関数)
はありません。Module-3 にあるような、オブジェクトのメンバをメソッドから参照するために短縮した 記法は使えません:
メソッド関数の宣言では、オブジェクト自体を表すパラメ タ第一引数に明示せねばなりません。第一引数のオブジェクトはメソッド呼び
出しの際に暗黙の引数として渡されます。Smalltalk に似て、クラスはそれ自 体がオブジェクトです。とはいえ、これは広義のオブジェクトという意味で、
Python では全てのデータ型はオブジェクトです。このことは、import や名前 変更といった操作のセマンティクスにつながります。 C++ や
Modula-3 と違って、ユーザは組込みの型を基底クラスにして拡張 を行えます。また、C++ とは同じで Modula-3 とは違う点として、特別な
構文を伴うほとんどの組み込み演算子 (算術演算子 (arithmetic operator) や添字表記) はクラスインスタンスで使うために再定義できます。

.. % % In \Cpp{} terminology, all class members (including the data members) are
.. % % \emph{public}, and all member functions are \emph{virtual}.  There are
.. % % no special constructors or destructors.  As in Modula-3, there are no
.. % % shorthands for referencing the object's members from its methods: the
.. % % method function is declared with an explicit first argument
.. % % representing the object, which is provided implicitly by the call.  As
.. % % in Smalltalk, classes themselves are objects, albeit in the wider
.. % % sense of the word: in Python, all data types are objects.  This
.. % % provides semantics for importing and renaming.  Unlike
.. % % \Cpp{} or Modula-3, built-in types can be used as base classes for
.. % % extension by the user.  Also, like in \Cpp{} but unlike in Modula-3, most
.. % % built-in operators with special syntax (arithmetic operators,
.. % % subscripting etc.) can be redefined for class instances.


.. _tut-terminology:

用語について一言
================

クラスに関して広範に受け入れられている用語定義がないので、 Smalltalk と C++ の用語を場合に応じて使っていくことに します。
(オブジェクト指向における意味付けの方法は C++よりも  Modula-3 のほうが Python に近いので Modula-3 の用語を使いたいのですが、
ほとんどの読者はそれを耳にしたことがないと思います。)

.. % A Word About Terminology
.. % % Lacking universally accepted terminology to talk about classes, I will
.. % % make occasional use of Smalltalk and \Cpp{} terms.  (I would use Modula-3
.. % % terms, since its object-oriented semantics are closer to those of
.. % % Python than \Cpp, but I expect that few readers have heard of it.)

オブジェクトには個体性があり、同一のオブジェクトに (複数のスコープの)  複数の名前を割り当てることができます。この機能は他の言語では 別名 (ailias)
づけとして知られています。Python を一見しただけでは、 別名づけの重要性は分からないことが多く、変更不能な基本型 (数値、文字列、 タプル)
を扱うときには無視して差し支えありません。 しかしながら、別名付けには、リストや辞書、またプログラムの外部 にある実体 (ファイル、ウィンドウ、など)
を表現するためのほとんどの型 が入った Python コードで意味付けを行う上で (意図的な！) 効果があります。
別名付けはいくつかの点でポインタのように振舞うので、通常はプログラムに 利するように使われます。例えば、オブジェクトの受け渡しは、実装上は
ポインタが渡されるだけなのでコストの低い操作になります; また、関数が あるオブジェクトを引数として渡されたとき、関数の呼び出し側から
オブジェクトに対する変更を見ることができます --- これにより、 Pascal にあるような二つの引数渡し機構をもつ必要をなくしています。

.. % % Objects have individuality, and multiple names (in multiple scopes)
.. % % can be bound to the same object.  This is known as aliasing in other
.. % % languages.  This is usually not appreciated on a first glance at
.. % % Python, and can be safely ignored when dealing with immutable basic
.. % % types (numbers, strings, tuples).  However, aliasing has an
.. % % (intended!) effect on the semantics of Python code involving mutable
.. % % objects such as lists, dictionaries, and most types representing
.. % % entities outside the program (files, windows, etc.).  This is usually
.. % % used to the benefit of the program, since aliases behave like pointers
.. % % in some respects.  For example, passing an object is cheap since only
.. % % a pointer is passed by the implementation; and if a function modifies
.. % % an object passed as an argument, the caller will see the change --- this
.. % % obviates the need for two different argument passing mechanisms as in
.. % % Pascal.


.. _tut-scopes:

Python のスコープと名前空間
===========================

クラスを紹介する前に、Python のスコープ規則についてあることを話して おかなければなりません。クラス定義はある巧みなトリックを名前空間に
施すので、何が起こっているのかを完全に理解するには、スコープと 名前空間がどのように動作するかを理解する必要があります。 ちなみに、この問題に関する知識は全ての
Python プログラマにとって 有用です。

.. % Python Scopes and Name Spaces
.. % % Before introducing classes, I first have to tell you something about
.. % % Python's scope rules.  Class definitions play some neat tricks with
.. % % namespaces, and you need to know how scopes and namespaces work to
.. % % fully understand what's going on.  Incidentally, knowledge about this
.. % % subject is useful for any advanced Python programmer.

まず定義から始めましょう。

.. % % Let's begin with some definitions.

*名前空間 (namespace)* とは、 名前からオブジェクトへの対応付け (mapping) です。 ほとんどの名前空間は、現状では Python
の辞書として実装されていますが、 そのことは通常は (パフォーマンス以外では) 目立つことはないし、 将来は変更されるかもしれません。
名前空間の例には、組込み名の集合 (:func:`abs` 等の関数や組込み 例外名)、モジュールないのグローバルな名前; 関数を呼び出したときの
ローカルな名前、があります。その意味では、オブジェクトの属性から なる集合もまた、名前空間を形成します。名前空間について知っておくべき
重要なことは、異なった名前空間にある名前の間には全く関係がないと いうことです; 例えば、二つの別々のモジュールの両方で関数  "maximize"
という関数を定義することができ、定義自体は混同され ることはありません  --- モジュールのユーザは名前の前にモジュール名を つけなければなりません。

.. % % A \emph{namespace} is a mapping from names to objects.  Most
.. % % namespaces are currently implemented as Python dictionaries, but
.. % % that's normally not noticeable in any way (except for performance),
.. % % and it may change in the future.  Examples of namespaces are: the set
.. % % of built-in names (functions such as \function{abs()}, and built-in
.. % % exception names); the global names in a module; and the local names in
.. % % a function invocation.  In a sense the set of attributes of an object
.. % % also form a namespace.  The important thing to know about namespaces
.. % % is that there is absolutely no relation between names in different
.. % % namespaces; for instance, two different modules may both define a
.. % % function ``maximize'' without confusion --- users of the modules must
.. % % prefix it with the module name.

ところで、*属性*という言葉は、ドットに続く名前すべてに対して 使っています --- 例えば式 ``z.real`` で、``real`` は オブジェクト
``z`` の属性です。厳密にいえば、モジュール内の名前に 対する参照は属性の参照です: 式 ``modname.funcname`` では、
``modname`` はあるモジュールオブジェクトで、``funcname`` は その属性です。この場合には、たまたまモジュールの属性とモジュール内の
グローバルな名前の間には この場合はたまたま、モジュールの属性とモジュールで定義されている グローバル名の間には、直接的な対応付けがされます: これらの名前は
同じ名前空間を共有しているのです！  [#]_

.. % % By the way, I use the word \emph{attribute} for any name following a
.. % % dot --- for example, in the expression \code{z.real}, \code{real} is
.. % % an attribute of the object \code{z}.  Strictly speaking, references to
.. % % names in modules are attribute references: in the expression
.. % % \code{modname.funcname}, \code{modname} is a module object and
.. % % \code{funcname} is an attribute of it.  In this case there happens to
.. % % be a straightforward mapping between the module's attributes and the
.. % % global names defined in the module: they share the same namespace!
.. % % \footnote{
.. % %         Except for one thing.  Module objects have a secret read-only
.. % %         attribute called \member{__dict__} which returns the dictionary
.. % %         used to implement the module's namespace; the name
.. % %         \member{__dict__} is an attribute but not a global name.
.. % %         Obviously, using this violates the abstraction of namespace
.. % %         implementation, and should be restricted to things like
.. % %         post-mortem debuggers.
.. % % }

属性は読取り専用にも、書き込み専用にもできます。 後者の場合、属性に代入することができます。 モジュール属性は書込み可能です:
``modname.the_answer = 42`` と書く ことができます。書込み可能な属性は、:keyword:`del` 文で削除することも
できます。例えば、``del modname.the_answer`` は、``modname``  で指定されたオブジェクトから属性
:attr:`the_answer` を除去します。

.. % % Attributes may be read-only or writable.  In the latter case,
.. % % assignment to attributes is possible.  Module attributes are writable:
.. % % you can write \samp{modname.the_answer = 42}.  Writable attributes may
.. % % also be deleted with the \keyword{del} statement.  For example,
.. % % \samp{del modname.the_answer} will remove the attribute
.. % % \member{the_answer} from the object named by \code{modname}.

名前空間は様々な時点で作成され、その寿命も様々です。 組み込みの名前が入った名前空間は Python インタプリタが起動するときに
作成され、決して削除されることはありません。モジュールのグローバルな 名前空間は、モジュール定義が読み込まれたときに作成されます; 通常、
モジュールの名前空間は、インタプリタが終了するまで残ります。 インタプリタのトップレベルで実行された文は、スクリプトファイルから
読み出されたものでも対話的に読み出されたものでも、:mod:`__main__` という名前のモジュールの一部分であるとみなされるので、独自の
名前空間を持つことになります。(組み込みの名前は実際にはモジュール内 に存在します; そのモジュールは :mod:`__builtin__`
と呼ばれています。)

.. % % Name spaces are created at different moments and have different
.. % % lifetimes.  The namespace containing the built-in names is created
.. % % when the Python interpreter starts up, and is never deleted.  The
.. % % global namespace for a module is created when the module definition
.. % % is read in; normally, module namespaces also last until the
.. % % interpreter quits.  The statements executed by the top-level
.. % % invocation of the interpreter, either read from a script file or
.. % % interactively, are considered part of a module called
.. % % \module{__main__}, so they have their own global namespace.  (The
.. % % built-in names actually also live in a module; this is called
.. % % \module{__builtin__}.)

関数のローカルな名前空間は、関数が呼び出されたときに作成され、 関数から戻ったときや、関数内で例外が送出され、かつ関数内で処理され なかった場合に削除されます。
(実際には、忘れられる、と言ったほうが起きていることをよく表して います。) もちろん、再帰呼出しのときには、各々の呼び出しで各自の
ローカルな名前空間があります。

.. % % The local namespace for a function is created when the function is
.. % % called, and deleted when the function returns or raises an exception
.. % % that is not handled within the function.  (Actually, forgetting would
.. % % be a better way to describe what actually happens.)  Of course,
.. % % recursive invocations each have their own local namespace.

*スコープ (scope)* とは、ある名前空間が直接アクセスできる (directly accessible) ような、Python
プログラムのテキスト上の領域 です。 "直接アクセス可能" とは、限定なし (unqualified) である名前を参照
した際に、その名前空間から名前を見つけようと試みることを意味します。

.. % % A \emph{scope} is a textual region of a Python program where a
.. % % namespace is directly accessible.  ``Directly accessible'' here means
.. % % that an unqualified reference to a name attempts to find the name in
.. % % the namespace.

スコープは静的に決定されますが、動的に使用されます。 実行中はいつでも、直接名前空間にアクセス可能な、少なくとも三つの 入れ子になったスコープがあります:
最初に検索される最も内側のスコープには、ローカルな名前が入っています; あるいは、最も内側のスコープを囲んでいる関数群のスコープで、最も
近傍のスコープから検索を始めます; 中間のスコープが次に検索され、 このスコープには現在のモジュールのグローバルな名前が入っています; (最後に検索される)
最も外側のスコープは、組み込みの名前が入った 名前空間です。

.. % % Although scopes are determined statically, they are used dynamically.
.. % % At any time during execution, there are at least three nested scopes whose
.. % % namespaces are directly accessible: the innermost scope, which is searched
.. % % first, contains the local names; the namespaces of any enclosing
.. % % functions, which are searched starting with the nearest enclosing scope;
.. % % the middle scope, searched next, contains the current module's global names;
.. % % and the outermost scope (searched last) is the namespace containing built-in
.. % % names.

名前がグローバルであると宣言されている場合、その名前に対する参照や 代入は全て、モジュールのグローバルな名前の入った中間のスコープに
対して直接行われます。そうでない場合、最も内側のスコープより外側に ある変数は全て読み出し専用(そのような変数に対する書き込みは、単に
*新しい*ローカル変数もっとも内側のスコープで作成し、外部のスコー プの値は変化しません)となります。

.. % % If a name is declared global, then all references and assignments go
.. % % directly to the middle scope containing the module's global names.
.. % % Otherwise, all variables found outside of the innermost scope are read-only
.. % % (an attempt to write to such a variable will simply create a \emph{new}
.. % % local variable in the innermost scope, leaving the identically named
.. % % outer variable unchanged).

通常、ローカルスコープは (プログラムテキスト上の) 現在の関数の ローカルな名前を参照します。関数の外側では、ローカルスコープは
グローバルな名前空間と同じ名前空間: モジュールの名前空間を参照します。 クラスを定義すると、ローカルスコープの中にもう一つ名前空間が置かれ ます。

.. % % Usually, the local scope references the local names of the (textually)
.. % % current function.  Outside functions, the local scope references
.. % % the same namespace as the global scope: the module's namespace.
.. % % Class definitions place yet another namespace in the local scope.

スコープはテキスト上で決定されていると理解することが重要です: モジュール内で定義される関数のグローバルなスコープは、
関数がどこから呼び出されても、どんな別名をつけて呼び出されても、 そのモジュールの名前空間になります。反対に、実際の名前の検索は 実行時に動的に行われます
--- とはいえ、言語の定義は、"コンパイル"  時の静的な名前解決の方向に進化しているので、 動的な名前解決に頼ってはいけません！
(事実、ローカルな変数は既に 静的に決定されています。)

.. % % It is important to realize that scopes are determined textually: the
.. % % global scope of a function defined in a module is that module's
.. % % namespace, no matter from where or by what alias the function is
.. % % called.  On the other hand, the actual search for names is done
.. % % dynamically, at run time --- however, the language definition is
.. % % evolving towards static name resolution, at ``compile'' time, so don't
.. % % rely on dynamic name resolution!  (In fact, local variables are
.. % % already determined statically.)

Python 特有の癖として、代入を行うと -- どの :keyword:`global` 文も有効でない場合は -- 名前がいつも最も内側のスコープに 入るというものがあります。代入はデータのコピーを行いません ---
単に名前をオブジェクトに結びつける (bind) だけです。オブジェクトの削除 でも同じです: ``del x`` は、``x``
をローカルスコープが参照している 名前空間から削除します。実際、新たな名前を導入する操作は全てローカル スコープを用います: とりわけ、 import
文や関数定義は、モジュールや 関数の名前をローカルスコープに結び付けます。(:keyword:`global` 文を使えば、
特定の変数がグローバルスコープにあることを示せます。)

.. % % A special quirk of Python is that assignments always go into the
.. % % innermost scope.  Assignments do not copy data --- they just
.. % % bind names to objects.  The same is true for deletions: the statement
.. % % \samp{del x} removes the binding of \code{x} from the namespace
.. % % referenced by the local scope.  In fact, all operations that introduce
.. % % new names use the local scope: in particular, import statements and
.. % % function definitions bind the module or function name in the local
.. % % scope.  (The \keyword{global} statement can be used to indicate that
.. % % particular variables live in the global scope.)


.. _tut-firstclasses:

クラス初見
==========

クラスでは、新しい構文を少しと、三つの新たなオブジェクト型、そして 新たな意味付けをいくつか取り入れています。

.. % A First Look at Classes
.. % % Classes introduce a little bit of new syntax, three new object types,
.. % % and some new semantics.


.. _tut-classdefinition:

クラス定義の構文
----------------

クラス定義の最も単純な形式は、以下のようになります:

.. % Class Definition Syntax
.. % % The simplest form of class definition looks like this:

::

   class ClassName:
       <文-1>
       .
       .
       .
       <文-N>

関数定義 (:keyword:`def` 文) と同様、クラス定義が効果をもつには まず実行しなければなりません。 (クラス定義を :keyword:`if`
文の分岐先や関数内部に置くことも、 考え方としてはありえます。)

.. % % Class definitions, like function definitions
.. % % (\keyword{def} statements) must be executed before they have any
.. % % effect.  (You could conceivably place a class definition in a branch
.. % % of an \keyword{if} statement, or inside a function.)

実際には、クラス定義の内側にある文は、通常は関数定義になりますが、 他の文を書くこともでき、それがそれが役に立つこともあります ---
これについては後で述べます。クラス内の関数定義は通常、メソッドの 呼び出し規約で決められた独特の形式の引数リストを持ちます --- これについても後で述べます。

.. % % In practice, the statements inside a class definition will usually be
.. % % function definitions, but other statements are allowed, and sometimes
.. % % useful --- we'll come back to this later.  The function definitions
.. % % inside a class normally have a peculiar form of argument list,
.. % % dictated by the calling conventions for methods --- again, this is
.. % % explained later.

クラス定義に入ると、新たな名前空間が作成され、ローカルな 名前空間として使われます --- 従って、ローカルな変数に対する
全ての代入はこの新たな名前空間に名要ります。特に、関数定義を 行うと、新たな関数の名前はこの名前空間に結び付けられます。

.. % % When a class definition is entered, a new namespace is created, and
.. % % used as the local scope --- thus, all assignments to local variables
.. % % go into this new namespace.  In particular, function definitions bind
.. % % the name of the new function here.

クラス定義から普通に (定義の終端に到達して) 抜けると、 *クラスオブジェクト (class object) * が生成されます。
クラスオブジェクトは、基本的にはクラス定義で作成された名前空間の 内容をくるむラッパ (wrapper) です; クラスオブジェクトについては
次の節で詳しく学ぶことにします。(クラス定義に入る前に有効だった) 元のローカルスコープが復帰し、生成されたクラスオブジェクトは
復帰したローカルスコープにクラス定義のヘッダで指定した名前 (上の例では :class:`ClassName`) で結び付けられます。

.. % % When a class definition is left normally (via the end), a \emph{class
.. % % object} is created.  This is basically a wrapper around the contents
.. % % of the namespace created by the class definition; we'll learn more
.. % % about class objects in the next section.  The original local scope
.. % % (the one in effect just before the class definitions was entered) is
.. % % reinstated, and the class object is bound here to the class name given
.. % % in the class definition header (\class{ClassName} in the example).


.. _tut-classobjects:

クラスオブジェクト
------------------

クラス・オブジェクトでは２種類の演算: 属性参照とインスタンス生成を サポートしています。

.. % Class Objects
.. % % Class objects support two kinds of operations: attribute references
.. % % and instantiation.

*属性参照 (attribute reference)* は、Python におけるすべての 属性参照で使われている標準的な構文、 ``obj.name``
を使います。 クラスオブジェクトが生成された際にクラスの名前空間にあった名前すべてが 有効な属性名です。従って、以下のようなクラス定義:

.. % % \emph{Attribute references} use the standard syntax used for all
.. % % attribute references in Python: \code{obj.name}.  Valid attribute
.. % % names are all the names that were in the class's namespace when the
.. % % class object was created.  So, if the class definition looked like
.. % % this:

::

   class MyClass:
       """A simple example class"""
       i = 12345
       def f(self):
           return 'hello world'

では、``MyClass.i`` と ``MyClass.f`` は妥当な属性参照であり、 それぞれ整数と関数オブジェクトを返します。
クラス属性に代入を行うこともできます。従って、``MyClass.i`` の値を 代入して変更できます。 ``__doc__``
も有効な属性で、そのクラスに属している docstring、 この場合は ``"A simple example class"`` を返します。

.. % % then \code{MyClass.i} and \code{MyClass.f} are valid attribute
.. % % references, returning an integer and a method object, respectively.
.. % % Class attributes can also be assigned to, so you can change the value
.. % % of \code{MyClass.i} by assignment.  \member{__doc__} is also a valid
.. % % attribute, returning the docstring belonging to the class: \code{"A
.. % % simple example class"}).

クラスの *インスタンス生成 (instantiation)* には関数のような 表記法を使います。クラスオブジェクトのことを、単にクラスの新しい
インスタンスを返すパラメタを持たない関数かのように扱います。 例えば (上記のクラスでいえば):

.. % % Class \emph{instantiation} uses function notation.  Just pretend that
.. % % the class object is a parameterless function that returns a new
.. % % instance of the class.  For example (assuming the above class):

::

   x = MyClass()

は、クラスの新しい*インスタンス (instance)* を生成し、 そのオブジェクトをローカル変数 ``x`` へ代入します。

.. % % creates a new \emph{instance} of the class and assigns this object to
.. % % the local variable \code{x}.

インスタンス生成操作 (クラスオブジェクトの "呼出し") を行うと、 空のオブジェクト (empty object) を生成します。多くのクラスは、
オブジェクトを作成する際に、カスタマイズされた特定の初期状態に なってほしいと望んで います。従って、クラスでは :meth:`__init__`
という名前の特別な メソッド定義することができます。例えば以下のようにします:

.. % % The instantiation operation (``calling'' a class object) creates an
.. % % empty object.  Many classes like to create objects with instances
.. % % customized to a specific initial state.
.. % % Therefore a class may define a special method named
.. % % \method{__init__()}, like this:

::

   def __init__(self):
       self.data = []

クラスが :meth:`__init__` メソッドを定義している場合、 クラスのインスタンスを生成すると、新しく生成された クラスインスタンスに対して自動的に
:meth:`__init__` を呼び出します。 従って、この例では、新たな初期済みのインスタンスを以下のように して得ることができます:

.. % % When a class defines an \method{__init__()} method, class
.. % % instantiation automatically invokes \method{__init__()} for the
.. % % newly-created class instance.  So in this example, a new, initialized
.. % % instance can be obtained by:

::

   x = MyClass()

もちろん、より大きな柔軟性を持たせるために、:meth:`__init__`  メソッドに複数の引数をもたせることができます。
その場合、クラスのインスタンス生成操作に渡された引数は :meth:`__init__` に渡されます。例えば以下のように:

.. % % Of course, the \method{__init__()} method may have arguments for
.. % % greater flexibility.  In that case, arguments given to the class
.. % % instantiation operator are passed on to \method{__init__()}.  For
.. % % example,

::

   >>> class Complex:
   ...     def __init__(self, realpart, imagpart):
   ...         self.r = realpart
   ...         self.i = imagpart
   ...
   >>> x = Complex(3.0, -4.5)
   >>> x.r, x.i
   (3.0, -4.5)


.. _tut-instanceobjects:

インスタンスオブジェクト
------------------------

ところで、インスタンスオブジェクトを使うと何ができるのでしょうか？ インスタンスオブジェクトが理解できる唯一の操作は、属性の参照です。
有効な属性の名前には二種類(データ属性およびメソッド)あります。

.. % Instance Objects
.. % % Now what can we do with instance objects?  The only operations
.. % % understood by instance objects are attribute references.  There are
.. % % two kinds of valid attribute names, data attributes and methods.

*データ属性 (data attribute)* は、これは Smalltalk の "インスタンス変数" (instance variable) や C++の
"データメンバ" (data member) に相当します。 データ属性を宣言する必要はありません; ローカルな変数と同様に、
これらの属性は最初に代入された時点で湧き出てきます。例えば、 上で生成した :class:`MyClass` のインスタンス ``x`` に対して、
以下のコード断片を実行すると、値 ``16`` を印字し、``x`` の 痕跡は残りません。

.. % % \emph{data attributes} correspond to
.. % % ``instance variables'' in Smalltalk, and to ``data members'' in
.. % % \Cpp.  Data attributes need not be declared; like local variables,
.. % % they spring into existence when they are first assigned to.  For
.. % % example, if \code{x} is the instance of \class{MyClass} created above,
.. % % the following piece of code will print the value \code{16}, without
.. % % leaving a trace:

::

   x.counter = 1
   while x.counter < 10:
       x.counter = x.counter * 2
   print x.counter
   del x.counter

もうひとつのインスタンス属性は *メソッド (method)* です。メソッドとは、オブジェクトに "属している"  関数のことです。(Python
では、メソッドという用語はクラスインスタンス だけのものではありません: オブジェクト型にもメソッドを持つことができます。 例えば、リストオブジェクトには、
append, insert, remove, sort などといった メソッドがあります。とはいえ、以下では特に明記しない限り、クラスの
インスタンスオブジェクトのメソッドだけを意味するものとして使うことに します。)

.. % % The other kind of instance attribute reference is a \emph{method}.
.. % % A method is a function that ``belongs to'' an
.. % % object.  (In Python, the term method is not unique to class instances:
.. % % other object types can have methods as well.  For example, list objects have
.. % % methods called append, insert, remove, sort, and so on.  However,
.. % % in the following discussion, we'll use the term method exclusively to mean
.. % % methods of class instance objects, unless explicitly stated otherwise.)

.. index:: object: method

インスタンスオブジェクトで有効なメソッド名は、そのクラスによります。 定義により、クラスの全てのo関数オブジェクトである属性が
インスタンスオブジェクトの妥当なメソッド名に決まります。 従って、例では、 ``MyClass.f`` は関数なので、 ``x.f``
はメソッドの参照として有効です。 しかし、``MyClass.i`` は関数ではないので、 ``x.i`` はメソッドの参照
として有効ではありません。``x.f`` は ``MyClass.f`` と同じものでは ありません --- 関数オブジェクトではなく、 *メソッドオブジェクト
(method object)* です。

.. % % Valid method names of an instance object depend on its class.  By
.. % % definition, all attributes of a class that are function
.. % % objects define corresponding methods of its instances.  So in our
.. % % example, \code{x.f} is a valid method reference, since
.. % % \code{MyClass.f} is a function, but \code{x.i} is not, since
.. % % \code{MyClass.i} is not.  But \code{x.f} is not the same thing as
.. % % \code{MyClass.f} --- it is a \obindex{method}\emph{method object}, not
.. % % a function object.


.. _tut-methodobjects:

メソッドオブジェクト
--------------------

普通、メソッドはバインドされた直後に呼び出されます:

.. % Method Objects
.. % % Usually, a method is called right after it is bound:

::

   x.f()

:class:`MyClass`の例では、上のコードは文字列 ``'hello world'`` を返すでしょう。
しかしながら、必ずしもメソッドをその場で呼び出さなければならない わけではありません: ``x.f`` はメソッドオブジェクトであり、
どこかに記憶しておいて後で呼び出すことができます。例えば以下のコード:

.. % % In the \class{MyClass} example, this will return the string \code{'hello world'}.
.. % % However, it is not necessary to call a method right away:
.. % % \code{x.f} is a method object, and can be stored away and called at a
.. % % later time.  For example:

::

   xf = x.f
   while True:
       print xf()

は、 ``hello world`` を時が終わるまで印字し続けるでしょう。

.. % % will continue to print \samp{hello world} until the end of time.

メソッドが呼び出されるときには実際には何が起きているのでしょうか？ :meth:`f` の関数定義では引数を一つ指定していたにもかかわらず、 上記では
``x.f`` が引数なしで呼び出されたことに気付いているかも しれませんね。引数はどうなったのでしょうか？ たしか、引数が必要な関数を
引数無しで呼び出すと、Python が例外を送出するはずです --- たとえその 引数が実際には使われなくても…。

.. % % What exactly happens when a method is called?  You may have noticed
.. % % that \code{x.f()} was called without an argument above, even though
.. % % the function definition for \method{f} specified an argument.  What
.. % % happened to the argument?  Surely Python raises an exception when a
.. % % function that requires an argument is called without any --- even if
.. % % the argument isn't actually used...

実際、もう答は想像できているかもしれませんね: メソッドについて 特別なこととして、オブジェクトが関数の第 1 引数として渡される、
ということがあります。我々の例では、``x.f()`` という呼び出しは、 ``MyClass.f(x)`` と厳密に等価なものです。 一般に、*n*
個の引数リストもったメソッドの呼出しは、 そのメソッドのオブジェクトを最初の引数の前に挿入した引数リストで メソッドに対応する関数を呼び出すことと等価です。

.. % % Actually, you may have guessed the answer: the special thing about
.. % % methods is that the object is passed as the first argument of the
.. % % function.  In our example, the call \code{x.f()} is exactly equivalent
.. % % to \code{MyClass.f(x)}.  In general, calling a method with a list of
.. % % \var{n} arguments is equivalent to calling the corresponding function
.. % % with an argument list that is created by inserting the method's object
.. % % before the first argument.

もしもまだメソッドの働きかたを理解できなければ、一度実装を見てみると事情がよく分かるかもしれません。
データ属性ではないインスタンス属性が参照された時は、そのクラスが検索されます。
その名前が有効なクラス属性を表している関数オブジェクトなら、インスタンスオブジェクトと見つかった関数オブジェクト (へのポインタ)
を抽象オブジェクト: すなわちメソッド オブジェクトにパック (pack) して作成します。
メソッドオブジェクトは、引数リストを伴って呼び出される際に再度\
アンパック (unpack) され、新たな引数リストがインスタンスオブジェクト\
とオリジナルの引数リストから構成され、関数オブジェクトは新たな引数\
リストを使って呼び出されます。

.. % % If you still don't understand how methods work, a look at the
.. % % implementation can perhaps clarify matters.  When an instance
.. % % attribute is referenced that isn't a data attribute, its class is
.. % % searched.  If the name denotes a valid class attribute that is a
.. % % function object, a method object is created by packing (pointers to)
.. % % the instance object and the function object just found together in an
.. % % abstract object: this is the method object.  When the method object is
.. % % called with an argument list, it is unpacked again, a new argument
.. % % list is constructed from the instance object and the original argument
.. % % list, and the function object is called with this new argument list.


.. _tut-remarks:

いろいろな注意点
================

.. % Random Remarks
.. % % [These should perhaps be placed more carefully...]
.. これらはおそらくもっと注意深く配置すべきだろう…

データ属性は同じ名前のメソッド属性を上書きしてしまいます; 大規模なプログラムでみつけにくいバグを引き起こすことがある
この偶然的な名前の衝突を避けるには、衝突の可能性を最小限にするような 規約を使うのが賢明です。
可能な規約としては、メソッド名を大文字で始める、データ属性名の先頭に 短い一意的な文字列 (あるいはただの下線) をつける、またメソッドには動詞、
データ属性には名詞を用いる、などがあります。

.. % % Data attributes override method attributes with the same name; to
.. % % avoid accidental name conflicts, which may cause hard-to-find bugs in
.. % % large programs, it is wise to use some kind of convention that
.. % % minimizes the chance of conflicts.  Possible conventions include
.. % % capitalizing method names, prefixing data attribute names with a small
.. % % unique string (perhaps just an underscore), or using verbs for methods
.. % % and nouns for data attributes.

データ属性は、メソッドから参照できると同時に、通常のオブジェクトの ユーザ ("クライアント") からも参照できます。言い換えると、
クラスは純粋な抽象データ型として使うことができません。実際、 Python では、データ隠蔽を補強するための機構はなにもありません ---
データの隠蔽はすべて規約に基づいています。(逆に、C 言語で書かれた Python の実装では実装の詳細を完全に隠蔽し、必要に応じてオブジェクト
へのアクセスを制御できます; この機構は C 言語で書かれた Python 拡張 で使うことができます)

.. % % Data attributes may be referenced by methods as well as by ordinary
.. % % users (``clients'') of an object.  In other words, classes are not
.. % % usable to implement pure abstract data types.  In fact, nothing in
.. % % Python makes it possible to enforce data hiding --- it is all based
.. % % upon convention.  (On the other hand, the Python implementation,
.. % % written in C, can completely hide implementation details and control
.. % % access to an object if necessary; this can be used by extensions to
.. % % Python written in C.)

クライアントはデータ属性を注意深く扱うべきです --- クライアントは、 メソッドを使うことで維持しているデータ属性の不変式を踏みにじり、
台無しにするかもしれません。 クライアントは、名前の衝突が回避されている限り、メソッドの有効性に
影響を及ぼすことなくインスタンスに独自の属性を追加することができる、 ということに注意してください --- ここでも、名前付けの規約は
頭痛の種を無くしてくれます。

.. % % Clients should use data attributes with care --- clients may mess up
.. % % invariants maintained by the methods by stamping on their data
.. % % attributes.  Note that clients may add data attributes of their own to
.. % % an instance object without affecting the validity of the methods, as
.. % % long as name conflicts are avoided --- again, a naming convention can
.. % % save a lot of headaches here.

データ属性を (またはその他のメソッドも！) メソッドの中で参照するための 短縮された記法はありません。私は、この仕様が実際にメソッドの
可読性を高めていると考えています: あるメソッドを眺めているときに ローカルな変数とインスタンス変数を混同する可能性はまったくありません。

.. % % There is no shorthand for referencing data attributes (or other
.. % % methods!) from within methods.  I find that this actually increases
.. % % the readability of methods: there is no chance of confusing local
.. % % variables and instance variables when glancing through a method.

しばしば、メソッドの最初の引数を、しばしば ``self`` と呼びます。 この名前付けは単なる慣行でしかありません: ``self`` という名前は、
Python では何ら特殊な意味を持ちません。 (とはいえ、この慣行に従わないと、 コードは他の Python プログラマにとってやや読みにくいものとなります。
また、 *クラスブラウザ (class browser)* プログラムがこの慣行を あてにして書かれているかもしれません。)

.. % % Often, the first argument of a method is called
.. % % \code{self}.  This is nothing more than a convention: the name
.. % % \code{self} has absolutely no special meaning to Python.  (Note,
.. % % however, that by not following the convention your code may be less
.. % % readable to other Python programmers, and it is also conceivable that
.. % % a \emph{class browser} program might be written that relies upon such a
.. % % convention.)

クラス属性である関数オブジェクトはいずれも、そのクラスのインスタンス のためのメソッドを定義しています。関数定義は、テキスト上では
クラス定義の中に入っていなければならないわけではありません: 関数オブジェクトをクラスのローカルな変数の中に代入するのも OK です。
例えば以下のコードのようにします:

.. % % Any function object that is a class attribute defines a method for
.. % % instances of that class.  It is not necessary that the function
.. % % definition is textually enclosed in the class definition: assigning a
.. % % function object to a local variable in the class is also ok.  For
.. % % example:

::

   # クラスの外側で定義された関数
   def f1(self, x, y):
       return min(x, x+y)

   class C:
       f = f1
       def g(self):
           return 'hello world'
       h = g

これで、``f``、 ``g`` 、および ``h`` は、すべて :class:`C` の属性であり関数オブジェクトを参照しています。
従って、これら全ては、:class:`C` のインスタンスのメソッドとなります ---  ``h`` は ``g`` と全く等価です。これを実践しても、大抵は
単にプログラムの読者に混乱をもたらすだけなので注意してください。

.. % % Now \code{f}, \code{g} and \code{h} are all attributes of class
.. % % \class{C} that refer to function objects, and consequently they are all
.. % % methods of instances of \class{C} --- \code{h} being exactly equivalent
.. % % to \code{g}.  Note that this practice usually only serves to confuse
.. % % the reader of a program.

メソッドは、``self`` 引数のメソッド属性を使って、 他のメソッドを呼び出すことができます:

.. % % Methods may call other methods by using method attributes of the
.. % % \code{self} argument:

::

   class Bag:
       def __init__(self):
           self.data = []
       def add(self, x):
           self.data.append(x)
       def addtwice(self, x):
           self.add(x)
           self.add(x)

メソッドは、通常の関数と同じようにして、グローバルな名前を参照しても かまいません。あるメソッドに関連付けられたグローバルなスコープは、
クラス定義の入っているモジュールになります。 (クラス自体はグローバルな スコープとして用いられることはありません！) メソッドでグローバルな
データを使う良い理由はほとんどありませんが、グローバルなスコープを 使う合法的な使い方は多々あります: 一つ挙げると、メソッド内では、 グローバルなスコープに
import された関数やモジュールや、 その中で定義された関数やクラスを使うことができます。 通常、メソッドの入っているクラス自体はグローバルなスコープ内で
定義されています。次の章では、メソッドが自分のクラスを参照する理由 として正当なものを見てみましょう！

.. % % Methods may reference global names in the same way as ordinary
.. % % functions.  The global scope associated with a method is the module
.. % % containing the class definition.  (The class itself is never used as a
.. % % global scope!)  While one rarely encounters a good reason for using
.. % % global data in a method, there are many legitimate uses of the global
.. % % scope: for one thing, functions and modules imported into the global
.. % % scope can be used by methods, as well as functions and classes defined
.. % % in it.  Usually, the class containing the method is itself defined in
.. % % this global scope, and in the next section we'll find some good
.. % % reasons why a method would want to reference its own class!

個々の値はオブジェクトなので、 *クラス* (*型* とも言います) を持っています。
それは ``object.__class__`` に保持されています。

.. _tut-inheritance:

継承
====

言うまでもなく、継承の概念をサポートしない言語機能は "クラス" と呼ぶに 値しません。導出クラス (derived class) を定義する構文は以下のように
なります:

.. % Inheritance
.. % % Of course, a language feature would not be worthy of the name ``class''
.. % % without supporting inheritance.  The syntax for a derived class
.. % % definition looks like this:

::

   class DerivedClassName(BaseClassName):
       <文-1>
       .
       .
       .
       <文-N>

基底クラス (base class) の名前 :class:`BaseClassName` は、
導出クラス定義の入っているスコープで定義されていなければなりません。 基底クラス名のかわりに任意の式を入れることもできます。 これは以下のように、

.. % % The name \class{BaseClassName} must be defined in a scope containing
.. % % the derived class definition.  In place of a base class name, other
.. % % arbitrary expression is also allowed.  This can be useful, for
.. % % example, when the base class is defined in another module:

::

   class DerivedClassName(modname.BaseClassName):

基底クラスが別モジュールで定義されているときに便利なことがあります。

導出クラス定義の実行は、基底クラスの場合と同じように進められます。 クラスオブジェクトが構築される時、基底クラスが記憶されます。
記憶された基底クラスは、属性参照を解決するために使われます: 要求された属性がクラスに見つからなかった場合、基底クラスに検索
が進みます。この規則は、基底クラスが他の何らかのクラスから導出された ものであった場合、再帰的に適用されます。

.. % % Execution of a derived class definition proceeds the same as for a
.. % % base class.  When the class object is constructed, the base class is
.. % % remembered.  This is used for resolving attribute references: if a
.. % % requested attribute is not found in the class, search proceeds to look in the
.. % % base class.  This rule is applied recursively if the base class itself
.. % % is derived from some other class.

導出クラスのインスタンス化では、特別なことは何もありません: ``DerivedClassName()`` はクラスの新たなインスタンスを生成します。
メソッドの参照は以下のようにしてい解決されます: まず対応するクラス属性 が検索されます。検索は、必要に応じ、基底クラス連鎖を下って行われ、
検索の結果として何らかの関数オブジェクトがもたらされた場合、 メソッド参照は有効なものとなります。

.. % % There's nothing special about instantiation of derived classes:
.. % % \code{DerivedClassName()} creates a new instance of the class.  Method
.. % % references are resolved as follows: the corresponding class attribute
.. % % is searched, descending down the chain of base classes if necessary,
.. % % and the method reference is valid if this yields a function object.

導出クラスは基底クラスのメソッドを上書き (override) してもかまいません。 メソッドは同じオブジェクトの別のメソッドを呼び出す際に何ら特殊な権限を
持ちません。このため、ある基底クラスのメソッドが、同じ基底クラスで 定義されているもう一つのメソッド呼び出しを行っている場合、
導出クラスで上書きされた何らかのメソッドが呼び出されることになる かもしれません。 (C++ プログラマへ:  Python では、すべてのメソッドは 事実上
``virtual`` です。)

.. % % Derived classes may override methods of their base classes.  Because
.. % % methods have no special privileges when calling other methods of the
.. % % same object, a method of a base class that calls another method
.. % % defined in the same base class may end up calling a method of
.. % % a derived class that overrides it.  (For \Cpp{} programmers: all methods
.. % % in Python are effectively \keyword{virtual}.)

導出クラスで上書きしているメソッドでは、実際は単に基底クラスの 同名のメソッドを置き換えるだけではなく、拡張を行いたいかもしれません。
基底クラスのメソッドを直接呼び出す簡単な方法があります: 単に ``BaseClassName.methodname(self, arguments)``
を呼び出すだけです。 この仕様は、場合によってはクライアントでも役に立ちます。 (この呼び出し方が動作するのは、基底クラスがグローバルなスコープ内で
定義されているか、直接 import されている場合だけなので注意してください。)

.. % % An overriding method in a derived class may in fact want to extend
.. % % rather than simply replace the base class method of the same name.
.. % % There is a simple way to call the base class method directly: just
.. % % call \samp{BaseClassName.methodname(self, arguments)}.  This is
.. % % occasionally useful to clients as well.  (Note that this only works if
.. % % the base class is defined or imported directly in the global scope.)

Python には継承に関係する 2 つの組み込み関数があります:

* :func:`isinstance` を使うとオブジェクトの型が調べられます: ``isinstance(obj, int)`` は ``obj.__class__`` が :class:`int` や :class:`int` の導出クラスの場合に限り ``True`` になります。

* :func:`issubclass` を使うとクラスの継承関係が調べられます: :class:`bool` は :class:`int` のサブクラスなので ``issubclass(bool, int)`` は ``True`` です。しかし、 :class:`unicode` は :class:`str` のサブクラスではない (単に共通の祖先 :class:`basestring` を共有している) ので ``issubclass(unicode, str)`` は ``False`` です。

.. _tut-multiple:

多重継承
--------

Python では、限られた形式の多重継承 (multiple inheritance) も サポートしています。複数の基底クラスをもつクラス定義は以下のように
なります:

.. % Multiple Inheritance
.. % % Python supports a limited form of multiple inheritance as well.  A
.. % % class definition with multiple base classes looks like this:

::

   class DerivedClassName(Base1, Base2, Base3):
       <文-1>
       .
       .
       .
       <文-N>

旧形式のクラスでは、
解決規則は深さ優先 (depth-first)、左から右へ (left-to-right) だけです。従って、ある属性が
:class:`DerivedClassName` で 見つからなければ :class:`Base1` で検索され、次に :class:`Base1` の
基底クラスで (再帰的に) 検索されます。それでも見つからなければ はじめて :class:`Base2` で検索される、といった具合です。

.. % % The only rule necessary to explain the semantics is the resolution
.. % % rule used for class attribute references.  This is depth-first,
.. % % left-to-right.  Thus, if an attribute is not found in
.. % % \class{DerivedClassName}, it is searched in \class{Base1}, then
.. % % (recursively) in the base classes of \class{Base1}, and only if it is
.. % % not found there, it is searched in \class{Base2}, and so on.

(人によっては、幅優先 (breadth first) --- :class:`Base2` と  :class:`Base3` を検索してから
:class:`Base1` の基底クラスで検索する ---  のほうが自然のように見えます。しかしながら、幅優先の検索では、 :class:`Base1`
の特定の属性のうち、実際に定義されているのが :class:`Base1` なのか、その基底クラスなのかを知らなければ、 :class:`Base2`
の属性との名前衝突がどんな結果をもたらすのか 分からないことになります。深さ優先規則では、 :class:`Base1` の直接の
属性と継承された属性とを区別しません。)

.. % % (To some people breadth first --- searching \class{Base2} and
.. % % \class{Base3} before the base classes of \class{Base1} --- looks more
.. % % natural.  However, this would require you to know whether a particular
.. % % attribute of \class{Base1} is actually defined in \class{Base1} or in
.. % % one of its base classes before you can figure out the consequences of
.. % % a name conflict with an attribute of \class{Base2}.  The depth-first
.. % % rule makes no differences between direct and inherited attributes of
.. % % \class{Base1}.)

.. % Python では偶然的な名前の衝突を慣習に頼って回避しているので、 見境なく多重継承の使用すると、メンテナンスの悪夢に陥ることは明らかです。
.. % 多重継承に関するよく知られた問題は、二つのクラスから導出された クラスがたまたま共通の基底クラスを持つ場合です。
.. % この場合になにが起こるかを結論することは簡単です (インスタンスは 共通の基底クラスで使われている "インスタンス変数" の単一の コピーを持つことになります)
.. % が、この意味付けが何の役に立つのかは 明らかではありません。

.. % % It is clear that indiscriminate use of multiple inheritance is a
.. % % maintenance nightmare, given the reliance in Python on conventions to
.. % % avoid accidental name conflicts.  A well-known problem with multiple
.. % % inheritance is a class derived from two classes that happen to have a
.. % % common base class.  While it is easy enough to figure out what happens
.. % % in this case (the instance will have a single copy of ``instance
.. % % variables'' or data attributes used by the common base class), it is
.. % % not clear that these semantics are in any way useful.

.. % % XXX Add rules for new-style MRO?

.. glossary

:term:`new-style class` では、 :func:`super` が適切に呼び出せるようにするためにメソッドの解決順序は動的に変わります。
このアプローチは他の多重継承のある言語で call-next-method として知られており、単一継承しかない言語の super 呼び出しよりも強力です。

新形式のクラスについて、多重継承の全ての場合に 1 つかそれ以上のダイヤモンド継承 (少なくとも 1 つの祖先クラスに対し最も下のクラスから到達する経路が複数ある状態) があるので動的順序付けが必要です。
例えば、全ての新形式のクラスは :class:`object` を継承しているので、どの多重継承でも :class:`object` へ到達するための道は複数存在します。
基底クラスが複数回アクセスされないようにするために、動的アルゴリズムで検索順序を直列化し、各クラスで指定されている祖先クラスどうしの左から右への順序は崩さず、各祖先クラスを一度だけ呼び出し、かつ一様になる (つまり祖先クラスの順序に影響を与えずにサブクラス化できる) ようにします。
まとめると、これらの特徴のおかげで信頼性と拡張性のある多重継承したクラスを設計することができるのです。
さらに詳細を知りたければ、 http://www.python.org/download/releases/2.3/mro/ を見てください。


.. _tut-private:

プライベート変数
================

クラスプライベート (class-private) の識別子に関して限定的なサポート がなされています。``__spam`` (先頭に二個以上の下線文字、末尾に
高々一個の下線文字) という形式の識別子、テキスト上では ``_classname__spam`` へと置換されるようになりました。 ここで
``classname`` は、現在のクラス名から先頭の下線文字を はぎとった名前になります。このような難号化 (mangle) は、識別子の
文法的な位置にかかわらず行われるので、クラスプライベートな インスタンス変数やクラス変数、メソッド、グローバル変数、そしてインスタ ンスに含まれる変数を
定義するために利用できます。また、このクラスにとってプライベートな インスタンス変数を *他の* クラスのインスタンスに格納するために
使うことさえできます。難号化した名前が 255 文字より長くなるときは、 切り詰めが起こるかもしれません。
クラスの外側や、クラス名が下線文字だけからできているときには、 難号化加工は起こりません。

.. % Private Variables
.. % % There is limited support for class-private
.. % % identifiers.  Any identifier of the form \code{__spam} (at least two
.. % % leading underscores, at most one trailing underscore) is now textually
.. % % replaced with \code{_classname__spam}, where \code{classname} is the
.. % % current class name with leading underscore(s) stripped.  This mangling
.. % % is done without regard to the syntactic position of the identifier, so
.. % % it can be used to define class-private instance and class variables,
.. % % methods, variables stored in globals, and even variables stored in instances.
.. % % private to this class on instances of \emph{other} classes.  Truncation
.. % % may occur when the mangled name would be longer than 255 characters.
.. % % Outside classes, or when the class name consists of only underscores,
.. % % no mangling occurs.

名前の難号化は、クラスにおいて、 "プライベートな" インスタンス変数や メソッドを定義する際に、導出クラスで定義されるインスタンス変数を気に
したり、クラスの外側のコードからインスタンス変数をいじりまわすことが ないように簡単に定義できるようにするためのものです。
難号化の規則は主に不慮の事故を防ぐためのものだということに注意して ください; 確信犯的な方法で、プライベートとされている変数にアクセス
したり変更することは依然として可能なのです。デバッガのような特殊な 状況では、この仕様は便利ですらあります。そのため、この抜け穴は 塞がれていません。
(些細なバグ: 基底クラスと同じ名前のクラスを導出すると、基底クラスの プライベート変数を使えるようになります。)

.. % % Name mangling is intended to give classes an easy way to define
.. % % ``private'' instance variables and methods, without having to worry
.. % % about instance variables defined by derived classes, or mucking with
.. % % instance variables by code outside the class.  Note that the mangling
.. % % rules are designed mostly to avoid accidents; it still is possible for
.. % % a determined soul to access or modify a variable that is considered
.. % % private.  This can even be useful in special circumstances, such as in
.. % % the debugger, and that's one reason why this loophole is not closed.
.. % % (Buglet: derivation of a class with the same name as the base class
.. % % makes use of private variables of the base class possible.)

``exec`` や ``eval()`` や ``execfile()`` へ渡されたコードでは、
呼出し元のクラス名を現在のクラスと見なさないことに注意してください; この仕様は ``global`` 文の効果と似ており、その効果もまた同様に、
バイトコンパイルされたコードに制限されています。 同じ制約が ``getattr()`` と ``setattr()`` と ``delattr()``
にも適用されます。また、``__dict__`` を直接参照するときにも適用されます。

.. % % Notice that code passed to \code{exec}, \code{eval()} or
.. % % \code{execfile()} does not consider the classname of the invoking
.. % % class to be the current class; this is similar to the effect of the
.. % % \code{global} statement, the effect of which is likewise restricted to
.. % % code that is byte-compiled together.  The same restriction applies to
.. % % \code{getattr()}, \code{setattr()} and \code{delattr()}, as well as
.. % % when referencing \code{__dict__} directly.


.. _tut-odds:

残りのはしばし
==============

Pascal の "レコード (record)" や、C 言語の "構造体 (struct)" のような、名前つきのデータ要素を一まとめにするデータ型があると
便利なことがたまにあります。空のクラス定義を使うとうまくできます:

.. % Odds and Ends
.. % % Sometimes it is useful to have a data type similar to the Pascal
.. % % ``record'' or C ``struct'', bundling together a few of named data
.. % % items.  An empty class definition will do nicely:

::

   class Employee:
       pass

   john = Employee() # 空の従業員レコードを造る

   # Fill the fields of the record
   john.name = 'John Doe'
   john.dept = 'computer lab'
   john.salary = 1000

ある特定の抽象データ型を要求する Python コードの断片には、 そのデータ型のメソッドをエミュレーションするクラスを代わりに渡す
ことができます。例えば、ファイルオブジェクトから何らかのデータを書式化 する関数がある場合、:meth:`read` と :meth:`readline`
を持つクラス を定義して、ファイルではなく文字列バッファからデータを書式するように しておき、引数として渡すことができます。
(残念なことに、このテクニックには限界があります: クラスにはシーケンスの添字アクセスや算術演算などの特殊構文でアクセスされる操作が定義できず、"疑似ファイル" を sys.stdin に代入してもそこからインタープリタに入力データを読み込ませることはできません。)

.. % % A piece of Python code that expects a particular abstract data type
.. % % can often be passed a class that emulates the methods of that data
.. % % type instead.  For instance, if you have a function that formats some
.. % % data from a file object, you can define a class with methods
.. % % \method{read()} and \method{readline()} that gets the data from a string
.. % % buffer instead, and pass it as an argument.
.. % (Unfortunately, this
.. % technique has its limitations: a class can't define operations that
.. % are accessed by special syntax such as sequence subscripting or
.. % arithmetic operators, and assigning such a ``pseudo-file'' to
.. % \code{sys.stdin} will not cause the interpreter to read further input
.. % from it.)

インスタンスメソッドオブジェクトにもまた、属性があります:  ``m.im_self`` はメソッド:meth:`m`の属しているインスタンスオブジェクトで、
``m.im_func`` はメソッドに対応する関数オブジェクトです。

.. % % Instance method objects have attributes, too: \code{m.im_self} is the
.. % % instance object with the method \method{m}, and \code{m.im_func} is the
.. % % function object corresponding to the method.


.. _tut-exceptionclasses:

例外はクラスであってもよい
--------------------------

ユーザ定義の例外をクラスとして識別することもできます。このメカニズムを 使って、拡張可能な階層化された例外を作成することができます。

.. % Exceptions Can Be Classes
.. % % User-defined exceptions are identified by classes as well.  Using this
.. % % mechanism it is possible to create extensible hierarchies of exceptions.

新しく二つの (意味付け的な) 形式の raise 文ができました:

.. % % There are two new valid (semantic) forms for the raise statement:

::

   raise Class, instance

   raise instance

第一の形式では、``instance`` は :class:`Class` またはその導出クラスの インスタンスでなければなりません。 第二の形式は以下の表記:

.. % % In the first form, \code{instance} must be an instance of
.. % % \class{Class} or of a class derived from it.  The second form is a
.. % % shorthand for:

::

   raise instance.__class__, instance

の短縮された記法です。

except 節には、文字列オブジェクトだけでなくクラスを並べることができます。 except 節のクラスは、同じクラスか基底クラスの例外のときに互換
(compatible) となります (逆方向では成り立ちません --- 導出クラスの例外がリストされている  except
節は基底クラスの例外と互換ではありません)。 例えば、次のコードは、 B, C, D を順序通りに出力します:

.. % % An except clause may list classes as well as string objects.  A class
.. % % in an except clause is compatible with an exception if it is the same
.. % % class or a base class thereof (but not the other way around --- an
.. % % except clause listing a derived class is not compatible with a base
.. % % class).  For example, the following code will print B, C, D in that
.. % % order:

::

   class B:
       pass
   class C(B):
       pass
   class D(C):
       pass

   for c in [B, C, D]:
       try:
           raise c()
       except D:
           print "D"
       except C:
           print "C"
       except B:
           print "B"

except 節が逆に並んでいた場合 (``except B`` が最初にくる場合)、 B, B, B と出力されるはずだったことに注意してください ---
最初に 一致した except 節が駆動されるのです。

.. % % Note that if the except clauses were reversed (with
.. % % \samp{except B} first), it would have printed B, B, B --- the first
.. % % matching except clause is triggered.

処理されないクラスの例外に対してエラーメッセージが出力されるとき、 まずクラス名が出力され、続いてコロン、スペース、最後に組み込み関数 :func:`str`
を使って文字列に変換したインスタンスが出力されます。

.. % % When an error message is printed for an unhandled exception, the
.. % % exception's class name is printed, then a colon and a space, and
.. % % finally the instance converted to a string using the built-in function
.. % % \function{str()}.

.. % % \section{Iterators\label{iterators}}


.. _tut-iterators:

イテレータ (iterator)
=====================

すでに気づいているでしょうが、``for`` 文を使うとほとんどの コンテナオブジェクトにわたってループを行うことができます:

.. % % By now you have probably noticed that most container objects can looped over
.. % % using a \code{for} statement:

::

   for element in [1, 2, 3]:
       print element
   for element in (1, 2, 3):
       print element
   for key in {'one':1, 'two':2}:
       print key
   for char in "123":
       print char
   for line in open("myfile.txt"):
       print line

こうしたアクセス方法は明確で、簡潔で、かつ便利なものです。イテレータの使用は Python
全体に普及していて、統一性をもたらしています。背後では、``for`` 文は コンテナオブジェクトの :func:`iter` を呼び出しています。この関数は
:meth:`next` メソッドの定義されたイテレータオブジェクトを返します。 :meth:`next`
メソッドは一度コンテナ内の要素に一度に一つづつアクセスします。 コンテナ内にアクセスすべき要素がなくなると、:meth:`next` は
:exc:`StopIteration` 例外を送出し、``for`` ループを終了させます。 実際にどのように動作するかを以下の例に示します:

.. % % This style of access is clear, concise, and convenient.  The use of iterators
.. % % pervades and unifies Python.  Behind the scenes, the \code{for} statement calls
.. % % \function{iter()} on the container object.  The function returns an iterator
.. % % object that defines the method \method{next()} which accesses elements in the
.. % % container one at a time.  When there are no more elements, \method{next()}
.. % % raises a \exception{StopIteration} exception which tells the \code{for} loop
.. % % to terminate.  This example shows how it all works:

::

   >>> s = 'abc'
   >>> it = iter(s)
   >>> it
   <iterator object at 0x00A1DB50>
   >>> it.next()
   'a'
   >>> it.next()
   'b'
   >>> it.next()
   'c'
   >>> it.next()

   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
       it.next()
   StopIteration

イテレータプロトコルの背後にあるメカニズムを一度目にすれば、自作のクラスに イテレータとしての振る舞いを追加するのは簡単です。:meth:`__iter__`
メソッド を定義して、:meth:`next` メソッドを持つオブジェクトを返すようにしてください。 クラス自体で :meth:`next`
を定義している場合、:meth:`__iter__` では 単に ``self`` を返すようにできます:

.. % % Having seen the mechanics behind the iterator protocol, it is easy to add
.. % % iterator behavior to your classes.  Define a \method{__iter__()} method
.. % % which returns an object with a \method{next()} method.  If the class defines
.. % % \method{next()}, then \method{__iter__()} can just return \code{self}:

::

   class Reverse:
       "Iterator for looping over a sequence backwards"
       def __init__(self, data):
           self.data = data
           self.index = len(data)
       def __iter__(self):
           return self
       def next(self):
           if self.index == 0:
               raise StopIteration
           self.index = self.index - 1
           return self.data[self.index]

   >>> for char in Reverse('spam'):
   ...     print char
   ...
   m
   a
   p
   s

.. % % \section{Generators\label{generators}}


.. _tut-generators:

ジェネレータ (generator)
========================

:term:`Generator` は、イテレータを作成するための簡潔で強力なツールです。 ジェネレータは通常の関数のように書かれますが、何らかのデータを返すときには
:keyword:`yield` 文を使います。 :meth:`next` が呼び出されるたびに、 ジェネレータは以前に中断した処理を再開します
(ジェネレータは、全てのデータ値と 最後にどの文が実行されたかを記憶しています)。以下の例を見れば、ジェネレータ がとても簡単に作成できることがわかります:

.. % % Generators are a simple and powerful tool for creating iterators.  They are
.. % % written like regular functions but use the \keyword{yield} statement whenever
.. % % they want to return data.  Each time the \method{next()} is called, the
.. % % generator resumes where it left-off (it remembers all the data values and
.. % % which statement was last executed).  An example shows that generators can
.. % % be trivially easy to create:

::

   def reverse(data):
       for index in range(len(data)-1, -1, -1):
           yield data[index]

   >>> for char in reverse('golf'):
   ...     print char
   ...
   f
   l
   o
   g

ジェネレータを使ってできることは、前節で記述したクラスに基づいたイテレータを 使えばできます。ジェネレータを使うとコンパクトに記述できるのは、
:meth:`__iter__` と :meth:`next` メソッドが自動的に作成されるからです。

.. % % Anything that can be done with generators can also be done with class based
.. % % iterators as described in the previous section.  What makes generators so
.. % % compact is that the \method{__iter__()} and \method{next()} methods are
.. % % created automatically.

ジェネレータのもう一つの重要な機能は、呼び出しごとにローカル変数と実行状態が 自動的に保存されるということです。これにより、``self.index`` や
``self.data`` といったインスタンス変数を使ったアプローチよりも簡単に 関数を書くことができるようになります。

.. % % Another key feature is that the local variables and execution state
.. % % are automatically saved between calls.  This made the function easier to write
.. % % and much more clear than an approach using instance variables like
.. % % \code{self.index} and \code{self.data}.

メソッドを自動生成したりプログラムの実行状態を自動保存するほかに、 ジェネレータは終了時に自動的に :exc:`StopIteration` を送出します。
これらの機能を組み合わせると、通常の関数を書くのに比べ、全く苦労する ことなく簡単にイテレータを生成できます。

.. % % In addition to automatic method creation and saving program state, when
.. % % generators terminate, they automatically raise \exception{StopIteration}.
.. % % In combination, these features make it easy to create iterators with no
.. % % more effort than writing a regular function.


.. _tut-genexps:

ジェネレータ式
==============

単純なジェネレータなら、式を使って簡潔にコードする方法があります。 リスト内包に似た構文の式ですが、各括弧ではなく丸括弧を使います。
ジェネレータ式は、関数の中でジェネレータをすぐに使いたいような状況 のために用意されています。ジェネレータ式はコンパクトですが、
完全なジェネレータに比べてちょっと融通の効かないところがあります。 同じ内容を返すリスト内包よりはメモリに優しいことが多いという利点も あります。

.. % Generator Expressions
.. % Some simple generators can be coded succinctly as expressions using a syntax
.. % similar to list comprehensions but with parentheses instead of brackets.  These
.. % expressions are designed for situations where the generator is used right
.. % away by an enclosing function.  Generator expressions are more compact but
.. % less versatile than full generator definitions and tend to be more memory
.. % friendly than equivalent list comprehensions.

例::

   >>> sum(i*i for i in range(10))                 # 平方和を求める
   285

   >>> xvec = [10, 20, 30]
   >>> yvec = [7, 5, 3]
   >>> sum(x*y for x,y in zip(xvec, yvec))         # 内積を求める
   260

   >>> from math import pi, sin
   >>> sine_table = dict((x, sin(x*pi/180)) for x in range(0, 91))

   >>> unique_words = set(word  for line in page  for word in line.split())

   >>> valedictorian = max((student.gpa, student.name) for student in graduates)

   >>> data = 'golf'
   >>> list(data[i] for i in range(len(data)-1,-1,-1))
   ['f', 'l', 'o', 'g']



.. rubric:: Footnotes

.. [#] 例外が一つあります。 モジュールオブジェクトには、秘密の読取り専用の属性 :attr:`__dict__`
   があり、モジュールの名前空間を実装するために使われている辞書を返します; :attr:`__dict__` という名前は属性ですが、グローバルな名前では
   ありません。この属性を利用すると名前空間の実装に対する抽象化を 侵すことになるので、プログラムを検死するデバッガのような用途に限る べきです。

