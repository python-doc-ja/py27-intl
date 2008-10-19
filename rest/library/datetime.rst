.. % XXX what order should the types be discussed in?


:mod:`datetime` --- 基本的な日付型および時間型
=================================

.. module:: datetime
   :synopsis: 基本的な日付型および時間型。
.. moduleauthor:: Tim Peters <tim@zope.com>
.. sectionauthor:: Tim Peters <tim@zope.com>
.. sectionauthor:: A.M. Kuchling <amk@amk.ca>


.. versionadded:: 2.3

:mod:`datetime` モジュールでは、日付や時間データを簡単な方法と 複雑な方法の両方で操作するためのクラスを提供しています。
日付や時刻を対象にした四則演算がサポートされている一方で、 このモジュールの実装では出力の書式化や操作を目的とした
データメンバの効率的な取り出しに焦点を絞っています。

日付および時刻オブジェクトには、"naive" および "aware" の 2種類があります。この区別はオブジェクトがタイムゾーン
や夏時間、あるいはその他のアルゴリズム的、政治的な理由に よる時刻の修正に関する何らかの表記をもつかどうかによるものです。
特定の数字がメートルか、マイルか、質量を表すかといったことが プログラムの問題であるように、 naive な :class:`datetime`
オブジェクトが標準世界時 (UTC: Coordinated Universal time) を表現するか、ローカルの時刻を表現するか、
ありは他のいずれかのタイムゾーンにおける時刻を表現するかは 純粋にプログラムの問題となります。 naive な :class:`datetime`
オブジェクトは、 現実世界のいくつかの側面を無視するという犠牲のもとに、 理解しやすく、かつ利用しやすくなっています。

より多くの情報を必要とするアプリケーションのために、 :class:`datetime` および :class:`time` オブジェクトはオプションの
タイムゾーン情報メンバ、:attr:`tzinfo` を持っています。このメンバ には抽象クラス :class:`tzinfo`
のサブクラスのインスタンスが入って います。:class:`tzinfo` オブジェクトは UTC 時刻からのオフセット、
タイムゾーン名、夏時間が有効になっているかどうか、といった情報 を記憶しています。 :mod:`datetime` モジュールでは具体的な
:class:`tsinfo` クラスを 提供していないので注意してください。必要な詳細仕様を備えた タイムゾーン機能を提供するのはアプリケーションの責任です。
世界各国における時刻の修正に関する法則は合理的というよりも政治的な ものであり、全てのアプリケーションに適した標準というものが 存在しないのです。

:mod:`datetime` モジュールでは以下の定数を公開しています:


.. data:: MINYEAR

   :class:`date` や :class:`datetime` オブジェクトで許されている、 年を表現する最小の数字です。:const:`MINYEAR`
   は ``1`` です。


.. data:: MAXYEAR

   :class:`date` や :class:`datetime` オブジェクトで許されている、 年を表現する最大の数字です。:const:`MAXYEAR`
   は ``9999`` です。


.. seealso::

   Module :mod:`calendar`
      汎用のカレンダー関連関数。

   Module :mod:`time`
      時刻へのアクセスと変換。


利用可能なデータ型
---------


.. class:: date

   理想化された naive な日付表現で、実質的には、これまでもこれからも 現在のグレゴリオ暦 (Gregorian calender) であると仮定しています。
   属性: :attr:`year`、 :attr:`month`、および :attr:`day`。


.. class:: time

   理想化された時刻表現で、あらゆる特定の日における影響から独立 しており、毎日厳密に 24\*60\*60 秒であると仮定します ("うるう秒: leap
   seconds" の概念はありません)。 属性: :attr:`hour`、 :attr:`minute`、:attr:`second`、
   :attr:`microsecond`、 および :attr:`tzinfo`。


.. class:: datetime

   日付と時刻を組み合わせたもの。 属性: :attr:`year`、 :attr:`month`、 :attr:`day`、 :attr:`hour`、
   :attr:`minute`、 :attr:`second`、 :attr:`microsecond`、および :attr:`tzinfo`。


.. class:: timedelta

   :class:`date`、:class:`time`、あるいは :class:`datetime` クラスの
   二つのインスタンス間の時間差をマイクロ秒精度で表す経過時間値です。


.. class:: tzinfo

   タイムゾーン情報オブジェクトの抽象基底クラスです。 :class:`datetime` および :class:`time` クラスで用いられ、
   カスタマイズ可能な時刻修正の概念 (たとえばタイムゾーンや 夏時間の計算）を提供します。

これらの型のオブジェクトは変更不可能 (immutable) です。

:class:`date` 型のオブジェクトは常に naive です。

:class:`time` や :class:`datetime` 型のオブジェクト *d* は naive にも aware にもできます。*d* は
``d.tzinfo`` が ``None`` でなく、かつ ``d.tzinfo.utcoffset(d)`` が ``None`` を返さない場合に
aware となります。``d.tzinfo`` が ``None`` の場合や、``d.tzinfo`` は ``None`` では ないが
``d.tzinfo.utcoffset(d)`` が ``None`` を 返す場合には、*d* は naive となります。

naive なオブジェクトと aware なオブジェクトの区別は :class:`timedelta` オブジェクトにはあてはまりません。

サブクラスの関係は以下のようになります::

   object
       timedelta
       tzinfo
       time
       date
           datetime


.. _datetime-timedelta:

:class:`timedelta` オブジェクト
-------------------------

:class:`timedelta` オブジェクトは経過時間、すなわち二つの日付 や時刻間の差を表します。


.. class:: timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])

   全ての引数がオプションで、デフォルト値は*0*です。引数は整数、長整 数、浮動小数点数にすることができ、正でも負でもかまいません。

   *days*、*seconds* および *microseconds* のみが 内部に記憶されます。引数は以下のようにして変換されます:

* 1 ミリ秒は 1000 マイクロ秒に変換されます。

* 1 分は 60 秒に変換されます。

* 1 時間は 3600 秒に変換されます。

* 1 週間は 7 日に変換されます。

   その後、日、秒、マイクロ秒は値が一意に表されるように、

* ``0 <= microseconds < 1000000``

* ``0 <= seconds < 3600*24`` (一日中の秒数)

* ``-999999999 <= days <= 999999999``

   で正規化されます。

   引数のいずれかが浮動小数点であり、小数のマイクロ秒が存在する場合、 小数のマイクロ秒は全ての引数から一度取り置かれ、それらの和は
   最も近いマイクロ秒に丸められます。浮動小数点の引数がない場合、 値の変換と正規化の過程は厳密な (失われる情報がない) ものとなります。

   日の値を正規化した結果、指定された範囲の外側になった場合には、 :exc:`OverflowError` が送出されます。

   負の値を正規化すると、一見混乱するような値になります。 例えば、 ::

      >>> d = timedelta(microseconds=-1)
      >>> (d.days, d.seconds, d.microseconds)
      (-1, 86399, 999999)

クラス属性を以下に示します:


.. attribute:: timedelta.min

   最小の値を表す :class:`timedelta` オブジェクトで、 ``timedelta(-999999999)`` です。


.. attribute:: timedelta.max

   最大の値を表す :class:`timedelta` オブジェクトで、 ``timedelta(days=999999999, hours=23,
   minutes=59, seconds=59, microseconds=999999)`` です。


.. attribute:: timedelta.resolution

   :class:`timedelta` オブジェクトが等しくならない最小の 時間差で、``timedelta(microseconds=1)`` です。

正規化のために、``timedelta.max`` >``-timedelta.min`` となるので注意してください。``-timedelta.max`` は
:class:`timedelta`  オブジェクトとして表現することができません。

以下に (読み出し専用の) インスタンス属性を示します:

+------------------+-----------------------------------+
| 属性               | 値                                 |
+==================+===================================+
| ``days``         | 両端値を含む -999999999 から 999999999 の間 |
+------------------+-----------------------------------+
| ``seconds``      | 両端値を含む 0 から 86399 の間              |
+------------------+-----------------------------------+
| ``microseconds`` | 両端値を含む 0 から 999999 の間             |
+------------------+-----------------------------------+

サポートされている操作を以下に示します:

.. % XXX this table is too wide!

+--------------------------------+-----------------------------------------------+
| 演算                             | 結果                                            |
+================================+===============================================+
| ``t1 = t2 + t3``               | *t2* と *t3* を加算します。演算後、  *t1*-*t2* == *t3*    |
|                                | および *t1*-*t3* == *t2* は 真になります。 (1)           |
+--------------------------------+-----------------------------------------------+
| ``t1 = t2 - t3``               | *t2* と *t3* の差分です。演算後、  *t1* == *t2* - *t3*   |
|                                | および *t2* == *t1* + *t3* は 真になります。 (1)         |
+--------------------------------+-----------------------------------------------+
| ``t1 = t2 * i or t1 = i * t2`` | 整数や長整数による乗算です。演算後、  *t1* // i == *t2* は ``i   |
|                                | != 0`` であれば真となります。                            |
+--------------------------------+-----------------------------------------------+
|                                | 一般的に、 *t1* \* i == *t1* \* (i-1) + *t1*       |
|                                | は真となります。(1)                                   |
+--------------------------------+-----------------------------------------------+
| ``t1 = t2 // i``               | 端数を切り捨てて除算され、剰余 (がある場合) は捨てられます。(3)           |
+--------------------------------+-----------------------------------------------+
| ``+t1``                        | 同じ値を持つ:class:`timedelta` オブジェクトを返します。(2)      |
+--------------------------------+-----------------------------------------------+
| ``-t1``                        | :class:`timedelta`\ (-*t1.days*,              |
|                                | -*t1.seconds*, -*t1.microseconds*)、および *t1*\* |
|                                | -1 と同じです。 (1)(4)                              |
+--------------------------------+-----------------------------------------------+
| ``abs(t)``                     | ``t.days >= 0`` のときには +*t* 、``t.days < 0`` の  |
|                                | ときには -*t* となります。(2)                           |
+--------------------------------+-----------------------------------------------+

注釈:

(1)
   この操作は厳密ですが、オーバフローするかもしれません。

(2)
   この操作は厳密であり、オーバフローしないはずです。

(3)
   0 による除算は  :exc:`ZeroDivisionError` を送出します。

(4)
   -*timedelta.max* は :class:`timedelta` オブジェクトで表現することができません。

上に列挙した操作に加えて、:class:`timedelta` オブジェクトは :class:`date` および :class:`datetime`
オブジェクトとの間で 加減算をサポートしています (下を参照してください)。

:class:`timedelta` オブジェクト間の比較はサポートされており、  より小さい経過時間を表す :class:`timedelta`
オブジェクトが より小さい timedelta と見なされます。 型混合の比較がデフォルトのオブジェクトアドレス比較となってしまう
のを抑止するために、:class:`timedelta` オブジェクトと異なる型の オブジェクトが比較されると、比較演算子が ``==`` または ``!=``
でないかぎり :exc:`TypeError` が送出されます。 後者の場合、それぞれ :const:`False` または :const:`True`
を返します。

:class:`timedelta` オブジェクトはハッシュ可能 (辞書のキーとして利用可能) であり、効率的な pickle
化をサポートします、また、ブール演算コンテキスト では、 :class:`timedelta` オブジェクトは ``timedelta(0)`` に等しくない
場合かつそのときに限り真となります。


.. _datetime-date:

:class:`date` オブジェクト
--------------------

:class:`date` オブジェクトは日付 (年、月、および日) を表します。 日付は理想的なカレンダー、すなわち現在のグレゴリオ暦を過去と未来の
両方向に無限に延長したもので表されます。1 年の 1 月 1 日は日番号 1、 1 年 1 月 2 日は日番号 2、となっていきます。この暦法は、
全ての計算における基本カレンダーである、 Dershowitz と Reingold の書籍 Calendrical Calculations における
"予期的グレゴリオ (proleptic Gregorian)" 暦の定義に一致します。


.. class:: date(year, month, day)

   全ての引数が必要です。引数は整数でも長整数でもよく、以下の範囲に 入らなければなりません:

* ``MINYEAR <= year <= MAXYEAR``

* ``1 <= month <= 12``

* ``1 <= day <= 指定された月と年における日数``

   範囲を超えた引数を与えた場合、:exc:`ValueError` が送出 されます。

他のコンストラクタ、および全てのクラスメソッドを以下に示します:


.. method:: date.today()

   現在のローカルな日付を返します。 ``date.fromtimestamp(time.time())`` と等価です。


.. method:: date.fromtimestamp(timestamp)

   :func:`time.time` が返すような POSIX タイムスタンプ に対応する、ローカルな日付を返します。 タイムスタンプがプラットフォームにおける
   C 関数 :cfunc:`localtime` でサポートされている範囲を超えている場合には :exc:`ValueError` を送出することがあります。
   この値はよく 1970 年から 2038 年に制限されていることがあります。 うるう秒がタイムスタンプの概念に含まれている非 POSIX システム
   では、:meth:`fromtimestamp` はうるう秒を無視します。


.. method:: date.fromordinal(ordinal)

   予期的グレゴリオ暦順序に対応する日付を表し、1 年 1 月 1 日が序数 1  となります。``1 <= ordinal <=
   date.max.toordinal()`` でない場合、:exc:`ValueError` が送出されます。 任意の日付 *d* に対し、
   ``date.fromordinal(d.toordinal()) ==  d`` となります。

以下にクラス属性を示します:


.. attribute:: date.min

   表現できる最も古い日付で、``date(MINYEAR, 1, 1)`` です。


.. attribute:: date.max

   表現できる最も新しい日付で、 ``date(MAXYEAR, 12, 31)`` です。


.. attribute:: date.resolution

   等しくない日付オブジェクト間の最小の差で、 ``timedelta(days=1)`` です。

以下に (読み出し専用の) インスタンス属性を示します:


.. attribute:: date.year

   両端値を含む :const:`MINYEAR` から :const:`MAXYEAR` までの値です。


.. attribute:: date.month

   両端値を含む 1 から 12 までの値です。


.. attribute:: date.day

   1 から与えられた月と年における日数までの値です。

サポートされている操作を以下に示します:

+-------------------------------+---------------------------------------------+
| 演算                            | 結果                                          |
+===============================+=============================================+
| ``date2 = date1 + timedelta`` | *date2* はから *date1* から ``timedelta.days`` 日 |
|                               | 移動した日付です。 (1)                               |
+-------------------------------+---------------------------------------------+
| ``date2 = date1 - timedelta`` | ``date2 + timedelta == date1`` であるような日付     |
|                               | *date2* を計算します。 (2)                         |
+-------------------------------+---------------------------------------------+
| ``timedelta = date1 - date2`` | \(3)                                        |
+-------------------------------+---------------------------------------------+
| ``date1 < date2``             | *date1* が時刻として *date2* よりも前を表す場合に、 *date1*  |
|                               | は*date2* よりも小さいと見なされます。 (4)                 |
+-------------------------------+---------------------------------------------+

注釈:

(1)
   *date2* は ``timedelta.days > 0`` の場合進む方向に、 ``timedelta.days < 0`` の場合戻る方向に移動します。
   演算後は、``date2 - date1 == timedelta.days`` となります。 ``timedelta.seconds`` および
   ``timedelta.microseconds`` は無視されます。 ``date2.year`` が :const:`MINYEAR` になってしまったり、
   :const:`MAXYEAR` より大きくなってしまう場合には :exc:`OverflowError` が送出されます。

(2)
   この操作は date1 + (-timedelta) と等価ではありません。なぜならば、 date1 -
   timedeltaがオーバフローしない場合でも、-timedelta 単体が オーバフローする可能性があるからです。 ``timedelta.seconds``
   および ``timedelta.microseconds`` は無視されます。

(3)
   この演算は厳密で、オーバフローしません。timedelta.seconds および timedelta.microseconds は 0 で、演算後には
   date2 + timedelta == date1 となります。

(4)
   別の言い方をすると、``date1.toordinal() < date2.toordinal()`` であり、かつそのときに限り ``date1 <
   date2`` となります。 型混合の比較がデフォルトのオブジェクトアドレス比較となってしまう のを抑止するために、:class:`timedelta`
   オブジェクトと異なる型の オブジェクトが比較されると :exc:`TypeError` が送出されます。 しかしながら、被比較演算子のもう一方が
   :meth:`timetuple` 属性を 持つ場合には ``NotImplemented`` が返されます。
   このフックにより、他種の日付オブジェクトに型混合比較を実装する チャンスを与えています。 そうでない場合、:class:`timedelta`
   オブジェクトと異なる型の オブジェクトが比較されると、比較演算子が ``==`` または ``!=`` でないかぎり :exc:`TypeError`
   が送出されます。 後者の場合、それぞれ :const:`False` または :const:`True` を返します。

:class:`date` オブジェクトは辞書のキーとして用いることができます。 ブール演算コンテキストでは、全ての :class:`date` オブジェクトは
真であるとみなされます。

以下にインスタンスメソッドを示します:


.. method:: date.replace(year, month, day)

   キーワード引数で指定されたデータメンバが置き換えられることを 除き、同じ値を持つ :class:`date` オブジェクトを返します。 例えば、``d ==
   date(2002, 12, 31)`` とすると、 ``d.replace(day=26) == date(2002, 12, 26)`` となります。


.. method:: date.timetuple()

   :func:`time.localtime` が返す形式の:class:`time.struct_time` を返します。 時間、分、および秒は 0 で、DST
   フラグは -1 になります。 ``d.timetuple()`` は ``time.struct_time((d.year, d.month, d.day,
   0, 0, 0,  d.weekday(),  d.toordinal() - date(d.year, 1, 1).toordinal() + 1,
   -1))`` と等価です。


.. method:: date.toordinal()

   予測的グレゴリオ暦における日付序数を返します。 1 年の 1 月 1 日が 序数 1 となります。任意の :class:`date` オブジェクト *d* に
   ついて、 ``date.fromordinal(d.toordinal()) == d`` となります。


.. method:: date.weekday()

   月曜日を 0、日曜日を 6 として、曜日を整数で返します。 例えば、 ``date(2002, 12, 4).weekday() == 2``
   であり、水曜日を示します。 :meth:`isoweekday` も参照してください。


.. method:: date.isoweekday()

   月曜日を 1、日曜日を 7 として、曜日を整数で返します。 例えば、 ``date(2002, 12, 4).weekday() == 3``
   であり、水曜日を示します。 :meth:`weekday`、:meth:`isocalendar` も参照してください。


.. method:: date.isocalendar()

   3 要素のタプル (ISO 年、ISO 週番号、ISO 曜日) を返します。

   ISO カレンダーはグレゴリオ暦の変種として広く用いられています。 細かい説明については `<http://www.phys.uu.nl/
   vgent/calendar/isocalendar.htm>`_ を参照してください。

   ISO 年は完全な週が 52 または 53 週あり、週は月曜から始まって日曜に 終わります。ISO 年でのある年における最初の週は、その年の木曜日を含む 最初の
   (グレゴリオ暦での) 週となります。この週は週番号 1 と呼ばれ、 この木曜日での ISO 年はグレゴリオ暦における年と等しくなります。

   例えば、2004 年は木曜日から始まるため、ISO 年の最初の週は 2003 年 12 月 29 日、月曜日から始まり、2004 年 1 月 4 日、日曜日に
   終わります。従って、 ``date(2003, 12, 29).isocalendar() == (2004, 1, 1)`` であり、かつ
   ``date(2004, 1, 4).isocalendar() == (2004, 1, 7)`` となります。


.. method:: date.isoformat()

   ISO 8601 形式、'YYYY-MM-DD' の日付を表す文字列を返します。 例えば、 ``date(2002, 12, 4).isoformat() ==
   '2002-12-04'`` となります。


.. method:: date.__str__()

   :class:`date` オブジェクト *d* において、 ``str(d)`` は ``d.isoformat()`` と等価です。


.. method:: date.ctime()

   日付を表す文字列を、例えば date(2002, 12, 4).ctime() == 'Wed Dec  4 00:00:00 2002'
   のようにして返します。 ネイティブの C 関数 :cfunc:`ctime`  (:func:`time.ctime` はこの関数を呼び出しますが、
   :meth:`date.ctime` は呼び出しません) が C 標準に準拠 しているプラットフォームでは、 ``d.ctime()`` は
   ``time.ctime(time.mktime(d.timetuple()))`` と等価です。


.. method:: date.strftime(format)

   明示的な書式化文字列で制御された、日付を表現する文字列を返します。 時間、分、秒を表す書式化コードは値 0 になります。 :meth:`strftime`
   のふるまいについてのセクション :ref:`strftime-behavior`を参照して ください。


.. _datetime-datetime:

:class:`datetime` オブジェクト
------------------------

:class:`datetime` オブジェクトは :class:`date` オブジェクトおよび :class:`time`
オブジェクトの全ての情報が入っている単一のオブジェクト です。:class:`date` オブジェクトと同様に、:class:`datetime` は
現在のグレゴリオ暦が両方向に延長されているものと仮定します; また、:class:`time` オブジェクトと同様に、:class:`datetime` は
毎日が厳密に 3600\*24 秒であると仮定します。

以下にコンストラクタを示します:


.. class:: datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])

   年、月、および日の引数は必須です。*tzinfo* は ``None`` または :class:`tzinfo` クラスのサブクラスのインスタンス
   にすることができます。残りの引数は整数または長整数で、 以下のような範囲に入ります:

* ``MINYEAR <= year <= MAXYEAR``

* ``1 <= month <= 12``

* ``1 <= day <= 与えられた年と月における日数``

* ``0 <= hour < 24``

* ``0 <= minute < 60``

* ``0 <= second < 60``

* ``0 <= microsecond < 1000000``

   引数がこれらの範囲外にある場合、 :exc:`ValueError` が送出されます。

その他のコンストラクタ、およびクラスメソッドを以下に示します:


.. method:: datetime.today()

   現在のローカルな :class:`datetime` を :attr:`tzinfo` が ``None`` であるものとして返します。 これは
   ``datetime.fromtimestamp(time.time())`` と等価です。 :meth:`now`、
   :meth:`fromtimestamp` も参照してください。


.. method:: datetime.now([tz])

   現在のローカルな日付および時刻を返します。オプションの引数 *tz* が ``None`` であるか指定されていない場合、この メソッドは
   :meth:`today` と同様ですが、可能ならば :func:`time.time` タイムスタンプを通じて得ることができる より高い精度で時刻を提供します
   (例えば、プラットフォームが C  関数 :cfunc:`gettimeofday` をサポートする場合には可能なことがあります)。

   そうでない場合、*tz* はクラス :class:`tzinfo` のサブクラスの インスタンスでなければならず、現在の日付および時刻は *tz*
   のタイムゾーンに変換されます。この場合、結果は ``tz.fromutc(datetime.utcnow().replace(tzinfo=tz))``
   と等価になります。 :meth:`today`, :meth:`utcnow` も参照してください。


.. method:: datetime.utcnow()

   現在の UTC における日付と時刻を、 :attr:`tzinfo` が ``None`` で あるものとして返します。このメソッドは :meth:`now`
   に似ていますが、 現在の UTC における日付と時刻を naive な :class:`datetime` オブジェクト として返します。:meth:`now`
   も参照してください。


.. method:: datetime.fromtimestamp(timestamp[, tz])

   :func:`time.time` が返すような、POSIX タイムスタンプに 対応するローカルな日付と時刻を返します。 オプションの引数 *tz* が
   ``None`` であるか、指定されて いない場合、タイムスタンプはプラットフォームのローカルな日付および 時刻に変換され、返される
   :class:`datetime` オブジェクトは naive  なものになります。

   そうでない場合、 *tz* はクラス :class:`tzinfo` のサブクラスの インスタンスでなければならず、現在の日付および時刻は *tz*
   のタイムゾーンに変換されます。この場合、結果は
   ``tz.fromutc(datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz))``
   と等価になります。

   タイムスタンプがプラットフォームの C 関数 :cfunc:`localtime` や :cfunc:`gmtime` でサポートされている範囲を超えた場合、
   :meth:`fromtimestamp` は :exc:`ValueError` を送出する ことがあります。この範囲はよく 1970 年から 2038
   年に制限されて います。 うるう秒がタイムスタンプの概念に含まれている非 POSIX システム では、:meth:`fromtimestamp`
   はうるう秒を無視します。 このため、秒の異なる二つのタイムスタンプが同一の :class:`datetime` オブジェクトとなることが起こり得ます。
   :meth:`utcfromtimestamp` も参照してください。


.. method:: datetime.utcfromtimestamp(timestamp)

   :func:`time.time` が返すような POSIX タイムスタンプ に対応する、UTC での :class:`datetime`
   オブジェクトを返します。 タイムスタンプがプラットフォームにおける C 関数 :cfunc:`localtime` でサポートされている範囲を超えている場合には
   :exc:`ValueError` を送出することがあります。 この値はよく 1970 年から 2038 年に制限されていることがあります。
   :meth:`fromtimestamp` も参照してください。


.. method:: datetime.fromordinal(ordinal)

   1 年 1 月 1 日を序数 1 とする予測的グレゴリオ暦序数に対応する :class:`datetime` オブジェクトを返します。 ``1 <=
   ordinal <=  datetime.max.toordinal()`` でないかぎり :exc:`ValueError`
   が送出されます。結果として返される オブジェクトの時間、分、秒、およびマイクロ秒はすべて 0 となり、 :attr:`tzinfo` は ``None``
   となります。


.. method:: datetime.combine(date, time)

   与えられた :class:`date` オブジェクトと同じデータメンバを持ち、 時刻と :attr:`tzinfo` メンバが与えられた
   :class:`time` オブジェクト と等しい、新たな :class:`datetime` オブジェクトを返します。 任意の
   :class:`datetime` オブジェクト *d* について、 ``d == datetime.combine(d.date(),
   d.timetz())`` となります。*date* が :class:`datetime` オブジェクトの場合、 その時刻と :attr:`tzinfo`
   は無視されます。


.. method:: datetime.strptime(date_string, format)

   *date_string* に対応した:class:`datetime` をかえします。 *format*にしたがって構文解析されます。これは、
   ``datetime(*(time.strptime(date_string, format)[0:6]))`` と等価です。
   date_stringとformatが:func:`time.strptime`で構文解析できない場合 や、この関数が
   時刻タプルを返してこない場合には:exc:`ValueError` がおこります。

   .. versionadded:: 2.5

以下にクラス属性を示します:


.. attribute:: datetime.min

   表現できる最も古い :class:`datetime` で、 ``datetime(MINYEAR, 1, 1, tzinfo=None)`` です。


.. attribute:: datetime.max

   表現できる最も新しい :class:`datetime` で、 ``datetime(MAXYEAR, 12, 31, 23, 59, 59, 999999,
   tzinfo=None)`` です。


.. attribute:: datetime.resolution

   等しくない :class:`datetime` オブジェクト間の最小の差で、  ``timedelta(microseconds=1)`` です。

以下に (読み出し専用の) インスタンス属性を示します:


.. attribute:: datetime.year

   両端値を含む :const:`MINYEAR` から :const:`MAXYEAR` までの値です。


.. attribute:: datetime.month

   両端値を含む 1 から 12 までの値です。


.. attribute:: datetime.day

   1 から与えられた月と年における日数までの値です。


.. attribute:: datetime.hour

   ``range(24)`` 内の値です。


.. attribute:: datetime.minute

   ``range(60)`` 内の値です。


.. attribute:: datetime.second

   ``range(60)`` 内の値です。


.. attribute:: datetime.microsecond

   ``range(1000000)`` 内の値です。


.. attribute:: datetime.tzinfo

   :class:`datetime` コンストラクタに *tzinfo* 引数として 与えられたオブジェクトになり、何も渡されなかった場合には ``None``
   になります。

以下にサポートされている演算を示します:

+---------------------------------------+-----------------------------------------------+
| 演算                                    | 結果                                            |
+=======================================+===============================================+
| ``datetime2 = datetime1 + timedelta`` | \(1)                                          |
+---------------------------------------+-----------------------------------------------+
| ``datetime2 = datetime1 - timedelta`` | \(2)                                          |
+---------------------------------------+-----------------------------------------------+
| ``timedelta = datetime1 - datetime2`` | \(3)                                          |
+---------------------------------------+-----------------------------------------------+
| ``datetime1 < datetime2``             | :class:`datetime` を :class:`datetime` と比較します。 |
|                                       | (4)                                           |
+---------------------------------------+-----------------------------------------------+

(1)
   datetime2 は datetime1 から時間 timedelta 移動したもので、 ``timedelta.days > 0`` の場合進む方向に、
   ``timedelta.days < 0`` の場合戻る方向に移動します。 結果は入力の datetime と同じ :attr:`tzinfo` を持ち、
   演算後には datetime2 - datetime1 == timedelta となります。 datetime2.year が
   :const:`MINYEAR` よりも小さいか、 :const:`MAXYEAR` より大きい場合には :exc:`OverflowError`
   が送出されます。 入力が aware なオブジェクトの場合でもタイムゾーン修正は全く行われ ません。

(2)
   datetime2 + timedelta == datetime1 となるような datetime2 を 計算します。ちなみに、結果は入力の datetime
   と同じ :attr:`tzinfo` メンバを持ち、入力が aware でもタイムゾーン修正は全く行われ ません。 この操作は date1 +
   (-timedelta) と等価ではありません。なぜならば、 date1 - timedeltaがオーバフローしない場合でも、-timedelta 単体が
   オーバフローする可能性があるからです。

(3)
   :class:`datetime` から :class:`datetime` の減算は両方の被演算子が naive であるか、両方とも aware
   である場合にのみ定義されています 片方が aware でもう一方が naive の場合、 :exc:`TypeError`  が送出されます。

   両方とも naive か、両方とも aware で同じ :attr:`tzinfo` メンバ を持つ場合、:attr:`tzinfo` メンバは無視され、結果は
   ``datetime2 + t == datetime1`` であるような :class:`timedelta` オブジェクト *t* となります。
   この場合タイムゾーン修正は全く行われません。

   両方が aware で異なる :attr:`tzinfo` メンバを持つ場合、 ``a-b`` は *a* および *b* をまず naive な UTC
   datetime オブジェクトに変換したかのようにして行います。演算結果は 決してオーバフローを起こさないことを除き、
   ``(a.replace(tzinfo=None) - a.utcoffset()) - (b.replace(tzinfo=None) -
   b.utcoffset())`` と同じになります。

(4)
   *datetime1* が時刻として *datetime2* よりも前を表す場合に、 *datetime1* は*datetime2*
   よりも小さいと見なされます。

   被演算子の片方が naive でもう一方が aware の場合、 :exc:`TypeError` が送出されます。両方の被演算子が aware で、 同じ
   :attr:`tzinfo` メンバを持つ場合、共通の :attr:`tzinfo` メンバは無視され、基本の datetime 間の比較が行われます。
   両方の被演算子が aware で異なる :attr:`tzinfo` メンバを持つ 場合、被演算子はまず (``self.utcoffset()``
   で得られる) UTC  オフセット で修正されます。

   .. note::

      型混合の比較がデフォルトのオブジェクトアドレス比較となってしまう のを抑止するために、被演算子のもう一方が :class:`datatime` オブジェクトと
      異なる型のオブジェクトの場合には :exc:`TypeError` が送出されます。 しかしながら、被比較演算子のもう一方が :meth:`timetuple`
      属性を 持つ場合には ``NotImplemented`` が返されます。 このフックにより、他種の日付オブジェクトに型混合比較を実装する
      チャンスを与えています。 そうでない場合、:class:`datetime` オブジェクトと異なる型の オブジェクトが比較されると、比較演算子が ``==``
      または ``!=`` でないかぎり :exc:`TypeError` が送出されます。 後者の場合、それぞれ :const:`False` または
      :const:`True` を返します。

:class:`datetime` オブジェクトは辞書のキーとして用いることができます。 ブール演算コンテキストでは、全ての :class:`datetime`
オブジェクトは 真であるとみなされます。

インスタンスメソッドを以下に示します:


.. method:: datetime.date()

   同じ年、月、日の :class:`date` オブジェクトを返します。


.. method:: datetime.time()

   同じ時、分、秒、マイクロ秒を持つ :class:`time` オブジェクトを返します。 :attr:`tzinfo` は ``None``
   です。:meth:`timetz` も参照 してください。


.. method:: datetime.timetz()

   同じ時、分、秒、マイクロ秒、および tzinfo メンバを持つ :class:`time` オブジェクトを返します。 :meth:`time`
   メソッドも参照してください。


.. method:: datetime.replace([year[, month[, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]]]]])

   キーワード引数で指定したメンバの値を除き、同じ値をもつ datetime  オブジェクトを返します。 メンバに対する変換を行わずに aware な
   datetime オブジェクトから  naive な datetime オブジェクトを生成するために、 ``tzinfo=None``
   を指定することもできます。


.. method:: datetime.astimezone(tz)

   :class:`datetime` オブジェクトを返します。返されるオブジェクトは 新たな :attr:`tzinfo` メンバ *tz* を持ちます。*tz*
   は日付および時刻を調整して、オブジェクトが *self* と同じ UTC 時刻を持つが、*tz* におけるローカルな時刻を表すようにします。

   *tz* は :class:`tzinfo` のサブクラスのインスタンスでなければ ならず、インスタンスの :meth:`utcoffset` および
   :meth:`dst`  メソッドは ``None`` を返してはなりません。*self* は aware でなくてはなりません
   (``self.tzinfo`` が ``None`` であってはならず、かつ ``self.utcoffset()`` は ``None``
   を返してはなりません)。

   ``self.tzinfo`` が *tz* の場合、 ``self.astimezone(tz)`` は *self* に等しくなります:
   日付および時刻データメンバに対する調整は行われません。 そうでない場合、結果はタイムゾーン *tz* におけるローカル時刻で、 *self* と同じ UTC
   時刻を表すようになります: ``astz = dt.astimezone(tz)`` とした後、 ``astz - astz.utcoffset()``
   は通常 ``dt - dt.utcoffset()`` と同じ日付および時刻 データメンバを持ちます。 :class:`tzinfo`
   クラスに関する議論では、夏時間 (Daylight Saving time) の遷移境界では上の等価性が成り立たないことを説明しています (*tz*
   が標準時と夏時間の両方をモデル化している場合のみの問題です)。

   単にタイムゾーンオブジェクト *tz* を :class:`datetime` オブジェクト *dt* に追加したいだけで、日付や時刻データメンバへの調整
   を行わないのなら、``dt.replace(tzinfo=tz)`` を使って ください。 単に aware な :class:`datetime`
   オブジェクト *dt* からタイムゾーン オブジェクトを除去したいだけで、日付や時刻データメンバの変換を
   行わないのなら、``dt.replace(tzinfo=None)`` を使ってください。

   デフォルトの :meth:`tzinfo.fromutc` メソッドを :class:`tzinfo`
   のサブクラスで上書きして、:meth:`astimezone` が返す結果に 影響を及ぼすことができます。エラーの場合を無視すると、
   :meth:`astimezone` は以下のように動作します::

      def astimezone(self, tz):
          if self.tzinfo is tz:
              return self
          # Convert self to UTC, and attach the new time zone object.
          utc = (self - self.utcoffset()).replace(tzinfo=tz)
          # Convert from UTC to tz's local time.
          return tz.fromutc(utc)


.. method:: datetime.utcoffset()

   :attr:`tzinfo` が ``None`` の場合、``None`` を返し、 そうでない場合には
   ``self.tzinfo.utcoffset(self)`` を返します。後者の式が ``None`` か、1 日以下の大きさを持つ 経過時間を表す
   :class:`timedelta` オブジェクトのいずれかを返さない 場合には例外を送出します。


.. method:: datetime.dst()

   :attr:`tzinfo` が ``None`` の場合、``None`` を返し、 そうでない場合には ``self.tzinfo.dst(self)``
   を返します。後者の式が ``None`` か、1 日以下の大きさを持つ 経過時間を表す :class:`timedelta` オブジェクトのいずれかを返さない
   場合には例外を送出します。


.. method:: datetime.tzname()

   :attr:`tzinfo` が ``None`` の場合、``None`` を返し、 そうでない場合には
   ``self.tzinfo.tzname(self)`` を返します。後者の式が ``None`` か文字列オブジェクトのいずれか
   を返さない場合には例外を送出します。


.. method:: datetime.timetuple()

   :func:`time.localtime` が返す形式の :class:`time.struct_time` を返します。 ``d.timetuple()``
   は ``time.struct_time((d.year, d.month, d.day, d.hour, d.minute, d.second,
   d.weekday(), d.toordinal() - date(d.year, 1, 1).toordinal() + 1, dst))`` と等価です。
   返されるタプルの :attr:`tm_isdst` フラグは :meth:`dst` メソッドに 従って設定されます:  :attr:`tzinfo` が
   ``None`` か :meth:`dst` が ``None`` を返す場合、 :attr:`tm_isdst` は ``-1`` に設定されます;
   そうでない場合、 :meth:`dst` がゼロでない値を返すと、:attr:`tm_isdst` は ``1`` となります; それ以外の場合には
   ``tm_isdst`` は``0`` に設定 されます。


.. method:: datetime.utctimetuple()

   :class:`datetime` インスタンス *d* が naive の場合、このメソッドは ``d.timetuple()``
   と同じであり、``d.dst()`` の返す内容に かかわらず :attr:`tm_isdst` が 0 に強制される点だけが異なります。 DST が UTC
   時刻に影響を及ぼすことは決してありません。

   *d* が aware の場合、*d* から ``d.utcoffset()`` が差し 引かれて UTC 時刻に正規化され、正規化された時刻の
   :class:`time.struct_time` を返します。:attr:`tm_isdst` は 0 に強制されます。 *d*.year が
   ``MINYEAR`` や ``MAXUEAR`` で、UTC への修正の結果 表現可能な年の境界を越えた場合には、戻り値の :attr:`tm_year`
   メンバは :const:`MINYEAR`\ -1 または :const:`MAXYEAR`\ +1 になることがあります。


.. method:: datetime.toordinal()

   予測的グレゴリオ暦における日付序数を返します。 ``self.date().toordinal()`` と同じです。


.. method:: datetime.weekday()

   月曜日を 0、日曜日を 6 として、曜日を整数で返します。 ``self.date().weekday()`` と同じです。
   :meth:`isoweekday` も参照してください。


.. method:: datetime.isoweekday()

   月曜日を 1、日曜日を 7 として、曜日を整数で返します。 ``self.date().isoweekday()`` と等価です。
   :meth:`weekday`、 :meth:`isocalendar` も参照してください。


.. method:: datetime.isocalendar()

   3 要素のタプル (ISO 年、ISO 週番号、ISO 曜日) を返します。 ``self.date().isocalendar()`` と等価です。


.. method:: datetime.isoformat([sep])

   日付と時刻を ISO 8601 形式、すなわち YYYY-MM-DDTHH:MM:SS.mmmmmm か、 :attr:`microsecond` が 0
   の場合には YYYY-MM-DDTHH:MM:SS で表した文字列を返します。 :meth:`utcoffset` が ``None`` を返さない場合、
   UTC からのオフセットを時間と分を表した (符号付きの) 6 文字からなる  文字列が追加されます: すなわち、 YYYY-MM-
   DDTHH:MM:SS.mmmmmm+HH:MM となるか、 :attr:`microsecond` が ゼロの場合には YYYY-MM-
   DDTHH:MM:SS+HH:MM となります。 オプションの引数 *sep* (デフォルトでは ``'T'`` です)  は 1
   文字のセパレータで、結果の文字列の日付と時刻の間に置かれます。 例えば、 ::

      >>> from datetime import tzinfo, timedelta, datetime
      >>> class TZ(tzinfo):
      ...     def utcoffset(self, dt): return timedelta(minutes=-399)
      ...
      >>> datetime(2002, 12, 25, tzinfo=TZ()).isoformat(' ')
      '2002-12-25 00:00:00-06:39'

   となります。


.. method:: datetime.__str__()

   :class:`datetime` オブジェクト *d* において、 ``str(d)`` は ``d.isoformat(' ')`` と等価です。


.. method:: datetime.ctime()

   日付を表す文字列を、例えば ``datetime(2002, 12, 4, 20, 30, 40).ctime() == 'Wed Dec  4
   20:30:40 2002'`` のようにして返します。 ネイティブの C 関数 :cfunc:`ctime`  (:func:`time.ctime`
   はこの関数を呼び出しますが、 :meth:`datetime.ctime` は呼び出しません) が C 標準に準拠 しているプラットフォームでは、
   ``d.ctime()`` は ``time.ctime(time.mktime(d.timetuple()))`` と等価です。


.. method:: datetime.strftime(format)

   明示的な書式化文字列で制御された、日付を表現する文字列を返します。 :meth:`strftime` のふるまいについてのセクション
   :ref:`strftime-behavior`を参照して ください。


.. _datetime-time:

:class:`time` オブジェクト
--------------------

:class:`time` オブジェクトは (ローカルの) 日中時刻を表現します。 この時刻表現は特定の日の影響を受けず、:class:`tzinfo`
オブジェクト を介した修正の対象となります。


.. class:: time(hour[, minute[, second[, microsecond[, tzinfo]]]])

   全ての引数はオプションです。*tzinfo* は ``None`` または :class:`tzinfo` クラスのサブクラスのインスタンス
   にすることができます。残りの引数は整数または長整数で、 以下のような範囲に入ります:

* ``0 <= hour < 24``

* ``0 <= minute < 60``

* ``0 <= second < 60``

* ``0 <= microsecond < 1000000``.

   引数がこれらの範囲外にある場合、 :exc:`ValueError` が送出されます。 *tzinfo*のデフォルト値が
   :const:`None`である以外のデフォルト値は*0*です。

以下にクラス属性を示します:


.. attribute:: time.min

   表現できる最も古い :class:`datetime` で、 ``time(0, 0, 0, 0)`` です。 The earliest
   representable :class:`time`, ``time(0, 0, 0, 0)``.


.. attribute:: time.max

   表現できる最も新しい :class:`datetime` で、 ``time(23, 59, 59, 999999, tzinfo=None)`` です。


.. attribute:: time.resolution

   等しくない :class:`datetime` オブジェクト間の最小の差で、  ``timedelta(microseconds=1)``
   ですが、:class:`time` オブジェクト間の四則演算はサポートされて いないので注意してください。

以下に (読み出し専用の) インスタンス属性を示します:


.. attribute:: time.hour

   ``range(24)`` 内の値です。


.. attribute:: time.minute

   ``range(60)`` 内の値です。


.. attribute:: time.second

   ``range(60)`` 内の値です。


.. attribute:: time.microsecond

   ``range(1000000)`` 内の値です。


.. attribute:: time.tzinfo

   :class:`time` コンストラクタに *tzinfo* 引数として 与えられたオブジェクトになり、何も渡されなかった場合には ``None``
   になります。

以下にサポートされている操作を示します:

* :class:`time` と :class:`time` の比較では、*a* が時刻として *b* よりも前を表す場合に *a* は *b*
  よりも小さいと見なされます。 被演算子の片方が naive でもう一方が aware の場合、 :exc:`TypeError`
  が送出されます。両方の被演算子が aware で、 同じ :attr:`tzinfo` メンバを持つ場合、共通の :attr:`tzinfo`
  メンバは無視され、基本の datetime 間の比較が行われます。 両方の被演算子が aware で異なる :attr:`tzinfo` メンバを持つ
  場合、被演算子はまず (``self.utcoffset()`` で得られる) UTC  オフセット で修正されます。
  型混合の比較がデフォルトのオブジェクトアドレス比較となってしまう のを抑止するために、:class:`time` オブジェクトが他の型のオブジェクトと
  比較された場合、比較演算子が ``==`` または ``!=`` でないかぎり :exc:`TypeError` が送出されます。 後者の場合、それぞれ
  :const:`False` または :const:`True` を返します。

* ハッシュ化、辞書のキーとしての利用

* 効率的な pickle 化

* ブール演算コンテキストでは、:class:`time` オブジェクトは、 分に変換し、:meth:`utfoffset` (``None``
  を返した場合には ``0``) を差し引いて変換した後の結果がゼロでない場合、かつその ときに限って真とみなされます。

以下にインスタンスメソッドを示します:


.. method:: time.replace([hour[, minute[, second[, microsecond[, tzinfo]]]]])

   キーワード引数で指定したメンバの値を除き、同じ値をもつ :class:`time` オブジェクトを返します。 メンバに対する変換を行わずに aware な
   datetime オブジェクトから  naive な :class:`time` オブジェクトを生成するために、 ``tzinfo=None``
   を指定することもできます。


.. method:: time.isoformat()

   日付と時刻を ISO 8601 形式、すなわち HH:MM:SS.mmmmmm か、 :attr:`microsecond` が 0 の場合には
   HH:MM:SS で表した文字列を返します。 :meth:`utcoffset` が ``None`` を返さない場合、 UTC
   からのオフセットを時間と分を表した (符号付きの) 6 文字からなる  文字列が追加されます: すなわち、 HH:MM:SS.mmmmmm+HH:MM
   となるか、 :attr:`microsecond` が 0 の場合には HH:MM:SS+HH:MM となります。


.. method:: time.__str__()

   :class:`time` オブジェクト *t* において、 ``str(t)`` は ``t.isoformat()`` と等価です。


.. method:: time.strftime(format)

   明示的な書式化文字列で制御された、日付を表現する文字列を返します。 :meth:`strftime` のふるまいについてのセクション
   :ref:`strftime-behavior`を参照して ください。


.. method:: time.utcoffset()

   :attr:`tzinfo` が ``None`` の場合、``None`` を返し、 そうでない場合には
   ``self.tzinfo.utcoffset(None)`` を返します。後者の式が ``None`` か、1 日以下の大きさを持つ 経過時間を表す
   :class:`timedelta` オブジェクトのいずれかを返さない 場合には例外を送出します。


.. method:: time.dst()

   :attr:`tzinfo` が ``None`` の場合、``None`` を返し、 そうでない場合には ``self.tzinfo.dst(None)``
   を返します。後者の式が ``None`` か、1 日以下の大きさを持つ 経過時間を表す :class:`timedelta` オブジェクトのいずれかを返さない
   場合には例外を送出します。


.. method:: time.tzname()

   :attr:`tzinfo` が ``None`` の場合、``None`` を返し、 そうでない場合には
   ``self.tzinfo.tzname(None)`` を返します。後者の式が ``None`` か文字列オブジェクトのいずれか
   を返さない場合には例外を送出します。


.. _datetime-tzinfo:

:class:`tzinfo` オブジェクト
----------------------

:class:`tzinfo` は抽象基底クラスです。つまり、このクラスは直接 インスタンス化して利用しません。具体的なサブクラスを導出し、 (少なくとも)
利用したい :class:`datetime` のメソッドが必要と する :class:`tzinfo` の標準メソッドを実装してやる必要があります。
:mod:`datetime` モジュールでは、:class:`tzinfo` の具体的な サブクラスは何ら提供していません。

:class:`tzinfo` (の具体的なサブクラス) のインスタンスは :class:`datetime` および :class:`time`
オブジェクトのコンストラクタに 渡すことができます。 後者のオブジェクトでは、データメンバをローカル時刻におけるものとして
見ており、:class:`tzinfo` オブジェクトはローカル時刻の UTC からの オフセット、タイムゾーンの名前、DST オフセットを、渡された
日付および時刻オブジェクトからの相対で示すためのメソッドを 提供します。

pickle 化についての特殊な要求事項: :class:`tzinfo` のサブクラスは 引数なしで呼び出すことのできる :meth:`__init__`
メソッドを持たねば なりません。そうでなければ、pickle 化することはできますがおそらく unpickle
化することはできないでしょう。これは技術的な側面からの 要求であり、将来緩和されるかもしれません。

:class:`tzinfo` の具体的なサブクラスでは、以下のメソッドを 実装する必要があります。厳密にどのメソッドが必要なのかは、 aware な
:mod:`datetime` オブジェクトがこのサブクラスの インスタンスをどのように使うかに依存します。不確かならば、 単に全てを実装してください。


.. method:: tzinfo.utcoffset(self, dt)

   ローカル時間の UTC からのオフセットを、UTC から東向きを正とした分で 返します。ローカル時間が UTC の西側にある場合、この値は負になります。
   このメソッドは UTC からのオフセットの総計を返すように意図されている ので注意してください; 例えば、 :class:`tzinfo` オブジェクトが
   タイムゾーンと DST 修正の両方を表現する場合、:meth:`utcoffset` はそれらの合計を返さなければなりません。UTC オフセットが未知である
   場合、``None`` を返してください。そうでない場合には、 返される値は -1439 から 1439 の両端を含む値 (1440 = 24\*60 ;
   つまり、オフセットの大きさは 1 日より短くなくてはなりません) が分で指定された :class:`timedelta` オブジェクトでなければなりません。
   ほとんどの :meth:`utcoffset` 実装は、おそらく以下の二つのうちの一つに 似たものになるでしょう::

      return CONSTANT                 # fixed-offset class
      return CONSTANT + self.dst(dt)  # daylight-aware class

   :meth:`utcoffset` が ``None`` を返さない場合、 :meth:`dst` も ``None`` を返してはなりません。

   :meth:`utcoffset` のデフォルトの実装は :exc:`NotImplementedError` を送出します。


.. method:: tzinfo.dst(self, dt)

   夏時間 (DST) 修正を、UTC から東向きを正とした分で 返します。DST 情報が未知の場合、``None`` が返されます。 DST が有効でない場合には
   ``timedelta(0)`` を返します。 DST が有効の場合、オフセットは :class:`timedelta` オブジェクト で返します
   (詳細は:meth:`utcoffset` を参照してください)。 DST オフセットが利用可能な場合、この値は :meth:`utcoffset`
   が返すUTC からのオフセットには既に加算されているため、 DST を個別に取得する必要がない限り :meth:`dst` を使って
   問い合わせる必要はないので注意してください。 例えば、:meth:`datetime.timetuple` は :attr:`tzinfo` メンバ の
   :meth:`dst` メソッドを呼んで :attr:`tm_isdst` フラグが
   セットされているかどうか判断し、:meth:`tzinfo.fromutc`  は :meth:`dst` タイムゾーンを移動する際に DST による変更
   があるかどうかを調べます。

   標準および夏時間の両方をモデル化している :class:`tzinfo` サブクラスの インスタンス *tz* は以下の式:

   ``tz.utcoffset(dt) - tz.dst(dt)``

   が、``dt.tzinfo == tz`` 全ての :class:`datetime` オブジェクト *dt*
   について常に同じ結果を返さなければならないという点で、 一貫性を持っていなければなりません。 正常に実装された :class:`tzinfo`
   のサブクラスでは、この式は タイムゾーンにおける "標準オフセット (standard offset)" を表し、
   特定の日や時刻の事情ではなく地理的な位置にのみ依存していなくては なりません。:meth:`datetime.astimezone` の実装はこの事実に
   依存していますが、違反を検出することができません; 正しく実装するのはプログラマの責任です。:class:`tzinfo` の
   サブクラスでこれを保証することができない場合、:meth:`tzinfo.fromutc`  の実装をオーバライドして、:meth:`astimezone`
   に関わらず 正しく動作するようにしてもかまいません。

   ほとんどの :meth:`dst` 実装は、おそらく以下の二つのうちの一つに 似たものになるでしょう::

      def dst(self):
          # a fixed-offset class:  doesn't account for DST
          return timedelta(0)

   or ::

      def dst(self):
          # Code to set dston and dstoff to the time zone's DST
          # transition times based on the input dt.year, and expressed
          # in standard local time.  Then

          if dston <= dt.replace(tzinfo=None) < dstoff:
              return timedelta(hours=1)
          else:
              return timedelta(0)

   デフォルトの :meth:`dst` 実装は :exc:`NotImplementedError` を送出します。


.. method:: tzinfo.tzname(self, dt)

   :class:`datetime` オブジェクト *dt* に対応するタイムゾーン名 を文字列で返します。 :mod:`datetime`
   モジュールでは文字列名について何も定義しておらず、 特に何かを意味するといった要求仕様もまったくありません。 例えば、"GMT"、"UTC"、 "-500"、
   "-5:00"、  "EDT"、 "US/Eastern"、 "America/New York" は全て有効な応答となります。 文字列名が未知の場合には
   ``None`` を返してください。 :class:`tzinfo` のサブクラスでは、 特に、:class:`tzinfo`
   クラスが夏時間について記述している場合のように、 渡された *dt* の特定の値によって異なった名前を返したい
   場合があるため、文字列値ではなくメソッドとなっていることに注意してください。

   デフォルトの :meth:`tzname` 実装は :exc:`NotImplementedError` を送出します。

以下のメソッドは :class:`datetime` や :class:`time` オブジェクトにおいて、
同名のメソッドが呼び出された際に応じて呼び出されます。:class:`datetime`
オブジェクトは自身を引数としてメソッドに渡し、:class:`time` オブジェクトは 引数として ``None``
をメソッドに渡します。従って、:class:`tzinfo` の サブクラスにおけるメソッドは引数 *dt* が ``None`` の場合と、
:class:`datetime` の場合を受理するように用意しなければなりません。

``None`` が渡された場合、最良の応答方法を決めるのはクラス設計者次第 です。例えば、このクラスが :class:`tzinfo`
プロトコルと関係をもたない ということを表明させたければ、``None`` が適切です。 標準時のオフセットを見つける他の手段がない場合には、 標準 UTC
オフセットを返すために ``utcoffset(None)`` を使うともっと便利かもしれません。

:class:`datetime` オブジェクトが :meth:`datetime` メソッド の応答として返された場合、``dt.tzinfo`` は
*self* と同じオブジェクトになります。ユーザが直接 :class:`tzinfo` メソッド を呼び出さないかぎり、:class:`tzinfo`
メソッドは ``dt.tzinfo`` と *self* が同じであることに依存します。 その結果 :class:`tzinfo` メソッドは *dt*
がローカル時間であると 解釈するので、他のタイムゾーンでのオブジェクトの振る舞いについて 心配する必要がありません。


.. method:: tzinfo.fromutc(self, dt)

   デフォルトの :class:`datetime.astimezone()` 実装で呼び出されます。 :class:`datetime.astimezone()`
   から呼ばれた場合、``dt.tzinfo`` は *self* であり、 *dt* の日付および時刻データメンバは UTC
   時刻を表しているものとして見えます。:meth:`fromutc`  の目的は、*self* のローカル時刻に等しい :class:`datetime`
   オブジェクト を返すことにより日付と時刻データメンバを修正することにあります。

   ほとんどの :class:`tzinfo` サブクラスではデフォルトの :meth:`fromutc`
   実装を問題なく継承できます。デフォルトの実装は、固定オフセットのタイムゾーン や、標準時と夏時間の両方について記述しているタイムゾーン、そして DST
   移行時刻が年によって異なる場合でさえ、扱えるくらい強力なものです。 デフォルトの :meth:`fromutc` 実装が全ての場合に対して正しく
   扱うことができないような例は、標準時の (UTCからの) オフセットが 引数として渡された特定の日や時刻に依存するもので、これは政治的な理由に
   よって起きることがあります。 デフォルトの :meth:`astimezone` や :meth:`fromutc` の実装は、
   結果が標準時オフセットの変化にまたがる何時間かの中にある場合、 期待通りの結果を生成しないかもしれません。

   エラーの場合のためのコードを除き、デフォルトの :meth:`fromutc` の 実装は以下のように動作します::

      def fromutc(self, dt):
          # raise ValueError error if dt.tzinfo is not self
          dtoff = dt.utcoffset()
          dtdst = dt.dst()
          # raise ValueError if dtoff is None or dtdst is None
          delta = dtoff - dtdst  # this is self's standard offset
          if delta:
              dt += delta   # convert to standard local time
              dtdst = dt.dst()
              # raise ValueError if dtdst is None
          if dtdst:
              return dt + dtdst
          else:
              return dt

以下に :class:`tzinfo` クラスの使用例を示します:


.. include:: ../includes/tzinfo-examples.py
   :literal:

標準時間 (standard time) および夏時間 (daylight time) の両方を 記述している :class:`tzinfo`
のサブクラスでは、回避不能の難解な問題が年に 2 度あるので注意してください。具体的な例として、東部アメリカ時刻 (US Eastern, UTC -5000)
を考えます。EDT は 4 月の最初の日曜日 の 1:59 (EST) 以後に開始し、10 月の最後の日曜日の 1:59 (EDT) に 終了します::

     UTC   3:MM  4:MM  5:MM  6:MM  7:MM  8:MM
     EST  22:MM 23:MM  0:MM  1:MM  2:MM  3:MM
     EDT  23:MM  0:MM  1:MM  2:MM  3:MM  4:MM

   start  22:MM 23:MM  0:MM  1:MM  3:MM  4:MM

     end  23:MM  0:MM  1:MM  1:MM  2:MM  3:MM

DST の開始の際 ("start" の並び) ローカルの壁時計は 1:59 から 3:00 に飛びます。この日は 2:MM の形式をとる時刻は実際には無意味と
なります。従って、``astimezone(Eastern)`` は DST が開始する 日には ``hour == 2`` となる結果を返すことはありません。
:meth:`astimezone` がこのことを保証するようにするには、 :meth:`tzinfo.dst` メソッドは "失われた時間"
(東部時刻における 2:MM) が夏時間に存在することを考えなければなりません。

DST が終了する際 ("end" の並び) では、問題はさらに悪化します: 1 時間の間、ローカルの壁時計ではっきりと時刻をいえなくなります:
それは夏時間の最後の 1 時間です。東部時刻では、その日の UTC での 5:MM に夏時間は終了します。ローカルの壁時計は 1:59 (夏時間) から
1:00 (標準時) に再び巻き戻されます。ローカルの時刻に おける 1:MM はあいまいになります。:meth:`astimezone` は二つの UTC
時刻を同じローカルの時刻に対応付けることで ローカルの時計の振る舞いをまねます。 東部時刻の例では、5:MM および 6:MM の形式をとる UTC 時刻は
両方とも、東部時刻に変換された際に 1:MM に対応づけられます。 :meth:`astimezone` がこのことを保証するようにするには、
:meth:`tzinfo.dst` は "繰り返された時間" が標準時に存在する ことを考慮しなければなりません。このことは、例えばタイムゾーンの標準の
ローカルな時刻に DST への切り替え時刻を表現することで簡単に設定する ことができます。

このようなあいまいさを許容できないアプリケーションは、 ハイブリッドな :class:`tzinfo` サブクラスを使って問題を回避しなければ なりません;
UTC や、他のオフセットが固定された :class:`tzinfo` の サブクラス (EST (-5 時間の固定オフセット) のみを表すクラスや、 EDT
(-4 時間の固定オフセット) のみを表すクラス) を使う限り、あいまいさは 発生しません。


.. _strftime-behavior:

:meth:`strftime` の振る舞い
----------------------

:class:`date`、 :class:`datetime`、および :class:`time` オブジェクトは全て、明示的な書式化文字列でコントロールして
時刻表現文字列を生成するための ``strftime(format)`` メソッドを サポートしています。大雑把にいうと、``d.strftime(fmt)``
は :mod:`time` モジュールの ``time.strftime(fmt, d.timetuple())``
のように動作します。ただし全てのオブジェクトが :meth:`timetuple`  メソッドをサポートしているわけではありません。

:class:`time` オブジェクトでは、年、月、日の値がないため、それらの 書式化コードを使うことができません。無理矢理使った場合、 年は
``1900`` に置き換えられ、月と日は ``0`` に置き換え られます。

:class:`date` オブジェクトでは、時、分、秒の値がないため、 それらの書式化コードを使うことができません。無理矢理使った場合、 これらの値は
``0`` に置き換えられます。

naive オブジェクトでは、書式化コード ``%z`` および ``%Z``  は空文字列に置き換えられます。

aware オブジェクトでは以下のようになります:

``%z``
   :meth:`utcoffset` は +HHMM あるいは -HHMM の形式をもった 5 文字の文字列に変換されます。HH は UTC
   オフセット時間を与える  2 桁の文字列で、MM は UTC オフセット分を与える 2 桁の文字列です。 例えば、:meth:`utcoffset` が
   ``timedelta(hours=-3, minutes=-30)`` を返した場合、``%z`` は文字列 ``'-0330'`` に置き換わります。

``%Z``
   :meth:`tzname` が ``None`` を返した場合、``%Z`` は 空文字列に置き換わります。そうでない場合、``%Z`` は返された
   値に置き換わりますが、これは文字列でなければなりません。

Python はプラットフォームの C ライブラリから :func:`strftime`
関数を呼び出し、プラットフォーム間のバリエーションはよくあることなので、 サポートされている書式化コードの全セットはプラットフォーム間で異なります。
Python の :mod:`time` モジュールのドキュメントでは、C 標準  (1989 年版) が要求する書式化コードをリストしており、これらのコードは
標準 C 準拠の実装がなされたプラットフォームでは全て動作します。 1999 年版の C 標準では書式化コードが追加されているので注意してください。

:meth:`strftime` が正しく動作する年の厳密な範囲はプラットフォーム 間で異なります。プラットフォームに関わらず、1900 年以前の年は
使うことができません。


使用例
---


Datetime オブジェクトをフォーマットされた文字列から生成する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`datetime`クラスは直接フォーマットされた時刻文字列の構文解析をサ ポートしていません。:func:`time.strptime`
を使うことによって構文解 析をし、返されるタプルから:class:`datetime`オブジェクトを生成することができます。 ::

   >>> s = "2005-12-06T12:13:14"
   >>> from datetime import datetime
   >>> from time import strptime
   >>> datetime(*strptime(s, "%Y-%m-%dT%H:%M:%S")[0:6])
   datetime.datetime(2005, 12, 6, 12, 13, 14)

