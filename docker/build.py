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

    for container, containerdetail in dataobject.containers.iteritems():
        print("Processing "+container+"...")
        global_flags = []
        if hasattr(containerdetail, "use"):
            for sign, uselist in containerdetail.use.iteritems():
                for use in uselist:
                    global_flags.append(sign+'use::'+use)
                
        packages_install = ""
        packages_use = {}
        for package, packagedetail in containerdetail.packages.iteritems():
            # Generate package atom with version
            if hasattr(packagedetail, "version"):
                packagedetail.atom = '='+package+'-'+packagedetail.version
            else:
                packagedetail.atom = package

            # Collect to be installed packages
            if packagedetail.install == True:
                packages_install += packagedetail.atom+' '

            # Collect package specific use flags
            if hasattr(packagedetail, "use"):
                packages_use[packagedetail.atom] = ""
                for sign, uselist in packagedetail.use.iteritems():
                    for use in uselist:
                        packages_use[packagedetail.atom] += sign+'use::'+use+' '

        thevars = {'metadata': dataobject.metadata,
                  'container': dataobject.containers.nova,
                  'global_flags': global_flags,
                  'packages_use': packages_use,
                  'packages_install': packages_install}

        # Get the template and render it using `myvars`
        try:
            tmpl_file = jinja_env.get_template('Dockerfile.'+container+'.jinja')
            rendered_file = tmpl_file.render(**thevars)

            # To write to another file, use `file`
            if not os.path.exists(container):
                os.makedirs(container)
            out_file_path=container+'/Dockerfile'
            out_file = file(out_file_path,'w')
            out_file.write(rendered_file)
            out_file.close()
            print(out_file_path + " written.")
        except Exception as e:
            print(e.__class__.__name__+": "+ str(e))

         
