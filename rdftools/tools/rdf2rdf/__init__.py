import os
from rdftools.tools.base import ExternalTool
import sh
from multiprocessing import Pool
import sys
from rdftools.raptorutil import rdf_ext

__author__ = 'basca'

_CLASSPATH = os.path.join(os.path.split(__file__)[0], 'classpath')


def dest_file_name(src, dst_format):
    ext = os.path.splitext(src)[-1]
    dst_ext = rdf_ext.get(dst_format, [None])[0]
    if ext != '.%s' % dst_ext:
        return '%s.%s' % (os.path.splitext(src)[0], dst_ext)
    return None


class Rdf2Rdf(ExternalTool):
    def __init__(self):
        global _CLASSPATH
        self._classpath = _CLASSPATH

    @property
    def jar(self):
        """
        the jar representing the rdf2rdf tool
        :return: the jar representing the rdf2rdf tool
        """
        return 'rdf2rdf-1.0.1-2.3.1.jar'

    @property
    def env_var(self):
        """
        the nxparrser environment variable
        :return: the nxparser environment variable
        """
        return 'RDF2RDF_PATH'

    @property
    def classpath(self):
        """
        the classpath of the bundled rdf2rdf, if the 'RDF2RDF_PATH' env var is set, the path is taken from there
        :return: the classpath
        """
        cp = self._classpath
        if self.env_var in os.environ:
            cp = os.environ.get(self.env_var, None)
        return cp if cp else self._classpath

    def convert(self, source, destination_format, clear_source=False):
        """
        convert source rdf files to destination format
        :param source: the source file(s)
        :param destination_format: the destination format
        :param clear_source: if set delete the source files, default = False
        :return: None
        """
        output = sh.java('-jar', self.jar, source, destination_format)
        if output.exit_code or output.strip('\n').strip().split('\n')[0].find('Exception:') >= 0:
            print "an error occured!"
            print output
        elif clear_source:
            print 'REMOVE : ', source
            os.remove(source)

    @staticmethod
    def pconvert(files, destination_format, clear_source=False):
        """
        parallel version of the `convert` method
        :param files: (rdf) files to convert
        :param destination_format: the destination format
        :param clear_source: if set, delete the source files. Default = False
        :return: None
        """

        def job_finished(res):
            print '[done]',
            sys.stdout.flush()

        def convert_file(source, dst_format, clr_src=False):
            rdf2rdf = Rdf2Rdf()
            rdf2rdf.convert(source, dst_format, clear_source=clr_src)

        pool = Pool()
        for src in files:
            dst = dest_file_name(src, destination_format)
            if dst:
                pool.apply_async(convert_file, (src, dst, clear_source), callback=job_finished)

        pool.close()
        pool.join()

