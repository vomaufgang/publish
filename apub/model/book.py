class Book():
    def __init__(self):
        """Creates a new instance of the book class."""
        self.__title = None
        self.__subtitle = None
        self.__chapters = []
        self.__series_name = None
        self.__no_in_series = None

    @property
    def title(self):
        """Gets or sets the title.

        *This property is mandatory.*

        :type: str
        :raises ValueError: if set to None, whitespace or empty"""
        return self.__title

    @title.setter
    def title(self, value):
        """:type value: str"""
        if value is None or value.isspace() or value == "":
            raise ValueError('title must not be None or empty')
        self.__title = value

    @property
    def subtitle(self):
        """Gets or sets the subtitle.

        Will be ignored if left unset, set to None or empty.

        :type: str"""
        return self.__subtitle

    @subtitle.setter
    def subtitle(self, value):
        return self.__subtitle

    @property
    def chapters(self):
        """Gets or sets the list of chapters.

        Chapters will be automatically processed, numbered and put out and in the order they were added to the book.

        :type: list of Chapter"""
        return self.__chapters

    @chapters.setter
    def chapters(self, value):
        self.__chapters = value

    @property
    def series_name(self):
        """Gets or sets the series name.

        Will be ignored if left unset, set to None or empty.

        :type: str"""
        return self.__series_name

    @series_name.setter
    def series_name(self, value):
        self.__series_name = value

    @property
    def no_in_series(self):
        """Gets or sets the number of this book within the series specified in series_name.

        Will be ignored during processing if series_name is left unset or set to None or empty.

        :type: int"""
        return self.__no_in_series

    @no_in_series.setter
    def no_in_series(self, value):
        self.__no_in_series = value