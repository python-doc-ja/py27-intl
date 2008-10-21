
:mod:`pyclbr` --- Python クラスブラウザーサポート
=================================================

.. module:: pyclbr
   :synopsis: Pythonクラスデスクリプタの情報抽出サポート


.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


この:mod:`pyclbr`はモジュールで定義されたクラス、メソッド、および トップレベルの関数について、限られた量の情報を定義するのに使われます。
このクラスによって提供される情報は、伝統的な 3 ペイン形式の クラスブラウザーを実装するのに十分なだけの量になります。
情報はモジュールのインポートによらず、ソースコードから抽出します。 このため、このモジュールは信用できないソースコードに対して利用しても
安全です。この制限から、多くの標準モジュールやオプションの拡張 モジュールを含む、Python で実装されていないモジュールに対して 利用することはできません。


.. function:: readmodule(module[, path])

   モジュールを読み込み、辞書マッピングクラスを返し、 クラス記述オブジェクトに名前をつけます。
   パラメタ*module*はモジュール名を表す文字列でなくてはなりません; パッケージ内のモジュール名でもかまいません。 *path*
   パラメタはシーケンス型でなくてはならず、 モジュールのソースコード がある場所を特定する際に ``sys.path`` の値に補完する形で使われます。

   .. % この'インパッケージ'パラメーターは内部的な用途のみのようです...


.. function:: readmodule_ex(module[, path])

   :func:`readmodule` に似ていますが、返される辞書は、クラス名から クラス記述オブジェクトへの対応付けに加えて、トップレベル関数から
   関数記述オブジェクトへの対応付けも行っています。さらに、読み出し対象の モジュールがパッケージの場合、返される辞書はキー ``'__path__'``
   を持ち、その値はパッケージの検索パスが入ったリストになります。

   .. % The 'inpackage' parameter appears to be for internal use only....


.. _pyclbr-class-objects:

クラス記述オブジェクト
----------------------

クラス記述オブジェクトは、:func:`readmodule` や :func:`readmodule()_ex` が返す辞書の値として
使われており、以下のデータメンバを提供しています。


.. attribute:: class descriptor.module

   クラス記述オブジェクトが記述している対象のクラスを定義している モジュールの名前です。


.. attribute:: class descriptor.name

   クラスの名前です。


.. attribute:: class descriptor.super

   クラス記述オブジェクトが記述しようとしている対象クラスの、直接の基底 クラス群について記述しているクラス記述オブジェクトのリストです。
   スーパクラスとして挙げられているが :func:`readmodule` が見つけ られなかったクラスは、クラス記述オブジェクトではなくクラス名として
   リストに挙げられます。


.. attribute:: class descriptor.methods

   メソッド名を行番号に対応付ける辞書です。


.. attribute:: class descriptor.file

   クラスを定義している ``class`` 文が入っているファイルの名前です。


.. attribute:: class descriptor.lineno

   :attr:`file` で指定されたファイル内にある ``class`` 文の数です。


.. _pyclbr-function-objects:

関数記述オブジェクト (Function Descriptor Object)
-------------------------------------------------

:func:`readmodule_ex` の返す辞書内でキーに対応する値として使われて いる関数記述オブジェクトは、以下のデータメンバを提供しています:


.. attribute:: function descriptor.module

   関数記述オブジェクトが記述している対象の関数を定義している モジュールの名前です。


.. attribute:: function descriptor.name

   関数の名前です。


.. attribute:: function descriptor.file

   関数を定義してる ``def`` 文が入っているファイルの名前です。


.. attribute:: function descriptor.lineno

   :attr:`file` で指定されたファイル内にある ``def`` 文の数です。

