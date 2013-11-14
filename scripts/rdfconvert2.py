#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
import time
import sys
import os
import commands
import rdftools
from multiprocessing import Pool
from rdftools.__version__ import str_version

BUNDLED_RDF2RDF_PATH = os.path.join(os.path.split(rdftools.__file__)[0],'RDF2RDF')

#-----------------------------------------------------------------------------------------------------------------------
#
# path to RDF2RDF (kept inside installed package)
#
#-----------------------------------------------------------------------------------------------------------------------
def get_rdf2rdf_path():
    rdf2rdf_path = BUNDLED_RDF2RDF_PATH
    if 'RDF2RDF_PATH' in os.environ:
        rdf2rdf_path = os.environ.get('RDF2RDF_PATH', BUNDLED_RDF2RDF_PATH)

    return BUNDLED_RDF2RDF_PATH if not rdf2rdf_path else rdf2rdf_path


#-----------------------------------------------------------------------------------------------------------------------
#
# the java convert function wrapper
#
#-----------------------------------------------------------------------------------------------------------------------
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

#-----------------------------------------------------------------------------------------------------------------------
#
# utility functions
#
#-----------------------------------------------------------------------------------------------------------------------
def dest_file_name(src, dst_format):
    ext = os.path.splitext(src)[-1]
    dst_ext = rdftools.raptorutil.rdf_ext.get(dst_format, [None])[0]
    if ext != '.%s'%dst_ext:
        return '%s.%s'%(os.path.splitext(src)[0], dst_ext)
    return None

def to_process(src, dst_format):
    if os.path.isdir(src):
        return False
    return dest_file_name(src, dst_format) is not None

#-----------------------------------------------------------------------------------------------------------------------
#
# parallel processor
#
#-----------------------------------------------------------------------------------------------------------------------
def convert_files(files, dst_format, rdf2rdf_path, clear):
    def job_finished(res):
        print '[done]',
        sys.stdout.flush()

    pool = Pool()
    for src in files:
        dst = dest_file_name(src, dst_format)
        if dst:
            pool.apply_async(convert,(rdf2rdf_path, src, dst, clear), callback = job_finished)

    pool.close()
    pool.join()

#-----------------------------------------------------------------------------------------------------------------------
#
# supported serializers and parsers
#
#-----------------------------------------------------------------------------------------------------------------------
parsers = [
    'rdfxml',
    'ntriples',
    'turtle',
    'trig',
    'guess',
    'rss-tag-soup',
    'rdfa',
    'nquads',
    'grddl'
]

serializers = [
    'rdfxml',
    'rdfxml-abbrev',
    'turtle',
    'ntriples',
    'rss-1.0',
    'dot',
    'html',
    'json',
    'atom',
    'nquads'
]

def main():
    """
usage: rdfconvert2.py [-h] [--clear] [--dst_format DST_FORMAT] [--version]
                      SOURCE

rdf converter (2), makes use of RDF2RDF - requires java

positional arguments:
  SOURCE                the source file or location (of files) to be converted

optional arguments:
  -h, --help            show this help message and exit
  --clear               clear the original files (delete) - this action is
                        permanent, use with caution!
  --dst_format DST_FORMAT
                        the destination format to convert to
  --version             the current version
    """
    parser = argparse.ArgumentParser(description='rdf converter (2), makes use of RDF2RDF - requires java')

    parser.add_argument('source', metavar='SOURCE', type=str,
                       help='the source file or location (of files) to be converted')
    parser.add_argument('--clear', dest='clear', action='store_true',
                       help='clear the original files (delete) - this action is permanent, use with caution!')
    parser.add_argument('--dst_format', dest='dst_format', action='store', type=str, default='ntriples',
                       help='the destination format to convert to')
    parser.add_argument('--version', dest='version', action='store_true',
                       help='the current version')

    args = parser.parse_args()

    rdf2rdf_path = get_rdf2rdf_path()
    print 'using RDF2RDF path=',rdf2rdf_path

    if args.version:
        print 'using version %s'%str_version
    else:
        t0      = time.time()
        files   = []
        src     = os.path.abspath(args.source)
        if  os.path.isdir(src):
            files = [os.path.join(src, f) for f in os.listdir(src) if to_process(f, args.dst_format)]
        elif os.path.exists(src):
            files = [src]
        print 'To process : ',files
        if args.clear:
            print 'will remove original files after conversion'
        convert_files(files, args.dst_format, rdf2rdf_path, args.clear)

        print 'Took %s seconds'%(str(time.time()-t0))


if __name__ == '__main__':
    main()