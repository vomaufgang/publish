class Project():
    def __init__(self):
        self.__simple_substitutions = []
        self.__regex_substitutions = []
        self.__books = []
        self.__outputs = []

    @property
    def books(self):
        """Gets the list of books managed in this project.

        You can add a book to a project like so::

            project = Project()
            book = Book()
            project.books.append(book)

        :type: list of Book"""
        return self.__books

    @property
    def outputs(self):
        """Gets the list of outputs.

        Each output is called once per book contained within the project.Unless an output has been directly assigned
        one or more books to process, in which case said output it will only process the book assigned to it.

        You can add an output to a project like so::

            project = Project()
            html_output = HtmlOutput()
            project.outputs.append(html_output)

        :type: list of Output"""
        return self.__outputs

    # todo move substitutions to book scope to cope for different languages per book

    @property
    def simple_substitutions(self):
        """Gets the list of simple substitutions.

        Each substitution is applied per line of text in the order they were added to the list. Thus substitutions cannot span multiple lines at once.

        You can add a simple substitution to a project like so::

            project.simple_substitutions.append('text', 'replacement')

        This substitution will be applied like so:

        original:

        > Line of text.

        after substitution:

        > Line of replacement.

        Note that the following substitution will *not* work due to the scope of one line of text mentioned above::

            import os
            project.simple_substitutions.append('first line' + os.linesep + 'following line', 'replacement')

        You can however substitute a single line of text with multiple new lines of text - or insert line breaks as
        follows::

            import os
            project.simple_substitutions.append('I will be replaced by a line break', os.linesep)

        :type: list of Output"""
        return self.__simple_substitutions

    @property
    def regex_substitutions(self):
        """Gets the list of regular expression substitutions.

        Each substitution is applied per line of text in the order they were added to the list.

        The rules concerning substitution scope detailed in the documentation of simple_substitutions apply here, too.

        You can add a regular expression substitution to a project like so::

            # Replace every capital letter with Navi's lovely catchphrase.
            project.regex_substitutions.append('[A-Z]', 'Hey, Link, listen!')

        This substitution will be applied like so::

            original: Line of text.
            after substitution: Line of replacement.

        :type: list of Output"""
        return self.__regex_substitutions