#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import codecs

from ..apub import _id_pattern


metadata_template = """from apub import Project, Book, Chapter


project = Project()
b = Book()
b.title = '{book_title}'
b.subtitle = {book_subtitle}
b.authors = '{authors}'"""

focus_template = """from apub import Project, Book, Chapter

"""


def main():
    project_id = input('Enter project id (may contain a-zA-Z0-9-_), will be '
                       'used as part of the metadata file name: ')
    while project_id is None or not _id_pattern.match(project_id):
        project_id = input('Invalid project id, please enter project id (may '
                           'contain a-zA-Z0-9-_): ')

    book_title = input('Enter the book\'s title: ')
    while book_title is None or book_title.isspace():
        book_title = input('Every book must have a title, please enter the '
                           'book\'s title: ')

    book_subtitle = input('Enter the book\' subtitle (optional, leave empty '
                          'to skip): ')
    if book_subtitle is None or book_subtitle.isspace():
        book_subtitle = 'None'
    else:
        book_subtitle = "'{book_subtitle}'".format(book_subtitle=book_subtitle)

    authors = input('Enter the author\'s name '
                    '(separate multiple authors by comma): ')
    first_chapter_name = input('Enter the name of the first chapter: ')
    first_chapter_id = input('Enter the id of the first chapter '
                             '(may contain a-zA-Z0-9-_): ')

    # todo check for existing files or projects of the same id before continuing

    metadata_filename = '{project_id}_metadata.py'.format(project_id=project_id)
    if os.path.exists(os.path.join(os.getcwd(), metadata_filename)):
        raise FileExistsError
        # todo error message, project seems to already exist

    with codecs.open(metadata_filename, 'w', 'utf-8') as metadata:
        metadata_file_contents = metadata_template.format(book_title=book_title,
                                                          book_subtitle=book_subtitle,
                                                          authors=authors)
        metadata.write(metadata_file_contents)
    with codecs.open('{project_id}_focus.py'.format(project_id=project_id),
                     'w',
                     'utf-8') as focus:
        focus.write('I need better glasses.')
    with codecs.open('{project_id}_make.py'.format(project_id=project_id),
                     'w',
                     'utf-8') as focus:
        focus.write('I need better glasses.')

    return


if __name__ == '__main__':
    main()