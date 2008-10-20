
.. _using:

***************************
Using Python on a Macintosh
***************************

.. sectionauthor:: Bob Savage <bobsavage@mac.com>


Python on a Macintosh running Mac OS X is in principle very similar to Python on
any other Unixplatform, but there are a number of additional features such as
the IDE and the Package Manager that are worth pointing out.

Python on Mac OS 9 or earlier can be quite different from Python on Unix or
Windows, but is beyond the scope of this manual, as that platform is no longer
supported, starting with Python 2.4. See `<http://www.cwi.nl/~jack/macpython>`_
for installers for the latest 2.3 release for Mac OS 9 and related
documentation.


.. _getting-osx:

Getting and Installing MacPython
================================

Mac OS X 10.3 comes with Python 2.3 pre-installed by Apple. This installation
does not come with the IDE and other additions, however, so to get these you
need to install the :program:`MacPython for Panther additions` from the
MacPython website, `<http://www.cwi.nl/~jack/macpython>`_.

For MacPython 2.4, or for any MacPython on earlier releases of Mac OS X, you
need to install a full distribution from the same website.

What you get after installing is a number of things:

* A :file:`MacPython-2.3` folder in your :file:`Applications` folder. In here
  you find the PythonIDE Integrated Development Environment; PythonLauncher, which
  handles double-clicking Python scripts from the Finder; and the Package Manager.

* A fairly standard Unix commandline Python interpreter in
  :file:`/usr/local/bin/python`, but without the usual
  :file:`/usr/local/lib/python`.

* A framework :file:`/Library/Frameworks/Python.framework`, where all the action
  really is, but which you usually do not have to be aware of.

To uninstall MacPython you can simply remove these three things.

If you use the "additions" installer to install on top of an existing Apple-
Python you will not get the framework and the commandline interpreter, as they
have been installed by Apple already, in
:file:`/System/Library/Frameworks/Python.framework` and :file:`/usr/bin/python`,
respectively. You should in principle never modify or delete these, as they are
Apple-controlled and may be used by Apple- or third-party software.

PythonIDE contains an Apple Help Viewer book called "MacPython Help" which you
can access through its help menu. If you are completely new to Python you should
start reading the IDE introduction in that document.

If you are familiar with Python on other Unix platforms you should read the
section on running Python scripts from the Unix shell.


How to run a Python script
--------------------------

Your best way to get started with Python on Mac OS X is through the PythonIDE
integrated development environment, see section :ref:`ide` and use the Help menu
when the IDE is running.

If you want to run Python scripts from the Terminal window command line or from
the Finder you first need an editor to create your script. Mac OS X comes with a
number of standard Unix command line editors, :program:`vim` and
:program:`emacs` among them. If you want a more Mac-like editor
:program:`BBEdit` or :program:`TextWrangler` from Bare Bones Software (see
`<http://www.barebones.com/products/bbedit/index.shtml>`_) are good choices.
:program:`AppleWorks` or any other word processor that can save files in ASCII
is also a possibility, including :program:`TextEdit` which is included with OS
X.

To run your script from the Terminal window you must make sure that
:file:`/usr/local/bin` is in your shell search path.

To run your script from the Finder you have two options:

* Drag it to :program:`PythonLauncher`

* Select :program:`PythonLauncher` as the default application to open your
  script (or any .py script) through the finder Info window and double-click it.

PythonLauncher has various preferences to control how your script is launched.
Option-dragging allows you to change these for one invocation, or use its
Preferences menu to change things globally.


.. _osx-gui-scripts:

Running scripts with a GUI
--------------------------

There is one Mac OS X quirk that you need to be aware of: programs that talk to
the Aqua window manager (in other words, anything that has a GUI) need to be run
in a special way. Use :program:`pythonw` instead of :program:`python` to start
such scripts.


configuration
-------------

MacPython honours all standard Unix environment variables such as
:envvar:`PYTHONPATH`, but setting these variables for programs started from the
Finder is non-standard as the Finder does not read your :file:`.profile` or
:file:`.cshrc` at startup. You need to create a file
:file:`~/.MacOSX/environment.plist`. See Apple's Technical Document QA1067 for
details.

Installing additional Python packages is most easily done through the Package
Manager, see the MacPython Help Book for details.


.. _ide:

The IDE
=======

The :program:`Python IDE` (Integrated Development Environment) is a separate
application that acts as a text editor for your Python code, a class browser, a
graphical debugger, and more.

The online Python Help contains a quick walkthrough of the IDE that shows the
major features and how to use them.


Using the "Python Interactive" window
-------------------------------------

Use this window like you would use a normal Unix command line interpreter.


.. _idewrite:

Writing a Python Script
-----------------------

In addition to using the :program:`Python IDE` interactively, you can also type
out a complete Python program, saving it incrementally, and execute it or
smaller selections of it.

You can create a new script, open a previously saved script, and save your
currently open script by selecting the appropriate item in the "File" menu.
Dropping a Python script onto the :program:`Python IDE` will open it for
editing.

When the :program:`Python IDE` saves a script, it uses the creator code settings
which are available by clicking on the small black triangle on the top right of
the document window, and selecting "save options". The default is to save the
file with the :program:`Python IDE` as the creator, this means that you can open
the file for editing by simply double-clicking on its icon. You might want to
change this behaviour so that it will be opened by the
:program:`PythonLauncher`, and run. To do this simply choose "PythonLauncher"
from the "save options". Note that these options are associated with the *file*
not the application.


.. _ideexecution:

Executing a script from within the IDE
--------------------------------------

You can run the script in the frontmost window of the :program:`Python IDE` by
hitting the run all button.  You should be aware, however that if you use the
Python convention ``if __name__ == "__main__":`` the script will *not* be
"__main__" by default. To get that behaviour you must select the "Run as
__main__" option from the small black triangle on the top right of the document
window.  Note that this option is associated with the *file* not the
application. It *will* stay active after a save, however; to shut this feature
off simply select it again.


.. _ideapplet:

"Save as" versus "Save as Applet"
---------------------------------

When you are done writing your Python script you have the option of saving it as
an "applet" (by selecting "Save as applet" from the "File" menu). This has a
significant advantage in that you can drop files or folders onto it, to pass
them to the applet the way command-line users would type them onto the command-
line to pass them as arguments to the script. However, you should make sure to
save the applet as a separate file, do not overwrite the script you are writing,
because you will not be able to edit it again.

Accessing the items passed to the applet via "drag-and-drop" is done using the
standard :attr:`sys.argv` mechanism. See the general documentation for more
Note that saving a script as an applet will not make it runnable on a system
without a Python installation.

.. % need to link to the appropriate place in non-Mac docs

.. % \subsection{Debugger}
.. % **NEED INFO HERE**
.. % \subsection{Module Browser}
.. % **NEED INFO HERE**
.. % \subsection{Profiler}
.. % **NEED INFO HERE**
.. % end IDE
.. % \subsection{The ``Scripts'' menu}
.. % **NEED INFO HERE**


The Package Manager
===================

Historically MacPython came with a number of useful extension packages included,
because most Macintosh users do not have access to a development environment and
C compiler. For Mac OS X that bundling is no longer done, but a new mechanism
has been made available to allow easy access to extension packages.

The Python Package Manager helps you installing additional packages that enhance
Python. It determines the exact MacOS version  and Python version you have and
uses that information to download  a database that has packages that are tested
and tried on that combination. In other words: if something is in your Package
Manager  window but does not work you are free to blame the database maintainer.

PackageManager then checks which of the packages you have installed  and which
ones are not. This should also work when you have installed packages  outside of
PackageManager.  You can select packages and install them, and PackageManager
will work out the requirements and install these too.

Often PackageManager will list a package in two flavors: binary  and source.
Binary should always work, source will only work if  you have installed the
Apple Developer Tools. PackageManager will warn  you about this, and also about
other external dependencies.

PackageManager is available as a separate application and also  as a function of
the IDE, through the File->Package Manager menu  entry.

