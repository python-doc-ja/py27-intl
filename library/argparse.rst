.. :mod:`argparse` --- Parser for command-line options, arguments and sub-commands

:mod:`argparse` --- コマンドラインオプション、引数、サブコマンドのパーサー
===============================================================================

.. module:: argparse
   :synopsis: コマンドラインオプションと引数のパーサーライブラリ
.. moduleauthor:: Steven Bethard <steven.bethard@gmail.com>
.. versionadded:: 2.7
.. sectionauthor:: Steven Bethard <steven.bethard@gmail.com>


:mod:`argparse` モジュールはユーザーフレンドリーなコマンドラインインタフェースの
作成を簡単にします。
プログラムがどんな引数を必要としているのかを定義すると、 :mod:`argparse` が
:data:`sys.argv` からそのオプションをパースする部分の面倒を見ます。
:mod:`argparse` モジュールは自動的にヘルプと使用方法メッセージを生成し、
ユーザーが不正な引数をプログラムに指定したときにエラーを発生させます。


.. Example

例
-------

次のコードは、整数のリストを受け取って合計か最大値を返す Python プログラムです::

   import argparse

   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument('integers', metavar='N', type=int, nargs='+',
                      help='an integer for the accumulator')
   parser.add_argument('--sum', dest='accumulate', action='store_const',
                      const=sum, default=max,
                      help='sum the integers (default: find the max)')

   args = parser.parse_args()
   print args.accumulate(args.integers)

上の Python コードが ``prog.py`` という名前のファイルに保存されたと仮定します。
コマンドラインから実行して、便利なヘルプメッセージを提供することができます。 ::

   $ prog.py -h
   usage: prog.py [-h] [--sum] N [N ...]

   Process some integers.

   positional arguments:
    N           an integer for the accumulator

   optional arguments:
    -h, --help  show this help message and exit
    --sum       sum the integers (default: find the max)

妥当な引数を与えて実行された場合、このプログラムはコマンドライン引数の整数列の
合計か最大値を表示します::

   $ prog.py 1 2 3 4
   4

   $ prog.py 1 2 3 4 --sum
   10

不正な引数が与えられた場合、エラーを発生させます::

   $ prog.py a b c
   usage: prog.py [-h] [--sum] N [N ...]
   prog.py: error: argument N: invalid int value: 'a'

以降のセクションでは、この例をひと通り解説して行きます。


.. Creating a parser

パーサーを作る
^^^^^^^^^^^^^^^^^

:mod:`argparse` を使う最初のステップは、 :class:`ArgumentParser`
オブジェクトを生成することです::

   >>> parser = argparse.ArgumentParser(description='Process some integers.')

:class:`ArgumentParser` オブジェクトはコマンドラインを解析して Python データ型にする
ために必要な全ての情報を保持します。


.. Adding arguments

引数を追加する
^^^^^^^^^^^^^^^^

:class:`ArgumentParser` にプログラム引数の情報を与えるために、
:meth:`~ArgumentParser.add_argument` メソッドを呼び出します。
一般的に、このメソッドの呼び出しは :class:`ArgumentParser` に、コマンドラインの
文字列を受け取ってそれをオブジェクトにする方法を教えます。
この情報は保存され、 :meth:`~ArgumentParser.parse_args` が呼び出されたときに
利用されます。例えば::

   >>> parser.add_argument('integers', metavar='N', type=int, nargs='+',
   ...                     help='an integer for the accumulator')
   >>> parser.add_argument('--sum', dest='accumulate', action='store_const',
   ...                     const=sum, default=max,
   ...                     help='sum the integers (default: find the max)')

あとで、 :meth:`~ArgumentParser.parse_args` を呼び出すと、 ``integers`` と
``accumulate`` という2つの属性を持ったオブジェクトを返します。
``integers`` 属性は1つ以上の整数のリストで、 ``accumulate`` 属性はコマンドラインから
``--sum`` が指定された場合は :func:`sum` 関数、それ以外の場合は :func:`max` 関数に
なります。


.. Parsing arguments

引数をパースする
^^^^^^^^^^^^^^^^^

:class:`ArgumentParser` は引数を :meth:`~ArgumentParser.parse_args`
メソッドでパースします。
このメソッドはコマンドラインを調べ、各引数を正しい型に変換して、適切なアクションを
実行します。ほとんどの場合、これはシンプルな namespace オブジェクトを
コマンドラインの解析結果から構築することを意味します::

   >>> parser.parse_args(['--sum', '7', '-1', '42'])
   Namespace(accumulate=<built-in function sum>, integers=[7, -1, 42])

スクリプトでは、 :meth:`~ArgumentParser.parse_args` は典型的には引数なしで
呼び出され、 :class:`ArgumentParser` は自動的に :data:`sys.argv` から
コマンドライン引数を取得します。


.. ArgumentParser objects

ArgumentParser オブジェクト
----------------------------

.. class:: ArgumentParser([description], [epilog], [prog], [usage], [add_help], [argument_default], [parents], [prefix_chars], [conflict_handler], [formatter_class])

   新しい :class:`ArgumentParser` オブジェクトを生成します。
   各引数についてはあとで詳しく説明しますが、簡単に言うと:

   * description_ - 引数のヘルプの前に表示されるテキスト

   * epilog_ - 引数のヘルプの後で表示されるテキスト

   * add_help_ - -h/--help オプションをパーサーに追加する (デフォルト: ``True``)

   * argument_default_ - 引数にグローバルのデフォルト値を設定する
     (デフォルト: ``None``)

   * parents_ - :class:`ArgumentParser` オブジェクトのリストで、このオブジェクトの
     引数が追加される

   * prefix_chars_ - オプションの引数の prefix になる文字集合
     (デフォルト: '-')

   * fromfile_prefix_chars_ - 追加の引数を読み込むファイルの prefix になる文字集合
     (デフォルト: ``None``)

   * formatter_class_ - ヘルプ出力をカスタマイズするためのクラス

   * conflict_handler_ - 衝突するオプションを解決する方法を定義する。
     通常は利用する必要はありません。

   * prog_ - プログラム名 (デフォルト: :data:`sys.argv[0]`)

   * usage_ - プログラムの利用方法を解説する文字列 (デフォルト: 生成される)

以下のセクションでは各オプションの利用方法を解説します。


description
^^^^^^^^^^^

多くの場合、 :class:`ArgumentParser` のコンストラクタを呼び出すときに
``description=`` キーワード引数が利用されます。
この引数はプログラムが何をしてどう動くのかについての短い説明です。
ヘルプメッセージで、この description はコマンドラインの利用法と引数の
ヘルプメッセージの間に表示されます::

   >>> parser = argparse.ArgumentParser(description='A foo that bars')
   >>> parser.print_help()
   usage: argparse.py [-h]

   A foo that bars

   optional arguments:
    -h, --help  show this help message and exit

デフォルトでは、 description は行ラップされるので、与えられたスペースに
マッチします。この挙動を変更するには、 formatter_class_ 引数を参照してください。


epilog
^^^^^^

いくつかのプログラムは、プログラムについての追加の説明を引数の解説の
後に表示します。このテキストは :class:`ArgumentParser` の ``epilog=`` 引数に
指定することができます::

   >>> parser = argparse.ArgumentParser(
   ...     description='A foo that bars',
   ...     epilog="And that's how you'd foo a bar")
   >>> parser.print_help()
   usage: argparse.py [-h]

   A foo that bars

   optional arguments:
    -h, --help  show this help message and exit

   And that's how you'd foo a bar

description_ 引数と同じく、 ``epilog=`` テキストもデフォルトで行ラップされ、
:class:`ArgumentParser` の formatter_class_ 引数で動作を調整することができます。


add_help
^^^^^^^^

デフォルトでは、 ArgumentParser オブジェクトはシンプルにパーサーの
ヘルプメッセージを表示するオプションを自動的に追加します。
例えば、以下のコードを含む ``myprogram.py`` ファイルについて
考えてください::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument('--foo', help='foo help')
   args = parser.parse_args()

コマンドラインに ``-h`` か ``--help`` が指定された場合、 ArgumentParser の
help が表示されます::

   $ python myprogram.py --help
   usage: myprogram.py [-h] [--foo FOO]

   optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   foo help

必要に応じて、この help オプションを無効にする場合があります。
これは :class:`ArgumentParser` の ``add_help=`` 引数に ``False``
を渡すことで可能です::

   >>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
   >>> parser.add_argument('--foo', help='foo help')
   >>> parser.print_help()
   usage: PROG [--foo FOO]

   optional arguments:
    --foo FOO  foo help

ヘルプオプションは通常 ``-h/--help`` です。例外は ``prefix_chars=``
が指定されてその中に ``'-'`` が無かった場合で、その場合は ``-h`` と
``--help`` は有効なオプションではありません。
この場合、 ``prefix_chars`` の最初の文字がヘルプオプションの prefix
として利用されます::

   >>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='+/')
   >>> parser.print_help()
   usage: PROG [+h]

   optional arguments:
     +h, ++help  show this help message and exit


prefix_chars
^^^^^^^^^^^^

ほとんどのコマンドラインオプションは、 ``-f/--foo`` のように prefix に ``'-'``
を使います。
``+f`` や ``/foo`` のような、他の、あるいは追加の prefix 文字をサポートしなければ
ならない場合、 ArgumentParser のコンストラクタの ``prefix_chars=`` 引数を指定します::

   >>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='-+')
   >>> parser.add_argument('+f')
   >>> parser.add_argument('++bar')
   >>> parser.parse_args('+f X ++bar Y'.split())
   Namespace(bar='Y', f='X')

``prefix_chars=`` 引数のデフォルトは ``'-'`` です。
``'-'`` を含まない文字集合を指定すると、 ``-f/--foo`` オプションが許可されなくなります。


fromfile_prefix_chars
^^^^^^^^^^^^^^^^^^^^^

ときどき、例えば非常に長い引数リストを扱う場合に、その引数リストを毎回コマンドラインに
タイプする代わりにファイルに置いておきたい場合があります。
:class:`ArgumentParser` のコンストラクタに ``fromfile_prefix_chars=`` 引数が指定された
場合、指定された文字のいずれかで始まる引数はファイルとして扱われ、そのファイルに
含まれる引数リストに置換されます。例えば::

   >>> with open('args.txt', 'w') as fp:
   ...    fp.write('-f\nbar')
   >>> parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
   >>> parser.add_argument('-f')
   >>> parser.parse_args(['-f', 'foo', '@args.txt'])
   Namespace(f='bar')

ファイルから読み込まれる引数は、デフォルトでは1行に1つ(ただし、
:meth:`~ArgumentParser.convert_arg_line_to_args` も参照してください)で、
コマンドライン上でファイルを参照する引数があった場所にその引数があったものとして
扱われます。なので、上の例では、 ``['-f', 'foo', '@args.txt']`` は
``['-f', 'foo', '-f', 'bar']`` と等価になります。

``fromfile_prefix_chars=`` 引数のデフォルト値は ``None`` で、
引数がファイル参照だとして扱われることが無いことを意味しています。


argument_default
^^^^^^^^^^^^^^^^

一般的には、引数のデフォルト値は :meth:`~ArgumentParser.add_argument` メソッドに
デフォルト値を渡すか、 :meth:`~ArgumentParser.set_defaults` メソッドに
name-value ペアを渡すことで指定します。
しかしまれに、1つのパーサー全体に適用されるデフォルト引数が便利なことがあります。
これをするには、 :class:`ArgumentParser` に ``argument_default=`` キーワード
引数を渡します。例えば、全体で :meth:`~ArgumentParser.parse_args` メソッド呼び出しの
属性の生成を抑制するには、 ``argument_default=SUPPRESS`` を指定します::

   >>> parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
   >>> parser.add_argument('--foo')
   >>> parser.add_argument('bar', nargs='?')
   >>> parser.parse_args(['--foo', '1', 'BAR'])
   Namespace(bar='BAR', foo='1')
   >>> parser.parse_args([])
   Namespace()


parents
^^^^^^^

ときどき、いくつかのパーサーが共通の引数セットを共有することがあります。
それらの引数を繰り返し定義する代わりに、全ての共通引数を持った parser を
:class:`ArgumentParser` の ``parents=`` 引数に渡すことができます。
``parents=`` 引数は :class:`ArgumentParser` オブジェクトのリストを受け取り、
全ての位置アクションとオプションのアクションをそれらから集め、
そのアクションを構築中の :class:`ArgumentParser` オブジェクトに追加します::

   >>> parent_parser = argparse.ArgumentParser(add_help=False)
   >>> parent_parser.add_argument('--parent', type=int)

   >>> foo_parser = argparse.ArgumentParser(parents=[parent_parser])
   >>> foo_parser.add_argument('foo')
   >>> foo_parser.parse_args(['--parent', '2', 'XXX'])
   Namespace(foo='XXX', parent=2)

   >>> bar_parser = argparse.ArgumentParser(parents=[parent_parser])
   >>> bar_parser.add_argument('--bar')
   >>> bar_parser.parse_args(['--bar', 'YYY'])
   Namespace(bar='YYY', parent=None)

一番親になるパーサーに ``add_help=False`` を指定していることに注目してください。
こうしないと、 :class:`ArgumentParser` は2つの ``-h/--help`` オプションを
与えられる (1つは親から、もうひとつは子から) ことになり、エラーを発生させます。

.. note::
   ``parents=`` に渡す前にパーサーを完全に初期化する必要があります。
   子パーサーを作成してから親パーサーを変更した場合、その変更は子パーサーに
   反映されません。


formatter_class
^^^^^^^^^^^^^^^

:class:`ArgumentParser` オブジェクトは代わりのフォーマットクラスを指定することで
ヘルプのフォーマットをカスタマイズすることができます。
現在、3つのフォーマットクラスがあります:

.. class:: RawDescriptionHelpFormatter
           RawTextHelpFormatter
           ArgumentDefaultsHelpFormatter

最初の2つは説明のテキストがどう表示されるかについてより制御できるようになっており、
残りの1つは引数のデフォルト値についての情報を自動的に追加します。

デフォルトでは、 :class:`ArgumentParser` オブジェクトはコマンドラインのヘルプ
メッセージ中でdescription_ と epilog_ を行ラップします::

   >>> parser = argparse.ArgumentParser(
   ...     prog='PROG',
   ...     description='''this description
   ...         was indented weird
   ...             but that is okay''',
   ...     epilog='''
   ...             likewise for this epilog whose whitespace will
   ...         be cleaned up and whose words will be wrapped
   ...         across a couple lines''')
   >>> parser.print_help()
   usage: PROG [-h]

   this description was indented weird but that is okay

   optional arguments:
    -h, --help  show this help message and exit

   likewise for this epilog whose whitespace will be cleaned up and whose words
   will be wrapped across a couple lines

``formatter_class=`` に :class:`~argparse.RawDescriptionHelpFormatter` を渡すと、
description_ と epilog_ がすでに正しくフォーマット済みで、行ラップしてはいけない
ことを指定できます::

   >>> parser = argparse.ArgumentParser(
   ...     prog='PROG',
   ...     formatter_class=argparse.RawDescriptionHelpFormatter,
   ...     description=textwrap.dedent('''\
   ...         Please do not mess up this text!
   ...         --------------------------------
   ...             I have indented it
   ...             exactly the way
   ...             I want it
   ...         '''))
   >>> parser.print_help()
   usage: PROG [-h]

   Please do not mess up this text!
   --------------------------------
      I have indented it
      exactly the way
      I want it

   optional arguments:
    -h, --help  show this help message and exit

:class:`RawTextHelpFormatter` は引数の説明を含めて全ての種類のヘルプテキストで
空白を維持します。

残りの利用できるフォーマットクラスである :class:`ArgumentDefaultsHelpFormatter`
は、各引数のデフォルト値に関する情報を追加します::

   >>> parser = argparse.ArgumentParser(
   ...     prog='PROG',
   ...     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   >>> parser.add_argument('--foo', type=int, default=42, help='FOO!')
   >>> parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
   >>> parser.print_help()
   usage: PROG [-h] [--foo FOO] [bar [bar ...]]

   positional arguments:
    bar         BAR! (default: [1, 2, 3])

   optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   FOO! (default: 42)


conflict_handler
^^^^^^^^^^^^^^^^

:class:`ArgumentParser` オブジェクトは同じオプション文字列に対して複数のアクションを
許可していません。デフォルトでは、 :class:`ArgumentParser` オブジェクトは、
すでに利用されているオプション文字列を使って新しい引数をつくろうとしたときに
例外を発生させます::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-f', '--foo', help='old foo help')
   >>> parser.add_argument('--foo', help='new foo help')
   Traceback (most recent call last):
    ..
   ArgumentError: argument --foo: conflicting option string(s): --foo

ときどき (例えば、 parents_ を利用する場合など), 古い引数を同じオプション文字列で
上書きするほうが便利な場合があります。この動作をするには、 :class:`ArgumentParser`
の ``conflict_handler=`` 引数に ``'resolve'`` を渡します::

   >>> parser = argparse.ArgumentParser(prog='PROG', conflict_handler='resolve')
   >>> parser.add_argument('-f', '--foo', help='old foo help')
   >>> parser.add_argument('--foo', help='new foo help')
   >>> parser.print_help()
   usage: PROG [-h] [-f FOO] [--foo FOO]

   optional arguments:
    -h, --help  show this help message and exit
    -f FOO      old foo help
    --foo FOO   new foo help

:class:`ArgumentParser` オブジェクトは、全てのオプション文字列がオーバーライド
サれた場合にだけアクションを削除することに注目してください。上の例では、
``--foo`` オプション文字列だけがオーバーライドされているので、
古い ``-f/--foo`` アクションは ``-f`` アクションとして残っています。


prog
^^^^

デフォルトでは、 :class:`ArgumentParser` オブジェクトはヘルプメッセージ中に表示する
プログラム名を ``sys.argv[0]`` から取得します。このデフォルトの動作は、プログラムが
コマンドライン上でどう起動されたにヘルプメッセージをマッチさせるので、か多くの場合に
正しい挙動です。例えば、 ``myprogram.py`` という名前のファイルに次のコードがあるとします::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument('--foo', help='foo help')
   args = parser.parse_args()

このプログラムのヘルプは、プログラム名として (プログラムがどこから起動されたのかに
関わらず) ``myprogram.py`` を表示します::

   $ python myprogram.py --help
   usage: myprogram.py [-h] [--foo FOO]

   optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   foo help
   $ cd ..
   $ python subdir\myprogram.py --help
   usage: myprogram.py [-h] [--foo FOO]

   optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   foo help

このデフォルトの動作を変更するには、 :class:`ArgumentParser` の ``prog=``
引数に他の値を指定します::

   >>> parser = argparse.ArgumentParser(prog='myprogram')
   >>> parser.print_help()
   usage: myprogram [-h]

   optional arguments:
    -h, --help  show this help message and exit

プログラム名は、 ``sys.argv[0]`` から取られた場合でも ``prog=`` 引数で与えられた場合でも、
ヘルプメッセージ中では ``%(prog)s`` フォーマット指定で利用することができます。

::

   >>> parser = argparse.ArgumentParser(prog='myprogram')
   >>> parser.add_argument('--foo', help='foo of the %(prog)s program')
   >>> parser.print_help()
   usage: myprogram [-h] [--foo FOO]

   optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   foo of the myprogram program


usage
^^^^^

デフォルトでは、 :class:`ArgumentParser` は使用法メッセージを、もっている
引数から生成します::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('--foo', nargs='?', help='foo help')
   >>> parser.add_argument('bar', nargs='+', help='bar help')
   >>> parser.print_help()
   usage: PROG [-h] [--foo [FOO]] bar [bar ...]

   positional arguments:
    bar          bar help

   optional arguments:
    -h, --help   show this help message and exit
    --foo [FOO]  foo help

デフォルトのメッセージは ``usage=`` キーワード引数でオーバーライドできます::

   >>> parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')
   >>> parser.add_argument('--foo', nargs='?', help='foo help')
   >>> parser.add_argument('bar', nargs='+', help='bar help')
   >>> parser.print_help()
   usage: PROG [options]

   positional arguments:
    bar          bar help

   optional arguments:
    -h, --help   show this help message and exit
    --foo [FOO]  foo help

``%(prog)s`` フォーマット指定子を、使用法メッセージ中でプログラム名として利用できます。


.. The add_argument() method

add_argument() メソッド
-------------------------

.. method:: ArgumentParser.add_argument(name or flags..., [action], [nargs], [const], [default], [type], [choices], [required], [help], [metavar], [dest])

   1つのコマンドライン引数がどう解析されるかを定義します。
   各引数についての解説は以下で行いますが、簡潔には:

   * `name or flags`_ - 名前か、オプション文字列のリスト (例: ``foo`` か
     ``-f, --foo``)

   * action_ - コマンドラインにこの引数があった時のアクション

   * nargs_ - 消費するべきコマンドライン引数の数

   * const_ - いくつかの action_ と nargs_ の組み合わせで利用される定数

   * default_ - コマンドラインに引数がなかった場合に生成される値

   * type_ - コマンドライン引数が変換されるべき型

   * choices_ - 引数として許される値のコンテナ

   * required_ - Whether or not the command-line option may be omitted
     (optionals only).

   * help_ - A brief description of what the argument does.

   * metavar_ - A name for the argument in usage messages.

   * dest_ - The name of the attribute to be added to the object returned by
     :meth:`parse_args`.

The following sections describe how each of these are used.


name or flags
^^^^^^^^^^^^^

:meth:`~ArgumentParser.add_argument` メソッドは、指定されているのが
``-f`` や ``--foo`` のようなオプション引数なのか、ファイル名リストなどの
位置引数なのかを知る必要があります。そのため、 :meth:`~ArgumentParser.add_argument`
の第1引数は、フラグのリストか、シンプルな引数名のどちらかになります。
例えば、オプション引数は次のようにして作ります::

   >>> parser.add_argument('-f', '--foo')

一方、位置引数は次のようにして作ります::

   >>> parser.add_argument('bar')

:meth:`~ArgumentParser.parse_args` が呼ばれた時、オプション引数は ``-`` prefix
により識別され、それ以外の引数は位置引数として扱われます::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-f', '--foo')
   >>> parser.add_argument('bar')
   >>> parser.parse_args(['BAR'])
   Namespace(bar='BAR', foo=None)
   >>> parser.parse_args(['BAR', '--foo', 'FOO'])
   Namespace(bar='BAR', foo='FOO')
   >>> parser.parse_args(['--foo', 'FOO'])
   usage: PROG [-h] [-f FOO] bar
   PROG: error: too few arguments


action
^^^^^^

:class:`ArgumentParser` オブジェクトはコマンドライン引数にアクションを割り当てます。
このアクションは、割り当てられたコマンドライン引数に関してどんな処理でもできますが、
ほとんどのアクションは単に :meth:`~ArgumentParser.parse_args` が返すオブジェクトに
属性を追加するだけです。 ``action`` キーワード引数は、コマンドライン引数がどう
処理されるかを指定します。サポートされているアクションは:

* ``'store'`` - これは単に引数の値を格納します。これはデフォルトのアクションです。
  例えば:

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo')
    >>> parser.parse_args('--foo 1'.split())
    Namespace(foo='1')

* ``'store_const'`` - このアクションは const_ キーワード引数で指定された値を
  格納します。 (const_ キーワード引数のデフォルト値はあまり役に立たない ``None``
  であることに注意) ``'store_const'`` アクションは、何かの種類のフラグを
  指定するオプション引数によく使われます。例えば::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action='store_const', const=42)
    >>> parser.parse_args('--foo'.split())
    Namespace(foo=42)

* ``'store_true'``, ``'store_false'`` - これらのアクションはそれぞれ ``True``
  と ``False`` を格納します。これらは ``'store_const'`` の特別版になります。
  例えば::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action='store_true')
    >>> parser.add_argument('--bar', action='store_false')
    >>> parser.parse_args('--foo --bar'.split())
    Namespace(bar=False, foo=True)

* ``'append'`` - このアクションはリストを格納して、各引数の値をそのリストに
  追加します。このアクションは複数回指定することができるオプションに便利です。
  利用例::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action='append')
    >>> parser.parse_args('--foo 1 --foo 2'.split())
    Namespace(foo=['1', '2'])

* ``'append_const'`` - このアクションはリストを格納して、 const_ キーワード引数に
  与えられた値をそのリストに追加します。(const_ キーワード引数のデフォルト値は
  あまり役に立たない ``None`` であることに注意) ``'append_const'`` アクションは、
  定数を同じリストに複数回格納する場合に便利です。例えば::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--str', dest='types', action='append_const', const=str)
    >>> parser.add_argument('--int', dest='types', action='append_const', const=int)
    >>> parser.parse_args('--str --int'.split())
    Namespace(types=[<type 'str'>, <type 'int'>])

* ``'version'`` - このアクションは :meth:`~ArgumentParser.add_argument` の呼び出しに
  ``version=`` キーワード引数を期待します。指定されたときはバージョン情報を表示して
  終了します。 ::

    >>> import argparse
    >>> parser = argparse.ArgumentParser(prog='PROG')
    >>> parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    >>> parser.parse_args(['--version'])
    PROG 2.0

Action API を実装したオブジェクトを渡すことで、任意のアクションを指定することもできます。
独自のアクションを作る一番手軽な方法は :class:`argparse.Action` を継承して、
適切な ``__call__`` メソッドを実装することです。 ``__call__`` メソッドは
4つの引数を受け取らなければなりません:

* ``parser`` - このアクションを持っている ArgumentParser オブジェクト

* ``namespace`` - :meth:`~ArgumentParser.parse_args` が返す namespace オブジェクト。
  ほとんどのアクションはこのオブジェクトに属性を追加します。

* ``values`` - 型変換が適用された後の、関連付けられたコマンドライン引数。
  (型変換は :meth:`~ArgumentParser.add_argument` メソッドの type_ キーワード引数で
  指定されます)

* ``option_string`` - このアクションを実行したオプション文字列。 ``option_string``
  引数はオプションで、アクションが位置引数に関連付けられた場合は渡されません。

カスタムアクションの例です::

   >>> class FooAction(argparse.Action):
   ...     def __call__(self, parser, namespace, values, option_string=None):
   ...         print '%r %r %r' % (namespace, values, option_string)
   ...         setattr(namespace, self.dest, values)
   ...
   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', action=FooAction)
   >>> parser.add_argument('bar', action=FooAction)
   >>> args = parser.parse_args('1 --foo 2'.split())
   Namespace(bar=None, foo=None) '1' None
   Namespace(bar='1', foo=None) '2' '--foo'
   >>> args
   Namespace(bar='1', foo='2')


nargs
^^^^^

ArgumentParser オブジェクトは通常1つのコマンドライン引数を1つのアクションに渡します。
``nargs`` キーワード引数は1つのアクションにそれ以外の数のコマンドライン引数を
割り当てます。指定できる値は:

* N (整数).  N 個の引数がコマンドラインから集められ、リストに格納されます。
  例えば::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', nargs=2)
     >>> parser.add_argument('bar', nargs=1)
     >>> parser.parse_args('c --foo a b'.split())
     Namespace(bar=['c'], foo=['a', 'b'])

  ``nargs=1`` は1要素のリストを作ることに注意してください。これはデフォルトの、
  要素がそのまま属性になる動作とは異なります。

* ``'?'``. 可能なら1つの引数がコマンドラインから取られ、1つのアイテムを作ります。
  コマンドライン引数が存在しない場合、 default_ の値が生成されます。
  オプション引数の場合、さらにオプション引数がしていされ、その後にコマンドライン
  引数が無いというケースもありえます。この場合は const_ の値が生成されます。
  この動作の例です::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', nargs='?', const='c', default='d')
     >>> parser.add_argument('bar', nargs='?', default='d')
     >>> parser.parse_args('XX --foo YY'.split())
     Namespace(bar='XX', foo='YY')
     >>> parser.parse_args('XX --foo'.split())
     Namespace(bar='XX', foo='c')
     >>> parser.parse_args(''.split())
     Namespace(bar='d', foo='d')

  ``nargs='?'`` のよくある利用例の1つは、入出力ファイルの指定オプションです::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
     ...                     default=sys.stdin)
     >>> parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
     ...                     default=sys.stdout)
     >>> parser.parse_args(['input.txt', 'output.txt'])
     Namespace(infile=<open file 'input.txt', mode 'r' at 0x...>,
               outfile=<open file 'output.txt', mode 'w' at 0x...>)
     >>> parser.parse_args([])
     Namespace(infile=<open file '<stdin>', mode 'r' at 0x...>,
               outfile=<open file '<stdout>', mode 'w' at 0x...>)

* ``'*'``. 全てのコマンドライン引数がリストに集められます。複数の位置引数が
  ``nargs='*'`` を持つことにあまり意味はありませんが、複数のオプション引数が
  ``nargs='*'`` を持つことはありえます。例えば::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', nargs='*')
     >>> parser.add_argument('--bar', nargs='*')
     >>> parser.add_argument('baz', nargs='*')
     >>> parser.parse_args('a b --foo x y --bar 1 2'.split())
     Namespace(bar=['1', '2'], baz=['a', 'b'], foo=['x', 'y'])

* ``'+'``. ``'*'`` と同じように、全てのコマンドライン引数をリストに集めます。
  加えて、最低でも1つのコマンドライン引数が存在しない場合にエラーメッセージを
  生成します。例えば::

     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> parser.add_argument('foo', nargs='+')
     >>> parser.parse_args('a b'.split())
     Namespace(foo=['a', 'b'])
     >>> parser.parse_args(''.split())
     usage: PROG [-h] foo [foo ...]
     PROG: error: too few arguments

``nargs`` キーワード引数が指定されない場合、消費される引数の数は action_ によって
決定されます。通常これは、1つのコマンドライン引数は1つのアイテムになる(リストには
ならない)ことを意味します。


const
^^^^^

:meth:`~ArgumentParser.add_argument` の ``const`` 引数は、コマンドライン引数から
読み込まれないけれども :class:`ArgumentParser` のいくつかのアクションで必要と
される値のために使われます。この引数の2つのよくあるユースケースは:

* :meth:`~ArgumentParser.add_argument` が ``action='store_const'`` か
  ``action='append_const'`` で呼び出された時、これらのアクションは ``const``
  の値を :meth:`~ArgumentParser.parse_args` が返すオブジェクトの属性に追加します。
  サンプルは action_ の解説を参照してください。

* :meth:`~ArgumentParser.add_argument` がオプション文字列 (``-f`` や ``--foo``)
  と ``nargs='?'`` で呼び出された場合。この場合0個か1つのコマンドライン引数を
  取るオプション引数が作られます。オプション引数にコマンドライン引数が続かなかった
  場合、 ``const`` の値が代わりに利用されます。
  サンプルは nargs_ の解説を参照してください。

``const`` キーワード引数のデフォルト値は ``None`` です。


default
^^^^^^^

All optional arguments and some positional arguments may be omitted at the
command line.  The ``default`` keyword argument of
:meth:`~ArgumentParser.add_argument`, whose value defaults to ``None``,
specifies what value should be used if the command-line arg is not present.
For optional arguments, the ``default`` value is used when the option string
was not present at the command line::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', default=42)
   >>> parser.parse_args('--foo 2'.split())
   Namespace(foo='2')
   >>> parser.parse_args(''.split())
   Namespace(foo=42)

For positional arguments with nargs_ ``='?'`` or ``'*'``, the ``default`` value
is used when no command-line arg was present::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('foo', nargs='?', default=42)
   >>> parser.parse_args('a'.split())
   Namespace(foo='a')
   >>> parser.parse_args(''.split())
   Namespace(foo=42)


Providing ``default=argparse.SUPPRESS`` causes no attribute to be added if the
command-line argument was not present.::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', default=argparse.SUPPRESS)
   >>> parser.parse_args([])
   Namespace()
   >>> parser.parse_args(['--foo', '1'])
   Namespace(foo='1')


type
^^^^

By default, ArgumentParser objects read command-line args in as simple strings.
However, quite often the command-line string should instead be interpreted as
another type, like a :class:`float`, :class:`int` or :class:`file`.  The
``type`` keyword argument of :meth:`~ArgumentParser.add_argument` allows any
necessary type-checking and type-conversions to be performed.  Many common
built-in types can be used directly as the value of the ``type`` argument::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('foo', type=int)
   >>> parser.add_argument('bar', type=file)
   >>> parser.parse_args('2 temp.txt'.split())
   Namespace(bar=<open file 'temp.txt', mode 'r' at 0x...>, foo=2)

To ease the use of various types of files, the argparse module provides the
factory FileType which takes the ``mode=`` and ``bufsize=`` arguments of the
``file`` object.  For example, ``FileType('w')`` can be used to create a
writable file::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('bar', type=argparse.FileType('w'))
   >>> parser.parse_args(['out.txt'])
   Namespace(bar=<open file 'out.txt', mode 'w' at 0x...>)

``type=`` can take any callable that takes a single string argument and returns
the type-converted value::

   >>> def perfect_square(string):
   ...     value = int(string)
   ...     sqrt = math.sqrt(value)
   ...     if sqrt != int(sqrt):
   ...         msg = "%r is not a perfect square" % string
   ...         raise argparse.ArgumentTypeError(msg)
   ...     return value
   ...
   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('foo', type=perfect_square)
   >>> parser.parse_args('9'.split())
   Namespace(foo=9)
   >>> parser.parse_args('7'.split())
   usage: PROG [-h] foo
   PROG: error: argument foo: '7' is not a perfect square

The choices_ keyword argument may be more convenient for type checkers that
simply check against a range of values::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('foo', type=int, choices=xrange(5, 10))
   >>> parser.parse_args('7'.split())
   Namespace(foo=7)
   >>> parser.parse_args('11'.split())
   usage: PROG [-h] {5,6,7,8,9}
   PROG: error: argument foo: invalid choice: 11 (choose from 5, 6, 7, 8, 9)

See the choices_ section for more details.


choices
^^^^^^^

Some command-line args should be selected from a restricted set of values.
These can be handled by passing a container object as the ``choices`` keyword
argument to :meth:`~ArgumentParser.add_argument`.  When the command line is
parsed, arg values will be checked, and an error message will be displayed if
the arg was not one of the acceptable values::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('foo', choices='abc')
   >>> parser.parse_args('c'.split())
   Namespace(foo='c')
   >>> parser.parse_args('X'.split())
   usage: PROG [-h] {a,b,c}
   PROG: error: argument foo: invalid choice: 'X' (choose from 'a', 'b', 'c')

Note that inclusion in the ``choices`` container is checked after any type_
conversions have been performed, so the type of the objects in the ``choices``
container should match the type_ specified::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('foo', type=complex, choices=[1, 1j])
   >>> parser.parse_args('1j'.split())
   Namespace(foo=1j)
   >>> parser.parse_args('-- -4'.split())
   usage: PROG [-h] {1,1j}
   PROG: error: argument foo: invalid choice: (-4+0j) (choose from 1, 1j)

Any object that supports the ``in`` operator can be passed as the ``choices``
value, so :class:`dict` objects, :class:`set` objects, custom containers,
etc. are all supported.


required
^^^^^^^^

In general, the :mod:`argparse` module assumes that flags like ``-f`` and ``--bar``
indicate *optional* arguments, which can always be omitted at the command line.
To make an option *required*, ``True`` can be specified for the ``required=``
keyword argument to :meth:`~ArgumentParser.add_argument`::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', required=True)
   >>> parser.parse_args(['--foo', 'BAR'])
   Namespace(foo='BAR')
   >>> parser.parse_args([])
   usage: argparse.py [-h] [--foo FOO]
   argparse.py: error: option --foo is required

As the example shows, if an option is marked as ``required``,
:meth:`~ArgumentParser.parse_args` will report an error if that option is not
present at the command line.

.. note::

    Required options are generally considered bad form because users expect
    *options* to be *optional*, and thus they should be avoided when possible.


help
^^^^

The ``help`` value is a string containing a brief description of the argument.
When a user requests help (usually by using ``-h`` or ``--help`` at the
command line), these ``help`` descriptions will be displayed with each
argument::

   >>> parser = argparse.ArgumentParser(prog='frobble')
   >>> parser.add_argument('--foo', action='store_true',
   ...         help='foo the bars before frobbling')
   >>> parser.add_argument('bar', nargs='+',
   ...         help='one of the bars to be frobbled')
   >>> parser.parse_args('-h'.split())
   usage: frobble [-h] [--foo] bar [bar ...]

   positional arguments:
    bar     one of the bars to be frobbled

   optional arguments:
    -h, --help  show this help message and exit
    --foo   foo the bars before frobbling

The ``help`` strings can include various format specifiers to avoid repetition
of things like the program name or the argument default_.  The available
specifiers include the program name, ``%(prog)s`` and most keyword arguments to
:meth:`~ArgumentParser.add_argument`, e.g. ``%(default)s``, ``%(type)s``, etc.::

   >>> parser = argparse.ArgumentParser(prog='frobble')
   >>> parser.add_argument('bar', nargs='?', type=int, default=42,
   ...         help='the bar to %(prog)s (default: %(default)s)')
   >>> parser.print_help()
   usage: frobble [-h] [bar]

   positional arguments:
    bar     the bar to frobble (default: 42)

   optional arguments:
    -h, --help  show this help message and exit


metavar
^^^^^^^

When :class:`ArgumentParser` generates help messages, it need some way to refer
to each expected argument.  By default, ArgumentParser objects use the dest_
value as the "name" of each object.  By default, for positional argument
actions, the dest_ value is used directly, and for optional argument actions,
the dest_ value is uppercased.  So, a single positional argument with
``dest='bar'`` will that argument will be referred to as ``bar``. A single
optional argument ``--foo`` that should be followed by a single command-line arg
will be referred to as ``FOO``.  An example::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo')
   >>> parser.add_argument('bar')
   >>> parser.parse_args('X --foo Y'.split())
   Namespace(bar='X', foo='Y')
   >>> parser.print_help()
   usage:  [-h] [--foo FOO] bar

   positional arguments:
    bar

   optional arguments:
    -h, --help  show this help message and exit
    --foo FOO

An alternative name can be specified with ``metavar``::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', metavar='YYY')
   >>> parser.add_argument('bar', metavar='XXX')
   >>> parser.parse_args('X --foo Y'.split())
   Namespace(bar='X', foo='Y')
   >>> parser.print_help()
   usage:  [-h] [--foo YYY] XXX

   positional arguments:
    XXX

   optional arguments:
    -h, --help  show this help message and exit
    --foo YYY

Note that ``metavar`` only changes the *displayed* name - the name of the
attribute on the :meth:`~ArgumentParser.parse_args` object is still determined
by the dest_ value.

Different values of ``nargs`` may cause the metavar to be used multiple times.
Providing a tuple to ``metavar`` specifies a different display for each of the
arguments::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-x', nargs=2)
   >>> parser.add_argument('--foo', nargs=2, metavar=('bar', 'baz'))
   >>> parser.print_help()
   usage: PROG [-h] [-x X X] [--foo bar baz]

   optional arguments:
    -h, --help     show this help message and exit
    -x X X
    --foo bar baz


dest
^^^^

Most :class:`ArgumentParser` actions add some value as an attribute of the
object returned by :meth:`~ArgumentParser.parse_args`.  The name of this
attribute is determined by the ``dest`` keyword argument of
:meth:`~ArgumentParser.add_argument`.  For positional argument actions,
``dest`` is normally supplied as the first argument to
:meth:`~ArgumentParser.add_argument`::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('bar')
   >>> parser.parse_args('XXX'.split())
   Namespace(bar='XXX')

For optional argument actions, the value of ``dest`` is normally inferred from
the option strings.  :class:`ArgumentParser` generates the value of ``dest`` by
taking the first long option string and stripping away the initial ``'--'``
string.  If no long option strings were supplied, ``dest`` will be derived from
the first short option string by stripping the initial ``'-'`` character.  Any
internal ``'-'`` characters will be converted to ``'_'`` characters to make sure
the string is a valid attribute name.  The examples below illustrate this
behavior::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('-f', '--foo-bar', '--foo')
   >>> parser.add_argument('-x', '-y')
   >>> parser.parse_args('-f 1 -x 2'.split())
   Namespace(foo_bar='1', x='2')
   >>> parser.parse_args('--foo 1 -y 2'.split())
   Namespace(foo_bar='1', x='2')

``dest`` allows a custom attribute name to be provided::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', dest='bar')
   >>> parser.parse_args('--foo XXX'.split())
   Namespace(bar='XXX')


The parse_args() method
-----------------------

.. method:: ArgumentParser.parse_args(args=None, namespace=None)

   Convert argument strings to objects and assign them as attributes of the
   namespace.  Return the populated namespace.

   Previous calls to :meth:`add_argument` determine exactly what objects are
   created and how they are assigned. See the documentation for
   :meth:`add_argument` for details.

   By default, the arg strings are taken from :data:`sys.argv`, and a new empty
   :class:`Namespace` object is created for the attributes.


Option value syntax
^^^^^^^^^^^^^^^^^^^

The :meth:`~ArgumentParser.parse_args` method supports several ways of
specifying the value of an option (if it takes one).  In the simplest case, the
option and its value are passed as two separate arguments::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-x')
   >>> parser.add_argument('--foo')
   >>> parser.parse_args('-x X'.split())
   Namespace(foo=None, x='X')
   >>> parser.parse_args('--foo FOO'.split())
   Namespace(foo='FOO', x=None)

For long options (options with names longer than a single character), the option
and value can also be passed as a single command-line argument, using ``=`` to
separate them::

   >>> parser.parse_args('--foo=FOO'.split())
   Namespace(foo='FOO', x=None)

For short options (options only one character long), the option and its value
can be concatenated::

   >>> parser.parse_args('-xX'.split())
   Namespace(foo=None, x='X')

Several short options can be joined together, using only a single ``-`` prefix,
as long as only the last option (or none of them) requires a value::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-x', action='store_true')
   >>> parser.add_argument('-y', action='store_true')
   >>> parser.add_argument('-z')
   >>> parser.parse_args('-xyzZ'.split())
   Namespace(x=True, y=True, z='Z')


Invalid arguments
^^^^^^^^^^^^^^^^^

While parsing the command line, :meth:`~ArgumentParser.parse_args` checks for a
variety of errors, including ambiguous options, invalid types, invalid options,
wrong number of positional arguments, etc.  When it encounters such an error,
it exits and prints the error along with a usage message::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('--foo', type=int)
   >>> parser.add_argument('bar', nargs='?')

   >>> # invalid type
   >>> parser.parse_args(['--foo', 'spam'])
   usage: PROG [-h] [--foo FOO] [bar]
   PROG: error: argument --foo: invalid int value: 'spam'

   >>> # invalid option
   >>> parser.parse_args(['--bar'])
   usage: PROG [-h] [--foo FOO] [bar]
   PROG: error: no such option: --bar

   >>> # wrong number of arguments
   >>> parser.parse_args(['spam', 'badger'])
   usage: PROG [-h] [--foo FOO] [bar]
   PROG: error: extra arguments found: badger


Arguments containing ``"-"``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :meth:`~ArgumentParser.parse_args` method attempts to give errors whenever
the user has clearly made a mistake, but some situations are inherently
ambiguous.  For example, the command-line arg ``'-1'`` could either be an
attempt to specify an option or an attempt to provide a positional argument.
The :meth:`~ArgumentParser.parse_args` method is cautious here: positional
arguments may only begin with ``'-'`` if they look like negative numbers and
there are no options in the parser that look like negative numbers::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-x')
   >>> parser.add_argument('foo', nargs='?')

   >>> # no negative number options, so -1 is a positional argument
   >>> parser.parse_args(['-x', '-1'])
   Namespace(foo=None, x='-1')

   >>> # no negative number options, so -1 and -5 are positional arguments
   >>> parser.parse_args(['-x', '-1', '-5'])
   Namespace(foo='-5', x='-1')

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-1', dest='one')
   >>> parser.add_argument('foo', nargs='?')

   >>> # negative number options present, so -1 is an option
   >>> parser.parse_args(['-1', 'X'])
   Namespace(foo=None, one='X')

   >>> # negative number options present, so -2 is an option
   >>> parser.parse_args(['-2'])
   usage: PROG [-h] [-1 ONE] [foo]
   PROG: error: no such option: -2

   >>> # negative number options present, so both -1s are options
   >>> parser.parse_args(['-1', '-1'])
   usage: PROG [-h] [-1 ONE] [foo]
   PROG: error: argument -1: expected one argument

If you have positional arguments that must begin with ``'-'`` and don't look
like negative numbers, you can insert the pseudo-argument ``'--'`` which tells
:meth:`~ArgumentParser.parse_args` that everything after that is a positional
argument::

   >>> parser.parse_args(['--', '-f'])
   Namespace(foo='-f', one=None)


Argument abbreviations
^^^^^^^^^^^^^^^^^^^^^^

The :meth:`~ArgumentParser.parse_args` method allows long options to be
abbreviated if the abbreviation is unambiguous::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-bacon')
   >>> parser.add_argument('-badger')
   >>> parser.parse_args('-bac MMM'.split())
   Namespace(bacon='MMM', badger=None)
   >>> parser.parse_args('-bad WOOD'.split())
   Namespace(bacon=None, badger='WOOD')
   >>> parser.parse_args('-ba BA'.split())
   usage: PROG [-h] [-bacon BACON] [-badger BADGER]
   PROG: error: ambiguous option: -ba could match -badger, -bacon

An error is produced for arguments that could produce more than one options.


Beyond ``sys.argv``
^^^^^^^^^^^^^^^^^^^

Sometimes it may be useful to have an ArgumentParser parse args other than those
of :data:`sys.argv`.  This can be accomplished by passing a list of strings to
:meth:`~ArgumentParser.parse_args`.  This is useful for testing at the
interactive prompt::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument(
   ...     'integers', metavar='int', type=int, choices=xrange(10),
   ...  nargs='+', help='an integer in the range 0..9')
   >>> parser.add_argument(
   ...     '--sum', dest='accumulate', action='store_const', const=sum,
   ...   default=max, help='sum the integers (default: find the max)')
   >>> parser.parse_args(['1', '2', '3', '4'])
   Namespace(accumulate=<built-in function max>, integers=[1, 2, 3, 4])
   >>> parser.parse_args('1 2 3 4 --sum'.split())
   Namespace(accumulate=<built-in function sum>, integers=[1, 2, 3, 4])


The Namespace object
^^^^^^^^^^^^^^^^^^^^

By default, :meth:`~ArgumentParser.parse_args` will return a new object of type
:class:`Namespace` where the necessary attributes have been set. This class is
deliberately simple, just an :class:`object` subclass with a readable string
representation. If you prefer to have dict-like view of the attributes, you
can use the standard Python idiom via :func:`vars`::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo')
   >>> args = parser.parse_args(['--foo', 'BAR'])
   >>> vars(args)
   {'foo': 'BAR'}

It may also be useful to have an :class:`ArgumentParser` assign attributes to an
already existing object, rather than a new :class:`Namespace` object.  This can
be achieved by specifying the ``namespace=`` keyword argument::

   >>> class C(object):
   ...     pass
   ...
   >>> c = C()
   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo')
   >>> parser.parse_args(args=['--foo', 'BAR'], namespace=c)
   >>> c.foo
   'BAR'


Other utilities
---------------

Sub-commands
^^^^^^^^^^^^

.. method:: ArgumentParser.add_subparsers()

   Many programs split up their functionality into a number of sub-commands,
   for example, the ``svn`` program can invoke sub-commands like ``svn
   checkout``, ``svn update``, and ``svn commit``.  Splitting up functionality
   this way can be a particularly good idea when a program performs several
   different functions which require different kinds of command-line arguments.
   :class:`ArgumentParser` supports the creation of such sub-commands with the
   :meth:`add_subparsers` method.  The :meth:`add_subparsers` method is normally
   called with no arguments and returns an special action object.  This object
   has a single method, :meth:`~ArgumentParser.add_parser`, which takes a
   command name and any :class:`ArgumentParser` constructor arguments, and
   returns an :class:`ArgumentParser` object that can be modified as usual.

   Some example usage::

     >>> # create the top-level parser
     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> parser.add_argument('--foo', action='store_true', help='foo help')
     >>> subparsers = parser.add_subparsers(help='sub-command help')
     >>>
     >>> # create the parser for the "a" command
     >>> parser_a = subparsers.add_parser('a', help='a help')
     >>> parser_a.add_argument('bar', type=int, help='bar help')
     >>>
     >>> # create the parser for the "b" command
     >>> parser_b = subparsers.add_parser('b', help='b help')
     >>> parser_b.add_argument('--baz', choices='XYZ', help='baz help')
     >>>
     >>> # parse some arg lists
     >>> parser.parse_args(['a', '12'])
     Namespace(bar=12, foo=False)
     >>> parser.parse_args(['--foo', 'b', '--baz', 'Z'])
     Namespace(baz='Z', foo=True)

   Note that the object returned by :meth:`parse_args` will only contain
   attributes for the main parser and the subparser that was selected by the
   command line (and not any other subparsers).  So in the example above, when
   the ``"a"`` command is specified, only the ``foo`` and ``bar`` attributes are
   present, and when the ``"b"`` command is specified, only the ``foo`` and
   ``baz`` attributes are present.

   Similarly, when a help message is requested from a subparser, only the help
   for that particular parser will be printed.  The help message will not
   include parent parser or sibling parser messages.  (A help message for each
   subparser command, however, can be given by supplying the ``help=`` argument
   to :meth:`add_parser` as above.)

   ::

     >>> parser.parse_args(['--help'])
     usage: PROG [-h] [--foo] {a,b} ...

     positional arguments:
       {a,b}   sub-command help
     a     a help
     b     b help

     optional arguments:
       -h, --help  show this help message and exit
       --foo   foo help

     >>> parser.parse_args(['a', '--help'])
     usage: PROG a [-h] bar

     positional arguments:
       bar     bar help

     optional arguments:
       -h, --help  show this help message and exit

     >>> parser.parse_args(['b', '--help'])
     usage: PROG b [-h] [--baz {X,Y,Z}]

     optional arguments:
       -h, --help     show this help message and exit
       --baz {X,Y,Z}  baz help

   The :meth:`add_subparsers` method also supports ``title`` and ``description``
   keyword arguments.  When either is present, the subparser's commands will
   appear in their own group in the help output.  For example::

     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers(title='subcommands',
     ...                                    description='valid subcommands',
     ...                                    help='additional help')
     >>> subparsers.add_parser('foo')
     >>> subparsers.add_parser('bar')
     >>> parser.parse_args(['-h'])
     usage:  [-h] {foo,bar} ...

     optional arguments:
       -h, --help  show this help message and exit

     subcommands:
       valid subcommands

       {foo,bar}   additional help


   One particularly effective way of handling sub-commands is to combine the use
   of the :meth:`add_subparsers` method with calls to :meth:`set_defaults` so
   that each subparser knows which Python function it should execute.  For
   example::

     >>> # sub-command functions
     >>> def foo(args):
     ...     print args.x * args.y
     ...
     >>> def bar(args):
     ...     print '((%s))' % args.z
     ...
     >>> # create the top-level parser
     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers()
     >>>
     >>> # create the parser for the "foo" command
     >>> parser_foo = subparsers.add_parser('foo')
     >>> parser_foo.add_argument('-x', type=int, default=1)
     >>> parser_foo.add_argument('y', type=float)
     >>> parser_foo.set_defaults(func=foo)
     >>>
     >>> # create the parser for the "bar" command
     >>> parser_bar = subparsers.add_parser('bar')
     >>> parser_bar.add_argument('z')
     >>> parser_bar.set_defaults(func=bar)
     >>>
     >>> # parse the args and call whatever function was selected
     >>> args = parser.parse_args('foo 1 -x 2'.split())
     >>> args.func(args)
     2.0
     >>>
     >>> # parse the args and call whatever function was selected
     >>> args = parser.parse_args('bar XYZYX'.split())
     >>> args.func(args)
     ((XYZYX))

   This way, you can let :meth:`parse_args` does the job of calling the
   appropriate function after argument parsing is complete.  Associating
   functions with actions like this is typically the easiest way to handle the
   different actions for each of your subparsers.  However, if it is necessary
   to check the name of the subparser that was invoked, the ``dest`` keyword
   argument to the :meth:`add_subparsers` call will work::

     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers(dest='subparser_name')
     >>> subparser1 = subparsers.add_parser('1')
     >>> subparser1.add_argument('-x')
     >>> subparser2 = subparsers.add_parser('2')
     >>> subparser2.add_argument('y')
     >>> parser.parse_args(['2', 'frobble'])
     Namespace(subparser_name='2', y='frobble')


FileType objects
^^^^^^^^^^^^^^^^

.. class:: FileType(mode='r', bufsize=None)

   The :class:`FileType` factory creates objects that can be passed to the type
   argument of :meth:`ArgumentParser.add_argument`.  Arguments that have
   :class:`FileType` objects as their type will open command-line args as files
   with the requested modes and buffer sizes:

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--output', type=argparse.FileType('wb', 0))
   >>> parser.parse_args(['--output', 'out'])
   Namespace(output=<open file 'out', mode 'wb' at 0x...>)

   FileType objects understand the pseudo-argument ``'-'`` and automatically
   convert this into ``sys.stdin`` for readable :class:`FileType` objects and
   ``sys.stdout`` for writable :class:`FileType` objects:

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('infile', type=argparse.FileType('r'))
   >>> parser.parse_args(['-'])
   Namespace(infile=<open file '<stdin>', mode 'r' at 0x...>)


Argument groups
^^^^^^^^^^^^^^^

.. method:: ArgumentParser.add_argument_group(title=None, description=None)

   By default, :class:`ArgumentParser` groups command-line arguments into
   "positional arguments" and "optional arguments" when displaying help
   messages. When there is a better conceptual grouping of arguments than this
   default one, appropriate groups can be created using the
   :meth:`add_argument_group` method::

     >>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
     >>> group = parser.add_argument_group('group')
     >>> group.add_argument('--foo', help='foo help')
     >>> group.add_argument('bar', help='bar help')
     >>> parser.print_help()
     usage: PROG [--foo FOO] bar

     group:
       bar    bar help
       --foo FOO  foo help

   The :meth:`add_argument_group` method returns an argument group object which
   has an :meth:`~ArgumentParser.add_argument` method just like a regular
   :class:`ArgumentParser`.  When an argument is added to the group, the parser
   treats it just like a normal argument, but displays the argument in a
   separate group for help messages.  The :meth:`add_argument_group` method
   accepts *title* and *description* arguments which can be used to
   customize this display::

     >>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
     >>> group1 = parser.add_argument_group('group1', 'group1 description')
     >>> group1.add_argument('foo', help='foo help')
     >>> group2 = parser.add_argument_group('group2', 'group2 description')
     >>> group2.add_argument('--bar', help='bar help')
     >>> parser.print_help()
     usage: PROG [--bar BAR] foo

     group1:
       group1 description

       foo    foo help

     group2:
       group2 description

       --bar BAR  bar help

   Note that any arguments not your user defined groups will end up back in the
   usual "positional arguments" and "optional arguments" sections.


Mutual exclusion
^^^^^^^^^^^^^^^^

.. method:: add_mutually_exclusive_group(required=False)

   Create a mutually exclusive group. :mod:`argparse` will make sure that only
   one of the arguments in the mutually exclusive group was present on the
   command line::

     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> group = parser.add_mutually_exclusive_group()
     >>> group.add_argument('--foo', action='store_true')
     >>> group.add_argument('--bar', action='store_false')
     >>> parser.parse_args(['--foo'])
     Namespace(bar=True, foo=True)
     >>> parser.parse_args(['--bar'])
     Namespace(bar=False, foo=False)
     >>> parser.parse_args(['--foo', '--bar'])
     usage: PROG [-h] [--foo | --bar]
     PROG: error: argument --bar: not allowed with argument --foo

   The :meth:`add_mutually_exclusive_group` method also accepts a *required*
   argument, to indicate that at least one of the mutually exclusive arguments
   is required::

     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> group = parser.add_mutually_exclusive_group(required=True)
     >>> group.add_argument('--foo', action='store_true')
     >>> group.add_argument('--bar', action='store_false')
     >>> parser.parse_args([])
     usage: PROG [-h] (--foo | --bar)
     PROG: error: one of the arguments --foo --bar is required

   Note that currently mutually exclusive argument groups do not support the
   *title* and *description* arguments of
   :meth:`~ArgumentParser.add_argument_group`.


Parser defaults
^^^^^^^^^^^^^^^

.. method:: ArgumentParser.set_defaults(**kwargs)

   Most of the time, the attributes of the object returned by :meth:`parse_args`
   will be fully determined by inspecting the command-line args and the argument
   actions.  :meth:`set_defaults` allows some additional
   attributes that are determined without any inspection of the command line to
   be added::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('foo', type=int)
     >>> parser.set_defaults(bar=42, baz='badger')
     >>> parser.parse_args(['736'])
     Namespace(bar=42, baz='badger', foo=736)

   Note that parser-level defaults always override argument-level defaults::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', default='bar')
     >>> parser.set_defaults(foo='spam')
     >>> parser.parse_args([])
     Namespace(foo='spam')

   Parser-level defaults can be particularly useful when working with multiple
   parsers.  See the :meth:`~ArgumentParser.add_subparsers` method for an
   example of this type.

.. method:: ArgumentParser.get_default(dest)

   Get the default value for a namespace attribute, as set by either
   :meth:`~ArgumentParser.add_argument` or by
   :meth:`~ArgumentParser.set_defaults`::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', default='badger')
     >>> parser.get_default('foo')
     'badger'


Printing help
^^^^^^^^^^^^^

In most typical applications, :meth:`~ArgumentParser.parse_args` will take
care of formatting and printing any usage or error messages.  However, several
formatting methods are available:

.. method:: ArgumentParser.print_usage(file=None)

   Print a brief description of how the :class:`ArgumentParser` should be
   invoked on the command line.  If *file* is ``None``, :data:`sys.stdout` is
   assumed.

.. method:: ArgumentParser.print_help(file=None)

   Print a help message, including the program usage and information about the
   arguments registered with the :class:`ArgumentParser`.  If *file* is
   ``None``, :data:`sys.stdout` is assumed.

There are also variants of these methods that simply return a string instead of
printing it:

.. method:: ArgumentParser.format_usage()

   Return a string containing a brief description of how the
   :class:`ArgumentParser` should be invoked on the command line.

.. method:: ArgumentParser.format_help()

   Return a string containing a help message, including the program usage and
   information about the arguments registered with the :class:`ArgumentParser`.


Partial parsing
^^^^^^^^^^^^^^^

.. method:: ArgumentParser.parse_known_args(args=None, namespace=None)

Sometimes a script may only parse a few of the command-line arguments, passing
the remaining arguments on to another script or program. In these cases, the
:meth:`~ArgumentParser.parse_known_args` method can be useful.  It works much like
:meth:`~ArgumentParser.parse_args` except that it does not produce an error when
extra arguments are present.  Instead, it returns a two item tuple containing
the populated namespace and the list of remaining argument strings.

::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', action='store_true')
   >>> parser.add_argument('bar')
   >>> parser.parse_known_args(['--foo', '--badger', 'BAR', 'spam'])
   (Namespace(bar='BAR', foo=True), ['--badger', 'spam'])


Customizing file parsing
^^^^^^^^^^^^^^^^^^^^^^^^

.. method:: ArgumentParser.convert_arg_line_to_args(arg_line)

   Arguments that are read from a file (see the *fromfile_prefix_chars*
   keyword argument to the :class:`ArgumentParser` constructor) are read one
   argument per line. :meth:`convert_arg_line_to_args` can be overriden for
   fancier reading.

   This method takes a single argument *arg_line* which is a string read from
   the argument file.  It returns a list of arguments parsed from this string.
   The method is called once per line read from the argument file, in order.

   A useful override of this method is one that treats each space-separated word
   as an argument::

    def convert_arg_line_to_args(self, arg_line):
        for arg in arg_line.split():
            if not arg.strip():
                continue
            yield arg


Exiting methods
^^^^^^^^^^^^^^^

.. method:: ArgumentParser.exit(status=0, message=None)

   This method terminates the program, exiting with the specified *status*
   and, if given, it prints a *message* before that.

.. method:: ArgumentParser.error(message)

   This method prints a usage message including the *message* to the
   standard output and terminates the program with a status code of 2.


.. _argparse-from-optparse:

Upgrading optparse code
-----------------------

Originally, the :mod:`argparse` module had attempted to maintain compatibility
with :mod:`optparse`.  However, :mod:`optparse` was difficult to extend
transparently, particularly with the changes required to support the new
``nargs=`` specifiers and better usage messages.  When most everything in
:mod:`optparse` had either been copy-pasted over or monkey-patched, it no
longer seemed practical to try to maintain the backwards compatibility.

A partial upgrade path from :mod:`optparse` to :mod:`argparse`:

* Replace all :meth:`optparse.OptionParser.add_option` calls with
  :meth:`ArgumentParser.add_argument` calls.

* Replace ``options, args = parser.parse_args()`` with ``args =
  parser.parse_args()`` and add additional :meth:`ArgumentParser.add_argument`
  calls for the positional arguments.

* Replace callback actions and the ``callback_*`` keyword arguments with
  ``type`` or ``action`` arguments.

* Replace string names for ``type`` keyword arguments with the corresponding
  type objects (e.g. int, float, complex, etc).

* Replace :class:`optparse.Values` with :class:`Namespace` and
  :exc:`optparse.OptionError` and :exc:`optparse.OptionValueError` with
  :exc:`ArgumentError`.

* Replace strings with implicit arguments such as ``%default`` or ``%prog`` with
  the standard Python syntax to use dictionaries to format strings, that is,
  ``%(default)s`` and ``%(prog)s``.

* Replace the OptionParser constructor ``version`` argument with a call to
  ``parser.add_argument('--version', action='version', version='<the version>')``
