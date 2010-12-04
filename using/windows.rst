.. highlightlang:: none

.. _using-on-windows:

**************************
 Windows で Python を使う
**************************

.. sectionauthor:: Robert Lehmann <lehmannro@gmail.com>

このドキュメントは、 Python を Microsoft Windows で使うときに知っておくべき、
Windows 独特の動作についての概要を伝えることを目的としています。


Python のインストール
======================

ほとんどの Unix システムやサービスと異なり、 Windows は Python に依存しておらず、
プリインストールの Python はありません。
しかし、 CPython チームは長年にわたり、コンパイル済みの Windows インストーラ
(MSI パッケージ)を `リリース <http://www.python.org/download/releases/>`_
毎に用意しています。


Python の継続的な開発の中で、過去にサポートされていた幾つかのプラットフォームが
(ユーザーと開発者の不足のために) サポートされなくなっています。
全てのサポートされないプラットフォームについての詳細は :pep:`11` をチェックしてください。

* DOS と Windows 3.x は Python 2.0 から廃止予定になり、Python 2.1 でこれらのシステム
  専用のコードは削除されました。
* 2.5 まで、 Python は Windows 95, 98, ME で動きました (ですが、すでにインストール時に
  廃止予定の警告をだしていました)。 Python 2.6 (とその後の全てのリリース) は、
  これらの OS のサポートが止められ、新しいリリースは Windows NT ファミリーしか
  考慮されていません。
* `Windows CE <http://pythonce.sourceforge.net/>`_ は今でもサポートされています。
* `Cygwin <http://cygwin.com/>`_ インストーラも `Python インタープリタ
  <http://cygwin.com/packages/python>`_ のインストールを提供しています。
  これは "Interpreters" の下に置かれています。(cf. `Cygwin package source
  <ftp://ftp.uni-erlangen.de/pub/pc/gnuwin32/cygwin/mirrors/cygnus/
  release/python>`_, `Maintainer releases
  <http://www.tishler.net/jason/software/python/>`_)


コンパイル済みインストーラが提供されているプラットフォームについての詳細な情報は
`Python for Windows (and DOS) <http://www.python.org/download/windows/>`_
を参照してください。


.. seealso::

   `Python on XP <http://www.richarddooling.com/index.php/2006/03/14/python-on-xp-7-minutes-to-hello-world/>`_
      "7 Minutes to "Hello World!""
      by Richard Dooling, 2006

   `Installing on Windows <http://diveintopython.org/installing_python/windows.html>`_
      in "`Dive into Python: Python from novice to pro
      <http://diveintopython.org/index.html>`_"
      by Mark Pilgrim, 2004,
      ISBN 1-59059-356-1

   `For Windows users <http://swaroopch.com/text/Byte_of_Python:Installing_Python#For_Windows_users>`_
      in "Installing Python"
      in "`A Byte of Python <http://www.byteofpython.info>`_"
      by Swaroop C H, 2003


Alternative bundles
===================

Besides the standard CPython distribution, there are modified packages including
additional functionality.  The following is a list of popular versions and their
key features:

`ActivePython <http://www.activestate.com/Products/activepython/>`_
    Installer with multi-platform compatibility, documentation, PyWin32

`Enthought Python Distribution <http://www.enthought.com/products/epd.php>`_
    Popular modules (such as PyWin32) with their respective documentation, tool
    suite for building extensible Python applications

Notice that these packages are likely to install *older* versions of Python.



Configuring Python
==================

In order to run Python flawlessly, you might have to change certain environment
settings in Windows.


Excursus: Setting environment variables
---------------------------------------

Windows has a built-in dialog for changing environment variables (following
guide applies to XP classical view): Right-click the icon for your machine
(usually located on your Desktop and called "My Computer") and choose
:menuselection:`Properties` there.  Then, open the :guilabel:`Advanced` tab
and click the :guilabel:`Environment Variables` button.

In short, your path is:

    :menuselection:`My Computer
    --> Properties
    --> Advanced
    --> Environment Variables`

In this dialog, you can add or modify User and System variables. To change
System variables, you need non-restricted access to your machine
(i.e. Administrator rights).

Another way of adding variables to your environment is using the :command:`set`
command::

    set PYTHONPATH=%PYTHONPATH%;C:\My_python_lib

To make this setting permanent, you could add the corresponding command line to
your :file:`autoexec.bat`. :program:`msconfig` is a graphical interface to this
file.

Viewing environment variables can also be done more straight-forward: The
command prompt will expand strings wrapped into percent signs automatically::

    echo %PATH%

Consult :command:`set /?` for details on this behaviour.

.. seealso::

   http://support.microsoft.com/kb/100843
      Environment variables in Windows NT

   http://support.microsoft.com/kb/310519
      How To Manage Environment Variables in Windows XP

   http://www.chem.gla.ac.uk/~louis/software/faq/q1.html
      Setting Environment variables, Louis J. Farrugia


Finding the Python executable
-----------------------------

Besides using the automatically created start menu entry for the Python
interpreter, you might want to start Python in the DOS prompt.  To make this
work, you need to set your :envvar:`%PATH%` environment variable to include the
directory of your Python distribution, delimited by a semicolon from other
entries.  An example variable could look like this (assuming the first two
entries are Windows' default)::

    C:\WINDOWS\system32;C:\WINDOWS;C:\Python25

Typing :command:`python` on your command prompt will now fire up the Python
interpreter.  Thus, you can also execute your scripts with command line options,
see :ref:`using-on-cmdline` documentation.


Finding modules
---------------

Python usually stores its library (and thereby your site-packages folder) in the
installation directory.  So, if you had installed Python to
:file:`C:\\Python\\`, the default library would reside in
:file:`C:\\Python\\Lib\\` and third-party modules should be stored in
:file:`C:\\Python\\Lib\\site-packages\\`.

.. `` this fixes syntax highlighting errors in some editors due to the \\ hackery

You can add folders to your search path to make Python's import mechanism search
in these directories as well.  Use :envvar:`PYTHONPATH`, as described in
:ref:`using-on-envvars`, to modify :data:`sys.path`.  On Windows, paths are
separated by semicolons, though, to distinguish them from drive identifiers
(:file:`C:\\` etc.).

.. ``

Modifying the module search path can also be done through the Windows registry
under the key :file:`HKLM\\SOFTWARE\\Python\\PythonCore\\{version}\\PythonPath`.
Subkeys which have semicolon-delimited path strings as their default value will
cause each path to be searched.  Multiple subkeys can be created and are
appended to the path in alphabetical order.  A convenient registry editor is
:program:`regedit` (start it by typing "regedit" into :menuselection:`Start -->
Run`).


Executing scripts
-----------------

Python scripts (files with the extension ``.py``) will be executed by
:program:`python.exe` by default.  This executable opens a terminal, which stays
open even if the program uses a GUI.  If you do not want this to happen, use the
extension ``.pyw`` which will cause the script to be executed by
:program:`pythonw.exe` by default (both executables are located in the top-level
of your Python installation directory).  This suppresses the terminal window on
startup.

You can also make all ``.py`` scripts execute with :program:`pythonw.exe`,
setting this through the usual facilities, for example (might require
administrative rights):

#. Launch a command prompt.
#. Associate the correct file group with ``.py`` scripts::

      assoc .py=Python.File

#. Redirect all Python files to the new executable::

      ftype Python.File=C:\Path\to\pythonw.exe "%1" %*


Additional modules
==================

Even though Python aims to be portable among all platforms, there are features
that are unique to Windows.  A couple of modules, both in the standard library
and external, and snippets exist to use these features.

The Windows-specific standard modules are documented in
:ref:`mswin-specific-services`.


PyWin32
-------

The `PyWin32 <http://python.net/crew/mhammond/win32/>`_ module by Mark Hammond
is a collection of modules for advanced Windows-specific support.  This includes
utilities for:

* `Component Object Model <http://www.microsoft.com/com/>`_ (COM)
* Win32 API calls
* Registry
* Event log
* `Microsoft Foundation Classes <http://msdn.microsoft.com/en-us/library/fe1cf721%28VS.80%29.aspx>`_ (MFC)
  user interfaces

`PythonWin <http://web.archive.org/web/20060524042422/
http://www.python.org/windows/pythonwin/>`_ is a sample MFC application
shipped with PyWin32.  It is an embeddable IDE with a built-in debugger.

.. seealso::

   `Win32 How Do I...? <http://timgolden.me.uk/python/win32_how_do_i.html>`_
      by Tim Golden

   `Python and COM <http://www.boddie.org.uk/python/COM.html>`_
      by David and Paul Boddie


Py2exe
------

`Py2exe <http://www.py2exe.org/>`_ is a :mod:`distutils` extension (see
:ref:`extending-distutils`) which wraps Python scripts into executable Windows
programs (:file:`{*}.exe` files).  When you have done this, you can distribute
your application without requiring your users to install Python.


WConio
------

Since Python's advanced terminal handling layer, :mod:`curses`, is restricted to
Unix-like systems, there is a library exclusive to Windows as well: Windows
Console I/O for Python.

`WConio <http://newcenturycomputers.net/projects/wconio.html>`_ is a wrapper for
Turbo-C's :file:`CONIO.H`, used to create text user interfaces.



Compiling Python on Windows
===========================

If you want to compile CPython yourself, first thing you should do is get the
`source <http://python.org/download/source/>`_. You can download either the
latest release's source or just grab a fresh `checkout
<http://www.python.org/dev/faq/#how-do-i-get-a-checkout-of-the-repository-read-only-and-read-write>`_.

For Microsoft Visual C++, which is the compiler with which official Python
releases are built, the source tree contains solutions/project files.  View the
:file:`readme.txt` in their respective directories:

+--------------------+--------------+-----------------------+
| Directory          | MSVC version | Visual Studio version |
+====================+==============+=======================+
| :file:`PC/VC6/`    | 6.0          | 97                    |
+--------------------+--------------+-----------------------+
| :file:`PC/VS7.1/`  | 7.1          | 2003                  |
+--------------------+--------------+-----------------------+
| :file:`PC/VS8.0/`  | 8.0          | 2005                  |
+--------------------+--------------+-----------------------+
| :file:`PCbuild/`   | 9.0          | 2008                  |
+--------------------+--------------+-----------------------+

Note that not all of these build directories are fully supported.  Read the
release notes to see which compiler version the official releases for your
version are built with.

Check :file:`PC/readme.txt` for general information on the build process.


For extension modules, consult :ref:`building-on-windows`.

.. seealso::

   `Python + Windows + distutils + SWIG + gcc MinGW <http://sebsauvage.net/python/mingw.html>`_
      or "Creating Python extensions in C/C++ with SWIG and compiling them with
      MinGW gcc under Windows" or "Installing Python extension with distutils
      and without Microsoft Visual C++" by Sébastien Sauvage, 2003

   `MingW -- Python extensions <http://oldwiki.mingw.org/index.php/Python%20extensions>`_
      by Trent Apted et al, 2007


Other resources
===============

.. seealso::

   `Python Programming On Win32 <http://www.oreilly.com/catalog/pythonwin32/>`_
      "Help for Windows Programmers"
      by Mark Hammond and Andy Robinson, O'Reilly Media, 2000,
      ISBN 1-56592-621-8

   `A Python for Windows Tutorial <http://www.imladris.com/Scripts/PythonForWindows.html>`_
      by Amanda Birmingham, 2004

