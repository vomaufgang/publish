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

        # todo This seems inefficient... Time it!

        self.__append_all_parent_substitutions_to_chapters(project)

        # the problem is complex, so my first solution will be complex

        self.__apply_substitutions(project)
        self.__transform_markdown_to_html(project)

        # everything creates: 1 html with everything, 1 html per book AND 1
        # html per chapter

        if self.output_range.startswith('everything'):
            self.everything(project)

        if self.output_range.startswith('books'):
            pass

        if self.output_range.startswith('chapters'):
            pass

        if self.output_path is not None:
            # todo write output
            pass



        # read all chapters into single string
        # run apubdown extensions (expand newlines)
        # run substitutions (according to levels - chapter > book > project)
        # hook markdown extensions
        # run markdown
        pass

# SIMPLIFY!
# if no filename is given, derive from project metadata
# everything - single file
# everything - per book
# everything - per chapter
# books - single file?
# books - per book
# books - per chapter
# a chapter
# a book



    def everything(self, project):
        if self.mode == single_file:
            pass
        elif self.mode == file_per_book:
            pass
        elif self.mode == file_per_chapter:
            # todo use this as a blueprint for the other scopes and modes
            for book in project:
                for chapter in book.chapters:
                    file = _File()
                    file.file_name = chapter.id if project.books.count == 1 \
                        else "[{0}]_{1}.html".format(book.id, chapter.id)
                    file.file_path = self.output_path
                    file.chapters = [chapter]
                    file.substitutions = chapter.substitutions \
                        + book.substitutions \
                        + project.substitutions  # still ugly

                    file.write()

    def projects(self, project, scope):
        raise NotImplementedError

    def chapters(self, project, scope):
        raise NotImplementedError


class _File():
    def __init__(self):
        self.chapters = []
        self.substitutions = []
        self.file_name = ""
        self.file_path = ""

    def write(self):
        markdown = ""
        for c in self.chapters:
            markdown += c.read()

        for s in self.substitutions:
            markdown = s.apply_to(markdown)

        html = md.markdown(markdown)

        # todo is join path
        with open(
                self.file_path + self.file_name,
                mode='w',
                encoding='utf-8') as file:
            file.write(html)