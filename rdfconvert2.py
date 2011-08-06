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

def get_rdf2rdf_path():
    rdf2rdf_path = BUNDLED_RDF2RDF_PATH
    if 'RDF2RDF_PATH' in os.environ:
        rdf2rdf_path = os.environ.get('RDF2RDF_PATH', BUNDLED_RDF2RDF_PATH)

    return BUNDLED_RDF2RDF_PATH if not rdf2rdf_path else rdf2rdf_path


def convert(rdf2rdf_path, src, dst, clear):
    cmd = 'java -jar %s/rdf2rdf-1.0.1-2.3.1.jar %s %s'%(rdf2rdf_path, src, dst)
    status, output = commands.getstatusoutput(cmd)
    print 'STATUS = ',status
    if status or output.strip('\n').strip().split('\n')[0].find('Exception:') >= 0:
        print "an error occured!"
        print cmd
        print output
        return

    if clear:
        print 'REMOVE : ',src
        os.remove(src)

def get_dst_fname(src, dst_format):
    ext = os.path.splitext(src)[-1]
    dst_ext = rdftools.raptorutil.rdf_ext.get(dst_format, [None])[0]
    if ext != '.%s'%dst_ext:
        return '%s.%s'%(os.path.splitext(src)[0], dst_ext)
    return None

def to_process(src, dst_format):
    if os.path.isdir(src):
        return False
    return get_dst_fname(src, dst_format) is not None


def convert_files(files, dst_format, rdf2rdf_path, clear):
    def job_finished(res):
        print '[done]',
        sys.stdout.flush()

    pool = Pool()
    for src in files:
        dst = get_dst_fname(src, dst_format)
        if dst:
            pool.apply_async(convert,(rdf2rdf_path, src, dst, clear), callback = job_finished)

    pool.close()
    pool.join()

parsers = ['rdfxml', 'ntriples', 'turtle', 'trig', 'guess', 'rss-tag-soup', 'rdfa', 'nquads', 'grddl']
serializers = ['rdfxml', 'rdfxml-abbrev', 'turtle', 'ntriples', 'rss-1.0', 'dot', 'html', 'json', 'atom', 'nquads']

def main():
    usage = "usage: %prog [options] SOURCE"
    parser = OptionParser(usage=usage)
    parser.add_option('-c','--clear',
                      action='store_true', dest='clear', default=False,
                      help='''clear the original files''')
    parser.add_option('-d','--dst_format', type='string',
                      action='store', dest='dst_format', default='ntriples',
                      help='''the destination format''')

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments (perhaps you did not specify the SOURCE, use --help for further details)")

    rdf2rdf_path = get_rdf2rdf_path()
    print 'RDF2RDF path=',rdf2rdf_path

    t0      = time.time()
    files   = []
    src     = os.path.abspath(args[0])
    if  os.path.isdir(src):
        files = [os.path.join(src, f) for f in os.listdir(src) if to_process(f, options.dst_format)]
    elif os.path.exists(src):
        files = [src]
    print 'To process : ',files
    print 'remove originals: ',options.clear
    convert_files(files, options.dst_format, rdf2rdf_path, options.clear)

    print 'Took %s seconds'%(str(time.time()-t0))


if __name__ == '__main__':
    main()