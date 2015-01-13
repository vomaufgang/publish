#!/usr/bin/python

import re


_id_pattern = re.compile('^[0-9a-zA-Z-_]+$')


def build(project=None):
    pass


def read_chapters(chapters=None):
    result = []
    if chapters is None:
        raise AttributeError('chapters must not be None')
    for chapter in chapters:
        result.append((chapter, read_chapter(chapter)))

    return result


def read_chapter(chapter=None):
    if chapter is None:
        raise AttributeError('chapter must not be None')
    if chapter.path is None:
        raise AttributeError('chapter.path must not be None')

    lines = []

    # todo read the actual chapter

    with open(chapter.path, mode='r', encoding='utf-8') as f:
        lines = f.readlines()

    return lines


def make(book):
    """

    :type book: Book
    """
    pass
