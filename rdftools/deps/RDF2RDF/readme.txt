http://www.l3s.de/~minack/rdf2rdf/

RDF2RDF

This Java tool converts your RDF files from any format to any format. It is wrapped into one single jar file for easy usage.

Download:
Latest version at rdf2rdf-1.0.1-2.3.1.jar [329 kByte].

License
This tool is licensed under GPL v2.0

Usage:
Run the jar file like this: java -jar rdf2rdf-1.0.1-2.3.1.jar INPUTFILE(S) OUTPUTFILE

Examples:
command	input file(s)	output file (format)	description
java -jar rdf2rdf-1.0.1-2.3.1.jar	test.rdf	test.nt	converts RDF/XML into NTRIPLES
test.rdf.gz	.nt	converts gzipped input file into unzipped NTRIPLES file test.nt
test1.rdf test2.n3	.nt	converts input files into NTRIPLES, here into test1.nt and test2.nt, respectively
test1.rdf test2.n3	test.nt	converts input files into NTRIPLES, concatenated into test.nt
test1.rdf test2.n3	-.nt	converts input files into NTRIPLES, streamed to STDOUT
-.rdf	-.nt	converts STDIN from RDF/XML into NTRIPLES, streamed to STDOUT
-.rdf.gz	-.nt.gz	converts gzipped RDF/XML from STDIN into gzipped NTRIPLES, streamed to STDOUT

Supported extensions
rdf, rdfs, owl, xml	RDF/XML
nt	N-Triples
ttl	Turtle
n3	N3
trig, xml	TriX
trig	TriG

RDF2RDF uses OpenRDF RIO 2.3.1 to convert formats. Please read their LICENSE!

07.05.2010 - Enrico Minack

