import argparse
from py4j.java_gateway import JavaGateway
from rdftools.nxparser import BUNDLED_NXPARSER_JAR

__author__ = 'basca'

def gen_void(jvm, data, dataset_id):
    print 'get VoiD object...'
    statsEngine = jvm.org.semanticweb.yars.stats.VoiD()
    assert data is not None, 'data input file must be present'

    print 'get input'
    _input  = jvm.java.io.FileInputStream(data)
    print 'get output'
    _output = jvm.java.io.FileOutputStream('%s.void.xml'%data)

    print 'gen void'
    statsEngine.analyseVoid(_input,dataset_id,_output)

#noinspection PyBroadException
def main():
    """
    usage: genvoid.py [-h] [--data DATA] [--dataset_id DATASET_ID]

generate a VoiD descriptor using the nxparser java package

optional arguments:
  -h, --help            show this help message and exit
  --data DATA           the input data file to pass the NX void generator
  --dataset_id DATASET_ID
                        dataset id
    """
    parser = argparse.ArgumentParser(description='generate a VoiD descriptor using the nxparser java package')

    parser.add_argument('--data', dest='data', action='store', type=str, default = None,
                       help='the input data file to pass the NX void generator')
    parser.add_argument('--dataset_id', dest='dataset_id', action='store', type=str, default = None,
                       help='dataset id')

    args = parser.parse_args()
    print 'start java gateway...'
    gateway = JavaGateway.launch_gateway(classpath='.:%s'%BUNDLED_NXPARSER_JAR)
    jvm = gateway.jvm
    gen_void(jvm, args.data, args.dataset_id)
    print 'done'

if __name__ == '__main__':
    main()
