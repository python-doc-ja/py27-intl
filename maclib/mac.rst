
:mod:`macpath` --- MacOS のパス操作関数
=======================================

.. module:: macpath
   :synopsis: MacOS のパス操作関数


.. % MacOS path manipulation functions
.. % Could be labeled \platform{Mac}, but the module should work anywhere and
.. % is distributed with the standard library.
.. % MacOS path manipulation functions.

このモジュールは :mod:`os.path` モジュールの Macintosh 9 (およびそれ以前) 用の実装です。これを使用すると、古い形式の
Macintosh のパス名を Mac OS X (あるいはその他の任意のプラットフォーム) 上で扱うことができます。 :mod:`os.path`
のドキュメントに関しては、 Python Library Reference (XXX reference: ../lib/lib.html)を参照してくだ
さい。

.. % % This module is the Mac OS 9 (and earlier) implementation of the \module{os.path}
.. % % module. It can be used to manipulate old-style Macintosh pathnames on Mac OS
.. % % X (or any other platform).
.. % % Refer to the
.. % % \citetitle[../lib/lib.html]{Python Library Reference} for
.. % % documentation of \module{os.path}.

次の関数がこのモジュールで利用できます。 :func:`normcase`、 :func:`normpath`、 :func:`isabs`、
:func:`join`、 :func:`split`、 :func:`isdir`、 :func:`isfile`、 :func:`walk`、
:func:`exists`。 :mod:`os.path` で利用できる他の関数については、ダミーの関数として相当する物が利用できます。

.. % % The following functions are available in this module:
.. % % For other functions available in \module{os.path} dummy counterparts
.. % % are available.

