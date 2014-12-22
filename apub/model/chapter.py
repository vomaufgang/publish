class Chapter():
    def __init__(self):
        #: :type: str
        self.__id = ""
        #: :type: str
        self.__title = ""
        #: :type: str
        self.__path = ""

    @property
    def id(self):
        """:rtype : str"""
        return self.__id

    @id.setter
    def id(self, value):
        """:type value: str"""
        self.__id = value

    @property
    def path(self):
        """:rtype : str"""
        return self.__path

    @path.setter
    def path(self, value):
        """:type value: str"""
        self.__path = value