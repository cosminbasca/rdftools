from base import LubmGenerator
import numpy as np

__author__ = 'basca'

class LubmUni2Many(LubmGenerator):
    def __call__(self, p=None):
        if p is None:
            raise ValueError('p (the probability distribution) cannot be None')
        super(LubmUni2Many, self).__call__(p=p)

    def _create_distribution(self, universities_rdf, p=None):
        base_sites = np.random.random_integers(0, self._sites-1, len(universities_rdf))