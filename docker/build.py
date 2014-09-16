#! ./python2.7_venv/bin/python

def load_yml():
    try:
        from yaml import load, dump
        from bunch import bunchify
        datafile = open("build.yml","r")
        data = load(datafile)
        return bunchify(data)
    except ImportError as e:
        print("Error loading file: " + str(e))
        os.exit(1)

def process_container(container, containerdetail):
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

    return {'global_flags': global_flags,
              'packages_use': packages_use,
              'packages_install': packages_install}

def parse_objectdata(dataobject):
    all_vars = {}
    for container, containerdetail in dataobject.containers.iteritems():
        try:
            single_vars = process_container(container,containerdetail)
            single_vars['metadata'] = dataobject.metadata
            all_vars[container] = single_vars
            print("Parsed " + container)
        except Exception as e:
            print(e.__class__.__name__+": "+ str(e))
    return all_vars
         
def main():
    import os
    from jinja2 import ChoiceLoader, PrefixLoader, FileSystemLoader, Environment

    print("Parsing configuration...")
    all_vars = parse_objectdata(load_yml())

    print("Rendering templates...")
    for container, single_vars in all_vars.iteritems():
        try:
            # Load jinja templates from container or default path
            default_template_loader = FileSystemLoader("templates")
            jinja_loader = ChoiceLoader([
                    default_template_loader, 
                    FileSystemLoader(container),
                    PrefixLoader({"!templates": default_template_loader})
                ])
            jinja_env = Environment(loader=jinja_loader,
                                    trim_blocks=True,
                                    lstrip_blocks=True)

            # Get the template and render it 
            tmpl_file = jinja_env.get_template('Dockerfile.jinja')
            rendered_file = tmpl_file.render(**single_vars)
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

main()
