from ..output import Output


class Project():
    def __init__(self):
        # todo one project may contain multiple books
        # i.e.: aus-1, aus-2, aus-3 with different chapters and aus with all chapters in a single package
        self.__books = []
        self.__outputs = []
        self.__series_name = None
        pass

    @property
    def books(self):
        return self.__books

    @books.setter
    def books(self, value):
        self.__books = value

    @property
    def outputs(self):
        """Gets or sets the outputs.

        Each output is called once per book contained within the project.Unless an output has been directly assigned
        one or more books to process, in which case said output it will only process the book assigned to it.

        :type: list of Output"""
        return self.__outputs

    @outputs.setter
    def outputs(self, value):
        self.outputs = value