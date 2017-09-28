#!/bin/sh

DTD=$1
ORIG_DBLP=$2
TO_DBLP=$3


if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    exit 1
fi

echo Reading DTD from $DTD
#if [ ! -e $DTD ]; then
#   echo "Cannot find DTD"
#   exit 1
#fi

#(gunzip -dc $ORIG_DBLP | grep -v "!DOCTYPE" |  xmllint --dtdvalid $DTD --dtdattr --noent -) > $TO_DBLP 2> dblp.err
(gunzip -dc $ORIG_DBLP | xmllint --loaddtd --dtdattr --noent --path $DTD - | gzip -c -) > $TO_DBLP 2> dblp.err
