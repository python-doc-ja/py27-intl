
:mod:`parser` --- Python解析木にアクセスする
==================================

.. module:: parser
   :synopsis: Pythonソースコードに対する解析木へのアクセス。
.. moduleauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


.. % Copyright 1995 Virginia Polytechnic Institute and State University
.. % and Fred L. Drake, Jr.  This copyright notice must be distributed on
.. % all copies, but this document otherwise may be distributed as part
.. % of the Python distribution.  No fee may be charged for this document
.. % in any representation, either on paper or electronically.  This
.. % restriction does not affect other elements in a distributed package
.. % in any way.

.. index:: single: parsing; Python source code

:mod:`parser`モジュールはPythonの内部パーサとバイトコード・コンパイラへのインターフェイスを提供します。このインターフェイスの第一の目的は、PythonコードからPythonの式の解析木を編集したり、これから実行可能なコードを作成したりできるようにすることです。これは任意のPythonコードの断片を文字列として構文解析や変更を行うより良い方法です。なぜなら、構文解析がアプリケーションを作成するコードと同じ方法で実行されるからです。その上、高速です。

このモジュールについて注意すべきことが少しあります。それは作成したデータ構造を利用するために重要なことです。この文書はPythonコードの解析木を編集するためのチュートリアルではありませんが、:mod:`parser`モジュールを使った例をいくつか示しています。

もっとも重要なことは、内部パーサが処理するPythonの文法についてよく理解しておく必要があるということです。言語の文法に関する完全な情報については、Python言語リファレンス
(XXX reference:
../ref/ref.html)を参照してください。標準のPythonディストリビューションに含まれるファイル:file:`Grammar/Grammar`の中で定義されている文法仕様から、パーサ自身は作成されています。このモジュールが作成するASTオブジェクトの中に格納される解析木は、下で説明する:func:`expr`または:func:`suite`関数によって作られるときに内部パーサから実際に出力されるものです。:func:`sequence2ast`が作るASTオブジェクトは忠実にこれらの構造をシミュレートしています。言語の形式文法が改訂されるために、"正しい"と考えられるシーケンスの値がPythonのあるバージョンから別のバージョンで変化することがあるということに注意してください。しかし、Pythonのあるバージョンから別のバージョンへテキストのソースのままコードを移せば、目的のバージョンで正しい解析木を常に作成できます。ただし、インタープリタの古いバージョンへ移行する際に、最近の言語コンストラクトをサポートしていないことがあるという制限だけがあります。ソースコードが常に前方互換性があるのに対して、一般的に解析木はあるバージョンから別のバージョンへの互換性がありません。

:func:`ast2list`または:func:`ast2tuple`から返されるシーケンスのそれぞれの要素は単純な形式です。文法の非終端要素を表すシーケンスは常に一より大きい長さを持ちます。最初の要素は文法の生成規則を識別する整数です。これらの整数はCヘッダファイル:file:`Include/graminit.h`とPythonモジュール:mod:`symbol`の中の特定のシンボル名です。シーケンスに付け加えられている各要素は、入力文字列の中で認識されたままの形で生成規則の構成要素を表しています:
これらは常に親と同じ形式を持つシーケンスです。この構造の注意すべき重要な側面は、:const:`if_stmt`の中のキーワード:keyword:`if`のような親ノードの型を識別するために使われるキーワードがいかなる特別な扱いもなくノードツリーに含まれているということです。例えば、:keyword:`if`キーワードはタプル``(1,
'if')``と表されます。ここで、``1``は、ユーザが定義した変数名と関数名を含むすべての:const:`NAME`トークンに対応する数値です。行番号情報が必要なときに返される別の形式では、同じトークンが``(1,
'if', 12)``のように表されます。ここでは、``12``が終端記号の見つかった行番号を表しています。

終端要素は同じ方法で表現されますが、子の要素や識別されたソーステキストの追加は全くありません。上記の:keyword:`if`キーワードの例が代表的なものです。終端記号のいろいろな型は、Cヘッダファイル:file:`Include/token.h`とPythonモジュール:mod:`token`で定義されています。

ASTオブジェクトはこのモジュールの機能をサポートするために必要ありませんが、三つの目的から提供されています:
アプリケーションが複雑な解析木を処理するコストを償却するため、Pythonのリストやタプル表現に比べてメモリ空間を保全する解析木表現を提供するため、解析木を操作する追加モジュールをCで作ることを簡単にするため。ASTオブジェクトを使っていることを隠すために、簡単な"ラッパー"クラスをPythonで作ることができます。

:mod:`parser`モジュールは二、三の別々の目的のために関数を定義しています。もっとも重要な目的はASTオブジェクトを作ることと、ASTオブジェクトを解析木とコンパイルされたコードオブジェクトのような他の表現に変換することです。しかし、ASTオブジェクトで表現された解析木の型を調べるために役に立つ関数もあります。


.. seealso::

   Module :mod:`symbol`
      解析木の内部ノードを表す便利な定数。

   Module :mod:`token`
      便利な解析木の葉のノードを表す定数とノード値をテストするための関数。


.. _creating asts:

ASTオブジェクトを作成する
--------------

ASTオブジェクトはソースコードあるいは解析木から作られます。ASTオブジェクトをソースから作るときは、``'eval'``と``'exec'``形式を作成するために別々の関数が使われます。


.. function:: expr(source)

   まるで``compile(source, 'file.py',
   'eval')``への入力であるかのように、:func:`expr`関数はパラメータ*source*を構文解析します。解析が成功した場合は、ASTオブジェクトは内部解析木表現を保持するために作成されます。そうでなければ、適切な例外を発生させます。


.. function:: suite(source)

   まるで``compile(source, 'file.py',
   'exec')``への入力であるかのように、:func:`suite`関数はパラメータ*source*を構文解析します。解析が成功した場合は、ASTオブジェクトは内部解析木表現を保持するために作成されます。そうでなければ、適切な例外を発生させます。


.. function:: sequence2ast(sequence)

   この関数はシーケンスとして表現された解析木を受け取り、可能ならば内部表現を作ります。木がPythonの文法に合っていることと、すべてのノードがPythonのホストバージョンで有効なノード型であることを確認した場合は、ASTオブジェクトが内部表現から作成されて呼び出し側へ返されます。内部表現の作成に問題があるならば、あるいは木が正しいと確認できないならば、:exc:`ParserError`例外を発生します。この方法で作られたASTオブジェクトが正しくコンパイルできると決めつけない方がよいでしょう。ASTオブジェクトが:func:`compileast`へ渡されたとき、コンパイルによって送出された通常の例外がまだ発生するかもしれません。これは(:exc:`MemoryError`例外のような)構文に関係していない問題を示すのかもしれないし、``del
   f(0)``を解析した結果のようなコンストラクトが原因であるかもしれません。このようなコンストラクトはPythonのパーサを逃れますが、バイトコードインタープリタによってチェックされます。

   終端トークンを表すシーケンスは、``(1, 'name')``形式の二つの要素のリストか、または``(1, 'name',
   56)``形式の三つの要素のリストです。三番目の要素が存在する場合は、有効な行番号だとみなされます。行番号が指定されるのは、入力木の終端記号の一部に対してです。


.. function:: tuple2ast(sequence)

   これは:func:`sequence2ast`と同じ関数です。このエントリポイントは後方互換性のために維持されています。


.. _converting asts:

ASTオブジェクトを変換する
--------------

作成するために使われた入力に関係なく、ASTオブジェクトはリスト木またはタプル木として表される解析木へ変換されるか、または実行可能なオブジェクトへコンパイルされます。解析木は行番号情報を持って、あるいは持たずに抽出されます。


.. function:: ast2list(ast[, line_info])

   この関数は呼び出し側から*ast*にASTオブジェクトを受け取り、解析木と等価なPythonのリストを返します。結果のリスト表現はインスペクションあるいはリスト形式の新しい解析木の作成に使うことができます。リスト表現を作るためにメモリが利用できる限り、この関数は失敗しません。解析木がインスペクションのためだけにつかわれるならば、メモリの消費量と断片化を減らすために:func:`ast2tuple`を代わりに使うべきです。リスト表現が必要とされるとき、この関数はタプル表現を取り出して入れ子のリストに変換するよりかなり高速です。

   *line_info*が真ならば、トークンを表すリストの三番目の要素として行番号情報がすべての終端トークンに含まれます。与えられた行番号はトークン*が終わる*行を指定していることに注意してください。フラグが偽または省略された場合は、この情報は省かれます。


.. function:: ast2tuple(ast[, line_info])

   この関数は呼び出し側から*ast*にASTオブジェクトを受け取り、解析木と等価なPythonのタプルを返します。リストの代わりにタプルを返す以外は、この関数は:func:`ast2list`と同じです。

   *line_info*が真ならば、トークンを表すリストの三番目の要素として行番号情報がすべての終端トークンに含まれます。フラグが偽または省略された場合は、この情報は省かれます。


.. function:: compileast(ast[, filename\ ``= '<ast>'``])

   .. index:: builtin: eval

   :keyword:`exec`文の一部として使える、あるいは、組み込み:func:`eval`関数への呼び出しとして使えるコードオブジェクトを生成するために、PythonバイトコードコンパイラをASTオブジェクトに対して呼び出すことができます。この関数はコンパイラへのインターフェイスを提供し、*filename*パラメータで指定されるソースファイル名を使って、*ast*からパーサへ内部解析木を渡します。*filename*に与えられるデフォルト値は、ソースがASTオブジェクトだったことを示唆しています。

   ASTオブジェクトをコンパイルすることは、コンパイルに関する例外を引き起こすことになるかもしれません。例としては、``del
   f(0)``の解析木によって発生させられる:exc:`SyntaxError`があります:
   この文はPythonの形式文法としては正しいと考えられますが、正しい言語コンストラクトではありません。この状況に対して発生する:exc:`SyntaxError`は、実際にはPythonバイトコンパイラによって通常作り出されます。これが:mod:`parser`モジュールがこの時点で例外を発生できる理由です。解析木のインスペクションを行うことで、コンパイルが失敗するほとんどの原因をプルグラムによって診断することができます。


.. _querying asts:

ASTオブジェクトに対する問い合わせ
------------------

ASTが式またはsuiteとして作成されたかどうかをアプリケーションが決定できるようにする二つの関数が提供されています。これらの関数のどちらも、ASTが:func:`expr`または:func:`suite`を通してソースコードから作られたかどうか、あるいは、:func:`sequence2ast`を通して解析木から作られたかどうかを決定できません。


.. function:: isexpr(ast)

   .. index:: builtin: compile

   *ast*が``'eval'``形式を表している場合に、この関数は真を返します。そうでなければ、偽を返します。これは役に立ちます。なぜならば、通常は既存の組み込み関数を使ってもコードオブジェクトに対してこの情報を問い合わせることができないからです。このどちらのようにも:func:`compileast`によって作成されたコードオブジェクトに問い合わせることはできませんし、そのコードオブジェクトは組み込み:func:`compile`関数によって作成されたコードオブジェクトと同じであることに注意してください。


.. function:: issuite(ast)

   ASTオブジェクトが(通常"suite"として知られる)``'exec'``形式を表しているかどうかを報告するという点で、この関数は:func:`isexpr`に酷似しています。追加の構文が将来サポートされるかもしれないので、この関数が``not
   isexpr(ast)``と等価であるとみなすのは安全ではありません。


.. _ast errors:

例外とエラー処理
--------

parserモジュールは例外を一つ定義していますが、Pythonランタイム環境の他の部分が提供する別の組み込み例外を発生させることもあります。各関数が発生させる例外の情報については、それぞれ関数を参照してください。


.. exception:: ParserError

   parserモジュール内部で障害が起きたときに発生する例外。普通の構文解析中に発生する組み込みの:exc:`SyntaxError`ではなく、一般的に妥当性確認が失敗した場合に引き起こされます。例外の引数としては、障害の理由を説明する文字列である場合と、:func:`sequence2ast`へ渡される解析木の中の障害を引き起こすシーケンスを含むタプルと説明用の文字列である場合があります。モジュール内の他の関数の呼び出しは単純な文字列値を検出すればよいだけですが、:func:`sequence2ast`の呼び出しはどちらの例外の型も処理できる必要があります。

普通は構文解析とコンパイル処理によって発生する例外を、関数:func:`compileast`、:func:`expr`および:func:`suite`が発生させることに注意してください。このような例外には組み込み例外:exc:`MemoryError`、:exc:`OverflowError`、:exc:`SyntaxError`および:exc:`SystemError`が含まれます。こうした場合には、これらの例外が通常その例外に関係する全ての意味を伝えます。詳細については、各関数の説明を参照してください。


.. _ast objects:

ASTオブジェクト
---------

ASTオブジェクト間の順序と等値性の比較がサポートされています。(:mod:`pickle`モジュールを使った)ASTオブジェクトのピクルス化もサポートされています。


.. data:: ASTType

   :func:`expr`、:func:`suite`と:func:`sequence2ast`が返すオブジェクトの型。

ASTオブジェクトは次のメソッドを持っています:


.. method:: AST.compile([filename])

   ``compileast(ast, filename)``と同じ。


.. method:: AST.isexpr()

   ``isexpr(ast)``と同じ。


.. method:: AST.issuite()

   ``issuite(ast)``と同じ。


.. method:: AST.tolist([line_info])

   ``ast2list(ast, line_info)``と同じ。


.. method:: AST.totuple([line_info])

   ``ast2tuple(ast, line_info)``と同じ。


.. _ast examples:

例
-

.. index:: builtin: compile

parserモジュールを使うと、バイトコードが生成される前にPythonのソースコードの解析木に演算を行えるようになります。また、モジュールは情報発見のために解析木のインスペクションを提供しています。例が二つあります。簡単な例では組み込み関数:func:`compile`のエミュレーションを行っており、複雑な例では情報を得るための解析木の使い方を示しています。


:func:`compile`のエミュレーション
^^^^^^^^^^^^^^^^^^^^^^^^

たくさんの有用な演算を構文解析とバイトコード生成の間に行うことができますが、もっとも単純な演算は何もしないことです。このため、:mod:`parser`モジュールを使って中間データ構造を作ることは次のコードと等価です。
::

   >>> code = compile('a + 5', 'file.py', 'eval')
   >>> a = 5
   >>> eval(code)
   10

:mod:`parser`モジュールを使った等価な演算はやや長くなりますが、ASTオブジェクトとして中間内部解析木が維持されるようにします::

   >>> import parser
   >>> ast = parser.expr('a + 5')
   >>> code = ast.compile('file.py')
   >>> a = 5
   >>> eval(code)
   10

ASTとコードオブジェクトの両方が必要なアプリケーションでは、このコードを簡単に利用できる関数にまとめることができます::

   import parser

   def load_suite(source_string):
       ast = parser.suite(source_string)
       return ast, ast.compile()

   def load_expression(source_string):
       ast = parser.expr(source_string)
       return ast, ast.compile()


情報発見
^^^^

.. index::
   single: string; documentation
   single: docstrings

あるアプリケーションでは解析木へ直接アクセスすることが役に立ちます。この節の残りでは、:keyword:`import`を使って調査中のコードを実行中のインタープリタにロードする必要も無しに、解析木を使ってdocstringsに定義されたモジュールのドキュメンテーションへのアクセスを可能にする方法を示します。これは信頼性のないコードを解析するためにとても役に立ちます。

一般に、例は興味のある情報を引き出すために解析木をどのような方法でたどればよいかを示しています。二つの関数と一連のクラスが開発され、モジュールが提供する高レベルの関数とクラスの定義をプログラムから利用できるようになります。クラスは情報を解析木から引き出し、便利な意味レベルでその情報へアクセスできるようにします。一つの関数は単純な低レベルのパターンマッチング機能を提供し、もう一つの関数は呼び出し側の代わりにファイル操作を行うという点でクラスへの高レベルなインターフェイスです。ここで言及されていてPythonのインストールに必要ないすべてのソースファイルは、ディストリビューションの:file:`Demo/parser/`ディレクトリにあります。

Pythonの動的な性質によってプログラマは非常に大きな柔軟性を得ることができます。しかし、クラス、関数およびメソッドを定義するときには、ほとんどのモジュールがこれの限られた部分しか必要としません。この例では、考察される定義だけがコンテキストのトップレベルにおいて定義されるものです。例を挙げると、モジュールのゼロ列目に:keyword:`def`文によって定義される関数で、:keyword:`if`
...
:keyword:`else`コンストラクトの枝の中に定義されていない関数(ある状況ではそうすることにもっともな理由があるのですが)。例で開発するコードによって、定義の入れ子を扱う予定です。

より上位レベルの抽出メソッドを作るために知る必要があるのは、解析木構造がどのようなものかということと、それのどの程度まで関心を持つ必要があるのかということです。Pythonはやや深い解析木を使いますので、たくさんの中間ノードがあります。Pythonが使う形式文法を読んで理解することは重要です。これは配布物に含まれるファイル:file:`Grammar/Grammar`に明記されています。docstringsを探すときに対象として最も単純な場合について考えてみてください:
docstringの他に何も無いモジュール。(ファイル:file:`docstring.py`を参照してください。) ::

   """Some documentation.
   """

インタープリタを使って解析木を調べると、数と括弧が途方に暮れるほど多くて、ドキュメンテーションが入れ子になったタプルの深いところに埋まっていることがわかります。
::

   >>> import parser
   >>> import pprint
   >>> ast = parser.suite(open('docstring.py').read())
   >>> tup = ast.totuple()
   >>> pprint.pprint(tup)
   (257,
    (264,
     (265,
      (266,
       (267,
        (307,
         (287,
          (288,
           (289,
            (290,
             (292,
              (293,
               (294,
                (295,
                 (296,
                  (297,
                   (298,
                    (299,
                     (300, (3, '"""Some documentation.\n"""'))))))))))))))))),
      (4, ''))),
    (4, ''),
    (0, ''))

木の各ノードの最初の要素にある数はノード型です。それらは文法の終端記号と非終端記号に直接に対応します。残念なことに、それらは内部表現の整数で表されていて、生成されたPythonの構造でもそのままになっています。しかし、:mod:`symbol`と:mod:`token`モジュールはノード型の記号名と整数からノード型の記号名へマッピングする辞書を提供します。

上に示した出力の中で、最も外側のタプルは四つの要素を含んでいます:
整数``257``と三つの付加的なタプル。ノード型``257``の記号名は:const:`file_input`です。これらの各内部タプルは最初の要素として整数を含んでいます。これらの整数``264``と``4``、``0``は、ノード型:const:`stmt`、:const:`NEWLINE`、:const:`ENDMARKER`をそれぞれ表しています。これらの値はあなたが使っているPythonのバージョンに応じて変化する可能性があることに注意してください。マッピングの詳細については、:file:`symbol.py`と:file:`token.py`を調べてください。もっとも外側のノードがファイルの内容ではなく入力ソースに主に関係していることはほとんど明らかで、差し当たり無視しても構いません。:const:`stmt`ノードはさらに興味深いです。特に、すべてのdocstringsは、このノードが作られるのとまったく同じように作られ、違いがあるのは文字列自身だけである部分木にあります。同様の木のdocstringと説明の対象である定義されたエンティティ(クラス、関数あるいはモジュール)の関係は、前述の構造を定義している木の内部におけるdocstring部分木の位置によって与えられます。

実際のdocstringを木の変数要素を意味する何かと置き換えることによって、簡単なパターンマッチング方法で与えられたどんな部分木でもdocstringsに対する一般的なパターンと同等かどうかを調べられるようになります。例では情報の抽出の実例を示しているので、``['variable_name']``という単純な変数表現を念頭において、リスト形式ではなくタプル形式の木を安全に要求できます。簡単な再帰関数でパターンマッチングを実装でき、その関数は真偽値と変数名から値へのマッピングの辞書を返します。(ファイル:file:`example.py`を参照してください。)
::

   from types import ListType, TupleType

   def match(pattern, data, vars=None):
       if vars is None:
           vars = {}
       if type(pattern) is ListType:
           vars[pattern[0]] = data
           return 1, vars
       if type(pattern) is not TupleType:
           return (pattern == data), vars
       if len(data) != len(pattern):
           return 0, vars
       for pattern, data in map(None, pattern, data):
           same, vars = match(pattern, data, vars)
           if not same:
               break
       return same, vars

この構文の変数用の簡単な表現と記号のノード型を使うと、docstring部分木の候補のパターンがとても読みやすくなります。(ファイル:file:`example.py`を参照してください。)
::

   import symbol
   import token

   DOCSTRING_STMT_PATTERN = (
       symbol.stmt,
       (symbol.simple_stmt,
        (symbol.small_stmt,
         (symbol.expr_stmt,
          (symbol.testlist,
           (symbol.test,
            (symbol.and_test,
             (symbol.not_test,
              (symbol.comparison,
               (symbol.expr,
                (symbol.xor_expr,
                 (symbol.and_expr,
                  (symbol.shift_expr,
                   (symbol.arith_expr,
                    (symbol.term,
                     (symbol.factor,
                      (symbol.power,
                       (symbol.atom,
                        (token.STRING, ['docstring'])
                        )))))))))))))))),
        (token.NEWLINE, '')
        ))

このパターンと:func:`match`関数を使うと、前に作った解析木からモジュールのdocstringを簡単に抽出できます::

   >>> found, vars = match(DOCSTRING_STMT_PATTERN, tup[1])
   >>> found
   1
   >>> vars
   {'docstring': '"""Some documentation.\n"""'}

特定のデータを期待された位置から抽出できると、次は情報を期待できる場所はどこかという疑問に答える必要がでてきます。docstringを扱う場合、答えはとても簡単です:
docstringはコードブロック(:const:`file_input`または:const:`suite`ノード型)の最初の:const:`stmt`ノードです。モジュールは一つの:const:`file_input`ノードと、正確にはそれぞれが一つの:const:`suite`ノードを含むクラスと関数の定義で構成されます。クラスと関数は``(stmt,
(compound_stmt, (classdef, ...``または``(stmt, (compound_stmt, (funcdef,
...``で始まるコードブロックノードの部分木として簡単に識別されます。これらの部分木は:func:`match`によってマッチさせることができないことに注意してください。なぜなら、数を無視して複数の兄弟ノードにマッチすることをサポートしていないからです。この限界を超えるためにより念入りにつくったマッチング関数を使うことができますが、例としてはこれで充分です。

文がdocstringかどうかを決定し、実際の文字列をその文から抽出する機能について考えると、ある作業にはモジュール全体の解析木を巡回してモジュールの各コンテキストにおいて定義される名前についての情報を抽出し、その名前とdocstringsを結び付ける必要があります。この作業を行うコードは複雑ではありませんが、説明が必要です。

そのクラスへの公開インターフェイスは簡単で、おそらく幾分かより柔軟でしょう。モジュールのそれぞれの"主要な"ブロックは、問い合わせのための幾つかのメソッドを提供するオブジェクトと、少なくともそれが表す完全な解析木の部分木を受け取るコンストラクタによって記述されます。:class:`ModuleInfo`コンストラクタはオプションの*name*パラメータを受け取ります。なぜなら、そうしないとモジュールの名前を決められないからです。

公開クラスには:class:`ClassInfo`、:class:`FunctionInfo`および:class:`ModuleInfo`が含まれます。すべてのオブジェクトはメソッド:meth:`get_name`、:meth:`get_docstring`、:meth:`get_class_names`および:meth:`get_class_info`を提供します。:class:`ClassInfo`オブジェクトは:meth:`get_method_names`と:meth:`get_method_info`をサポートしますが、他のクラスは:meth:`get_function_names`と:meth:`get_function_info`を提供しています。

公開クラスが表すコードブロックの形式のそれぞれにおいて、トップレベルで定義された関数が"メソッド"として参照されるという違いがクラスにはありますが、要求される情報のほとんどは同じ形式をしていて、同じ方法でアクセスされます。クラスの外側で定義される関数との実際の意味の違いを名前の付け方が違うことで反映しているため、実装はこの違いを保つ必要があります。そのため、公開クラスのほとんどの機能が共通の基底クラス:class:`SuiteInfoBase`に実装されており、他の場所で提供される関数とメソッドの情報に対するアクセサを持っています。関数とメソッドの情報を表すクラスが一つだけであることに注意してください。これは要素の両方の型を定義するために:keyword:`def`文を使うことに似ています。

アクセサ関数のほとんどは:class:`SuiteInfoBase`で宣言されていて、サブクラスでオーバーライドする必要はありません。より重要なこととしては、解析木からのほとんどの情報抽出が:class:`SuiteInfoBase`コンストラクタに呼び出されるメソッドを通して行われるということがあります。平行して形式文法を読めば、ほとんどのクラスのコード例は明らかです。しかし、再帰的に新しい情報オブジェクトを作るメソッドはもっと調査が必要です。:file:`example.py`の:class:`SuiteInfoBase`定義の関連する箇所を以下に示します::

   class SuiteInfoBase:
       _docstring = ''
       _name = ''

       def __init__(self, tree = None):
           self._class_info = {}
           self._function_info = {}
           if tree:
               self._extract_info(tree)

       def _extract_info(self, tree):
           # extract docstring
           if len(tree) == 2:
               found, vars = match(DOCSTRING_STMT_PATTERN[1], tree[1])
           else:
               found, vars = match(DOCSTRING_STMT_PATTERN, tree[3])
           if found:
               self._docstring = eval(vars['docstring'])
           # discover inner definitions
           for node in tree[1:]:
               found, vars = match(COMPOUND_STMT_PATTERN, node)
               if found:
                   cstmt = vars['compound']
                   if cstmt[0] == symbol.funcdef:
                       name = cstmt[2][1]
                       self._function_info[name] = FunctionInfo(cstmt)
                   elif cstmt[0] == symbol.classdef:
                       name = cstmt[2][1]
                       self._class_info[name] = ClassInfo(cstmt)

初期状態に初期化した後、コンストラクタは:meth:`_extract_info`メソッドを呼び出します。このメソッドがこの例全体で行われる情報抽出の大部分を実行します。抽出には二つの別々の段階があります:
渡された解析木のdocstringの位置の特定、解析木が表すコードブロック内の付加的な定義の発見。

最初の:keyword:`if`テストは入れ子のsuiteが"短い形式"または"長い形式"かどうかを決定します。以下のコードブロックの定義のように、コードブロックが同じ行であるときに短い形式が使われます。
::

   def square(x): "Square an argument."; return x ** 2

長い形式では字下げされたブロックを使い、入れ子になった定義を許しています::

   def make_power(exp):
       "Make a function that raises an argument to the exponent `exp'."
       def raiser(x, y=exp):
           return x ** y
       return raiser

短い形式が使われるとき、コードブロックはdocstringを最初の:const:`small_stmt`要素として(ことによるとそれだけを)持っています。このようなdocstringの抽出は少し異なり、より一般的な場合に使われる完全なパターンの一部だけを必要とします。実装されているように、:const:`simple_stmt`ノードに:const:`small_stmt`ノードが一つだけある場合には、docstringしかないことがあります。短い形式を使うほとんどの関数とメソッドがdocstringを提供しないため、これで充分だと考えられます。docstringの抽出は前述の:func:`match`関数を使って進み、docstringが:class:`SuiteInfoBase`オブジェクトの属性として保存されます。

docstringを抽出した後、簡単な定義発見アルゴリズムを:const:`suite`ノードの:const:`stmt`ノードに対して実行します。短い形式の特別な場合はテストされません。短い形式では:const:`stmt`ノードが存在しないため、アルゴリズムは黙って:const:`simple_stmt`ノードを一つスキップします。正確に言えば、どんな入れ子になった定義も発見しません。

コードブロックのそれぞれの文をクラス定義(関数またはメソッドの定義、あるいは、何か他のもの)として分類します。定義文に対しては、定義された要素の名前が抽出され、コンストラクタに引数として渡される部分木の定義とともに定義に適した代理オブジェクトが作成されます。代理オブジェクトはインスタンス変数に保存され、適切なアクセサメソッドを使って名前から取り出されます。

公開クラスは:class:`SuiteInfoBase`クラスが提供するアクセサより具体的で、必要とされるどんなアクセサでも提供します。しかし、実際の抽出アルゴリズムはコードブロックのすべての形式に対して共通のままです。高レベルの関数をソースファイルから完全な情報のセットを抽出するために使うことができます。(ファイル:file:`example.py`を参照してください。)
::

   def get_docs(fileName):
       import os
       import parser

       source = open(fileName).read()
       basename = os.path.basename(os.path.splitext(fileName)[0])
       ast = parser.suite(source)
       return ModuleInfo(ast.totuple(), basename)

これはモジュールのドキュメンテーションに対する使いやすいインターフェイスです。この例のコードで抽出されない情報が必要な場合は、機能を追加するための明確に定義されたところで、コードを拡張することができます。

