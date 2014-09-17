import os
import io
import sh
import re
from multiprocessing import Pool, cpu_count
from rdftools import interval_split
from rdftools.tools.base import RdfTool
from rdftools.tools.jvmrdftools import run_lubm_generator
from rdftools.tools.raptor import RaptorRdf

__author__ = 'basca'

UNIS_PER_WORKER = 20

class Lubm(RdfTool):
    def __init__(self, ontology=None, path=None, *args, **kwargs):
        super(Lubm, self).__init__(*args, **kwargs)
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

    def _run(self, num_universities, index=0, generator_seed=0, workers = -1):
        """
        a paralel version of the `generate` method

        :param num_universities: number of universities to generate
        :param index: the index at whitch the generation process starts
        :param generator_seed:  a seed used by the generator
        :return: None
        """

        def job_finished(res):
            pass

        num_cpus = cpu_count()
        num_workers = workers if 0 < workers < num_cpus else num_cpus

        pool = Pool(processes=num_workers)

        # for start, unis_per_worker in interval_split(num_workers, num_universities, threshold=10):
        for start in xrange(0, num_universities, UNIS_PER_WORKER):
            idx = start + index
            unis_per_worker = UNIS_PER_WORKER if (start + UNIS_PER_WORKER) < num_universities else num_universities - start

            self._log.info('run lubm generator [%s, %s]', idx, unis_per_worker)
            pool.apply_async(
                run_lubm_generator,
                (unis_per_worker, idx, generator_seed, self.ontology, self._output_path),
                callback=job_finished)

        pool.close()
        self._log.info('wait for work to finalize')
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


