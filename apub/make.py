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

# Here be dragons.


from .output import Output


def make(project, output=None):
    """

    :type project: :class:`apub.metadata.Project`
    """
    if output is None:
        make_every_output(project)

    if isinstance(output, Output):
        output.make(project)
        return

    try:
        output = find_output(project, output)
        output.make(project)
    except OutputNotFoundError:
        raise


def make_every_output(project):
    for output in project.outputs:
        output.make(project)


def find_output(project, output_name):
    for output in project.outputs:
        if output.output_name == output_name:
            return output
    raise OutputNotFoundError("No output using the following name could "
                              "be found: '{0}'".format(output_name))


class OutputNotFoundError(Exception):
    pass


class ChapterRepository():
    def __init__(self, project):
        pass

    def get_all(self):
        pass

    def get_chapter_by_id(self, chapter_id):
        pass

    def get_chapter_by_number(self, chapter_number):
        pass

    def get_chapters_by_book(self, book):
        pass

    def get_chapters_by_book_id(self, book_id):
        pass


class BookRepository():
    def __init__(self):
        pass

    def get_all(self):
        pass

    def get_book_by_id(self):
        pass

    def get_book_by_chapter(self, chapter):
        pass

    def get_book_by_chapter_id(self, chapter_id):
        pass








