
:mod:`csv` --- CSV ファイルの読み書き
============================

.. module:: csv
   :synopsis: デリミタで区切られた形式のファイルに対するテーブル状データ読み書き。
.. sectionauthor:: Skip Montanaro <skip@pobox.com>


.. versionadded:: 2.3

.. index::
   single: csv
   pair: data; tabular

CSV (Comma Separated Values、カンマ区切り値列) と呼ばれる形式は、
スプレッドシートやデータベース間でのデータのインポートやエクスポート における最も一般的な形式です。"CSV 標準" は存在しないため、 CSV
形式はデータを読み書きする多くのアプリケーション上の操作に応じて 定義されているにすぎません。標準がないということは、異なるアプリケーション
によって生成されたり取り込まれたりするデータ間では、しばしば微妙な 違いが発生するということを意味します。こうした違いのために、複数の データ源から得られた
CSV ファイルを処理する作業が鬱陶しいものになる ことがあります。とはいえ、デリミタ (delimiter) やクオート文字の
相違はあっても、全体的な形式は十分似通っているため、こうしたデータを 効率的に操作し、データの読み書きにおける細々としたことをプログラマ
から隠蔽するような単一のモジュールを書くことは可能です。

:mod:`csv` モジュールでは、CSV 形式で書かれたテーブル状の データを読み書きするためのクラスを実装しています。
このモジュールを使うことで、プログラマは Excel で使われている CSV  形式に関して詳しい知識をもっていなくても、 "このデータを Excel で
推奨されている形式で書いてください" とか、 "データを Excel で 作成されたこのファイルから読み出してください" と言うことができます。
プログラマはまた、他のアプリケーションが解釈できる CSV 形式を記述したり、 独自の特殊な目的をもった CSV 形式を定義することができます。

:mod:`csv` モジュールの :class:`reader` および :class:`writer`
オブジェクトはシーケンス型を読み書きします。プログラマは :class:`DictReader` や :class:`DictWriter`
クラスを使うことで、 データを辞書形式で読み書きすることもできます。

.. note::

   このバージョンの :mod:`csv` モジュールは Unicode 入力をサポート していません。また、現在のところ、 ASCII NUL
   文字に関連したいくつかの 問題があります。従って、安全を期すには、全ての入力を UTF-8 または印字可能な ASCII
   にしなければなりません。これについては:ref:`csv-examples`節の 例を参照してください。これらの制限は将来取り去られることになっています。


.. seealso::

   .. % \seemodule{array}{Arrays of uniformly types numeric values.}

   :pep:`305` - CSV File API
      Python へのこのモジュールの追加を提案している Python 改良案 (PEP: Python Enhancement Proposal)


.. _csv-contents:

モジュールの内容
--------

:mod:`csv` モジュールでは以下の関数を定義しています:


.. function:: reader(csvfile[, dialect=``'excel'``][, fmtparam])

   与えられた *csvfile* 内の行を反復処理するような reader  オブジェクトを返します。*csvfile* はイテレータプロトコル
   をサポートし、:meth:`next` メソッドが呼ばれた際に常に文字列を 返すような任意のオブジェクトにすることができます --- ファイルオブジェクトでも
   リストでも構いません。 *csvfile* がファイルオブジェクトの場合、ファイルオブジェクトの 形式に違いがあるようなプラットフォームでは 'b'
   フラグを付けて 開かなければなりません。 オプションとして *dialect* パラメタを与えることができ、 特定の CSV 表現形式 (dialect)
   特有のパラメタの集合を定義するために 使われます。*dialect* パラメタは :class:`Dialect` クラスのサブクラス
   のインスタンスか、:func:`list_dialects` 関数が返す文字列 の一つにすることができます。別のオプションである *fmtparam*
   キーワード引数は、現在の表現形式における個々の書式パラメタを上書きする ために与えることができます。表現形式および書式化パラメタの詳細 については、
   :ref:`csv-fmt-params` 節、 "Dialect クラスと書式化パラメタ" を参照してください。

   読み出されたデータは全て文字列として返されます。データ型の変換が 自動的に行われることはありません。

   .. versionchanged:: 2.5
      パーサが複数行に亘るクオートされたフィールドに関して厳格になりました。 以前は、クオートされたフィールドの中で終端の改行文字無しに行が終わった場合、
      返されるフィールドには改行が挿入されていましたが、この振る舞いはフールドの中に 復帰文字を含むようなファイルを読むときに問題を起こしていました。
      そこでフィールドに改行文字を挿入せずに返すように改められました。 この結果、フィールドに埋め込まれた改行文字が重要ならば、入力は改行文字を保存する
      ような仕方で複数行に分割されなければなりません。 .


.. function:: writer(csvfile[, dialect=``'excel'``][, fmtparam])

   ユーザが与えたデータをデリミタで区切られた文字列に変換し、与えられた ファイルオブジェクトにするための writer オブジェクトを返します。
   *csvfile* は :func:`write` メソッドを持つ任意のオブジェクトで かまいません。 *csvfile*
   がファイルオブジェクトの場合、ファイルオブジェクトの 形式に違いがあるようなプラットフォームでは 'b' フラグを付けて 開かなければなりません。
   オプションとして *dialect* パラメタを与えることができ、 特定の CSV 表現形式 (dialect) 特有のパラメタの集合を定義するために
   使われます。*dialect* パラメタは :class:`Dialect` クラスのサブクラス のインスタンスか、:func:`list_dialects`
   関数が返す文字列 の一つにすることができます。別のオプションである *fmtparam*
   キーワード引数は、現在の表現形式における個々の書式パラメタを上書きする ために与えることができます。表現形式および書式化パラメタの詳細 については、
   :ref:`csv-fmt-params` 節、 "Dialect クラスと書式化パラメタ" を参照してください。 DB API
   を実装するモジュールとのインタフェースを可能な限り容易に するために、:const:`None` は空文字列として書き込まれます。
   この処理は可逆な変換ではありませんが、SQL で NULL データ値を CSV にダンプする処理を、``cursor.fetch*`` 呼び出しによって
   返されたデータを前処理することなく簡単に行うことができます。 他の非文字データは、書き出される前に :func:`str` を使って 文字列に変換されます。


.. function:: register_dialect(name[, dialect][, fmtparam])

   *dialect* を *name* と関連付けます。*name* は文字列か Unicode オブジェクトでなければなりません。 表現形式(dialect)は
   :class:`Dialect` のサブクラスを渡すか、 またはキーワード引数 *fmtparam*、もしくは両方で指定できますが、
   キーワード引数の方が優先されます。表現形式と書式化パラメタについてより詳しいことは :ref:`csv-fmt-params`節「Dialect
   クラスと書式化パラメタ」を参照してください。


.. function:: unregister_dialect(name)

   *name* に関連づけられた表現形式を表現形式レジストリから削除します。 *name* が表現形式名でない場合には :exc:`Error` を送出します。


.. function:: get_dialect(name)

   *name* に関連づけられた表現形式を返します。 *name* が表現形式名でない場合には :exc:`Error` を送出します。


.. function:: list_dialects()

   登録されている全ての表現形式を返します。


.. function:: field_size_limit([new_limit])

   パーサが許容する現在の最大フィールドサイズを返します。 *new_limit* が渡されたときは、その値が新しい上限になります。

   .. versionadded:: 2.5

:mod:`csv` モジュールでは以下のクラスを定義しています:


.. class:: DictReader(csvfile[, fieldnames=:const:`None`,[, restkey=:const:`None`[, restval=:const:`None`[, dialect=``'excel'``[, *args, **kwds]]]]])

   省略可能な*fieldnames* パラメタで与えられたキーを読み出された情報 に対応付ける他は正規の reader のように動作するオブジェクトを生成します。
   *fieldnames*パラメタが無い場合には、*csvfile*の最初の行の値が フィールド名として利用されます。 読み出された行が *fieldnames*
   のシーケンスよりも多くのフィールドを 持っていた場合、残りのフィールドデータは *restkey* の値をキーと するシーケンスに追加されます。読み出された行が
   *fieldnames* のシーケンス よりも少ないフィールドしか持たない場合、残りのキーはオプションの *restval*
   パラメタに指定された値を取ります。その他の省略可能また はキーワード形式のパラメタはベースになっている :class:`reader` のインス
   タンスに渡されます。


.. class:: DictWriter(csvfile, fieldnames[, restval=""[, extrasaction=``'raise'``[, dialect=``'excel'``[, *args, **kwds]]]])

   辞書を出力行に対応付ける他は正規の writer のように動作する オブジェクトを生成します。*fieldnames* パラメタには、 辞書中の
   :meth:`writerow` メソッドに渡される値がどの順番で *csvfile* に書き出されるかを指定します。 オプションの *restval*
   パラメタは、*fieldnames* 内の キーが辞書中にない場合に書き出される値を指定します。 :meth:`writerow` メソッドに渡された辞書に、
   *fieldnames* 内には 存在しないキーが入っている場合、オプションの *extraaction*
   パラメタでどのような動作を行うかを指定します。この値が ``'raise'`` に設定されている場合 :exc:`ValueError` が送出されます。
   ``'ignore'`` に設定されている場合、辞書の余分の値は無視されます。 その他のパラメタはベースになっている :class:`writer`
   のインスタンスに渡 されます。

   :class:`DictReader`クラスとは違い、:class:`DictWriter`の*fieldnames*
   パラメータは省略可能ではありません。Pythonの:class:`dict`オブジェクトは
   整列されていないので、列が*csvfile*に書かれるべき順序を推定するた めの十分な情報はありません。


.. class:: Dialect

   :class:`Dialect` クラスはコンテナクラスで、基本的な用途としては、 その属性を特定の :class:`reader` や
   :class:`writer` インスタンスの パラメタを定義するために用います。


.. class:: excel()

   :class:`excel` クラスは Excel で生成される CSV ファイルの通常の プロパティを定義します。


.. class:: excel_tab()

   :class:`excel` クラスは Excel で生成されるタブ分割ファイルの通常の プロパティを定義します。


.. class:: Sniffer([sample=16384])

   :class:`Sniffer` クラスは CSV ファイルの書式を推理するために用いられる クラスです。

:class:`Sniffer` クラスではメソッドを二つ提供しています:


.. method:: Sniffer.sniff(fileobj)

   与えられた *sample* を解析し、発見されたパラメタを 反映した :class:`Dialect` サブクラスを返します。 オプションの
   *delimiters* パラメタを与えた場合、 有効なデリミタ文字を含んでいるはずの文字列として解釈されます。


.. method:: Sniffer.has_header(sample)

   (CSV 形式と仮定される) サンプルテキストを解析して、 最初の行がカラムヘッダの羅列のように推察される場合 :const:`True` を返します。

:mod:`csv` モジュールでは以下の定数を定義しています:


.. data:: QUOTE_ALL

   :class:`writer` オブジェクトに対し、全てのフィールドをクオートするように 指示します。


.. data:: QUOTE_MINIMAL

   :class:`writer` オブジェクトに対し、*delimiter*、*quotechar* または *lineterminator*
   に含まれる任意の文字のような特別な文字 を含むフィールドだけをクオートするように指示します。


.. data:: QUOTE_NONNUMERIC

   :class:`writer` オブジェクトに対し、全ての非数値フィールドをクオート するように指示します。

   :class:`reader` に対しては、クオートされていない全てのフィールドを *float* 型に 変換するよう指示します。


.. data:: QUOTE_NONE

   :class:`writer` オブジェクトに対し、フィールドを決してクオートしない ように指示します。現在の *delimiter* が出力データ中に現れた
   場合、現在設定されている *escapechar* 文字が前に付けられます。 *escapechar* がセットされていない場合、エスケープが必要な文字に
   遭遇した writer は :exc:`Error` を送出します。

   :class:`reader` に対しては、クオート文字の特別扱いをしないように指示します。

:mod:`csv` モジュールでは以下の例外を定義しています:


.. exception:: Error

   全ての関数において、エラーが検出された際に送出される例外です。


.. _csv-fmt-params:

Dialect クラスと書式化パラメタ
-------------------

レコードに対する入出力形式の指定をより簡単にするために、 特定の書式化パラメタは表現形式 (dialect) にまとめてグループ化されます。 表現形式は
:class:`Dialect` クラスのサブクラスで、様々なクラス特有の メソッドと、:meth:`validate` メソッドを一つ持っています。
:class:`reader` または :class:`writer` オブジェクトを生成するとき、 プログラマは文字列または :class:`Dialect`
クラスのサブクラスを表現形式 パラメタとして渡さなければなりません。さらに、*dialect* パラメタ
の代りに、プログラマは上で定義されている属性と同じ名前を持つ 個々の書式化パラメタを :class:`Dialect` クラスに指定することができます。

Dialect は以下の属性をサポートしています:


.. attribute:: Dialect.delimiter

   フィールド間を分割するのに用いられる 1 文字からなる文字列です。 デフォルトでは ``','`` です。


.. attribute:: Dialect.doublequote

   フィールド内に現れた *quotechar* のインスタンスで、クオートではない その文字自身でなければならない文字をどのようにクオートするかを制御します。
   :const:`True` の場合、この文字は二重化されます。 :const:`False` の場合、 *escapechar* は *quotechar*
   の前に置かれます。デフォルトでは :const:`True` です。

   出力においては、*doublequote* が :const:`False` で *escapechar* がセットされていない場合、フールド内に
   *quotechar* が現れると :exc:`Error` が送出されます。


.. attribute:: Dialect.escapechar

   writer が、 *quoting* が :const:`QUOTE_NONE` に設定されている場合に *delimiter*
   をエスケープするため、および、 *doublequote* が :const:`False` の場合に *quotechar*
   をエスケープするために用いられる、 1 文字からなる文字列です。 読み込み時には *escapechar* はそれに引き続く文字の特別な意味を取り除きます。
   デフォルトでは :const:`None` で、エスケープを行ないません。


.. attribute:: Dialect.lineterminator

   :class:`writer` が作り出す各行を終端する際に用いられる文字列です。 デフォルトでは ``'\r\n'`` です。

   .. note::

      :class:`reader` は ``'\r'`` または ``'\n'`` のどちらかを行末と 認識するようにハードコードされており、
      *lineterminator* を無視します。 この振る舞いは将来変更されるかもしれません。


.. attribute:: Dialect.quotechar

   *delimiter* や *quotechar* といった特殊文字を含むか、 改行文字を含むフィールドをクオートする際に 用いられる 1
   文字からなる文字列です。デフォルトでは ``'"'`` です。


.. attribute:: Dialect.quoting

   クオートがいつ writer によって生成されるか、また reader によって認識されるかを制御します。 :const:`QUOTE_\*` 定数のいずれか
   (:ref:`csv-contents` 節参照) を とることができ、デフォルトでは:const:`QUOTE_MINIMAL` です。


.. attribute:: Dialect.skipinitialspace

   :const:`True` の場合、*delimiter* の直後に続く空白は無視されます。 デフォルトでは :const:`False` です。


reader オブジェクト
-------------

reader オブジェクト(:class:`DictReader` インスタンス、および  :func:`reader` 関数によって返されたオブジェクト)
は、以下の public なメソッドを持っています:


.. method:: csv reader.next()

   reader の反復可能なオブジェクトから、現在の表現形式に基づいて 次の行を解析して返します。

reader オブジェクトには以下の公開属性があります:


.. attribute:: csv reader.dialect

   パーサで使われる表現形式の読み取り専用の記述です。


.. attribute:: csv reader.line_num

   ソースイテレータから読んだ行数です。この数は返されるレコードの数とは、 レコードが複数行に亘ることがあるので、一致しません。


writer オブジェクト
-------------

:class:`Writer` オブジェクト(:class:`DictWriter` インスタンス、および  :func:`writer`
関数によって返されたオブジェクト) は、以下の public なメソッドを持っています:

:class:`Writer` オブジェクト(:func:`writer` で生成される  :class:`DictWriter`
クラスのインスタンス）は、以下の公開メソッドを持っています。 *row* には、:class:`Writer` オブジェクトの場合には文字列か数値のシーケンスを
指定し、:class:`DictWriter` オブジェクトの場合はフィールド名をキーとして対応する 文字列か数値を格納した辞書オブジェクトを指定します(数値は
:func:`str`で変換 されます)。 複素数を出力する場合、値をかっこで囲んで出力します。このため、CSV
ファイルを読み込むアプリケーションで（そのアプリケーションが複素数をサポートして いたとしても）問題が発生する場合があります。


.. method:: csv writer.writerow(row)

   *row* パラメタを現在の表現形式に基づいて書式化し、 writer のファイル オブジェクトに書き込みます。


.. method:: csv writer.writerows(rows)

   *rows* パラメタ(上記 *row* のリスト)全てを現在の表現形式に基づいて書式化し、  writer のファイルオブジェクトに書き込みます。

writer オブジェクトには以下の公開属性があります:


.. attribute:: csv writer.dialect

   writer で使われる表現形式の読み取り専用の記述です。


.. _csv-examples:

使用例
---

最も簡単な CSV ファイル読み込みの例です::

   import csv
   reader = csv.reader(file("some.csv", "rb"))
   for row in reader:
       print row

別の書式での読み込み::

   import csv
   reader = csv.reader(open("passwd", "rb"), delimiter=':', quoting=csv.QUOTE_NONE)
   for row in reader:
       print row

上に対して、単純な書き込みのプログラム例は以下のようになります。 ::

   import csv
   writer = csv.writer(file("some.csv", "wb"))
   writer.writerows(someiterable)

新しい表現形式の登録::

   import csv

   csv.register_dialect('unixpwd', delimiter=':', quoting=csv.QUOTE_NONE)

   reader = csv.reader(open("passwd", "rb"), 'unixpwd')

もう少し手の込んだ reader の使い方 --- エラーを捉えてレポートします。 ::

   import csv, sys
   filename = "some.csv"
   reader = csv.reader(open(filename, "rb"))
   try:
       for row in reader:
           print row
   except csv.Error, e:
       sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

このモジュールは文字列の解析は直接サポートしませんが、簡単にできます。 ::

   import csv
   for row in csv.reader(['one,two,three']):
       print row

:mod:`csv` モジュールは直接は Unicode の読み書きをサポートしませんが、 ASCII NUL
文字に関わる問題のために8ビットクリーンに書き込みます。 ですから、NUL を使う UTF-16 のようなエンコーディングを避ける限り
エンコード・デコードを行なう関数やクラスを書くことができます。 UTF-8 がお勧めです。

以下の :func:`unicode_csv_reader` は Unicode の CSV データ (Unicode 文字列のリスト)を扱うための
:class:`csv.reader` をラップする ジェネレータです。:func:`utf_8_encoder` は一度に 1 文字列(または行) ずつ
Unicode 文字列を UTF-8 としてエンコードするジェネレータです。 エンコードされた文字列は CSV reader により分解され、
:func:`unicode_csv_reader` が UTF-8 エンコードの分解された文字列を デコードして Unicode に戻します。 ::

   import csv

   def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
       # csv.py doesn't do Unicode; encode temporarily as UTF-8:
       csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                               dialect=dialect, **kwargs)
       for row in csv_reader:
           # decode UTF-8 back to Unicode, cell by cell:
           yield [unicode(cell, 'utf-8') for cell in row]

   def utf_8_encoder(unicode_csv_data):
       for line in unicode_csv_data:
           yield line.encode('utf-8')

その他のエンコーディングには以下の :class:`UnicodeReader` クラスと :class:`UnicodeWriter`
クラスが使えます。二つのクラスは *encoding* パラメータをコンストラクタで取り、本物の reader や writer に渡されるデータが UTF-8
でエンコードされていることを保証します。 ::

   import csv, codecs, cStringIO

   class UTF8Recoder:
       """
       Iterator that reads an encoded stream and reencodes the input to UTF-8
       """
       def __init__(self, f, encoding):
           self.reader = codecs.getreader(encoding)(f)

       def __iter__(self):
           return self

       def next(self):
           return self.reader.next().encode("utf-8")

   class UnicodeReader:
       """
       A CSV reader which will iterate over lines in the CSV file "f",
       which is encoded in the given encoding.
       """

       def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
           f = UTF8Recoder(f, encoding)
           self.reader = csv.reader(f, dialect=dialect, **kwds)

       def next(self):
           row = self.reader.next()
           return [unicode(s, "utf-8") for s in row]

       def __iter__(self):
           return self

   class UnicodeWriter:
       """
       A CSV writer which will write rows to CSV file "f",
       which is encoded in the given encoding.
       """

       def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
           # Redirect output to a queue
           self.queue = cStringIO.StringIO()
           self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
           self.stream = f
           self.encoder = codecs.getincrementalencoder(encoding)()

       def writerow(self, row):
           self.writer.writerow([s.encode("utf-8") for s in row])
           # Fetch UTF-8 output from the queue ...
           data = self.queue.getvalue()
           data = data.decode("utf-8")
           # ... and reencode it into the target encoding
           data = self.encoder.encode(data)
           # write to the target stream
           self.stream.write(data)
           # empty queue
           self.queue.truncate(0)

       def writerows(self, rows):
           for row in rows:
               self.writerow(row)

