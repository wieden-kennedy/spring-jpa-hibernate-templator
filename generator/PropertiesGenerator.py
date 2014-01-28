from Generator import Generator
from os.path import exists,join
from os import mkdir

class PropertiesGenerator(Generator):
    
    def generate_properties_file(self):
        application_properties = open(self.template_path,'r')
        application_properties_data = application_properties.readlines()
        application_properties.close()

        self.out_file=open(self.out_path, 'w')
        for line in application_properties_data:
            out_line = line
            out_line = out_line.replace('${database_username}',self.properties['database_username'])
            out_line = out_line.replace('${database_password}',self.properties['database_password'])
            out_line = out_line.replace('${database_url}',self.properties['database_url'])
            out_line = out_line.replace('${database_databasename}',self.properties['database_databasename'])
            out_line = out_line.replace('${basepackage}', self.basepackage)
            out_line = out_line.replace('${database_flavor}', self.properties['database_flavor'])
            out_line = out_line.replace('${hibernate_dialect}', self.properties['hibernate_dialect'])

            self.out_file.write(out_line)
        self.out_file.close()

    def generate(self):
        if not exists(join(self.root_dir,'src/resources')):
            mkdir(join(self.root_dir,'src/resources'))
        self.out_path = join(join(self.root_dir,'src/resources'),'application.properties')
        self.generate_properties_file()

    def set_properties(self,properties):
        self.properties = properties

