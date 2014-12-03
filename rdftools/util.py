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
from contextlib import contextmanager
from time import time
import sh

__author__ = 'basca'

# ----------------------------------------------------------------------------------------------------------------------
#
# utility functions
#
# ----------------------------------------------------------------------------------------------------------------------
def log_time(logger=None):
    def wrapper(func):
        def wrapper_func(*arg, **kwargs):
            t1 = time()
            res = func(*arg, **kwargs)
            t2 = time()
            msg = '[TIMEIT] %s took %.2f ms' % (func.func_name, (t2 - t1) * 1000)
            if logger and hasattr(logger, 'info'):
                logger.info(msg)
            else:
                print msg
            return res

        return wrapper_func

    return wrapper


@contextmanager
def working_directory(directory):
    _cwd = sh.pwd()
    sh.cd(directory)
    yield
    sh.cd(_cwd)


def interval_split(num_splits, size, threshold=10):
    step = threshold if size / num_splits < threshold else size / num_splits
    for i in xrange(0, size, step):
        yield i, step - 1 if (i + step - 1) < size else size - i

