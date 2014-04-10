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
    def __init__(self, precision=0):
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
            print 'rounding "%s" -> "%s"' % (ntfile, round_ntfile)
            with open(ntfile, 'r+') as NTFILE:
                with open(round_ntfile, 'w+') as ROUND_NTFILE:
                    for line in NTFILE:
                        try:
                            r_line = re.sub(self.numeric_pattern, repl, line)
                        except Exception, e:
                            print line
                            raise e
                        ROUND_NTFILE.write(r_line)

        except Exception:
            print '[fail]'
            print traceback.format_exc()
        else:
            print '[ok]'

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
