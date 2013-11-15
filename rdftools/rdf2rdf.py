import os
import commands

__author__ = 'basca'

BUNDLED_RDF2RDF_PATH = os.path.join(os.path.split(__file__)[0],'rdf2rdf')

#-----------------------------------------------------------------------------------------------------------------------
#
# path to rdf2rdf (kept inside installed package)
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
def exec_rdf2rdf(rdf2rdf_path, src, dst, clear):
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
