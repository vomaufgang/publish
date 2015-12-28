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
import json
import logging
import os

from apub.errors import MalformedProjectJsonError
from apub.project import Project

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler)


def read_project(path=None):
    """Welp

    Args:
        path (str): Optional

    Returns:
        Something.
    """
    log.debug('start read_project')
    log.debug('path = {0}'.format(path))
    project_file_path = None
    default_project_file_name = '.apub.json'

    if not path:
        log.debug('path is None, look for {0} in cwd {1}'.format(
            default_project_file_name,
            os.getcwd()))
        project_file_path = os.path.join(
            os.getcwd(),
            default_project_file_name)
    elif os.path.isdir(os.path.join(os.getcwd(), path)):
        log.debug('path is {0}, look for {1}'.format(
            os.path.join(os.getcwd(), path),
            default_project_file_name))
        project_file_path = os.path.join(
            path,
            default_project_file_name)
    elif os.path.isfile(os.path.join(os.getcwd(), path)):
        project_file_path = path
        log.debug('path is {0}, use it')

    log.debug('reading {0}'.format(project_file_path))
    with open(project_file_path) as project_file:
        data = project_file.read()
        log.debug('{0} read containing {1}'.format(project_file_path,
                                                   data))
    try:
        dict_ = json.loads(data)
    except ValueError as value_error:
        raise MalformedProjectJsonError(
            "The provided project json contained malformed data. "
            "Expected a valid json object, got{0}'{1}'{0}"
            "Inspect the enclosed ValueError for more information."
            .format(os.linesep, data)) from value_error

    # todo: validate the data before calling the factory chain

    log.debug('end read_project')
    return Project.from_dict(dict_)
