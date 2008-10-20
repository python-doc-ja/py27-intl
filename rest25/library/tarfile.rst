
:mod:`tarfile` --- Read and write tar archive files
===================================================

.. module:: tarfile
   :synopsis: Read and write tar-format archive files.


.. versionadded:: 2.3

.. moduleauthor:: Lars Gustäbel <lars@gustaebel.de>
.. sectionauthor:: Lars Gustäbel <lars@gustaebel.de>


The :mod:`tarfile` module makes it possible to read and create tar archives.
Some facts and figures:

* reads and writes :mod:`gzip` and :mod:`bzip2` compressed archives.

* creates POSIX 1003.1-1990 compliant or GNU tar compatible archives.

* reads GNU tar extensions *longname*, *longlink* and *sparse*.

* stores pathnames of unlimited length using GNU tar extensions.

* handles directories, regular files, hardlinks, symbolic links, fifos,
  character devices and block devices and is able to acquire and restore file
  information like timestamp, access permissions and owner.

* can handle tape devices.


.. function:: open([name[, mode [, fileobj[, bufsize]]]])

   Return a :class:`TarFile` object for the pathname *name*. For detailed
   information on :class:`TarFile` objects, see TarFile Objects (section
   :ref:`tarfile-objects`).

   *mode* has to be a string of the form ``'filemode[:compression]'``, it defaults
   to ``'r'``. Here is a full list of mode combinations:

   +------------------+------------------------------------------+
   | mode             | action                                   |
   +==================+==========================================+
   | ``'r' or 'r:*'`` | Open for reading with transparent        |
   |                  | compression (recommended).               |
   +------------------+------------------------------------------+
   | ``'r:'``         | Open for reading exclusively without     |
   |                  | compression.                             |
   +------------------+------------------------------------------+
   | ``'r:gz'``       | Open for reading with gzip compression.  |
   +------------------+------------------------------------------+
   | ``'r:bz2'``      | Open for reading with bzip2 compression. |
   +------------------+------------------------------------------+
   | ``'a' or 'a:'``  | Open for appending with no compression.  |
   +------------------+------------------------------------------+
   | ``'w' or 'w:'``  | Open for uncompressed writing.           |
   +------------------+------------------------------------------+
   | ``'w:gz'``       | Open for gzip compressed writing.        |
   +------------------+------------------------------------------+
   | ``'w:bz2'``      | Open for bzip2 compressed writing.       |
   +------------------+------------------------------------------+

   Note that ``'a:gz'`` or ``'a:bz2'`` is not possible. If *mode* is not suitable
   to open a certain (compressed) file for reading, :exc:`ReadError` is raised. Use
   *mode* ``'r'`` to avoid this.  If a compression method is not supported,
   :exc:`CompressionError` is raised.

   If *fileobj* is specified, it is used as an alternative to a file object opened
   for *name*.

   For special purposes, there is a second format for *mode*:
   ``'filemode|[compression]'``.  :func:`open` will return a :class:`TarFile`
   object that processes its data as a stream of blocks.  No random seeking will be
   done on the file. If given, *fileobj* may be any object that has a :meth:`read`
   or :meth:`write` method (depending on the *mode*). *bufsize* specifies the
   blocksize and defaults to ``20 * 512`` bytes. Use this variant in combination
   with e.g. ``sys.stdin``, a socket file object or a tape device. However, such a
   :class:`TarFile` object is limited in that it does not allow to be accessed
   randomly, see "Examples" (section :ref:`tar-examples`).  The currently possible
   modes:

   +-------------+--------------------------------------------+
   | Mode        | Action                                     |
   +=============+============================================+
   | ``'r|*'``   | Open a *stream* of tar blocks for reading  |
   |             | with transparent compression.              |
   +-------------+--------------------------------------------+
   | ``'r|'``    | Open a *stream* of uncompressed tar blocks |
   |             | for reading.                               |
   +-------------+--------------------------------------------+
   | ``'r|gz'``  | Open a gzip compressed *stream* for        |
   |             | reading.                                   |
   +-------------+--------------------------------------------+
   | ``'r|bz2'`` | Open a bzip2 compressed *stream* for       |
   |             | reading.                                   |
   +-------------+--------------------------------------------+
   | ``'w|'``    | Open an uncompressed *stream* for writing. |
   +-------------+--------------------------------------------+
   | ``'w|gz'``  | Open an gzip compressed *stream* for       |
   |             | writing.                                   |
   +-------------+--------------------------------------------+
   | ``'w|bz2'`` | Open an bzip2 compressed *stream* for      |
   |             | writing.                                   |
   +-------------+--------------------------------------------+


.. class:: TarFile

   Class for reading and writing tar archives. Do not use this class directly,
   better use :func:`open` instead. See "TarFile Objects" (section
   :ref:`tarfile-objects`).


.. function:: is_tarfile(name)

   Return :const:`True` if *name* is a tar archive file, that the :mod:`tarfile`
   module can read.


.. class:: TarFileCompat(filename[, mode[, compression]])

   Class for limited access to tar archives with a :mod:`zipfile`\ -like interface.
   Please consult the documentation of the :mod:`zipfile` module for more details.
   *compression* must be one of the following constants:


   .. data:: TAR_PLAIN

      Constant for an uncompressed tar archive.


   .. data:: TAR_GZIPPED

      Constant for a :mod:`gzip` compressed tar archive.


.. exception:: TarError

   Base class for all :mod:`tarfile` exceptions.


.. exception:: ReadError

   Is raised when a tar archive is opened, that either cannot be handled by the
   :mod:`tarfile` module or is somehow invalid.


.. exception:: CompressionError

   Is raised when a compression method is not supported or when the data cannot be
   decoded properly.


.. exception:: StreamError

   Is raised for the limitations that are typical for stream-like :class:`TarFile`
   objects.


.. exception:: ExtractError

   Is raised for *non-fatal* errors when using :meth:`extract`, but only if
   :attr:`TarFile.errorlevel`\ ``== 2``.


.. seealso::

   Module :mod:`zipfile`
      Documentation of the :mod:`zipfile` standard module.

   `GNU tar manual, Basic Tar Format <http://www.gnu.org/software/tar/manual/html_node/tar_134.html#SEC134>`_
      Documentation for tar archive files, including GNU tar extensions.

.. % -----------------
.. % TarFile Objects
.. % -----------------


.. _tarfile-objects:

TarFile Objects
---------------

The :class:`TarFile` object provides an interface to a tar archive. A tar
archive is a sequence of blocks. An archive member (a stored file) is made up of
a header block followed by data blocks. It is possible, to store a file in a tar
archive several times. Each archive member is represented by a :class:`TarInfo`
object, see TarInfo Objects (section :ref:`tarinfo-objects`) for details.


.. class:: TarFile([name [, mode[, fileobj]]])

   Open an *(uncompressed)* tar archive *name*. *mode* is either ``'r'`` to read
   from an existing archive, ``'a'`` to append data to an existing file or ``'w'``
   to create a new file overwriting an existing one. *mode* defaults to ``'r'``.

   If *fileobj* is given, it is used for reading or writing data. If it can be
   determined, *mode* is overridden by *fileobj*'s mode.

   .. note::

      *fileobj* is not closed, when :class:`TarFile` is closed.


.. method:: TarFile.open(...)

   Alternative constructor. The :func:`open` function on module level is actually a
   shortcut to this classmethod. See section :ref:`module-tarfile` for details.


.. method:: TarFile.getmember(name)

   Return a :class:`TarInfo` object for member *name*. If *name* can not be found
   in the archive, :exc:`KeyError` is raised.

   .. note::

      If a member occurs more than once in the archive, its last occurrence is assumed
      to be the most up-to-date version.


.. method:: TarFile.getmembers()

   Return the members of the archive as a list of :class:`TarInfo` objects. The
   list has the same order as the members in the archive.


.. method:: TarFile.getnames()

   Return the members as a list of their names. It has the same order as the list
   returned by :meth:`getmembers`.


.. method:: TarFile.list(verbose=True)

   Print a table of contents to ``sys.stdout``. If *verbose* is :const:`False`,
   only the names of the members are printed. If it is :const:`True`, output
   similar to that of :program:`ls -l` is produced.


.. method:: TarFile.next()

   Return the next member of the archive as a :class:`TarInfo` object, when
   :class:`TarFile` is opened for reading. Return ``None`` if there is no more
   available.


.. method:: TarFile.extractall([path[, members]])

   Extract all members from the archive to the current working directory or
   directory *path*. If optional *members* is given, it must be a subset of the
   list returned by :meth:`getmembers`. Directory informations like owner,
   modification time and permissions are set after all members have been extracted.
   This is done to work around two problems: A directory's modification time is
   reset each time a file is created in it. And, if a directory's permissions do
   not allow writing, extracting files to it will fail.

   .. versionadded:: 2.5


.. method:: TarFile.extract(member[, path])

   Extract a member from the archive to the current working directory, using its
   full name. Its file information is extracted as accurately as possible. *member*
   may be a filename or a :class:`TarInfo` object. You can specify a different
   directory using *path*.

   .. note::

      Because the :meth:`extract` method allows random access to a tar archive there
      are some issues you must take care of yourself. See the description for
      :meth:`extractall` above.


.. method:: TarFile.extractfile(member)

   Extract a member from the archive as a file object. *member* may be a filename
   or a :class:`TarInfo` object. If *member* is a regular file, a file-like object
   is returned. If *member* is a link, a file-like object is constructed from the
   link's target. If *member* is none of the above, ``None`` is returned.

   .. note::

      The file-like object is read-only and provides the following methods:
      :meth:`read`, :meth:`readline`, :meth:`readlines`, :meth:`seek`, :meth:`tell`.


.. method:: TarFile.add(name[, arcname[, recursive]])

   Add the file *name* to the archive. *name* may be any type of file (directory,
   fifo, symbolic link, etc.). If given, *arcname* specifies an alternative name
   for the file in the archive. Directories are added recursively by default. This
   can be avoided by setting *recursive* to :const:`False`; the default is
   :const:`True`.


.. method:: TarFile.addfile(tarinfo[, fileobj])

   Add the :class:`TarInfo` object *tarinfo* to the archive. If *fileobj* is given,
   ``tarinfo.size`` bytes are read from it and added to the archive.  You can
   create :class:`TarInfo` objects using :meth:`gettarinfo`.

   .. note::

      On Windows platforms, *fileobj* should always be opened with mode ``'rb'`` to
      avoid irritation about the file size.


.. method:: TarFile.gettarinfo([name[, arcname[, fileobj]]])

   Create a :class:`TarInfo` object for either the file *name* or the file object
   *fileobj* (using :func:`os.fstat` on its file descriptor).  You can modify some
   of the :class:`TarInfo`'s attributes before you add it using :meth:`addfile`.
   If given, *arcname* specifies an alternative name for the file in the archive.


.. method:: TarFile.close()

   Close the :class:`TarFile`. In write mode, two finishing zero blocks are
   appended to the archive.


.. attribute:: TarFile.posix

   If true, create a POSIX 1003.1-1990 compliant archive. GNU extensions are not
   used, because they are not part of the POSIX standard.  This limits the length
   of filenames to at most 256, link names to 100 characters and the maximum file
   size to 8 gigabytes. A :exc:`ValueError` is raised if a file exceeds this limit.
   If false, create a GNU tar compatible archive.  It will not be POSIX compliant,
   but can store files without any of the above restrictions.

   .. versionchanged:: 2.4
      *posix* defaults to :const:`False`.


.. attribute:: TarFile.dereference

   If false, add symbolic and hard links to archive. If true, add the content of
   the target files to the archive.  This has no effect on systems that do not
   support symbolic links.


.. attribute:: TarFile.ignore_zeros

   If false, treat an empty block as the end of the archive. If true, skip empty
   (and invalid) blocks and try to get as many members as possible. This is only
   useful for concatenated or damaged archives.


.. attribute:: TarFile.debug=0

   To be set from ``0`` (no debug messages; the default) up to ``3`` (all debug
   messages). The messages are written to ``sys.stderr``.


.. attribute:: TarFile.errorlevel

   If ``0`` (the default), all errors are ignored when using :meth:`extract`.
   Nevertheless, they appear as error messages in the debug output, when debugging
   is enabled.  If ``1``, all *fatal* errors are raised as :exc:`OSError` or
   :exc:`IOError` exceptions.  If ``2``, all *non-fatal* errors are raised as
   :exc:`TarError` exceptions as well.

.. % -----------------
.. % TarInfo Objects
.. % -----------------


.. _tarinfo-objects:

TarInfo Objects
---------------

A :class:`TarInfo` object represents one member in a :class:`TarFile`. Aside
from storing all required attributes of a file (like file type, size, time,
permissions, owner etc.), it provides some useful methods to determine its type.
It does *not* contain the file's data itself.

:class:`TarInfo` objects are returned by :class:`TarFile`'s methods
:meth:`getmember`, :meth:`getmembers` and :meth:`gettarinfo`.


.. class:: TarInfo([name])

   Create a :class:`TarInfo` object.


.. method:: TarInfo.frombuf()

   Create and return a :class:`TarInfo` object from a string buffer.


.. method:: TarInfo.tobuf(posix)

   Create a string buffer from a :class:`TarInfo` object. See :class:`TarFile`'s
   :attr:`posix` attribute for information on the *posix* argument. It defaults to
   :const:`False`.

   .. versionadded:: 2.5
      The *posix* parameter.

A ``TarInfo`` object has the following public data attributes:


.. attribute:: TarInfo.name

   Name of the archive member.


.. attribute:: TarInfo.size

   Size in bytes.


.. attribute:: TarInfo.mtime

   Time of last modification.


.. attribute:: TarInfo.mode

   Permission bits.


.. attribute:: TarInfo.type

   File type.  *type* is usually one of these constants: :const:`REGTYPE`,
   :const:`AREGTYPE`, :const:`LNKTYPE`, :const:`SYMTYPE`, :const:`DIRTYPE`,
   :const:`FIFOTYPE`, :const:`CONTTYPE`, :const:`CHRTYPE`, :const:`BLKTYPE`,
   :const:`GNUTYPE_SPARSE`.  To determine the type of a :class:`TarInfo` object
   more conveniently, use the ``is_*()`` methods below.


.. attribute:: TarInfo.linkname

   Name of the target file name, which is only present in :class:`TarInfo` objects
   of type :const:`LNKTYPE` and :const:`SYMTYPE`.


.. attribute:: TarInfo.uid

   User ID of the user who originally stored this member.


.. attribute:: TarInfo.gid

   Group ID of the user who originally stored this member.


.. attribute:: TarInfo.uname

   User name.


.. attribute:: TarInfo.gname

   Group name.

A :class:`TarInfo` object also provides some convenient query methods:


.. method:: TarInfo.isfile()

   Return :const:`True` if the :class:`Tarinfo` object is a regular file.


.. method:: TarInfo.isreg()

   Same as :meth:`isfile`.


.. method:: TarInfo.isdir()

   Return :const:`True` if it is a directory.


.. method:: TarInfo.issym()

   Return :const:`True` if it is a symbolic link.


.. method:: TarInfo.islnk()

   Return :const:`True` if it is a hard link.


.. method:: TarInfo.ischr()

   Return :const:`True` if it is a character device.


.. method:: TarInfo.isblk()

   Return :const:`True` if it is a block device.


.. method:: TarInfo.isfifo()

   Return :const:`True` if it is a FIFO.


.. method:: TarInfo.isdev()

   Return :const:`True` if it is one of character device, block device or FIFO.

.. % ------------------------
.. % Examples
.. % ------------------------


.. _tar-examples:

Examples
--------

How to extract an entire tar archive to the current working directory::

   import tarfile
   tar = tarfile.open("sample.tar.gz")
   tar.extractall()
   tar.close()

How to create an uncompressed tar archive from a list of filenames::

   import tarfile
   tar = tarfile.open("sample.tar", "w")
   for name in ["foo", "bar", "quux"]:
       tar.add(name)
   tar.close()

How to read a gzip compressed tar archive and display some member information::

   import tarfile
   tar = tarfile.open("sample.tar.gz", "r:gz")
   for tarinfo in tar:
       print tarinfo.name, "is", tarinfo.size, "bytes in size and is",
       if tarinfo.isreg():
           print "a regular file."
       elif tarinfo.isdir():
           print "a directory."
       else:
           print "something else."
   tar.close()

How to create a tar archive with faked information::

   import tarfile
   tar = tarfile.open("sample.tar.gz", "w:gz")
   for name in namelist:
       tarinfo = tar.gettarinfo(name, "fakeproj-1.0/" + name)
       tarinfo.uid = 123
       tarinfo.gid = 456
       tarinfo.uname = "johndoe"
       tarinfo.gname = "fake"
       tar.addfile(tarinfo, file(name))
   tar.close()

The *only* way to extract an uncompressed tar stream from ``sys.stdin``::

   import sys
   import tarfile
   tar = tarfile.open(mode="r|", fileobj=sys.stdin)
   for tarinfo in tar:
       tar.extract(tarinfo)
   tar.close()

