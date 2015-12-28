====
apub
====

.. .. image:: https://badge.fury.io/py/apub.png
    :target: http://badge.fury.io/py/apub
    
.. image:: https://travis-ci.org/vomaufgang/apub.svg?branch=develop
        :target: https://travis-ci.org/vomaufgang/apub

.. .. image:: https://pypip.in/d/apub/badge.png
        :target: https://pypi.python.org/pypi/apub


Python package with command line interface to turn markdown files into ebooks.

Created to make publishing stories a lot easier for myself.

* **Free software**: `GPLv3 <http://www.gnu.org/licenses/gpl-3.0>`_
* **Official page**: http://anited.de/apub
* **Documentation**: http://apub.readthedocs.org.

Features
--------

* Write your book entirely in markdown.

* Use whatever text editor you like, as long as it produces utf8 plain text files.

  (If you don't have a favourite text editor yet, go take a look at Graeme Gott's excellent FocusWriter.
  You will not regret it.)

* Describe your project and desired output in a simple json format.

  Place the file as :code:`.apub.json` inside a folder and the command line interface
  will automatically identify the folder as a apub project.

  A simple project might look like this:

.. todo:: Update example json to new json format

.. code-block:: javascript

    {
      "metadata": {
        "title": "My Book",
        "authors": "Mr. and Ms. AwesomeSauce",
        "language": "en",
      },
      "chapters": [
        {
          "title": "Beginnings",
          "url_friendly_title": "beginnings",
          "source": "chapters/01-beginnings.chapter",
          "publish": true
        }
      ],
      "output": [
        {
          "name": "html",
          "type": "html",
          "path": "output/my_book.htm"
        },
        {
          "name": "epub",
          "type": "ebook-convert",
          "path": "output/my_book.epub",
          "ebookconvert_params": {
            "cover": "resources/cover.jpg"
          }
        }
      ],
      "substitutions": [
        {
          "type": "simple",
          "find": "Douglas Adams",
          "replace_with": "Terry Pratchett"
        }
      ]
    }

* Make your desired outputs by calling apub's command line interface.

  Continuing the example above:

  :code:`apub make` builds all outputs described in the .apub.json of the current working directory.

  :code:`apub make --output-name=html` builds the output with :code:`"name": "html"`.

  :code:`apub make --output-type=ebook-convert` builds all outputs of :code:`"type": "ebook-convert`.

* Don't want to create the .apub.json yourself?

  Call :code:`apub quickstart` within an empty folder or a folder that didn't contain an apub project previously
  and apub will create the project for you - including some useful default outputs.

* The following output types are available:

  * HTML, as in 'good old hyper text markup language'
  * JSON for use with the apub-WebReader
  * epub, mobi, azw3 or, to be exact, any format calibre/ebook-convert supports

    (requires an additional installation of `Kavid Goyal's Calibre <http://calibre-ebook.com/>`_)