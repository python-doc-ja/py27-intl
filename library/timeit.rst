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


基本的な例
--------------

次の例は、3つの異なる式を比較するために :ref:`command-line-interface` を
使う方法を示します:

.. code-block:: sh

   $ python -m timeit '"-".join(str(n) for n in range(100))'
   10000 loops, best of 3: 40.3 usec per loop
   $ python -m timeit '"-".join([str(n) for n in range(100)])'
   10000 loops, best of 3: 33.4 usec per loop
   $ python -m timeit '"-".join(map(str, range(100)))'
   10000 loops, best of 3: 25.2 usec per loop

これは、次のように :ref:`python-interface` を使って達成することができます::

   >>> import timeit
   >>> timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
   0.8187260627746582
   >>> timeit.timeit('"-".join([str(n) for n in range(100)])', number=10000)
   0.7288308143615723
   >>> timeit.timeit('"-".join(map(str, range(100)))', number=10000)
   0.5858950614929199

ただし、 :mod:`timeit` が自動的に反復の回数を決定するのはコマンドライン
インターフェースを使った時だけということに注意してください。
:ref:`timeit-examples` の節にはより高度な例があります。


.. _python-interface:

Python インターフェース
-----------------------

このモジュールには3つの便利関数と1つの公開クラスが定義されています。


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

   プラットフォーム依存の方法でデフォルトのタイマを定義します。
   Windows の場合、 :func:`time.clock` はマイクロ秒の精度がありますが、
   :func:`time.time` は 1/60 秒の精度しかありません。
   一方 Unixの場合、 :func:`time.clock` でも 1/100 秒の精度があり、
   :func:`time.time` はもっと正確です。いずれのプラットフォームにおいても、
   デフォルトのタイマ関数は CPU 時間ではなく通常の時間 (wall clock time) を返します。
   つまり、同じコンピュータ上で別のプロセスが動いている場合、
   測定に干渉する可能性があるということです。


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

      メイン文を *number* 回実行した時間を計測します。このメソッドはセットアップ文を1回だけ実行し、メイン文を指定回数実行するのにかかった秒数を浮動小数で返します。
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
所要時間が 0.2 秒になるまで回数を増やすことで適切なループ回数が
自動計算されるようになっています。

:func:`default_timer` の結果は同じコンピュータ上で動作している別の
プロセスに影響を受けることがあります。そのため、正確な時間を計測する必要が
ある場合に最善の方法は、時間の取得を数回くり返してその中の最短の時間を
採用することです。 :option:`-r` オプションはこれをおこなうもので、
デフォルトのくり返し回数は3回になっています。多くの場合はデフォルトのままで
充分でしょう。 Unix の場合 :func:`time.clock` を使って CPU 時間で測定
することもできます。

.. note::

   pass 文の実行による基本的なオーバーヘッドが存在することに注意してください。
   ここにあるコードはこの事実を隠そうとはしていませんが、注意する必要があります。
   基本的なオーバーヘッドは引数なしでプログラムを起動することにより計測でき、
   それは Python のバージョンによって異なるでしょう。
   Python 2.3 とそれ以前の Python の公平な比較をおこなう場合、
   古い Python では :option:`-O` オプションを付けて起動して
   ``SET_LINENO`` 命令の実行時間が含まれないようにする必要があります。


.. _timeit-examples:

使用例
------

最初に一回だけ実行されるセットアップ文を提供することが可能です:

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

同じことは :class:`Timer` クラスとそのメソッドを使用して行うこともできます::

   >>> import timeit
   >>> t = timeit.Timer('char in text', setup='text = "sample string"; char = "g"')
   >>> t.timeit()
   0.3955516149999312
   >>> t.repeat()
   [0.40193588800002544, 0.3960157959998014, 0.39594301399984033]


以下の例は、複数行を含んだ式を計測する方法を示しています。
ここでは、オブジェクトの存在する属性と存在しない属性に対してテストするために
:func:`hasattr` と :keyword:`try`/:keyword:`except` を使用した場合のコストを
比較しています:

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
