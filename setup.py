__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext

__version__ = (0,0,2)
str_ver = lambda : '%d.%d.%d'%(__version__[0],__version__[1],__version__[2])

setup(
    name ='rdftools',
    version = str_ver(),
    description = 'collection of RDF scripts and tools',
    author = 'Cosmin Basca',
    author_email = 'basca@ifi.uzh.ch',
    cmdclass = {'build_ext': build_ext},
    packages = ["rdftools"],
    ext_modules = [
                   Extension('rdftools.converter', ['rdftools/converter.pyx', 'rdftools/crdfio.pxd'],
                            #library_dirs 	= ['/usr/lib', '/usr/local/lib'],
                            libraries 		= ['raptor',],
                            #include_dirs    = ['/usr/local/include','/usr/include'],
                            extra_compile_args = ['-fPIC']),
                   ],
    install_requires = ['cython>=0.13'],
    scripts = ['rdfconvert.py'],
)