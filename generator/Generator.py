from os import chdir,mkdir
from os.path import join,exists

class Generator:
    def __init__(self,generator_type,root_dir,basepackage,java_source_dir,model=None):
        if generator_type:
            self.type=generator_type
        if root_dir:
            self.root_dir=root_dir
        if basepackage:
            self.basepackage = basepackage
            self.basepackage_path=basepackage.replace('.','/')
        if root_dir and generator_type:
            self.template_dir=join(join(self.root_dir,'templates'),self.type)
            self.template_path=join(self.template_dir,'template.txt')
        if java_source_dir:
            self.java_source_dir = java_source_dir
        if model:
            self.model = model

    def generate_class():
        pass

    def get_template_data(self):
        f=open(self.template_path,'r')
        template_data = f.readlines()
        f.close()
        return template_data

    def set_generator_type(self,generator_type):
        self.type=generator_type

    def set_out_path(self,path):
        self.out_path=path

    def set_template_dir(self,dir_path):
        self.template_dir=dir_path

    def set_licensing(self,license_text_path):
        self.licensing_path = license_text_path

    def write_license(self,out_file=None):
        if not out_file:
            out_file = self.out_file
        if hasattr(self,'licensing_path'):
            license_file = open(self.licensing_path,'r')
            license_data = license_file.readlines()
            license_file.close()
            for line in license_data:
                out_file.write(line)

    def generate(self):
        chdir(self.root_dir)
        chdir(self.java_source_dir)
        self.template_data = self.get_template_data()
        if not exists('./%s/%s' % (self.basepackage_path,self.type)):
            mkdir('./%s/%s' % (self.basepackage_path,self.type))
        self.set_out_path('./%s/%s/%s.java' % (self.basepackage_path,self.type,self.model['model_name']))
        self.generate_class()