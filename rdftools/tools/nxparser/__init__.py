import os
from rdftools.util import log_time
from rdftools.tools.base import RdfTool
from rdftools.raptorutil import rdf_ext
from py4j.java_gateway import JavaGateway

__author__ = 'basca'

_CLASSPATH = os.path.join(os.path.split(__file__)[0], 'classpath')


def dest_file_name(src, dst_format):
    ext = os.path.splitext(src)[-1]
    dst_ext = rdf_ext.get(dst_format, [None])[0]
    if ext != '.%s' % dst_ext:
        return '%s.%s' % (os.path.splitext(src)[0], dst_ext)
    return None


class NxParser(RdfTool):
    def __init__(self):
        global _CLASSPATH
        self._classpath = _CLASSPATH

    @property
    def jar(self):
        """
        the jar representing the nxparser library
        :return: the jar representing the nxparser library
        """
        return 'nxparser-1.2.3.jar'

    @property
    def env_var(self):
        """
        the nxparrser environment variable
        :return: the nxparser environment variable
        """
        return 'NXPARSER_PATH'

    @property
    def classpath(self):
        """
        the classpath of the bundled nxparser, if the 'NXPARSER_PATH' env var is set, the path is taken from there
        :return: the classpath
        """
        cp = self._classpath
        if self.env_var in os.environ:
            cp = os.environ.get(self.env_var, None)
        return cp if cp else self._classpath


    @log_time(None)
    def gen_void(self, source, dataset_id):
        """
        generate void statistics from source data using the nxparser library
        :param source: the source file(s)
        :param dataset_id: the dataset id to analize
        :return: None
        """
        if source is None:
            print 'source files cannot be None'
            return

        gateway = JavaGateway.launch_gateway(classpath='.:%s/%s' % (self.classpath, self.jar))
        jvm = gateway.jvm
        print 'get VoiD object...'
        stats_engine = jvm.org.semanticweb.yars.stats.VoiD()

        print 'get input'
        _input = jvm.java.io.FileInputStream(source)
        print 'get output'
        _output = jvm.java.io.FileOutputStream('%s.void.xml' % source)

        print 'gen void'
        stats_engine.analyseVoid(_input, dataset_id, _output)
