__author__ = 'basca'

import os

rdf_ext = {
    'rdfxml'        : 'rdf',
    'ntriples'      : 'nt',
    'turtle'        : 'n3',
    'rdfa'          : 'rdfa',
    'guess'         : None,
    'rss-tag-soup'  : None,
}

def get_parser_type(fname, default='rdfdxml'):
    ext = os.path.splitext(fname)[1][1:]
    for k in rdf_ext:
        if rdf_ext[k] is not None and ext.upper() == rdf_ext[k].upper():
            return k
    return default

def get_rdfext(format):
    return rdf_ext.get(format,None)

def supported(fname):
    fext = os.path.splitext(fname)[1][1:]
    for rdf_type, ext in rdf_ext.items():
        if ext is None:
            continue
        if fext.lower() == ext.lower():
            return True
    return False
  