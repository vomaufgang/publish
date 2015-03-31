# apub - Python package to turn markdown files into ebooks
# Copyright (C) 2015  Christopher Knörndel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from apub.validation import id_pattern


class Project():
    def __init__(self):
        super().__init__()
        self.__id = None
        self.__substitutions = []
        self.__books = []
        self.__outputs = []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not id_pattern.match(value):
            raise ValueError('The provided id contains invalid characters, '
                             'may consist only of a-z, A-Z, 0-9, -, _')
        self.__id = value

    @property
    def books(self):
        """Gets the list of books managed in this project.

        You can add a book to a project like so::

            project = Project()
            book = Book()
            project.books.append(book)

        :type: list of :class:`apub.book.Book`"""
        return self.__books

    @property
    def outputs(self):
        """Gets the list of outputs.

        Each output is called once per book contained within the
        project unless an output has been directly assigned one or more
        books to process, in which case said output it will only process the
        book assigned to it.

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

    def chapters(self):
        chapters = []
        for book in self.books:
            chapters.append(book.chapters)
        return chapters
