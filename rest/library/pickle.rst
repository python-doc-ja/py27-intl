
:mod:`pickle` --- Python オブジェクトの整列化
===================================

.. index::
   single: persistence
   pair: persistent; objects
   pair: serializing; objects
   pair: marshalling; objects
   pair: flattening; objects
   pair: pickling; objects

.. module:: pickle
   :synopsis: Python オブジェクトからバイトストリームへの変換、およびその逆。


.. % Substantial improvements by Jim Kerr <jbkerr@sr.hp.com>.
.. % Rewritten by Barry Warsaw <barry@zope.com>

:mod:`pickle` モジュールでは、Python オブジェクトデータ構造を 直列化 (serialize) したり非直列化 (de-serialize)
するための 基礎的ですが強力なアルゴリズムを実装しています。 "Pickle 化 (Pickling)" は Python のオブジェクト階層をバイト
ストリームに変換する過程を指します。"非 Pickle 化 (unpickling)" はその逆の操作で、バイトストリームをオブジェクト階層に戻すように
変換します。Pickle 化 (及び非 Pickle 化) は、別名 "直列化 (serialization)" や "整列化 (marshalling)"
[#]_ 、"平坦化 (flattening)" として知られていますが、 ここでは混乱を避けるため、用語として "Pickle 化" および  "非
Pickle 化" を使います。

このドキュメントでは :mod:`pickle` モジュールおよび :mod:`cPickle` モジュールの両方について記述します。


他の Python モジュールとの関係
-------------------

:mod:`pickle` モジュールには :mod:`cPickle` と呼ばれる 最適化のなされた親類モジュールがあります。名前が示すように、
:mod:`cPickle` は C で書かれており、このため :mod:`pickle` より 1000 倍くらいまで高速になる可能性があります。しかしながら
:mod:`cPickle` では :func:`Pickler` および  :func:`Unpickler` クラスのサブクラス化をサポートしていません。
これは :mod:`cPickle` では、これらは関数であってクラスでは ないからです。ほとんどのアプリケーションではこの機能は
不要であり、:mod:`cPickle` の持つ高いパフォーマンスの 恩恵を受けることができます。その他の点では、二つのモジュールに
おけるインタフェースはほとんど同じです; このマニュアルでは 共通のインタフェースを記述しており、必要に応じてモジュール間
の相違について指摘します。以下の議論では、:mod:`pickle`  と :mod:`cPickle` の総称として "pickle" という用語を使う
ことにします。

これら二つのモジュールが生成するデータストリームは相互交換 できることが保証されています。

Python には :mod:`marshal` と呼ばれるより原始的な直列化モジュール がありますが、一般的に Python
オブジェクトを直列化する方法としては :mod:`pickle` を選ぶべきです。:mod:`marshal` は基本的に :file:`.pyc`
ファイルをサポートするために存在しています。

:mod:`pickle` モジュールはいくつかの点で :mod:`marshal` と明確に異なります:

* :mod:`pickle` モジュールでは、同じオブジェクトが再度直列化 されることのないよう、すでに直列化されたオブジェクトについて追跡
  情報を保持します。:mod:`marshal` はこれを行いません。

  この機能は再帰的オブジェクトと共有オブジェクトの両方に重要な 関わりをもっています。再帰的オブジェクトとは自分自身に対する
  参照を持っているオブジェクトです。再帰的オブジェクトは marshal で扱うことができず、実際、再帰的オブジェクトを marshal 化しようと すると
  Python インタプリタをクラッシュさせてしまいます。 共有オブジェクトは、直列化しようとするオブジェクト階層の異なる
  複数の場所で同じオブジェクトに対する参照が存在する場合に生じます。 共有オブジェクトを共有のままにしておくことは、変更可能なオブジェクト
  の場合には非常に重要です。

* :mod:`marshal` はユーザ定義クラスやそのインスタンスを 直列化するために使うことができません。:mod:`pickle` は
  クラスインスタンスを透過的に保存したり復元したりすることができますが、 クラス定義をインポートすることが可能で、かつオブジェクトが保存
  された際と同じモジュールで定義されていなければなりません。

* :mod:`marshal` の直列化フォーマットは Python の異なる バージョンで可搬性があることを保証していません。:mod:`marshal`
  の本来の仕事は :file:`.pyc` ファイルのサポートなので、Python  を実装する人々には、必要に応じて直列化フォーマットを以前の
  バージョンと互換性のないものに変更する権限が残されています。 :mod:`pickle` 直列化フォーマットには、全ての Python リリース
  間で以前のバージョンとの互換性が保証されています。

  .. % \item \module{pickle} モジュールはコードオブジェクトを扱いませんが、
  .. % \module{marshal} は扱います。これにより、 \module{pickle} モジュールを
  .. % 通してプログラムにトロイの木馬を持ち込まれる可能性を避けています
  .. % \footnote{このことは \module{pickle} が本質的に安全であるということを
  .. % 示すわけではありません。\module{pickle} モジュールの安全性に関する
  .. % より詳細な議論については、~\ref{pickle-sec} 節を読んで下さい。
  .. % なお、\module{pickle} は最終的にコードオブジェクトの直列化を
  .. % サポートする可能性があります。}。

.. 警告::

   :mod:`pickle` モジュールは誤りを含む、あるいは悪意を持って 構築されたデータに対して安全にはされていません。信用できない、
   あるいは認証されていないデータ源から受信したデータを逆 pickle 化 しないでください。

直列化は永続化 (persisitence) よりも原始的な概念です; :mod:`pickle` はファイルオブジェクトを読み書きしますが、永続化
されたオブジェクトの名前付け問題や、(より複雑な) オブジェクトに 対する競合アクセスの問題を扱いません。:mod:`pickle` モジュール
は複雑なオブジェクトをバイトストリームに変換することができ、 バイトストリームを変換前と同じ内部構造をオブジェクトに変換する
ことができます。このバイトストリームの最も明白な用途は ファイルへの書き込みですが、その他にもネットワークを介して送信
したり、データベースに記録したりすることができます。 モジュール :mod:`shelve` はオブジェクトを DBM 形式の データベースファイル上で
pickle 化したり unpickle 化したりする ための単純なインタフェースを提供しています。


データストリームの形式
-----------

.. index::
   single: XDR
   single: External Data Representation

:mod:`pickle` が使うデータ形式は Python 特有です。そうする ことで、XDR のような 外部の標準が持つ制限 (例えば XDR
ではポインタの共有を表現できません) を課せられることがないという利点があります; しかしこれは Python で書かれていないプログラムが pickle
化された Python オブジェクトを 再構築できない可能性があることを意味します。

標準では、:mod:`pickle` データ形式では印字可能な ASCII 表現を 使います。これはバイナリ表現よりも少しかさばるデータになります。 印字可能な
ASCII の利用 (とその他の :mod:`pickle` 表現形式が 持つ特徴) の大きな利点は、デバッグやリカバリを目的とした場合に、 pickle
化されたファイルを標準的なテキストエディタで読めるという ことです。

現在、pickle化に使われるプロトコルは、以下の 3 種類です。

* バージョン 0 のプロトコルは、最初の ASCII プロトコルで、以前のバージョンのPython と後方互換です。

* バージョン 1 のプロトコルは、古いバイナリ形式で、以前のバージョンの Python と後方互換です。

* バージョン 2 のプロトコルは、Python 2.3 で導入されました。新しいスタイルのクラスを、より効率よく piclke 化します。

詳細は PEP 307 を参照してください。

*protocol* を指定しない場合、プロトコル 0 が使われます。*protocol* に負値か :const:`HIGHEST_PROTOCOL`
を指定すると、有効なプロトコルの内、もっとも高いバージョンのものが使われます。

.. versionchanged:: 2.3
   *protocol* パラメータが導入されました。.

*protocol* version >= 1 を指定することで、少しだけ効率の高いバイナリ 形式を選ぶことができます。


使用法
---

オブジェクト階層を直列化するには、まず pickler を生成し、続いてpickler  の :meth:`dump`
メソッドを呼び出します。データストリームから非直列化 するには、まず unpickler を生成し、続いて unpicklerの :meth:`load` メ
ソッドを呼び出します。:mod:`pickle` モジュールでは以下の定数を提供して います:


.. data:: HIGHEST_PROTOCOL

   有効なプロトコルのうち、最も大きいバージョン。この値は、*protocol*  として渡せます。

   .. versionadded:: 2.3

.. note::

   protocols >= 1 で作られた pickle ファイルは、常にバイナリモードで オープンするようにしてください。古い ASCII ベースの
   pickle プロトコル 0 では、 矛盾しない限りにおいてテキストモードとバイナリモードのいずれも利用することができます。

   プロトコル 0 で書かれたバイナリの pickle ファイルは、行ターミネータとして単独の改行(LF)を含んでいて、 ですのでこの形式をサポートしない、
   Notepad や他のエディタで見たときに「おかしく」見えるかもしれません。

この pickle 化の手続きを便利にするために、:mod:`pickle` モジュールでは 以下の関数を提供しています:


.. function:: dump(obj, file[, protocol])

   すでに開かれているファイルオブジェクト *file* に、*obj* を pickle 化したものを表現する文字列を書き込みます。
   ``Pickler(file, protocol).dump(obj)``  と同じです。

   *protocol* を指定しない場合、プロトコル 0 が使われます。 *protocol* に負値か :const:`HIGHEST_PROTOCOL`
   を指定すると、 有効なプロトコルの内、もっとも高いバージョンのものが使われます。

   .. versionchanged:: 2.3
      *protocol* パラメータが導入されました。.

   *file* は、単一の文字列引数を受理する :meth:`write` メソッド を持たなければなりません。従って、 *file* としては、書き込みのために
   開かれたファイルオブジェクト、 :mod:`StringIO` オブジェクト、 その他前述のインタフェースに適合する他のカスタムオブジェクトをとることが
   できます。


.. function:: load(file)

   すでに開かれているファイルオブジェクト *file* から文字列を読み出し、 読み出された文字列を pickle 化されたデータ列として解釈して、もとの
   オブジェクト階層を再構築して返します。``Unpickler(file).load()`` と同じです。

   *file* は、整数引数をとる :meth:`read` メソッドと、引数の必要 ない :meth:`readline` メソッドを持たなければなりません。
   これらのメソッドは両方とも文字列を返さなければなりません。 従って、 *file* としては、読み出しのために 開かれたファイルオブジェクト、
   :mod:`StringIO` オブジェクト、 その他前述のインタフェースに適合する他のカスタムオブジェクトをとることが できます。

   この関数はデータ列の書き込まれているモードがバイナリかそうでないかを 自動的に判断します。


.. function:: dumps(obj[, protocol])

   *obj* の pickle 化された表現を、ファイルに書き込む代わりに 文字列で返します。

   *protocol* を指定しない場合、プロトコル 0 が使われます。 *protocol* に負値か :const:`HIGHEST_PROTOCOL`
   を指定すると、 有効なプロトコルの内、もっとも高いバージョンのものが使われます。

   .. versionchanged:: 2.3
      *protocol* パラメータが追加されました。.


.. function:: loads(string)

   pickle 化されたオブジェクト階層を文字列から読み出します。 文字列中で pickle 化されたオブジェクト表現よりも後に続く文字列 は無視されます。

:mod:`pickle` モジュールでは、以下の 3 つの例外も定義しています:


.. exception:: PickleError

   下で定義されている他の例外で共通の基底クラスです。:exc:`Exception` を継承しています。


.. exception:: PicklingError

   この例外は unpickle 不可能なオブジェクトが :meth:`dump` メソッドに 渡された場合に送出されます。


.. exception:: UnpicklingError

   この例外は、オブジェクトを unpickle 化する際に問題が発生した場合に 送出されます。 unpickle 化中には
   :exc:`AttributeError`、 :exc:`EOFError`、 :exc:`ImportError`、および :exc:`IndexError`
   といった他の例外 (これだけとは限りません) も発生する可能性があるので 注意してください。

:mod:`pickle` モジュールでは、2 つの呼び出し可能オブジェクト  [#]_ として、:class:`Pickler` および
:class:`Unpickler` を提供しています:


.. class:: Pickler(file[, protocol])

   pickle 化されたオブジェクトのデータ列を書き込むためのファイル類似の オブジェクトを引数にとります。

   *protocol* を指定しない場合、プロトコル 0 が使われます。*protocol* に負値か :const:`HIGHEST_PROTOCOL`
   を指定すると、有効なプロトコルの内、もっとも高いバージョンのものが使われます。

   .. versionchanged:: 2.3
      *protocol* パラメータが導入されました。.

   *file* は単一の文字列引数を受理する :meth:`write` メソッドを 持たなければなりません。従って、 *file* としては、書き込みのために
   開かれたファイルオブジェクト、 :mod:`StringIO` オブジェクト、 その他前述のインタフェースに適合する他のカスタムオブジェクトをとることが
   できます。

:class:`Pickler` オブジェクトでは、一つ (または二つ) の public なメソッド を定義しています:


.. method:: Pickler.dump(obj)

   コンストラクタで与えられた、すでに開かれているファイルオブジェクトに *obj* の pickle 化された表現を書き込みます。コンストラクタに渡された
   *protocol* 引数の値に応じて、バイナリおよびASCII 形式が使われます。


.. method:: Pickler.clear_memo()

   picller の "メモ" を消去します。メモとは、共有オブジェクトまたは 再帰的なオブジェクトが値ではなく参照で記憶されるようにするために、 pickler
   がこれまでどのオブジェクトに遭遇してきたかを記憶するデータ 構造です。このメソッドは pickler を再利用する際に便利です。

   .. note::

      Python 2.3 以前では、:meth:`clear_memo` は :mod:`cPickle`  で生成された pickler
      でのみ利用可能でした。:mod:`pickle` モジュール では、pickler は :attr:`memo` と呼ばれる Python 辞書型のインスタンス
      変数を持ちます。従って、:mod:`pickler` モジュールにおける pickler のメモを消去は、以下のようにしてできます::

         mypickler.memo.clear()

      以前のバージョンの Python での動作をサポートする必要のないコードでは、 単に :meth:`clear_memo` を使ってください。

同じ :class:`Pickler` のインスタンスに対し、 :meth:`dump` メソッドを 複数回呼び出すことは可能です。この呼び出しは、対応する
:class:`Unpickler` インスタンスで同じ回数だけ :meth:`load` を呼び出す操作に対応します。 同じオブジェクトが
:meth:`dump` を複数回呼び出して pickle 化された 場合、:meth:`load` は全て同じオブジェクトに対して参照を行います  [#]_。
。

:class:`Unpickler` オブジェクトは以下のように定義されています:


.. class:: Unpickler(file)

   pickle データ列を読み出すためのファイル類似のオブジェクトを引数に 取ります。このクラスはデータ列がバイナリモードかどうかを自動的に
   判別します。従って、:class:`Pickler` のファクトリメソッドのような フラグを必要としません。

   *file* は、整数引数を取る :meth:`read` メソッド、および引数を 持たない :meth:`readline` メソッドの、 2
   つのメソッドを持ちます。 両方のメソッドとも文字列を返します。従って、 *file* としては、 読み出しのために開かれたファイルオブジェクト、
   :mod:`StringIO`  オブジェクト、その他前述のインタフェースに適合する他のカスタム オブジェクトをとることができます。

:class:`Unpickler` オブジェクトは 1 つ (または 2 つ) の public な メソッドを持っています:


.. method:: Unpickler.load()

   コンストラクタで渡されたファイルオブジェクトからオブジェクトの pickle 化表現 を読み出し、中に収められている再構築されたオブジェクト階層を返します。


.. method:: Unpickler.noload()

   :meth:`load` に似ていますが、実際には何もオブジェクトを生成 しないという点が違います。この関数は第一に pickle
   化データ列中で参照されている、"永続化 id" と呼ばれている 値を検索する上で便利です。 詳細は以下の  :ref:`pickle-protocol`
   を参照してください。

   **注意:** :meth:`noload` メソッドは現在 :mod:`cPickle` モジュールで生成された :class:`Unpickler`
   オブジェクトのみで 利用可能です。:mod:`pickle` モジュールの :class:`Unpickler`  には、 :meth:`noload`
   メソッドがありません。


何を pickle 化したり unpickle 化できるのか?
-------------------------------

以下の型は pickle 化できます:

* ``None``、 ``True``、および ``False``

* 整数、長整数、浮動小数点数、複素数

* 通常文字列および Unicode 文字列

* pickle 化可能なオブジェクトからなるタプル、リスト、集合および辞書

* モジュールのトップレベルで定義されている関数

* モジュールのトップレベルで定義されている組込み関数

* モジュールのトップレベルで定義されているクラス

* :attr:`__dict__` または :meth:`__setstate__` を pickle 化 できる上記クラスのインスタンス (詳細は
  :ref:`pickle-protocol` 節を 参照してください)

pickle 化できないオブジェクトを pickle 化しようとすると、 :exc:`PicklingError` 例外が送出されます; この例外が起きた
場合、背後のファイルには未知の長さのバイト列が書き込まれて しまいます。 極端に再帰的なデータ構造を pickle 化しようとした場合には
再帰の深さ制限を越えてしまうかもしれず、この場合には :exc:`RuntimeError` が
送出されます。この制限は、:func:`sys.setrecursionlimit` で 慎重に上げていくことは可能です。

(組み込みおよびユーザ定義の) 関数は、値ではなく "完全記述された" 参照名として pickle 化されるので注意してください。これは、
関数の定義されているモジュールの名前と一緒と併せ、関数名 だけが pickle 化されることを意味します。 関数のコードや関数の属性は何も pickle
化されません。 従って、定義しているモジュールは unpickle 化環境で import 可能で
なければならず、そのモジュールには指定されたオブジェクトが含まれて いなければなりません。そうでない場合、例外が送出されます  [#]_ 。

クラスも同様に名前参照で pickle 化されるので、unpickle 化環境には 同じ制限が課せられます。クラス中のコードやデータは何も pickle 化
されないので、以下の例ではクラス属性 ``attr`` が unpickle 化環境 で復元されないことに注意してください::

   class Foo:
       attr = 'a class attr'

   picklestring = pickle.dumps(Foo)

pickle 化可能な関数やクラスがモジュールのトップレベルで定義されて いなければならないのはこれらの制限のためです。

同様に、クラスのインスタンスが pickle 化された際、そのクラスの コードおよびデータはオブジェクトと一緒に pickle 化されることは
ありません。インスタンスのデータのみが pickle 化されます。 この仕様は、クラス内のバグを修正したりメソッドを追加した後でも、
そのクラスの以前のバージョンで作られたオブジェクトを読み出せるように 意図的に行われています。あるクラスの多くのバージョンで使われる
ような長命なオブジェクトを作ろうと計画しているなら、 そのクラスの :meth:`__setstate__` メソッドによって適切な変換が
行われるようにオブジェクトのバージョン番号を入れておくとよいかも しれません。


.. _pickle-protocol:

pickle 化プロトコル
-------------

この節では pickler/unpickler と直列化対象のオブジェクトとの間の インタフェースを定義する "pickle 化プロトコル"
について記述します。 このプロトコルは自分のオブジェクトがどのように直列化されたり非直列化 されたりするかを定義し、カスタマイズし、制御するための標準的な方法を
提供します。この節での記述は、unpickle 化環境を不信な pickle 化データ に対して安全にするために使う特殊なカスタマイズ化についてはカバー
していません; 詳細は  :ref:`pickle-sub` を参照してください。


.. _pickle-inst:

通常のクラスインスタンスの pickle 化および unpickle 化
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   single: __getinitargs__() (copy protocol)
   single: __init__() (instance constructor)
   single: __getnewargs__() (copy protocol)

pickle 化されたクラスインスタンスが unpickle 化されたとき、 :meth:`__init__` メソッドは通常呼び出され*ません* 。
unpickle 化の際に :meth:`__init__` が呼び出される方が望ましい場合、 旧スタイルクラスではメソッド
:meth:`__getinitargs__` を定義することが できます。このメソッドはクラスコンストラクタ (例えば :meth:`__init__`)
に渡されるべき *タプルを* 返さなければなりません。 :meth:`__getinitargs__` メソッドは pickle 時に呼び出されます;
この関数が返すタプルはインスタンスの pickle 化データに組み込まれます。

新スタイルクラスでは、プロトコル 2 で呼び出される :meth:`__getnewargs__` を定義する事ができます。インスタンス生成時に内
部的な不変条件が成立する必要があったり、（タプルや文字列のように）型の :meth:`__new__`メソッドに指定する引数によってメモリの割り当てを変更す
る必要がある場合には:meth:`__getnewargs__`を定義してください。新スタ
イルクラス:class:`C`のインスタンスは、次のように生成されます。 ::

   obj = C.__new__(C, \*args)


ここで*args*は元のオブジェクトの:meth:`__getnewargs__`メソッドを
呼び出した時の戻り値となります。:meth:`__getnewargs__`を定義していな い場合、*args*は空のタプルとなります。

.. index::
   single: __getstate__() (copy protocol)
   single: __setstate__() (copy protocol)
   single: __dict__ (instance attribute)

クラスは、インスタンスの pickle 化方法にさらに影響を与えることが できます; クラスが :meth:`__getstate__` メソッドを定義している
場合、このメソッドが呼び出され、返された状態値はインスタンスの内容 として、インスタンスの辞書の代わりに pickle 化されます。
:meth:`__getstate__` メソッドが定義されていない場合、 インスタンスの :attr:`__dict__` の内容が pickle
化されます。

unpickle 化では、クラスが :meth:`__setstate__` も定義していた 場合、unpickle 化された状態値とともに呼び出されます
[#]_。:meth:`__setstate__` メソッドが定義 されていない場合、pickle 化された状態は辞書型でなければならず、
その要素は新たなインスタンスの辞書に代入されます。クラスが :meth:`__getstate__` と :meth:`__setstate__`
の両方を定義して いる場合、状態値オブジェクトは辞書である必要はなく、これらのメソッド は期待通りの動作を行います。  [#]_

.. warning::

   新しいスタイルのクラスにおいて :meth:`__getstate__` が負値を返す場合、:meth:`__setstate__` メソッドは呼ばれません。


拡張型の pickle 化および unpickle 化
^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`Pickler` が全く未知の型の --- 拡張型のような --- オブジェクトに 遭遇した場合、pickle 化方法のヒントとして 2
個所を探します。 第一は :meth:`__reduce__` メソッドを実装しているかどうかです。 もし実装されていれば、pickle 化時に
:meth:`__reduce__` メソッド が引数なしで呼び出されます。メソッドはこの呼び出しに対して 文字列またはタプルのどちらかを返さねばなりません。

文字列を返す場合、その文字列は通常通りに pickle 化されるグローバル変数 の名前を指しています。:meth:`__reduce__` の返す文字列は、
モジュールにからみてオブジェクトのローカルな名前でなければなりません; pickle モジュールはモジュールの名前空間を検索して、オブジェクトの
属するモジュールを決定します。

タプルを返す場合、タプルの要素数は 2 から 5 でなければなりません。 オプションの要素は省略したり ``None`` を指定したりできます。
各要素の意味づけは以下の通りです:

* 呼び出し可能なオブジェクトで、unpickle 化環境において、クラスか、 "安全なコンストラクタ (safe constructor)"
  (下を参照してください) として登録 されているか、属性 :attr:`__safe_for_unpickling__` を持ち値が真に
  設定されているような呼び出し可能なオブジェクトでなければなりません。 そうでない場合、 unpickle 化環境で :exc:`UnpicklingError`
  が 送出されます。通常通り、呼び出しオブジェクト自体はその名前が pickle 化されます。

* オブジェクトの初期バージョンを生成するために呼び出される 呼び出し可能オブジェクトです。この呼び出し可能オブジェクトへの引数
  はタプルの次の要素で与えられます。それ以降の要素では pickle 化されたデータを完全に再構築するために使われる付加的な状態情報 が与えられます。

  逆 pickle 化の環境下では、このオブジェクトはクラスか、 "安全なコンストラクタ (safe constructor, 下記参照)" として登録
  されていたり属性:attr:`__safe_for_unpickling__` の値が真であるような 呼び出し可能オブジェクトでなければなりません。
  そうでない場合、逆 pickle 化を行う環境で:exc:`UnpicklingError` が送出されます。通常通り、 callable は名前だけで
  pickle 化されるので 注意してください。

* 呼び出し可能なオブジェクトのための引数からなるタプル

  .. versionchanged:: 2.5
     以前は、この引数には ``None`` もあり得ました。.

* オプションとして、オブジェクトの状態。 :ref:`pickle-inst` 節で記述されているようにして、オブジェクトの
  :meth:`__setstate__` メソッドに渡されます。オブジェクトが :meth:`__setstate__` メソッドを持たない場合、上記のように、
  この値は辞書でなくてはならず、オブジェクトの :attr:`__dict__` に追加されます。

* オプションとして、リスト中の連続する要素を返すイテレータ (シーケンスではありません)。このリストの要素は pickle 化され、
  ``obj.append(item)`` または ``obj.extend(list_of_items)``
  のいずれかを使って追加されます。主にリストのサブクラスで用いられて いますが、他のクラスでも、適切なシグネチャの :meth:`append` や
  :meth:`extend` を備えている限り利用できます。 (:meth:`append` と:meth:`extend` のいずれを使うかは、
  どのバージョンの pickle プロトコルを使っているか、そして追加する 要素の数で決まります。従って両方のメソッドをサポートしていなければ なりません。)

*

* オプションとして、辞書中の連続する要素を返すイテレータ (シーケンスではありません)。このリストの要素は ``(key, value)``
  という形式でなければなりません。要素は pickle 化され、 ``obj[key] = value`` を使ってオブジェクトに格納
  されます。主に辞書のサブクラスで用いられていますが、他のクラスでも、 :meth:`__setitem__` を備えている限り利用できます。

.. % % unpickle 化の際、(上の条件に合致する場合) 呼び出し可能
.. % % オブジェクトは引数のタプルを渡して呼び出されます; オブジェクトは
.. % % unpickle 化されたオブジェクトを返さなくてはなりません。
.. % % タプルの二つ目の要素が \code{None} だった場合、呼び出し可能
.. % % オブジェクトを直接呼び出す代わりに、オブジェクトの
.. % % \method{__basicnew__()} メソッドが引数なしで呼び出されます。
.. % % オブジェクトは同様に unpickle 化されたオブジェクトを返さなければ
.. % % なりません。

.. deprecated:: 2.3
   引数のタプルを使ってください。

:meth:`__reduce__` を実装する場合、プロトコルのバージョンを 知っておくと便利なことがあります。これは :meth:`__reduce__`
の 代わりに:meth:`__reduce_ex__` を使って実現できます。 :meth:`__reduce_ex__` が定義されている場合、
:meth:`__reduce__` よりも優先して呼び出されます (以前のバージョンとの互換性のために :meth:`__reduce__`
を残しておいてもかまいません)。 :meth:`__reduce_ex__` はプロトコルのバージョンを表す 整数の引数を一つ伴って呼び出されます。

:class:`object` クラスでは :meth:`__reduce__` と :meth:`__reduce_ex__`
の両方を定義しています。とはいえ、 サブクラスで :meth:`__reduce__` をオーバライドしており、 :meth:`__reduce_ex__`
をオーバライドしていない場合には、 :meth:`__reduce_ex__` の実装がそれを検出して :meth:`__reduce__`
を呼び出すようになっています。

pickle 化するオブジェクト上で :meth:`__reduce__` メソッドを実装 する代わりに、:mod:`copy_reg` モジュールを使って
呼び出し可能オブジェクトを登録する方法もあります。このモジュール はプログラムに "縮小化関数 (reduction function)" と
ユーザ定義型のためのコンストラクタを登録する方法を提供します。 縮小化関数は、単一の引数として pickle 化するオブジェクトをとる ことを除き、上で述べた
:meth:`__reduce__` メソッドと同じ意味 とインタフェースを持ちます。

登録されたコンストラクタは上で述べたような unpickle 化については "安全なコンストラクタ" であると考えられます。


外部オブジェクトの pickle 化および unpickle 化
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

オブジェクトの永続化を便利にするために、:mod:`pickle` は pickle 化されたデータ列上にないオブジェクトに対して参照を
行うという概念をサポートしています。これらのオブジェクトは "永続化 id (persistent id)" で参照されており、この id は 単に印字可能な
ASCII 文字からなる任意の文字列です。 これらの名前の解決方法は :mod:`pickle` モジュールでは定義されて いません;
オブジェクトはこの名前解決を pickler および unpickler 上のユーザ定義関数にゆだねます  [#]_ 。

外部永続化 id の解決を定義するには、pickler オブジェクトの :attr:`persistent_id` 属性と、 unpickler オブジェクトの
:attr:`persistent_load` 属性を設定する必要があります。

外部永続化 id を持つオブジェクトを pickle 化するには、pickler は自作の :func:`persistent_id` メソッドを
持たなければなりません。このメソッドは一つの引数をとり、 ``None`` とオブジェクトの永続化 id のうちどちらかを
返さなければなりません。``None`` が返された場合、 pickler は単にオブジェクトを通常のように pickle 化するだけ です。永続化 id
文字列が返された場合、 piclkler はその 文字列に対して、、unpickler がこの文字列を永続化 id として 認識できるように、マーカと共に
pickle 化します。

外部オブジェクトを unpickle 化するには、unpickler は自作の :func:`persistent_load` 関数を持たなければなりません。
この関数は永続化 id 文字列を引数にとり、参照されているオブジェクト を返します。

*多分* より理解できるようになるようなちょっとした 例を以下に示します::

   import pickle
   from cStringIO import StringIO

   src = StringIO()
   p = pickle.Pickler(src)

   def persistent_id(obj):
       if hasattr(obj, 'x'):
           return 'the value %d' % obj.x
       else:
           return None

   p.persistent_id = persistent_id

   class Integer:
       def __init__(self, x):
           self.x = x
       def __str__(self):
           return 'My name is integer %d' % self.x

   i = Integer(7)
   print i
   p.dump(i)

   datastream = src.getvalue()
   print repr(datastream)
   dst = StringIO(datastream)

   up = pickle.Unpickler(dst)

   class FancyInteger(Integer):
       def __str__(self):
           return 'I am the integer %d' % self.x

   def persistent_load(persid):
       if persid.startswith('the value '):
           value = int(persid.split()[2])
           return FancyInteger(value)
       else:
           raise pickle.UnpicklingError, 'Invalid persistent id'

   up.persistent_load = persistent_load

   j = up.load()
   print j

:mod:`cPickle` モジュール内では、 unpickler の :attr:`persistent_load` 属性は Python
リスト型として設定することができます。この場合、 unpickler が永続化 id に遭遇しても、永続化 id 文字列は単にリストに
追加されるだけです。この仕様は、pickle データ中の全てのオブジェクトを 実際にインスタンス化しなくても、 pickle データ列中でオブジェクトに対する
参照を "嗅ぎ回る" ことができるようにするために存在しています  [#]_。 リストに :attr:`persistent_load` を設定するやり方は、
よく Unpickler クラスの :meth:`noload` メソッドと共に使われます。

.. % BAW: Both pickle and cPickle support something called
.. % inst_persistent_id() which appears to give unknown types a second
.. % shot at producing a persistent id.  Since Jim Fulton can't remember
.. % why it was added or what it's for, I'm leaving it undocumented.
.. % \subsection{セキュリティ \label{pickle-sec}}
.. % \module{pickle} および \module{cPickle} モジュールを取り囲むセキュリティ
.. % 問題のほとんどは unpickle 化に関するものです。\module{pickle}
.. % モジュールとやり取りをするオブジェクトは (プログラマが) 制御でき、
.. % \module{pickle} は文字列を生成するので、pickle 化に関係した
.. % セキュリティ上の既知の脆弱性はありません。
.. % しかしながら、unpickle 化については、例えばソケットから読み出された
.. % 文字列のように、発信元が明らかでない信頼されない文字列を unpickle 化
.. % するのは \strong{全く} よいアイデアではありません。
.. % これは、 unpickle 化によって予期しないオブジェクトが生成される可能性
.. % があり、それらのオブジェクトのコンストラクタやデストラクタのような
.. % メソッドが呼び出される可能性さえあるからです \footnote{
.. % 特筆して警告すべきものとして、 \refmodule{Cookie} モジュール
.. % が挙げられます。標準では、 \class{Cookie.Cookie} クラスは
.. % \class{Cookie.SmartCookie} クラスの別名で、渡された cookie データ
.. % 文字列を全て unpickle 化しようと ``お世話'' します。
.. % cookie データは通常信頼されない情報源からやってくるので、
.. % これは非常に深刻なセキュリティホールになります。
.. % 明示的に \class{Cookie.SimpleCookie} クラス --- このクラスは文字列を
.. % unpickle 化しようとはしません --- を明示的に使うか、この節で後に
.. % 述べている防衛性のあるプログラムステップの実装を行ってください。}。
.. % 何が unpickle 化され、どの呼び出し可能オブジェクトが呼び出される
.. % かを制御するように unpickle をカスタマイズすることで、この脆弱性を
.. % 防御することができます。不幸なことに、この防御をどうやって行うかは
.. % 使っているのが \module{pickle} か \module{cPickle} かによって
.. % 異なります。
.. % 両方のモジュールにおける実装で共通な仕様の一つは
.. % \member{__safe_for_unpickling__} 属性です。
.. % クラスでない呼び出し可能オブジェクトを呼び出す前に、 unpickler
.. % は呼び出し可能オブジェクトが \refmodule[copyreg]{copy_reg} モジュール
.. % を介して安全な呼び出し可能オブジェクトとして登録されているか、
.. % または \member{__safe_for_unpickling__} 属性が真に設定されている
.. % かを調べます。これにより、unpickle 化環境で
.. % 任意のファイル名に対して \code{os.unlink()} を呼び出すといった、
.. % 邪悪な行いを仕掛けられないようにできます。詳しくは
.. % \ref{pickle-protocol} を参照してください。
.. % クラスのインスタンスを安全に unpickle 化するためには、どのクラスを
.. % 生成するのかを厳密に制御する必要があります。クラスのコンストラクタ
.. % は呼び出されうる  (pickler が \method{__getinitargs__()} メソッドを
.. % 発見した場合) こと、そしてデストラクタもオブジェクトが
.. % ガーベジコレクションされる際に呼び出される可能性がある
.. % (つまり \method{__del__()} メソッド) ことに注意してください。
.. % クラスによっては、これらのメソッドを悪用してファイルを削除すると
.. % いったことは難しくありません。


.. _pickle-sub:

Unpickler をサブクラス化する
-------------------

デフォルトでは、逆 pickle 化は pickle 化されたデータ中に見つかった クラスを import することになります。自前の unpickler
をカスタマイズ することで、何が unpickle 化されて、どのメソッドが呼び出されるか を厳密に制御することはできます。しかし不運なことに、厳密に
なにを行うべきかは:mod:`pickle`  と :mod:`cPickle` のどちらを使うかで異なります  [#]_。

:mod:`pickle` モジュールでは、:class:`Unpickler` からサブクラスを 導出し、:meth:`load_global`
メソッドを上書きする必要があります。 :meth:`load_global` は pickle データ列から最初の 2 行を読まなければ
ならず、ここで最初の行はそのクラスを含むモジュールの名前、2 行目は そのインスタンスのクラス名になるはずです。
次にこのメソッドは、例えばモジュールをインポートして属性を掘り起こす などしてクラスを探し、発見されたものを unpickler のスタックに置きます。
その後、このクラスは空のクラスの :attr:`__class__` 属性に代入する 方法で、クラスの :meth:`__init__`
を使わずにインスタンスを魔法のように 生成します。 あなたの作業は (もしその作業を受け入れるなら)、unpickler のスタックの 上に push された
:meth:`load_global` を、unpickle しても安全だと 考えられる何らかのクラスの既知の安全なバージョンにすることです。
あるいは全てのインスタンスに対して unpickling を許可したくないなら エラーを送出してください。このからくりがハックのように
思えるなら、あなたは間違っていません。このからくりを動かすには、 ソースコードを参照してください。

:mod:`cPickle` では事情は多少すっきりしていますが、十分という わけではありません。何を unpickle 化するかを制御するには、
unpickler の :attr:`find_global` 属性を関数か ``None`` に 設定します。属性が ``None`` の場合、インスタンスを
unpickle  しようとする試みは全て :exc:`UnpicklingError` を送出します。
属性が関数の場合、この関数はモジュール名またはクラス名を 受理し、対応するクラスオブジェクトを返さなくてはなりません。
このクラスが行わなくてはならないのは、クラスの探索、必要な import のやり直しです。そしてそのクラスのインスタンスが unpickle
化されるのを防ぐためにエラーを送出することもできます。

以上の話から言えることは、アプリケーションが unpickle 化する 文字列の発信元については非常に高い注意をはらわなくてはならないと いうことです。


.. _pickle-example:

例
-

いちばん単純には、:func:`dump` と :func:`load` を 使用してください。自己参照リストが正しく pickle 化およびリストアされる
ことに注目してください。 ::

   import pickle

   data1 = {'a': [1, 2.0, 3, 4+6j],
            'b': ('string', u'Unicode string'),
            'c': None}

   selfref_list = [1, 2, 3]
   selfref_list.append(selfref_list)

   output = open('data.pkl', 'wb')

   # Pickle dictionary using protocol 0.
   pickle.dump(data1, output)

   # Pickle the list using the highest protocol available.
   pickle.dump(selfref_list, output, -1)

   output.close()

以下の例は pickle 化された結果のデータを読み込みます。 pickle を含むデータを読み込む場合、ファイルはバイナリモードで
オープンしなければいけません。これは ASCII 形式とバイナリ形式の どちらが使われているかは分からないからです。 ::

   import pprint, pickle

   pkl_file = open('data.pkl', 'rb')

   data1 = pickle.load(pkl_file)
   pprint.pprint(data1)

   data2 = pickle.load(pkl_file)
   pprint.pprint(data2)

   pkl_file.close()

より大きな例で、クラスを pickle 化する挙動を変更するやり方を示します。 :class:`TextReader` クラスはテキストファイルを開き、
:meth:`readline` メソッドが呼ばれるたびに行番号と行の内容を 返します。:class:`TextReader` インスタンスが pickle
化された場合、 ファイルオブジェクト *以外の* 全ての属性が保存されます。 インスタンスが unpickle 化された際、ファイルは再度開かれ、
以前のファイル位置から読み出しを再開します。上記の動作を 実装するために、:meth:`__setstat__` および
:meth:`__getstate__`  メソッドが使われています。 ::

   class TextReader:
       """Print and number lines in a text file."""
       def __init__(self, file):
           self.file = file
           self.fh = open(file)
           self.lineno = 0

       def readline(self):
           self.lineno = self.lineno + 1
           line = self.fh.readline()
           if not line:
               return None
           if line.endswith("\n"):
               line = line[:-1]
           return "%d: %s" % (self.lineno, line)

       def __getstate__(self):
           odict = self.__dict__.copy() # copy the dict since we change it
           del odict['fh']              # remove filehandle entry
           return odict

       def __setstate__(self,dict):
           fh = open(dict['file'])      # reopen file
           count = dict['lineno']       # read from file...
           while count:                 # until line count is restored
               fh.readline()
               count = count - 1
           self.__dict__.update(dict)   # update attributes
           self.fh = fh                 # save the file object

使用例は以下のようになるでしょう::

   >>> import TextReader
   >>> obj = TextReader.TextReader("TextReader.py")
   >>> obj.readline()
   '1: #!/usr/local/bin/python'
   >>> # (more invocations of obj.readline() here)
   ... obj.readline()
   '7: class TextReader:'
   >>> import pickle
   >>> pickle.dump(obj,open('save.p','w'))

:mod:`pickle` が Python プロセス間でうまく働くことを見たい なら、先に進む前に他の Python セッションを開始してください。
以下の振る舞いは同じプロセスでも新たなプロセスでも起こります。 ::

   >>> import pickle
   >>> reader = pickle.load(open('save.p'))
   >>> reader.readline()
   '8:     "Print and number lines in a text file."'


.. seealso::

   Module :mod:`copy_reg`
      拡張型を登録するための Pickle インタフェース構成機構。

   Module :mod:`shelve`
      オブジェクトのインデクス付きデータベース; :mod:`pickle` を使います。

   Module :mod:`copy`
      オブジェクトの浅いコピーおよび深いコピー。

   Module :mod:`marshal`
      高いパフォーマンスを持つ組み込み型整列化機構。


:mod:`cPickle` --- より高速な :mod:`pickle`
======================================

.. module:: cPickle
   :synopsis: pickle の高速バージョンですが、サブクラスはできません。
.. moduleauthor:: Jim Fulton <jfulton@zope.com>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


.. index:: module: pickle

:mod:`cPickle` モジュールは Python オブジェクトの直列化および 非直列化をサポートし、:mod:`pickle`
モジュールとほとんど同じインタフェースと機能を提供します。 いくつか相違点がありますが、最も重要な違いはパフォーマンスと サブクラス化が可能かどうかです。

第一に、:mod:`cPickle` は C で実装されているため、:mod:`pickle`  よりも最大で 1000
倍高速です。第二に、:mod:`cPickle` モジュール 内では、呼び出し可能オブジェクト :func:`Pickler` および
:func:`Unpickler` は関数で、クラスではありません。 つまり、pickle 化や unpickle 化を行うカスタムのサブクラスを
導出することができないということです。 多くのアプリケーションではこの機能は不要なので、:mod:`cPickle`
モジュールによる大きなパフォーマンス向上の恩恵を受けられるはず です。:mod:`pickle` と :mod:`cPickle` で作られた pickle
データ列は同じなので、既存の pickle データに対して :mod:`pickle` と :mod:`cPickle` を互換に使用することができます
[#]_。

:mod:`cPickle` と :mod:`pickle` の API 間には他にも些細な相違が ありますが、ほとんどのアプリケーションで互換性があります。
より詳細なドキュメンテーションは :mod:`pickle` のドキュメント にあり、そこでドキュメント化されている相違点について挙げています。

.. rubric:: Footnotes

.. [#] :mod:`marshal` モジュールと間違えないように注意 してください

.. [#] :mod:`pickle`では、これらの呼び出し可能オブジェクトはクラスであり、 サブクラス化してその動作をカスタマイズすることができます。しかし、
   :mod:`cPickle` モジュールでは、これらの呼び出し可能オブジェクト はファクトリ関数であり、サブクラス化することができません。
   サブクラスを作成する共通の理由の一つは、どのオブジェクトを実際に unpickle するかを制御することです。詳細については
   :ref:`pickle-sub` を参照してください。

.. [#] *警告*: これは、複数のオブジェクトを pickle 化する際に、オブジェクト やそれらの一部に対する変更を妨げないようにするための仕様です。
   あるオブジェクトに変更を加えて、その後同じ :class:`Pickler` を使って 再度 pickle 化しようとしても、そのオブジェクトは pickle
   化しなおされ ません --- そのオブジェクトに対する参照が pickle 化され、:class:`Unpickler`
   は変更された値ではなく、元の値を返します。これには 2 つの問題点 : (1) 変更の検出、そして (2) 最小限の変更を整列化すること、があります。
   ガーベジコレクションもまた問題になります。

.. [#] 送出される例外は :exc:`ImportError` や :exc:`AttributeError` になるはずですが、他の例外も 起こりえます

.. [#] これらのメソッドはクラスインスタンスのコピーを 実装する際にもｔ用いられます

.. [#] このプロトコルはまた、 :mod:`copy` で定義されている浅いコピーや深いコピー操作でも用いら れます。

.. [#] ユーザ定義関数に関連付けを行うための実際のメカニズムは、 :mod:`pickle` および :mod:`cPickle` では少し異なります。
   :mod:`pickle` のユーザは、サブクラス化を行い、 :meth:`persistend_id` および :meth:`persistent_load`
   メソッドを上書きすることで同じ効果を得ることができます

.. [#] Guide と Jim が居間に座り込んでピクルス (pickles) を 嗅いでいる光景を想像してください。

.. [#] 注意してください: ここで記述されている機構は内部の属性とメソッドを 使っており、これらはPython の将来のバージョンで変更される対象に
   なっています。われわれは将来、この挙動を制御するための、 :mod:`pickle` および :mod:`cPickle` の両方で動作する、
   共通のインタフェースを提供するつもりです。

.. [#] pickle データ形式は実際には小規模なスタック指向のプログラム 言語であり、またあるオブジェクトをエンコードする際に多少の自由度が
   あるため、二つのモジュールが同じ入力オブジェクトに対して異なる データ列を生成することもあります。しかし、常に互いに他のデータ列
   を読み出せることが保証されています。

