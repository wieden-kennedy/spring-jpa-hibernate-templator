from os.path import join
from Generator import Generator
class PomGenerator(Generator):
    def __init__(self, template_dir, basepackage):
        Generator.__init__(self,None,None,None,None)
        self.basepackage = basepackage
        if not template_dir:
            self.template_path='./templates/pom/template.txt'
        else:
            self.template_path=join(template_dir,'template.txt')

    def set_group(self, group_id):
        self.group_id = group_id
    
    def set_artifact(self,artifact_id):
        self.artifact_id = artifact_id
    
    def set_package(self,package_name):
        self.package_name = package_name

    def generate_class(self):
        out_file=open(self.out_path,'w')
        for line in self.template_data:
            out_line = line
            out_line = out_line.replace('${groupId}',self.group_id)
            out_line = out_line.replace('${artifactId}',self.artifact_id)
            out_line = out_line.replace('${packageName}',self.package_name)

            out_file.write(out_line)

        out_file.close()

    def generate(self):
        self.template_data = self.get_template_data()
        self.set_out_path('./pom.xml')
        self.generate_class()