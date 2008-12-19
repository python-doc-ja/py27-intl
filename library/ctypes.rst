
:mod:`ctypes` --- Pythonのための外部関数ライブラリ。
====================================================

.. module:: ctypes
   :synopsis: A foreign function library for Python.
.. moduleauthor:: Thomas Heller <theller@python.net>


.. versionadded:: 2.5

``ctypes``はPythonのための外部関数ライブラリです。このライブラリは Cと互換性のあるデータ型を提供し、動的リンク/共有ライブラリ内の
関数呼び出しを可能にします。動的リンク/共有ライブラリを純粋なPythonで ラップするために使うことができます。


.. _ctypes-ctypes-tutorial:

ctypesチュートリアル
--------------------

注意: このチュートリアルのコードサンプルは動作確認のために``doctest``を 使います。コードサンプルの中にはLinux、Windows、あるいはMac
OS X上で 異なる動作をするものがあるため、サンプルのコメントにdoctest命令を 入れてあります。

注意: かなりのコードサンプルでctypesの:class:`c_int`型を参照しています。
32ビットシステムにおいてこの型は:class:`c_long`型のエイリアスです。
そのため、:class:`c_int`型を想定しているときに:class:`c_long`が 表示されたとしても、混乱しないようにしてください ---
実際には同じ型なのです。


.. _ctypes-loading-dynamic-link-libraries:

動的リンクライブラリをロードする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

動的リンクライブラリをロードするために、``ctypes``は*cdll*をエクスポートします。
Windowsではさらに*windll*と*oledll*オブジェクトもエクスポートします。

これらのオブジェクトの属性としてライブラリにアクセスすることでライブラリをロードします。
*cdll*は標準``cdecl``呼び出し規約を用いて関数をエクスポートしているライブラリをロードします。
それに対して、*windll*ライブラリは``stdcall``呼び出し規約を用いる関数を呼び出します。
*oledll*も``stdcall``呼び出し規約を使いますが、関数がWindows :class:`HRESULT`エラーコードを
返すことを想定しています。このエラーコードは関数呼び出しが失敗したとき、 :class:`WindowsError`
Python例外を自動的に発生させるために使われます。

Windows用の例ですが、``msvcrt``はほとんどの標準C関数が含まれているMS標準Cライブラリであり、
cdecl呼び出し規約を使うことに注意してください::

   >>> from ctypes import *
   >>> print windll.kernel32 # doctest: +WINDOWS
   <WinDLL 'kernel32', handle ... at ...>
   >>> print cdll.msvcrt # doctest: +WINDOWS
   <CDLL 'msvcrt', handle ... at ...>
   >>> libc = cdll.msvcrt # doctest: +WINDOWS
   >>>

Windowsではいつもの'.dll'ファイル拡張子を自動的に追加します。

Linuxではライブラリをロードするために拡張子を*含む*ファイル名を 指定する必要があるので、属性アクセスは動作しません。
dllローダーの:meth:`LoadLibrary`メソッドを使うか、 コンストラクタを呼び出してCDLLのインスタンスを作ることでライブラリを
ロードするかのどちらかを行わなければなりません::

   >>> cdll.LoadLibrary("libc.so.6") # doctest: +LINUX
   <CDLL 'libc.so.6', handle ... at ...>
   >>> libc = CDLL("libc.so.6")     # doctest: +LINUX
   >>> libc                         # doctest: +LINUX
   <CDLL 'libc.so.6', handle ... at ...>
   >>>

.. % XXX Add section for Mac OS X.


.. _ctypes-accessing-functions-from-loaded-dlls:

ロードしたdllから関数にアクセスする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

dllオブジェクトの属性として関数にアクセスします::

   >>> from ctypes import *
   >>> libc.printf
   <_FuncPtr object at 0x...>
   >>> print windll.kernel32.GetModuleHandleA # doctest: +WINDOWS
   <_FuncPtr object at 0x...>
   >>> print windll.kernel32.MyOwnFunction # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
     File "ctypes.py", line 239, in __getattr__
       func = _StdcallFuncPtr(name, self)
   AttributeError: function 'MyOwnFunction' not found
   >>>

``kernel32``や``user32``のようなwin32システムdllは、多くの場合
関数のUNICODEバージョンに加えてANSIバージョンもエクスポートすることに
注意してください。UNICODEバージョンは後ろに``W``が付いた名前でエクスポートされ、 ANSIバージョンは``A``が付いた名前でエクスポートされます。
与えられたモジュールの*モジュールハンドル*を返すwin32 ``GetModuleHandle``関数は
次のようなCプロトタイプを持ちます。UNICODEバージョンが定義されているか
どうかにより``GetModuleHandle``としてどちらか一つを公開するためにマクロが使われます::

   /* ANSI version */
   HMODULE GetModuleHandleA(LPCSTR lpModuleName);
   /* UNICODE version */
   HMODULE GetModuleHandleW(LPCWSTR lpModuleName);

*windll*は魔法を使ってどちらか一つを選ぼうとはしません。
``GetModuleHandleA``もしくは``GetModuleHandleW``を明示的に指定して
必要とするバージョンにアクセスし、通常の文字列かユニコード文字列を使って それぞれ呼び出さなければなりません。

時には、dllが関数を``"??2@YAPAXI@Z"``のようなPython識別子として 有効でない名前でエクスポートすることがあります。このような場合に
関数を取り出すには、``getattr``を使わなければなりません。  ::

   >>> getattr(cdll.msvcrt, "??2@YAPAXI@Z") # doctest: +WINDOWS
   <_FuncPtr object at 0x...>
   >>>

Windowsでは、名前ではなく序数によって関数をエクスポートするdllもあります。 こうした関数には序数を使ってdllオブジェクトにインデックス指定することで
アクセスします::

   >>> cdll.kernel32[1] # doctest: +WINDOWS
   <_FuncPtr object at 0x...>
   >>> cdll.kernel32[0] # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
     File "ctypes.py", line 310, in __getitem__
       func = _StdcallFuncPtr(name, self)
   AttributeError: function ordinal 0 not found
   >>>


.. _ctypes-calling-functions:

関数を呼び出す
^^^^^^^^^^^^^^

これらの関数は他のPython呼び出し可能オブジェクトと同じように呼び出すことができます。
この例では``time()``関数（Unixエポックからのシステム時間を秒単位で返す）と、
``GetModuleHandleA()``関数（win32モジュールハンドルを返す）を使います。

この例は両方の関数をNULLポインタとともに呼び出します (``None``をNULLポインタとして使う必要があります)::

   >>> print libc.time(None) # doctest: +SKIP
   1150640792
   >>> print hex(windll.kernel32.GetModuleHandleA(None)) # doctest: +WINDOWS
   0x1d000000
   >>>

``ctypes``は引数の数を間違えたり、あるいは呼び出し規約を間違えた関数呼び出しから
あなたを守ろうとします。残念ながら、これはWindowsでしか機能しません。 関数が返った後にスタックを調べることでこれを行います。したがって、
エラーは発生しますが、その関数は呼び出された*後です*::

   >>> windll.kernel32.GetModuleHandleA() # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: Procedure probably called with not enough arguments (4 bytes missing)
   >>> windll.kernel32.GetModuleHandleA(0, 0) # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: Procedure probably called with too many arguments (4 bytes in excess)
   >>>

同じ例外が``cdecl``呼び出し規約を使って``stdcall``関数を呼び出したときに発生しますし、 逆の場合も同様です。  ::

   >>> cdll.kernel32.GetModuleHandleA(None) # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: Procedure probably called with not enough arguments (4 bytes missing)
   >>>

   >>> windll.msvcrt.printf("spam") # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: Procedure probably called with too many arguments (4 bytes in excess)
   >>>

正しい呼び出し規約を知るためには、呼び出したい関数についてのCヘッダファイル もしくはドキュメントを見なければなりません。

Windowsでは、関数が無効な引数とともに呼び出された場合の一般保護例外による
クラッシュを防ぐために、``ctypes``はwin32構造化例外処理を使います::

   >>> windll.kernel32.GetModuleHandleA(32) # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   WindowsError: exception: access violation reading 0x00000020
   >>>

しかし、``ctypes``を使ってPythonをクラッシュさせる方法は十分なほどあるので、 よく注意すべきです。

``None``、整数、長整数、バイト文字列およびユニコード文字列だけが、 こうした関数呼び出しにおいてパラメータとして直接使えるネイティブの
Pythonオブジェクトです。``None``はCの``NULL``ポインタとして 渡され、バイト文字列とユニコード文字列はそのデータを含むメモリブロックへの
ポインタ(``char *`` または ``wchar_t *``)として渡されます。 Python整数とPython長整数はプラットホームのデフォルトのC
``int``型として渡され、 その値はC ``int``型に合うようにマスクされます。

他のパラメータ型をもつ関数呼び出しに移る前に、 ``ctypes``データ型についてさらに学ぶ必要があります。


.. _ctypes-fundamental-data-types:

基本のデータ型
^^^^^^^^^^^^^^

``ctypes``はたくさんのCと互換性のあるデータ型を定義しています :

   +----------------------+------------------------------+----------------------------+
   | ctypesの型           | Cの型                        | Pythonの型                 |
   +======================+==============================+============================+
   | :class:`c_char`      | ``char``                     | 1文字の 文字列             |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_wchar`     | ``wchar_t``                  | 1文字の ユニコード文字列   |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_byte`      | ``char``                     | 整数/長整数                |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_ubyte`     | ``unsigned char``            | 整数/長整数                |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_short`     | ``short``                    | 整数/長整数                |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_ushort`    | ``unsigned short``           | 整数/長整数                |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_int`       | ``int``                      | 整数/長整数                |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_uint`      | ``unsigned int``             | 整数/長整数                |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_long`      | ``long``                     | 整数/長整数                |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_ulong`     | ``unsigned long``            | 整数/長整数                |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_longlong`  | ``__int64`` or ``long long`` | 整数/長整数                |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_ulonglong` | ``unsigned __int64`` or      | 整数/長整数                |
   |                      | ``unsigned long long``       |                            |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_float`     | ``float``                    | 浮動小数点数               |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_double`    | ``double``                   | 浮動小数点数               |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_char_p`    | ``char *`` (NUL 終端)        | 文字列または ``None``      |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_wchar_p`   | ``wchar_t *`` (NUL 終端)     | ユニコードまたは ``None``  |
   +----------------------+------------------------------+----------------------------+
   | :class:`c_void_p`    | ``void *``                   | 整数/長整数 または``None`` |
   +----------------------+------------------------------+----------------------------+


これら全ての型はその型を呼び出すことによって作成でき、オプションとして型と値が合っている 初期化子を指定することができます::

   >>> c_int()
   c_long(0)
   >>> c_char_p("Hello, World")
   c_char_p('Hello, World')
   >>> c_ushort(-3)
   c_ushort(65533)
   >>>

これらの型は変更可能であり、値を後で変更することもできます::

   >>> i = c_int(42)
   >>> print i
   c_long(42)
   >>> print i.value
   42
   >>> i.value = -99
   >>> print i.value
   -99
   >>>

新しい値をポインタ型:class:`c_char_p`、:class:`c_wchar_p`、
および:class:`c_void_p`のインスタンスへ代入すると、 メモリブロックの*内容ではなく*指している*メモリ位置*が変わります、
(もちろんできません。なぜなら、Python文字列は変更不可能だからです)::

   >>> s = "Hello, World"
   >>> c_s = c_char_p(s)
   >>> print c_s
   c_char_p('Hello, World')
   >>> c_s.value = "Hi, there"
   >>> print c_s
   c_char_p('Hi, there')
   >>> print s                 # 最初の文字列は変更されていない
   Hello, World
   >>>

しかし、変更可能なメモリを指すポインタであることを想定している関数へ それらを渡さないように注意すべきです。もし変更可能なメモリブロックが必要なら、
ctypesには``create_string_buffer``関数があり、いろいろな方法で作成する ことできます。
現在のメモリブロックの内容は``raw``プロパティを使ってアクセス (あるいは変更)することができます。もし現在のメモリブロックにNUL終端文字列として
アクセスしたいなら、``value``プロパティを使ってください::

   >>> from ctypes import *
   >>> p = create_string_buffer(3)      # 3バイトのバッファを作成、NULで初期化される
   >>> print sizeof(p), repr(p.raw)
   3 '\x00\x00\x00'
   >>> p = create_string_buffer("Hello")      # NUL終端文字列を含むバッファを作成
   >>> print sizeof(p), repr(p.raw)
   6 'Hello\x00'
   >>> print repr(p.value)
   'Hello'
   >>> p = create_string_buffer("Hello", 10)  # 10バイトのバッファを作成
   >>> print sizeof(p), repr(p.raw)
   10 'Hello\x00\x00\x00\x00\x00'
   >>> p.value = "Hi"      
   >>> print sizeof(p), repr(p.raw)
   10 'Hi\x00lo\x00\x00\x00\x00\x00'
   >>>

``create_string_buffer``関数は初期のctypesリリースにあった``c_string``関数
だけでなく、(エイリアスとしてはまだ利用できる)``c_buffer``関数をも置き換えるものです。
Cの型``wchar_t``のユニコード文字を含む変更可能なメモリブロックを作成するには、
``create_unicode_buffer``関数を使ってください。


.. _ctypes-calling-functions-continued:

続・関数を呼び出す
^^^^^^^^^^^^^^^^^^

printfは``sys.stdout``では*なく*、本物の標準出力チャンネルへ プリントすることに注意してください。したがって、これらの例は
コンソールプロンプトでのみ動作し、*IDLE*や*PythonWin*では動作しません::

   >>> printf = libc.printf
   >>> printf("Hello, %s\n", "World!")
   Hello, World!
   14
   >>> printf("Hello, %S", u"World!")
   Hello, World!
   13
   >>> printf("%d bottles of beer\n", 42)
   42 bottles of beer
   19
   >>> printf("%f bottles of beer\n", 42.5)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ArgumentError: argument 2: exceptions.TypeError: Don't know how to convert parameter 2
   >>>

前に述べたように、必要なCのデータ型へ変換できるようにするためには、 整数、文字列およびユニコード文字列を除くすべてのPython型を
対応する``ctypes``型でラップしなければなりません::

   >>> printf("An int %d, a double %f\n", 1234, c_double(3.14))
   Integer 1234, double 3.1400001049
   31
   >>>


.. _ctypes-calling-functions-with-own-custom-data-types:

自作のデータ型とともに関数を呼び出す
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

自作のクラスのインスタンスを関数引数として使えるように、``ctypes``引数変換を カスタマイズすることもできます。
``ctypes``は:attr:`_as_parameter_`属性を探し出し、関数引数として使います。
もちろん、整数、文字列もしくはユニコードの中の一つでなければなりません::

   >>> class Bottles(object):
   ...     def __init__(self, number):
   ...         self._as_parameter_ = number
   ...
   >>> bottles = Bottles(42)
   >>> printf("%d bottles of beer\n", bottles)
   42 bottles of beer
   19
   >>>

インスタンスのデータを:attr:`_as_parameter_`インスタンス変数の中に
入れたくない場合には、そのデータを利用できるようにする``property``を 定義することができます。


.. _ctypes-specifying-required-argument-types:

要求される引数の型を指定する (関数プロトタイプ)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:attr:`argtypes`属性を設定することによって、 DLLからエクスポートされている関数に要求される引数の型を指定することができます。

:attr:`argtypes`はCデータ型のシーケンスでなければなりません(この場合 ``printf``関数はおそらく良い例ではありません。なぜなら、
引数の数が可変であり、フォーマット文字列に依存した異なる型の パラメータを取るからです。一方では、この機能の実験には とても便利です)::

   >>> printf.argtypes = [c_char_p, c_char_p, c_int, c_double]
   >>> printf("String '%s', Int %d, Double %f\n", "Hi", 10, 2.2)
   String 'Hi', Int 10, Double 2.200000
   37
   >>>

(Cの関数のプロトタイプのように)書式を指定すると互換性のない引数型になるのを防ぎ、 引数を有効な型へ変換しようとします::

   >>> printf("%d %d %d", 1, 2, 3)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ArgumentError: argument 2: exceptions.TypeError: wrong type
   >>> printf("%s %d %f", "X", 2, 3)
   X 2 3.00000012
   12
   >>>

関数呼び出しへ渡す自作のクラスを定義した場合には、 :attr:`argtypes`シーケンスの中で使えるようにするために、
そのクラスに:meth:`from_param`クラスメソッドを実装しなければなりません。
:meth:`from_param`クラスメソッドは関数呼び出しへ渡された
Pythonオブジェクトを受け取り、型チェックもしくはこのオブジェクトが受け入れ可能であると 確かめるために必要なことはすべて行ってから、オブジェクト自身、
:attr:`_as_parameter_`属性、あるいは、この場合に C関数引数として渡したい何かの値を返さなければなりません。
繰り返しになりますが、その返される結果は整数、文字列、ユニコード、``ctypes``インスタンス、
あるいは:attr:`_as_parameter_`属性をもつものであるべきです。


.. _ctypes-return-types:

戻り値の型
^^^^^^^^^^

デフォルトでは、関数はC ``int``を返すと仮定されます。他の戻り値の型を指定するには、 関数オブジェクトの:attr:`restype`属性に設定します。

さらに高度な例として、``strchr``関数を使います。この関数は文字列ポインタとcharを受け取り、 文字列へのポインタを返します。  ::

   >>> strchr = libc.strchr
   >>> strchr("abcdef", ord("d")) # doctest: +SKIP
   8059983
   >>> strchr.restype = c_char_p # c_char_pは文字列へのポインタ
   >>> strchr("abcdef", ord("d"))
   'def'
   >>> print strchr("abcdef", ord("x"))
   None
   >>>

上の``ord("x")``呼び出しを避けたいなら、:attr:`argtypes`属性を設定することができます。
二番目の引数が一文字のPython文字列からCのcharへ変換されます::

   >>> strchr.restype = c_char_p
   >>> strchr.argtypes = [c_char_p, c_char]
   >>> strchr("abcdef", "d")
   'def'
   >>> strchr("abcdef", "def")
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ArgumentError: argument 2: exceptions.TypeError: one character string expected
   >>> print strchr("abcdef", "x")
   None
   >>> strchr("abcdef", "d")
   'def'
   >>>

外部関数が整数を返す場合は、:attr:`restype`属性として呼び出し可能な Pythonオブジェクト(例えば、関数またはクラス)を使うこともできます。
呼び出し可能オブジェクトはC関数が返す``integer``とともに呼び出され、 この呼び出しの結果は関数呼び出しの結果として使われるでしょう。
これはエラーの戻り値をチェックして自動的に例外を発生させるために役に立ちます::

   >>> GetModuleHandle = windll.kernel32.GetModuleHandleA # doctest: +WINDOWS
   >>> def ValidHandle(value):
   ...     if value == 0:
   ...         raise WinError()
   ...     return value
   ...
   >>>
   >>> GetModuleHandle.restype = ValidHandle # doctest: +WINDOWS
   >>> GetModuleHandle(None) # doctest: +WINDOWS
   486539264
   >>> GetModuleHandle("something silly") # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
     File "<stdin>", line 3, in ValidHandle
   WindowsError: [Errno 126] The specified module could not be found.
   >>>

``WinError``はエラーコードの文字列表現を得るためにWindowsの``FormatMessage()`` apiを
呼び出し、例外を*返す*関数です。``WinError``はオプションで エラーコードパラメータを取ります。このパラメータが使われない場合は、
エラーコードを取り出すために:func:`GetLastError`を呼び出します。

:attr:`errcheck`属性によってもっと強力なエラーチェック機構を利用できることに 注意してください。詳細はリファレンスマニュアルを参照してください。


.. _ctypes-passing-pointers:

ポインタを渡す(または、パラメータの参照渡し)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

時には、C api関数がパラメータのデータ型として*ポインタ*を想定していることが あります。おそらくパラメータと同一の場所に書き込むためか、もしくは
そのデータが大きすぎて値渡しできない場合です。これは*パラメータの参照渡し*としても 知られています。

``ctypes``は:func:`byref`関数をエクスポートしており、パラメータを参照渡しするために
使用します。``pointer``関数を使っても同じ効果が得られます。
しかし、``pointer``は本当のポインタオブジェクトを構築するためより多くの処理を行うことから、
Python側でポインタオブジェクト自体を必要としないならば:func:`byref`を使う方がより高速です::

   >>> i = c_int()
   >>> f = c_float()
   >>> s = create_string_buffer('\000' * 32)
   >>> print i.value, f.value, repr(s.value)
   0 0.0 ''
   >>> libc.sscanf("1 3.14 Hello", "%d %f %s",
   ...             byref(i), byref(f), s)
   3
   >>> print i.value, f.value, repr(s.value)
   1 3.1400001049 'Hello'
   >>>


.. _ctypes-structures-unions:

構造体と共用体
^^^^^^^^^^^^^^

構造体と共用体は``ctypes``モジュールに定義されている:class:`Structure`および:class:`Union`
ベースクラスから導出されなければなりません。それぞれのサブクラスは:attr:`_fields_`属性を
定義する必要があります。:attr:`_fields_`は*フィールド名*と*フィールド型*を持つ *2要素タプル*のリストでなければなりません。

フィールド型は:class:`c_int`か他の``ctypes``型(構造体、共用体、配列、ポインタ)から
導出された``ctypes``型である必要があります。

``x``と``y``という名前の二つの整数からなる簡単なPOINT構造体の例です。 コンストラクタで構造体の初期化する方法の説明にもなっています::

   >>> from ctypes import *
   >>> class POINT(Structure):
   ...     _fields_ = [("x", c_int),
   ...                 ("y", c_int)]
   ...
   >>> point = POINT(10, 20)
   >>> print point.x, point.y
   10 20
   >>> point = POINT(y=5)
   >>> print point.x, point.y
   0 5
   >>> POINT(1, 2, 3)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ValueError: too many initializers
   >>>

また、さらに複雑な構造体を構成することができます。Structureはそれ自体が フィールド型に構造体を使うことで他の構造体を内部に持つことができます。

``upperleft``と``lowerright``という名前の二つのPOINTを持つRECT構造体です::

   >>> class RECT(Structure):
   ...     _fields_ = [("upperleft", POINT),
   ...                 ("lowerright", POINT)]
   ...
   >>> rc = RECT(point)
   >>> print rc.upperleft.x, rc.upperleft.y
   0 5
   >>> print rc.lowerright.x, rc.lowerright.y
   0 0
   >>>

入れ子になった構造体はいくつかの方法を用いてコンストラクタで 初期化することができます::

   >>> r = RECT(POINT(1, 2), POINT(3, 4))
   >>> r = RECT((1, 2), (3, 4))

フィールド記述子は*クラス*から取り出せます。デバッグするときに役に立つ情報を 得ることができます::

   >>> print POINT.x
   <Field type=c_long, ofs=0, size=4>
   >>> print POINT.y
   <Field type=c_long, ofs=4, size=4>
   >>>


.. _ctypes-structureunion-alignment-byte-order:

構造体/共用体アライメントとバイトオーダー
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

デフォルトでは、StructureとUnionのフィールドはCコンパイラが行うのと同じ方法で
アライメントされています。サブクラスを定義するときに:attr:`_pack_`クラス属性を 指定することでこの動作を変えることは可能です。
このクラス属性には正の整数を設定する必要があり、フィールドの最大アライメントを指定します。 これはMSVCで``#pragma
pack(n)``が行っていること同じです。

``ctypes``はStructureとUnionに対してネイティブのバイトオーダーを使います。
ネイティブではないバイトオーダーの構造体を作成するには、BigEndianStructure、
LittleEndianStructure、BigEndianUnionおよびLittleEndianUnionベースクラスの中の一つを
使います。これらのクラスにポインタフィールドを持たせることはできません。


.. _ctypes-bit-fields-in-structures-unions:

構造体と共用体におけるビットフィールド
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ビットフィールドを含む構造体と共用体を作ることができます。 ビットフィールドは整数フィールドに対してのみ作ることができ、
ビット幅は:attr:`_fields_`タプルの第三要素で指定します::

   >>> class Int(Structure):
   ...     _fields_ = [("first_16", c_int, 16),
   ...                 ("second_16", c_int, 16)]
   ...
   >>> print Int.first_16
   <Field type=c_long, ofs=0:0, bits=16>
   >>> print Int.second_16
   <Field type=c_long, ofs=0:16, bits=16>
   >>>


.. _ctypes-arrays:

配列
^^^^

Arrayはシーケンスであり、決まった数の同じ型のインスタンスを持ちます。

推奨されている配列の作成方法はデータ型に正の整数を掛けることです::

   TenPointsArrayType = POINT * 10

ややわざとらしいデータ型の例になりますが、他のものに混ざって 4個のPOINTがある構造体です::

   >>> from ctypes import *
   >>> class POINT(Structure):
   ...    _fields_ = ("x", c_int), ("y", c_int)
   ...
   >>> class MyStruct(Structure):
   ...    _fields_ = [("a", c_int),
   ...                ("b", c_float),
   ...                ("point_array", POINT * 4)]
   >>>
   >>> print len(MyStruct().point_array)
   4
   >>>

インスタンスはクラスを呼び出す通常の方法で作成します::

   arr = TenPointsArrayType()
   for pt in arr:
       print pt.x, pt.y

上記のコードは``0 0``という行が並んだものを表示します。 配列の要素がゼロで初期化されているためです。

正しい型の初期化子を指定することもできます::

   >>> from ctypes import *
   >>> TenIntegers = c_int * 10
   >>> ii = TenIntegers(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
   >>> print ii
   <c_long_Array_10 object at 0x...>
   >>> for i in ii: print i,
   ...
   1 2 3 4 5 6 7 8 9 10
   >>>


.. _ctypes-pointers:

ポインタ
^^^^^^^^

ポインタのインスタンスは``ctypes``型に対して``pointer``関数を 呼び出して作成します::

   >>> from ctypes import *
   >>> i = c_int(42)
   >>> pi = pointer(i)
   >>>

ポインタインスタンスはポインタが指すオブジェクト(上の例では``i``)を返す ``contents``属性を持ちます::

   >>> pi.contents
   c_long(42)
   >>>

``ctypes``はOOR (original object return、元のオブジェクトを返すこと)ではないことに
注意してください。属性を取り出す度に、新しい同等のオブジェクトを作成していいるのです::

   >>> pi.contents is i
   False
   >>> pi.contents is pi.contents
   False
   >>>

別の:class:`c_int`インスタンスがポインタのcontents属性に代入されると、 これが記憶されているメモリ位置を指すポインタに変化します::

   >>> i = c_int(99)
   >>> pi.contents = i
   >>> pi.contents
   c_long(99)
   >>>

ポインタインスタンスは整数でインデックス指定することもできます::

   >>> pi[0]
   99
   >>>

整数インデックスへ代入するとポインタが指す値が変更されます::

   >>> print i
   c_long(99)
   >>> pi[0] = 22
   >>> print i
   c_long(22)
   >>>

0ではないインデックスを使うこともできますが、Cの場合と同じように 自分が何をしているかを理解している必要があります。
任意のメモリ位置にアクセスもしくは変更できるのです。 一般的にこの機能を使うのは、C関数からポインタを受け取り、そのポインタが
単一の要素ではなく実際に配列を指していると*分かっている*場合だけです。

舞台裏では、``pointer``関数は単にポインタインスタンスを作成する という以上のことを行っています。はじめにポインタ*型*を作成する必要があります。
これは任意の``ctypes``型を受け取る``POINTER``関数を使って行われ、新しい型を 返します::

   >>> PI = POINTER(c_int)
   >>> PI
   <class 'ctypes.LP_c_long'>
   >>> PI(42)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: expected c_long instead of int
   >>> PI(c_int(42))
   <ctypes.LP_c_long object at 0x...>
   >>>

ポインタ型を引数なしで呼び出すと``NULL``ポインタを作成します。 ``NULL``ポインタは``False``ブール値を持っています::

   >>> null_ptr = POINTER(c_int)()
   >>> print bool(null_ptr)
   False
   >>>

``ctypes``はポインタの指す値を取り出すときに``NULL``かどうかを調べます
(しかし、``NULL``でないポインタの指す値の取り出す行為はPythonをクラッシュさせるでしょう)::

   >>> null_ptr[0]
   Traceback (most recent call last):
       ....
   ValueError: NULL pointer access
   >>>

   >>> null_ptr[0] = 1234
   Traceback (most recent call last):
       ....
   ValueError: NULL pointer access
   >>>


.. _ctypes-type-conversions:

型変換
^^^^^^

たいていの場合、ctypesは厳密な型チェックを行います。これが意味するのは、
関数の:attr:`argtypes`リスト内に、もしくは、構造体定義におけるメンバーフィールドの型として
``POINTER(c_int)``がある場合、厳密に同じ型のインスタンスだけを 受け取るということです。このルールにはctypesが他のオブジェクトを
受け取る場合に例外がいくつかあります。例えば、ポインタ型の代わりに 互換性のある配列インスタンスを渡すことができます。このように、
``POINTER(c_int)``に対して、ctypesはc_intの配列を受け取ります::

   >>> class Bar(Structure):
   ...     _fields_ = [("count", c_int), ("values", POINTER(c_int))]
   ...
   >>> bar = Bar()
   >>> bar.values = (c_int * 3)(1, 2, 3)
   >>> bar.count = 3
   >>> for i in range(bar.count):
   ...     print bar.values[i]
   ...
   1
   2
   3
   >>>

POINTER型フィールドを``NULL``に設定するために、``None``を代入してもよい::

   >>> bar.values = None
   >>>

XXX list other conversions...

時には、非互換な型のインスタンスであることもあります。``C``では、 ある型を他の型へキャストすることができます。``ctypes``は
同じやり方で使える``cast``関数を提供しています。上で定義した``Bar``構造体は
``POINTER(c_int)``ポインタまたは:class:`c_int`配列を``values``フィールドに
対して受け取り、他の型のインスタンスは受け取りません::

   >>> bar.values = (c_byte * 4)()
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: incompatible types, c_byte_Array_4 instance instead of LP_c_long instance
   >>>

このような場合には、``cast``関数が便利です。

``cast``関数はctypesインスタンスを異なるctypesデータ型を指すポインタへ キャストするために使えます。``cast``は二つのパラメータ、
ある種のポインタかそのポインタへ変換できるctypesオブジェクトと、 ctypesポインタ型を取ります。そして、第二引数のインスタンスを返します。
このインスタンスは第一引数と同じメモリブロックを参照しています::

   >>> a = (c_byte * 4)()
   >>> cast(a, POINTER(c_int))
   <ctypes.LP_c_long object at ...>
   >>>

したがって、``cast``を``Bar``構造体の``values``フィールドへ代入するために 使うことができます::

   >>> bar = Bar()
   >>> bar.values = cast((c_byte * 4)(), POINTER(c_int))
   >>> print bar.values[0]
   0
   >>>


.. _ctypes-incomplete-types:

不完全型
^^^^^^^^

*不完全型*はメンバーがまだ指定されていない構造体、共用体もしくは配列です。 Cでは、前方宣言により指定され、後で定義されます::

   struct cell; /* 前方宣言 */

   struct {
       char *name;
       struct cell *next;
   } cell;

ctypesコードへの直接的な変換ではこうなるでしょう。 しかし、動作しません::

   >>> class cell(Structure):
   ...     _fields_ = [("name", c_char_p),
   ...                 ("next", POINTER(cell))]
   ...
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
     File "<stdin>", line 2, in cell
   NameError: name 'cell' is not defined
   >>>

なぜなら、新しい``class cell``はクラス文自体の中では利用できないからです。
``ctypes``では、``cell``クラスを定義して、:attr:`_fields_`属性を クラス文の後で設定することができます::

   >>> from ctypes import *
   >>> class cell(Structure):
   ...     pass
   ...
   >>> cell._fields_ = [("name", c_char_p),
   ...                  ("next", POINTER(cell))]
   >>>

試してみましょう。``cell``のインスタンスを二つ作り、互いに参照し合うように します。最後に、つながったポインタを何度かたどります::

   >>> c1 = cell()
   >>> c1.name = "foo"
   >>> c2 = cell()
   >>> c2.name = "bar"
   >>> c1.next = pointer(c2)
   >>> c2.next = pointer(c1)
   >>> p = c1
   >>> for i in range(8):
   ...     print p.name,
   ...     p = p.next[0]
   ...
   foo bar foo bar foo bar foo bar
   >>>    


.. _ctypes-callback-functions:

コールバック関数
^^^^^^^^^^^^^^^^

``ctypes``はCの呼び出し可能な関数ポインタをPython呼び出し可能オブジェクトから
作成できるようにします。これらは*コールバック関数*と呼ばれることがあります。

最初に、コールバック関数のためのクラスを作る必要があります。そのクラスには
呼び出し規約、戻り値の型およびこの関数が受け取る引数の数と型についての情報があります。

CFUNCTYPEファクトリ関数は通常のcdecl呼び出し規約を用いて コールバック関数のための型を作成します。
Windowsでは、WINFUNCTYPEファクトリ関数がstdcall呼び出し規約を用いて コールバック関数の型を作成します。

これらのファクトリ関数はともに最初の引数に戻り値の型、 残りの引数としてコールバック関数が想定する引数の型を渡して 呼び出されます。

標準Cライブラリの:func:`qsort`関数を使う例を示します。 これはコールバック関数の助けをかりて要素をソートするために使われます。
:func:`qsort`は整数の配列をソートするために使われます::

   >>> IntArray5 = c_int * 5
   >>> ia = IntArray5(5, 1, 7, 33, 99)
   >>> qsort = libc.qsort
   >>> qsort.restype = None
   >>>

:func:`qsort`はソートするデータを指すポインタ、データ配列の要素の数、
要素の一つの大きさ、およびコールバック関数である比較関数へのポインタを引数に渡して
呼び出さなければなりません。そして、コールバック関数は要素を指す二つのポインタを渡されて 呼び出され、一番目が二番目より小さいなら負の数を、等しいならゼロを、
それ以外なら正の数を返さなければなりません。

コールバック関数は整数へのポインタを受け取り、整数を 返す必要があります。まず、コールバック関数のための``type``を 作成します::

   >>> CMPFUNC = CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))
   >>>

コールバック関数のはじめての実装なので、受け取った引数を単純に表示して、 0を返します(漸進型開発(incremental development)です
;-)::

   >>> def py_cmp_func(a, b):
   ...     print "py_cmp_func", a, b
   ...     return 0
   ...
   >>>

Cの呼び出し可能なコールバック関数を作成します::

   >>> cmp_func = CMPFUNC(py_cmp_func)
   >>>

そうすると、準備完了です::

   >>> qsort(ia, len(ia), sizeof(c_int), cmp_func) # doctest: +WINDOWS
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   py_cmp_func <ctypes.LP_c_long object at 0x00...> <ctypes.LP_c_long object at 0x00...>
   >>>

ポインタの中身にアクセスする方法がわかっているので、コールバック関数を再定義しましょう::

   >>> def py_cmp_func(a, b):
   ...     print "py_cmp_func", a[0], b[0]
   ...     return 0
   ...
   >>> cmp_func = CMPFUNC(py_cmp_func)
   >>>

Windowsでの実行結果です::

   >>> qsort(ia, len(ia), sizeof(c_int), cmp_func) # doctest: +WINDOWS
   py_cmp_func 7 1
   py_cmp_func 33 1
   py_cmp_func 99 1
   py_cmp_func 5 1
   py_cmp_func 7 5
   py_cmp_func 33 5
   py_cmp_func 99 5
   py_cmp_func 7 99
   py_cmp_func 33 99
   py_cmp_func 7 33
   >>>

linuxではソート関数がはるかに効率的に動作しており、 実施する比較の数が少ないように見えるのが不思議です::

   >>> qsort(ia, len(ia), sizeof(c_int), cmp_func) # doctest: +LINUX
   py_cmp_func 5 1
   py_cmp_func 33 99
   py_cmp_func 7 33
   py_cmp_func 5 7
   py_cmp_func 1 7
   >>>

ええ、ほぼ完成です！最終段階は、実際に二つの要素を比較して 実用的な結果を返すことです::

   >>> def py_cmp_func(a, b):
   ...     print "py_cmp_func", a[0], b[0]
   ...     return a[0] - b[0]
   ...
   >>>

Windowsでの最終的な実行結果です::

   >>> qsort(ia, len(ia), sizeof(c_int), CMPFUNC(py_cmp_func)) # doctest: +WINDOWS
   py_cmp_func 33 7
   py_cmp_func 99 33
   py_cmp_func 5 99
   py_cmp_func 1 99
   py_cmp_func 33 7
   py_cmp_func 1 33
   py_cmp_func 5 33
   py_cmp_func 5 7
   py_cmp_func 1 7
   py_cmp_func 5 1
   >>>

Linuxでは::

   >>> qsort(ia, len(ia), sizeof(c_int), CMPFUNC(py_cmp_func)) # doctest: +LINUX
   py_cmp_func 5 1
   py_cmp_func 33 99
   py_cmp_func 7 33
   py_cmp_func 1 7
   py_cmp_func 5 7
   >>>

Windowsの:func:`qsort`関数はlinuxバージョンより多く比較する必要があることがわかり、 非常におもしろいですね！

簡単に確認できるように、今では配列はソートされています::

   >>> for i in ia: print i,
   ...
   1 5 7 33 99
   >>>

**コールバック関数についての重要な注意事項:**

Cコードから使われる限り、CFUNCTYPEオブジェクトへの参照を確実に保持してください。
``ctypes``は保持しません。もしあなたがやらなければ、オブジェクトはゴミ集めされてしまい、
コールバックしたときにあなたのプログラムをクラッシュさせるかもしれません。


.. _ctypes-accessing-values-exported-from-dlls:

dllからエクスポートされている値へアクセスする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

dllは関数だけでなく変数をエクスポートしていることもあります。 Pythonライブラリにある例としては``Py_OptimizeFlag``、
起動時の:option:`-O`または:option:`-OO`フラグに依存して、 0, 1または2が設定される整数があります。

``ctypes``は型の:meth:`in_dll`クラスメソッドを使ってこのように 値にアクセスできます。*pythonapi*はPython C
apiへのアクセスできるように するための予め定義されたシンボルです::

   >>> opt_flag = c_int.in_dll(pythonapi, "Py_OptimizeFlag")
   >>> print opt_flag
   c_long(0)
   >>>

インタープリタが:option:`-O`を指定されて動き始めた場合、サンプルは
``c_long(1)``を表示するでしょうし、:option:`-OO`が指定されたならば ``c_long(2)``を表示するでしょう。

ポインタの使い方を説明する拡張例では、Pythonがエクスポートする ``PyImport_FrozenModules``ポインタにアクセスします。

Pythonドキュメントからの引用すると: *このポインタは メンバーがすべてNULLまたはゼロであるレコードを最後に持つ"struct
_frozen"レコードの 配列を指すように初期化されます。 フローズン(frozen)モジュールがインポートされたとき、このテーブルから探索されます。
サードパーティ製コードは動的に作成されたフローズンモジュールの集合を提供するためと、 これにいたずらすることができます。*

これで、このポインタを操作することが役に立つことを証明できるでしょう。 例の大きさを制限するために、このテーブルを``ctypes``を使って読む方法だけを
示します::

   >>> from ctypes import *
   >>>
   >>> class struct_frozen(Structure):
   ...     _fields_ = [("name", c_char_p),
   ...                 ("code", POINTER(c_ubyte)),
   ...                 ("size", c_int)]
   ...
   >>>

私たちは``struct _frozen``データ型を定義済みなので、このテーブルを指す ポインタを得ることができます::

   >>> FrozenTable = POINTER(struct_frozen)
   >>> table = FrozenTable.in_dll(pythonapi, "PyImport_FrozenModules")
   >>>

``table``が``struct_frozen``レコードの配列への``pointer``なので、
その配列に対して反復処理を行えます。しかし、ループが確実に終了するように する必要があります。なぜなら、ポインタに大きさの情報がないからです。
遅かれ早かれ、アクセス違反か何かでクラッシュすることになるでしょう。 NULLエントリに達したときはループを抜ける方が良い::

   >>> for item in table:
   ...    print item.name, item.size
   ...    if item.name is None:
   ...        break
   ...
   __hello__ 104
   __phello__ -104
   __phello__.spam 104
   None 0
   >>>

標準Pythonはフローズンモジュールとフローズンパッケージ(負のサイズのメンバーで 表されています)を持っているという事実はあまり知られておらず、テストにだけ
使われています。例えば、``import __hello__``を試してみてください。


.. _ctypes-surprises:

予期しないこと
^^^^^^^^^^^^^^

``ctypes``には別のことを期待しているのに実際に起きる起きることは違うという場合が あります。

次に示す例について考えてみてください::

   >>> from ctypes import *
   >>> class POINT(Structure):
   ...     _fields_ = ("x", c_int), ("y", c_int)
   ...
   >>> class RECT(Structure):
   ...     _fields_ = ("a", POINT), ("b", POINT)
   ...
   >>> p1 = POINT(1, 2)
   >>> p2 = POINT(3, 4)
   >>> rc = RECT(p1, p2)
   >>> print rc.a.x, rc.a.y, rc.b.x, rc.b.y
   1 2 3 4
   >>> # now swap the two points
   >>> rc.a, rc.b = rc.b, rc.a
   >>> print rc.a.x, rc.a.y, rc.b.x, rc.b.y
   3 4 3 4
   >>>

うーん、最後の文に``3 4 1 2``と表示されることを期待していたはずです。 何が起きたのでしょうか？上の行の``rc.a, rc.b = rc.b,
rc.a``の 各段階はこのようになります::

   >>> temp0, temp1 = rc.b, rc.a
   >>> rc.a = temp0
   >>> rc.b = temp1
   >>>

``temp0``と``temp1``は前記の``rc``オブジェクトの内部バッファで まだ使われているオブジェクトです。したがって、``rc.a =
temp0``を実行すると ``temp0``のバッファ内容が``rc``のバッファへコピーされます。さらに、
これは``temp1``の内容を変更します。そのため、最後の代入``rc.b = temp1``は、 期待する結果にはならないのです。

Structure、UnionおよびArrayのサブオブジェクトを取り出しても、そのサブオブジェクトが
*コピー*されるわけではなく、ルートオブジェクトの内部バッファにアクセスする ラッパーオブジェクトを取り出すことを覚えておいてください。

期待とは違う振る舞いをする別の例はこれです::

   >>> s = c_char_p()
   >>> s.value = "abc def ghi"
   >>> s.value
   'abc def ghi'
   >>> s.value is s.value
   False
   >>>

なぜ``False``と表示されるのでしょうか？ctypesインスタンスは メモリの内容にアクセスするいくつかの記述子付きメモリを含むオブジェクトです。
メモリブロックにPythonオブジェクトを保存してもオブジェクト自身が保存 される訳ではなく、オブジェクトの``contents``が保存されます。
そのcontentsに再アクセスすると新しいPythonオブジェクトがその度に作られます。


.. _ctypes-variable-sized-data-types:

可変サイズのデータ型
^^^^^^^^^^^^^^^^^^^^

``ctypes``は可変サイズの配列と構造体をサポートしています (バージョン0.9.9.7で追加されました)。

``resize``関数は既存のctypesオブジェクトのメモリバッファのサイズを 変更したい場合に使えます。この関数は第一引数にオブジェクト、第二引数に
要求されたサイズをバイト単位で指定します。メモリブロックはオブジェクト型で 指定される通常のメモリブロックより小さくすることはできません。
これをやろうとすると、``ValueError``が発生します::

   >>> short_array = (c_short * 4)()
   >>> print sizeof(short_array)
   8
   >>> resize(short_array, 4)
   Traceback (most recent call last):
       ...
   ValueError: minimum size is 8
   >>> resize(short_array, 32)
   >>> sizeof(short_array)
   32
   >>> sizeof(type(short_array))
   8
   >>>

これはこれで上手くいっていますが、この配列の追加した要素へ どうやってアクセスするのでしょうか？この型は要素の数が4個であると
まだ認識しているので、他の要素にアクセスするとエラーになります::

   >>> short_array[:]
   [0, 0, 0, 0]
   >>> short_array[7]
   Traceback (most recent call last):
       ...
   IndexError: invalid index
   >>>

``ctypes``で可変サイズのデータ型を使うもう一つの方法は、 必要なサイズが分かった後にPythonの動的性質を使って
一つ一つデータ型を(再)定義することです。


.. _ctypes-bugs-todo-non-implemented-things:

バグ、ToDoおよび実装されていないもの
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

列挙型は実装されていません。ベースクラスに:class:`c_int`を使うことで 簡単に実装できます。

``long double``は実装されていません。

.. % Local Variables:
.. % compile-command: "make.bat"
.. % End:


.. _ctypes-ctypes-reference:

ctypesリファレンス
------------------


.. _ctypes-finding-shared-libraries:

共有ライブラリを見つける
^^^^^^^^^^^^^^^^^^^^^^^^

コンパイルされる言語でプログラミングしている場合、共有ライブラリはプログラムを
コンパイル/リンクしているときと、そのプログラムが動作しているときにアクセスされます。

ctypesライブラリローダーはプログラムが動作しているときのように振る舞い、
ランタイムローダーを直接呼び出すのに対し、``find_library``関数の目的は コンパイラが行うのと似た方法でライブラリを探し出すことです
(複数のバージョンの共有ライブラリがあるプラットホームでは、 一番最近に見つかったものがロードされます)。

``ctypes.util``モジュールはロードするライブラリを決めるのに 役立つ関数を提供します。


.. data:: find_library(name)
   :noindex:

   ライブラリを見つけてパス名を返そうと試みます。*name*は *lib*のような接頭辞、``.so``、``.dylib``のような接尾辞、
   あるいは、バージョン番号が何も付いていないライブラリの名前です (これは posix リンカのオプション:option:`-l`)に使われている形式です)。
   もしライブラリが見つからなければ、``None``を返します。

厳密な機能はシステムに依存します。

Linuxでは、``find_library``はライブラリファイルを見つけるために 外部プログラム
(/sbin/ldcon?g、gccおよびobjdump)を実行しようとします。 ライブラリファイルのファイル名を返します。いくつか例があります::

   >>> from ctypes.util import find_library
   >>> find_library("m")
   'libm.so.6'
   >>> find_library("c")
   'libc.so.6'
   >>> find_library("bz2")
   'libbz2.so.1.0'
   >>>

OS Xでは、``find_library``はライブラリの位置を探すために、 予め定義された複数の命名方法とパスを試し、成功すればフルパスを返します::

   >>> from ctypes.util import find_library
   >>> find_library("c")
   '/usr/lib/libc.dylib'
   >>> find_library("m")
   '/usr/lib/libm.dylib'
   >>> find_library("bz2")
   '/usr/lib/libbz2.dylib'
   >>> find_library("AGL")
   '/System/Library/Frameworks/AGL.framework/AGL'
   >>>

Windows では、``find_library``はシステムの探索パスに沿って探し、 フルパスを返します。しかし、予め定義された命名方法がないため、
``find_library("c")``のような呼び出しは失敗し、 ``None``を返します。

もし``ctypes``を使って共有ライブラリをラップするなら、 実行時にライブラリを探すために``find_library``を使う代わりに、
開発時に共有ライブラリ名をを決めて、ラッパーモジュールに ハードコードした方が良い*かもしれません*。


.. _ctypes-loading-shared-libraries:

共有ライブラリをロードする
^^^^^^^^^^^^^^^^^^^^^^^^^^

共有ライブラリをPythonプロセスへロードする方法はいくつかあります。 一つの方法は下記のクラスの一つをインスタンス化することです:


.. class:: CDLL(name, mode=DEFAULT_MODE, handle=None)

   このクラスのインスタンスはロードされた共有ライブラリをあらわします。 これらのライブラリの関数は標準 C 呼び出し規約を使用し、
   ``int``を返すと仮定されます。


.. class:: OleDLL(name, mode=DEFAULT_MODE, handle=None)

   Windows用: このクラスのインスタンスはロードされた共有ライブラリを あらわします。これらのライブラリの関数は``stdcall``呼び出し規約を使用し、
   windows固有の:class:`HRESULT`コードを返すと仮定されます。 :class:`HRESULT`値には関数呼び出しが失敗したのか成功したのかを
   特定する情報とともに、補足のエラーコードが含まれます。 戻り値が失敗を知らせたならば、:class:`WindowsError`が自動的に 発生します。


.. class:: WinDLL(name, mode=DEFAULT_MODE, handle=None)

   Windows用: このクラスのインスタンスはロードされた共有ライブラリを あらわします。これらのライブラリの関数は``stdcall``呼び出し規約を使用し、
   デフォルトでは``int``を返すと仮定されます。

   Windows CEでは標準呼び出し規約だけが使われます。便宜上、 このプラットホームでは、:class:`WinDLL`と:class:`OleDLL`が
   標準呼び出し規約を使用します。

これらのライブラリがエクスポートするどの関数でも呼び出す前に Python GIL は解放され、後でまた必要になります。


.. class:: PyDLL(name, mode=DEFAULT_MODE, handle=None)

   Python GILが関数呼び出しの間解放*されず*、関数実行の後にPython エラーフラグが チェックされるということを除けば、このクラスのインスタンスは
   :class:`CDLL`インスタンスのように振る舞います。エラーフラグがセットされた場合、 Python 例外が発生します。

   要するに、これはPython C api関数を直接呼び出すのに便利だというだけです。

これらすべてのクラスは少なくとも一つの引数、すなわちロードする共有ライブラリの パスを渡して呼び出すことでインスタンス化されます。すでにロード済みの
共有ライブラリへのハンドルがあるなら、``handle``名前付き引数として 渡すことができます。土台となっているプラットホームの``dlopen``または
:meth:`LoadLibrary`関数がプロセスへライブラリをロードするために使われ、 そのライブラリに対するハンドルを得ます。

*mode*パラメータはライブラリがどうやってロードされたかを特定するために
使うことができます。詳細は、``dlopen(3)``マニュアルページを参考にしてください。 Windowsでは*mode*は無視されます。


.. data:: RTLD_GLOBAL
   :noindex:

   *mode*パラメータとして使うフラグ。このフラグが利用できないプラットホームでは、 整数のゼロと定義されています。


.. data:: RTLD_LOCAL
   :noindex:

   *mode*パラメータとして使うフラグ。これが利用できないプラットホームでは、 *RTLD_GLOBAL*と同様です。


.. data:: DEFAULT_MODE
   :noindex:

   共有ライブラリをロードするために使われるデフォルトモード。 OSX 10.3では*RTLD_GLOBAL*であり、そうでなければ
   *RTLD_LOCAL*と同じです。

これらのクラスのインスタンスには公開メソッドがありません。けれども、 :meth:`__getattr__`と:meth:`__getitem__`は
特別ははたらきをします。その共有ライブラリがエクスポートする関数に 添字を使って属性としてアクセスできるのです。:meth:`__getattr__`と
:meth:`__getitem__`のどちらもが結果をキャッシュし、 そのため常に同じオブジェクトを返すことに注意してください。

次に述べる公開属性が利用できます。それらの名前はエクスポートされた関数名に 衝突しないように下線で始まります:


.. attribute:: PyDLL._handle

   ライブラリへのアクセスに用いられるシステムハンドル。


.. attribute:: PyDLL._name

   コンストラクタに渡されたライブラリの名前。

共有ライブラリは(:class:`LibraryLoader`クラスのインスタンスである)
前もって作られたオブジェクトの一つを使うことによってロードすることもできます。
それらの:meth:`LoadLibrary`メソッドを呼び出すか、ローダーインスタンスの属性として ライブラリを取り出すかのどちらかによりロードします。


.. class:: LibraryLoader(dlltype)

   共有ライブラリをロードするクラス。``dlltype``は:class:`CDLL`、:class:`PyDLL`、
   :class:`WinDLL`もしくは:class:`OleDLL`型の一つであるべきです。

   :meth:`__getattr__`は特別なはたらきをします: ライブラリローダーインスタンスの
   属性として共有ライブラリにアクセスするとそれがロードされるということを可能にします。 結果はキャッシュされます。そのため、繰り返し属性アクセスを行うと
   いつも同じライブラリが返されます。


.. method:: LibraryLoader.LoadLibrary(name)

   共有ライブラリをプロセスへロードし、それを返します。 このメソッドはライブラリの新しいインスタンスを常に返します。

これらの前もって作られたライブラリローダーを利用することができます:


.. data:: cdll
   :noindex:

   :class:`CDLL`インスタンスを作ります。


.. data:: windll
   :noindex:

   Windows用: :class:`WinDLL`インスタンスを作ります。


.. data:: oledll
   :noindex:

   Windows用: :class:`OleDLL`インスタンスを作ります。


.. data:: pydll
   :noindex:

   :class:`PyDLL`インスタンスを作ります。

C Python api に直接アクセするために、すぐに使用できる Python共有ライブラリオブジェクトが用意されています:


.. data:: pythonapi
   :noindex:

   属性としてPython C api関数を公開する:class:`PyDLL`のインスタンス。 これらすべての関数はC
   ``int``を返すと仮定されますが、もちろん常に正しいとは 限りません。そのため、これらの関数を使うためには
   正しい:attr:`restype`属性を代入しなければなりません。


.. _ctypes-foreign-functions:

外部関数
^^^^^^^^

前節で説明した通り、外部関数はロードされた共有ライブラリの属性として アクセスできます。デフォルトではこの方法で作成された関数オブジェクトは
どんな数の引数でも受け取り、引数としてどんな ctypesデータのインスタンスをも 受け取り、そして、ライブラリローダーが指定したデフォルトの結果の値の型を
返します。関数オブジェクトはプライベートクラスのインスタンスです:


.. class:: _FuncPtr

   Cの呼び出し可能外部関数のためのベースクラス。

外部関数のインスタンスも C 互換データ型です。それらは Cの関数ポインタを表しています。

この振る舞いは外部関数オブジェクトの特別な属性に代入することによって、 カスタマイズすることができます。


.. attribute:: _FuncPtr.restype

   外部関数の結果の型を指定するためにctypes型を代入する。 何も返さない関数を表す``void``に対しては``None``を 使います。

   ctypes 型ではない呼び出し可能な Python オブジェクトを代入することは可能です。 このような場合、関数がC
   ``int``を返すと仮定され、呼び出し可能オブジェクトは この整数を引数に呼び出されます。さらに処理を行ったり、エラーチェックをしたり
   できるようにするためです。これの使用は推奨されません。より柔軟な後処理や エラーチェックのためには restype として ctypes
   型を使い、:attr:`errcheck`属性へ 呼び出し可能オブジェクトを代入してください。


.. attribute:: _FuncPtr.argtypes

   関数が受け取る引数の型を指定するためにctypes型のタプルを代入します。 ``stdcall``呼び出し規約をつかう関数はこのタプルの長さと同じ数の引数で
   呼び出されます。 その上、C呼び出し規約をつかう関数は追加の不特定の引数も取ります。

   外部関数が呼ばれたとき、それぞれの実引数は:attr:`argtypes`タプルの要素の
   :meth:`from_param`クラスメソッドへ渡されます。このメソッドは実引数を 外部関数が受け取るオブジェクトに合わせて変えられるようにします。
   例えば、:attr:`argtypes`タプルの:class:`c_char_p`要素は、 ctypes変換規則にしたがって引数として渡されたユニコード文字列を
   バイト文字列へ変換するでしょう。

   新: ctypes型でない要素をargtypesに入れることができますが、 個々の要素は引数として使える値(整数、文字列、ctypesインスタンス)を返す
   :meth:`from_param`メソッドを持っていなければなりません。 これにより関数パラメータとしてカスタムオブジェクトを
   適合するように変更できるアダプタが定義可能となります。


.. attribute:: _FuncPtr.errcheck

   Python関数または他の呼び出し可能オブジェクトをこの属性に代入します。 呼び出し可能オブジェクトは三つ以上の引数とともに呼び出されます。


.. function:: callable(result, func, arguments)
   :noindex:

   ``result``は外部関数が返すもので、:attr:`restype`属性で 指定されます。

   ``func``は外部関数オブジェクト自身で、これにより複数の関数の処理結果を チェックまたは後処理するために、同じ呼び出し可能オブジェクトを再利用
   できるよになります。

   ``arguments``は関数呼び出しに最初に渡されたパラメータが入ったタプルです。
   これにより使われた引数に基づた特別な振る舞いをさせることができるようになります。

   この関数が返すオブジェクトは外部関数呼び出しから返された値でしょう。 しかし、戻り値をチェックして、外部関数呼び出しが失敗しているなら例外を
   発生させることもできます。


.. exception:: ArgumentError()

   この例外は外部関数呼び出しが渡された引数を変換できなかったときに 発生します。


.. _ctypes-function-prototypes:

関数プロトタイプ
^^^^^^^^^^^^^^^^

外部関数は関数プロトタイプをインスタンス化することによって作成されます。 関数プロトタイプはCの関数プロトタイプと似ています。実装を定義せずに、
関数(戻り値、引数の型、呼び出し規約)を記述します。 ファクトリ関数は関数に要求する戻り値の型と引数の型とともに呼び出されます。


.. function:: CFUNCTYPE(restype, *argtypes)

   返された関数プロトタイプは標準C呼び出し規約をつかう関数を作成します。 関数は呼び出されている間GILを解放します。


.. function:: WINFUNCTYPE(restype, *argtypes)

   Windows用: 返された関数プロトタイプは``stdcall``呼び出し規約を つかう関数を作成します。ただし、:func:`WINFUNCTYPE`が
   :func:`CFUNCTYPE`と同じであるWindows CEを除く。 関数は呼び出されている間GILを解放します。


.. function:: PYFUNCTYPE(restype, *argtypes)

   返された関数プロトタイプはPython呼び出し規約をつかう関数を作成します。 関数は呼び出されている間GILを解放*しません*。

ファクトリ関数によって作られた関数プロトタイプは呼び出しのパラメータの型と数に依存した 別の方法でインスタンス化することができます。


.. function:: prototype(address)
   :noindex:

   指定されたアドレスの外部関数を返します。


.. function:: prototype(callable)
   :noindex:

   Pythonの``callable``からCの呼び出し可能関数(コールバック関数)を作成します。


.. function:: prototype(func_spec[, paramflags])
   :noindex:

   共有ライブラリがエクスポートしている外部関数を返します。 ``func_spec``は2要素タプル``(name_or_ordinal,
   library)``でなければなりません。 第一要素はエクスポートされた関数の名前である文字列、またはエクスポートされた関数の
   序数である小さい整数です。第二要素は共有ライブラリインスタンスです。


.. function:: prototype(vtbl_index, name[, paramflags[, iid]])
   :noindex:

   COMメソッドを呼び出す外部関数を返します。 ``vtbl_index``は仮想関数テーブルのインデックスで、非負の小さい整数です。
   *name*はCOMメソッドの名前です。*iid*はオプションの インターフェイス識別子へのポインタで、拡張されたエラー情報の提供のために 使われます。

   COMメソッドは特殊な呼び出し規約を用います。このメソッドは :attr:`argtypes`タプルに指定されたパラメータに加えて、
   第一引数としてCOMインターフェイスへのポインタを必要とします。

オプションの*paramflags*パラメータは上述した機能より多機能な 外部関数ラッパーを作成します。

*paramflags*は:attr:`argtypes`と同じ長さのタプルでなければならない。

このタプルの個々の要素はパラメータについてのより詳細な情報を持ち、 1、2もしくは3要素を含むタプルでなければならない。

第一要素はパラメータについてのフラグを含んだ整数です。


.. data:: 1
   :noindex:

   入力パラメータを関数に指定します。


.. data:: 2
   :noindex:

   出力パラメータ。外部関数が値を書き込みます。


.. data:: 4
   :noindex:

   デフォルトで整数ゼロになる入力パラメータ。

オプションの第二要素はパラメータ名の文字列です。これが指定された場合は、 外部関数を名前付きパラメータで呼び出すことができます。

オプションの第三要素はこのパラメータのデフォルト値です。

この例では、デフォルトパラメータと名前付き引数をサポートするために Windows ``MessageBoxA``関数をラップする方法を示します。
windowsヘッダファイルのCの宣言はこれです::

   WINUSERAPI int WINAPI
   MessageBoxA(
       HWND hWnd ,
       LPCSTR lpText,
       LPCSTR lpCaption,
       UINT uType);

``ctypes``を使ってラップします:

   ::

      >>> from ctypes import c_int, WINFUNCTYPE, windll
      >>> from ctypes.wintypes import HWND, LPCSTR, UINT
      >>> prototype = WINFUNCTYPE(c_int, HWND, LPCSTR, LPCSTR, UINT)
      >>> paramflags = (1, "hwnd", 0), (1, "text", "Hi"), (1, "caption", None), (1, "flags", 0)
      >>> MessageBox = prototype(("MessageBoxA", windll.user32), paramflags)
      >>>

今はMessageBox外部関数をこのような方法で呼び出すことができます::

   >>> MessageBox()
   >>> MessageBox(text="Spam, spam, spam")
   >>> MessageBox(flags=2, text="foo bar")
   >>>

二番目の例は出力パラメータについて説明します。win32の``GetWindowRect``関数は、
指定されたウィンドウの大きさを呼び出し側が与える``RECT``構造体へコピーすることで 取り出します。 Cの宣言はこうです::

   WINUSERAPI BOOL WINAPI
   GetWindowRect(
        HWND hWnd,
        LPRECT lpRect);

``ctypes``を使ってラップします:

   ::

      >>> from ctypes import POINTER, WINFUNCTYPE, windll, WinError
      >>> from ctypes.wintypes import BOOL, HWND, RECT
      >>> prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
      >>> paramflags = (1, "hwnd"), (2, "lprect")
      >>> GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
      >>>

もし単一の値もしくは一つより多い場合には出力パラメータ値が入ったタプルがあるならば、 出力パラメータを持つ関数は自動的に出力パラメータ値を返すでしょう。
そのため、今はGetWindowRect関数は呼び出されたときにRECTインスタンスを返します。

さらに出力処理やエラーチェックを行うために、出力パラメータを:attr:`errcheck`プロトコルと 組み合わせることができます。win32
``GetWindowRect`` api関数は成功したか失敗したかを 知らせるために``BOOL``を返します。そのため、この関数はエラーチェックを行って、
api呼び出しが失敗した場合に例外を発生させることができます::

   >>> def errcheck(result, func, args):
   ...     if not result:
   ...         raise WinError()
   ...     return args
   >>> GetWindowRect.errcheck = errcheck
   >>>

:attr:`errcheck`関数が変更なしに受け取った引数タプルを返したならば、 ``ctypes``は出力パラメータに対して通常の処理を続けます。
``RECT``インスタンスの代わりにwindow座標のタプルを返してほしいなら、 関数のフィールドを取り出し、代わりにそれらを返すことができます。
通常処理はもはや行われないでしょう::

   >>> def errcheck(result, func, args):
   ...     if not result:
   ...         raise WinError()
   ...     rc = args[1]
   ...     return rc.left, rc.top, rc.bottom, rc.right
   >>>
   >>> GetWindowRect.errcheck = errcheck
   >>>


.. _ctypes-utility-functions:

ユーティリティ関数
^^^^^^^^^^^^^^^^^^


.. function:: addressof(obj)

   メモリバッファのアドレスを示す整数を返します。``obj``は ctypes型のインスタンスでなければなりません。


.. function:: alignment(obj_or_type)

   ctypes型のアライメントの必要条件を返します。 ``obj_or_type``はctypes型またはインスタンスでなければなりません。


.. function:: byref(obj)

   ``obj``\ (ctypes型のインスタンスでなければならない)への軽量ポインタを返します。
   返されるオブジェクトは外部関数呼び出しのパラメータとしてのみ使用できます。 ``pointer(obj)``と似たふるまいをしますが、作成が非常に速く行えます。


.. function:: cast(obj, type)

   この関数はCのキャスト演算子に似ています。``obj``と同じメモリブロックを 指している``type``の新しいインスタンスを返します。
   ``type``はポインタ型でなければならず、``obj``は ポインタとして解釈できるオブジェクトでなければならない。


.. function:: create_string_buffer(init_or_size[, size])

   この関数は変更可能な文字バッファを作成します。返されるオブジェクトは :class:`c_char`のctypes配列です。

   ``init_or_size``は配列のサイズを指定する整数もしくは 配列要素を初期化するために使われる文字列である必要があります。

   第一引数として文字列が指定された場合は、バッファが文字列の長さより一要素分大きく 作られます。配列の最後の要素がNUL終端文字であるためです。
   文字列の長さを使うべきでない場合は、配列のサイズを指定するために 整数を第二引数として渡すことができます。

   第一引数がユニコード文字列ならば、ctypes変換規則にしたがい 8ビット文字列へ変換されます。


.. function:: create_unicode_buffer(init_or_size[, size])

   この関数は変更可能なユニコード文字バッファを作成します。 返されるオブジェクトは:class:`c_wchar`のctypes配列です。

   ``init_or_size``は配列のサイズを指定する整数もしくは 配列要素を初期化するために使われるユニコード文字列です。

   第一引数としてユニコード文字列が指定された場合は、バッファが文字列の長さより 一要素分大きく作られます。配列の最後の要素がNUL終端文字であるためです。
   文字列の長さを使うべきでない場合は、配列のサイズを指定するために 整数を第二引数として渡すことができます。

   第一引数が8ビット文字列ならば、ctypes変換規則にしたがい ユニコード文字列へ変換されます。


.. function:: DllCanUnloadNow()

   Windows用: この関数はctypesをつかってインプロセスCOMサーバーを 実装できるようにするためのフックです。_ctypes拡張dllが
   エクスポートしているDllCanUnloadNow関数から呼び出されます。


.. function:: DllGetClassObject()

   Windows用: この関数はctypesをつかってインプロセスCOMサーバーを 実装できるようにするためのフックです。``_ctypes``拡張dllが
   エクスポートしているDllGetClassObject関数から呼び出されます。


.. function:: FormatError([code])

   Windows用: エラーコードの説明文を返す。エラーコードが指定されない場合は、 Windows
   api関数GetLastErrorを呼び出して、もっとも新しいエラーコードが 使われます。


.. function:: GetLastError()

   Windows用: 呼び出し側のスレッド内でWindowsによって設定された 最新のエラーコードを返します。


.. function:: memmove(dst, src, count)

   標準Cのmemmoveライブラリ関数と同じもの: *count*バイトを ``src``から*dst*へコピーします。*dst*と``src``は
   ポインタへ変換可能な整数またはctypesインスタンスでなければなりません。


.. function:: memset(dst, c, count)

   標準Cのmemsetライブラリ関数と同じもの: アドレス*dst*の メモリブロックを値*c*を*count*バイト分書き込みます。
   *dst*はアドレスを指定する整数またはctypesインスタンスである 必要があります。


.. function:: POINTER(type)

   このファクトリ関数は新しいctypesポインタ型を作成して返します。 ポインタ型はキャッシュされ、内部で再利用されます。したがって、この関数を
   繰り返し呼び出してもコストは小さいです。型はctypes型でなければなりません。


.. function:: pointer(obj)

   この関数は``obj``を指す新しいポインタインスタンスを作成します。 戻り値はPOINTER(type(obj))型のオブジェクトです。

   注意: 外部関数呼び出しへオブジェクトへのポインタを渡したいだけなら、 はるかに高速な``byref(obj)``を使うべきです。


.. function:: resize(obj, size)

   この関数はobjの内部メモリバッファのサイズを変更します。 objはctypes型のインスタンスでなければなりません。
   バッファをsizeof(type(obj))で与えられるオブジェクト型の 本来のサイズより小さくすることはできませんが、バッファを 拡大することはできます。


.. function:: set_conversion_mode(encoding, errors)

   この関数は8ビット文字列とユニコード文字列の間で変換するときに 使われる規則を設定します。encodingは``'utf-8'``や``'mbcs'``のような
   エンコーディングを指定する文字列でなければなりません。 errorsはエンコーディング/デコーディングエラーについての
   エラー処理を指定する文字列でなければなりません。 指定可能な値の例としては、``"strict"``、``"replace"``または
   ``"ignore"``があります。

   ``set_conversion_mode``は以前の変換規則を含む2要素タプルです。 windowsでは初期の変換規則は``('mbcs',
   'ignore')``であり、 他のシステムでは``('ascii', 'strict')``です。


.. function:: sizeof(obj_or_type)

   ctypes型もしくはインスタンスのメモリバッファのサイズをバイト単位で 返します。Cの``sizeof()``関数と同じ動作です。


.. function:: string_at(address[, size])

   この関数はメモりアドレスaddressから始まる文字列を返します。 sizeが指定された場合はサイズとして使われます。指定されなければ、
   文字列がゼロ終端されていると仮定します。


.. function:: WinError(code=None, descr=None)

   Windows用: この関数はctypesの中でもおそらく最悪な名前がつけれたものです。
   WindowsErrorのインスタンスを作成します。*code*が指定されないならば、
   エラーコードを決めるために``GetLastError``が呼び出されます。 ``descr``が指定されないならば、:func:`FormatError`が
   エラーの説明文を得るために呼び出されます。


.. function:: wstring_at(address)

   この関数はユニコード文字列としてメモリアドレス``address``から始まる ワイドキャラクタ文字列を返します。``size``が指定されたならば、
   文字列の文字数として使われます。指定されなければ、 文字列がゼロ終端されていると仮定します。


.. _ctypes-data-types:

データ型
^^^^^^^^


.. class:: _CData

   この非公開クラスはすべてのctypesデータ型の共通のベースクラスです。 他のものに取り込まれることで、すべてのctypes型インスタンスがはC互換データを
   保持するメモリブロックを内部に持ちます。 メモリブロックのアドレスを``addressof()``ヘルパー関数が
   返さします。別のインスタンス変数は:attr:`_objects`として 公開されます。これはメモリブロックがポインタを含む場合に
   存続し続ける必要のある他のPythonオブジェクトを含んでいます。

ctypesデータ型の共通メソッド、すべてのクラスメソッドが存在します(正確には、 メタクラスのメソッドです):


.. method:: _CData.from_address(address)

   このメソッドはaddressによって指定されたメモリを使用している ctypes型のインスタンスを返します。addressは整数でなければならない。


.. method:: _CData.from_param(obj)

   このメソッドはobjをctypes型に適合させます。その型が外部関数の :attr:`argtypes`タプルに存在する場合に、実際の外部関数呼び出しに
   使われるオブジェクトを与えて呼び出します。 関数呼び出しパラメータとして使えるオブジェクトを返さなければなりません。

   すべてのctypesデータ型にはこのクラスメソッドのデフォルト実装が存在し、 通常は``obj``がその型のインスタンスならそのままを返します。
   いくつかの型は他のオブジェクトも受け取ります。


.. method:: _CData.in_dll(library, name)

   このメソッドは共有ライブラリがエクスポートするctypes型のインスタンスを 返します。*name*はデータをエクスポートしているシンボル名であり、
   *library*はロードされた共有ライブラリです。

ctypesデータ型に共通のインスタンス変数:


.. attribute:: _CData._b_base_

   時にはctypesデータインスタンスは自信が含まれるメモリブロックを持たないことがあります。 その代わり、ベースオブジェクトのメモリブロックの一部を共有します。
   :attr:`_b_base_`読み出し専用メンバーがメモリブロックを保有している ルートctypesオブジェクトです。


.. attribute:: _CData._b_needsfree_

   ctypesデータインスタンスが確保したメモリブロック自体を保有している場合、 この読み出し専用変数は真であり、それ以外では偽です。


.. attribute:: _CData._objects

   このメンバーは``None``またはPythonオブジェクトが含まれる辞書であり、 Pythonオブジェクトはメモリブロックの内容を有効に保つために、
   生き続けている必要があります。このオブジェクトはデバッギングのために エクスポートされているだけです。この辞書の内容を決して変更してはいけません。


.. _ctypes-fundamental-data-types:

基本データ型
^^^^^^^^^^^^


.. class:: _SimpleCData

   この非公開クラスはすべての基本ctypesデータ型のベースクラスです。 ここでこのクラスに触れたのは、基本ctypesデータ型の共通属性を含んでいるからです。
   ``_SimpleCData``は``_CData``のサブクラスですので、 そのメソッドと属性を継承しています。

インスタンスはただ一つの属性を持ちます:


.. attribute:: _SimpleCData.value

   この属性にはインスタンスの実際の値が入っています。それは 整数とポインタ型に対しては整数、文字型に対しては 一文字だけの文字列、文字ポインタ型に対しては
   Python文字列またはユニコード文字列です。

   ``value``属性をctypesインスタンスから取り出したとき、 たいていは新しいオブジェクトがその都度返されます。``ctypes``は
   元のオブジェクトを戻すことは*しません*。常に新しいオブジェクトが 作られます。同じことはすべての他のctypesオブジェクトインスタンスに
   対しても当てはまります。

基本データ型は、外部関数呼び出しの結果として返されたときや、 例えば構造体のフィールドメンバーや配列要素を取り出すときに、
ネイティブのPython型へ透過的に変換されます。言い換えると、 外部関数が:class:`c_char_p`の:attr:`restype`を持つ場合は、
:class:`c_char_p`インスタンスでは*なく*常にPython文字列を 受け取ることでしょう。

基本データ型のサブクラスはこの振る舞いを継承*しません*。 したがって、外部関数の:attr:`restype`が:class:`c_void_p`の
サブクラスならば、関数呼び出しからこのサブクラスのインスタンスを 受け取ります。もちろん、``value``属性にアクセスしてポインタの値を
得ることができます。

これらが基本データ型です:


.. class:: c_byte

   Cのsigned charデータ型を表し、小整数として値を解釈します。 コンストラクタはオプションの整数初期化子を受け取ります。
   オーバーフローのチェックは行われません。


.. class:: c_char

   C charデータ型を表し、単一の文字として値を解釈します。 コンストラクタはオプションの文字列初期化子を受け取り、
   その文字列の長さちょうど一文字である必要があります。


.. class:: c_char_p

   C char \*データ型を表し、ゼロ終端文字列へのポインタで なければなりません。コンストラクタは整数のアドレスもしくは 文字列を受け取ります。


.. class:: c_double

   C doubleデータ型を表します。コンストラクタはオプションの 浮動小数点数初期化子を受け取ります。


.. class:: c_float

   C floatデータ型を表します。コンストラクタはオプションの 浮動小数点数初期化子を受け取ります。


.. class:: c_int

   C signed intデータ型を表します。コンストラクタはオプションの 整数初期化子を受け取ります。オーバーフローのチェックは行われません。
   ``sizeof(int) == sizeof(long)``であるプラットホームでは、 :class:`c_long`の別名です。


.. class:: c_int8

   C 8-bit ``signed int``データ型を表します。たいていは、 :class:`c_byte`の別名です。


.. class:: c_int16

   C 16-bit signed intデータ型を表します。たいていは、 :class:`c_short`の別名です。


.. class:: c_int32

   C 32-bit signed intデータ型を表します。たいていは、 :class:`c_int`の別名です。


.. class:: c_int64

   C 64-bit ``signed int``データ型を表します。たいていは、 :class:`c_longlong`の別名です。


.. class:: c_long

   C ``signed long``データ型を表します。コンストラクタはオプションの 整数初期化子を受け取ります。オーバーフローのチェックは行われません。


.. class:: c_longlong

   C ``signed long long``データ型を表します。コンストラクタはオプションの
   整数初期化子を受け取ります。オーバーフローのチェックは行われません。


.. class:: c_short

   C ``signed short``データ型を表します。コンストラクタはオプションの 整数初期化子を受け取ります。オーバーフローのチェックは行われません。


.. class:: c_size_t

   C ``size_t``データ型を表します。


.. class:: c_ubyte

   C ``unsigned char``データ型を表します。その値は小整数として 解釈されます。コンストラクタはオプションの整数初期化子を
   受け取ります。オーバーフローのチェックは行われません。


.. class:: c_uint

   C ``unsigned int``データ型を表します。コンストラクタはオプションの 整数初期化子を受け取ります。オーバーフローのチェックは行われません。
   ``sizeof(int) == sizeof(long)``であるプラットホームでは、 :class:`c_ulong`の別名です。


.. class:: c_uint8

   C 8-bit unsigned intデータ型を表します。たいていは、 :class:`c_ubyte`の別名です。


.. class:: c_uint16

   C 16-bit unsigned intデータ型を表します。たいていは、 :class:`c_ushort`の別名です。


.. class:: c_uint32

   C 32-bit unsigned intデータ型を表します。たいていは、 :class:`c_uint`の別名です。


.. class:: c_uint64

   C 64-bit unsigned intデータ型を表します。たいていは、 :class:`c_ulonglong`の別名です。


.. class:: c_ulong

   C ``unsigned long``データ型を表します。コンストラクタはオプションの 整数初期化子を受け取ります。オーバーフローのチェックは行われません。


.. class:: c_ulonglong

   C ``unsigned long long``データ型を表します。コンストラクタは オプションの整数初期化子を受け取ります。オーバーフローのチェックは
   行われません。


.. class:: c_ushort

   C ``unsigned short``データ型を表します。コンストラクタはオプションの 整数初期化子を受け取ります。オーバーフローのチェックは行われません。


.. class:: c_void_p

   C ``void *``データ型を表します。値は整数として表されます。 コンストラクタはオプションの整数初期化子を受け取ります。


.. class:: c_wchar

   C ``wchar_t``データ型を表し、値はユニコード文字列の 単一の文字として解釈されます。コンストラクタはオプションの
   文字列初期化子を受け取り、その文字列の長さはちょうど 一文字である必要があります。


.. class:: c_wchar_p

   C ``wchar_t *``データ型を表し、ゼロ終端ワイド文字列への ポインタでなければなりません。コンストラクタは整数のアドレス
   もしくは文字列を受け取ります。


.. class:: c_bool

   C ``bool``データ型(より正確には、C99の_Bool)を表します。 その値はTrueまたはFalseであり、コンストラクタは
   どんなオブジェクト(真値を持ちます)でも受け取ります。

   .. versionadded:: 2.6


.. class:: HRESULT

   Windows用: :class:`HRESULT`値を表し、関数またはメソッド呼び出しに対する 成功またはエラーの情報を含んでいます。


.. class:: py_object

   C ``PyObject *``データ型を表します。引数なしでこれを呼び出すと ``NULL`` ``PyObject *``ポインタを作成します。

``ctypes.wintypes``モジュールは他のWindows固有のデータ型を提供します。
例えば、``HWND``、``WPARAM``または``DWORD``です。 ``MSG``や``RECT``のような有用な構造体も定義されています。


.. _ctypes-structured-data-types:

標準データ型
^^^^^^^^^^^^


.. class:: Union(*args, **kw)

   ネイティブのバイトオーダーでの共用体のための抽象ベースクラス。


.. class:: BigEndianStructure(*args, **kw)

   *ビックエンディアン*バイトオーダーでの構造体のための抽象ベースクラス。


.. class:: LittleEndianStructure(*args, **kw)

   *リトルエンディアン*バイトオーダーでの構造体のための抽象ベースクラス。

ネイティブではないバイトオーダーを持つ構造体にポインタ型フィールドあるいは ポインタ型フィールドを含む他のどんなデータ型をも入れることはできません。


.. class:: Structure(*args, **kw)

   *ネイティブ*のバイトオーダーでの構造体のための抽象ベースクラス。

具象構造体型と具象共用体型はこれらの型の一つをサブクラス化することで 作らなければなりません。少なくとも、:attr:`_fields_`クラス変数を
定義する必要があります。``ctypes``は、属性に直接アクセスしてフィールドを 読み書きできるようにする記述子を作成するでしょう。これらは、


.. attribute:: Structure._fields_

   構造体のフィールドを定義するシーケンス。要素は2要素タプルか3要素タプルで なければなりません。第一要素はフィールドの名前です。
   第二要素はフィールドの型を指定します。それはどんなctypesデータ型でも 構いません。

   :class:`c_int`のような整数型のために、オプションの第三要素を 与えることができます。フィールドのビット幅を定義する
   正の小整数である必要があります。

   一つの構造体と共用体の中で、フィールド名はただ一つである必要があります。 これはチェックされません。名前が繰り返しでてきたときにアクセスできるのは
   一つのフィールドだけです。

   Structureサブクラスを定義するクラス文の*後で*、 :attr:`_fields_`クラス変数を定義することができます。
   これにより自身を直接または間接的に参照するデータ型を 作成できるようになります::

      class List(Structure):
          pass
      List._fields_ = [("pnext", POINTER(List)),
                       ...
                      ]

   しかし、:attr:`_fields_`クラス変数はその型が最初に使われる
   (インスタンスが作成される、それに対して``sizeof()``が呼び出されるなど)より前に
   定義されていなければなりません。その後:attr:`_fields_`クラス変数へ代入すると AttributeErrorが発生します。

   構造体および共用体サブクラスは位置引数と名前付き引数の両方を受け取ります。 位置引数は:attr:`_fields_`定義中に現れたのと同じ順番で
   フィールドを初期化するために使われ、 名前付き引数は対応する名前を使ってフィールドを初期化するために 使われます。

   構造体型のサブクラスを定義することができ、もしあるならサブクラス内で 定義された:attr:`_fields_`に加えて、ベースクラスのフィールドも
   継承します。


.. attribute:: Structure._pack_

   インスタンスの構造体フィールドのアライメントを上書きできるようにする オブションの小整数。:attr:`_pack_`は:attr:`_fields_`が
   代入されたときすでに定義されていなければならない。そうでなければ、 何ら影響はありません。


.. attribute:: Structure._anonymous_

   無名(匿名)フィールドの名前が並べあげられたオプションのシーケンス。 :attr:`_fields_`が代入されたとき、``_anonymous_``がすでに
   定義されていなければならない。そうでなければ、何ら影響はありません。

   この変数に並べあげられたフィールドは構造体型もしくは共用体型フィールドで ある必要があります。構造体フィールドまたは共用体フィールドを作る必要なく、
   入れ子になったフィールドに直接アクセスできるようにするために、 ``ctypes``は構造体型の中に記述子を作成します。

   型の例です(Windows)::

      class _U(Union):
          _fields_ = [("lptdesc", POINTER(TYPEDESC)),
                      ("lpadesc", POINTER(ARRAYDESC)),
                      ("hreftype", HREFTYPE)]

      class TYPEDESC(Structure):
          _fields_ = [("u", _U),
                      ("vt", VARTYPE)]

          _anonymous_ = ("u",)

   ``TYPEDESC``構造体はCOMデータ型を表現しており、``vt``フィールドは 共用体フィールドのどれが有効であるかを指定します。``u``フィールドは
   匿名フィールドとして定義されているため、TYPEDESCインスタンスから取り除かれて そのメンバーへ直接アクセスできます。
   ``td.lptdesc``と``td.u.lptdesc``は同等ですが、前者がより高速です。 なぜなら一時的な共用体インスタンスを作る必要がないためです::

      td = TYPEDESC()
      td.vt = VT_PTR
      td.lptdesc = POINTER(some_type)
      td.u.lptdesc = POINTER(some_type)

構造体のサブ-サブクラスを定義することができ、ベースクラスのフィールドを 継承します。サブクラス定義に別の:attr:`_fields_`変数がある場合は、
この中で指定されたフィールドはベースクラスのフィールドへ追加されます。

構造体と共用体のコンストラクタは位置引数とキーワード引数の両方を受け取ります。
位置引数は:attr:`_fields_`の中に現れたのと同じ順番でメンバーフィールドを
初期化するために使われます。コンストラクタのキーワード引数は属性代入として解釈され、 そのため、同じ名前をもつ:attr:`_fields_`を初期化するか、
:attr:`_fields_`に存在しない名前に対しては新しい属性を作ります。


.. _ctypes-arrays-pointers:

配列とポインタ
^^^^^^^^^^^^^^

未作成 - チュートリアルの節 :ref:`ctypes-pointers`ポインタと 節 :ref:`ctypes-arrays`配列を参照してください。

