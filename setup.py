__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from libutil import get_lib_dir, get_include_dir

str_version = None
execfile('rdftools/__version__.py')

def extension(name, libs, language='c', options=[], c_sources=[]):
    extension_name = 'rdftools.%s'%name
    extension_path = 'rdftools/%s.pyx'%('/'.join(name.split('.')))
    return Extension(extension_name,
                     [extension_path,] + c_sources,
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
    package_dir = {"rdftools":"rdftools"},
    ext_modules = [
        extension('rdfparse'     ,['raptor2']),
        extension('gcityhash'    ,['cityhash'],     language='c++',  options=['-Wno-sign-compare'])
    ],
    install_requires =[
        'cython>=0.19.2',
        'py4j>=0.8',
        'pyyaml>=3.10',
        'cybloom>=0.7.2',
        'sh>=1.09',
    ],
    include_package_data = True,
    exclude_package_data = {
        'rdftools': ['*.c', '*.h', '*.pyx', '*.pxd']
    },
    zip_safe = False,
    scripts = [
        'scripts/rdfconvert.py',
        'scripts/rdfconvert2.py',
        'scripts/rdfencode.py',
        'scripts/genlubm.py',
        'scripts/genlubmdistro.py',
        'scripts/genvoid.py',
        'scripts/genvoid2.py',
        'scripts/ntround.py',
    ],
)