from contextlib import contextmanager
from time import time
import sh

__author__ = 'basca'

# ================================================================================================
#
# enum simulation
#
# ================================================================================================
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)


# ================================================================================================
#
# utility functions
#
# ================================================================================================
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
def working_directory(dir):
    _cwd = sh.pwd()
    sh.cd(dir)
    yield
    sh.cd(_cwd)