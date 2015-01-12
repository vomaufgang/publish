from .substitutions import Substitution


class Project():
    def __init__(self):
        super().__init__()
        self.__substitutions = []
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

    @property
    def substitutions(self):
        """
        :type: list of :class:`apub.model.substitutions.Substitution`"""
        return self.__substitutions