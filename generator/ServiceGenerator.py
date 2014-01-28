from Generator import Generator
from os.path import exists,join
from os import mkdir,chdir
from re import search

class ServiceGenerator(Generator):
    
    def generate_base_service_class(self):
        baseServiceClassTemplate = open(join(self.template_dir,'template.abstract.txt'),'r')
        baseServiceClassData = baseServiceClassTemplate.readlines()
        baseServiceClassTemplate.close()

        out_file = open('./%s/%s/ModelService.java' % (self.basepackage_path,self.type), 'w')

        for line in baseServiceClassData:
            out_line = line
            out_line = out_line.replace('${basepackage}',self.basepackage)
            if search('#license',out_line):
                self.write_license(out_file)
            else:
                out_file.write(out_line)

        out_file.close()

    def generate_class(self):
        model_name=self.model['model_name']

        if not exists('./%s/%s' % (self.basepackage_path,self.type)):
            mkdir('./%s/%s' % (self.basepackage_path,self.type))

        if not exists('./%s/%s/ModelService.java' % (self.basepackage_path,self.type)):
            self.generate_base_service_class()

        self.out_file = open('./%s/%s/%sService.java' % (self.basepackage_path,self.type,model_name), 'w')

        for line in self.template_data:
            out_line = line

            out_line = out_line.replace('${basepackage}', self.basepackage)
            out_line = out_line.replace('${model}', model_name.lower())
            out_line = out_line.replace('${Model}', model_name)
            out_line = out_line.replace('${T}', model_name)
            out_line = out_line.replace('${t}', model_name.lower())
            out_line = out_line.replace('${ID}', self.model['id_type'])
            out_line = out_line.replace('${Serializable}', self.model['id_type'])

            if search('#license',out_line):
                self.write_license()
            else:
                self.out_file.write(out_line)

        self.out_file.close()

        self.generate_impl_class()

    def generate_impl_class(self):
        serviceImplTemplate = open(join(self.template_dir,'template.impl.txt'),'r')
        serviceImplTemplateData = serviceImplTemplate.readlines()
        serviceImplTemplate.close()

        model_name = self.model['model_name']

        if not exists('./%s/%s' % (self.basepackage_path,self.type)):
            mkdir('./%s/%s' % (self.basepackage_path,self.type))

        out_file = open('./%s/%s/%sServiceImpl.java' % (self.basepackage_path,self.type,model_name), 'w')

        for line in serviceImplTemplateData:
            out_line = line

            out_line = out_line.replace('${basepackage}', self.basepackage)
            out_line = out_line.replace('${model}', model_name.lower())
            out_line = out_line.replace('${Model}', model_name)
            out_line = out_line.replace('${T}', model_name)
            out_line = out_line.replace('${t}', model_name.lower())
            out_line = out_line.replace('${ID}', self.model['id_type'])
            out_line = out_line.replace('${Serializable}', self.model['id_type'])

            if search('#additional_methods',out_line):
                if self.model['additional_query_methods']:
                    for method in self.model['additional_query_methods']:
                        params = ''
                        args = ''
                        for param in method['params']:
                            params += '%s %s, ' % (param['type'],param['name'])
                            args += '%s, ' % param['name']
                        out_file.write('\tpublic %s %s(%s){\n\t\treturn this.%s%sRepository.%s(%s);\n\t}\n\n' % (method['returns'],method['name'],params[:-2],model_name[0].lower(),model_name[1:],method['name'],args[:-2]))

            elif search('#license',out_line):
                self.write_license(out_file)
            else:
                out_file.write(out_line)

        out_file.close()

