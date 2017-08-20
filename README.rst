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
------------

* develop: |DEVELOP| |DEVCOVERAGE|
* master: |MASTER|

.. |DEVELOP| image:: https://travis-ci.org/vomaufgang/apub.svg?branch=develop
   :target: https://travis-ci.org/vomaufgang/apub/branches

.. |MASTER| image:: https://travis-ci.org/vomaufgang/apub.svg?branch=master
   :target: https://travis-ci.org/vomaufgang/apub/branches

.. |DEVCOVERAGE| image:: https://coveralls.io/repos/github/vomaufgang/apub/badge.svg?branch=develop
   :target: https://coveralls.io/github/vomaufgang/apub?branch=develop


Features
--------

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

    from apub import Book, Chapter, HtmlOutput, setup

    setup(book=Book(title='My Book',
                    chapters=[Chapter(source='my_first_chapter.md'),
                              Chapter(source='my_second_chapter.md')]),
          outputs=[HtmlOutput(path='my_book.html',
                              name='my_output')])

  Given the above is saved in a file :code:`my_project.py` and the markdown
  files are present, the output :code:`my_book.html` can be created
  by simply executing

  .. code-block:: shell

    python my_project.py make

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

.. note:: Several parameters of the api use trailing underscores as per pep8
          recommendation for overlapping type and parameter names.

          These parameter names may display without trailing underscores in the
          html documentation. This is due to bug
          https://github.com/sphinx-doc/sphinx/issues/519
          in sphinx-doc falsely removing underscores from parameter names.

          Afflicted parameters are documented accordingly until this issue is
          resolved.
