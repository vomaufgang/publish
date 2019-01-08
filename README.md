# anited. publish - Overview

anited. publish is a python package with command line interface to turn markdown files
into ebooks.

Created to make publishing stories a lot easier for myself.

* **Free software**: [MIT](https://opensource.org/licenses/MIT>)
* **Official page**: https://anited.de/publish
* **Documentation**: https://docs.anited.de/publish

## Build status

* master: [![master pipeline status](https://gitlab.com/anited/publish/badges/master/build.svg)](https://gitlab.com/anited/publish/commits/master)
          [![master code coverage](https://gitlab.com/anited/publish/badges/master/coverage.svg?job=cover)](https://gitlab.com/anited/publish/commits/master)

## Features

* Write your book entirely in markdown.

* Use whatever text editor you like, as long as it produces utf8 plain text files.

  (If you don't have a favourite text editor yet, go take a look at Graeme Gott's excellent
  FocusWriter. You will not regret it.)

* Describe your project and desired output in a simple python file.

  A simple project might look like this:

  ~~~python
  from publish.book import Book, Chapter
  from publish.output import HtmlOutput, EbookConvertOutput
  from publish.substitution import SimpleSubstitution
  
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
  ~~~

  Given the above is saved in a file `my_project.py` and the markdown
  files are present, the output `my_book.html` can be created
  by executing

  ~~~shell
  python my_project.py
  ~~~

  on the command line.

  **Note**: Unix/Linux users might have to call python3 instead, depending on their distribution.

  A more in depth guide to anited. publish including additional features like multiple
  outputs, default outputs, text substitutions and more can be found at at
  https://docs.anited.de/publish.

  If complete and working examples are more to your liking you can find such an
  example project in the **examples** directory of the repository.

* The following output types are available:

  * HTML, as in 'good old hyper text markup language'
  * epub, mobi, azw3 or, to be exact, any format calibre/ebook-convert supports

    (requires an additional installation of [Kavid Goyal's Calibre](https://calibre-ebook.com/))

* The following output types are planned for an upcoming version:

  * HTML in JSON for use with https://gitlab.com/anited/read

## Installation

For the time being apub is only available via this git repository. You can use pip to install it
into your local or virtual Python environment:

~~~shell
pip install https://gitlab.com/anited/publish/-/archive/master/publish-master.zip
~~~
