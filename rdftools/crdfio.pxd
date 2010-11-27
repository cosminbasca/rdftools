__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from libc.stdio cimport *
from libc.stdlib cimport *

#-----------------------------------------------------------------------------------------------------------------------
# the rdf raptor parser ----> must be 1.X
#-----------------------------------------------------------------------------------------------------------------------
cdef extern from "raptor.h":
    ctypedef struct raptor_serializer:
        pass
    ctypedef struct raptor_uri:
        pass
    ctypedef enum raptor_identifier_type:
        pass
    ctypedef struct raptor_statement:
        void *subject
        raptor_identifier_type subject_type
        void *predicate
        raptor_identifier_type predicate_type
        void *object
        raptor_identifier_type object_type
        raptor_uri *object_literal_datatype
        unsigned char *object_literal_language
    ctypedef struct raptor_parser:
        pass

    ctypedef void (*raptor_statement_handler)(void *user_data, raptor_statement *statement)

    # library
    void raptor_init()
    void raptor_finish()

    # parser
    raptor_parser* raptor_new_parser(char *name)
    raptor_parser*      raptor_new_parser_for_content(raptor_uri *uri, char *mime_type, unsigned char *buffer, size_t len, unsigned char *identifier)
    void raptor_set_statement_handler(raptor_parser* parser, void *user_data, raptor_statement_handler handler)
    int raptor_parse_file(raptor_parser* rdf_parser, raptor_uri *uri, raptor_uri *base_uri)
    void raptor_free_parser(raptor_parser* parser)
    int raptor_parse_chunk(raptor_parser* rdf_parser, unsigned char* buffer, size_t len, int is_end)
    int raptor_start_parse(raptor_parser *rdf_parser, raptor_uri *uri)

    # serializer
    raptor_serializer* raptor_new_serializer(char *name)
    int raptor_serialize_start_to_file_handle(raptor_serializer *rdf_serializer, raptor_uri *uri, FILE *fh)
    int raptor_serialize_start_to_filename(raptor_serializer *rdf_serializer, char *filename)
    int raptor_serialize_start_to_string(raptor_serializer *rdf_serializer, raptor_uri *uri, void **string_p, size_t *length_p)
    int raptor_serialize_statement(raptor_serializer* rdf_serializer, raptor_statement *statement)
    int raptor_serialize_end(raptor_serializer *rdf_serializer)
    void raptor_free_serializer(raptor_serializer* rdf_serializer)

    # uri
    unsigned char *raptor_uri_filename_to_uri_string(char *filename)
    raptor_uri* raptor_new_uri(unsigned char *uri_string)
    void raptor_free_uri(raptor_uri *uri)
    raptor_uri* raptor_uri_copy(raptor_uri *uri)

    # memory
    void raptor_free_memory(void *ptr)



