#!/usr/bin/env python3
# coding: utf8
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (C) 2015  Christopher Knörndel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from .chapter import Chapter
from ..output import Output
from ..substitution import Substitution


class Project():
    def __init__(self):
        super().__init__()
        self.metadata = {}
        self.chapters = []
        self.outputs = []
        self.substitutions = []

    @property
    def published_chapters(self):
        for chapter in self.chapters:
            if chapter.published:
                yield chapter

    @staticmethod
    def from_file(path):
        with open(path) as file:
            json = file.read()

        return Project.from_json(json)

    @staticmethod
    def from_json(json_):
        import json

        dict_ = json.loads(json_)

        return Project.from_dict(dict_)

    @staticmethod
    def from_dict(dict_):
        project = Project()

        project.metadata = dict_['metadata']

        chapters = []
        for chapter_dict in dict_['chapters']:
            chapters.append(Chapter.from_dict(chapter_dict))
        project.chapters = chapters

        outputs = []
        for output_dict in dict_['outputs']:
            outputs.append(Output.from_dict(output_dict))
        project.outputs = outputs

        substitutions = []
        for substitution_dict in dict_['substitutions']:
            substitutions.append(Substitution.from_dict(substitution_dict))
        project.substitutions = substitutions

        return project
