#!/usr/bin/python

import markdown, re
from apub.extensions.markdown.delimitscene import DelimitSceneExtension
from . import Book, Chapter


id_pattern = re.compile('^[0-9a-zA-Z-_]+$')


p = Book()

class _Output(object):
    def __init__(self, project=None, chapters_to_build=None):
        self.project = project
        if not chapters_to_build:
            self.chapters_to_build = ["*"]
        else:
            self.chapters_to_build = chapters_to_build

    def build(self):
        if not self.project:
            return
        else:
            pass


class _EbookOutput(_Output):
    def build(self, project=None):
        pass

#class EpubOutput(_EbookOutput):
#    def build(self, project=None):
#        if not SourceFormat.html in project.chapters.formats:
#            pass  # transform valid source format to html
        # persist to hard drive, call ebook-convert


class MobiOutput(_EbookOutput):
    pass

class JSONOutput(_Output):
    pass

class HtmlOutput(_Output):
    def build(self, project=None):
        pass

#def transform(source_format=None, target_format=None):
#    if source_format is SourceFormat.apubdown or source_format is SourceFormat.markdown:
#        pass




class Output(object):
    def __init__(
            self,
            file_name=None,
            options=None):
        self.file_name = file_name
        self.options = options


def build(project=None):
    pass
# todo: test.chapter or text
#    with open('test.chapter', 'r') as f:
#        contents = f.read()
# todo: add a switch to expand single /n to /n/n
#       in case the input file is focuswriter-made and not
#       pure markdown
#    contents = contents.replace('\n', '\n\n')

#     html = markdown.markdown("""# Heading
# some text
#
# some more text
#
# ++ chapter break
#
# text
#
# the end
# """, extensions=[DelimitSceneExtension()])
#     print(html)
#     pass
    # my code here

def make(book):
    """

    :type book: Book
    """
    pass