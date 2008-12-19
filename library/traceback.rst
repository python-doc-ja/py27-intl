
:mod:`traceback` --- スタックトレースの表示や取り出し
=====================================================

.. module:: traceback
   :synopsis: スタックトレースの表示や取り出し。


このモジュールはPythonプログラムのスタックトレースを抽出し、書式を整え、表示するための標準インターフェースを提供します。モジュールがスタックトレースを表示するとき、Pythonインタープリタの動作を正確に模倣します。インタープリタの"ラッパー"の場合のように、プログラムの制御の元でスタックトレースを表示したいと思ったときに役に立ちます。

.. index:: object: traceback

モジュールはtracebackオブジェクトを使います --- これは変数``sys.exc_traceback``\
(非推奨)と``sys.last_traceback``に保存され、:func:`sys.exc_info`から三番目の項目として返されるオブジェクト型です。

モジュールは次の関数を定義します:


.. function:: print_tb(traceback[, limit[, file]])

   *traceback*から*limit*までスタックトレース項目を出力します。*limit*が省略されるか``None``の場合は、すべての項目が表示されます。*file*が省略されるか``None``の場合は、``sys.stderr``へ出力されます。それ以外の場合は、出力を受けるためのオープンしたファイルまたはファイルに類似したオブジェクトであるべきです。


.. function:: print_exception(type, value, traceback[, limit[, file]])

   例外情報と*traceback*から*limit*までスタックトレース項目を*file*へ出力します。これは次のようにすることで:func:`print_tb`とは異なります:
   (1) *traceback*が``None``でない場合は、ヘッダ``Traceback (most recent call last):``を出力します。
   (2) スタックトレースの後に例外*type*と*value*を出力します。 (3)
   *type*が:exc:`SyntaxError`であり、*value*が適切な形式の場合は、エラーのおおよその位置を示すカレットを付けて構文エラーが起きた行を出力します。


.. function:: print_exc([limit[, file]])

   これは``print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback, limit,
   file)``のための省略表現です。(非推奨の変数を使う代わりにスレッドセーフな方法で同じ情報を引き出すために、実際には:func:`sys.exc_info`を使います。)


.. function:: format_exc([limit])

   これは、``print_exc(limit)``に似ていますが、ファイルに出力す るかわりに文字列を返します。

   .. versionadded:: 2.4


.. function:: print_last([limit[, file]])

   これは``print_exception(sys.last_type, sys.last_value, sys.last_traceback, limit,
   file)``の省略表現です。


.. function:: print_stack([f[, limit[, file]]])

   この関数は呼び出された時点からのスタックトレースを出力します。オプションの*f*引数は代わりの最初のスタックフレームを指定するために使えます。:func:`print_exception`に付いて言えば、オプションの*limit*と*file*引数は同じ意味を持ちます。


.. function:: extract_tb(traceback[, limit])

   トレースバックオブジェクト*traceback*から*limit*まで取り出された"前処理済み"スタックトレース項目のリストを返します。スタックトレースの代わりの書式設定を行うために役に立ちます。*limit*が省略されるか``None``の場合は、すべての項目が取り出されます。"前処理済み"スタックトレース項目とは四つの部分からなる(*filename*,
   *line number*, *function name*,
   *text*)で、スタックトレースに対して通常出力される情報を表しています。*text*は前と後ろに付いている空白を取り除いた文字列です。ソースが使えない場合は``None``です。


.. function:: extract_stack([f[, limit]])

   現在のスタックフレームから生のトレースバックを取り出します。戻り値は:func:`extract_tb`と同じ形式です。:func:`print_stack`について言えば、オプションの*f*と*limit*引数は同じ意味を持ちます。


.. function:: format_list(list)

   :func:`extract_tb`または:func:`extract_stack`が返すタプルのリストが与えられると、出力の準備を整えた文字列のリストを返します。結果として生じるリストの中の各文字列は、引数リストの中の同じインデックスの要素に対応します。各文字列は末尾に改行が付いています。その上、ソーステキスト行が``None``でないそれらの要素に対しては、文字列は内部に改行を含んでいるかもしれません。


.. function:: format_exception_only(type, value)

   トレースバックの例外部分の書式を設定します。引数は``sys.last_type``と``sys.last_value``のような例外の型と値です。戻り値はそれぞれが改行で終わっている文字列のリストです。通常、リストは一つの文字列を含んでいます。しかし、:exc:`SyntaxError`例外に対しては、(出力されるときに)構文エラーが起きた場所についての詳細な情報を示す行をいくつか含んでいます。どの例外が起きたのかを示すメッセージは、常にリストの最後の文字列です。


.. function:: format_exception(type, value, tb[, limit])

   スタックトレースと例外情報の書式を設定します。引数は:func:`print_exception`の対応する引数と同じ意味を持ちます。戻り値は文字列のリストで、それぞれの文字列は改行で終わり、そのいくつかは内部に改行を含みます。これらの行が連結されて出力される場合は、厳密に:func:`print_exception`と同じテキストが出力されます。


.. function:: format_tb(tb[, limit])

   ``format_list(extract_tb(tb, limit))``の省略表現。


.. function:: format_stack([f[, limit]])

   ``format_list(extract_stack(f, limit))``の省略表現。


.. function:: tb_lineno(tb)

   この関数はトレースバックオブジェクトに設定された現在の行番号をかえします。この関数は必要でした。なぜなら、:option:`-O`フラグがPythonへ渡されたとき、Pythonの2.3より前のバージョンでは``tb.tb_lineno``が正しく更新されなかったからです。この関数は2.3以降のバージョンでは役に立ちません。


.. _traceback-example:

トレースバックの例
------------------

この簡単な例では基本的なread-eval-
printループを実装います。それは標準的なPythonの対話インタープリタループに似ていますが、Pythonのものより便利ではありません。インタープリタループのより完全な実装については、:mod:`code`モジュールを参照してください。
::

   import sys, traceback

   def run_user_code(envdir):
       source = raw_input(">>> ")
       try:
           exec source in envdir
       except:
           print "Exception in user code:"
           print '-'*60
           traceback.print_exc(file=sys.stdout)
           print '-'*60

   envdir = {}
   while 1:
       run_user_code(envdir)

