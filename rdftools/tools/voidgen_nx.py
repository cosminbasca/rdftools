import os
from rdftools.tools.base import RdfTool
from rdftools.raptorutil import rdf_ext
from rdftools.tools.jvmrdftools import run_nxvoid_generator

__author__ = 'basca'

def dest_file_name(src, dst_format):
    ext = os.path.splitext(src)[-1]
    dst_ext = rdf_ext.get(dst_format, [None])[0]
    if ext != '.%s' % dst_ext:
        return '%s.%s' % (os.path.splitext(src)[0], dst_ext)
    return None


class VoIDGenNX(RdfTool):
    def __init__(self, *args, **kwargs):
        super(VoIDGenNX, self).__init__(*args, **kwargs)

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

        run_nxvoid_generator(source, dataset_id, '{0}.void.xml'.format(source))
