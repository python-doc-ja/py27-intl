
:mod:`sqlite3` --- SQLite データベースに対する DB-API 2.0 インタフェース
========================================================================

.. module:: sqlite3
   :synopsis: A DB-API 2.0 implementation using SQLite 3.x.
.. sectionauthor:: Gerhard Häring <gh@ghaering.de>


.. versionadded:: 2.5

SQLite は、別にサーバプロセスは必要とせずデータベースのアクセスに SQL 問い合わせ言語の非標準的な一種を使える軽量なディスク上のデータベースを
提供する C ライブラリです。ある種のアプリケーションは内部データ保存 に SQLite を使えます。また、SQLite を使ってアプリケーションのプロトタイ
プを作りその後そのコードを PostgreSQL や Oracle のような大規模データベー スに移植するということも可能です。

pysqlite は Gerhard Häring によって書かれ、:pep:`249` に記述され た DB-API 2.0 仕様に準拠したSQL
インタフェースを提供するものです。

このモジュールを使うには、最初にデータベースを表す :class:`Connection` オブジェクトを作ります。ここではデータはファイル
:file:`/tmp/example` に 格納されているものとします。 ::

   conn = sqlite3.connect('/tmp/example')

特別な名前である ``:memory:`` を使うと RAM 上にデータベースを作るこ ともできます。

:class:`Connection` があれば、 :class:`Cursor` オブジェクトを作りそ の :meth:`execute` メソッドを呼んで
SQL コマンドを実行することができ ます。 ::

   c = conn.cursor()

   # Create table
   c.execute('''create table stocks
   (date text, trans text, symbol text,
    qty real, price real)''')

   # Insert a row of data
   c.execute("""insert into stocks
             values ('2006-01-05','BUY','RHAT',100,35.14)""")

たいてい、SQL 操作は Python 変数の値を使う必要があります。この時、クエ リーを Python
の文字列操作を使って構築することは、安全とは言えないので、 すべきではありません。そのようなことをするとプログラムが SQL インジェク
ション攻撃に対し脆弱になりかねません。

代わりに、DB-API のパラメータ割り当てを使います。``?`` を変数の値を 使いたいところに埋めておきます。その上で、値のタプルをカーソル の
:meth:`execute` メソッドの第2引数として引き渡します。(他のデータ ベースモジュールでは変数の場所を示すのに``%s`` や ``:1``
などの 異なった表記を用いることがあります。) 例を示します。 ::

   # Never do this -- insecure!
   symbol = 'IBM'
   c.execute("... where symbol = '%s'" % symbol)

   # Do this instead
   t = (symbol,)
   c.execute('select * from stocks where symbol=?', t)

   # Larger example
   for t in (('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSOFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ):
       c.execute('insert into stocks values (?,?,?,?,?)', t)

SELECT 文を実行した後データを取得する方法は3つありどれを使っても構いま せん。一つはカーソルをイテレータとして扱う、一つはカーソル の
:meth:`fetchone` メソッドを呼んで一致した内の一行を取得する、もう 一つは :meth:`fetchall`
メソッドを呼んで一致した全ての行のリストとし て受け取る、という3つです。

以下の例ではイテレータの形を使います。 ::

   >>> c = conn.cursor()
   >>> c.execute('select * from stocks order by price')
   >>> for row in c:
   ...    print row
   ...
   (u'2006-01-05', u'BUY', u'RHAT', 100, 35.140000000000001)
   (u'2006-03-28', u'BUY', u'IBM', 1000, 45.0)
   (u'2006-04-06', u'SELL', u'IBM', 500, 53.0)
   (u'2006-04-05', u'BUY', u'MSOFT', 1000, 72.0)
   >>>


.. seealso::

   http://www.pysqlite.org
      pysqlite のウェブページ

   http://www.sqlite.org
      SQLite のウェブページ。 ここの文書ではサポートされる SQL 方言の文法と使えるデータ型を説明しています

   :pep:`249` - Database API Specification 2.0
      Marc-André Lemburg により書かれた PEP

   http://www.python.jp/doc/contrib/peps/pep-0249.txt
      訳注: PEP 249 の日本語訳があります


.. _sqlite3-module-contents:

モジュールの関数と定数
----------------------


.. data:: PARSE_DECLTYPES

   この定数は :func:`connect` 関数の *detect_types* パラメータと して使われます。

   この定数を設定すると :mod:`sqlite3` モジュールは戻り値のカラムの宣言 された型を読み取るようになります。意味を持つのは宣言の最初の単語です。
   すなわち、"integer primary key" においては "integer" が読み取られます。
   そしてそのコラムに対して、変換関数の辞書を探してその型に対して登録され た関数を使うようにします。変換関数の名前は大文字と小文字を区別します!


.. data:: PARSE_COLNAMES

   この定数は :func:`connect` 関数の *detect_types* パラメータと して使われます。

   この定数を設定すると SQLite のインタフェースは戻り値のそれぞれのカラムの名前を 読み取るようになります。文字列の中の [mytype]
   といった形の部分を探し、'mytype' がそのカラムの名前であると判断します。そして 'mytype' のエントリを変換関数辞書
   の中から見つけ、見つかった変換関数を値を返す際に用います。 :attr:`cursor.description`
   で見つかるカラム名はその最初の単語だけです。すなわち、 もし ``'as "x [datetime]"'`` のようなものを SQL の中で使っていたとすると、
   読み取るのはカラム名の中の最初の空白までの全てですので、カラム名として使われるのは 単純に "x" ということになります。


.. function:: connect(database[, timeout, isolation_level, detect_types, factory])

   ファイル *database* の SQLite データベースへの接続を開きます。 ``":memory:"`` という名前を使うことでディスクの代わりに
   RAM 上 のデータベースへの接続を開くこともできます。

   データベースが複数の接続からアクセスされている状況で、その内の一つがデー タベースに変更を加えたとき、SQLite データベースはそのトランザクションが
   コミットされるまでロックされます。*timeout* パラメータで、例外を送 出するまで接続がロックが解除されるのをどれだけ待つかを決めます。デフォ ルトは
   5.0 (5秒) です。

   *isolation_level* パラメータについて は、:ref:`sqlite3-connection-isolationlevel`節の
   :class:`Connection` オブ ジェクトの :attr:`isolation_level` プロパティの説明を参照してくださ い。

   SQLite がネイティブにサポートするのは TEXT, INTEGER, FLOAT, BLOB およ び NULL
   型だけです。もし他の型を使いたければ、その型のためのサポートを 自分で追加しなければなりません。*detect_types* パラメータを、モジュー ルレベルの
   :func:`register_converter` 関数で登録した自作の **変換関数** と一緒に使えば、簡単にできます。

   パラメータ *detect_types* のデフォルトは 0 (つまりオフ、型検知無し)です。
   型検知を有効にするためには、:const:`PARSE_DECLTYPES` と :const:`PARSE_COLNAMES`
   の適当な組み合わせをこのパラメータにセットします。

   デフォルトでは、 :mod:`sqlite3` モジュールは connect の呼び出しの際に モジュールの :class:`Connection`
   クラスを使います。しか し、:class:`Connection` クラスを継承したクラスを *factory* パラメー タに渡して
   :func:`connect` にそのクラスを使わせることもできます。詳 しくはこのマニュアルの
   :ref:`sqlite3-types`節を参考にしてください。

   :mod:`sqlite3` モジュールは SQL 解析のオーバーヘッドを避けるために内 部で文キャッシュを使っています。接続に対してキャッシュされる文の数を自
   分で指定したいならば、*cached_statements* パラメータに設定してくだ さい。現在の実装ではデフォルトでキャッシュされる SQL 文の数を
   100 にし ています。


.. function:: register_converter(typename, callable)

   データベースから得られるバイト列を希望する Python の型に変換する呼び 出し可能オブジェクト (callable) を登録します。その呼び出し可能オブジェ
   クトは型が *typename* である全てのデータベース上の値に対して呼び 出されます。型検知がどのように働くかについては :func:`connect` 関
   数の *detect_types* パラメータの説明も参照してください。注意が必 要なのは *typename* はクエリの中の型名と大文字小文字も一致しなけ
   ればならないということです。


.. function:: register_adapter(type, callable)

   自分が使いたい Python の型 *type* を SQLite がサポートしている型 に変換する呼び出し可能オブジェクト (callable)
   を登録します。その呼び 出し可能オブジェクト *callable* はただ一つの引数に Python の値を 受け取り、int, long, float,
   (UTF-8 でエンコードされた) str, unicode または buffer のいずれかの型の値を返さなければなりません


.. function:: complete_statement(sql)

   もし文字列 *sql* がセミコロンで終端された一つ以上の完全な SQL 文 であれば :const:`True` を返します。判定は SQL
   文として文法的に正し いかではなく、閉じられていない文字列リテラルが無いことおよびセミコロン で終端されていることだけで行なわれます。

   この関数は以下の例にあるような SQLite のシェルを作る際に使われます。


   .. include:: ../includes/sqlite3/complete_statement.py
      :literal:


.. function:: enable_callback_tracebacks(flag)

   デフォルトでは、ユーザ定義の関数、集計関数、変換関数、認可コールバック などはトレースバックを出力しません。デバッグの際にはこの関数を *flag* に
   :const:`True` を指定して呼び出します。そうした後は 先に述べたような関数のトレースバックが ``sys.stderr`` に出力されま
   す。元に戻すには :const:`False` を使います。

   .. % authorizer callbacks = 認可コールバック?


.. _sqlite3-connection-objects:

Connection オブジェクト
-----------------------

:class:`Connection` のインスタンスには以下の属性とメソッドがあります:

.. _sqlite3-connection-isolationlevel:


.. attribute:: Connection.isolation_level

   現在の分離レベルを取得または設定します。None で自動コミットモードまたは "DEFERRED", "IMMEDIATE", "EXLUSIVE"
   のどれかです。より詳しい説明は :ref:`sqlite3-controlling-transactions`節「トランザクション制御」を 参照してください。


.. method:: Connection.cursor([cursorClass])

   cursor メソッドはオプション引数 *CursorClass* を受け付けます。 これを指定するならば、指定されたクラスは
   :class:`sqlite3.Cursor` を 継承したカーソルクラスでなければなりません。


.. method:: Connection.execute(sql, [parameters])

   このメソッドは非標準のショートカットで、cursor メソッドを呼び出して中間的な カーソルオブジェクトを作り、そのカーソルの :meth:`execute`
   メソッドを与えられた パラメータと共に呼び出します。


.. method:: Connection.executemany(sql, [parameters])

   このメソッドは非標準のショートカットで、cursor メソッドを呼び出して中間的な カーソルオブジェクトを作り、そのカーソルの
   :meth:`executemany` メソッドを与えられた パラメータと共に呼び出します。


.. method:: Connection.executescript(sql_script)

   このメソッドは非標準のショートカットで、cursor メソッドを呼び出して中間的な カーソルオブジェクトを作り、そのカーソルの
   :meth:`executescript` メソッドを与えられた パラメータと共に呼び出します。


.. method:: Connection.create_function(name, num_params, func)

   後から SQL 文中で *name* という名前の関数として使えるユーザ定義関数を作成します。 *num_params* は関数が受け付ける引数の数、
   *func* は SQL 関数として使われる Python の呼び出し可能オブジェクトです。

   関数は SQLite でサポートされている任意の型を返すことができます。具体的には unicode, str, int, long, float, buffer
   および None です。

   例:


   .. include:: ../includes/sqlite3/md5func.py
      :literal:


.. method:: Connection.create_aggregate(name, num_params, aggregate_class)

   ユーザ定義の集計関数を作成します。

   集計クラスには パラメータ *num_params*　で指定される個数の引数を取る ``step`` メソッドおよび最終的な集計結果を返す
   ``finalize`` メソッドを 実装しなければなりません。

   ``finalize`` メソッドは SQLite でサポートされている任意の型を返すことができます。 具体的には unicode, str, int,
   long, float, buffer および None です。

   例:


   .. include:: ../includes/sqlite3/mysumaggr.py
      :literal:


.. method:: Connection.create_collation(name, callable)

   *name* と *callable* で指定される照合順序を作成します。呼び出 し可能オブジェクトには二つの文字列が渡されます。一つめのものが二つめ
   のものより低く順序付けられるならば -1 を返し、等しければ 0 を返し、一 つめのものが二つめのものより高く順序付けられるならば 1 を返すようにし
   なければなりません。この関数はソート(SQL での ORDER BY)をコントロール するもので、比較を行なうことは他の SQL 操作には影響を与えないことに注
   意しましょう。

   また、呼び出し可能オブジェクトに渡される引数は Python のバイト文字列 として渡されますが、それは通常 UTF-8 で符号化されたものになります。

   以下の例は「間違った方法で」ソートする自作の照合順序です:


   .. include:: ../includes/sqlite3/collation_reverse.py
      :literal:

   照合順序を取り除くには ``create_collation`` を callable とし て None を渡して呼び出します::

      con.create_collation("reverse", None)


.. method:: Connection.interrupt()

   このメソッドを別スレッドから呼び出して接続上で現在実行中であろうクエリを中断させられます。 クエリが中断されると呼び出し元は例外を受け取ります。


.. method:: Connection.set_authorizer(authorizer_callback)

   このルーチンはコールバックを登録します。コールバックはデータベースの テーブルのカラムにアクセスしようとするたびに呼び出されます。コールバッ
   クはアクセスが許可されるならば :const:`SQLITE_OK` を、SQL 文全体が エラーとともに中断されるべきならば
   :const:`SQLITE_DENY` を、カラム が NULL 値として扱われるべきなら :const:`SQLITE_IGNORE` を返さなけ
   ればなりません。これらの定数は :mod:`sqlite3` モジュールに用意され ています。

   コールバックの第一引数はどの種類の操作が許可されるかを決めます。第二第 三引数には第一引数に依存して本当に使われる引数か :const:`None` かが渡
   されます。第四引数はもし適用されるならばデータベースの名前("main", "temp", etc.)です。第五引数はアクセスを試みる要因となった最も内側のトリ
   ガまたはビューの名前、またはアクセスの試みが入力された SQL コードに直接 起因するものならば :const:`None` です。

   第一引数に与えることができる値や、その第一引数によって決まる第二第三引 数の意味については、SQLite の文書を参考にしてください。必要な定数は全 て
   :mod:`sqlite3` モジュールに用意されています。


.. attribute:: Connection.row_factory

   この属性を、カーソルとタプルの形での元の行のデータを受け取り最終的な 行を表すオブジェクトを返す呼び出し可能オブジェクトに、変更することが
   できます。これによって、より進んだ結果の返し方を実装することができま す。例えば、カラムの名前で各データにアクセスできるようなオブジェクト を返したりできます。

   例:


   .. include:: ../includes/sqlite3/row_factory.py
      :literal:

   タプルを返すのでは物足りず、名前に基づいたカラムへのアクセスが行ない たい場合は、高度に最適化された :class:`sqlite3.Row` 型を
   :attr:`row_factory` にセットすることを考えてはいかがでしょうか。 :class:`Row`
   クラスでは添字でも大文字小文字を無視した名前でもカラムに アクセスでき、しかもほとんどメモリーを浪費しません。
   おそらく、辞書を使うような独自実装のアプローチよりも、もしか すると db の行に基づいた解法よりも良いものかもしれません。

   .. % XXX what's a db_row-based solution?


.. attribute:: Connection.text_factory

   この属性を使って TEXT データ型をどのオブジェクトで返すかを制御できます。 デフォルトではこの属性は :class:`unicode` に設定されており、
   :mod:`sqlite3` モジュールは TEXT を Unicode オブジェクトで返します。 もしバイト列で返したいならば、:class:`str`
   に設定してください。

   効率の問題を考えて、非ASCIIデータに限って Unicode オブジェクトを返し、 その他の場合にはバイト列を返す方法もあります。これを有効にしたければ、
   この属性を :const:`sqlite3.OptimizedUnicode` に設定してください。

   バイト列を受け取って望みの型のオブジェクトを返すような呼び出し可能オブジェクトを 何でも設定して構いません。

   以下の説明用のコード例を参照してください:


   .. include:: ../includes/sqlite3/text_factory.py
      :literal:


.. attribute:: Connection.total_changes

   データベース接続が開始されて以来の行の変更・挿入・削除がなされた行の総数を返します。

   .. % 返す?


.. _sqlite3-cursor-objects:

カーソルオブジェクト
--------------------

:class:`Cursor` のインスタンスはには以下の属性とメソッドがあります:


.. method:: Cursor.execute(sql, [parameters])

   SQL 文を実行します。SQL 文はパラメータ化できます(すなわち SQL リテラル の代わりの場所確保文字 (placeholder) を入れておけます)。
   :mod:`sqlite3` モジュールは2種類の場所確保記法をサポートします。 一つは疑問符(qmark スタイル)、もう一つは名前(named
   スタイル)です。

   まず最初の例は qmark スタイルのパラメータを使った書き方を示します:


   .. include:: ../includes/sqlite3/execute_1.py
      :literal:

   次の例は named スタイルの使い方です:


   .. include:: ../includes/sqlite3/execute_2.py
      :literal:

   :meth:`execute` は一つの SQL 文しか実行しません。二つ以上の文を実行 しようとすると、Warning を発生させます。複数の SQL
   文を一つの呼び出し で実行したい場合は :meth:`executescript` を使ってください。


.. method:: Cursor.executemany(sql, seq_of_parameters)

   SQL 文 *sql* を *seq_of_parameters* の全てのパラメータシーケン
   スまたはマッピングに対して実行します。:mod:`sqlite3` モジュールでは、シーケンスの代わりにパラメータの組を
   作り出すイテレータ使うことが許されています。

   .. % という意味だと思うが。


   .. include:: ../includes/sqlite3/executemany_1.py
      :literal:

   もう少し短いジェネレータを使った例です:


   .. include:: ../includes/sqlite3/executemany_2.py
      :literal:


.. method:: Cursor.executescript(sql_script)

   これは非標準の便宜メソッドで、一度に複数の SQL 文を実行することができ ます。メソッドは最初に COMMIT 文を発行し、次いで引数として渡された SQL
   スクリプトを実行します。

   *sql_script* はバイト文字列または Unicode 文字列です。

   例:


   .. include:: ../includes/sqlite3/executescript.py
      :literal:


.. attribute:: Cursor.rowcount

   一応 :mod:`sqlite3` モジュールの :class:`Cursor` クラスはこの属性を実
   装していますが、データベースエンジン自身の「影響を受けた行」/「選択さ れた行」の決定方法は少し風変わりです。

   ``SELECT`` 文では、全ての行を取得し終えるまで全部で何行になったか決 められないので :attr:`rowcount` はいつでも None です。

   ``DELETE`` 文では、条件を付けずに ``DELETE FROM table`` とすると SQLite は :attr:`rowcount` を 0
   と報告します。

   :meth:`executemany` では、変更数が :attr:`rowcount` に合計されます。

   Python DB API 仕様で求められているように、:attr:`rowcount` 属性は 「現在のカーソルがまだ executeXXX()
   を実行していない場合や、 データベースインタフェースから最後に行った操作の結果行数を 決定できない場合には、この属性は -1 となります」。


.. _sqlite3-types:

SQLite と Python の型
---------------------


入門編
^^^^^^

SQLite が最初からサポートしているのは次の型です: NULL, INTEGER, REAL, TEXT, BLOB。

したがって、次の Python の型は問題なく SQLite に送り込めます:

+---------------------------+-------------+
| Python の型               | SQLite の型 |
+===========================+=============+
| ``None``                  | NULL        |
+---------------------------+-------------+
| ``int``                   | INTEGER     |
+---------------------------+-------------+
| ``long``                  | INTEGER     |
+---------------------------+-------------+
| ``float``                 | REAL        |
+---------------------------+-------------+
| ``str (UTF8 エンコード)`` | TEXT        |
+---------------------------+-------------+
| ``unicode``               | TEXT        |
+---------------------------+-------------+
| ``buffer``                | BLOB        |
+---------------------------+-------------+

SQLite の型から Python の型へのデフォルトでの変換は以下の通りです:

+-------------+-------------------------------------------------------+
| SQLite の型 | Python の型                                           |
+=============+=======================================================+
| ``NULL``    | None                                                  |
+-------------+-------------------------------------------------------+
| ``INTEGER`` | int または long (サイズによる)                        |
+-------------+-------------------------------------------------------+
| ``REAL``    | float                                                 |
+-------------+-------------------------------------------------------+
| ``TEXT``    | text_factory に依存して決まるがデフォルトでは unicode |
+-------------+-------------------------------------------------------+
| ``BLOB``    | buffer                                                |
+-------------+-------------------------------------------------------+

:mod:`sqlite3` モジュールの型システムは二つの方法で拡張できます。一つ はオブジェクト適合(adaptation)を通じて追加された Python
の型を SQLite に格納することです。もう一つは変換関数(converter)を通じ て :mod:`sqlite3` モジュールに SQLite
の型を違った Python の型に変換 させることです。


追加された Python の型を SQLite データベースに格納するために適合関数を使う
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

既に述べたように、SQLite が最初からサポートする型は限られたものだけです。 それ以外の Python の型を SQLite で使うには、その型を
:mod:`sqlite3` モジュールがサポートしている型の一つに **適合** させなくてはなりま せん。サポートしている型というのは、NoneType,
int, long, float, str, unicode, buffer です。

:mod:`sqlite3` モジュールは :pep:`246` に述べられているような Python オブジェクト適合を用います。使われるプロトコル は
:class:`PrepareProtocol` です。

:mod:`sqlite3` モジュールで望みの Python の型をサポートされている型 の一つに適合させる方法は二つあります。


オブジェクト自身で適合するようにする
""""""""""""""""""""""""""""""""""""

自分でクラスを書いているならばこの方法が良いでしょう。次のようなクラス があるとします::

   class Point(object):
       def __init__(self, x, y):
           self.x, self.y = x, y

さてこの点を SQLite の一つのカラムに収めたいと考えたとしましょう。最初 にしなければならないのはサポートされている型の中から点を表現するのに使
えるものを選ぶことです。ここでは単純に文字列を使うことにして、座標を区 切るのにはセミコロンを使いましょう。次に必要なのはクラスに変換された値 を返す
``__conform__(self, protocol)`` メソッドを追加することです。 引数 *protocol* は
:class:`PrepareProtocol` になります。


.. include:: ../includes/sqlite3/adapter_point_1.py
   :literal:


適合関数を登録する
""""""""""""""""""

もう一つの可能性は型を文字列表現に変換する関数を作り :meth:`register_adapter` でその関数を登録することです。

.. note::

   適合させる型/クラスは新形式クラスでなければなりません。すなわち、:class:`object` を基底クラスの一つとしていなければなりません。


.. include:: ../includes/sqlite3/adapter_point_2.py
   :literal:

:mod:`sqlite3` モジュールには二つの Python 標準型 :class:`datetime.date` と
:class:`datetime.datetime` に対するデフォルト適合関数があります。いま :class:`datetime.datetime`
オブジェクトを ISO 表現でなく Unix タイムスタンプ として格納したいとしましょう。


.. include:: ../includes/sqlite3/adapter_datetime.py
   :literal:


SQLite の値を好きな Python 型に変換する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

適合関数を書くことで好きな Python 型を SQLite に送り込めるようになりました。 しかし、本当に使い物になるようにするには Python から
SQLite さらに Python へという 往還(roundtrip)の変換ができる必要があります。

そこで変換関数(converter)です。

:class:`Point` クラスの例に戻りましょう。x, y 座標をセミコロンで区切った文字列として SQLite に格納したのでした。

まず、文字列を引数として取り :class:`Point` オブジェクトをそれから構築する変換関数 を定義します。

.. note::

   変換関数は SQLite に送り込んだデータ型に関係なく**常に**文字列を渡されます。

.. note::

   変換関数の名前を探す際、大文字と小文字は区別されます。

::

   def convert_point(s):
       x, y = map(float, s.split(";"))
       return Point(x, y)

次に :mod:`sqlite3` モジュールにデータベースから取得したものが本当に点 であることを教えなければなりません。二つの方法があります:

* 宣言された型を通じて暗黙的に

* カラム名を通じて明示的に

どちらの方法も:ref:`sqlite3-module-contents`節"モジュールの関数と定数"の中で 説明されています。それぞれ
:const:`PARSE_DECLTYPES` 定数と :const:`PARSE_COLNAMES` 定数の項目です。

以下の例で両方のアプローチを紹介します。


.. include:: ../includes/sqlite3/converter_point.py
   :literal:


デフォルトの適合関数と変換関数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

datetime モジュールの date 型および datetime 型のためのデフォルト適合関数 があります。これらの型は ISO 日付 / ISO
タイムスタンプとして SQLite に送られます。

デフォルトの変換関数は :class:`datetime.date` 用が "date" という名前で、 :class:`datetime.datetime`
用が "timestamp" という名前で登録されています。

これにより、多くの場合特別な細工無しに Python の日付 / タイムスタンプを使えます。 適合関数の書式は実験的な SQLite の date/time
関数とも互換性があります。

以下の例でこのことを確かめます。


.. include:: ../includes/sqlite3/pysqlite_datetime.py
   :literal:


.. _sqlite3-controlling-transactions:

トランザクション制御
--------------------

デフォルトでは、:mod:`sqlite3` モジュールはデータ変更言語(DML)文(すなわち
INSERT/UPDATE/DELETE/REPLACE)の前に暗黙のうちにトランザクションを開始し、 非DML、非クエリ文(すなわち
SELECT/INSERT/UPDATE/DELETE/REPLACE のいずれでも ないもの)の前にトランザクションをコミットします。

ですから、もしトランザクション中に ``CREATE TABLE ...``, ``VACUUM``, ``PRAGMA``
といったコマンドを発行すると、:mod:`sqlite3` モジュールはその コマンドの実行前に暗黙のうちにコミットします。このようにする理由は二つあります。
第一にこうしたコマンドのうちの幾つかはトランザクション中ではうまく動きません。 第二に pysqlite
はトランザクションの状態(トランザクションが掛かっているかどうか)を 追跡する必要があるからです。

pysqlite が暗黙のうちに実行する"BEGIN"文の種類(またはそういうものを使わないこと)を :func:`connect` 呼び出しの
*isolation_level* パラメータを通じて、または 接続の :attr:`isolation_level`
プロパティを通じて、制御することができます。

もし**自動コミットモード**が使いたければ、:attr:`isolation_level` は None にしてください。

そうでなければデフォルトのまま"BEGIN"文を使い続けるか、SQLite がサポートする分離レベル DEFERRED, IMMEDIATE または
EXCLUSIVE を設定してください。

:mod:`sqlite` モジュールがトランザクション状態を把握する必要があるの で、SQL の中で ``OR ROLLBACK`` や ``ON
CONFLICT ROLLBACK`` を使っ てはなりません。その代わりに、:exc:`IntegrityError` を捕捉して接続
の:meth:`rollback` メソッドを自分で呼び出すようにしてください。


pysqlite の効率的な使い方
-------------------------


ショートカットメソッドを使う
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`Connection` オブジェクトの非標準的なメソッド :meth:`execute`, :meth:`executemany`,
:meth:`executescript` を使うことで、 (しばしば余計な) :class:`Cursor` オブジェクトをわざわざ作り出さずに済むので、
コードをより簡潔に書くことができます。:class:`Cursor` オブジェクトは暗黙裡に
生成されショートカットメソッドの戻り値として受け取ることができます。この方法を 使えば、 SELECT 文を実行してその結果について反復することが、
:class:`Connection` オブジェクトに対する呼び出し一つで行なえます。


.. include:: ../includes/sqlite3/shortcut_methods.py
   :literal:


位置ではなく名前でカラムにアクセスする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`sqlite3` モジュールの有用な機能の一つに、行生成関数として使われるための :class:`sqlite3.Row` クラスがあります。

このクラスでラップされた行は、位置インデクス(タプルのような)でも 大文字小文字を区別しない名前でもアクセスできます:


.. include:: ../includes/sqlite3/rowclass.py
   :literal:

