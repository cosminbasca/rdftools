from libc.stddef cimport size_t
from libc.stdint cimport uint32_t, uint64_t
from libcpp.pair cimport pair

cdef extern from "city.h" nogil:
    ctypedef uint32_t uint32
    ctypedef uint64_t uint64
    ctypedef pair[unsigned long,unsigned long] uint128

    uint64 CityHash64(const char *buf, size_t len)
    uint64 CityHash64WithSeed(const char *buf, size_t len, uint64 seed)
    uint64 CityHash64WithSeeds(const char *buf, size_t len, uint64 seed0, uint64 seed1)
    uint128 CityHash128(const char *s, size_t len)
    uint128 CityHash128WithSeed(const char *s, size_t len, uint128 seed)
    uint32 CityHash32(const char *buf, size_t len)
    uint64 Hash128to64(uint128& x)


cpdef uint64 city64(bytes value)
cpdef uint64 city64seed(bytes value, uint64 seed)
cpdef uint64 city64seeds(bytes value, uint64 seed1, uint64 seed2)
cpdef tuple city128(bytes value)
cpdef tuple city128seed(bytes value, tuple seed)
cpdef uint64 city128to64(tuple digest)

cdef class City64:
    cdef public uint64 digest64

    cpdef update(self, bytes value)


cdef class City128:
    cdef public tuple digest128

    cpdef update(self, bytes value)