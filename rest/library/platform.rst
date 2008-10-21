
:mod:`platform` ---  実行中プラットフォームの固有情報を参照する
===============================================================

.. module:: platform
   :synopsis: 実行中プラットフォームからできるだけ多くの固有情報を取得する
.. moduleauthor:: Marc-Andre Lemburg <mal@egenix.com>
.. sectionauthor:: Bjorn Pettersen <bpettersen@corp.fairisaac.com>


.. versionadded:: 2.3

.. note::

   プラットフォーム毎にアルファベット順に並べています。Linuxについては Unixセクションを参照してください。


クロス プラットフォーム
-----------------------


.. function:: architecture(executable=sys.executable, bits='', linkage='')

   *executable*で指定した実行可能ファイル（省略時はPythonインタープリ タのバイナリ）の各種アーキテクチャ情報を調べます。

   戻り値はタプル``(bits, linkage)``で、アーキテクチャのビット数と実行 可能ファイルのリンク形式を示します。どちらの値も文字列で返ります。

   値が不明な場合は、パラメータで指定した値が返ります。*bits*を
   ``''``と指定した場合、ビット数として:cfunc:`sizeof(pointer)`が返
   ります。（Pythonのバージョンが1.5.2以下の場合は、サポートされているポ インタサイズとして:cfunc:`sizeof(long)`を使用します。）

   この関数は、システムの:file:`file`コマンドを使用します。:file:`file`はほ
   とんどのUnixプラットフォームと一部の非Unixプラットフォームで利用
   可能ですが、:file:`file`コマンドが利用できず、かつ*executable*が Pythonインタープリタでない場合には適切なデフォルト値が返ります。


.. function:: machine()

   ``'i386'``のような、機種を返します。不明な場合は空文字列を返します。


.. function:: node()

   コンピュータのネットワーク名を返します。ネットワーク名は完全修飾名とは 限りません。不明な場合は空文字列を返します。


.. function:: platform(aliased=0, terse=0)

   実行中プラットフォームを識別する文字列を返します。この文字列には、有益 な情報をできるだけ多く付加しています。

   戻り値は機械で処理しやすい形式ではなく、*人間にとって読みやすい* 形式となっています。異なったプラットフォームでは異なった戻り値となるよ うになっています。

   *aliased* が真なら、システムの名称として一般的な名称ではなく、別名 を使用して結果を返します。たとえば、SunOS は Solaris
   となります。この 機能は :func:`system_alias` で実装されています。

   *terse*が真なら、プラットフォームを特定するために最低限必要な情報 だけを返します。


.. function:: processor()

   ``'amdk6'``のような、（現実の）プロセッサ名を返します。

   不明な場合は空文字列を返します。NetBSDのようにこの情報を提供しない、ま たは:func:`machine`と同じ値しか返さないプラットフォームも多く存在
   しますので、注意してください。


.. function:: python_build()

   Pythonのビルド番号と日付を、``(buildno, builddate)``の タプルで返します。


.. function:: python_compiler()

   Pythonをコンパイルする際に使用したコンパイラを示す文字列を返します。


.. function:: python_version()

   Pythonのバージョンを、``'major.minor.patchlevel'``形式の文字列で返 します。

   ``sys.version``と異なり、patchlevel（デフォルトでは0)も必ず含まれて います。


.. function:: python_version_tuple()

   Pythonのバージョンを、文字列のタプル ``(major, minor, patchlevel)``  で返します。

   ``sys.version``と異なり、patchlevel（デフォルトでは``0``)も必ず 含まれています。


.. function:: release()

   ``'2.2.0'`` や ``'NT'`` のような、システムのリリース情報を返しま す。不明な場合は空文字列を返します。


.. function:: system()

   ``'Linux'``, ``'Windows'``, ``'Java'`` のような、システム/OS 名を返します。不明な場合は空文字列を返します。


.. function:: system_alias(system, release, version)

   マーケティング目的で使われる一般的な別名に変換して``(system, release, version)`` を返します。混乱を避けるために、情報を
   並べなおす場合があります。


.. function:: version()

   ``'#3 on degas'``のような、システムのリリース情報を返します。不明 な場合は空文字列を返します。


.. function:: uname()

   非常に可搬性の高い uname インターフェースで、実行中プラットフォームを 示す情報を、文字列のタプル``(system, node, release,
   version, machine, processor)`` で返し ます。

   :func:`os.uname`と異なり、複数のプロセッサ名が候補としてタプルに 追加される場合があります。

   不明な項目は ``''``となります。


Java プラットフォーム
---------------------


.. function:: java_ver(release='', vendor='', vminfo=('','',''), osinfo=('','',''))

   Jython用のバージョンインターフェースで、タプル``(release, vendor, vminfo, osinfo)`` を返します。*vminfo*は
   タプル``(vm_name, vm_release, vm_vendor)``、 *osinfo*はタプル``(os_name, os_version,
   os_arch)``です。不明な項目は引数で指定した値（デフォルトは ``''``）となります。


Windows プラットフォーム
------------------------


.. function:: win32_ver(release='', version='', csd='', ptype='')

   Windowsのレジストリからバージョン情報を取得し、バージョン番号/CSDレベ ル/OSタイプ（シングルプロセッサ又はマルチプロセッサ）をタプル
   ``(version, csd, ptype)``で返します。

   参考：*ptype*はシングルプロセッサのNT上では ``'Uniprocessor Free'``、マルチプロセッサでは ``'Multiprocessor
   Free'``となります。*'Free'* がついている場合 はデバッグ用のコードが含まれていないことを示し、*'Checked'*がつい
   ていれば引数や範囲のチェックなどのデバッグ用コードが含まれていることを 示します。

   .. note::

      この関数は、Mark Hammondの:mod:`win32all`がインストールされたWin32 互換プラットフォームでのみ利用可能です。


Win95/98 固有
^^^^^^^^^^^^^


.. function:: popen(cmd, mode='r', bufsize=None)

   可搬性の高い :func:`popen` インターフェースで、可能なら
   :func:`win32pipe.popen`を使用します。:func:`win32pipe.popen` はWindows
   NTでは利用可能ですが、Windows 9xではハングしてしまいます。

   .. % This KnowledgeBase article appears to be missing...
   .. % See also \ulink{MS KnowledgeBase article Q150956}{}.


Mac OS プラットフォーム
-----------------------


.. function:: mac_ver(release='', versioninfo=('','',''), machine='')

   Mac OSのバージョン情報を、タプル``(release, versioninfo, machine)``で返します。*versioninfo* は、タ
   プル``(version, dev_stage, non_release_version)`` です。

   不明な項目は``''``となります。タプルの要素は全て文字列です。

   この関数で使用している:cfunc:`gestalt` API については、
   `<http://www.rgaros.nl/gestalt/>`_を参照してください。


Unix プラットフォーム
---------------------


.. function:: dist(distname='', version='', id='', supported_dists=('SuSE','debian','redhat','mandrake'))

   OSディストリビューション名の取得を試みます。戻り値はタプル ``(distname, version, id)``で、不明な項目は引数で
   指定した値となります。


.. function:: libc_ver(executable=sys.executable, lib='', version='', chunksize=2048)

   executableで指定したファイル（省略時はPythonインタープリタ）がリンクし ているlibcバージョンの取得を試みます。戻り値は文字列のタプル
   ``(lib, version)``で、不明な項目は引数で指定した値とな ります。

   この関数は、実行形式に追加されるシンボルの細かな違いによって、libcの バージョンを特定します。この違いは:program:`gcc`でコンパイルされた実行
   可能ファイルでのみ有効だと思われます。

   *chunksize*にはファイルから情報を取得するために読み込むバイト数を 指定します。

