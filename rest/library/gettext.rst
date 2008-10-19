
:mod:`gettext` --- 多言語対応に関する国際化サービス
===================================

.. module:: gettext
   :synopsis: 多言語対応に関する国際化サービス。
.. moduleauthor:: Barry A. Warsaw <barry@zope.com>
.. sectionauthor:: Barry A. Warsaw <barry@zope.com>


:mod:`gettext` モジュールは、 Python によるモジュールや アプリケーションの国際化 (I18N,
I-nternationalizatio-N) および地域化  (L10N, L-ocalizatio-N) サービスを提供します。 このモジュールは GNU
``gettext`` メッセージカタログへの API と、 より高レベルで Python ファイルに適しているクラスに基づいた API の
両方をサポートしてます。以下で述べるインタフェースを使うことで、 モジュールやアプリケーションのメッセージをある自然言語で記述しておき、
翻訳されたメッセージのカタログを与えて他の異なる自然言語の環境下で動作 させることができます。

ここでは Python のモジュールやアプリケーションを地域化する ためのいくつかのヒントも提供しています。


GNU :program:`gettext` API
--------------------------

:mod:`gettext` モジュールでは、以下の GNU :program:`gettext` API に 非常に良く似た API を提供しています。この
API を使う場合、 メッセージ翻訳の影響はアプリケーション全体に及ぼすことになります。 アプリケーションが単一の言語しか扱わず、各言語に依存する部分を
ユーザのロケール情報によって選ぶのなら、ほとんどの場合この方法で やりたいことを実現できます。Python モジュールを地域化していたり、
アプリケーションの実行中に言語を切り替えたい場合、おそらくクラス に基づいた API を使いたくなるでしょう。


.. function:: bindtextdomain(domain[, localedir])

   *domain* をロケール辞書 *localedir* に結び付け (bind) ます。 具体的には、 :mod:`gettext`
   は与えられたドメインに対する バイナリ形式の :file:`.mo` ファイルを、(Unixでは)
   :file:`localedir/language/LC_MESSAGES/domain.mo` から探します。ここで *languages*
   はそれぞれ環境変数 :envvar:`LANGUAGE`、:envvar:`LC_ALL` 、:envvar:`LC_MESSAGES`、 および
   :envvar:`LANG` の中から検索されます。

   *localedir* が省略されるか ``None`` の場合、現在 *domain* に結び付けられている内容が返されます。 [#]_


.. function:: bind_textdomain_codeset(domain[, codeset])

   *domain* を*codeset* に結び付けて、:func:`gettext`  ファミリの関数が返す文字列のエンコード方式を変更します。
   *codeset* を省略すると、現在結び付けられているコードセットを 返します。

   .. versionadded:: 2.4


.. function:: textdomain([domain])

   現在のグローバルドメインを調べたり変更したりします。 *domain* が ``None`` の場合、現在のグローバルドメインが返され
   ます。それ以外の場合にはグローバルドメインは *domain* に設定され、 設定されたグローバルドメインを返します。


.. function:: gettext(message)

   現在のグローバルドメイン、言語、およびロケール辞書に基づいて、 *message* の特定地域向けの翻訳を返します。通常、 ローカルな名前空間ではこの関数に
   :func:`_` という別名をつけます (下の例を参照してください)。


.. function:: lgettext(message)

   :func:`gettext` と同じですが、:func:`bind_textdomain_codeset`
   で特にエンコードを指定しない限り、翻訳結果を優先システムエンコーディング (preferred system encoding) で返します。

   .. versionadded:: 2.4


.. function:: dgettext(domain, message)

   :func:`gettext` と同様ですが、指定された *domain* から メッセージを探します。


.. function:: ldgettext(message)

   :func:`dgettext` と同じですが、:func:`bind_textdomain_codeset`
   で特にエンコードを指定しない限り、翻訳結果を優先システムエンコーディング (preferred system encoding) で返します。

   .. versionadded:: 2.4


.. function:: ngettext(singular, plural, n)

   :func:`gettext` と同様ですが、複数形の場合を考慮しています。 翻訳文字列が見つかった場合、*n* の様式を適用し、
   その結果得られたメッセージを返します (言語によっては二つ以上の 複数形があります)。 翻訳文字列が見つからなかった場合、 *n* が 1 なら
   *singular* を返します; そうでない場合 *plural* を返します。

   複数形の様式はカタログのヘッダから取り出されます。様式は C または Python の式で、自由な変数 n を持ちます; 式の評価値はカタログ中の
   複数形のインデクスとなります。.po ファイルで用いられる 詳細な文法と、様々な言語における様式については、GNU gettext
   ドキュメントを参照してください。

   .. versionadded:: 2.3


.. function:: lngettext(message)

   :func:`ngettext` と同じですが、:func:`bind_textdomain_codeset`
   で特にエンコードを指定しない限り、翻訳結果を優先システムエンコーディング (preferred system encoding) で返します。

   .. versionadded:: 2.4


.. function:: dngettext(domain, singular, plural, n)

   :func:`ngettext` と同様ですが、指定された *domain* から メッセージを探します。

   .. versionadded:: 2.3


.. function:: ldngettext(message)

   :func:`dngettext` と同じですが、:func:`bind_textdomain_codeset`
   で特にエンコードを指定しない限り、翻訳結果を優先システムエンコーディング (preferred system encoding) で返します。

   .. versionadded:: 2.4

GNU :program:`gettext` では :func:`dcgettext` も定義していますが、
このメソッドはあまり有用ではないと思われるので、現在のところ 実装されていません。

以下にこの API の典型的な使用法を示します::

   import gettext
   gettext.bindtextdomain('myapplication', '/path/to/my/language/directory')
   gettext.textdomain('myapplication')
   _ = gettext.gettext
   # ...
   print _('This is a translatable string.')


クラスに基づいた API
------------

クラス形式の :mod:`gettext` モジュールのAPI は GNU :program:`gettext` API
よりも高い柔軟性と利便性を持っています。 Python のアプリケーションやモジュールを地域化するにはこちらを使う 方を勧めます。:mod:`gettext`
では、GNU :file:`.mo` 形式のファイルを 解釈し、標準の 8 ビット文字列または Unicode 文字列形式でメッセージ を返す "翻訳"
クラスを定義しています。 この "翻訳" クラスのインスタンスも、組み込み名前空間に関数  :func:`_` として組みこみ (install) できます。


.. function:: find(domain[, localedir[,  languages[, all]]])

   この関数は標準的な :file:`.mo` ファイル検索アルゴリズムを実装 しています。:func:`textdomain` と同じく、*domain*
   を引数に とります。オプションの *localedir* は :func:`bindtextdomain` と同じです。またオプションの *languages*
   は文字列を列挙したリスト で、各文字列は言語コードを表します。

   *localedir* が与えられていない場合、標準のシステムロケール ディレクトリが使われます。 [#]_

   *languages* が与えられなかった場合、以下の環境変数: :envvar:`LANGUAGE`、:envvar:`LC_ALL`、
   :envvar:`LC_MESSAGES`、および :envvar:`LANG` が検索されます。空でない値を返した最初の候補が *languages*
   変数として使われます。 この環境変数は言語名をコロンで分かち書きしたリストを含んで いなければなりません。:func:`find` はこの文字列をコロンで
   分割し、言語コードの候補リストを生成します。

   :func:`find` は次に言語コードを展開および正規化し、リストの 各要素について、以下のパス構成:

   :file:`localedir/language/LC_MESSAGES/domain.mo`

   からなる実在するファイルの探索を反復的に行います。:func:`find`  は上記のような実在するファイルで最初に見つかったものを返します。
   該当するファイルが見つからなかった場合、``None`` が返されます。 *all* が与えられていれば、全ファイル名のリストが言語リストまたは
   環境変数で指定されている順番に並べられたものを返します。


.. function:: translation(domain[, localedir[, languages[, class_[, fallback[, codeset]]]]])

   :class:`Translations` インスタンスを *domain*、*localedir*、および *languages* に基づいて
   生成して返します。 *domain*、*localedir*、および *languages* はまず 関連付けられている :file:`.mo`
   ファイルパスのリストを取得する ために:func:`find` に渡されます。同じ :file:`.mo` ファイル名を
   持つインスタンスはキャッシュされます。実際にインスタンス化される クラスは *class_* が与えられていればそのクラスが、そうでない 時には
   :class:`GNUTranslations` です。クラスのコンストラクタは 単一の引数としてファイルオブジェクトを取らなくてはなりません。
   *codeset* を指定した場合、翻訳文字列のエンコードに使う 文字セットを変更します。

   複数のファイルが発見された場合、後で見つかったファイルは前に見つかった ファイルの代替でと見なされ、後で見つかった方が利用されます。
   代替の設定を可能にするには、:func:`copy.copy` を使ってキャッシュから 翻訳オブジェクトを複製します;
   こうすることで、実際のインスタンスデータは キャッシュのものと共有されます。

   :file:`.mo` ファイルが見つからなかった場合、*fallback* が偽 (標準の設定です) ならこの関数は :exc:`IOError` を送出し、
   *fallback* が真なら :class:`NullTranslations` インスタンスが 返されます。

   .. versionchanged:: 2.4
      *codeset* パラメタを追加しました.


.. function:: install(domain[, localedir[, unicode [, codeset[, names]]]])

   :func:`translation` に*domain*、 *localedir*、 および*codeset* を渡してできる関数 :func:`_` を
   Python の組み込み名前空間に組み込みます。 *unicode* フラグは :func:`translation` の返す翻訳オブジェクト の
   :meth:`install` メソッドに渡されます。

   *names* パラメタについては、翻訳オブジェクトの :meth:`install` メソッドの説明を参照ください。

   以下に示すように、通常はアプリケーション中の文字列を関数 :func:`_`  の呼び出しで包み込んで翻訳対象候補であることを示します::

      print _('This string will be translated.')

   利便性を高めるためには、:func:`_` 関数を Python の組み込み 名前空間に組み入れる必要があります。こうすることで、アプリケーション内の
   全てのモジュールからアクセスできるようになります。

   .. versionchanged:: 2.4
      *codeset* パラメタを追加しました.

   .. versionchanged:: 2.5
      *names* パラメタを追加しました.


:class:`NullTranslations` クラス
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

翻訳クラスは、元のソースファイル中のメッセージ文字列から 翻訳されたメッセージ文字列への変換を実際に実装しているクラスです。
全ての翻訳クラスが基底クラスとして用いるクラスが :class:`NullTranslations` です; このクラスでは独自の特殊な翻訳
クラスを実装するために使うことができる基本的なインタフェースを 以下に :class:`NullTranslations` のメソッドを示します:


.. method:: NullTranslations.__init__([fp])

   オプションのファイルオブジェクト *fp* を取ります。この引数 は基底クラスでは無視されます。このメソッドは  "保護された (protected)"
   インスタンス変数 *_info* および  *_charset* を初期化します。これらの変数の値は導出クラスで設定 することができます。同様に
   *_fallback* も初期化しますが、 この値は :meth:`add_fallback` で設定されます。その後、 *fp* が ``None``
   でない場合 ``self._parse(fp)`` を 呼び出します。


.. method:: NullTranslations._parse(fp)

   基底クラスでは何もしない (no-op) ようになっています。このメソッド の役割はファイルオブジェクト *fp* を引数に取り、ファイルからデータを
   読み出し、メッセージカタログを初期化することです。サポートされていない メッセージカタログ形式を使っている場合、その形式を解釈するためには
   このメソッドを上書きしなくてはなりません。


.. method:: NullTranslations.add_fallback(fallback)

   *fallback* を現在の翻訳オブジェクトの代替オブジェクトとして追加 します。翻訳オブジェクトが与えられたメッセージに対して翻訳メッセージ
   を提供できない場合、この代替オブジェクトに問い合わせることになります。


.. method:: NullTranslations.gettext(message)

   代替オブジェクトが設定されている場合、:meth:`gettext` を代替オブジェクト に転送します。そうでない場合、翻訳されたメッセージを返します。
   導出クラスで上書きするメソッドです。


.. method:: NullTranslations.lgettext(message)

   代替オブジェクトが設定されている場合、:meth:`lgettext` を代替オブジェクト に転送します。そうでない場合、翻訳されたメッセージを返します。
   導出クラスで上書きするメソッドです。

   .. versionadded:: 2.4


.. method:: NullTranslations.ugettext(message)

   代替オブジェクトが設定されている場合、:meth:`gettext` を代替オブジェクト に転送します。そうでない場合、翻訳されたメッセージを Unicode
   文字列 で返します。導出クラスで上書きするメソッドです。


.. method:: NullTranslations.ngettext(singular, plural, n)

   代替オブジェクトが設定されている場合、:meth:`ngettext` を代替オブジェクト に転送します。そうでない場合、翻訳されたメッセージを返します。
   導出クラスで上書きするメソッドです。

   .. versionadded:: 2.3


.. method:: NullTranslations.lngettext(singular, plural, n)

   代替オブジェクトが設定されている場合、:meth:`lngettext` を代替オブジェクト に転送します。そうでない場合、翻訳されたメッセージを返します。
   導出クラスで上書きするメソッドです。

   .. versionadded:: 2.4


.. method:: NullTranslations.ungettext(singular, plural, n)

   代替オブジェクトが設定されている場合、:meth:`ungettext` を代替オブジェクト に転送します。そうでない場合、翻訳されたメッセージを
   Unicode 文字列 で返します。導出クラスで上書きするメソッドです。

   .. versionadded:: 2.3


.. method:: NullTranslations.info()

   "protected" の:attr:`_info` 変数を返します。


.. method:: NullTranslations.charset()

   "protected" の:attr:`_charset` 変数を返します。


.. method:: NullTranslations.output_charset()

   翻訳メッセージとして返す文字列のエンコードを決める、 "protected" の:attr:`_output_charset` 変数を返します。

   .. versionadded:: 2.4


.. method:: NullTranslations.set_output_charset(charset)

   翻訳メッセージとして返す文字列のエンコードを決める、 "protected" の変数 :attr:`_output_charset` を変更します。

   .. versionadded:: 2.4


.. method:: NullTranslations.install([unicode [, names]])

   *unicode* フラグが偽の場合、このメソッドは :meth:`self.gettext` を組み込み名前空間に組み入れ、``_`` と結び付けます。
   *unicode* が真の場合、:meth:`self.gettext` の代わりに :meth:`self.ugettext` を結び付けます。 標準では
   *unicode* は偽です。

   *names* パラメタには、:func:`_` 以外に組み込みの名前空間に インストールしたい関数名のシーケンスを指定します。サポートしている名前は
   ``'gettext'`` (*unicode* フラグの設定に応じて :meth:`self.gettext` あるいは
   :meth:`self.ugettext` のいずれかに対応します)、 ``'ngettext'`` (*unicode* フラグの設定に応じて
   :meth:`self.ngettext` あるいは :meth:`self.ungettext` のいずれかに対応します)、 ``'lgettext'``
   および ``'lngettext'`` です。

   この方法はアプリケーションで :func:`_` 関数を利用できるようにする ための最も便利な方法ですが、唯一の手段でもあるので注意してください。
   この関数はアプリケーション全体、とりわけ組み込み名前空間に影響する ので、地域化されたモジュールで :func:`_` を組み入れることが
   できないのです。その代わりに、以下のコード::

      import gettext
      t = gettext.translation('mymodule', ...)
      _ = t.gettext

   を使って :func:`_` を使えるようにしなければなりません。

   この操作は :func:`_` をモジュール内だけのグローバル名前空間に 組み入れるので、モジュール内の :func:`_` の呼び出しだけに影響 します。

   .. versionchanged:: 2.5
      *names* パラメタを追加しました.


:class:`GNUTranslations` クラス
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`gettext` モジュールでは :class:`NullTranslations` から 導出されたもう一つのクラス:
:class:`GNUTranslations` を提供しています。 このクラスはビッグエンディアン、およびリトルエンディアン両方の バイナリ形式の GNU
:program:`gettext` :file:`.mo` ファイル を読み出せるように :meth:`_parse` を上書きしています。
また、このクラスはメッセージ id とメッセージ文字列の両方を Unicode に型強制します。

このクラスではまた、翻訳カタログ以外に、オプションのメタデータ を読み込んで解釈します。GNU :program:`gettext` では、空の文字列に
対する変換先としてメタデータを取り込むことが慣習になっています。 このメタデータは :rfc:`822` 形式の ``key: value`` のペアに
なっており、 ``Project-Id-Version`` キーを含んでいなければ なりません。キー ``Content-Type`` があった場合、
``charset`` の特性値 (property) は "保護された" :attr:`_charset` インスタンス
変数を初期化するために用いられます。値がない場合には、デフォルトと して ``None`` が使われます。
エンコードに用いられる文字セットが指定されている場合、カタログから 読み出された全てのメッセージ id とメッセージ文字列は、指定された エンコードを用いて
Unicode に変換されます。:meth:`ugettext` は常に Unicode を返し、:meth:`gettext` はエンコードされた 8
ビット文字列を返します。どちらのメソッドにおける引数 id の 場合も、Unicode 文字列か US-ASCII 文字のみを含む 8 ビット文字列
だけが受理可能です。国際化されたPython プログラムでは、メソッドの Unicode 版 (すなわち :meth:`ugettext` や
:meth:`ungettext`) の利用が推奨されています。

key/value ペアの集合全体は辞書型データ中に配置され、"保護された"  :attr:`_info` インスタンス変数に設定されます。

:file:`.mo` ファイルのマジックナンバーが不正な場合、あるいは その他の問題がファイルの読み出し中に発生した場合、
:class:`GNUTranslations` クラスのインスタンス化で :exc:`IOError` が送出されることがあります。

以下のメソッドは基底クラスの実装からオーバライドされています:


.. method:: GNUTranslations.gettext(message)

   カタログから *message* id を検索して、対応するメッセージ文字列を、 カタログの文字セットが既知のエンコードの場合、エンコードされた 8 ビット
   文字列として返します。*message* id に対するエントリがカタログに 存在せず、フォールバックが設定されている場合、フォールバック 検索はオブジェクトの
   :meth:`gettext` メソッドに転送されます。 そうでない場合、*message* id 自体が返されます。


.. method:: GNUTranslations.ugettext(message)

   カタログから *message* id を検索して、対応するメッセージ文字列を、 Unicode でエンコードして返します。*message* id
   に対するエントリが カタログに存在せず、フォールバックが設定されている場合、フォールバック 検索はオブジェクトの :meth:`ugettext`
   メソッドに転送されます。 そうでない場合、*message* id 自体が返されます。


.. method:: GNUTranslations.ngettext(singular, plural, n)

   メッセージ id に対する複数形を検索します。カタログに対する検索では *singular* がメッセージ id として用いられ、 *n* には
   どの複数形を用いるかを指定します。返されるメッセージ文字列は 8 ビットの文字列で、カタログの文字セットが既知の場合にはその
   文字列セットでエンコードされています。

   メッセージ id がカタログ中に見つからず、フォールバックオブジェクト が指定されている場合、メッセージ検索要求はフォールバックオブジェクトの
   :meth:`ngettext` メソッドに転送されます。そうでない場合、 *n* が 1 ならば *singular* が返され、それ以外に対しては
   *plural* が返されます。

   .. versionadded:: 2.3


.. method:: GNUTranslations.ungettext(singular, plural, n)

   メッセージ id に対する複数形を検索します。カタログに対する検索では *singular* がメッセージ id として用いられ、 *n* には
   どの複数形を用いるかを指定します。返されるメッセージ文字列は Unicode 文字列です。

   メッセージ id がカタログ中に見つからず、フォールバックオブジェクト が指定されている場合、メッセージ検索要求はフォールバックオブジェクトの
   :meth:`ungettext` メソッドに転送されます。そうでない場合、 *n* が 1 ならば *singular* が返され、それ以外に対しては
   *plural* が返されます。

   以下に例を示します。::

      n = len(os.listdir('.'))
      cat = GNUTranslations(somefile)
      message = cat.ungettext(
          'There is %(num)d file in this directory',
          'There are %(num)d files in this directory',
          n) % {'num': n}

   .. versionadded:: 2.3


Solaris メッセージカタログ機構のサポート
^^^^^^^^^^^^^^^^^^^^^^^^

Solaris オペレーティングシステムでは、独自の :file:`.mo`  バイナリファイル形式を定義していますが、この形式に関する
ドキュメントが手に入らないため、現時点ではサポートされていません。


Catalog コンストラクタ
^^^^^^^^^^^^^^^

.. index:: single: GNOME

GNOME では、James Henstridge によるあるバージョンの :mod:`gettext` モジュールを使っていますが、このバージョンは
少し異なった API を持っています。ドキュメントに書かれている 利用法は::

   import gettext
   cat = gettext.Catalog(domain, localedir)
   _ = cat.gettext
   print _('hello world')

となっています。過去のモジュールとの互換性のために、 :func:`Catalog` は前述の :func:`translation`
関数の別名になっています。

このモジュールと Henstridge のバージョンとの間には一つ相違点が あります: 彼のカタログオブジェクトはマップ型の API を介した
アクセスがサポートされていましたが、この API は使われていない らしく、現在はサポートされていません。


プログラムやモジュールを国際化する
-----------------

国際化 (I18N, I-nternationalizatio-N) とは、プログラムを複数の言語に 対応させる操作を指します。地域化 (L10N,
L-ocalizatio-N) とは、すでに 国際化されているプログラムを特定地域の言語や文化的な事情に対応させる ことを指します。Python
プログラムに多言語メッセージ機能を追加するには、 以下の手順を踏む必要があります:

#. プログラムやモジュールで翻訳対象とする文字列に特殊なマークを つけて準備します

#. マークづけをしたファイルに一連のツールを走らせ、生のメッセージ カタログを生成します

#. 特定の言語へのメッセージカタログの翻訳を作成します

#. メッセージ文字列を適切に変換するために :mod:`gettext` モジュールを使います

ソースコードを I18N 化する準備として、ファイル内の全ての文字列 を探す必要があります。翻訳を行う必要のある文字列はどれも ``_('...')`` ---
すなわち関数 :func:`_` の呼び出しで 包むことでマーク付けしなくてはなりません。例えば以下のようにします::

   filename = 'mylog.txt'
   message = _('writing a log message')
   fp = open(filename, 'w')
   fp.write(message)
   fp.close()

この例では、文字列 ``'writing a log message'`` が翻訳対象候補として マーク付けされており、文字列 ``'mylog.txt'``
および ``'w'`` は されていません。

Python の配布物には、ソースコードに準備作業を行った後で メッセージカタログの生成を助ける 2 つのツールが付属します。
これらはバイナリ配布の場合には付属していたりしなかったりしますが、 ソースコード配布には入っており、:file:`Tools/i18n` ディレクトリ
にあります。

:program:`pygettext` プログラム  [#]_  は全ての Python ソースコードを走査し、予め翻訳対象としてマーク
した文字列を探し出します。このツールは GNU :program:`gettext` プログラムと同様ですが、Python ソースコードの機微について
熟知している反面、C 言語や C++言語のソースコードについては 全く知りません。(C 言語による拡張モジュールのように) C 言語の
コードも翻訳対象にしたいのでない限り、 GNU ``gettext``  は必要ありません。

:program:`pygettext` は、テキスト形式 Uniforum スタイルによる人間が 判読可能なメッセージカタログ :file:`.pot`
ファイル群を生成します。 このファイル群はソースコード中でマークされた全ての文字列と、 それに対応する翻訳文字列のためのプレースホルダを含むファイル
で構成されています。 :program:`pygettext` はコマンドライン形式のスクリプトで、 :program:`xgettext`
と同様のコマンドラインインタフェースをサポート します; 使用法についての詳細を見るには::

   pygettext.py --help

を起動してください。

これら :file:`.pot` ファイルのコピーは次に、サポート対象の 各自然言語について、言語ごとのバージョンを作成する個々の人間の
翻訳者に頒布されます。翻訳者たちはプレースホルダ部分を埋めて 言語ごとのバージョンをつくり、:file:`.po` ファイルとして
返します。(:file:`Tools/i18n` ディレクトリ内の)  :program:`msgfmt.py` [#]_
プログラムを使い、翻訳者から返された :file:`.po` ファイルから 機械可読な :file:`.mo` バイナリカタログファイルを生成します。
:file:`.mo` ファイルは、 :mod:`gettext` モジュールが実行時に 実際の翻訳処理を行うために使われます。

:mod:`gettext` モジュールをソースコード中でどのように使うかは 単一のモジュールを国際化するのか、それともアプリケーション全体を
国際化するのかによります。 次のふたつのセクションで、それぞれについて説明します。


モジュールを地域化する
^^^^^^^^^^^

モジュールを地域化する場合、グローバルな変更、例えば組み込み名前空間 への変更を行わないように注意しなければなりません。GNU ``gettext``  API
ではなく、クラスベースの API を使うべきです。

仮に対象のモジュール名を "spam" とし、モジュールの各言語における 翻訳が収められた :file:`.mo` ファイルが
:file:`/usr/share/locale`  に GNU :program:`gettext` 形式で置かれているとします。
この場合、モジュールの最初で以下のようにします::

   import gettext
   t = gettext.translation('spam', '/usr/share/locale')
   _ = t.lgettext

翻訳オブジェクトが :file:`.po` ファイル中の Unicode 文字列を返す ようになっているのなら、上の代わりに以下のようにします::

   import gettext
   t = gettext.translation('spam', '/usr/share/locale')
   _ = t.ugettext


アプリケーションを地域化する
^^^^^^^^^^^^^^

アプリケーションを地域化するのなら、関数 :func:`_` を グローバルな組み込み名前空間に組み入れなければならず、これは 通常アプリケーションの主ドライバ
(main driver) ファイル で 行います。この操作によって、アプリケーション独自のファイルは 明示的に各ファイルで :func:`_`
の組み入れを行わなくても 単に ``_('...')`` を使うだけで済むようになります。

単純な場合では、単に以下の短いコードをアプリケーションの 主ドライバファイルに追加するだけです::

   import gettext
   gettext.install('myapplication')

ロケールディレクトリや *unicode* フラグを設定する必要が ある場合、それらの値を :func:`install` 関数に渡すことが できます::

   import gettext
   gettext.install('myapplication', '/usr/share/locale', unicode=1)


動作中 (on the fly) に言語を切り替える
^^^^^^^^^^^^^^^^^^^^^^^^^^

多くの言語を同時にサポートする必要がある場合、複数の翻訳インスタンスを 生成して、例えば以下のコード::

   import gettext

   lang1 = gettext.translation('myapplication', languages=['en'])
   lang2 = gettext.translation('myapplication', languages=['fr'])
   lang3 = gettext.translation('myapplication', languages=['de'])

   # start by using language1
   lang1.install()

   # ... time goes by, user selects language 2
   lang2.install()

   # ... more time goes by, user selects language 3
   lang3.install()

のように、インスタンスを明示的に切り替えてもかまいません。


翻訳処理の遅延解決
^^^^^^^^^

コードを書く上では、ほとんどの状況で文字列はコードされた場所で 翻訳されます。しかし場合によっては、翻訳対象として文字列をマーク
はするが、その後実際に翻訳が行われるように遅延させる必要が 生じます。古典的な例は以下のようなコートです::

   animals = ['mollusk',
              'albatross',
   	   'rat',
   	   'penguin',
   	   'python',
   	   ]
   # ...
   for a in animals:
       print a

ここで、リスト ``animals`` 内の文字列は翻訳対象としてマーク はしたいが、文字列が出力されるまで実際に翻訳を行うのは避けたい とします。

こうした状況を処理する一つの方法を以下に示します::

   def _(message): return message

   animals = [_('mollusk'),
              _('albatross'),
   	   _('rat'),
   	   _('penguin'),
   	   _('python'),
   	   ]

   del _

   # ...
   for a in animals:
       print _(a)

ダミーの :func:`_` 定義が単に文字列をそのまま返すように なっているので、上のコードはうまく動作します。かつ、このダミーの
定義は、組み込み名前空間に置かれた :func:`_` の定義で (:keyword:`del` 命令を実行するまで) 一時的に上書きすることが
できます。もしそれまでに :func:`_` をローカルな名前空間に 持っていたら注意してください。

二つ目の例における :func:`_` の使い方では、"a" は文字列 リテラルではないので、:program:`pygettext` プログラムが翻訳可能な
対象として識別しません。

もう一つの処理法は、以下の例のようなやり方です::

   def N_(message): return message

   animals = [N_('mollusk'),
              N_('albatross'),
   	   N_('rat'),
   	   N_('penguin'),
   	   N_('python'),
   	   ]

   # ...
   for a in animals:
       print _(a)

この例の場合では、翻訳可能な文字列を関数 :func:`N_` で マーク付けしており  [#]_  、:func:`_`
の定義とは全く衝突しません。しかしメッセージ 展開プログラムには翻訳対象の文字列が :func:`N_` でマーク
されていることを教える必要が出てくるでしょう。 :program:`pygettext` および :program:`xpot` は両方とも、コマンドライン
上のスイッチでこの機能をサポートしています。


:func:`gettext` vs. :func:`lgettext`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python 2.4 からは、 :func:`lgettext` ファミリが導入されました。 この関数の目的は、現行の GNU gettext
実装によりよく準拠した 別の関数を提供することにあります。翻訳メッセージファイル中で 使われているのと同じコードセットを使って文字列をエンコードして
返す:func:`gettext` と違い、これらの関数は :func:`locale.getpreferredencoding` の返す
優先システムエンコーディングを使って翻訳メッセージ文字列をエンコード して返します。また、Python 2.4 では、翻訳メッセージ文字列
で使われているコードセットを明示的に選べるようにする関数が新たに 導入されていることにも注意してください。コードセットを明示的に
設定すると、:func:`lgettext` でさえ、指定したコードセットで 翻訳メッセージ文字列を返します。これは GNU gettext 実装が期待している
仕様と同じです。


謝辞
--

以下の人々が、このモジュールのコード、フィードバック、設計に関する 助言、過去の実装、そして有益な経験談による貢献をしてくれました:

* Peter Funk

* James Henstridge

* Juan David Ibáñez Palomar

* Marc-André Lemburg

* Martin von Löwis

* François Pinard

* Barry Warsaw

.. rubric:: Footnotes

.. [#] 標準でロケールが収められているディレクトリはシステム依存です; 例えば、RedHat Linux では :file:`/usr/share/locale`
   ですが、 Solaris では :file:`/usr/lib/locale` です。 :mod:`gettext`
   モジュールはこうしたシステム依存の標準設定をサポートしません; その代わりに :file:`sys.prefix/share/locale` を標準の
   設定とします。この理由から、常にアプリケーションの開始時に 絶対パスで明示的に指定して :func:`bindtextdomain` を呼び出す
   のが最良のやり方ということになります。

.. [#] 上の :func:`bindtextdomain` に関する脚注を参照してください。

.. [#] 同様の作業を行う :program:`xpot` と呼ばれるプログラムを  François Pinard が書いています。このプログラムは 彼の
   :program:`po-utils` パッケージの一部で、 `<http://po-utils.progiciels-bpi.ca/>`_ で入手できます。

.. [#] :program:`msgfmt.py` は GNU :program:`msgfmt` とバイナリ互換ですが、 より単純で、Python
   だけを使った実装がされています。 このプログラムと :program:`pygettext.py` があれば、通常 Python プログラムを国際化するために
   GNU :program:`gettext` パッケージを インストールする必要はありません。

.. [#] この :func:`N_` をどうするかは全くの自由です;  :func:`MarkThisStringForTranslation`
   などとしてもかまいません。

