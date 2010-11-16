.. _tut-fp-issues:

******************************
浮動小数点演算、その問題と制限
******************************

.. sectionauthor:: Tim Peters <tim_one@users.sourceforge.net>


浮動小数点数は、計算機ハードウェアの中では、基数を 2 とする (2進法の) 分数として表現されています。例えば、小数

.. % % Floating Point Arithmetic:  Issues and Limitations
.. % % Floating-point numbers are represented in computer hardware as
.. % % base 2 (binary) fractions.  For example, the decimal fraction

::

   0.125

は、 1/10 + 2/100 + 5/1000 という値を持ちますが、これと同様に、 2 進法の分数

.. % % has value 1/10 + 2/100 + 5/1000, and in the same way the binary fraction

::

   0.001

は 0/2 + 0/4 + 1/8 という値になります。これら二つの分数は同じ値を持っていますが、ただ一つ、最初の分数は基数 10 で記述されており、
二番目の分数は基数 2 で記述されていることが違います。

.. % % has value 0/2 + 0/4 + 1/8.  These two fractions have identical values,
.. % % the only real difference being that the first is written in base 10
.. % % fractional notation, and the second in base 2.

残念なことに、ほとんどの小数は 2 進法の分数として正確に表わすことができません。その結果、一般に、入力した 10 進の浮動小数点数は、 2
進法の浮動小数点数で近似された後、実際にマシンに記憶されます。

.. % % Unfortunately, most decimal fractions cannot be represented exactly as
.. % % binary fractions.  A consequence is that, in general, the decimal
.. % % floating-point numbers you enter are only approximated by the binary
.. % % floating-point numbers actually stored in the machine.

最初は基数 10 を使うと問題を簡単に理解できます。分数 1/3 を考えてみましょう。分数 1/3 は、基数 10 の分数として、以下のように近似する
ことができます:

.. % % The problem is easier to understand at first in base 10.  Consider the
.. % % fraction 1/3.  You can approximate that as a base 10 fraction:

::

   0.3

さらに正確な近似は、

.. % % or, better,

::

   0.33

です。さらに正確に近似すると、

.. % % or, better,

::

   0.333

となり、以後同様です。何個桁数を増やして書こうが、結果は決して厳密な 1/3 にはなりません。しかし、少しづつ正確な近似にはなっていくでしょう。

.. % % and so on.  No matter how many digits you're willing to write down, the
.. % % result will never be exactly 1/3, but will be an increasingly better
.. % % approximation to 1/3.

同様に、基数を 2 とした表現で何桁使おうとも、10 進数の 0.1 は基数を 2 とした分数で正確に表現することはできません。基数 2 では、1/10
は循環小数 (repeating fraction)

.. % % In the same way, no matter how many base 2 digits you're willing to
.. % % use, the decimal value 0.1 cannot be represented exactly as a base 2
.. % % fraction.  In base 2, 1/10 is the infinitely repeating fraction

::

   0.0001100110011001100110011001100110011001100110011...

となります。どこか有限の桁で止めると、近似値を得ることになります。これこそが、以下のような事態:

.. % % Stop at any finite number of bits, and you get an approximation.  This
.. % % is why you see things like:

::

   >>> 0.1
   0.10000000000000001

に出くわす理由です。

今日では、ほとんどのマシンでは、0.1 を Python のプロンプトから入力すると上のような結果を目にします。そうならないかもしれませんが、これは
ハードウェアが浮動小数点数を記憶するのに用いているビット数がマシンによって異なり、Python は単にマシンに 2 進で記憶されている、真の 10 進の
値を近似した値を、されに 10 進で近似して出力するだけだからです。ほとんどのマシンでは、Python が 0.1 を記憶するために 2 進近似した真の値を
10 進で表すと、以下のような出力

.. % % On most machines today, that is what you'll see if you enter 0.1 at
.. % % a Python prompt.  You may not, though, because the number of bits
.. % % used by the hardware to store floating-point values can vary across
.. % % machines, and Python only prints a decimal approximation to the true
.. % % decimal value of the binary approximation stored by the machine.  On
.. % % most machines, if Python were to print the true decimal value of
.. % % the binary approximation stored for 0.1, it would have to display

::

   >>> 0.1
   0.1000000000000000055511151231257827021181583404541015625

になるでしょう！ Python プロンプトは、文字列表現を得るために何に対しても :func:`repr` を使います。浮動小数点数の場合、
``repr(float)`` は真の 10 進値を有効数字 17 桁で丸め、以下のような表示

.. % % instead!  The Python prompt uses the builtin
.. % % \function{repr()} function to obtain a string version of everything it
.. % % displays.  For floats, \code{repr(\var{float})} rounds the true
.. % % decimal value to 17 significant digits, giving

::

   0.10000000000000001

を行います。

``repr(float)`` が有効数字 17桁の値を生成するのは、この値が (ほとんどのマシン上で) 、全ての有限の浮動小数点数 *x* について
``eval(repr(x)) == x`` が成り立つのに十分で、かつ有効数字 16 桁に丸めると成り立たないからです。

.. % % \code{repr(\var{float})} produces 17 significant digits because it
.. % % turns out that's enough (on most machines) so that
.. % % \code{eval(repr(\var{x})) == \var{x}} exactly for all finite floats
.. % % \var{x}, but rounding to 16 digits is not enough to make that true.

これは 2 進法の浮動小数点の性質です: Python のバグでも、ソースコードのバグでもなく、浮動小数点演算を扱えるハードウェア上の、すべての言語で同じ
類の現象が発生します (ただし、言語によっては、デフォルトのモードや全ての出力モードでその差を *表示しない* かもしれません)。

.. % % Note that this is in the very nature of binary floating-point: this is
.. % % not a bug in Python, and it is not a bug in your code either. You'll
.. % % see the same kind of thing in all languages that support your
.. % % hardware's floating-point arithmetic (although some languages may
.. % % not \emph{display} the difference by default, or in all output modes).

Python の組み込みの :func:`str` 関数は有効数字 12 桁しか生成しません。このため、この関数を代わりに使用したいと思うかもしれません。
この関数は ``eval(str(x))`` としたときに *x* を再現しないことが多いですが、出力を目で見るには好ましいかもしれません:

.. % % Python's builtin \function{str()} function produces only 12
.. % % significant digits, and you may wish to use that instead.  It's
.. % % unusual for \code{eval(str(\var{x}))} to reproduce \var{x}, but the
.. % % output may be more pleasant to look at:

::

   >>> print str(0.1)
   0.1

現実という考えからは、上の表示は錯覚であると気づくのは重要なことです: マシン内の値は厳密に 1/10 ではなく、単に真のマシン内の  *表示される値*
を丸めているだけなのです。

.. % % It's important to realize that this is, in a real sense, an illusion:
.. % % the value in the machine is not exactly 1/10, you're simply rounding
.. % % the \emph{display} of the true machine value.

まだ驚くべきことがあります。例えば、以下

.. % % Other surprises follow from this one.  For example, after seeing

::

   >>> 0.1
   0.10000000000000001

を見て、 :func:`round` 関数を使って桁を切り捨て、期待する 1 桁にしたい誘惑にかられたとします。しかし、結果は依然同じ値です:

.. % % you may be tempted to use the \function{round()} function to chop it
.. % % back to the single digit you expect.  But that makes no difference:

::

   >>> round(0.1, 1)
   0.10000000000000001

問題は、"0.1" を表すために記憶されている 2 進表現の浮動小数点数の値は、すでに 1/10 に対する最良の近似になっており、値を再度丸めようとしても
これ以上ましにはならないということです: すでに値は、 :func:`round` で得られる値になっているというわけです。

.. % % The problem is that the binary floating-point value stored for "0.1"
.. % % was already the best possible binary approximation to 1/10, so trying
.. % % to round it again can't make it better:  it was already as good as it
.. % % gets.

もう一つの重要なことは、0.1 が正確に 1/10 ではないため、0.1 を 10 個加算すると厳密に 1.0 にはならないこともある、ということです:

.. % % Another consequence is that since 0.1 is not exactly 1/10,
.. % % summing ten values of 0.1 may not yield exactly 1.0, either:

::

   >>> sum = 0.0
   >>> for i in range(10):
   ...     sum += 0.1
   ...
   >>> sum
   0.99999999999999989

2 進の浮動小数点数に対する算術演算は、このような意外性をたくさん持っています。"0.1" に関する問題は、以下の "表現エラー" の章で詳細に説明します。
2 進法の浮動小数点演算にともなうその他のよく知られた意外な事象に関しては `The Perils of Floating Point
<http://www.lahey.com/float.htm>`_ を参照してください。

.. % % Binary floating-point arithmetic holds many surprises like this.  The
.. % % problem with "0.1" is explained in precise detail below, in the
.. % % "Representation Error" section.  See
.. % % \citetitle[http://www.lahey.com/float.htm]{The Perils of Floating
.. % % Point} for a more complete account of other common surprises.

究極的にいうと、"容易な答えはありません"。ですが、浮動小数点数のことを過度に警戒しないでください！ Python の float 型操作における
エラーは浮動小数点処理ハードウェアから受けついたものであり、ほとんどのマシン上では一つの演算あたり高々 2\*\*53 分の 1 です。
この誤差はほとんどの作業で相当以上のものですが、浮動小数点演算は 10 進の演算えはなく、浮動小数点の演算を新たに行うと、新たな
丸め誤差の影響を受けることを心にとどめておいてください。

.. % % As that says near the end, ``there are no easy answers.''  Still,
.. % % don't be unduly wary of floating-point!  The errors in Python float
.. % % operations are inherited from the floating-point hardware, and on most
.. % % machines are on the order of no more than 1 part in 2**53 per
.. % % operation.  That's more than adequate for most tasks, but you do need
.. % % to keep in mind that it's not decimal arithmetic, and that every float
.. % % operation can suffer a new rounding error.

異常なケースが存在する一方で、普段の浮動小数点演算の利用では、単に最終的な結果の値を必要な
10 進の桁数に丸めて表示するのなら、最終的には期待通りの結果を得ることになるでしょう。
こうした操作は普通 :func:`str` で事足りますし、よりきめ細かな制御をしたければ、
:ref:`formatstrings` にある :meth:`str.format` メソッドのフォーマット仕様を参照してください。

.. % % While pathological cases do exist, for most casual use of
.. % % floating-point arithmetic you'll see the result you expect in the end
.. % % if you simply round the display of your final results to the number of
.. % % decimal digits you expect.  \function{str()} usually suffices, and for
.. % % finer control see the discussion of Pythons's \code{\%} format
.. % % operator: the \code{\%g}, \code{\%f} and \code{\%e} format codes
.. % % supply flexible and easy ways to round float results for display.


.. _tut-fp-error:

表現エラー
==========

この章では、"0.1" の例について詳細に説明し、このようなケースに対してどのようにすれば正確な分析を自分で行えるかを示します。ここでは、 2
進法表現の浮動小数点数についての基礎的な知識があるものとして話を進めます。

.. % Representation Error
.. % % This section explains the ``0.1'' example in detail, and shows how
.. % % you can perform an exact analysis of cases like this yourself.  Basic
.. % % familiarity with binary floating-point representation is assumed.

:dfn:`表現エラー` は、いくつかの (実際にはほとんどの) 10 進の小数が 2 進法 (基数 2 )
の分数として表現できないという事実に関係しています。これは Python (あるいは Perl、 C、 C++、Japa、Fortran 、および
その他多く) が期待通りの正確な 10 進数を表示できない主要な理由です:

.. % % \dfn{Representation error} refers to the fact that some (most, actually)
.. % % decimal fractions cannot be represented exactly as binary (base 2)
.. % % fractions.  This is the chief reason why Python (or Perl, C, \Cpp,
.. % % Java, Fortran, and many others) often won't display the exact decimal
.. % % number you expect:

::

   >>> 0.1
   0.10000000000000001

なぜこうなるのでしょうか？ 1/10 は 2 進法の分数で厳密に表現することができません。今日 (2000年11月) のマシンは、ほとんどすべて
IEEE-754 浮動小数点演算を使用しており、ほとんどすべてのプラットフォームでは Python の浮動小数点を IEEE-754 における "倍精度
(double precision)"  に対応付けます。754 の double には 53 ビットの精度を持つ数が入るので、
計算機に入力を行おうとすると、可能な限り 0.1 を最も近い値の分数に変換し、
*J*/2\*\**N* の形式にしようと努力します。 *J* はちょうど 53 ビットの精度の整数です。

.. % % Why is that?  1/10 is not exactly representable as a binary fraction.
.. % % Almost all machines today (November 2000) use IEEE-754 floating point
.. % % arithmetic, and almost all platforms map Python floats to IEEE-754
.. % % "double precision".  754 doubles contain 53 bits of precision, so on
.. % % input the computer strives to convert 0.1 to the closest fraction it can
.. % % of the form \var{J}/2**\var{N} where \var{J} is an integer containing
.. % % exactly 53 bits.  Rewriting

::

   1 / 10 ~= J / (2**N)

を書き直すと、

.. % % as

::

   J ~= 2**N / 10

となります。  *J* は厳密に 53 ビットの精度を持っている (``>= 2**52`` だが ``< 2**53`` ) ことを思い出すと、 *N*
として最適な値は 56 になります:

.. % % and recalling that \var{J} has exactly 53 bits (is \code{>= 2**52} but
.. % % \code{< 2**53}), the best value for \var{N} is 56:

::

   >>> 2**52
   4503599627370496L
   >>> 2**53
   9007199254740992L
   >>> 2**56/10
   7205759403792793L

すなわち、56 は *J* をちょうど 53 ビットの精度のままに保つ *N* の唯一の値です。 *J* の取りえる値はその商を丸めたものです:

.. % % That is, 56 is the only value for \var{N} that leaves \var{J} with
.. % % exactly 53 bits.  The best possible value for \var{J} is then that
.. % % quotient rounded:

::

   >>> q, r = divmod(2**56, 10)
   >>> r
   6L

残りは 10 の半分以上なので、最良の近似は丸め値を一つ増やした (round up)  ものになります:

.. % % Since the remainder is more than half of 10, the best approximation is
.. % % obtained by rounding up:

::

   >>> q+1
   7205759403792794L

従って、754 倍精度における 1/10 の取りえる最良の近似は 2\*\*56 以上の値、もしくは

.. % % Therefore the best possible approximation to 1/10 in 754 double
.. % % precision is that over 2**56, or

::

   7205759403792794 / 72057594037927936

となります。丸め値を 1 増やしたので、この値は実際には 1/10 より少し小さいことに注意してください; 丸め値を 1 増やさない場合、商は 1/10
よりもわずかに小さくなります。しかし、どちらにしろ *厳密に* 1/10 ではありません！

.. % % Note that since we rounded up, this is actually a little bit larger than
.. % % 1/10; if we had not rounded up, the quotient would have been a little
.. % % bit smaller than 1/10.  But in no case can it be \emph{exactly} 1/10!

つまり、計算機は 1/10 を "理解する" ことは決してありません:  計算機が理解できるのは、上記のような厳密な分数であり、 754
の倍精度浮動小数点数で得られるもっともよい近似は:

.. % % So the computer never ``sees'' 1/10:  what it sees is the exact
.. % % fraction given above, the best 754 double approximation it can get:

::

   >>> .1 * 2**56
   7205759403792794.0

となります。

この分数に 10\*\*30 を掛ければ、有効数字 30 桁の十進数の  (切り詰められた) 値を見ることができます:

.. % % If we multiply that fraction by 10**30, we can see the (truncated)
.. % % value of its 30 most significant decimal digits:

::

   >>> 7205759403792794 * 10**30 / 2**56
   100000000000000005551115123125L

これは、計算機が記憶している正確な数値が、10 進数値 0.100000000000000005551115123125 にほぼ等しいということです。この値を
有効数字 17 桁で丸めると、Python が表示する値は 0.10000000000000001 になります (もちろんこのような値になるのは、 IEEE
754 に適合していて、C ライブラリで可能な限り正確に値の入出力を行った場合だけです --- 読者の計算機ではそうではないかもしれません！)

.. % % meaning that the exact number stored in the computer is approximately
.. % % equal to the decimal value 0.100000000000000005551115123125.  Rounding
.. % % that to 17 significant digits gives the 0.10000000000000001 that Python
.. % % displays (well, will display on any 754-conforming platform that does
.. % % best-possible input and output conversions in its C library --- yours may
.. % % not!).


