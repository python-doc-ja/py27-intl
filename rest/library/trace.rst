--- Python-Docs-2.4/./lib/libtrace.tex  1970-01-01 09:00:00.000000000 +0900 +++
Python-Docs-2.5/./lib/libtrace.tex      2006-05-03 11:04:40.000000000 +0900 @@
-0,1 +1,1 @@


:mod:`trace` --- Python ステートメント実行のトレースと追跡
==========================================================

.. module:: trace
   :synopsis: Python ステートメント実行のトレースと追跡


:mod:`trace` モジュールはプログラム実行のトレースを可能にし, generate
ステートメントのカバレッジリストを注釈付きで生成して、呼び出し元/呼び出し先の 関連やプログラム実行中に実行された関数のリストを出力します。これは別個の
プログラム中またはコマンドラインから利用することができます。


.. _trace-cli:

コマンドラインからの利用
------------------------

:mod:`trace` モジュールはコマンドラインから起動することができます。これは次のように単純です。 ::

   python -m trace --count somefile.py ...

これで、:file:`somefile.py` の実行中に import された Python モジュールの注釈付きリストが生成されます。

以下のコマンドライン引数がサポートされています：

:option:`--trace`, :option:`-t`
   実行されるままに行を表示します。

:option:`--count`, :option:`-c`
   プログラム完了時に、それぞれのステートメントが何回実行されたかを示す 注釈付きリストのファイルを生成します。

:option:`--report`, :option:`-r`
   :option:`--count` と :option:`--file` 引数を使った、過去の プログラム実行結果から注釈付きリストのファイルを生成します。

:option:`--no-report`, :option:`-R`
   注釈付きリストを生成しません。これは :option:`--count` を何度か走らせてから 最後に単一の注釈付きリストを生成するような場合に便利です。

:option:`--listfuncs`, :option:`-l`
   プログラム実行の際に実行された関数を列挙します。

:option:`--trackcalls`, :option:`-T`
   プログラム実行によって明らかになった呼び出しの関連を生成します。

:option:`--file`, :option:`-f`
   カウント(count) を含む（べき）ファイルに名前をつけます。

:option:`--coverdir`, :option:`-C`
   中に注釈付きリストのファイルを保存するディレクトリを指定します。

:option:`--missing`, :option:`-m`
   注釈付きリストの生成時に、実行されなかった行に '``>>>>>>``' の印を付けます。

:option:`--summary`, :option:`-s`
   :option:`--count` または :option:`--report` の利用時に、
   処理されたファイルそれぞれの簡潔なサマリを標準出力(stdout)に書き出します。

:option:`--ignore-module`
   指定されたモジュールとそのサブモジュールを（パッケージだった場合に）無視します。 複数回指定できます。

:option:`--ignore-dir`
   指定されたディレクトリとサブディレクトリ中のモジュールとパッケージを 全て無視します。複数回指定できます。


.. _trace-api:

プログラミングインターフェース
------------------------------


.. class:: Trace([count=1[, trace=1[, countfuncs=0[, countcallers=0[, ignoremods=()[, ignoredirs=()[, infile=None[, outfile=None]]]]]]]])

   文(statement)や式(expression)の実行をトレースするオブジェクトを作成します。 全てのパラメタがオプションです。*count*
   は行数を数えます。 *trace* は行実行のトレースを行います。*countfuncs* は実行中に 呼ばれた関数を列挙します。*countcallers*
   は呼び出しの関連の追跡を 行います。*ignoremods* は無視するモジュールやパッケージのリストです。 *ignoredirs*
   は無視するパッケージやモジュールを含むディレクトリのリストです。 *infile* は保存された集計(count)情報を読むファイルです。*outfile* は
   更新された集計(count)情報を書き出すファイルです。


.. method:: Trace.run(cmd)

   *cmd* を、Trace オブジェクトのコントロール下で 現在のトレースパラメタのもとに実行します。


.. method:: Trace.runctx(cmd[, globals=None[, locals=None]])

   *cmd* を、Trace オブジェクトのコントロール下で 現在のトレースパラメタのもと、定義されたグローバルおよびローカル環境で
   実行します。定義しない場合、*globals* と *locals* はデフォルトで 空の辞書となります。


.. method:: Trace.runfunc(func, *args, **kwds)

   与えられた引数の *func* を、Trace オブジェクトのコントロール下で 現在のトレースパラメタのもとに呼び出します。

これはこのモジュールの使い方を示す簡単な例です： ::

   import sys
   import trace

   # Trace オブジェクトを、無視するもの、トレースや行カウントのいずれか
   # または両方を行うか否かを指定して作成します。
   tracer = trace.Trace(
       ignoredirs=[sys.prefix, sys.exec_prefix],
       trace=0,
       count=1)

   # 与えられたトレーサを使って、コマンドを実行します。
   tracer.run('main()')

   # 出力先を /tmp としてレポートを作成します。
   r = tracer.results()
   r.write_results(show_missing=True, coverdir="/tmp")

