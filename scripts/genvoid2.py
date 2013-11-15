import argparse
from pprint import pprint
import shutil
from py4j.java_gateway import JavaGateway

__author__ = 'basca'

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
    gateway = JavaGateway.launch_gateway(classpath='.:/Users/basca/env/opt/jvm/jars/nxparser-1.2.3.jar')
    jvm = gateway.jvm
    print 'get VoiD object...'
    statsEngine = jvm.org.semanticweb.yars.stats.VoiD()
    assert args.data is not None, 'data input file must be present'

    print 'get input'
    _input  = jvm.java.io.FileInputStream(args.data)
    print 'get output'
    _output = jvm.java.io.FileOutputStream('%s.void.xml'%args.data)

    print 'gen void'
    statsEngine.analyseVoid(_input,args.dataset_id,_output)
    print 'done'

if __name__ == '__main__':
    main()
