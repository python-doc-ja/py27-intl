
:mod:`__builtin__` --- 組み込みオブジェクト
===========================================

.. module:: __builtin__
   :synopsis: 組み込み名前空間を提供するモジュール


このモジュールはPythonの全ての「組み込み」識別子を直接アクセスするためのものです。
例えば ``__builtin__.open`` は:func:`open` 関数のための 全ての組み込み関数を表示します。
:ref:`builtin` 章も参照してください。

このモジュールは通常ほとんどのアプリケーションにおいて直接名指しでアクセスされることはありませんが、
組み込みの名前と同じ名前のオブジェクトを提供しつつ組み込みのその名前も必要であるようなモジュールにおいて有用です。
たとえば、:func:`open` という関数を組み込みの :func:`open` をラップして実装したいというモジュールがあったとすると、
このモジュールは次のように直接的に使われます。 ::

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

実装の詳細に属することですが、ほとんどのモジュールでは ``__builtins__`` (``'s'`` に注意) がグローバルの一部として
使えるようになっています。 ``__builtins__`` の内容は通常このモジュール そのものか、またはこのモジュールの:attr:`__dict__`
属性です。 実装の詳細部分ということで、異なる Python の実装の下ではこのようになっていないかもしれません。

