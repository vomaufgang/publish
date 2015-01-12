from abc import ABCMeta, abstractmethod


class Substitution(metaclass=ABCMeta):
    pass

    @abstractmethod
    def apply(self, line):
        pass


class SimpleSubstitution(Substitution):
    def apply(self, line):
        pass


class RegexSubstitution(Substitution):
    def apply(self, line):
        pass