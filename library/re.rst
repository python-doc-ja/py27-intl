:mod:`re` --- 正規表現操作
==========================

.. module:: re
   :synopsis: 正規表現操作
.. moduleauthor:: Fredrik Lundh <fredrik@pythonware.com>
.. sectionauthor:: Andrew M. Kuchling <amk@amk.ca>


このモジュールでは、 Perl で見られるものと同様な正規表現マッチング操作を提供しています。
パターンと検索対象文字列の両方について、 8 ビット文字列と Unicode 文字列を同じように扱えます。

正規表現では、特殊な形式を表したり、特殊文字の持つ特別な意味を呼び出さずにその特殊な文字を
使えるようにするために、バックスラッシュ文字 (``'\'``) を使います。こうしたバックスラッシュの
使い方は、 Python の文字列リテラルにおける同じバックスラッシュ文字と衝突を起こします。
例えば、バックスラッシュ自体にマッチさせるには、パターン文字列として ``'\\\\'`` と書かなければ
なりません、というのも、正規表現は ``\\`` でなければならず、さらに正規な Python 文字列リテラル
では各々のバックスラッシュを ``\\`` と表現せねばならないからです。

正規表現パターンに Python の raw string 記法を使えばこの問題を解決できます。
``'r'`` を前置した文字列リテラル内ではバックスラッシュを特別扱いしません。従って、
``"\n"`` が改行一文字の入った文字列になるのに対して、 ``r"\n"`` は ``'\'`` と ``'n'`` と
いう二つの文字の入った文字列になります。通常、 Python コード中では、パターンをこの raw string
記法を使って表現します。

大抵の正規表現操作がモジュールレベルの関数と、 :class:`RegexObject` のメソッドとして提供される
ことに注意して下さい。
関数は正規表現オブジェクトのコンパイルを必要としない近道ですが、いくつかのチューニング変数を失います。

.. _re-syntax:

正規表現のシンタクス
--------------------

正規表現 (すなわち RE) は、表現にマッチ (match) する文字列の集合を表しています。
このモジュールの関数を使えば、ある文字列が指定の正規表現にマッチするか
(または指定の正規表現がある文字列にマッチするか、つまりは同じことですが) を検査できます。

正規表現を連結すると新しい正規表現を作れます。 *A* と *B* がともに正規表現であれば *AB*
も正規表現です。一般的に、文字列 *p* が A　とマッチし、別の文字列 *q* が B とマッチすれば、
文字列 *pq* は AB にマッチします。ただし、この状況が成り立つのは、 *A* と *B*
との間に境界条件がある場合や、番号付けされたグループ参照のような、優先度の低い演算を *A* や *B*
が含まない場合だけです。
かくして、ここで述べるような、より簡単でプリミティブな正規表現から、複雑な正規表現を容易に構築
できます。正規表現に関する理論と実装の詳細については上記の Friedl 本か、コンパイラの構築に
関する教科書を調べて下さい。

以下で正規表現の形式に関する簡単な説明をしておきます。より詳細な情報や
よりやさしい説明に関しては、 :ref:`regex-howto` を参照下さい。

正規表現には、特殊文字と通常文字の両方を含められます。 ``'A'`` 、 ``'a'`` 、あるいは ``'0'``
のようなほとんどの通常文字は最も簡単な正規表現になります。こうした文字は、単純にその文字自体に
マッチします。通常の文字は連結できるので、 ``last`` は文字列 ``'last'`` とマッチします。
(この節の以降の説明では、正規表現を引用符を使わずに ``この表示スタイル: special style``
で書き、マッチ対象の文字列は、 ``'引用符で括って'`` 書きます。)

``'|'`` や ``'('`` といったいくつかの文字は特殊文字です。特殊文字は通常の文字の種別を表したり、
あるいは特殊文字の周辺にある通常の文字に対する解釈方法に影響します。
正規表現パターン文字列には、 null byte を含めることができませんが、
``\number`` 記法や、 ``'\x00'`` などとして指定することができます。

特殊文字を以下に示します:


``'.'``
   (ドット)  デフォルトのモードでは改行以外の任意の文字にマッチします。
   :const:`DOTALL` フラグが指定されていれば改行も含むすべての文字にマッチします。

``'^'``
   (キャレット)  文字列の先頭とマッチします。
   :const:`MULTILINE` モードでは各改行の直後にマッチします。

``'$'``
   文字列の末尾、あるいは文字列の末尾の改行の直前にマッチします。
   例えば、 ``foo`` は 'foo' と 'foobar'
   の両方にマッチします。一方、正規表現 ``foo$`` は 'foo' だけとマッチします。
   興味深いことに、 ``'foo1\nfoo2\n'`` を
   ``foo.$`` で検索した場合、通常のモードでは 'foo2' だけにマッチし、
   :const:`MULTILINE` モードでは 'foo1' にもマッチします。
   ``$`` だけで ``'foo\n'`` を検索した場合、2箇所 (内容は空) でマッチします: 1つは、改行の
   直前で、もう1つは、文字列の最後です。


``'*'``
   直前にある RE に作用して、 RE を 0 回以上できるだけ多く繰り返したものにマッチさせる
   ようにします。例えば ``ab*`` は
   'a'、'ab'、あるいは 'a' に任意個数の'b' を続けたものにマッチします。

``'+'``
   直前にある RE に作用して、 RE を、1 回以上繰り返したものにマッチさせるようにします。
   例えば ``ab+`` は 'a' に一つ以上の 'b'
   が続いたものにマッチし、 'a' 単体にはマッチしません。

``'?'``
   直前にある RE に作用して、 RE を 0 回か 1 回繰り返したものにマッチさせるようにします。
   例えば ``ab?`` は 'a' あるいは 'ab'
   にマッチします。

``*?``, ``+?``, ``??``
   ``'*'`` 、 ``'+'`` 、 ``'?'`` といった修飾子は、すべて :dfn:`貪欲 (greedy)`
   マッチ、すなわちできるだけ多くのテキストにマッチするようになっています。時にはこの動作が
   望ましくない場合もあります。例えば正規表現 ``<.*>`` を ``'<H1>title</H1>'`` に
   マッチさせると、 ``'<H1>'`` だけにマッチするのではなく全文字列にマッチしてしまいます。
   ``'?'`` を修飾子の後に追加すると、 :dfn:`非貪欲 (non-greedy)` あるいは
   :dfn:`最小一致 (minimal)` のマッチになり、できるだけ *少ない* 文字数のマッチになります。
   例えば上の式で ``.*?`` を使うと ``'<H1>'`` だけにマッチします。

``{m}``
   前にある RE の *m* 回の正確なコピーとマッチすべきであることを指定します；マッチ回数が
   少なければ、RE 全体ではマッチしません。例えば、
   ``a{6}`` は、正確に 6個の ``'a'`` 文字とマッチしますが、 5個ではマッチしません。

``{m,n}``
   結果の RE は、前にある RE を、 *m* 回から *n* 回まで繰り返したもので、できるだけ多く繰り返した
   ものとマッチするように、マッチします。
   例えば、 ``a{3,5}`` は、3個から 5個の ``'a'`` 文字とマッチします。 *m* を省略するとマッチ
   回数の下限として0を指定した事になり、 *n*
   を省略することは、上限が無限であることを指定します； ``a{4,}b`` は ``aaaab`` や、千個の
   ``'a'`` 文字に ``b`` が続いたものとマッチしますが、 ``aaab`` とはマッチしません。
   コンマは省略できません、そうでないと修飾子が上で述べた形式と混同されてしまうからです。

``{m,n}?``
   結果の RE は、前にある RE の *m* 回から *n* 回まで繰り返したもので、できるだけ *少なく*
   繰り返したものとマッチするように、マッチします。これは、前の修飾子の控え目バージョンです。
   例えば、 6文字文字列 ``'aaaaaa'`` では、 ``a{3,5}`` は、5個の ``'a'`` 文字と
   マッチしますが、 ``a{3,5}?`` は3個の文字とマッチするだけです。

``'\'``
   特殊文字をエスケープする( ``'*'`` や ``'?'`` 等のような文字とのマッチをできるようにする)
   か、あるいは、特殊シーケンスの合図です;
   特殊シーケンスは後で議論します。

   もしパターンを表現するのに raw string を使用していないのであれば、 Python も、
   バックスラッシュを文字列リテラルでのエスケープシーケンスとして使っていることを覚えて
   いて下さい；もしエスケープシーケンスを Python の構文解析器が認識して処理しなければ、
   そのバックスラッシュとそれに続く文字は、結果の文字列にそのまま含まれます。
   しかし、もし Python が結果のシーケンスを認識するのであれば、バックスラッシュを 2回
   繰り返さなければいけません。このことは複雑で理解しにくいので、最も簡単な表現以外は、
   すべて raw string を使うことをぜひ勧めます。

``[]``
   文字の集合を指定するのに使用します。集合には以下のものが指定できます:

   * 個別に指定できる文字。 ``[amk]`` は ``'a'`` 、
     ``'m'`` 、または ``'k'`` とマッチします。

   * 連続した文字の範囲を、先頭と最後の2文字とその間に ``'-'`` を挟んだ形で指定できます。
     ``[a-z]`` はすべての小文字の ASCII 文字とマッチします。 ``[0-5][0-9]`` は ``00`` から
     ``59`` までの、すべての 2 桁の数字とマッチします。 ``[0-9A-Fa-f]`` はすべての 16 進数と
     マッチします。 ``-`` が、エスケープされた場合 (例: ``[a\-z]``)、あるいは先頭か末尾に
     置かれた場合 (例: ``[a-]``)、リテラル ``'-'`` とマッチします。

   * 集合内では、特殊文字はその意味を失います。 ``[(+*)]`` はリテラル文字 ``'('`` 
     ``'+'`` 、 ``'*'`` 、あるいは ``')'`` のいずれかとマッチします。

   * ``\w`` や ``\S`` のような文字クラス (後述) も集合内に指定できますが、それらにマッチする
     文字は :const:`LOCALE` か :const:`UNICODE` のどちらか有効にされているモードに依存します。

   * 範囲内にない文字とは、その集合の :dfn:`補集合` をとることでマッチできます。集合の
     最初の文字が ``'^'`` の時、集合に *ない* 文字すべてとマッチします。 ``[^5]`` は
     ``'5'`` を除くあらゆる文字にマッチします。 ``[^^]`` は ``'^'`` を除くあらゆる文字に
     マッチします。 ``^`` は集合の最初の文字でない限り特別の意味を持ちません。

   * 集合内でリテラル ``']'`` をマッチさせるには、その前にバックスラッシュをつけるか、集合の
     先頭に置きます。 ``[()[\]{}]`` と ``[]()[{}]`` はどちらも ``']'`` にマッチします。

``'|'``
   ``A|B`` は、ここで A と B は任意の RE ですが、 A か B のどちらかとマッチする正規表現を
   作成します。任意個数の RE を、こういう風に ``'|'`` で分離することができます。
   これはグループ (以下参照) 内部でも同様に使えます。検査対象文字列をスキャンする中で、 ``'|'``
   で分離された RE は左から右への順に検査されます。
   一つでも完全にマッチしたパターンがあれば、そのパターン枝が受理されます。このことは、もし ``A``
   がマッチすれば、たとえ ``B`` によるマッチが全体としてより長いマッチになったとしても、 ``B``
   を決して検査しないことを意味します。
   言いかえると、 ``'|'`` 演算子は決して貪欲 (greedy) ではありません。文字通りの ``'|'``
   とマッチするには、 ``\|`` を使うか、
   あるいはそれを ``[|]`` のように文字クラス内に入れます。

``(...)``
   丸括弧の中にどのような正規表現があってもマッチし、またグループの先頭と末尾を表します；
   グループの中身は、マッチが実行された後に検索され、後述する
   ``\number`` 特殊シーケンス付きの文字列内で、後でマッチされます。文字通りの
   ``'('`` や ``')'`` とマッチするには、 ``\(``
   あるいは ``\)`` を使うか、それらを文字クラス内に入れます： ``[(] [)]`` 。

``(?...)``
   これは拡張記法です (``'('`` に続く ``'?'`` は他には意味がありません) 。 ``'?'``
   の後の最初の文字が、この構造の意味とこれ以上の
   シンタクスがどういうものであるかを決定します。拡張記法は普通新しいグループを作成しません；
   ``(?P<name>...)`` がこの規則の唯一の例外です。
   以下に現在サポートされている拡張記法を示します。

``(?iLmsux)``
   ( 集合 ``'i'``, ``'L'``, ``'m'``, ``'s'``, ``'u'``, ``'x'``
   から1文字以上) 。グループは空文字列ともマッチします；文字は、正規表現全体の対応するフラグ
   (:const:`re.I` (大文字・小文字を区別しない), :const:`re.L` (ロケール依存),
   :const:`re.M` (MULTILINEモード), :const:`re.S` (DOTALLモード),
   :const:`re.U` (Unicode依存), :const:`re.X` (冗長) ) を設定します。
   (フラグについては、 :ref:`contents-of-module-re` に記述があります)
   これは、もし *flag* 引数を :func:`re.compile` 関数に渡さずに、そのフラグを
   正規表現の一部として含めたいならば役に立ちます。

   ``(?x)`` フラグは、式が構文解析される方法を変更することに注意して下さい。
   これは式文字列内の最初か、あるいは1つ以上の空白文字の後で使うべきです。
   もしこのフラグの前に非空白文字があると、その結果は未定義です。

``(?:...)``
   正規表現の丸括弧の取り込まないバージョンです。
   どのような正規表現が丸括弧内にあってもマッチしますが、グループによってマッチされたサブ文字列は、
   マッチを実行したあと検索されることも、あるいは後でパターンで参照されることも *できません* 。

``(?P<name>...)``
   正規表現の丸括弧に似ていますが、グループによってマッチした部分文字列はシンボリック\
   グループ名 *name* によってアクセス可能になります。グループ名は有効な Python 識別子でなければならず、
   グループ名は 1 個の正規表現内で一意でなければなりません。シンボリックグループは番号付けもされており、
   番号によるアクセスも可能です。

   名前付きグループは 3 つのコンテキストで参照できます。パターンが ``(?P<quote>['\"]).*?(?P=quote)``
   (シングルまたはダブルクオートのどちらかにマッチ) の場合`:

   +-----------------------------------------+----------------------------------+
   | グループ "quote" を参照するコンテキスト | 参照方法                         |
   +=========================================+==================================+
   | 同一パターンへの参照                    | * ``(?P=quote)`` (そのまま)      |
   |                                         | * ``\1``                         |
   +-----------------------------------------+----------------------------------+
   | マッチオブジェクト ``m`` の処理時       | * ``m.group('quote')``           |
   |                                         | * ``m.end('quote')`` (etc.)      |
   +-----------------------------------------+----------------------------------+
   | ``re.sub()`` の ``repl`` 属性へ渡される | * ``\g<quote>``                  |
   | 文字列                                  | * ``\g<1>``                      |
   |                                         | * ``\1``                         |
   +-----------------------------------------+----------------------------------+

``(?P=name)``
   名前付きグループへの後方参照です; 既出のグループ名 *name* にマッチする文字列は
   何にでもマッチします。

``(?#...)``
   コメントです；括弧の内容は単純に無視されます。

``(?=...)``
   もし ``...`` が次に続くものとマッチすればマッチしますが、文字列をまったく消費しません。
   これは先読みアサーション (lookahead assertion) と呼ばれます。例えば、
   ``Isaac (?=Asimov)`` は、 ``'Isaac '`` に
   ``'Asimov'`` が続く場合だけ、 ``'Isaac '`` とマッチします。

``(?!...)``
   もし ``...`` が次に続くものとマッチしなければマッチします。これは否定先読みアサーション
   (negative lookahead assertion) です。例えば、
   ``Isaac (?!Asimov)`` は、 ``'Isaac '`` に
   ``'Asimov'`` が続か *ない* 場合のみマッチします。

``(?<=...)``

   文字列内の現在位置の前に、現在位置で終わる ``...`` とのマッチがあれば、
   マッチします。これは :dfn:`後読みアサーション` と呼ばれます。 ``(?<=abc)def``
   は ``abcdef`` にマッチを見つけます。後読みは 3 文字をバックアップし、
   含まれているパターンとマッチするかどうか検査します。含まれるパターンは、
   固定長の文字列にのみマッチしなければなりません。すなわち、 ``abc`` や ``a|b`` は
   許されますが、 ``a*`` や ``a{3,4}`` は許されません。グループ参照は
   固定長の文字列にマッチするときでさえサポートされません。肯定後読み
   アサーションで始まるパターンは、検索される文字列の先頭とは決してマッチ
   しないことに注意して下さい; この表現を使用するのは、おそらく :func:`match` 関数
   より :func:`search` 関数の方が適しています:

      >>> import re
      >>> m = re.search('(?<=abc)def', 'abcdef')
      >>> m.group(0)
      'def'

   この例ではハイフンに続く単語を探します:

      >>> m = re.search('(?<=-)\w+', 'spam-egg')
      >>> m.group(0)
      'egg'

``(?<!...)``
   文字列内の現在位置の前に ``...`` とのマッチがない場合に、マッチします。
   これは :dfn:`否定後読みアサーション(negative lookbehind assertion)` と呼ばれます。
   肯定後読みアサーションと同様に、含まれるパターンは固定長さの文字列だけにマッチ
   しなければならず、グループ参照を含んではなりません。否定後読みアサーションで
   始まるパターンは、検索される文字列の先頭とマッチできます。

``(?(id/name)yes-pattern|no-pattern)``
   グループに *id* が与えられている、もしくは *name* があるとき、 ``yes-pattern``  と
   マッチします。存在しないときには ``no-pattern`` とマッチします。 ``no-pattern`` は
   オプションで省略できます。例えば
   ``(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)`` はemailアドレスとマッチする最低限のパターンです。
   これは ``'<user@host.com>'`` や ``'user@host.com'`` にはマッチしますが、
   ``'<user@host.com'``
   にはマッチしません。

   .. versionadded:: 2.4

特殊シーケンスは ``'\'`` と以下のリストにある文字から構成されます。もしリストにあるのが通常文字で
ないならば、結果の RE は2番目の文字とマッチします。例えば、 ``\$`` は文字 ``'$'`` とマッチします。

``\number``
   同じ番号のグループの中身とマッチします。グループは1から始まる番号をつけられます。
   例えば、 ``(.+) \1`` は、 ``'the the'`` あるいは ``'55 55'`` とマッチしますが、
   ``'thethe'`` とはマッチしません(グループの後のスペースに注意して下さい)。
   この特殊シーケンスは最初の 99 グループのうちの一つとマッチするのに使うことができるだけです。
   もし *number* の最初の桁が 0 である、すなわち *number* が 3 桁の8進数であれば、それは
   グループのマッチとは解釈されず、 8進数値 *number* を持つ文字として解釈されます。
   文字クラスの ``'['`` と ``']'`` の中の数値エスケープは、文字として扱われます。

``\A``
   文字列の先頭だけにマッチします。

``\b``
   空文字列とマッチしますが、単語の先頭か末尾の時だけです。単語は英数字あるいは下線文字の並んだ
   ものとして定義されていますので、単語の末尾は空白あるいは非英数字、非下線文字によって表されます。
   Note that formally, ``\b`` is defined as the boundary between a ``\w`` and
   a ``\W`` character (or vice versa), or between ``\w`` and the beginning/end
   of the string, so the precise set of characters deemed to be alphanumeric
   depends on the values of the ``UNICODE`` and ``LOCALE`` flags.
   For example, ``r'\bfoo\b'`` matches ``'foo'``, ``'foo.'``, ``'(foo)'``,
   ``'bar foo baz'`` but not ``'foobar'`` or ``'foo3'``.
   Inside a character range, ``\b`` represents the backspace character, for
   compatibility with Python's string literals.

..
   旧原文と旧訳
   Note that  ``\b`` is defined as the boundary between ``\w`` and ``\W``, so the
   precise set of characters deemed to be alphanumeric depends on the values of the
   ``UNICODE`` and ``LOCALE`` flags.  Inside a character range, ``\b`` represents
   the backspace character, for compatibility with Python's string literals.
   文字の正確な集合は、 ``UNICODE`` と ``LOCALE`` フラグの値に依存することに注意して下さい。
   文字の範囲の中では、 ``\b`` は、 Python の文字列リテラルと互換性を持たせるために、後退
   (backspace)文字を表します。

``\B``
   Matches the empty string, but only when it is *not* at the beginning or end of a
   word.  This means that ``r'py\B'`` matches ``'python'``, ``'py3'``, ``'py2'``,
   but not ``'py'``, ``'py.'``, or ``'py!'``.
   ``\B`` is just the opposite of ``\b``, so is also subject to the settings
   of ``LOCALE`` and ``UNICODE``.

..
   旧原文と旧訳
   Matches the empty string, but only when it is *not* at the beginning or end of a
   word.  This is just the opposite of ``\b``, so is also subject to the settings
   of ``LOCALE`` and ``UNICODE``.
   空文字列とマッチしますが、それが単語の先頭あるいは末尾に *ない* 時だけです。
   これは ``\b`` のちょうど反対ですので、同じように ``LOCALE`` と ``UNICODE``
   の設定に影響されます。

``\d``
   :const:`UNICODE` フラグが指定されていない場合、任意の十進数とマッチします；これは集合
   ``[0-9]`` と同じ意味です。
   :const:`UNICODE` がある場合、Unicode 文字特性データベースで十進数字と分類されているものに
   マッチします。

``\D``
   :const:`UNICODE` フラグが指定されていない場合、任意の非数字文字とマッチします；これは集合
   ``[^0-9]`` と同じ意味です。 :const:`UNICODE` がある場合、これは Unicode 文字特性データ
   ベースで数字とマーク付けされている文字以外にマッチします。

``\s``
   When the :const:`UNICODE` flag is not specified, it matches any whitespace
   character, this is equivalent to the set ``[ \t\n\r\f\v]``. The
   :const:`LOCALE` flag has no extra effect on matching of the space.
   If :const:`UNICODE` is set, this will match the characters ``[ \t\n\r\f\v]``
   plus whatever is classified as space in the Unicode character properties
   database.

..
   旧原文と旧訳
   When the :const:`LOCALE` and :const:`UNICODE` flags are not specified, matches
   any whitespace character; this is equivalent to the set ``[ \t\n\r\f\v]``. With
   :const:`LOCALE`, it will match this set plus whatever characters are defined as
   space for the current locale. If :const:`UNICODE` is set, this will match the
   characters ``[ \t\n\r\f\v]`` plus whatever is classified as space in the Unicode
   character properties database.
   :const:`LOCALE` と :const:`UNICODE` フラグが指定されていない場合、任意の空白文字とマッチ
   します；これは集合 ``[ \t\n\r\f\v]`` と同じ意味です。

   :const:`LOCALE` がある場合、これはこの集合に加えて現在のロケールで空白と定義されている全てに
   マッチします。 :const:`UNICODE` が設定されると、これは ``[ \t\n\r\f\v]`` と Unicode
   文字特性データベースで空白と分類されている全てにマッチします。

``\S``
   When the :const:`UNICODE` flag is not specified, matches any non-whitespace
   character; this is equivalent to the set ``[^ \t\n\r\f\v]`` The
   :const:`LOCALE` flag has no extra effect on non-whitespace match.  If
   :const:`UNICODE` is set, then any character not marked as space in the
   Unicode character properties database is matched.

..
   旧原文と旧訳
   When the :const:`LOCALE` and :const:`UNICODE` flags are not specified, matches
   any non-whitespace character; this is equivalent to the set ``[^ \t\n\r\f\v]``
   With :const:`LOCALE`, it will match any character not in this set, and not
   defined as space in the current locale. If :const:`UNICODE` is set, this will
   match anything other than ``[ \t\n\r\f\v]`` and characters marked as space in
   the Unicode character properties database.
   :const:`LOCALE` と :const:`UNICODE` がフラグが指定されていない場合、任意の非空白文字と
   マッチします；これは集合 ``[^ \t\n\r\f\v]`` と同じ意味です。 :const:`LOCALE` がある場合、
   これはこの集合に無い文字と、現在のロケールで空白と定義されていない文字にマッチします。
   :const:`UNICODE` が設定されていると、 ``[ \t\n\r\f\v]`` でない文字と、
   Unicode 文字特性データベースで空白とマーク付けされていないものにマッチします。

``\w``
   :const:`LOCALE` と :const:`UNICODE` フラグが指定されていない時は、任意の英数文字および
   下線とマッチします；これは、集合 ``[a-zA-Z0-9_]`` と同じ意味です。 :const:`LOCALE` が設定
   されていると、集合 ``[0-9_]`` プラス現在のロケール用に英数字として定義されている任意の文字と
   マッチします。もし :const:`UNICODE` が設定されていれば、文字 ``[0-9_]`` プラス Unicode
   文字特性データベースで英数字として分類されているものとマッチします。

``\W``
   When the :const:`LOCALE` and :const:`UNICODE` flags are not specified, matches
   any non-alphanumeric character; this is equivalent to the set ``[^a-zA-Z0-9_]``.
   With :const:`LOCALE`, it will match any character not in the set ``[0-9_]``, and
   not defined as alphanumeric for the current locale. If :const:`UNICODE` is set,
   this will match anything other than ``[0-9_]`` plus characters classified as
   not alphanumeric in the Unicode character properties database.
..
   旧原文と旧訳
   When the :const:`LOCALE` and :const:`UNICODE` flags are not specified, matches
   any non-alphanumeric character; this is equivalent to the set ``[^a-zA-Z0-9_]``.
   With :const:`LOCALE`, it will match any character not in the set ``[0-9_]``, and
   not defined as alphanumeric for the current locale. If :const:`UNICODE` is set,
   this will match anything other than ``[0-9_]`` and characters marked as
   alphanumeric in the Unicode character properties database.
   :const:`LOCALE` と :const:`UNICODE` フラグが指定されていない時、任意の非英数文字とマッチ
   します；これは集合 ``[^a-zA-Z0-9_]`` と同じ意味です。 :const:`LOCALE` が指定されていると、
   集合 ``[0-9_]`` になく、現在のロケールで英数字として定義されていない任意の文字とマッチします。
   もし :const:`UNICODE` がセットされていれば、これは ``[0-9_]`` および Unicode 文字特性
   データベースで英数字として表されている文字以外のものとマッチします。

``\Z``
   文字列の末尾とのみマッチします。

.. 以下 If both 部分、新規追加部分なので訳出忘れずに。

If both :const:`LOCALE` and :const:`UNICODE` flags are included for a
particular sequence, then :const:`LOCALE` flag takes effect first followed by
the :const:`UNICODE`.

Python 文字列リテラルによってサポートされている標準エスケープのほとんども、正規表現パーザに認識
されます::

   \a      \b      \f      \n
   \r      \t      \v      \x
   \\

.. 以下新規追加なので訳出忘れずに。

(Note that ``\b`` is used to represent word boundaries, and means "backspace"
only inside character classes.)


8進エスケープは制限された形式で含まれています：もし第1桁が 0 であるか、もし8進3桁であれば、それは
8進エスケープとみなされます。
そうでなければ、それはグループ参照です。文字列リテラルについて、 8進エスケープはほとんどの場合3桁長
になります。

.. seealso::

   Mastering Regular Expressions 詳説正規表現
      Jeffrey Friedl 著、O'Reilly 刊の正規表現に関する本です。この本の第2版\
      ではPyhonについては触れていませんが、良い正規表現パターンの書き方を非常に\
      くわしく説明しています。



.. _contents-of-module-re:



モジュールコンテンツ
---------------------

このモジュールは幾つかの関数、定数、例外を定義します。この関数のいくつかはコンパイル済み
正規表現向けの完全版のメソッドを簡略化したバージョンです。
それなりのアプリケーションのほとんどで、コンパイルされた形式が用いられるのが普通です。


.. function:: compile(pattern, flags=0)

   正規表現パターンを正規表現オブジェクトにコンパイルします。このオブジェクトは、以下で述べる
   :func:`~RegexObject.match` と :func:`~RegexObject.search` メソッドを使って、マッチングに使うことができます。

   式の動作は、 *flags* の値を指定することで加減することができます。値は以下の変数を、ビットごとの
   OR ( ``|`` 演算子)を使って組み合わせることができます。

   シーケンス ::

      prog = re.compile(pattern)
      result = prog.match(string)

   は、 ::

      result = re.match(pattern, string)

   と同じ意味ですが、 :func:`re.compile` を使ってその結果の正規表現オブジェクトを
   再利用した方が、その式を一つのプログラムで何回も使う時にはより効率的です。

   .. note::

      最後に :func:`re.match`, :func:`re.search`, :func:`re.compile` に渡されたパターンのコンパイル
      されたものがキャッシュとして残ります。そのため、正規表現をひとつだけしか使わないプログラムは
      正規表現のコンパイルを気にする必要はありません。


.. data:: DEBUG

   コンパイルした表現に関するデバッグ情報を出力します。



.. data:: I
          IGNORECASE

   大文字・小文字を区別しないマッチングを実行します； ``[A-Z]`` のような式は、小文字にもマッチします。
   これは現在のロケールには影響されません。


.. data:: L
          LOCALE

   ``\w`` 、 ``\W`` 、 ``\b`` および、 ``\B`` 、 ``\s`` と ``\S`` を、現在のロケールに従わさせます。


.. data:: M
          MULTILINE

   指定されると、パターン文字 ``'^'`` は、文字列の先頭および各行の先頭(各改行の直後)とマッチします；
   そしてパターン文字 ``'$'`` は文字列の末尾および各行の末尾 (改行の直前) とマッチします。デフォルト
   では、 ``'^'`` は、文字列の先頭とだけマッチし、 ``'$'`` は、文字列の末尾および文字列の末尾の
   改行の直前(がもしあれば)とマッチします。


.. data:: S
          DOTALL

   特殊文字 ``'.'`` を、改行を含む任意の文字と、とにかくマッチさせます；このフラグがなければ、
   ``'.'`` は、改行 *以外の* 任意の文字とマッチします。


.. data:: U
          UNICODE

   ``\w`` 、 ``\W`` 、 ``\b`` 、 ``\B`` 、 ``\d`` 、 ``\D`` 、 ``\s`` と ``\S`` を、 Unicode
   文字特性データベースに従わさせます。

   .. versionadded:: 2.0


.. data:: X
          VERBOSE

   このフラグによって、より見やすく正規表現を書くことができます。パターン内の
   空白は、文字クラス内にあるかエスケープされていないバックスラッシュが
   前にある時以外は無視されます。また、行に、文字クラス内にもなく、エスケープ
   されていないバックスラッシュが前にもない ``'#'`` がある時は、そのような
   ``'#'`` の左端からその行の末尾までが無視されます。

   つまり、数字にマッチする下記のふたつの正規表現オブジェクトは、機能的に等価です。::

      a = re.compile(r"""\d +  # 整数部
                         \.    # 小数点
                         \d *  # 小数点以下""", re.X)
      b = re.compile(r"\d+\.\d*")

.. function:: search(pattern, string, flags=0)

   *string* 全体を走査して、正規表現 *pattern* がマッチを発生する最初の位置を探して、対応する
   :class:`MatchObject` インスタンスを返します。
   もし文字列内に、そのパターンとマッチする位置がないならば、 ``None`` を返します；
   これは、文字列内のある点で長さゼロのマッチを探すこととは異なることに注意して下さい。


.. function:: match(pattern, string, flags=0)

   もし *string* の先頭で 0 個以上の文字が正規表現 *pattern* とマッチすれば、対応する
   :class:`MatchObject` インスタンスを返します。もし文字列がパターンとマッチしなければ、
   ``None`` を返します；
   これは長さゼロのマッチとは異なることに注意して下さい。

   Note that even in :const:`MULTILINE` mode, :func:`re.match` will only match
   at the beginning of the string and not at the beginning of each line.

   If you want to locate a match anywhere in *string*, use :func:`search`
   instead (see also :ref:`search-vs-match`).

..
   旧原文と翻訳
   .. note::

      If you want to locate a match anywhere in *string*, use :func:`search`
      instead.
   .. note::

      もし *string* のどこかにマッチを位置付けたいのであれば、代わりに
      :func:`search` を使って下さい。


.. function:: split(pattern, string, maxsplit=0, flags=0)

   *string* を、 *pattern* があるたびに分割します。もし括弧のキャプチャが *pattern* で使われていれば、
   パターン内のすべてのグループのテキストも結果のリストの一部として返されます。 *maxsplit* がゼロでなければ、
   高々 *maxsplit* 個の分割が発生し、文字列の残りは、リストの最終要素として返されます。
   (非互換性ノート：オリジナルの Python 1.5 リリースでは、
   *maxsplit* は無視されていました。これはその後のリリースでは修正されました。)

      >>> re.split('\W+', 'Words, words, words.')
      ['Words', 'words', 'words', '']
      >>> re.split('(\W+)', 'Words, words, words.')
      ['Words', ', ', 'words', ', ', 'words', '.', '']
      >>> re.split('\W+', 'Words, words, words.', 1)
      ['Words', 'words, words.']
      >>> re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE)
      ['0', '3', '9']

   もし、捕捉するグループが分割パターンに含まれ、それが文字列の先頭にあるならば、
   分割結果は、空文字列から始まります。文字列最後においても同様です。

      >>> re.split('(\W+)', '...words, words...')
      ['', '...', 'words', ', ', 'words', '...', '']

   その場合、常に、分割要素が、分割結果のリストの相対的なインデックスに現れます。
   (例えば、分割子の中に捕捉するグループが一つだけあれば、0番目、2番目、そして、4番目です)

   *split* は空のパターンマッチでは、文字列を分割しないことに注意して下さい。
   例えば:

      >>> re.split('x*', 'foo')
      ['foo']
      >>> re.split("(?m)^$", "foo\n\nbar\n")
      ['foo\n\nbar\n']

   .. versionchanged:: 2.7
      オプションの flags 引数が追加されました。


.. function:: findall(pattern, string, flags=0)

   *pattern* の *string* へのマッチのうち、重複しない全てのマッチを文字列のリストとして返します。
   *string* は左から右へと走査され、マッチは見つかった順番で返されます。
   パターン中に何らかのグループがある場合、グループのリストを返します。
   グループが複数定義されていた場合、タプルのリストになります。他のマッチの開始部分に接触しないかぎり、
   空のマッチも結果に含められます。

   .. versionadded:: 1.5.2

   .. versionchanged:: 2.4
      オプションの flags 引数を追加しました.


.. function:: finditer(pattern, string, flags=0)

   *string* 内の RE *pattern* の重複しないマッチを :class:`MatchObject` インスタンス
   を返す :term:`iterator` を返します。
   *string* は左から右へと走査され、マッチは見つかった順番で返されます。
   他のマッチの開始部分に接触しないかぎり、空のマッチも結果に含められます。


   .. versionadded:: 2.2

   .. versionchanged:: 2.4
      Added the optional flags argument.


.. function:: sub(pattern, repl, string, count=0, flags=0)

   *string* 内で、 *pattern* と重複しないマッチの内、一番左にあるものを置換 *repl* で置換して
   得られた文字列を返します。もしパターンが見つからなければ、 *string* を変更せずに返します。 *repl*
   は文字列でも関数でも構いません；
   もしそれが文字列であれば、それにある任意のバックスラッシュエスケープは処理されます。
   すなわち、 ``\n`` は単一の改行文字に変換され、 ``\r`` は、キャリッジリターンに変換されます、等々。
   ``\j`` のような未知のエスケープはそのままにされます。
   ``\6`` のような後方参照(backreference)は、パターンのグループ 6 とマッチしたサブ文字列で置換されます。
   例えば:

      >>> re.sub(r'def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s* \(\s*\):',
      ...        r'static PyObject*\npy_\1(void)\n{',
      ...        'def myfunc():')
      'static PyObject*\npy_myfunc(void)\n{'

   もし *repl* が関数であれば、重複しない *pattern* が発生するたびにその関数が呼ばれます。
   この関数は一つのマッチオブジェクト引数を取り、置換文字列を返します。例えば:

      >>> def dashrepl(matchobj):
      ...     if matchobj.group(0) == '-': return ' '
      ...     else: return '-'
      >>> re.sub('-{1,2}', dashrepl, 'pro----gram-files')
      'pro--gram files'
      >>> re.sub(r'\sAND\s', ' & ', 'Baked Beans And Spam', flags=re.IGNORECASE)
      'Baked Beans & Spam'

   パターンは、文字列でも RE オブジェクトでも構いません。

   省略可能な引数 *count* は、置換されるパターンの出現回数の最大値です； *count* は非負の整数で
   なければなりません。
   もし省略されるかゼロであれば、出現したものがすべて置換されます。パターンのマッチが空であれば、
   以前のマッチと隣合わせでない時だけ置換されますので、 ``sub('x*', '-', 'abc')`` は
   ``'-a-b-c-'`` を返します。

   In string-type *repl* arguments, in addition to the character escapes and
   backreferences described above,
   ``\g<name>`` will use the substring matched by the group named ``name``, as
   defined by the ``(?P<name>...)`` syntax. ``\g<number>`` uses the corresponding
   group number; ``\g<2>`` is therefore equivalent to ``\2``, but isn't ambiguous
   in a replacement such as ``\g<2>0``.  ``\20`` would be interpreted as a
   reference to group 20, not a reference to group 2 followed by the literal
   character ``'0'``.  The backreference ``\g<0>`` substitutes in the entire
   substring matched by the RE.

   ..
       旧原文と旧訳(In addition toの部分だけ違う)
       In addition to character escapes and backreferences as described above,
       ``\g<name>`` will use the substring matched by the group named ``name``, as
       defined by the ``(?P<name>...)`` syntax. ``\g<number>`` uses the corresponding
       group number; ``\g<2>`` is therefore equivalent to ``\2``, but isn't ambiguous
       in a replacement such as ``\g<2>0``.  ``\20`` would be interpreted as a
       reference to group 20, not a reference to group 2 followed by the literal
       character ``'0'``.  The backreference ``\g<0>`` substitutes in the entire
       substring matched by the RE.
       上で述べた文字エスケープや後方参照の他に、 ``\g<name>`` は、 ``(?P<name>...)`` のシンタクスで定義されているように、
       ``name`` という名前のグループとマッチしたサブ文字列を使います。 ``\g<number>`` は対応するグループ番号を使います；それゆえ
       ``\g<2>`` は ``\2`` と同じ意味ですが、 ``\g<2>0`` のような置換でもあいまいではありません。 ``\20`` は、グループ 20
       への参照として解釈されますが、グループ 2 にリテラル文字 ``'0'`` が続いたものへの参照としては解釈されません。後方参照  ``\g<0>`` は、
       RE とマッチするサブ文字列全体を置き換えます。

   .. versionchanged:: 2.7
      オプションの flags 引数が追加されました。

   
.. function:: subn(pattern, repl, string, count=0, flags=0)

   :func:`sub` と同じ操作を行いますが、タプル ``(new_string、 number_of_subs_made)`` を返します。

   .. versionchanged:: 2.7
      オプションの flags 引数が追加されました。

   
.. function:: escape(string)

   バックスラッシュにすべての非英数字をつけた *string* を返します；これはもし、その中に正規表現のメタ文字を持つかもしれない任意のリテラル文字列と
   マッチしたいとき、役に立ちます。


.. function:: purge()

   .. Clear the regular expression cache.

   正規表現キャッシュをクリアします。


.. exception:: error

   ここでの関数の一つに渡された文字列が、正しい正規表現ではない時 (例えば、その括弧が対になっていなかった)、あるいはコンパイルや
   マッチングの間になんらかのエラーが発生したとき、発生する例外です。たとえ文字列がパターンとマッチしなくても、決してエラーではありません。


.. _re-objects:

正規表現オブジェクト
--------------------

.. class:: RegexObject

   :class:`RegexObject` クラスは以下のメソッドと属性をサポートします:

   .. method:: RegexObject.search(string[, pos[, endpos]])

      *string* を走査して、この正規表現がマッチする場所を探し、対応する
      :class:`MatchObject` インスタンスを返します。
      string のどこにもマッチしない場合は ``None`` を返します。これは、 string
      内のどこかで長さ0でマッチした場合と異なることに注意してください。

      省略可能な、2つ目の引数 *pos* は、 string のどこから探し始めるかを指定する
      index で、デフォルトでは 0 です。これは、文字列をスライスしてから検索するのと、
      完全には同じではありません。パターン文字 ``'^'`` は本当の文字列の先頭と、
      改行の直後にマッチしますが、検索を開始する index がマッチするとは限りません。

      省略可能な引数 *endpos* は string のどこまでを検索するかを制限します。
      これは string の長さが *endpos* 文字だった場合と同じように動作します。
      つまり、 *pos* から ``endpos - 1`` の範囲の文字に対してパターンマッチします。
      *endpos* が *pos* よりも小さい場合は、マッチは見つかりません。
      それ以外の場合は、 *rx* がコンパイルされた正規表現として、
      ``rx.search(string, 0, 50)`` は ``rx.search(string[:50], 0)`` と同じです。

      >>> pattern = re.compile("d")
      >>> pattern.search("dog")     # Match at index 0
      <_sre.SRE_Match object at ...>
      >>> pattern.search("dog", 1)  # No match; search doesn't include the "d"

   .. method:: RegexObject.match(string[, pos[, endpos]])

      もし *string* の **先頭の** 0 個以上の文字がこの正規表現とマッチすれば、
      対応する :class:`MatchObject` インスタンスを返します。
      もし文字列がパタンーとマッチしなければ、 ``None`` を返します。
      これは長さゼロのマッチとは異なることに注意して下さい。

      省略可能な引数 *pos* と *endpos* 引数は、 :meth:`~RegexObject.search`
      メソッドと同じ意味を持ちます。

      >>> pattern = re.compile("o")
      >>> pattern.match("dog")      # "o" は文字列 "dog." の先頭にないため、マッチしません
      >>> pattern.match("dog", 1)   # "o" が文字列 "dog" の2番目にあるので、マッチします
      <_sre.SRE_Match object at ...>

      *string* のどこにでもマッチさせたければ、代わりに :meth:`~RegexObject.search` を
      使って下さい( :ref:`search-vs-match`) も参照してください)。


   .. method:: RegexObject.split(string, maxsplit=0)

      :func:`split` 関数と同様で、コンパイルしたパターンを使います。
      ただし、 :meth:`match` と同じように、省略可能な *pos*, *endpos*
      引数で検索範囲を指定することができます。


   .. method:: RegexObject.findall(string[, pos[, endpos]])

      :func:`findall` 関数と同様で、コンパイルしたパターンを使います。
      ただし、 :meth:`match` と同じように、省略可能な *pos*, *endpos*
      引数で検索範囲を指定することができます。


   .. method:: RegexObject.finditer(string[, pos[, endpos]])

      :func:`finditer` 関数と同様で、コンパイルしたパターンを使います。
      ただし、 :meth:`match` と同じように、省略可能な *pos*, *endpos*
      引数で検索範囲を指定することができます。


   .. method:: RegexObject.sub(repl, string, count=0)

      :func:`sub` 関数と同様で、コンパイルしたパターンを使います。


   .. method:: RegexObject.subn(repl, string, count=0)

      :func:`subn` 関数と同様で、コンパイルしたパターンを使います。


   .. attribute:: RegexObject.flags

      The regex matching flags.  This is a combination of the flags given to
      :func:`.compile` and any ``(?...)`` inline flags in the pattern.

      ..
        旧原文と旧訳
        The flags argument used when the RE object was compiled, or ``0`` if no flags
        were provided.
        RE オブジェクトがコンパイルされたとき使われた flags 引数です。
        もし flags が何も提供されなければ ``0`` です。


   .. attribute:: RegexObject.groups

      パターンにあるキャプチャグループの数です。


   .. attribute:: RegexObject.groupindex

      ``(?P<id>)`` で定義された任意の記号グループ名の、グループ番号への辞書マッピングです。もし記号グループが
      パターン内で何も使われていなければ、辞書は空です。


   .. attribute:: RegexObject.pattern

      RE オブジェクトがそれからコンパイルされたパターン文字列です。


.. _match-objects:

MatchObject オブジェクト
------------------------

.. class:: MatchObject

   Match objects always have a boolean value of ``True``.
   Since :meth:`~regex.match` and :meth:`~regex.search` return ``None``
   when there is no match, you can test whether there was a match with a simple
   ``if`` statement::

      match = re.search(pattern, string)
      if match:
          process(match)

   Match objects support the following methods and attributes:

   ..
      旧原文と旧訳
      Match Objects always have a boolean value of :const:`True`, so that you can test
      whether e.g. :func:`match` resulted in a match with a simple if statement.  They
      support the following methods and attributes:
      :class:`MatchObject` は、常に真偽値 :const:`True` を持ちます。
      そのため、例えば :func:`match` がマッチしたかどうかを単純な if 文で確認する
      ことができます。
      :class:`MatchObject` は以下のメソッドと、属性を持ちます。


   .. method:: MatchObject.expand(template)

      テンプレート文字列 *template* に、 :meth:`~RegexObject.sub` メソッドが
      するようなバックスラッシュ置換をして得られる文字列を返します。
      ``\n`` のようなエスケープは適当な文字に変換され、数値の後方参照
      (``\1``, ``\2``) と名前付きの後方参照 (``\g<1>``, ``\g<name>``) は、
      対応するグループの内容で置き換えられます。


   .. method:: MatchObject.group([group1, ...])

      マッチした1個以上のサブグループを返します。
      もし引数で一つであれば、その結果は一つの文字列です。複数の引数があれば、
      その結果は、引数ごとに一項目を持つタプルです。引数がなければ、 *group1*
      はデフォールトでゼロです(マッチしたものすべてが返されます)。
      もし *groupN* 引数がゼロであれば、対応する戻り値は、マッチする文字列
      全体です。
      もしそれが範囲 [1..99] 内であれば、それは、対応する丸括弧つきグループと
      マッチする文字列です。もしグループ番号が負であるか、あるいはパターンで
      定義されたグループの数より大きければ、 :exc:`IndexError` 例外が発生します。
      グループがマッチしなかったパターンの一部に含まれていれば、対応する結果は
      ``None`` です。グループが、複数回マッチしたパターンの一部に含まれて
      いれば、最後のマッチが返されます。

         >>> m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
         >>> m.group(0)       # マッチした全体
         'Isaac Newton'
         >>> m.group(1)       # ひとつめのパターン化されたサブグループ
         'Isaac'
         >>> m.group(2)       # ふたつめのパターン化されたサブグループ
         'Newton'
         >>> m.group(1, 2)    # 複数の引数を与えるとタプルが返る
         ('Isaac', 'Newton')

      もし正規表現が ``(?P<name>...)`` シンタックスを使うならば、 *groupN*
      引数は、それらのグループ名によってグループを識別する文字列であっても
      構いません。
      もし文字列引数がパターンのグループ名として使われていないものであれば、
      :exc:`IndexError` 例外が発生します。

      適度に複雑な例題:

         >>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcom Reynolds")
         >>> m.group('first_name')
         'Malcom'
         >>> m.group('last_name')
         'Reynolds'

      名前の付けられたグループは、そのインデックスによっても参照できます。

         >>> m.group(1)
         'Malcom'
         >>> m.group(2)
         'Reynolds'

      もし、グループが複数回マッチする場合、最後のマッチだけが利用可能となります。

         >>> m = re.match(r"(..)+", "a1b2c3")  # 3回マッチする
         >>> m.group(1)                        # 最後のマッチだけが返る
         'c3'


   .. method:: MatchObject.groups([default])

      マッチの、1からパターン内にある全グループ数までのすべてのサブグループを
      含むタプルを返します。
      *default* 引数は、マッチに加わらなかったグループ用に使われ、
      デフォールトでは ``None`` です。
      (非互換性ノート：オリジナルの Python 1.5 リリースでは、
      たとえタプルが一要素長であっても、その代わりに文字列を返していました。
      (1.5.1 以降の)後のバージョンでは、そのような場合には、要素がひとつの
      タプルが返されます。)

      例えば:

         >>> m = re.match(r"(\d+)\.(\d+)", "24.1632")
         >>> m.groups()
         ('24', '1632')

      もし、整数部にのみ着目し、あとの部分をオプションとした場合、
      マッチの中に現れないグループがあるかも知れません。
      それらのグループは、 *default* 引数が与えられていない場合、デフォルトでは
      ``None`` になります。

         >>> m = re.match(r"(\d+)\.?(\d+)?", "24")
         >>> m.groups()      # ふたつめのグループはデフォルトでは None になる
         ('24', None)
         >>> m.groups('0')   # この場合、ふたつめのグループのデフォルトは 0 になる
         ('24', '0')


   .. method:: MatchObject.groupdict([default])

      マッチの、すべての *名前つきの* サブグループを含む、サブグループ名でキー付けされた
      辞書を返します。 *default* 引数はマッチに加わらなかったグループに使われ、
      デフォールトでは ``None`` です。例えば、

         >>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcom Reynolds")
         >>> m.groupdict()
         {'first_name': 'Malcom', 'last_name': 'Reynolds'}


   .. method:: MatchObject.start([group])
               MatchObject.end([group])

      *group* とマッチした部分文字列の先頭と末尾のインデックスを返します。
      *group* は、デフォルトでは(マッチした部分文字列全体を意味する）ゼロです。
      *group* が存在してもマッチに寄与しなかった場合は、 ``-1`` を返します。
      マッチオブジェクト *m* および、マッチに寄与しなかったグループ *g* があって、
      グループ *g* とマッチしたサブ文字列 ( ``m.group(g)`` と同じ意味ですが ) は::

         m.string[m.start(g):m.end(g)]

      です。もし *group* が空文字列とマッチすれば、 ``m.start(group)`` が
      ``m.end(group)`` と等しくなることに注意して下さい。例えば、
      ``m = re.search('b(c?)', 'cba')`` とすると、 ``m.start(0)`` は 1 で、
      ``m.end(0)`` は 2 であり、 ``m.start(1)`` と ``m.end(1)`` は
      ともに 2 であり、 ``m.start(2)`` は :exc:`IndexError` 例外を発生します。

      例として、電子メールのアドレスから *remove_this* を取り除く場合を示します。

         >>> email = "tony@tiremove_thisger.net"
         >>> m = re.search("remove_this", email)
         >>> email[:m.start()] + email[m.end():]
         'tony@tiger.net'


   .. method:: MatchObject.span([group])

      :class:`MatchObject` *m* について、大きさ2のタプル
      ``(m.start(group), m.end(group))`` を返します。
      もし *group* がマッチに寄与しなかったら、これは ``(-1, -1)`` です。
      また *group* はデフォルトでゼロです。


   .. attribute:: MatchObject.pos

      :class:`RegexObject` の :meth:`~RegexObject.search` か
      :meth:`~RegexObject.match` に渡された *pos* の値です。
      これは RE エンジンがマッチを探し始める位置の文字列のインデックスです。


   .. attribute:: MatchObject.endpos

      :class:`RegexObject` の :meth:`~RegexObject.search` か
      :meth:`~RegexObject.match` に渡された *endpos* の値です。
      これは RE エンジンがそれ以上は進まない位置の文字列のインデックスです。


   .. attribute:: MatchObject.lastindex

      最後にマッチした取り込みグループの整数インデックスです。
      もしどのグループも全くマッチしなければ ``None`` です。
      例えば、 ``(a)b``, ``((a)(b))`` や  ``((ab))`` といった表現が ``'ab'`` に適用された場合、
      ``lastindex == 1``  となり、同じ文字列に ``(a)(b)`` が適用された場合には ``lastindex == 2``
      となるでしょう。


   .. attribute:: MatchObject.lastgroup

      最後にマッチした取り込みグループの名前です。もしグループに名前がないか、
      あるいはどのグループも全くマッチしなければ ``None`` です。


   .. attribute:: MatchObject.re

      この :class:`MatchObject` インスタンスを :meth:`~RegexObject.match`
      あるいは :meth:`~RegexObject.search` メソッドで生成した正規表現
      オブジェクトです。


   .. attribute:: MatchObject.string

      :meth:`~RegexObject.match` あるいは :meth:`~RegexObject.search`
      に渡された文字列です。


例
--


ペアの確認
^^^^^^^^^^^

この例では、マッチオブジェクトの表示を少し美しくするために、下記の補助関数を使用します :

.. testcode::

   def displaymatch(match):
       if match is None:
           return None
       return '<Match: %r, groups=%r>' % (match.group(), match.groups())

あなたがポーカープログラムを書いているとします。プレイヤーの持ち札はそれぞれの文字が1枚のカードを
意味する5文字の文字列によって表現されます。
"a" はエース、 "k" はキング、 "q" はクイーン、 "j" はジャック "t" は10、そして "2" から
"9" はそれぞれの数字のカードを表します。

与えられた文字列が、持ち札として有効かを確認するために、下記のようにするかも知れません。 :

   >>> valid = re.compile(r"^[a2-9tjqk]{5}$")
   >>> displaymatch(valid.match("akt5q"))  # Valid.
   "<Match: 'akt5q', groups=()>"
   >>> displaymatch(valid.match("akt5e"))  # Invalid.
   >>> displaymatch(valid.match("akt"))    # Invalid.
   >>> displaymatch(valid.match("727ak"))  # Valid.
   "<Match: '727ak', groups=()>"

最後の持ち札 ``"727ak"`` は、ペアを含んでいます。言い換えると同じ値のカードが2枚あります。
これを正規表現にマッチさせるために、後方参照を使う場合もあります :

   >>> pair = re.compile(r".*(.).* \1")
   >>> displaymatch(pair.match("717ak"))     # 7 のペア
   "<Match: '717', groups=('7',)>"
   >>> displaymatch(pair.match("718ak"))     # ペア無し
   >>> displaymatch(pair.match("354aa"))     # エースのペア
   "<Match: '354aa', groups=('a',)>"

どのカードのペアになっているかを調べるため、下記のように :class:`MatchObject` の
:meth:`~RegexObject.group` メソッドを使う場合があります。

.. doctest::

   >>> pair.match("717ak").group(1)
   '7'

   # re.match() が group() メソッドを持たない None を返すため、エラーとなる :
   >>> pair.match("718ak").group(1)
   Traceback (most recent call last):
     File "<pyshell#23>", line 1, in <module>
       re.match(r".*(.).* \1", "718ak").group(1)
   AttributeError: 'NoneType' object has no attribute 'group'

   >>> pair.match("354aa").group(1)
   'a'


scanf() をシミュレートする
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: single: scanf()

Python には現在のところ、 :c:func:`scanf` に相当するものがありません。正規表現は、
:c:func:`scanf` のフォーマット文字列よりも、一般的により強力であり、また冗長でもあります。
以下の表に、 :c:func:`scanf` のフォーマットトークンと正規表現の大体同等な対応付けを示します。

+--------------------------------+---------------------------------------------+
| :c:func:`scanf` トークン       | 正規表現                                    |
+================================+=============================================+
| ``%c``                         | ``.``                                       |
+--------------------------------+---------------------------------------------+
| ``%5c``                        | ``.{5}``                                    |
+--------------------------------+---------------------------------------------+
| ``%d``                         | ``[-+]?\d+``                                |
+--------------------------------+---------------------------------------------+
| ``%e``, ``%E``, ``%f``, ``%g`` | ``[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?`` |
+--------------------------------+---------------------------------------------+
| ``%i``                         | ``[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)``     |
+--------------------------------+---------------------------------------------+
| ``%o``                         | ``[-+]?[0-7]+``                             |
+--------------------------------+---------------------------------------------+
| ``%s``                         | ``\S+``                                     |
+--------------------------------+---------------------------------------------+
| ``%u``                         | ``\d+``                                     |
+--------------------------------+---------------------------------------------+
| ``%x``, ``%X``                 | ``[-+]?(0[xX])?[\dA-Fa-f]+``                |
+--------------------------------+---------------------------------------------+

::

   /usr/sbin/sendmail - 0 errors, 4 warnings

のような文字列からファイル名と数値を抽出するには、 ::

   %s - %d errors, %d warnings

のように :c:func:`scanf` フォーマットを使うでしょう。それと同等な正規表現は ::

   (\S+) - (\d+) errors, (\d+) warnings


.. _search-vs-match:

search() vs. match()
^^^^^^^^^^^^^^^^^^^^

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

Python は正規表現ベースの 2 個の基本的な関数、文字列の先頭でのみのマッチを
確認する :func:`re.match` および、文字列内の位置にかかわらずマッチを
確認する :func:`re.search` (Perl でのデフォルトの挙動) を提供しています。

例えば::

   >>> re.match("c", "abcdef")  # No match
   >>> re.search("c", "abcdef") # Match
   <_sre.SRE_Match object at ...>

``'^'`` で始まる正規表現は、 :func:`search` において、マッチを文字列の先頭からに
制限するために使用します::

   >>> re.match("c", "abcdef")  # No match
   >>> re.search("^c", "abcdef") # No match
   >>> re.search("^a", "abcdef")  # Match
   <_sre.SRE_Match object at ...>

ただし、 :const:`MULTILINE` モードの :func:`match` では文字列の先頭にのみマッチするのに対し、
正規表現に ``'^'`` を使った :func:`search` では各行の先頭にもマッチします。

   >>> re.match('X', 'A\nB\nX', re.MULTILINE)  # No match
   >>> re.search('^X', 'A\nB\nX', re.MULTILINE)  # Match
   <_sre.SRE_Match object at ...>


電話帳の作成
^^^^^^^^^^^^

:func:`split` は文字列を与えられたパターンで分割し、リストにして返します。
下記の、電話帳作成の例のように、このメソッドはテキストデータを読みやすくしたり、 Python で編集
したりしやすくする際に、非常に役に立ちます。

最初に、入力を示します。通常、これはファイルからの入力になるでしょう。ここでは、3重引用符の書式
とします :

   >>> text = """Ross McFluff: 834.345.1254 155 Elm Street
   ...
   ... Ronald Heathmore: 892.345.3428 436 Finley Avenue
   ... Frank Burger: 925.541.7625 662 South Dogwood Way
   ...
   ...
   ... Heather Albrecht: 548.326.4584 919 Park Place"""

個々の記録は、1つ以上の改行で区切られています。まずは、文字列から空行を除き、記録ごとのリストに
変換しましょう。

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> entries = re.split("\n+", text)
   >>> entries
   ['Ross McFluff: 834.345.1254 155 Elm Street',
   'Ronald Heathmore: 892.345.3428 436 Finley Avenue',
   'Frank Burger: 925.541.7625 662 South Dogwood Way',
   'Heather Albrecht: 548.326.4584 919 Park Place']

そして、各記録を、名、姓、電話番号、そして、住所に分割してリストにします。
分割のためのパターンに使っている空白文字が、住所には含まれるため、 :func:`split` の
``maxsplit`` 引数を使います。 :


.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> [re.split(":? ", entry, 3) for entry in entries]
   [['Ross', 'McFluff', '834.345.1254', '155 Elm Street'],
   ['Ronald', 'Heathmore', '892.345.3428', '436 Finley Avenue'],
   ['Frank', 'Burger', '925.541.7625', '662 South Dogwood Way'],
   ['Heather', 'Albrecht', '548.326.4584', '919 Park Place']]

パターン、 ``:?`` は姓に続くコロンにマッチします。そのため、コロンは分割結果のリストには現れません。
``maxsplit`` を ``4`` にすれば、ハウスナンバーと、ストリート名を分割することができます。 :


.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> [re.split(":? ", entry, 4) for entry in entries]
   [['Ross', 'McFluff', '834.345.1254', '155', 'Elm Street'],
   ['Ronald', 'Heathmore', '892.345.3428', '436', 'Finley Avenue'],
   ['Frank', 'Burger', '925.541.7625', '662', 'South Dogwood Way'],
   ['Heather', 'Albrecht', '548.326.4584', '919', 'Park Place']]


テキストの秘匿
^^^^^^^^^^^^^^^

:func:`sub` はパターンにマッチした部分を文字列や関数の返り値で置き換えます。
この例では、"秘匿" する文字列に、関数と共に :func:`sub` を適用する例を示します。
言い換えると、最初と最後の文字を除く、単語中の文字の位置をランダム化します。 ::

   >>> def repl(m):
   ...   inner_word = list(m.group(2))
   ...   random.shuffle(inner_word)
   ...   return m.group(1) + "".join(inner_word) + m.group(3)
   >>> text = "Professor Abdolmalek, please report your absences promptly."
   >>> re.sub(r"(\w)(\w+)(\w)", repl, text)
   'Poefsrosr Aealmlobdk, pslaee reorpt your abnseces plmrptoy.'
   >>> re.sub(r"(\w)(\w+)(\w)", repl, text)
   'Pofsroser Aodlambelk, plasee reoprt yuor asnebces potlmrpy.'


全ての形容動詞を見つける
^^^^^^^^^^^^^^^^^^^^^^^^^

:func:`findall` はパターンにマッチする *全てに* マッチします。
:func:`search` がそうであるように、最初のものだけに、ではありません。
例えば、なにかの文章の全ての副詞を見つけたいとき、下記のように :func:`findall` を使います。 :

   >>> text = "He was carefully disguised but captured quickly by police."
   >>> re.findall(r"\w+ly", text)
   ['carefully', 'quickly']


全ての形容動詞と、その位置を見つける
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

もし、パターンにマッチするものについて、マッチしたテキスト以上の情報を得たいと考えたとき、
文字列ではなく :class:`MatchObject` のインスタンスを返す :func:`finditer` が便利です。
以下に例を示すように、なにかの文章の全ての副詞と、 *その位置を* 調べたいと考えたとき、
下記のように :func:`finditer` を使います。 :

   >>> text = "He was carefully disguised but captured quickly by police."
   >>> for m in re.finditer(r"\w+ly", text):
   ...     print '%02d-%02d: %s' % (m.start(), m.end(), m.group(0))
   07-16: carefully
   40-47: quickly


Raw String記法
^^^^^^^^^^^^^^

Raw string記法 (``r"text"``) により、バックスラッシュ (``'\'``) を個々にバックスラッシュで
エスケープすることなしに、正規表現を正常な状態に保ちます。
例えば、下記の2つのコードは機能的に等価です。 :

   >>> re.match(r"\W(.)\1\W", " ff ")
   <_sre.SRE_Match object at ...>
   >>> re.match("\\W(.)\\1\\W", " ff ")
   <_sre.SRE_Match object at ...>

文字通りのバックスラッシュにマッチさせたいなら、正規表現中ではエスケープする必要があります。
Raw string記法では、 ``r"\\"``  ということになります。
Raw string記法を用いない場合、 ``"\\\\"`` としなくてはなりません。
下記のコードは機能的に等価です。 :

   >>> re.match(r"\\", r"\\")
   <_sre.SRE_Match object at ...>
   >>> re.match("\\\\", r"\\")
   <_sre.SRE_Match object at ...>
