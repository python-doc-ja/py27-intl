
:mod:`types` --- 組み込み型の名前
=========================

.. module:: types
   :synopsis: 組み込み型の名前


このモジュールは標準のPythonインタプリタで使われているオブジェクト の型について、名前を定義しています(拡張モジュールで定義されている型を除
く)。このモジュールは``listiterator``型のようなプロセス中に例外 をふくまないので、``from types import
*``のように使っても安全です。このモジュールの 将来のバージョンで追加される名前は、``Type``で終わる予定です。

関数での典型的な利用方法は、以下のように引数の型によって異なる動作をする 場合です::

   from types import *
   def delete(mylist, item):
       if type(item) is IntType:
          del mylist[item]
       else:
          mylist.remove(item)

Python 2.2以降では、:func:`int` や :func:`str`のような
ファクトリ関数は、型の名前となりましたので、:mod:`types`を使用する 必要はなくなりました。上記のサンプルは、以下のように記述する事が
推奨されています。 ::

   def delete(mylist, item):
       if isinstance(item, int):
          del mylist[item]
       else:
          mylist.remove(item)

このモジュールは以下の名前を定義しています。


.. data:: NoneType

   ``None``の型です。


.. data:: TypeType

   .. index:: builtin: type

   typeオブジェクトの型です (:func:`type`などによって返 されます)。


.. data:: BooleanType

   :class:`bool`の``True``と``False``の型です。これは組み込み関数の :func:`bool`のエイリアスです。

   .. % The type of the \class{bool} values \code{True} and \code{False}; this
   .. % is an alias of the built-in \function{bool()} function.
   .. % \versionadded{2.3}


.. data:: IntType

   整数の型です(e.g. ``1``)。


.. data:: LongType

   長整数の型です(e.g. ``1L``)。


.. data:: FloatType

   浮動小数点数の型です(e.g. ``1.0``)。


.. data:: ComplexType

   複素数の型です(e.g. ``1.0j``)。 Pythonが複素数のサポートなしでコンパイルされていた場合には 定義されません。


.. data:: StringType

   文字列の型です(e.g. ``'Spam'``)。


.. data:: UnicodeType

   Unicode文字列の型です(e.g. ``u'Spam'``)。 Pythonがユニコードのサポートなしでコンパイルされていた場合には 定義されません。


.. data:: TupleType

   タプルの型です(e.g. ``(1, 2, 3, 'Spam')``)。


.. data:: ListType

   リストの型です(e.g. ``[0, 1, 2, 3]``)。


.. data:: DictType

   辞書の型です(e.g. ``{'Bacon': 1, 'Ham': 0}``)。


.. data:: DictionaryType

   ``DictType``の別名です。


.. data:: FunctionType

   ユーザー定義の関数またはlambdaの型です。


.. data:: LambdaType

   ``FunctionType``の別名です。


.. data:: GeneratorType

   ジェネレータ関数の呼び出しによって生成されたイテレータオブジェクトの型で す。

   .. versionadded:: 2.2


.. data:: CodeType

   .. index:: builtin: compile

   :func:`compile`関数などによって返されるコード オブジェクトの型です。


.. data:: ClassType

   ユーザー定義のクラスの型です。


.. data:: InstanceType

   ユーザー定義のクラスのインスタンスの型です。


.. data:: MethodType

   ユーザー定義のクラスのインスタンスのメソッドの型です。


.. data:: UnboundMethodType

   ``MethodType``の別名です。


.. data:: BuiltinFunctionType

   :func:`len` や :func:`sys.exit`のような組み込み関数の型です。


.. data:: BuiltinMethodType

   ``BuiltinFunction``の別名です。


.. data:: ModuleType

   モジュールの型です。


.. data:: FileType

   ``sys.stdout``のようなopenされたファイルオブジェクトの型です。


.. data:: XRangeType

   .. index:: builtin: xrange

   :func:`xrange`関数によって返されるrangeオブジェ クトの型です。


.. data:: SliceType

   .. index:: builtin: slice

   :func:`slice`関数によって返されるオブジェクトの 型です。


.. data:: EllipsisType

   ``Ellipsis``の型です。


.. data:: TracebackType

   ``sys.exc_traceback``に含まれるようなトレースバックオブジェクトの型です。


.. data:: FrameType

   フレームオブジェクトの型です。 トレースバックオブジェクト``tb``の``tb.tb_frame``などです。


.. data:: BufferType

   .. index:: builtin: buffer

   :func:`buffer`関数によって作られるバッファオブ ジェクトの型です。


.. data:: DictProxyType

   ``TypeType.__dict__`` のような dictへのプロキシ型です。


.. data:: NotImplementedType

   ``NotImplemented``の型です。


.. data:: GetSetDescriptorType

   ``FrameType.f_locals`` や ``array.array.typecode`` のような ``PyGetSetDef`` のある
   拡張モジュールで定義されたオブジェクトの型です。 この定数は上のような拡張型がないPythonでは定義されません。
   ポータブルなコードでは``hasattr(types, 'GetSetDescriptorType')``を 使用してください。

   .. versionadded:: 2.5


.. data:: MemberDescriptorType

   ``datetime.timedelta.days`` のような ``PyMemberDef``のある 拡張モジュールで定義されたオブジェクトの型です。
   この定数は上のような拡張型がないPythonでは定義されません。 ポータブルなコードでは``hasattr(types,
   'MemberDescriptorType')``を 使用してください。

   .. versionadded:: 2.5


.. data:: StringTypes

   文字列型のチェックを簡単にするための``StringType``と ``UnicodeType``を含むシーケンスです。
   ``UnicodeType``は実行中の版のPythonに含まれている場合にだけ含まれるの
   で、2つの文字列型のシーケンスを使うよりこれを使う方が移植性が高くなります。 例: ``isinstance(s, types.StringTypes)``.

   .. versionadded:: 2.2

