
:mod:`itertools` --- 効率的なループ実行のためのイテレータ生成関数
=================================================================

.. module:: itertools
   :synopsis: 効率的なループ実行のためのイテレータ生成関数。
.. moduleauthor:: Raymond Hettinger <python@rcn.com>
.. sectionauthor:: Raymond Hettinger <python@rcn.com>


.. versionadded:: 2.3

このモジュールではイテレータを構築する部品を実装しています。プログラム言
語HaskellとSMLからアイデアを得ていますが、Pythonに適した形に修正されてい ます。

このモジュールは、高速でメモリ効率に優れ、単独でも組み合わせても使用する ことのできるツールを標準化したものです。標準化により、多数の個人が、それ
ぞれの好みと命名規約で、それぞれ少しだけ異なる実装を行う為に発生する可読 性と信頼性の問題を軽減する事ができます。

ここで定義したツールは簡単に組み合わせて使用することができるようになって おり、アプリケーション固有のツールを簡潔かつ効率的に作成する事ができます。

例えば、SMLの作表ツール``tabulate(f)``は``f(0), f(1), ...``のシー
ケンスを作成します。このツールボックスでは:func:`imap`と :func:`count`を用意しており、この二つを組み合わせて ``imap(f,
count())``とすれば同じ結果を得る事ができます。

同様に、:mod:`operator`モジュールの高速な関数とも一緒に使用すること ができるようになっています。

他にこのモジュールに追加したい基本的な構築部品があれば、開発者に提案して ください。

イテレータを使用すると、Python で書いてもコンパイル言語で書いても リストを使用した同じ処理よりメモリ効率がよく、高速になります。
これはデータをメモリ上に "在庫"しておくのではなく、 必要に応じて作成する注文生産方式を採用しているためです。

イテレータによるパフォーマンス上のメリットは、要素の数が増えるにつれてよ り明確になります。一定以上の要素を持つリストでは、メモリキャッシュのパフ
ォーマンスに対する影響が大きく、実行速度が低下します。


.. seealso::

   The Standard ML Basis Library, `The Standard ML Basis Library
   <http://www.standardml.org/Basis/>`_.

   Haskell, A Purely Functional Language, `Definition of Haskell and the Standard
   Libraries <http://www.haskell.org/definition/>`_.


.. _itertools-functions:

Itertool関数
------------

以下の関数は全て、イテレータを作成して返します。無限長のストリームのイテ レータを返す関数もあり、この場合にはストリームを中断するような関数かルー
プ処理から使用しなければなりません。


.. function:: chain(*iterables)

   先頭のiterableの全要素を返し、次に2番目のiterableの全要素…と全 iterableの要素を返すイテレータを作成します。連続したシーケンスを、一つ
   のシーケンスとして扱う場合に使用します。この関数は以下のスクリプトと同 等です： ::

      def chain(*iterables):
          for it in iterables:
              for element in it:
                  yield element


.. function:: count([n])

   *n*で始まる、連続した整数を返すイテレータを作成します。*n* を 指定しなかった場合、デフォルト値はゼロです。現在、
   Pythonの長整数はサポートしていません。:func:`imap`で連続したデー タを生成する場合や:func:`izip`でシーケンスに番号を追加する場合な
   どに引数として使用することができます。この関数は以下のスクリプトと同等 です： ::

      def count(n=0):
          while True:
              yield n
              n += 1

   :func:`count`はオーバーフローのチェックを行いません。このため、 ``sys.maxint``を超えると負の値を返します。この動作は将来変更されま
   す。


.. function:: cycle(iterable)

   iterableから要素を取得し、同時にそのコピーを保存するイテレータを作成し ます。iterableの全要素を返すと、セーブされたコピーから要素を返し、これ
   を無限に繰り返します。この関数は以下のスクリプトと同等です： ::

      def cycle(iterable):
          saved = []
          for element in iterable:
              yield element
              saved.append(element)
          while saved:
              for element in saved:
                    yield element

   :func:`cycle`は大きなメモリ領域を使用し ます。使用するメモリ量はiterableの大きさに依存します。


.. function:: dropwhile(predicate, iterable)

   predicateが真である限りは要素を無視し、その後は全ての要素を返すイテ レータを作成します。このイテレータは、predicateが真の間は*全く*要
   素を返さないため、最初の要素を返すまでに長い時間がかかる場合がありま す。この関数は以下のスクリプトと同等です： ::

      def dropwhile(predicate, iterable):
          iterable = iter(iterable)
          for x in iterable:
              if not predicate(x):
                  yield x
                  break
          for x in iterable:
              yield x


.. function:: groupby(iterable[, key])

   同じキーをもつような要素からなる*iterable* 中のグループに対して、 キーとグループを返すようなイテレータを作成します。 *key*
   は各要素に対するキー値を計算する関数です。キーを指定しない 場合や ``None`` にした場合、*key* 関数のデフォルトは恒等関数になり
   要素をそのまま返します。通常、*iterable* は 同じキー関数で並べ替え済みである必要があります。

   返されるグループはそれ自体がイテレータで、:func:`groupby` と *iterable* を共有しています。もととなる*iterable* を
   共有しているため、:func:`groupby` オブジェクトの要素取り出しを 先に進めると、それ以前の要素であるグループは見えなくなってしまいます。
   従って、データが後で必要な場合にはリストの形で保存しておく必要があります::

      groups = []
      uniquekeys = []
      for k, g in groupby(data, keyfunc):
          groups.append(list(g))      # Store group iterator as a list
          uniquekeys.append(k)

   :func:`groupby` は以下のコードと等価です::

      class groupby(object):
          def __init__(self, iterable, key=None):
              if key is None:
                  key = lambda x: x
              self.keyfunc = key
              self.it = iter(iterable)
              self.tgtkey = self.currkey = self.currvalue = xrange(0)
          def __iter__(self):
              return self
          def next(self):
              while self.currkey == self.tgtkey:
                  self.currvalue = self.it.next() # Exit on StopIteration
                  self.currkey = self.keyfunc(self.currvalue)
              self.tgtkey = self.currkey
              return (self.currkey, self._grouper(self.tgtkey))
          def _grouper(self, tgtkey):
              while self.currkey == tgtkey:
                  yield self.currvalue
                  self.currvalue = self.it.next() # Exit on StopIteration
                  self.currkey = self.keyfunc(self.currvalue)

   .. versionadded:: 2.4


.. function:: ifilter(predicate, iterable)

   predicateが``True``となる要素だけを返すイテレータを作成します。
   *predicate*が``None``の場合、値が真であるアイテムだけを返しま す。この関数は以下のスクリプトと同等です： ::

      def ifilter(predicate, iterable):
          if predicate is None:
              predicate = bool
          for x in iterable:
              if predicate(x):
                  yield x


.. function:: ifilterfalse(predicate, iterable)

   predicateが``False``となる要素だけを返すイテレータを作成します。
   *predicate*が``None``の場合、値が偽であるアイテムだけを返しま す。この関数は以下のスクリプトと同等です： ::

      def ifilterfalse(predicate, iterable):
          if predicate is None:
              predicate = bool
          for x in iterable:
              if not predicate(x):
                  yield x


.. function:: imap(function, *iterables)

   iterablesの要素を引数としてfuntionを呼び出すイテレータを作成します。 *function*が``None``の場合、引数のタプルを返します。
   :func:`map`と似ていますが、最短のiterableの末尾まで到達した後は ``None``を補って処理を続行するのではなく、終了します。これは、
   :func:`map`に無限長のイテレータを指定するのは多くの場合誤りですが (全出力が評価されてしまうため)、:func:`imap`の場合には一般的で役
   に立つ方法であるためです。この関数は以下のスクリプトと同等です： ::

      def imap(function, *iterables):
          iterables = map(iter, iterables)
          while True:
              args = [i.next() for i in iterables]
              if function is None:
                  yield tuple(args)
              else:
                  yield function(*args)


.. function:: islice(iterable, [start,] stop [, step])

   iterableから要素を選択して返すイテレータを作成します。*start*が0以
   外であれば、iterableの先頭要素はstartに達するまでスキップします。以 降、*step*が1以下なら連続した要素を返し、1以上なら指定された値分の
   要素をスキップします。*stop*が``None``であれば、無限に、もしく はiterableの全要素を返すまで値を返します。``None``以外ならイテレー
   タは指定された要素位置で停止します。通常のスライスと異なり、 *start*、*stop*、*step*に負の値を指定する事はできません。
   シーケンス化されたデータから関連するデータを取得する場合（複数行からなるレ ポートで、三行ごとに名前が指定されている場合など）に使用します。この関
   数は以下のスクリプトと同等です：  ::

      def islice(iterable, *args):
          s = slice(*args)
          it = iter(xrange(s.start or 0, s.stop or sys.maxint, s.step or 1))
          nexti = it.next()
          for i, element in enumerate(iterable):
              if i == nexti:
                  yield element
                  nexti = it.next()          

   *start*が``None``ならば、繰返しは0から始まります。 *step*が``None``ならば、ステップは1となります。

   .. versionchanged:: 2.5
      *start*と*step*はデフォルト値として ``None``を受け付けます。.


.. function:: izip(*iterables)

   各iterableの要素をまとめるイテレータを作成します。:func:`zip`に似 ていますが、リストではなくイテレータを返します。複数のイテレート可能オ
   ブジェクトに対して、同じ繰り返し処理を同時に行う場合に使用します。この 関数は以下のスクリプトと同等です： ::

      def izip(*iterables):
          iterables = map(iter, iterables)
          while iterables:
              result = [it.next() for it in iterables]
              yield tuple(result)

   .. versionchanged:: 2.4
      イテレート可能オブジェクトを指定しない場合、 :exc:`TypeError`例外を送出する代わりに長さゼロのイテレータを返し ます。.

   イテレート可能オブジェクトの左から右への評価順序は保証されることに注意 して下さい。このことによって、データ列を長さnのグループにまとめる常套 句
   ``izip(*[iter(s)]*n)`` が実現可能になります。長さnのグループにま とめるのに中途半端なデータ列に対しては
   ``izip(*[chain(s, [None]*(n-1))]*n)`` のように、最後のタプルを埋める値をあらかじめ準備し ておくことができます。

   もう一つの注意は :func:`izip` が長さが不揃いの入力に対して呼ばれた 時、:func:`izip` 終了の後引き続いて長い方のイテレート可能オブジェ
   クトを呼び出した結果は保証の限りではないということです。可能性として、 残ったそれぞれのイテレート可能オブジェクトから値が一つ失われているかも
   しれないし失われていないかもしれません。これは次のようにして起こります。 実行中にそれぞれのイテレート可能オブジェクトから一つずつ値を取り出しま
   すが、その処理がいずれかのイテレート可能オブジェクトが空になることによ り終了します。この時途中まで取り出された値たちは宙に浮きます(不完全なタ
   プルとして送り出されることもなく、また次の ``it.next()`` のためにイ テレート可能オブジェクトに押し戻すこともできません)。一般に、
   :func:`izip` を長さが不揃いな入力に使うのは、残され使われなかった 長い方のイテレート可能オブジェクトの値を気にしない時だけにするべきです。


.. function:: repeat(object[, times])

   繰り返し*object*を返すイテレータを作成します。*times*を指定し ない場合、無限に値を返し続けます。:func:`imap`で常に同じオブジェク
   トを関数の引数として指定する場合に使用します。また、:func:`izip` で作成するタプルの全要素に常に同じオブジェクトを指定する場合にも使用す
   ることもできます。この関数は以下のスクリプトと同等です： ::

      def repeat(object, times=None):
          if times is None:
              while True:
                  yield object
          else:
              for i in xrange(times):
                  yield object


.. function:: starmap(function, iterable)

   iterablesの要素を引数としてfuntionを呼び出すイテレータを作成します。
   functionの引数が単一のiterableにタプルとして格納されている場合("zip済
   み")、:func:`imap`の代わりに使用します。:func:`imap`と :func:`starmap`ではfunctionの呼び出し方法が異なり、
   :func:`imap`は``function(a,b)``、:func:`starmap`では
   ``function(*c)``のように呼び出します。この関数は以下のスクリプトと 同等です： ::

      def starmap(function, iterable):
          iterable = iter(iterable)
          while True:
              yield function(*iterable.next())


.. function:: takewhile(predicate, iterable)

   predicateが真である限りiterableから要素を返すイテレータを作成します。 この関数は以下のスクリプトと同等です： ::

      def takewhile(predicate, iterable):
          for x in iterable:
              x = iterable.next()
              if predicate(x):
                  yield x
              else:
                  break


.. function:: tee(iterable[, n=2])

   一つの*iterable* から*n* 個の独立したイテレータを生成して 返します。``n==2`` の場合は、以下のコードと等価になります::

      def tee(iterable):
          def gen(next, data={}, cnt=[0]):
              for i in count():
                  if i == cnt[0]:
                      item = data[i] = next()
                      cnt[0] += 1
                  else:
                      item = data.pop(i)
                  yield item
          it = iter(iterable)
          return (gen(it.next), gen(it.next))

   一度:func:`tee` でイテレータを分割すると、もとの *iterable* を他で使ってはならなくなるので注意してください; さもなければ、
   :func:`tee` オブジェクトの知らない間に*iterable* が先の要素に 進んでしまうことになります。

   :func:`tee`はかなり大きなメモリ領域を使用します (使用するメモリ量はiterableの大きさに依存します)。
   一般には、一つのイテレータが他のイテレータよりも先に ほとんどまたは全ての要素を消費するような場合には、:func:`tee` よりも:func:`list`
   を使った方が高速です。

   .. versionadded:: 2.4


.. _itertools-example:

例
--

以下に各ツールの一般的な使い方と、ツールの組み合わせの例を示します。 ::

   >>> amounts = [120.15, 764.05, 823.14]
   >>> for checknum, amount in izip(count(1200), amounts):
   ...     print 'Check %d is for $%.2f' % (checknum, amount)
   ...
   Check 1200 is for $120.15
   Check 1201 is for $764.05
   Check 1202 is for $823.14

   >>> import operator
   >>> for cube in imap(operator.pow, xrange(1,5), repeat(3)):
   ...    print cube
   ...
   1
   8
   27
   64

   >>> reportlines = ['EuroPython', 'Roster', '', 'alex', '', 'laura',
                     '', 'martin', '', 'walter', '', 'mark']
   >>> for name in islice(reportlines, 3, None, 2):
   ...    print name.title()
   ...
   Alex
   Laura
   Martin
   Walter
   Mark

   # Show a dictionary sorted and grouped by value
   >>> from operator import itemgetter
   >>> d = dict(a=1, b=2, c=1, d=2, e=1, f=2, g=3)
   >>> di = sorted(d.iteritems(), key=itemgetter(1))
   >>> for k, g in groupby(di, key=itemgetter(1)):
   ...     print k, map(itemgetter(0), g)
   ...
   1 ['a', 'c', 'e']
   2 ['b', 'd', 'f']
   3 ['g']

   # Find runs of consecutive numbers using groupby.  The key to the solution
   # is differencing with a range so that consecutive numbers all appear in
   # same group.
   >>> data = [ 1,  4,5,6, 10, 15,16,17,18, 22, 25,26,27,28]
   >>> for k, g in groupby(enumerate(data), lambda (i,x):i-x):
   ...     print map(operator.itemgetter(1), g)
   ... 
   [1]
   [4, 5, 6]
   [10]
   [15, 16, 17, 18]
   [22]
   [25, 26, 27, 28]


.. % $ bow here


.. _itertools-recipes:

レシピ
------

この節では、既存の itertools をビルディングブロックとしてツールセットを 拡張するためのレシピを示します。

iterable 全体を一度にメモリ上に置くよりも、要素を一つづつ処理する方が メモリ効率上の有利さを保てます。関数形式のままツールをリンクしてゆくと、
コードのサイズを減らし、一時変数を減らす助けになります。 インタプリタのオーバヘッドをもたらす for ループやジェネレータを使わずに、 "ベクトル化された"
ビルディングブロックを使うと、高速な処理を実現 できます。 ::

   def take(n, seq):
       return list(islice(seq, n))

   def enumerate(iterable):
       return izip(count(), iterable)

   def tabulate(function):
       "Return function(0), function(1), ..."
       return imap(function, count())

   def iteritems(mapping):
       return izip(mapping.iterkeys(), mapping.itervalues())

   def nth(iterable, n):
       "Returns the nth item"
       return list(islice(iterable, n, n+1))

   def all(seq, pred=None):
       "Returns True if pred(x) is true for every element in the iterable"
       for elem in ifilterfalse(pred, seq):
           return False
       return True

   def any(seq, pred=None):
       "Returns True if pred(x) is true for at least one element in the iterable"
       for elem in ifilter(pred, seq):
           return True
       return False

   def no(seq, pred=None):
       "Returns True if pred(x) is false for every element in the iterable"
       return True not in imap(pred, seq)

   def quantify(seq, pred=None):
       "Count how many times the predicate is true in the sequence"
       return sum(imap(pred, seq))

   def padnone(seq):
       """Returns the sequence elements and then returns None indefinitely.

       Useful for emulating the behavior of the built-in map() function.
       """
       return chain(seq, repeat(None))

   def ncycles(seq, n):
       "Returns the sequence elements n times"
       return chain(*repeat(seq, n))

   def dotproduct(vec1, vec2):
       return sum(imap(operator.mul, vec1, vec2))

   def flatten(listOfLists):
       return list(chain(*listOfLists))

   def repeatfunc(func, times=None, *args):
       """Repeat calls to func with specified arguments.

       Example:  repeatfunc(random.random)
       """
       if times is None:
           return starmap(func, repeat(args))
       else:
           return starmap(func, repeat(args, times))

   def pairwise(iterable):
       "s -> (s0,s1), (s1,s2), (s2, s3), ..."
       a, b = tee(iterable)
       try:
           b.next()
       except StopIteration:
           pass
       return izip(a, b)

   def grouper(n, iterable, padvalue=None):
       "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
       return izip(*[chain(iterable, repeat(padvalue, n-1))]*n)



