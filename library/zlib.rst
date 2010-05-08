
:mod:`zlib` --- :program:`gzip` 互換の圧縮
==========================================

.. module:: zlib
   :synopsis: gzip 互換の圧縮／解凍ルーチンへの低レベルインタフェース


このモジュールでは、データ圧縮を必要とするアプリケーションが zlib ライブラリを使って圧縮および解凍を行えるようにします。 zlib ライブラリ自体の
Webページは http://www.zlib.net です。 Pythonモジュールと zlib
ライブラリの1.1.3より前のバージョンには互換性のない部分があることが知られています。1.1.3にはセキュリティホールが存
在しますので、1.1.4以降のバージョンを利用することをお勧めします。

zlib の関数にはたくさんのオプションがあり、しばしば特定の順番で使う必要があります。
このドキュメントでは順番のことについて全てを説明し尽くそうとはしていません。信頼できる情報が必要ならば
http://www.zlib.net/manual.html にある zlib のマニュアルを参照するようにしてください。

.. For reading and writing ``.gz`` files see the :mod:`gzip` module. For
   other archive formats, see the :mod:`bz2`, :mod:`zipfile`, and
   :mod:`tarfile` modules.

``.gz`` ファイルの読み書きのためには、 :mod:`gzip` モジュールを参照してください。
その他のアーカイブフォーマットについては、 :mod:`bz2`, :mod:`zipfile`, :mod:`tarfile`
モジュールを参照してください。

このモジュールで利用可能な例外と関数を以下に示します:


.. exception:: error

   圧縮および解凍時のエラーによって送出される例外。


.. function:: adler32(data[, value])

   *data* のAdler-32 チェックサムを計算します。（Adler-32 チェックサムは、おおむね CRC32 と同等の信頼性を持ちながら
   はるかに高速に計算することができます。） *value* が与えられていれば、 *value* はチェックサム計算の
   初期値として使われます。それ以外の場合には固定のデフォルト値が使われます。この機能によって、複数の入力を結合したデータ全体
   にわたり、通しのチェックサムを計算することができます。このアルゴリズムは暗号法論的には強力とはいえないので、認証やデジタル
   署名などに用いるべきではありません。このアルゴリズムはチェックサムアルゴリズムとして用いるために設計されたものなので、汎用的な
   ハッシュアルゴリズムには向きません。

   .. This function always returns an integer object.

   この関数は常に整数オブジェクトを返します。

.. note::
   .. To generate the same numeric value across all Python versions and
      platforms use adler32(data) & 0xffffffff.  If you are only using
      the checksum in packed binary format this is not necessary as the
      return value is the correct 32bit binary representation
      regardless of sign.

   全てのPythonのバージョンとプラットフォームで共通な数値を正壊死するには、
   ``adler32(data) & 0xffffffff`` を利用してください。
   もしチェックサムをパックされたバイナリフォーマットのためにしか利用しないのであれば、
   符号が関係なくなり、32bitのバイナリ値としては戻り値は正しいので、この処理は必要ありません。

.. versionchanged:: 2.6
   .. The return value is in the range [-2**31, 2**31-1]
      regardless of platform.  In older versions the value is
      signed on some platforms and unsigned on others.

   戻り値の範囲は、プラットフォームに関係なく [-2**31, 2**31-1] になりました。
   古いバージョンでは、この値は幾つかのプラットフォームでは符号付き、
   別のプラットフォームでは符号なしになっていました。

.. versionchanged:: 3.0
   .. The return value is unsigned and in the range [0, 2**32-1]
      regardless of platform.

   戻り値の範囲は、プラットフォームに関係なく [0, 2**32-1] です。

.. function:: compress(string[, level])

   *string* で与えられた文字列を圧縮し、圧縮されたデータを含む文字列を返します。 *level* は ``1`` から ``9`` までの
   整数をとる値で、圧縮のレベルを制御します。 ``1`` は最も高速で最小限の圧縮を行います。 ``9`` はもっとも低速になりますが
   最大限の圧縮を行います。デフォルトの値は ``6`` です。圧縮時に何らかのエラーが発生した場合、 :exc:`error` 例外を送出します。


.. function:: compressobj([level])

   一度にメモリ上に置くことができないようなデータストリームを圧縮するための圧縮オブジェクトを返します。 *level* は ``1`` から ``9``
   までの整数で、圧縮レベルを制御します。 ``1`` はもっとも高速で最小限の圧縮を、 ``9`` はもっとも低速になりますが
   最大限の圧縮を行います。デフォルトの値は ``6`` です。


.. function:: crc32(data[, value])

   .. index::
      single: Cyclic Redundancy Check
      single: checksum; Cyclic Redundancy Check

   *data* の CRC (Cyclic Redundancy Check, 巡回符号方式)   チェックサムを計算します。 *value*
   が与えられていれば、チェックサム計算の初期値として使われます。与えられていなければデフォルトの初期値が使われます。 *value*
   を与えることで、複数の入力を結合したデータ全体にわたり、通しのチェックサムを計算することができます。
   このアルゴリズムは暗号法論的には強力ではなく、認証やデジタル署名に用いるべきではありません。アルゴリズムはチェックサムアルゴリズムと
   して設計されてえいるので、汎用のハッシュアルゴリズムには向きません。

   この関数は常に整数オブジェクトを返します。

.. note::
   .. To generate the same numeric value across all Python versions and
      platforms use crc32(data) & 0xffffffff.  If you are only using
      the checksum in packed binary format this is not necessary as the
      return value is the correct 32bit binary representation
      regardless of sign.

   全てのPythonのバージョンとプラットフォームで共通な数値を正壊死するには、
   ``crc32(data) & 0xffffffff`` を利用してください。
   もしチェックサムをパックされたバイナリフォーマットのためにしか利用しないのであれば、
   符号が関係なくなり、32bitのバイナリ値としては戻り値は正しいので、この処理は必要ありません。

.. versionchanged:: 2.6
   .. The return value is in the range [-2**31, 2**31-1]
      regardless of platform.  In older versions the value is
      signed on some platforms and unsigned on others.

   戻り値の範囲は、プラットフォームに関係なく [-2**31, 2**31-1] になりました。
   古いバージョンでは、この値は幾つかのプラットフォームでは符号付き、
   別のプラットフォームでは符号なしになっていました。

.. versionchanged:: 3.0
   .. The return value is unsigned and in the range [0, 2**32-1]
      regardless of platform.

   戻り値の範囲は、プラットフォームに関係なく [0, 2**32-1] です。


.. function:: decompress(string[, wbits[, bufsize]])

   *string* 内のデータを解凍して、解凍されたデータを含む文字列を返します。 *wbits* パラメタはウィンドウバッファの大きさを制御します。
   *bufsize* が与えられていれば、出力バッファの書記サイズとして使われます。解凍処理に何らかのエラーが生じた場合、 :exc:`error`
   例外を送出します。

   *wbits* の絶対値は、データを圧縮する際に用いられるヒストリバッファのサイズ (ウィンドウサイズ) に対し、 2 を底とする対数を
   とったものです。最近のほとんどのバージョンの zlib ライブラリを使っているなら、 *wbits* の絶対値は 8 から 15 とするべきです。
   より大きな値はより良好な圧縮につながりますが、より多くのメモリを必要とします。デフォルトの値は 15 です。 *wbits* の値が負の場合、標準的な
   :program:`gzip` ヘッダを出力しません。これは zlib ライブラリの非公開仕様であり、 :program:`unzip` の
   圧縮ファイル形式に対する互換性のためのものです。

   *bufsize* は解凍されたデータを保持するためのバッファサイズの初期値です。バッファの空きは必要に応じて必要なだけ増加するので、
   なれば、必ずしも正確な値を指定する必要はありません。この値のチューニングでできることは、 :cfunc:`malloc` が呼ばれる回数を
   数回減らすことぐらいです。デフォルトのサイズは 16384 です。


.. function:: decompressobj([wbits])

   メモリ上に一度に展開できないようなデータストリームを解凍するために用いられる解凍オブジェクトを返します。 *wbits* パラメタは
   ウィンドウバッファのサイズを制御します。

圧縮オブジェクトは以下のメソッドをサポートします:


.. method:: Compress.compress(string)

   *string* を圧縮し、圧縮されたデータを含む文字列を返します。この文字列は少なくとも *string* に相当します。このデータは以前に呼んだ
   :meth:`compress` が返した出力と結合することができます。入力の一部は以後の処理のために内部バッファに保存されることもあります。


.. method:: Compress.flush([mode])

   未処理の入力データが処理され、この未処理部分を圧縮したデータを含む文字列が返されます。 *mode* は定数 :const:`Z_SYNC_FLUSH` 、
   :const:`Z_FULL_FLUSH` 、または :const:`Z_FINISH` のいずれかをとり、デフォルト値は :const:`Z_FINISH`
   です。 :const:`Z_SYNC_FLUSH` および :const:`Z_FULL_FLUSH` ではこれ以後にもデータ文字列を圧縮できる
   モードです。一方、 :const:`Z_FINISH` は圧縮ストリームを閉じ、これ以後のデータの圧縮を禁止します。 *mode* に
   :const:`Z_FINISH` を設定して :meth:`flush` メソッドを呼び出した後は、 :meth:`compress`
   メソッドを再び呼ぶべきではありません。唯一の現実的な操作はこのオブジェクトを削除することだけです。


.. method:: Compress.copy()

   圧縮オブジェクトのコピーを返します。これを使うと先頭部分が共通している複数のデータを効率的に圧縮することができます。

   .. versionadded:: 2.5

解凍オブジェクトは以下のメソッドと 2 つの属性をサポートします:


.. attribute:: Decompress.unused_data

   圧縮データの末尾までのバイト列が入った文字列です。すなわち、この値は圧縮データの入っているバイト列の最後の文字までが読み出せるかぎり ``""``
   となります。入力文字列全てが圧縮データを含んでいた場合、この属性は ``""`` 、すなわち空文字列になります。

   圧縮データ文字列がどこで終了しているかを決定する唯一の方法は、実際にそれを解凍することです。つまり、大きなファイル
   の一部分に圧縮データが含まれているときに、その末端を調べるためには、データをファイルから読み出し、空でない文字列を後ろに続けて、
   :attr:`unused_data` が空文字列でなくなるまで、解凍オブジェクトの  :meth:`decompress`
   メソッドに入力しつづけるしかありません。


.. attribute:: Decompress.unconsumed_tail

   解凍されたデータを収めるバッファの長さ制限を超えたために、最も最近の :meth:`decompress` 呼び出しで処理しきれなかったデータを含む文字列です。
   このデータはまだ zlib 側からは見えていないので、正しい解凍出力を得るには以降の :meth:`decompress` メソッド呼び出しに
   (場合によっては後続のデータが追加された) データを差し戻さなければなりません。


.. method:: Decompress.decompress(string[, max_length])

   *string* を解凍し、少なくとも *string* の一部分に対応する解凍されたデータを含む文字列を返します。このデータは以前に
   :meth:`decompress` メソッドを呼んだ時に返された出力と結合することができます。入力データの一部分が以後の処理のために内部バッファに
   保存されることもあります。

   オプションパラメタ *max_length* が与えられると、返される解凍データの長さが *max_length* 以下に制限されます。このことは入力した圧縮
   データの全てが処理されるとは限らないことを意味し、処理されなかったデータは :attr:`unconsumed_tail` 属性に保存されます。
   解凍処理を継続したいならば、この保存されたデータを以降の :meth:`decompress` 呼び出しに渡さなくてはなりません。 *max_length*
   が与えられなかった場合、全ての入力が解凍され、 :attr:`unconsumed_tail` 属性は空文字列になります。


.. method:: Decompress.flush([length])

   未処理の入力データを全て処理し、最終的に圧縮されなかった残りの出力文字列を返します。 :meth:`flush` を呼んだ後、
   :meth:`decompress`  を再度呼ぶべきではありません。このときできる唯一現実的な操作はオブジェクトの削除だけです。

   オプション引数 *length* は出力バッファの初期サイズを決めます。


.. method:: Decompress.copy()

   解凍オブジェクトのコピーを返します。これを使うとデータストリームの途中にある解凍オブジェクトの状態を保存でき、未来のある時点で行なわれるストリームの
   ランダムなシークをスピードアップするのに利用できます。

   .. versionadded:: 2.5


.. seealso::

   Module :mod:`gzip`
      Reading and writing :program:`gzip` \ -format files.

   http://www.zlib.net
      zlib ライブラリホームページ

   http://www.zlib.net/manual.html
      zlib ライブラリの多くの関数の意味と使い方を解説したマニュアル

