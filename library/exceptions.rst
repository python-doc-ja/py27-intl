.. _bltin-exceptions:

組み込み例外
============

.. module:: exceptions
   :synopsis: 標準の例外クラス群


例外はクラスオブジェクトです。 例外はモジュール :mod:`exceptions` で定
義されています。このモジュールを明示的にインポートする必要はありません:
例外は :mod:`exceptions` モジュールと同様に組み込み名前空間で与えられ
ます。


.. index::
   statement: try
   statement: except

:keyword:`try` 文の中で、 :keyword:`except` 節を使って特定の例外クラス
について記述した場合、その節は指定した例外クラスから導出されたクラスも
扱います (指定した例外クラスを導出した元のクラスは含みません) 。
サブクラス化の関係にない例外クラスが二つあった場合、それらに同じ名前を
付けたとしても、等しくなることはありません。


.. index:: statement: raise

以下に列挙した組み込み例外はインタプリタや組み込み関数によって生成され
ます。特に注記しないかぎり、これらの例外はエラーの詳しい原因を示してい
る、 "関連値 (associated value)" を持ちます。この値は文字列または複数
の情報 (例えばエラーコードや、エラーコードを説明する文字列) を含むタプ
ルです。この関連値は :keyword:`raise` 文の二つ目の引数です。
例外が標準のルートクラスである :exc:`BaseException` から導出された場合、
関連値は例外インスタンスの :attr:`args` 属性中に置かれます。

ユーザによるコードも組み込み例外を送出することができます。これは例外処
理をテストしたり、インタプリタがある例外を送出する状況と "ちょうど同じ
ような" エラー条件であることを報告させるために使うことができます。しか
し、ユーザが適切でないエラーを送出するようコードするのを妨げる方法はな
いので注意してください。

組み込み例外クラスは新たな例外を定義するためにサブクラス化することがで
きます; プログラマには、新しい例外を少なくとも :exc:`Exception` クラス
から導出するよう勧めます。 :exc:`BaseException` からは導出しないで下さ
い。例外を定義する上での詳しい情報は、 Python チュートリアルの "ユーザ
定義の例外" (:ref:`tut-userexceptions`) の項目にあります。

以下の例外クラスは他の例外クラスの基底クラスとしてのみ使われます。


.. exception:: BaseException

   全ての組み込み例外のルートクラスです。ユーザ定義例外を直接このクラ
   スから導出することは意図していません(そういう場合は
   :exc:`Exception` を使ってください)。このクラスに対して :func:`str`
   や :func:`unicode` が呼ばれた場合、引数の文字列表現かまたは引数が無
   い時には空文字列が返されます。
   全ての引数はタプルとして :attr:`args` に格納されます。

   .. versionadded:: 2.5


.. exception:: Exception

   全ての組み込み例外のうち、システム終了でないものはこのクラスから導
   出されています。全てのユーザ定義例外はこのクラスから導出されるべき
   です。

   .. versionchanged:: 2.5
      :exc:`BaseException` から導出するように変更されました.


.. exception:: StandardError

   :exc:`StopIteration` 、:exc:`SystemExit` 、
   :exc:`KeyboardInterrupt` および :exc:`SystemExit` 以外の、全ての組
   み込み例外の基底クラスです。 :exc:`StandardError` 自体は
   :exc:`Exception` から導出されています。


.. exception:: ArithmeticError

   算術上の様々なエラーにおいて送出される組み込み例外:
   :exc:`OverflowError` 、:exc:`ZeroDivisionError` 、
   :exc:`FloatingPointError` の基底クラスです。


.. exception:: LookupError

   マップ型またはシーケンス型に使ったキーやインデクスが無効な値の場合
   に送出される例外: :exc:`IndexError` 、 :exc:`KeyError` の基底クラス
   です。 :func:`sys.setdefaultencoding` によって直接送出されることも
   あります。


.. exception:: EnvironmentError

   Python システムの外部で起こっているはずの例外: :exc:`IOError` 、
   :exc:`OSError` の基底クラスです。この型の例外が 2 つの要素をもつタ
   プルで生成された場合、最初の要素はインスタンスの :attr:`errno`  属
   性で得ることができます (この値はエラー番号と見なされます) 。二つめ
   の要素は :attr:`strerror` 属性です (この値は通常、エラーに関連する
   メッセージです) 。タプル自体は :attr:`args` 属性から得ることもでき
   ます。

   .. versionadded:: 1.5.2

   :exc:`EnvironmentError` 例外が 3 要素のタプルで生成された場合、最初
   の 2 つの要素は上と同様に得ることができる一方、 3 つ目の要素は
   :attr:`filename` 属性で得ることができます。しかしながら、以前のバー
   ジョンとの互換性のために、 :attr:`args` 属性にはコンストラクタに渡
   した最初の 2 つの引数からなる 2 要素のタプルしか含みません。

   この例外が 3 つ以外の引数で生成された場合、 :attr:`filename` 属性は
   ``None`` になります。この例外が 2 または 3 つ以外の引数で生成された
   場合、 :attr:`errno` および :attr:`strerror` 属性も ``None`` になり
   ます。後者のケースでは、 :attr:`args` がコンストラクタに与えた引数
   をそのままタプルの形で含んでいます。

以下の例外は実際に送出される例外です。


.. exception:: AssertionError

   .. index:: statement: assert

   :keyword:`assert` 文が失敗した場合に送出されます。


.. exception:: AttributeError

   属性の参照 (:ref:`attribute-references` を参照下さい) や代入が失敗
   した場合に送出されます (オブジェクトが属性の参照や属性の代入をまっ
   たくサポートしていない場合には :exc:`TypeError` が送出されます ) 。


.. exception:: EOFError

   組み込み関数 (:func:`input` または :func:`raw_input`) のいずれかで、
   データを全く読まないうちにファイルの終端 (EOF) に到達した場合に送出
   されます (注意: :meth:`file.read` および :meth:`file.readline` メソッ
   ドの場合、データを読まないうちに EOF にたどり着くと空の文字列を返し
   ます) 。


.. exception:: FloatingPointError

   浮動小数点演算が失敗した場合に送出されます。この例外はどの Python
   のバージョンでも常に定義されていますが、 Python が
   :option:`--with-fpectl` オプションをつけた状態に設定されているか、
   :file:`pyconfig.h` ファイルにシンボル :const:`WANT_SIGFPE_HANDLER`
   が定義されている場合にのみ送出されます。


.. exception:: GeneratorExit

   ジェネレータ (:term:`generator`) の :meth:`close` メソッドが呼び出
   されたときに送出されます。この例外は技術的にはエラーでないので
   :exc:`StandardError` ではなく :exc:`BaseException` から導出されてい
   ます。

   .. versionchanged:: 2.6
      :exc:`BaseException` からの継承に変更されました。


.. exception:: IOError

   (:keyword:`print` 文、組み込みの :func:`open` またはファイルオブジェ
   クトに対するメソッドといった) I/O 操作が、例えば "ファイルが存在し
   ません" や "ディスクの空き領域がありません" といった I/O に関連した
   理由で失敗した場合に送出されます。

   このクラスは :exc:`EnvironmentError` から導出されています。この例外
   クラスのインスタンス属性に関する情報は上記の
   :exc:`EnvironmentError` に関する議論を参照してください。

   .. versionchanged:: 2.6
      :exc:`socket.error` は、これを基底クラスとして使うように変更され
      ました。


.. exception:: ImportError

   :keyword:`import` 文でモジュール定義を見つけられなかった場合や、
   ``from ... import`` 文で指定した名前をインポートすることができなかっ
   ... た場合に送出されます。


.. exception:: IndexError

   シーケンスのインデクス指定がシーケンスの範囲を超えている場合に送出
   されます　(スライスのインデクスはシーケンスの範囲に収まるように暗黙
   のうちに調整されます; インデクスが通常の整数でない場合、
   :exc:`TypeError` が送出されます) 。

   .. XXX xref to sequences


.. exception:: KeyError

   マップ型 (辞書型) オブジェクトのキーが、オブジェクトのキー集合内に
   見つからなかった場合に送出されます。

   .. XXX xref to mapping objects?


.. exception:: KeyboardInterrupt

   ユーザが割り込みキー (通常は :kbd:`Control-C` または :kbd:`Delete`
   キーです) を押した場合に送出されます。割り込みが起きたかどうかはイ
   ンタプリタの実行中に定期的に調べられます。組み込み関数
   :func:`input` や :func:`raw_input` がユーザの入力を待っている間に割
   り込みキーを押しても、この例外が送出されます。 この例外は
   :exc:`Exception` を捕まえるコードに間違って捕まってインタプリタが終
   了するのを阻止されないように  :exc:`BaseException` から導出されてい
   ます。

   .. versionchanged:: 2.5
      :exc:`BaseException` から導出されるように変更されました.


.. exception:: MemoryError

   ある操作中にメモリが不足したが、その状況は (オブジェクトをいくつか
   消去することで) まだ復旧可能かもしれない場合に送出されます。例外に
   関連づけられた値は、どの種の (内部) 操作がメモリ不足になっている か
   を示す文字列です。背後にあるメモリ管理アーキテクチャ (C の
   :cfunc:`malloc` 関数) によっては、インタプリタが常にその状況を完璧
   に復旧できるとはかぎらないので注意してください; プログラムの暴走が
   原因の場合にも、やはり実行スタックの追跡結果を出力できるようにする
   ために例外が送出されます。


.. exception:: NameError

   ローカルまたはグローバルの名前が見つからなかった場合に送出されます。
   これは非限定の名前のみに適用されます。関連付けられた値は見つからな
   かった名前を含むエラーメッセージです。


.. exception:: NotImplementedError

   この例外は :exc:`RuntimeError` から導出されています。ユーザ定義の基
   底クラスにおいて、そのクラスの導出クラスにおいてオーバライドするこ
   とが必要な抽象化メソッドはこの例外を送出しなくてはなりません。

   .. versionadded:: 1.5.2


.. exception:: OSError

   .. index:: module: errno

   このクラスは :exc:`EnvironmentError` から導出されています。
   関数がシステムに関連したエラーを返した場合に送出されます (引数の
   型が間違っている場合や、他の偶発的なエラーは除きます ) 。
   :attr:`errno` 属性は、 :cdata:`errno` に基づく数字のエラーコードで
   あり、 :attr:`strerror` 属性は、 C の :cfunc:`perror` 関数で印字さ
   れる文字列とみなされます。
   オペレーティングシステムに依存したエラーコードの定義と名前について
   は、 :mod:`errno` モジュールを参照下さい。
   
   ファイルシステムのパスに関係する例外 ( :func:`chdir` や
   :func:`unlink` など ) では、例外インスタンスは関数に渡されたファイ
   ル名を 3 つめの属性として :attr:`filename` を持ちます。

   .. versionadded:: 1.5.2


.. exception:: OverflowError

   算術演算の結果、表現するには大きすぎる値になった場合に送出されます。
   これは長整数の演算では起こらず (長整数の演算ではむしろ
   :exc:`MemoryError` が送出されることになるでしょう) 、通常の整数
   に関するほとんどの操作では長整数を返します。 C では浮動小数点演算に
   おける例外処理の標準化が行われていないので、ほとんどの浮動小数点演
   算もチェックされていません。


.. exception:: ReferenceError

   :func:`weakref.proxy` によって生成された弱参照 (weak reference) プ
   ロキシを使って、ガーベジコレクションによって処理された後の参照対象
   オブジェクトの属性にアクセスした場合に送出されます。弱参照について
   は :mod:`weakref` モジュールを参照してください。

   .. versionadded:: 2.2
      以前は :exc:`weakref.ReferenceError` 例外として知られていました。


.. exception:: RuntimeError

   他のカテゴリに分類できないエラーが検出された場合に送出されます。関
   連付けられた値は何が問題だったのかをより詳細に示す文字列です (こ
   の例外はほとんど過去のバージョンのインタプリタにおける遺物です; こ
   の例外はもはやあまり使われることはありません) 。


.. exception:: StopIteration

   イテレータ (:term:`iterator`) の :meth:`next` メソッドにより、それ
   以上要素がないことを知らせるために送出されます。
   この例外は、通常のアプリケーションではエラーとはみなされないので、
   :exc:`StandardError` ではなく :exc:`Exception` から導出 されていま
   す。

   .. versionadded:: 2.2


.. exception:: SyntaxError

   パーザが構文エラーに遭遇した場合に送出されます。この例外は
   :keyword:`import` 文、 :keyword:`exec` 文、組み込み関数
   :func:`evel` や :func:`input` 、初期化スクリプトの読み込みや標準入
   力で (対話的な実行時にも) 起こる可能性があります。

   このクラスのインスタンスは、例外の詳細に簡単にアクセスできるように
   するために、属性 :attr:`filename` 、:attr:`lineno` 、
   :attr:`offset` および :attr:`text` を持ちます。 例外インスタンスに
   対する :func:`str` はメッセージのみを返します。


.. exception:: SystemError

   インタプリタが内部エラーを発見したが、その状況は全ての望みを棄てさ
   せるほど深刻ではないように思われる場合に送出されます。関連づけられ
   た値は (控えめな言い方で) 何がまずいのかを示す文字列です。

   Python の作者か、あなたの Python インタプリタを保守している人にこの
   エラーを報告してください。このとき、 Python インタプリタのバージョ
   ン (``sys.version``; Python の対話的セッションを開始した際にも出力
   されます) 、正確なエラーメッセージ (例外に関連付けられた値) を忘れ
   ずに報告してください。そしてもし可能ならエラーを引き起こしたプログ
   ラムのソースコードを報告してください。


.. exception:: SystemExit

   この例外は :func:`sys.exit` 関数によって送出されます。この例外が処
   理されなかった場合、 Python インタプリタは終了します; スタックのト
   レースバックは全く印字されません。関連付けられた値が通常の整数であ
   る場合、システム終了状態を指定しています (:cfunc:`exit` 関数に渡さ
   れます); 値が ``None`` の場合、終了状態はゼロです; (文字列のような)
   他の型の場合、そのオブジェクトの値が印字され、終了状態は 1 になりま
   す。

   この例外のインスタンスは属性 :attr:`code` を持ちます。この値は終了
   状態またはエラーメッセージ (標準では ``None`` です) に設定されます。
   また、この例外は技術的にはエラーではないため、 :exc:`StandardError`
   からではなく、:exc:`BaseException` から導出されています。

   :func:`sys.exit` は、後始末のための処理 (:keyword:`try` 文の
   :keyword:`finally` 節) が実行されるようにするため、またデバッガが制
   御不能になるリスクを冒さずにスクリプトを実行できるようにするために
   例外に翻訳されます。即座に終了することが真に強く必要であるとき (例
   えば、 :func:`fork` を呼んだ後の子プロセス内) には :func:`os._exit`
   関数を使うことができます。

   この例外は :exc:`Exception` を捕まえるコードに間違って捕まえられな
   いように、 :exc:`StandardError` や :exc:`Exception` からではなく
   :exc:`BaseException` から導出されています。これにより、この例外は着
   実に呼出し元の方に伝わっていってインタプリタを終了させます。

   .. versionchanged:: 2.5
      :exc:`BaseException` から導出されるように変更され ました。


.. exception:: TypeError

   組み込み演算または関数が適切でない型のオブジェクトに対して適用され
   た際に送出されます。関連付けられる値は型の不整合に関して詳細を述べ
   た文字列です。


.. exception:: UnboundLocalError

   関数やメソッド内のローカルな変数に対して参照を行ったが、その変数に
   は値がバインドされていなかった際に送出されます。 :exc:`NameError`
   のサブクラスです。

   .. versionadded:: 2.0


.. exception:: UnicodeError

   Unicode に関するエンコードまたはデコードのエラーが発生した際に送出
   されます。 :exc:`ValueError` のサブクラスです。

   .. versionadded:: 2.0


.. exception:: UnicodeEncodeError

   Unicode 関連のエラーがエンコード中に発生した際に送出されます。
   :exc:`UnicodeError` のサブクラスです。

   .. versionadded:: 2.3


.. exception:: UnicodeDecodeError

   Unicode 関連のエラーがデコード中に発生した際に送出されます。
   :exc:`UnicodeError` のサブクラスです。

   .. versionadded:: 2.3


.. exception:: UnicodeTranslateError

   Unicode 関連のエラーがコード翻訳に発生した際に送出されます。
   :exc:`UnicodeError` のサブクラスです。

   .. versionadded:: 2.3


.. exception:: ValueError

   組み込み演算や関数が、正しい型だが適切でない値を受け取った場合、お
   よび :exc:`IndexError` のように、より詳細な説明のできない状況で送出
   されます。


.. exception:: VMSError

   VMS においてのみ利用可能。 VMS独自のエラーが起こったときに発生する。


.. exception:: WindowsError

   Windows 特有のエラーか、エラー番号が :cdata:`errno` 値に対応しない
   場合に送出されます。 :attr:`winerrno` および :attr:`strerror` 値は
   Windows プラットフォーム API の関数、 :cfunc:`GetLastError` と
   :cfunc:`FormatMessage` の戻り値から生成されます。 :attr:`errno` の
   値は :attr:`winerror` 値を対応する ``errno.h`` の値に対応付けたもの
   です。

   :exc:`OSError` のサブクラスです。

   .. versionadded:: 2.0

   .. versionchanged:: 2.5
      以前のバージョンは :cfunc:`GetLastError` のコード を
      :attr:`errno` に入れていました。


.. exception:: ZeroDivisionError

   除算またモジュロ演算における二つ目の引数がゼロであった場合に送出さ
   れます。関連付けられている値は文字列で、その演算における被演算子の
   型を示します。

以下の例外は警告カテゴリとして使われます; 詳細については
:mod:`warnings` モジュールを参照してください。


.. exception:: Warning

   警告カテゴリの基底クラスです。


.. exception:: UserWarning

   ユーザコードによって生成される警告の基底クラスです。


.. exception:: DeprecationWarning

   廃用された機能に対する警告の基底クラスです。


.. exception:: PendingDeprecationWarning

   将来廃用されることになっている機能に対する警告の基底クラスです。


.. exception:: SyntaxWarning

   曖昧な構文に対する警告の基底クラスです。


.. exception:: RuntimeWarning

   あいまいなランタイム挙動に対する警告の基底クラスです。


.. exception:: FutureWarning

   将来意味構成が変わることになっている文の構成に対する警告の基底クラスです。


.. exception:: ImportWarning

   モジュールインポートの誤りと思われるものに対する警告の基底クラスです。

   .. versionadded:: 2.5


.. exception:: UnicodeWarning

   ユニコードに関連した警告の基底クラスです。

   .. versionadded:: 2.5

組み込み例外のクラス階層は以下のようになっています:


.. literalinclude:: ../includes/exception_hierarchy.txt

