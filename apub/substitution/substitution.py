from abc import ABCMeta, abstractmethod
import os


class Substitution(metaclass=ABCMeta):
    pass

    @abstractmethod
    def apply_to(self, chapter):
        pass


class SimpleSubstitution(Substitution):
    def __init__(self):
        self.old = ""
        self.new = ""

    def apply_to(self, text):
        lines = text.splitlines

        for line in lines:
            line.replace()

        return os.linesep.join(lines)


class RegexSubstitution(Substitution):
    def apply_to(self, text):
        pass