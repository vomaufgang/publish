from abc import ABCMeta, abstractmethod, abstractproperty
from enum import Enum


class Source(object):
    __metaclass__ = ABCMeta

    def __init__(self, source_format=None):
        self._source_format = source_format
        pass

    @property
    @abstractmethod
    def text(self):
        pass


class FileSource(Source):
    @property
    def text(self):
        pass

    def __init__(self):
        super().__init__()
        self.path = "."
        self.format = SourceFormat.apubdown

    def read(self):
        pass


class TextSource(Source):
    def __init__(self,text=None):
        pass





class SourceFormat(Enum):
    """ Defines input or intermediate formats whose contents
    can be read or transformed in memory. """
    apubdown = 1  # input format, will be assumed for file type .ad
    markdown = 2  # input format, will be assumed for file type .md