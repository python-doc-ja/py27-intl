
:mod:`string` --- 一般的な文字列操作
===========================

.. module:: string
   :synopsis: 一般的な文字列操作


.. index:: module: re

:mod:`string` モジュールには便利な定数やクラスが数多く入っています。 また、現在は文字列のメソッドとして利用できる、すでに撤廃された古い関数
も入っています。正規表現に関する文字列操作の関数は :mod:`re` を参照してください。


文字列定数
-----

このモジュールでは以下の定数を定義しています。


.. data:: ascii_letters

   後述の :const:`ascii_lowercase` と:const:`ascii_uppercase` を合わ せたもの。この値はロケールに依存しません。


.. data:: ascii_lowercase

   小文字 ``'abcdefghijklmnopqrstuvwxyz'``。この値はロケールに依存せ ず、固定です。


.. data:: ascii_uppercase

   大文字 ``'ABCDEFGHIJKLMNOPQRSTUVWXYZ'``。この値はロケールに依存せ ず、固定です。


.. data:: digits

   文字列 ``'0123456789'`` です。


.. data:: hexdigits

   文字列 ``'0123456789abcdefABCDEF'`` です。


.. data:: letters

   後述の :const:`lowercase` と :const:`uppercase` を合わせた文字列です。
   具体的な値はロケールに依存しており、:func:`locale.setlocale`  が呼ばれたときに更新されます。


.. data:: lowercase

   小文字として扱われる文字全てを含む文字列です。ほとんどのシステムでは 文字列 ``'abcdefghijklmnopqrstuvwxyz'``
   です。この定義を変更しては なりません --- 変更した場合の:func:`upper` と :func:`swapcase`
   に対する影響は定義されていません。具体的な値はロケールに依存しており、 :func:`locale.setlocale` が呼ばれたときに更新されます。


.. data:: octdigits

   文字列 ``'01234567'`` です。


.. data:: punctuation

   ``C`` ロケールにおいて、句読点として扱われる ASCII 文字の文字列です。


.. data:: printable

   印刷可能な文字で構成される文字列です。 :const:`digits`、:const:`letters`、:const:`punctuation` および
   :const:`whitespace` を組み合わせたものです。


.. data:: uppercase

   大文字として扱われる文字全てを含む文字列です。ほとんどのシステムでは  ``'ABCDEFGHIJKLMNOPQRSTUVWXYZ'``
   です。この定義を変更してはなりません ---- 変更した場合の:func:`lower` と :func:`swapcase` に対する
   影響は定義されていません。具体的な値はロケールに依存しており、   :func:`locale.setlocale` が呼ばれたときに更新されます。


.. data:: whitespace

   空白 (whitespace) として扱われる文字全てを含む文字列です。 ほとんどのシステムでは、これはスペース (space)、タブ (tab)、改行
   (linefeed)、 復帰 (return)、改頁 (formfeed)、垂直タブ (vertical tab) です。 この定義を変更してはなりません
   --- 変更した場合の:func:`strip` と :func:`split` に対する影響は定義されていません。


テンプレート文字列
---------

テンプレート (template) を使うと、:pep:`292`で解説されているように より簡潔に文字列置換 (string substitution)
を行えるようになります。 通常の``%`` ベースの置換に代わって、テンプレートでは以下のような 規則に従った``$``ベースの置換をサポートしています:

* ``$$`` はエスケープ文字です; ``$`` 一つに置換されます。

* ``$identifier`` は置換プレースホルダの指定で、 "identifier"
  というキーへの対応付けに相当します。デフォルトは、"identifier" の部分には Python の識別子が書かれていなければなりません。 ``$``
  の後に識別子に使えない文字が出現すると、そこでプレースホルダ名の 指定が終わります。

* ``${identifier}`` は``$identifier`` と同じです。 プレースホルダ名の後ろに識別子として使える文字列が続いていて、それを
  プレースホルダ名の一部として扱いたくない場合、例えば "${noun}ification" のような場合に必要な書き方です。

上記以外の書き方で文字列中に``$`` を使うと:exc:`ValueError`  を送出します。

.. versionadded:: 2.4

:mod:`string` モジュールでは、上記のような規則を実装した :class:`Template` クラスを提供しています。
:class:`Template` のメソッドを以下に示します:


.. class:: Template(template)

   コンストラクタはテンプレート文字列になる引数を一つだけ取ります。


.. method:: Template.substitute(mapping[, **kws])

   テンプレート置換を行い、新たな文字列を生成して返します。*mapping* は テンプレート中のプレースホルダに対応するキーを持つような任意の辞書類似
   オブジェクトです。辞書を指定する代わりに、キーワード引数も指定でき、その 場合にはキーワードをプレースホルダ名に対応させます。 *mapping* と
   *kws* の両方が指定され、内容が重複した場合には、 *kws* に指定したプレースホルダを優先します。


.. method:: Template.safe_substitute(mapping[, **kws])

   :meth:`substitute` と同じですが、プレースホルダに対応するものを *mapping* や *kws* から見つけられなかった場合に、
   :exc:`KeyError` 例外を送出する代わりにもとのプレースホルダが そのまま入ります。また、:meth:`substitute`とは違い、規則外の
   書き方で ``$`` を使った場合でも、:exc:`ValueError` を送出 せず単に ``$`` を返します。

   その他の例外も発生しうる一方で、このメソッドが「安全 (safe)」 と呼ばれているのは、置換操作が常に例外を送出する代わりに利用可能な
   文字列を返そうとしているからです。別の見方をすれば、 :meth:`safe_substitute` は区切り間違いによるぶら下がり (dangling
   delimiter) や波括弧の非対応、Python の識別子として無効な プレースホルダ名を含むような不正なテンプレートを何も警告せずに
   無視するため、安全とはいえないのです。

:class:`Template` のインスタンスは、次のような public な属性を 提供しています:


.. attribute:: string.template

   コンストラクタの引数 *template* に渡されたオブジェクトです。通常、 この値を変更すべきではありませんが、読み込み専用アクセスを強制している
   わけではありません。

Templateの使い方の例を以下に示します::

   >>> from string import Template
   >>> s = Template('$who likes $what')
   >>> s.substitute(who='tim', what='kung pao')
   'tim likes kung pao'
   >>> d = dict(who='tim')
   >>> Template('Give $who $100').substitute(d)
   Traceback (most recent call last):
   [...]
   ValueError: Invalid placeholder in string: line 1, col 10
   >>> Template('$who likes $what').substitute(d)
   Traceback (most recent call last):
   [...]
   KeyError: 'what'
   >>> Template('$who likes $what').safe_substitute(d)
   'tim likes $what'

さらに進んだ使い方: :class:`Template` のサブクラスを導出して、 プレースホルダの書式、区切り文字、テンプレート文字列の解釈に
使われている正規表現全体をカスタマイズできます。 こうした作業には、以下のクラス属性をオーバライドします:

.. % $

* *delimiter* -- プレースホルダの開始を示すリテラル文字列 です。デフォルトの値は ``$`` です。実装系はこの文字列に対して 必要に応じて
  :meth:`re.escape` を呼び出すので、正規表現を表す ような文字列にしては *なりません*。

* *idpattern* -- 波括弧でくくらない形式のプレースホルダ の表記パターンを示す正規表現です (波括弧は自動的に適切な場所に追加
  されます)。で尾フォルトの値は``[_a-z][_a-z0-9]*`` という 正規表現です。

他にも、クラス属性*pattern* をオーバライドして、正規表現パターン 全体を指定できます。オーバライドを行う場合、*pattern* の値は 4
つの名前つきキャプチャグループ (capturing group) を持った 正規表現オブジェクトでなければなりません。これらのキャプチャグループは、
上で説明した規則と、無効なプレースホルダに対する規則に対応しています:

* *escaped* -- このグループはエスケープシーケンス、すなわち デフォルトパターンにおける ``$$`` に対応します。

* *named* -- このグループは波括弧でくくらないプレースホルダ名に 対応します; キャプチャグループに区切り文字を含めてはなりません。

* *braced* -- このグループは波括弧でくくったプレースホルダ名に 対応します; キャプチャグループに区切り文字を含めてはなりません。

* *invalid* -- このグループはそのほかの区切り文字のパターン (通常は区切り文字一つ) に対応し、正規表現の末尾に出現せねばなりません。


文字列操作関数
-------

以下の関数は文字列またはUnicodeオブジェクトを操作できます。これらの関数は 文字列型のメソッドにはありません。


.. function:: capwords(s)

   :func:`split` を使って引数を単語に分割し、:func:`capitalize` を 使ってそれぞれの単語の先頭の文字を大文字に変換し、
   :func:`join`  を使ってつなぎ合わせます。 この置換処理は文字列中の連続する空白文字をスペース一つに置き換え、
   先頭と末尾の空白を削除するので注意してください。


.. function:: maketrans(from, to)

   :func:`translate` や :func:`regex.compile` に渡すのに適した 変換テーブルを返します。このテーブルは、 *from*
   内の各文字を *to* の同じ位置にある文字に対応付けます; *from* と *to* は同じ長さでなければなりません。

   .. warning::

      :const:`lowercase` と :const:`uppercase` から取り出した 文字列を引数に使ってはなりません;
      ロケールによっては、これらは同じ 長さになりません。大文字小文字の変換には、常に:func:`lower`  または
      :func:`upper`を使ってください。


撤廃された文字列関数
----------

以下の一連の関数は、文字列型や Unicode 型のオブジェクトのメソッドとしても 定義されています; 詳しくは "文字列型のメソッド" (:ref
:`string-methods`)を 参照してください。 ここに挙げた関数は Python 3.0 で削除されることはないはずですが、
撤廃された関数とみなして下さい。このモジュールで定義されている関数は以下の 通りです:


.. function:: atof(s)

   .. deprecated:: 2.0
      組み込み関数 :func:`float` を使ってください。

   .. index:: builtin: float

   文字列を浮動小数点型の数値に変換します。文字列は Python における 標準的なの浮動小数点リテラルの文法に従っていなければなりません。
   先頭に符号（``+`` または ``-``）が付くのは構いません。 この関数に文字列を渡した場合は、組み込み関数 :func:`float`
   と同じように振舞います。

   .. note::

      .. index::
         single: NaN
         single: Infinity

      文字列を渡した場合、根底にある C ライブラリによって NaN や Infinity を返す場合があります。
      こうした値を返させるのがどんな文字列の集合であるかは、全て C  ライブラリに依存しており、ライブラリによって異なると知られています。


.. function:: atoi(s[, base])

   .. deprecated:: 2.0
      組み込み関数 :func:`int` を使ってください。

   .. index:: builtin: eval

   文字列 *s* を、*base* を基数とする整数に変換します。  文字列は 1 桁またはそれ以上の数字からなっていなければなりません。 先頭に符号
   (``+`` または ``-``) が付くのは構いません。 *base* のデフォルト値は 10 です。 *base* が 0 の場合、
   (符号を剥ぎ取った後の) 文字列の先頭にある文字列に従ってデフォルトの 基数を決定します。``0x`` か ``0X`` なら 16、``0`` なら 8、
   その他の場合は 10 が基数になります。*base* が 16 の場合、先頭の ``0x`` や ``0X``
   が付いていても受け付けますが、必須ではありません。 文字列を渡す場合、この関数は組み込み関数 :func:`int` と同じように 振舞います。
   (数値リテラルをより柔軟に解釈したい場合には、組み込み関数 :func:`eval` を使ってください。)


.. function:: atol(s[, base])

   .. deprecated:: 2.0
      組み込み関数 :func:`long` を使ってください。

   .. index:: builtin: long

   文字列 *s* を、*base* を基数とする長整数に変換します。  文字列は 1 桁またはそれ以上の数字からなっていなければなりません。 先頭に符号
   (``+`` または ``-``) が付くのは構いません。 *base* は :func:`atoi` と同じ意味です。基数が 0 の場合を 除き、文字列末尾に
   ``l`` や``L`` を付けてはなりません。 *base* を指定しないか、10 を指定して文字列を渡した場合には、 この関数は組み込み関数
   :func:`long`  と同じように振舞います。


.. function:: capitalize(word)

   先頭文字だけ大文字にした *word* のコピーを返します。


.. function:: expandtabs(s[, tabsize])

   現在のカラムと指定タブ幅に従って文字列中のタブを展開し、 一つまたはそれ以上のスペースに置き換えます。文字列中に改行が出現する たびにカラム番号は 0
   にリセットされます。 この関数は、他の非表示文字やエスケープシーケンスを解釈しません。 タブ幅のデフォルトは 8 です。


.. function:: find(s, sub[, start[,end]])

   ``s[start:end]`` の中で、部分文字列 *sub* が 完全な形で入っている場所のうち、最初のものを *s* のインデクスで
   返します。見つからなかった場合は ``-1`` を返します。 *start* と *end* のデフォルト値、および、負の値を指定した
   場合の解釈は文字列のスライスと同じです。


.. function:: rfind(s, sub[, start[, end]])

   :func:`find` と同じですが、最後に見つかったもののインデックスを返 します。


.. function:: index(s, sub[, start[, end]])

   :func:`find` と同じですが、部分文字列が見つからなかったときに   :exc:`ValueError` を送出します。


.. function:: rindex(s, sub[, start[, end]])

   :func:`rfind` と同じですが、部分文字列が見つからなかったときに :exc:`ValueError` 送出します。


.. function:: count(s, sub[, start[, end]])

   ``s[start:end]`` における、部分文字列 *sub* の (重複しない) 出現回数を返します。*start* と *end* のデフォルト値、
   および、負の値を指定した場合の解釈は文字列のスライスと同じです。


.. function:: lower(s)

   *s* のコピーを大文字を小文字に変換して返します。


.. function:: split(s[, sep[, maxsplit]])

   文字列*s* 内の単語からなるリストを返します。オプションの第二引数 *sep* を指定しないか、または``None`` にした場合、 空白文字
   (スペース、タブ、改行、リターン、改頁) からなる任意の文字列 で単語に区切ります。*sep* を``None`` 以外の値に指定した場合、
   単語の分割に使う文字列の指定になります。戻り値のリストには、 文字列中に分割文字列が重複せずに出現する回数より一つ多い要素が 入るはずです。オプションの第三引数
   *maxsplit* はデフォルトで 0 です。 この値がゼロでない場合、最大でも *maxsplit* 回の分割しか行わず、
   リストの最後の要素は未分割の残りの文字列になります (従って、リスト中の 要素数は最大でも``maxsplit+1`` です)。

   空文字列に対する分割を行った場合の挙動は *sep* の値に依存します。 *sep* を指定しないか``None`` にした場合、結果は空のリストに なります。
   *sep* に文字列を指定した場合、空文字列一つの入った リストになります。


.. function:: rsplit(s[, sep[, maxsplit]])

   *s* 中の単語からなるリストを *s* の末尾から検索して生成し 返します。関数の返す語のリストは全ての点で :func:`split` の
   返すものと同じになります。ただし、オプションの第三引数 *maxsplit* をゼロでない値に指定した場合には必ずしも同じにはなりません。 *maxsplit*
   がゼロでない場合には、最大で*maxsplit* 個の 分割を *右端から* 行います - 未分割の残りの文字列はリストの 最初の要素として返されます
   (従って、リスト中の要素数は最大でも ``maxsplit+1`` です)。

   .. versionadded:: 2.4


.. function:: splitfields(s[, sep[, maxsplit]])

   この関数は :func:`split` と同じように振舞います。 (以前は :func:`split`
   は単一引数の場合にのみ使い、:func:`splitfields`  は引数2つの場合でのみ使っていました)。


.. function:: join(words[, sep])

   単語のリストやタプルを間に*sep* を入れて連結します。   *sep* のデフォルト値はスペース文字 1 つです。
   ``string.join(string.split(s, sep), sep)`` は 常に *s* になります。


.. function:: joinfields(words[, sep])

   この関数は :func:`join` と同じふるまいをします (以前は、 :func:`join` を使えるのは引数が 1 つの場合だけで、
   :func:`joinfields` は引数2つの場合だけでした)。 文字列オブジェクトには :meth:`joinfields` メソッドがないので
   注意してください。代わりに :meth:`join` メソッドを使ってください。


.. function:: lstrip(s[, chars])

   文字列の先頭から文字を取り除いたコピーを生成して返します。 *chars* を指定しない場合や ``None`` にした場合、
   先頭の空白を取り除きます。*chars* を``None`` 以外の値にする場合、 *chars* は文字列でなければなりません。

   .. versionchanged:: 2.2.3
      *chars* パラメタを追加しました。  初期の 2.2 バージョンでは、*chars* パラメータを渡せませんでした.


.. function:: rstrip(s[, chars])

   文字列の末尾から文字を取り除いたコピーを生成して返します。 *chars* を指定しない場合や ``None`` にした場合、
   末尾の空白を取り除きます。*chars* を``None`` 以外の値にする場合、 *chars* は文字列でなければなりません。

   .. versionchanged:: 2.2.3
      *chars* パラメタを追加しました。  初期の 2.2 バージョンでは、*chars* パラメータを渡せませんでした.


.. function:: strip(s[, chars])

   文字列の先頭と末尾から文字を取り除いたコピーを生成して返します。 *chars* を指定しない場合や ``None`` にした場合、
   先頭と末尾の空白を取り除きます。*chars* を ``None`` 以外に指定する 場合、*chars* は文字列でなければなりません。

   .. versionchanged:: 2.2.3
      *chars* パラメタを追加しました。  初期の 2.2 バージョンでは、*chars* パラメータを渡せませんでした.


.. function:: swapcase(s)

   *s* の大文字と小文字を入れ替えたものを返します。


.. function:: translate(s, table[, deletechars])

   *s* の中から、 (もし指定されていれば) *deletechars* に入っている 文字を削除し、*table* を使って文字変換を行って返します。
   *table* は 256 文字からなる文字列で、各文字はそのインデクスを序数と する文字に対する変換先の文字の指定になります。


.. function:: upper(s)

   *s* に含まれる小文字を大文字に置換して返します。


.. function:: ljust(s, width)
              rjust(s, width)
              center(s, width)

   文字列を指定した文字幅のフィールド中でそれぞれ左寄せ、右寄せ、中央寄せ します。これらの関数は指定幅になるまで文字列 *s* の左側、右側、および
   両側のいずれかにスペースを追加して、少なくとも *width* 文字からなる 文字列にして返します。文字列を切り詰めることはありません。


.. function:: zfill(s, width)

   数値を表現する文字列の左側に、指定の幅になるまでゼロを付加します。符号付きの 数字も正しく処理します。


.. function:: replace(str, old, new[, maxreplace])

   *s* 内の部分文字列 *old* を全て *new* に置換したものを返し  ます。 *maxreplace* を指定した場合、最初に見つかった
   *maxreplace*  個分だけ置換します。

