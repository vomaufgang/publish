#!/usr/bin/python

import markdown
from enum import Enum
from apub.extensions.markdown.delimitscene import DelimitSceneExtension


class Project(object):
    def __init__(
            self,
            title=None,
            outputs=None,
            markdown_extensions=None,
            chapters=None):
        """

        :param title:
        :param outputs:
        :param markdown_extensions:
        :param chapters:
        :type chapters: list of Chapter
        """
        self.title = title
        if not outputs:
            self.outputs = []
        else:
            self.outputs = outputs

        if not markdown_extensions:
            self.markdown_extensions = []
        else:
            self.markdown_extensions = markdown_extensions

        if not chapters:
            self.chapters = []
        else:
            #: :type: list of Chapter
            self.chapters = chapters

        self.chapters[0].id = 1


class Chapter(object):
    def __init__(self):
        #: :type: int
        self.id = None
        self.sourceFile = SourceFile()
        self.formats = []
        self.formats = {Format.apubdown: "# I am a Heading"}
        # must be specified unless file type is .ad or .md
        self.sourceFormat = Format.apubdown


class Format(Enum):
    """ Defines input or intermediate formats whose contents
    can be read or transformed in memory. """
    apubdown = 1  # input format, will be assumed for file type .ad
    markdown = 2  # input format, will be assumed for file type .md
    html = 3  # intermediate format, can be outputted via HtmlOutput


class Source(object):
    def read(self):
        pass


class SourceFile(Source):
    def __init__(self):
        self.path = "."
        self.format = Format.apubdown

    def read(self):
        pass




class SourceText(Source):
    pass


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

class EpubOutput(_EbookOutput):
    def build(self, project=None):
        if not Format.html in project.chapters.formats:
            pass  # transform valid source format to html
        # persist to hard drive, call ebook-convert


class MobiOutput(_EbookOutput):
    pass

class JSONOutput(_Output):
    pass

class HtmlOutput(_Output):
    def build(self, project=None):
        pass

def transform(source_format=None, target_format=None):
    if source_format is Format.apubdown or source_format is Format.markdown:
        pass




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


def main():
    build()


if __name__ == "__main__":
    main()
