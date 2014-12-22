from apub.output.output import Output

__author__ = 'Christopher'


class HtmlOutput(Output):

    def __init__(self, project, out_path):
        super().__init__(project, out_path)
        pass

    def make(self):
        # read all chapters into single string
        # run apubdown extensions (expand newlines)
        # hook markdown extensions
        # run markdown
        pass
