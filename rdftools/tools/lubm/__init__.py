import os
import io
import sh
import sys
import re
from multiprocessing import Pool
from rdftools.tools.base import RdfTool
from rdftools.tools.raptor import RaptorRdf

__author__ = 'basca'

_CLASSPATH = os.path.join(os.path.split(__file__)[0], 'classpath')


def gen_uni(num_unis, idx, seed):
    lubm = Lubm()
    lubm.generate(num_unis, idx, seed)


class Lubm(RdfTool):
    def __init__(self, ontology=None):
        global _CLASSPATH
        self._classpath = _CLASSPATH
        self._ontology = ontology if ontology else 'http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl'

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
    def classpath(self):
        """
        the classpath of the bundled lubm, if the 'LUBM_PATH' env var is set, the path is taken from there
        :return: the classpath
        """
        cp = self._classpath
        if self.env_var in os.environ:
            cp = os.environ.get(self.env_var, None)
        return cp if cp else self._classpath

    def generate(self, num_universities, index, generator_seed):
        """
        the method calls the bundled lubm generator with the specified parameters

        :param num_universities: number of universities to generate
        :param index: the index at whitch the generation process starts
        :param generator_seed:  a seed used by the generator
        """
        print '[generate] Lubm num_unis=%s, index=%s'%(num_universities, index)
        sys.stdout.flush()
        output = sh.java('-cp', self.classpath, 'edu.lehigh.swat.bench.uba.Generator', '-univ', num_universities,
                         '-index', index,
                         '-seed', generator_seed, '-onto', self.ontology)
        if output.exit_code:
            print 'an error occured, while running lubm'
            print output

    def _run(self, num_universities, index=0, generator_seed=0):
        """
        a paralel version of the `generate` method

        :param num_universities: number of universities to generate
        :param index: the index at whitch the generation process starts
        :param generator_seed:  a seed used by the generator
        :return: None
        """

        def job_finished(res):
            # print '.',
            # sys.stdout.flush()
            pass

        max_unis = 10

        pool = Pool()
        for idx in xrange(index, num_universities + index, max_unis):
            pool.apply_async(gen_uni, (max_unis, idx, generator_seed), callback=job_finished)

        pool.close()
        pool.join()

        # convert all to ntriples
        print 'converting to ntriples ... '
        rdf_converter = RaptorRdf()
        rdf_converter('.', destination_format='ntriples', buffer_size=64, clear=True)

        # now concatenate all files belonging to 1 university together
        files = os.listdir('.')
        sfiles = ' '.join(files)
        uni_files = lambda uni: re.findall('University%d_[0-9]+\.nt'%uni, sfiles)
        for uni in xrange(num_universities):
            ufiles = uni_files(uni)

            with io.open('University%d.nt'%uni, 'w+') as UNI:
                for upart in ufiles:
                    with io.open(upart, 'r+') as UPART:
                        UNI.write(UPART.read())
                    sh.rm(upart)

        print 'done'


