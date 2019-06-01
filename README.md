# anited. publish - Overview

anited. publish is a python package with command line interface to turn markdown files
into ebooks.

Created to make publishing stories a lot easier for myself.

* **Free software**: [MIT](https://opensource.org/licenses/MIT>)
* **Official page**: https://anited.de/publish
* **Documentation**: https://docs.anited.de/publish

## Build status

* master: [![master pipeline status](https://gitlab.com/anited/publish/badges/master/build.svg)](https://gitlab.com/anited/publish/commits/master)
          [![master code coverage](https://gitlab.com/anited/publish/badges/master/coverage.svg)](https://gitlab.com/anited/publish/commits/master)

## Features

* Write your book entirely in markdown.

* Use whatever text editor you like, as long as it produces utf8 plain text files.

  (If you don't have a favourite text editor yet, go take a look at Graeme Gott's excellent
  FocusWriter. You will not regret it.)

* Describe your project and desired output using either a yaml project file or use publish directly
  from Python.

## Examples

Below is a short overview over the two project formats, Python and yaml. You can find complete,
runnable examples covering every single feature and setting in the `examples` folder.

All examples require an installation of anited. publish in your Python environment.

You can install the latest stable version by following the installation note at the bottom of
this readme (recommended) or the latest development version by cloning this repository, checking
out the desired branch and following the installation guide in `CONTRIBUTING.md`.

Examples `python_*` can be run by calling `python publish.py` inside the folder of the example
you want to run.

Examples `yaml_*` can be run by calling `publish` inside the folder of the example you want
to run.

### Yaml project format

Describe your project in a yaml file called `.publish.yaml` alongside your markdown files.

For example, your folder structure might look like this:

~~~
/
    .publish.yaml
    first_chapter.md
    second_chapter.md
    unfinished_chapter.md
    style.css
~~~

In this case the file `.publish.yaml` might look like this:

~~~yaml
title: My book
author: Max Mustermann
language: en

chapters:
  - src: first_chapter.md
  - src: second_chapter.md
  - src: unfinished_chapter.md
    publish: False

substitutions:
  - old: Cows
    new: Substitutions
  - pattern: \+\+(?P<text>.*?)\+\+
    replace_with: <span class="small-caps">\g<text></span>

stylesheet: style.css

outputs:
  - path: example.html
  - path: example.epub
~~~

Then, if anited. publish is installed in your global python interpreter, simply open a terminal
in the folder containing your project and use the

~~~shell
$ publish
~~~

command to process your book and create the desired output files.

### Using anited. publish as a Python package

Assuming the same folder structure as above, a simple project in pure Python might look like this:

~~~python
from publish.book import Book, Chapter
from publish.output import HtmlOutput, EbookConvertOutput
from publish.substitution import SimpleSubstitution, RegexSubstitution

book = Book(
  title='Example',
  authors='Max Mustermann',
  language='en')

book.chapters.extend(
  [Chapter(src='first_chapter.md'),
   Chapter(src='second_chapter.md'),
   Chapter(src='unfinished_chapter.md', publish=False)])

substitutions = [
    SimpleSubstitution(old='Cows',
                       new='Substitutions'),
    RegexSubstitution(pattern=r'\+\+(?P<text>.*?)\+\+',
                      replace_with=r'<span class="small-caps">\g<text></span>')]

html_output = HtmlOutput(
  path='example.html',
  stylesheet='style.css')
html_output.make(book, substitutions)

ebook_output = EbookConvertOutput(
  path='example.epub',
  stylesheet='style.css')
ebook_output.make(book, substitutions)
~~~

Given the above is saved in a file `my_project.py` and the markdown
files are present, the output files can be created
by calling

~~~shell
$ python my_project.py
~~~

on the command line.

**Note**: Unix/Linux users might have to call python3 instead, depending on their distribution.

### Supported output types

* The following output types are available:

  * HTML, as in 'good old hyper text markup language'
  * epub, mobi, azw3 or, to be exact, any format calibre/ebook-convert supports

    (requires an additional installation of [Kavid Goyal's Calibre](https://calibre-ebook.com/))

* The following output types are planned for an upcoming version:

  * HTML in JSON for use with https://gitlab.com/anited/read

## Documentation and examples

A more in depth guide to anited. publish including additional features like multiple
outputs, default outputs, text substitutions and more can be found in the 
[Wiki](https://gitlab.com/anited/publish/wikis).

If complete and working examples are more to your liking you can find several such example
projects in the **examples** directory of the repository.

## Installation

For the time being apub is only available via this git repository. You can use pip to install it
into your local or virtual Python environment:

~~~shell
pip install https://gitlab.com/anited/publish/-/archive/master/publish-master.zip
~~~

Releases via gitlab pipeline artifacts in the form of wheels are planned but I have no timeframe
on the availability yet.
