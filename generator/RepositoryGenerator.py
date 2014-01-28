from Generator import Generator
from os.path import exists, join
from os import mkdir
from re import search

class RepositoryGenerator(Generator):

    def generate_abstract_repository(self):
        abstract_repository_template = open(join(self.template_dir,'template.abstract.txt'),'r')
        abstract_repository_template_data = abstract_repository_template.readlines()
        abstract_repository_template.close()

        out_file = open('./%s/%s/ModelRepository.java' % (self.basepackage_path,self.type), 'w')

        for line in abstract_repository_template_data:
            out_line = line
            out_line = out_line.replace('${basepackage}',self.basepackage)
            if search('#license',out_line):
                self.write_license(out_file)
            else:
                out_file.write(out_line)

        out_file.close()

    def generate_class(self):
        if not exists('./%s/%s/ModelRepository.java' %(self.basepackage_path,self.type)):
            self.generate_abstract_repository()

        model_name = self.model['model_name']

        if not exists('./%s/%s' % (self.basepackage_path,self.type)):
            mkdir('./%s/%s' % (self.basepackage_path,self.type))

        self.out_file = open('./%s/%s/%sRepository.java' % (self.basepackage_path,self.type,model_name), 'w')

        for line in self.template_data:
            out_line = line

            out_line = out_line.replace('${basepackage}', self.basepackage)
            out_line = out_line.replace('${model}', model_name.lower())
            out_line = out_line.replace('${Model}', model_name)
            out_line = out_line.replace('${T}', model_name)
            out_line = out_line.replace('${ID}', self.model['id_type'])
            
            if search('#additional_methods',out_line):
                if self.model['additional_query_methods']:
                    for method in self.model['additional_query_methods']:
                        query = '@Query("%s")' % method['query']
                        params = ''

                        for param in method['params']:
                            params += '@Param("%s") %s %s, ' % (param['name'],param['type'],param['name'])

                        m = 'public %s %s(%s);' % (method['returns'],method['name'],params[:-2])
                        self.out_file.write('\t%s\n\t%s\n\n' % (query,m))

            elif search('#license',out_line):
                self.write_license()
            
            else:
                self.out_file.write(out_line)

        self.out_file.close()