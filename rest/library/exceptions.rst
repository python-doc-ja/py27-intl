
組み込み例外
======

.. module:: exceptions
   :synopsis: 標準の例外クラス群


例外はクラスオブジェクトです。 例外はモジュール :mod:`exceptions` で定義されています。
このモジュールを明示的にインポートする必要はありません: 例外は :mod:`exceptions` モジュールと同様に組み込み名前空間で 与えられます。

.. % \begin{note}

.. note::

   過去の Python のバージョンでは、文字列の例外がサポートされていました。 Python 1.5 よりも新しいバージョンでは、全ての標準的な例外は
   クラスオブジェクトに変換され、ユーザにも同様にするよう奨励しています。 文字列による例外は Python 2.5 以降は
   ``DeprecationWarning`` を 送出するようになります。 将来のバージョンでは、文字列による例外のサポートは削除されます。

   同じ値を持つ別々の文字列オブジェクトは異なる例外と見なされます。 これはプログラマに対して、例外処理を指定する際に、
   文字列ではなく例外名を使わせるための変更です。組み込み例外の文字列値は 全てその名前となりますが、ユーザ定義の例外やライブラリモジュールで定義される
   例外についてもそうするように要求しているわけではありません。

.. index::
   statement: try
   statement: except

:keyword:`try` 文の中で、:keyword:`except`  節を使って特定の例外クラスについて記述した場合、その節は
指定した例外クラスから導出されたクラスも扱います (指定した例外 クラスを導出した元のクラスは含みません)
サブクラス化の関係にない例外クラスが二つあった場合、それらに同じ 名前を付けたとしても、等しくなることはありません。

.. % \end{note}

.. index:: statement: raise

以下に列挙した組み込み例外はインタプリタや組み込み関数によって生成 されます。特に注記しないかぎり、これらの例外は エラーの詳しい原因を 示している、 "関連値
(associated value)" を持ちます。 この値は文字列または複数の情報 (例えばエラーコードや、エラーコード を説明する文字列)
を含むタプルです。この関連値は :keyword:`raise` 文の二つ目の引数です。 文字列の例外の場合、関連値自体は :keyword:`except`
節 (あった場合) の二つ目の引数として与えた名前を持つ変数に記憶されます。 クラス例外の場合、この値は例外クラスのインスタンスです。
例外が標準のルートクラスである :exc:`BaseException` から 導出された場合、関連値は例外インスタンスの :attr:`args` 属性中
に置かれます。もし引数が一つならば(このようにすることが望まれますが)、 その引数の値は :attr:`message` 属性に収められます。

ユーザによるコードも組み込み例外を送出することができます。 これは例外処理をテストしたり、インタプリタがある例外を送出する 状況と "ちょうど同じような"
エラー条件であることを報告させるために 使うことができます。しかし、ユーザが適切でないエラーを送出するよう コードするのを妨げる方法はないので注意してください。

組み込み例外クラスは新たな例外を定義するためにサブクラス化する ことができます; プログラマには、新しい例外を少なくとも :exc:`Exception`
クラスから導出するよう勧めます。 :exc:`BaseException` からは導出しないで下さい。 例外を定義する上での詳しい情報は、 Python
チュートリアル (XXX reference: ../tut/tut.html) の "ユーザ定義の例外" の項目にあります。

以下の例外クラスは他の例外クラスの基底クラスとしてのみ使われます。


.. exception:: BaseException

   全ての組み込み例外のルートクラスです。ユーザ定義例外を直接このクラス から導出することは意図していません(そういう場合は :exc:`Exception`
   を使ってください)。このクラスに対して :func:`str` や :func:`unicode` が呼ばれた場合、引数の文字列表現かまたは引数が無
   い時には空文字列が返されます。一つだけの引数が渡された場合、それが :attr:`message` 属性に格納されます。二つ以上の引数が渡された場合、
   :attr:`message` 属性は空文字列になります。こうした振舞いは :attr:`message` がなぜ例外が送出されたかを説明するメッセージを格納す
   る場所だという事実を反映することを意図しています。例外に対してより多く のデータを紐付けたい場合は、インスタンスの任意の属性が利用できます。 全ての引数は
   :attr:`args` にもタプルとして格納されるようになっていま すが、この属性は廃止の方向に向かっていますのでできるだけ使わないように
   する方がいいでしょう。

   .. versionadded:: 2.5


.. exception:: Exception

   全ての組み込み例外のうち、システム終了でないものはこのクラスから導出 されています。全てのユーザ定義例外はこのクラスから導出される べきです。

   .. versionchanged:: 2.5
      :exc:`BaseException` から導出するように変更されました.


.. exception:: StandardError

   :exc:`StopIteration`、:exc:`SystemExit`、 :exc:`KeyboardInterrupt` および
   :exc:`SystemExit` 以外の、全ての組み込み例外の基底クラスです。 :exc:`StandardError` 自体は
   :exc:`Exception` から導出されています。


.. exception:: ArithmeticError

   算術上の様々なエラーにおいて送出される組み込み例外:  :exc:`OverflowError`、:exc:`ZeroDivisionError`、
   :exc:`FloatingPointError` の基底クラスです。


.. exception:: LookupError

   マップ型またはシーケンス型に使ったキーやインデクスが無効な値の場合に 送出される例外::exc:`IndexError`、:exc:`KeyError`
   の基底クラスです。:func:`sys.setdefaultencoding` によって直接送出されることもあります。


.. exception:: EnvironmentError

   Python システムの外部で起こっているはずの例外: :exc:`IOError`、 :exc:`OSError` の基底クラスです。この型の例外が 2
   つの要素を もつタプルで生成された場合、最初の要素はインスタンスの :attr:`errno`  属性で得ることができます
   (この値はエラー番号と見なされます)。二つめの 要素は :attr:`strerror` 属性です (この値は通常、エラーに関連する
   メッセージです)。タプル自体は :attr:`args` 属性から得ることもできます。

   .. versionadded:: 1.5.2

   :exc:`EnvironmentError` 例外が 3 要素のタプルで生成された場合、 最初の 2 つの要素は上と同様に得ることができる一方、3
   つ目の要素は :attr:`filename` 属性で得ることができます。しかしながら、以前の バージョンとの互換性のために、:attr:`args`
   属性にはコンストラクタに渡した 最初の 2 つの引数からなる 2 要素のタプルしか含みません。

   この例外が 3 つ以外の引数で生成された場合、:attr:`filename` 属性は ``None`` になります。この例外が 2 または 3
   つ以外の引数で生成 された場合、:attr:`errno` および :attr:`strerror` 属性も ``None``
   になります。後者のケースでは、:attr:`args` が コンストラクタに与えた引数をそのままタプルの形で含んでいます。

以下の例外は実際に送出される例外です。


.. exception:: AssertionError

   .. index:: statement: assert

   :keyword:`assert` 文が失敗した場合に送出されます。


.. exception:: AttributeError

   属性の参照や代入が失敗した場合に送出されます。(オブジェクトが 属性の参照や属性の代入をまったくサポートしていない場合には :exc:`TypeError`
   が送出されます。)

   .. % xref to attribute reference?


.. exception:: EOFError

   組み込み関数 (:func:`input` または  :func:`raw_input`)  のいずれかで、データを全く読まないうちにファイルの終端 (EOF)
   に 到達した場合に送出されます。 (注意: ファイルオブジェクトの :meth:`read` および :meth:`readline`
   メソッドの場合、データを読まないうちに EOFにたどり着くと空の文字列 を返します。)

   .. % XXXJH xrefs here
   .. % XXXJH xrefs here


.. exception:: FloatingPointError

   浮動小数点演算が失敗した場合に送出されます。この例外はどの Python のバージョンでも常に定義されていますが、Python が
   :option:`--with-fpectl` オプションをつけた状態に設定されて いるか、:file:`pyconfig.h` ファイルにシンボル
   :const:`WANT_SIGFPE_HANDLER` が定義されている場合にのみ 送出されます。


.. exception:: GeneratorExit

   ジェネレータの :meth:`close` メソッドが呼び出されたときに送出されま す。この例外は技術的にはエラーでないので
   :exc:`StandardError` ではなく :exc:`Exception` から導出されています。

   .. versionadded:: 2.5


.. exception:: IOError

   (:keyword:`print` 文、組み込みの :func:`open` またはファイル オブジェクトに対するメソッドといった) I/O 操作が、例えば
   "ファイルが存在しません" や "ディスクの空き領域がありません" といった I/O に関連した理由で失敗した場合に送出されます。

   .. % XXXJH xrefs here

   このクラスは :exc:`EnvironmentError` から導出されています。 この例外クラスのインスタンス属性に関する情報は上記の
   :exc:`EnvironmentError` に関する議論を参照してください。


.. exception:: ImportError

   :keyword:`import` 文でモジュール定義を見つけられなかった場合や、 ``from ... import`` 文で指定した名前をインポート
   することができなかった場合に送出されます。

   .. % XXXJH xref to import statement?


.. exception:: IndexError

   シーケンスのインデクス指定がシーケンスの範囲を超えている場合に送出 されます。(スライスのインデクスはシーケンスの範囲に収まるように暗黙のうちに 調整されます;
   インデクスが通常の整数でない場合、:exc:`TypeError` が送出されます。)

   .. % XXXJH xref to sequences


.. exception:: KeyError

   マップ型 (辞書型) オブジェクトのキーが、オブジェクトのキー集合内に 見つからなかった場合に送出されます。

   .. % XXXJH xref to mapping objects?


.. exception:: KeyboardInterrupt

   ユーザが割り込みキー (通常は :kbd:`Control-C` または :kbd:`Delete` キー です)
   を押した場合に送出されます。割り込みが起きたかどうかはインタプリタ の実行中に定期的に調べられます。 組み込み関数 :func:`input` や
   :func:`raw_input` がユーザの 入力を待っている間に割り込みキーを押しても、この例外が送出されます。 この例外は
   :exc:`Exception` を捕まえるコードに間違って捕まってイ ンタプリタが終了するのを阻止されないように  :exc:`BaseException`
   から導出されています。

   .. % XXX(hylton) xrefs here

   .. versionchanged:: 2.5
      :exc:`BaseException` から導出されるように変更され ました.


.. exception:: MemoryError

   ある操作中にメモリが不足したが、その状況は (オブジェクトをいくつか 消去することで) まだ復旧可能かもしれない場合に送出されます。
   例外に関連づけられた値は、どの種の (内部) 操作がメモリ不足になっている かを示す文字列です。背後にあるメモリ管理アーキテクチャ (C の
   :cfunc:`malloc` 関数) によっては、インタプリタが常にその状況 を完璧に復旧できるとはかぎらないので注意してください; プログラムの
   暴走が原因の場合にも、やはり実行スタックの追跡結果を出力 できるようにするために例外が送出されます。


.. exception:: NameError

   ローカルまたはグローバルの名前が見つからなかった場合に送出されます。 これは非限定の名前のみに適用されます。関連付けられた値は見つからなかった
   名前を含むエラーメッセージです。


.. exception:: NotImplementedError

   この例外は :exc:`RuntimeError` から導出されています。ユーザ定義の 基底クラスにおいて、そのクラスの導出クラスにおいてオーバライドする
   ことが必要な抽象化メソッドはこの例外を送出しなくてはなりません。

   .. versionadded:: 1.5.2


.. exception:: OSError

   このクラスは :exc:`EnvironmentError` から導出されており、 主に :mod:`os` モジュールの ``os.error``
   例外で使われて います。例外に関連付けられる可能性のある値については、上記の  :exc:`EnvironmentError` を参照してください。

   .. % xref for os module

   .. versionadded:: 1.5.2


.. exception:: OverflowError

   算術演算の結果、表現するには大きすぎる値になった場合に送出されます。 これは長整数の演算では起こりません (長整数の演算ではむしろ
   :exc:`MemoryError` が送出されることになるでしょう)。 C では浮動小数点演算における例外処理の標準化が行われていないので、
   ほとんどの浮動小数点演算もチェックされていません。通常の整数では、 オーバフローを起こす全ての演算がチェックされます。例外は左シフトで、
   典型的なアプリケーションでは左シフトのオーバフローでは例外を送出する よりもむしろ、オーバフローしたビットを捨てるようにしています。

   .. % XXXJH reference to long's and/or int's?


.. exception:: ReferenceError

   :func:`weakref.proxy` によって生成された弱参照 (weak reference) プロキシを使って、ガーベジコレクションによって処理
   された後の参照対象オブジェクトの属性にアクセスした場合に送出されます。 弱参照については :mod:`weakref` モジュールを参照してください。

   .. versionadded:: 2.2
      以前は :exc:`weakref.ReferenceError` 例外として知られていました。.


.. exception:: RuntimeError

   他のカテゴリに分類できないエラーが検出された場合に送出されます。 関連付けられた値は何が問題だったのかをより詳細に示す文字列です。
   (この例外はほとんど過去のバージョンのインタプリタにおける遺物です; この例外はもはやあまり使われることはありません)


.. exception:: StopIteration

   イテレータの :meth:`next` メソッドにより、それ以上要素がないことを 知らせるために送出されます。
   この例外は、通常のアプリケーションではエラーとはみなされないので、 :exc:`StandardError` ではなく :exc:`Exception`
   から導出 されています。

   .. versionadded:: 2.2


.. exception:: SyntaxError

   パーザが構文エラーに遭遇した場合に送出されます。この例外は :keyword:`import` 文、:keyword:`exec` 文、組み込み関数
   :func:`evel` や :func:`input`、初期化スクリプトの 読み込みや標準入力で (対話的な実行時にも) 起こる可能性があります。

   .. % XXXJH xref to these functions?

   このクラスのインスタンスは、例外の詳細に簡単にアクセスできるように するために、属性 :attr:`filename`、:attr:`lineno`、
   :attr:`offset` および :attr:`text` を持ちます。 例外インスタンスに対する :func:`str` はメッセージのみを返します。


.. exception:: SystemError

   インタプリタが内部エラーを発見したが、その状況は全ての望みを 棄てさせるほど深刻ではないように思われる場合に送出されます。 関連づけられた値は
   (控えめな言い方で) 何がまずいのかを示す文字列です。

   Python の作者か、あなたの Python インタプリタを保守している人に このエラーを報告してください。このとき、 Python インタプリタの
   バージョン (``sys.version``; Python の対話的セッションを開始した 際にも出力されます)、正確なエラーメッセージ
   (例外に関連付けられた値) を忘れずに報告してください。 そしてもし可能ならエラーを引き起こしたプログラムのソースコードを 報告してください。


.. exception:: SystemExit

   この例外は :func:`sys.exit` 関数によって送出されます。この例外が 処理されなかった場合、Python インタプリタは終了します; スタックの
   トレースバックは全く印字されません。関連付けられた値が通常の整数 である場合、システム終了状態を指定しています (:cfunc:`exit` 関数に
   渡されます); 値が ``None``の場合、終了状態はゼロです; (文字列のような) 他の型の場合、そのオブジェクトの値が印字され、終了状態は 1
   になります。

   .. % XXX(hylton) xref to module sys?

   この例外のインスタンスは属性 :attr:`code` を持ちます。この値は 終了状態またはエラーメッセージ (標準では ``None`` です) に
   設定されます。また、この例外は技術的にはエラーではないため、 :exc:`StandardError` からではなく、:exc:`BaseException`
   から 導出されています。

   :func:`sys.exit` は、後始末のための処理 (:keyword:`try` 文の  :keyword:`finally` 節)
   が実行されるようにするため、またデバッガが 制御不能になるリスクを冒さずにスクリプトを実行できるようにするために
   例外に翻訳されます。即座に終了することが真に強く必要であるとき (例えば、:func:`fork` を呼んだ後の子プロセス内) には
   :func:`os._exit` 関数を使うことができます。

   この例外は :exc:`Exception` を捕まえるコードに間違って捕まえられ ないように、:exc:`StandardError` や
   :exc:`Exception` からで はなく :exc:`BaseException` から導出されています。これにより、
   この例外は着実に呼出し元の方に伝わっていってインタプリタを終了させます。

   .. versionchanged:: 2.5
      :exc:`BaseException` から導出されるように変更され ました。.


.. exception:: TypeError

   組み込み演算または関数が適切でない型のオブジェクトに対して適用 された際に送出されます。関連付けられる値は型の不整合に関して 詳細を述べた文字列です。


.. exception:: UnboundLocalError

   関数やメソッド内のローカルな変数に対して参照を行ったが、その変数には 値がバインドされていなかった際に送出されます。:exc:`NameError`
   のサブクラスです。

   .. versionadded:: 2.0


.. exception:: UnicodeError

   Unicode に関するエンコードまたはデコードのエラーが発生した際に送出 されます。:exc:`ValueError` のサブクラスです。

   .. versionadded:: 2.0


.. exception:: UnicodeEncodeError

   Unicode 関連のエラーがエンコード中に発生した際に送出されます。 :exc:`UnicodeError` のサブクラスです。

   .. versionadded:: 2.3


.. exception:: UnicodeDecodeError

   Unicode 関連のエラーがデコード中に発生した際に送出されます。 :exc:`UnicodeError` のサブクラスです。

   .. versionadded:: 2.3


.. exception:: UnicodeTranslateError

   Unicode 関連のエラーがコード翻訳に発生した際に送出されます。 :exc:`UnicodeError` のサブクラスです。

   .. versionadded:: 2.3


.. exception:: ValueError

   組み込み演算や関数が、正しい型だが適切でない値を受け取った場合、 および :exc:`IndexError` のように、より詳細な説明のできない
   状況で送出されます。


.. exception:: WindowsError

   Windows 特有のエラーか、エラー番号が :cdata:`errno` 値に対応しない 場合に送出されます。:attr:`winerrno` および
   :attr:`strerror` 値は Windows プラットフォーム API の関数、 :cfunc:`GetLastError` と
   :cfunc:`FormatMessage` の戻り値から生成されます。 :attr:`errno` の値は :attr:`winerror` 値を対応する
   ``errno.h``  の値に対応付けたものです。

   :exc:`OSError` のサブクラスです。

   .. versionadded:: 2.0

   .. versionchanged:: 2.5
      以前のバージョンは :cfunc:`GetLastError` のコード を :attr:`errno` に入れていました。.


.. exception:: ZeroDivisionError

   除算またモジュロ演算における二つ目の引数がゼロであった場合に 送出されます。関連付けられている値は文字列で、その演算における 被演算子の型を示します。

以下の例外は警告カテゴリとして使われます; 詳細については :mod:`warnings` モジュールを参照してください。


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


.. include:: ../includes/exception_hierarchy.txt
   :literal:

