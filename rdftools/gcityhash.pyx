from cython cimport *
from cpython cimport *
from libc.stdio cimport *
from libc.stdlib cimport *
from libc.string cimport *
from libc.stdint cimport uint32_t, uint64_t
from libcpp.pair cimport pair

cpdef inline uint64 city64(bytes value):
    return CityHash64(value, len(value))

cpdef inline uint64 city64seed(bytes value, uint64 seed):
    return CityHash64WithSeed(value, len(value), seed)

cpdef inline uint64 city64seeds(bytes value, uint64 seed1, uint64 seed2):
    return CityHash64WithSeeds(value, len(value), seed1, seed2)

cpdef inline tuple city128(bytes value):
    return CityHash128(value, len(value))

cpdef inline tuple city128seed(bytes value, tuple seed):
    return CityHash128WithSeed(value, len(value), seed)

cpdef inline uint64 city128to64(tuple digest):
    return Hash128to64(digest)


cdef class City64:
    def __cinit__(self, bytes value = None):
        self.digest64 = city64(value) if value else 0

    cpdef update(self, bytes value):
        if self.digest64:
            self.digest64 = city64seed(value, self.digest64)
        else:
            self.digest64 = city64(value)

    property digest:
        def __get__(self):
            return self.digest64


cdef class City128:
    def __cinit__(self, bytes value = None):
        self.digest128 = city128(value) if value else None

    cpdef update(self, bytes value):
        if self.digest128:
            self.digest128 = city128seed(value, self.digest128)
        else:
            self.digest128 = city128(value)

    property digest:
        def __get__(self):
            return self.digest128
