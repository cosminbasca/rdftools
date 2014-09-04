from base import LubmGenerator

__author__ = 'basca'

"""
distribution process:

1) randoly distribute a seed of resources to hosts,
2) propagate from that point on (keep seed specific stuff on the same host)
"""
class LubmSeedPropagation(LubmGenerator):
    def _create_distribution(self, universities_rdf, **kwargs):
        #TODO: implement me!
        raise NotImplementedError