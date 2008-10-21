
:mod:`contextlib` --- :keyword:`with`\ -構文 コンテキストのためのユーティリティ。
=================================================================================

.. module:: contextlib
   :synopsis: with-構文 コンテキストのためのユーティリティ。


.. versionadded:: 2.5

このモジュールは:keyword:`with`文を必要とする一般的なタスクのための ユーティリティを提供します。

用意されている関数:


.. function:: contextmanager(func)

   この関数はデコレータであり、:keyword:`with`文コンテキストマネージャのための ファクトリ関数の定義に利用できます。
   ファクトリ関数を定義するために、クラスあるいは 別の:meth:`__enter__`と:meth:`__exit__`メソッドを作る必要はありません。

   簡単な例（実際にHTMLを生成する方法としてはお勧めできません！）::

      from __future__ import with_statement
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

   デコレートされた関数は呼び出されたときにジェネレータ-イテレータを返します。 このイテレータは値をちょうど一つyieldしなければなりません。
   :keyword:`with`文の:keyword:`as`節が存在するなら、 その値がas節のターゲットへ束縛されることになります。

   ジェネレータがyieldするところで、:keyword:`with`文のネストされたブロックが実行されます。
   ジェネレータはブロックから出た後に再開されます。ブロック内で処理されない例外が発生した場合は、 yieldが起きた場所でジェネレータ内部へ再送出されます。
   このように、（もしあれば）エラーを捕捉したり、後片付け処理を確実に実行したりするために、 :keyword:`try`...\
   :keyword:`except`...\ :keyword:`finally`文を使うことができます。
   単に例外のログをとるためだけに、もしくは（完全に例外を抑えてしまうのではなく）
   あるアクションを実行するだけに例外を捕まえるなら、ジェネレータはその例外を再送出しなければなりません。
   そうしないと、ジェネレータコンテキストマネージャは例外が処理された:keyword:`with`文を指しており、
   その:keyword:`with`文のすぐ後につづく文から実行を再開します。


.. function:: nested(mgr1[, mgr2[, ...]])

   複数のコンテキストマネージャを一つのネストされたコンテキストマネージャへ結合します。

   このようなコードは::

      from contextlib import nested

      with nested(A, B, C) as (X, Y, Z):
          do_something()

   これと同等です::

      with A as X:
          with B as Y:
              with C as Z:
                  do_something()

   ネストされたコンテキストマネージャの一つの:meth:`__exit__`メソッドに 止めるべき例外がある場合は、残りの外側のコンテキストマネージャすべてに
   例外情報が渡されないということに注意してください。 同じように、ネストされたマネージャの一つの:meth:`__exit__`メソッドが
   例外を送出したならば、どんな以前の例外状態も失われ、 新しい例外が残りすべての外側にあるコンテキストマネージャの
   :meth:`__exit__`メソッドに渡されます。 一般的に:meth:`__exit__`メソッドが例外を送出することは避けるべきであり、
   特に渡された例外を再送出すべきではありません。

.. _context-closing:


.. function:: closing(thing)

   ブロックの完了時に*thing*を閉じるコンテキストマネージャを返します。 これは基本的に以下と等価です::

      from contextlib import contextmanager

      @contextmanager
      def closing(thing):
          try:
              yield thing
          finally:
              thing.close()

   そして、明確に``page``を閉じる必要なしに、このように書くことができます::

      from __future__ import with_statement
      from contextlib import closing
      import codecs

      with closing(urllib.urlopen('http://www.python.org')) as page:
          for line in page:
              print line

   たとえエラーが発生したとしても、:keyword:`with`ブロックを出るときに ``page.close()``が呼ばれます。


.. seealso::

   :pep:`0343` - The "with" statement
      仕様、背景、および、Python :keyword:`with`文の例。

