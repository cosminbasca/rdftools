rdftools
========

rdftools is a python wrapper over a number of RDF related tools
* rdf parsers / serializers
* void utilities
* lubm generator
* etc

Important Notes
---------------
This software is the product of research carried out at the [University of Zurich](http://www.ifi.uzh.ch/ddis.html) and comes with no warrenty whatsoever. Have fun!

TODO's
------
* The project is not documented (yet)

How to Compile the Project
--------------------------
Ensure that *libraptor2* v2.0.13+ and *cityhash* are installed on your system (either using the package manager of the OS or compiled from source).

To install **rdftools** you have two options: 1) manual installation (install requirements first) or 2) automatic with **pip**

Install the project manually from source (after downloading it locally):
```sh
$ python setup.py install
```

Install the project with pip:
```sh
$ pip install https://github.com/cosminbasca/rdftools
```

Also have a look at the build.sh, clean.sh, test.sh scripts included in the codebase 

Thanks a lot to
---------------
* [University of Zurich](http://www.ifi.uzh.ch/ddis.html) and the [Swiss National Science Foundation](http://www.snf.ch/en/Pages/default.aspx) for generously funding the research that led to this software.
