__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from libutil import get_lib_dir, get_include_dir
from rdftools.__version__ import str_version

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
    version = str_version,
    description = 'collection of RDF scripts and tools',
    author = 'Cosmin Basca',
    author_email = 'basca@ifi.uzh.ch',
    cmdclass = {'build_ext': build_ext},
    packages = ["rdftools"],
    ext_modules = [extension('converter'    ,['raptor2'])],
    install_requires =[
        'cython>=0.19.2',
        'cybloom>=0.7.2',
        'py4j>=0.8',
    ],
    include_package_data = True,
    exclude_package_data = {
        'rdftools': ['*.c', '*.h', '*.pyx', '*.pxd']
    },
    zip_safe = False,
    scripts = [
        'scripts/rdfconvert.py',
        'scripts/rdfconvert2.py',
        'scripts/genlubm.py',
        'scripts/genvoid.py'
        'scripts/genvoid2.py'
    ],
)