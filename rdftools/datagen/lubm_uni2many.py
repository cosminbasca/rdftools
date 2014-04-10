from base import LubmGenerator
import numpy as np

__author__ = 'basca'

def weighted_values(values, probabilities, size):
    bins = np.add.accumulate(probabilities)
    return values[np.digitize(np.random.random_sample(size), bins)]

class LubmUni2Many(LubmGenerator):
    def _create_distribution(self, universities_rdf):
        np.random.random_integers(0, self._sites-1, len(universities_rdf))