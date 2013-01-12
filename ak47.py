import yaml
import optparse
import subprocess
from os.path import basename, abspath, exists
from mako.template import Template
from tempfile import NamedTemporaryFile
from shutil import copy2, move


TemplatesDir = 'templates/'
Config = 'ak47.yaml'

def log(msg):
    print msg

class AK47(object):
    def __init__(self, config_yaml, templates_dir):
        self.templates_dir = templates_dir
        self.config_yaml = config_yaml
        self.protect = True

    @property
    def protector(self):
        return self.protect

    @protector.setter
    def protector(self, value):
        self.protect = value

    def exec_service_cmd(self, cmd):
        retcode = subprocess.call(cmd)
        if retcode > 0:
            log('Command "%s" returned non-zero: %d' % (cmd, retcode))

    def write_file_safe(self, dst, buffer):
        with NamedTemporaryFile(delete = False) as out:
            out.write(buffer)
            src = out.name
        if exists(dst):
            bkp = dst+'.ak47save'
            move(dst, bkp)
        move(src, dst)

    def fire(self):
        with open(self.config_yaml) as values:
            config = yaml.load(values)

            for tpl in config.keys():
                tpl_path = basename(tpl)
                buffer = ''
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
                            buffer += out.render(**section)
                    self.write_file_safe(tpl, buffer)
                    self.exec_service_cmd(service_cmd)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-p', action = 'store_true', dest = 'protector', default = False, help = 'Switch off protector and let AK47 modify files')
    parser.add_option('-r', action = 'store_true', dest = 'run', default = False, help = 'Run process')
    opts, args = parser.parse_args()

    if opts.run:
        ak47loaded = AK47(Config, TemplatesDir)
        if opts.protector:
            ak47loaded.protector = not opts.protector
        ak47loaded.fire()
    else:
        parser.print_help()

