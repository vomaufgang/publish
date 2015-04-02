# -*- coding: utf-8 -*-

__author__ = 'Christopher Knörndel'
__email__ = 'cknoerndel@anited.de'
__version__ = '1.0.0-pre'

from .input import Project, Book, Chapter
from .substitution import Substitution, SimpleSubstitution, RegexSubstitution
from .output import Output, HtmlOutput, EpubOutput
from .make import make
from .errors import MalformedIdError, MalformedSlugError, OutputNotFoundError

__all__ = ['Project',
           'Book',
           'Chapter',
           'Substitution',
           'SimpleSubstitution',
           'RegexSubstitution',
           'Output',
           'HtmlOutput',
           'EpubOutput',
           'MalformedIdError',
           'MalformedSlugError',
           'OutputNotFoundError'
           'make']