
:mod:`pyclbr` --- Python クラスブラウザーサポート
=================================================

.. module:: pyclbr
   :synopsis: Python クラスデスクリプタの情報抽出サポート


.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


この :mod:`pyclbr` モジュールはモジュールで定義されたクラス、メソッド、およびトップレベルの関数について、限られた量の情報を定義するのに使われます。
このクラスによって提供される情報は、伝統的な 3 ペイン形式のクラスブラウザーを実装するのに十分なだけの量になります。
情報はモジュールのインポートによらず、ソースコードから抽出します。このため、このモジュールは信用できないソースコードに対して利用しても安全です。
この制限から、多くの標準モジュールやオプションの拡張モジュールを含む、Python で実装されていないモジュールに対して利用することはできません。


.. function:: readmodule(module[, path=None])

   モジュールを読み込み、辞書マッピングクラスを返し、クラス記述オブジェクトに名前をつけます。
   パラメタ *module* はモジュール名を表す文字列でなくてはなりません;
   パッケージ内のモジュール名でもかまいません。
   *path* パラメタはシーケンス型でなくてはならず、モジュールのソースコード\
   がある場所を特定する際に ``sys.path`` の値に補完する形で使われます。


.. function:: readmodule_ex(module[, path=None])

   :func:`readmodule` に似ていますが、返される辞書は、クラス名から\
   クラス記述オブジェクトへの対応付けに加えて、トップレベル関数から\
   関数記述オブジェクトへの対応付けも行っています。さらに、読み出し対象の\
   モジュールがパッケージの場合、返される辞書はキー ``'__path__'``
   を持ち、その値はパッケージの検索パスが入ったリストになります。


.. _pyclbr-class-objects:

Class オブジェクト
-------------------

:class:`Class` オブジェクトは、 :func:`readmodule` や :func:`readmodule_ex`
が返す辞書の値として使われており、以下のデータメンバを提供しています:


.. attribute:: Class.module

   クラス記述オブジェクトが記述している対象のクラスを定義しているモジュールの名前です。


.. attribute:: Class.name

   クラスの名前です。


.. attribute:: Class.super

   記述しようとしている対象クラスの、直接の基底クラス群について記述している
   :class:`Class` オブジェクトのリストです。
   スーパクラスとして挙げられているが :func:`readmodule` が見つけられなかったクラスは、
   :class:`Class` オブジェクトではなくクラス名の文字列としてリストに挙げられます。


.. attribute:: Class.methods

   メソッド名を行番号に対応付ける辞書です。


.. attribute:: Class.file

   クラスを定義している ``class`` 文が入っているファイルの名前です。


.. attribute:: Class.lineno

   :attr:`file` で指定されたファイルにおける ``class`` 文の行番号です。


.. _pyclbr-function-objects:

Function オブジェクト
----------------------

:class:`Function` オブジェクトは、 :func:`readmodule_ex`
が返す辞書内でキーに対応する値として使われており、以下のデータメンバを提供しています:


.. attribute:: Function.module

   関数記述オブジェクトが記述している対象の関数を定義しているモジュールの名前です。


.. attribute:: Function.name

   関数の名前です。


.. attribute:: Function.file

   関数を定義してる ``def`` 文が入っているファイルの名前です。


.. attribute:: Function.lineno

   :attr:`file` で指定されたファイルにおける ``def`` 文の行番号です。
