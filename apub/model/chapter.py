import re

id_pattern = re.compile('^[0-9a-zA-Z-_]+$')


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
        """Gets or sets the id. May only contain the characters
        a-z, A-Z, '-' and '_' and must be unique within the containing project.

        Setting this to an invalid id will raise an error.

        Using the same id for two separate chapters will raise an error at build time.

        :type: str
        :raises ValueError: if the value contains any characters not in this range: a-z, A-Z, '-' and '_'"""
        return self.__id

    @id.setter
    def id(self, value):
        """:type value: str"""
        if not id_pattern.match(value):
            raise ValueError('value contains invalid characters, may consist only of a-z, A-Z, -, _')

        self.__id = value

    @property
    def title(self):
        """Gets or sets the title."""
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def path(self):
        """Gets or sets the path.

        :type: str"""
        return self.__path

    @path.setter
    def path(self, value):
        """:type value: str"""
        self.__path = value