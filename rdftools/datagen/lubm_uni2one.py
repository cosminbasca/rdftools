from base import LubmGenerator
import numpy as np
import io

__author__ = 'basca'


class LubmUni2One(LubmGenerator):
    def _create_distribution(self, universities_rdf):
        sites_index = np.random.random_integers(0, self._sites-1, len(universities_rdf))
        print 'site index = ', sites_index
        for i in xrange(self._sites):
            unis = np.where(sites_index == i)
            print 'site %s'%i
            print '\tunis = ',unis
            if unis.size > 0:
                with io.open(self.site_path(i), mode='w+') as SITE:
                    for uni_rdf in [universities_rdf[idx] for idx in unis]:
                        with io.open(uni_rdf, mode='r') as UNI:
                            SITE.write(UNI.read())

