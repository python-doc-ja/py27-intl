
:mod:`binascii` --- バイナリデータと ASCIIデータとの間での変換
==============================================================

.. module:: binascii
   :synopsis: バイナリと各種 ASCIIコード化バイナリ表現との間の 変換を行うツール群。


.. index::
   module: uu
   module: base64
   module: binhex

:mod:`binascii` モジュールにはバイナリと ASCIIコード化された バイナリ表現との間の変換を行うための多数のメソッドが含まれています。
通常、これらの関数を直接使う必要はなく、 :mod:`uu`、 :mod:`base64`や :mod:`binhex` といった、ラッパ(wrapper)
モジュールを使うことになるでしょう。 :mod:`binascii`モジュールは、高レベルなモジュールで利用される、高速
なCで書かれた低レベル関数を提供しています。

:mod:`binascii` モジュールでは以下の関数を定義します:


.. function:: a2b_uu(string)

   uuencode された 1 行のデータ をバイナリに変換し、変換後のバイナリ データを返します。最後の行を除いて、通常 1 行には(バイナリデータで)  45
   バイトが含まれます。入力データの先頭には空白文字が連続していても かまいません。


.. function:: b2a_uu(data)

   バイナリデータを uuencode して 1 行の ASCII 文字列に変換します。 戻り値は変換後の 1 行の文字列で、改行を含みます。*data* の長さは
   45 バイト以下でなければなりません。


.. function:: a2b_base64(string)

   base64 でエンコードされたデータのブロックをバイナリに変換し、 変換後のバイナリデータを返します。一度に 1 行以上のデータを 与えてもかまいません。


.. function:: b2a_base64(data)

   バイナリデータを base64 でエンコードして 1 行の ASCII 文字列に 変換します。戻り値は変換後の 1 行の文字列で、改行文字を含みます。
   base64 標準を遵守するためには、*data* の長さは 57 バイト以下で なくてはなりません。


.. function:: a2b_qp(string[, header])

   quoted-printable 形式のデータをバイナリに変換し、バイナリデータを 返します。一度に 1 行以上のデータを渡すことができます。 オプション引数
   *header* が与えられており、かつその値が真であれば、 アンダースコアは空白文字にデコードされます。


.. function:: b2a_qp(data[, quotetabs, istext, header])

   バイナリデータを quoted-printable 形式でエンコードして 1 行から複数行の ASCII 文字列に変換します。変換後の文字列を返します。
   オプション引数 *quptetabs* が存在し、かつその値が真であれば、 全てのタブおよび空白文字もエンコードされます。オプション引数  *istext*
   が存在し、かつその値が真であれば、改行はエンコードされま せんが、行末の空白文字はエンコードされます。 オプション引数
   *header*が存在し、かつその値が真である場合、空白文 字はRFC1522にしたがってアンダースコアにエンコードされます。 オプション引数
   *header*が存在し、かつその値が偽である場合、改行文字も同様にエンコードされます。 そうでない場合、復帰 (linefeed)
   文字の変換によってバイナリデータ ストリームが破損してしまうかもしれません。


.. function:: a2b_hqx(string)

   binhex4 形式の ASCII 文字列データを RLE 展開を行わないでバイナリに 変換します。文字列はバイナリのバイトデータを完全に含むような長さか、
   または (binhex4 データの最後の部分の場合) 余白のビットがゼロになって いなければなりません。


.. function:: rledecode_hqx(data)

   *data* に対し、binhex4 標準に従って RLE 展開を行います。 このアルゴリズムでは、あるバイトの後ろに ``0x90`` がきた場合、
   そのバイトの反復を指示しており、さらにその後ろに反復カウントが 続きます。カウントが ``0`` の場合 ``0x90`` 自体を示します。
   このルーチンは入力データの末端における反復指定が不完全でない かぎり解凍されたデータを返しますが、不完全な場合、例外 :exc:`Incomplete`
   が送出されます。


.. function:: rlecode_hqx(data)

   binhex4 方式の RLE 圧縮を *data* に対して行い、その結果を 返します。


.. function:: b2a_hqx(data)

   バイナリを hexbin4 エンコードして ASCII 文字列に変換し、変換後の 文字列を返します。引数の *data* はすでに RLE エンコードされて
   いなければならず、その長さは (最後のフラグメントを除いて) 3 で 割り切れなければなりません。


.. function:: crc_hqx(data, crc)

   *data* の binhex4 CRC 値を計算します。初期値は *crc* で、計算 結果を返します。


.. function:: crc32(data[, crc])

   32 ビットチェックサムである CRC-32 を *data* に対して計算します。 初期値は *crc* です。これは ZIP
   ファイルのチェックサムと同じです。 このアルゴリズムはチェックサムアルゴリズムとして設計されたもので、
   一般的なハッシュアルゴリズムには向きません。以下のようにして使います::

      print binascii.crc32("hello world")
      # Or, in two pieces:
      crc = binascii.crc32("hello")
      crc = binascii.crc32(" world", crc)
      print crc


.. function:: b2a_hex(data)
              hexlify(data)

   バイナリデータ *data* の16進数表現を返します。*data* の各 バイトは対応する 2 桁の16進数表現に変換されます。従って、変換結果の
   文字列は*data* の 2 倍の長さになります。


.. function:: a2b_hex(hexstr)
              unhexlify(hexstr)

   16 進数表記の文字列 *hexstr* の表すバイナリデータを返します。 この関数は :func:`b2a_hex` の逆です。*hexstr* は
   16進数字 (大文字でも小文字でもかまいません) を偶数個含んでいなければ なりません。そうでないばあい、例外 :exc:`TypeError` が送出
   されます。


.. exception:: Error

   エラーが発生した際に送出される例外です。通常はプログラムのエラーです。


.. exception:: Incomplete

   変換するデータが不完全な場合に送出される例外です。通常はプログラムの エラーではなく、多少追加読み込みを行って再度変換 を試みることで対処できます。


.. seealso::

   Module :mod:`base64`
      MIME 電子メールメッセージで使われる base64 エンコードのサポート。

   Module :mod:`binhex`
      Macintosh で使われる binhex フォーマットのサポート。

   Module :mod:`uu`
      Unixで使われる UU エンコードのサポート。

   Module :mod:`quopri`
      MIME 電子メールメッセージで使われる quoted-printable エンコードのサポート。

