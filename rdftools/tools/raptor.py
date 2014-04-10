import os
import sys
from multiprocessing import Pool
from rdftools.tools import RdfTool
from rdftools.rdfparse import convert_chunked
from rdftools.raptorutil import supported, get_parser_type, MB

__author__ = 'basca'


class RaptorRdf(RdfTool):
    parsers = [
        'rdfxml',
        'ntriples',
        'turtle',
        'trig',
        'guess',
        'rss-tag-soup',
        'rdfa',
        'nquads',
        'grddl'
    ]

    serializers = [
        'rdfxml',
        'rdfxml-abbrev',
        'turtle',
        'ntriples',
        'rss-1.0',
        'dot',
        'html',
        'json',
        'atom',
        'nquads'
    ]

    def _run(self, source, destination_format='ntriples', buffer_size=32, clear=False, verbose=False):
        buffer_size = buffer_size * MB
        files = []
        src = os.path.abspath(source)
        if os.path.isdir(src):
            files = [os.path.join(src, f) for f in os.listdir(src) if
                     supported(f) and get_parser_type(f) != destination_format]
        elif os.path.exists(src):
            files = [src]
        # print 'To process : ', files
        if clear:
            print 'will remove original files after conversion'

        def job_finished(res):
            print '.',
            sys.stdout.flush()
            pass

        pool = Pool()
        for src in files:
            pool.apply_async(convert_chunked, (src, destination_format, buffer_size, False),
                             callback=job_finished)

        pool.close()
        pool.join()

        if clear:
            [os.remove(f) for f in files]