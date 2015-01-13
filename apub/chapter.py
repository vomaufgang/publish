from .apub import _id_pattern


class Chapter():
    def __init__(self):
        super().__init__()
        self.__substitutions = []
        self.__id = ""
        self.__title = ""
        self.__path = ""

    @property
    def id(self):
        """Gets or sets the id. May only contain the characters
        a-z, A-Z, 0-9, '-' and '_' and must be unique within the containing
        project.

        Setting this to an invalid id will raise an error.

        Using the same id for two separate chapters will raise an error at
        build time.

        *This property is mandatory.*

        :type: str
        :raises ValueError:
         if the value contains any characters not in this range: a-z, A-Z,
         0-9, '-' and '_'"""
        return self.__id

    @id.setter
    def id(self, value):
        """:type value: str"""
        if not _id_pattern.match(value):
            raise ValueError('value contains invalid characters, may consist '
                             'only of a-z, A-Z, 0-9, -, _')

        self.__id = value

    @property
    def title(self):
        """Gets or sets the title.

        You can specify the title in three distinct ways:

        1. As an ordinary markdown heading at the top of the chapter file.
        2. Via the title attribute of the chapter object in question.
        3. Not at all.

        todo: further describe and specify the options above, i.e. "for
        option 2 the heading must be the first line
              within the document" and "for option 3 a heading is
              automatically generated, using the number of the
              chapter as it appears in the book as the chapter title, i.e. "3"

        todo: add option to create own chapter title formats via string
        formatting:
        http://stackoverflow.com/questions/11022655/string-format-with-optional-placeholders
        """
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

    def read(self):
        if self.path is None:
            raise AttributeError('path must not be None')

        with open(self.path, 'r', encoding='utf-8') as f:
            result = f.readlines()

        return result

    @property
    def substitutions(self):
        return self.__substitutions
