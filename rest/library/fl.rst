
:mod:`fl` --- グラフィカルユーザーインターフェースのためのFORMSライブラリ
=========================================================================

.. module:: fl
   :platform: IRIX
   :synopsis: グラフィカルユーザーインターフェースのためのFORMSライブラリ。


.. index::
   single: Overmars, Mark
   single: FORMS Library

このモジュールは、Mark OvermarsによるFORMS Library へのインターフェースを提供します。
FORMSライブラリのソースはanonymous ftp ``ftp.cs.ruu.nl``の :file:`SGI/FORMS`ディレクトリから入手できます。
最新のテストはバージョン2.0bで行いました。

ほとんどの関数は接頭辞の``fl_``を取ると、対応するCの関数名になりま す。 ライブラリで使われる定数は後述の:mod:`FL`モジュールで
定義されています。

Pythonでこのオブジェクトを作る方法はCとは少し違っています： ライブラリに保持された'現在のフォーム'に新しいFORMSオブジェクトを加える
のではなく、フォームにFORMSオブジェクトを加えるには、フォームを示す Pythonオブジェクトのメソッドで全て行います。
したがって、Cの関数の:cfunc:`fl_addto_form`と :cfunc:`fl_end_form`に相当するものはPythonにはありませんし、
:cfunc:`fl_bgn_form`に相当するものとしては:func:`fl.make_form` を呼び出します。

用語のちょっとした混乱に注意してください： FORMSではフォームの中に置くことができるボタン、スライダーなどに :dfn:`object`の用語を使います。
Pythonでは全ての値が'オブジェクト'です。 FORMSへのPythonのインターフェースによって、2つの新しいタイプのPythonオブ
ジェクト：フォームオブジェクト（フォーム全体を示します）とFORMSオブジェ クト（ボタン、スライダーなどの一つひとつを示します）を作ります。
おそらく、混乱するほどのことではありません。

FORMSへのPythonインターフェースに'フリーオブジェクト'はありませんし、 Pythonでオブジェクトクラスを書いて加える簡単な方法もありません。
しかし、GLイベントハンドルへのFORMSインターフェースが利用可能で、純粋な GLウィンドウにFORMSを組み合わせることができます。

** 注意：**  :mod:`fl`をインポートすると、GLの関数:cfunc:`foreground`と
FORMSのルーチン:cfunc:`fl_init`を呼び出します。


:mod:`fl`モジュールに定義されている関数
---------------------------------------

.. _fl functions:

:mod:`fl`モジュールには以下の関数が定義されています。 これらの関数の働きに関する詳しい情報については、FORMSドキュメントで対応
するCの関数の説明を参照してください。


.. function:: make_form(type, width, height)

   与えられたタイプ、幅、高さでフォームを作ります。 これは:dfn:`form`オブジェクトを返します。このオブジェクトは後述のメソッド を持ちます。


.. function:: do_forms()

   標準のFORMSのメインループです。 ユーザからの応答が必要なFORMSオブジェクトを示すPythonオブジェクト、ある
   いは特別な値:const:`FL.EVENT`を返します。


.. function:: check_forms()

   FORMSイベントを確認します。 :func:`do_forms`が返すもの、あるいはユーザからの応答をすぐに必要と
   するイベントがないなら``None``を返します。


.. function:: set_event_call_back(function)

   イベントのコールバック関数を設定します。


.. function:: set_graphics_mode(rgbmode, doublebuffering)

   グラフィックモードを設定します。


.. function:: get_rgbmode()

   現在のRGBモードを返します。 これはCのグローバル変数:cdata:`fl_rgbmode`の値です。


.. function:: show_message(str1, str2, str3)

   3行のメッセージとOKボタンのあるダイアログボックスを表示します。


.. function:: show_question(str1, str2, str3)

   3行のメッセージとYES、NOのボタンのあるダイアログボックスを表示します。 ユーザによってYESが押されたら``1``、NOが押されたら``0``を返しま
   す。


.. function:: show_choice(str1, str2, str3, but1[, but2[, but3]])

   3行のメッセージと最大3つまでのボタンのあるダイアログボックスを表示しま す。 ユーザによって押されたボタンの数値を返します（それぞれ``1``、``2``
   、``3``）。


.. function:: show_input(prompt, default)

   1行のプロンプトメッセージと、ユーザが入力できるテキストフィールドを持つ ダイアログボックスを表示します。 2番目の引数はデフォルトで表示される入力文字列です。
   ユーザが入力した文字列が返されます。


.. function:: show_file_selector(message, directory, pattern,  default)

   ファイル選択ダイアログを表示します。 ユーザによって選択されたファイルの絶対パス、あるいはユーザがCancelボタン を押した場合は``None``を返します。


.. function:: get_directory()
              get_pattern()
              get_filename()

   これらの関数は最後にユーザが:func:`show_file_selector`で選択した ディレクトリ、パターン、ファイル名（パスの末尾のみ）を返します。


.. function:: qdevice(dev)
              unqdevice(dev)
              isqueued(dev)
              qtest()
              qread()
              qreset()
              qenter(dev, val)
              get_mouse()
              tie(button, valuator1, valuator2)

   これらの関数は対応するGL関数へのFORMSのインターフェースです。 :func:`fl.do_events`を使っていて、自分で何かGLイベントを操作したい
   ときにこれらを使います。 FORMSが扱うことのできないGLイベントが検出されたら
   :func:`fl.do_forms`が特別の値:const:`FL.EVENT`を返すので、
   :func:`fl.qread`を呼び出して、キューからイベントを読み込むべきで す。 対応するGLの関数は使わないでください！

   .. % \funcline{blkqread}{?}


.. function:: color()
              mapcolor()
              getmcolor()

   FORMSドキュメントにある:cfunc:`fl_color`、 :cfunc:`fl_mapcolor`、:cfunc:`fl_getmcolor`
   の記述を参照してください。


.. _form-objects:

フォームオブジェクト
--------------------

フォームオブジェクト（上で述べた:func:`make_form`で返されます）には 下記のメソッドがあります。
各メソッドは名前の接頭辞に``fl_``を付けたCの関数に対応します；また、 最初の引数はフォームのポインタです；
説明はFORMSの公式文書を参照してください。

全ての:meth:`add_\*`メソッドは、FORMSオブジェクトを示すPythonオブジェ クトを返します。
FORMSオブジェクトのメソッドを以下に記載します。 ほとんどのFORMSオブジェクトは、そのオブジェクトの種類ごとに特有のメソッ ドもいくつか持っています。


.. method:: form.show_form(placement, bordertype, name)

   フォームを表示します。


.. method:: form.hide_form()

   フォームを隠します。


.. method:: form.redraw_form()

   フォームを再描画します。


.. method:: form.set_form_position(x, y)

   フォームの位置を設定します。


.. method:: form.freeze_form()

   フォームを固定します。


.. method:: form.unfreeze_form()

   固定したフォームの固定を解除します。


.. method:: form.activate_form()

   フォームをアクティベートします。


.. method:: form.deactivate_form()

   フォームをディアクティベートします。


.. method:: form.bgn_group()

   新しいオブジェクトのグループを作ります；グループオブジェクトを返します。


.. method:: form.end_group()

   現在のオブジェクトのグループを終了します。


.. method:: form.find_first()

   フォームの中の最初のオブジェクトを見つけます。


.. method:: form.find_last()

   フォームの中の最後のオブジェクトを見つけます。

.. % ---


.. method:: form.add_box(type, x, y, w, h, name)

   フォームにボックスオブジェクトを加えます。 特別な追加のメソッドはありません。


.. method:: form.add_text(type, x, y, w, h, name)

   フォームにテキストオブジェクトを加えます。 特別な追加のメソッドはありません。

.. % \begin{methoddesc}[form]{add_bitmap}{type, x, y, w, h, name}
.. % Add a bitmap object to the form.
.. % \end{methoddesc}


.. method:: form.add_clock(type, x, y, w, h, name)

   フォームにクロックオブジェクトを加えます。 ---  メソッド： :meth:`get_clock`。

.. % ---


.. method:: form.add_button(type, x, y, w, h,  name)

   フォームにボタンオブジェクトを加えます。 ---  メソッド： :meth:`get_button`、 :meth:`set_button`。


.. method:: form.add_lightbutton(type, x, y, w, h, name)

   フォームにライトボタンオブジェクトを加えます。 ---  メソッド： :meth:`get_button`、 :meth:`set_button`。


.. method:: form.add_roundbutton(type, x, y, w, h, name)

   フォームにラウンドボタンオブジェクトを加えます。 ---  メソッド： :meth:`get_button`、 :meth:`set_button`。

.. % ---


.. method:: form.add_slider(type, x, y, w, h, name)

   フォームにスライダーオブジェクトを加えます。 ---  メソッド： :meth:`set_slider_value`、
   :meth:`get_slider_value`、 :meth:`set_slider_bounds`、 :meth:`get_slider_bounds`、
   :meth:`set_slider_return`、 :meth:`set_slider_size`、
   :meth:`set_slider_precision`、 :meth:`set_slider_step`。


.. method:: form.add_valslider(type, x, y, w, h, name)

   フォームにバリュースライダーオブジェクトを加えます。 ---  メソッド： :meth:`set_slider_value`、
   :meth:`get_slider_value`、 :meth:`set_slider_bounds`、 :meth:`get_slider_bounds`、
   :meth:`set_slider_return`、 :meth:`set_slider_size`、
   :meth:`set_slider_precision`、 :meth:`set_slider_step`。


.. method:: form.add_dial(type, x, y, w, h, name)

   フォームにダイアルオブジェクトを加えます。 ---  メソッド： :meth:`set_dial_value`、 :meth:`get_dial_value`、
   :meth:`set_dial_bounds`、 :meth:`get_dial_bounds`。


.. method:: form.add_positioner(type, x, y, w, h, name)

   フォームに2次元ポジショナーオブジェクトを加えます。 ---  メソッド： :meth:`set_positioner_xvalue`、
   :meth:`set_positioner_yvalue`、 :meth:`set_positioner_xbounds`、
   :meth:`set_positioner_ybounds`、 :meth:`get_positioner_xvalue`、
   :meth:`get_positioner_yvalue`、 :meth:`get_positioner_xbounds`、
   :meth:`get_positioner_ybounds`。


.. method:: form.add_counter(type, x, y, w, h, name)

   フォームにカウンタオブジェクトを加えます。 ---  メソッド： :meth:`set_counter_value`、
   :meth:`get_counter_value`、 :meth:`set_counter_bounds`、 :meth:`set_counter_step`,
   :meth:`set_counter_precision`、 :meth:`set_counter_return`。

.. % ---


.. method:: form.add_input(type, x, y, w, h, name)

   フォームにインプットオブジェクトを加えます。 ---  メソッド： :meth:`set_input`、 :meth:`get_input`、
   :meth:`set_input_color`、 :meth:`set_input_return`。

.. % ---


.. method:: form.add_menu(type, x, y, w, h, name)

   フォームにメニューオブジェクトを加えます。 ---  メソッド： :meth:`set_menu`、 :meth:`get_menu`、
   :meth:`addto_menu`。


.. method:: form.add_choice(type, x, y, w, h, name)

   フォームにチョイスオブジェクトを加えます。 ---  メソッド： :meth:`set_choice`、 :meth:`get_choice`、
   :meth:`clear_choice`、 :meth:`addto_choice`、 :meth:`replace_choice`、
   :meth:`delete_choice`、 :meth:`get_choice_text`、 :meth:`set_choice_fontsize`、
   :meth:`set_choice_fontstyle`。


.. method:: form.add_browser(type, x, y, w, h, name)

   フォームにブラウザオブジェクトを加えます。 ---  メソッド： :meth:`set_browser_topline`、
   :meth:`clear_browser`、 :meth:`add_browser_line`、 :meth:`addto_browser`、
   :meth:`insert_browser_line`、 :meth:`delete_browser_line`、
   :meth:`replace_browser_line`、 :meth:`get_browser_line`、 :meth:`load_browser`、
   :meth:`get_browser_maxline`、 :meth:`select_browser_line`、
   :meth:`deselect_browser_line`、 :meth:`deselect_browser`、
   :meth:`isselected_browser_line`、 :meth:`get_browser`、
   :meth:`set_browser_fontsize`、 :meth:`set_browser_fontstyle`、
   :meth:`set_browser_specialkey`。

.. % ---


.. method:: form.add_timer(type, x, y, w, h, name)

   フォームにタイマーオブジェクトを加えます。 ---  メソッド： :meth:`set_timer`、 :meth:`get_timer`。

フォームオブジェクトには以下のデータ属性があります；FORMSドキュメントを 参照してください：

+---------------------+-----------------+--------------------------------------------------+
| 名称                | Cの型           | 意味                                             |
+=====================+=================+==================================================+
| :attr:`window`      | int (read-only) | GLウィンドウのid                                 |
+---------------------+-----------------+--------------------------------------------------+
| :attr:`w`           | float           | フォームの幅                                     |
+---------------------+-----------------+--------------------------------------------------+
| :attr:`h`           | float           | フォームの高さ                                   |
+---------------------+-----------------+--------------------------------------------------+
| :attr:`x`           | float           | フォーム左肩のx座標                              |
+---------------------+-----------------+--------------------------------------------------+
| :attr:`y`           | float           | フォーム左肩のy座標                              |
+---------------------+-----------------+--------------------------------------------------+
| :attr:`deactivated` | int             | フォームがディアクティベートされているなら非ゼロ |
+---------------------+-----------------+--------------------------------------------------+
| :attr:`visible`     | int             | フォームが可視なら非ゼロ                         |
+---------------------+-----------------+--------------------------------------------------+
| :attr:`frozen`      | int             | フォームが固定されているなら非ゼロ               |
+---------------------+-----------------+--------------------------------------------------+
| :attr:`doublebuf`   | int             | ダブルバッファリングがオンなら非ゼロ             |
+---------------------+-----------------+--------------------------------------------------+


.. _forms-objects:

FORMSオブジェクト
-----------------

FORMSオブジェクトの種類ごとに特有のメソッドの他に、全てのFORMSオブジェク トは以下のメソッドも持っています：


.. method:: FORMS object.set_call_back(function, argument)

   オブジェクトのコールバック関数と引数を設定します。 オブジェクトがユーザからの応答を必要とするときには、コールバック関数は2
   つの引数、オブジェクトとコールバックの引数とともに呼び出されます。 （コールバック関数のないFORMSオブジェクトは、ユーザからの応答を必要とす
   るときには:func:`fl.do_forms`あるいは:func:`fl.check_forms`に よって返されます。）
   引数なしにこのメソッドを呼び出すと、コールバック関数を削除します。


.. method:: FORMS object.delete_object()

   オブジェクトを削除します。


.. method:: FORMS object.show_object()

   オブジェクトを表示します。


.. method:: FORMS object.hide_object()

   オブジェクトを隠します。


.. method:: FORMS object.redraw_object()

   オブジェクトを再描画します。


.. method:: FORMS object.freeze_object()

   オブジェクトを固定します。


.. method:: FORMS object.unfreeze_object()

   固定したオブジェクトの固定を解除します。

FORMSオブジェクトには以下のデータ属性があります；FORMSドキュメントを参照 してください。

.. % \begin{methoddesc}[FORMS object]{handle_object}{} XXX
.. % \end{methoddesc}
.. % \begin{methoddesc}[FORMS object]{handle_object_direct}{} XXX
.. % \end{methoddesc}

+--------------------+-----------------+---------------------------+
| 名称               | Cの型           | 意味                      |
+====================+=================+===========================+
| :attr:`objclass`   | int (read-only) | オブジェクトクラス        |
+--------------------+-----------------+---------------------------+
| :attr:`type`       | int (read-only) | オブジェクトタイプ        |
+--------------------+-----------------+---------------------------+
| :attr:`boxtype`    | int             | ボックスタイプ            |
+--------------------+-----------------+---------------------------+
| :attr:`x`          | float           | 左肩のx座標               |
+--------------------+-----------------+---------------------------+
| :attr:`y`          | float           | 左肩のy座標               |
+--------------------+-----------------+---------------------------+
| :attr:`w`          | float           | 幅                        |
+--------------------+-----------------+---------------------------+
| :attr:`h`          | float           | 高さ                      |
+--------------------+-----------------+---------------------------+
| :attr:`col1`       | int             | 第1の色                   |
+--------------------+-----------------+---------------------------+
| :attr:`col2`       | int             | 第2の色                   |
+--------------------+-----------------+---------------------------+
| :attr:`align`      | int             | 配置                      |
+--------------------+-----------------+---------------------------+
| :attr:`lcol`       | int             | ラベルの色                |
+--------------------+-----------------+---------------------------+
| :attr:`lsize`      | float           | ラベルのフォントサイズ    |
+--------------------+-----------------+---------------------------+
| :attr:`label`      | string          | ラベルの文字列            |
+--------------------+-----------------+---------------------------+
| :attr:`lstyle`     | int             | ラベルのスタイル          |
+--------------------+-----------------+---------------------------+
| :attr:`pushed`     | int (read-only) | （FORMSドキュメント参照） |
+--------------------+-----------------+---------------------------+
| :attr:`focus`      | int (read-only) | （FORMSドキュメント参照） |
+--------------------+-----------------+---------------------------+
| :attr:`belowmouse` | int (read-only) | （FORMSドキュメント参照） |
+--------------------+-----------------+---------------------------+
| :attr:`frozen`     | int (read-only) | （FORMSドキュメント参照） |
+--------------------+-----------------+---------------------------+
| :attr:`active`     | int (read-only) | （FORMSドキュメント参照） |
+--------------------+-----------------+---------------------------+
| :attr:`input`      | int (read-only) | （FORMSドキュメント参照） |
+--------------------+-----------------+---------------------------+
| :attr:`visible`    | int (read-only) | （FORMSドキュメント参照） |
+--------------------+-----------------+---------------------------+
| :attr:`radio`      | int (read-only) | （FORMSドキュメント参照） |
+--------------------+-----------------+---------------------------+
| :attr:`automatic`  | int (read-only) | （FORMSドキュメント参照） |
+--------------------+-----------------+---------------------------+


:mod:`FL` --- :mod:`fl`モジュールで使用される定数
=================================================

.. module:: FL
   :platform: IRIX
   :synopsis: flモジュールで使用される定数。


このモジュールには、組み込みモジュール:mod:`fl`を使うのに必要なシン ボル定数が定義されています（上記参照）；これらは名前の接頭辞``FL_``が
省かれていることを除いて、Cのヘッダファイル``<forms.h>``に定義されて いるものと同じです。
定義されている名称の完全なリストについては、モジュールのソースをご覧くだ さい。 お勧めする使い方は以下の通りです： ::

   import fl
   from FL import *


:mod:`flp` --- 保存されたFORMSデザインをロードする関数
======================================================

.. module:: flp
   :platform: IRIX
   :synopsis: 保存されたFORMSデザインをロードする関数。


このモジュールには、FORMSライブラリ（上記の:mod:`fl`モジュールを参 照してください）とともに配布される'フォームデザイナー'
（:program:`fdesign`）プログラムで作られたフォームの定義を読み込む関数が 定義されています。

詳しくはPythonライブラリソースのディレクトリの中の:file:`flp.doc`を参照し てください。

XXX　完全な説明をここに書いて！

