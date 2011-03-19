:mod:`contextlib` --- :keyword:`with` \ -構文コンテキストのためのユーティリティ
===============================================================================

.. module:: contextlib
   :synopsis: with-構文コンテキストのためのユーティリティ。


.. versionadded:: 2.5

.. This module provides utilities for common tasks involving the :keyword:`with`
.. statement. For more information see also :ref:`typecontextmanager` and
.. :ref:`context-managers`.

このモジュールは :keyword:`with` 構文に関わる一般的なタスクのためのユーティリティを提供します。
詳しい情報は、 :ref:`typecontextmanager` と :ref:`context-managers` を参照してください。


.. Functions provided:

提供されている関数:


.. function:: contextmanager(func)

   .. This function is a :term:`decorator` that can be used to define a factory
   .. function for :keyword:`with` statement context managers, without needing to
   .. create a class or separate :meth:`__enter__` and :meth:`__exit__` methods.

   この関数は :keyword:`with` 構文コンテキストマネージャのファクトリ関数を
   定義するためのデコレータ (:term:`decorator`) です。
   新しいクラスを作ったり :meth:`__enter__` と :meth:`__exit__` のメソッドを
   別々にしなくても、ファクトリ関数を定義することができます。


   .. A simple example (this is not recommended as a real way of generating HTML!):

   簡単な例（実際にHTMLを生成する方法としてはお勧めできません！）


   ::

      from contextlib import contextmanager

      @contextmanager
      def tag(name):
          print "<%s>" % name
          yield
          print "</%s>" % name

      >>> with tag("h1"):
      ...    print "foo"
      ...
      <h1>
      foo
      </h1>


   .. The function being decorated must return a :term:`generator`-iterator when
   .. called. This iterator must yield exactly one value, which will be bound to
   .. the targets in the :keyword:`with` statement's :keyword:`as` clause, if any.

   デコレート対象の関数は呼び出されたときにジェネレータ(:term:`generator`)-イテレータを返す必要があります。
   このイテレータは値をちょうど一つ yield しなければなりません。
   :keyword:`with` 構文の :keyword:`as` 節が存在するなら、その値は as 節のターゲットへ束縛されることになります。


   .. At the point where the generator yields, the block nested in the :keyword:`with`
   .. statement is executed.  The generator is then resumed after the block is exited.
   .. If an unhandled exception occurs in the block, it is reraised inside the
   .. generator at the point where the yield occurred.  Thus, you can use a
   .. :keyword:`try`...\ :keyword:`except`...\ :keyword:`finally` statement to trap
   .. the error (if any), or ensure that some cleanup takes place. If an exception is
   .. trapped merely in order to log it or to perform some action (rather than to
   .. suppress it entirely), the generator must reraise that exception. Otherwise the
   .. generator context manager will indicate to the :keyword:`with` statement that
   .. the exception has been handled, and execution will resume with the statement
   .. immediately following the :keyword:`with` statement.

   ジェネレータが yield を実行した箇所で :keyword:`with` 文のネストされたブロックが実行されます。
   ブロックから抜けた後でジェネレータは再開されます。
   ブロック内で処理されない例外が発生した場合は、ジェネレータ内部の yield を実行した箇所で例外が再送出されます。
   このように、（もしあれば）エラーを捕捉したり、クリーンアップ処理を確実に実行したりするために、
   :keyword:`try`...\ :keyword:`except`...\ :keyword:`finally` 構文を使うことができます。
   例外を捕捉する目的が、（完全に例外を抑制してしまうのではなく）
   単に例外のログをとるため、もしくはあるアクションを実行するためなら、
   ジェネレータはその例外を再送出しなければなりません。
   例外を再送出しない場合、ジェネレータコンテキストマネージャは :keyword:`with` 文に対して
   例外が処理されたことを示し、 :keyword:`with` 文の直後の文から実行を再開します。


.. function:: nested(mgr1[, mgr2[, ...]])

   .. Combine multiple context managers into a single nested context manager.

   複数のコンテキストマネージャを一つのネストされたコンテキストマネージャへ結合します。


   .. Code like this:

   このようなコードは


   ::

      from contextlib import nested

      with nested(A(), B(), C()) as (X, Y, Z):
          do_something()


   .. is equivalent to this:

   これと同等です:


   ::

      m1, m2, m3 = A(), B(), C()
      with m1 as X:
          with m2 as Y:
              with m3 as Z:
                  do_something()


   .. Note that if the :meth:`__exit__` method of one of the nested context managers
   .. indicates an exception should be suppressed, no exception information will be
   .. passed to any remaining outer context managers. Similarly, if the
   .. :meth:`__exit__` method of one of the nested managers raises an exception, any
   .. previous exception state will be lost; the new exception will be passed to the
   .. :meth:`__exit__` methods of any remaining outer context managers. In general,
   .. :meth:`__exit__` methods should avoid raising exceptions, and in particular they
   .. should not re-raise a passed-in exception.

   ネストされたコンテキストマネージャのうちのいずれかの :meth:`__exit__` メソッドが
   例外を抑制すべきと判断した場合、外側にある残りのすべてのコンテキストマネージャに
   例外情報が渡されないということに注意してください。同様に、ネストされた
   コンテキストマネージャのうちのいずれかの :meth:`__exit__` メソッドが例外を送出したならば、
   それ以前の例外状態は失われ、新しい例外が外側にある残りのすべての
   コンテキストマネージャの :meth:`__exit__` メソッドに渡されます。
   一般的に :meth:`__exit__` メソッドが例外を送出することは避けるべきであり、
   特に渡された例外を再送出すべきではありません。


.. function:: closing(thing)

   .. Return a context manager that closes *thing* upon completion of the block.  This
   .. is basically equivalent to:

   ブロックの完了時に *thing* を close するコンテキストマネージャを返します。これは基本的に以下と等価です


   ::

      from contextlib import contextmanager

      @contextmanager
      def closing(thing):
          try:
              yield thing
          finally:
              thing.close()


   .. And lets you write code like this:

   そして、明示的に ``page`` を close する必要なしに、このように書くことができます:


   ::

      from contextlib import closing
      import urllib

      with closing(urllib.urlopen('http://www.python.org')) as page:
          for line in page:
              print line


   .. without needing to explicitly close ``page``.  Even if an error occurs,
   .. ``page.close()`` will be called when the :keyword:`with` block is exited.

   たとえエラーが発生したとしても、 :keyword:`with` ブロックを出るときに ``page.close()`` が呼ばれます。


.. seealso::

   :pep:`0343` - The "with" statement

      .. The specification, background, and examples for the Python :keyword:`with`
      .. statement.

      仕様、背景、および、Python :keyword:`with` 文の例。

