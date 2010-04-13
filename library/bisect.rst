
:mod:`bisect` --- 配列二分法アルゴリズム
========================================

.. module:: bisect
   :synopsis: バイナリサーチ用の配列二分法アルゴリズム。
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. example based on the PyModules FAQ entry by Aaron Watters
.. <arw@pythonpros.com>.

このモジュールは、挿入の度にリストをソートすることなく、リストをソートされた順序に保つことをサポートします。
大量の比較操作を伴うような、アイテムがたくさんあるリストでは、より一般的なアプローチに比べて、パフォーマンスが向上します。
動作に基本的な二分法アルゴリズムを使っているので、 :mod:`bisect` と呼ばれています。
ソースコードはこのアルゴリズムの実例として一番役に立つかもしれません (境界条件はすでに正しいです!)。

次の関数が用意されています。


.. function:: bisect_left(list, item[, lo[, hi]])

   ソートされた順序を保ったまま *item* を *list* に挿入するのに適した挿入点を探し当てます。
   リストの中から検索する部分集合を指定するには、パラメーターの *lo* と *hi* を使います。デフォルトでは、リスト全体が使われます。 *item*
   がすでに *list* に含まれている場合、挿入点はどのエントリーよりも前(左)になります。戻り値は、 ``list.insert()``
   の第一引数として使うのに適しています。 *list* はすでにソートされているものとします。

   .. versionadded:: 2.1


.. function:: bisect_right(list, item[, lo[, hi]])

   :func:`bisect_left` と似ていますが、 *list* に含まれる *item*
   のうち、どのエントリーよりも後ろ(右)にくるような挿入点を返します。

   .. versionadded:: 2.1


.. function:: bisect(...)

   :func:`bisect_right` のエイリアス。


.. function:: insort_left(list, item[, lo[, hi]])

   *item* を *list* にソートされた順序で(ソートされたまま)挿入します。これは、
   ``list.insert(bisect.bisect_left(list, item, lo, hi), item)`` と同等です。 *list*
   はすでにソートされているものとします。

   .. versionadded:: 2.1


.. function:: insort_right(list, item[, lo[, hi]])

   :func:`insort_left` と似ていますが、 *list* に含まれる *item* のうち、どのエントリーよりも後ろに *item* を挿入します。

   .. versionadded:: 2.1


.. function:: insort(...)

   :func:`insort_right` のエイリアス。


使用例
------

.. _bisect-example:

一般には、 :func:`bisect` 関数は数値データを分類するのに役に立ちます。この例では、 :func:`bisect`
を使って、(たとえば)順序のついた数値の区切り点の集合に基づいて、試験全体の成績の文字を調べます。区切り点は 85 以上は 'A'、 75..84 は
'B'、などです。

   >>> grades = "FEDCBA"
   >>> breakpoints = [30, 44, 66, 75, 85]
   >>> from bisect import bisect
   >>> def grade(total):
   ...           return grades[bisect(breakpoints, total)]
   ...
   >>> grade(66)
   'C'
   >>> map(grade, [33, 99, 77, 44, 12, 88])
   ['E', 'A', 'B', 'D', 'F', 'A']

