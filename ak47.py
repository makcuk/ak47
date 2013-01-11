import yaml
from os.path import basename, abspath, exists
from mako.template import Template

TemplatesDir = 'templates/'
File = 'ak47.yaml'

def log(self, msg):
    print msg

class AK47(object):
    def __init__(self, config_yaml, templates_dir):
        self.templates_dir = templates_dir
        self.config_yaml = config_yaml

    def exec_service_cmd(self, cmd):
        print cmd


    def fire(self):
        with open(self.config_yaml) as values:
            config = yaml.load(values)

            for tpl in config.keys():
                tpl_path = basename(tpl)
                if not exists(self.templates_dir+tpl_path):
                    log("Template %s not exist" % (tpl_path))
                else:
                    slot = config[tpl]
                    for item in slot:
                        out = Template(filename = self.templates_dir+tpl_path)
                        section = slot[item]
                        if item in ('post-action'):
                           service_cmd = slot[item]
                        else:
                            section['section_name'] = item
                            print out.render(**section)
                    self.exec_service_cmd(service_cmd)

if __name__ == '__main__':
    AK47(File, TemplatesDir).fire()

