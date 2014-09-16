#! ./python2.7_venv/bin/python

from yaml import load, dump
from bunch import bunchify

dataobject = None

try:
    datafile = open("build.yml","r")
    data = load(datafile)

    dataobject = bunchify(data)

except ImportError as e:
    print("Error loading file: " + str(e))

  

if dataobject != None:
    import os
    from jinja2 import FileSystemLoader, Environment

    # Load jinja
    jinja_loader = FileSystemLoader("templates")
    jinja_env = Environment(loader=jinja_loader,
                            trim_blocks=True,
                            lstrip_blocks=True)
    myvars = {'metadata': dataobject.metadata,
              'container': dataobject.containers.nova}

    # Get the template and render it using `myvars`
    tmpl_file = jinja_env.get_template('Dockerfile.jinja')
    rendered_file = tmpl_file.render(**myvars)
     
     # To write to another file, use `file`
    out_file = file('Dockerfile','w')
    out_file.write(rendered_file)
    out_file.close()
