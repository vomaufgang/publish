=========================
anited_publish - Overview
=========================

anited_publish is a python package with command line interface to turn markdown files
into ebooks.

Created to make publishing stories a lot easier for myself.

* **Free software**: `MIT <https://opensource.org/licenses/MIT>`_
* **Official page**: https://anited.de/publish
* **Documentation**: https://docs.anited.de/publish

Build status
============

* master: |MASTER| |MASTERCOVERAGE|

Features
========

* Write your book entirely in markdown.

* Use whatever text editor you like, as long as it produces utf8 plain text files.

  (If you don't have a favourite text editor yet, go take a look at Graeme Gott's excellent
  FocusWriter. You will not regret it.)

* Describe your project and desired output in a simple python file.

  A simple project might look like this:

  .. code-block:: python

    from anited_publish.book import Book, Chapter
    from anited_publish.output import HtmlOutput, EbookConvertOutput
    from anited_publish.substitution import SimpleSubstitution

    book = Book(
        title='Example',
        authors='Max Mustermann',
        language='en')

    book.chapters.extend(
        [Chapter(src='first_chapter.md'),
         Chapter(src='second_chapter.md')])

    substitution = SimpleSubstitution(
        old='Cows',
        new='Substitutions')

    html_output = HtmlOutput(
        path='example.html',
        stylesheet='style.css')
    html_output.make(book, [substitution])

    ebook_output = EbookConvertOutput(
        path='example.epub',
        stylesheet='style.css')
    ebook_output.make(book, [substitution])

  Given the above is saved in a file :code:`my_project.py` and the markdown
  files are present, the output :code:`my_book.html` can be created
  by executing

  .. code-block:: shell

    python my_project.py

  on the command line.

  .. note:: Unix/Linux users might have to call python3 instead, depending on
            their distribution.

  A more in depth guide to anited_publish including additional features like multiple
  outputs, default outputs, text substitutions and more can be found at at
  https://docs.anited.de/publish.

  If complete and working examples are more to your liking you can find such an
  example project in the **examples** directory of the repository.

* The following output types are available:

  * HTML, as in 'good old hyper text markup language'
  * epub, mobi, azw3 or, to be exact, any format calibre/ebook-convert supports

    (requires an additional installation of `Kavid Goyal's Calibre <https://calibre-ebook.com/>`_)

* The following output types are planned for an upcoming version:

  * HTML in JSON for use with https://gitlab.com/anited/read

Installation
============

For the time being apub is only available via this git repository. You can use pip to install it
into your local or virtual Python environment:

.. code-block:: shell

  pip install https://gitlab.com/anited/publish/-/archive/master/publish-master.zip

.. |MASTER| image:: https://gitlab.com/anited/publish/badges/master/build.svg
   :target: https://gitlab.com/anited/publish/commits/master

.. |MASTERCOVERAGE| image:: https://gitlab.com/anited/publish/badges/master/coverage.svg?job=cover
   :target: https://gitlab.com/anited/publish/commits/master

.. Currently unused badges:
   image:: https://badge.fury.io/py/apub.png
        :target: http://badge.fury.io/py/apub
   image:: https://pypip.in/d/apub/badge.png
        :target: https://pypi.python.org/pypi/apub
