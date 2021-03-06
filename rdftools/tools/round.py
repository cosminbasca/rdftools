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
import re
import traceback
import os
from multiprocessing import Pool
from rdftools.util import log_time
from rdftools.tools import RdfTool

__author__ = 'basca'


def round_file(nt_file, rounded_nt_file, prec):
    ntfloat_rounder = NtFloatRounder(precision=prec)
    ntfloat_rounder.round_file(nt_file, rounded_nt_file)


class NtFloatRounder(RdfTool):
    def __init__(self, precision=0, *args, **kwargs):
        super(NtFloatRounder, self).__init__(*args, **kwargs)
        self._round_pattern = '"%.' + str(precision) + 'f"' if precision > 0 else '"%d"'
        self._numeric_pattern = re.compile('"-?(0\.\d*[1-9]\d*|[1-9]\d*(\.\d+)?)"')

    @property
    def numeric_pattern(self):
        return self._numeric_pattern

    @property
    def round_pattern(self):
        return self._round_pattern

    # noinspection PyBroadException
    def round_file(self, ntfile, round_ntfile):
        def repl(val):
            return self._round_pattern % float(val.group(0)[1:-1])

        try:
            self._log.info('rounding "{0}" -> "{1}"'.format(ntfile, round_ntfile))
            with open(ntfile, 'r+') as NTFILE:
                with open(round_ntfile, 'w+') as ROUND_NTFILE:
                    for line in NTFILE:
                        try:
                            r_line = re.sub(self.numeric_pattern, repl, line)
                        except Exception, e:
                            self._log.error('line: {0}'.format(line))
                            raise e
                        ROUND_NTFILE.write(r_line)

        except Exception:
            self._log.error('[fail] traceback: \n{0}'.format(traceback.format_exc()))
        else:
            self._log.info('[ok]')

    def _run(self, path, prefix='rounded', precision=0):
        """
        parallel rounding of ntriples files in given path
        :param path: the ntriple files location
        :param prefix: the prefix used for files that are transformed, cannot be the enpty string
        :param precision: the desired precision (0 decimals is default)
        :return: None
        """
        if os.path.isdir(path):
            data_files = [(os.path.join(path, dfile), os.path.join(path, '%s_%s' % (prefix, dfile)))
                          for dfile in os.listdir(path)
                          if not dfile.startswith('.') and os.path.splitext(dfile)[1] == ".nt"]
        else:
            base, name = os.path.split(path)
            data_files = [(os.path.join(base, name), os.path.join(base, '%s_%s' % (prefix, name)))]

        pool = Pool()
        for ntfile, round_ntfile in data_files:
            pool.apply_async(round_file, (ntfile, round_ntfile, precision))
        pool.close()
        pool.join()
