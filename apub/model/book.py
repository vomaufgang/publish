class Book():
    def __init__(self):
        """

        """
        self.__subtitle = ""
        self.__title = ""
        self.__chapters = []
        self.__series = ""
        self.__no_in_series = 0


    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def subtitle(self):
        return self.__subtitle

    @subtitle.setter
    def subtitle(self, value):
        pass

    @property
    def chapters(self):
        """:rtype : list of Chapter"""
        return self.__chapters

    @chapters.setter
    def chapters(self, value):
        """:type value: list of Chapter"""
        self.__chapters = value