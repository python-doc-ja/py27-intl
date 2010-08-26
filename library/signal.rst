:mod:`signal` --- 非同期イベントにハンドラを設定する
====================================================

.. module:: signal
   :synopsis: 非同期イベントにハンドラを設定します。


このモジュールでは Python でシグナルハンドラを使うための機構を提供します。
シグナルとハンドラを扱う上で一般的なルールがいくつかあります:

* 特定のシグナルに対するハンドラが一度設定されると、明示的にリセットしないかぎり設定されたままになります (Python は背後の実装系に関係なく BSD
  形式のインタフェースをエミュレートします)。例外は :const:`SIGCHLD` のハンドラで、この場合は背後の実装系の仕様に従います。

* クリティカルセクションから一時的にシグナルを"ブロック"することはできません。この機能をサポートしないUnix系システムも存在するためです。

* Python のシグナルハンドラは Python のユーザが望む限り非同期で呼び出されますが、呼び出されるのは Python インタプリタの  "原子的な
  (atomic)" 命令実行単位の間です。従って、 (巨大なサイズのテキストに対する正規表現の一致検索のような)  純粋に C
  言語のレベルで実現されている時間のかかる処理中に到着したシグナルは、不定期間遅延する可能性があります。

* シグナルが I/O 操作中に到着すると、シグナルハンドラが処理を返した後に I/O 操作が例外を送出する可能性があります。これは背後にある Unix
  システムが割り込みシステムコールにどういう意味付けをしているかに依存します。

* C 言語のシグナルハンドラは常に処理を返すので、 :const:`SIGFPE` や :const:`SIGSEGV`
  のような同期エラーの捕捉はほとんど意味がありません。

* Python は標準でごく小数のシグナルハンドラをインストールしています: :const:`SIGPIPE` は無視されます
  (従って、パイプやソケットに対する書き込みで生じたエラーは通常の Python 例外として報告されます) :const:`SIGINT` は
  :exc:`KeyboardInterrupt` 例外に変換されます。これらはどれも上書きすることができます。

* シグナルとスレッドの両方を同じプログラムで使用する場合にはいくつか注意が必要です。
  シグナルとスレッドを同時に利用する上で基本的に注意すべきことは、常に:func:`signal`
  命令は主スレッド (main thread)の処理中で実行するということです。
  どのスレッドも :func:`alarm`, :func:`getsignal`, :func:`pause`, :func:`setitimer`, :func:`getitimer` を実行することができます。
  しかし、主スレッドだけが新たなシグナルハンドラを設定することができ、従ってシグナルを受け取ることができるのは主スレッドだけです
  (これは、背後のスレッド実装が個々のスレッドに対するシグナル送信をサポートしているかに関わらず、Python :mod:`signal`
  モジュールが強制している仕様です)。従って、シグナルをスレッド間通信の手段として使うことはできません。代わりにロック機構を使ってください。

以下に :mod:`signal` モジュールで定義されている変数を示します:


.. data:: SIG_DFL

   二つある標準シグナル処理オプションのうちの一つです; 単にシグナルに対する標準の関数を実行します。例えば、ほとんどのシステムでは、
   :const:`SIGQUIT` に対する標準の動作はコアダンプと終了で、 :const:`SIGCHLD` に対する標準の動作は単にシグナルの無視です。


.. data:: SIG_IGN

   もう一つの標準シグナル処理オプションで、単に受け取ったシグナルを無視します。


.. data:: SIG*

   全てのシグナル番号はシンボル定義されています。例えば、ハングアップシグナルは :const:`signal.SIGHUP` で定義されています; 変数名は C
   言語のプログラムで使われているのと同じ名前で、 ``<signal.h>`` にあります。 ':cfunc:`signal`' に関する Unix
   マニュアルページでは、システムで定義されているシグナルを列挙しています (あるシステムではリストは :manpage:`signal(2)`
   に、別のシステムでは :manpage:`signal(7)` に列挙されています)。全てのシステムで同じシグナル名のセットを定義しているわけではないので
   注意してください; このモジュールでは、システムで定義されているシグナル名だけを定義しています。


.. data:: NSIG

   最も大きいシグナル番号に 1 を足した値です。


.. data:: ITIMER_REAL
   .. Decrements interval timer in real time, and delivers :const:`SIGALRM` upon expiration.

   実時間でデクリメントするインターバルタイマーです。タイマーが発火したときに :const:`SIGALRM` を送ります。


.. data:: ITIMER_VIRTUAL

   .. Decrements interval timer only when the process is executing, and delivers
      SIGVTALRM upon expiration.

   プロセスの実行時間だけデクリメントするインターバルタイマーです。タイマーが発火したときに :const:`SIGVTALRM` を送ります。


.. data:: ITIMER_PROF

   .. Decrements interval timer both when the process executes and when the
      system is executing on behalf of the process. Coupled with ITIMER_VIRTUAL,
      this timer is usually used to profile the time spent by the application
      in user and kernel space. SIGPROF is delivered upon expiration.

   プロセスの実行中と、システムがそのプロセスのために実行している時間だけデクリメントするインターバルタイマーです。
   ITIMER_VIRTUAL と組み合わせて、このタイマーはよくアプリケーションがユーザー空間とカーネル空間で消費した時間のプロファイリングに利用されます。
   タイマーが発火したときに :const:`SIGPROF` を送ります。

.. The :mod:`signal` module defines one exception:

:mod:`signal` モジュールは1つの例外を定義しています:

.. exception:: ItimerError

   Raised to signal an error from the underlying :func:`setitimer` or
   :func:`getitimer` implementation. Expect this error if an invalid
   interval timer or a negative time is passed to :func:`setitimer`.
   This error is a subtype of :exc:`IOError`.


:mod:`signal` モジュールでは以下の関数を定義しています:

.. function:: alarm(time)

   *time* がゼロでない値の場合、この関数は *time* 秒後頃に :const:`SIGALRM` をプロセスに送るように要求します。
   それ以前にスケジュールしたアラームはキャンセルされます (常に一つのアラームしかスケジュールできません)。この場合、戻り値は以前に設定
   されたアラームシグナルが通知されるまであと何秒だったかを示す値です。 *time* がゼロの場合、アラームは一切スケジュールされず、現在
   スケジュールされているアラームがキャンセルされます。
   戻り値がゼロの場合、現在アラームがスケジュールされていないことを示します。(Unix マニュアルページ :manpage:`alarm(2)`
   を参照してください)。利用可能: Unix。


.. function:: getsignal(signalnum)

   シグナル *signalnum* に対する現在のシグナルハンドラを返します。戻り値は呼び出し可能な Python
   オブジェクトか、 :const:`signal.SIG_IGN` 、 :const:`signal.SIG_DFL` 、および :const:`None`
   といった特殊な値のいずれかです。ここで :const:`signal.SIG_IGN` は以前そのシグナルが
   無視されていたことを示し、 :const:`signal.SIG_DFL` は以前そのシグナルの標準の処理方法が使われていたことを示し、 ``None``
   はシグナルハンドラがまだ Python によってインストールされていないことを示します。


.. function:: pause()

   シグナルを受け取るまでプロセスを一時停止します; その後、適切なハンドラが呼び出されます。戻り値はありません。Windows では利用できません。(Unix
   マニュアルページ :manpage:`signal(2)` を参照してください。)


.. function:: setitimer(which, seconds[, interval])

   .. Sets given interval timer (one of :const:`signal.ITIMER_REAL`,
      :const:`signal.ITIMER_VIRTUAL` or :const:`signal.ITIMER_PROF`) specified
      by *which* to fire after *seconds* (float is accepted, different from
      :func:`alarm`) and after that every *interval* seconds. The interval
      timer specified by *which* can be cleared by setting seconds to zero.

   *which* で指定されたタイマー(:const:`signal.ITIMER_REAL`, :const:`signal.ITIMER_VIRTUAL`,
   :const:`signal.ITIMER_PROF` のどれか)を、 *seconds* (:func:`alarm` と異なり、floatを指定できます)
   秒後と、それから *interval* 秒間隔で起動するように設定します。
   *seconds* に0を指定すると、そのタイマーをクリアすることができます。

   .. When an interval timer fires, a signal is sent to the process.
      The signal sent is dependent on the timer being used;
      :const:`signal.ITIMER_REAL` will deliver :const:`SIGALRM`,
      :const:`signal.ITIMER_VIRTUAL` sends :const:`SIGVTALRM`,
      and :const:`signal.ITIMER_PROF` will deliver :const:`SIGPROF`.

   インターバルタイマーが起動したとき、シグナルがプロセスに送られます。
   送られるシグナルは利用されたタイマーの種類に依存します。
   :const:`signal.ITIMER_REAL` の場合は :const:`SIGALRM` が、
   :const:`signal.ITIMER_VIRTUAL` の場合は :const:`SIGVTALRM` が、
   :const:`signal.ITIMER_PROF` の場合は :const:`SIGPROF` が送られます。

   .. The old values are returned as a tuple: (delay, interval).

   戻り値は古い値が (delay, interval) のタプルです。

   .. Attempting to pass an invalid interval timer will cause a :exc:`ItimerError`.

   無効なインターバルタイマーを渡すと :exc:`ItimerError` 例外を発生させます。

   .. versionadded:: 2.6


.. function:: getitimer(which)

   .. Returns current value of a given interval timer specified by *which*.

   *which* で指定されたインターバルタイマーの現在の値を返します。

   .. versionadded:: 2.6


.. function:: set_wakeup_fd(fd)

   .. Set the wakeup fd to *fd*.  When a signal is received, a ``'\0'`` byte is
      written to the fd.  This can be used by a library to wakeup a poll or select
      call, allowing the signal to be fully processed.

   wakeup fd を *fd* に設定します。
   シグナルを受信したときに、 ``'\0'`` バイトがそのfdに書き込まれます。
   これは、pollやselectをしているライブラリを起こして、シグナルの処理をさせるのに利用できます。

   .. The old wakeup fd is returned.  *fd* must be non-blocking.  It is up to the
      library to remove any bytes before calling poll or select again.

   戻り値は古い wakeup fd です。
   *fd* はノンブロッキングでなければなりません。
   起こされたライブラリは、次の poll や select を実行する前にこの fd からすべてのバイトを取り除かなければなりません。

   .. When threads are enabled, this function can only be called from the main thread;
      attempting to call it from other threads will cause a :exc:`ValueError`
      exception to be raised.

   スレッドが有効な場合、この関数はメインスレッドからしか実行できません。
   それ以外のスレッドからこの関数を実行しようとすると :exc:`ValueError` 例外が発生します。


.. function:: siginterrupt(signalnum, flag)

   .. Change system call restart behaviour: if *flag* is :const:`False`, system calls
      will be restarted when interrupted by signal *signalnum*, otherwise system calls will
      be interrupted. Returns nothing. Availability: Unix (see the man page
      :manpage:`siginterrupt(3)` for further information).

   システムコールのリスタートの動作を変更します。
   *flag* が :const:`False` の場合、 *signalnum* シグナルに中断されたシステムコールは再実行されます。
   それ以外の場合、システムコールは中断されます。戻り値はありません。

   利用できる環境: Unix (詳しい情報についてはman page :manpage:`siginterrupt(3)` を参照してください)

   .. Note that installing a signal handler with :func:`signal` will reset the restart
      behaviour to interruptible by implicitly calling :cfunc:`siginterrupt` with a true *flag*
      value for the given signal.

   :func:`signal` を使ってシグナルハンドラを設定したときに、暗黙のうちに :cfunc:`siginterrupt` を
   *flag* に true を指定して実行され、

   .. versionadded:: 2.6



.. function:: signal(signalnum, handler)

   シグナル *signalnum* に対するハンドラを関数 *handler* にします。 *handler* は二つの引数 (下記参照) を取る呼び出し可能な
   Python  オブジェクトにするか、 :const:`signal.SIG_IGN` あるいは :const:`signal.SIG_DFL`
   といった特殊な値にすることができます。以前に使われていたシグナルハンドラが返されます (上記の :func:`getsignal`
   の記述を参照してください)。 (Unix マニュアルページ :manpage:`signal(2)` を参照してください。)

   複数スレッドの使用が有効な場合、この関数は主スレッドからのみ呼び出すことができます; 主スレッド以外のスレッドで呼び出そうとすると、例外
   :exc:`ValueError` が送出されます。

   .. index:: object: frame

   *handler* は二つの引数: シグナル番号、および現在のスタックフレーム (``None`` またはフレームオブジェクト; フレームオブジェクトに
   ついての記述はリファレンスマニュアルの標準型の階層か、 :mod:`inspect` モジュールの属性の説明を参照してください)、とともに呼び出されます。


.. _signal-example:

例
--

以下は最小限のプログラム例です。この例では :func:`alarm` を使って、ファイルを開く処理を待つのに費やす時間を制限します;
これはそのファイルが電源の入れられていないシリアルデバイスを表している場合に有効で、通常こうした場合には :func:`os.open`
は未定義の期間ハングアップしてしまいます。ここではファイルを開くまで 5 秒間のアラームを設定することで解決しています; ファイルを
開く処理が長くかかりすぎると、アラームシグナルが送信され、ハンドラが例外を送出するようになっています。 ::

   import signal, os

   pdef handler(signum, frame):
       print 'Signal handler called with signal', signum
       raise IOError, "Couldn't open device!"

   # Set the signal handler and a 5-second alarm
   signal.signal(signal.SIGALRM, handler)
   signal.alarm(5)

   # This open() may hang indefinitely
   fd = os.open('/dev/ttyS0', os.O_RDWR)

   signal.alarm(0)          # Disable the alarm

