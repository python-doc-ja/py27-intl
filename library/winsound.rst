
:mod:`winsound` --- Windows 用の音声再生インタフェース
======================================================

.. module:: winsound
   :platform: Windows
   :synopsis: Windows の音声再生機構へのアクセス。
.. moduleauthor:: Toby Dickenson <htrd90@zepler.org>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


.. versionadded:: 1.5.2

:mod:`winsound` モジュールは Windows プラットフォーム上で提供されて
いる基本的な音声再生機構へのアクセス手段を提供します。このモジュールでは いくつかの関数と定数が定義されています。


.. function:: Beep(frequency, duration)

   PC のスピーカを鳴らします。 引数 *frequency* は鳴らす音の周波数の指定で、単位は Hz です。 値は 37 から 32.767
   でなくてはなりません。 引数 *duration* は音を何ミリ秒鳴らすかの指定です。 システムがスピーカを鳴らすことができない場合、例外
   :exc:`RuntimeError` が送出されます。

   .. note::

      Windows 95 および 98 では、Windows の関数 :cfunc:`Beep` は存在しますが役に立ちません
      (この関数は引数を無視します)。これらの ケースでは、Python はポートを直接操作して :cfunc:`Beep`  をシミュレートします (バージョン
      2.1 で追加されました) 。この機能が 全てのシステムで動作するかどうかはわかりません。

   .. versionadded:: 1.6


.. function:: PlaySound(sound, flags)

   プラットフォームの API から関数 :cfunc:`PlaySound` を呼び出します。 引数 *sound* はファイル名、音声データの文字列、または
   ``None`` をとり得ます。*sound* の解釈は *flags* の値に依存します。この値は 以下に述べる定数をビット単位で OR
   して組み合わせたものになります。 システムのエラーが発生した場合、例外 :exc:`RuntimeError` が送出されます。


.. function:: MessageBeep([type=``MB_OK``])

   根底にある :cfunc:`MessageBeep` 関数をプラットフォームの API から 呼び出します。この関数は音声をレジストリの指定に従って再生します。
   *type* 引数はどの音声を再生するかを指定します; とり得る値は ``-1`` 、 ``MB_ICONASTERISK`` 、
   ``MB_ICONEXCLAMATION`` 、 ``MB_ICONHAND`` 、 ``MB_ICONQUESTION`` 、および ``MB_OK`` で、
   全て以下に記述されています。 値 ``-1`` は "単純なビープ音" を再生します; この値は他の場合で音声を再生することができなかった
   際の最終的な代替音です。

   .. versionadded:: 2.3


.. data:: SND_FILENAME

   *sound* パラメタが WAV ファイル名であることを示します。 :const:`SND_ALIAS` と同時に使ってはいけません。


.. data:: SND_ALIAS

   引数 *sound* はレジストリにある音声データに関連付けられた名前で あることを示します。指定した名前がレジストリ上にない場合、定数
   :const:`SND_NODEFAULT` が同時に指定されていない限り、システム標準の 音声データが再生されます。標準の音声データが登録されていない場合、
   例外 :exc:`RuntimeError` が送出されます。 :const:`SND_FILENAME` と同時に使ってはいけません。

   全ての Win32 システムは少なくとも以下の名前をサポートします; ほとんどの システムでは他に多数あります:

   +--------------------------+--------------------------------------+
   | :func:`PlaySound` *name* | 対応するコントロールパネルでの音声名 |
   +==========================+======================================+
   | ``'SystemAsterisk'``     | Asterisk                             |
   +--------------------------+--------------------------------------+
   | ``'SystemExclamation'``  | Exclamation                          |
   +--------------------------+--------------------------------------+
   | ``'SystemExit'``         | Exit Windows                         |
   +--------------------------+--------------------------------------+
   | ``'SystemHand'``         | Critical Stop                        |
   +--------------------------+--------------------------------------+
   | ``'SystemQuestion'``     | Question                             |
   +--------------------------+--------------------------------------+

   例えば以下のように使います::

      import winsound
      # Play Windows exit sound.
      winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

      # Probably play Windows default sound, if any is registered (because
      # "*" probably isn't the registered name of any sound).
      winsound.PlaySound("*", winsound.SND_ALIAS)


.. data:: SND_LOOP

   音声データを繰り返し再生します。システムがブロックしないようにするため、 :const:`SND_ASYNC` フラグを同時に使わなくてはなりません。
   :const:`SND_MEMORY` と同時に使うことはできません。


.. data:: SND_MEMORY

   :func:`PlaySound` の引数 *sound* が文字列の形式をとった WAV  ファイルのメモリ上のイメージであることを示します。

   .. note::

      このモジュールはメモリ上のイメージを非同期に再生する機能をサポート していません。従って、このフラグと :const:`SND_ASYNC` を組み合わせると
      例外 :exc:`RuntimeError` が送出されます。


.. data:: SND_PURGE

   指定した音声の全てのインスタンスについて再生処理を停止します。


.. data:: SND_ASYNC

   音声を非同期に再生するようにして、関数呼び出しを即座に返します。


.. data:: SND_NODEFAULT

   指定した音声が見つからなかった場合にシステム標準の音声を鳴らさないように します。


.. data:: SND_NOSTOP

   現在鳴っている音声を中断させないようにします。


.. data:: SND_NOWAIT

   サウンドドライバがビジー状態にある場合、関数がすぐ返るようにします。


.. data:: MB_ICONASTERISK

   音声 ``SystemDefault`` を再生します。


.. data:: MB_ICONEXCLAMATION

   音声 ``SystemExclamation`` を再生します。


.. data:: MB_ICONHAND

   音声 ``SystemHand`` を再生します。


.. data:: MB_ICONQUESTION

   音声 ``SystemQuestion`` を再生します。


.. data:: MB_OK

   音声 ``SystemDefault`` を再生します。

