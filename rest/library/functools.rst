
:mod:`functools` --- 高階関数と呼び出し可能オブジェクトの操作
=============================================================

.. module:: functools
.. moduleauthor:: Peter Harris <scav@blueyonder.co.uk>
.. moduleauthor:: Raymond Hettinger <python@rcn.com>
.. moduleauthor:: Nick Coghlan <ncoghlan@gmail.com>
.. sectionauthor:: Peter Harris <scav@blueyonder.co.uk>


.. % standard library, in Python



.. versionadded:: 2.5

モジュール :mod:`functools` は高階関数、 つまり関数に対する関数、あるいは他の関数を返す関数、のためのものです。
一般に、どんな呼び出し可能オブジェクトでもこのモジュールの目的には関数として扱えます。

モジュール :mod:`functools` では以下の関数を定義します。


.. function:: partial(func[,*args][, **keywords])

   新しい :class:`partial` オブジェクトを返します。 このオブジェクトは呼び出されると位置引数 *args* とキーワード引数
   *keywords* 付きで呼び出された *func* のように振る舞います。 呼び出しに際してさらなる引数が渡された場合、それらは *args*
   に付け加えられます。 追加のキーワード引数が渡された場合には、それらで *keywords* を拡張または上書きします。 大雑把にいうと、次のコードと等価です。
   ::

      def partial(func, *args, **keywords):
          def newfunc(*fargs, **fkeywords):
              newkeywords = keywords.copy()
              newkeywords.update(fkeywords)
              return func(*(args + fargs), **newkeywords)
          newfunc.func = func
          newfunc.args = args
          newfunc.keywords = keywords
          return newfunc

   関数 :func:`partial` は、 関数の引数と/かキーワードの一部を「凍結」した部分適用として使われ、
   簡素化された引数形式をもった新たなオブジェクトを作り出します。 例えば、:func:`partial` を使って *base* 引数のデフォルトが 2 である
   :func:`int` 関数のように振る舞う呼び出し可能オブジェクトを作ることができます。  ::

      >>> basetwo = partial(int, base=2)
      >>> basetwo.__doc__ = 'Convert base 2 string to an int.'
      >>> basetwo('10010')
      18


.. function:: update_wrapper(wrapper, wrapped[, assigned][, updated])

   wrapper 関数を wrapped 関数に見えるようにアップデートします。 オプション引数はタプルで、 元の関数のどの属性が wrapper
   関数の一致する属性に直接書き込まれる(assigned)か、 また wrapper
   関数のどの属性が元の関数の対応する属性でアップデートされる(updated)か、 を指定します。 これらの引数のデフォルト値はモジュール定数
   *WRAPPER_ASSIGNMENTS* (wrapper 関数に名前、モジュールそしてドキュメンテーション文字列を書き込みます) と
   *WRAPPER_UPDATES* (wrapper 関数のインスタンス辞書をアップデートします) です。

   この関数は主に関数を包んで wrapper を返すデコレータ関数の中で使われるよう意図されています。 もし wrapper 関数がアップデートされないとすると、
   返される関数のメタデータは元の関数の定義ではなく wrapper 関数の定義を反映してしまい、 これは典型的に役立たずです。


.. function:: wraps(wrapped[, assigned][, updated])

   これはラッパ関数を定義するときに ``partial(update_wrapper, wrapped=wrapped, assigned=assigned,
   updated=updated)`` を関数デコレータとして呼び出す便宜関数です。  ::

      >>> def my_decorator(f):
      ...     @wraps(f)
      ...     def wrapper(*args, **kwds):
      ...         print 'Calling decorated function'
      ...         return f(*args, **kwds)
      ...     return wrapper
      ...
      >>> @my_decorator
      ... def example():
      ...     print 'Called example function'
      ...
      >>> example()
      Calling decorated function
      Called example function
      >>> example.__name__
      'example'

   このデコレータ・ファクトリーを使わなければ、 上の例中の関数の名前は ``'wrapper'`` となっているところです。


.. _partial-objects:

:class:`partial` オブジェクト
-----------------------------

:class:`partial` オブジェクトは、 :func:`partial` 関数によって作られる呼び出し可能オブジェクトです。
オブジェクトには読み取り専用の属性が三つあります。


.. attribute:: callable.func

   呼び出し可能オブジェクトまたは関数です。 :class:`partial` の呼び出しは新しい引数とキーワードと共に :attr:`func` に転送されます。


.. attribute:: tuple.args

   最左の位置引数で、:class:`partial` オブジェクトの呼び出し時にその呼び出しの際の位置引数の前に追加されます。


.. attribute:: dict.keywords

   :class:`partial` オブジェクトの呼び出し時に渡されるキーワード引数です。

:class:`partial` オブジェクトは :class:`function` オブジェクトのように呼び出し可能で、
弱参照可能で、属性を持つことができます。 重要な相違点もあります。 例えば、:attr:`__name__` と :attr:`__doc__`
両属性は自動では作られません。 また、クラス中で定義された :class:`partial` オブジェクトはスタティックメソッドのように振る舞い、
インスタンスの属性問い合わせの中で束縛メソッドに変換されません。

