:mod:`__future__` --- Future ステートメントの定義
=================================================

.. module:: __future__
   :synopsis: Future ステートメントの定義


:mod:`__future__` は実際にモジュールであり、3つの役割があります。

* import ステートメントを解析する既存のツールを混乱させるのを避け、
  そのステートメントがインポートしようとしているモジュールを見つけられるようにするため。

* 2.1 以前のリリースで future ステートメントが実行されれば、最低でもランタイム例外を投げるようにするため。
  (:mod:`__future__` はインポートできません。というのも、2.1 以前にはそういう名前のモジュールはなかったからです。)

* いつ互換でない変化が導入され、いつ強制的になる -- あるいは、なった -- のか文書化するため。
  これは実行できる形式で書かれたドキュメントでなので、:mod:`__future__`
  をインポートし、その中身を調べるようプログラムすれば確かめられます。

:file:`__future__.py` の各ステートメントは次のような形をしています::

   FeatureName = _Feature(OptionalRelease, MandatoryRelease,
                          CompilerFlag)


ここで、普通は、 *OptionalRelease* は *MandatoryRelease* より小さく、2つとも ``sys.version_info``
と同じフォーマットの5つのタプルからなります。 ::

   (PY_MAJOR_VERSION, # the 2 in 2.1.0a3; an int
    PY_MINOR_VERSION, # the 1; an int
    PY_MICRO_VERSION, # the 0; an int
    PY_RELEASE_LEVEL, # "alpha", "beta", "candidate" or "final"; string
    PY_RELEASE_SERIAL # the 3; an int
   )

*OptionalRelease* はその機能が導入された最初のリリースを記録します。

まだ時期が来ていない *MandatoryRelease* の場合、 *MandatoryRelease* はその機能が言語の一部となるリリースを記します。

その他の場合、 *MandatoryRelease* はその機能がいつ言語の一部になったのかを記録します。
そのリリースから、あるいはそれ以降のリリースでは、この機能を使う際に
future ステートメントは必要ではありませんが、future ステートメントを使い続けても構いません。

*MandatoryRelease* は ``None`` になるかもしれません。つまり、予定された機能が破棄されたということです。

:class:`_Feature` クラスのインスタンスには対応する2つのメソッド、 :meth:`getOptionalRelease` と
:meth:`getMandatoryRelease` があります。

*CompilerFlag* は動的にコンパイルされるコードでその機能を有効にするために、組み込み関数 :func:`compile`
の第4引数に渡されなければならない (ビットフィールド)フラグです。このフラグは :class:`_Feature` インスタンスの
:attr:`compilier_flag` 属性に保存されています。

:mod:`__future__` で解説されている機能のうち、削除されたものはまだありません。

