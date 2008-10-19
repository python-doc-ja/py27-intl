
:mod:`distutils` --- Python モジュールの構築とインストール
===========================================

.. module:: distutils
   :synopsis: 現在インストールされている Python に追加するためのモジュール構築、 および実際のインストールを支援する。
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


:mod:`distutils` パッケージは、現在インストールされている Python に
追加するためのモジュール構築、および実際のインストールを支援します。 新規のモジュールは 100%-pure Python でも、C
で書かれた拡張モジュールでも、 あるいは Python と C 両方のコードが入っているモジュールからなる Python パッケージでもかまいません。

このパッケージは、Python ドキュメンテーション パッケージに含まれている これとは別の
2つのドキュメントで詳しく説明されています。:mod:`distutils` の機能を使って新しいモジュールを配布する方法は、 Python
モジュールを配布する (XXX reference: ../dist/dist.html) に書かれています。 このドキュメントには distutils
を拡張する方法も含まれています。 Python モジュールをインストールする方法は、 モジュールの作者が :mod:`distutils`
パッケージを使っている場合でもいない場合でも、 Python モジュールをインストールする (XXX reference: ../inst/inst.html)
に書かれています。


.. seealso::

   `Python モジュールを配布する <../dist/dist.html>`_
      このマニュアルは Python モジュールの開発者およびパッケージ担当に向けたものです。 ここでは、現在インストールされている Python に簡単に追加できる
      :mod:`distutils`ベースのパッケージをどうやって用意するかについて 説明しています。

   `Python モジュールをインストールする <../inst/inst.html>`_
      現在インストールされている Python にモジュールを追加するための 情報が書かれた "管理者" 向けのマニュアルです。 この文書を読むのに Python
      プログラマである必要はありません。

