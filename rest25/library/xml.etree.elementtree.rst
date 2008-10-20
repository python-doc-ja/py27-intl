
:mod:`xml.etree.ElementTree` --- The ElementTree XML API
========================================================

.. module:: xml.etree.ElementTree
   :synopsis: Implementation of the ElementTree API.
.. moduleauthor:: Fredrik Lundh <fredrik@pythonware.com>


.. versionadded:: 2.5

The Element type is a flexible container object, designed to store hierarchical
data structures in memory. The type can be described as a cross between a list
and a dictionary.

Each element has a number of properties associated with it:

* a tag which is a string identifying what kind of data this element represents
  (the element type, in other words).

* a number of attributes, stored in a Python dictionary.

* a text string.

* an optional tail string.

* a number of child elements, stored in a Python sequence

To create an element instance, use the Element or SubElement factory functions.

The :class:`ElementTree` class can be used to wrap an element structure, and
convert it from and to XML.

A C implementation of this API is available as :mod:`xml.etree.cElementTree`.


.. _elementtree-functions:

Functions
---------


.. function:: Comment([text])

   Comment element factory.  This factory function creates a special element that
   will be serialized as an XML comment. The comment string can be either an 8-bit
   ASCII string or a Unicode string. *text* is a string containing the comment
   string.


   .. data:: Returns:
      :noindex:

      An element instance, representing a comment.


.. function:: dump(elem)

   Writes an element tree or element structure to sys.stdout.  This function should
   be used for debugging only.

   The exact output format is implementation dependent.  In this version, it's
   written as an ordinary XML file.

   *elem* is an element tree or an individual element.


.. function:: Element(tag[, attrib][, **extra])

   Element factory.  This function returns an object implementing the standard
   Element interface.  The exact class or type of that object is implementation
   dependent, but it will always be compatible with the _ElementInterface class in
   this module.

   The element name, attribute names, and attribute values can be either 8-bit
   ASCII strings or Unicode strings. *tag* is the element name. *attrib* is an
   optional dictionary, containing element attributes. *extra* contains additional
   attributes, given as keyword arguments.


   .. data:: Returns:
      :noindex:

      An element instance.


.. function:: fromstring(text)

   Parses an XML section from a string constant.  Same as XML. *text* is a string
   containing XML data.


   .. data:: Returns:
      :noindex:

      An Element instance.


.. function:: iselement(element)

   Checks if an object appears to be a valid element object. *element* is an
   element instance.


   .. data:: Returns:
      :noindex:

      A true value if this is an element object.


.. function:: iterparse(source[, events])

   Parses an XML section into an element tree incrementally, and reports what's
   going on to the user. *source* is a filename or file object containing XML data.
   *events* is a list of events to report back.  If omitted, only "end" events are
   reported.


   .. data:: Returns:
      :noindex:

      A (event, elem) iterator.


.. function:: parse(source[, parser])

   Parses an XML section into an element tree. *source* is a filename or file
   object containing XML data. *parser* is an optional parser instance.  If not
   given, the standard XMLTreeBuilder parser is used.


   .. data:: Returns:
      :noindex:

      An ElementTree instance


.. function:: ProcessingInstruction(target[, text])

   PI element factory.  This factory function creates a special element that will
   be serialized as an XML processing instruction. *target* is a string containing
   the PI target. *text* is a string containing the PI contents, if given.


   .. data:: Returns:
      :noindex:

      An element instance, representing a PI.


.. function:: SubElement(parent, tag[, attrib] [, **extra])

   Subelement factory.  This function creates an element instance, and appends it
   to an existing element.

   The element name, attribute names, and attribute values can be either 8-bit
   ASCII strings or Unicode strings. *parent* is the parent element. *tag* is the
   subelement name. *attrib* is an optional dictionary, containing element
   attributes. *extra* contains additional attributes, given as keyword arguments.


   .. data:: Returns:
      :noindex:

      An element instance.


.. function:: tostring(element[, encoding])

   Generates a string representation of an XML element, including all subelements.
   *element* is an Element instance. *encoding* is the output encoding (default is
   US-ASCII).


   .. data:: Returns:
      :noindex:

      An encoded string containing the XML data.


.. function:: XML(text)

   Parses an XML section from a string constant.  This function can be used to
   embed "XML literals" in Python code. *text* is a string containing XML data.


   .. data:: Returns:
      :noindex:

      An Element instance.


.. function:: XMLID(text)

   Parses an XML section from a string constant, and also returns a dictionary
   which maps from element id:s to elements. *text* is a string containing XML
   data.


   .. data:: Returns:
      :noindex:

      A tuple containing an Element instance and a dictionary.


.. _elementtree-elementtree-objects:

ElementTree Objects
-------------------


.. class:: ElementTree([element,] [file])

   ElementTree wrapper class.  This class represents an entire element hierarchy,
   and adds some extra support for serialization to and from standard XML.

   *element* is the root element. The tree is initialized with the contents of the
   XML *file* if given.


.. method:: ElementTree._setroot(element)

   Replaces the root element for this tree.  This discards the current contents of
   the tree, and replaces it with the given element.  Use with care. *element* is
   an element instance.


.. method:: ElementTree.find(path)

   Finds the first toplevel element with given tag. Same as getroot().find(path).
   *path* is the element to look for.


   .. data:: Returns:
      :noindex:

      The first matching element, or None if no element was found.


.. method:: ElementTree.findall(path)

   Finds all toplevel elements with the given tag. Same as getroot().findall(path).
   *path* is the element to look for.


   .. data:: Returns:
      :noindex:

      A list or iterator containing all matching elements, in section order.


.. method:: ElementTree.findtext(path[, default])

   Finds the element text for the first toplevel element with given tag.  Same as
   getroot().findtext(path). *path* is the toplevel element to look for. *default*
   is the value to return if the element was not found.


   .. data:: Returns:
      :noindex:

      The text content of the first matching element, or the default value no element
      was found.  Note that if the element has is found, but has no text content, this
      method returns an empty string.


.. method:: ElementTree.getiterator([tag])

   Creates a tree iterator for the root element.  The iterator loops over all
   elements in this tree, in section order. *tag* is the tag to look for (default
   is to return all elements)


   .. data:: Returns:
      :noindex:

      An iterator.


.. method:: ElementTree.getroot()

   Gets the root element for this tree.


   .. data:: Returns:
      :noindex:

      An element instance.


.. method:: ElementTree.parse(source[, parser])

   Loads an external XML section into this element tree. *source* is a file name or
   file object. *parser* is an optional parser instance.  If not given, the
   standard XMLTreeBuilder parser is used.


   .. data:: Returns:
      :noindex:

      The section root element.


.. method:: ElementTree.write(file[, encoding])

   Writes the element tree to a file, as XML. *file* is a file name, or a file
   object opened for writing. *encoding* is the output encoding (default is US-
   ASCII).


.. _elementtree-qname-objects:

QName Objects
-------------


.. class:: QName(text_or_uri[, tag])

   QName wrapper.  This can be used to wrap a QName attribute value, in order to
   get proper namespace handling on output. *text_or_uri* is a string containing
   the QName value, in the form {uri}local, or, if the tag argument is given, the
   URI part of a QName. If *tag* is given, the first argument is interpreted as an
   URI, and this argument is interpreted as a local name.


   .. data:: Returns:
      :noindex:

      An opaque object, representing the QName.


.. _elementtree-treebuilder-objects:

TreeBuilder Objects
-------------------


.. class:: TreeBuilder([element_factory])

   Generic element structure builder.  This builder converts a sequence of start,
   data, and end method calls to a well-formed element structure. You can use this
   class to build an element structure using a custom XML parser, or a parser for
   some other XML-like format. The *element_factory* is called to create new
   Element instances when given.


.. method:: TreeBuilder.close()

   Flushes the parser buffers, and returns the toplevel documen element.


   .. data:: Returns:
      :noindex:

      An Element instance.


.. method:: TreeBuilder.data(data)

   Adds text to the current element. *data* is a string.  This should be either an
   8-bit string containing ASCII text, or a Unicode string.


.. method:: TreeBuilder.end(tag)

   Closes the current element. *tag* is the element name.


   .. data:: Returns:
      :noindex:

      The closed element.


.. method:: TreeBuilder.start(tag, attrs)

   Opens a new element. *tag* is the element name. *attrs* is a dictionary
   containing element attributes.


   .. data:: Returns:
      :noindex:

      The opened element.


.. _elementtree-xmltreebuilder-objects:

XMLTreeBuilder Objects
----------------------


.. class:: XMLTreeBuilder([html,] [target])

   Element structure builder for XML source data, based on the expat parser. *html*
   are predefined HTML entities.  This flag is not supported by the current
   implementation. *target* is the target object.  If omitted, the builder uses an
   instance of the standard TreeBuilder class.


.. method:: XMLTreeBuilder.close()

   Finishes feeding data to the parser.


   .. data:: Returns:
      :noindex:

      An element structure.


.. method:: XMLTreeBuilder.doctype(name, pubid, system)

   Handles a doctype declaration. *name* is the doctype name. *pubid* is the public
   identifier. *system* is the system identifier.


.. method:: XMLTreeBuilder.feed(data)

   Feeds data to the parser.

   *data* is encoded data.

