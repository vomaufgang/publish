====
TODO
====

.. todo:: Review CONTRIBUTING, esp. Get Started!, Testing, ff.

.. todo:: Incorporate this advice with regards to "type checking is
          unnessecary":
          http://stackoverflow.com/questions/9816878/how-do-ruby-programmers-do-type-checking

.. todo:: Move todos to issue tracker

.. todo:: https://github.com/sphinx-doc/sphinx/issues/3545 autodoc generates duplicate entries when subpackage 'redeclares' package contents via __all__.

.. todo::

    Use consistent markup for page titles and headings:

    ::

        ==========
        Page title
        ==========

        Heading 1
        =========

        Heading 2
        ---------

        Heading 3
        ~~~~~~~~~

    Not all pages follow this style yet.

.. todo:: Move to google style docstrings. Inform contributors about the docstring style.

IDEAS
=====

.. todo:: Connect apub to apub-server instances via
          apub-push [*|1-5|1,3,5]

          **rejected**: With my current workload a fully featured server is
            out of the question. areader will be implemented as a pure
            html/javascript solution.
            apub will create json files that can be used as input for areader.
            You will be able to drop the files anywhere on your webserver as
            long as you point areader to them.

Long Term Goals
===============

.. todo:: Create a standalone implementation of ebook-convert OR take
          ebook-convert, remove all gui references and dependencies on calibre
          and offer it as a pure python package with optional cli.

.. todo::

    Wouldn't it suffice to have setup.py- and manage.py-*like* capabilities
    instead of a full blown json project format?

    Define your project in a `project.py`, import apub.cli and your project.py
    gains command line parameters like `python project.py make my_output`

    Of course that would mean that I need to somehow provide the project
    metadata to the cli - maybe offer some global fields that have to be
    set in project.py?

    ::

        from apub.cli import apub
        apub(book=Book(), outputs=[Output(name='my_output')], ...)

    would allow for

    ::

        >>> python my_project.py make my_output


    Note that this would also mean that I don't need from_dict anymore, since
    the entire implementation and usage would be strictly bound to python
    files - and from_dict is really only needed für json project files.

    I think I'll go with yagni on this one - and remove from_dict.

    As for quick execution of apub - `python project.py` allows for the
    author to provide his own default action via `__main__`, which could be
    ignored if any parameters are given - or apub() takes additional
    parameters offering the possibility to define default actions.

    ::

        from apub.cli import apub
        apub(..., default_output='my_output')

