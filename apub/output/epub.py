from tempfile import mkstemp
import os

from .output import Output
from .html import HtmlOutput

__author__ = 'Christopher'


class EpubOutput(Output):
    def __init__(self, project, out_path):
        super().__init__(project)
        pass

    def make(self):
        temp_file = mkstemp(suffix=".html")
        HtmlOutput(project=self.__project, out_path=temp_file).make()
        os.remove(temp_file)
        pass


# todo if htmloutput.destination is none  -> use tempfile.mkdtemp
# todo force: if true, make will run each time called, if false make will run once per output