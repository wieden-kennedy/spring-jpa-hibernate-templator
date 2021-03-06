from os import mkdir
from os.path import join, exists
from Generator import Generator
from re import search
class ModelGenerator(Generator):
    def generate_class(self):
        model_name=self.model['model_name']

        if not exists('./%s/model' % self.basepackage_path):
           mkdir('./%s/model' % self.basepackage_path) 
        self.out_file=open(self.out_path, 'w')
        for line in self.template_data:
            out_line = line
            
            out_line = out_line.replace('${basepackage}',self.basepackage_path.replace('/','.'))
            out_line = out_line.replace('${model_name}', model_name)
            out_line = out_line.replace('${TABLE}', '%s' % self.model['table'].upper())
            out_line = out_line.replace('${idType}', self.model['id_type'])


            if search('#members', out_line):
                self.generate_members()

            elif search('#getters_setters', out_line):
                self.generate_getters_setters()

            elif search('#license',out_line):
                self.write_license()

            else:
                self.out_file.write(out_line)

        self.out_file.close()

    def generate_members(self):
        # first write in members
        for member in self.model['member_variables']:
            protection = 'private'
            if not member['field_name'] == 'id':
                # if 'maps_id' in member or 'relationship_type' in member or 'foreign_key' in member:
                #     protection = 'public'
                # if 'maps_id' in member:
                #     self.out_file.write('\t@MapsId\n')
                # if 'relationship_type' in member:
                #     self.out_file.write('\t@%s\n' % member['relationship_type'])
                # if 'foreign_key' in member:
                #     self.out_file.write('\t@JoinColumn(name="%s")\n' % member['foreign_key'])
                # if 'use_primary_key' in member:
                #     self.out_file.write('\t@PrimaryKeyJoinColumn\n')
                if not 'relationship_type' in member:
                    if 'column' in member:
                        self.out_file.write('\t@Column(name = "%s")\n' % member['column'].upper())
                self.out_file.write('\t%s %s %s;\n\n' % (protection,member['type'],member['field_name']))
        
        self.out_file.write('\n')

    def generate_getters_setters(self):
        getter_setter_template = open(join(self.template_dir,'getter_setter.txt'))
        getter_setter_template_data = getter_setter_template.readlines()
        getter_setter_template.close()

        for member in self.model['member_variables']:
            titlecase_member = '%s%s' % (member['field_name'][0].upper(),member['field_name'][1:])
            for gs_line in getter_setter_template_data:
                out_gs_line = gs_line
                out_gs_line = out_gs_line.replace('${type}',member['type'])
                out_gs_line = out_gs_line.replace('${Member}',titlecase_member)
                out_gs_line = out_gs_line.replace('${member}', member['field_name'])

                self.out_file.write('\t%s' % out_gs_line)
