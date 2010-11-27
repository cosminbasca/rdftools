__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
                   Extension('rdftools.converter', ['rdftools/converter.pyx', 'rdftools/crdfio.pxd'],
                            #library_dirs 	= ['/usr/lib', '/usr/local/lib'],
                            libraries 		= ['raptor',],
                            #include_dirs    = ['/usr/local/include','/usr/include'],
                            extra_compile_args = ['-fPIC']),
                   ],
)