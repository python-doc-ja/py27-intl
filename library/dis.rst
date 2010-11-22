
:mod:`dis` --- Pythonバイトコードの逆アセンブラ
===============================================

.. module:: dis
   :synopsis: Pythonバイトコードの逆アセンブラ。


:mod:`dis` モジュールは Python バイトコード(:term:`bytecode`) を逆アセンブルしてバイトコードの解析を助けます。
Pythonアセンブラがないため、このモジュールがPythonアセンブリ言語を定義しています。
このモジュールが入力として受け取る Python バイトコード はファイル :file:`Include/opcode.h` に定義されており、
コンパイラとインタプリタが使用しています。

例: 関数 :func:`myfunc` を考えると::

   def myfunc(alist):
       return len(alist)

次のコマンドを :func:`myfunc` の逆アセンブリを得るために使うことができます::

   >>> dis.dis(myfunc)
     2           0 LOAD_GLOBAL              0 (len)
                 3 LOAD_FAST                0 (alist)
                 6 CALL_FUNCTION            1
                 9 RETURN_VALUE        

("2"は行番号です)。

:mod:`dis` モジュールは次の関数と定数を定義します:


.. function:: dis([bytesource])

   *bytesource* オブジェクトを逆アセンブルします
   *bytesource* はモジュール、クラス、関数、あるいはコードオブジェクトのいずれかを示します。
   モジュールに対しては、すべての関数を逆アセンブルします。クラスに対しては、すべてのメソッドを逆アセンブルします。
   単一のコードシーケンスに対しては、バイトコード命令ごとに一行をプリントします。
   オブジェクトが与えられない場合は、最後のトレースバックを逆アセンブルします。


.. function:: distb([tb])

   トレースバックのスタックの先頭の関数を逆アセンブルします。
   Noneが渡された場合は最後のトレースバックを使います。例外を引き起こした命令が表示されます。


.. function:: disassemble(code[, lasti])

   コードオブジェクトを逆アセンブルします。
   *lasti* が与えられた場合は、最後の命令を示します。出力は次のようなカラムに分割されます:

   #. 各行の最初の命令に対する行番号。
   #. 現在の命令。 ``-->`` として示されます。
   #. ラベル付けされた命令。 ``>>`` とともに表示されます。
   #. 命令のアドレス。
   #. 演算コード名。
   #. 演算パラメータ。
   #. 括弧の中のパラメータのインタプリテーション。

   パラメータインタープリテーションはローカルおよびグルーバル変数名、定数値、
   分岐目標、そして比較演算子を認識します。


.. function:: disco(code[, lasti])

   disassembleの別名。よりタイプしやすく、以前のPythonリリースと互換性があります。


.. data:: opname

   演算名。一連のバイトコードを使ってインデキシングできます。


.. data:: opmap

   バイトコードからオペレーション名へのマッピング辞書。


.. data:: cmp_op

   すべての比較演算名。


.. data:: hasconst

   定数パラメータを持つ一連のバイトコード。


.. data:: hasfree

   自由変数にアクセスする一連のバイトコード。


.. data:: hasname

   名前によって属性にアクセスする一連のバイトコード。


.. data:: hasjrel

   相対ジャンプターゲットをもつ一連のバイトコード。


.. data:: hasjabs

   絶対ジャンプターゲットをもつ一連のバイトコード。


.. data:: haslocal

   ローカル変数にアクセスする一連のバイトコード。


.. data:: hascompare

   ブール演算の一連のバイトコード。


.. _bytecodes:

Pythonバイトコード命令
----------------------

現在Pythonコンパイラは次のバイトコード命令を生成します。


.. opcode:: STOP_CODE ()

   コンパイラにend-of-code(コードの終わり)を知らせます。インタプリタでは使われません。


.. opcode:: NOP ()

   なにもしないコード。バイトコードオプティマイザでプレースホルダとして使われます。


.. opcode:: POP_TOP ()

   top-of-stack (TOS)(スタックの先頭)の項目を取り除きます。


.. opcode:: ROT_TWO ()

   スタックの先頭から二つの項目を入れ替えます。


.. opcode:: ROT_THREE ()

   スタックの二番目と三番目の項目の位置を一つ上げ、先頭を三番目へ下げます。


.. opcode:: ROT_FOUR ()

   スタックの二番目、三番目および四番目の位置を一つ上げ、先頭を四番目に下げます。


.. opcode:: DUP_TOP ()

   スタックの先頭に参照の複製を作ります。

一項演算はスタックの先頭を取り出して演算を適用し、結果をスタックへプッシュし戻します。


.. opcode:: UNARY_POSITIVE ()

   ``TOS = +TOS`` を実行します。


.. opcode:: UNARY_NEGATIVE ()

   ``TOS = -TOS`` を実行します。


.. opcode:: UNARY_NOT ()

   ``TOS = not TOS`` を実行します。


.. opcode:: UNARY_CONVERT ()

   ``TOS = `TOS``` を実行します。


.. opcode:: UNARY_INVERT ()

   ``TOS = ~TOS`` を実行します。


.. opcode:: GET_ITER ()

   ``TOS = iter(TOS)`` を実行します。

二項演算はスタックからスタックの先頭(TOS)と先頭から二番目のスタック項目を取り除きます。
演算を実行し、スタックへ結果をプッシュし戻します。


.. opcode:: BINARY_POWER ()

   ``TOS = TOS1 ** TOS`` を実行します。


.. opcode:: BINARY_MULTIPLY ()

   ``TOS = TOS1 * TOS`` を実行します。


.. opcode:: BINARY_DIVIDE ()

   ``from __future__ import division`` が有効でないとき、 ``TOS = TOS1 / TOS`` を実行します。


.. opcode:: BINARY_FLOOR_DIVIDE ()

   ``TOS = TOS1 // TOS`` を実行します。


.. opcode:: BINARY_TRUE_DIVIDE ()

   ``from __future__ import division`` が有効でないとき、 ``TOS = TOS1 / TOS`` を実行します。


.. opcode:: BINARY_MODULO ()

   ``TOS = TOS1 % TOS`` を実行します。


.. opcode:: BINARY_ADD ()

   ``TOS = TOS1 + TOS`` を実行します。


.. opcode:: BINARY_SUBTRACT ()

   ``TOS = TOS1 - TOS`` を実行します。


.. opcode:: BINARY_SUBSCR ()

   ``TOS = TOS1[TOS]`` を実行します。


.. opcode:: BINARY_LSHIFT ()

   ``TOS = TOS1 << TOS`` を実行します。


.. opcode:: BINARY_RSHIFT ()

   ``TOS = TOS1 >> TOS`` を実行します。


.. opcode:: BINARY_AND ()

   ``TOS = TOS1 & TOS`` を実行します。


.. opcode:: BINARY_XOR ()

   ``TOS = TOS1 ^ TOS`` を実行します。


.. opcode:: BINARY_OR ()

   ``TOS = TOS1 | TOS`` を実行します。

インプレース演算はTOSとTOS1を取り除いて結果をスタックへプッシュするという点で二項演算と似ています。
しかし、TOS1がインプレース演算をサポートしている場合には演算が直接TOS1に行われます。
また、演算結果のTOSは元のTOS1と同じオブジェクトになることが多いですが、常に同じというわけではありません。


.. opcode:: INPLACE_POWER ()

   インプレースに ``TOS = TOS1 ** TOS`` を実行します。


.. opcode:: INPLACE_MULTIPLY ()

   インプレースに ``TOS = TOS1 * TOS`` を実行します。


.. opcode:: INPLACE_DIVIDE ()

   ``from __future__ import division`` が有効でないとき、インプレースに ``TOS = TOS1 / TOS`` を実行します。


.. opcode:: INPLACE_FLOOR_DIVIDE ()

   インプレースに ``TOS = TOS1 // TOS`` を実行します。


.. opcode:: INPLACE_TRUE_DIVIDE ()

   ``from __future__ import division`` が有効でないとき、インプレースに ``TOS = TOS1 / TOS`` を実行します。


.. opcode:: INPLACE_MODULO ()

   インプレースに ``TOS = TOS1 % TOS`` を実行します。


.. opcode:: INPLACE_ADD ()

   インプレースに ``TOS = TOS1 + TOS`` を実行します。


.. opcode:: INPLACE_SUBTRACT ()

   インプレースに ``TOS = TOS1 - TOS`` を実行します。


.. opcode:: INPLACE_LSHIFT ()

   インプレースに ``TOS = TOS1 << TOS`` を実行します。


.. opcode:: INPLACE_RSHIFT ()

   インプレースに ``TOS = TOS1 >> TOS`` を実行します。


.. opcode:: INPLACE_AND ()

   インプレースに ``TOS = TOS1 & TOS`` を実行します。


.. opcode:: INPLACE_XOR ()

   インプレースに ``TOS = TOS1 ^ TOS`` を実行します。


.. opcode:: INPLACE_OR ()

   インプレースに ``TOS = TOS1 | TOS`` を実行します。

スライス演算は三つまでのパラメータを取ります。


.. opcode:: SLICE+0 ()

   ``TOS = TOS[:]`` を実行します。


.. opcode:: SLICE+1 ()

   ``TOS = TOS1[TOS:]`` を実行します。


.. opcode:: SLICE+2 ()

   ``TOS = TOS1[:TOS]`` を実行します。


.. opcode:: SLICE+3 ()

   ``TOS = TOS2[TOS1:TOS]`` を実行します。

スライス代入はさらに別のパラメータを必要とします。どんな文もそうであるように、スタックに何もプッシュしません。


.. opcode:: STORE_SLICE+0 ()

   ``TOS[:] = TOS1`` を実行します。


.. opcode:: STORE_SLICE+1 ()

   ``TOS1[TOS:] = TOS2`` を実行します。


.. opcode:: STORE_SLICE+2 ()

   ``TOS1[:TOS] = TOS2`` を実行します。


.. opcode:: STORE_SLICE+3 ()

   ``TOS2[TOS1:TOS] = TOS3`` を実行します。


.. opcode:: DELETE_SLICE+0 ()

   ``del TOS[:]`` を実行します。


.. opcode:: DELETE_SLICE+1 ()

   ``del TOS1[TOS:]`` を実行します。


.. opcode:: DELETE_SLICE+2 ()

   ``del TOS1[:TOS]`` を実行します。


.. opcode:: DELETE_SLICE+3 ()

   ``del TOS2[TOS1:TOS]`` を実行します。


.. opcode:: STORE_SUBSCR ()

   ``TOS1[TOS] = TOS2`` を実行します。


.. opcode:: DELETE_SUBSCR ()

   ``del TOS1[TOS]`` を実行します。

その他の演算。


.. opcode:: PRINT_EXPR ()

   対話モードのための式文を実行します。TOSはスタックから取り除かれプリントされます。
   非対話モードにおいては、式文は ``POP_STACK`` で終了しています。


.. opcode:: PRINT_ITEM ()

   ``sys.stdout`` に束縛されたファイル互換のオブジェクトへTOSをプリントします。
   :keyword:`print` 文に、各項目に対するこのような命令が一つあります。


.. opcode:: PRINT_ITEM_TO ()

   ``PRINT_ITEM`` と似ていますが、TOSから二番目の項目をTOSにあるファイル互換オブジェクトへプリントします。
   これは拡張print文で使われます。


.. opcode:: PRINT_NEWLINE ()

   ``sys.stdout`` へ改行をプリントします。
   これは:keyword:`print` 文がコンマで終わっていない場合に:keyword:`print` 文の最後の演算として生成されます。


.. opcode:: PRINT_NEWLINE_TO ()

   ``PRINT_NEWLINE`` と似ていますが、TOSのファイル互換オブジェクトに改行をプリントします。これは拡張print文で使われます。


.. opcode:: BREAK_LOOP ()

   :keyword:`break` 文があるためループを終了します。


.. opcode:: CONTINUE_LOOP (target)

   :keyword:`continue` 文があるためループを継続します。
   *target* はジャンプするアドレスです(アドレスは ``FOR_ITER`` 命令であるべきです)。


.. opcode:: LIST_APPEND ()

   ``list.append(TOS1, TOS)`` を呼びます。 リスト内包表記を実装するために使われます。


.. opcode:: LOAD_LOCALS ()

   現在のスコープのローカルな名前空間(locals)への参照をスタックにプッシュします。
   これはクラス定義のためのコードで使われます:
   クラス本体が評価された後、localsはクラス定義へ渡されます。


.. opcode:: RETURN_VALUE ()

   関数の呼び出し元へTOSを返します。


.. opcode:: YIELD_VALUE ()

   ``TOS`` をポップし、それをジェネレータ(:term:`generator`)からyieldします。


.. opcode:: IMPORT_STAR ()

   ``'_'`` で始まっていないすべてのシンボルをモジュールTOSから直接ローカル名前空間へロードします。
   モジュールはすべての名前をロードした後にポップされます。
   この演算コードは ``from module import *`` を実行します。


.. opcode:: EXEC_STMT ()

   ``exec TOS2,TOS1,TOS`` を実行します。コンパイラは見つからないオプションのパラメータを ``None`` で埋めます。


.. opcode:: POP_BLOCK ()

   ブロックスタックからブロックを一つ取り除きます。
   フレームごとにブロックのスタックがあり、ネストしたループ、try文などを意味しています。


.. opcode:: END_FINALLY ()

   :keyword:`finally` 節を終わらせます。
   インタプリタは例外を再び発生させなければならないかどうか、あるいは、
   関数が返り外側の次のブロックに続くかどうかを思い出します。


.. opcode:: BUILD_CLASS ()

   新しいクラスオブジェクトを作成します。TOSはメソッド辞書、TOS1は基底クラスの名前のタプル、TOS2はクラス名です。


.. opcode:: WITH_CLEANUP ()

   :keyword:`with` ステートメントブロックがあるときに、スタックをクリーンアップします。
   スタックのトップは 1--3 個の値で、 なぜ/どのように finally 項に到達したかを表します:

   * TOP = ``None``
   * (TOP, SECOND) = (``WHY_{RETURN,CONTINUE}``), retval
   * TOP = ``WHY_*``; no retval below it
   * (TOP, SECOND, THIRD) = exc_info()

   その下に、 コンテキストマネージャーの :meth:`__exit__` バウンドメソッドの EXIT があります。

   最後のケースでは、 ``EXIT(TOP, SECOND, THIRD)`` が呼ばれ、それ以外では
   ``EXIT(None, None, None)`` が呼ばれます。

   EXIT はスタックから取り除かれ、その上の値は順序を維持したまま残されます。
   加えて、スタックが例外を表し、 *かつ* 関数呼び出しが *true* 値を返した場合、
   ``END_FINALLY`` を例外の再創出から守るためにこの情報は削除されます("zapped")。
   (しかし、 non-local goto はなお実行されます)

   .. XXX explain the WHY stuff!


次の演算コードはすべて引数を要求します。引数はより重要なバイトを下位にもつ2バイトです。


.. opcode:: STORE_NAME (namei)

   ``name = TOS`` を実行します。
   *namei* はコードオブジェクトの属性:attr:`co_names` における *name* のインデックスです。
   コンパイラは可能ならば ``STORE_FAST`` または ``STORE_GLOBAL`` を使おうとします。


.. opcode:: DELETE_NAME (namei)

   ``del name`` を実行します。ここで、 *namei* はコードオブジェクトの:attr:`co_names` 属性へのインデックスです。


.. opcode:: UNPACK_SEQUENCE (count)

   TOSを *count* 個のへ個別の値に分け、右から左にスタックに置かれます。


.. opcode:: DUP_TOPX (count)

   *count* 個の項目を同じ順番を保ちながら複製します。
   実装上の制限から、 *count* は1から5の間(5を含む)でなければいけません。


.. opcode:: STORE_ATTR (namei)

   ``TOS.name = TOS1`` を実行します。ここで、 *namei* は:attr:`co_names` における名前のインデックスです。


.. opcode:: DELETE_ATTR (namei)

   :attr:`co_names` へのインデックスとして *namei* を使い、 ``del TOS.name`` を実行します。


.. opcode:: STORE_GLOBAL (namei)

   ``STORE_NAME`` として機能しますが、グローバルとして名前を記憶します。


.. opcode:: DELETE_GLOBAL (namei)

   ``DELETE_NAME`` として機能しますが、グルーバル名を削除します。


.. opcode:: LOAD_CONST (consti)

   ``co_consts[consti]`` をスタックにプッシュします。


.. opcode:: LOAD_NAME (namei)

   ``co_names[namei]`` に関連付けられた値をスタックにプッシュします。


.. opcode:: BUILD_TUPLE (count)

   スタックから *count* 個の項目を消費するタプルを作り出し、できたタプルをスタックにプッシュします。


.. opcode:: BUILD_LIST (count)

   ``BUILD_TUPLE`` として機能しますが、リストを作り出します。


.. opcode:: BUILD_MAP (count)

   スタックに新しい辞書オブジェクトをプッシュします。
   辞書は *count* 個のエントリを持つサイズに設定されます。


.. opcode:: LOAD_ATTR (namei)

   TOSを ``getattr(TOS, co_names[namei])`` と入れ替えます。


.. opcode:: COMPARE_OP (opname)

   ブール演算を実行します。演算名は ``cmp_op[opname]`` にあります。


.. opcode:: IMPORT_NAME (namei)

   モジュール ``co_names[namei]`` をインポートします。
   TOS と TOS1 がポップされ、 :func:`__import__` の *fromlist* と *level* 引数になります。
   モジュールオブジェクトはスタックへプッシュされます。現在の名前空間は影響されません:
   適切なimport文に対して、それに続く ``STORE_FAST`` 命令が名前空間を変更します。


.. opcode:: IMPORT_FROM (namei)

   属性 ``co_names[namei]`` をTOSに見つかるモジュールからロードします。
   作成されたオブジェクトはスタックにプッシュされ、その後 ``STORE_FAST`` 命令によって記憶されます。


.. opcode:: JUMP_FORWARD (delta)

   バイトコードカウンタを *delta* だけ増加させます。


.. opcode:: JUMP_IF_TRUE (delta)

   TOSが真ならば、 *delta* だけバイトコードカウンタを増加させます。TOSはスタックに残されます。


.. opcode:: JUMP_IF_FALSE (delta)

   TOSが偽ならば、 *delta* だけバイトコードカウンタを増加させます。TOSは変更されません。


.. opcode:: JUMP_ABSOLUTE (target)

   バイトコードカウンタを *target* に設定します。


.. opcode:: FOR_ITER (delta)

   ``TOS`` はイテレータです。その:meth:`next` メソッドを呼び出します。
   これが新しい値を作り出すならば、それを(その下にイテレータを残したまま)スタックにプッシュします。
   イテレータが尽きたことを示した場合は、 ``TOS`` がポップされます。
   そして、バイトコードカウンタが *delta* だけ増やされます。


.. opcode:: LOAD_GLOBAL (namei)

   グルーバル名 ``co_names[namei]`` をスタック上にロードします。


.. opcode:: SETUP_LOOP (delta)

   ブロックスタックにループのためのブロックをプッシュします。
   ブロックは現在の命令から *delta* バイトの大きさを占めます。


.. opcode:: SETUP_EXCEPT (delta)

   try-except節からtryブロックをブロックスタックにプッシュします。
   *delta* は最初のexceptブロックを指します。


.. opcode:: SETUP_FINALLY (delta)

   try-except節からtryブロックをブロックスタックにプッシュします。 *delta* はfinallyブロックを指します。

.. opcode:: STORE_MAP ()

   key, value のペアを辞書に格納します。辞書がスタックに残っている間 (while leaving the dictionary on the stack)
   key と value をポップします。

.. opcode:: LOAD_FAST (var_num)

   ローカルな ``co_varnames[var_num]`` への参照をスタックにプッシュします。


.. opcode:: STORE_FAST (var_num)

   TOSをローカルな ``co_varnames[var_num]`` の中に保存します。


.. opcode:: DELETE_FAST (var_num)

   ローカルな ``co_varnames[var_num]`` を削除します。


.. opcode:: LOAD_CLOSURE (i)

   セルと自由変数記憶領域のスロット *i* に含まれるセルへの参照をプッシュします。
   *i* が *co_cellvars* の長さより小さければ、変数の名前は ``co_cellvars[i]`` です。
   そうでなければ、それは ``co_freevars[i - len(co_cellvars)]`` です。


.. opcode:: LOAD_DEREF (i)

   セルと自由変数記憶領域のスロット *i* に含まれるセルをロードします。
   セルが持つオブジェクトへの参照をスタックにプッシュします。


.. opcode:: STORE_DEREF (i)

   セルと自由変数記憶領域のスロット *i* に含まれるセルへTOSを保存します。


.. opcode:: SET_LINENO (lineno)

   このペコードは廃止されました。


.. opcode:: RAISE_VARARGS (argc)

   例外を発生させます。 *argc* はraise文へ与えるパラメータの数を0から3の範囲で示します。
   ハンドラはTOS2としてトレースバック、TOS1としてパラメータ、そしてTOSとして例外を見つけられます。


.. opcode:: CALL_FUNCTION (argc)

   関数を呼び出します。 *argc* の低位バイトは位置パラメータを示し、高位バイトはキーワードパラメータの数を示します。
   オペコードは最初にキーワードパラメータをスタック上に見つけます。
   それぞれのキーワード引数に対して、その値はキーの上にあります。
   スタック上のキーワードパラメータの下に位置パラメータはあり、先頭に最も右のパラメータがあります。
   スタック上のパラメータの下には、呼び出す関数オブジェクトがあります。
   全ての関数引数をポップし、関数自体もスタックから取り除き、戻り値をプッシュします。


.. opcode:: MAKE_FUNCTION (argc)

   新しい関数オブジェクトをスタックにプッシュします。
   TOSは関数に関連付けられたコードです。
   関数オブジェクトはTOSの下にある *argc* デフォルトパラメータをもつように定義されます。


.. opcode:: MAKE_CLOSURE (argc)

   新しい関数オブジェクトを作り出し、その *func_closure* スロットを設定し、それをスタックにプッシュします。
   TOSは関数に関連付けられたコードで、TOS1 は クロージャ の自由変数に対する cell を格納したタプルです。
   関数はセルの前にある *argc* デフォルトパラメータも持っています。


.. opcode:: BUILD_SLICE (argc)

   .. index:: builtin: slice

   スライスオブジェクトをスタックにプッシュします。 *argc* は2あるいは3でなければなりません。
   2ならば ``slice(TOS1, TOS)`` がプッシュされます。
   3ならば ``slice(TOS2, TOS1, TOS)`` がプッシュされます。
   これ以上の情報については、 :func:`slice()` 組み込み関数を参照してください。


.. opcode:: EXTENDED_ARG (ext)

   大きすぎてデフォルトの二バイトに当てはめることができない引数をもつあらゆるオペコードの前に置かれます。
   *ext* は二つの追加バイトを保持し、その後ろのオペコードの引数と一緒になって取られます。
   それらは四バイト引数を構成し、 *ext* はその最上位バイトです。


.. opcode:: CALL_FUNCTION_VAR (argc)

   関数を呼び出します。 *argc* は ``CALL_FUNCTION`` のように解釈実行されます。
   スタックの先頭の要素は変数引数リストを含んでおり、その後にキーワードと位置引数が続きます。


.. opcode:: CALL_FUNCTION_KW (argc)

   関数を呼び出します。 *argc* は ``CALL_FUNCTION`` のように解釈実行されます。
   スタックの先頭の要素はキーワード引数辞書を含んでおり、その後に明示的なキーワードと位置引数が続きます。


.. opcode:: CALL_FUNCTION_VAR_KW (argc)

   関数を呼び出します。 *argc* は ``CALL_FUNCTION`` のように解釈実行されます。
   スタックの先頭の要素はキーワード引数辞書を含んでおり、その後に変数引数のタプルが続き、
   さらに明示的なキーワードと位置引数が続きます。


.. opcode:: HAVE_ARGUMENT ()

   これはオペコードではありません。引数をとらないオペコード ``< HAVE_ARGUMENT``  と、
   とるオペコード ``>= HAVE_ARGUMENT`` を分割する行です。
