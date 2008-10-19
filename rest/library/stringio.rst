
:mod:`StringIO` --- ファイルのように文字列を読み書きする
======================================

.. module:: StringIO
   :synopsis: ファイルのように文字列を読み書きする。


このモジュールは、(*メモリファイル*としても知られている) 文字列のバッファに対して読み書きを行うファイルのようなクラス、 :class:`StringIO`
、を実装しています。

操作方法についてはファイルオブジェクトの説明を参照してください(セクション :ref:`bltin-file-objects`)。


.. class:: StringIO([buffer])

   :class:`StringIO` オブジェクトを作る際に、コンストラクターに文字列を渡すこと で初期化することができます。 文字列を渡さない場合、最初は
   :class:`StringIO` はカラです。 どちらの場合でも最初のファイル位置は 0 から始まります。

   :class:`StringIO` オブジェクトはユニコードも 8-bit の文字列も受け付けますが、 この2つを混ぜることには少し注意が必要です。
   この2つが一緒に使われると、 :meth:`getvalue` が呼ばれたときに、 (8th ビットを使っている)7-bit ASCII に解釈できない
   8-bit の文字列は、 :exc:`UnicodeError` を引き起こします。

次にあげる :class:`StringIO` オブジェクトのメソッドには特別な説明が必要です:


.. method:: StringIO.getvalue()

   :class:`StringIO` オブジェクトの :meth:`close` メソッドが呼ばれる前ならいつでも、 "file" の中身全体を返します。
   ユニコードと 8-bit の文字列を混ぜることの説明は、上の注意を参照してください。 この2つの文字コードを混ぜると、このメソッドは
   :exc:`UnicodeError` を 引き起こすかもしれません。


.. method:: StringIO.close()

   メモリバッファを解放します。

使用例::

   import StringIO

   output = StringIO.StringIO()
   output.write('First line.\n')
   print >>output, 'Second line.'

   # ファイルの内容を取り出す -- ここでは
   # 'First line.\nSecond line.\n'
   contents = output.getvalue()

   # オブジェクトを閉じてメモリバッファを解放する --
   # .getvalue() は例外を送出するようになる。
   output.close()


:mod:`cStringIO` --- 高速化された :mod:`StringIO`
===========================================

.. module:: cStringIO
   :synopsis: StringIOを高速にしたものだが、サブクラス化はできない。
.. moduleauthor:: Jim Fulton <jim@zope.com>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


:mod:`cStringIO` モジュールは :mod:`StringIO` モジュールと同様の インターフェースを提供しています。
:class:`StringIO.StringIO` オブジェクトを酷使する場合、 このモジュールにある  :func:`StringIO`
関数をかわりに使うと効果的です。

このモジュールは、ビルトイン型のオブジェクトを返すファクトリー関数を提供しているので、 サブクラス化して自分用の物を作ることはできません。
そうした場合には、オリジナルの :mod:`StringIO` モジュールを使ってください。

:mod:`StringIO` モジュールで実装されているメモリファイルとは異なり、 このモジュールで提供されているものは、プレイン ASCII
文字列にエンコードできない ユニコードを受け付けることができません。

また、引数に文字列を指定して:func:`StringIO`呼び出すと読み出し専用のオブジェクト が生成されますが、この場合
:class:`cStringIO.StringIO()` では write()メソッドを持たない オブジェクトを生成します。
これらのオブジェクトは普段は見えません。 トレースバックに :class:`StringI` と :class:`StringO` として表示されます。

次にあげるデータオブジェクトも提供されています:


.. data:: InputType

   文字列をパラメーターに渡して :func:`StringIO` を呼んだときに作られるオブジェクトの オブジェクト型。


.. data:: OutputType

   パラメーターを渡さすに :func:`StringIO` を呼んだときに返されるオブジェクトの オブジェクト型。

このモジュールには C API もあります。詳しくはこのモジュールのソースを参照してください。

使用例::

   import cStringIO

   output = cStringIO.StringIO()
   output.write('First line.\n')
   print >>output, 'Second line.'

   # ファイルの内容を取り出す -- ここでは
   # 'First line.\nSecond line.\n'
   contents = output.getvalue()

   # オブジェクトを閉じてメモリバッファを解放する --
   # 以降 .getvalue() は例外を送出するようになる。
   output.close()

