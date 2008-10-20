
:mod:`collections` --- High-performance container datatypes
===========================================================

.. module:: collections
   :synopsis: High-performance datatypes
.. moduleauthor:: Raymond Hettinger <python@rcn.com>
.. sectionauthor:: Raymond Hettinger <python@rcn.com>


.. versionadded:: 2.4

This module implements high-performance container datatypes.  Currently, there
are two datatypes, deque and defaultdict. Future additions may include balanced
trees and ordered dictionaries.

.. versionchanged:: 2.5
   Added defaultdict.


.. _deque-objects:

:class:`deque` objects
----------------------


.. function:: deque([iterable])

   Returns a new deque objected initialized left-to-right (using :meth:`append`)
   with data from *iterable*.  If *iterable* is not specified, the new deque is
   empty.

   Deques are a generalization of stacks and queues (the name is pronounced "deck"
   and is short for "double-ended queue").  Deques support thread-safe, memory
   efficient appends and pops from either side of the deque with approximately the
   same ``O(1)`` performance in either direction.

   Though :class:`list` objects support similar operations, they are optimized for
   fast fixed-length operations and incur ``O(n)`` memory movement costs for
   ``pop(0)`` and ``insert(0, v)`` operations which change both the size and
   position of the underlying data representation.

   .. versionadded:: 2.4

Deque objects support the following methods:


.. method:: XXX Class.append(x)

   Add *x* to the right side of the deque.


.. method:: XXX Class.appendleft(x)

   Add *x* to the left side of the deque.


.. method:: XXX Class.clear()

   Remove all elements from the deque leaving it with length 0.


.. method:: XXX Class.extend(iterable)

   Extend the right side of the deque by appending elements from the iterable
   argument.


.. method:: XXX Class.extendleft(iterable)

   Extend the left side of the deque by appending elements from *iterable*.  Note,
   the series of left appends results in reversing the order of elements in the
   iterable argument.


.. method:: XXX Class.pop()

   Remove and return an element from the right side of the deque. If no elements
   are present, raises an :exc:`IndexError`.


.. method:: XXX Class.popleft()

   Remove and return an element from the left side of the deque. If no elements are
   present, raises an :exc:`IndexError`.


.. method:: XXX Class.remove(value)

   Removed the first occurrence of *value*.  If not found, raises a
   :exc:`ValueError`.

   .. versionadded:: 2.5


.. method:: XXX Class.rotate(n)

   Rotate the deque *n* steps to the right.  If *n* is negative, rotate to the
   left.  Rotating one step to the right is equivalent to:
   ``d.appendleft(d.pop())``.

In addition to the above, deques support iteration, pickling, ``len(d)``,
``reversed(d)``, ``copy.copy(d)``, ``copy.deepcopy(d)``, membership testing with
the :keyword:`in` operator, and subscript references such as ``d[-1]``.

Example::

   >>> from collections import deque
   >>> d = deque('ghi')                 # make a new deque with three items
   >>> for elem in d:                   # iterate over the deque's elements
   ...     print elem.upper()	
   G
   H
   I

   >>> d.append('j')                    # add a new entry to the right side
   >>> d.appendleft('f')                # add a new entry to the left side
   >>> d                                # show the representation of the deque
   deque(['f', 'g', 'h', 'i', 'j'])

   >>> d.pop()                          # return and remove the rightmost item
   'j'
   >>> d.popleft()                      # return and remove the leftmost item
   'f'
   >>> list(d)                          # list the contents of the deque
   ['g', 'h', 'i']
   >>> d[0]                             # peek at leftmost item
   'g'
   >>> d[-1]                            # peek at rightmost item
   'i'

   >>> list(reversed(d))                # list the contents of a deque in reverse
   ['i', 'h', 'g']
   >>> 'h' in d                         # search the deque
   True
   >>> d.extend('jkl')                  # add multiple elements at once
   >>> d
   deque(['g', 'h', 'i', 'j', 'k', 'l'])
   >>> d.rotate(1)                      # right rotation
   >>> d
   deque(['l', 'g', 'h', 'i', 'j', 'k'])
   >>> d.rotate(-1)                     # left rotation
   >>> d
   deque(['g', 'h', 'i', 'j', 'k', 'l'])

   >>> deque(reversed(d))               # make a new deque in reverse order
   deque(['l', 'k', 'j', 'i', 'h', 'g'])
   >>> d.clear()                        # empty the deque
   >>> d.pop()                          # cannot pop from an empty deque
   Traceback (most recent call last):
     File "<pyshell#6>", line 1, in -toplevel-
       d.pop()
   IndexError: pop from an empty deque

   >>> d.extendleft('abc')              # extendleft() reverses the input order
   >>> d
   deque(['c', 'b', 'a'])


.. _deque-recipes:

Recipes
^^^^^^^

This section shows various approaches to working with deques.

The :meth:`rotate` method provides a way to implement :class:`deque` slicing and
deletion.  For example, a pure python implementation of ``del d[n]`` relies on
the :meth:`rotate` method to position elements to be popped::

   def delete_nth(d, n):
       d.rotate(-n)
       d.popleft()
       d.rotate(n)

To implement :class:`deque` slicing, use a similar approach applying
:meth:`rotate` to bring a target element to the left side of the deque. Remove
old entries with :meth:`popleft`, add new entries with :meth:`extend`, and then
reverse the rotation.

With minor variations on that approach, it is easy to implement Forth style
stack manipulations such as ``dup``, ``drop``, ``swap``, ``over``, ``pick``,
``rot``, and ``roll``.

A roundrobin task server can be built from a :class:`deque` using
:meth:`popleft` to select the current task and :meth:`append` to add it back to
the tasklist if the input stream is not exhausted::

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


Multi-pass data reduction algorithms can be succinctly expressed and efficiently
coded by extracting elements with multiple calls to :meth:`popleft`, applying
the reduction function, and calling :meth:`append` to add the result back to the
queue.

For example, building a balanced binary tree of nested lists entails reducing
two adjacent nodes into one by grouping them in a list::

   def maketree(iterable):
       d = deque(iterable)
       while len(d) > 1:
           pair = [d.popleft(), d.popleft()]
           d.append(pair)
       return list(d)

   >>> print maketree('abcdefgh')
   [[[['a', 'b'], ['c', 'd']], [['e', 'f'], ['g', 'h']]]]



.. _defaultdict-objects:

:class:`defaultdict` objects
----------------------------


.. function:: defaultdict([default_factory[, ...]])

   Returns a new dictionary-like object.  :class:`defaultdict` is a subclass of the
   builtin :class:`dict` class.  It overrides one method and adds one writable
   instance variable.  The remaining functionality is the same as for the
   :class:`dict` class and is not documented here.

   The first argument provides the initial value for the :attr:`default_factory`
   attribute; it defaults to ``None``. All remaining arguments are treated the same
   as if they were passed to the :class:`dict` constructor, including keyword
   arguments.

   .. versionadded:: 2.5

:class:`defaultdict` objects support the following method in addition to the
standard :class:`dict` operations:


.. method:: XXX Class.__missing__(key)

   If the :attr:`default_factory` attribute is ``None``, this raises an
   :exc:`KeyError` exception with the *key* as argument.

   If :attr:`default_factory` is not ``None``, it is called without arguments to
   provide a default value for the given *key*, this value is inserted in the
   dictionary for the *key*, and returned.

   If calling :attr:`default_factory` raises an exception this exception is
   propagated unchanged.

   This method is called by the :meth:`__getitem__` method of the :class:`dict`
   class when the requested key is not found; whatever it returns or raises is then
   returned or raised by :meth:`__getitem__`.

:class:`defaultdict` objects support the following instance variable:


.. data:: default_factory

   This attribute is used by the :meth:`__missing__` method; it is initialized from
   the first argument to the constructor, if present, or to ``None``,  if absent.


.. _defaultdict-examples:

:class:`defaultdict` Examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using :class:`list` as the :attr:`default_factory`, it is easy to group a
sequence of key-value pairs into a dictionary of lists::

   >>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
   >>> d = defaultdict(list)
   >>> for k, v in s:
           d[k].append(v)

   >>> d.items()
   [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

When each key is encountered for the first time, it is not already in the
mapping; so an entry is automatically created using the :attr:`default_factory`
function which returns an empty :class:`list`.  The :meth:`list.append`
operation then attaches the value to the new list.  When keys are encountered
again, the look-up proceeds normally (returning the list for that key) and the
:meth:`list.append` operation adds another value to the list. This technique is
simpler and faster than an equivalent technique using :meth:`dict.setdefault`::

   >>> d = {}
   >>> for k, v in s:
   	d.setdefault(k, []).append(v)

   >>> d.items()
   [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

Setting the :attr:`default_factory` to :class:`int` makes the
:class:`defaultdict` useful for counting (like a bag or multiset in other
languages)::

   >>> s = 'mississippi'
   >>> d = defaultdict(int)
   >>> for k in s:
           d[k] += 1

   >>> d.items()
   [('i', 4), ('p', 2), ('s', 4), ('m', 1)]

When a letter is first encountered, it is missing from the mapping, so the
:attr:`default_factory` function calls :func:`int` to supply a default count of
zero.  The increment operation then builds up the count for each letter. This
technique makes counting simpler and faster than an equivalent technique using
:meth:`dict.get`::

   >>> d = {}
   >>> for k in s:
   	d[k] = d.get(k, 0) + 1

   >>> d.items()
   [('i', 4), ('p', 2), ('s', 4), ('m', 1)]

Setting the :attr:`default_factory` to :class:`set` makes the
:class:`defaultdict` useful for building a dictionary of sets::

   >>> s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
   >>> d = defaultdict(set)
   >>> for k, v in s:
           d[k].add(v)

   >>> d.items()
   [('blue', set([2, 4])), ('red', set([1, 3]))]

