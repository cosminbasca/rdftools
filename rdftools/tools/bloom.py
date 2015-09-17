from warnings import warn

__author__ = 'cbasca'

try:
    from cybloom import ScalableBloomFilter
    add = lambda sbf, key: sbf.add(key)
    check = lambda sbf, key: sbf.check(key)

except ImportError:
    warn("Could not find cybloom, proceeding with pybloom")
    from pybloom import ScalableBloomFilter
    add = lambda sbf, key: not sbf.add(key)
    check = lambda sbf, key: key in sbf
