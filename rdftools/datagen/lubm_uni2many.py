from base import LubmGenerator
import numpy as np

__author__ = 'basca'

DISTRIBUTIONS = {
    # 'd1': np.array([ 1.0/6.0, 2.0/3.0, 1.0/6.0 ]),
    'd1': np.array([1.0 / 4.0, 2.0 / 4.0, 1.0 / 4.0]),
    'd2': np.array([1.0 / 16, 3.0 / 16, 8.0 / 16, 3.0 / 16, 1.0 / 16]),
}

is_valid_distribution = lambda distro: np.sum(distro) == 0


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
        base_sites = np.random.random_integers(0, self._sites - 1, len(universities_rdf))
        sorted_p = np.sort(p)

