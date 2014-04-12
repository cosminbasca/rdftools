from base import LubmGenerator
import numpy as np
import io
import sh

__author__ = 'basca'

DISTRIBUTIONS = {
    # one uni to 3 sites
    # '3S': np.array([1.0,
    #                   2.0,
    #                   1.0]) / 4.0,

    '3S': np.array([3.0,
                    10.0,
                    3.0]) / 16.0,

    # one uni to 5 sites
    '5S': np.array([1.0,
                    3.0,
                    8.0,
                    3.0,
                    1.0]) / 16.0,

    # one uni to 7 sites
    '7S': np.array([1.0,
                    3.0,
                    12.0,
                    32.0,
                    12.0,
                    3.0,
                    1.0]) / 64.0,

}

is_valid_distribution = lambda distro: np.sum(distro) == 1.0


class LubmUni2Many(LubmGenerator):
    def __call__(self, p=None):
        if p is None:
            raise ValueError('p (the probability distribution) cannot be None')
        if not is_valid_distribution(p):
            raise ValueError(
                'p (the probability distribution) is not valid, all values must sum up to 1. SUM(%s) = %s' % (
                    p, np.sum(p)))
        super(LubmUni2Many, self).__call__(p=p)

    def _create_distribution(self, universities_rdf, p=None):
        num_unis = len(universities_rdf)
        base_sites = np.random.random_integers(0, self._num_sites - 1, num_unis)
        print 'base sites = ', base_sites
        sorted_p = np.sort(p)
        num_extra_sites = len(sorted_p) - 1

        sites = np.arange(self._num_sites)

        uni_site_distros = [
            # get the disrtribution of sites for that uni, base_sites[i] = the base university
            [base_sites[i]] + list(
                np.random.choice(sites[sites != base_sites[i]], num_extra_sites, replace=False))
            for i in xrange(num_unis)
        ]

        # open the site files
        site_files = [io.open(self.site_path(i), mode='w+', buffering=1024 * 1024 * 16) for i in xrange(self.num_sites)]

        for i, uni_rdf in enumerate(universities_rdf):
            num_triples = long(sh.wc('-l', uni_rdf).strip().replace(uni_rdf, ''))
            print '[distributing] university %s to sites: %s, with %s triples' % (
                uni_rdf, uni_site_distros[i], num_triples)
            site_index = np.random.choice(uni_site_distros[i], num_triples, p=sorted_p)
            with io.open(uni_rdf, mode='r', buffering=1024 * 1024 * 16) as UNI:
                for j, triple in enumerate(UNI):
                    site = site_index[j]
                    site_files[site].write('%s' % triple)

        # close site files
        [site_rdf.close() for site_rdf in site_files]