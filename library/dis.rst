
:mod:`dis` --- Pythonバイトコードの逆アセンブラ
===============================================

.. module:: dis
   :synopsis: Pythonバイトコードの逆アセンブラ。


.. The :mod:`dis` module supports the analysis of CPython :term:`bytecode` by
.. disassembling it. The CPython bytecode which this module takes as an
.. input is defined in the file :file:`Include/opcode.h` and used by the compiler
.. and the interpreter.

:mod:`dis` モジュールは CPython バイトコード(:term:`bytecode`) を逆アセンブルしてバイトコードの解析を助けます。
このモジュールが入力として受け取る CPython バイトコードはファイル :file:`Include/opcode.h` に定義されており、
コンパイラとインタプリタが使用しています。


.. impl-detail::

   .. Bytecode is an implementation detail of the CPython interpreter!  No
   .. guarantees are made that bytecode will not be added, removed, or changed
   .. between versions of Python.  Use of this module should not be considered to
   .. work across Python VMs or Python releases.

   バイトコードは CPython インタプリタの実装詳細です! Python のバージョン
   間でバイトコードの追加や、削除、変更がないという保証はありません。この
   モジュールを使用することによって Python の異なる VM または異なるリリース
   の間で動作すると考えるべきではありません。


.. Example: Given the function :func:`myfunc`:

例: 関数 :func:`myfunc` を考えると


::

   def myfunc(alist):
       return len(alist)


.. the following command can be used to get the disassembly of :func:`myfunc`:

次のコマンドを :func:`myfunc` の逆アセンブリを得るために使うことができます


::

   >>> dis.dis(myfunc)
     2           0 LOAD_GLOBAL              0 (len)
                 3 LOAD_FAST                0 (alist)
                 6 CALL_FUNCTION            1
                 9 RETURN_VALUE


.. (The "2" is a line number).

("2"は行番号です)。


.. The :mod:`dis` module defines the following functions and constants:

:mod:`dis` モジュールは次の関数と定数を定義します:


.. function:: dis([bytesource])

   .. Disassemble the *bytesource* object. *bytesource* can denote either a module, a
   .. class, a method, a function, or a code object.   For a module, it disassembles
   .. all functions.  For a class, it disassembles all methods.  For a single code
   .. sequence, it prints one line per bytecode instruction.  If no object is
   .. provided, it disassembles the last traceback.

   *bytesource* オブジェクトを逆アセンブルします
   *bytesource* はモジュール、クラス、関数、あるいはコードオブジェクトのいずれかを示します。
   モジュールに対しては、すべての関数を逆アセンブルします。クラスに対しては、すべてのメソッドを逆アセンブルします。
   単一のコードシーケンスに対しては、バイトコード命令ごとに一行をプリントします。
   オブジェクトが与えられない場合は、最後のトレースバックを逆アセンブルします。


.. function:: distb([tb])

   .. Disassembles the top-of-stack function of a traceback, using the last traceback
   .. if none was passed.  The instruction causing the exception is indicated.

   トレースバックのスタックの先頭の関数を逆アセンブルします。
   Noneが渡された場合は最後のトレースバックを使います。例外を引き起こした命令が表示されます。


.. function:: disassemble(code[, lasti])

   .. Disassembles a code object, indicating the last instruction if *lasti* was
   .. provided.  The output is divided in the following columns:

   コードオブジェクトを逆アセンブルします。
   *lasti* が与えられた場合は、最後の命令を示します。出力は次のようなカラムに分割されます:


   .. #. the line number, for the first instruction of each line
   .. #. the current instruction, indicated as ``-->``,
   .. #. a labelled instruction, indicated with ``>>``,
   .. #. the address of the instruction,
   .. #. the operation code name,
   .. #. operation parameters, and
   .. #. interpretation of the parameters in parentheses.

   #. 各行の最初の命令に対する行番号。
   #. 現在の命令。 ``-->`` として示されます。
   #. ラベル付けされた命令。 ``>>`` とともに表示されます。
   #. 命令のアドレス。
   #. 演算コード名。
   #. 演算パラメータ。
   #. 括弧の中のパラメータのインタプリテーション。


   .. The parameter interpretation recognizes local and global variable names,
   .. constant values, branch targets, and compare operators.

   パラメータインタープリテーションはローカルおよびグルーバル変数名、定数値、
   分岐目標、そして比較演算子を認識します。


.. function:: disco(code[, lasti])

   .. A synonym for disassemble.  It is more convenient to type, and kept for
   .. compatibility with earlier Python releases.

   disassembleの別名。よりタイプしやすく、以前のPythonリリースと互換性があります。


.. data:: opname

   .. Sequence of operation names, indexable using the bytecode.

   演算名。一連のバイトコードを使ってインデキシングできます。


.. data:: opmap

   .. Dictionary mapping bytecodes to operation names.

   バイトコードからオペレーション名へのマッピング辞書。


.. data:: cmp_op

   .. Sequence of all compare operation names.

   すべての比較演算名。


.. data:: hasconst

   .. Sequence of bytecodes that have a constant parameter.

   定数パラメータを持つ一連のバイトコード。


.. data:: hasfree

   .. Sequence of bytecodes that access a free variable.

   自由変数にアクセスする一連のバイトコード。


.. data:: hasname

   .. Sequence of bytecodes that access an attribute by name.

   名前によって属性にアクセスする一連のバイトコード。


.. data:: hasjrel

   .. Sequence of bytecodes that have a relative jump target.

   相対ジャンプターゲットをもつ一連のバイトコード。


.. data:: hasjabs

   .. Sequence of bytecodes that have an absolute jump target.

   絶対ジャンプターゲットをもつ一連のバイトコード。


.. data:: haslocal

   .. Sequence of bytecodes that access a local variable.

   ローカル変数にアクセスする一連のバイトコード。


.. data:: hascompare

   .. Sequence of bytecodes of Boolean operations.

   ブール演算の一連のバイトコード。


.. _bytecodes:

Pythonバイトコード命令
----------------------

.. The Python compiler currently generates the following bytecode instructions.

現在Pythonコンパイラは次のバイトコード命令を生成します。


.. opcode:: STOP_CODE ()

   .. Indicates end-of-code to the compiler, not used by the interpreter.

   コンパイラにend-of-code(コードの終わり)を知らせます。インタプリタでは使われません。


.. opcode:: NOP ()

   .. Do nothing code.  Used as a placeholder by the bytecode optimizer.

   なにもしないコード。バイトコードオプティマイザでプレースホルダとして使われます。


.. opcode:: POP_TOP ()

   .. Removes the top-of-stack (TOS) item.

   top-of-stack (TOS)(スタックの先頭)の項目を取り除きます。


.. opcode:: ROT_TWO ()

   .. Swaps the two top-most stack items.

   スタックの先頭から二つの項目を入れ替えます。


.. opcode:: ROT_THREE ()

   .. Lifts second and third stack item one position up, moves top down to position
   .. three.

   スタックの二番目と三番目の項目の位置を一つ上げ、先頭を三番目へ下げます。


.. opcode:: ROT_FOUR ()

   .. Lifts second, third and forth stack item one position up, moves top down to
   .. position four.

   スタックの二番目、三番目および四番目の位置を一つ上げ、先頭を四番目に下げます。


.. opcode:: DUP_TOP ()

   .. Duplicates the reference on top of the stack.

   スタックの先頭に参照の複製を作ります。


.. Unary Operations take the top of the stack, apply the operation, and push the
.. result back on the stack.

一項演算はスタックの先頭を取り出して演算を適用し、結果をスタックへプッシュし戻します。


.. opcode:: UNARY_POSITIVE ()

   .. Implements ``TOS = +TOS``.

   ``TOS = +TOS`` を実行します。


.. opcode:: UNARY_NEGATIVE ()

   .. Implements ``TOS = -TOS``.

   ``TOS = -TOS`` を実行します。


.. opcode:: UNARY_NOT ()

   .. Implements ``TOS = not TOS``.

   ``TOS = not TOS`` を実行します。


.. opcode:: UNARY_CONVERT ()

   .. Implements ``TOS = `TOS```.

   ``TOS = `TOS``` を実行します。


.. opcode:: UNARY_INVERT ()

   .. Implements ``TOS = ~TOS``.

   ``TOS = ~TOS`` を実行します。


.. opcode:: GET_ITER ()

   .. Implements ``TOS = iter(TOS)``.

   ``TOS = iter(TOS)`` を実行します。


.. Binary operations remove the top of the stack (TOS) and the second top-most
.. stack item (TOS1) from the stack.  They perform the operation, and put the
.. result back on the stack.

二項演算はスタックからスタックの先頭(TOS)と先頭から二番目のスタック項目を取り除きます。
演算を実行し、スタックへ結果をプッシュし戻します。


.. opcode:: BINARY_POWER ()

   .. Implements ``TOS = TOS1 ** TOS``.

   ``TOS = TOS1 ** TOS`` を実行します。


.. opcode:: BINARY_MULTIPLY ()

   .. Implements ``TOS = TOS1 * TOS``.

   ``TOS = TOS1 * TOS`` を実行します。


.. opcode:: BINARY_DIVIDE ()

   .. Implements ``TOS = TOS1 / TOS`` when ``from __future__ import division`` is not
   .. in effect.

   ``from __future__ import division`` が有効でないとき、 ``TOS = TOS1 / TOS`` を実行します。


.. opcode:: BINARY_FLOOR_DIVIDE ()

   .. Implements ``TOS = TOS1 // TOS``.

   ``TOS = TOS1 // TOS`` を実行します。


.. opcode:: BINARY_TRUE_DIVIDE ()

   .. Implements ``TOS = TOS1 / TOS`` when ``from __future__ import division`` is in
   .. effect.

   ``from __future__ import division`` が有効でないとき、 ``TOS = TOS1 / TOS`` を実行します。


.. opcode:: BINARY_MODULO ()

   .. Implements ``TOS = TOS1 % TOS``.

   ``TOS = TOS1 % TOS`` を実行します。


.. opcode:: BINARY_ADD ()

   .. Implements ``TOS = TOS1 + TOS``.

   ``TOS = TOS1 + TOS`` を実行します。


.. opcode:: BINARY_SUBTRACT ()

   .. Implements ``TOS = TOS1 - TOS``.

   ``TOS = TOS1 - TOS`` を実行します。


.. opcode:: BINARY_SUBSCR ()

   .. Implements ``TOS = TOS1[TOS]``.

   ``TOS = TOS1[TOS]`` を実行します。


.. opcode:: BINARY_LSHIFT ()

   .. Implements ``TOS = TOS1 << TOS``.

   ``TOS = TOS1 << TOS`` を実行します。


.. opcode:: BINARY_RSHIFT ()

   .. Implements ``TOS = TOS1 >> TOS``.

   ``TOS = TOS1 >> TOS`` を実行します。


.. opcode:: BINARY_AND ()

   .. Implements ``TOS = TOS1 & TOS``.

   ``TOS = TOS1 & TOS`` を実行します。


.. opcode:: BINARY_XOR ()

   .. Implements ``TOS = TOS1 ^ TOS``.

   ``TOS = TOS1 ^ TOS`` を実行します。


.. opcode:: BINARY_OR ()

   .. Implements ``TOS = TOS1 | TOS``.

   ``TOS = TOS1 | TOS`` を実行します。


.. In-place operations are like binary operations, in that they remove TOS and
.. TOS1, and push the result back on the stack, but the operation is done in-place
.. when TOS1 supports it, and the resulting TOS may be (but does not have to be)
.. the original TOS1.

インプレース演算はTOSとTOS1を取り除いて結果をスタックへプッシュするという点で二項演算と似ています。
しかし、TOS1がインプレース演算をサポートしている場合には演算が直接TOS1に行われます。
また、演算結果のTOSは元のTOS1と同じオブジェクトになることが多いですが、常に同じというわけではありません。


.. opcode:: INPLACE_POWER ()

   .. Implements in-place ``TOS = TOS1 ** TOS``.

   インプレースに ``TOS = TOS1 ** TOS`` を実行します。


.. opcode:: INPLACE_MULTIPLY ()

   .. Implements in-place ``TOS = TOS1 * TOS``.

   インプレースに ``TOS = TOS1 * TOS`` を実行します。


.. opcode:: INPLACE_DIVIDE ()

   .. Implements in-place ``TOS = TOS1 / TOS`` when ``from __future__ import
   .. division`` is not in effect.

   ``from __future__ import division`` が有効でないとき、インプレースに ``TOS = TOS1 / TOS`` を実行します。


.. opcode:: INPLACE_FLOOR_DIVIDE ()

   .. Implements in-place ``TOS = TOS1 // TOS``.

   インプレースに ``TOS = TOS1 // TOS`` を実行します。


.. opcode:: INPLACE_TRUE_DIVIDE ()

   .. Implements in-place ``TOS = TOS1 / TOS`` when ``from __future__ import
   .. division`` is in effect.

   ``from __future__ import division`` が有効でないとき、インプレースに ``TOS = TOS1 / TOS`` を実行します。


.. opcode:: INPLACE_MODULO ()

   .. Implements in-place ``TOS = TOS1 % TOS``.

   インプレースに ``TOS = TOS1 % TOS`` を実行します。


.. opcode:: INPLACE_ADD ()

   .. Implements in-place ``TOS = TOS1 + TOS``.

   インプレースに ``TOS = TOS1 + TOS`` を実行します。


.. opcode:: INPLACE_SUBTRACT ()

   .. Implements in-place ``TOS = TOS1 - TOS``.

   インプレースに ``TOS = TOS1 - TOS`` を実行します。


.. opcode:: INPLACE_LSHIFT ()

   .. Implements in-place ``TOS = TOS1 << TOS``.

   インプレースに ``TOS = TOS1 << TOS`` を実行します。


.. opcode:: INPLACE_RSHIFT ()

   .. Implements in-place ``TOS = TOS1 >> TOS``.

   インプレースに ``TOS = TOS1 >> TOS`` を実行します。


.. opcode:: INPLACE_AND ()

   .. Implements in-place ``TOS = TOS1 & TOS``.

   インプレースに ``TOS = TOS1 & TOS`` を実行します。


.. opcode:: INPLACE_XOR ()

   .. Implements in-place ``TOS = TOS1 ^ TOS``.

   インプレースに ``TOS = TOS1 ^ TOS`` を実行します。


.. opcode:: INPLACE_OR ()

   .. Implements in-place ``TOS = TOS1 | TOS``.

   インプレースに ``TOS = TOS1 | TOS`` を実行します。


.. The slice opcodes take up to three parameters.

スライス演算は三つまでのパラメータを取ります。


.. opcode:: SLICE+0 ()

   .. Implements ``TOS = TOS[:]``.

   ``TOS = TOS[:]`` を実行します。


.. opcode:: SLICE+1 ()

   .. Implements ``TOS = TOS1[TOS:]``.

   ``TOS = TOS1[TOS:]`` を実行します。


.. opcode:: SLICE+2 ()

   .. Implements ``TOS = TOS1[:TOS]``.

   ``TOS = TOS1[:TOS]`` を実行します。


.. opcode:: SLICE+3 ()

   .. Implements ``TOS = TOS2[TOS1:TOS]``.

   ``TOS = TOS2[TOS1:TOS]`` を実行します。


.. Slice assignment needs even an additional parameter.  As any statement, they put
.. nothing on the stack.

スライス代入はさらに別のパラメータを必要とします。どんな文もそうであるように、スタックに何もプッシュしません。


.. opcode:: STORE_SLICE+0 ()

   .. Implements ``TOS[:] = TOS1``.

   ``TOS[:] = TOS1`` を実行します。


.. opcode:: STORE_SLICE+1 ()

   .. Implements ``TOS1[TOS:] = TOS2``.

   ``TOS1[TOS:] = TOS2`` を実行します。


.. opcode:: STORE_SLICE+2 ()

   .. Implements ``TOS1[:TOS] = TOS2``.

   ``TOS1[:TOS] = TOS2`` を実行します。


.. opcode:: STORE_SLICE+3 ()

   .. Implements ``TOS2[TOS1:TOS] = TOS3``.

   ``TOS2[TOS1:TOS] = TOS3`` を実行します。


.. opcode:: DELETE_SLICE+0 ()

   .. Implements ``del TOS[:]``.

   ``del TOS[:]`` を実行します。


.. opcode:: DELETE_SLICE+1 ()

   .. Implements ``del TOS1[TOS:]``.

   ``del TOS1[TOS:]`` を実行します。


.. opcode:: DELETE_SLICE+2 ()

   .. Implements ``del TOS1[:TOS]``.

   ``del TOS1[:TOS]`` を実行します。


.. opcode:: DELETE_SLICE+3 ()

   .. Implements ``del TOS2[TOS1:TOS]``.

   ``del TOS2[TOS1:TOS]`` を実行します。


.. opcode:: STORE_SUBSCR ()

   .. Implements ``TOS1[TOS] = TOS2``.

   ``TOS1[TOS] = TOS2`` を実行します。


.. opcode:: DELETE_SUBSCR ()

   .. Implements ``del TOS1[TOS]``.

   ``del TOS1[TOS]`` を実行します。


.. Miscellaneous opcodes.

その他の演算。


.. opcode:: PRINT_EXPR ()

   .. Implements the expression statement for the interactive mode.  TOS is removed
   .. from the stack and printed.  In non-interactive mode, an expression statement is
   .. terminated with ``POP_STACK``.

   対話モードのための式文を実行します。TOSはスタックから取り除かれプリントされます。
   非対話モードにおいては、式文は ``POP_STACK`` で終了しています。


.. opcode:: PRINT_ITEM ()

   .. Prints TOS to the file-like object bound to ``sys.stdout``.  There is one such
   .. instruction for each item in the :keyword:`print` statement.

   ``sys.stdout`` に束縛されたファイル互換のオブジェクトへTOSをプリントします。
   :keyword:`print` 文に、各項目に対するこのような命令が一つあります。


.. opcode:: PRINT_ITEM_TO ()

   .. Like ``PRINT_ITEM``, but prints the item second from TOS to the file-like object
   .. at TOS.  This is used by the extended print statement.

   ``PRINT_ITEM`` と似ていますが、TOSから二番目の項目をTOSにあるファイル互換オブジェクトへプリントします。
   これは拡張print文で使われます。


.. opcode:: PRINT_NEWLINE ()

   .. Prints a new line on ``sys.stdout``.  This is generated as the last operation of
   .. a :keyword:`print` statement, unless the statement ends with a comma.

   ``sys.stdout`` へ改行をプリントします。
   これは:keyword:`print` 文がコンマで終わっていない場合に:keyword:`print` 文の最後の演算として生成されます。


.. opcode:: PRINT_NEWLINE_TO ()

   .. Like ``PRINT_NEWLINE``, but prints the new line on the file-like object on the
   .. TOS.  This is used by the extended print statement.

   ``PRINT_NEWLINE`` と似ていますが、TOSのファイル互換オブジェクトに改行をプリントします。これは拡張print文で使われます。


.. opcode:: BREAK_LOOP ()

   .. Terminates a loop due to a :keyword:`break` statement.

   :keyword:`break` 文があるためループを終了します。


.. opcode:: CONTINUE_LOOP (target)

   .. Continues a loop due to a :keyword:`continue` statement.  *target* is the
   .. address to jump to (which should be a ``FOR_ITER`` instruction).

   :keyword:`continue` 文があるためループを継続します。
   *target* はジャンプするアドレスです(アドレスは ``FOR_ITER`` 命令であるべきです)。


.. opcode:: LIST_APPEND ()

   .. Calls ``list.append(TOS1, TOS)``.  Used to implement list comprehensions.

   ``list.append(TOS1, TOS)`` を呼びます。リスト内包表記を実装するために使われます。


.. opcode:: LOAD_LOCALS ()

   .. Pushes a reference to the locals of the current scope on the stack. This is used
   .. in the code for a class definition: After the class body is evaluated, the
   .. locals are passed to the class definition.

   現在のスコープのローカルな名前空間(locals)への参照をスタックにプッシュします。
   これはクラス定義のためのコードで使われます:
   クラス本体が評価された後、localsはクラス定義へ渡されます。


.. opcode:: RETURN_VALUE ()

   .. Returns with TOS to the caller of the function.

   関数の呼び出し元へTOSを返します。


.. opcode:: YIELD_VALUE ()

   .. Pops ``TOS`` and yields it from a :term:`generator`.

   ``TOS`` をポップし、それをジェネレータ(:term:`generator`)からyieldします。


.. opcode:: IMPORT_STAR ()

   .. Loads all symbols not starting with ``'_'`` directly from the module TOS to the
   .. local namespace. The module is popped after loading all names. This opcode
   .. implements ``from module import *``.

   ``'_'`` で始まっていないすべてのシンボルをモジュールTOSから直接ローカル名前空間へロードします。
   モジュールはすべての名前をロードした後にポップされます。
   この演算コードは ``from module import *`` を実行します。


.. opcode:: EXEC_STMT ()

   .. Implements ``exec TOS2,TOS1,TOS``.  The compiler fills missing optional
   .. parameters with ``None``.

   ``exec TOS2,TOS1,TOS`` を実行します。コンパイラは見つからないオプションのパラメータを ``None`` で埋めます。


.. opcode:: POP_BLOCK ()

   .. Removes one block from the block stack.  Per frame, there is a  stack of blocks,
   .. denoting nested loops, try statements, and such.

   ブロックスタックからブロックを一つ取り除きます。
   フレームごとにブロックのスタックがあり、ネストしたループ、try文などを意味しています。


.. opcode:: END_FINALLY ()

   .. Terminates a :keyword:`finally` clause.  The interpreter recalls whether the
   .. exception has to be re-raised, or whether the function returns, and continues
   .. with the outer-next block.

   :keyword:`finally` 節を終わらせます。
   インタプリタは例外を再び発生させなければならないかどうか、あるいは、
   関数が返り外側の次のブロックに続くかどうかを思い出します。


.. opcode:: BUILD_CLASS ()

   .. Creates a new class object.  TOS is the methods dictionary, TOS1 the tuple of
   .. the names of the base classes, and TOS2 the class name.

   新しいクラスオブジェクトを作成します。TOSはメソッド辞書、TOS1は基底クラスの名前のタプル、TOS2はクラス名です。


.. opcode:: WITH_CLEANUP ()

   .. Cleans up the stack when a :keyword:`with` statement block exits.  On top of
   .. the stack are 1--3 values indicating how/why the finally clause was entered:

   :keyword:`with` ステートメントブロックがあるときに、スタックをクリーンアップします。
   スタックのトップは 1--3 個の値で、なぜ/どのように finally 項に到達したかを表します:


   * TOP = ``None``
   * (TOP, SECOND) = (``WHY_{RETURN,CONTINUE}``), retval
   * TOP = ``WHY_*``; no retval below it
   * (TOP, SECOND, THIRD) = exc_info()


   .. Under them is EXIT, the context manager's :meth:`__exit__` bound method.

   その下に、コンテキストマネージャーの :meth:`__exit__` バウンドメソッドの EXIT があります。


   .. In the last case, ``EXIT(TOP, SECOND, THIRD)`` is called, otherwise
   .. ``EXIT(None, None, None)``.

   最後のケースでは、 ``EXIT(TOP, SECOND, THIRD)`` が呼ばれ、それ以外では
   ``EXIT(None, None, None)`` が呼ばれます。


   .. EXIT is removed from the stack, leaving the values above it in the same
   .. order. In addition, if the stack represents an exception, *and* the function
   .. call returns a 'true' value, this information is "zapped", to prevent
   .. ``END_FINALLY`` from re-raising the exception.  (But non-local gotos should
   .. still be resumed.)

   EXIT はスタックから取り除かれ、その上の値は順序を維持したまま残されます。
   加えて、スタックが例外を表し、 *かつ* 関数呼び出しが *true* 値を返した場合、
   ``END_FINALLY`` を例外の再創出から守るためにこの情報は削除されます("zapped")。
   (しかし、 non-local goto はなお実行されます)


   .. XXX explain the WHY stuff!


.. All of the following opcodes expect arguments.  An argument is two bytes, with
.. the more significant byte last.

次の演算コードはすべて引数を要求します。引数はより重要なバイトを下位にもつ2バイトです。


.. opcode:: STORE_NAME (namei)

   .. Implements ``name = TOS``. *namei* is the index of *name* in the attribute
   .. :attr:`co_names` of the code object. The compiler tries to use ``STORE_FAST``
   .. or ``STORE_GLOBAL`` if possible.

   ``name = TOS`` を実行します。
   *namei* はコードオブジェクトの属性 :attr:`co_names` における *name* のインデックスです。
   コンパイラは可能ならば ``STORE_FAST`` または ``STORE_GLOBAL`` を使おうとします。


.. opcode:: DELETE_NAME (namei)

   .. Implements ``del name``, where *namei* is the index into :attr:`co_names`
   .. attribute of the code object.

   ``del name`` を実行します。ここで、 *namei* はコードオブジェクトの :attr:`co_names` 属性へのインデックスです。


.. opcode:: UNPACK_SEQUENCE (count)

   .. Unpacks TOS into *count* individual values, which are put onto the stack
   .. right-to-left.

   TOSを *count* 個のへ個別の値に分け、右から左にスタックに置かれます。


.. opcode:: DUP_TOPX (count)

   .. Duplicate *count* items, keeping them in the same order. Due to implementation
   .. limits, *count* should be between 1 and 5 inclusive.

   *count* 個の項目を同じ順番を保ちながら複製します。
   実装上の制限から、 *count* は1から5の間(5を含む)でなければいけません。


.. opcode:: STORE_ATTR (namei)

   .. Implements ``TOS.name = TOS1``, where *namei* is the index of name in
   .. :attr:`co_names`.

   ``TOS.name = TOS1`` を実行します。ここで、 *namei* は :attr:`co_names` における名前のインデックスです。


.. opcode:: DELETE_ATTR (namei)

   .. Implements ``del TOS.name``, using *namei* as index into :attr:`co_names`.

   :attr:`co_names` へのインデックスとして *namei* を使い、 ``del TOS.name`` を実行します。


.. opcode:: STORE_GLOBAL (namei)

   .. Works as ``STORE_NAME``, but stores the name as a global.

   ``STORE_NAME`` として機能しますが、グローバルとして名前を記憶します。


.. opcode:: DELETE_GLOBAL (namei)

   .. Works as ``DELETE_NAME``, but deletes a global name.

   ``DELETE_NAME`` として機能しますが、グルーバル名を削除します。


.. opcode:: LOAD_CONST (consti)

   .. Pushes ``co_consts[consti]`` onto the stack.

   ``co_consts[consti]`` をスタックにプッシュします。


.. opcode:: LOAD_NAME (namei)

   .. Pushes the value associated with ``co_names[namei]`` onto the stack.

   ``co_names[namei]`` に関連付けられた値をスタックにプッシュします。


.. opcode:: BUILD_TUPLE (count)

   .. Creates a tuple consuming *count* items from the stack, and pushes the resulting
   .. tuple onto the stack.

   スタックから *count* 個の項目を消費するタプルを作り出し、できたタプルをスタックにプッシュします。


.. opcode:: BUILD_LIST (count)

   .. Works as ``BUILD_TUPLE``, but creates a list.

   ``BUILD_TUPLE`` として機能しますが、リストを作り出します。


.. opcode:: BUILD_MAP (count)

   .. Pushes a new dictionary object onto the stack.  The dictionary is pre-sized
   .. to hold *count* entries.

   スタックに新しい辞書オブジェクトをプッシュします。
   辞書は *count* 個のエントリを持つサイズに設定されます。


.. opcode:: LOAD_ATTR (namei)

   .. Replaces TOS with ``getattr(TOS, co_names[namei])``.

   TOSを ``getattr(TOS, co_names[namei])`` と入れ替えます。


.. opcode:: COMPARE_OP (opname)

   .. Performs a Boolean operation.  The operation name can be found in
   .. ``cmp_op[opname]``.

   ブール演算を実行します。演算名は ``cmp_op[opname]`` にあります。


.. opcode:: IMPORT_NAME (namei)

   .. Imports the module ``co_names[namei]``.  TOS and TOS1 are popped and provide
   .. the *fromlist* and *level* arguments of :func:`__import__`.  The module
   .. object is pushed onto the stack.  The current namespace is not affected:
   .. for a proper import statement, a subsequent ``STORE_FAST`` instruction
   .. modifies the namespace.

   モジュール ``co_names[namei]`` をインポートします。
   TOS と TOS1 がポップされ、 :func:`__import__` の *fromlist* と *level* 引数になります。
   モジュールオブジェクトはスタックへプッシュされます。現在の名前空間は影響されません:
   適切なimport文に対して、それに続く ``STORE_FAST`` 命令が名前空間を変更します。


.. opcode:: IMPORT_FROM (namei)

   .. Loads the attribute ``co_names[namei]`` from the module found in TOS. The
   .. resulting object is pushed onto the stack, to be subsequently stored by a
   .. ``STORE_FAST`` instruction.

   属性 ``co_names[namei]`` をTOSに見つかるモジュールからロードします。
   作成されたオブジェクトはスタックにプッシュされ、その後 ``STORE_FAST`` 命令によって記憶されます。


.. opcode:: JUMP_FORWARD (delta)

   .. Increments bytecode counter by *delta*.

   バイトコードカウンタを *delta* だけ増加させます。


.. opcode:: JUMP_IF_TRUE (delta)

   .. If TOS is true, increment the bytecode counter by *delta*.  TOS is left on the
   .. stack.

   TOSが真ならば、 *delta* だけバイトコードカウンタを増加させます。TOSはスタックに残されます。


.. opcode:: JUMP_IF_FALSE (delta)

   .. If TOS is false, increment the bytecode counter by *delta*.  TOS is not
   .. changed.

   TOSが偽ならば、 *delta* だけバイトコードカウンタを増加させます。TOSは変更されません。


.. opcode:: JUMP_ABSOLUTE (target)

   .. Set bytecode counter to *target*.

   バイトコードカウンタを *target* に設定します。


.. opcode:: FOR_ITER (delta)

   .. ``TOS`` is an :term:`iterator`.  Call its :meth:`!next` method.  If this
   .. yields a new value, push it on the stack (leaving the iterator below it).  If
   .. the iterator indicates it is exhausted ``TOS`` is popped, and the bytecode
   .. counter is incremented by *delta*.

   ``TOS`` はイテレータです。その :meth:`!next` メソッドを呼び出します。
   これが新しい値を作り出すならば、それを(その下にイテレータを残したまま)スタックにプッシュします。
   イテレータが尽きたことを示した場合は、 ``TOS`` がポップされます。
   そして、バイトコードカウンタが *delta* だけ増やされます。


.. opcode:: LOAD_GLOBAL (namei)

   .. Loads the global named ``co_names[namei]`` onto the stack.

   グルーバル名 ``co_names[namei]`` をスタック上にロードします。


.. opcode:: SETUP_LOOP (delta)

   .. Pushes a block for a loop onto the block stack.  The block spans from the
   .. current instruction with a size of *delta* bytes.

   ブロックスタックにループのためのブロックをプッシュします。
   ブロックは現在の命令から *delta* バイトの大きさを占めます。


.. opcode:: SETUP_EXCEPT (delta)

   .. Pushes a try block from a try-except clause onto the block stack. *delta* points
   .. to the first except block.

   try-except節からtryブロックをブロックスタックにプッシュします。
   *delta* は最初のexceptブロックを指します。


.. opcode:: SETUP_FINALLY (delta)

   .. Pushes a try block from a try-except clause onto the block stack. *delta* points
   .. to the finally block.

   try-except節からtryブロックをブロックスタックにプッシュします。 *delta* はfinallyブロックを指します。


.. opcode:: STORE_MAP ()

   .. Store a key and value pair in a dictionary.  Pops the key and value while leaving
   .. the dictionary on the stack.

   key, value のペアを辞書に格納します。辞書がスタックに残っている間 (while leaving the dictionary on the stack)
   key と value をポップします。


.. opcode:: LOAD_FAST (var_num)

   .. Pushes a reference to the local ``co_varnames[var_num]`` onto the stack.

   ローカルな ``co_varnames[var_num]`` への参照をスタックにプッシュします。


.. opcode:: STORE_FAST (var_num)

   .. Stores TOS into the local ``co_varnames[var_num]``.

   TOSをローカルな ``co_varnames[var_num]`` の中に保存します。


.. opcode:: DELETE_FAST (var_num)

   .. Deletes local ``co_varnames[var_num]``.

   ローカルな ``co_varnames[var_num]`` を削除します。


.. opcode:: LOAD_CLOSURE (i)

   .. Pushes a reference to the cell contained in slot *i* of the cell and free
   .. variable storage.  The name of the variable is  ``co_cellvars[i]`` if *i* is
   .. less than the length of *co_cellvars*.  Otherwise it is  ``co_freevars[i -
   .. len(co_cellvars)]``.

   セルと自由変数記憶領域のスロット *i* に含まれるセルへの参照をプッシュします。
   *i* が *co_cellvars* の長さより小さければ、変数の名前は ``co_cellvars[i]`` です。
   そうでなければ、それは ``co_freevars[i - len(co_cellvars)]`` です。


.. opcode:: LOAD_DEREF (i)

   .. Loads the cell contained in slot *i* of the cell and free variable storage.
   .. Pushes a reference to the object the cell contains on the stack.

   セルと自由変数記憶領域のスロット *i* に含まれるセルをロードします。
   セルが持つオブジェクトへの参照をスタックにプッシュします。


.. opcode:: STORE_DEREF (i)

   .. Stores TOS into the cell contained in slot *i* of the cell and free variable
   .. storage.

   セルと自由変数記憶領域のスロット *i* に含まれるセルへTOSを保存します。


.. opcode:: SET_LINENO (lineno)

   .. This opcode is obsolete.

   このペコードは廃止されました。


.. opcode:: RAISE_VARARGS (argc)

   .. Raises an exception. *argc* indicates the number of parameters to the raise
   .. statement, ranging from 0 to 3.  The handler will find the traceback as TOS2,
   .. the parameter as TOS1, and the exception as TOS.

   例外を発生させます。 *argc* はraise文へ与えるパラメータの数を0から3の範囲で示します。
   ハンドラはTOS2としてトレースバック、TOS1としてパラメータ、そしてTOSとして例外を見つけられます。


.. opcode:: CALL_FUNCTION (argc)

   .. Calls a function.  The low byte of *argc* indicates the number of positional
   .. parameters, the high byte the number of keyword parameters. On the stack, the
   .. opcode finds the keyword parameters first.  For each keyword argument, the value
   .. is on top of the key.  Below the keyword parameters, the positional parameters
   .. are on the stack, with the right-most parameter on top.  Below the parameters,
   .. the function object to call is on the stack.  Pops all function arguments, and
   .. the function itself off the stack, and pushes the return value.

   関数を呼び出します。 *argc* の低位バイトは位置パラメータを示し、高位バイトはキーワードパラメータの数を示します。
   オペコードは最初にキーワードパラメータをスタック上に見つけます。
   それぞれのキーワード引数に対して、その値はキーの上にあります。
   スタック上のキーワードパラメータの下に位置パラメータはあり、先頭に最も右のパラメータがあります。
   スタック上のパラメータの下には、呼び出す関数オブジェクトがあります。
   全ての関数引数をポップし、関数自体もスタックから取り除き、戻り値をプッシュします。


.. opcode:: MAKE_FUNCTION (argc)

   .. Pushes a new function object on the stack.  TOS is the code associated with the
   .. function.  The function object is defined to have *argc* default parameters,
   .. which are found below TOS.

   新しい関数オブジェクトをスタックにプッシュします。
   TOSは関数に関連付けられたコードです。
   関数オブジェクトはTOSの下にある *argc* デフォルトパラメータをもつように定義されます。


.. opcode:: MAKE_CLOSURE (argc)

   .. Creates a new function object, sets its *func_closure* slot, and pushes it on
   .. the stack.  TOS is the code associated with the function, TOS1 the tuple
   .. containing cells for the closure's free variables.  The function also has
   .. *argc* default parameters, which are found below the cells.

   新しい関数オブジェクトを作り出し、その *func_closure* スロットを設定し、それをスタックにプッシュします。
   TOSは関数に関連付けられたコードで、TOS1 はクロージャの自由変数に対する cell を格納したタプルです。
   関数はセルの前にある *argc* デフォルトパラメータも持っています。


.. opcode:: BUILD_SLICE (argc)

   .. index:: builtin: slice

   .. Pushes a slice object on the stack.  *argc* must be 2 or 3.  If it is 2,
   .. ``slice(TOS1, TOS)`` is pushed; if it is 3, ``slice(TOS2, TOS1, TOS)`` is
   .. pushed. See the :func:`slice` built-in function for more information.

   スライスオブジェクトをスタックにプッシュします。 *argc* は2あるいは3でなければなりません。
   2ならば ``slice(TOS1, TOS)`` がプッシュされます。
   3ならば ``slice(TOS2, TOS1, TOS)`` がプッシュされます。
   これ以上の情報については、 :func:`slice()` 組み込み関数を参照してください。


.. opcode:: EXTENDED_ARG (ext)

   .. Prefixes any opcode which has an argument too big to fit into the default two
   .. bytes.  *ext* holds two additional bytes which, taken together with the
   .. subsequent opcode's argument, comprise a four-byte argument, *ext* being the two
   .. most-significant bytes.

   大きすぎてデフォルトの二バイトに当てはめることができない引数をもつあらゆるオペコードの前に置かれます。
   *ext* は二つの追加バイトを保持し、その後ろのオペコードの引数と一緒になって取られます。
   それらは四バイト引数を構成し、 *ext* はその最上位バイトです。


.. opcode:: CALL_FUNCTION_VAR (argc)

   .. Calls a function. *argc* is interpreted as in ``CALL_FUNCTION``. The top element
   .. on the stack contains the variable argument list, followed by keyword and
   .. positional arguments.

   関数を呼び出します。 *argc* は ``CALL_FUNCTION`` のように解釈実行されます。
   スタックの先頭の要素は変数引数リストを含んでおり、その後にキーワードと位置引数が続きます。


.. opcode:: CALL_FUNCTION_KW (argc)

   .. Calls a function. *argc* is interpreted as in ``CALL_FUNCTION``. The top element
   .. on the stack contains the keyword arguments dictionary,  followed by explicit
   .. keyword and positional arguments.

   関数を呼び出します。 *argc* は ``CALL_FUNCTION`` のように解釈実行されます。
   スタックの先頭の要素はキーワード引数辞書を含んでおり、その後に明示的なキーワードと位置引数が続きます。


.. opcode:: CALL_FUNCTION_VAR_KW (argc)

   .. Calls a function. *argc* is interpreted as in ``CALL_FUNCTION``.  The top
   .. element on the stack contains the keyword arguments dictionary, followed by the
   .. variable-arguments tuple, followed by explicit keyword and positional arguments.

   関数を呼び出します。 *argc* は ``CALL_FUNCTION`` のように解釈実行されます。
   スタックの先頭の要素はキーワード引数辞書を含んでおり、その後に変数引数のタプルが続き、
   さらに明示的なキーワードと位置引数が続きます。


.. opcode:: HAVE_ARGUMENT ()

   .. This is not really an opcode.  It identifies the dividing line between opcodes
   .. which don't take arguments ``< HAVE_ARGUMENT`` and those which do ``>=
   .. HAVE_ARGUMENT``.

   これはオペコードではありません。引数をとらないオペコード ``< HAVE_ARGUMENT``  と、
   とるオペコード ``>= HAVE_ARGUMENT`` を分割する行です。
