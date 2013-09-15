:mod:`timeit` --- 小さなコード断片の実行時間計測
================================================

.. module:: timeit
   :synopsis: 小さなコード断片の実行時間計測。


.. versionadded:: 2.3

.. index::
   single: Benchmarking
   single: Performance

--------------

このモジュールは Python の小さなコード断片の時間を簡単に計測する手段を提供します。
インターフェースはコマンドラインとメソッドとして呼び出し可能なものの両方を備えています。
また、このモジュールは実行時間の計測にあたり陥りがちな落し穴に対する様々な対策が取られています。詳しくは、 O'Reilly の
Python Cookbook、"Algorithms" の章にある Tim Peters が書いた解説を参照してください。


Basic Examples
--------------

The following example shows how the :ref:`command-line-interface`
can be used to compare three different expressions:

.. code-block:: sh

   $ python -m timeit '"-".join(str(n) for n in range(100))'
   10000 loops, best of 3: 40.3 usec per loop
   $ python -m timeit '"-".join([str(n) for n in range(100)])'
   10000 loops, best of 3: 33.4 usec per loop
   $ python -m timeit '"-".join(map(str, range(100)))'
   10000 loops, best of 3: 25.2 usec per loop

This can be achieved from the :ref:`python-interface` with::

   >>> import timeit
   >>> timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
   0.8187260627746582
   >>> timeit.timeit('"-".join([str(n) for n in range(100)])', number=10000)
   0.7288308143615723
   >>> timeit.timeit('"-".join(map(str, range(100)))', number=10000)
   0.5858950614929199

Note however that :mod:`timeit` will automatically determine the number of
repetitions only when the command-line interface is used.  In the
:ref:`timeit-examples` section you can find more advanced examples.


.. _python-interface:

Python Interface
----------------

The module defines three convenience functions and a public class:


.. function:: timeit(stmt='pass', setup='pass', timer=<default timer>, number=1000000)

   .. Create a :class:`Timer` instance with the given statement, setup code and timer
      function and run its :meth:`timeit` method with *number* executions.

   指定された *stmt*, *setup*, *timer* を使って :class:`Timer` インスタンスを作成し、
   指定された *number* を使ってその :meth:`timeit` メソッドを実行します。

   .. versionadded:: 2.6


.. function:: repeat(stmt='pass', setup='pass', timer=<default timer>, repeat=3, number=1000000)

   .. Create a :class:`Timer` instance with the given statement, setup code and timer
      function and run its :meth:`repeat` method with the given repeat count and
      *number* executions.

   指定された *stmt*, *setup*, *timer* を使って :class:`Timer` インスタンスを作成し、
   指定された *repeat*, *number* を使ってその :meth:`repeat` メソッドを実行します。

   .. versionadded:: 2.6


.. function:: default_timer()

   Define a default timer, in a platform-specific manner.  On Windows,
   :func:`time.clock` has microsecond granularity, but :func:`time.time`'s
   granularity is 1/60th of a second.  On Unix, :func:`time.clock` has 1/100th of
   a second granularity, and :func:`time.time` is much more precise.  On either
   platform, :func:`default_timer` measures wall clock time, not the CPU
   time.  This means that other processes running on the same computer may
   interfere with the timing.


.. class:: Timer(stmt='pass', setup='pass', timer=<timer function>)

   小さなコード断片の実行時間計測をおこなうためのクラスです。

   コンストラクタは引数として、時間計測の対象となる文、セットアップに使用する追加の文、タイマ関数を受け取ります。文のデフォルト値は両方とも
   ``'pass'`` で、タイマ関数はプラットフォーム依存(モジュールの doc string を参照)です。
   *stmt* と *setup* は複数行の文字列リテラルを含まない限り、改行や ``;`` で区切られた複数の文を入れることができます。

   最初の文の実行時間を計測には :meth:`timeit` メソッドを使用します。また :meth:`timeit` を複数回呼び出し、その結果のリストを返す
   :meth:`repeat` メソッドも用意されています。

   .. .. versionchanged:: 2.6
      The *stmt* and *setup* parameters can now also take objects that are callable
      without arguments. This will embed calls to them in a timer function that will
      then be executed by :meth:`timeit`.  Note that the timing overhead is a little
      larger in this case because of the extra function calls.

   .. versionchanged:: 2.6
      *stmt* と *setup* 引数は、引数なしの呼び出し可能オブジェクトも
      受け取れるようになりました。
      オブジェクトを与えると、そのオブジェクトへの呼び出しがタイマー関数に
      埋め込まれ、そしてその関数が :meth:`timeit` によって実行されます。
      この場合、関数呼び出しが増えるために、オーバーヘッドが少し増えることに注意してください。


   .. method:: Timer.timeit(number=1000000)

      メイン文の実行時間を *number* 回取得します。このメソッドはセットアップ文を1回だけ実行し、メイン文を指定回数実行するのにかかった秒数を浮動小数で返します。
      引数はループを何回実行するかの指定で、デフォルト値は 100万回です。メイン文、セットアップ文、タイマ関数はコンストラクタで指定されたものを使用します。

      .. note::

         デフォルトでは、 :meth:`timeit` は時間計測中、一時的にガーベッジコレクション(:term:`garbage collection`)を切ります。
         このアプローチの利点は、個別の測定結果を比較しやすくなることです。不利な点は、GC が測定している関数のパフォーマンスの重要な一部かもしれないということです。
         そうした場合、 *setup* 文字列の最初の文で GC を再度有効にすることができます。例えば ::

            timeit.Timer('for i in xrange(10): oct(i)', 'gc.enable()').timeit()


   .. method:: Timer.repeat(repeat=3, number=1000000)

      :meth:`timeit` を複数回呼び出します。

      このメソッドは :meth:`timeit` を複数回呼び出し、その結果をリストで返すユーティリティ関数です。最初の引数には :meth:`timeit`
      を呼び出す回数を指定します。2番目の引数は :meth:`timeit` へ引数として渡す *number* です。

      .. note::

         結果のベクトルから平均値や標準偏差を計算して出力させたいと思うかもしれませんが、それはあまり意味がありません。
         多くの場合、最も低い値がそのマシンが与えられたコード断片を実行する場合の下限値です。
         結果のうち高めの値は、Python のスピードが一定しないために生じたものではなく、時刻取得の際他のプロセスと衝突がおこったため、
         正確さが損なわれた結果生じたものです。したがって、結果のうち :func:`min` だけが見るべき値となるでしょう。
         この点を押さえた上で、統計的な分析よりも常識的な判断で結果を見るようにしてください。


   .. method:: Timer.print_exc(file=None)

      計測対象コードのトレースバックを出力するためのヘルパー。

      利用例::

         t = Timer(...)       # try/except の外側で
         try:
             t.timeit(...)    # または t.repeat(...)
         except:
             t.print_exc()

      標準のトレースバックより優れた点は、コンパイルしたテンプレートのソース行が表示されることです。オプションの引数 *file* にはトレースバック
      の出力先を指定します。デフォルトは ``sys.stderr`` になっています。


.. _command-line-interface:

コマンドライン・インターフェース
--------------------------------

コマンドラインからプログラムとして呼び出す場合は、次の書式を使います。 ::

   python -m timeit [-n N] [-r N] [-s S] [-t] [-c] [-h] [statement ...]

以下のオプションが使用できます。

.. program:: timeit

.. cmdoption:: -n N, --number=N

   'statement' を何回実行するか

.. cmdoption:: -r N, --repeat=N

   タイマを何回リピートするか(デフォルトは 3)

.. cmdoption:: -s S, --setup=S

   最初に1回だけ実行する文 (デフォルトは ``pass``)

.. cmdoption:: -t, --time

   :func:`time.time` を使用する (Windows を除くすべてのプラットフォームのデフォルト)

.. cmdoption:: -c, --clock

   :func:`time.clock` を使用する(Windows のデフォルト)

.. cmdoption:: -v, --verbose

   時間計測の結果をそのまま詳細な数値でくり返し表示する

.. cmdoption:: -h, --help

   簡単な使い方を表示して終了する

文は複数行指定することもできます。
その場合、各行は独立した文として引数に指定されたものとして処理します。
クォートと行頭のスペースを使って、インデントした文を使うことも可能です。
この複数行のオプションは  :option:`-s` においても同じ形式で指定可能です。

オプション :option:`-n` でループの回数が指定されていない場合、10回から始めて、
所要時間が 0.2 秒になるまで回数を増やすことで適切なループ回数が\
自動計算されるようになっています。

:func:`default_timer` measurations can be affected by other programs running on
the same machine, so
the best thing to do when accurate timing is necessary is to repeat
the timing a few times and use the best time.  The :option:`-r` option is good
for this; the default of 3 repetitions is probably enough in most cases.  On
Unix, you can use :func:`time.clock` to measure CPU time.

.. note::

   pass 文の実行による基本的なオーバーヘッドが存在することに注意してください。ここにあるコードはこの事実を隠そうとはしておらず、注意を払う
   必要があります。基本的なオーバーヘッドは引数なしでプログラムを起動することにより計測できます。
   基本的なオーバヘッドは Python のバージョンによって異なります。
   Python 2.3 とそれ以前の Python の公平な比較をおこなう場合、
   古い方の Python は  :option:`-O` オプションで起動し
   ``SET_LINENO`` 命令の実行時間が含まれないようにする必要があります。


.. _timeit-examples:

使用例
------

It is possible to provide a setup statement that is executed only once at the beginning:

.. code-block:: sh

   $ python -m timeit -s 'text = "sample string"; char = "g"'  'char in text'
   10000000 loops, best of 3: 0.0877 usec per loop
   $ python -m timeit -s 'text = "sample string"; char = "g"'  'text.find(char)'
   1000000 loops, best of 3: 0.342 usec per loop

::

   >>> import timeit
   >>> timeit.timeit('char in text', setup='text = "sample string"; char = "g"')
   0.41440500499993504
   >>> timeit.timeit('text.find(char)', setup='text = "sample string"; char = "g"')
   1.7246671520006203

The same can be done using the :class:`Timer` class and its methods::

   >>> import timeit
   >>> t = timeit.Timer('char in text', setup='text = "sample string"; char = "g"')
   >>> t.timeit()
   0.3955516149999312
   >>> t.repeat()
   [0.40193588800002544, 0.3960157959998014, 0.39594301399984033]


The following examples show how to time expressions that contain multiple lines.
Here we compare the cost of using :func:`hasattr` vs. :keyword:`try`/:keyword:`except`
to test for missing and present object attributes:

.. code-block:: sh

   $ python -m timeit 'try:' '  str.__nonzero__' 'except AttributeError:' '  pass'
   100000 loops, best of 3: 15.7 usec per loop
   $ python -m timeit 'if hasattr(str, "__nonzero__"): pass'
   100000 loops, best of 3: 4.26 usec per loop

   $ python -m timeit 'try:' '  int.__nonzero__' 'except AttributeError:' '  pass'
   1000000 loops, best of 3: 1.43 usec per loop
   $ python -m timeit 'if hasattr(int, "__nonzero__"): pass'
   100000 loops, best of 3: 2.23 usec per loop

::

   >>> import timeit
   >>> # attribute is missing
   >>> s = """\
   ... try:
   ...     str.__nonzero__
   ... except AttributeError:
   ...     pass
   ... """
   >>> timeit.timeit(stmt=s, number=100000)
   0.9138244460009446
   >>> s = "if hasattr(str, '__bool__'): pass"
   >>> timeit.timeit(stmt=s, number=100000)
   0.5829014980008651
   >>>
   >>> # attribute is present
   >>> s = """\
   ... try:
   ...     int.__nonzero__
   ... except AttributeError:
   ...     pass
   ... """
   >>> timeit.timeit(stmt=s, number=100000)
   0.04215312199994514
   >>> s = "if hasattr(int, '__bool__'): pass"
   >>> timeit.timeit(stmt=s, number=100000)
   0.08588060699912603

定義した関数に :mod:`timeit` モジュールがアクセスできるようにするために、
import 文の入った ``setup`` 引数を渡すことができます::

   def test():
       """Stupid test function"""
       L = []
       for i in range(100):
           L.append(i)

   if __name__ == '__main__':
       import timeit
       print(timeit.timeit("test()", setup="from __main__ import test"))
