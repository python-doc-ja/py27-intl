
:mod:`__builtin__` --- 組み込みオブジェクト
===========================================

.. module:: __builtin__
   :synopsis: 組み込み名前空間を提供するモジュール


.. This module provides direct access to all 'built-in' identifiers of Python; for
.. example, ``__builtin__.open`` is the full name for the built-in function
.. :func:`open`.

このモジュールはPythonの全ての「組み込み」識別子を直接アクセスするためのものです。
例えば ``__builtin__.open`` は :func:`open` 関数のための全ての組み込み関数を表示します。


.. This module is not normally accessed explicitly by most applications, but can be
.. useful in modules that provide objects with the same name as a built-in value,
.. but in which the built-in of that name is also needed.  For example, in a module
.. that wants to implement an :func:`open` function that wraps the built-in
.. :func:`open`, this module can be used directly:

このモジュールは通常ほとんどのアプリケーションにおいて直接名指しでアクセスされることはありませんが、
組み込みの名前と同じ名前のオブジェクトを提供しつつ組み込みのその名前も必要であるようなモジュールにおいて有用です。
たとえば、 :func:`open` という関数を組み込みの :func:`open` をラップして実装したいというモジュールがあったとすると、
このモジュールは次のように直接的に使われます。


::

   import __builtin__

   def open(path):
       f = __builtin__.open(path, 'r')
       return UpperCaser(f)

   class UpperCaser:
       '''Wrapper around a file that converts output to upper-case.'''

       def __init__(self, f):
           self._f = f

       def read(self, count=-1):
           return self._f.read(count).upper()

       # ...


.. impl-detail::

   .. Most modules have the name ``__builtins__`` (note the ``'s'``) made available
   .. as part of their globals.  The value of ``__builtins__`` is normally either
   .. this module or the value of this modules's :attr:`__dict__` attribute.  Since
   .. this is an implementation detail, it may not be used by alternate
   .. implementations of Python.

   ほとんどのモジュールでは ``__builtins__`` (``'s'`` に注意) がグローバルの一部として
   使えるようになっています。 ``__builtins__`` の内容は通常このモジュールそのものか、またはこのモジュールの :attr:`__dict__`
   属性です。実装の詳細部分ということで、異なる Python の実装の下ではこのようになっていないかもしれません。

