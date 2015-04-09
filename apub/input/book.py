import validators


class Book():
    def __init__(self,
                 id=None,
                 title=None,
                 subtitle=None,
                 slug=None,
                 language=None,
                 chapters=None,
                 substitutions=None,
                 cover_image_path=None):
        """Creates a new instance of the book class."""
        self.__id = None
        self.__title = None
        self.__series = None
        self.__number = None
        self.__slug = None
        self.__language = None
        self.__chapters = None
        self.__substitutions = None
        self.__cover_image = None

        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.slug = slug
        self.language = language
        self.chapters = chapters
        self.substitutions = substitutions
        self.cover_image = cover_image_path

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value and not validators.uuid(value):
            raise ValueError

        self.__id = value

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
        self.__title = value

    @property
    def subtitle(self):
        """Gets or sets the subtitle.

        Will be ignored if left unset, set to None or empty.

        :type: str"""
        return self.__series

    @subtitle.setter
    def subtitle(self, value):
        self.__series = value

    @property
    def chapters(self):
        """Gets or sets the list of chapters.

        Chapters will be automatically processed, numbered and put out and
        in the order they were added to the book.

        :type: list of Chapter"""
        return self.__chapters

    @chapters.setter
    def chapters(self, value):
        if value:
            self.__chapters = value
        else:
            self.__chapters = []
    
    @property
    def cover_image(self):
        return self.__cover_image

    @cover_image.setter
    def cover_image(self, value):
        self.__cover_image = value

    @property
    def language(self):
        """Gets or sets the language of this book.

        Using a valid ISO3166 or ISO3166-2 country or country subdivision
        code like 'EN', 'DE' or 'EN-US' is strongly
        recommended.

        Default: 'UND' as in undefined"""
        return self.__language

    @language.setter
    def language(self, value):
        self.__language = value

    @property
    def substitutions(self):
        return self.__substitutions

    @substitutions.setter
    def substitutions(self, value):
        pass

    @property
    def slug(self):
        return self.__slug

    @slug.setter
    def slug(self, value):
        self.__slug = value
