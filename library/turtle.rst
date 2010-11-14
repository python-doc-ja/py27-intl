]


:mod:`turtle` --- Tkのためのタートルグラフィックス
==================================================

.. module:: turtle
   :platform: Tk
   :synopsis: タートルグラフィックスのための環境。
.. moduleauthor:: Guido van Rossum <guido@python.org>


.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>


:mod:`turtle` モジュールはオブジェクト指向と手続き指向の両方の方法でタートルグラフィックス・プリミティブを提供します。グラフィックスの基礎として :mod:`Tkinter` を使っているために、TkをサポートしたPythonのバージョンが必要です。

手続き型インターフェイスでは、関数のどれかが呼び出されたときに自動的に作られるペンとキャンバスを使います。

:mod:`turtle` モジュールは次の関数を定義しています:


.. function:: degrees()

   角度を計る単位を度にします。


.. function:: radians()

   角度を計る単位をラジアンにします。


.. function:: setup(**kwargs)

   メインウインドウの大きさと位置を設定します。キーワードは：

* ``width`` : ピクセル数かスクリーンに対する割合での大きさ。デフォルトはスクリーンの 50% です。

* ``height`` : ピクセル数かスクリーンに対する割合での大きさ。デフォルトはスクリーンの 50% です。

* ``startx`` : スクリーン左端からのピクセル数での開始位置。 ``None`` はデフォルト値で、スクリーンの水平方向にセンタリングします。

* ``starty`` : スクリーン左端からのピクセル数での開始位置。 ``None`` はデフォルト値で、スクリーンの垂直方向にセンタリングします。

   例： ::

      # デフォルトのジオメトリを利用：スクリーンの 50% x 50%、センタリング。
      setup()  

      # ウインドウを 200x200 ピクセル、スクリーンの左上。
      setup (width=200, height=200, startx=0, starty=0)

      # ウインドウをスクリーンの 75% x 50% にして、センタリング。
      setup(width=.75, height=0.5, startx=None, starty=None)


.. function:: title(title_str)

   ウインドウのタイトルを *title* に設定します。


.. function:: done()

   Tk のメインループに入ります。ウインドウは、クローズされるか、プロセスが kill されるまで表示され続けます。


.. function:: reset()

   スクリーンを消去し、ペンを中心に持って行き、変数をデフォルト値に設定します。


.. function:: clear()

   スクリーンを消去します。


.. function:: tracer(flag)

   トレースをon/offにします(フラグが真かどうかに応じて)。トレースとは、線に沿って矢印のアニメーションが付き、線がよりゆっくりと引かれることを意味します。


.. function:: speed(speed)

   タートルのスピードを設定します。 *speed* パラメータに適切な値は ``'fastest'`` （ウェイト無し）、 ``'fast'`` （5ms
   のウェイト）、 ``'normal'`` （10ms のウェイト）、 ``'slow'`` （15ms のウェイト）、それと ``'slowest'``
   （20ms のウェイト）です。

   .. versionadded:: 2.5


.. function:: delay(delay)

   タートルのスピードを *delay* に設定します。これは ms で与えます。

   .. versionadded:: 2.5


.. function:: forward(distance)

   *distance* ステップだけ前に進みます。


.. function:: backward(distance)

   *distance* ステップだけ後ろに進みます。


.. function:: left(angle)

   *angle* 単位だけ左に回ります。単位のデフォルトは度ですが、 :func:`degrees` と :func:`radians` 関数を使って設定できます。


.. function:: right(angle)

   *angle* 単位だけ右に回ります。単位のデフォルトは度ですが、 :func:`degrees` と :func:`radians` 関数を使って設定できます。


.. function:: up()

   ペンを上げます --- 線を引くことを止めます。


.. function:: down()

   ペンを下げます --- 移動したときに線を引きます。


.. function:: width(width)

   線幅を *width* に設定します。


.. function:: color(s)
              color((r, g, b))
              color(r, g, b)

   ペンの色を設定します。最初の形式では、色は文字列としてTkの色の仕様の通りに指定されます。二番目の形式は色をRGB値(それぞれは範囲[0..1])のタプルとして指定します。三番目の形式では、色は三つに別れたパラメータとしてRGB値(それぞれは範囲[0..1])を与えて指定しています。


.. function:: write(text[, move])

   現在のペンの位置に *text* を書き込みます。 *move* が真ならば、ペンはテキストの右下の角へ移動します。デフォルトでは、 *move* は偽です。


.. function:: fill(flag)

   完全な仕様はかなり複雑ですが、推奨する使い方は:
   塗りつぶしたい経路を描く前に ``fill(1)`` を呼び出し、経路を描き終えたときに ``fill(0)`` を呼び出します。


.. function:: begin_fill()

   タートルを塗りつぶしモードにします。後には、対応する end_fill() 呼び出しが続かなければいけません。さもないと、これは無視されてしまいます。

   .. versionadded:: 2.5


.. function:: end_fill()

   塗りつぶしモードを終了し、図形を塗りつぶします； ``fill(0)`` と等価です。 End filling mode, and fill the
   shape; equivalent to ``fill(0)``.

   .. versionadded:: 2.5


.. function:: circle(radius[, extent])

   半径 *radius* 、中心がタートルの左 *radius* ユニットの円を描きます。 *extent* は円のどの部分を描くかを決定します:
   与えられなければ、デフォルトで完全な円になります。

   *extent* が完全な円である場合は、弧の一つの端点は、現在のペンの位置です。 *radius* が正の場合、弧は反時計回りに描かれます。そうでなければ、時計回りです。


.. function:: goto(x, y)
              goto((x, y))

   座標 *x*, *y* へ移動します。座標は二つの別個の引数か、2-タプルのどちらかで指定することができます。


.. function:: towards(x, y)

   タートルの位置から点 *x* 、 *y* までの線の角度を返します。この座標は二つの別々の引数、2タプルまたは別のペンオブジェクトとして指定できます。

   .. versionadded:: 2.5


.. function:: heading()

   タートルの現在の向きを返します。

   .. versionadded:: 2.3


.. function:: setheading(angle)

   タートルの向きを *angle* に設定します。

   .. versionadded:: 2.3


.. function:: position()

   タートルの現在の位置を ``(x,y)`` のペアで返します。

   .. versionadded:: 2.3


.. function:: setx(x)

   タートルの x 座標を *x* に設定します。

   .. versionadded:: 2.3


.. function:: sety(y)

   タートルの y 座標を *y* に設定します。 Set the y coordinate of the turtle to *y*.

   .. versionadded:: 2.3


.. function:: window_width()

   キャンバスウインドウの幅を返します。

   .. versionadded:: 2.3


.. function:: window_height()

   キャンバスウインドウの高さを返します。

   .. versionadded:: 2.3

このモジュールは``from math import
*``も実行します。従って、タートルグラフィックスのために役に立つ追加の定数と関数については、 :mod:`math` モジュールのドキュメントを参照してください。


.. function:: demo()

   モジュールをちょっとばかり試しています。


.. exception:: Error

   このモジュールによって捕捉されたあらゆるエラー対して発生した例外。

例として、 :func:`demo` 関数のコードを参照してください。

このモジュールは次のクラスを定義します:


.. class:: Pen()

   ペンを定義します。上記のすべての関数は与えられたペンのメソッドとして呼び出されます。このコンストラクタは線を描くキャンバスを自動的に作成します。


.. class:: Turtle()

   ペンを定義します。これは基本的に ``Pen()`` と同義です;  :class:`Turtle` は、 :class:`Pen` の空の派生クラスです。


.. class:: RawPen(canvas)

   キャンバス *canvas* に描くペンを定義します。これは"実際の"プログラムでグラフィックスを作成するためにモジュールを使いたい場合に役に立ちます。


.. _pen-rawpen-objects:

Turtle、Pen と RawPen オブジェクト
----------------------------------

モジュールで利用可能なグローバル関数の大部分は :class:`Turtle` 、 :class:`Pen` や :class:`RawPen`
のメソッドとしても利用可能で、これは特定のペンの状態にだけ影響します。

メソッドとして強力になっているメソッドは :func:`degrees` だけで、これは1回転相当の単位数を指定できるオプション引数を取ります。


.. method:: Turtle.degrees([fullcircle])

   *fullcircle* はデフォルトで360です。たとえ *fullcircle* にラジアンで2\*$π、あるいは度で400を与えようとも、これはペンがどんな角度単位でも取ることができるようにしています。

