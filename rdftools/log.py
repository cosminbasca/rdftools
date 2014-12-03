#
# author: Cosmin Basca
#
# Copyright 2010 University of Zurich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from inspect import isclass
import logging
from logging.config import fileConfig
import os
import sys

__all__ = ['get_logger', 'set_level', 'logger']

__author__ = 'basca'

__levels__ = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.ini'))


def get_logger(group=None, owner=None):
    name = None
    if isinstance(owner, basestring):
        name = '{0}.{1}'.format(group, owner) if isinstance(group, basestring) else owner
    elif owner:
        group = owner.__module__
        if group == '__main__':
            group = os.path.splitext(os.path.basename(sys.modules[group].__file__))[0]
        name = '{0}.{1}'.format(group, owner.__name__ if isclass(owner) else owner.__class__.__name__)
    return logging.getLogger(name)


def set_level(level, name=None, default=logging.WARNING):
    if isinstance(level, basestring):
        level = __levels__.get(level, default)
    current_logger = logging.getLogger(name) if name else logging.root
    current_logger.setLevel(level)


logger = get_logger(sys.modules[__name__])