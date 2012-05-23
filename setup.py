__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from libutil import get_lib_dir, get_include_dir

__version__ = (0,0,4)
str_ver = lambda : '%d.%d.%d'%(__version__[0],__version__[1],__version__[2])

def extension(name, libs, language='c', options=[]):
    return Extension('rdftools.%s'%name,
                     ['rdftools/%s.pyx'%name,],
                     language           = language,
                     libraries          = list(libs),
                     library_dirs 	    = get_lib_dir(),
                     include_dirs       = get_include_dir(),
                     extra_compile_args = ['-fPIC']+options)

setup(
    name ='rdftools',
    version = str_ver(),
    description = 'collection of RDF scripts and tools',
    author = 'Cosmin Basca',
    author_email = 'basca@ifi.uzh.ch',
    cmdclass = {'build_ext': build_ext},
    packages = ["rdftools"],
    ext_modules = [extension('converter'    ,['raptor2'])],
    install_requires = ['cython==0.15.1'],
    include_package_data = True,
    exclude_package_data = { 'rdftools': ['*.c', '*.h', '*.pyx', '*.pxd'] },
    zip_safe = False,
    scripts = ['rdfconvert.py','rdfconvert2.py','genlubm.py'],
)