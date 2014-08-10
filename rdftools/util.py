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
    step = size / num_splits
    if step < threshold:
        for i in xrange(0, size, step):
            yield i, step
    else:
        for i in xrange(0, size, step):
            yield i, step if (i + step) < size else size - (i + step)


if __name__ == '__main__':
    print list(interval_split(4, 40))
    print list(interval_split(4, 11))
    print list(interval_split(4, 12))
