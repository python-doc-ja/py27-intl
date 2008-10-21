.. _documenting-index:

######################
  Documenting Python
######################


.. The Python language has a substantial body of documentation, much of it
.. contributed by various authors. The markup used for the Python documentation is
.. `reStructuredText`_, developed by the `docutils`_ project, amended by custom
.. directives and using a toolset named *Sphinx* to postprocess the HTML output.

Python には様々な著者により寄稿された非常に多くのドキュメント類があります。
Python のドキュメントのマークアップには、 `docutils`_ プロジェクトによって
開発された `reStructuredText`_ を、独自のディレクティブ (directive) で拡張して
利用しています。そして、 *Sphinx* というツールセットを利用して、HTML 出力へと
変換しています。

.. This document describes the style guide for our documentation, the custom
.. reStructuredText markup introduced to support Python documentation and how it
.. should be used, as well as the Sphinx build system.

このドキュメントでは、ドキュメントを作成する上でのスタイルガイドと、 
Python のドキュメントのために作られた独自の reStructuredText マークアップと
その利用方法、そして Sphinx のビルドシステムについて説明します。

.. _reStructuredText: http://docutils.sf.net/rst.html
.. _docutils: http://docutils.sf.net/

.. If you're interested in contributing to Python's documentation, there's no need
.. to write reStructuredText if you're not so inclined; plain text contributions
.. are more than welcome as well.

Python のドキュメントを寄贈したいと思っているなら、そのために reStructuredText
をわざわざ学ぶ必要はありません; 平文での寄贈も大歓迎です。

.. toctree::

   intro.rst
   style.rst
   rest.rst
   markup.rst
   sphinx.rst

.. XXX add credits, thanks etc.

