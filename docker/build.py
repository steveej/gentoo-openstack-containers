#! ./python2.7_venv/bin/python

import traceback, sys, copy
from yaml import load, dump
from string import Template

def load_yml(filename):
    try:
        datafile = open(filename, "r")
        data = load(datafile)
        return data
    except ImportError as e:
        print("Error loading file: " + str(e))
        os.exit(1)

def deepupdate(original, update):
    """
    Recursively update a dict.
    Subdict's won't be overwritten but also updated.
    """
    for key, value in original.iteritems(): 
        if not key in update:
            update[key] = value
        elif isinstance(value, dict):
            deepupdate(value, update[key]) 
        else:
            print("Key %s in update but is no dict") % key
    return update

class YamlFilter:

    def __init__(self, data, gentoo_scheme):
        self._data = data
        self._gentoo_scheme = gentoo_scheme
        self._gentoo_data = None
        self._fig_data = None

    @property
    def fig_data(self):
        self._fig_data = copy.deepcopy(self._data)

        default = {}
        if "default" in self._fig_data:
            print("Found default section")
            default = copy.deepcopy(self._fig_data["default"])
            for def_key, def_value in self._fig_data["default"].iteritems():
                if def_key in self._gentoo_scheme["default"]:
                    del default[def_key]
            del self._fig_data["default"]

        for key, value in copy.deepcopy(self._fig_data).iteritems():
            for container_key, container_value in value.iteritems():
                if container_key in self._gentoo_scheme["default"]:
                    print("Deleting option %(1)s from container %(2)s") % {"1": container_key, "2": key}
                    del self._fig_data[key][container_key]
            self._fig_data[key] = deepupdate(copy.deepcopy(default), self._fig_data[key]) 
            if "build" not in self._fig_data[key]:
                self._fig_data[key]["build"] = key

        return self._fig_data

    @property
    def gentoo_data(self):
        self._gentoo_data = copy.deepcopy(self._data)

#        default={}
#            del self._gentoo_data["default"]
#            for key in self._gentoo_scheme["default"].keys()+self._gentoo_scheme["required"].keys():
#                if key not in tupel[0]:
#                    del self._gentoo_data["default"][def_key]
#        if "default" in self._gentoo_data:
#            print("Found default section")
#            default = self._gentoo_data["default"].copy()

        paths_to_default = []
        cur_path = []
        it = self._gentoo_data.iteritems()
        it_stack = [it]
        while(len(it_stack) > 0):
            tup = next(it_stack[-1], False)
            while(tup):
                depth = len(it_stack)-1
                if isinstance(tup[1], type(dict())):
                    it_stack.append(tup[1].iteritems())
                    cur_path.append(tup[0])
                    if tup[0] == "default":
                        print("Found default key in dictionary with depth %s and path %s") % (depth, cur_path)
                        paths_to_default.append(copy.deepcopy(cur_path))
                tup = next(it_stack[-1], False)
            it_stack.pop()

        for path in paths_to_default:
            cur_data = self._gentoo_data
            cur_scheme = self._gentoo_scheme
            keyword = path.pop()
            for key in path:
                print("Recursing into %s") % key
                cur_data = cur_data[key]
                cur_scheme = cur_scheme[key]
            print("Current path is %s") % path
            overlap_keys = [overlap_key for overlap_key in set(cur_data["default"].keys())-set(cur_scheme["default"].keys())]
            if len(overlap_keys) > 0:
                print("Warning: overlapping keys not specified in scheme: %s") % overlap_keys
            for overlap_key in overlap_keys:
                del cur_data["default"][overlap_key]
            missing_keys = [missing_key for missing_key in set(cur_scheme["default"].keys())-set(cur_data["default"].keys())]
            if len(missing_keys) > 0:
                print("Info: missing keys filled in from scheme: %s") % missing_keys
                deepupdate(cur_scheme["default"], cur_data["default"])
        
        print(dump(self._gentoo_data))
                
#        for key, value in copy.deepcopy(self._gentoo_data).iteritems():
#            for container_key, container_value in value.iteritems():
#                if container_key not in self._gentoo_scheme["default"].keys()+self._gentoo_scheme["required"].keys():
#                    print("Deleting option %(1)s from container %(2)s") % {"1": container_key, "2": key}
#                    del self._gentoo_data[key][container_key]
#            self._gentoo_data[key] = deepupdate(copy.deepcopy(default), self._gentoo_data[key]) 
#
#            for rkey, rvalue in self._gentoo_scheme["required"].iteritems():
#                if rkey not in self._gentoo_data[key]: 
#                    raise Exception("Required key '"+rkey+"' not specified for '"+key+"'")
#                else:
#                    want_type = type(rvalue) 
#                    got_type = type(self._gentoo_data[key][rkey])
#                    if want_type != got_type:
#                        raise Exception("Wrong type specified for '"+rkey+"' for '"+key+"': " 
#                                        + str(got_type) + " want: " + str(want_type))
        
        #print(dump(self._gentoo_data))
        return self._gentoo_data


def process_gentoo(yaml, scheme):
    template_data = copy.deepcopy(yaml)

    for container, container_values in yaml.iteritems():
        template_data[container]["cmds"] = []
        for containerkey, containervalue in container_values.iteritems():
            template_data[container]["cmds"] = []
#            for sign, uselist in container_values["use"].iteritems():
#                for use in uselist:
#                    substmap = {"sign": sign, "use": use}
#                    template = Template(scheme["commands"]["packages"]["use"][sign])
#                    cmd = template.substitute(substmap)
#                    cmd("Adding command to %s: %s") (cmd, container)
#                    template_data[container]["cmds"].append(cmd)
#            for package, packagedetails in container_values["packages"].iteritems():
#                atom = package
#                if packagedetails["version"]:
#                    atom = "=%s-%s" % (package, packagedetails["version"])
#                for use, uselist in packagedetails["use"].iteritems():
#                    substmap = {"sign": sign, "use": use, "atom": atom}
#                    template = Template(scheme["commands"]["packages"]["package"]["use"][sign])
#                    cmd = template.substitute(substmap)
#                    template_data[container]["cmds"].append(cmd)
#
#                if packagedetails["install"]:
#                    template = Template(scheme["commands"]["packages"]["package"]["install"])
#                    cmd = template.substitute(substmap)
#                    template_data[container]["cmds"].append(cmd)
    return template_data
        

#class Generator():
#    import os
#    from jinja2 import ChoiceLoader, PrefixLoader, FileSystemLoader, Environment
#
#    def do_dockerfiles():
#        for container, single_vars in all_vars.iteritems():
#            try:
#                # Load jinja templates from container or default path
#                default_template_loader = FileSystemLoader("templates")
#                jinja_loader = ChoiceLoader([
#                        FileSystemLoader(container),
#                        default_template_loader, 
#                        PrefixLoader({"!templates": default_template_loader})
#                    ])
#                jinja_env = Environment(loader=jinja_loader,
#                                        trim_blocks=True,
#                                        lstrip_blocks=True)
#
#                # Get the template and render it 
#                tmpl_file = jinja_env.get_template('Dockerfile.jinja')
#                rendered_file = tmpl_file.render(**single_vars)
#                # To write to another file, use `file`
#                if not os.path.exists(container):
#                    os.makedirs(container)
#                out_file_path=container+'/Dockerfile'
#                out_file = file(out_file_path,'w')
#                out_file.write(rendered_file)
#                out_file.close()
#                print(out_file_path + " written.")
#            except Exception as e:
#                exc_type, exc_value, exc_traceback = sys.exc_info()
#                traceback.print_exception(exc_type, exc_value, exc_traceback,
#                                              limit=2, file=sys.stdout)
#                print(e.__class__.__name__+": "+ str(e))

def main():
    yml = load_yml("build.yml")
    yml_gentoo_scheme = load_yml("gentoo_scheme.yml")
    yaml_filter = YamlFilter(yml, yml_gentoo_scheme)

    fig_yml = dump(yaml_filter.fig_data)
    fig_yml_file = open("fig.yml","w")
    fig_yml_file.write(fig_yml)
    fig_yml_file.close()

    gentoo_data = yaml_filter.gentoo_data
    gentoo_yml = dump(gentoo_data)
    gentoo_yml_file = open("gentoo.yml","w")
    gentoo_yml_file.write(gentoo_yml)
    gentoo_yml_file.close()

    gentoo_prepared = process_gentoo(gentoo_data, yml_gentoo_scheme)
#    generator.render_gentoo_dockerfiles(gentoo_prepared)

if __name__ == "__main__":
    main()
