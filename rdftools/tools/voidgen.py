#
# author: Cosmin Basca
#
# Copyright 2010 University of Zurich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import io
import os
import sys
from yaml import dump
from cybloom import ScalableBloomFilter
from collections import defaultdict
from rdftools.tools.base import ParserVisitorTool

__author__ = 'basca'

FP_ERR_RATE = 0.5
MIL = 1000000
INIT_CAPACITY_HIGH = 100 * MIL  # 100 million
INIT_CAPACITY_MED = 10 * MIL  # 10 million
INIT_CAPACITY_LOW = 10000  # 10K
INIT_CAPACITY_XTRA_LOW = 1000  # 10K

#-----------------------------------------------------------------------------------------------------------------------
#
# analyze void from file, returns a VoID dict stats
#
#-----------------------------------------------------------------------------------------------------------------------
class UniqueCounter(object):
    def __init__(self, init_capacity, err_rate=FP_ERR_RATE):
        self.unique_count = 0
        self.sbf = ScalableBloomFilter(init_capacity, err_rate)
        self._add = self.sbf.add

    def add(self, item):
        if not self._add(item):
            self.unique_count += 1


class PartitionCounter(object):
    def __init__(self, init_capacity, err_rate=FP_ERR_RATE):
        self.unique_counts = defaultdict(lambda: UniqueCounter(init_capacity, err_rate))

    def add(self, key, value):
        self.unique_counts[key].add(value)

    def counts(self):
        return dict([(k, uc.unique_count) for k, uc in self.unique_counts.items()])

    def __len__(self):
        return len(self.unique_counts)


class VoIDGen(ParserVisitorTool):
    def __init__(self, source_file, capacity_triples=INIT_CAPACITY_MED):
        super(VoIDGen, self).__init__(source_file, capacity_triples=capacity_triples)

        self.sbf_subjects = UniqueCounter(capacity_triples, FP_ERR_RATE)
        self.sbf_objects = UniqueCounter(capacity_triples, FP_ERR_RATE)
        self.part_classes = PartitionCounter(capacity_triples, FP_ERR_RATE)
        self.part_properties = PartitionCounter(capacity_triples, FP_ERR_RATE)
        self.t_count = 0

        # loop optimisations
        self.sbf_subjects_add = self.sbf_subjects.add
        self.sbf_objects_add = self.sbf_objects.add
        self.part_classes_add = self.part_classes.add
        self.part_properties_add = self.part_properties.add

        #TODO: some of these stats require a min sketch counter - not unique - implement this later...
        self.stats = {
            'properties': 0,
            'triples': 0,
            'objects': 0,
            'subjects': 0,
            'classes': 0,
            'doc_path': os.path.abspath(self.source_file),
            'partition_classes': None,
            'partition_properties': None,
        }

    @property
    def rdf_type(self):
        return 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'

    def on_visit(self, s, p, o, c):
        if self.t_count % 50000 == 0 and self.t_count > 0:
            self._log.info('[processed {0} triples]'.format(self.t_count))

        self.sbf_subjects_add(s)
        self.sbf_objects_add(o)
        if p == self.rdf_type:
            self.part_classes_add(o, '%s %s' % (s, p))
        self.part_properties_add(p, '%s %s' % (s, o))
        self.t_count += 1


    def get_results(self):
        self.stats['triples'] = self.t_count
        self.stats['properties'] = len(self.part_properties)
        self.stats['classes'] = len(self.part_classes)
        self.stats['subjects'] = self.sbf_subjects.unique_count
        self.stats['objects'] = self.sbf_objects.unique_count
        self.stats['partition_classes'] = self.part_classes.counts()
        self.stats['partition_properties'] = self.part_properties.counts()

        with io.open('%s.yaml' % self.source_file, 'w+') as OUT:
            dump(self.stats, OUT)

        return self.stats

