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
import os
from rdftools.tools.base import RdfTool
from rdftools.raptorutil import rdf_ext
from rdftools.tools.jvmrdftools import run_jvmvoid_generator

__author__ = 'basca'

def dest_file_name(src, dst_format):
    ext = os.path.splitext(src)[-1]
    dst_ext = rdf_ext.get(dst_format, [None])[0]
    if ext != '.%s' % dst_ext:
        return '%s.%s' % (os.path.splitext(src)[0], dst_ext)
    return None


class VoIDGenScala(RdfTool):
    def __init__(self, *args, **kwargs):
        super(VoIDGenScala, self).__init__(*args, **kwargs)

    def _run(self, source, dataset_id):
        """
        generate void statistics from source data using the nxparser library
        :param source: the source file(s)
        :param dataset_id: the dataset id to analize
        :return: None
        """
        if source is None:
            self._log.error('source files cannot be None')
            return

        run_jvmvoid_generator(source, dataset_id, '{0}.void.json'.format(source))
