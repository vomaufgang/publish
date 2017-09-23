===============
apub - Overview
===============

apub is a python package with command line interface to turn markdown files
into ebooks.

Created to make publishing stories a lot easier for myself.

* **Free software**: `MIT <https://opensource.org/licenses/MIT>`_
* **Official page**: https://anited.de/apub
* **Documentation**: https://apub.readthedocs.org.

.. .. image:: https://badge.fury.io/py/apub.png
        :target: http://badge.fury.io/py/apub

.. .. image:: https://pypip.in/d/apub/badge.png
        :target: https://pypi.python.org/pypi/apub

Build status
============

* develop: |DEVELOP| |DEVCOVERAGE|
* master: |MASTER| |MASTERCOVERAGE|

.. |DEVELOP| image:: https://travis-ci.org/vomaufgang/apub.svg?branch=develop
   :target: https://travis-ci.org/vomaufgang/apub/branches

.. |MASTER| image:: https://travis-ci.org/vomaufgang/apub.svg?branch=master
   :target: https://travis-ci.org/vomaufgang/apub/branches

.. |DEVCOVERAGE| image:: https://coveralls.io/repos/github/vomaufgang/apub/badge.svg?branch=develop
   :target: https://coveralls.io/github/vomaufgang/apub?branch=develop

.. |MASTERCOVERAGE| image:: https://coveralls.io/repos/github/vomaufgang/apub/badge.svg?branch=master
   :target: https://coveralls.io/github/vomaufgang/apub?branch=master

Features
========

* Write your book entirely in markdown.

* Use whatever text editor you like, as long as it produces utf8 plain text files.

  (If you don't have a favourite text editor yet, go take a look at Graeme Gott's excellent FocusWriter.
  You will not regret it.)

* Describe your project and desired output in a simple python file.

  Import apub, describe your project in python using the apub api
  and your python file will automatically accept commands like :code:`make`
  when called from the command line.

  A simple project might look like this:

  .. code-block:: python

    from apub.book import Book, Chapter
    from apub.output import HtmlOutput, EbookConvertOutput
    from apub.substitution import SimpleSubstitution

    book = Book(
        title='Example',
        authors='Max Mustermann',
        language='en')

    book.chapters.extend(
        [Chapter(source='first_chapter.md'),
         Chapter(source='second_chapter.md')])

    substitution = SimpleSubstitution(
        old='Cows',
        new='Substitutions')

    html_output = HtmlOutput(
        path='example.html',
        css_path='style.css')
    html_output.make(book, [substitution])

    ebook_output = EbookConvertOutput(
        path='example.epub',
        css_path='style.css')
    ebook_output.make(book, [substitution])

  Given the above is saved in a file :code:`my_project.py` and the markdown
  files are present, the output :code:`my_book.html` can be created
  by simply executing

  .. code-block:: shell

    python my_project.py

  on the command line.

  .. note:: Unix/Linux users might have to call python3 instead, depending on
            their distribution.

  A more in depth guide to apub including additional features like multiple
  outputs, default outputs, text substitutions and more can be found at at
  https://apub.readthedocs.org

  If complete and working examples are more to your liking you can find such a
  documented example project in the **examples** subfolder of the repository.

* The following output types are available:

  * HTML, as in 'good old hyper text markup language'
  * epub, mobi, azw3 or, to be exact, any format calibre/ebook-convert supports

    (requires an additional installation of `Kavid Goyal's Calibre <https://calibre-ebook.com/>`_)

* The following output types are planned for an upcoming version:

  * JSON for use with https://github.com/vomaufgang/areader
