__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from libutil import get_include_dir, get_lib_dir

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
                   Extension('rdftools.converter', ['rdftools/converter.pyx', 'rdftools/crdfio.pxd'],
                             libraries 		    = ['raptor2',],
                             library_dirs 	    = get_lib_dir(),
                             include_dirs       = get_include_dir(),
                             extra_compile_args = ['-fPIC']),
                   ],
)