.. _tut-structures:

*****
データ構造
*****

この章では、すでに学んだことについてより詳しく説明するとともに、 いくつか新しいことを追加します。

.. % Data Structures
.. % % This chapter describes some things you've learned about already in
.. % % more detail, and adds some new things as well.


.. _tut-morelists:

リスト型についてもう少し
============

リストデータ型には、他にもいくつかメソッドがあります。リストオブジェクト のすべてのメソッドを以下に示します:

.. % More on Lists
.. % % The list data type has some more methods.  Here are all of the methods
.. % % of list objects:


.. method:: list.append(x)

   リストの末尾に要素を一つ追加します。 ``a[len(a):] = [x]`` と等価です。

   .. % % Add an item to the end of the list;
   .. % % equivalent to \code{a[len(a):] = [\var{x}]}.


.. method:: list.extend(L)

   指定したリスト中のすべての要素を対象のリストに追加し、リストを 拡張します。 ``a[len(a):] = L`` と等価です。

   .. % % Extend the list by appending all the items in the given list;
   .. % % equivalent to \code{a[len(a):] = \var{L}}.


.. method:: list.insert(i, x)

   指定した位置に要素を挿入します。 第 1 引数は、リストのインデクスで、そのインデクスを持つ要素の直前に挿入 が行われます。従って、``a.insert(0,
   x)`` はリストの先頭に挿入 を行います。また ``a.insert(len(a), x)`` は ``a.append(x)``  と等価です。

   .. % % Insert an item at a given position.  The first argument is the index
   .. % % of the element before which to insert, so \code{a.insert(0, \var{x})}
   .. % % inserts at the front of the list, and \code{a.insert(len(a), \var{x})}
   .. % % is equivalent to \code{a.append(\var{x})}.


.. method:: list.remove(x)

   リスト中で、値 *x* を持つ最初の要素を削除します。 該当する項目がなければエラーとなります。

   .. % % Remove the first item from the list whose value is \var{x}.
   .. % % It is an error if there is no such item.


.. method:: list.pop([i])

   リスト中の指定された位置にある要素をリストから削除して、その要素を 返します。インデクスが指定されなければ、``a.pop()`` はリストの
   末尾の要素を削除して、返します。この場合も要素は削除されます。 (メソッドの用法 (signature) で *i* の両側にある角括弧は、
   この引数がオプションであることを表しているだけなので、角括弧を 入力する必要はありません。この表記法は Python Library Reference
   (XXX reference: ../lib/lib.html) の中で頻繁に見ることになるでしょう。)

   .. % % Remove the item at the given position in the list, and return it.  If
   .. % % no index is specified, \code{a.pop()} removes and returns the last item
   .. % % in the list.  (The square brackets
   .. % % around the \var{i} in the method signature denote that the parameter
   .. % % is optional, not that you should type square brackets at that
   .. % % position.  You will see this notation frequently in the
   .. % % \citetitle[../lib/lib.html]{Python Library Reference}.)


.. method:: list.index(x)

   リスト中で、値 *x* を持つ最初の要素のインデクスを返します。 該当する項目がなければエラーとなります。

   .. % % Return the index in the list of the first item whose value is \var{x}.
   .. % % It is an error if there is no such item.


.. method:: list.count(x)

   リストでの *x* の出現回数を返します。

   .. % % Return the number of times \var{x} appears in the list.


.. method:: list.sort()

   リストの項目を、インプレース演算 (in place、元のデータを演算結果で 置き換えるやりかた) でソートします。

   .. % % Sort the items of the list, in place.


.. method:: list.reverse()

   リストの要素を、インプレース演算で逆順にします。

   .. % % Reverse the elements of the list, in place.

以下にリストのメソッドをほぼ全て使った例を示します:

.. % % An example that uses most of the list methods:

::

   >>> a = [66.25, 333, 333, 1, 1234.5]
   >>> print a.count(333), a.count(66.25), a.count('x')
   2 1 0
   >>> a.insert(2, -1)
   >>> a.append(333)
   >>> a
   [66.25, 333, -1, 333, 1, 1234.5, 333]
   >>> a.index(333)
   1
   >>> a.remove(333)
   >>> a
   [66.25, -1, 333, 1, 1234.5, 333]
   >>> a.reverse()
   >>> a
   [333, 1234.5, 1, 333, -1, 66.25]
   >>> a.sort()
   >>> a
   [-1, 1, 66.25, 333, 333, 1234.5]


.. _tut-lists-as-stacks:

リストをスタックとして使う
-------------

.. sectionauthor:: Ka-Ping Yee <ping@lfw.org>


.. % Using Lists as Stacks

リスト型のメソッドのおかげで、簡単にリストをスタックとして使えます。 スタックでは、最後に追加された要素が最初に取り出されます ("last-in,
first-out") 。スタックの一番上に要素を追加するには :meth:`append` を使います。スタックの一番上から要素を取り出すには
:meth:`pop` をインデクスを指定せずに使います。 例えば以下のようにします:

.. % % The list methods make it very easy to use a list as a stack, where the
.. % % last element added is the first element retrieved (``last-in,
.. % % first-out'').  To add an item to the top of the stack, use
.. % % \method{append()}.  To retrieve an item from the top of the stack, use
.. % % \method{pop()} without an explicit index.  For example:

::

   >>> stack = [3, 4, 5]
   >>> stack.append(6)
   >>> stack.append(7)
   >>> stack
   [3, 4, 5, 6, 7]
   >>> stack.pop()
   7
   >>> stack
   [3, 4, 5, 6]
   >>> stack.pop()
   6
   >>> stack.pop()
   5
   >>> stack
   [3, 4]


.. _tut-lists-as-queues:

リストをキューとして使う
------------

.. sectionauthor:: Ka-Ping Yee <ping@lfw.org>


.. % Using Lists as Queues

リストをキュー (queue) として手軽に使うこともできます。 キューでは、最初に追加された要素が最初に取り出されます ("first-in, first-
out")。キューの末尾に項目を追加するには :meth:`append` を使います。キューの先頭から項目を取り出すには  インデクスに ``0``
を指定して :meth:`pop` を使います。 例えば以下のようにします:

.. % % You can also use a list conveniently as a queue, where the first
.. % % element added is the first element retrieved (``first-in,
.. % % first-out'').  To add an item to the back of the queue, use
.. % % \method{append()}.  To retrieve an item from the front of the queue,
.. % % use \method{pop()} with \code{0} as the index.  For example:

::

   >>> queue = ["Eric", "John", "Michael"]
   >>> queue.append("Terry")           # Terry が到着 (arrive) する
   >>> queue.append("Graham")          # Graham が到着する
   >>> queue.pop(0)
   'Eric'
   >>> queue.pop(0)
   'John'
   >>> queue
   ['Michael', 'Terry', 'Graham']


.. _tut-functional:

実用的なプログラミングツール
--------------

組み込み関数には、リストで使うと非常に便利なものが三つあります: :func:`filter` 、 :func:`map` 、:func:`reduce`
です。

.. % Functional Programming Tools
.. % % There are three built-in functions that are very useful when used with
.. % % lists: \function{filter()}, \function{map()}, and \function{reduce()}.

``filter(function, sequence)`` は、 シーケンス *sequence* 中の要素 *item* から、
``function(item)`` が真となるような要素からなる シーケンスを返します。 もし *sequence* が :class:`string`か
:class:`tuple`なら、 返り値も同じタイプになります。そうでなければ :class:`list`になります。
例えば、いくつかの素数を計算するには以下のようにします:

.. % % \samp{filter(\var{function}, \var{sequence})} returns a sequence
.. % % consisting of those items from the
.. % % sequence for which \code{\var{function}(\var{item})} is true.
.. % % If \var{sequence} is a \class{string} or \class{tuple}, the result will
.. % % be of the same type; otherwise, it is always a \class{list}.
.. % % For example, to compute some primes:

::

   >>> def f(x): return x % 2 != 0 and x % 3 != 0
   ...
   >>> filter(f, range(2, 25))
   [5, 7, 11, 13, 17, 19, 23]

``map(function, sequence)`` は、 シーケンス *sequence* の各要素 *item* に対して
``function(item)`` を呼び出し、その戻り値からなる リストを返します。例えば、三乗された値の列を計算するには以下のように します:

.. % % \samp{map(\var{function}, \var{sequence})} calls
.. % % \code{\var{function}(\var{item})} for each of the sequence's items and
.. % % returns a list of the return values.  For example, to compute some
.. % % cubes:

::

   >>> def cube(x): return x*x*x
   ...
   >>> map(cube, range(1, 11))
   [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]

.. % % More than one sequence may be passed; the function must then have as
.. % % many arguments as there are sequences and is called with the
.. % % corresponding item from each sequence (or \code{None} if some sequence
.. % % is shorter than another). For example:

::

   >>> seq = range(8)
   >>> def add(x, y): return x+y
   ...
   >>> map(add, seq, seq)
   [0, 2, 4, 6, 8, 10, 12, 14]

``reduce(function, sequence)`` は単一の値を返します。 この値は 2 つの引数をとる関数 *function* をシーケンス
*sequence* の最初の 二つの要素を引数として呼び出し、次にその結果とシーケンスの次の要素を 引数にとり、以降これを繰り返すことで構成します。 例えば、
1 から 10 までの数の総和を計算するには以下のようにします:

.. % % \samp{reduce(\var{function}, \var{sequence})} returns a single value
.. % % constructed by calling the binary function \var{function} on the first two
.. % % items of the sequence, then on the result and the next item, and so
.. % % on.  For example, to compute the sum of the numbers 1 through 10:

::

   >>> def add(x,y): return x+y
   ...
   >>> reduce(add, range(1, 11))
   55

シーケンス中にただ一つしか要素がなければ、その値自体が返されます; シーケンスが空なら、例外が送出されます。

.. % % If there's only one item in the sequence, its value is returned; if
.. % % the sequence is empty, an exception is raised.

3 つめの引数をわたして、初期値を指定することもできます。 この場合、空のシーケンスを渡すと初期値が返されます。それ以外の場合には、
まず初期値とシーケンス中の最初の要素に対して関数が適用され、次いでその結果 とシーケンスの次の要素に対して適用され、以降これが繰り返されます。例えば
以下のようになります:

.. % % A third argument can be passed to indicate the starting value.  In this
.. % % case the starting value is returned for an empty sequence, and the
.. % % function is first applied to the starting value and the first sequence
.. % % item, then to the result and the next item, and so on.  For example,

::

   >>> def sum(seq):
   ...     def add(x,y): return x+y
   ...     return reduce(add, seq, 0)
   ... 
   >>> sum(range(1, 11))
   55
   >>> sum([])
   0

(2.3 以降では) 実際には、上の例のように :func:`sum` を定義しないでください: 数値の合計は広く必要とされている操作なので、すでに組み込み関数
``sum(sequence)`` が提供されており、上の例と全く同様に 動作します。

.. % % Don't use this example's definition of \function{sum()}: since summing
.. % % numbers is such a common need, a built-in function
.. % % \code{sum(\var{sequence})} is already provided, and works exactly like
.. % % this.
.. % % \versionadded{2.3}

.. versionadded:: 2.3


リストの内包表記
--------

リストの内包表記 (list comprehension) は、リストの生成を :func:`map` や :func:`filter` や
:keyword:`lambda` の使用に 頼らずに行うための簡潔な方法を提供しています。
結果として得られるリストの定義は、しばしば上記の構文を使ってリストを 生成するよりも明快になります。各々のリストの内包表記は、 式、続いて
:keyword:`for` 節、そしてその後ろに続くゼロ個かそれ以上の :keyword:`for` 節または :keyword:`if` 節からなります。
式をタプルで評価したいなら、丸括弧で囲わなければなりません。

.. % List Comprehensions
.. % % List comprehensions provide a concise way to create lists without resorting
.. % % to use of \function{map()}, \function{filter()} and/or \keyword{lambda}.
.. % % The resulting list definition tends often to be clearer than lists built
.. % % using those constructs.  Each list comprehension consists of an expression
.. % % followed by a \keyword{for} clause, then zero or more \keyword{for} or
.. % % \keyword{if} clauses.  The result will be a list resulting from evaluating
.. % % the expression in the context of the \keyword{for} and \keyword{if} clauses
.. % % which follow it.  If the expression would evaluate to a tuple, it must be
.. % % parenthesized.

::

   >>> freshfruit = ['  banana', '  loganberry ', 'passion fruit  ']
   >>> [weapon.strip() for weapon in freshfruit]
   ['banana', 'loganberry', 'passion fruit']
   >>> vec = [2, 4, 6]
   >>> [3*x for x in vec]
   [6, 12, 18]
   >>> [3*x for x in vec if x > 3]
   [12, 18]
   >>> [3*x for x in vec if x < 2]
   []
   >>> [[x,x**2] for x in vec]
   [[2, 4], [4, 16], [6, 36]]
   >>> [x, x**2 for x in vec]  # エラー - タプルには丸かっこが必要
     File "<stdin>", line 1, in ?
       [x, x**2 for x in vec]
                  ^
   SyntaxError: invalid syntax
   >>> [(x, x**2) for x in vec]
   [(2, 4), (4, 16), (6, 36)]
   >>> vec1 = [2, 4, 6]
   >>> vec2 = [4, 3, -9]
   >>> [x*y for x in vec1 for y in vec2]
   [8, 6, -18, 16, 12, -36, 24, 18, -54]
   >>> [x+y for x in vec1 for y in vec2]
   [6, 5, -7, 8, 7, -5, 10, 9, -3]
   >>> [vec1[i]*vec2[i] for i in range(len(vec1))]
   [8, 12, -54]

リストの内包表記は :func:`map` よりもはるかに柔軟性があり、 複雑な式や入れ子になった関数でも利用できます:

.. % % List comprehensions are much more flexible than \function{map()}
.. % % and can be applied to complex expressions and nested functions:

::

   >>> [str(round(355/113.0, i)) for i in range(1, 6)]
   ['3.1', '3.14', '3.142', '3.1416', '3.14159']


.. _tut-del:

:keyword:`del` 文
================

指定された値の要素をリストから削除する代わりに、インデクスで指定する 方法があります: それが :keyword:`del`
文です。これは:meth:`pop`メソッ ドとちがい、値を返しません。:keyword:`del`文はリストから
スライスを除去したり、リスト全体を削除することもできます (以前はスライスに空のリストを代入 して行っていました)。例えば以下のようにします:

.. % The \keyword{del} statement
.. % % There is a way to remove an item from a list given its index instead
.. % % of its value: the \keyword{del} statement.  This can also be used to
.. % % remove slices from a list (which we did earlier by assignment of an
.. % % empty list to the slice).  For example:
.. % % of its value: the \keyword{del} statement.  This differs from the
.. % % \method{pop()}) method which returns a value.  The \keyword{del}
.. % % statement can also be used to remove slices from a list or clear the
.. % % entire list (which we did earlier by assignment of an empty list to
.. % % the slice).  For example:

::

   >>> a
   [-1, 1, 66.25, 333, 333, 1234.5]
   >>> del a[0]
   >>> a
   [1, 66.25, 333, 333, 1234.5]
   >>> del a[2:4]
   >>> a
   [1, 66.25, 1234.5]
   >>> del a[:]
   >>> a
   []

:keyword:`del` は変数全体の削除にも使えます:

.. % % \keyword{del} can also be used to delete entire variables:

::

   >>> del a

この文の後で名前 ``a`` を参照すると、(別の値を ``a`` に 代入するまで) エラーになります。:keyword:`del` の別の用途について
はまた後で取り上げます。

.. % % Referencing the name \code{a} hereafter is an error (at least until
.. % % another value is assigned to it).  We'll find other uses for
.. % % \keyword{del} later.


.. _tut-tuples:

タプルとシーケンス
=========

リストや文字列には、インデクスやスライスを使った演算のように、 数多くの共通の性質があることを見てきました。これらは *シーケンス (sequence)*
データ型 (XXX reference: ../lib/typesseq.html)  の二つの例です。Python はまだ
進歩の過程にある言語なので、他のシーケンスデータ型が追加されるかも しれません。標準のシーケンス型はもう一つあります: *タプル (tuple)* 型です。

.. % Tuples and Sequences
.. % % We saw that lists and strings have many common properties, such as
.. % % indexing and slicing operations.  They are two examples of
.. % % \ulink{\emph{sequence}} data types}{../lib/typesseq.html}.  Since Python is an evolving language,
.. % % other sequence data types may be added.  There is also another
.. % % standard sequence data type: the \emph{tuple}.

タプルはコンマで区切られたいくつかの値からなります。例えば以下の ように書きます:

.. % % A tuple consists of a number of values separated by commas, for
.. % % instance:

::

   >>> t = 12345, 54321, 'hello!'
   >>> t[0]
   12345
   >>> t
   (12345, 54321, 'hello!')
   >>> # タプルを入れ子にしてもよい
   ... u = t, (1, 2, 3, 4, 5)
   >>> u
   ((12345, 54321, 'hello!'), (1, 2, 3, 4, 5))

ご覧のように、タプルは常に丸括弧で囲われています。これは、入れ子に なったタプルが正しく解釈されるようにするためです; 入力の際には
丸括弧なしでもかまいませんが、結局 (タプルがより大きな式の 一部分の場合) たいてい必要となります。

.. % % As you see, on output tuples are alway enclosed in parentheses, so
.. % % that nested tuples are interpreted correctly; they may be input with
.. % % or without surrounding parentheses, although often parentheses are
.. % % necessary anyway (if the tuple is part of a larger expression).

タプルの用途はたくさんあります。例えば、(x, y) 座標対、データベースから 取り出した従業員レコードなどです。タプルは文字列と同じく、変更不能です:
タプルの個々の要素に代入を行うことはできません (スライスと連結を使って 同じ効果を実現することはできますが)。リストのような変更可能な
オブジェクトの入ったタプルを作成することもできます。

.. % % Tuples have many uses.  For example: (x, y) coordinate pairs, employee
.. % % records from a database, etc.  Tuples, like strings, are immutable: it
.. % % is not possible to assign to the individual items of a tuple (you can
.. % % simulate much of the same effect with slicing and concatenation,
.. % % though).  It is also possible to create tuples which contain mutable
.. % % objects, such as lists.

問題は 0 個または 1 個の項目からなるタプルの構築です: これらの操作を 行うため、構文には特別な細工がされています。空のタプルは
空の丸括弧ペアで構築できます; 一つの要素を持つタプルは、 値の後ろにコンマを続ける (単一の値を丸括弧で囲むだけでは不十分です)
ことで構築できます。美しくはないけれども、効果的です。例えば以下の ようにします:

.. % % A special problem is the construction of tuples containing 0 or 1
.. % % items: the syntax has some extra quirks to accommodate these.  Empty
.. % % tuples are constructed by an empty pair of parentheses; a tuple with
.. % % one item is constructed by following a value with a comma
.. % % (it is not sufficient to enclose a single value in parentheses).
.. % % Ugly, but effective.  For example:

::

   >>> empty = ()
   >>> singleton = 'hello',    # <-- 末尾のコンマに注目
   >>> len(empty)
   0
   >>> len(singleton)
   1
   >>> singleton
   ('hello',)

文 ``t = 12345, 54321, 'hello!'`` は *タプルのパック (tuple packing)* の例です: 値 ``12345`` 、
``54321`` 、および ``'hello!'`` が一つのタプルにパックされます。 逆の演算も可能です:

.. % % The statement \code{t = 12345, 54321, 'hello!'} is an example of
.. % % \emph{tuple packing}: the values \code{12345}, \code{54321} and
.. % % \code{'hello!'} are packed together in a tuple.  The reverse operation
.. % % is also possible:

::

   >>> x, y, z = t

この操作は、*シーケンスのアンパック (sequence unpacking)* とでも 呼ぶべきものです。シーケンスのアンパックでは、左辺に列挙されている
変数が、右辺のシーケンスの長さと同じであることが要求されます。 複数同時の代入が実はタプルのパックとシーケンスのアンパックを
組み合わせたものに過ぎないことに注意してください！

.. % % This is called, appropriately enough, \emph{sequence unpacking}.
.. % % Sequence unpacking requires the list of variables on the left
.. % % have the same number of elements as the length of the sequence.  Note
.. % % that multiple assignment is really just a combination of tuple packing
.. % % and sequence unpacking!

この操作にはわずかな非対称性があります: 複数の値をパックすると 常にタプルが生成されますが、アンパックはどのシーケンスにも働きます。

.. % % There is a small bit of asymmetry here:  packing multiple values
.. % % always creates a tuple, and unpacking works for any sequence.

.. % XXX Add a bit on the difference between tuples and lists.


.. _tut-sets:

集合型
===

Python には、*集合 (set)* を扱うためのデータ型もあります。集合 とは、重複する要素をもたない、順序づけられていない要素の集まりです。 Set
オブジェクトは、結合 (union)、交差 (intersection)、差分 (difference)、 対象差 (symmetric difference)
といった数学的な演算もサポートしています。

.. % Sets
.. % Python also includes a data type for \emph{sets}.  A set is an unordered
.. % collection with no duplicate elements.  Basic uses include membership
.. % testing and eliminating duplicate entries.  Set objects also support
.. % mathematical operations like union, intersection, difference, and
.. % symmetric difference.

簡単なデモンストレーションを示します::

   >>> basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
   >>> fruit = set(basket)               # 重複のない集合を作成
   >>> fruit
   set(['orange', 'pear', 'apple', 'banana'])
   >>> 'orange' in fruit                 # 高速なメンバシップテスト
   True
   >>> 'crabgrass' in fruit
   False

   >>> # 二つの単語の文字を例にした集合間の演算
   ...
   >>> a = set('abracadabra')
   >>> b = set('alacazam')
   >>> a                                  # a 内の一意な文字
   set(['a', 'r', 'b', 'c', 'd'])
   >>> a - b                              # a にあって b にない文字
   set(['r', 'd', 'b'])
   >>> a | b                              # a か b にある文字
   set(['a', 'c', 'r', 'd', 'b', 'm', 'z', 'l'])
   >>> a & b                              # a と b の双方にある文字
   set(['a', 'c'])
   >>> a ^ b                              # a または b の片方だけにある文字
   set(['r', 'd', 'b', 'm', 'z', 'l'])


.. _tut-dictionaries:

辞書
==

もう一つ、有用な型が Python に組み込まれています。それは  *辞書 (dictionary)* (XXX reference:
../lib/typesmapping.html) です。辞書は他の言語にも "連想記憶 (associated memory)" や "連想配列
(associative array)" として存在することがあります。 ある範囲の数でインデクス化されているシーケンスと異なり、辞書は *キー (key)*
でインデクス化されています。このキーは何らかの変更不能な型になります; 文字列、数値、およびタプルは常にキーにすることができます; ただし、タプルに
何らかの変更可能なオブジェクトが含まれている場合にはキーに使うことは できません。リストをキーとして使うことはできません。これは、リストに
スライスやインデクス指定の代入を行ったり、 :meth:`append` や :meth:`extend`のようなメソッドを使うと、
インプレースで変更することができるためです。

.. % Dictionaries
.. % % Another useful data type built into Python is the
.. % % \ulink{\emph{dictionary}}{../lib/typesmapping.html}.
.. % % Dictionaries are sometimes found in other languages as ``associative
.. % % memories'' or ``associative arrays''.  Unlike sequences, which are
.. % % indexed by a range of numbers, dictionaries are indexed by \emph{keys},
.. % % which can be any immutable type; strings and numbers can always be
.. % % keys.  Tuples can be used as keys if they contain only strings,
.. % % numbers, or tuples; if a tuple contains any mutable object either
.. % % directly or indirectly, it cannot be used as a key.  You can't use
.. % % lists as keys, since lists can be modified in place using
.. % % index. assignments, slice assignments, or methods like
.. % % \method{append()} and \method{extend()}.

辞書は順序付けのされていない *キー(key): 値(value)* のペアからなり、 キーが (辞書の中で)
一意でければならない、と考えると最もよいでしょう。 波括弧 (brace) のペア: ``{}`` は空の辞書を生成します。 カンマで区切られた key:
value のペアを波括弧ペアの間に入れると、 辞書の初期値となる key: value が追加されます; この表現方法は
出力時に辞書が書き出されるのと同じ方法です。

.. % % It is best to think of a dictionary as an unordered set of
.. % % \emph{key: value} pairs, with the requirement that the keys are unique
.. % % (within one dictionary).
.. % % A pair of braces creates an empty dictionary: \code{\{\}}.
.. % % Placing a comma-separated list of key:value pairs within the
.. % % braces adds initial key:value pairs to the dictionary; this is also the
.. % % way dictionaries are written on output.

辞書での主な操作は、ある値を何らかのキーを付けて記憶することと、 キーを指定して値を取り出すことです。 ``del`` で key: value のペアを
削除することもできます。 すでに使われているキーを使って値を記憶すると、以前そのキーに関連 づけられていた値は忘れ去られてしまいます。存在しないキーを使って
値を取り出そうとするとエラーになります。

.. % % The main operations on a dictionary are storing a value with some key
.. % % and extracting the value given the key.  It is also possible to delete
.. % % a key:value pair
.. % % with \code{del}.
.. % % If you store using a key that is already in use, the old value
.. % % associated with that key is forgotten.  It is an error to extract a
.. % % value using a non-existent key.

.. % % The \method{keys()} method of a dictionary object returns a list of all
.. % % the keys used in the dictionary, in random order (if you want it
.. % % sorted, just apply the \method{sort()} method to the list of keys).  To
.. % % check whether a single key is in the dictionary, either use the dictionary's
.. % % \method{has_key()} method or the \keyword{in} keyword.

辞書オブジェクトの :meth:`keys` メソッドは、辞書で使われている 全てのキーからなるリストを適当な順番で返します (リストをソート
したいなら、このキーのリストに :meth:`sort` を使ってください)。 ある単一のキーが辞書にあるかどうか調べるには、辞書の
:meth:`has_key`  メソッドか、:keyword:`in`キーワード を使います。

以下に、辞書を使った小さな例を示します:

.. % % Here is a small example using a dictionary:

::

   >>> tel = {'jack': 4098, 'sape': 4139}
   >>> tel['guido'] = 4127
   >>> tel
   {'sape': 4139, 'guido': 4127, 'jack': 4098}
   >>> tel['jack']
   4098
   >>> del tel['sape']
   >>> tel['irv'] = 4127
   >>> tel
   {'guido': 4127, 'irv': 4127, 'jack': 4098}
   >>> tel.keys()
   ['guido', 'irv', 'jack']
   >>> tel.has_key('guido')
   1
   >>> 'guido' in tel
   True

:func:`dict` コンストラクタは、キーと値のペアをタプルにしたもの からなるリストを使って直接辞書を生成します。キーと値のペアが
あるパターンをなしているなら、リストの内包表現を使えばキーと値の リストをコンパクトに指定できます。

.. % % The \function{dict()} constructor builds dictionaries directly from
.. % % lists of key-value pairs stored as tuples.  When the pairs form a
.. % % pattern, list comprehensions can compactly specify the key-value list.

::

   >>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
   {'sape': 4139, 'jack': 4098, 'guido': 4127}
   >>> dict([(x, x**2) for x in (2, 4, 6)])     # リスト内包表現を利用
   {2: 4, 4: 16, 6: 36}

チュートリアルの後部では、キー=値ペアを:func:`dict`コンストラクタ に渡すために適したジェネレータ式について学習します。

.. % % Later in the tutorial, we will learn about Generator Expressions
.. % % which are even better suited for the task of supplying key-values pairs to
.. % % the \function{dict()} constructor.

キーが単純な文字列の場合、キーワード引数を使って定義する方が単純な場合 もあります。

.. % % When the keys are simple strings, it is sometimes easier to specify
.. % % pairs using keyword arguments:

::

   >>> dict(sape=4139, guido=4127, jack=4098)
   {'sape': 4139, 'jack': 4098, 'guido': 4127}


.. _tut-loopidioms:

ループのテクニック
=========

辞書の内容にわたってループを行う際、:meth:`iteritems` メソッドを使うと、 キーとそれに対応する値を同時に取り出せます。

.. % Looping Techniques
.. % % When looping through dictionaries, the key and corresponding value can
.. % % be retrieved at the same time using the \method{iteritems()} method.

::

   >>> knights = {'gallahad': 'the pure', 'robin': 'the brave'}
   >>> for k, v in knights.iteritems():
   ...     print k, v
   ...
   gallahad the pure
   robin the brave

シーケンスにわたるループを行う際、:func:`enumerate` 関数を使うと、要素の インデクスと要素を同時に取り出すことができます。

.. % % When looping through a sequence, the position index and corresponding
.. % % value can be retrieved at the same time using the
.. % % \function{enumerate()} function.
.. % % begin{verbatim}
.. % % >>> for i, v in enumerate(['tic', 'tac', 'toe']):
.. % % ...     print i, v
.. % % ...
.. % % 0 tic
.. % % 1 tac
.. % % 2 toe
.. % % end{verbatim}

::

   >>> for i, v in enumerate(['tic', 'tac', 'toe']):
   ...     print i, v
   ...
   0 tic
   1 tac
   2 toe

二つまたはそれ以上のシーケンス型を同時にループするために、 関数 :func:`zip` を使って各要素をひと組みにすることができます。

.. % % To loop over two or more sequences at the same time, the entries
.. % % can be paired with the \function{zip()} function.

::

   >>> questions = ['name', 'quest', 'favorite color']
   >>> answers = ['lancelot', 'the holy grail', 'blue']
   >>> for q, a in zip(questions, answers):
   ...     print 'What is your %s?  It is %s.' % (q, a)
   ... 
   What is your name?  It is lancelot.
   What is your quest?  It is the holy grail.
   What is your favorite color?  It is blue.

シーケンスを逆方向に渡ってループするには、まずシーケンスの範囲を順方向に指定し、 次いで関数:func:`reversed` を呼び出します。

.. % % To loop over a sequence in reverse, first specify the sequence
.. % % in a forward direction and then call the \function{reversed()}
.. % % function.

::

   >>> for i in reversed(xrange(1,10,2)): 
   ...     print i 
   ... 
   9 
   7 
   5 
   3 
   1 

シーケンスを並び順にループするには、:func:`sorted` 関数を使います。 この関数は元の配列を変更せず、並べ変え済みの新たな配列を返します。

.. % To loop over a sequence in sorted order, use the \function{sorted()}
.. % function which returns a new sorted list while leaving the source
.. % unaltered.

::

   >>> basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
   >>> for f in sorted(set(basket)):
   ...     print f
   ... 	
   apple
   banana
   orange
   pear


.. _tut-conditions:

条件についてもう少し
==========

``while`` や ``if`` 文 で使った条件 (condiction) には、 値の比較だけでなく、他の演算子も使うことができます、

.. % More on Conditions
.. % % The conditions used in \code{while} and \code{if} statements above can
.. % % contain other operators besides comparisons.

比較演算子 ``in`` および ``not in`` は、ある値があるシーケンス中に 存在するか (または存在しないか) どうかを調べます。演算子
``is``  および ``is not`` は、二つのオブジェクトが実際に同じオブジェクト であるかどうかを調べます; この比較は、リストのような変更可能な
オブジェクトにだけ意味があります。全ての比較演算子は同じ優先順位を 持っており、ともに数値演算子よりも低い優先順位となります。

.. % % The comparison operators \code{in} and \code{not in} check whether a value
.. % % occurs (does not occur) in a sequence.  The operators \code{is} and
.. % % \code{is not} compare whether two objects are really the same object; this
.. % % only matters for mutable objects like lists.  All comparison operators
.. % % have the same priority, which is lower than that of all numerical
.. % % operators.

比較は連鎖 (chain) させることができます。例えば、 ``a < b == c`` は、``a`` が ``b`` より小さく、 かつ ``b`` と
``c`` が等しいかどうか、をテストします。

.. % % Comparisons can be chained.  For example, \code{a < b == c} tests
.. % % whether \code{a} is less than \code{b} and moreover \code{b} equals
.. % % \code{c}.

比較演算はブール演算子 ``and`` や ``or`` で組み合わせられます。また、 比較演算 (あるいは何らかのブール式) の結果の否 (negate)
は``not`` で とれます。これらの演算子は全て、比較演算子よりも低い優先順位になっています。 ``A and not B or C`` と ``(A
and (not B)) or C`` が等価になるように、 ブール演算子の中で、``not`` の優先順位が最も高く、``or`` が最も
低くなっています。もちろん、丸括弧を使えば望みの組み合わせを表現できます。

.. % % Comparisons may be combined using the Boolean operators \code{and} and
.. % % \code{or}, and the outcome of a comparison (or of any other Boolean
.. % +expression) may be negated with \code{not}.  These have lower
.. % +priorities than comparison operators; between them, \code{not} has
.. % +the highest priority and \code{or} the lowest, so that
.. % +\code{A and not B or C} is equivalent to \code{(A and (not B)) or C}.
.. % +As always, parentheses can be used to express the desired composition.

ブール演算子 ``and`` と ``or`` は、いわゆる *短絡 (short-circuit)* 演算子です: これらの演算子の引数は
左から右へと順に評価され、結果が確定した時点で評価を止めます。 例えば、``A`` と ``C`` は真で ``B`` が偽のとき、 ``A and B and
C`` は式 ``C`` を評価しません。 一般に、短絡演算子の戻り値をブール値ではなくて一般的な値として用いると、 値は最後に評価された引数になります。

.. % % The Boolean operators \code{and} and \code{or} are so-called
.. % % \emph{short-circuit} operators: their arguments are evaluated from
.. % % left to right, and evaluation stops as soon as the outcome is
.. % % determined.  For example, if \code{A} and \code{C} are true but
.. % % \code{B} is false, \code{A and B and C} does not evaluate the
.. % % expression \code{C}.  When used as a general value and not as a
.. % % Boolean, the return value of a short-circuit operator is the last
.. % % evaluated argument.

比較や他のブール式の結果を変数に代入することもできます。例えば、

.. % % It is possible to assign the result of a comparison or other Boolean
.. % % expression to a variable.  For example,

::

   >>> string1, string2, string3 = '', 'Trondheim', 'Hammer Dance'
   >>> non_null = string1 or string2 or string3
   >>> non_null
   'Trondheim'

Python では、C 言語と違って、式の内部で代入を行えないので注意してください。 C 言語のプログラマは不満を呈するかもしれませんが、この仕様は、 C 言語
プログラムで遭遇する、式の中で ``==`` のつもりで ``=`` とタイプ してしまうといったありふれた問題を回避します。

.. % % Note that in Python, unlike C, assignment cannot occur inside expressions.
.. % % C programmers may grumble about this, but it avoids a common class of
.. % % problems encountered in C programs: typing \code{=} in an expression when
.. % % \code{==} was intended.


.. _tut-comparing:

シーケンスとその他の型の比較
==============

シーケンスオブジェクトは同じシーケンス型の他のオブジェクトと比較できます。 比較には *辞書的な (lexicographical)* 順序が用いられます:
まず、最初の二つの要素を比較し、その値が等しくなければその時点で 比較結果が決まります。等しければ次の二つの要素を比較し、以降
シーケンスの要素が尽きるまで続けます。比較しようとする二つの要素が いずれも同じシーケンス型であれば、そのシーケンス間での辞書比較を再帰的に行います。
二つのシーケンスの全ての要素の比較結果が等しくなれば、シーケンスは等しいと みなされます。片方のシーケンスがもう一方の先頭部分にあたる部分シーケンス
ならば、短い方のシーケンスが小さい (劣位の) シーケンスとみなされます。 文字列に対する辞書的な順序づけには、個々の文字ごとに ASCII 順序を 用います。
以下に、同じ型のオブジェクトを持つシーケンス間での比較を行った例を示します:

.. % Comparing Sequences and Other Types
.. % % Sequence objects may be compared to other objects with the same
.. % % sequence type.  The comparison uses \emph{lexicographical} ordering:
.. % % first the first two items are compared, and if they differ this
.. % % determines the outcome of the comparison; if they are equal, the next
.. % % two items are compared, and so on, until either sequence is exhausted.
.. % % If two items to be compared are themselves sequences of the same type,
.. % % the lexicographical comparison is carried out recursively.  If all
.. % % items of two sequences compare equal, the sequences are considered
.. % % equal.  If one sequence is an initial sub-sequence of the other, the
.. % % shorter sequence is the smaller (lesser) one.  Lexicographical
.. % % ordering for strings uses the \ASCII{} ordering for individual
.. % % characters.  Some examples of comparisons between sequences of the
.. % % same type:

::

   (1, 2, 3)              < (1, 2, 4)
   [1, 2, 3]              < [1, 2, 4]
   'ABC' < 'C' < 'Pascal' < 'Python'
   (1, 2, 3, 4)           < (1, 2, 4)
   (1, 2)                 < (1, 2, -1)
   (1, 2, 3)             == (1.0, 2.0, 3.0)
   (1, 2, ('aa', 'ab'))   < (1, 2, ('abc', 'a'), 4)

違う型のオブジェクト間の比較は認められていることに注意してください。 比較結果は決定性がありますが、その決め方は、型は型の名前で順番づけられる、
という恣意的なものです。従って、リスト (list) 型は常に文字列 (string) 型よりも小さく、文字列型は常にタプル (tuple)
よりも小さい、といった 具合になります。 [#]_

.. % % Note that comparing objects of different types is legal.  The outcome
.. % % is deterministic but arbitrary: the types are ordered by their name.
.. % % Thus, a list is always smaller than a string, a string is always
.. % % smaller than a tuple, etc.  \footnote{
.. % %         The rules for comparing objects of different types should
.. % %         not be relied upon; they may change in a future version of
.. % %         the language.
.. % % }  Mixed numeric types are compared according to their numeric value, so
.. % % 0 equals 0.0, etc.

型混合の数値の比較は、数値そのものに従って比較 されるので、例えば 0 は 0.0 と等しい、という結果になります。


.. rubric:: Footnotes

.. [#] 異なる型のオブジェクトを比較するための規則を今後にわたって当てに してはなりません; Python 言語の将来のバージョンでは変更されるかも しれません。

