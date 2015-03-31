from abc import ABCMeta, abstractmethod


class Output(metaclass=ABCMeta):
    def __init__(self, output_name=None, output_path=None,
                 output_range='everything', output_file=None):
        if not output_name or output_name.isspace():
            raise AttributeError('name is empty. Every output must '
                                 'have a unique name.')
        self.output_path = output_path
        self.output_range = output_range
        self.output_file = output_file
        self.__output_name = output_name

    @abstractmethod
    def make(self, project):
        pass

    @property
    def output_name(self):
        return self.__output_name

    @output_name.setter
    def output_name(self, value):
        # todo must
        self.__output_name = value
