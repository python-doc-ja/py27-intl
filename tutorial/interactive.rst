.. _tut-interacting:

**************************
対話入力編集とヒストリ置換
**************************

あるバージョンの Python インタプリタでは、Korn シェルや GNU Bash シェルに見られる機能に似た、現在の入力行に対する編集機能や
ヒストリ置換機能をサポートしています。 この機能は *GNU Readline* ライブラリを使って実装されています。 このライブラリは Emacs スタイルと
vi スタイルの編集をサポート しています。ライブラリには独自のドキュメントがあり、ここでそれを 繰り返すつもりはありません;
とはいえ、基本について簡単に解説する ことにします。ここで述べる対話的な編集とヒストリについては、 Unix 版と Cygwin
版のインタプリタでオプションとして利用 することができます。

.. % Interactive Input Editing and History Substitution
.. % % Some versions of the Python interpreter support editing of the current
.. % % input line and history substitution, similar to facilities found in
.. % % the Korn shell and the GNU Bash shell.  This is implemented using the
.. % % \emph{GNU Readline} library, which supports Emacs-style and vi-style
.. % % editing.  This library has its own documentation which I won't
.. % % duplicate here; however, the basics are easily explained.  The
.. % % interactive editing and history described here are optionally
.. % % available in the \UNIX{} and Cygwin versions of the interpreter.

この章では、Mark Hammond の PythonWin パッケージや、 Python とともに配布される Tk ベースの環境である IDLE にある
編集機能については解説*しません*。 NT 上の DOS ボックスやその他の DOS および Windows 類で働く
コマンド行ヒストリ呼出しもまた別のものです。

.. % % This chapter does \emph{not} document the editing facilities of Mark
.. % % Hammond's PythonWin package or the Tk-based environment, IDLE,
.. % % distributed with Python.  The command line history recall which
.. % % operates within DOS boxes on NT and some other DOS and Windows flavors
.. % % is yet another beast.


.. _tut-lineediting:

行編集
======

入力行の編集がサポートされている場合、インタプリタが一次または二次 プロンプトを出力している際にはいつでも有効になっています。現在の行は、 慣例的な Emacs
制御文字を使って編集することができます。 そのうち最も重要なものとして、以下のようなキーがあります: :kbd:`C-A` (Control-A)
はカーソルを行の先頭へ移動させます。 :kbd:`C-E` は末尾へ移動させます。 :kbd:`C-B` は逆方向へ一つ移動させます。 :kbd:`C-F`
は順方向へ移動させます。 Backspace は逆方向に向かって文字を消します。 :kbd:`C-D` は順方向に向かって消します。 :kbd:`C-K`
は順方向に向かって行の残りを kill し (消し) ます 、 :kbd:`C-Y` は最後に kill された文字列を再び yank し (取り出し) ます。
:kbd:`C-underscore` 最後の変更を元に戻します; これは、繰り返して どんどんさかのぼることができます。

.. % Line Editing
.. % % If supported, input line editing is active whenever the interpreter
.. % % prints a primary or secondary prompt.  The current line can be edited
.. % % using the conventional Emacs control characters.  The most important
.. % % of these are: \kbd{C-A} (Control-A) moves the cursor to the beginning
.. % % of the line, \kbd{C-E} to the end, \kbd{C-B} moves it one position to
.. % % the left, \kbd{C-F} to the right.  Backspace erases the character to
.. % % the left of the cursor, \kbd{C-D} the character to its right.
.. % % \kbd{C-K} kills (erases) the rest of the line to the right of the
.. % % cursor, \kbd{C-Y} yanks back the last killed string.
.. % % \kbd{C-underscore} undoes the last change you made; it can be repeated
.. % % for cumulative effect.


.. _tut-history:

ヒストリ置換
============

ヒストリ置換は次のように働きます。入力された行のうち、空行でない 実行された行はすべてヒストリバッファに保存されます。そして、プロンプト
が呈示されるときには、ヒストリバッファの最も下の新たな行に移動 します。:kbd:`C-P` はヒストリバッファの中を一行だけ上に移動し (戻し)
ます。:kbd:`C-N` は 1 行だけ下に移動します。ヒストリバッファの どの行も編集することができます。行が編集されると、それを示すために
プロンプトの前にアスタリスクが表示されます  [#]_。 :kbd:`Return` キーを押すと現在行がインタプリタへ渡されます。 :kbd:`C-R`
はインクリメンタルな逆方向サーチ (reverse search) を開始し、 :kbd:`C-S` は順方向サーチ (forward search)
を開始します。

.. % History Substitution
.. % % History substitution works as follows.  All non-empty input lines
.. % % issued are saved in a history buffer, and when a new prompt is given
.. % % you are positioned on a new line at the bottom of this buffer.
.. % % \kbd{C-P} moves one line up (back) in the history buffer,
.. % % \kbd{C-N} moves one down.  Any line in the history buffer can be
.. % % edited; an asterisk appears in front of the prompt to mark a line as
.. % % modified.  Pressing the \kbd{Return} key passes the current line to
.. % % the interpreter.  \kbd{C-R} starts an incremental reverse search;
.. % % \kbd{C-S} starts a forward search.


.. _tut-keybindings:

キー割り当て
============

Readline ライブラリのキー割り当て (key binding) やその他のパラメタ は、:file:`~/.inputrc` という初期化ファイル
[#]_にコマンドを置くことでカスタマイズできます。 キー割り当ての形式は

.. % Key Bindings
.. % % The key bindings and some other parameters of the Readline library can
.. % % be customized by placing commands in an initialization file called
.. % % \file{\~{}/.inputrc}.  Key bindings have the form

::

   key-name: function-name

または

.. % % or

::

   "string": function-name

で、オプションの設定方法は

.. % % and options can be set with

::

   set option-name value

です。例えば、以下のように設定します:

.. % % For example:

::

   # vi スタイルの編集を選択する:
   set editing-mode vi

   # 一行だけを使って編集する:
   set horizontal-scroll-mode On

   # いくつかのキーを再束縛する:
   Meta-h: backward-kill-word
   "\C-u": universal-argument
   "\C-x\C-r": re-read-init-file

Python では、:kbd:`Tab` に対するデフォルトの割り当ては TAB の挿入です。 Readline
のデフォルトであるファイル名補完関数ではないので注意して ください。 もし、どうしても Readline のデフォルトを割り当てたいのなら、
:file:`~/.inputrc` に

.. % % Note that the default binding for \kbd{Tab} in Python is to insert a
.. % % \kbd{Tab} character instead of Readline's default filename completion
.. % % function.  If you insist, you can override this by putting

::

   Tab: complete

を入れれば設定を上書きすることができます。 (もちろん、:kbd:`Tab`  を使って補完を行うのに慣れている場合、この設定を行うと
インデントされた継続行を入力しにくくなります。)

.. % % in your \file{\~{}/.inputrc}.  (Of course, this makes it harder to
.. % % type indented continuation lines if you're accustomed to using
.. % % \kbd{Tab} for that purpose.)

.. index::
   module: rlcompleter
   module: readline

変数名とモジュール名の自動的な補完がオプションとして利用できます。 補完をインタプリタの対話モードで有効にするには、
以下の設定をスタートアップファイルに追加します:  [#]_

.. % % Automatic completion of variable and module names is optionally
.. % % available.  To enable it in the interpreter's interactive mode, add
.. % % the following to your startup file:\footnote{
.. % %   Python will execute the contents of a file identified by the
.. % %   \envvar{PYTHONSTARTUP} environment variable when you start an
.. % %   interactive interpreter.}
.. % % \refstmodindex{rlcompleter}\refbimodindex{readline}

::

   import rlcompleter, readline
   readline.parse_and_bind('tab: complete')

この設定は、:kbd:`Tab` キーを補完関数に束縛します。従って、 :kbd:`Tab` キーを二回たたくと補完候補が示されます; 補完機能は Python
の文の名前、現在のローカル変数、および利用可能なモジュール名を 検索します。``string.a`` のようなドットで区切られた式については、 最後の
``'.'`` までの式を評価し、結果として得られたオブジェクトの 属性から補完候補を示します。 :meth:`__getattr__`
メソッドを持ったオブジェクトが式に含まれている 場合、:meth:`__getattr__` がアプリケーション定義のコードを実行する
かもしれないので注意してください。

.. % % This binds the \kbd{Tab} key to the completion function, so hitting
.. % % the \kbd{Tab} key twice suggests completions; it looks at Python
.. % % statement names, the current local variables, and the available module
.. % % names.  For dotted expressions such as \code{string.a}, it will
.. % % evaluate the expression up to the final \character{.} and then
.. % % suggest completions from the attributes of the resulting object.  Note
.. % % that this may execute application-defined code if an object with a
.. % % \method{__getattr__()} method is part of the expression.

より良くできたスタートアップファイルは以下例のようになります。 この例では、作成した名前が不要になると削除されるので気をつけてください;
これは、スタートアップファイルが対話コマンドと同じ名前空間で実行され ているので、不要な名前を除去して対話環境に副作用を生まないように
するためです。import されたモジュールのうち、:mod:`os` のような インタプリタのほとんどのセッションで必要なものについては、残しておくと
便利に思うかもしれません。

.. % % A more capable startup file might look like this example.  Note that
.. % % this deletes the names it creates once they are no longer needed; this
.. % % is done since the startup file is executed in the same namespace as
.. % % the interactive commands, and removing the names avoids creating side
.. % % effects in the interactive environments.  You may find it convenient
.. % % to keep some of the imported modules, such as \module{os}, which turn
.. % % out to be needed in most sessions with the interpreter.

::

   # Add auto-completion and a stored history file of commands to your Python
   # interactive interpreter. Requires Python 2.0+, readline. Autocomplete is
   # bound to the Esc key by default (you can change it - see readline docs).
   #
   # Store the file in ~/.pystartup, and set an environment variable to point
   # to it, e.g. "export PYTHONSTARTUP=/max/home/itamar/.pystartup" in bash.
   #
   # Note that PYTHONSTARTUP does *not* expand "~", so you have to put in the
   # full path to your home directory.

   import atexit
   import os
   import readline
   import rlcompleter

   historyPath = os.path.expanduser("~/.pyhistory")

   def save_history(historyPath=historyPath):
       import readline
       readline.write_history_file(historyPath)

   if os.path.exists(historyPath):
       readline.read_history_file(historyPath)

   atexit.register(save_history)
   del os, atexit, readline, rlcompleter, save_history, historyPath


.. _tut-commentary:

解説
====

この機能は、初期の版のインタプリタに比べれば大きな進歩です; とはいえ、まだいくつかの要望が残されています: 例えば、
行を継続するときに正しいインデントが呈示されたら快適でしょう (パーサは 次の行でインデントトークンが必要かどうかを知っています)。
補完機構がインタプリタのシンボルテーブルを使ってもよいかもしれません。 かっこやクォートなどの対応をチェックする (あるいは指示する) コマンドも
有用でしょう。

.. % Commentary
.. % % This facility is an enormous step forward compared to earlier versions
.. % % of the interpreter; however, some wishes are left: It would be nice if
.. % % the proper indentation were suggested on continuation lines (the
.. % % parser knows if an indent token is required next).  The completion
.. % % mechanism might use the interpreter's symbol table.  A command to
.. % % check (or even suggest) matching parentheses, quotes, etc., would also
.. % % be useful.


.. rubric:: Footnotes

.. [#] 訳注: これはデフォルト設定の Readline では現れません。 ``set mark-modified-lines on`` という行を
   :file:`~/.inputrc` または 環境変数 :envvar:`INPUTRC` が指定するファイルに置くことによって 現れるようになります。

.. [#] 訳注: このファイル名は 環境変数 :envvar:`INPUTRC` がもしあればその指定が優先されます。

.. [#] Python は、対話インタプリタを開始する時に :envvar:`PYTHONSTARTUP`  環境変数が指定するファイルの内容を実行します。

