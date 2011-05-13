:mod:`collections` --- 高性能なコンテナ・データ型
=================================================

.. module:: collections
   :synopsis: High-performance container datatypes
.. moduleauthor:: Raymond Hettinger <python@rcn.com>
.. sectionauthor:: Raymond Hettinger <python@rcn.com>

.. versionadded:: 2.4

.. testsetup:: *

   from collections import *
   import itertools
   __name__ = '<doctest>'

このモジュールでは高性能なコンテナ・データ型を実装しています。現在のところ、
:class:`deque` と :class:`defaultdict` という２つのデータ型と、
:func:`namedtuple` というデータ型ファクトリ関数があります。


.. versionchanged:: 2.5
   :class:`defaultdict` の追加.

.. versionchanged:: 2.6
   :func:`namedtuple` の追加.

このモジュールが提供する特殊なコンテナは、 Python の汎用的なコンテナ、
:class:`dict`, :class:`list`, :class:`set`, :class:`tuple` の代わりに
なります。

ここで提供されるコンテナと別に、オプションとして :mod:`bsddb` モジュールが
in-memory もしくは file を使った、文字列をキーとする順序付き辞書を、
:meth:`bsddb.btopen` メソッドで提供しています。

コンテナ型に加えて、 collections モジュールは幾つかの ABC (abstract base
classes = 抽象基底クラス) を提供しています。
ABC はクラスが特定のインタフェース(例えばhashable や mapping)を
持っているかどうかをテストするのに利用します。

.. versionchanged:: 2.6
   抽象基底クラス (abstract base class) の追加

ABCs - abstract base classes
----------------------------

collections モジュールは以下の ABC を提供します。

=========================  =====================  ======================  ====================================================
ABC                        継承しているクラス     Abstract Methods        Mixin Methods
=========================  =====================  ======================  ====================================================
:class:`Container`                                ``__contains__``
:class:`Hashable`                                 ``__hash__``
:class:`Iterable`                                 ``__iter__``
:class:`Iterator`          :class:`Iterable`      ``next``                ``__iter__``
:class:`Sized`                                    ``__len__``
:class:`Callable`                                 ``__call__``

:class:`Sequence`          :class:`Sized`,        ``__getitem__``         ``__contains__``. ``__iter__``, ``__reversed__``.
                           :class:`Iterable`,                             ``index``, ``count``
                           :class:`Container`

:class:`MutableSequnce`    :class:`Sequence`      ``__setitem__``         Sequence から継承したメソッドと、
                                                  ``__delitem__``,        ``append``, ``reverse``, ``extend``, ``pop``,
                                                  ``insert``,             ``remove``, ``__iadd__``

:class:`Set`               :class:`Sized`,                                ``__le__``, ``__lt__``, ``__eq__``, ``__ne__``,
                           :class:`Iterable`,                             ``__gt__``, ``__ge__``, ``__and__``, ``__or__``
                           :class:`Container`                             ``__sub__``, ``__xor__``, and ``isdisjoint``

:class:`MutableSet`        :class:`Set`           ``add``,                Set から継承したメソッドと、
                                                  ``discard``             ``clear``, ``pop``, ``remove``, ``__ior__``,
                                                                          ``__iand__``, ``__ixor__``, ``__isub__``

:class:`Mapping`           :class:`Sized`,        ``__getitem__``         ``__contains__``, ``keys``, ``items``, ``values``,
                           :class:`Iterable`,                             ``get``, ``__eq__``, ``__ne__``
                           :class:`Container`

:class:`MutableMapping`    :class:`Mapping`       ``__setitem__``         Mapping から継承したメソッドと、
                                                  ``__detitem__``,        ``pop``, ``popitem``, ``clear``, ``update``,
                                                                          ``setdefault``

:class:`MappingView`       :class:`Sized`                                 ``__len__``
:class:`KeysView`          :class:`MappingView`,                          ``__contains__``,
                           :class:`Set`                                   ``__iter__``
:class:`ItemsView`         :class:`MappingView`,                          ``__contains__``,
                           :class:`Set`                                   ``__iter__``
:class:`ValuesView`        :class:`MappingView`                           ``__contains__``, ``__iter__``
=========================  =====================  ======================  ====================================================

これらの ABC はクラスやインスタンスが特定の機能を提供しているかどうかを
テストするのに使えます。例えば::

    size = None
    if isinstance(myvar, collections.Sized):
       size = len(myvar)

幾つかの ABC はコンテナ型APIを提供するクラスを開発するのを助ける mixin型としても
使えます。例えば、 :class:`Set` API を提供するクラスを作る場合、3つの基本になる
抽象メソッド :meth:`__contains__`, :meth:`__iter__`, :meth:`__len__` だけが
必要です。 ABC が残りの :meth:`__and__` や :meth:`isdisjoint` といったメソッドを
提供します。 ::

    class ListBasedSet(collections.Set):
         ''' 速度よりもメモリ使用量を重視して、 hashable も提供しない
             set の別の実装 '''
         def __init__(self, iterable):
             self.elements = lst = []
             for value in iterable:
                 if value not in lst:
                     lst.append(value)
         def __iter__(self):
             return iter(self.elements)
         def __contains__(self, value):
             return value in self.elements
         def __len__(self):
             return len(self.elements)

    s1 = ListBasedSet('abcdef')
    s2 = ListBasedSet('defghi')
    overlap = s1 & s2            # __and__() は ABC により自動的に提供される

:class:`Set` と :class:`MutableSet` を mixin型として利用するときの注意点:

(1)
   幾つかの set の操作は新しい set を作るので、デフォルトの mixin メソッドは
   iterable から新しいインスタンスを作成する方法を必要とします。クラスの
   コンストラクタは ``ClassName(iterable)`` の形のシグネチャを持つと仮定されます。
   内部の :meth:`_from_iterable` というクラスメソッドが ``cls(iterable)``
   を呼び出して新しい set を作る部分でこの仮定が使われています。
   コンストラクタのシグネチャが異なるクラスで :class:`Set` を使う場合は、
   iterable 引数から新しいインスタンスを生成するように :meth:`_from_iterable`
   をオーバーライドする必要があります。

(2)
   (たぶん意味はそのままに速度を向上する目的で)比較をオーバーライドする場合、
   :meth:`__le__` だけを再定義すれば、その他の演算は自動的に追随します。

(3)
   :class:`Set` mixin型は set のハッシュ値を計算する :meth:`_hash` メソッドを
   提供しますが、すべての set が hashable や immutable とは限らないので、
   :meth:`__hash__` は提供しません。 mixin を使って hashable な set を作る場合は、
   :class:`Set` と :class:`Hashable` の両方を継承して、 ``__hash__ = Set._hash``
   と定義してください。

.. seealso::

   * :class:`MutableSet` を使った例として
     `OrderedSet recipe <http://code.activestate.com/recipes/576694/>`_

   * ABCs についての詳細は、 :mod:`abc` モジュールと :pep:`3119` を参照してください。


:class:`deque` オブジェクト
---------------------------

.. class:: deque([iterable[, maxlen]])

   *iterable* で与えられるデータから、新しい deque オブジェクトを (:meth:`append` をつかって)
   左から右に初期化して返します。
   *iterable* が指定されない場合、新しい deque オブジェクトは空になります。

   Deque とは、スタックとキューを一般化したものです (この名前は「デック」と発音され、これは「double-ended
   queue」の省略形です)。Deque はどちらの側からも append と pop が可能で、スレッドセーフでメモリ効率がよく、
   どちらの方向からもおよそ ``O(1)`` のパフォーマンスで実行できます。

   :class:`list` オブジェクトでも同様の操作を実現できますが、これは高速な固定長の
   操作に特化されており、内部のデータ表現形式のサイズと位置を両方変えるような
   ``pop(0)`` や ``insert(0, v)`` などの操作ではメモリ移動のために ``O(n)``
   のコストを必要とします。

   .. versionadded:: 2.4

   *maxlen* が指定され無かったり *None* だった場合、 deque は不定のサイズまで
   大きくなります。それ以外の場合、 deque は指定された最大長に制限されます。
   長さが制限された deque がいっぱいになると、新しい要素を追加するときに追加した
   要素数分だけ追加した逆側から要素が捨てられます。長さが制限された deque は Unix に
   おける ``tail`` フィルタと似た機能を提供します。トランザクションの tracking や
   最近使った要素だけを残したいデータプール (pool of data) などにも便利です。

   .. versionchanged:: 2.6
      *maxlen* パラメータを追加しました。

   Deque オブジェクトは以下のようなメソッドをサポートしています:


   .. method:: append(x)

      *x* を deque の右側につけ加えます。


   .. method:: appendleft(x)

      *x* を deque の左側につけ加えます。


   .. method:: clear()

      deque からすべての要素を削除し、長さを 0 にします。


   .. method:: extend(iterable)

      イテレータ化可能な引数 iterable から得られる要素を deque の右側に追加し拡張します。


   .. method:: extendleft(iterable)

      イテレータ化可能な引数 iterable から得られる要素を deque の左側に追加し拡張します。注意: 左から追加した結果は、イテレータ引数の
      順序とは逆になります。


   .. method:: pop()

      deque の右側から要素をひとつ削除し、その要素を返します。要素がひとつも存在しない場合は :exc:`IndexError` を発生させます。


   .. method:: popleft()

      deque の左側から要素をひとつ削除し、その要素を返します。要素がひとつも存在しない場合は :exc:`IndexError` を発生させます。


   .. method:: remove(value)

      最初に現れる value を削除します。要素がみつからないない場合は :exc:`ValueError` を発生させます。

      .. versionadded:: 2.5


   .. method:: rotate(n)

      deque の要素を全体で *n* ステップだけ右にローテートします。
      *n* が負の値の場合は、左にローテートします。Deque を
      ひとつ右にローテートすることは ``d.appendleft(d.pop())`` と同じです。

上記の操作のほかにも、deque は次のような操作をサポートしています: イテレータ化、pickle、 ``len(d)``, ``reversed(d)``,
``copy.copy(d)``, ``copy.deepcopy(d)``, :keyword:`in` 演算子による包含検査、そして ``d[-1]``
などの添え字による参照。
両端についてインデックスアクセスは O(1) ですが、中央部分については O(n) の遅さです。
高速なランダムアクセスが必要ならリストを使ってください。

例:

.. doctest::

   >>> from collections import deque
   >>> d = deque('ghi')                 # 3つの要素からなる新しい deque をつくる。
   >>> for elem in d:                   # deque の要素をひとつずつたどる。
   ...     print elem.upper()
   G
   H
   I

   >>> d.append('j')                    # 新しい要素を右側につけたす。
   >>> d.appendleft('f')                # 新しい要素を左側につけたす。
   >>> d                                # deque の表現形式。
   deque(['f', 'g', 'h', 'i', 'j'])

   >>> d.pop()                          # いちばん右側の要素を削除し返す。
   'j'
   >>> d.popleft()                      # いちばん左側の要素を削除し返す。
   'f'
   >>> list(d)                          # deque の内容をリストにする。
   ['g', 'h', 'i']
   >>> d[0]                             # いちばん左側の要素をのぞく。
   'g'
   >>> d[-1]                            # いちばん右側の要素をのぞく。
   'i'

   >>> list(reversed(d))                # deque の内容を逆順でリストにする。
   ['i', 'h', 'g']
   >>> 'h' in d                         # deque を検索。
   True
   >>> d.extend('jkl')                  # 複数の要素を一度に追加する。
   >>> d
   deque(['g', 'h', 'i', 'j', 'k', 'l'])
   >>> d.rotate(1)                      # 右ローテート
   >>> d
   deque(['l', 'g', 'h', 'i', 'j', 'k'])
   >>> d.rotate(-1)                     # 左ローテート
   >>> d
   deque(['g', 'h', 'i', 'j', 'k', 'l'])

   >>> deque(reversed(d))               # 新しい deque を逆順でつくる。
   deque(['l', 'k', 'j', 'i', 'h', 'g'])
   >>> d.clear()                        # deque を空にする。
   >>> d.pop()                          # 空の deque からは pop できない。
   Traceback (most recent call last):
     File "<pyshell#6>", line 1, in -toplevel-
       d.pop()
   IndexError: pop from an empty deque

   >>> d.extendleft('abc')              # extendleft() は入力を逆順にする。
   >>> d
   deque(['c', 'b', 'a'])


:class:`deque` のレシピ
------------------------

この節では deque をつかったさまざまなアプローチを紹介します。

長さが制限された deque は Unix における ``tail`` フィルタに相当する機能を
提供します::

   def tail(filename, n=10):
       'ファイルの最後の n 行を返す.'
       return deque(open(filename), n)

別のアプローチとして deque を右に append して左に pop して使うことで追加した要素を維持するのに使えます::

    def moving_average(iterable, n=3):
        # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
        # http://en.wikipedia.org/wiki/Moving_average
        it = iter(iterable)
        d = deque(itertools.islice(it, n-1))
        d.appendleft(0)
        s = sum(d)
        for elem in it:
            s += elem - d.popleft()
            d.append(elem)
            yield s / float(n)

:meth:`rotate` メソッドのおかげで、 :class:`deque` の一部を切り出したり削除したりできることになります。たとえば ``del
d[n]`` の純粋な Python 実装では pop したい要素まで :meth:`rotate` します ::

   def delete_nth(d, n):
       d.rotate(-n)
       d.popleft()
       d.rotate(n)

:class:`deque` の切り出しを実装するのにも、同様のアプローチを使います。まず対象となる要素を :meth:`rotate` によって deque
の左端までもってきてから、 :meth:`popleft` をつかって古い要素を消します。そして、 :meth:`extend`
で新しい要素を追加したのち、逆のローテートでもとに戻せばよいのです。
このアプローチをやや変えたものとして、Forth スタイルのスタック操作、つまり ``dup``, ``drop``, ``swap``, ``over``,
``pick``, ``rot``, および ``roll`` を実装するのも簡単です。


:class:`defaultdict` オブジェクト
---------------------------------

.. class:: defaultdict([default_factory[, ...]])

   新しいディクショナリ状のオブジェクトを返します。 :class:`defaultdict` は組込みの
   :class:`dict` のサブクラスです。メソッドをオーバーライドし、書き込み可能なインスタンス変数を1つ追加している以外は
   :class:`dict` クラスと同じです。同じ部分については以下では省略されています。

   1つめの引数は :attr:`default_factory` 属性の初期値です。デフォルトは
   ``None`` です。残りの引数はキーワード引数もふくめ、 :class:`dict` のコンストラクタにあたえられた場合と同様に扱われます。

   .. versionadded:: 2.5

   :class:`defaultdict` オブジェクトは標準の :class:`dict` に加えて、以下のメソッドを実装しています:


   .. method:: defaultdict.__missing__(key)

      もし :attr:`default_factory` 属性が ``None`` であれば、このメソッドは
      :exc:`KeyError` 例外を、 *key* を引数として発生させます。

      もし :attr:`default_factory` 属性が ``None`` でなければ、このメソッドは
      :attr:`default_factory` を引数なしで呼び出し、あたえられた *key* に対応するデフォルト値を作ります。そしてこの値を *key*
      に対応する値を辞書に登録して返ります。

      もし :attr:`default_factory` の呼出が例外を発生させた場合には、変更せずそのまま例外を投げます。

      このメソッドは :class:`dict` クラスの :meth:`__getitem__` メソッドで、キー
      が存在しなかった場合によびだされます。値を返すか例外を発生させるのどち
      らにしても、 :meth:`__getitem__` からもそのまま値が返るか例外が発生します。

   :class:`defaultdict` オブジェクトは以下のインスタンス変数をサポートしています:


   .. attribute:: defaultdict.default_factory

      この属性は :meth:`__missing__` メソッドによって使われます。
      これは存在すればコンストラクタの第1引数によって初期化され、そうでなければ
      ``None`` になります。


:class:`defaultdict` の使用例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`list` を :attr:`default_factory` とすることで、キー=値ペアのシーケンスをリストの辞書へ簡単にグループ化できます。:

   >>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
   >>> d = defaultdict(list)
   >>> for k, v in s:
   ...     d[k].append(v)
   ...
   >>> d.items()
   [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

それぞれのキーが最初に登場したとき、マッピングにはまだ存在しません。
そのためエントリは :attr:`default_factory` 関数が返す空の :class:`list` を使って自動的に作成されます。
:meth:`list.append` 操作は新しいリストに紐付けられます。キーが再度出現下場合には、通常の参照動作が行われます(そのキーに対応す
るリストが返ります)。そして :meth:`list.append` 操作で別の値をリスト
に追加します。このテクニックは :meth:`dict.setdefault` を使った等価なものよりシンプルで速いです:

   >>> d = {}
   >>> for k, v in s:
   ...     d.setdefault(k, []).append(v)
   ...
   >>> d.items()
   [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

:attr:`default_factory` を :class:`int` にすると、 :class:`defaultdict` を(他の言語の bag や
multisetのように)要素の数え上げに便利に使うことができます:

   >>> s = 'mississippi'
   >>> d = defaultdict(int)
   >>> for k in s:
   ...     d[k] += 1
   ...
   >>> d.items()
   [('i', 4), ('p', 2), ('s', 4), ('m', 1)]

最初に文字が出現したときは、マッピングが存在しないので :attr:`default_factory` 関数が :func:`int` を呼んでデフォルトのカ
ウント0を生成します。インクリメント操作が各文字を数え上げます。

常に0を返す :func:`int` は特殊な関数でした。定数を生成するより速くて柔軟な方法は、
0に限らず何でも定数を生成する :func:`itertools.repeat` を使うことです。

   >>> def constant_factory(value):
   ...     return itertools.repeat(value).next
   >>> d = defaultdict(constant_factory('<missing>'))
   >>> d.update(name='John', action='ran')
   >>> '%(name)s %(action)s to %(object)s' % d
   'John ran to <missing>'

:attr:`default_factory` を :class:`set` に設定することで、
:class:`defaultdict` をセットの辞書を作るために利用することができます:

   >>> s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
   >>> d = defaultdict(set)
   >>> for k, v in s:
   ...     d[k].add(v)
   ...
   >>> d.items()
   [('blue', set([2, 4])), ('red', set([1, 3]))]

:func:`namedtuple` 名前付きフィールドを持ったタプルのファクトリ関数
--------------------------------------------------------------------

名前付きタプルはタプルの中の場所に意味を割り当てて、より読みやすく自己解説的な
コードを書けるようにします。通常のタプルが利用されていた場所で利用でき、
場所に対するインデックスの代わりに名前を使ってフィールドにアクセスできます。

.. function:: namedtuple(typename, field_names, [verbose])

   *typename* という名前の tuple の新しいサブクラスを返します。新しいサブクラスは、
   tuple に似ているけれどもインデックスやイテレータだけでなく属性名によるアクセスも
   できるオブジェクトを作るのに使います。このサブクラスのインスタンスは、わかりやすい
   docstring (型名と属性名が入っています) や、 tuple の内容を ``name=value`` という
   形のリストで返す使いやすい :meth:`__repr__` も持っています。

   *field_names* は各属性名を空白文字 (whitespace) と/あるいはカンマ (,) で区切った
   文字列です。例えば、 ``'x y'`` か ``'x, y'`` です。代わりに *field_names* に
   ``['x', 'y']`` のような文字列のシーケンスを渡すこともできます。

   アンダースコア (_) で始まる名前を除いて、 Python の正しい識別子 (identifier)
   ならなんでも属性名として使うことができます。正しい識別子とはアルファベット(letters),
   数字(digits), アンダースコア(_) を含みますが、数字やアンダースコアで始まる名前や、
   *class*, *for*, *return*, *global*, *pass*, *print*, *raise* などといった
   :mod:`keyword` は使えません。

   *verbose* が真なら、クラスを作る直前にクラス定義が表示されます。

   名前付きタプルのインスタンスはインスタンスごとの辞書を持たないので、
   軽量で、普通のタプル以上のメモリを使用しません。

   .. versionadded:: 2.6

Example:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> Point = namedtuple('Point', 'x y')
   >>> p = Point(11, y=22)     # 順序による引数やキーワード引数を使ってインスタンス化
   >>> p[0] + p[1]             # 通常の tuple (11, 22) と同じようにインデックスアクセス
   33
   >>> x, y = p                # 通常の tuple と同じようにアンパック
   >>> x, y
   (11, 22)
   >>> p.x + p.y               # 名前でフィールドにアクセス
   33
   >>> p                       # name=value スタイルの読みやすい __repr__
   Point(x=11, y=22)

   >>> Point = namedtuple('Point', 'x y', verbose=True) # クラス定義を表示
   class Point(tuple):
           'Point(x, y)'
   <BLANKLINE>
           __slots__ = ()
   <BLANKLINE>
           _fields = ('x', 'y')
   <BLANKLINE>
           def __new__(_cls, x, y):
               return _tuple.__new__(cls, (x, y))
   <BLANKLINE>
           @classmethod
           def _make(cls, iterable, new=tuple.__new__, len=len):
               'Make a new Point object from a sequence or iterable'
               result = new(cls, iterable)
               if len(result) != 2:
                   raise TypeError('Expected 2 arguments, got %d' % len(result))
               return result
   <BLANKLINE>
           def __repr__(self):
               return 'Point(x=%r, y=%r)' % self
   <BLANKLINE>
           def _asdict(t):
               'Return a new dict which maps field names to their values'
               return {'x': t[0], 'y': t[1]}
   <BLANKLINE>
           def _replace(_self, **kwds):
               'Return a new Point object replacing specified fields with new values'
               result = _self._make(map(kwds.pop, ('x', 'y'), _self))
               if kwds:
                   raise ValueError('Got unexpected field names: %r' % kwds.keys())
               return result
   <BLANKLINE>
           def __getnewargs__(self):
               return tuple(self)
   <BLANKLINE>
           x = property(itemgetter(0))
           y = property(itemgetter(1))


名前付きタプルは :mod:`csv` や :mod:`sqlite3` モジュールが返すタプルのフィールドに名前を
付けるときにとても便利です::

   EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')

   import csv
   for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
       print emp.name, emp.title

   import sqlite3
   conn = sqlite3.connect('/companydata')
   cursor = conn.cursor()
   cursor.execute('SELECT name, age, title, department, paygrade FROM employees')
   for emp in map(EmployeeRecord._make, cursor.fetchall()):
       print emp.name, emp.title

タプルから継承したメソッドに加えて、名前付きタプルは3つの追加メソッドと
一つの属性をサポートしています。フィールド名との衝突を避けるために
メソッド名と属性名はアンダースコアで始まります。

.. classmethod:: somenamedtuple._make(iterable)

   既存の sequence や Iterable から新しいインスタンスを作るクラスメソッド.

   .. doctest::

      >>> t = [11, 22]
      >>> Point._make(t)
      Point(x=11, y=22)

.. method:: somenamedtuple._asdict()

   フィールド名とその値をもとに新しい辞書(dict)を作って返します::

      >>> p._asdict()
      {'x': 11, 'y': 22}

.. method:: somenamedtuple._replace(kwargs)

   指定されたフィールドを新しい値で置き換えた、新しい名前付きタプルを作って返します::

      >>> p = Point(x=11, y=22)
      >>> p._replace(x=33)
      Point(x=33, y=22)

      >>> for partnum, record in inventory.items():
      ...     inventory[partnum] = record._replace(price=newprices[partnum], timestamp=time.now())

.. attribute:: somenamedtuple._fields

   フィールド名をリストにしたタプル. 内省 (introspection) したり、既存の名前付きタプルを
   もとに新しい名前つきタプルを作成する時に便利です。

   .. doctest::

      >>> p._fields            # view the field names
      ('x', 'y')

      >>> Color = namedtuple('Color', 'red green blue')
      >>> Pixel = namedtuple('Pixel', Point._fields + Color._fields)
      >>> Pixel(11, 22, 128, 255, 0)
      Pixel(x=11, y=22, red=128, green=255, blue=0)

文字列に格納された名前を使って名前つきタプルから値を取得するには :func:`getattr`
関数を使います:

   >>> getattr(p, 'x')
   11

辞書を名前付きタプルに変換するには、 ``**`` 演算子 (double-star-operator,
:ref:`tut-unpacking-arguments` で説明しています) を使います。:

   >>> d = {'x': 11, 'y': 22}
   >>> Point(**d)
   Point(x=11, y=22)

名前付きタプルは通常の Python クラスなので、継承して機能を追加したり変更するのは
容易です。次の例では計算済みフィールドと固定幅の print format を追加しています。

    >>> class Point(namedtuple('Point', 'x y')):
    ...     __slots__ = ()
    ...     @property
    ...     def hypot(self):
    ...         return (self.x ** 2 + self.y ** 2) ** 0.5
    ...     def __str__(self):
    ...         return 'Point: x=%6.3f  y=%6.3f  hypot=%6.3f' % (self.x, self.y, self.hypot)

    >>> for p in Point(3, 4), Point(14, 5/7.):
    ...     print p
    Point: x= 3.000  y= 4.000  hypot= 5.000
    Point: x=14.000  y= 0.714  hypot=14.018

このサブクラスは ``__slots__`` に空のタプルをセットしています。
これにより、インスタンス辞書の作成を抑制してメモリ使用量を低く保つのに役立ちます。

サブクラス化は新しいフィールドを追加するのには適していません。
代わりに、新しい名前付きタプルを :attr:`_fields` 属性を元に作成してください:

    >>> Point3D = namedtuple('Point3D', Point._fields + ('z',))

:meth:`_replace` でプロトタイプのインスタンスをカスタマイズする方法で、デフォルト値を
実現できます。

   >>> Account = namedtuple('Account', 'owner balance transaction_count')
   >>> default_account = Account('<owner name>', 0.0, 0)
   >>> johns_account = default_account._replace(owner='John')

列挙型定数は名前付きタプルでも実装できますが、クラス定義を利用した方がシンプルで
効率的です。

    >>> Status = namedtuple('Status', 'open pending closed')._make(range(3))
    >>> Status.open, Status.pending, Status.closed
    (0, 1, 2)
    >>> class Status:
    ...     open, pending, closed = range(3)

.. seealso::

   `Named tuple recipe <http://code.activestate.com/recipes/500261/>`_
   は Python 2.4 で使えます。
