__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

cimport crdfio
cimport cython
from cpython cimport *
from libc.stdio cimport *
from libc.stdlib cimport *
import os
import sys
from raptorutil import *

# some constants
MB = 1024*1024  # 1 MegaByte
GB = 1024*MB    # 1 GigaByte

#-----------------------------------------------------------------------------------------------------------------------
# default (straight covertion)
#-----------------------------------------------------------------------------------------------------------------------
cdef inline void serialize_handler(void *user_data,crdfio.raptor_statement* statement):
    crdfio.raptor_serialize_statement(<crdfio.raptor_serializer*>user_data, statement)

cpdef convert(char* srcfname, char* dstformat, char* baseuri=NULL):
    srcformat = get_parser_type(srcfname)
    dstfname  = '%s.%s'%(os.path.splitext(srcfname)[0], get_rdfext(dstformat))
    print 'converting [%s] (%s) ====> [%s] (%s)'%(srcfname, srcformat, dstfname, dstformat)

    # init raptor
    crdfio.raptor_init()

    # the base uri.. usualy not needed
    cdef crdfio.raptor_uri* base_uri                = NULL
    cdef unsigned char* uri_string                  = crdfio.raptor_uri_filename_to_uri_string(srcfname)
    cdef crdfio.raptor_uri* uri                     = crdfio.raptor_new_uri(uri_string)
    if baseuri is NULL:
        base_uri = crdfio.raptor_new_uri(uri_string)

    # the parser & the serializer
    cdef crdfio.raptor_parser* rdf_parser           = crdfio.raptor_new_parser(srcformat)
    cdef crdfio.raptor_serializer* rdf_serializer   = crdfio.raptor_new_serializer(dstformat)
    crdfio.raptor_serialize_start_to_filename(rdf_serializer, dstfname)

    # setup the parser
    crdfio.raptor_set_statement_handler(rdf_parser, rdf_serializer,
                                        <crdfio.raptor_statement_handler>serialize_handler)
    print 'Start parsing...'
    crdfio.raptor_parse_file(rdf_parser, uri, base_uri)

    print 'Done converting'
    crdfio.raptor_free_parser(rdf_parser)
    crdfio.raptor_serialize_end(rdf_serializer)
    crdfio.raptor_free_serializer(rdf_serializer)

    crdfio.raptor_free_memory(uri_string)
    crdfio.raptor_free_uri(uri)
    if baseuri is not NULL:
        crdfio.raptor_free_uri(base_uri)

    crdfio.raptor_finish()


#-----------------------------------------------------------------------------------------------------------------------
# in chunks
#-----------------------------------------------------------------------------------------------------------------------
cdef char* copy_str_to_cstring(string):
    cdef char* copy = <char*>malloc(len(string)+1)
    copy[len(string)] = 0
    strcpy(copy, <char*>string)
    return copy

cdef class SerializerArg:
    cdef crdfio.raptor_serializer* rdf_serializer
    cdef int current
    cdef int chunk_size
    cdef char* srcfname
    cdef char* dstformat

    def __cinit__(self, chunk_size, srcfname, dstformat):
        self.current        = 0
        self.chunk_size     = chunk_size
        self.srcfname       = copy_str_to_cstring(srcfname)
        self.dstformat      = copy_str_to_cstring(dstformat)

        self.rdf_serializer = crdfio.raptor_new_serializer(self.dstformat)
        dstfname = chunk_filename(srcfname, dstformat, 0)
        crdfio.raptor_serialize_start_to_filename(self.rdf_serializer, <char*>dstfname)

    def __dealloc__(self):
        free(self.srcfname)
        free(self.dstformat)

    cdef serializer_end(self):
        if self.rdf_serializer is not NULL:
            crdfio.raptor_serialize_end(self.rdf_serializer)
            crdfio.raptor_free_serializer(self.rdf_serializer)

    cdef serialize_to_next_chunk(self):
        #print 'Serialize to chunk %d'%(self.chunk_no)
        crdfio.raptor_serialize_end(self.rdf_serializer)
        crdfio.raptor_free_serializer(self.rdf_serializer)

        self.rdf_serializer = crdfio.raptor_new_serializer(self.dstformat)
        dstfname = chunk_filename(<str>self.srcfname, <str>self.dstformat, self.chunk_no)
        crdfio.raptor_serialize_start_to_filename(self.rdf_serializer, <char*>dstfname)

    @property
    def chunk_no(self):
        return self.current / self.chunk_size

    def chunks(self):
        return [chunk_filename(<str>self.srcfname, <str>self.dstformat, i) for i in xrange(self.chunk_no+1)]

cdef inline void serialize_handler_chunk(void *user_data,crdfio.raptor_statement* statement):
    # default serialize handler used by the converter
    cdef SerializerArg ser_data = <SerializerArg>user_data
    crdfio.raptor_serialize_statement(ser_data.rdf_serializer, statement)
    ser_data.current += 1

    if ser_data.current != 0 and ser_data.current % ser_data.chunk_size == 0:
        ser_data.serialize_to_next_chunk()

cpdef convert_chunked(char* srcfname, char* dstformat, long io_buffer_size=160*MB, char* baseuri=NULL):
    srcformat = get_parser_type(srcfname)
    dstfname  = '%s.%s'%(os.path.splitext(srcfname)[0], get_rdfext(dstformat))
    print 'converting [%s] (%s) ====> [%s] (%s)'%(srcfname, srcformat, dstfname, dstformat)
    print 'buffer size = %d MB'%(io_buffer_size/MB)
    # init raptor
    crdfio.raptor_init()

    # the base uri.. usualy not needed
    cdef crdfio.raptor_uri* base_uri                = NULL
    cdef unsigned char* uri_string                  = crdfio.raptor_uri_filename_to_uri_string(srcfname)
    cdef crdfio.raptor_uri* uri                     = crdfio.raptor_new_uri(uri_string)
    if not baseuri:
        base_uri = crdfio.raptor_new_uri(uri_string)

    # the parser & the serializer
    cdef crdfio.raptor_parser* rdf_parser           = crdfio.raptor_new_parser(srcformat)
    cdef crdfio.raptor_serializer* rdf_serializer   = crdfio.raptor_new_serializer(dstformat)
    crdfio.raptor_serialize_start_to_filename(rdf_serializer, dstfname)

    # setup the parser
    crdfio.raptor_set_statement_handler(rdf_parser, rdf_serializer,
                                        <crdfio.raptor_statement_handler>serialize_handler)
    print 'Start parsing...'
    crdfio.raptor_start_parse(rdf_parser, base_uri)
    with open(srcfname,'r+b') as SRC:
        while True:
            chunk = SRC.read(io_buffer_size)
            if len(chunk) == 0: break
            while chunk[len(chunk)-1] != '\n':
                chunk += SRC.read(1)
            print '.',
            sys.stdout.flush()
            crdfio.raptor_parse_chunk(rdf_parser, <unsigned char*>chunk, len(chunk), 0)
    crdfio.raptor_parse_chunk(rdf_parser, NULL, 0, 1)
    print
    print 'Done converting'

    crdfio.raptor_free_parser(rdf_parser)
    crdfio.raptor_serialize_end(rdf_serializer)
    crdfio.raptor_free_serializer(rdf_serializer)

    crdfio.raptor_free_memory(uri_string)
    crdfio.raptor_free_uri(uri)
    if not baseuri:
        crdfio.raptor_free_uri(base_uri)

    crdfio.raptor_finish()