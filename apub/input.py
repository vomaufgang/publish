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

"""Package level docstring."""

from apub import metadata

import os
import logging

log = logging.getLogger(__name__)


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

    log.debug('end read_project')
    return metadata.Project.from_json(data)


def _build_project(project_data):
    raise NotImplementedError
