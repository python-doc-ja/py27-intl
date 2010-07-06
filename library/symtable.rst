:mod:`symtable` --- コンパイラの記号表へのアクセス
==========================================================

.. module:: symtable
   :synopsis: コンパイラ内部の記号表へのインターフェイス。

.. moduleauthor:: Jeremy Hylton <jeremy@alum.mit.edu>
.. sectionauthor:: Benjamin Peterson


記号表(symbol table)が作られるのはコンパイラが AST からバイトコードを生成する直前です。
記号表はコード中の全ての識別子のスコープの算出に責任を持ちます。
:mod:`symtable` はこうした記号表を調べるインターフェイスを提供します。


記号表の作成
------------

.. function:: symtable(code, filename, compile_type)

   Python ソース *code* に対するトップレベルの :class:`SymbolTable`
   を返します。 *filename* はコードを収めてあるファイルの名前です。
   *compile_type* は :func:`compile` の *mode* 引数のようなものです。


記号表の検査
------------

.. class:: SymbolTable

   ブロックに対する名前空間の表。
   コンストラクタはパブリックではありません。

   .. method:: get_type()

      記号表の型を返します。
      有り得る値は ``'class'``, ``'module'``, ``'function'`` です。

   .. method:: get_id()

      表の識別子を返します。

   .. method:: get_name()

      表の名前を返します。この名前は表がクラスに対するものであればクラス名であり、
      関数に対するものであれば関数名であり、グローバルな (:meth:`get_type` が
      ``'module'`` を返す) 表であれば ``'top'`` です。

   .. method:: get_lineno()

      この表が表しているブロックの一行目の行番号を返します。

   .. method:: is_optimized()

      この表の locals が最適化できるならば ``True`` を返します。

   .. method:: is_nested()

      ブロックが入れ子のクラスまたは関数のとき ``True`` を返します。

   .. method:: has_children()

      ブロックが入れ子の名前空間を抱えているならば ``True`` を返します。
      入れ子の名前空間は :meth:`get_children` で得られます。

   .. method:: has_exec()

      ブロックの中で ``exec`` が使われているならば ``True`` を返します。

   .. method:: has_import_start()

      ブロックの中でアスタリスクの from-import が使われているならば
      ``True`` を返します。

   .. method:: get_identifiers()

      この表にある記号の名前のリストを返します。

   .. method:: lookup(name)

      表から *name* を見つけ出して :class:`Symbol` インスタンスとして返します。

   .. method:: get_symbols()

      表中の名前を表す :class:`Symbol` インスタンスのリストを返します。

   .. method:: get_children()

      入れ子になった記号表のリストを返します。


.. class:: Function

   関数またはメソッドの名前空間。
   このクラスは :class:`SymbolTable` を継承しています。

   .. method:: get_parameters()

      この関数の引数名からなるタプルを返します。

   .. method:: get_locals()

      この関数のローカルな名前からなるタプルを返します。

   .. method:: get_globals()

      この関数のグローバルな名前からなるタプルを返します。

   .. method:: get_frees()

      この関数の自由変数の名前からなるタプルを返します。


.. class:: Class

   クラスの名前空間。
   このクラスは :class:`SymbolTable` を継承しています。

   .. method:: get_methods()

      このクラスで宣言されているメソッド名からなるタプルを返します。


.. class:: Symbol

   :class:`SymbolTable` のエントリーでソースの識別子に対応するものです。
   コンストラクタはパブリックではありません。

   .. method:: get_name()

      記号の名前を返します。

   .. method:: is_referenced()

      記号がブロックの中で使われていれば ``True`` を返します。

   .. method:: is_imported()

      記号が import 文で作られたものならば ``True`` を返します。

   .. method:: is_parameter()

      記号がパラメータならば ``True`` を返します。

   .. method:: is_global()

      記号がグローバルならば ``True`` を返します。

   .. method:: is_local()

      記号がブロックのローカルならば ``True`` を返します。

   .. method:: is_free()

      記号がブロックの中で参照されても代入は行われないならば ``True`` を返します。

   .. method:: is_assigned()

      記号がブロックの中で代入されているならば ``True`` を返します。

   .. method:: is_namespace()

      名前の束縛が新たな名前空間を導入するならば ``True`` を返します。

      名前が関数またはクラス文のターゲットとして使われるならば、真です。

      一つの名前が複数のオブジェクトに束縛されうることに注意しましょう。
      結果が ``True`` であったとしても、その名前が他のオブジェクトにも束縛され、
      それがたとえば整数やリストであれば、そこでは新たな名前空間は導入されません。

   .. method:: get_namespaces()

      この名前に束縛された名前空間のリストを返します。

   .. method:: get_namespace()

      この名前に束縛されたただ一つの名前空間を返します。
      束縛された名前空間が一つより多くあれば :exc:`ValueError` が送出されます。
