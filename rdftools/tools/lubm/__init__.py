import os
import io
import sh
import sys
import re
from multiprocessing import Pool, cpu_count
from rdftools import interval_split
from rdftools.tools.base import RdfTool
from rdftools.tools.raptor import RaptorRdf
from py4j.java_gateway import JavaGateway

__author__ = 'basca'

_CLASSPATH = os.path.join(os.path.split(__file__)[0], 'classpath')


def lubm_generator(classpath, jar, num_universities, index, generator_seed, ontology, output_path):
    gateway = JavaGateway.launch_gateway(classpath='.:%s/%s' % (classpath, jar), die_on_exit=True)
    jvm = gateway.jvm
    generator = jvm.edu.lehigh.swat.bench.uba.Generator()
    generator.start(int(num_universities), int(index), int(generator_seed), False, ontology, output_path)
    gateway.shutdown_gateway()


class Lubm(RdfTool):
    def __init__(self, ontology=None, path=None, *args, **kwargs):
        super(Lubm, self).__init__(*args, **kwargs)
        global _CLASSPATH
        self._classpath = _CLASSPATH
        self._ontology = ontology if ontology else 'http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl'
        self._output_path = os.path.abspath(path) if path else os.getcwd()
        if not os.path.isdir(self._output_path):
            raise ValueError('path: {0} is not a valid path'.format(self._output_path))

    @property
    def ontology(self):
        """
        the lubm ontology, used internally by the generator
        :return: the lubm ontology
        """
        return self._ontology

    @property
    def env_var(self):
        """
        the lubm environment variable
        :return: the lubm environment variable
        """
        return 'LUBM_PATH'

    @property
    def jar(self):
        """
        the jar representing the nxparser library
        :return: the jar representing the nxparser library
        """
        return 'uba1.7.jar'

    @property
    def classpath(self):
        """
        the classpath of the bundled lubm, if the 'LUBM_PATH' env var is set, the path is taken from there
        :return: the classpath
        """
        cp = self._classpath
        if self.env_var in os.environ:
            cp = os.environ.get(self.env_var, None)
        return cp if cp else self._classpath


    def _run(self, num_universities, index=0, generator_seed=0):
        """
        a paralel version of the `generate` method

        :param num_universities: number of universities to generate
        :param index: the index at whitch the generation process starts
        :param generator_seed:  a seed used by the generator
        :return: None
        """

        def job_finished(res):
            pass

        num_workers = cpu_count()
        pool = Pool(processes=num_workers)

        for start, unis_per_worker in interval_split(num_workers, num_universities, threshold=10):
            idx = start + index
            pool.apply_async(
                lubm_generator,
                (self.classpath, self.jar, unis_per_worker, idx, generator_seed, self.ontology, self._output_path),
                callback=job_finished)

        pool.close()
        pool.join()

        # convert all to ntriples

        self._log.info('converting to ntriples ... ')
        rdf_converter = RaptorRdf()
        rdf_converter(self._output_path, destination_format='ntriples', buffer_size=16, clear=True)
        print

        # now concatenate all files belonging to 1 university together
        files = os.listdir(self._output_path)
        sfiles = ' '.join(files)
        uni_files = lambda uni: re.findall(r'University%d_[0-9]+\.nt' % uni, sfiles)
        for uni in xrange(num_universities):
            ufiles = uni_files(uni)

            with io.open(os.path.join(self._output_path, 'University%d.nt' % uni), 'w+') as UNI:
                for upart in ufiles:
                    upart_file = os.path.join(self._output_path, upart)
                    with io.open(upart_file, 'r+') as UPART:
                        UNI.write(UPART.read())
                    sh.rm(upart_file)

        self._log.info('done')


