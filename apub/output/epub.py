from tempfile import mkstemp
import os

from .output import Output
from .html import HtmlOutput


justifications = ['original', 'left', 'justify', 'right']


class EpubOutput(Output):

    def __init__(self, project, out_path, ebookconvert_params=None):
        super().__init__(project, out_path)
        self.__change_justification = 'original'
        self.__out_path = out_path
        self.__ebookconvert_params = ebookconvert_params

    def make(self):
        temp_file = mkstemp(suffix=".html")
        HtmlOutput(project=self.__project, out_path=temp_file).make()
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




# todo if htmloutput.destination is none  -> use tempfile.mkdtemp
# todo force: if true, make will run each time called, if false make will run once per output