from Generator import Generator
from os.path import join,exists
from os import mkdir,chdir
from re import search

class ConfigGenerator(Generator):

    def generate_service_beans(self):
        serviceBeanTemplate = open(join(self.template_dir,'service_bean_template.txt'),'r')
        serviceBeanData = serviceBeanTemplate.readlines()
        serviceBeanTemplate.close()

        for model in self.models:
            model_name=model['model_name']
            for line in serviceBeanData:
                out_line = line
                out_line = out_line.replace('${model}',model_name[0].lower()+model_name[1:])
                out_line = out_line.replace('${Model}','%s%s' % (model_name[0].upper(),model_name[1:]))
                self.out_file.write(out_line)

    def generate_service_imports(self):
        for model in self.models:
            model_name = '%s%s' % (model['model_name'][0].upper(),model['model_name'][1:])
            self.out_file.write('import %s.service.%sService;\n' % (self.basepackage, model_name))
            self.out_file.write('import %s.service.%sServiceImpl;\n' % (self.basepackage, model_name))
    
    def generate_abstract_config(self):
        abstract_config_template=open(join(self.template_dir,'template.abstract.txt'),'r')
        abstract_config_template_data = abstract_config_template.readlines()
        abstract_config_template.close()

        out_file = open('./%s/%s/AbstractAppConfig.java' % (self.basepackage_path,self.type), 'w')

        for line in abstract_config_template_data:
            out_line = line
            out_line = out_line.replace('${basepackage}', self.basepackage)
            if search('#license',out_line):
                self.write_license(out_file)
            else:
                out_file.write(out_line)
        out_file.close()

    def generate_class(self):
        if not exists('./%s/%s' % (self.basepackage_path, self.type)):
            mkdir('./%s/%s' % (self.basepackage_path, self.type))

        if not exists('./%s/%s/AbstractAppConfig.java' % (self.basepackage_path,self.type)):
            self.generate_abstract_config()

        self.out_file = open(self.out_path, 'w')

        for line in self.template_data:
            out_line = line

            out_line = out_line.replace('${basepackage}', self.basepackage)
            out_line = out_line.replace('${propertiesFileName}', self.properties_file_name)
            out_line = out_line.replace('${additional_entity_packages}',',%s' % ','.join(self.packages_to_scan))

            if search('#serviceBeanDefs', out_line):
                self.generate_service_beans()

            elif search('#importService',out_line):
                self.generate_service_imports()

            elif search('#license',out_line):
                self.write_license()
                
            else:
                self.out_file.write(out_line)

        self.out_file.close()

    def set_models(self, models):
        self.models = models

    def set_properties_file(self,properties_file_name):
        self.properties_file_name = properties_file_name

    def set_additional_entity_packages(self,packages):
        self.packages_to_scan = []
        for package in packages:
            self.packages_to_scan.append('"%s"' % package)

    def generate(self):
        chdir(self.root_dir)
        chdir(self.java_source_dir)
        self.template_data = self.get_template_data()
        if not exists('./%s/%s' % (self.basepackage_path,self.type)):
            mkdir('./%s/%s' % (self.basepackage_path,self.type))
        self.set_out_path('./%s/%s/PersistenceConfig.java' % (self.basepackage_path,self.type))
        self.generate_class()