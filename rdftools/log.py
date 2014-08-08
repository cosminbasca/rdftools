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