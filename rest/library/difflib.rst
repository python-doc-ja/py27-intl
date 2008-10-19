
:mod:`difflib` --- 差異の計算を助ける
============================

.. module:: difflib
   :synopsis: オブジェクト同士の違いを計算する
.. moduleauthor:: Tim Peters <tim_one@users.sourceforge.net>
.. sectionauthor:: Tim Peters <tim_one@users.sourceforge.net>


.. % LaTeXification by Fred L. Drake, Jr. <fdrake@acm.org>.

.. versionadded:: 2.1


.. class:: SequenceMatcher

   柔軟性のあるクラスで、ハッシュ化できる要素の連続であれば、 どんな型のものであっても比較可能です。基礎的なアルゴリズムは
   可塑的なものであり、1980年代の後半に発表されたRatcliffとObershelp によるアルゴリズム、大げさに名づけられた"ゲシュタルトパターン
   マッチング"よりはもう少し良さそうなものです。その考え方は、 "junk"要素を含まない最も長いマッチ列を探すことです（Ratcliffと
   Obershelpのアルゴリズムではjunkを示しません）。このアイデアは、 下位のマッチ列から左または右に伸びる列の断片に対して再帰的に
   あてはまります。これは小さな文字列に対して効率良いものでは ありませんが、人間の目からみて「良く見える」ようにマッチする 傾向があります。

   **実行時間:** 基本的なRatcliff-Obershelpアルゴリズムは、最
   悪の場合3乗、期待値でも2乗となります。:class:`SequenceMatcher` オブジェクトは、最悪のケースで4乗、期待値はシーケンスの
   中の要素数に非常にややこしく依存しています。最良の場合 は線形時間になります。


.. class:: Differ

   テキスト行からなるシーケンスを比較するクラスです。人が読むことの できる差異を作成します。Differクラスは:class:`SequenceMatcher`
   クラスを利用します。これらは、列からなるシーケンスを比較し、 (ほぼ) 同一の列内の文字を比較します。

   :class:`Differ`クラスによる差異の各行は、2文字のコードではじめられます。

   +----------+--------------------+
   | コード      | 意味                 |
   +==========+====================+
   | ``'- '`` | 列は文字列1にのみ存在する      |
   +----------+--------------------+
   | ``'+ '`` | 列は文字列2にのみ存在する      |
   +----------+--------------------+
   | ``'  '`` | 列は両方の文字列で同一        |
   +----------+--------------------+
   | ``'? '`` | 列は入力文字列のどちらにも存在しない |
   +----------+--------------------+

   '? 'で始まる列は線内の差異に注意を向けようとします。その差異は、 入力されたシーケンスのどちらにも存在しません。シーケンスが
   タブ文字を含むとき、これらのラインは判別しづらいものになる ことがあります。


.. class:: HtmlDiff

   このクラスは、二つのテキストを左右に並べて比較表示し、行間あるいは行内の 変更点を強調表示するような HTML テーブル (またはテーブルの入った 完全な
   HTML ファイル) を生成するために使います。テーブルは完全差分モード、 コンテキスト差分モードのいずれでも生成できます。

   このクラスのコンストラクタは以下のようになっています:


   .. function:: __init__([tabsize][, wrapcolumn][, linejunk][, charjunk])

      :class:`HtmlDiff` のインスタンスを初期化します。

      *tabsize* はオプションのキーワード引数で、タブストップ幅を指定 します。デフォルトは ``8`` です。

      *wrapcolumn* はオプションのキーワード引数で、テキストを折り返す カラム幅を指定します。デフォルトは ``None`` で折り返しを行いません。

      *linejunk* および *charjunk* はオプションのキーワード引数で、 ``ndiff()`` (:class:`HtmlDiff`
      はこの関数を使って左右のテキストの 差分を HTML で生成します) に渡されます。それぞれの引数のデフォルト値 および説明は ``ndiff()``
      のドキュメントを参照してください。

   以下のメソッドが public になっています:


   .. function:: make_file(fromlines, tolines [, fromdesc][, todesc][, context][, numlines])

      *fromlines* と *tolines* (いずれも文字列のリスト) を比較し、 行間または行内の変更点が強調表示された行差分の入った表を持つ完全な
      HTML  ファイルを文字列で返します。

      *fromdesc* および *todesc* はオプションのキーワード引数で、 差分表示テーブルにおけるそれぞれ差分元、差分先ファイルのカラムの
      ヘッダになる文字列を指定します (いずれもデフォルト値は空文字列です)。

      *context* および *numlines* はともにオプションのキーワード 引数です。*contest* を ``True`` にするとコンテキスト差分を
      表示し、デフォルトの ``False`` にすると完全なファイル差分を 表示します。*numlines* のデフォルト値は ``5`` で、 *context*
      が ``True`` の場合、 *numlines* は強調部分の前後に あるコンテキスト行の数を制御します。*context* が ``False``
      の場合、*numlines* は "next" と書かれたハイパーリンクをたどった時に 到達する場所が次の変更部分より何行前にあるかを制御します
      (値をゼロにした場合、"next" ハイパーリンクを辿ると変更部分の強調表示が ブラウザの最上部に表示されるようになります)。


   .. function:: make_table(fromlines, tolines [, fromdesc][, todesc][, context][, numlines])

      *fromlines* と *tolines* (いずれも文字列のリスト) を比較し、 行間または行内の変更点が強調表示された行差分の入った完全な HTML
      テーブル を文字列で返します。

      このメソッドの引数は、:meth:`make_file` メソッドの引数と同じです。

   :file:`Tools/scripts/diff.py` はこのクラスへのコマンドラインフロントエンド で、使い方を学ぶ上で格好の例題が入っています。

   .. versionadded:: 2.4


.. function:: context_diff(a, b[, fromfile][, tofile][, fromfiledate][, tofiledate][, n][, lineterm])

   *a* と *b* (文字列のリスト) を比較し、差異 (差異のある行を生成するジェネレータ) を、diff のコンテクスト形式で返します。

   コンテクスト形式は、変更があった行に前後数行を加えてある、コンパクトな表 現方法です。変更箇所は、変更前/変更後に分けて表します。コンテクスト（変
   更箇所前後の行）の行数は *n* で指定し、デフォルト値は 3 です。

   デフォルトでは、diff の制御行 (``***`` や ``---`` を含む行) の最
   後には、改行文字が付加されます。この場合、入出力共、行末に改行文字を持つ ので、:func:`file.readlines` で得た入力から生成した差異を、
   :func:`file.writelines` に渡す場合に便利です。行末に改行文字を持た ない入力に対しては、出力でも改行文字を付加しないように
   *lineterm* 引 数に ``""`` を渡してください。

   diff コンテクスト形式は、通常、ヘッダにファイル名と変更時刻を持ってい ます。この情報は、文字列
   *fromfile*、*tofile*、*fromfiledate*、 *tofiledate* で指定できます。変更時刻の書式は、通常、
   :func:`time.ctime` の戻り値と同じものを使います。指定しなかった場合 のデフォルト値は、空文字列です。

   :file:`Tools/scripts/diff.py` は、この関数のコマンドラインのフロントエンド（インターフェイス）になっています。

   .. versionadded:: 2.3


.. function:: get_close_matches(word, possibilities[, n][, cutoff])

   最も「十分」なマッチのリストを返します。*word*は、なるべく マッチして欲しい（一般的には文字列の）シーケンスです。
   *possibilities*は*word*にマッチさせる（一般的には文字列） シーケンスのリストです。

   オプションの引数*n*（デフォルトでは``3``）はメソッドの返す マッチの最大数です。*n* は ``0`` より大きくなければなりません。

   オプションの引数 *cutoff* （デフォルトでは ``0.6``）は、 [0, 1]の間となるfloatの値です。可能性として、少なくとも *word*
   が無視されたのと同様の数値にはなりません。

   可能性のある、（少なくとも *n* に比べて）最もよいマッチはリストに よって返され、同一性を表す数値に応じて最も近いものから順に格納されます。 ::

      >>> get_close_matches('appel', ['ape', 'apple', 'peach', 'puppy'])
      ['apple', 'ape']
      >>> import keyword
      >>> get_close_matches('wheel', keyword.kwlist)
      ['while']
      >>> get_close_matches('apple', keyword.kwlist)
      []
      >>> get_close_matches('accept', keyword.kwlist)
      ['except']


.. function:: ndiff(a, b[, linejunk[, charjunk]])

   *a* と *b* （文字列からなるリスト）を比較し、:class:`Differ`  オブジェクト形式の差異（解析器は差異のある列）を返します。

   オプションのパラメータ *linejunk* と *charjunk* は、filter 機能のためのキーワードです（使わないときは空にする）。

   *linejunk*: string型の引数ひとつを受け取る関数で、文字列が junkか否かによってtrueを（違うときにはtrueを）返します。Python
   2.3以降、デフォルトでは（``None``）になります。それまでは、 モジュールレべルの関数:func:`IS_LINE_JUNK`であり、それは
   少なくともひとつのシャープ記号（``'#'``）をのぞく、可視の キャラクタを含まない行をフィルタリングします。 Python
   2.3では、下位にある:class:`SequenceMatcher`クラスが、 雑音となるくらい頻繁に登場する列であるか否かを、動的に分析します。
   これは、バージョン2.3以前でのデフォルト値よりうまく動作します。

   *charjunk*: 長さ1の文字を受け取る関数です。デフォルトでは、 モジュールレべルの関数 IS_CHARACTER_JUNK()であり、これは空白文字列
   （空白またはタブ、注：改行文字をこれに含めるのは悪いアイデア！）を フィルタリングします。

   :file:`Tools/scripts/ndiff.py` は、この関数のコマンドラインのフロント エンド（インターフェイス）です。 ::

      >>> diff = ndiff('one\ntwo\nthree\n'.splitlines(1),
      ...              'ore\ntree\nemu\n'.splitlines(1))
      >>> print ''.join(diff),
      - one
      ?  ^
      + ore
      ?  ^
      - two
      - three
      ?  -
      + tree
      + emu


.. function:: restore(sequence, which)

   差異を生成したシーケンスのひとつを返します。

   与えられる*sequence*は :meth:`Differ.compare` または  :meth:`ndiff`によって生成され、ファイル1または2（引数
   *which*で指定される）によって元の列に復元され、行頭の プレフィクスが取りのぞかれます。

   例:

   .. % Example:

   ::

      >>> diff = ndiff('one\ntwo\nthree\n'.splitlines(1),
      ...              'ore\ntree\nemu\n'.splitlines(1))
      >>> diff = list(diff) # materialize the generated delta into a list
      >>> print ''.join(restore(diff, 1)),
      one
      two
      three
      >>> print ''.join(restore(diff, 2)),
      ore
      tree
      emu


.. function:: unified_diff(a, b[, fromfile][, tofile][, fromfiledate][, tofiledate][, n][, lineterm])

   *a* と *b* (共に文字列のリスト) を比較し、diff の unified 形式 で、差異 (差分行を生成するジェネレータ) を返します。

   unified 形式は変更があった行に前後数行を加えた、コンパクトな表現方法で す。変更箇所は (変更前/変更後を分離したブロックではなく) インライン・ス
   タイルで表されます。コンテクスト（変更箇所前後の行）の行数は、*n* で 指定し、デフォルト値は 3 です。

   デフォルトでは、diff の制御行 (``---``、``+++``、``@@`` を含 む行)
   は行末で改行します。この場合、入出力共、行末に改行文字を持つので、 :func:`file.readlines` で得た入力を処理して生成した差異を、
   :func:`file.writelines` に渡す場合に便利です。

   行末に改行文字を持たない入力には、出力も同じように改行なしになるように、*lineterm* 引数を ``""`` にセットしてください

   diff コンテクスト形式は、通常、ヘッダにファイル名と変更時刻を持ってい ます。  この情報は、文字列 *fromfile*、*tofile*、
   *fromfiledate*、*tofiledate* で指定できます。変更時刻の書式は、 通常、:func:`time.ctime`
   の戻り値と同じものを使います。 指定しなかっ た場合のデフォルト値は、空文字列です。

   :file:`Tools/scripts/diff.py` は、この関数のコマンドラインのフロントエ ンド（インターフェイス）です。

   .. versionadded:: 2.3


.. function:: IS_LINE_JUNK(line)

   無視できる列のときtrueを返します。列 *line* が空白、または  ``'#"'`` ひとつのときには無視できます。それ以外の時には
   無視できません。:func:`ndiff` の引数*linkjunk*として デフォルトで使用されます。
   :func:`ndiff`の*linejunk*はPython 2.3以前のものです。


.. function:: IS_CHARACTER_JUNK(ch)

   無視できる文字のときtrueを返します。文字 *ch* が空白、または タブ文字のときには無視できます。それ以外の時には無視できません。
   :func:`ndiff` の引数*charjunk*としてデフォルトで使用されます。


.. seealso::

   `Pattern Matching: The Gestalt Approach （パターン マッチング: 全体アプローチ） <http://www.ddj.com/documents/s=1103/ddj8807c/>`_
      John W. Ratcliff と  D. E. Metzener による同一性アルゴリズムに関する議論。 `Dr. Dobb's Journal
      <http://www.ddj.com/>`_  1988年7月号掲載。


.. _sequence-matcher:

SequenceMatcherオブジェクト
---------------------

The :class:`SequenceMatcher` クラスには、以下のようなコンストラクタがあります。:


.. class:: SequenceMatcher([isjunk[, a[, b]]])

   オプションの引数 *isjunk* は、``None`` (デフォルトの値です) にするか、単一の引数をとる関数にせねばなりません。後者の場合、関数は
   シーケンスの要素を受け取り、要素が "junk" であり、無視すべきである場合に 限り真をかえすようにせねばなりません。 *isjunk* に ``None``
   を渡すと、``lambda x: 0`` を渡したのと 同じになります; すなわち、いかなる要素も無視しなくなります。
   例えば以下のような引数を渡すと、空白とタブ文字を無視して文字のシーケンスを 比較します。 ::

      lambda x: x in " \t"

   オプションの引数 *a* と *b* は、比較される文字列です。 デフォルトで、それらは空の文字列で、文字列の要素はハッシュ化できます。

:class:`SequenceMatcher` オブジェクトは以下のメソッドを持ちます。


.. method:: SequenceMatcher.set_seqs(a, b)

   比較される2つの文字列を設定します。

:class:`SequenceMatcher` オブジェクトは2つ目の文字列についての詳細な情報を
算定し、保管します。そのため、ひとつの文字列をいくつもの文字列と比較する場合、 まず :meth:`set_seq2`
を使って文字列を設定しておき、別の文字列をひとつづつ 比較するために、繰り返し :meth:`set_seq` を呼び出します。


.. method:: SequenceMatcher.set_seq1(a)

   比較を行うひとつ目の文字列を設定します。比較される2つ目の文字列は 変更されません。


.. method:: SequenceMatcher.set_seq2(b)

   比較を行う2つめ目のシーケンスを設定します。比較されるひとつ目の シーケンスは変更されません。


.. method:: SequenceMatcher.find_longest_match(alo, ahi, blo, bhi)

   ``a[alo:ahi]`` と``b[blo: bhi]``の中から、最長のマッチ列を探します。

   *isjunk*が省略されたか``None``の時、:meth:`get_longest_match` は``a[i:i+k]``が``b[j:
   j+k]``と等しいような``(i, j, k)``を 返します。その値は``alo <= i <= i+k <=  ahi``かつ``blo <= j <=
   j+k <=  bhi``となります。``(i', j', k')``でも、 同じようになります。さらに``k >= k', i <= i'`` が``i ==
   i', j <= j'``でも同様です。 言い換えると、いくつものマッチ列すべてのうち、*a*内で最初に
   始まるものを返します。そしてその*a*内で最初のマッチ列すべての うち*b*内で最初に始まるものを返します。 ::

      >>> s = SequenceMatcher(None, " abcd", "abcd abcd")
      >>> s.find_longest_match(0, 5, 0, 9)
      (0, 4, 5)

   引数*isjunk*が与えられている場合、上記の通り、はじめに再長の マッチ列を判定します。ブロック内にjunk要素が見当たらないような
   追加条件の際はこれに該当しません。次にそのマッチ列を、その両側の junk要素にマッチするよう、できる限り広げていきます。そのため結果
   となる列は、探している列のたまたま直前にあった同一のjunk以外の junkにはマッチしません。

   以下は前と同じサンプルですが、空白をjunkとみなしています。これは ``' abcd'``が2つ目の列の末尾にある``' abcd'``にマッチしない
   ようにしています。代わりに``'abcd'``にはマッチします。そして 2つ目の文字列中、一番左の``'abcd'``にマッチします。 ::

      >>> s = SequenceMatcher(lambda x: x==" ", " abcd", "abcd abcd")
      >>> s.find_longest_match(0, 5, 0, 9)
      (1, 0, 4)

   どんな列にもマッチしない時は、``(alo, blo, 0)``を 返します。


.. method:: SequenceMatcher.get_matching_blocks()

   マッチしたシーケンス中で個別にマッチしたシーケンスをあらわす、 3つの値のリストを返します。それぞれの値は``(i, j,
   n)``という形式であらわされ、``a[i:i+n] == b[j:j+n]``いう関係を意味します。3つの値は *i*と*j*の間で単調に増加します。

   最後のタプルはダミーで、``(len(a), len(b), 0)``という 値を持ちます。これは``n==0``である唯一のタプルです。

   .. % Explain why a dummy is used!

   もし ``(i, j, n)`` と ``(i', j', n')`` がリストで並んでいる3つ組で、 2つ目が最後の3つ組でなければ、 ``i+n !=
   i'`` または ``j+n != j'`` です。言い換えると並んでいる3つ組 は常に隣接していない同じブロックを表しています。

   .. versionchanged:: 2.5
      隣接する3つ組は常に隣接しないブロックを表すと保証するようになりました.

   ::

      >>> s = SequenceMatcher(None, "abxcd", "abcd")
      >>> s.get_matching_blocks()
      [(0, 0, 2), (3, 2, 2), (5, 4, 0)]


.. method:: SequenceMatcher.get_opcodes()

   aをbにするための方法を記述する5つのタプルを返します。それぞれの タプルは``(tag, i1, i2, j1, j2)``
   という形式であらわされます。最初のタプルは``i1 == j1 == 0``であり、*i1*はその前にあるタプルの*i2*と同じ値です。
   同様に*j1*は前の*j2*と同じ値になります。

   *tag*の値は文字列であり、次のような意味です。

   +---------------+--------------------------------------------+
   | 値             | 意味                                         |
   +===============+============================================+
   | ``'replace'`` | ``a[i1:i2]``は``b[ j1:j2]``に置き換えられる         |
   +---------------+--------------------------------------------+
   | ``'delete'``  | ``a[i1:i2]`` は削除される。 この時、``j1 == j2``である   |
   +---------------+--------------------------------------------+
   | ``'insert'``  | ``b[j1:j2]`` が``a [i1:i1]``に挿入される。 この時``i1 |
   |               | == i2``である。                                |
   +---------------+--------------------------------------------+
   | ``'equal'``   | ``a[i1:i2] == b[j1:j2]`` (下位の文字列は同一)       |
   +---------------+--------------------------------------------+

   例::

      >>> a = "qabxcd"
      >>> b = "abycdf"
      >>> s = SequenceMatcher(None, a, b)
      >>> for tag, i1, i2, j1, j2 in s.get_opcodes():
      ...    print ("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %
      ...           (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2]))
       delete a[0:1] (q) b[0:0] ()
        equal a[1:3] (ab) b[0:2] (ab)
      replace a[3:4] (x) b[2:3] (y)
        equal a[4:6] (cd) b[3:5] (cd)
       insert a[6:6] () b[5:6] (f)


.. method:: SequenceMatcher.get_grouped_opcodes([n])

   最大 *n* 行までのコンテクストを含むグループを生成するような、ジェネレータを返します。

   このメソッドは、:meth:`get_opcodes` で返されるグループの中から、似 たような差異のかたまりに分け、間に挟まっている変更の無い部分を省きます。

   グループは :meth:`get_opcodes` と同じ書式で返されます。

   .. versionadded:: 2.3


.. method:: SequenceMatcher.ratio()

   [0, 1]の範囲の浮動小数点で、シーケンスの同一性を測る値を返します。

   Tが2つのシーケンスそれぞれがもつ要素の総数だと仮定し、Mをマッチした 数とすると、この値は2.0\*M/Tであらわされます。もしシーケンスがまったく
   同じ場合、値は1.0となり、まったく異なる場合には``0.0``となります。

   このメソッドは:meth:`get_matching_blocks`または:meth:`get_opcodes`が
   まだ呼び出されていない場合には非常にコストが高く、この時より限定された
   機能をもった:meth:`quick_ratio`もしくは:meth:`real_quick_ratio`を 最初に試してみることができます。


.. method:: SequenceMatcher.quick_ratio()

   :meth:`ratio`で測定する同一性をより素早く、限定された形で測ります。

   このメソッドは:meth:`ratio`より限定されており、これを超えるとは 見なされませんが、高速に実行します。


.. method:: SequenceMatcher.real_quick_ratio()

   ratio()で測定する同一性を非常に素早く測ります。

   このメソッドは:meth:`ratio`より限定されており、これを
   超えるとは見なされませんが、:meth:`ratio`や:meth:`quick_ratio`より高速に実行します。

この文字列全体のマッチ率を返す3つのメソッドは、異なる近似値に基づく
異なる結果を返します。とはいえ、:meth:`quick_ratio`と:meth:`real_quick_ratio`は、常に:meth:`ratio`より大きな値を示します。
::

   >>> s = SequenceMatcher(None, "abcd", "bcde")
   >>> s.ratio()
   0.75
   >>> s.quick_ratio()
   0.75
   >>> s.real_quick_ratio()
   1.0


.. _sequencematcher-examples:

SequenceMatcher の例
------------------

この例は2つの文字列を比較します。空白を"junk"とします。 ::

   >>> s = SequenceMatcher(lambda x: x == " ",
   ...                     "private Thread currentThread;",
   ...                     "private volatile Thread currentThread;")

:meth:`ratio` は、[0, 1] の範囲の値を返し、シーケンスの同一性を測ります。 経験によると、:meth:`ratio`
の値が0.6を超えると、シーケンスがよく似て いることを示します。 ::

   >>> print round(s.ratio(), 3)
   0.866

シーケンスのどこがマッチしているかにだけ興味のある時には  :meth:`get_matching_blocks` が手軽でしょう。 ::

   >>> for block in s.get_matching_blocks():
   ...     print "a[%d] and b[%d] match for %d elements" % block
   a[0] and b[0] match for 8 elements
   a[8] and b[17] match for 6 elements
   a[14] and b[23] match for 15 elements
   a[29] and b[38] match for 0 elements

注意:最後のタプルは、:meth:`get_matching_blocks`が常にダミーで あることで返されるものです。 ``(len(a), len(b),
0)``  であり、これは最後のタプルの要素（マッチするようその数）がゼロとなる 唯一のケースです。

はじめのシーケンスがどのようにして2番目のものになるのかを知るには、 :meth:`get_opcodes` を使います。 ::

   >>> for opcode in s.get_opcodes():
   ...     print "%6s a[%d:%d] b[%d:%d]" % opcode
    equal a[0:8] b[0:8]
   insert a[8:8] b[8:17]
    equal a[8:14] b[17:23]
    equal a[14:29] b[23:38]

See also the function :func:`get_close_matches` in this module, which shows how
simple code building on :class:`SequenceMatcher` can be used to do useful work.
:class:`SequenceMatcher` を使った、シンプルで使えるコードを知るには、 このモジュールの関数
:func:`get_close_matches` を参照してください。


.. _differ-objects:

Differ オブジェクト
-------------

:class:`Differ`オブジェクトによって抽出された差分は、**最小単位**の 差分を見ても問題なく抽出されます。反対に、最小の差分の場合にはこれとは
反対のように見えます。それらが、どこれも可能ときに同期するからです。 時折、思いがけなく100ページもの部分にマッチします。隣接するマッチ列の
同期するポイントを制限することで、より長い差異を算出する再帰的なコスト での、局所性の概念を制限します。

:class:`Differ`は、以下のようなコンストラクタを持ちます。


.. class:: Differ([linejunk[, charjunk]])

   オプションのパラメータ*linejunk*と*charjunk*はfilter関数の ために指定します（もしくは``None``を指定）。

   *linejunk*:ひとつの文字列引数を受け取れるべき関数です。 文字列がjunkのときにtrueを返します。デフォルトでは、``None``
   であり、どんな行であってもjunkとは見なされません。

   *charjunk*: この関数は（長さ1の）文字列を引数として受け取り、文字列が
   junkであるときにtrueを返します。デフォルトは``None``であり、どんな文字列も junkとは見なされません。

:class:`Differ`オブジェクトは、以下のひとつのメソッドによって使われます （違いを生成します）。


.. method:: Differ.compare(a, b)

   文字列からなる2つのシーケンスを比較し、差異（を表す文字列からなる シーケンス）を生成します。

   Each sequence must contain individual single-line strings ending with newlines.
   Such sequences can be obtained from the :meth:`readlines` method of file-like
   objects.  The delta generated also consists of newline-terminated strings, ready
   to be printed as-is via the :meth:`writelines` method of a file-like object.
   それぞれのシーケンスは、改行文字によって終了する、独立したひと連なりの 文字列でなければなりません。そのようなシーケンスは、ファイル形式オブジェクトの
   :meth:`readline`メソッドによって得ることができます。（得られる）差異は
   改行文字で終了する文字列として得られ、ファイル形式オブジェクトの:meth:`writeline` メソッドによって出力できる形になっています。


.. _differ-examples:

Differ の例
---------

この例では2つのテキストを比較します。初めに、改行文字で終了する独立した 1行の連続した（ファイル形式オブジェクトの:meth:`readlines`メソッドに
よって得られるような）テキストを用意します。 ::

   >>> text1 = '''  1. Beautiful is better than ugly.
   ...   2. Explicit is better than implicit.
   ...   3. Simple is better than complex.
   ...   4. Complex is better than complicated.
   ... '''.splitlines(1)
   >>> len(text1)
   4
   >>> text1[0][-1]
   '\n'
   >>> text2 = '''  1. Beautiful is better than ugly.
   ...   3.   Simple is better than complex.
   ...   4. Complicated is better than complex.
   ...   5. Flat is better than nested.
   ... '''.splitlines(1)

次にDifferオブジェクトをインスタンス化します。 ::

   >>> d = Differ()

注意：:class:`Differ`オブジェクトをインスタンス化するとき、 "junk."である列と文字をフィルタリングす関数を渡すことができます。
詳細は:meth:`Differ`コンストラクタを参照してください。

最後に、2つを比較します。 ::

   >>> result = list(d.compare(text1, text2))

``result``は文字列のリストなので、pretty-printしてみましょう。 ::

   >>> from pprint import pprint
   >>> pprint(result)
   ['    1. Beautiful is better than ugly.\n',
    '-   2. Explicit is better than implicit.\n',
    '-   3. Simple is better than complex.\n',
    '+   3.   Simple is better than complex.\n',
    '?     ++                                \n',
    '-   4. Complex is better than complicated.\n',
    '?            ^                     ---- ^  \n',
    '+   4. Complicated is better than complex.\n',
    '?           ++++ ^                      ^  \n',
    '+   5. Flat is better than nested.\n']

これは、複数行の文字列として、次のように出力されます。 ::

   >>> import sys
   >>> sys.stdout.writelines(result)
       1. Beautiful is better than ugly.
   -   2. Explicit is better than implicit.
   -   3. Simple is better than complex.
   +   3.   Simple is better than complex.
   ?     ++
   -   4. Complex is better than complicated.
   ?            ^                     ---- ^
   +   4. Complicated is better than complex.
   ?           ++++ ^                      ^
   +   5. Flat is better than nested.

