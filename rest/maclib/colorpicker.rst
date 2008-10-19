
:mod:`ColorPicker` --- 色選択ダイアログ
===============================

.. module:: ColorPicker
   :platform: Mac
   :synopsis: 標準色選択ダイアログへのインターフェース
.. moduleauthor:: Just van Rossum <just@letterror.com>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


.. % Color selection dialog
.. % Interface to the standard color selection dialog.

:mod:`ColorPicker` モジュールは標準色選択ダイアログへのアクセスを提 供します。

.. % % The \module{ColorPicker} module provides access to the standard color
.. % % picker dialog.


.. function:: GetColor(prompt, rgb)

   標準色選択ダイアログを表示し、ユーザが色を選択することを可能にします。 *prompt* の文字列によりユーザに指示を与えられ、デフォルトの選択 色を
   *rgb* で設定する事ができます。*rgb* は赤、緑、青の色要 素のタプルで与えてください。:func:`GetColor` はユーザが選択した
   色のタプルと色が選択されたか、取り消されたかを示すフラグを返します。

   .. % %   Show a standard color selection dialog and allow the user to select
   .. % %   a color.  The user is given instruction by the \var{prompt} string,
   .. % %   and the default color is set to \var{rgb}.  \var{rgb} must be a
   .. % %   tuple giving the red, green, and blue components of the color.
   .. % %   \function{GetColor()} returns a tuple giving the user's selected
   .. % %   color and a flag indicating whether they accepted the selection of
   .. % %   cancelled.

