from libc.stdio cimport *
from libc.stdlib cimport *

__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

#-----------------------------------------------------------------------------------------------------------------------
# the rdf raptor parser ----> must be 1.X
#-----------------------------------------------------------------------------------------------------------------------
cdef extern from "raptor.h":
    ctypedef struct raptor_world:
        pass

    ctypedef struct raptor_parser:
        pass

    ctypedef struct raptor_serializer:
        pass

    ctypedef struct raptor_uri:
        pass

    ctypedef enum raptor_term_type:
        pass

    ctypedef struct raptor_term_literal_value:
        unsigned char *string
        unsigned int string_len
        raptor_uri *datatype
        unsigned char *language
        unsigned char language_len

    ctypedef struct raptor_term_blank_value:
        unsigned char *string
        unsigned int string_len

    ctypedef union raptor_term_value:
        raptor_uri *uri
        raptor_term_literal_value literal
        raptor_term_blank_value blank

    ctypedef struct raptor_term:
        raptor_world* world
        int usage
        raptor_term_type type
        raptor_term_value value

    ctypedef struct raptor_statement:
        raptor_world* world
        int usage
        raptor_term* subject
        raptor_term* predicate
        raptor_term* object
        raptor_term* graph

    ctypedef void (*raptor_statement_handler)(void *user_data, raptor_statement *statement)

    #--------------------------------------------------------------------------------------------------------
    # library
    #--------------------------------------------------------------------------------------------------------
    raptor_world* raptor_new_world()
    int raptor_world_open(raptor_world *world)
    void raptor_free_world(raptor_world *world)

    #--------------------------------------------------------------------------------------------------------
    # parser
    #--------------------------------------------------------------------------------------------------------
    raptor_parser* raptor_new_parser(raptor_world *world, char *name)
    raptor_parser* raptor_new_parser_for_content(raptor_world *world, raptor_uri *uri, char *mime_type, unsigned char *buffer, size_t len, unsigned char *identifier)
    void raptor_free_parser(raptor_parser *parser)
    void raptor_parser_set_statement_handler(raptor_parser *parser, void *user_data, raptor_statement_handler handler)
    int raptor_parser_parse_chunk(raptor_parser *rdf_parser, unsigned char *buffer, size_t len, int is_end)
    int raptor_parser_parse_file(raptor_parser *rdf_parser, raptor_uri *uri, raptor_uri *base_uri)
    int raptor_parser_parse_start(raptor_parser *rdf_parser, raptor_uri *uri)

    #--------------------------------------------------------------------------------------------------------
    # serializer
    #--------------------------------------------------------------------------------------------------------
    raptor_serializer* raptor_new_serializer(raptor_world *world, char *name)
    void raptor_free_serializer(raptor_serializer *rdf_serializer)
    int raptor_serializer_start_to_filename(raptor_serializer *rdf_serializer, char *filename)
    int raptor_serializer_start_to_string(raptor_serializer *rdf_serializer, raptor_uri *uri, void **string_p, size_t *length_p)
    int raptor_serializer_start_to_file_handle(raptor_serializer *rdf_serializer, raptor_uri *uri, FILE *fh)
    int raptor_serializer_serialize_statement(raptor_serializer *rdf_serializer, raptor_statement *statement)
    int raptor_serializer_serialize_end(raptor_serializer *rdf_serializer)
    
    #--------------------------------------------------------------------------------------------------------
    # uri
    #--------------------------------------------------------------------------------------------------------
    raptor_uri* raptor_new_uri(raptor_world *world, unsigned char *uri_string)
    void raptor_free_uri(raptor_uri *uri)
    raptor_uri* raptor_uri_copy(raptor_uri *uri)
    unsigned char* raptor_uri_filename_to_uri_string(char *filename)
    
    #--------------------------------------------------------------------------------------------------------
    # memory
    #--------------------------------------------------------------------------------------------------------
    void raptor_free_memory(void *ptr)
    