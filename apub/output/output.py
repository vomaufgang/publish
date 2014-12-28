from abc import ABCMeta, abstractmethod


class Output(metaclass=ABCMeta):
    def __init__(self, project, out_path):
        self.__project = project
        self.__out_path = out_path

    @abstractmethod
    def make(self):
        pass

    @property
    def project(self):
        return self.__project

    @property
    def out_path(self):
        return self.__out_path


