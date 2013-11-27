__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from libutil import get_include_dir, get_lib_dir

def extension(name, libs, language='c', options=[]):
    return Extension('rdftools.%s'%name,
                     ['rdftools/%s.pyx'%name,],
                     language           = language,
                     libraries          = list(libs),
                     library_dirs 	    = get_lib_dir(),
                     include_dirs       = get_include_dir(),
                     extra_compile_args = ['-fPIC']+options)

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        extension('converter'    ,['raptor2']),
        extension('gcityhash'    ,['cityhash'],     language='c++')
    ]
)