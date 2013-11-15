from time import time

__author__ = 'basca'

# ================================================================================================
#
# enum simulation
#
# ================================================================================================
def enum(**enums):
    """simulate enume pattern, from here: http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
    example
    >>> Numbers = enum(ONE=1, TWO=2, THREE='three')
    >>> Numbers.ONE
    1
    >>> Numbers.TWO
    2
    >>> Numbers.THREE
    'three
    """
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
            msg = '[TIMEIT] %s took %.2f ms'%(func.func_name, (t2-t1)*1000)
            if logger and hasattr(logger, 'info'):
                logger.info(msg)
            else:
                print msg
            return res
        return wrapper_func
    return wrapper