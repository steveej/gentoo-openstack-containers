#!/bin/bash
VENV="python2.7_venv"

if [[ ! -d $VENV ]]; then
	virtualenv -p python2.7 $VENV
	source $VENV/bin/activate
	pip install -r requirements.txt
fi

echo "Now run 'source ${VENV}/bin/activate'"
