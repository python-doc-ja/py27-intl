
:mod:`getopt` --- コマンドラインオプションのパーザ
==================================================

.. module:: getopt
   :synopsis: ポータブルなコマンドラインオプションのパーザ。長短の両方 の形式をサポートします。


このモジュールは``sys.argv``に入っているコマンドラインオプションの構文解 析を支援します。 '``-``' や '``-``\ ``-``'
の特別扱いも含めて、 Unixの:cfunc:`getopt`と同じ記法をサポートしています。 3番目の引数(省略可能)を設定することで、
GNUのソフトウェアでサポートされているような長形式のオプションも利用することが できます。 このモジュールは1つの関数と例外を提供しています:

.. % This module helps scripts to parse the command line arguments in
.. % \code{sys.argv}.
.. % It supports the same conventions as the \UNIX{} \cfunction{getopt()}
.. % function (including the special meanings of arguments of the form
.. % `\code{-}' and `\code{-}\code{-}').
.. % % That's to fool latex2html into leaving the two hyphens alone!
.. % Long options similar to those supported by
.. % GNU software may be used as well via an optional third argument.
.. % This module provides a single function and an exception:


.. function:: getopt(args, options[, long_options])

   コマンドラインオプションとパラメータのリストを構文解析します。 *args*は構文解析の対象になる引数リストです。これは
   先頭のプログラム名を除いたもので、通常``sys.argv[1:]``で与えられます。 *options*
   はスクリプトで認識させたいオプション文字と、引数が必要な場 合にはコロン(``':'``)をつけます。つまりUnixの
   :cfunc:`getopt`と同じフォーマットになります。

   .. % Parses command line options and parameter list.  \var{args} is the
   .. % argument list to be parsed, without the leading reference to the
   .. % running program. Typically, this means \samp{sys.argv[1:]}.
   .. % \var{options} is the string of option letters that the script wants to
   .. % recognize, with options that require an argument followed by a colon
   .. % (\character{:}; i.e., the same format that \UNIX{}
   .. % \cfunction{getopt()} uses).

   .. % \note{Unlike GNU \cfunction{getopt()}, after a non-option
   .. % argument, all further arguments are considered also non-options.
   .. % This is similar to the way non-GNU \UNIX{} systems work.}

   .. note::

      GNUの :cfunc:`getopt`とは違って、オプションでない引数の後は全て オプションではないと判断されます。これは GNUでない、Unixシステムの挙
      動に近いものです。

   *long_options*は長形式のオプションの名前を示す文字列のリストです。 名前には、先頭の``'-``\ ``-'``は含めません。引数が必要な場合
   には名前の最後に等号(``'='``)を入れます。長形式のオプションだけを 受けつけるためには、*options*は空文字列である必要があります。
   長形式のオプションは、該当するオプションを一意に決定できる長さまで入力さ れていれば認識されます。たとえば、*long_options*が ``['foo',
   'frob']``の場合、:option:`--fo`は:option:`--foo` に該当しますが、:option:`--f` では一意に決定できないので、
   :exc:`GetoptError`が発生します。

   .. % \var{long_options}, if specified, must be a list of strings with the
   .. % names of the long options which should be supported.  The leading
   .. % \code{'-}\code{-'} characters should not be included in the option
   .. % name.  Long options which require an argument should be followed by an
   .. % equal sign (\character{=}).  To accept only long options,
   .. % \var{options} should be an empty string.  Long options on the command
   .. % line can be recognized so long as they provide a prefix of the option
   .. % name that matches exactly one of the accepted options.  For example,
   .. % if \var{long_options} is \code{['foo', 'frob']}, the option
   .. % \longprogramopt{fo} will match as \longprogramopt{foo}, but
   .. % \longprogramopt{f} will not match uniquely, so \exception{GetoptError}
   .. % will be raised.

   返り値は2つの要素から成っています: 最初は ``(option, value)``のタプルのリスト、2つ目はオプションリス
   トを取り除いたあとに残ったプログラムの引数リストです(*args*の末尾部 分のスライスになります)。
   それぞれの引数と値のタプルの最初の要素は、短形式の時はハイフン 1つで始まる文字列(例:``'-x'``)、長形式の時はハイフン2つで始まる文字 列(例:
   ``'-``\ ``-long-option'``)となり、引数が2番目の要素になりま す。引数をとらない場合には空文字列が入ります。オプションは見つかった順
   に並んでいて、複数回同じオプションを指定することができます。長形式と短 形式のオプションは混在させることができます。

   .. % The return value consists of two elements: the first is a list of
   .. % \code{(\var{option}, \var{value})} pairs; the second is the list of
   .. % program arguments left after the option list was stripped (this is a
   .. % trailing slice of \var{args}).  Each option-and-value pair returned
   .. % has the option as its first element, prefixed with a hyphen for short
   .. % options (e.g., \code{'-x'}) or two hyphens for long options (e.g.,
   .. % \code{'-}\code{-long-option'}), and the option argument as its second
   .. % element, or an empty string if the option has no argument.  The
   .. % options occur in the list in the same order in which they were found,
   .. % thus allowing multiple occurrences.  Long and short options may be
   .. % mixed.


.. function:: gnu_getopt(args, options[, long_options])

   この関数はデフォルトでGNUスタイルのスキャンモードを使う以外は :func:`getopt`と同じように動作します。つまり、オプションと
   オプションでない引数とを混在させることができます。:func:`getopt`関 数はオプションでない引数を見つけると解析をやめてしまいます。

   .. % This function works like \function{getopt()}, except that GNU style
   .. % scanning mode is used by default. This means that option and
   .. % non-option arguments may be intermixed. The \function{getopt()}
   .. % function stops processing options as soon as a non-option argument is
   .. % encountered.

   オプション文字列の最初の文字が '+'にするか、環境変数 POSIXLY_CORRECTを設定することで、
   オプションでない引数を見つけると解析をやめるように振舞いを変えることがで きます。

   .. % If the first character of the option string is `+', or if the
   .. % environment variable POSIXLY_CORRECT is set, then option processing
   .. % stops as soon as a non-option argument is encountered.

   .. versionadded:: 2.3


.. exception:: GetoptError

   引数リストの中に認識できないオプションがあった場合か、引数が必要なオプショ ンに引数が与えられなかった場合に発生します。例外の引数は原因を示す文字
   列です。長形式のオプションについては、不要な引数が与えられた場合にもこ
   の例外が発生します。:attr:`msg`属性と:attr:`opt`属性で、エラーメッセー
   ジと関連するオプションを取得できます。特に関係するオプションが無い場合 には:attr:`opt`は空文字列となります。

   .. % This is raised when an unrecognized option is found in the argument
   .. % list or when an option requiring an argument is given none.
   .. % The argument to the exception is a string indicating the cause of the
   .. % error.  For long options, an argument given to an option which does
   .. % not require one will also cause this exception to be raised.  The
   .. % attributes \member{msg} and \member{opt} give the error message and
   .. % related option; if there is no specific option to which the exception
   .. % relates, \member{opt} is an empty string.

   .. versionchanged:: 1.6
      :exc:`GetoptError` は :exc:`error`の別名として導入されました。.


.. exception:: error

   :exc:`GetoptError`へのエイリアスです。後方互換性のために残されてい ます。

Unixスタイルのオプションを使った例です::

   >>> import getopt
   >>> args = '-a -b -cfoo -d bar a1 a2'.split()
   >>> args
   ['-a', '-b', '-cfoo', '-d', 'bar', 'a1', 'a2']
   >>> optlist, args = getopt.getopt(args, 'abc:d:')
   >>> optlist
   [('-a', ''), ('-b', ''), ('-c', 'foo'), ('-d', 'bar')]
   >>> args
   ['a1', 'a2']

長形式のオプションを使っても同様です::

   >>> s = '--condition=foo --testing --output-file abc.def -x a1 a2'
   >>> args = s.split()
   >>> args
   ['--condition=foo', '--testing', '--output-file', 'abc.def', '-x', 'a1', 'a2']
   >>> optlist, args = getopt.getopt(args, 'x', [
   ...     'condition=', 'output-file=', 'testing'])
   >>> optlist
   [('--condition', 'foo'), ('--testing', ''), ('--output-file', 'abc.def'), ('-x',
    '')]
   >>> args
   ['a1', 'a2']

スクリプト中での典型的な使い方は以下のようになります::

   import getopt, sys

   def main():
       try:
           opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
       except getopt.GetoptError:
           # ヘルプメッセージを出力して終了
           usage()
           sys.exit(2)
       output = None
       verbose = False
       for o, a in opts:
           if o == "-v":
               verbose = True
           if o in ("-h", "--help"):
               usage()
               sys.exit()
           if o in ("-o", "--output"):
               output = a
       # ...

   if __name__ == "__main__":
       main()


.. seealso::

   Module :mod:`optparse`
      よりオブジェクト指向的なコマンドラインオプショ ンのパーズを提供します。

