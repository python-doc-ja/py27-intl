
:mod:`commands` --- コマンド実行ユーティリティ
=================================

.. module:: commands
   :platform: Unix
   :synopsis: 外部コマンドを実行するためのユーティリティです。
.. sectionauthor:: Sue Williams <sbw@provis.com>


:mod:`commands`は、システムへコマンド文字列を渡して実行する :func:`os.popen`のラッパー関数を含んでいるモジュールです。
外部で実行したコマンドの結果や、その終了ステータスを扱います。

:mod:`commands`モジュールは以下の関数を定義しています。


.. function:: getstatusoutput(cmd)

   文字列*cmd*を:func:`os.popen`を使いシェル上で実行し、 タプル``(status, output)``を返します。 実際には``{ cmd
   ; } 2>&1``と実行されるため、 標準出力とエラー出力が混合されます。 また、出力の最後の改行文字は取り除かれます。
   コマンドの終了ステータスはC言語関数の:cfunc:`wait`の規則に従って 解釈することができます。


.. function:: getoutput(cmd)

   :func:`getstatusoutput`に似ていますが、 終了ステータスは無視され、コマンドの出力のみを返します。

.. % TeXの記号文字の扱いを調べてないので変換後どうなるかわからんです。


.. function:: getstatus(file)

   ``ls -ld file``の出力を文字列で返します。 この関数は:func:`getoutput`を使い、引数内の
   バックスラッシュ記号「$\\」とドル記号「$」を適切にエスケープします。

例::

   >>> import commands
   >>> commands.getstatusoutput('ls /bin/ls')
   (0, '/bin/ls')
   >>> commands.getstatusoutput('cat /bin/junk')
   (256, 'cat: /bin/junk: No such file or directory')
   >>> commands.getstatusoutput('/bin/junk')
   (256, 'sh: /bin/junk: not found')
   >>> commands.getoutput('ls /bin/ls')
   '/bin/ls'
   >>> commands.getstatus('/bin/ls')
   '-rwxr-xr-x  1 root        13352 Oct 14  1994 /bin/ls'

