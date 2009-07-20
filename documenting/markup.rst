.. highlightlang:: rest

.. Additional Markup Constructs
.. ============================

拡張マークアップ構成部 (Additional Markup Constructs)
======================================================

Sphinx は標準の reST マークアップに対して、たくさんのディレクティブと
"interpreted text roles" を拡張しています。
このセクションにはそれらの拡張された構成部のリファレンスがあります。
"標準"の reST 構成部は、 Python ドキュメントで使用されてはいますが、
そのドキュメントはここにはありません。

.. Sphinx adds a lot of new directives and interpreted text roles to standard reST
.. markup.  This section contains the reference material for these facilities.
.. Documentation for "standard" reST constructs is not included here, though
.. they are used in the Python documentation.

.. note::

   これは Sphinx の拡張マークアップの機能の概要です。
   網羅された情報は `Sphinxのドキュメント
   <http://sphinx.pocoo.org/contents.html>` にあります。

.. Meta-information markup
.. -----------------------

メタ情報マークアップ (Meta-information markup)
------------------------------------------------

.. describe:: sectionauthor

   現在のセクションの著者を示します。引数には、(公表されないにしても)公表されても
   良いような名前と、email アドレスを含むべきです。
   アドレスのドメイン名部分は小文字で記述されるべきです。 例::

      .. sectionauthor:: Guido van Rossum <guido@python.org>

   現在のところ、このマークアップは出力には全く利用されていませんが、だれが貢献した
   のかを把握するのに役に立っています。


モジュール用のマークアップ (Module-specific markup)
----------------------------------------------------

この節では、ドキュメント中のモジュールに関する情報を提供するために使われるマークアップに
ついて説明します。各モジュールは各々のファイルでドキュメントされるべきです。
通常このマークアップは、そのファイルのタイトルヘッダの後に使います。典型的な
ファイルは次のように始まります::

   :mod:`parrot` -- Dead parrot access
   ===================================

   .. module:: parrot
      :platform: Unix, Windows
      :synopsis: Analyze and reanimate dead parrots.
   .. moduleauthor:: Eric Cleese <eric@python.invalid>
   .. moduleauthor:: John Idle <john@python.invalid>

..    :mod:`parrot` -- Dead parrot access
..    ===================================
.. 
..    .. module:: parrot
..       :platform: Unix, Windows
..       :synopsis: Analyze and reanimate dead parrots.
..    .. moduleauthor:: Eric Cleese <eric@python.invalid>
..    .. moduleauthor:: John Idle <john@python.invalid>

.. As you can see, the module-specific markup consists of two directives, the
.. ``module`` directive and the ``moduleauthor`` directive.

ごらんの通り、モジュール専用マークアップには、 ``module`` と ``moduleauthor`` 
という二つのディレクティブを持ちます。

.. describe:: module

   このディレクティブはモジュールの説明の始まりを示します。
   （パッケージのサブモジュールの場合は、モジュール名はパッケージ名を含めて全体を
   記述すること）

   ``platform`` オプションは、そのモジュールが利用可能なプラットフォームをカンマで
   区切ったリストです。（全てのプラットフォームで利用可能であるなら、このオプションは
   外すべきです） 要素は短い識別子で、 "IRIX", "Mac", "Windows", "Unix" などが使われ
   ています。できるだけ、すでに使われている識別子を使うようにしてください。

   ``synopsis`` オプションは、モジュールの目的を説明する一文で構成されます。
   これは、現在のところ、 Global Module Index でのみ利用されています。

.. .. describe:: module
.. 
..    This directive marks the beginning of the description of a module (or package
..    submodule, in which case the name should be fully qualified, including the
..    package name).
.. 
..    The ``platform`` option, if present, is a comma-separated list of the
..    platforms on which the module is available (if it is available on all
..    platforms, the option should be omitted).  The keys are short identifiers;
..    examples that are in use include "IRIX", "Mac", "Windows", and "Unix".  It is
..    important to use a key which has already been used when applicable.
.. 
..    The ``synopsis`` option should consist of one sentence describing the
..    module's purpose -- it is currently only used in the Global Module Index.

.. describe:: moduleauthor

   ``moduleauthor`` ディレクティブは、``sectionauthor`` と同じで、作者の名前になります。
   このディレクティブは、作者の人数だけ繰り返して利用できます。
   現在、このディレクティブは出力に利用されていません。

.. .. describe:: moduleauthor
.. 
..    The ``moduleauthor`` directive, which can appear multiple times, names the
..    authors of the module code, just like ``sectionauthor`` names the author(s)
..    of a piece of documentation.  It too does not result in any output currently.


.. note::

   モジュールを解説するファイルのセクションタイトルは、概要ファイルの中の
   table-of-contents ツリーに利用されるので、意味が解るようにしてください。

.. .. note::
.. 
..    It is important to make the section title of a module-describing file
..    meaningful since that value will be inserted in the table-of-contents trees
..    in overview files.


情報単位 (Information units)
----------------------------

.. There are a number of directives used to describe specific features provided by
.. modules.  Each directive requires one or more signatures to provide basic
.. information about what is being described, and the content should be the
.. description.  The basic version makes entries in the general index; if no index
.. entry is desired, you can give the directive option flag ``:noindex:``.  The
.. following example shows all of the features of this directive type::

モジュールが提供する機能を解説するために使うディレクティブが幾つかあります。
各ディレクティブは、何を説明しようとしているのかを判別する情報として
一つかそれ以上のシグネチャを必要とします。そして、ディレクティブの内容は
その解説であるべきです。
デフォルトではディレクティブはインデックスのエントリに登録されます。
インデックスのエントリが必要ない場合は、ディレクティブオプションとして
``:noindex:`` というフラグを追加します。
次の例は、ここまでで説明した要素を全て含んだディレクティブになります::

    .. function:: spam(eggs)
                  ham(eggs)
       :noindex:

       Spam or ham the foo.

.. The signatures of object methods or data attributes should always include the
.. type name (``.. method:: FileInput.input(...)``), even if it is obvious from the
.. context which type they belong to; this is to enable consistent
.. cross-references.  If you describe methods belonging to an abstract protocol,
.. such as "context managers", include a (pseudo-)type name too to make the
.. index entries more informative.

オブジェクトのメソッドやデータ属性(attribute)のシグネチャは、文脈からどの型に
属しているかが明らかな場合であっても、 (``.. method::FileInput.input(...)``) の
ように型名を含める必要があります。 これは、一貫したクロスリファレンスを実現する
ためです。
"context managers" といった抽象プロトコルに属するメソッドを解説する場合にも、
インデックスを判りやすくするために、（仮想）型名を付けてください。

.. The directives are:

ディレクティブは以下の通りです。

.. describe:: cfunction

   Cの関数を説明します。シグネチャはC言語のまま付けてください。例::

      .. cfunction:: PyObject* PyType_GenericAlloc(PyTypeObject *type, Py_ssize_t nitems)

   このディレクティブは関数ライクなプリプロセッサマクロを説明するのにも使います。
   引数の名前を省略しないでください。引数の名前を説明の中で利用できます。

   シグネチャの中のアスタリスクをバックスラッシュでエスケープしなくても良いことを
   覚えておいてください。reST のインラインに対するパース処理は行われません。

.. .. describe:: cfunction
.. 
..    Describes a C function. The signature should be given as in C, e.g.::
.. 
..       .. cfunction:: PyObject* PyType_GenericAlloc(PyTypeObject *type, Py_ssize_t nitems)
.. 
..    This is also used to describe function-like preprocessor macros.  The names
..    of the arguments should be given so they may be used in the description.
.. 
..    Note that you don't have to backslash-escape asterisks in the signature,
..    as it is not parsed by the reST inliner.

.. describe:: cmember

   Cの構造体メンバを説明します。シグネチャの例::

      .. cmember:: PyObject* PyTypeObject.tp_bases

   説明文は、値の取り得る範囲、値がどのように扱われるか、値を変更しても良いのかどうかに
   ついて記述するべきです。 テキストの中で構造体のメンバを参照するときには ``member`` role を
   利用するべきです。

.. describe:: cmacro

   "シンプル"な C言語のマクロについて説明します。 シンプルなマクロとは、引数を取らず、
   関数として解説されないものです。 このディレクティブは単純な定数の定義には利用しません。
   Python ドキュメントの中でこのディレクティブが使われている例には、 :cmacro:`PyObject_HEAD` と
   :cmacro:`Py_BEGIN_ALLOW_THREADS` があります。

.. describe:: ctype

   C の型を説明します。シグネチャは単に型の名前であるべきです。

..    Describes a C type. The signature should just be the type name.

.. describe:: cvar

   C のグローバル変数を説明します。 シグネチャは、次の例のように、型を含めるべき
   です::

      .. cvar:: PyObject* PyClass_Type

.. describe:: data

   モジュール内のグローバルなデータを説明します。変数にも、 "定数として宣言された" 
   値にも利用します。 クラスとオブジェクトの属性には使いません。

..    Describes global data in a module, including both variables and values used
..    as "defined constants."  Class and object attributes are not documented
..    using this environment.

.. describe:: exception

   例外クラスについて説明します。 シグネチャは、必要ではありませんが、コンストラクタ
   引数と丸括弧を含むことができます。

..    Describes an exception class.  The signature can, but need not include
..    parentheses with constructor arguments.

.. describe:: function

   モジュールレベル関数を説明します。シグネチャには引数を記述するべきです。
   オプションの引数は角括弧で囲みます。明快さのために必要であれば、デフォルト値を
   含めることもできます。例::

      .. function:: Timer.repeat([repeat=3[, number=1000000]])

   このディレクティブはオブジェクトメソッドには利用されません。モジュールの名前空間にあり、
   モジュールの公開インタフェースになっている、束縛済みのオブジェクトメソッド
   (Bound object method) については、通常の関数とほとんど変わらないので、
   このディレクティブを使います。

   説明文は、必要とされる引数と、それがどのように使われるか（特に、可変(mutable) オブジェクトが
   変更されるかどうか）、副作用、発生しうる例外についての情報を含むべきです。
   小さな例を提供するのも良いでしょう。

.. describe:: class

   クラスを説明します。シグネチャには丸括弧とコンストラクタ引数を含めることが
   できます。

.. describe:: attribute

   オブジェクトの属性を説明します。説明文は、期待されるデータ型と、直接変更しても
   良いかどうかを含むべきです。

..    Describes an object data attribute.  The description should include
..    information about the type of the data to be expected and whether it may be
..    changed directly.

.. describe:: method

   オブジェクトメソッドを説明します。パラメータからは、 ``self`` パラメータを除外
   するべきです。説明文は ``function`` と同じような情報を提供するべきです。

..    Describes an object method.  The parameters should not include the ``self``
..    parameter.  The description should include similar information to that
..    described for ``function``.

.. describe:: opcode

   Python バイトコードの命令を説明します。

..    Describes a Python bytecode instruction.


.. There is also a generic version of these directives:

もっと汎用的なバージョンの以下のディレクティブもあります:

.. describe:: describe

   このディレクティブは、上で説明したディレクティブと同じフォーマットを生成しますが、
   インデックスエントリやクロスリファレンスターゲットは生成しません。
   このディレクティブは、たとえば、このドキュメントでディレクティブの説明をする
   ために利用しています。例::

      .. describe:: opcode
      
         Python バイトコードの命令を説明します。

..    This directive produces the same formatting as the specific ones explained
..    above but does not create index entries or cross-referencing targets.  It is
..    used, for example, to describe the directives in this document. Example::
.. 
..       .. describe:: opcode
.. 
..          Describes a Python bytecode instruction.


.. Showing code examples
.. ---------------------

コードサンプルを表示する (Showing code examples)
--------------------------------------------------

.. Examples of Python source code or interactive sessions are represented using
.. standard reST literal blocks.  They are started by a ``::`` at the end of the
.. preceding paragraph and delimited by indentation.

Python ソースコードやインタラクティブセッションの例は、 reST 標準のリテラルブロックを
利用して書きます。手前の段落の最後を ``::`` にして、インデントで範囲を指定します。

.. Representing an interactive session requires including the prompts and output
.. along with the Python code.  No special markup is required for interactive
.. sessions.  After the last line of input or output presented, there should not be
.. an "unused" primary prompt; this is an example of what *not* to do::

インタラクティブセッションを表現するときは、プロンプトと出力を Python コードと一緒に
書いてください。インタラクティブセッションに対して特別なマークアップは用意されて
いません。入力か出力の最後の行の後に、 "使用されない" プロンプトを入れてはいけません。
次の例のように *してはいけません* ::

   >>> 1 + 1
   2
   >>>

.. Syntax highlighting is handled in a smart way:

シンタックスハイライトはスマートに処理されます:

* 各ソースファイルには、 "ハイライト言語" があります。多数のファイルで Python の
  コードをハイライトするために、デフォルトでは ``'python'`` に設定されています。

* Python ハイライティングモードでは、インタラクティブセッションは自動的に認識
  されて適切にハイライトされます。

* ハイライト言語は ``highlightlang`` ディレクティブを利用して変更することができます。
  以下のようにして利用します::

     .. highlightlang:: c

  このディレクティブで設定されたハイライト言語は、次の ``highlightlang`` ディレクティブ
  まで有効になります。　

* ハイライト言語のよく使われる値は以下の通りです:

  * ``python`` (デフォルト)
  * ``c``
  * ``rest``
  * ``none`` (ハイライトなし)

* 現在のハイライト言語でのハイライティングに失敗した場合、そのブロックは全く
  ハイライトされません。

.. * There is a "highlighting language" for each source file.  Per default,
..   this is ``'python'`` as the majority of files will have to highlight Python
..   snippets.
.. 
.. * Within Python highlighting mode, interactive sessions are recognized
..   automatically and highlighted appropriately.
.. 
.. * The highlighting language can be changed using the ``highlightlang``
..   directive, used as follows::
.. 
..      .. highlightlang:: c
.. 
..   This language is used until the next ``highlightlang`` directive is
..   encountered.
.. 
.. * The valid values for the highlighting language are:
.. 
..   * ``python`` (the default)
..   * ``c``
..   * ``rest``
..   * ``none`` (no highlighting)
.. 
.. * If highlighting with the current language fails, the block is not highlighted
..   in any way.

.. Longer displays of verbatim text may be included by storing the example text in
.. an external file containing only plain text.  The file may be included using the
.. standard ``include`` directive with the ``literal`` option flag.  For example,
.. to include the Python source file :file:`example.py`, use::

長い、そのまま表示されるテキストは、外部のプレインテキストのみで書かれたファイルに
格納して、取り込む (include) こともできます。その場合、標準の ``include`` ディレクティブに
``literal`` オプションフラグを付けて利用します。たとえば、 :file:`example.py` という
Python ソースファイルを取り込む場合は::

   .. include:: example.py
      :literal:


.. Inline markup
.. -------------

インラインマークアップ (Inline markup)
--------------------------------------

前に述べたように、 Sphinx はドキュメント内に意味に基づくマークアップを挿入する
ために、 "interpreted text roles" を使います。

関数/メソッドの引数のようなローカル変数名は例外で、シンプルに ``*var*``
とマークされます。

その他の全ての role について、 ``:rolename:`content``` のように書く必要があります。

そのほかにもクロスリファレンス role をより他用途にする便利な機能があります。

* 明示的なタイトルと参照ターゲットを、 reST の直接ハイパーリンクのように書くことができます:
  ``:role:`title <target>``` は *target* を参照しますが、リンクテキストは *title*
  になります。

* コンテントにprefix ``!`` を付けると、 参照もハイパーリンクも作られません。

* Python オブジェクトのロールにおいて、コンテントに ``~`` というprefixをつけると、
  リンクターゲットはターゲットの最後の部分になります。例えば、 ``:meth:`~Queue.Queue.get```
  は ``Queue.Queue.get`` を参照しますが、リンクテキストとしては ``get``
  だけを表示します。

  HTML出力において、そのリンクの ``title`` 属性 (例えばマウスオーバー時のツールチップに
  表示される) は完全なターゲット名になります。

.. The following roles refer to objects in modules and are possibly hyperlinked if
.. a matching identifier is found:

以下の roles はモジュール内のオブジェクトを参照し、該当する識別子があればハイパーリンクを
作成します。

.. describe:: mod

   モジュールの名前。ドット付きの名前も使われる。これはパッケージの名前にも使う。

..    The name of a module; a dotted name may be used.  This should also be used for
..    package names.

.. describe:: func

   Python 関数の名前。ドット付きの名前も使われる。可読性のために、 role のテキストには
   後ろの丸括弧も含めるべきである。丸括弧は該当する識別子を検索するときには無視される。

..    The name of a Python function; dotted names may be used.  The role text
..    should include trailing parentheses to enhance readability.  The parentheses
..    are stripped when searching for identifiers.

.. describe:: data

   モジュールレベル変数や定数の名前。

..    The name of a module-level variable.

.. describe:: const

   定数として "宣言された" 名前。これは C言語 の ``#define`` か、
   Python の変更されないことを意図された変数である。

..    The name of a "defined" constant.  This may be a C-language ``#define``
..    or a Python variable that is not intended to be changed.

.. describe:: class

   クラス名。ドット付きの名前も使われる。

..    A class name; a dotted name may be used.

.. describe:: meth

   オブジェクトメソッドの名前。 role テキストには型の名前と、メソッド名、後続の
   丸括弧を含めるべきである。ドット付きの名前も使われる。

..   The name of a method of an object.  The role text should include the type
..   name, method name and the trailing parentheses.  A dotted name may be used.

.. describe:: attr

   オブジェクトのデータ属性の名前。

..    The name of a data attribute of an object.

.. describe:: exc

   例外の名前。ドット付きの名前も使われる。

..   The name of an exception. A dotted name may be used.

.. The name enclosed in this markup can include a module name and/or a class name.
.. For example, ``:func:`filter``` could refer to a function named ``filter`` in
.. the current module, or the built-in function of that name.  In contrast,
.. ``:func:`foo.filter``` clearly refers to the ``filter`` function in the ``foo``
.. module.

このマークアップで囲まれた名前は、モジュール名とクラス名の両方あるいは片方を
含めることができます。たとえば、 ``:func:`filter``` は、現在のモジュール内にある
``filter`` という名前の関数か、その名前のビルトイン関数を参照できます。
それに対して、 ``:func:`foo.filter``` とすると、はっきりと ``foo`` モジュールの
中の ``filter`` 関数だけを参照します。

.. A similar heuristic is used to determine whether the name is an attribute of
.. the currently documented class.

同じようなことが、ある名前が現在ドキュメントしているクラスの属性かどうかを
決定する際にも行われます。

.. The following roles create cross-references to C-language constructs if they
.. are defined in the API documentation:

以下の roles は、その C言語の要素が API ドキュメントにあれば、それに対する
クロスリファレンスを作成します。

.. describe:: cdata

   C言語の変数の名前。

..   The name of a C-language variable.

.. describe:: cfunc

   C言語の関数の名前。後続の丸括弧も含めるべきである。

..   The name of a C-language function. Should include trailing parentheses.

.. describe:: cmacro

   前述した、 "シンプルな" C のマクロの名前。

..   The name of a "simple" C macro, as defined above.

.. describe:: ctype

   C言語の型の名前。

..   The name of a C-language type.


.. The following role does possibly create a cross-reference, but does not refer
.. to objects:

以下の role はクロスリファレンスは作るかもしれませんが、オブジェクトを参照する
事はありません。

.. describe:: token

   文法上のトークンの名前。(リファレンスマニュアルにおいて、出力間のリンクを
   作成するために使われます)

..   The name of a grammar token (used in the reference manual to create links
..   between production displays).

---------

.. The following roles don't do anything special except formatting the text
.. in a different style:

以下の roles はテキストのフォーマットスタイルを変更する以外何もしません。

.. describe:: command

   ``rm`` のような、OS レベルのコマンドの名前。

..   The name of an OS-level command, such as ``rm``.

.. describe:: dfn

   テキストの中で定義される語をマークする。 (インデックスエントリは
   作成されない)

..   Mark the defining instance of a term in the text.  (No index entries are
..   generated.)

.. describe:: envvar

   環境変数。インデックスエントリが作成される。

..   An environment variable.  Index entries are generated.

.. describe:: file

   ファイルやディレクトリの名前。この中では、 "可変" な部分を示すために
   波括弧 "{}" を利用できる。例::

      ... は :file:`/usr/lib/python2.{x}/site-packages` にインストールされます ...

   ビルドされたドキュメントの中では、この ``x`` は、 Python マイナーバージョンで
   置き換えられることを示すために、違った形式で表示されます。

..    The name of a file or directory.  Within the contents, you can use curly
..    braces to indicate a "variable" part, for example::
.. 
..       ... is installed in :file:`/usr/lib/python2.{x}/site-packages` ...
.. 
..    In the built documentation, the ``x`` will be displayed differently to
..    indicate that it is to be replaced by the Python minor version.

.. describe:: guilabel

   インタラクティブなユーザーインタフェースの一部として表示されているラベルは、
   ``guilabel`` を使ってマークされるべきです。これには、 :mod:`curses` やその他の
   テキストベースのライブラリを利用して作られた、テキストベースのインタフェースの
   中のラベルも含みます。ボタンラベル、ウィンドウタイトル、フィールド名、メニューと
   その項目、選択リスト内の要素など、インタフェース内のどんなラベルにも、この role を
   利用するべきです。

..    Labels presented as part of an interactive user interface should be marked
..    using ``guilabel``.  This includes labels from text-based interfaces such as
..    those created using :mod:`curses` or other text-based libraries.  Any label
..    used in the interface should be marked with this role, including button
..    labels, window titles, field names, menu and menu selection names, and even
..    values in selection lists.

.. describe:: kbd

   キーストロークシーケンスをマークアップします。キーシーケンスをどんな形式で表現
   するかは、プラットフォームやアプリケーションごとに慣習があります。適切な慣習が
   無い場合は、初心者や非ネイティブスピーカーにも判るように、修飾キー (modifier key)
   を省略形にしないでください。例えば、 *xemacs* キーシーケンスは、 ``:kbd:`C-x C-f```
   のように記述できますが、特定のアプリケーションやプラットフォームに関連づけられて
   いない場合は、このキーシーケンスは ``:kbd:`Control-x Control-f``` とマークアップ
   されるべきです。

..    Mark a sequence of keystrokes.  What form the key sequence takes may depend
..    on platform- or application-specific conventions.  When there are no relevant
..    conventions, the names of modifier keys should be spelled out, to improve
..    accessibility for new users and non-native speakers.  For example, an
..    *xemacs* key sequence may be marked like ``:kbd:`C-x C-f```, but without
..    reference to a specific application or platform, the same sequence should be
..    marked as ``:kbd:`Control-x Control-f```.

.. describe:: keyword

   プログラミング言語の予約後(keyword).

..    The name of a keyword in a programming language.

.. describe:: mailheader

   RFC 822 形式のメールヘッダの名前。このマークアップは、そのヘッダが e-mail で
   利用されることを意味するわけではなく、同じ "スタイル" のどんなヘッダを参照する
   のにも使えます。多種の MIME 仕様で定義されているヘッダにも利用されます。ヘッダの
   名前は、実際に利用される場合と同じように書くべきで、一般的な使い方が複数ある
   場合は camel-case が好まれます。例: ``:mailheader:`Content-Type```.

..    The name of an RFC 822-style mail header.  This markup does not imply that
..    the header is being used in an email message, but can be used to refer to any
..    header of the same "style."  This is also used for headers defined by the
..    various MIME specifications.  The header name should be entered in the same
..    way it would normally be found in practice, with the camel-casing conventions
..    being preferred where there is more than one common usage. For example:
..    ``:mailheader:`Content-Type```.

.. describe:: makevar

   :command:`make` の変数名。

..    The name of a :command:`make` variable.

.. describe:: manpage

   セクションを含む、Unix manual page への参照。例: ``:manpage:`ls(1)```.

..    A reference to a Unix manual page including the section,
..    e.g. ``:manpage:`ls(1)```.

.. describe:: menuselection

   メニュー項目は ``menuselection`` role を使ってマークアップされるべきです。
   これは、サブメニューや特定の操作のの選択を含め、完全なメニュー項目の並びや、
   その一部をマークアップするのに使われます。各項目の名前は ``-->`` を使って
   区切るべきです。

   例えば、"スタート > プログラム" をマークアップする場合は、次の様にします::

      :menuselection:`スタート --> プログラム`

   幾つかのOSで、メニュー項目の後ろに何か記号を付けてダイアログボックスを開く
   事を示すといったことがあります。そういったメニュー項目の後ろに続く表記は、
   メニュー項目名に含めないべきです。

..    Menu selections should be marked using the ``menuselection`` role.  This is
..    used to mark a complete sequence of menu selections, including selecting
..    submenus and choosing a specific operation, or any subsequence of such a
..    sequence.  The names of individual selections should be separated by
..    ``-->``.
.. 
..    For example, to mark the selection "Start > Programs", use this markup::
.. 
..       :menuselection:`Start --> Programs`
.. 
..    When including a selection that includes some trailing indicator, such as the
..    ellipsis some operating systems use to indicate that the command opens a
..    dialog, the indicator should be omitted from the selection name.

.. describe:: mimetype

   MIME type もしくは MIME type の構成要素 (メジャーもしくはマイナー部分だけ)
   の名前。

..    The name of a MIME type, or a component of a MIME type (the major or minor
..    portion, taken alone).

.. describe:: newsgroup

   Usenet ニュースグループの名前。

..    The name of a Usenet newsgroup.

.. describe:: option

   実行可能プログラムのコマンドラインオプション。先頭のハイフンも含めなければ
   ならない。

..   A command-line option to an executable program.  The leading hyphen(s) must
..   be included.

.. describe:: program

   実行可能プログラムの名前。幾つかのプラットフォームでは、実行可能ファイル名と
   異なるかもしれない。特に、Windows のプログラムでは、 ``.exe`` (もしくは他の)
   拡張子は除くべきである。

..    The name of an executable program.  This may differ from the file name for
..    the executable for some platforms.  In particular, the ``.exe`` (or other)
..    extension should be omitted for Windows programs.

.. describe:: regexp

   正規表現。クォートを含めるべきではない。

..    A regular expression. Quotes should not be included.

.. describe:: samp

   コードのようなリテラルテキスト。
   ``:file:`` と同じく、この中では "可変" な部分を示すために波括弧を
   利用できます。

   "可変" 部分が要らないのであれば、通常の ````code```` を使ってください。
 
.. describe:: var

   Python か C の、変数か引数の名前。

..    A Python or C variable or parameter name.


.. The following roles generate external links:

以下の roles は外部リンクを生成する:

.. describe:: pep

   Python Enhancement Proposal への参照。これは適切なインデックスのエントリを
   生成する。HTML出力では、 "PEP *number*\ " というテキストが生成され、この
   テキストは指定された PEP のオンラインコピーへのハイパーリンクになる。

..    A reference to a Python Enhancement Proposal.  This generates appropriate
..    index entries. The text "PEP *number*\ " is generated; in the HTML output,
..    this text is a hyperlink to an online copy of the specified PEP.

.. describe:: rfc

   Internet Request for Comments (RFC) への参照。これは適切なインデックスのエントリを
   生成する。HTML 出力では "RFC *number*\ " というテキストが生成され、この
   テキストは指定された RFC のオンラインコピーへのハイパーリンクになる。

..    A reference to an Internet Request for Comments.  This generates appropriate
..    index entries. The text "RFC *number*\ " is generated; in the HTML output,
..    this text is a hyperlink to an online copy of the specified RFC.


.. Note that there are no special roles for including hyperlinks as you can use
.. the standard reST markup for that purpose.

ハイパーリンクのために特別な role が用意されていないことに注意してください。
reST 標準の方法がその目的に利用できるからです。


.. _doc-ref-role:

.. Cross-linking markup
.. --------------------

クロスリンクのマークアップ (Cross-linking markup)
-------------------------------------------------

.. To support cross-referencing to arbitrary sections in the documentation, the
.. standard reST labels are "abused" a bit:  Every label must precede a section
.. title; and every label name must be unique throughout the entire documentation
.. source.

ドキュメント中の任意のセクションに対してのクロスリファレンスをサポートするには、
reST 標準のラベルはあまり良くありません。 全てのラベルはセクションタイトルの前に
おかなければならず、全てのラベルの名前はドキュメントのソース全体に渡って
ユニークでなければなりません。

.. You can then reference to these sections using the ``:ref:`label-name``` role.

そこで、セクションを参照するのには ``:ref:`label-name``` という role を、利用
できます。


例::

   .. _my-reference-label:

   クロスリファレンスされるセクション
   ----------------------------------

   セクションの文字列。

   このセクション自体を参照します。 :ref:`my-reference-label` を見てください。

   .. _my-reference-label:

..    Section to cross-reference
..    --------------------------
.. 
..    This is the text of the section.
.. 
..    It refers to the section itself, see :ref:`my-reference-label`.

.. The ``:ref:`` invocation is replaced with the section title.

``:ref:`` の部分はセクションタイトルで置き換えられます。


.. Paragraph-level markup
.. ----------------------

段落レベルでのマークアップ (Paragraph-level markup)
---------------------------------------------------

.. These directives create short paragraphs and can be used inside information
.. units as well as normal text:

以下のディレクティブは、通常のテキストと同じように情報単位の中で利用でき、
短いパラグラフを作成します。

.. describe:: note

   この note に関係あるどの API を利用するときにも、ユーザーが気をつけるべき
   特に重要な情報。このディレクティブの内容は完全な文で、適切な句読点を全て含め
   なければなりません。

..    An especially important bit of information about an API that a user should be
..    aware of when using whatever bit of API the note pertains to.  The content of
..    the directive should be written in complete sentences and include all
..    appropriate punctuation.

   例::

      .. note::

         この関数はスパムメールを送るためのものではありません。

..          This function is not suitable for sending spam e-mails.

.. describe:: warning

   この warning に関係あるどの API を使うときにでも、ユーザーがとても慎重になるべき
   重要な情報。このディレクティブの内容は完全な文で、適切な句読点を全て含め
   なければなりません。 ``note`` との違いは、セキュリティに関する情報について、
   ``note`` よりも推奨されていることです。


..    An important bit of information about an API that a user should be very aware
..    of when using whatever bit of API the warning pertains to.  The content of
..    the directive should be written in complete sentences and include all
..    appropriate punctuation. This differs from ``note`` in that it is recommended
..    over ``note`` for information regarding security.

.. describe:: versionadded

   このディレクティブは、どのバージョンの Python で対象の要素がライブラリや C API
   に追加されたのかを示します。このディレクティブがモジュール全体に適用する場合、
   ディレクティブをモジュールセクションのどの文章よりも先におかれるべきです。

   最初の引数は必須で、バージョンです。二つ目の引数は任意で、変更点の *簡潔な* 
   説明です。

   例::

      .. versionadded:: 2.5
         *spam* 引数.

   ディレクティブの先頭行と説明との間に空行を入れてはならないことに注意してください。
   これはマークアップされたときにブロックが視覚的に連続するためです。

.. describe:: versionchanged

   ``versionadded`` とほとんど同じですが、対象の要素がいつどのように変更 (新しい引数が
   追加された、副作用が変わった、等) されたかを説明します。

..    Similar to ``versionadded``, but describes when and what changed in the named
..    feature in some way (new parameters, changed side effects, etc.).

--------------

.. describe:: seealso

   たくさんのセクションで、モジュールドキュメントや外部ドキュメントが参照されています。
   これらのリストは、 ``seealso`` ディレクティブで作成されます。
   
   ``seealso`` ディレクティブは一般的に、セクションの中で、どのサブセクションより
   前に置かれます。 HTML 出力では、本文の流れから切り離された区画の中に表示されます。

   ``seealso`` ディレクティブの中身は、 reST の定義リストであるべきです。例::

      .. seealso::

         Module :mod:`zipfile`
            :mod:`zipfile` 標準モジュールのドキュメント。

         `GNU tar manual, Basic Tar Format <http://link>`_
            GNU tar 拡張を含む、 tar アーカイブファイルのドキュメント。

..    Many sections include a list of references to module documentation or
..    external documents.  These lists are created using the ``seealso`` directive.
.. 
..    The ``seealso`` directive is typically placed in a section just before any
..    sub-sections.  For the HTML output, it is shown boxed off from the main flow
..    of the text.
.. 
..    The content of the ``seealso`` directive should be a reST definition list.
..    Example::
.. 
..       .. seealso::
.. 
..          Module :mod:`zipfile`
..             Documentation of the :mod:`zipfile` standard module.
.. 
..          `GNU tar manual, Basic Tar Format <http://link>`_
..             Documentation for tar archive files, including GNU tar extensions.

.. describe:: rubric

   このディレクティブは、目次 (table of contents) の項目にならない段落見出しを
   作ります。現在のところ、 "脚注" キャプションに利用されています。

..    This directive creates a paragraph heading that is not used to create a
..    table of contents node.  It is currently used for the "Footnotes" caption.

.. describe:: centered

   このディレクティブは、センタリングされた太字の段落を作ります。次のようにして
   使います::

      .. centered::

         段落の内容

..    This directive creates a centered boldfaced paragraph.  Use it as follows::
.. 
..       .. centered::
.. 
..          Paragraph contents.

.. Table-of-contents markup
.. ------------------------

Table-of-contents マークアップ (Table-of-contents markup)
---------------------------------------------------------

reST が複数のドキュメントを繋いだり、ドキュメントを複数のファイルに分割して出力する
機能を持たないので、 Sphinx は table-of-contents を作成したり、ドキュメントの元ファイル
間に関連を持たせたりするためにカスタムのディレクティブを利用しています。 ``toctree`` 
ディレクティブはその中心になる要素です。

.. Since reST does not have facilities to interconnect several documents, or split
.. documents into multiple output files, Sphinx uses a custom directive to add
.. relations between the single files the documentation is made of, as well as
.. tables of contents.  The ``toctree`` directive is the central element.

.. describe:: toctree

   このディレクティブは、ディレクティブの要素として与えられたファイルの中の TOCs 
   ("sub-TOC trees" を含む) から作成した "TOC tree" をその場所に挿入します。
   ``maxdepth`` オプションに数値を指定することで、 "TOC tree" の深さを指定できます。
   デフォルトでは全レベルを利用します。

..    This directive inserts a "TOC tree" at the current location, using the
..    individual TOCs (including "sub-TOC trees") of the files given in the
..    directive body.  A numeric ``maxdepth`` option may be given to indicate the
..    depth of the tree; by default, all levels are included.

..    Consider this example (taken from the library reference index)::

   次の例(ライブラリリファレンスインデックスから持ってきました)を考えてみます::

      .. toctree::
         :maxdepth: 2

         intro.rst
         strings.rst
         datatypes.rst
         numeric.rst
         (もっとたくさん)

   このディレクティブは二つの事を行います:

   * 指定されたファイル全てから TOC を作ります。深さが２、つまり一段階ネストした
     見出しまで含まれます。各ファイルの中の ``toctree`` ディレクティブも含まれます。

   * Sphinx は ``intro.rst``, ``strings.rst``, ... というファイルの相対順序と、それぞれの
     ファイルが現在のライブラリインデックスというファイルの子供である事を識別します。
     この情報から、 "next chapter", "previous chapter", "parent chapter" というリンクが
     作成されます。

.. TODO: 日本語ドキュメントをビルドしたときにリンクがどういう文字列になるか確認する。

..    This accomplishes two things:
.. 
..    * Tables of contents from all those files are inserted, with a maximum depth
..      of two, that means one nested heading.  ``toctree`` directives in those
..      files are also taken into account.
..    * Sphinx knows that the relative order of the files ``intro.rst``,
..      ``strings.rst`` and so forth, and it knows that they are children of the
..      shown file, the library index.  From this information it generates "next
..      chapter", "previous chapter" and "parent chapter" links.
.. 
..    In the end, all files included in the build process must occur in one
..    ``toctree`` directive; Sphinx will emit a warning if it finds a file that is
..    not included, because that means that this file will not be reachable through
..    standard navigation.

   最後に、ビルドされる全てのファイルはどこか一つの ``toctree`` ディレクティブに
   出現しなければなりません。どこにも含まれていないファイルがあると、そのファイルは
   標準のナビゲーションで到達不可能になるので、 Sphinx は警告を出します。

   特別な ``contents.rst`` というソースディレクトリのルートにあるファイルは、
   TOC tree 階層の "root" になります。このファイルから "コンテンツ" ページが
   作成されます。

.. TODO: 各用語を、カタカナにするべきか、アルファベットのままにするべきかを、
   Sphinx のビルド結果を元にチェックする。

.. Index-generating markup
.. -----------------------

インデックス生成マークアップ (Index-generating markup)
------------------------------------------------------

.. Sphinx automatically creates index entries from all information units (like
.. functions, classes or attributes) like discussed before.

Sphinx は自動的にインデックスのエントリを、先に述べた全ての情報の単位
(function, class, attribute のような) から作成します。

.. However, there is also an explicit directive available, to make the index more
.. comprehensive and enable index entries in documents where information is not
.. mainly contained in information units, such as the language reference.

しかし、インデックスをより有用なものにしたり、言語リファレンスのような情報が
情報の単位の中に含まれないようなドキュメントでもインデックスのエントリを作成
できるようにするために、明示的なディレクティブも利用可能です。

.. The directive is ``index`` and contains one or more index entries.  Each entry
.. consists of a type and a value, separated by a colon.

そのディレクティブは ``index`` で、一つかそれ以上のインデックスエントリを含みます。
各エントリは、種類と値をコロンで区切ったもので構成されます。

例::

   .. index::
      single: execution!context
      module: __main__
      module: sys
      triple: module; search; path

.. This directive contains five entries, which will be converted to entries in the
.. generated index which link to the exact location of the index statement (or, in
.. case of offline media, the corresponding page number).

このディレクティブは５つのエントリを持ち、 index 文の場所へのリンクになっている
インデックスエントリに変換されます。(もしくは、オフラインメディアの場合、該当する
ページ番号になります)

.. The possible entry types are:

利用可能なエントリの種類は:

single
   単独のインデックスエントリを生成します。サブエントリのテキストをセミコロンで
   区切る（これは以降の種類でも、どんなエントリを作るのかを指定するときに使います）
   ことによってサブエントリを作成できます。
pair
   ``pair: loop; statement`` は、 ``loop; statement`` と ``statement; loop`` という
   名前の二つのインデックスエントリを一度に作成するショートカットです。
triple
   同じように、 ``triple: module; search; path;`` は、 ``module; search path``,
   ``search; path, module``, ``path; module search`` というエントリを作成する
   ショートカットです。
module, keyword, operator, object, exception, statement, builtin
   これらは全て二つのインデックスエントリを作成します。例えば、 ``module: hashlib`` は、
   ``module; hashlib`` と ``hashlib; module`` を作ります。

.. single
..    Creates a single index entry.  Can be made a subentry by separating the
..    subentry text with a semicolon (this is also used below to describe what
..    entries are created).
.. pair
..    ``pair: loop; statement`` is a shortcut that creates two index entries,
..    namely ``loop; statement`` and ``statement; loop``.
.. triple
..    Likewise, ``triple: module; search; path`` is a shortcut that creates three
..    index entries, which are ``module; search path``, ``search; path, module`` and
..     ``path; module search``.
.. module, keyword, operator, object, exception, statement, builtin
..    These all create two index entries.  For example, ``module: hashlib`` creates
..    the entries ``module; hashlib`` and ``hashlib; module``.

.. Grammar production displays
.. ---------------------------

文法導出表記 (Grammar production displays)
------------------------------------------

.. Special markup is available for displaying the productions of a formal grammar.
.. The markup is simple and does not attempt to model all aspects of BNF (or any
.. derived forms), but provides enough to allow context-free grammars to be
.. displayed in a way that causes uses of a symbol to be rendered as hyperlinks to
.. the definition of the symbol.  There is this directive:

形式的な文法の導出を表示するための特別なマークアップが利用可能です。
このマークアップはシンプルで BNF (やその派生系) の全ての側面を表そうとはしていま
せんが、文脈自由文法 (context-free grammer) を、記号が使われている部分からその
記号の定義部分へハイパーリンクが張られている形で表記するために十分な能力を
提供しています。

.. describe:: productionlist

   このディレクティブは導出のグループを囲むために使われます。各導出は一つの行として
   渡され、名前と、コロンで区切られた残りの定義で構成されます。定義が複数行に
   渡る場合は、継続する各行は最初の行のコロンと同じ位置にあるコロンで始まらなければ
   なりません。

   空行は ``productionlist`` ディレクティブの引数として許可されていません。

   定義には interpreted text としてマークアップされたトークン名を使うことができます。
   (例: ``unaryneg ::= "-" `integer```) -- これは、各トークンの導出に対する
   クロスリファレンスを作成します。代替を示すために利用される縦棒はバックスラッシュで
   エスケープしなければならないことに気をつけてください。そうしないと、 reST パーサーは
   縦棒を置換参照 (substitution reference) として認識するからです。

   production においては、これ以上の reST パース処理が行われない事に注意してください。
   なので、 ``*`` や ``|`` といった文字をエスケープする必要がありません。

..    This directive is used to enclose a group of productions.  Each production is
..    given on a single line and consists of a name, separated by a colon from the
..    following definition.  If the definition spans multiple lines, each
..    continuation line must begin with a colon placed at the same column as in the
..    first line.
.. 
..    Blank lines are not allowed within ``productionlist`` directive arguments.
.. 
..    The definition can contain token names which are marked as interpreted text
..    (e.g. ``sum ::= `integer` "+" `integer```) -- this generates cross-references
..    to the productions of these tokens.  Note that vertical bars used to indicate
..    alternatives must be escaped with backslashes because otherwise they would
..    indicate a substitution reference to the reST parser.


.. XXX describe optional first parameter 

以下は Python リファレンスマニュアルの中の例です::

   .. productionlist::
      try_stmt: try1_stmt \| try2_stmt
      try1_stmt: "try" ":" :token:`suite`
               : ("except" [:token:`expression` ["," :token:`target`]] ":" :token:`suite`)+
               : ["else" ":" :token:`suite`]
               : ["finally" ":" :token:`suite`]
      try2_stmt: "try" ":" :token:`suite`
               : "finally" ":" :token:`suite`


置換 (Substitutions)
--------------------

ドキュメントシステムはデフォルトで定義されている３種類の置換を用意しています。
それらはビルド設定ファイル :file:`conf.py` で設定されます。

.. describe:: |release|

   ドキュメントが言及している Python のリリースへ置換されます。これは、例えば
   ``2.5.2b3`` のような、 alpha/beta/release candiate
   を含む完全バージョン文字列です。

.. describe:: |version|

   ドキュメントが言及している Python バージョンへ置換されます。これは、たとえば
   バージョン 2.5.1 において ``2.5`` の様に、バージョン文字列のうち メジャー・
   マイナー部のみで構成されます。

.. describe:: |today|

   今日の日付か、ビルド設定ファイルで指定された日付のどちらかに置換されます。
   通常は ``April 14, 2007`` のようなフォーマットになります。

