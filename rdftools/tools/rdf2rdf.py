import os
import sys
from multiprocessing import Pool
from rdftools.raptorutil import rdf_ext
from rdftools.tools.base import RdfTool
from rdftools.tools.jvmrdftools import run_rdf2rdf_converter

__author__ = 'basca'

def dest_file_name(src, dst_format):
    ext = os.path.splitext(src)[-1]
    dst_ext = rdf_ext.get(dst_format, [None])[0]
    if ext != '.%s' % dst_ext:
        return '%s.%s' % (os.path.splitext(src)[0], dst_ext)
    return None


def to_process(src, dst_format):
    if os.path.isdir(src):
        return False
    return dest_file_name(src, dst_format) is not None


def convert_file(source, dst_format, clr_src=False):
    rdf2rdf = Rdf2Rdf()
    rdf2rdf.convert(source, dst_format, clear_source=clr_src)


class Rdf2Rdf(RdfTool):
    def __init__(self, *args, **kwargs):
        super(Rdf2Rdf, self).__init__(*args, **kwargs)

    def convert(self, source, destination_format, clear_source=False):
        """
        convert source rdf files to destination format
        :param source: the source file(s)
        :param destination_format: the destination format
        :param clear_source: if set delete the source files, default = False
        :return: None
        """
        run_rdf2rdf_converter(source, destination_format)
        if clear_source:
            self._log.warn('REMOVE: {0}'.format(source))
            os.remove(source)

    def _run(self, source, destination_format, clear_source=False):
        """
        parallel version of the `convert` method
        :param source: (rdf) files to convert (source path)
        :param destination_format: the destination format
        :param clear_source: if set, delete the source files. Default = False
        :return: None
        """

        files = []
        src = os.path.abspath(source)
        if os.path.isdir(src):
            files = [os.path.join(src, f) for f in os.listdir(src) if to_process(f, destination_format)]
        elif os.path.exists(src):
            files = [src]
        self._log.info('to process: {0}'.format(files))
        if clear_source:
            self._log.warn('will remove original files after conversion')

        def job_finished(res):
            print '.',
            sys.stdout.flush()

        pool = Pool()
        for src in files:
            dst = dest_file_name(src, destination_format)
            if dst:
                pool.apply_async(convert_file, (src, dst, clear_source), callback=job_finished)

        pool.close()
        pool.join()

