
:mod:`fractions` --- 有理数
=====================================

.. module:: fractions
   :synopsis: 有理数
.. moduleauthor:: Jeffrey Yasskin <jyasskin at gmail.com>
.. sectionauthor:: Jeffrey Yasskin <jyasskin at gmail.com>
.. versionadded:: 2.6


:mod:`fractions` モジュールは有理数計算のサポートを提供します。


Fraction インスタンスは一対の整数、他の有理数または文字列から組み立てられます。

.. class:: Fraction(numerator=0, denominator=1)
           Fraction(other_fraction)
           Fraction(string)

   最初のバージョンは *numerator* と *denominator* が :class:`numbers.Integral`
   のインスタンスであることを要求し、 ``numerator/denominator`` の値を持った\
   新しい :class:`Fraction` インスタンスを返します。
   *denominator* が :const:`0` ならば、 :exc:`ZeroDivisionError`
   を送出します。
   二番目のバージョンは *other_fraction* が :class:`numbers.Rational`
   のインスタンスであることを要求し、同じ値を持った新しい :class:`Fraction`
   インスタンスを返します。
   最後のバージョンは二つの可能な形式のうちどちらかであるような\
   文字列またはユニコードのインスタンスを渡されると思っています。
   一つめの形式は::

      [sign] numerator ['/' denominator]

   で、ここにオプションの ``sign`` は '+' か '-' のどちらかであり、\
   ``numerator`` および ``denominator`` (もしあるならば) は十進数の\
   数字の並びです。二つめの許容される形式は小数点を含んだ::

      [sign] integer '.' [fraction] | [sign] '.' fraction

   の形をとり、ここで ``integer`` と ``fraction`` は数字の並びです。
   どちらの形式でも入力される文字列は前後に空白があって構いません。
   例を見ましょう::

      >>> from fractions import Fraction
      >>> Fraction(16, -10)
      Fraction(-8, 5)
      >>> Fraction(123)
      Fraction(123, 1)
      >>> Fraction()
      Fraction(0, 1)
      >>> Fraction('3/7')
      Fraction(3, 7)
      [40794 refs]
      >>> Fraction(' -3/7 ')
      Fraction(-3, 7)
      >>> Fraction('1.414213 \t\n')
      Fraction(1414213, 1000000)
      >>> Fraction('-.125')
      Fraction(-1, 8)


   :class:`Fraction` クラスは抽象基底クラス :class:`numbers.Rational`
   を継承し、その全てのメソッドと演算を実装します。 :class:`Fraction`
   インスタンスはハッシュ可能で、したがって不変(immutable)であるものとして\
   扱います。加えて、 :class:`Fraction` には以下のメソッドがあります:


   .. method:: from_float(flt)

      このクラスメソッドは :class:`float` である *flt* の正確な値を表す
      :class:`Fraction` を構築します。
      気を付けてください ``Fraction.from_float(0.3)`` と ``Fraction(3, 10)``
      の値は同じではありません。


   .. method:: from_decimal(dec)

      このクラスメソッドは :class:`decimal.Decimal` である *dec* の正確な値を表す
      :class:`Fraction` を構築します。


   .. method:: limit_denominator(max_denominator=1000000)

      高々 max_denominator を分母に持つ ``self`` に最も近い :class:`Fraction` 
      を見付けて返します。
      このメソッドは与えられた浮動小数点数の有理数近似を見つけるのに役立ちます:

         >>> from fractions import Fraction
         >>> Fraction('3.1415926535897932').limit_denominator(1000)
         Fraction(355, 113)

      あるいは float で表された有理数を元に戻すのにも使えます:

         >>> from math import pi, cos
         >>> Fraction.from_float(cos(pi/3))
         Fraction(4503599627370497, 9007199254740992)
         >>> Fraction.from_float(cos(pi/3)).limit_denominator()
         Fraction(1, 2)


.. function:: gcd(a, b)

   整数 *a* と *b* の最大公約数を返します。 *a* も *b* もゼロでないとすると、
   ``gcd(a, b)`` の絶対値は *a* と *b* の両方を割り切る最も大きな整数です。
   ``gcd(a, b)`` は *b* がゼロでなければ *b* と同じ符号になります。
   そうでなければ *a* の符号を取ります。
   ``gcd(0, 0)`` は `0` を返します。


.. seealso::

   :mod:`numbers` モジュール
      数値の塔を作り上げる抽象基底クラス。
