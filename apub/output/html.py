import markdown as md
import os
from apub.output.output import Output

__author__ = 'Christopher'

single_file = 'single_file'
file_per_book = 'file_per_book'
file_per_chapter = 'file_per_chapter'

modes = [single_file, file_per_book, file_per_chapter]


class HtmlOutput(Output):
    def __init__(self, output_path, output_range, css_path):
        super().__init__(output_path, output_range)
        self.__css_path = css_path
        self.mode = single_file
        pass

    @property
    def css_path(self):
        return self.__css_path

    @css_path.setter
    def css_path(self, value):
        self.__css_path = value

    def make(self, project=None):
        """
        If the output range is book:some_book, the book metadata
        overrides the project metadata for epub generation, i.e. title,
        subtitle, number of book in series etc.

        :param project:
        :type project: Project
        :return: The generated html content.
        """
        if project is None:
            raise AttributeError('project must not be None')

        # everything creates: 1 html with everything, 1 html per book AND 1
        # html per chapter

        if self.output_range.startswith('everything'):
            self.everything(project)
        elif self.output_range.startswith('books'):
            self.book(project)
        elif self.output_range.startswith('chapters'):
            self.chapters(project)

    def everything(self, project):
        if self.mode == single_file:
            self.everything_single_file(project)
        elif self.mode == file_per_book:
            self.file_per_book(project)

        elif self.mode == file_per_chapter:
            self.everything_per_chapter(project)

    def chapters(self, project, scope):
        raise NotImplementedError

    def file_per_book(self, project, books=None):
        if books is None:
            books = project.books

        for book in books:
            file = _File()
            file.prefix = self.get_book_file_prefix(book)
            file.file_name = book.id + ".html"
            file.file_path = self.output_path
            file.chapters = book.chapters
            file.global_substitutions = book.substitutions \
                + project.substitutions

            file.make()

    def everything_per_chapter(self, project):
        for book in project:
            for chapter in book.chapters:
                file = _File()
                file.prefix = self.get_chapter_file_prefix(book, chapter)
                file.file_name = chapter.slug
                file.file_path = self.output_path
                file.chapters = [chapter]
                file.global_substitutions = book.substitutions \
                    + project.substitutions

                file.make()

    @staticmethod
    def get_chapter_file_prefix(book, chapter):
        return "{0}-{1}_".format(book.number, chapter.number)

    @staticmethod
    def get_book_file_prefix(book):
        return "{0}_".format(book.number)

    def everything_single_file(self, project):
        pass

    def book(self, project):
        pass


class _File():
    def __init__(self):
        self.chapters = []
        self.global_substitutions = []
        self.file_name = ""
        self.prefix = ""
        self.file_type = ".html"
        self.file_path = ""
        self.css = ""

    def make(self):
        markdown = ""
        for c in self.chapters:
            markdown += c.read()

        for s in self.global_substitutions:
            markdown = s.apply_to(markdown)

        html = md.markdown(markdown)

        name = "{0}{1}{2}{3}".format(self.prefix,
                                     self.file_name,
                                     self.suffix,
                                     self.file_type)

        path = os.path.join(self.file_path, name)

        # todo is join path
        with open(
                path,
                mode='w',
                encoding='utf-8') as file:
            file.write(html)


class Scope():
    @staticmethod
    def parse_scope(self, scope_string):
        pass

