
:mod:`aepack` --- Python変数とAppleEventデータコンテナ間の変換
==============================================================

.. module:: aepack
   :platform: Mac
   :synopsis: Python変数とAppleEventデータコンテナ間の変換
.. sectionauthor:: Vincent Marchetti <vincem@en.com>


.. % Conversion between Python variables and AppleEvent data containers
.. % \moduleauthor{Jack Jansen?}{email}
.. % Conversion between Python variables and AppleEvent data containers.

:mod:`aepack` モジュールは、Python 変数から AppleEvent ディスクリプ
タへの変換(パック)と、その逆に変換(アンパック)する関数を定義しています。  Python 内では AppleEvent ディスクリプタは、組み込み型である
AEDesc の Python オブジェクトとして扱われます。:class:`AEDesc` は :mod:`Carbon.AE`
モジュールで定義されています。

.. % % The \module{aepack} module defines functions for converting (packing)
.. % % Python variables to AppleEvent descriptors and back (unpacking).
.. % % Within Python the AppleEvent descriptor is handled by Python objects
.. % % of built-in type \class{AEDesc}, defined in module \refmodule{AE}.

:mod:`aepack` モジュールは次の関数を定義しています。

.. % % The \module{aepack} module defines the following functions:


.. function:: pack(x[, forcetype])

   Python 値 x を変換した値を保持する :class:`AEDesc` オブジェクトを返しま す。*forcetype*
   が与えることで、結果のディスクリプタ型を指定できま す。それ以外では、Python 型から Apple Eventディスクリプタ型へのデフォ
   ルトのマッピングが使われます。マッピングは次の通りとなります。

   .. % % Returns an \class{AEDesc} object  containing a conversion of Python
   .. % % value x. If \var{forcetype} is provided it specifies the descriptor
   .. % % type of the result. Otherwise, a default mapping of Python types to
   .. % % Apple Event descriptor types is used, as follows:

   +-----------------+-----------------------------------+
   | Python type     | descriptor type                   |
   +=================+===================================+
   | :class:`FSSpec` | typeFSS                           |
   +-----------------+-----------------------------------+
   | :class:`FSRef`  | typeFSRef                         |
   +-----------------+-----------------------------------+
   | :class:`Alias`  | typeAlias                         |
   +-----------------+-----------------------------------+
   | integer         | typeLong (32 bit integer)         |
   +-----------------+-----------------------------------+
   | float           | typeFloat (64 bit floating point) |
   +-----------------+-----------------------------------+
   | string          | typeText                          |
   +-----------------+-----------------------------------+
   | unicode         | typeUnicodeText                   |
   +-----------------+-----------------------------------+
   | list            | typeAEList                        |
   +-----------------+-----------------------------------+
   | dictionary      | typeAERecord                      |
   +-----------------+-----------------------------------+
   | instance        | *see below*                       |
   +-----------------+-----------------------------------+

   *x* がPythonインスタンスなら、この関数は :meth:`__aepack__` メ ソッドを呼びだそうとします。このメソッドは
   :class:`AEDesc` オブジェ クトを返します。

   .. % % If \var{x} is a Python instance then this function attempts to call an
   .. % % \method{__aepack__()} method.  This method should return an
   .. % % \class{AE.AEDesc} object.

   *x* の変換が上で定義されていない場合は、この関数は、テキストディス クリプタとしてエンコードされた、値の(repr()関数による)Python文字列表現
   が返されます。

   .. % % If the conversion \var{x} is not defined above, this function returns
   .. % % the Python string representation of a value (the repr() function)
   .. % % encoded as a text descriptor.


.. function:: unpack(x[, formodulename])

   *x* は :class:`AEDesc` タイプのオブジェクトでなければいけません。 この関数は、Apple Eventディスクリプタ *x*
   のデータのPythonオブジェ クト表現を返します。単純なAppleEventデータ型(整数、テキスト、浮動少
   数点数)の、対応するPython型が返されます。Apple EventリストはPythonリ ストとして返され、リストの要素は再帰的にアンパックされます。
   ``formodulename`` の指定がない場合、オブジェクト参照 (例：``line 3 of document
   1``)が、:class:`aetypes.ObjectSpecifier` のインスタ
   ンスとして返されます。ディスクリプタ型がtypeFSSであるAppleEventディ スクリプタが、:class:`FSSpec`
   オブジェクトとして返されます。  AppleEventレコードディスクリプタが、再帰的にアンパックされた、型の4
   文字キーと要素を持つPython辞書として返されます。

   .. % %   \var{x} must be an object of type \class{AEDesc}. This function
   .. % %   returns a Python object representation of the data in the Apple
   .. % %   Event descriptor \var{x}. Simple AppleEvent data types (integer,
   .. % %   text, float) are returned as their obvious Python counterparts.
   .. % %   Apple Event lists are returned as Python lists, and the list
   .. % %   elements are recursively unpacked.  Object references
   .. % %   (ex. \code{line 3 of document 1}) are returned as instances of
   .. % %   \class{aetypes.ObjectSpecifier}, unless \code{formodulename}
   .. % %   is specified.  AppleEvent descriptors with
   .. % %   descriptor type typeFSS are returned as \class{FSSpec}
   .. % %   objects.  AppleEvent record descriptors are returned as Python
   .. % %   dictionaries, with 4-character string keys and elements recursively
   .. % %   unpacked.

   オプションの ``formodulename`` 引数は :mod:`gensuitemodule` よ
   り作成されるスタブパッケージにより利用され、オブジェクト指定子のため の OSA クラスをモジュールの中で見つけられることを保証します。これは、
   例えば、ファインダがウィンドウに対してオブジェクト指定子を返す場合、 ``Finder.Window``
   のインスタンスが得られ、``aetypes.Window``  が得られないことを保証します。前者は、ファインダ上のウィンドウが持っ
   ている、すべての特性および要素のことを知っています。一方、後者のもの はそれらのことを知りません。

   .. % %   The optional \code{formodulename} argument is used by the stub packages
   .. % %   generated by \module{gensuitemodule}, and ensures that the OSA classes
   .. % %   for object specifiers are looked up in the correct module. This ensures
   .. % %   that if, say, the Finder returns an object specifier for a window
   .. % %   you get an instance of \code{Finder.Window} and not a generic
   .. % %   \code{aetypes.Window}. The former knows about all the properties
   .. % %   and elements a window has in the Finder, while the latter knows
   .. % %   no such things.


.. seealso::

   .. % %   \seemodule{Carbon.AE}{Built-in access to Apple Event Manager routines.}
   .. % %   \seemodule{aetypes}{Python definitions of codes for Apple Event
   .. % %                       descriptor types.}
   .. % %   \seetitle[http://developer.apple.com/techpubs/mac/IAC/IAC-2.html]{
   .. % %             Inside Macintosh: Interapplication
   .. % %             Communication}{Information about inter-process
   .. % %             communications on the Macintosh.}

   Module :mod:`Carbon.AE`
      Apple Eventマネージャルーチンへの組み込みアクセス

   Module :mod:`aetypes`
      Apple Eventディスクリプタ型としてコードされたPython定義

   ` Inside Macintosh: Interapplication Communication <http://developer.apple.com/techpubs/mac/IAC/IAC-2.html>`_
      Macintosh上でのプロセス間通信に関する情報

