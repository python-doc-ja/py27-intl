.. highlightlang:: c

.. _string-conversion:

文字列の変換と書式化
================================

数値変換と、書式化文字列出力のための関数群


.. cfunction:: int PyOS_snprintf(char *str, size_t size,  const char *format, ...)

   書式化文字列 *format* と追加の引数から、 *size* バイトを超えない文字列を
   *str* に出力します。
   Unix man page の :manpage:`snprintf(2)` を参照してください。


.. cfunction:: int PyOS_vsnprintf(char *str, size_t size, const char *format, va_list va)

   書式化文字列 *format* と可変長引数リスト *va* から、 *size* バイトを超えない文字列を
   *str* に出力します。
   Unix man page の :manpage:`vsnprintf(2)` を参照してください。

:c:func:`PyOS_snprintf` と :c:func:`PyOS_vsnprintf` は標準Cライブラリの
:c:func:`snprintf` と :c:func:`vsnprintf` 関数をラップします。
これらの関数の目的は、C標準ライブラリが保証していないコーナーケースでの
動作を保証することです。

これらのラッパ関数は、戻るときに *str*[*size*-1] が常に ``'\0'`` であることを保証します。
(str の末尾の ``'\0'`` を含めて) *size* バイト以上を書き込みません。
``str != NULL``, ``size > 0``, ``format != NULL`` を要求します。


もし :c:func:`vsnprintf` のないプラットフォームで、切り捨てを避けるために必要な
バッファサイズが *size* を512バイトより大きく超過していれば、 Python は
*Py_FatalError* で abort します。

The return value (*rv*) for these functions should be interpreted as follows:
これらの関数の戻り値 (*rv*) は次のように解釈されなければなりません:

* ``0 <= rv < size`` のとき、変換出力は成功して、 (最後の *str*[*rv*] にある
  ``'\0'`` を除いて) *rv* 文字が *str* に出力された。

* ``rv >= size`` のとき、変換出力は切り詰められており、成功するためには ``rv + 1``
  バイトが必要だったことを示します。 *str*[*size*-1] は ``'\0'`` です。

* ``rv < 0`` のときは、何か悪いことが起こった時です。この場合でも *str*[*size*-1]
  は ``'\0'`` ですが、 *str* のそれ以外の部分は未定義です。エラーの正確な原因は
  プラットフォーム依存です。

以下の関数は locale 非依存な文字列から数値への変換を行ないます。


.. cfunction:: double PyOS_ascii_strtod(const char *nptr, char **endptr)

   文字列を :c:type:`double` へ変換します。
   この関数は、C locale におけるC標準の :c:func:`strtod` と同じように動作します。
   スレッドセーフのために、この関数は現在の locale を変更せずに実装されています。

   :c:func:`PyOS_ascii_strtod` は通常、設定ファイルを読み込むときや、ロケール独立な
   非ユーザーからの入力を読み込むときに使われるべきです。

   .. versionadded:: 2.4

   詳細は Unix man page の :manpage:`strtod(2)` を参照してください。


.. cfunction:: char * PyOS_ascii_formatd(char *buffer, size_t buf_len, const char *format, double d)

   :c:type:`double` を ``'.'`` を小数点記号に利用して文字列に変換します。
   *format* は数値のフォーマットを指定する :c:func:`printf` スタイルの文字列です。
   利用できる変換文字は ``'e'``, ``'E'``, ``'f'``, ``'F'``, ``'g'``, ``'G'`` です。

   戻り値は、変換された文字列が格納された *buffer* へのポインタか、失敗した場合は NULL です。

   .. versionadded:: 2.4


.. cfunction:: double PyOS_ascii_atof(const char *nptr)

   文字列を、 locale 非依存な方法で :c:type:`double` へ変換します。

   .. versionadded:: 2.4

   詳細は Unix man page の :manpage:`atof(2)` を参照してください。


.. cfunction:: char * PyOS_stricmp(char *s1, char *s2)

   大文字/小文字を区別しない文字列比較。
   大文字/小文字を無視する以外は、 :c:func:`strcmp` と同じ動作をします。

   .. versionadded:: 2.6


.. cfunction:: char * PyOS_strnicmp(char *s1, char *s2, Py_ssize_t  size)

   大文字/小文字を区別しない文字列比較。
   大文字/小文字を無視する以外は、 :c:func:`strncmp` と同じ動作をします。

   .. versionadded:: 2.6
