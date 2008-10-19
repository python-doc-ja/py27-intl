
:mod:`collections` --- 高性能なコンテナ・データ型
====================================

.. module:: collections
   :synopsis: High-performance container datatypes
.. moduleauthor:: Raymond Hettinger <python@rcn.com>
.. sectionauthor:: Raymond Hettinger <python@rcn.com>


.. versionadded:: 2.4

このモジュールでは高性能なコンテナ・データ型を実装しています。 現在のところ、実装されている型は deque と defaultdict です。 将来的に
B-tree と ordere dictionary がふくまれるかもしれません。

.. versionchanged:: 2.5
   defaultdict の追加.


.. _deque-objects:

:class:`deque` オブジェクト
---------------------


.. class:: deque([iterable])

   *iterable* で与えられるデータから、新しい deque オブジェクトを (:meth:`append` をつかって) 左→右に初期化し、返します。
   *iterable* が指定されない場合、新しい deque オブジェクトは空になります。

   Deque とは、スタックとキューを一般化したものです (この名前は「デック」と 発音され、これは「double-ended
   queue」の省略形です)。Deque はどちらの側からも append と pop が可能で、スレッドセーフでメモリ効率がよく、どちらの方向からも およそ
   ``O(1)`` のパフォーマンスで実行できます。

   :class:`list` オブジェクトでも同様の操作を実現できますが、これは高速な 固定長の操作に特化されており、内部のデータ表現形式のサイズと位置を
   両方変えるような ``pop(0)`` and ``insert(0, v)`` などの操作では メモリ移動のために ``O(n)`` のコストを必要とします。

   .. versionadded:: 2.4

Deque オブジェクトは以下のようなメソッドをサポートしています:


.. method:: deque.append(x)

   *x* を deque の右側につけ加えます。


.. method:: deque.appendleft(x)

   *x* を deque の左側につけ加えます。


.. method:: deque.clear()

   Deque からすべての要素を削除し、長さを 0 にします。


.. method:: deque.extend(iterable)

   イテレータ化可能な引数 iterable から得られる要素を deque の右側に 追加し拡張します。


.. method:: deque.extendleft(iterable)

   イテレータ化可能な引数 iterable から得られる要素を deque の左側に 追加し拡張します。注意: 左から追加した結果は、イテレータ引数の
   順序とは逆になります。


.. method:: deque.pop()

   Deque の右側から要素をひとつ削除し、その要素を返します。 要素がひとつも存在しない場合は :exc:`IndexError` を発生させます。


.. method:: deque.popleft()

   Deque の左側から要素をひとつ削除し、その要素を返します。 要素がひとつも存在しない場合は :exc:`IndexError` を発生させます。


.. method:: deque.remove(value)

   最初に現れる value を削除します。 要素がみつからないない場合は :exc:`ValueError` を発生させます。

   .. versionadded:: 2.5


.. method:: deque.rotate(n)

   Deque の要素を全体で *n*ステップだけ右にローテートします。 *n* が負の値の場合は、左にローテートします。Deque を
   ひとつ右にローテートすることは ``d.appendleft(d.pop())`` と同じです。

上記の操作のほかにも、deque は次のような操作をサポートしています: イテレータ化、pickle、``len(d)``、``reversed(d)``、
``copy.copy(d)``、 ``copy.deepcopy(d)``、 :keyword:`in` 演算子による 包含検査、そして ``d[-1]``
などの添え字による参照。

例::

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


.. _deque-recipes:

レシピ
---

この節では deque をつかったさまざまなアプローチを紹介します。

:meth:`rotate` メソッドのおかげで、 :class:`deque` の一部を切り出したり 削除したりできることになります。たとえば ``del
d[n]`` の純粋な Python 実装では pop したい要素まで :meth:`rotate` します ::

   def delete_nth(d, n):
       d.rotate(-n)
       d.popleft()
       d.rotate(n)

:class:`deque` の切り出しを実装するのにも、同様のアプローチを使います。 まず対象となる要素を :meth:`rotate` によって deque
の左端まで もってきてから、:meth:`popleft` をつかって古い要素を消します。 そして、:meth:`extend`
で新しい要素を追加したのち、逆のローテートで もとに戻せばよいのです。

このアプローチをやや変えたものとして、Forth スタイルのスタック操作、 つまり ``dup``, ``drop``, ``swap``, ``over``,
``pick``, ``rot``, および ``roll`` を実装するのも簡単です。

ラウンドロビンのタスクサーバは :class:`deque` をつかって、 :meth:`popleft` で現在のタスクを選択し、
入力ストリームが使い果たされなければ :meth:`append` で タスクリストの戻してやることができます::

   def roundrobin(*iterables):
       pending = deque(iter(i) for i in iterables)
       while pending:
           task = pending.popleft()
           try:
               yield task.next()
           except StopIteration:
               continue
           pending.append(task)

   >>> for value in roundrobin('abc', 'd', 'efgh'):
   ...     print value

   a
   d
   e
   b
   f
   c
   g
   h


複数パスのデータ・リダクション アルゴリズムは、:meth:`popleft` を 複数回呼んで要素をとりだし、リダクション用の関数を適用してから
:meth:`append` で deque に戻してやることにより、簡潔かつ効率的に 表現することができます。

たとえば入れ子状になったリストでバランスされた二進木をつくりたい場合、 2つの隣接するノードをひとつのリストにグループ化することになります::

   def maketree(iterable):
       d = deque(iterable)
       while len(d) > 1:
           pair = [d.popleft(), d.popleft()]
           d.append(pair)
       return list(d)

   >>> print maketree('abcdefgh')
   [[[['a', 'b'], ['c', 'd']], [['e', 'f'], ['g', 'h']]]]



.. _defaultdict-objects:

:class:`defaultdict` オブジェクト
---------------------------


.. class:: defaultdict([default_factory[, ...]])

   新しいディクショナリ状のオブジェクトを返します。:class:`defaultdict`は 組込みの
   :class:`dict`のサブクラスです。メソッドをオーバーライドし、書 き込み可能なインスタンス変数を1つ追加している以外は
   :class:`dict`クラスと同じです。 同じ部分については以下では省略されています。

   1つめの引数は:attr:`default_factory`属性の初期値です。デフォルトは
   ``None``です。残りの引数はキーワード引数もふくめ、:class:`dict`のコ ンストラクタにあたえられた場合と同様に扱われます。

   .. versionadded:: 2.5

:class:`defaultdict` オブジェクトは標準の:class:`dict`に加えて、以下のメ ソッドを実装しています:


.. method:: defaultdict.__missing__(key)

   もし:attr:`default_factory`属性が``None``であれば、このメソッドは
   :exc:`KeyError`例外を、*key*を引数として発生させます。

   もし:attr:`default_factory`属性が``None``でなければ、このメソッドは
   :attr:`default_factory`を引数なしで呼び出し、あたえられた*key*に 対応するデフォルト値を作ります。そしてこの値を *key*
   に対応する値 を辞書に登録して返ります。

   もし :attr:`default_factory` の呼出が例外を発生させた場合には、 変更せずそのまま例外を投げます。

   このメソッドは:class:`dict`クラスの :meth:`__getitem__` メソッドで、キー
   が存在しなかった場合によびだされます。値を返すか例外を発生させるのどち
   らにしても、:meth:`__getitem__`からもそのまま値が返るか例外が発生します。

:class:`defaultdict` オブジェクトは以下のインスタンス変数をサポートして います:


.. data:: default_factory

   この属性は :meth:`__missing__` メソッドによって使われます。これは 存在すればコンストラクタの第1引数によって初期化され、そうでなければ
   ``None``になります。


.. _defaultdict-examples:

:class:`defaultdict` の使用例
^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`list`を:attr:`default_factory`とすることで、キー=値ペアのシー ケンスをリストの辞書へ簡単にグループ化できます。
::

   >>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
   >>> d = defaultdict(list)
   >>> for k, v in s:
           d[k].append(v)

   >>> d.items()
   [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

それぞれのキーが最初に登場したとき、マッピングにはまだ存在しません。
そのためエントリは:attr:`default_factory`関数が返す空の:class:`list` を使って自動的に作成されます。
:meth:`list.append`操作は新しいリストに紐付けられます。 キーが再度出現下場合には、通常の参照動作が行われます(そのキーに対応す
るリストが返ります)。そして :meth:`list.append`操作で別の値をリスト
に追加します。このテクニックは:meth:`dict.setdefault`を使った等価な ものよりシンプルで速いです::

   >>> d = {}
   >>> for k, v in s:
   	d.setdefault(k, []).append(v)

   >>> d.items()
   [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

:attr:`default_factory` を :class:`int` にすると、:class:`defaultdict` を(他の言語の bag や
multisetのように)要素の数え上げに便利に使うことができます::

   >>> s = 'mississippi'
   >>> d = defaultdict(int)
   >>> for k in s:
           d[k] += 1

   >>> d.items()
   [('i', 4), ('p', 2), ('s', 4), ('m', 1)]

最初に文字が出現したときは、マッピングが存在しないので :attr:`default_factory` 関数が :func:`int`を呼んでデフォルトのカ
ウント0 を生成します。インクリメント操作が各文字を数え上げます。 このテクニックは以下の :meth:`dict.get`を使った等価なものよりシンプ
ルで速いです::

   >>> d = {}
   >>> for k in s:
   	d[k] = d.get(k, 0) + 1

   >>> d.items()
   [('i', 4), ('p', 2), ('s', 4), ('m', 1)]

:attr:`default_factory` を :class:`set` に設定することで、
:class:`defaultdict`をセットの辞書を作るために利用することができます::

   >>> s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
   >>> d = defaultdict(set)
   >>> for k, v in s:
           d[k].add(v)

   >>> d.items()
   [('blue', set([2, 4])), ('red', set([1, 3]))]

