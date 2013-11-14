__author__ = 'basca'

import os

# the first extension is considered as a default extension
rdf_ext = {
    'rdfxml'        : ['rdf', 'xml', 'owl'],
    'ntriples'      : ['nt'],
    'nquads'        : ['nq'],
    'turtle'        : ['n3', 'ttl'],
    'rdfa'          : ['rdfa'],
    'trig'          : ['trig'],
    'guess'         : None,
    'rss-tag-soup'  : None,
}

NOEXTENSION = '~'

KB = 1024           # 1 Kilobyte
MB = 1048576        # 1 MegaByte
GB = 1073741824     # 1 GigaByte

def get_parser_type(fname, default='rdfdxml'):
    fext = os.path.splitext(fname)[1][1:]
    for ptype, extns in rdf_ext.items():
        if extns is None:
            pass
        else:
            for ex in extns:
                if fext.upper() == ex.upper():
                    return ptype
    return default

def get_rdfext(format):
    rext = rdf_ext.get(format,None)
    return rext[0] if rext is not None else NOEXTENSION

def supported(fname):
    fext = os.path.splitext(fname)[1][1:]
    for ptype, extns in rdf_ext.items():
        if extns is None:
            continue
        else:
            for ex in extns:
                if fext.upper() == ex.upper():
                    return True
    return False
  