
:mod:`ConfigParser` --- 設定ファイルの構文解析器
====================================

.. module:: ConfigParser
   :synopsis: Configuration file parser.
.. moduleauthor:: Ken Manheimer <klm@zope.com>
.. moduleauthor:: Barry Warsaw <bwarsaw@python.org>
.. moduleauthor:: Eric S. Raymond <esr@thyrsus.com>
.. sectionauthor:: Christopher G. Petrilli <petrilli@amber.org>


.. index::
   pair: .ini; file
   pair: configuration; file
   single: ini file
   single: Windows ini file

このモジュールでは， :class:`ConfigParser`クラスを定義しています。   :class:`ConfigParser`
クラスは，Microsoft Windows の INI ファイルに 見られるような構造をもつ，基礎的な設定ファイルを実装しています．
このモジュールを使って，エンドユーザーが簡単にカスタマイズできるような Python プログラムを書くことができます。

.. % The \class{ConfigParser} class implements a basic configuration file
.. % parser language which provides a structure similar to what you would
.. % find on Microsoft Windows INI files.  You can use this to write Python
.. % programs which can be customized by end users easily.

.. % \begin{notice}[warning]
.. % This library does \emph{not} interpret or write the value-type
.. % prefixes used in the Windows Registry extended version of INI syntax.
.. % \end{notice}

.. warning::

   このライブラリでは、Windowsのレジストリ用に拡張された INI 文法はサポート *していません*。

設定ファイルは 1 つ以上のセクションからなり、セクションは ``[section]`` ヘッダとそれに続く:rfc:`822` 形式の ``name:
value`` エントリからなっています。 ``name=value`` という形式も使えます。 値の先頭にある空白文字は削除されるので注意してください．
オプションの値には，同じセクションか ``DEFAULT`` セクションに ある値を参照するような書式化文字列を含めることができます．
初期化時や検索時に別のデフォルト値を与えることもできます． ``'#'``か``';'`` ではじまる行は無視され，コメントを書く ために利用できます。

.. % The configuration file consists of sections, lead by a
.. % \samp{[section]} header and followed by \samp{name: value} entries,
.. % with continuations in the style of \rfc{822}; \samp{name=value} is
.. % also accepted.  Note that leading whitespace is removed from values.
.. % The optional values can contain format strings which refer to other
.. % values in the same section, or values in a special
.. % \code{DEFAULT} section.  Additional defaults can be provided on
.. % initialization and retrieval.  Lines beginning with \character{\#} or
.. % \character{;} are ignored and may be used to provide comments.

例::

   [My Section]
   foodir: %(dir)s/whatever
   dir=frob

この場合``%(dir)s``は変数``dir`` (この場合は``frob``)に展開さ れます。 参照の展開は必要に応じて実行されます。

.. % would resolve the \samp{\%(dir)s} to the value of
.. % \samp{dir} (\samp{frob} in this case).  All reference expansions are
.. % done on demand.

デフォルト値は :class:`ConfigParser`のコンストラクタに辞書として渡すことで設定できます。
追加の(他の値をオーバーライドする)デフォルト値は:meth:`get`メソッドに 渡すことができます。

.. % Default values can be specified by passing them into the
.. % \class{ConfigParser} constructor as a dictionary.  Additional defaults
.. % may be passed into the \method{get()} method which will override all
.. % others.


.. class:: RawConfigParser([defaults])

   基本的な設定オブジェクトです。 *defaults*が与えられた場合、オブジェクト に固有のデフォルト値がその値で初期化されます。
   このクラスは値の置換をサポートしません。

   .. versionadded:: 2.3


.. class:: ConfigParser([defaults])

   :class:`RawConfigParser`の派生クラスで値の置換を実装しており、
   :meth:`get`メソッドと:meth:`items`メソッドに省略可能な引数を追加し ています。
   *defaults*に含まれる値は``%()s``による値の置換に 適当なものである必要があります。
   *__name__*は組み込みのデフォルト値で、セクション名が含まれるので *defaults*で設定してもオーバーライドされます。

   .. % Derived class of \class{RawConfigParser} that implements the magical
   .. % interpolation feature and adds optional arguments the \method{get()}
   .. % and \method{items()} methods.  The values in \var{defaults} must be
   .. % appropriate for the \samp{\%()s} string interpolation.  Note that
   .. % \var{__name__} is an intrinsic default; its value is the section name,
   .. % and will override any value provided in \var{defaults}.
   .. % 
   .. % All option names used in interpolation will be passed through the
   .. % \method{optionxform()} method just like any other option name
   .. % reference.  For example, using the default implementation of
   .. % \method{optionxform()} (which converts option names to lower case),
   .. % the values \samp{foo \%(bar)s} and \samp{foo \%(BAR)s} are
   .. % equivalent.

   置換で使われるすべてのオプション名は、ほかのオプション名への参照と同様に :meth:`optionxform` メソッドを介して渡されます。たとえば、
   :meth:`optionxform` のデフォルト実装 (これはオプション名を小文字に変換します) を 使うと、値 ``foo %(bar)s`` および
   ``foo %(BAR)s`` は同一になります。


.. class:: SafeConfigParser([defaults])

   .. % Derived class of \class{ConfigParser} that implements a more-sane
   .. % variant of the magical interpolation feature.  This implementation is
   .. % more predictable as well.
   .. % % XXX Need to explain what's safer/more predictable about it.
   .. % New applications should prefer this version if they don't need to be
   .. % compatible with older versions of Python.

   :class:`ConfigParser`の派生クラスでより安全な値の置換を実装しています。 この実装のはより予測可能性が高くなっています。
   新規に書くアプリケーションでは、古いバージョンのPythonと互換性を持たせる 必要がない限り、このバージョンを利用することが望ましいです。

   .. % XXX 何がどう安全で予測可能性なのか書くこと。

   .. versionadded:: 2.3


.. exception:: NoSectionError

   指定したセクションが見つからなかった時に起きる例外です。


.. exception:: DuplicateSectionError

   すでに存在するセクション名に対して :meth:`add_section` が 呼び出された際に起きる例外です。

   .. % Exception raised if \method{add_section()} is called with the name of
   .. % a section that is already present.


.. exception:: NoOptionError

   指定したオプションが指定したセクションに存在しなかった時に起きる例外です。

   .. % Exception raised when a specified option is not found in the specified
   .. % section.


.. exception:: InterpolationError

   文字列の置換中に問題が起きた時に発生する例外の基底クラスです。

   .. % Exception raised when problems occur performing string interpolation.


.. exception:: InterpolationDepthError

   :exc:`InterpolationError`の派生クラスで、文字列の置換回数が
   :const:`MAX_INTERPOLATION_DEPTH`を越えたために完了しなかった場合に 発生する例外です。

   .. % Exception raised when string interpolation cannot be completed because
   .. % the number of iterations exceeds \constant{MAX_INTERPOLATION_DEPTH}.


.. exception:: InterpolationMissingOptionError

   :exc:`InterpolationError`の派生クラスで、値が参照しているオプションが 見つからない場合に発生する例外です。

   .. % Exception raised when an option referenced from a value does not exist.
   .. % Subclass of \exception{InterpolationError}.
   .. % \versionadded{2.3}


.. exception:: InterpolationSyntaxError

   :exc:`InterpolationError`の派生クラスで、指定された構文で値を置換 することができなかった場合に発生する例外です。

   .. % Exception raised when the source text into which substitutions are
   .. % made does not conform to the required syntax.
   .. % Subclass of \exception{InterpolationError}.

   .. versionadded:: 2.3


.. exception:: MissingSectionHeaderError

   セクションヘッダを持たないファイルを構文解析しようとした時に起きる例外です。

   .. % Exception raised when attempting to parse a file which has no section
   .. % headers.


.. exception:: ParsingError

   ファイルの構文解析中にエラーが起きた場合に発生する例外です。

   .. % Exception raised when errors occur attempting to parse a file.


.. data:: MAX_INTERPOLATION_DEPTH

   *raw*が偽だった場合の:meth:`get`による再帰的な文字列置換の繰り返
   しの最大値です。:class:`ConfigParser`クラスだけに関係します。

   .. % The maximum depth for recursive interpolation for \method{get()} when
   .. % the \var{raw} parameter is false.  This is relevant only for the
   .. % \class{ConfigParser} class.


.. seealso::

   Module :mod:`shlex`
      Unix のシェルに似た，アプリケーションの設定ファイル 用フォーマットとして使えるもう一つの小型言語です．

      .. % Support for a creating \UNIX{} shell-like
      .. % minilanguages which can be used as an alternate format
      .. % for application configuration files.


.. _rawconfigparser-objects:

RawConfigParser オブジェクト
----------------------

:class:`RawConfigParser`クラスのインスタンスは以下のメソッドを持ちます:

.. % \class{RawConfigParser} instances have the following methods:


.. method:: RawConfigParser.defaults()

   インスタンス全体で使われるデフォルト値の辞書を返します。

   .. % Return a dictionary containing the instance-wide defaults.


.. method:: RawConfigParser.sections()

   利用可能なセクションのリストを返します。``DEFAULT``はこのリストに含まれ ません。

   .. % Return a list of the sections available; \code{DEFAULT} is not
   .. % included in the list.


.. method:: RawConfigParser.add_section(section)

   *section*という名前のセクションをインスタンスに追加します。 同名のセク
   ションが存在した場合、:exc:`DuplicateSectionError`が発生 します。

   .. % Add a section named \var{section} to the instance.  If a section by
   .. % the given name already exists, \exception{DuplicateSectionError} is
   .. % raised.


.. method:: RawConfigParser.has_section(section)

   指定したセクションがコンフィグレーションファイルに存在するかを返します。 ``DEFAULT``セクションは存在するとみなされません。

   .. % Indicates whether the named section is present in the
   .. % configuration. The \code{DEFAULT} section is not acknowledged.


.. method:: RawConfigParser.options(section)

   *section*で指定したセクションで利用できるオプションのリストを返し ます。

   .. % Returns a list of options available in the specified \var{section}.


.. method:: RawConfigParser.has_option(section, option)

   与えられたセクションが存在してかつオプションが与えられていれば :const:`True` を返し、 そうでなければ :const:`False` を返します。

   .. % If the given section exists, and contains the given option,
   .. % return \constant{True}; otherwise return \constant{False}.

   .. versionadded:: 1.6


.. method:: RawConfigParser.read(filenames)

   ファイル名のリストを読んで解析をこころみ、 うまく解析できたファイル名のリストを返します。
   もし*filenames*が文字列かユニコード文字列なら、1つのファイル名として
   扱われます。*filenames*で指定されたファイルが開けない場合、そのファイ ルは無視されます。この挙動は設定ファイルが置かれる可能性のある場所(例えば、
   カレントディレクトリ、ホームディレクトリ、システム全体の設定を行うディ レクトリ)を設定して、そこに存在する設定ファイルを読むことを想定して設計 されています。
   設定ファイルが存在しなかった場合、:class:`ConfigParser` のインスタンスは
   空のデータセットを持ちます。初期値の設定ファイルを先に読み込んでおく 必要があるアプリケーションでは、:meth:`readfp())`を
   :meth:`read`の前に呼び出すことでそのような動作を実現できます:

   .. % Attempt to read and parse a list of filenames, returning a list of filenames
   .. % which were successfully parsed.  If \var{filenames} is a string or
   .. % Unicode string, it is treated as a single filename.
   .. % If a file named in \var{filenames} cannot be opened, that file will be
   .. % ignored.  This is designed so that you can specify a list of potential
   .. % configuration file locations (for example, the current directory, the
   .. % user's home directory, and some system-wide directory), and all
   .. % existing configuration files in the list will be read.  If none of the
   .. % named files exist, the \class{ConfigParser} instance will contain an
   .. % empty dataset.  An application which requires initial values to be
   .. % loaded from a file should load the required file or files using
   .. % \method{readfp()} before calling \method{read()} for any optional
   .. % files:

   ::

      import ConfigParser, os

      config = ConfigParser.ConfigParser()
      config.readfp(open('defaults.cfg'))
      config.read(['site.cfg', os.path.expanduser('~/.myapp.cfg')])

   .. versionchanged:: 2.4
      うまく解析できたファイル名のリストを返す.


.. method:: RawConfigParser.readfp(fp[, filename])

   *fp*で与えられるファイルかファイルのようなオブジェクトを読み込んで構 文解析します(:meth:`readline`メソッドだけを使います)。もし
   *filename*が省略されて*fp*が:attr:`name`属性を持っていれば
   *filename*の代わりに使われます。ファイル名の初期値は``<???>``です。

   .. % Read and parse configuration data from the file or file-like object in
   .. % \var{fp} (only the \method{readline()} method is used).  If
   .. % \var{filename} is omitted and \var{fp} has a \member{name} attribute,
   .. % that is used for \var{filename}; the default is \samp{<???>}.


.. method:: RawConfigParser.get(section, option)

   *section*の*option*変数を取得します。

   .. % Get an \var{option} value for the named \var{section}.


.. method:: RawConfigParser.getint(section, option)

   *section*の*option*を整数として評価する関数です。

   .. % A convenience method which coerces the \var{option} in the specified
   .. % \var{section} to an integer.


.. method:: RawConfigParser.getfloat(section, option)

   *section*の*option*を浮動小数点数として評価する関数です。

   .. % A convenience method which coerces the \var{option} in the specified
   .. % \var{section} to a floating point number.


.. method:: RawConfigParser.getboolean(section, option)

   指定した *section* の *option* 値をブール値に型強制する 便宜メソッドです。*option* として受理できる値は、真 (True)
   としては ``"1"``、 ``"yes"``、 ``"true"``、 ``"on"`` 、偽 (False) としては ``"0"``、 ``"no"``、
   ``"false"``、 ``"off"`` です。 これらの文字列値に対しては大文字小文字の区別をしません。 その他の値の場合には
   :exc:`ValueError` を送出します。

   .. % A convenience method which coerces the \var{option} in the specified
   .. % \var{section} to a Boolean value.  Note that the accepted values
   .. % for the option are \code{"1"}, \code{"yes"}, \code{"true"}, and \code{"on"},
   .. % which cause this method to return \code{True}, and \code{"0"}, \code{"no"},
   .. % \code{"false"}, and \code{"off"}, which cause it to return \code{False}.  These
   .. % string values are checked in a case-insensitive manner.  Any other value will
   .. % cause it to raise \exception{ValueError}.


.. method:: RawConfigParser.items(section)

   与えられた*section*のそれぞれのオプションについて ``(name, value)``ペアのリストを返します。

   .. % Return a list of \code{(\var{name}, \var{value})} pairs for each
   .. % option in the given \var{section}.


.. method:: RawConfigParser.set(section, option, value)

   与えられたセクションが存在していれば、オプションを指定された値に設定します。 セクションが存在しなければ :exc:`NoSectionError`
   を発生させます。 :class:`RawConfigParser` (あるいは*raw* パラメータをセットした :class:`ConfigParser`)
   を文字列型でない値の *内部的な* 格納場所として 使うことは可能ですが、すべての機能 (置換やファイルへの出力を含む) が
   サポートされるのは文字列を値として使った場合だけです。

   .. % If the given section exists, set the given option to the specified
   .. % value; otherwise raise \exception{NoSectionError}.  While it is
   .. % possible to use \class{RawConfigParser} (or \class{ConfigParser} with
   .. % \var{raw} parameters set to true) for \emph{internal} storage of
   .. % non-string values, full functionality (including interpolation and
   .. % output to files) can only be achieved using string values.

   .. versionadded:: 1.6


.. method:: RawConfigParser.write(fileobject)

   設定を文字列表現に変換してファイルオブジェクトに書き出します。この 文字列表現は:meth:`read`で読み込むことができます。

   .. % Write a representation of the configuration to the specified file
   .. % object.  This representation can be parsed by a future \method{read()}
   .. % call.

   .. versionadded:: 1.6


.. method:: RawConfigParser.remove_option(section, option)

   指定された*section*から指定された*option*を削除します。 セクションが存在しなければ、:exc:`NoSectionError` を起こします。
   存在するオプションを削除した時は :const:`True` を、 そうでない時は :const:`False` を返します。

   .. % Remove the specified \var{option} from the specified \var{section}.
   .. % If the section does not exist, raise \exception{NoSectionError}.
   .. % If the option existed to be removed, return \constant{True};
   .. % otherwise return \constant{False}.

   .. versionadded:: 1.6


.. method:: RawConfigParser.remove_section(section)

   指定された*section*を設定から削除します。 もし指定されたセクションが存在すれば``True``、そうでなければ ``False``を返します。

   .. % Remove the specified \var{section} from the configuration.
   .. % If the section in fact existed, return \code{True}.
   .. % Otherwise return \code{False}.


.. method:: RawConfigParser.optionxform(option)

   入力ファイル中に見つかったオプション名か， クライアントコードから渡されたオプション名 *option* を，
   内部で利用する形式に変換します。デフォルトでは*option*を 全て小文字に変換した名前が返されます。サブルクラスではこの関数をオーバー
   ライドすることでこの振舞いを替えることができます。たとえば、このメソッ ドを:func:`str`に設定することで大小文字の差を区別するように
   変更することができます。

   .. % Transforms the option name \var{option} as found in an input file or
   .. % as passed in by  client code to the form that should be used in the
   .. % internal structures.  The default implementation returns a lower-case
   .. % version of \var{option}; subclasses may override this or client code
   .. % can set an attribute of this name on instances to affect this
   .. % behavior.  Setting this to \function{str()}, for example, would make
   .. % option names case sensitive.


.. _configparser-objects:

ConfigParser オブジェクト
-------------------

:class:`ConfigParser`クラスは:class:`RawConfigParser`のインターフェースを
いくつかのメソッドについて拡張し、省略可能な引数を追加しています。


.. method:: ConfigParser.get(section, option[, raw[, vars]])

   *section*の*option*変数を取得します。 *raw*が真でない時には、全ての``'%'``置換は
   コンストラクタに渡されたデフォルト値か、*vars* が与えられていれば それを元にして展開されてから返されます。

   .. % Get an \var{option} value for the named \var{section}.  All the
   .. % \character{\%} interpolations are expanded in the return values, based
   .. % on the defaults passed into the constructor, as well as the options
   .. % \var{vars} provided, unless the \var{raw} argument is true.


.. method:: ConfigParser.items(section[, raw[, vars]])

   指定した*section* 内の各オプションに対して、 ``(name, value)`` のペアからなるリストを返します。
   省略可能な引数は``get()``メソッドと同じ意味を持ちます。

   .. % Return a list of \code{(\var{name}, \var{value})} pairs for each
   .. % option in the given \var{section}. Optional arguments have the
   .. % same meaning as for the \method{get()} method.

   .. versionadded:: 2.3


.. _safeconfigparser-objects:

SafeConfigParser オブジェクト
-----------------------

:class:`SafeConfigParser` は :class:`ConfigParser` と同様の拡張インターフェイスを
もっていますが、以下のような機能が追加されています:

.. % The \class{SafeConfigParser} class implements the same extended
.. % interface as \class{ConfigParser}, with the following addition:


.. method:: SafeConfigParser.set(section, option, value)

   もし与えられたセクションが存在している場合は、指定された値を 与えられたオプションに設定します。そうでない場合は :exc:`NoSectionError` を
   発生させます。  *value* は文字列  (:class:`str` または :class:`unicode`) でなければならず、 そうでない場合には
   :exc:`TypeError` が発生します。

   .. % If the given section exists, set the given option to the specified
   .. % value; otherwise raise \exception{NoSectionError}.  \var{value} must
   .. % be a string (\class{str} or \class{unicode}); if not,
   .. % \exception{TypeError} is raised.

   .. versionadded:: 2.4

