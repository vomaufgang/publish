from tempfile import mkstemp
import os

from .output import Output
from .html import HtmlOutput


justifications = ['original', 'left', 'justify', 'right']


class EpubOutput(Output):

    def __init__(self, output_path=None, ebookconvert_params=None,
                 css_path=None):
        super().__init__(output_path)
        self.__change_justification = 'original'
        self.__css_path = css_path
        self.__output_path = output_path
        self.__ebookconvert_params = ebookconvert_params

    def make(self, project):
        if self.output_path is None:
            raise AttributeError("output_path of EpubOutput must not be None")

        temp_file = mkstemp(suffix=".html")
        HtmlOutput(
            output_path=self.output_path,
            output_range="todo",
            css_path=self.__css_path
        ).make()
        # todo call ebook-convert
        os.remove(temp_file)
        pass
    
    @property
    def change_justification(self):
        """Gets or sets the justification for *all* text within a project.

        Please consult the official documentation over at `manual.calibre.com
        <http://manual.calibre-ebook.com/cli/ebook-convert.html#cmdoption-ebook-convert--change-justification>`_
        to learn about the effects of this parameter.

        :type: :class:`Justification`"""
        return self.__change_justification
    
    @change_justification.setter
    def change_justification(self, value):
        if value not in justifications:
            raise AttributeError('value must be either of the following: {0}'.format(justifications))
        self.__change_justification = value





# todo force: if true, make will run each time called, if false make will run once per output