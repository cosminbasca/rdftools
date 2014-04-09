from base import LubmGenerator
import numpy as np
import io

__author__ = 'basca'


class LubmUni2One(LubmGenerator):
    def _create_distribution(self, universities_rdf):
        sites_index = np.random.random_integers(0, self._sites, len(universities_rdf))
        for i in xrange(self._sites):
            unis = sites_index[sites_index==i]
            if unis.size > 0:
                with io.open('site_%s.nt', mode='w+', buffering=1024*1024*16) as SITE:
                    for uni_rdf in [universities_rdf[idx] for idx in unis]:
                        with io.open(uni_rdf, mode='r', buffering=1024*1024*16) as UNI:
                            triples = UNI.read()
                        SITE.write(triples)

