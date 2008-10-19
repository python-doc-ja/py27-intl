
:mod:`Cookie` --- HTTPの状態管理
===========================

.. % HTTP state management}

.. module:: Cookie
   :synopsis: HTTP状態管理(cookies)のサポート。
.. moduleauthor:: Timothy O'Malley <timo@alum.mit.edu>
.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>


.. % \modulesynopsis{Support for HTTP state management (cookies).}

:mod:`Cookie`モジュールはHTTPの状態管理機能であるcookieの概念を抽象
化、定義しているクラスです。単純な文字列のみで構成されるcookieのほか、 シリアル化可能なあらゆるデータ型でクッキーの値を保持するための機能も備
えています。

.. % The \module{Cookie} module defines classes for abstracting the concept of
.. % cookies, an HTTP state management mechanism. It supports both simple
.. % string-only cookies, and provides an abstraction for having any serializable
.. % data-type as cookie value.

このモジュールは元々:rfc:`2109`と:rfc:`2068`に定義されている構文解析の規 則を厳密に守っていました。しかし、MSIE
3.0xがこれらのRFCで定義された文 字の規則に従っていないことが判明したため、結局、やや厳密さを欠く構文 解析規則にせざるを得ませんでした。

.. % The module formerly strictly applied the parsing rules described in in
.. % the \rfc{2109} and \rfc{2068} specifications.  It has since been discovered
.. % that MSIE 3.0x doesn't follow the character rules outlined in those
.. % specs.  As a result, the parsing rules used are a bit less strict.

.. % \begin{excdesc}{CookieError}
.. % Exception failing because of \rfc{2109} invalidity: incorrect
.. % attributes, incorrect \code{Set-Cookie} header, etc.
.. % \end{excdesc}


.. exception:: CookieError

   属性や:mailheader:`Set-Cookie`ヘッダが正しくないなど、:rfc:`2109`に合致してい ないときに発生する例外です。

.. % \begin{classdesc}{BaseCookie}{\optional{input}}
.. % This class is a dictionary-like object whose keys are strings and
.. % whose values are \class{Morsel}s. Note that upon setting a key to
.. % a value, the value is first converted to a \class{Morsel} containing
.. % the key and the value.


.. class:: BaseCookie([input])

   このクラスはキーが文字列、値が:class:`Morsel`インスタンスで構成される辞書風オブジェ クトです。値に対するキーを設定するときは、値がキーと値を含む
   :class:`Morsel`に変換されることに注意してください。

   *input*が与えられたときは、そのまま:meth:`load`メソッドへ渡され ます。

   .. % If \var{input} is given, it is passed to the \method{load()} method.
   .. % \end{classdesc}

.. % \begin{classdesc}{SimpleCookie}{\optional{input}}
.. % This class derives from \class{BaseCookie} and overrides
.. % \method{value_decode()} and \method{value_encode()} to be the identity
.. % and \function{str()} respectively.
.. % \end{classdesc}


.. class:: SimpleCookie([input])

   このクラスは:class:`BaseCookie`の派生クラスで、:meth:`value_decode`
   は与えられた値の正当性を確認するように、:meth:`value_encode`は :func:`str`で文字列化するようにそれぞれオーバライドします。

.. % \begin{classdesc}{SerialCookie}{\optional{input}}
.. % This class derives from \class{BaseCookie} and overrides
.. % \method{value_decode()} and \method{value_encode()} to be the
.. % \function{pickle.loads()} and  \function{pickle.dumps()}.


.. class:: SerialCookie([input])

   このクラスは:class:`BaseCookie`の派生クラスで、:meth:`value_decode`
   と:meth:`value_encode`をそれぞれ:func:`pickle.loads`と
   :func:`pickle.dumps`を実行するようにオーバーライドします。

   .. % \strong{Do not use this class!}  Reading pickled values from untrusted
   .. % cookie data is a huge security hole, as pickle strings can be crafted
   .. % to cause arbitrary code to execute on your server.  It is supported
   .. % for backwards compatibility only, and may eventually go away.
   .. % \end{classdesc}

   .. deprecated:: 2.3
      このクラスを使ってはいけません! 信頼できないcookieのデータか ら pickle 化された値を読み込むことは、あなたのサーバ上で任意のコードを
      実行するために pickle 化した文字列の作成が可能であることを意味し、重大 なセキュリティホールとなります。

.. % \begin{classdesc}{SmartCookie}{\optional{input}}
.. % This class derives from \class{BaseCookie}. It overrides
.. % \method{value_decode()} to be \function{pickle.loads()} if it is a
.. % valid pickle, and otherwise the value itself. It overrides
.. % \method{value_encode()} to be \function{pickle.dumps()} unless it is a
.. % string, in which case it returns the value itself.


.. class:: SmartCookie([input])

   このクラスは:class:`BaseCookie`の派生クラスで、:meth:`value_decode`  を、値が pickle
   化されたデータとして正当なときは :func:`pickle.loads`を実行、そうでないときはその値自体を返すよう
   にオーバーライドします。また:meth:`value_encode`を、値が文字列以外
   のときは:func:`pickle.dumps`を実行、文字列のときはその値自体を返 すようにオーバーライドします。

   .. % \strong{Note:} The same security warning from \class{SerialCookie}
   .. % applies here.
   .. % \end{classdesc}

   .. deprecated:: 2.3
      :class:`SerialCookie`と同じセキュリティ上の注意が当ては まります。

関連して、さらなるセキュリティ上の注意があります。後方互換性のため、 :mod:`Cookie`モジュールは:class:`Cookie`というクラス名を
:class:`SmartCookie`のエイリアスとしてエクスポートしています。これはほ
ぼ確実に誤った措置であり、将来のバージョンでは削除することが適当と思わ
れます。アプリケーションにおいて:class:`SerialCookie`クラスを使うべきで
ないのと同じ理由で:class:`Cookie`クラスを使うべきではありません。

.. % A further security note is warranted.  For backwards compatibility,
.. % the \module{Cookie} module exports a class named \class{Cookie} which
.. % is just an alias for \class{SmartCookie}.  This is probably a mistake
.. % and will likely be removed in a future version.  You should not use
.. % the \class{Cookie} class in your applications, for the same reason why
.. % you should not use the \class{SerialCookie} class.

.. % \begin{seealso}
.. % \seemodule{cookielib}{HTTP cookie handling for web
.. % \emph{clients}.  The \module{cookielib} and \module{Cookie}
.. % modules do not depend on each other.}
.. % 
.. % \seerfc{2109}{HTTP State Management Mechanism}{This is the state
.. % management specification implemented by this module.}
.. % \end{seealso}


.. seealso::

   Module :mod:`cookielib`
      Web*クライアント*向けの HTTP クッキー処理です。 :mod:`cookielib`と:mod:`Cookie`は互いに独立しています。

   :rfc:`2109` - HTTP State Management Mechanism
      このモジュールが実装 しているHTTPの状態管理に関する規格です。

.. % \subsection{Cookie Objects \label{cookie-objects}}


.. _cookie-objects:

Cookieオブジェクト
------------

.. % \begin{methoddesc}[BaseCookie]{value_decode}{val}
.. % Return a decoded value from a string representation. Return value can
.. % be any type. This method does nothing in \class{BaseCookie} --- it exists
.. % so it can be overridden.
.. % \end{methoddesc}


.. method:: BaseCookie.value_decode(val)

   文字列表現を値にデコードして返します。戻り値の型はどのようなものでも許
   されます。このメソッドは:class:`BaseCookie`において何も実行せず、オーバー ライドされるためにだけ存在します。

.. % \begin{methoddesc}[BaseCookie]{value_encode}{val}
.. % Return an encoded value. \var{val} can be any type, but return value
.. % must be a string. This method does nothing in \class{BaseCookie} --- it exists
.. % so it can be overridden


.. method:: BaseCookie.value_encode(val)

   エンコードした値を返します。元の値はどのような型でもかまいませんが、戻
   り値は必ず文字列となります。このメソッドは:class:`BaseCookie`において何 も実行せず、オーバーライドされるためにだけ存在します。

   通常:meth:`value_encode`と:meth:`value_decode`はともに
   *value_decode*の処理内容から逆算した範囲に収まっていなければなりま せん。

   .. % In general, it should be the case that \method{value_encode()} and
   .. % \method{value_decode()} are inverses on the range of \var{value_decode}.
   .. % \end{methoddesc}

.. % \begin{methoddesc}[BaseCookie]{output}{\optional{attrs\optional{, header\optional{, sep}}}}
.. % Return a string representation suitable to be sent as HTTP headers.
.. % \var{attrs} and \var{header} are sent to each \class{Morsel}'s
.. % \method{output()} method. \var{sep} is used to join the headers
.. % together, and is by default the combination \code{'\e r\e n'} (CRLF).
.. % \versionchanged[The default separator has been changed from \code{'\e n'}
.. % to match the cookie specification]{2.5}
.. % \end{methoddesc}


.. method:: BaseCookie.output([attrs[, header[, sep]]])

   HTTPヘッダ形式の文字列表現を返します。*attrs*と*header*はそれ
   ぞれ:class:`Morsel`の:meth:`output`メソッドに送られます。*sep*
   はヘッダの連結に用いられる文字で、デフォルトは``'\r\n'`` (CRLF)となっています。

   .. versionchanged:: 2.5
      デフォルトのセパレータを ``'\n'``　から、クッキー の使用にあわせた.


.. method:: BaseCookie.output([attrs[, header[, sep]]])

   HTTPヘッダ形式の文字列表現を返します。

.. % \begin{methoddesc}[BaseCookie]{js_output}{\optional{attrs}}
.. % Return an embeddable JavaScript snippet, which, if run on a browser which
.. % supports JavaScript, will act the same as if the HTTP headers was sent.


.. method:: BaseCookie.js_output([attrs])

   ブラウザがJavaScriptをサポートしている場合、HTTPヘッダを送信した場合と 同様に動作する埋め込み可能なJavaScript
   snippetを返します。

   *attrs*の意味は:meth:`output`と同じです。

   .. % The meaning for \var{attrs} is the same as in \method{output()}.
   .. % \end{methoddesc}

.. % \begin{methoddesc}[BaseCookie]{load}{rawdata}
.. % If \var{rawdata} is a string, parse it as an \code{HTTP_COOKIE} and add
.. % the values found there as \class{Morsel}s. If it is a dictionary, it
.. % is equivalent to:


.. method:: BaseCookie.load(rawdata)

   *rawdata*が文字列であれば、``HTTP_COOKIE``として処理し、その値
   を:class:`Morsel`として追加します。辞書の場合は次と同様の処理をおこない ます。 ::

      for k, v in rawdata.items():
          cookie[k] = v

.. % \subsection{Morsel Objects \label{morsel-objects}}


.. _morsel-objects:

Morselオブジェクト
------------

.. % \begin{classdesc}{Morsel}{}
.. % Abstract a key/value pair, which has some \rfc{2109} attributes.


.. class:: Morsel()

   :rfc:`2109`の属性をキーと値で保持するabstractクラスです。

   Morselは辞書風のオブジェクトで、キーは次のような:rfc:`2109`準拠の定数と なっています。

   .. % Morsels are dictionary-like objects, whose set of keys is constant ---
   .. % the valid \rfc{2109} attributes, which are

* ``expires``

* ``path``

* ``comment``

* ``domain``

* ``max-age``

* ``secure``

* ``version``

   キーの大小文字は区別されます。

   .. % The keys are case-insensitive.
   .. % \end{classdesc}

.. % \begin{memberdesc}[Morsel]{value}
.. % The value of the cookie.
.. % \end{memberdesc}


.. attribute:: Morsel.value

   クッキーの値。

.. % \begin{memberdesc}[Morsel]{coded_value}
.. % The encoded value of the cookie --- this is what should be sent.
.. % \end{memberdesc}


.. attribute:: Morsel.coded_value

   実際に送信する形式にエンコードされたcookieの値。

.. % \begin{memberdesc}[Morsel]{key}
.. % The name of the cookie.
.. % \end{memberdesc}


.. attribute:: Morsel.key

   cookieの名前。

.. % \begin{methoddesc}[Morsel]{set}{key, value, coded_value}
.. % Set the \var{key}, \var{value} and \var{coded_value} members.
.. % \end{methoddesc}


.. method:: Morsel.set(key, value, coded_value)

   メンバ*key*、*value*、*coded_value*に値をセットします。

.. % \begin{methoddesc}[Morsel]{isReservedKey}{K}
.. % Whether \var{K} is a member of the set of keys of a \class{Morsel}.
.. % \end{methoddesc}


.. method:: Morsel.isReservedKey(K)

   *K*が:class:`Morsel`のキーであるかどうかを判定します。

.. % \begin{methoddesc}[Morsel]{output}{\optional{attrs\optional{, header}}}
.. % Return a string representation of the Morsel, suitable
.. % to be sent as an HTTP header. By default, all the attributes are included,
.. % unless \var{attrs} is given, in which case it should be a list of attributes
.. % to use. \var{header} is by default \code{"Set-Cookie:"}.
.. % \end{methoddesc}


.. method:: Morsel.output([attrs[, header]])

   MoselをHTTPヘッダ形式の文字列表現にして返します。*attrs* を指定しない 場合、デフォルトですべての属性を含めます。*attrs*を指定する場合，
   属性をリストで渡さなければなりません。*header*のデフォルトは ``"Set-Cookie:"``です。

.. % \begin{methoddesc}[Morsel]{js_output}{\optional{attrs}}
.. % Return an embeddable JavaScript snippet, which, if run on a browser which
.. % supports JavaScript, will act the same as if the HTTP header was sent.


.. method:: Morsel.js_output([attrs])

   ブラウザがJavaScriptをサポートしている場合、HTTPヘッダを送信した場合と 同様に動作する埋め込み可能なJavaScript
   snippetを返します。

   *attrs*の意味は:meth:`output`と同じです。

   .. % The meaning for \var{attrs} is the same as in \method{output()}.
   .. % \end{methoddesc}

.. % \begin{methoddesc}[Morsel]{OutputString}{\optional{attrs}}
.. % Return a string representing the Morsel, without any surrounding HTTP
.. % or JavaScript.


.. method:: Morsel.OutputString([attrs])

   Moselの文字列表現をHTTPやJavaScriptで囲まずに出力します。

   *attrs*の意味は:meth:`output`と同じです。

   .. % The meaning for \var{attrs} is the same as in \method{output()}.
   .. % \end{methoddesc}


.. _cookie-example:

例
-

次の例は:mod:`Cookie`の使い方を示したものです。

.. % The following example demonstrates how to use the \module{Cookie} module.

::

   >>> import Cookie
   >>> C = Cookie.SimpleCookie()
   >>> C = Cookie.SerialCookie()
   >>> C = Cookie.SmartCookie()
   >>> C["fig"] = "newton"
   >>> C["sugar"] = "wafer"
   >>> print C # generate HTTP headers
   Set-Cookie: sugar=wafer
   Set-Cookie: fig=newton
   >>> print C.output() # same thing
   Set-Cookie: sugar=wafer
   Set-Cookie: fig=newton
   >>> C = Cookie.SmartCookie()
   >>> C["rocky"] = "road"
   >>> C["rocky"]["path"] = "/cookie"
   >>> print C.output(header="Cookie:")
   Cookie: rocky=road; Path=/cookie
   >>> print C.output(attrs=[], header="Cookie:")
   Cookie: rocky=road
   >>> C = Cookie.SmartCookie()
   >>> C.load("chips=ahoy; vienna=finger") # load from a string (HTTP header)
   >>> print C
   Set-Cookie: vienna=finger
   Set-Cookie: chips=ahoy
   >>> C = Cookie.SmartCookie()
   >>> C.load('keebler="E=everybody; L=\\"Loves\\"; fudge=\\012;";')
   >>> print C
   Set-Cookie: keebler="E=everybody; L=\"Loves\"; fudge=\012;"
   >>> C = Cookie.SmartCookie()
   >>> C["oreo"] = "doublestuff"
   >>> C["oreo"]["path"] = "/"
   >>> print C
   Set-Cookie: oreo=doublestuff; Path=/
   >>> C = Cookie.SmartCookie()
   >>> C["twix"] = "none for you"
   >>> C["twix"].value
   'none for you'
   >>> C = Cookie.SimpleCookie()
   >>> C["number"] = 7 # equivalent to C["number"] = str(7)
   >>> C["string"] = "seven"
   >>> C["number"].value
   '7'
   >>> C["string"].value
   'seven'
   >>> print C
   Set-Cookie: number=7
   Set-Cookie: string=seven
   >>> C = Cookie.SerialCookie()
   >>> C["number"] = 7
   >>> C["string"] = "seven"
   >>> C["number"].value
   7
   >>> C["string"].value
   'seven'
   >>> print C
   Set-Cookie: number="I7\012."
   Set-Cookie: string="S'seven'\012p1\012."
   >>> C = Cookie.SmartCookie()
   >>> C["number"] = 7
   >>> C["string"] = "seven"
   >>> C["number"].value
   7
   >>> C["string"].value
   'seven'
   >>> print C
   Set-Cookie: number="I7\012."
   Set-Cookie: string=seven

