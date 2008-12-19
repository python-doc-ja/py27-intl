
.. _compiler:

***************************
Python コンパイラパッケージ
***************************

.. sectionauthor:: Jeremy Hylton <jeremy@zope.com>


Python compiler パッケージは Python のソースコードを分析したり Python バイトコードを生成するためのツールです。compiler
は Python のソースコードから抽象的な構文木を生成し、その構文木から Python バイトコードを生成するライブラリをそなえています。

:mod:`compiler` パッケージは、Python で書かれた Python ソースコードからバイトコードへの変換プログラムです。
これは組み込みの構文解析器をつかい、そこで得られた 具体的な構文木に対して標準的な :mod:`parser` モジュールを使用します。
この構文木から抽象構文木 AST (Abstract Syntax Tree) が生成され、 その後 Python バイトコードが得られます。

このパッケージの機能は、Python インタプリタに内蔵されている 組み込みのコンパイラがすべて含んでいるものです。これはその機能と
正確に同じものになるよう意図してつくられています。なぜ同じことをする コンパイラをもうひとつ作る必要があるのでしょうか? このパッケージは
いろいろな目的に使うことができるからです。これは組み込みのコンパイラよりも 簡単に変更できますし、これが生成する AST は Python ソースコードを
解析するのに有用です。

この章では :mod:`compiler` パッケージのいろいろなコンポーネントが
どのように動作するのかを説明します。そのため説明はリファレンスマニュアル的なものと、 チュートリアル的な要素がまざったものになっています。

以下のモジュールは :mod:`compiler` パッケージの一部です:


.. toctree::

   ast.rst

基本的なインターフェイス
========================

.. module:: compiler


このパッケージのトップレベルでは 4つの関数が定義されています。 :mod:`compiler` モジュールを import すると、これらの関数および
このパッケージに含まれている一連のモジュールが使用可能になります。


.. function:: parse(buf)

   *buf* 中の Python ソースコードから得られた抽象構文木 AST を返します。 ソースコード中にエラーがある場合、この関数は
   :exc:`SyntaxError` を発生させます。 返り値は :class:`compiler.ast.Module` インスタンスであり、
   この中に構文木が格納されています。


.. function:: parseFile(path)

   *path* で指定されたファイル中の Python ソースコードから得られた 抽象構文木 AST を返します。これは
   ``parse(open(path).read())`` と等価な働きをします。


.. function:: walk(ast, visitor[, verbose])

   *ast* に格納された抽象構文木の各ノードを先行順序 (pre-order) で たどっていきます。各ノードごとに *visitor* インスタンスの
   該当するメソッドが呼ばれます。


.. function:: compile(source, filename, mode, flags=None,  dont_inherit=None)

   文字列 *source*、Python モジュール、文あるいは式を exec 文あるいは :func:`eval` 関数で実行可能なバイトコードオブジェクトに
   コンパイルします。この関数は組み込みの :func:`compile` 関数を 置き換えるものです。

   *filename* は実行時のエラーメッセージに使用されます。

   *mode* は、モジュールをコンパイルする場合は 'exec'、 (対話的に実行される) 単一の文をコンパイルする場合は 'single'、
   式をコンパイルする場合には 'eval' を渡します。

   引数 *flags* および *dont_inherit* は将来的に使用される文に 影響しますが、いまのところはサポートされていません。


.. function:: compileFile(source)

   ファイル *source* をコンパイルし、.pyc ファイルを生成します。

:mod:`compiler` パッケージは以下のモジュールを含んでいます: :mod:`ast`、 :mod:`consts`,、
:mod:`future`、 :mod:`misc`、 :mod:`pyassem`、 :mod:`pycodegen`、 :mod:`symbols`、
:mod:`transformer`、 そして :mod:`visitor`。


制限
====

compiler パッケージにはエラーチェックにいくつか問題が存在します。 構文エラーはインタープリタの 2つの別々のフェーズによって認識されます。
ひとつはインタープリタのパーザによって認識されるもので、 もうひとつはコンパイラによって認識されるものです。 compiler
パッケージはインタープリタのパーザに依存しているので、 最初の段階のエラーチェックは労せずして実現できています。
しかしその次の段階は、実装されてはいますが、その実装は不完全です。 たとえば compiler パッケージは引数に同じ名前が 2度以上出てきていても
エラーを出しません: ``def f(x, x): ...``

compiler の将来のバージョンでは、これらの問題は修正される予定です。


Python 抽象構文
===============

:mod:`compiler.ast` モジュールは Python の抽象構文木 AST を定義します。 AST
では各ノードがそれぞれの構文要素をあらわします。 木の根は :class:`Module` オブジェクトです。

抽象構文木 AST は、パーズされた Python ソースコードに対する 高水準のインターフェイスを提供します。Python インタプリタにおける
`parser <http://www.python.org/doc/current/lib/module-parser.html>`_ モジュールと
コンパイラは C で書かれおり、具体的な構文木を使っています。 具体的な構文木は Python のパーザ中で使われている構文と密接に関連しています。
ひとつの要素に単一のノードを割り当てる代わりに、ここでは Python の 優先順位に従って、何層にもわたるネストしたノードがしばしば使われています。

抽象構文木 AST は、:mod:`compiler.transformer` (変換器) モジュールに よって生成されます。transformer
は組み込みの Python パーザに依存しており、 これを使って具体的な構文木をまず生成します。つぎにそこから抽象構文木 AST を 生成します。

.. index::
   single: Stein, Greg
   single: Tutt, Bill

:mod:`transformer` モジュールは、実験的な Python-to-C コンパイラ用に Greg Stein と Bill Tutt
によって作られました。 現行のバージョンではいくつもの修正と改良がなされていますが、 抽象構文木 AST と transformer の基本的な構造は
Stein と Tutt によるものです。


AST ノード
----------

.. module:: compiler.ast


:mod:`compiler.ast` モジュールは、各ノードのタイプとその要素を記述した
テキストファイルからつくられます。各ノードのタイプはクラスとして表現され、 そのクラスは抽象基底クラス :class:`compiler.ast.Node`
を継承し 子ノードの名前属性を定義しています。


.. class:: Node()

   :class:`Node` インスタンスはパーザジェネレータによって自動的に作成されます。 ある特定の :class:`Node`
   インスタンスに対する推奨されるインターフェイスとは、 子ノードにアクセスするために public な (訳注: 公開された) 属性を使うことです。 public
   な属性は単一のノード、あるいは一連のノードのシーケンスに 束縛されている (訳注: バインドされている) かもしれませんが、 これは :class:`Node`
   のタイプによって違います。 たとえば :class:`Class` ノードの :attr:`bases` 属性は
   基底クラスのノードのリストに束縛されており、:attr:`doc` 属性は 単一のノードのみに束縛されている、といった具合です。

   各 :class:`Node` インスタンスは :attr:`lineno` 属性をもっており、 これは ``None`` かもしれません。 XXX
   どういったノードが使用可能な lineno をもっているかの規則は定かではない。

:class:`Node` オブジェクトはすべて以下のメソッドをもっています:


.. method:: Node.getChildren()

   子ノードと子オブジェクトを、これらが出てきた順で、平らなリスト形式にして返します。 とくにノードの順序は、 Python
   文法中に現れるものと同じになっています。 すべての子が :class:`Node` インスタンスなわけではありません。
   たとえば関数名やクラス名といったものは、ただの文字列として表されます。


.. method:: Node.getChildNodes()

   子ノードをこれらが出てきた順で平らなリスト形式にして返します。 このメソッドは :meth:`getChildren` に似ていますが、
   :class:`Node` インスタンスしか返さないという点で異なっています。

:class:`Node` クラスの一般的な構造を説明するため、 以下に 2つの例を示します。:keyword:`while` 文は以下のような文法規則により
定義されています::

   while_stmt:     "while" expression ":" suite
                  ["else" ":" suite]

:class:`While` ノードは 3つの属性をもっています: :attr:`test`、 :attr:`body`、 および :attr:`else_`
です。(ある属性にふさわしい名前が Python の予約語としてすでに使われているとき、その名前を属性名にすることは
できません。そのため、ここでは名前が正規のものとして受けつけられるように アンダースコアを後につけてあります、そのため :attr:`else_` は
:keyword:`else` のかわりです。)

:keyword:`if` 文はもっとこみ入っています。なぜならこれは いくつもの条件判定を含む可能性があるからです。 ::

   if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]

:class:`If` ノードでは、:attr:`tests` および :attr:`else_` の
2つだけの属性が定義されています。:attr:`tests` 属性には条件式とその後の動作の タプルがリスト形式で入っています。おのおのの
:keyword:`if`/:keyword:`elif` 節ごとに 1タプルです。各タプルの最初の要素は条件式で、2番目の要素はもしその式が
真ならば実行されるコードをふくんだ :class:`Stmt` ノードになっています。

:class:`If` の :meth:`getChildren` メソッドは、
子ノードの平らなリストを返します。:keyword:`if`/:keyword:`elif` 節が 3つあって :keyword:`else`
節がない場合なら、:meth:`getChildren` は 6要素のリストを 返すでしょう: 最初の条件式、最初の
:class:`Stmt`、2番目の条件式…といった具合です。

以下の表は :mod:`compiler.ast` で定義されている :class:`Node` サブクラスと、
それらのインスタンスに対して使用可能なパブリックな属性です。 ほとんどの属性の値じたいは :class:`Node` インスタンスか、インスタンスのリストです。
この値がインスタンス型以外の場合、その型は備考の中で記されています。 これら属性の順序は、 :meth:`getChildren` および
:meth:`getChildNodes` が返す順です。

XXX: input{asttable} :XXX

代入ノード
----------

代入をあらわすのに使われる一群のノードが存在します。 ソースコードにおけるそれぞれの代入文は、抽象構文木 AST では 単一のノード
:class:`Assign` になっています。 :attr:`nodes` 属性は各代入の対象にたいするノードのリストです。 これが必要なのは、たとえば
``a = b = 2`` のように 代入が連鎖的に起こるためです。 このリスト中における各 :class:`Node` は、
次のうちどれかのクラスになります: :class:`AssAttr`、 :class:`AssList`、 :class:`AssName`、 または
:class:`AssTuple`。

代入対象の各ノードには代入されるオブジェクトの種類が記録されています。 :class:`AssName` は ``a = 1`` などの単純な変数名、
:class:`AssAttr` は ``a.x = 1`` などの属性に対する代入、 :class:`AssList` および
:class:`AssTuple` はそれぞれ、 ``a, b, c = a_tuple`` などのようなリストとタプルの展開をあらわします。

代入対象ノードはまた、そのノードが代入で使われるのか、それとも del 文で使われるのかをあらわす属性 :attr:`flags` も持っています。
:class:`AssName` は ``del x`` などのような del 文をあらわすのにも 使われます。

ある式がいくつかの属性への参照をふくんでいるときは、 代入あるいは del 文はただひとつだけの :class:`AssAttr` ノードをもちます --
最終的な属性への参照としてです。それ以外の属性への参照は :class:`AssAttr` インスタンスの :attr:`expr` 属性にある
:class:`Getattr` ノードによってあらわされます。


サンプル
--------

この節では、Python ソースコードに対する抽象構文木 AST の かんたんな例をいくつかご紹介します。これらの例では :func:`parse`
関数をどうやって使うか、AST の repr 表現は どんなふうになっているか、そしてある AST ノードの属性に アクセスするにはどうするかを説明します。

最初のモジュールでは単一の関数を定義しています。 かりにこれは :file:`/tmp/doublelib.py` に格納されていると仮定しましょう。 ::

   """This is an example module.

   This is the docstring.
   """

   def double(x):
       "Return twice the argument"
       return x * 2

以下の対話的インタプリタのセッションでは、 見やすさのため 長い AST の repr を整形しなおしてあります。 AST の repr では qualify
されていないクラス名が使われています。 repr 表現からインスタンスを作成したい場合は、 :mod:`compiler.ast` モジュールから
それらのクラス名を import しなければなりません。 ::

   >>> import compiler
   >>> mod = compiler.parseFile("/tmp/doublelib.py")
   >>> mod
   Module('This is an example module.\n\nThis is the docstring.\n', 
          Stmt([Function(None, 'double', ['x'], [], 0,
                         'Return twice the argument', 
                         Stmt([Return(Mul((Name('x'), Const(2))))]))]))
   >>> from compiler.ast import *
   >>> Module('This is an example module.\n\nThis is the docstring.\n', 
   ...    Stmt([Function(None, 'double', ['x'], [], 0,
   ...                   'Return twice the argument', 
   ...                   Stmt([Return(Mul((Name('x'), Const(2))))]))]))
   Module('This is an example module.\n\nThis is the docstring.\n', 
          Stmt([Function(None, 'double', ['x'], [], 0,
                         'Return twice the argument', 
                         Stmt([Return(Mul((Name('x'), Const(2))))]))]))
   >>> mod.doc
   'This is an example module.\n\nThis is the docstring.\n'
   >>> for node in mod.node.nodes:
   ...     print node
   ... 
   Function(None, 'double', ['x'], [], 0, 'Return twice the argument',
            Stmt([Return(Mul((Name('x'), Const(2))))]))
   >>> func = mod.node.nodes[0]
   >>> func.code
   Stmt([Return(Mul((Name('x'), Const(2))))])


Visitor を使って AST をわたり歩く
=================================

.. module:: compiler.visitor


visitor パターンは ...   :mod:`compiler` パッケージは、Python のイントロスペクション機能を利用して visitor
のために必要な大部分のインフラを省略した、visitor パターンの変種を使っています。

visit されるクラスは、visitor を受け入れるようにプログラムされている必要はありません。 visitor
が必要なのはただそれがとくに興味あるクラスに対して visit メソッドを 定義することだけです。それ以外はデフォルトの visit メソッドが処理します。

XXX The magic :meth:`visit` method for visitors.


.. function:: walk(tree, visitor[, verbose])


.. class:: ASTVisitor()

   :class:`ASTVisitor` は構文木を正しい順序でわたり歩くようにします。 それぞれのノードはまず :meth:`preorder`
   の呼び出しではじまります。 各ノードに対して、これは 'visitNodeType' という名前のメソッドに対する :meth:`preorder` 関数への
   *visitor* 引数をチェックします。 ここで NodeType の部分はそのノードのクラス名です。たとえば :class:`While`
   ノードなら、:meth:`visitWhile` が呼ばれるわけです。 もしそのメソッドが存在している場合、それはそのノードを第一引数として呼び出されます。

   ある特定のノード型に対する visitor メソッドでは、 その子ノードをどのようにわたり歩くかが制御できます。 :class:`ASTVisitor` は
   visitor に visit メソッドを追加することで、 その visitor 引数を修正します。特定のノード型に対する visitor が 存在しない場合、
   :meth:`default` メソッドが呼び出されます。

:class:`ASTVisitor` オブジェクトには以下のようなメソッドがあります:

XXX 追加の引数を記述


.. method:: ASTVisitor.default(node[, ...])


.. method:: ASTVisitor.dispatch(node[, ...])


.. method:: ASTVisitor.preorder(tree, visitor)


バイトコード生成
================

バイトコード生成器はバイトコードを出力する visitor です。 visit メソッドが呼ばれるたびにこれは :meth:`emit` メソッドを
呼び出し、バイトコードを出力します。基本的なバイトコード生成器は モジュール、クラス、および関数によって拡張できます。
アセンブラがこれらの出力された命令を低レベルのバイトコードに変換します。 これはコードオブジェクトからなる定数のリスト生成や、
分岐のオフセット計算といった処理をおこないます。

