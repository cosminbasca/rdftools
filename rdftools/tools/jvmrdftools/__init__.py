import os
import signal
from subprocess import Popen, PIPE, STDOUT, call
from threading import Thread
from natsort import natsorted

__author__ = 'basca'

__LIB_NAME__ = 'jvmrdftools-assembly-'

__LIB__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
__JARS__ = natsorted([(jar.replace(__LIB_NAME__, "").replace(".jar", ""),
                       os.path.join(__LIB__, jar))
                      for jar in os.listdir(__LIB__) if jar.startswith(__LIB_NAME__)],
                     key=lambda (ver, jar_file): ver)


def latest_jar():
    global __JARS__
    return __JARS__[-1]


class JavaNotFoundException(Exception):
    pass


DEVNULL = open(os.devnull, 'w')

XMS = 128
XMX = 2048

def check_java(message=""):
    if call(['java', '-version'], stderr=DEVNULL) != 0:
        raise JavaNotFoundException(
            'Java is not installed in the system path. {0}'.format(message))


def run_tool(main_class, xms=XMS, xmx=XMX, *options):
    latest_version, jar_path = latest_jar()
    command = ["java", "-Xms{0}m".format(xms), "-Xmx{0}m".format(xmx), "-classpath", jar_path, main_class] + \
              [str(opt) for opt in options]
    # call(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT, preexec_fn=os.setsid)
    call(command)


# ----------------------------------------------------------------------------------------------------------------------
#
# the specific tools
#
# ----------------------------------------------------------------------------------------------------------------------
def run_lubm_generator(num_universities, index, generator_seed, ontology, output_path, xms=XMS, xmx=XMX):
    run_tool("com.rdftools.LubmGenerator",
             xms, xmx,
             "--num_universities", num_universities,
             "--start_index", index,
             "--seed", generator_seed,
             "--ontology", ontology,
             "--output_path", output_path)


def run_nxvoid_generator(source, dataset_id, output_path, xms=XMS, xmx=XMX):
    run_tool("com.rdftools.NxVoidGenerator",
             xms, xmx,
             "--source", source,
             "--dataset_id", dataset_id,
             "--output_path", output_path)


def run_jvmvoid_generator(source, dataset_id, output_path, xms=XMS, xmx=XMX):
    run_tool("com.rdftools.VoIDGenerator",
             xms, xmx,
             "--source", source,
             "--dataset_id", dataset_id,
             "--output_path", output_path)


def run_rdf2rdf_converter(source, destination, xms=XMS, xmx=XMX):
    run_tool("com.rdftools.Rdf2RdfConverter",
             xms, xmx,
             source, destination)