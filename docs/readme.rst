.. include:: ../README.rst


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

        python my_project.py make my_output


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

