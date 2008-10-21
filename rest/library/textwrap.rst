
:mod:`textwrap` --- テキストの折り返しと詰め込み
================================================

.. module:: textwrap
   :synopsis: テキストの折り返しと詰め込み
.. moduleauthor:: Greg Ward <gward@python.net>
.. sectionauthor:: Greg Ward <gward@python.net>


.. versionadded:: 2.3

:mod:`textwrap`モジュールでは、二つの簡易関数:func:`wrap`と
:func:`fill`、そして作業のすべてを行うクラス:class:`TextWrapper` とユーティリティ関数 :func:`dedent`
を提供しています。 単に一つや二つのテキスト文字列の折り返しまたは詰め込みを行っている ならば、簡易関数で十分間に合います。そうでなければ、
効率のために:class:`TextWrapper`のインスタンスを使った方が良いでしょう。


.. function:: wrap(text[, width[, ...]])

   *text*(文字列)内の段落を一つだけ折り返しを行います。したがって、すべての行が高々*width*文字の長さになります。最後に改行が付かない出力行のリストを返します。

   オプションのキーワード引数は、以下で説明する:class:`TextWrapper`のインスタンス属性に対応しています。*width*はデフォルトで``70``です。


.. function:: fill(text[, width[, ...]])

   *text*内の段落を一つだけ折り返しを行い、折り返しが行われた段落を含む一つの文字列を返します。:func:`fill`は  ::

      "\n".join(wrap(text, ...))

   の省略表現です。

   特に、:func:`fill`は:func:`wrap`とまったく同じ名前のキーワード引数を受け取ります。

:func:`wrap`と:func:`fill`の両方ともが:class:`TextWrapper`インスタンスを作成し、その一つのメソッドを呼び出すことで機能します。そのインスタンスは再利用されません。したがって、たくさんのテキスト文字列を折り返し/詰め込みを行うアプリケーションのためには、あなた自身の:class:`TextWrapper`オブジェクトを作成することでさらに効率が良くなるでしょう。

追加のユーティリティ関数である :func:`dedent` は、不要な 空白をテキストの左側に持つ文字列からインデントを取り去ります。


.. function:: dedent(text)

   *text* の各行に対し、共通して現れる先頭の空白を削除します。

   この関数は通常、三重引用符で囲われた文字列をスクリーン/その他の 左端にそろえ、なおかつソースコード中ではインデントされた形式を
   損なわないようにするために使われます。

   タブとスペースはともにホワイトスペースとして扱われますが、同じではないこ とに注意してください:  ``"  hello"`` という行と
   ``"\\thello"``　は、同じ先頭の空白文字をもっていない とみなされます。(このふるまいは Python 2.5で導入されました。古いバージョ
   ンではこのモジュールは不正にタブを展開して共通の先頭空白文字列を探して いました）

   以下に例を示します::

      def test():
          # end first line with \ to avoid the empty line!
          s = '''\
          hello
            world
          '''
          print repr(s)          # prints '    hello\n      world\n    '
          print repr(dedent(s))  # prints 'hello\n  world\n'


.. class:: TextWrapper(...)

   :class:`TextWrapper`コンストラクタはたくさんのオプションのキーワード引数を受け取ります。それぞれの引数は一つのインスタンス属性に対応します。したがって、例えば、
   ::

      wrapper = TextWrapper(initial_indent="* ")

   は  ::

      wrapper = TextWrapper()
      wrapper.initial_indent = "* "

   と同じです。

   あなたは同じ:class:`TextWrapper`オブジェクトを何回も再利用できます。また、使用中にインスタンス属性へ代入することでそのオプションのどれでも変更できます。

:class:`TextWrapper`インスタンス属性(とコンストラクタのキーワード引数)は以下の通りです:


.. attribute:: TextWrapper.width

   (デフォルト: ``70``)
   折り返しが行われる行の最大の長さ。入力行に:attr:`width`より長い単一の語が無い限り、:class:`TextWrapper`は:attr:`width`文字より長い出力行が無いことを保証します。


.. attribute:: TextWrapper.expand_tabs

   (デフォルト: ``True``)
   もし真ならば、そのときは*text*内のすべてのタブ文字は*text*の:meth:`expand_tabs`メソッドを用いて空白に展開されます。


.. attribute:: TextWrapper.replace_whitespace

   (デフォルト: ``True``)
   もし真ならば、タブ展開の後に残る(``string.whitespace``に定義された)空白文字のそれぞれが一つの空白と置き換えられます。

   .. note::

      :attr:`expand_tabs`が偽で:attr:`replace_whitespace`が真ならば、各タブ文字は一つの空白に置き換えられます。それはタブ展開と同じでは*ありません*。


.. attribute:: TextWrapper.initial_indent

   (デフォルト: ``''``) 折り返しが行われる出力の一行目の先頭に付けられる文字列。一行目の折り返しの長さになるまで含められます。


.. attribute:: TextWrapper.subsequent_indent

   (デフォルト: ``''``) 一行目以外の折り返しが行われる出力のすべての行の先頭に付けられる文字列。一行目以外の各行が折り返しの長さまで含められます。


.. attribute:: TextWrapper.fix_sentence_endings

   (デフォルト: ``False``)
   もし真ならば、:class:`TextWrapper`は文の終わりを見つけようとし、確実に文がちょうど二つの空白で常に区切られているようにします。これは一般的に固定スペースフォントのテキストに対して望ましいです。しかし、文の検出アルゴリズムは完全ではありません:
   文の終わりには、後ろに空白がある``'.'``、``'!'``または``'?'``の中の一つ、ことによると``'"'``あるいは``'''``が付随する小文字があると仮定しています。これに伴う一つの問題は
   ::

      [...] Dr. Frankenstein's monster [...]

   の"Dr."と ::

      [...] See Spot. See Spot run [...]

   の"Spot."の間の差異を検出できないアルゴリズムです。

   :attr:`fix_sentence_endings`はデフォルトで偽です。

   文検出アルゴリズムは"小文字"の定義のために``string.lowercase``に依存し、同一行の文を区切るためにピリオドの後に二つの空白を使う慣習に依存しているため、英文テキストに限定されたものです。


.. attribute:: TextWrapper.break_long_words

   (デフォルト: ``True``)
   もし真ならば、そのとき:attr:`width`より長い行が確実にないようにするために、:attr:`width`より長い語は切られます。偽ならば、長い語は切られないでしょう。そして、:attr:`width`より長い行があるかもしれません。(:attr:`width`を超える分を最小にするために、長い語は単独で一行に置かれるでしょう。)

:class:`TextWrapper`はモジュールレベルの簡易関数に類似した二つの公開メソッドも提供します:


.. method:: TextWrapper.wrap(text)

   *text*(文字列)内の段落を一つだけ折り返しを行います。したがって、すべての行は高々:attr:`width`文字です。すべてのラッピングオプションは:class:`TextWrapper`インスタンスのインスタンス属性から取られています。最後に改行の無い出力された行のリストを返します。


.. method:: TextWrapper.fill(text)

   *text*内の段落を一つだけ折り返しを行い、折り返しが行われた段落を含む一つの文字列を返します。

