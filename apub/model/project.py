class Project():
    def __init__(self):
        self.__books = []
        self.__outputs = []
        pass

    @property
    def books(self):
        """Gets or sets the books managed in this project.

        :type: list of Book"""
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
        self.__outputs = value