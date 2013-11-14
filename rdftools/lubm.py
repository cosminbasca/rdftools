import os
import commands

__author__ = 'basca'

BUNDLED_LUBM_PATH = os.path.join(os.path.split(__file__)[0],'Uba1.7')
LUBM_ONTO = 'http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl'

#-----------------------------------------------------------------------------------------------------------------------
#
# path to lubm generator (bundled inside installed package)
#
#-----------------------------------------------------------------------------------------------------------------------
def get_lubm_path(args):
    lubm_path = BUNDLED_LUBM_PATH
    if len(args) == 1:
        lubm_path = args[0]
    elif 'LUBM_PATH' in os.environ:
        lubm_path = os.environ.get('LUBM_PATH', None)
    return BUNDLED_LUBM_PATH if not lubm_path else lubm_path


#-----------------------------------------------------------------------------------------------------------------------
#
# lubm command
#
#-----------------------------------------------------------------------------------------------------------------------
def exec_lubm(lubm_path, univ, index, seed, onto):
    status, output = commands.getstatusoutput('java -cp %s edu.lehigh.swat.bench.uba.Generator -univ %s -index %s -seed %s -onto %s'%(
        lubm_path, univ, index, seed, onto
    ))
    if status:
        print "an error occured!"
        print output
