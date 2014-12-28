from ..output import Output

class Project():
    def __init__(self):
        self.__book = None
        self.__outputs = []
        pass

    @property
    def book(self):
        return self.__book

    @book.setter
    def book(self, value):
        self.__book = value

    @property
    def outputs(self):
        return self.__outputs

    @outputs.setter
    def outputs(self, value):
        self.outputs = value