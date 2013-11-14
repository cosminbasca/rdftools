from cython cimport *
from cpython cimport *
from libc.stdio cimport *
from libc.stdlib cimport *
from raptor cimport *

import os
import sys
from raptorutil import *


__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

#-----------------------------------------------------------------------------------------------------------------------
#
# default (straight covertion)
#
#-----------------------------------------------------------------------------------------------------------------------
cdef inline void serialize_handler(void *user_data, raptor_statement* statement):
    raptor_serializer_serialize_statement(<raptor_serializer*>user_data, statement)

cpdef convert(char* source_file, char* dest_format, char* base_uri=NULL):
    source_format = get_parser_type(source_file)
    dest_file  = '%s.%s'%(os.path.splitext(source_file)[0], get_rdfext(dest_format))
    print 'converting [%s] (%s) ====> [%s] (%s)'%(source_file, source_format, dest_file, dest_format)

    # LOCAL VARS
    cdef raptor_world *world                = NULL
    cdef raptor_parser* rdf_parser          = NULL
    cdef raptor_serializer* rdf_serializer  = NULL
    cdef unsigned char *uri_string          = raptor_uri_filename_to_uri_string(source_file)
    cdef raptor_uri *uri                    = NULL
    cdef raptor_uri *r_base_uri               = NULL

    # INIT
    world = raptor_new_world()
    if base_uri is NULL:
        r_base_uri = raptor_new_uri(world, uri_string)
    uri = raptor_new_uri(world, uri_string)

    # SERIALIZER
    rdf_serializer = raptor_new_serializer(world, dest_format)
    raptor_serializer_start_to_filename(rdf_serializer, dest_file)

    # PARSER
    rdf_parser = raptor_new_parser(world, source_format)
    raptor_parser_set_statement_handler(rdf_parser, rdf_serializer, <raptor_statement_handler>serialize_handler)

    # START
    print 'Start parsing...'
    raptor_parser_parse_file(rdf_parser, uri, r_base_uri)

    print 'Done converting'
    raptor_free_parser(rdf_parser)
    raptor_serializer_serialize_end(rdf_serializer)
    raptor_free_serializer(rdf_serializer)

    raptor_free_memory(uri_string)
    raptor_free_uri(uri)
    if r_base_uri is not NULL:
        raptor_free_uri(r_base_uri)

    raptor_free_world(world)


#-----------------------------------------------------------------------------------------------------------------------
#
# chunked conversion
#
#-----------------------------------------------------------------------------------------------------------------------
cpdef convert_chunked(char* source_file, char* dest_format, long io_buffer_size=160*MB, char* base_uri=NULL):
    source_format = get_parser_type(source_file)
    dest_file  = '%s.%s'%(os.path.splitext(source_file)[0], get_rdfext(dest_format))
    print 'converting [%s] (%s) ====> [%s] (%s)'%(source_file, source_format, dest_file, dest_format)
    print 'buffer size = %d MB'%(io_buffer_size/MB)

    # LOCAL VARS
    cdef raptor_world *world                = NULL
    cdef raptor_parser* rdf_parser          = NULL
    cdef raptor_serializer* rdf_serializer  = NULL
    cdef unsigned char *uri_string          = raptor_uri_filename_to_uri_string(source_file)
    cdef raptor_uri *uri                    = NULL
    cdef raptor_uri *r_base_uri               = NULL

    # INIT
    world = raptor_new_world()
    if base_uri is NULL:
        r_base_uri = raptor_new_uri(world, uri_string)
    uri = raptor_new_uri(world, uri_string)

    # SERIALIZER
    rdf_serializer = raptor_new_serializer(world, dest_format)
    raptor_serializer_start_to_filename(rdf_serializer, dest_file)

    # PARSER
    rdf_parser = raptor_new_parser(world, source_format)
    raptor_parser_set_statement_handler(rdf_parser, rdf_serializer, <raptor_statement_handler>serialize_handler)

    # START
    print 'Start parsing...'
    raptor_parser_parse_start(rdf_parser, r_base_uri)
    with open(source_file,'r+b') as SRC:
        while True:
            chunk = SRC.read(io_buffer_size)
            if len(chunk) == 0: break
            while chunk[len(chunk)-1] != '\n':
                chunk += SRC.read(1)
            print '.',
            sys.stdout.flush()
            raptor_parser_parse_chunk(rdf_parser, <unsigned char*>chunk, len(chunk), 0)
    raptor_parser_parse_chunk(rdf_parser, NULL, 0, 1)

    print 'Done converting'
    raptor_free_parser(rdf_parser)
    raptor_serializer_serialize_end(rdf_serializer)
    raptor_free_serializer(rdf_serializer)

    raptor_free_memory(uri_string)
    raptor_free_uri(uri)
    if base_uri is not NULL:
        raptor_free_uri(r_base_uri)

    raptor_free_world(world)


#-----------------------------------------------------------------------------------------------------------------------
#
# raptor term to string
#
#-----------------------------------------------------------------------------------------------------------------------
cdef inline bytes raptor_term_to_bytes(raptor_term* term):
    if term == NULL:
        return None
    cdef bytes _rep = None
    if term.type == RAPTOR_TERM_TYPE_URI:
        _rep = raptor_uri_as_string(term.value.uri)
    elif term.type == RAPTOR_TERM_TYPE_LITERAL:
        _rep = PyBytes_FromStringAndSize(<char*>term.value.blank.string, term.value.blank.string_len)
    elif term.type == RAPTOR_TERM_TYPE_BLANK:
        _rep = PyBytes_FromStringAndSize(<char*>term.value.literal.string, term.value.literal.string_len)
    else:
        _rep = <bytes>''
    return _rep

#-----------------------------------------------------------------------------------------------------------------------
#
# the raptor parse handler
#
#-----------------------------------------------------------------------------------------------------------------------
cdef inline void parse_handler(void *user_data, raptor_statement* statement):
    cdef RDFParser parser = <RDFParser>user_data
    parser.results.append( (raptor_term_to_bytes(statement.subject) ,
                            raptor_term_to_bytes(statement.predicate),
                            raptor_term_to_bytes(statement.object),
                            raptor_term_to_bytes(statement.graph)) )

#-----------------------------------------------------------------------------------------------------------------------
#
# the actual Parser (wrapper)
#
#-----------------------------------------------------------------------------------------------------------------------
cdef class RDFParser:
    cdef raptor_parser* rap_parser
    cdef unsigned char* uri_string
    cdef raptor_uri* base_uri
    cdef public list results

    def __cinit__(self, src, base_uri = None, format = None):
        cdef raptor_world* world = raptor_new_world()
        self.uri_string = raptor_uri_filename_to_uri_string(src)
        if not base_uri:
            self.base_uri = raptor_new_uri_from_counted_string(world, self.uri_string, len(self.uri_string))

        source_format = get_parser_type(src) if not format else format
        self.rap_parser = raptor_new_parser(world, source_format)
        self.results  = []
        raptor_parser_set_statement_handler(self.rap_parser, <void*>self, <raptor_statement_handler>parse_handler)
        raptor_parser_parse_start(self.rap_parser, self.base_uri)

    def __dealloc__(self):
        if self.uri_string != NULL: raptor_free_memory(self.uri_string)
        if self.base_uri != NULL: raptor_free_uri(self.base_uri)
        if self.rap_parser != NULL:
            raptor_parser_parse_chunk(self.rap_parser, NULL, 0, 1)
            raptor_free_parser(self.rap_parser)

    cpdef clear_buffer(self):
        del self.results[:]

    cpdef list parse(self, bytes data):
        del self.results[:] # clear the results
        raptor_parser_parse_chunk(self.rap_parser, <unsigned char*>data, len(data), 0)
        return self.results

#-----------------------------------------------------------------------------------------------------------------------
#
# chunk generator over file
#
#-----------------------------------------------------------------------------------------------------------------------
def read_chunk(file, buffer_size):
    while True:
        chunk = file.read(buffer_size)
        if len(chunk) == 0:
            break
        # read til EOL
        while len(chunk) > 0 and chunk[len(chunk)-1] != '\n':
            chunk += file.read(1)
        yield chunk

#-----------------------------------------------------------------------------------------------------------------------
#
# get all source files in a directory, given an extension
#
#-----------------------------------------------------------------------------------------------------------------------
def get_source_files(location, ext='nt'):
    sources = None
    if os.path.exists(location):
        if os.path.isdir(location):
            sources = [os.path.join(location, f) for f in os.listdir(location) if os.path.splitext(f)[1][1:].upper() == ext.upper()]
        else:
            sources = [location]
    else:
        dir = os.path.split(location)[0]
        sources = [os.path.join(location, f) for f in os.listdir(dir) if os.path.splitext(f)[1][1:].upper() == ext.upper()]
    sources.sort()
    return sources

#-----------------------------------------------------------------------------------------------------------------------
#
# get an rdf stream of statements
#
#-----------------------------------------------------------------------------------------------------------------------
def rdf_stream(src, format=None, buffer_size=524288):
    parser = RDFParser(src, None, format)
    with open(src, 'r+') as SRC:
        for chunk in read_chunk(SRC, buffer_size):
            for stmt in  parser.parse(chunk):
                yield stmt

