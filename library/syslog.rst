
:mod:`syslog` --- Unix syslog ライブラリルーチン群
==================================================

.. module:: syslog
   :platform: Unix
   :synopsis: Unix syslog ライブラリルーチン群へのインタフェース。


このモジュールでは Unix ``syslog`` ライブラリルーチン群へのインタフェースを提供します。
``syslog`` の便宜レベルに関する詳細な記述は Unix マニュアルページを参照してください。

このモジュールでは以下の関数を定義しています:


.. function:: syslog([priority,] message)

   文字列 *message* をシステムログ機構に送信します。
   末尾の改行文字は必要に応じて追加されます。
   各メッセージは *facility* および *level* からなる優先度でタグ付けされます。
   オプションの *priority* 引数はメッセージの優先度を定義します。
   標準の値は :const:`LOG_INFO` です。
   *priority* 中に、便宜レベルが  (``LOG_INFO | LOG_USER`` のように)
   論理和を使ってコード化されていない場合、 :func:`openlog` を呼び出した際の値が使われます。


.. function:: openlog(ident[, logopt[, facility]])

   標準以外のログオプションは、 :func:`syslog` の呼び出しに先立って :func:`openlog`
   でログファイルを開く際、明示的に設定することができます。
   標準の値は (通常) *indent* = ``'syslog'`` 、 *logopt* =
   ``0`` 、 *facility* = :const:`LOG_USER` です。
   *ident* 引数は全てのメッセージの先頭に付加する文字列です。
   オプションの *logopt* 引数はビットフィールドの値になります - とりうる組み合わせ\
   値については以下を参照してください。 オプションの *facility* 引数は、
   便宜レベルコードの設定が明示的になされていないメッセージに対する、
   標準の便宜レベルを設定します。


.. function:: closelog()

   ログファイルを閉じます。


.. function:: setlogmask(maskpri)

   優先度マスクを *maskpri* に設定し、以前のマスク値を返します。
   *maskpri* に設定されていない優先度レベルを持った
   :func:`syslog` の呼び出しは無視されます。標準では全ての優先度をログ出力します。
   関数 ``LOG_MASK(pri)`` は個々の優先度
   *pri* に対する優先度マスクを計算します。関数 ``LOG_UPTO(pri)`` は優先度 *pri*
   までの全ての優先度を含むようなマスクを計算します。

このモジュールでは以下の定数を定義しています:

優先度 (高い優先度順):
   :const:`LOG_EMERG` 、 :const:`LOG_ALERT` 、 :const:`LOG_CRIT` 、 :const:`LOG_ERR` 、
   :const:`LOG_WARNING` 、 :const:`LOG_NOTICE` 、 :const:`LOG_INFO` 、
   :const:`LOG_DEBUG` 。

便宜レベル:
   :const:`LOG_KERN` 、 :const:`LOG_USER` 、 :const:`LOG_MAIL` 、 :const:`LOG_DAEMON` 、
   :const:`LOG_AUTH` 、 :const:`LOG_LPR` 、 :const:`LOG_NEWS` 、 :const:`LOG_UUCP` 、
   :const:`LOG_CRON` 、および :const:`LOG_LOCAL0` から :const:`LOG_LOCAL7` 。

ログオプション:
   ``<syslog.h>`` で定義されている場合、 :const:`LOG_PID` 、 :const:`LOG_CONS` 、
   :const:`LOG_NDELAY` 、 :const:`LOG_NOWAIT` 、および :const:`LOG_PERROR` 。

