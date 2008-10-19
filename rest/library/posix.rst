
:mod:`posix` --- 最も一般的な POSIX システムコール群
======================================

.. module:: posix
   :platform: Unix
   :synopsis: 最も一般的な POSIX システムコール群 (通常は os モジュールを介して利用されます)。


このモジュールはオペレーティングシステムの機能のうち、C 言語標準 および POSIX 標準 (Unix インタフェースをほんの少し隠蔽した)
で標準化されている機能に対するアクセス機構を提供します。

.. index:: module: os

**このモジュールを直接 import しないで下さい。** その代わりに、 移植性のあるインタフェースを提供している :mod:`os` をインポート
してください。Unixでは、 :mod:`os` モジュールが提供する インタフェースは :mod:`posix` の内容を内包しています。 非 Unix
オペレーティングシステムでは :mod:`posix` モジュール を使うことはできませんが、その部分的な機能セットは、たいてい :mod:`os`
インタフェースを介して利用することができます。 :mod:`os` は、一度 import してしまえば :mod:`posix` の代わり
であることによるパフォーマンス上のペナルティは *全くありません*。 その上、:mod:`os`  は ``os.environ`` の
内容が変更された際に自動的に :func:`putenv` を呼ぶなど、 いくつかの追加機能を提供しています。

以下の説明は非常に簡潔なものです; 詳細については、 Unix マニュアルの (または POSIX) ドキュメントの) 対応する項目を
参照してください。*path* で呼ばれる引数は文字列で与えられた パス名を表します。

エラーは例外として報告されます; よくある例外は型エラーです。 一方、システムコールから報告されたエラーは以下に述べるように :exc:`error`
(標準例外 :exc:`OSError` と同義です) を送出します。


.. _posix-large-files:

ラージファイルのサポート
------------

.. index::
   single: large files
   single: file; large files

.. sectionauthor:: Steve Clift <clift@mail.anacapa.net>


いくつかのオペレーティングシステム (AIX, HPIX, Irix および Solaris が含まれます) は、:ctype:`int` および
:ctype:`long` を 32 ビット値と する C プログラムモデルで 2Gb を超えるサイズのファイルのサポート
を提供しています。このサポートは典型的には 64 ビット値のオフセット 値と、そこからの相対サイズを定義することで実現しています。この
ようなファイルは時にラージファイル (:dfn:`large files`) と呼ばれます。

Python では、:ctype:`off_t` のサイズが :ctype:`long` より大きく、 かつ :ctype:`long long`
型を利用することができて、少なくとも  :ctype:`off_t` 型と同じくらい大きなサイズである場合、ラージファイルの
サポートが有効になります。この場合、ファイルのサイズ、オフセットおよび Python の通常整数型の範囲を超えるような値の表現には Python の長整数型が
使われます。例えば、ラージファイルのサポートは Irix の最近のバージョン では標準で有効ですが、Solaris 2.6 および 2.7 では、以下のように
する必要があります::

   CFLAGS="`getconf LFS_CFLAGS`" OPT="-g -O2 $CFLAGS" \
           ./configure

On large-file-capable Linux systems, this might work:

.. % $ <-- bow to font-lock

::

   CFLAGS='-D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64' OPT="-g -O2 $CFLAGS" \
           ./configure

.. % $ <-- bow to font-lock


.. _posix-contents:

モジュールの内容
--------

:mod:`posix` では以下のデータ項目を定義しています:


.. data:: environ

   インタプリタが起動した時点の環境変数文字列を表現する辞書です。 例えば、``environ['HOME']`` はホームディレクトリの パス名で、C 言語の
   ``getenv("HOME")`` と等価です。

   この辞書を変更しても、:func:`execv`、:func:`popen` または :func:`system`
   などに渡される環境変数文字列には影響しません; そうした環境を変更するする必要がある場合、``environ`` を  :func:`execve`
   に渡すか、:func:`system` または :func:`popen` の命令文字列に変数の代入や export 文を 追加してください。

   .. note::

      :mod:`os` モジュールでは、もう一つの ``environ``  実装を提供しており、環境変数が変更された場合、その内容を更新する
      ようになっています。``os.environ`` を更新した場合、この辞書は 古い内容を表していることになってしまうので、このことにも注意
      してください。:mod:`posix` モジュール版を直接アクセスするよりも、 :mod:`os` モジュール版を使う方が推奨されています。

このモジュールのその他の内容は :mod:`os` モジュールからのみの アクセスになっています; 詳しい説明は:mod:`os` モジュールの
ドキュメントを参照してください。

