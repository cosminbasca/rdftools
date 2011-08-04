#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from optparse import OptionParser
import time
import sys
import os
import commands
import rdftools
from multiprocessing import Pool

BUNDLED_RDF2RDF_PATH = os.path.join(os.path.split(rdftools.__file__)[0],'RDF2RDF')

def get_rdf2rdf_path(args):
    rdf2rdf_path = BUNDLED_RDF2RDF_PATH
    if len(args) == 1:
        rdf2rdf_path = args[0]
    elif 'RDF2RDF_PATH' in os.environ:
        rdf2rdf_path = os.environ.get('RDF2RDF_PATH', None)

    return BUNDLED_RDF2RDF_PATH if not rdf2rdf_path else rdf2rdf_path


def convert(rdf2rdf_path, src, dst):
    status, output = commands.getstatusoutput('java -jar %s/rdf2rdf-1.0.1-2.3.1.jar %s %s'%(
        rdf2rdf_path, src, dst
    ))
    if status:
        print "an error occured!"
        print output


def convert_files(files, dst_format, buffer_size):
    def job_finished(res):
        print '|',
        sys.stdout.flush()

    pool = Pool()
    for src in files:
        pool.apply_async(convert_chunked,(src, dst_format, buffer_size), callback = job_finished)

    pool.close()
    pool.join()

parsers = ['rdfxml', 'ntriples', 'turtle', 'trig', 'guess', 'rss-tag-soup', 'rdfa', 'nquads', 'grddl']
serializers = ['rdfxml', 'rdfxml-abbrev', 'turtle', 'ntriples', 'rss-1.0', 'dot', 'html', 'json', 'atom', 'nquads']

def main():
    usage = "usage: %prog [options] SOURCE"
    parser = OptionParser(usage=usage)
    parser.add_option('-c','--clear', type='bool',
                      action='store', dest='clear', default=False,
                      help='''clear the original files''')
    parser.add_option('-d','--dst_format', type='string',
                      action='store', dest='dst_format', default='ntriples',
                      help='''the destination format''')

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments (perhaps you did not specify the SOURCE, use --help for further details)")

    t0      = time.time()
    files   = []
    src     = os.path.abspath(args[0])
    if  os.path.isdir(src):
        files = [os.path.join(src, f) for f in os.listdir(src)]
    elif os.path.exists(src):
        files = [src]
    print 'To process : ',files
    convert_files(files)

    print 'Took %s seconds'%(str(time.time()-t0))


if __name__ == '__main__':
    main()