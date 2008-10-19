
:mod:`optparse` --- より強力なコマンドラインオプション解析器
========================================

.. module:: optparse
   :synopsis: より便利で柔軟性に富んだ強力なコマンドライン解析ライブラリ
.. moduleauthor:: Greg Ward <gward@python.net>


.. versionadded:: 2.3

.. sectionauthor:: Greg Ward <gward@python.net>


:mod:`optparse` モジュールは、``getopt`` よりも簡便で、柔軟性に富み、 かつ強力なコマンドライン解析ライブラリです。
:mod:`optparse` では、より明快なスタイルのコマンドライン解析手法、 すなわち:class:`OptionParser`
のインスタンスを作成してオプションを 追加してゆき、そのインスタンスでコマンドラインを解析するという手法を とっています。``optparse``
を使うと、GNU/POSIX 構文でオプションを 指定できるだけでなく、使用法やヘルプメッセージの生成も行えます。

.. % An intro blurb used only when generating LaTeX docs for the Python
.. % manual (based on README.txt).

:mod:`optparse` を使った簡単なスクリプト例を以下に示します::

   from optparse import OptionParser

   [...]
   parser = OptionParser()
   parser.add_option("-f", "--file", dest="filename",
                     help="write report to FILE", metavar="FILE")
   parser.add_option("-q", "--quiet",
                     action="store_false", dest="verbose", default=True,
                     help="don't print status messages to stdout")

   (options, args) = parser.parse_args()

このようにわずかな行数のコードによって、スクリプトのユーザは コマンドライン上で例えば以下のような 「よくある使い方」 を実行できるように なります::

   <yourscript> --file=outfile -q

コマンドライン解析の中で、``optparse`` はユーザの指定した コマンドライン引数値に応じて:meth:`parse_args` の返す
``options`` の属性値を設定してゆきます。 :meth:`parse_args` がコマンドライン解析から処理を戻したとき、
``options.filename`` は``"outfile"`` に、``options.verbose`` は ``False``
になっているはずです。``optparse`` は 長い形式と短い形式の両方のオプション表記をサポートしており、
短い形式は結合して指定できます。また、様々な形でオプションに 引数値を関連付けられます。従って、以下のコマンドラインは全て上の例 と同じ意味になります::

   <yourscript> -f outfile --quiet
   <yourscript> --quiet --file outfile
   <yourscript> -q -foutfile
   <yourscript> -qfoutfile

さらに、ユーザが ::

   <yourscript> -h
   <yourscript> --help

のいずれかを実行すると、:mod:`optparse` はスクリプトの オプションについて簡単にまとめた内容を出力します::

   usage: <yourscript> [options]

   options:
     -h, --help            show this help message and exit
     -f FILE, --file=FILE  write report to FILE
     -q, --quiet           don't print status messages to stdout

*yourscript* の中身は実行時に決まります (通常は ``sys.argv[0]`` になります)。


.. _optparse-background:

Background
----------

:mod:`optparse` は、素直で慣習に則ったコマンドラインインタフェースを 備えたプログラムの作成を援助する目的で設計されました。 その結果、Unix
で慣習的に使われているコマンドラインの構文や機能 だけをサポートするに留まっています。こうした慣習に詳しくなければ、
よく知っておくためにもこの節を読んでおきましょう。


.. _optparse-terminology:

Terminology
^^^^^^^^^^^

引数 (argument)
   コマンドラインでユーザが入力するテキストの塊で、シェルが :cfunc:`execl` や :cfunc:`execv` に引き渡すものです。Python
   では、引数は ``sys.argv[1:]`` の要素となります。(``sys.argv[0]``
   は実行しようとしているプログラムの名前です。引数解析に関しては、この要 素はあまり重要ではありません。) Unix シェルでは、 「語 (word)」 と
   いう用語も使います。

   場合によっては ``sys.argv[1:]`` 以外の引数リストを代入する方が望ま しいことがあるので、「引数」 は 「``sys.argv[1:]``
   または ``sys.argv[1:]`` の代替として提供される別のリストの要素」と読むべき でしょう。

オプション (option)
   追加的な情報を与えるための引数で、プログラムの実行に対する教示やカスタ マイズを行います。オプションには多様な文法が存在します。伝統的な Unix
   における書法はハイフン ("-") の後ろに一文字が続くもので、例 えば ``"-x"`` や ``"-F"`` です。また、伝統的な Unix における
   書法では、複数のオプションを一つの引数にまとめられます。例えば ``"-x -F"`` は``"-xF"`` と等価です。 GNU プロジェクトでは
   ``"--"`` の後ろにハイフンで区切りの語を指定 する方法、例えば ``"--file"`` や ``"--dry-run"`` も提供して
   います。:mod:`optparse` は、これら二種類のオプション書法だけをサポー トしています。

   他に見られる他のオプション書法には以下のようなものがあります:

*   ハイフンの後ろに数個の文字が続くもので、例えば ``"-pf"``  (このオプションは複数のオプションを一つにまとめたものとは *違います*)

*  ハイフンの後ろに語が続くもので、例えば ``"-file"``  (これは技術的には上の書式と同じですが、通常同じプログラム上で一緒に
     使うことはありません)

*  プラス記号の後ろに一文字、数個の文字、または語を続けたもので、 例えば ``"+f"`` 、 ``"+rgb"``

*  スラッシュ記号の後ろに一文字、数個の文字、または語を続けたもので、 例えば ``"/f"`` 、 ``"/file"``

   上記のオプション書法は :mod:`optparse` ではサポートしておらず、 今後もサポートする予定はありません。これは故意によるものです:
   最初の三つはどの環境の標準でもなく、最後の一つは VMS や MS-DOS, そして Windows を対象にしているときにしか意味をなさないからです。

オプション引数 (option argument)
   あるオプションの後ろに続く引数で、そのオプションに密接な関連を もち、オプションと同時に引数リストから取り出されます。 :mod:`optparse`
   では、オプション引数は以下のように別々の引数にできます::

      -f foo
      --file foo

   また、一つの引数中にも入れられます::

      -ffoo
      --file=foo

   通常、オプションは引数をとることもとらないこともあります。 あるオプションは引数をとることがなく、またあるオプションは 常に引数をとります。多くの人々が
   「オプションのオプション引数」 機能を欲しています。これは、あるオプションが引数が指定されている
   場合には引数をとり、そうでない場合には引数をもたないようにするという機能です。 この機能は引数解析をあいまいにするため、議論の的となっています: 例えば、もし
   :option:`-a` がオプション引数を とり、:option:`-b` がまったく別のオプションだとしたら、 :option:`-ab`
   をどうやって解析すればいいのでしょうか？ こうした曖昧さが存在するため、:mod:`optparse` は今のところこの機能をサポートしていません。

固定引数 (positional argument)
   他のオプションが解析される、すなわち他のオプションとその引数が 解析されて引数リストから除去された後に引数リストに置かれている ものです。

必須のオプション (required option)
   コマンドラインで与えなければならないオプションです; 「必須なオプション (required
   option)」という語は、英語では矛盾した言葉です。:mod:`optparse`
   では必須オプションの実装を妨げてはいませんが、とりたてて実装上役立つこともしていません。 :mod:`optparse`
   で必須オプションを実装する方法は、:mod:`optparse` ソースコード配布物中の``examples/required_1.py`` や
   ``examples/required_2.py`` を参照してください。

例えば、下記のような架空のコマンドラインを考えてみましょう::

   prog -v --report /tmp/report.txt foo bar

``"-v"`` と``"--report"`` はどちらもオプションです。 :option:`--report` オプションが引数をとるとすれば、
``"/tmp/report.txt"`` はオプションの引数です。 ``"foo"``と``"bar"`` は固定引数になります。


.. _optparse-what-options-for:

オプションとは何か
^^^^^^^^^

オプションはプログラムの実行を調整したり、カスタマイズしたりするための補助的な
情報を与えるために使います。もっとはっきりいうと、オプションはあくまでもオプション
(省略可能)であるということです。本来、プログラムはともかくもオプションなしでうまく 実行できてしかるべきです。(Unix やGNU
ツールセットのプログラムをランダムに ピックアップしてみてください。オプションを全く指定しなくてもちゃんと動くでしょう？ 例外は``find``,
``tar``, ``dd`` くらいです---これらの例外は、 オプション文法が標準的でなく、インタフェースが混乱を招くと酷評されてきた変種の
はみ出しものなのです)

多くの人が自分のプログラムに「必須のオプション」を持たせたいと考えます。しかし よく考えてください。必須なら、それは*オプション(省略可能) ではないのです！*
プログラムを正しく動作させるのに絶対的に必要な情報があるとすれば、そこには 固定引数を割り当てるべきなのです。

良くできたコマンドラインインタフェース設計として、ファイルのコピーに使われる ``cp`` ユーティリティのことを考えてみましょう。ファイルのコピーでは、
コピー先を指定せずにファイルをコピーするのは無意味な操作ですし、少なくとも一つの コピー元が必要です。従って、``cp`` は引数無しで実行すると失敗します。
とはいえ、``cp`` はオプションを全く必要としない柔軟で便利なコマンドライン 文法を備えています::

   cp SOURCE DEST
   cp SOURCE ... DEST-DIR

まだあります。ほとんどの ``cp`` の実装では、ファイルモードや変更時刻を変えずに
コピーする、シンボリックリンクの追跡を行わない、すでにあるファイルを上書きする前に
ユーザに尋ねる、など、ファイルをコピーする方法をいじるための一連のオプションを実装
しています。しかし、こうしたオプションは、一つのファイルを別の場所にコピーする、 または複数のファイルを別のディレクトリにコピーするという、``cp``
の中心的な処理 を乱すことはないのです。


.. _optparse-what-positional-arguments-for:

固定引数とは何か
^^^^^^^^

固定引数とは、プログラムを動作させる上で絶対的に必要な情報となる引数です。

よいユーザインタフェースとは、可能な限り少ない固定引数をもつものです。 プログラムを正しく動作させるために 17 個もの別個の情報が必要だとしたら、
その*方法* はさして問題にはなりません ---ユーザはプログラムを正しく 動作させられないうちに諦め、立ち去ってしまうからです。
ユーザインタフェースがコマンドラインでも、設定ファイルでも、GUI やその他の 何であっても同じです: 多くの要求をユーザに押し付ければ、ほとんどのユーザはただ
音をあげてしまうだけなのです。

要するに、ユーザが絶対に提供しなければならない情報だけに制限する --- そして可能な限りよく練られたデフォルト設定を使うよう試みてください。
もちろん、プログラムには適度な柔軟性を持たせたいとも望むはずですが、 それこそがオプションの果たす役割です。繰り返しますが、設定ファイルのエントリ であろうが、
GUI でできた「環境設定」ダイアログ上のウィジェットであろうが、 コマンドラインオプションであろうが関係ありません ---
より多くのオプションを実装すればプログラムはより柔軟性を持ちますが、 実装はより難解になるのです。高すぎる柔軟性はユーザを閉口させ、コードの維持を
より難しくするのです。


.. _optparse-tutorial:

Tutorial
--------

:mod:`optparse` はとても柔軟で強力でありながら、ほとんどの場合には簡単に利用 できます。この節では、:mod:`optparse`
ベースのプログラムで広く使われて いるコードパターンについて述べます。

まず、:class:`OptionParser` クラスを import しておかねばなりません。 次に、プログラムの冒頭で
:class:`OptionParser` インスタンスを生成しておきます::

   from optparse import OptionParser
   [...]
   parser = OptionParser()

これでオプションを定義できるようになりました。基本的な構文は以下の通りです::

   parser.add_option(opt_str, ...,
                     attr=value, ...)

各オプションには、``"-f"`` や``"--file"`` のような一つまたは複数の
オプション文字列と、パーザがコマンドライン上のオプションを見つけた際に、 何を準備し、何を行うべきかを:mod:`optparse`
に教えるためのオプション属性 (option attribute)がいくつか入ります。

通常、各オプションには短いオプション文字列と長いオプション文字列があります。 例えば::

   parser.add_option("-f", "--file", ...)

といった具合です。

オプション文字列は、(ゼロ文字の場合も含め)いくらでも短く、またいくらでも長く できます。ただしオプション文字列は少なくとも一つなければなりません。

:meth:`add_option` に渡されたオプション文字列は、実際にはこの 関数で定義したオプションに対するラベルになります。簡単のため、以後では
コマンドライン上で*オプションを見つける* という表現をしばしば使いますが、 これは実際には:mod:`optparse`
がコマンドライン上の*オプション文字列* を見つけ、対応づけされているオプションを捜し出す、という処理に相当します。

オプションを全て定義したら、:mod:`optparse` にコマンドラインを解析するように 指示します::

   (options, args) = parser.parse_args()

(お望みなら、:meth:`parse_args` に自作の引数リストを渡してもかまいません。 とはいえ、実際にはそうした必要はほとんどないでしょう:
:mod:`optionparser` はデフォルトで``sys.argv[1:]``を使うからです。)

:meth:`parse_args` は二つの値を返します:

*   全てのオプションに対する値の入ったオブジェクト``options`` --- 例えば、 ``"--file"``
  が単一の文字列引数をとる場合、``options.file`` は ユーザが指定したファイル名になります。オプションを指定しなかった場合には ``None``
  になります。

*   オプションの解析後に残った固定引数からなるリスト``args``。

このチュートリアルの節では、最も重要な四つのオプション属性: :attr:`action`, :attr:`type`, :attr:`dest`
(destination), および :attr:`help` についてしか触れません。このうち最も重要なのは:attr:`action` です。


.. _optparse-understanding-option-actions:

オプション・アクションを理解する
^^^^^^^^^^^^^^^^

アクション(action)は:mod:`optparse` が コマンドライン上にあるオプションを
見つけたときに何をすべきかを指示します。:mod:`optparse` には押し着せの アクションのセットがハードコードされています。
新たなアクションの追加は上級者向けの話題であり、 :ref:`optparse-extending-optparse` の「:mod:`optparse`
の拡張」で触れます。 ほとんどのアクションは、値を何らかの変数に記憶するよう:mod:`optparse` に 指示します ---
例えば、文字列をコマンドラインから取り出して、``options`` の 属性の中に入れる、といった具合にです。

オプション・アクションを指定しない場合、:mod:`optparse` のデフォルトの動作は ``store`` になります。


.. _optparse-store-action:

store アクション
^^^^^^^^^^^

もっとも良く使われるアクションは ``store`` です。このアクションは 次の引数 (あるいは現在の引数の残りの部分) を取り出し、正しい型の値か確かめ、
指定した保存先に保存するよう:mod:`optparse` に指示します。

例えば::

   parser.add_option("-f", "--file",
                     action="store", type="string", dest="filename")

のように指定しておき、偽のコマンドラインを作成して :mod:`optparse` に 解析させてみましょう::

   args = ["-f", "foo.txt"]
   (options, args) = parser.parse_args(args)

オプション文字列 ``"-f"`` を見つけると、:mod:`optparse` は次の 引数である ``"foo.txt"`` を消費し、その値を
``options.filename`` に 保存します。従って、この:meth:`parse_args`呼び出し後には
``options.filename`` は``"foo.txt"``になっています。

オプションの型として、:mod:`optparse` は他にも``int`` や``float`` をサポートしています。

整数の引数を想定したオプションの例を示します::

   parser.add_option("-n", type="int", dest="num")

このオプションには長い形式のオプション文字列がないため、設定に問題がないという ことに注意してください。また、デフォルトのアクションは ``store``
なので、 ここでは action を明示的に指定していません。

架空のコマンドラインをもう一つ解析してみましょう。今度は、オプション引数を オプションの右側にぴったりくっつけて一緒くたにします: :option:`-n42`
(一つの引数のみ) は :option:`-n 42` (二つの引数からなる) と等価になるので、 ::

   (options, args) = parser.parse_args(["-n42"])
   print options.num

は ``"42"`` を出力します。

型を指定しない場合、 :mod:`optparse` は引数を``string`` であると仮定します。 デフォルトのアクションが ``store``
であることも併せて考えると、最初の例はもっと 短くなります::

   parser.add_option("-f", "--file", dest="filename")

保存先 (destination) を指定しない場合、 :mod:`optparse` はデフォルト値として オプション文字列から気のきいた名前を設定します:
最初に指定した長い形式のオプション 文字列が``"--foo-bar"`` であれば、デフォルトの保存先は ``foo_bar``
になります。長い形式のオプション文字列がなければ、:mod:`optparse` は最初に指定 した短い形式のオプション文字列を探します:
例えば、``"-f"`` に対する保存先は ``f`` になります。

:mod:`optparse` では、``long`` や``complex`` といった組み込み型も 取り入れています。型の追加は:ref
:`optparse-extending-optparse` 節の 「:mod:`optparse` の拡張」で触れています。


.. _optparse-handling-boolean-options:

ブール値 (フラグ) オプションの処理
^^^^^^^^^^^^^^^^^^^

フラグオプション---特定のオプションに対して真または偽の値の値を設定するオプション--- はよく使われます。:mod:`optparse`
では、二つのアクション、``store_true`` および ``store_false`` をサポートしています。例えば、 ``verbose``
というフラグを``"-v"`` で有効にして、``"-q"`` で無効に したいとします::

   parser.add_option("-v", action="store_true", dest="verbose")
   parser.add_option("-q", action="store_false", dest="verbose")

ここでは二つのオプションに同じ保存先を指定していますが、全く問題ありません (下記のように、デフォルト値の設定を少し注意深く行わねばならないだけです)

``"-v"`` をコマンドライン上に見つけると、:mod:`optparse` は ``options.verbose`` を ``True``
に設定します。``"-q"`` を見つければ、``options.verbose`` は ``False`` にセットされます。


.. _optparse-other-actions:

その他のアクション
^^^^^^^^^

この他にも、:mod:`optparse` は以下のようなアクションをサポートしています:

``store_const``
   定数値を保存します。

``append``
   オプションの引数を指定のリストに追加します。

``count``
   指定のカウンタを 1 増やします。

``callback``
   指定の関数を呼び出します。

これらのアクションについては、:ref:`optparse-reference-guide` 節の 「リファレンスガイド」および:ref:`optparse-
option-callbacks` 節の 「オプション・コールバック」で触れます。


.. _optparse-default-values:

デフォルト値
^^^^^^

上記の例は全て、何らかのコマンドラインオプションが見つかった時に 何らかの変数 (保存先: destination) に値を設定していました。
では、該当するオプションが見つからなかった場合には何が起きるのでしょうか？ デフォルトは全く与えていないため、これらの値は全て ``None`` になります。
たいていはこれで十分ですが、もっときちんと制御したい場合もあります。 :mod:`optparse` では各保存先に対してデフォルト値を指定し、コマンドライン
の解析前にデフォルト値が設定されるようにできます。

まず、 verbose/quiet の例について考えてみましょう。:mod:`optparse` に 対して、``"-q"`` がない限り
``verbose`` を ``True`` に設定 させたいなら、以下のようにします::

   parser.add_option("-v", action="store_true", dest="verbose", default=True)
   parser.add_option("-q", action="store_false", dest="verbose")

デフォルトの値は特定のオプションではなく *保存先* に対して適用されます。 また、これら二つのオプションはたまたま同じ保存先を持っているにすぎないため、
上のコードは下のコードと全く等価になります::

   parser.add_option("-v", action="store_true", dest="verbose")
   parser.add_option("-q", action="store_false", dest="verbose", default=True)

下のような場合を考えてみましょう::

   parser.add_option("-v", action="store_true", dest="verbose", default=False)
   parser.add_option("-q", action="store_false", dest="verbose", default=True)

やはり``verbose`` のデフォルト値は ``True`` になります; 特定の目的変数に対するデフォルト値として有効なのは、最後に指定した値だからです。

デフォルト値をすっきりと指定するには、:class:`OptionParser` の :meth:`set_defaults`
メソッドを使います。このメソッドは :meth:`parse_args` を呼び出す前ならいつでも使えます::

   parser.set_defaults(verbose=True)
   parser.add_option(...)
   (options, args) = parser.parse_args()

前の例と同様、あるオプションの値の保存先に対するデフォルトの値は最後に指定した
値になります。コードを読みやすくするため、デフォルト値を設定するときには両方のやり方 を混ぜるのではなく、片方だけを使うようにしましょう。


.. _optparse-generating-help:

ヘルプの生成
^^^^^^

:mod:`optparse` にはヘルプと使い方の説明 (usage text) を生成する機能があり、
ユーザに優しいコマンドラインインタフェースを作成する上で役立ちます。 やらなければならないのは、各オプションに対する:attr:`help` の値と、
必要ならプログラム全体の使用法を説明する短いメッセージを与えることだけです。

ユーザフレンドリな (ドキュメント付きの) オプションを追加した :class:`OptionParser` を以下に示します::

   usage = "usage: %prog [options] arg1 arg2"
   parser = OptionParser(usage=usage)
   parser.add_option("-v", "--verbose",
                     action="store_true", dest="verbose", default=True,
                     help="make lots of noise [default]")
   parser.add_option("-q", "--quiet",
                     action="store_false", dest="verbose", 
                     help="be vewwy quiet (I'm hunting wabbits)")
   parser.add_option("-f", "--filename",
                     metavar="FILE", help="write output to FILE"),
   parser.add_option("-m", "--mode",
                     default="intermediate",
                     help="interaction mode: novice, intermediate, "
                          "or expert [default: %default]")

:mod:`optparse` がコマンドライン上で``"-h"`` や``"--help"`` を
見つけた場合やユーザが:meth:`parser.print_help` を呼び出した場合、 この:class:`OptionParser`
は以下のようなメッセージを標準出力に出力します::

   usage: <yourscript> [options] arg1 arg2

   options:
     -h, --help            show this help message and exit
     -v, --verbose         make lots of noise [default]
     -q, --quiet           be vewwy quiet (I'm hunting wabbits)
     -f FILE, --filename=FILE
                           write output to FILE
     -m MODE, --mode=MODE  interaction mode: novice, intermediate, or
                           expert [default: intermediate]

(help オプションでヘルプを出力した場合、:mod:`optparse` は出力後に プログラムを終了します。)

:mod:`optparse` ができるだけうまくメッセージを生成するよう手助けするには、 他にもまだまだやるべきことがあります:

*   スクリプト自体の利用法を表すメッセージを定義します::

     usage = "usage: %prog [options] arg1 arg2"

  :mod:`optparse` は ``"%prog"`` を現在のプログラム名、すなわち ``os.path.basename(sys.argv[0])``
  と置き換えます。この文字列は 詳細なオプションヘルプの前に展開され出力されます。

  usage の文字列を指定しない場合、:mod:`optparse` は型どおりとはいえ 気の効いたデフォルト値、 ``"usage: %prog
  [options]"`` を 使います。固定引数をとらないスクリプトの場合はこれで十分でしょう。

*   全てのオプションにヘルプ文字列を定義します。行の折り返しは気にしなくて かまいません --- :mod:`optparse`
  は行の折り返しに気を配り、見栄えの よいヘルプ出力を生成します。

*   オプションが値をとるということは自動的に生成されるヘルプメッセージの中で 分かります。例えば、"mode" option の場合には::

     -m MODE, --mode=MODE

  のようになります。

  ここで "MODE" はメタ変数 (meta-variable) と呼ばれます: メタ変数は、 ユーザが
  :option:`-m`/:option:`--mode` に対して指定するはずの 引数を表します。デフォルトでは、:mod:`optparse`
  は保存先の変数名を 大文字だけにしたものをメタ変数に使います。これは時として期待通りの結果に なりません ---
  例えば、上の例の:option:`--filename` オプションでは 明示的に ``metavar="FILE"`` を設定しており、その結果自動生成された
  オプション説明テキストは::

     -f FILE, --filename=FILE

  のようになります。

  この機能の重要さは、単に表示スペースを節約するといった理由にとどまりません:  上の例では、手作業で書いたヘルプテキストの中でメタ変数として "FILE" を
  使っています。その結果、ユーザに対してやや堅苦しい表現の書法 "-f FILE" と、より平易に意味付けを説明した "write output to FILE"
  との間に 対応があるというヒントを与えています。これは、エンドユーザにとってより明解で 便利なヘルプテキストを作成する単純でありながら効果的な手法なのです。

*   デフォルト値を持つオプションのヘルプ文字列には``%default`` を入れられ ます --- :mod:`optparse`
  は``%default`` をデフォルト値の :func:`str` で置き換えます。該当するオプションにデフォルト値がない場合 (あるいはデフォルト値が
  ``None`` である場合) ``%default`` の 展開結果は ``none`` になります。


.. _optparse-printing-version-string:

バージョン番号の出力
^^^^^^^^^^

:mod:`optparse` では、使用法メッセージと同様にプログラムのバージョン文字列を 出力できます。:class:`OptionParser`
の``version`` 引数に文字列を渡します::

   parser = OptionParser(usage="%prog [-f] [-q]", version="%prog 1.0")

``"%prog"`` は*usage* と同じような展開を受けます。 その他にも``version`` には何でも好きな内容を入れられます。
``version`` を指定した場合、:mod:`optparse` は自動的に``"--version"`` オプションをパーザに渡します。
コマンドライン中に``"--version"`` が見つかると、:mod:`optparse` は``version`` 文字列を展開して
(``"%prog"`` を置き換えて) 標準出力に出力し、プログラムを終了します。

例えば、 ``/usr/bin/foo`` という名前のスクリプトなら::

   $ /usr/bin/foo --version
   foo 1.0

のようになります。


.. _optparse-how-optparse-handles-errors:

:mod:`optparse` のエラー処理法
^^^^^^^^^^^^^^^^^^^^^^^

:mod:`optparse` を使う場合に気を付けねばならないエラーには、 大きく分けてプログラマ側のエラーとユーザ側のエラーという二つの種類があります。
プログラマ側のエラーの多くは、例えば不正なオプション文字列や定義されていない オプション属性の指定、あるいはオプション属性を指定し忘れるといった、
誤った``parser.add_option()`` 呼び出しによるものです。
こうした誤りは通常通りに処理されます。すなわち、例外(``optparse.OptionError`` や ``TypeError``)
を送出して、プログラムをクラッシュさせます。 もっと重要なのはユーザ側のエラーの処理です。というのも、ユーザの操作エラーという
ものはコードの安定性に関係なく起こるからです。 :mod:`optparse` は、誤ったオプション引数の指定 (整数を引数にとるオプション
:option:`-n` に対して ``"-n4x"`` と指定してしまうなど) や、引数を 指定し忘れた場合 (:option:`-n`
が何らかの引数をとるオプションであるのに、 ``"-n"`` が引数の末尾に来ている場合) といった、ユーザによるエラーを自動的に
検出します。また、アプリケーション側で定義されたエラー条件が起きた場合、 ``parser.error()`` を呼び出してエラーを通知できます::

   (options, args) = parser.parse_args()
   [...]
   if options.a and options.b:
       parser.error("options -a and -b are mutually exclusive")

いずれの場合にも :mod:`optparse` はエラーを同じやり方で処理します。すなわち、
プログラムの使用法メッセージとエラーメッセージを標準エラー出力に出力して、 終了ステータス 2 でプログラムを終了させます。

上に挙げた最初の例、すなわち整数を引数にとるオプションにユーザが ``"4x"`` を 指定した場合を考えてみましょう::

   $ /usr/bin/foo -n 4x
   usage: foo [options]

   foo: error: option -n: invalid integer value: '4x'

値を全く指定しない場合には、以下のようになります::

   $ /usr/bin/foo -n
   usage: foo [options]

   foo: error: -n option requires an argument

:mod:`optparse` は、常にエラーを引き起こしたオプションについて説明の入った エラーメッセージを生成するよう気を配ります;
従って、``parser.error()`` を アプリケーションコードから呼び出す場合にも、同じようなメッセージになるように してください。

:mod:`optparse` のデフォルトのエラー処理動作が気に入らないのなら、 :class:`OptionParser`
をサブクラス化して、``exit()`` かつ/または :meth:`error` をオーバライドする必要があります。


.. _optparse-putting-it-all-together:

全てをつなぎ合わせる
^^^^^^^^^^

:mod:`optparse` を使ったスクリプトは、通常以下のようになります::

   from optparse import OptionParser
   [...]
   def main():
       usage = "usage: %prog [options] arg"
       parser = OptionParser(usage)
       parser.add_option("-f", "--file", dest="filename",
                         help="read data from FILENAME")
       parser.add_option("-v", "--verbose",
                         action="store_true", dest="verbose")
       parser.add_option("-q", "--quiet",
                         action="store_false", dest="verbose")
       [...]
       (options, args) = parser.parse_args()
       if len(args) != 1:
           parser.error("incorrect number of arguments")
       if options.verbose:
           print "reading %s..." % options.filename
       [...]

   if __name__ == "__main__":
       main()


.. _optparse-reference-guide:

リファレンスガイド
---------


.. _optparse-creating-parser:

Creating the parser
^^^^^^^^^^^^^^^^^^^

:mod:`optparse` を使う最初の一歩は OptionParser インスタンスを作ることです。  ::

   parser = OptionParser(...)

OptionParser のコンストラクタの引数はどれも必須ではありませんが、いくつ ものキーワード引数がオプションとして使えます。これらはキーワード引数と
して渡さなければなりません。すなわち、引数が宣言されている順番に頼っては いけません。

   ``usage`` (デフォルト: ``"%prog [options]"``)
      プログラムが間違った方法で実行されるかまたはヘルプオプションを付けて 実行された場合に表示される使用法です。:mod:`optparse` は使用法の文
      字列を表示する際に ``%prog`` を ``os.path.basename(sys.argv[0])`` (または ``prog``
      キーワード引数が指定されていればその値) に展開します。 使用法メッセージを抑制するためには特別な ``optparse.SUPPRESS_USAGE``
      という値を指定します。

   ``option_list`` (デフォルト: ``[]``)
      パーザに追加する Option オブジェクトのリストです。``option_list`` の 中のオプションは ``standard_option_list``
      (OptionParser の サブクラスでセットされる可能性のあるクラス属性) の後に追加されますが、バージョンや ヘルプのオプションよりは前になります。
      このオプションの使用は推奨されません。パーザを作成した後で、:meth:`add_option` を使って追加してください。

   ``option_class`` (デフォルト: optparse.Option)
      :meth:`add_option` でパーザにオプションを追加するときに使用されるクラス。

   ``version`` (デフォルト: ``None``)
      ユーザがバージョンオプションを与えたときに表示されるバージョン文字列です。 ``version`` に真の値を与えると、:mod:`optparse`
      は自動的に 単独のオプション文字列 ``"--version"`` とともにバージョンオプションを 追加します。部分文字列 ``"%prog"`` は
      ``usage`` と同様に 展開されます。

   ``conflict_handler`` (デフォルト: ``"error"``)
      オプション文字列が衝突するようなオプションがパーザに追加されたときにどうするかを 指定します。:ref:`optparse-conflicts-between-
      options` 節「オプション間の衝突」 を参照して下さい。

   ``description`` (デフォルト: ``None``)
      プログラムの概要を表す一段落のテキストです。:mod:`optparse` は ユーザがヘルプを要求したときにこの概要を現在のターミナルの幅に合わせて
      整形し直して表示します (``usage`` の後、オプションリストの前に表示されます)。

   ``formatter`` (デフォルト: 新しい IndentedHelpFormatter)
      ヘルプテキストを表示する際に使われる optparse.HelpFormatter のインスタンスです。 :mod:`optparse`
      はこの目的のためにすぐ使えるクラスを二つ提供しています。 IndentedHelpFormatter と TitledHelpFormatter がそれです。

   ``add_help_option`` (デフォルト: ``True``)
      もし真ならば、:mod:`optparse` はパーザにヘルプオプションを (オプション文字列 ``"-h"`` と ``"--help"`` とともに)
      追加します。

   ``prog``
      ``usage`` や ``version`` の中の ``"%prog"`` を展開するときに
      ``os.path.basename(sys.argv[0])`` の代わりに使われる文字列です。



.. _optparse-populating-parser:

パーザへのオプション追加
^^^^^^^^^^^^

パーザにオプションを加えていくにはいくつか方法があります。推奨するのは :ref:`optparse-tutorial` 節のチュートリアルで示したような
``OptionParser.add_option()`` を使う方法です。 :meth:`add_option` は以下の二つのうちいずれかの方法で
呼び出せます:

*   :func:`make_option`に (すなわち:class:`Option` のコンストラクタに)
  固定引数とキーワード引数の組み合わせを渡して、:class:`Option` インスタンスを 生成させます。

*  (:func:`make_option` などが返す):class:`Option`インスタンスを渡します。

もう一つの方法は、あらかじめ作成しておいた:class:`Option` インスタンスから なるリストを、以下のようにして
:class:`OptionParser` のコンストラクタに渡す というものです::

   option_list = [
       make_option("-f", "--filename",
                   action="store", type="string", dest="filename"),
       make_option("-q", "--quiet",
                   action="store_false", dest="verbose"),
       ]
   parser = OptionParser(option_list=option_list)

(:func:`make_option` は :class:`Option` インスタンスを生成する ファクトリ関数です;
現在のところ、個の関数は:class:`Option` のコンストラクタの
別名にすぎません。:mod:`optparse`の将来のバージョンでは、:class:`Option` を
複数のクラスに分割し、:func:`make_option` は適切なクラスを選んで
インスタンスを生成するようになる予定です。従って、:class:`Option` を直接 インスタンス化しないでください。)


.. _optparse-defining-options:

オプションの定義
^^^^^^^^

各々の:class:`Option` インスタンス、は:option:`-f` や:option:`--file`
といった同義のコマンドラインオプションからなる集合を表現しています。 一つの:class:`Option` には任意の数のオプションを短い形式でも長い形式でも
指定できます。ただし、少なくとも一つは指定せねばなりません。

正しい方法で:class:`Option` インスタンスを生成するには、 :class:`OptionParser` の :meth:`add_option`
を使います::

   parser.add_option(opt_str[, ...], attr=value, ...)

短い形式のオプション文字列を一つだけ持つようなオプションを生成するには::

   parser.add_option("-f", attr=value, ...)

のようにします。

また、長い形式のオプション文字列を一つだけ持つようなオプションの定義は::

   parser.add_option("--foo", attr=value, ...)

のようになります。

キーワード引数は新しい :class:`Option` オブジェクトの属性を定義します。オプションの属性のうちでもっとも重要なのは :attr:`action`
です。:attr:`action` は他のどの属性と関連があるか、そして どの属性が必要かに大きく作用します。関係のないオプション属性を指定したり、
必要な属性を指定し忘れたりすると、:mod:`optparse` は誤りを解説した :exc:`OptionError`例外を送出します。

コマンドライン上にあるオプションが見つかったときの:mod:`optparse` の 振舞いを決定しているのは *アクション(action)* です。
:mod:`optparse` でハードコードされている標準的なアクションには 以下のようなものがあります:

``store``
   オプションの引数を保存します (デフォルトの動作です)

``store_const``
   定数を保存します

``store_true``
   真 (:const:`True`) を保存します

``store_false``
   偽 (:const:`False`) を保存します

``append``
   オプションの引数をリストに追加します

``append_const``
   定数をリストに追加します

``count``
   カウンタを一つ増やします

``callback``
   指定された関数を呼び出します

:attr:`help`
   全てのオプションとそのドキュメントの入った使用法メッセージを出力します。

(アクションを指定しない場合、デフォルトは ``store`` になります。このアクション では、 :attr:`type` および :attr:`dest`
オプション属性を指定せねばなりません。 下記を参照してください。)

すでにお分かりのように、ほとんどのアクションはどこかに値を保存したり、値を更新 したりします。 この目的のために、:mod:`optparse`
は常に特別なオブジェクトを作り出し、 それは通常 ``options`` と呼ばれます (``optparse.Values`` の
インスタンスになっています)。 オプションの引数 (や、その他の様々な値) は、:attr:`dest` (保存先:  destination)
オプション属性に従って、*options*の属性として保存されます。

例えば、  ::

   parser.parse_args()

を呼び出した場合、:mod:`optparse` はまず ``options`` オブジェクト を生成します::

   options = Values()

パーザ中で以下のようなオプション  ::

   parser.add_option("-f", "--file", action="store", type="string", dest="filename")

が定義されていて、パーズしたコマンドラインに以下のいずれかが入っていた場合::

   -ffoo
   -f foo
   --file=foo
   --file foo

:mod:`optparse` はこのオプションを見つけて、 ::

   options.filename = "foo"

と同等の処理を行います。

:attr:`type` および :attr:`dest` オプション属性は :attr:`action` と同じくらい 重要ですが、*全ての*
オプションで意味をなすのは:attr:`action` だけなのです。


.. _optparse-standard-option-actions:

標準的なオプション・アクション
^^^^^^^^^^^^^^^

様々なオプション・アクションにはどれも互いに少しづつ異なった条件と作用があります。 ほとんどのアクションに関連するオプション属性がいくつかあり、値を指定して
:mod:`optparse`の挙動を操作できます; いくつかのアクションには必須の属性 があり、必ず値を指定せねばなりません。

*   ``store`` [relevant: :attr:`type`, :attr:`dest`, ``nargs``, ``choices``]

  オプションの後には必ず引数が続きます。引数は:attr:`type` に従った値に変換されて :attr:`dest` に保存されます。*nargs* > 1
  の場合、 複数の引数をコマンドラインから取り出します; 引数は全て :attr:`type` に従って 変換され、:attr:`dest`
  にタプルとして保存されます。 下記の :ref:`optparse-standard-option-types` 節「標準のオプション型」 を
  参照してください。

  ``choices`` を(文字列のリストかタプルで) 指定した場合、型のデフォルト値は "choice" になります。

  :attr:`type` を指定しない場合、デフォルトの値は ``string`` です。

  :attr:`dest` を指定しない場合、 :mod:`optparse` は保存先を最初の長い形式の オプション文字列から導出します
  (例えば、``"--foo-bar"`` は ``foo_bar`` になります)。長い形式のオプション文字列がない場合、 :mod:`optparse`
  は最初の短い形式のオプションから保存先の変数名を導出します (``"-f"`` は ``f`` になります)。

  例えば::

     parser.add_option("-f")
     parser.add_option("-p", type="float", nargs=3, dest="point")

  とすると、以下のようなコマンドライン::

     -f foo.txt -p 1 -3.5 4 -fbar.txt

  を解析した場合、:mod:`optparse` は  ::

     options.f = "foo.txt"
     options.point = (1.0, -3.5, 4.0)
     options.f = "bar.txt"

  のように設定を行います。

*   ``store_const`` [required: ``const``; relevant: :attr:`dest`]

  値``cost`` を:attr:`dest` に保存します。

  例えば::

     parser.add_option("-q", "--quiet",
                       action="store_const", const=0, dest="verbose")
     parser.add_option("-v", "--verbose",
                       action="store_const", const=1, dest="verbose")
     parser.add_option("--noisy",
                       action="store_const", const=2, dest="verbose")

  とします。

  ``"--noisy"`` が見つかると、 :mod:`optparse` は  ::

     options.verbose = 2

  のように設定を行います。

*   ``store_true`` [relevant: :attr:`dest`]

  ``store_const`` の特殊なケースで、真 (True) を:attr:`dest` に保存します。

*   ``store_false`` [relevant: :attr:`dest`]

  ``store_true`` と同じですが、偽 (False) を保存します。

  例::

     parser.add_option("--clobber", action="store_true", dest="clobber")
     parser.add_option("--no-clobber", action="store_false", dest="clobber")

*   ``append`` [relevant: :attr:`type`, :attr:`dest`, ``nargs``, ``choices``]

  このオプションの後ろには必ず引数が続きます。引数は:attr:`dest` のリストに 追加されます。:attr:`dest`
  のデフォルト値を指定しなかった場合、 :mod:`optparse` がこのオプションを最初にみつけた時点で空のリストを自動的に生成します。 ``nargs``
  > 1 の場合、複数の引数をコマンドラインから取り出し、 長さ ``nargs`` のタプルを生成して :attr:`dest`に追加します。

  :attr:`type` および :attr:`dest` のデフォルト値は ``store`` アクションと 同じです。

  例::

     parser.add_option("-t", "--tracks", action="append", type="int")

  ``"-t3"`` がコマンドライン上で見つかると、:mod:`optparse` は::

     options.tracks = []
     options.tracks.append(int("3"))

  と同等の処理を行います。

  その後、``"--tracks=4"`` が見つかると::

     options.tracks.append(int("4"))

  を実行します。

*   ``append_const`` [required: ``const``; relevant: :attr:`dest`]

  ``store_const`` と同様ですが、``const`` の値は :attr:`dest` に 追加(append)されます。 ``append``
  の場合と同じように :attr:`dest` のデフォルトは ``None`` ですが このオプションを最初にみつけた時点で空のリストを自動的に生成します。

*   ``count`` [relevant: :attr:`dest`]

  :attr:`dest` に保存されている整数値をインクリメントします。 :attr:`dest` は (デフォルトの値を指定しない限り)
  最初にインクリメントを 行う前にゼロに設定されます。

  例::

     parser.add_option("-v", action="count", dest="verbosity")

  コマンドライン上で最初に ``"-v"`` が見つかると、:mod:`optparse` は::

     options.verbosity = 0
     options.verbosity += 1

  と同等の処理を行います。

  以後、``"-v"`` が見つかるたびに、  ::

     options.verbosity += 1

  を実行します。

*   ``callback`` [required: ``callback``; relevant: :attr:`type`, ``nargs``,
  ``callback_args``, ``callback_kwargs``]

  ``callback`` に指定された関数を次のように呼び出します。  ::

     func(option, opt_str, value, parser, *args, **kwargs)

  詳細は、:ref:`optparse-option-callbacks` 節「オプション処理コールバック」を 参照してください。

*   :attr:`help`

  現在のオプションパーザ内の全てのオプションに対する完全なヘルプメッセージを出力します。 ヘルプメッセージは :class:`OptionParser`
  のコンストラクタに渡した``usage``  文字列と、各オプションに渡した :attr:`help` 文字列から生成します。

  オプションに :attr:`help` 文字列が指定されていなくても、オプションは
  ヘルプメッセージ中に列挙されます。オプションを完全に表示させないようにするには、 特殊な値 ``optparse.SUPPRESS_HELP``
  を使ってください。

  :mod:`optparse` は全ての:class:`OptionParser` に自動的に:attr:`help`
  オプションを追加するので、通常自分で生成する必要はありません。

  例::

     from optparse import OptionParser, SUPPRESS_HELP

     parser = OptionParser()
     parser.add_option("-h", "--help", action="help"),
     parser.add_option("-v", action="store_true", dest="verbose",
                       help="Be moderately verbose")
     parser.add_option("--file", dest="filename",
                       help="Input file to read data from"),
     parser.add_option("--secret", help=SUPPRESS_HELP)

  :mod:`optparse` がコマンドライン上に ``"-h"`` または  ``"--help"`` を見つけると、以下のようなヘルプメッセージを
  標準出力に出力します (``sys.argv[0]`` は``"foo.py"`` だとします)::

     usage: foo.py [options]

     options:
       -h, --help        Show this help message and exit
       -v                Be moderately verbose
       --file=FILENAME   Input file to read data from

  ヘルプメッセージの出力後、:mod:`optparse` は ``sys.exit(0)`` でプロセスを終了します。

*   ``version``

  :class:`OptionParser` に指定されているバージョン番号を標準出力に 出力して終了します。バージョン番号は、実際には
  :class:`OptionParser` の:meth:`print_version` メソッドで書式化されてから出力されます。 通常、
  :class:`OptionParser` のコンストラクタに *version* が指定されたときのみ関係のあるアクションです。 :attr:`help`
  オプションと同様、:mod:`optparse` はこのオプションを 必要に応じて自動的に追加するので、``version`` オプションを作成する
  ことはほとんどないでしょう。


.. _optparse-option-attributes:

オプション属性
^^^^^^^

以下のオプション属性は ``parser.add_option()`` へのキーワード引数として
渡すことができます。特定のオプションに無関係なオプション属性を渡した場合、 または必須のオプションを渡しそこなった場合、:mod:`optparse` は
OptionError を送出します。

*  :attr:`action` (デフォルト: ``"store"``)

  このオプションがコマンドラインにあった場合に :mod:`optparse` に何をさせるかを決めます。 取りうるオプションについては既に説明しました。

*   :attr:`type` (デフォルト: ``"string"``)

  このオプションに与えられる引数の型 (たとえば ``"string"`` や ``"int"``) です。取りうるオプションの型については既に説明しました。

*   :attr:`dest` (デフォルト: オプション文字列から)

  このオプションのアクションがある値をどこかに書いたり書き換えたりを意味する場合、 これは :mod:`optparse` にその書く場所を教えます。詳しく言えば
  :attr:`dest` には :mod:`optparse` がコマンドラインを解析しながら 組み立てる ``options``
  オブジェクトの属性の名前を指定します。

*   ``default`` (非推奨)

  コマンドラインに指定がなかったときにこのオプションの対象に使われる値です。 使用は推奨されません。代わりに ``parser.set_defaults()``
  を使ってください。

*   ``nargs`` (デフォルト: 1)

  このオプションがあったときに幾つの :attr:`type` 型の引数が消費されるべきかを 指定します。もし > 1 ならば、:mod:`optparse` は
  :attr:`dest` に値のタプルを格納します。

*   ``const``

  定数を格納する動作のための、その定数です。

*   ``choices``

  ``"choice"`` 型オプションに対してユーザがその中から選べる文字列のリストです。

*   ``callback``

  アクションが ``"callback"`` であるオプションに対し、このオプションがあったときに 呼ばれる呼び出し可能オブジェクトです。``callable``
  に渡す引数の詳細については、 :ref:`optparse-option-callbacks` 節「オプション処理コールバック」を参照してください。

*   ``callback_args``, ``callback_kwargs``

  ``callback`` に渡される標準的な4つのコールバック引数の後ろに追加する 位置による引数またはキーワード引数です。

*   :attr:`help`

  ユーザが :attr:`help` オプション(``"--help"`` のような)を指定したときに
  表示される使用可能な全オプションのリストの中のこのオプションに関する説明文です。 説明文を提供しておかなければ、オプションは説明文なしで表示されます。
  オプションを隠すには特殊な値 ``SUPPRESS_HELP`` を使います。

*   ``metavar`` (デフォルト: オプション文字列から)

  説明文を表示する際にオプションの引数の身代わりになるものです。 例は :ref:`optparse-tutorial` 節のチュートリアルを参照してください。


.. _optparse-standard-option-types:

標準のオプション型
^^^^^^^^^

:mod:`optparse` には、:dfn:`string` (文字列)、:dfn:`int` (整数)、  :dfn:`long` (長整数)、
:dfn:`choice` (選択肢)、 :dfn:`float` (浮動小数点数)  および :dfn:`complex` (複素数) の 6
種類のオプション型があります。 新たなオプションの型を追加したければ、:ref:`optparse-extending-optparse` 節、
「:mod:`optparse` の拡張」を参照してください。

文字列オプションの引数はチェックや変換を一切受けません: コマンドライン上のテキストは 保存先にそのまま保存されます (またはコールバックに渡されます)。

整数引数 (``int`` 型や ``long`` 型) は次のように読み取られます。

*   数が ``0x`` から始まるならば、16進数として読み取られます

*   数が ``0`` から始まるならば、8進数として読み取られます

*   数が ``0b`` から始まるならば、2進数として読み取られます

*   それ以外の場合、数は10進数として読み取られます


変換は適切な底(2, 8, 10, 16 のどれか)とともに ``int()`` または ``long()`` を呼び出すことで行なわれます。
この変換が失敗した場合 :mod:`optparse` の処理も失敗に終わりますが、 より役に立つエラーメッセージを出力します。

``float`` および ``complex`` のオプション引数は直接 ``float()`` や ``complex()`` で変換されます。
エラーは同様の扱いです。

``choice`` オプションは ``string`` オプションのサブタイプです。 ``choice`` オプションの属性 (文字列からなるシーケンス)
には、利用できる オプション引数のセットを指定します。``optparse.check_choice()``
はユーザの指定したオプション引数とマスタリストを比較して、無効な文字列が 指定された場合には:exc:`OptionValueError` を送出します。


.. _optparse-parsing-arguments:

引数の解析
^^^^^

OptionParser を作成してオプションを追加していく上で大事なポイントは、 :meth:`parse_args` メソッドの呼び出しです。  ::

   (options, args) = parser.parse_args(args=None, options=None)

ここで入力パラメータは

``args``
   処理する引数のリスト (デフォルト: ``sys.argv[1:]``)

``options``
   オプション引数を格納するオブジェクト (デフォルト: 新しい optparse.Values のインスタンス)

であり、戻り値は

``options``
   ``options`` に渡されたものと同じオブジェクト、または :mod:`optparse` によって生成された optparse.Values
   インスタンス

``args``
   全てのオプションの処理が終わった後で残った位置引数

です。

一番普通の使い方は一切キーワード引数を使わないというものです。 ``options`` を指定した場合、それは繰り返される ``setattr()``
の呼び出し (大雑把に言うと保存される各オプション引数につき一回ずつ) で更新されていき、:meth:`parse_args` で返されます。

:meth:`parse_args` が引数リストでエラーに遭遇した場合、 OptionParser の :meth:`error`
メソッドを適切なエンドユーザ向けの エラーメッセージとともに呼び出します。この呼び出しにより、最終的に終了ステータス 2 (伝統的な Unix
におけるコマンドラインエラーの終了ステータス) でプロセスを終了させることになります。


.. _optparse-querying-manipulating-option-parser:

オプション解析器への問い合わせと操作
^^^^^^^^^^^^^^^^^^

自前のオプションパーザをつつきまわして、何が起こるかを調べると便利 なことがあります。:class:`OptionParser` では便利な二つのメソッドを提供
しています:

``has_option(opt_str)``
   :class:`OptionParser` に(``"-q"`` や ``"--verbose"`` のような) オプション ``opt_str``
   がある場合、真を返します。

``get_option(opt_str)``
   オプション文字列``opt_str``に対する:class:`Option` インスタンスを返します。 該当するオプションがなければ ``None``
   を返します。

``remove_option(opt_str)``
   :class:`OptionParser` に``opt_str`` に対応するオプションがある場合、
   そのオプションを削除します。該当するオプションに他のオプション文字列が指定されて いた場合、それらのオプション文字列は全て無効になります。
   ``opt_str`` がこの :class:`OptionParser` オブジェクトのどのオプション にも属さない場合、:exc:`ValueError`
   を送出します。


.. _optparse-conflicts-between-options:

オプション間の衝突
^^^^^^^^^

注意が足りないと、衝突するオプションを定義しやすくなります::

   parser.add_option("-n", "--dry-run", ...)
   [...]
   parser.add_option("-n", "--noisy", ...)

(とりわけ、:class:`OptionParser` から標準的なオプションを備えた自前のサブクラスを 定義してしまった場合にはよく起きます。)

ユーザがオプションを追加するたびに、:mod:`optparse` は既存のオプションとの衝突
がないかチェックします。何らかの衝突が見付かると、現在設定されている衝突処理メカニズム を呼び出します。衝突処理メカニズムはコンストラクタ中で呼び出せます::

   parser = OptionParser(..., conflict_handler=handler)

個別にも呼び出せます::

   parser.set_conflict_handler(handler)

衝突時の処理をおこなうハンドラ(handler)には、以下のものが利用できます:

   ``error`` (デフォルトの設定)
      オプション間の衝突をプログラム上のエラーとみなし、 :exc:`OptionConflictError` を送出します。

   ``resolve``
      オプション間の衝突をインテリジェントに解決します (下記参照)。


一例として、衝突をインテリジェントに解決する:class:`OptionParser` を定義し、衝突を起こすようなオプションを追加してみましょう::

   parser = OptionParser(conflict_handler="resolve")
   parser.add_option("-n", "--dry-run", ..., help="do no harm")
   parser.add_option("-n", "--noisy", ..., help="be noisy")

この時点で、:mod:`optparse` はすでに追加済のオプションが オプション文字列 ``"-n"`` を使っていることを検出します。
``conflict_handler`` が ``"resolve"`` なので、 :mod:`optparse`は既に追加済のオプションリストの方から
``"-n"`` を除去して問題を解決します。従って、``"-n"`` の除去 されたオプションは``"--dry-run"`` だけでしか有効にできなく
なります。ユーザがヘルプ文字列を要求した場合、問題解決の結果を反映した メッセージが出力されます::

   options:
     --dry-run     do no harm
     [...]
     -n, --noisy   be noisy

これまでに追加したオプション文字列を跡形もなく削り去り、ユーザがそのオプションを コマンドラインから起動する手段をなくせます。
この場合、:mod:`optparse` はオプションを完全に除去してしまうので、 こうしたオプションはヘルプテキストやその他のどこにも表示されなくなります。
例えば、現在の :class:`OptionParser` の場合、以下の操作::

   parser.add_option("--dry-run", ..., help="new dry-run option")

を行った時点で、最初の :option:`-n/--dry-run` オプションはもはやアクセスできなくなります。このため、:mod:`optparse` は
オプションを消去してしまい、ヘルプテキスト::

   options:
     [...]
     -n, --noisy   be noisy
     --dry-run     new dry-run option

だけが残ります。


.. _optparse-cleanup:

クリーンアップ
^^^^^^^

OptionParser インスタンスはいくつかの循環参照を抱えています。 このことは Python のガーベジコレクタにとって問題になるわけではありませんが、
使い終わった OptionParser に対して ``destroy()`` を呼び出すことで この循環参照を意図的に断ち切るという方法を選ぶこともできます。
この方法は特に長時間実行するアプリケーションで OptionParser から 大きなオブジェクトグラフが到達可能になっているような場合に有用です。


.. _optparse-other-methods:

その他のメソッド
^^^^^^^^

OptionParser にはその他にも幾つかの公開されたメソッドがあります:

*   ``set_usage(usage)``

  上で説明したコンストラクタの ``usage`` キーワード引数での規則に従った 使用法の文字列をセットします。``None``
  を渡すとデフォルトの使用法文字列が 使われるようになり、``SUPPRESS_USAGE`` によって使用法メッセージを 抑制できます。

*   ``enable_interspersed_args()``, ``disable_interspersed_args()``

  位置引数をオプションと混ぜこぜにする GNU getopt のような扱いを有効化/無効化する (デフォルトでは有効)。たとえば、``"-a"`` と
  ``"-b"`` はどちらも引数を 取らない単純なオプションだとすると、:mod:`optparse` は通常つぎのような文法を 受け入れます。  ::

     prog -a arg1 -b arg2

  そして扱いは次のように指定した時と同じです。  ::

     prog -a -b arg1 arg2

  この機能を無効化したい時は ``disable_interspersed_args()`` を 呼び出してください。この呼び出しにより、伝統的な Unix
  文法に回帰し、 オプションの解析は最初のオプションでない引数で止まるようになります。

*   ``set_defaults(dest=value, ...)``

  幾つかの保存先に対してデフォルト値をまとめてセットします。 :meth:`set_defaults` を使うのは複数のオプションにデフォルト値をセットする
  好ましいやり方です。というのも複数のオプションが同じ保存先を共有することがあり得るからです。 たとえば幾つかの "mode"
  オプションが全て同じ保存先をセットするものだったとすると、 どのオプションもデフォルトをセットすることができ、しかし最後に指定したものが勝ちます。  ::

     parser.add_option("--advanced", action="store_const",
                       dest="mode", const="advanced",
                       default="novice")    # 上書きされます
     parser.add_option("--novice", action="store_const",
                       dest="mode", const="novice",
                       default="advanced")  # 上の設定を上書きします

  こうした混乱を避けるために :meth:`set_defaults` を使います。  ::

     parser.set_defaults(mode="advanced")
     parser.add_option("--advanced", action="store_const",
                       dest="mode", const="advanced")
     parser.add_option("--novice", action="store_const",
                       dest="mode", const="novice")


.. _optparse-option-callbacks:

オプション処理コールバック
-------------

:mod:`optparse` の組み込みのアクションや型が望みにかなったものでない 場合、二つの選択肢があります: 一つは :mod:`optparse`
の拡張、もう一つは callback オプションの定義です。 :mod:`optparse` の拡張は汎用性に富んでいますが、単純なケースに対して
いささか大げさでもあります。大体は簡単なコールバックで事足りるでしょう。

``callback`` オプションの定義は二つのステップからなります:

*   ``callback`` アクションを使ってオプション自体を定義する。

*   コールバックを書く。コールバックは少なくとも後で説明する 4 つの引数を とる関数 (またはメソッド) でなければなりません。


.. _optparse-defining-callback-option:

callbackオプションの定義
^^^^^^^^^^^^^^^^

callbackオプションを最も簡単に定義するには、 ``parser.add_option()`` メソッドを使います。 :attr:`action`
の他に指定しなければならない属性は ``callback``、 すなわちコールバックする関数自体です::

   parser.add_option("-c", action="callback", callback=my_callback)

``callback`` は関数 (または呼び出し可能オブジェクト)なので、callback オプションを定義する時にはあらかじめ
``my_callback()`` を定義しておかねば なりません。この単純なケースでは、:mod:`optparse` は :option:`-c` が
何らかの引数をとるかどうか判別できず、通常は:option:`-c` が引数を 伴わないことを意味します --- 知りたいことはただ単に
:option:`-c` がコマンドライン上に 現れたどうかだけです。とはいえ、場合によっては、自分のコールバック関数に
任意の個数のコマンドライン引数を消費させたいこともあるでしょう。これがコールバック関数 をトリッキーなものにしています;
これについてはこの節の後の方で説明します。

:mod:`optparse` は常に四つの引数をコールバックに渡し、その他には ``callback_args`` および
``callback_kwargs`` で指定した 追加引数しか渡しません。従って、最小のコールバック関数シグネチャは::

   def my_callback(option, opt, value, parser):

のようになります。

コールバックの四つの引数については後で説明します。

callback オプションを定義する場合には、他にもいくつかオプション属性を 指定できます:

:attr:`type`
   他で使われているのと同じ意味です: ``store`` や ``append`` アクションの時と同じく、
   この属性は:mod:`optparse`に引数を一つ消費して、:attr:`type` に指定した 型に変換させます。:mod:`optparse`
   は変換後の値をどこかに保存する代わりに コールバック関数に渡します。

``nargs``
   これも他で使われているのと同じ意味です: このオプションが指定されていて、 かつ ``nargs`` > 1 である場合、 :mod:`optparse`
   は``nargs`` 個の引数を消費します。このとき各引数は :attr:`type`
   型に変換できねばなりません。変換後の値はタプルとしてコールバックに渡されます。

``callback_args``
   その他の固定引数からなるタプルで、コールバックに渡されます。

``callback_kwargs``
   その他のキーワード引数からなるタプルで、コールバックに渡されます。


.. _optparse-how-callbacks-called:

コールバック関数はどのように呼び出されるか
^^^^^^^^^^^^^^^^^^^^^

コールバックは全て以下の形式で呼び出されます::

   func(option, opt_str, value, parser, *args, **kwargs)

ここで、

``option``
   コールバックを呼び出している :class:`Option` のインスタンスです。

``opt_str``
   は、コールバック呼び出しのきっかけとなったコマンドライン上のオプション文字列です。 (長い形式のオプションに対する省略形が使われている場合、*opt*
   は完全な、 正式な形のオプション文字列となります ---  例えば、ユーザが :option:`--foobar` の短縮形として ``"--foo"``
   をコマンドラインに入力した時には、*opt_str*  は ``"--foobar"`` となります。)

``value``
   オプションの引数で、コマンドライン上に見つかったものです。 :mod:`optparse` は、``type`` が設定されている場合、
   単一の引数しかとりません;``value`` の型はオプションの型 として指定された型になります。このオプションに対する :attr:`type` が None
   である(引数なしの) 場合、*value* は None になります。 ``nargs`` > 1 であれば、``value`` は
   は適切な型をもつ値のタプルになります。

``parser``
   現在のオプション解析の全てを駆動している :class:`OptionParser`  インスタンスです。この変数が有用なのは、この値を介してインスタンス属性と
   していくつかの興味深いデータにアクセスできるからです:

   ``parser.largs``
      現在放置されている引数、すなわち、すでに消費されたものの、オプションでも オプション引数でもない引数からなるリストです。 ``parser.largs``
      は自由に変更でき、 たとえば引数を追加したりできます (このリストは ``args`` 、すなわち :meth:`parse_args`
      の二つ目の戻り値になります)

   ``parser.rargs``
      現在残っている引数、すなわち、 ``opt_str`` および ``value`` があれば除き、それ以外の引数が残っているリストです。
      ``parser.rargs`` は自由に変更でき、例えばさらに引数を消費したり できます。

   ``parser.values``
      オプションの値がデフォルトで保存されるオブジェクト (``optparse.OptionValues`` のインスタンス
      です。この値を使うと、コールバック関数がオプションの値を記憶するために、 他の:mod:`optparse`
      と同じ機構を使えるようにするため、グローバル変数や閉包 (closure) を台無しにしないので便利です。
      コマンドライン上にすでに現れているオプションの値にもアクセスできます。

``args``
   ``callback_args`` オプション属性で与えられた任意の固定引数 からなるタプルです。

``kwargs``
   ``callback_args`` オプション属性で与えられた任意のキーワード引数 からなるタプルです。


.. _optparse-raising-errors-in-callback:

コールバック中で例外を送出する
^^^^^^^^^^^^^^^

オプション自体か、あるいはその引数に問題があるばあい、コールバック関数は :exc:`OptionValueError`
を送出せねばなりません。:mod:`optparse` は この例外をとらえてプログラムを終了させ、ユーザが指定しておいたエラーメッセージを
標準エラー出力に出力します。エラーメッセージは明確、簡潔かつ正確で、どの オプションに誤りがあるかを示さねばなりません。さもなければ、ユーザは自分の
操作のどこに問題があるかを解決するのに苦労することになります。


.. _optparse-callback-example-1:

コールバックの例 1: ありふれたコールバック
^^^^^^^^^^^^^^^^^^^^^^^

引数をとらず、発見したオプションを単に記録するだけのコールバックオプションの例を 以下に示します::

   def record_foo_seen(option, opt_str, value, parser):
       parser.saw_foo = True

   parser.add_option("--foo", action="callback", callback=record_foo_seen)

もちろん、``store_true`` アクションを使っても実現できます。


.. _optparse-callback-example-2:

コールバックの例 2: オプションの順番をチェックする
^^^^^^^^^^^^^^^^^^^^^^^^^^^

もう少し面白みのある例を示します: この例では、``"-b"`` を発見して、その後で ``"-a"`` がコマンドライン中に現れた場合にはエラーになります。
::

   def check_order(option, opt_str, value, parser):
       if parser.values.b:
           raise OptionValueError("can't use -a after -b")
       parser.values.a = 1
   [...]
   parser.add_option("-a", action="callback", callback=check_order)
   parser.add_option("-b", action="store_true", dest="b")


.. _optparse-callback-example-3:

コールバックの例 3: オプションの順番をチェックする (汎用的)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

このコールバック (フラグを立てるが、``"-b"`` が既に指定されていればエラーになる)
を同様の複数のオプションに対して再利用したければ、もう少し作業する必要があります: エラーメッセージとセットされるフラグを一般化しなければなりません。  ::

   def check_order(option, opt_str, value, parser):
       if parser.values.b:
           raise OptionValueError("can't use %s after -b" % opt_str)
       setattr(parser.values, option.dest, 1)
   [...]
   parser.add_option("-a", action="callback", callback=check_order, dest='a')
   parser.add_option("-b", action="store_true", dest="b")
   parser.add_option("-c", action="callback", callback=check_order, dest='c')


.. _optparse-callback-example-4:

コールバックの例 4: 任意の条件をチェックする
^^^^^^^^^^^^^^^^^^^^^^^^

もちろん、単に定義済みのオプションの値を調べるだけにとどまらず、コールバックには 任意の条件を入れられます。例えば、満月でなければ呼び出してはならないオプション
があるとしましょう。やらなければならないことはこれだけです::

   def check_moon(option, opt_str, value, parser):
       if is_moon_full():
           raise OptionValueError("%s option invalid when moon is full"
                                  % opt_str)
       setattr(parser.values, option.dest, 1)
   [...]
   parser.add_option("--foo",
                     action="callback", callback=check_moon, dest="foo")

(``is_moon_full()`` の定義は読者への課題としましょう。


.. _optparse-callback-example-5:

コールバックの例5: 固定引数
^^^^^^^^^^^^^^^

決まった数の引数をとるようなコールパックオプションを定義するなら、問題はやや興味深く なってきます。引数をとるようコールバックに指定するのは、``store``
や ``append`` オプションの定義に似ています: :attr:`type` を定義していれば、
そのオプションは引数を受け取ったときに該当する型に変換できねばなりません; さらに ``nargs`` を指定すれば、オプションは ``nargs``
個の引数を 受け取ります。

標準の ``store`` アクションをエミュレートする例を以下に示します::

   def store_value(option, opt_str, value, parser):
       setattr(parser.values, option.dest, value)
   [...]
   parser.add_option("--foo",
                     action="callback", callback=store_value,
                     type="int", nargs=3, dest="foo")

:mod:`optparse` は 3 個の引数を受け取り、それらを整数に変換するところまで 面倒をみてくれます; ユーザは単にそれを保存するだけです。
(他の処理もできます; いうまでもなく、この例にはコールバックは必要ありません)


.. _optparse-callback-example-6:

コールバックの例6: 可変個の引数
^^^^^^^^^^^^^^^^^

あるオプションに可変個の引数を持たせたいと考えているなら、問題はいささか手強く なってきます。この場合、:mod:`optparse`
では該当する組み込みのオプション解析 機能を提供していないので、自分でコールバックを書かねばなりません。さらに、 :mod:`optparse`
が普段処理している、伝統的な Unix コマンドライン解析における 難題を自分で解決せねばなりません。とりわけ、コールバック関数では 引数が裸の``"--"``
や ``"-"`` の場合における慣習的な処理規則:

*   either ``"--"`` or ``"-"`` can be option arguments

*   裸の ``"--"`` (何らかのオプションの引数でない場合): コマンドライン処理を 停止し、``"--"``を無視します。

*   裸の``"-"`` (何らかのオプションの引数でない場合): コマンドライン処理を停止しますが、 ``"-"`` は残します
  (``parser.largs`` に追加します)。

を実装せねばなりません。

オプションが可変個の引数をとるようにさせたいなら、いくつかの 巧妙で厄介な問題に配慮しなければなりません。どういう実装を
とるかは、アプリケーションでどのようなトレードオフを考慮するか によります (このため、:mod:`optparse` では可変個の引数に
関する問題を直接的に取り扱わないのです)。

とはいえ、可変個の引数をもつオプションに対するスタブ (stub、仲介 インタフェース) を以下に示しておきます::

   def vararg_callback(option, opt_str, value, parser):
       assert value is None
       done = 0
       value = []
       rargs = parser.rargs
       while rargs:
           arg = rargs[0]

           # "--foo", "-a", "-fx", "--file=f" といった引数で停止。
           # "-3" や "-3.0" でも止まるので、オプションに数値が入る場合には
           # それを処理せねばならない。
           if ((arg[:2] == "--" and len(arg) > 2) or
               (arg[:1] == "-" and len(arg) > 1 and arg[1] != "-")):
               break
           else:
               value.append(arg)
               del rargs[0]

        setattr(parser.values, option.dest, value)

   [...]
   parser.add_option("-c", "--callback",
                     action="callback", callback=varargs)

この実装固有の弱点は、``"-c"`` 以後に続いて負の数を表す 引数があった場合、その引数は ``"-c"`` の引数ではなく次の
オプションとして解釈される(そしておそらくエラーを引き起こす) ということです。この問題の修正は読者の練習課題としておきます。


.. _optparse-extending-optparse:

:mod:`optparse` の拡張
-------------------

:mod:`optparse` がコマンドラインオプションをどのように解釈するかを決 める二つの重要な要素はそれぞれのオプションのアクションと型なので、拡張
の方向は新しいアクションと型を追加することになると思います。


.. _optparse-adding-new-types:

新しい型の追加
^^^^^^^

新しい型を追加するためには、:mod:`optparse` の Option クラスのサブクラスを 自身で定義する必要があります。このクラスには
:mod:`optparse` における型を定義する 一対の属性があります。それは :attr:`TYPES` と :attr:`TYPE_CHECKER`
です。

:attr:`TYPES` は型名のタプルです。新しく作るサブクラスでは、 タプル :attr:`TYPES`
は単純に標準的なもののを利用して定義すると良いでしょう。

:attr:`TYPE_CHECKER` は辞書で型名を型チェック関数に対応付けるものです。 型チェック関数は以下のような引数をとります。  ::

   def check_mytype(option, opt, value)

ここで ``option`` は :class:`Option` のインスタンスであ り、``opt`` はオプション文字列(たとえ ば
``"-f"``)で、``value`` は望みの型としてチェックされ変換される べくコマンドラインで与えられる文字列です。``check_mytype()``
は想 定されている型 ``mytype`` のオブジェクトを返さなければなりません。型 チェック関数から返される値は
:meth:`OptionParser.parse_args` で返 されるOptionValues インスタンスに収められるか、またはコールバック に
``value`` パラメータとして渡されます。

型チェック関数は何か問題に遭遇したら OptionValueError を送出しなければなりません。 OptionValueError
は文字列一つを引数に取り、それはそのまま OptionParser の :meth:`error` メソッドに渡され、そこでプログラム名と文字列
``"error:"`` が前置されてプロセスが終了する前に stderr に出力されます。

馬鹿馬鹿しい例ですが、Python スタイルの複素数を解析する ``complex`` オプション型
を作ってみせることにします。(:mod:`optparse` 1.3 が複素数のサポートを
組み込んでしまったため以前にも増して馬鹿らしくなりましたが、気にしないでください。)

最初に必要な import 文を書きます。  ::

   from copy import copy
   from optparse import Option, OptionValueError

まずは型チェック関数を定義しなければなりません。 これは後で(これから定義する Option のサブクラスの :attr:`TYPE_CHECKER`
クラス属性 の中で)参照されることになります。  ::

   def check_complex(option, opt, value):
       try:
           return complex(value)
       except ValueError:
           raise OptionValueError(
               "option %s: invalid complex value: %r" % (opt, value))

最後に Option のサブクラスです。  ::

   class MyOption (Option):
       TYPES = Option.TYPES + ("complex",)
       TYPE_CHECKER = copy(Option.TYPE_CHECKER)
       TYPE_CHECKER["complex"] = check_complex

(もしここで :attr:`Option.TYPE_CHECKER` に :func:`copy` を適用しなければ、 :mod:`optparse` の
Option クラスの :attr:`TYPE_CHECKER` 属性をいじってしまう ことになります。Python
の常として、良いマナーと常識以外にそうすることを止めるものは ありません。)

これだけです! もう新しいオプション型を使うスクリプトを他の :mod:`optparse` に基づいた
スクリプトとまるで同じように書くことができます。ただし、 OptionParser に Option でなく MyOption
を使うように指示しなければなければなりません。  ::

   parser = OptionParser(option_class=MyOption)
   parser.add_option("-c", type="complex")

別のやり方として、オプションリストを構築して OptionParser に渡すという方法もあります。 :meth:`add_option`
を上でやったように使わないならば、OptionParser に どのクラスを使うのか教える必要はありません。  ::

   option_list = [MyOption("-c", action="store", type="complex", dest="c")]
   parser = OptionParser(option_list=option_list)


.. _optparse-adding-new-actions:

新しいアクションの追加
^^^^^^^^^^^

新しいアクションの追加はもう少しトリッキーです。というのも :mod:`optparse`  が使っている二つのアクションの分類を理解する必要があるからです。

"store" アクション
   :mod:`optparse` が値を現在の OptionValues の属性に格納することになるアクションです。 この種類のオプションは Option
   のコンストラクタに :attr:`dest` 属性を与えることが 要求されます。

"typed" アクション
   コマンドラインから引数を受け取り、それがある型であることが期待されているアクションです。 もう少しはっきり言えば、その型に変換される文字列を受け取るものです。
   この種類のオプションは Option のコンストラクタに :attr:`type` 属性を与えることが 要求されます。

この分類には重複する部分があります。デフォルトの "store" アクションには
``store``、``store_const``、``append``、``count`` などがありますが、 デフォルトの "typed" オプションは
``store``、``append``、``callback`` の三つです。

アクションを追加する際に、以下の Option のクラス属性(全て文字列のリストです)
の中の少なくとも一つに付け加えることでそのアクションを分類する必要があります。

:attr:`ACTIONS`
   全てのアクションは ACTIONS にリストされていなければなりません

:attr:`STORE_ACTIONS`
   "store" アクションはここにもリストされます

:attr:`TYPED_ACTIONS`
   "typed" アクションはここにもリストされます

``ALWAYS_TYPED_ACTIONS``
   型を取るアクション (つまりそのオプションが値を取る) はここにもリストされます。 このことの唯一の効果は :mod:`optparse`
   が、型の指定が無くアクション が ``ALWAYS_TYPED_ACTIONS`` のリストにあるオプションに、 デフォルト型 ``string``
   を割り当てるということだけです。

実際に新しいアクションを実装するには、Option の :meth:`take_action`
メソッドをオーバライドしてそのアクションを認識する場合分けを追加しなければなりません。

例えば、``extend`` アクションというのを追加してみましょう。このアクションは 標準的な ``append``
アクションと似ていますが、コマンドラインから一つだけ値を 読み取って既存のリストに追加するのではなく、複数の値をコンマ区切りの文字列として
読み取ってそれらで既存のリストを拡張します。すなわち、もし ``"--names"`` が ``string`` 型の ``extend``
オプションだとすると、次のコマンドライン  ::

   --names=foo,bar --names blah --names ding,dong

の結果は次のリストになります。  ::

   ["foo", "bar", "blah", "ding", "dong"]

再び Option のサブクラスを定義します。  ::

   class MyOption (Option):

       ACTIONS = Option.ACTIONS + ("extend",)
       STORE_ACTIONS = Option.STORE_ACTIONS + ("extend",)
       TYPED_ACTIONS = Option.TYPED_ACTIONS + ("extend",)
       ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("extend",)

       def take_action(self, action, dest, opt, value, values, parser):
           if action == "extend":
               lvalue = value.split(",")
               values.ensure_value(dest, []).extend(lvalue)
           else:
               Option.take_action(
                   self, action, dest, opt, value, values, parser)

注意すべきは次のようなところです。

*   ``extend`` はコマンドラインの値を予期していると同時にその値をどこかに格納します ので、:attr:`STORE_ACTIONS` と
  :attr:`TYPED_ACTIONS` の両方に入ります。

*   :mod:`optparse` が ``extend`` アクションに ``string`` 型を割り当てるように ``extend`` アクションは
  ``ALWAYS_TYPED_ACTIONS`` にも入れてあります。

*   :meth:`MyOption.take_action` にはこの新しいアクション一つの扱いだけを 実装してあり、他の標準的な
  :mod:`optparse` のアクションについては :meth:`Option.take_action` に制御を戻すようにしてあります。

*   ``values`` は optparse_parser.Values クラスのインスタンスであり、 非常に有用な
  :meth:`ensure_value` メソッドを提供しています。 :meth:`ensure_value` は本質的に安全弁付きの
  :func:`getattr` です。 次のように呼び出します。  ::

     values.ensure_value(attr, value)

  ``values`` に ``attr`` 属性が無いか None だった場合に、 :meth:`ensure_value` は最初に ``value``
  をセットし、 それから ``value`` を返します。 この振る舞いは ``extend``、``append``、``count``
  のように、データを変数に 集積し、またその変数がある型 (最初の二つはリスト、最後のは整数) であると期待されるアクション
  を作るのにとても使い易いものです。:meth:`ensure_value` を使えば、
  作ったアクションを使うスクリプトはオプションに保存先にデフォルト値をセットすることに 煩わされずに済みます。デフォルトを None にしておけば
  :meth:`ensure_value` が それが必要になったときに適当な値を返してくれます。

