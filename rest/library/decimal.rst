
:mod:`decimal` --- 10進浮動小数点数の算術演算
=============================================

.. module:: decimal
   :synopsis: 汎用 10 進数算術仕様 (General Decimal Arithmetic Specification) の実装。


.. moduleauthor:: Eric Price <eprice at tjhsst.edu>
.. moduleauthor:: Facundo Batista <facundo at taniquetil.com.ar>
.. moduleauthor:: Raymond Hettinger <python at rcn.com>
.. moduleauthor:: Aahz <aahz at pobox.com>
.. moduleauthor:: Tim Peters <tim.one at comcast.net>


.. sectionauthor:: Raymond D. Hettinger <python at rcn.com>


.. versionadded:: 2.4

:mod:`decimal` モジュールは10 進の浮動小数点算術をサポートします。 :mod:`decimal` には、 :class:`float()`
データ型に比べて、以下のような 利点があります:

* 10 進数を正確に表現できます。:const:`1.1` のような数は、2 進数の 浮動小数点型では正しく表現できません。エンドユーザは普通、 2
  進数における:const:`1.1` の近似値が:const:`1.1000000000000001`
  だからといって、そのように表示してほしいとは考えないものです。

* 値の正確さは算術にも及びます。10 進の浮動小数点による計算では、 ``0.1 + 0.1 + 0.1 - 0.3`` は厳密にゼロに等しくなります。 2
  進浮動小数点では:const:`5.5511151231257827e-017` になってしまいます。
  ゼロに近い値とはいえ、この誤差は数値間の等価性テストの信頼性を阻害します。 また、誤差が蓄積されることもあります。こうした理由から、数値間の等価性を
  厳しく保たねばならないようなアプリケーションを考えるなら、10 進数による 数値表現が望ましいということになります。

* :mod:`decimal` モジュールでは、有効桁数の表記が取り入れられており、 例えば ``1.30 + 1.20`` は :const:`2.50`
  になります。すなわち、 末尾のゼロは有効数字を示すために残されます。こうした仕様は通貨計算を行う
  アプリケーションでは慣例です。乗算の場合、「教科書的な」アプローチでは、 乗算の被演算子すべての桁数を使います。 例えば、``1.3 * 1.2`` は
  :const:`1.56` になり、 ``1.30 * 1.20`` は :const:`1.5600` になります。

* ハードウェアによる 2 進浮動小数点表現と違い、:mod:`decimal`  モジュールでは計算精度をユーザが指定できます(デフォルトでは 28
  桁です)。 この桁数はほとんどの問題解決に十分な大きさです::

     >>> getcontext().prec = 6
     >>> Decimal(1) / Decimal(7)
     Decimal("0.142857")
     >>> getcontext().prec = 28
     >>> Decimal(1) / Decimal(7)
     Decimal("0.1428571428571428571428571429")

* 2 進と 10 進の浮動小数点は、いずれも広く公開されている標準仕様の もとに実装されています。組み込みの浮動小数点型では、標準仕様で提唱されている
  機能のほんのささやかな部分を利用できるにすぎませんが、 :mod:`decimal`  では標準仕様が要求している全ての機能を利用できます。必要に応じて、
  プログラマは値の丸めやシグナル処理を完全に制御できます。

このモジュールは、 10 進数型、算術コンテキスト (context for arithmetic)、 そしてシグナル (signal)
という三つの概念を中心に設計されています、

10 進数型は変更不可能な型です。この型には符号部、仮数部、そして指数部 があります。有効桁数を残すために、仮数部の末尾にあるゼロの切り詰めは 行われません。
:mod:`decimal` では、 :const:`Infinity`, :const:`-Infinity`, および :const:`NaN`
といった特殊な値も定義されています。 標準仕様では :const:`-0` と :const:`+0` も区別しています。

算術コンテキストとは、精度や値丸めの規則、指数部の制限を決めている 環境です。この環境では、演算結果を表すためのフラグや、演算上発生した
特定のシグナルを例外として扱うかどうかを決めるトラップイネーブラも 定義しています。丸め規則には:const:`ROUND_CEILING`,
:const:`ROUND_DOWN`, :const:`ROUND_FLOOR`, :const:`ROUND_HALF_DOWN`,
:const:`ROUND_HALF_EVEN`, :const:`ROUND_HALF_UP`, および :const:`ROUND_UP` があります。

シグナルとは、演算の過程で生じる例外的条件です。個々のシグナルは、 アプリケーションそれぞれの要求に従って、無視されたり、単なる情報と
みなされたり、例外として扱われたりします。:mod:`decimal` モジュール には、:const:`Clamped`,
:const:`InvalidOperation`, :const:`DivisionByZero`, :const:`Inexact`,
:const:`Rounded`, :const:`Subnormal`, :const:`Overflow`, および :const:`Underflow`
といったシグナルがあります。

各シグナルには、フラグとトラップイネーブラがあります。演算上 何らかのシグナルに遭遇すると、フラグはゼロからインクリメントされて
ゆきます。このとき、もしトラップイネーブラが 1 にセットされて いれば、例外を送出します。フラグの値は膠着型 (sticky) なので、
演算によるフラグの変化をモニタしたければ、予めフラグをリセット しておかねばなりません。


.. seealso::

   IBM による汎用 10 進演算仕様、 `The General Decimal Arithmetic Specification
   <http://www2.hursley.ibm.com/decimal/decarith.html>`_。

   IEEE 標準化仕様 854-1987, `IEEE 854 に関する非公式のテキスト
   <http://www.cs.berkeley.edu/~ejr/projects/754/private/drafts/854-1987/dir.html>`_。

.. % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-tutorial:

Quick-start Tutorial
--------------------

普通、:mod:`decimal` を使うときには、モジュールを import し、現在の 演算コンテキストを :func:`getcontext`
で調べ、必要に応じて 精度や丸めを設定し、演算エラーのトラップを有効にします::

   >>> from decimal import *
   >>> getcontext()
   Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999999, Emax=999999999,
           capitals=1, flags=[], traps=[Overflow, InvalidOperation,
           DivisionByZero])

   >>> getcontext().prec = 7       # 新たな精度を設定

:class:`Decimal` のインスタンスは、整数、文字列またはタプルから生成 できます。:class:`Decimal` を
:class:`float` から生成したければ、まず 文字列型に変換せねばなりません。そうすることで、変換方法の詳細を (representation
error も含めて) 明示的に残せます。 :class:`Decimal` は "数値ではない (Not a Number)" を表す
:const:`NaN` や正負の :const:`Infinity` (無限大)、 :const:`-0` といった特殊な値も表現できます。 ::

   >>> Decimal(10)
   Decimal("10")
   >>> Decimal("3.14")
   Decimal("3.14")
   >>> Decimal((0, (3, 1, 4), -2))
   Decimal("3.14")
   >>> Decimal(str(2.0 ** 0.5))
   Decimal("1.41421356237")
   >>> Decimal("NaN")
   Decimal("NaN")
   >>> Decimal("-Infinity")
   Decimal("-Infinity")

新たな :class:`Decimal` 型数値の有効桁数は入力した数の桁数だけで決まります。
演算コンテキストにおける精度や値丸めの設定が影響するのは算術操作の 中だけです。 ::

   >>> getcontext().prec = 6
   >>> Decimal('3.0')
   Decimal("3.0")
   >>> Decimal('3.1415926535')
   Decimal("3.1415926535")
   >>> Decimal('3.1415926535') + Decimal('2.7182818285')
   Decimal("5.85987")
   >>> getcontext().rounding = ROUND_UP
   >>> Decimal('3.1415926535') + Decimal('2.7182818285')
   Decimal("5.85988")

:class:`Decimal` 型数値はほとんどの場面で Python の他の機能とうまく やりとりできます。 :class:`Decimal`
浮動小数点小劇場 (flying circus) を示しましょう::

   >>> data = map(Decimal, '1.34 1.87 3.45 2.35 1.00 0.03 9.25'.split())
   >>> max(data)
   Decimal("9.25")
   >>> min(data)
   Decimal("0.03")
   >>> sorted(data)
   [Decimal("0.03"), Decimal("1.00"), Decimal("1.34"), Decimal("1.87"),
    Decimal("2.35"), Decimal("3.45"), Decimal("9.25")]
   >>> sum(data)
   Decimal("19.29")
   >>> a,b,c = data[:3]
   >>> str(a)
   '1.34'
   >>> float(a)
   1.3400000000000001
   >>> round(a, 1)     # round() は値をまず二進の浮動小数点数に変換します
   1.3
   >>> int(a)
   1
   >>> a * 5
   Decimal("6.70")
   >>> a * b
   Decimal("2.5058")
   >>> c % a
   Decimal("0.77")

:meth:`quantize` メソッドは位を固定して数値を丸めます。このメソッドは、
計算結果を固定の桁数で丸めることがよくある、通貨を扱うアプリケーションで 便利です::

   >>> Decimal('7.325').quantize(Decimal('.01'), rounding=ROUND_DOWN)
   Decimal("7.32")
   >>> Decimal('7.325').quantize(Decimal('1.'), rounding=ROUND_UP)
   Decimal("8")

前述のように、:func:`getcontext` 関数を使うと現在の演算コンテキスト にアクセスでき、設定を変更できます。ほとんどのアプリケーションはこの
アプローチで十分です。

より高度な作業を行う場合、:func:`Context` コンストラクタを使って 別の演算コンテキストを作っておくと便利なことがあります。
別の演算コンテキストをアクティブにしたければ、:func:`setcontext` を使います。

:mod:`Decimal` モジュールでは、標準仕様に従って、すぐ利用できる 二つの標準コンテキスト、:const:`BasicContext` および
:const:`ExtendedContext` を提供しています。後者はほとんどのトラップが 有効になっており、とりわけデバッグの際に便利です::

   >>> myothercontext = Context(prec=60, rounding=ROUND_HALF_DOWN)
   >>> setcontext(myothercontext)
   >>> Decimal(1) / Decimal(7)
   Decimal("0.142857142857142857142857142857142857142857142857142857142857")

   >>> ExtendedContext
   Context(prec=9, rounding=ROUND_HALF_EVEN, Emin=-999999999, Emax=999999999,
           capitals=1, flags=[], traps=[])
   >>> setcontext(ExtendedContext)
   >>> Decimal(1) / Decimal(7)
   Decimal("0.142857143")
   >>> Decimal(42) / Decimal(0)
   Decimal("Infinity")

   >>> setcontext(BasicContext)
   >>> Decimal(42) / Decimal(0)
   Traceback (most recent call last):
     File "<pyshell#143>", line 1, in -toplevel-
       Decimal(42) / Decimal(0)
   DivisionByZero: x / 0

演算コンテキストには、演算中に遭遇した例外的状況をモニタするための シグナルフラグがあります。フラグが一度セットされると、明示的に
クリアするまで残り続けます。そのため、フラグのモニタを行いたいような 演算の前には:meth:`clear_flags` メソッドでフラグをクリアして
おくのがベストです。 ::

   >>> setcontext(ExtendedContext)
   >>> getcontext().clear_flags()
   >>> Decimal(355) / Decimal(113)
   Decimal("3.14159292")
   >>> getcontext()
   Context(prec=9, rounding=ROUND_HALF_EVEN, Emin=-999999999, Emax=999999999,
           capitals=1, flags=[Inexact, Rounded], traps=[])

*flags* エントリから、:const:`Pi` の有理数による近似値が丸められた (コンテキスト内で決められた精度を超えた桁数が捨てられた) ことと、
計算結果が厳密でない (無視された桁の値に非ゼロのものがあった) ことが わかります。

コンテキストの :attr:`traps` フィールドに入っている辞書を使うと、 個々のトラップをセットできます::

   >>> Decimal(1) / Decimal(0)
   Decimal("Infinity")
   >>> getcontext().traps[DivisionByZero] = 1
   >>> Decimal(1) / Decimal(0)
   Traceback (most recent call last):
     File "<pyshell#112>", line 1, in -toplevel-
       Decimal(1) / Decimal(0)
   DivisionByZero: x / 0

ほとんどのプログラムでは、開始時に一度だけ現在の演算コンテキストを 修正します。また、多くのアプリケーションでは、データから :class:`Decimal`
への変換はループ内で一度だけキャストして行います。コンテキストを設定し、 :class:`Decimal` オブジェクトを生成できたら、ほとんどのプログラムは
他の Python 数値型と全く変わらないかのように:class:`Decimal` を操作できます。

.. % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-decimal:

Decimal オブジェクト
--------------------


.. class:: Decimal([value [, context]])

   *value* に基づいて新たな :class:`Decimal` オブジェクトを構築 します。

   *value* は整数、文字列、タプル、および他の :class:`Decimal`  オブジェクトにできます。*value* を指定しない場合、
   ``Decimal("0")`` を返します。 *value* が文字列の場合、 以下の 10 進数文字列の文法に従わねばなりません::

      sign           ::=  '+' | '-'
      digit          ::=  '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
      indicator      ::=  'e' | 'E'
      digits         ::=  digit [digit]...
      decimal-part   ::=  digits '.' [digits] | ['.'] digits
      exponent-part  ::=  indicator [sign] digits
      infinity       ::=  'Infinity' | 'Inf'
      nan            ::=  'NaN' [digits] | 'sNaN' [digits]
      numeric-value  ::=  decimal-part [exponent-part] | infinity
      numeric-string ::=  [sign] numeric-value | [sign] nan  

   *value* を :class:`tuple` にする場合、タプルは三つの要素を持ち、 それぞれ符号 (正なら:const:`0`、負なら
   :const:`1`)、仮数部を 表す数字のタプル、そして指数を表す整数でなければなりません。 例えば、``Decimal((0, (1, 4, 1, 4),
   -3))`` は ``Decimal("1.414")`` を返します。

   *context* に指定した精度 (precision) は、オブジェクトが記憶する 桁数には影響しません。桁数は *value* に指定した桁数だけから
   決定されます。例えば、演算コンテキストに指定された精度が 3 桁しかなくても、 ``Decimal("3.00000")`` は 5 つのゼロを全て記憶します。

   *context* 引数の目的は、*value* が正しくない形式の文字列 であった場合に行う処理を決めることにあります;
   演算コンテキストが:const:`InvalidOperation` をトラップするように なっていれば、例外を送出します。それ以外の場合には、コンストラクタは
   値が:const:`NaN` の:class:`Decimal` を返します。

   一度生成すると、:class:`Decimal` オブジェクトは変更不能 (immutable)  になります。

10 進浮動小数点オブジェクトは、:class:`float` や:class:`int` のような
他の組み込み型と多くの点で似ています。通常の数学演算や特殊メソッドを 適用できます。また、:class:`Decimal` オブジェクトは
コピーでき、pickle 化でき、print で出力でき、辞書のキーにでき、 集合の要素にでき、比較、保存、他の型 (:class:`float`
や:class:`long`) への型強制を行えます。

こうした標準的な数値型の特性の他に、10進浮動小数点オブジェクトには 様々な特殊メソッドがあります:


.. method:: Decimal.adjusted()

   仮数部の先頭の一桁だけが残るように桁シフトを行い、そのときの指数部を 返します: ``Decimal("321e+5").adjusted()`` なら 7
   です。 最上桁の小数点からの相対位置を調べる際に使います。


.. method:: Decimal.as_tuple()

   数値を表現するためのタプル: ``(sign, digittuple, exponent)`` を返します。


.. method:: Decimal.compare(other[, context])

   :meth:`__cmp__` に似ていますが、:class:`Decimal` インスタンスを 返します。  ::

      a or b is a NaN ==> Decimal("NaN")
      a < b           ==> Decimal("-1")
      a == b          ==> Decimal("0")
      a > b           ==> Decimal("1")


.. method:: Decimal.max(other[, context])

   ``max(self, other)`` と同じですが、値を返す前に現在のコンテキストに 即した丸め規則を適用します。また、  :const:`NaN`
   に対して、(コンテキストでシグナルまたは黙認のどちらが 設定されているかに応じて) シグナルを発行するか無視します。


.. method:: Decimal.min(other[, context])

   ``min(self, other)`` と同じですが、値を返す前に現在のコンテキストに 即した丸め規則を適用します。また、  :const:`NaN`
   に対して、(コンテキストでシグナルまたは黙認のどちらが 設定されているかに応じて) シグナルを発行するか無視します。


.. method:: Decimal.normalize([context])

   数値を正規化 (normalize) して、右端に連続しているゼロを除去し、 :const:`Decimal("0")` と同じ結果はすべて
   :const:`Decimal("0e0")` に変換します。 同じクラスの値から基準表現を生成する際に用います。 たとえば、
   ``Decimal("32.100")`` と ``Decimal("0.321000e+2")`` の正規化は、いずれも同じ値
   ``Decimal("32.1")`` になります。


.. method:: Decimal.quantize(exp [, rounding[, context[, watchexp]]])

   指数部を*exp* と同じにします。値丸めの際、まず*rounding* が あるか調べ、次に*context* を調べ、最後に現在のコンテキストの
   設定を用います。

   *watchexp* が (default) に設定されている場合、処理結果の指数 が :attr:`Emax` よりも大きい場合や :attr:`Etiny`
   よりも小さい 場合にエラーを返します。


.. method:: Decimal.remainder_near(other[, context])

   モジュロを計算し、正負のモジュロのうちゼロに近い値を返します。 たとえば、 ``Decimal(10).remainder_near(6)`` は
   ``Decimal("4")`` よりもゼロに近い値 ``Decimal("-2")`` を返します。

   ゼロからの差が同じ場合には、 *self* と同じ符号を持った方を 返します。


.. method:: Decimal.same_quantum(other[, context])

   *self* と *other* が同じ指数を持っているか、あるいは 双方とも :const:`NaN` である場合に真を返します。


.. method:: Decimal.sqrt([context])

   平方根を精度いっぱいまで求めます。


.. method:: Decimal.to_eng_string([context])

   数値を工学で用いられる形式 (工学表記; enginnering notation)  の文字列に変換します。

   工学表記では指数は 3 の倍数になります。従って、 最大で 3 桁までの数字が基数の小数部に現れます。たとえば、 ``Decimal('123E+1')`` は
   ``Decimal("1.23E+3")`` に変換されます。


.. method:: Decimal.to_integral([rounding[, context]])

   :const:`Inexact` や :const:`Rounded` といったシグナルを出さずに 最近傍の整数に値を丸めます。*rounding*
   が指定されていれば適用 されます; それ以外の場合、値丸めの方法は*context* の設定か現在の コンテキストの設定になります。

.. % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-decimal:

Context オブジェクト
--------------------

コンテキスト (context) とは、算術演算における環境設定です。 コンテキストは計算精度を決定し、値丸めの方法を設定し、
シグナルのどれが例外になるかを決め、指数の範囲を制限しています。

多重スレッドで処理を行う場合には各スレッドごとに現在のコンテキストが あり、:func:`getcontext` や :func:`setcontext`
といった関数で アクセスしたり設定変更できます:


.. function:: getcontext()

   アクティブなスレッドの現在のコンテキストを返します。


.. function:: setcontext(c)

   アクティブなスレッドのコンテキストを *c* に設定します。

Python 2.5 から、:keyword:`with` 文と :func:`localcontext` 関数を使っ
て実行するコンテキストを一時的に変更することもできるようになりました。


.. function:: localcontext([c])

   with 文の入口でアクティブなスレッドのコンテキストを *c* のコピー に設定し、with 文を抜ける時に元のコンテキストに復旧する、コンテキスト
   マネージャを返します。コンテキストが指定されなければ、現在のコンテキ ストのコピーが使われます。

   .. versionadded:: 2.5

   たとえば、以下のコードでは精度を42桁に設定し、計算を実行し、そして 元のコンテキストに復帰します。  ::

      from __future__ import with_statement
      from decimal import localcontext

      with localcontext() as ctx:
          ctx.prec = 42   # 高精度の計算を実行
          s = calculate_something()
      s = +s  # 最終的な結果をデフォルトの精度に丸める

新たなコンテキストは、以下で説明する:class:`Context` コンストラクタを 使って生成できます。その他にも、:mod:`decimal`
モジュールでは 作成済みのコンテキストを提供しています:


.. class:: BasicContext

   General Decimal Arithmetic Specification で定義されている標準コンテキスト の一つです。精度は 9
   桁に設定されています。丸め規則は :const:`ROUND_HALF_UP`
   です。すべての演算結果フラグはクリアされています。:const:`Inexact`、 :const:`Rounded`、:const:`Subnormal`
   を除く全ての演算エラートラップが 有効 (例外として扱う) になっています。

   多くのトラップが有効になっているので、デバッグの際に便利なコンテキスト です。


.. class:: ExtendedContext

   General Decimal Arithmetic Specification で定義されている標準コンテキスト の一つです。精度は 9
   桁に設定されています。丸め規則は :const:`ROUND_HALF_EVEN` です。すべての演算結果フラグはクリアされています。 トラップは全て無効
   (演算中に一切例外を送出しない) になっています。

   トラップが無効になっているので、エラーの伴う演算結果を :const:`NaN` や  :const:`Infinity`
   にし、例外を送出しないようにしたいアプリケーションに 向いたコンテキストです。このコンテキストを使うと、他の場合にはプログラム
   が停止してしまうような状況があっても実行を完了させられます。


.. class:: DefaultContext

   :class:`Context` コンストラクタが新たなコンテキストを作成するさいに 雛形にするコンテキストです。このコンテキストのフィールド
   (精度の設定など) を変更すると、:class:`Context` コンストラクタが生成する新たなコンテキストに 影響を及ぼします。

   このコンテキストは、主に多重スレッド環境で便利です。スレッドを開始する 前に何らかのフィールドを変更しておくと、システム全体のデフォルト設定
   に効果を及ぼせます。スレッドを開始した後にフィールドを変更すると 競合条件を抑制するためにスレッドを同期化せねばならないので推奨しません。

   単一スレッドの環境では、このコンテキストを使わないよう薦めます。 下で述べるように明示的にコンテキストを作成してください。

   デフォルトの値は精度 28 桁、丸め規則 :const:`ROUND_HALF_EVEN` で、 トラップ
   :const:`Overflow`、:const:`InvalidOperation`、および :const:`DivisionByZero`
   が有効になっています。

上に挙げた三つのコンテキストに加え、:class:`Context` コンストラクタを 使って新たなコンテキストを生成できます。


.. class:: Context(prec=None, rounding=None, traps=None, flags=None, Emin=None, Emax=None, capitals=1)

   新たなコンテキストを生成します。あるフィールドが定義されていないか :const:`None` であれば、 :const:`DefaultContext`
   からデフォルト値を コピーします。 *flags* フィールドが設定されていいか :const:`None` の場合には、全てのフラグがクリアされます。

   *prec* フィールドは正の整数で、コンテキストにおける算術演算の 計算精度を設定します。

   *rounding* は、

* :const:`ROUND_CEILING` (:const:`Infinity` 寄りの値にする),

* :const:`ROUND_DOWN` (ゼロ寄りの値にする),

* :const:`ROUND_FLOOR` (:const:`-Infinity` 寄りの値にする),

* :const:`ROUND_HALF_DOWN` (最近値のうちゼロ寄りの値にする),

* :const:`ROUND_HALF_EVEN` (最近値のうち偶数値を優先する),

* :const:`ROUND_HALF_UP` (最近値のうちゼロから遠い値にする), または

* :const:`ROUND_UP` (ゼロから遠い値にする)

   のいずれかです。

   *traps* および *flags* フィールドには、セットしたい シグナルを列挙します。一般的に、新たなコンテキストを作成するときには
   トラップだけを設定し、フラグはクリアしておきます。

   *Emin* および *Emax* フィールドには、指数範囲の外側値を整数で 指定します。

   *capitals* フィールドは :const:`0` または :const:`1` (デフォルト) にします。:const:`1`
   に設定すると、指数記号を大文字 :const:`E` で 出力します。それ以外の場合には  :const:`Decimal('6.02e+23')`
   のように:const:`e` を使います。

:class:`Context` クラスでは、いくつかの汎用のメソッドの他、現在の コンテキストで算術演算を直接行うためのメソッドを数多く定義しています。


.. method:: Context.clear_flags()

   フラグを全て :const:`0` にリセットします。


.. method:: Context.copy()

   コンテキストの複製を返します。


.. method:: Context.create_decimal(num)

   *self* をコンテキストとする新たな Decimal インスタンスを *num* から生成します。:class:`Decimal` コンストラクタと違い、
   数値を変換する際にコンテキストの精度、値丸め方法、フラグ、トラップ を適用します。

   定数値はしばしばアプリケーションの要求よりも高い精度を持っているため、 このメソッドが役に立ちます。また、値丸めを即座に行うため、
   例えば以下のように、入力値に値丸めを行わないために合計値にゼロの加算を 追加するだけで結果が変わってしまうといった、現在の精度
   よりも細かい値の影響が紛れ込む問題を防げるという恩恵もあります。 ::

      >>> getcontext().prec = 3
      >>> Decimal("3.4445") + Decimal("1.0023")
      Decimal("4.45")
      >>> Decimal("3.4445") + Decimal(0) + Decimal("1.0023")
      Decimal("4.44")


.. method:: Context.Etiny()

   ``Emmin - prec + 1`` に等しい値を返します。 演算結果の劣化が起こる桁の最小値です。アンダーフローが起きた場合、 指数は
   :const:`Etiny` に設定されます。


.. method:: Context.Etop()

   ``Emax - prec + 1`` に等しい値を返します。

:class:`Decimal` を使った処理を行う場合、通常は :class:`Decimal`
インスタンスを生成して、算術演算を適用するというアプローチを とります。演算はアクティブなスレッドにおける現在のコンテキストの
下で行われます。もう一つのアプローチは、コンテキストのメソッドを 使った特定のコンテキスト下での計算です。 コンテキストのメソッドは
:class:`Decimal` クラスのメソッドに似ているので、 ここでは簡単な説明にとどめます。


.. method:: Context.abs(x)

   *x* の絶対値を返します。


.. method:: Context.add(x, y)

   *x* と *y* の加算を返します。


.. method:: Context.compare(x, y)

   二つの値を数値として比較します。

   :meth:`__cmp__` に似ていますが、 以下のように:class:`Decimal`  インスタンスを返します::

      a or b is a NaN ==> Decimal("NaN")
      a < b           ==> Decimal("-1")
      a == b          ==> Decimal("0")
      a > b           ==> Decimal("1")


.. method:: Context.divide(x, y)

   *x* を *y* で除算した値を返します。


.. method:: Context.divmod(x, y)

   二つの数値間の除算を行い、結果の整数部を返します。


.. method:: Context.max(x, y)

   二つの値を数値として比較し、大きいほうを返します。

   数値上二つの値が等しい場合には、左側値を結果として返します。


.. method:: Context.min(x, y)

   二つの値を数値として比較し、小さいほうを返します。

   数値上二つの値が等しい場合には、左側値を結果として返します。


.. method:: Context.minus(x)

   Python における単項の符号反転前置演算子 (unary prefix minus operator)  に対応する演算です。


.. method:: Context.multiply(x, y)

   *x* と*y* の積を返します。


.. method:: Context.normalize(x)

   被演算子をもっとも単純な表記にします。

   本質的には、:meth:`plus` 演算の結果から末尾のゼロを全て取り除いた ものと同じです。


.. method:: Context.plus(x)

   Python における単項の符号非反転前置演算子 (unary prefix plus operator)
   に対応する演算です。コンテキストにおける精度や値丸めを適用する ので、等値 (identity) 演算とは *違います*。


.. method:: Context.power(x, y[, modulo])

   ``x ** y`` を計算します。*modulo* が指定されていれば使います。

   右被演算子は整数部が 9 桁以下で、小数部 (のある場合) は値丸め前に 全てゼロになっていなければなりません。被演算子は正でも負でもゼロでも
   かまいません。右被演算子が負の場合には、左被演算子の逆数 (1 を左被演算子で割った値) を右被演算子の逆数でべき乗します。

   中間演算でより高い計算精度が必要になり、その精度が実装の提供している 精度を超えた場合、:const:`InvalidOperation`
   エラーをシグナルします。

   負のべき乗を行う際に 1 への除算でアンダーフローが起きても、 その時点では演算を停止せず継続します。


.. method:: Context.quantize(x, y)

   *x* に値丸めを適用し、指数を *y* にした値を返します。

   他の演算と違い、量子化後の係数の長さが精度よりも大きい場合には :const:`InvalidOperation` をシグナルします。
   このため、エラーが生じないかぎり、量子化後の指数は右側の被演算子 の指数と等しくなることが保証されます。

   また、結果が劣化していたり不正確な値であっても、:const:`Underflow` をシグナルしないという点も他の演算と異なります。


.. method:: Context.remainder(x, y)

   整数除算の剰余を返します。

   剰余がゼロでない場合、符号は割られる数の符号と同じになります。


.. method:: Context.remainder_near(x, y)

   モジュロを計算し、正負のモジュロのうちゼロに近い値を返します。 たとえば、 ``Decimal(10).remainder_near(6)`` は
   ``Decimal("4")`` よりもゼロに近い値 ``Decimal("-2")`` を返します。

   ゼロからの差が同じ場合には、 *self* と同じ符号を持った方を 返します。


.. method:: Context.same_quantum(x, y)

   *self* と *other* が同じ指数を持っているか、あるいは 双方とも :const:`NaN` である場合に真を返します。


.. method:: Context.sqrt(x)

   *x* の平方根を精度いっぱいまで求めます。


.. method:: Context.subtract(x, y)

   *x* と*y* の間の差を返します。


.. method:: Context.to_eng_string()

   工学表記で文字列に変換します。

   工学表記では指数は 3 の倍数になります。従って、 最大で 3 桁までの数字が基数の小数部に現れます。たとえば、 ``Decimal('123E+1')`` は
   ``Decimal("1.23E+3")`` に変換されます。


.. method:: Context.to_integral(x)

   :const:`Inexact` や :const:`Rounded` といったシグナルを出さずに 最近傍の整数に値を丸めます。


.. method:: Context.to_sci_string(x)

   数値を科学表記で文字列に変換します。

.. % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-signals:

シグナル
--------

シグナルは、計算中に生じた様々なエラー条件を表現します。 各々のシグナルは一つのコンテキストフラグと一つのトラップイネーブラに 対応しています。

コンテキストフラグは、該当するエラー条件に遭遇するたびに加算されて ゆきます。演算後にフラグを調べれば、演算に関する情報 (例えば計算が厳密だったかどうか)
がわかります。 フラグを調べたら、次の計算を始める前にフラグを全てクリアするように してください。

あるコンテキストのトラップイネーブラがあるシグナルに対してセット されている場合、該当するエラー条件が生じると Python の例外を送出
します。例えば、:class:`DivisionByZero` が設定されていると、 エラー条件が生じた際に :exc:`DivisionByZero`
例外を送出します。


.. class:: Clamped

   値の表現上の制限に沿わせるために指数部が変更されたことを通知します。

   通常、クランプ (clamp) は、指数部がコンテキストにおける指数桁の制限値 :attr:`Emin` および:attr:`Emax`
   を越えたなった場合に発生します。 可能な場合には、係数部にゼロを加えた表現に合わせて指数部を減らします。


.. class:: DecimalException

   他のシグナルの基底クラスで、:exc:`ArithmeticError` の サブクラスです。


.. class:: DivisionByZero

   有限値をゼロで除算したときのシグナルです。

   除算やモジュロ除算、数を負の値で累乗した場合に起きることがあります。 このシグナルをトラップしない場合、演算結果は :const:`Infinity` または
   :const:`-Infinity` になり、その符号は演算に使った入力に基づいて決まります。


.. class:: Inexact

   値の丸めによって演算結果から厳密さが失われたことを通知します。

   このシグナルは値丸め操作中にゼロでない桁を無視した際に生じます。 演算結果は値丸め後の値です。シグナルのフラグやトラップは、
   演算結果の厳密さが失われたことを検出するために使えるだけです。


.. class:: InvalidOperation

   無効な演算が実行されたことを通知します。

   ユーザが有意な演算結果にならないような操作を要求したことを示します。 このシグナルをトラップしない場合、:const:`NaN` を返します。
   このシグナルの発生原因として考えられるのは、以下のような状況です::

      Infinity - Infinity
      0 * Infinity
      Infinity / Infinity
      x % 0
      Infinity % x
      x._rescale( non-integer )
      sqrt(-x) and x > 0
      0 ** 0
      x ** (non-integer)
      x ** Infinity      


.. class:: Overflow

   数値オーバフローを示すシグナルです。

   このシグナルは、値丸めを行った後の指数部が :attr:`Emax` より大きいことを 示します。シグナルをトラップしない場合、演算結果は値丸めのモードにより、
   表現可能な最大の数値になるように内側へ引き込んで丸めを行った値か、 :const:`Infinity` になるように外側に丸めた値のいずれかになります。
   いずれの場合も、:class:`Inexact` および :class:`Rounded` が同時に シグナルされます。


.. class:: Rounded

   情報が全く失われていない場合も含み、値丸めが起きたときのシグナルです。

   このシグナルは、値丸めによって桁がなくなると常に発生します。 なくなった桁がゼロ (例えば:const:`5.00` を丸めて :const:`5.0`
   になった場合) であってもです。このシグナルをトラップしなければ、 演算結果をそのまま返します。このシグナルは有効桁数の減少を検出 する際に使います。


.. class:: Subnormal

   値丸めを行う前に指数部が :attr:`Emin` より小さかったことを示す シグナルです。

   演算結果が微小である場合 (指数が小さすぎる場合) に発生します。 このシグナルをトラップしなければ、演算結果をそのまま返します。


.. class:: Underflow

   演算結果が値丸めによってゼロになった場合に生じる数値アンダフローです。

   演算結果が微小なため、値丸めによってゼロになった場合に発生します。 :class:`Inexact` および :class:`Subnormal`
   シグナルも同時に発生します。

これらのシグナルの階層構造をまとめると、以下の表のようになります::

   exceptions.ArithmeticError(exceptions.StandardError)
       DecimalException
           Clamped
           DivisionByZero(DecimalException, exceptions.ZeroDivisionError)
           Inexact
               Overflow(Inexact, Rounded)
               Underflow(Inexact, Rounded, Subnormal)
           InvalidOperation
           Rounded
           Subnormal

.. % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-notes:

浮動小数点数に関する注意
------------------------


精度を上げて丸め誤差を抑制する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

10 進浮動小数点数を使うと、 10 進数表現による誤差を抑制できます (:const:`0.1` を正確に表現できるようになります); しかし、ゼロでない
桁が一定の精度を越えている場合には、演算によっては依然として値丸めによる 誤差を引き起こします。 Knuth は、十分でない計算精度の下で値丸めを伴う
浮動小数点演算を行った結果、加算の結合則や分配則における恒等性が崩れて しまう例を二つ示しています::

   # Examples from Seminumerical Algorithms, Section 4.2.2.
   >>> from decimal import Decimal, getcontext
   >>> getcontext().prec = 8

   >>> u, v, w = Decimal(11111113), Decimal(-11111111), Decimal('7.51111111')
   >>> (u + v) + w
   Decimal("9.5111111")
   >>> u + (v + w)
   Decimal("10")

   >>> u, v, w = Decimal(20000), Decimal(-6), Decimal('6.0000003')
   >>> (u*v) + (u*w)
   Decimal("0.01")
   >>> u * (v+w)
   Decimal("0.0060000")

:mod:`decimal` モジュールでは、最下桁を失わないように十分に計算精度を 広げることで、上で問題にしたような恒等性をとりもどせます::

   >>> getcontext().prec = 20
   >>> u, v, w = Decimal(11111113), Decimal(-11111111), Decimal('7.51111111')
   >>> (u + v) + w
   Decimal("9.51111111")
   >>> u + (v + w)
   Decimal("9.51111111")
   >>> 
   >>> u, v, w = Decimal(20000), Decimal(-6), Decimal('6.0000003')
   >>> (u*v) + (u*w)
   Decimal("0.0060000")
   >>> u * (v+w)
   Decimal("0.0060000")


特殊値
^^^^^^

:mod:`decimal` モジュールの数体系では、:const:`NaN`, :const:`sNaN`,  :const:`-Infinity` ,
:const:`Infinity` , および二つのゼロ、 :const:`+0` と :const:`-0` といった特殊な値を提供しています。

無限大 (Infinity) は ``Decimal('Infinity')`` で直接構築できます。 また、:exc:`DivisionByZero`
をトラップせずにゼロで除算を行った 場合にも出てきます。同様に、 :exc:`Overflow` シグナルをトラップ
しなければ、表現可能な最大の数値の制限を越えた値を丸めたときに出てきます。

無限大には符号があり (アフィン: affine であり)、算術演算に使用でき、
非常に巨大で不確定の(indeterminate)値として扱われます。例えば、無限大に 何らかの定数を加算すると、演算結果は別の無限大になります。

演算によっては結果が不確定になるものがあり、:const:`NaN` を返します。 ただし、:exc:`InvalidOperation`
シグナルをトラップするように なっていれば例外を送出します。

例えば、``0/0`` は :const:`NaN` を返します。:const:`NaN` は 「非数値 (not a number)」を表します。このような
:const:`NaN` は 暗黙のうちに生成され、一度生成されるとそれを他の計算にも流れてゆき、 関係する個々の演算全てが個別の :const:`NaN`
を返すようになります。 この挙動は、たまに入力値が欠けるような状況で一連の計算を行う際に 便利です --- 特定の計算に対しては無効な結果を示すフラグを立てつつ
計算を進められるからです。

一方、:const:`NaN` の変種である:const:`sNaN` は関係する全ての演算 で演算後にシグナルを送出します。:const:`sNaN`
は、無効な演算結果 に対して特別な処理を行うために計算を停止する必要がある場合に便利です。

アンダフローの起きた計算は、符号付きのゼロ (signed zero) を返す ことがあります。符号は、より高い精度で計算を行った結果の 符号と同じになります。
符号付きゼロの大きさはやはりゼロなので、正のゼロと負のゼロは 等しいとみなされ、符号は単なる参考にすぎません。

二つの符号付きゼロが区別されているのに等価であることに加えて、 異なる精度におけるゼロの表現はまちまちなのに、値は等価と
みなされるということがあります。これに慣れるには多少時間がかかります。 正規化浮動小数点表現に目が慣れてしまうと、以下の計算でゼロに
等しい値が返っているとは即座に分かりません::

   >>> 1 / Decimal('Infinity')
   Decimal("0E-1000000026")

.. % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-threads:

スレッドを使った処理
--------------------

関数:func:`getcontext` は、スレッド毎に別々の:class:`Context`
オブジェクトにアクセスします。別のスレッドコンテキストを持つということは、 複数のスレッドが互いに影響を及ぼさずに
(``getcontext.prec=10`` のような) 変更を適用できるということです。

同様に、:func:`setcontext` 関数は自動的に引数のコンテキスト を現在のスレッドのコンテキストに設定します。

:func:`getcontext` を呼び出す前に:func:`setcontext` が
呼び出されていなければ、現在のスレッドで使うための新たなコンテキスト を生成するために:func:`getcontext` が自動的に呼び出されます。

新たなコンテキストは、*DefaultContext* と呼ばれる雛形から コピーされます。アプリケーションを通じて全てのスレッドに同じ
値を使うようにデフォルトを設定したければ、*DefaultContext* オブジェクトを直接変更します。:func:`getcontext` を呼び出す
スレッド間で競合条件が生じないようにするため、*DefaultContext* への変更はいかなるスレッドを開始するよりも*前に* 行わねば
なりません。以下に例を示します::

   # スレッドを立ち上げる前にアプリケーションにわたるデフォルトを設定
   DefaultContext.prec = 12
   DefaultContext.rounding = ROUND_DOWN
   DefaultContext.traps = ExtendedContext.traps.copy()
   DefaultContext.traps[InvalidOperation] = 1
   setcontext(DefaultContext)

   # その後でスレッドを開始
   t1.start()
   t2.start()
   t3.start()
    . . .

.. % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-recipes:

レシピ
------

:class:`Decimal` クラスの利用を実演している例をいくつか示します。 これらはユーティリティ関数としても利用できます::

   def moneyfmt(value, places=2, curr='', sep=',', dp='.',
                pos='', neg='-', trailneg=''):
       """Decimal を通貨表現の文字列に変換します。

       places:  小数点以下の値を表すのに必要な桁数
       curr:    符号の前に置く通貨記号 (オプションで、空でもかまいません)
       sep:     桁のグループ化に使う記号、オプションです (コンマ、ピリオド、
                スペース、または空)
       dp:      小数点 (コンマまたはピリオド)
                小数部がゼロの場合には空にできます。
       pos:     正数の符号オプション: '+', 空白または空文字列
       neg:     負数の符号オプション: '-', '(', 空白または空文字列
       trailneg:後置マイナス符号オプション:  '-', ')', 空白または空文字列

       >>> d = Decimal('-1234567.8901')
       >>> moneyfmt(d, curr='$')
       '-$1,234,567.89'
       >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
       '1.234.568-'
       >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
       '($1,234,567.89)'
       >>> moneyfmt(Decimal(123456789), sep=' ')
       '123 456 789.00'
       >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
       '<.02>'

       """
       q = Decimal((0, (1,), -places))    # 小数点以下2桁 --> '0.01'
       sign, digits, exp = value.quantize(q).as_tuple()
       assert exp == -places    
       result = []
       digits = map(str, digits)
       build, next = result.append, digits.pop
       if sign:
           build(trailneg)
       for i in range(places):
           if digits:
               build(next())
           else:
               build('0')
       build(dp)
       i = 0
       while digits:
           build(next())
           i += 1
           if i == 3 and digits:
               i = 0
               build(sep)
       build(curr)
       if sign:
           build(neg)
       else:
           build(pos)
       result.reverse()
       return ''.join(result)

   def pi():
       """現在の精度まで円周率を計算します。

       >>> print pi()
       3.141592653589793238462643383

       """
       getcontext().prec += 2  # 中間ステップのための余分の数字
       three = Decimal(3)      # 普通の float に対する "three=3.0" の代わり
       lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
       while s != lasts:
           lasts = s
           n, na = n+na, na+8
           d, da = d+da, da+32
           t = (t * n) / d
           s += t
       getcontext().prec -= 2
       return +s               # 単項のプラスで新しい精度に変換します

   def exp(x):
       """e の x 乗を返します。結果の型は入力の型と同じです。

       >>> print exp(Decimal(1))
       2.718281828459045235360287471
       >>> print exp(Decimal(2))
       7.389056098930650227230427461
       >>> print exp(2.0)
       7.38905609893
       >>> print exp(2+0j)
       (7.38905609893+0j)

       """
       getcontext().prec += 2
       i, lasts, s, fact, num = 0, 0, 1, 1, 1
       while s != lasts:
           lasts = s    
           i += 1
           fact *= i
           num *= x     
           s += num / fact   
       getcontext().prec -= 2        
       return +s

   def cos(x):
       """x ラジアンの余弦を返します。

       >>> print cos(Decimal('0.5'))
       0.8775825618903727161162815826
       >>> print cos(0.5)
       0.87758256189
       >>> print cos(0.5+0j)
       (0.87758256189+0j)

       """
       getcontext().prec += 2
       i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
       while s != lasts:
           lasts = s    
           i += 2
           fact *= i * (i-1)
           num *= x * x
           sign *= -1
           s += num / fact * sign 
       getcontext().prec -= 2        
       return +s

   def sin(x):
       """x ラジアンの正弦を返します。

       >>> print sin(Decimal('0.5'))
       0.4794255386042030002732879352
       >>> print sin(0.5)
       0.479425538604
       >>> print sin(0.5+0j)
       (0.479425538604+0j)

       """
       getcontext().prec += 2
       i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
       while s != lasts:
           lasts = s    
           i += 2
           fact *= i * (i-1)
           num *= x * x
           sign *= -1
           s += num / fact * sign 
       getcontext().prec -= 2        
       return +s


.. % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-faq:

Decimal FAQ
-----------

Q.  ``decimal.Decimal('1234.5')`` などと打ち込むのは煩わしいのですが、
対話式インタプリタを使う際にタイプ量を少なくする方法はありませんか?

A.  コンストラクタを1文字に縮める人もいるようです。 ::

   >>> D = decimal.Decimal
   >>> D('1.23') + D('3.45')
   Decimal("4.68")

Q.  小数点以下2桁の固定小数点数のアプリケーションの中で、いくつかの 入力が余計な桁を保持しているのでこれを丸めなければなりません。その他の
ものに余計な桁はなくそのまま使えます。どのメソッドを使うのがいいでしょうか?

A.  :meth:`quantize` メソッドで固定した桁に丸められます。 :const:`Inexact` トラップを設定しておけば、確認にも有用です。
::

   >>> TWOPLACES = Decimal(10) ** -2       # Decimal('0.01') と同じ

   >>> # 小数点以下2桁に丸める
   >>> Decimal("3.214").quantize(TWOPLACES)
   Decimal("3.21")

   >>> # 小数点以下2桁を越える桁を保持していないことの確認
   >>> Decimal("3.21").quantize(TWOPLACES, context=Context(traps=[Inexact]))
   Decimal("3.21")

   >>> Decimal("3.214").quantize(TWOPLACES, context=Context(traps=[Inexact]))
   Traceback (most recent call last):
      ...
   Inexact: Changed in rounding

Q.  正当な2桁の入力が得られたとして、その正当性をアプリケーション実行中も 変わらず保ち続けるにはどうすればいいでしょうか?

A.  加減算のような演算は自動的に固定小数点を守ります。その他の乗除算などは 小数点以下の桁を変えてしまいますので実行後は  :meth:`quantize`
ステップ が必要です。

Q.  一つの値に対して多くの表現方法があります。 :const:`200` と:const:`200.000` と :const:`2E2` と
:const:`.02E+4` は全て同じ値で違った精度の数です。これらをただ一つの 正規化された値に変換することはできますか?

A.  :meth:`normalize` メソッドは全ての等しい値をただ一つの表現に直します。 ::

   >>> values = map(Decimal, '200 200.000 2E2 .02E+4'.split())
   >>> [v.normalize() for v in values]
   [Decimal("2E+2"), Decimal("2E+2"), Decimal("2E+2"), Decimal("2E+2")]

Q.  ある種の10進数値はいつも指数表記で表示されます。 指数表記以外の表示にする方法はありますか?

A.  値によっては、指数表記だけが有効桁数を表せる表記法なのです。 たとえば、 :const:`5.0E+3` を :const:`5000`
と表してしまうと、 値は変わりませんが元々の2桁という有効数字が反映されません。

Q.  普通の float を :class:`Decimal` に変換できますか?

A.  はい。どんな2進浮動小数点数も Decimal として正確に表現できます。 正確な変換は直感的に考えたよりも多い桁になることもありますので、
:const:`Inexact` をトラップしたとすればそれはもっと精度を上げる 必要性があることを示しています。 ::

   def floatToDecimal(f):
       "浮動小数点数を情報の欠落無く Decimal に変換します"

       # float で表された数を仮数 (0.5 <= abs(m) < 1.0) と指数に(正確に)転
       # 換します。仮数を整数になるまで2倍し続けます。整数化した仮数と指数
       # を使って等価な Decimal を求めます。この手続きが正確に行なえなかっ
       # たら、精度を上げて再度同じことをします。

       mantissa, exponent = math.frexp(f)
       while mantissa != int(mantissa):
           mantissa *= 2.0
           exponent -= 1
       mantissa = int(mantissa)

       oldcontext = getcontext()
       setcontext(Context(traps=[Inexact]))
       try:
           while True:
               try:
                  return mantissa * Decimal(2) ** exponent
               except Inexact:
                   getcontext().prec += 1
       finally:
           setcontext(oldcontext)

Q.  上の :func:`floatToDecimal` はなぜモジュールに入っていないのですか?

A.  2進と10進の浮動小数点数を混ぜるようにアドバイスするべきかどうか疑問が あります。また、これを使うときには2進浮動小数点数の表示の問題を避けるように
注意しなければなりません。 ::

   >>> floatToDecimal(1.1)
   Decimal("1.100000000000000088817841970012523233890533447265625")

Q.  複雑な計算の中で、精度不足や丸めの異常で間違った結果になっていない ことをどうやって保証すれば良いでしょうか?

A.  decimal モジュールでは検算は容易です。一番良い方法は、大きめの精度や 様々な丸めモードで再計算してみることです。大きく異なった結果が出てきたら、
精度不足や丸めの問題や悪条件の入力、または数値計算的に不安定なアルゴリズム を示唆しています。

Q.  コンテキストの精度は計算結果には適用されていますが入力には適用されて いないようです。様々に異なる精度の入力値を混ぜて計算する時に注意すべき
ことはありますか?

A.  はい。原則として入力値は正確であると見做しておりそれらの値を使った 計算も同様です。結果だけが丸められます。入力の強みは "what you type
is what you get" (打ち込んだ値が得られる値)という点にあります。 入力が丸められないということを忘れていると結果が奇妙に見えるというのは
弱点です。 ::

   >>> getcontext().prec = 3
   >>> Decimal('3.104') + D('2.104')
   Decimal("5.21")
   >>> Decimal('3.104') + D('0.000') + D('2.104')
   Decimal("5.20")

解決策は精度を上げるかまたは単項のプラス演算子を使って入力の丸めを強制する ことです。 ::

   >>> getcontext().prec = 3
   >>> +Decimal('1.23456789')      # 単項のプラスで丸めを引き起こします
   Decimal("1.23")

もしくは、入力を :meth:`Context.create_decimal` を使って生成時に丸め てしまうこともできます。 ::

   >>> Context(prec=5, rounding=ROUND_DOWN).create_decimal('1.2345678')
   Decimal("1.2345")

