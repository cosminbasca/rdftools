#!/bin/sh
echo "-------------------------------------------------------------------------"
echo "-     BUILDING the EGG"
./dist.sh
echo "-------------------------------------------------------------------------"
echo "-     INSTALLING the EGG"
cd dist
easy_install $(find ./rdftools-*.egg -mtime -3)
echo "-     DONE"
echo "-------------------------------------------------------------------------"