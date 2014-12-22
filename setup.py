#!/usr/bin/env python
#
# author: Cosmin Basca
#
# Copyright 2010 University of Zurich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup

from setuptools.extension import Extension
from Cython.Distutils import build_ext
import os


def get_lib_dir(default='/usr/lib:/usr/local/lib'):
    libpath = os.environ.get('DYLD_LIBRARY_PATH', None)
    libpath = libpath if libpath else os.environ.get('LD_LIBRARY_PATH', None)
    libpath = libpath if libpath else default
    return [p for p in libpath.split(':') if p]


def get_include_dir(default='/usr/local/include:/usr/include'):
    incpath = os.environ.get('C_INCLUDE_PATH', None)
    incpath = incpath if incpath else default
    return [p for p in incpath.split(':') if p]


NAME = 'rdftools'


def extension(name, libs, language='c', options=None, c_sources=None):
    if not c_sources: c_sources = []
    if not options: options = []
    extension_name = '{0}.{1}'.format(NAME, name)
    extension_path = '{0}/{1}.pyx'.format(NAME, '/'.join(name.split('.')))
    return Extension(extension_name, [extension_path, ] + c_sources, language=language, libraries=list(libs),
                     library_dirs=get_lib_dir(), include_dirs=get_include_dir(), extra_compile_args=['-fPIC'] + options)


str_version = None
execfile('{0}/__version__.py'.format(NAME))

# Load up the description from README
with open('README.md') as f:
    DESCRIPTION = f.read()

pip_deps = [
    'cython>=0.21',
    'pyyaml>=3.11',
    'rdflib>=4.1.2',
    'natsort>=3.5.0 ',
    'sh>=1.09',
]

manual_deps = [
    'cybloom>=0.7.3'
]

setup(
    name=NAME,
    version=str_version,
    author='Cosmin Basca',
    author_email='cosmin.basca@gmail.com; basca@ifi.uzh.ch',
    # url=None,
    description='A ollection of RDF scripts and tools',
    long_description=DESCRIPTION,
    cmdclass={'build_ext': build_ext},
    ext_modules=[
        extension('rdfparse', ['raptor2']),
        extension('gcityhash', ['cityhash'], language='c++', options=['-Wno-sign-compare'])
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Cython',
        'Programming Language :: C',
        'Programming Language :: Java',
        'Topic :: Software Development'
    ],
    packages=[NAME,
              '{0}/tools'.format(NAME),
              '{0}/tools/jvmrdftools'.format(NAME),
              '{0}/datagen'.format(NAME),
    ],
    package_data={
        '{0}/tools/jvmrdftools'.format(NAME): ['lib/*', ],
        '{0}'.format(NAME): ['*.ini', '*.pxd', ],
    },
    install_requires=pip_deps + manual_deps,
    entry_points={
        'console_scripts': [
            '{1} = {0}.cli:{1}'.format(NAME, 'rdfconvert'),
            '{1} = {0}.cli:{1}'.format(NAME, 'rdfconvert2'),
            '{1} = {0}.cli:{1}'.format(NAME, 'rdfencode'),
            '{1} = {0}.cli:{1}'.format(NAME, 'genlubm'),
            '{1} = {0}.cli:{1}'.format(NAME, 'genlubmdistro'),
            '{1} = {0}.cli:{1}'.format(NAME, 'genvoid'),
            '{1} = {0}.cli:{1}'.format(NAME, 'genvoid2'),
            '{1} = {0}.cli:{1}'.format(NAME, 'ntround'),
        ]
    }
)
