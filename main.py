from generator.ModelGenerator import ModelGenerator
from generator.ServiceGenerator import ServiceGenerator
from generator.RepositoryGenerator import RepositoryGenerator
from generator.ConfigGenerator import ConfigGenerator
from generator.PomGenerator import PomGenerator
from generator.PackageGenerator import PackageGenerator
from generator.PropertiesGenerator import PropertiesGenerator

from os import getcwd, mkdir, chdir
from os.path import exists, join
from subprocess import call
from shutil import move

import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="command line args to assist configure templator")
    parser.add_argument('-f',type=str,dest='f',help='add the full path to your models (json) file',required=False)
    parser.add_argument('-l',type=str,dest='l',help='add the full path to your licensing text file, if present',required=False)
    parser.add_argument('-j',help='create a jar package from this build',action='store_true')
    parser.add_argument('-i',help='install the jar package on the local system (packages to ./target by default)',action='store_true')
    parser.add_argument('-o',help='output directory for generated source files and jar, if packaged', type=str,required=False)
    parser.add_argument('-d',help='dry run. print out expected args without running program',action='store_true')
    return parser.parse_args()

def jarThis(installNotPackage):
    target='package'
    if installNotPackage:
        target='install'
    args = ['mvn','clean',target]
    call(args)

if __name__ == '__main__':
    args = parse_args()

    TEMPLATE_DIR='templates'
    MODELS_DATA=None
    JAVA_SOURCE_PATH='src/main/java'
    BASE_PACKAGE=None
    CWD=getcwd()
    MODELS_FILE='./model.json'
    LICENSING_FILE=None
    models=[]

    if args.f:
        MODELS_FILE = args.f
    if args.l:
        LICENSING_FILE=join(CWD,args.l)

    # read in the models JSON file        
    with open(MODELS_FILE) as data_file:
        # load in template data from data file
        MODELS_DATA = json.load(data_file)

    BASE_PACKAGE = MODELS_DATA['basepackage']
    APP_PROPS = MODELS_DATA['application_properties']

    # generate package directories if not present
    packageGenerator = PackageGenerator(CWD,BASE_PACKAGE,JAVA_SOURCE_PATH)
    packageGenerator.generate()

    # generate POM.xml
    pom_generator = PomGenerator(join(TEMPLATE_DIR,'pom'),BASE_PACKAGE)
    pom_generator.set_group(MODELS_DATA['group_id'])
    pom_generator.set_artifact(MODELS_DATA['artifact_id'])
    pom_generator.set_package(MODELS_DATA['package_name'])
    pom_generator.generate()

    # for each model in the template data
    for model in MODELS_DATA['models']:
        models.append(model)
        # generate Model class
        mg = ModelGenerator('model',CWD,BASE_PACKAGE,JAVA_SOURCE_PATH, model)
        if LICENSING_FILE:
            mg.set_licensing(LICENSING_FILE)
        mg.generate()

        # generate Service Classes
        sg = ServiceGenerator('service',CWD,BASE_PACKAGE,JAVA_SOURCE_PATH,model)
        if LICENSING_FILE:
            sg.set_licensing(LICENSING_FILE)
        sg.generate()

        # generate Repository Class
        rg = RepositoryGenerator('repository',CWD,BASE_PACKAGE,JAVA_SOURCE_PATH,model)
        if LICENSING_FILE:
            rg.set_licensing(LICENSING_FILE)
        rg.generate()

    # generate config class
    config_generator = ConfigGenerator('config',CWD,BASE_PACKAGE,JAVA_SOURCE_PATH,None)
    config_generator.set_models(models)
    config_generator.set_properties_file(MODELS_DATA['properties_file_name'])
    if LICENSING_FILE:
        config_generator.set_licensing(LICENSING_FILE)
    config_generator.generate()

    properties_generator = PropertiesGenerator('properties',CWD,BASE_PACKAGE,None,None)
    properties_generator.set_properties(APP_PROPS)
    properties_generator.generate()

    if args.o:
        chdir(CWD)
        source_root = JAVA_SOURCE_PATH.split('/')[0]
        move(source_root,join(args.o,source_root))
        move('pom.xml',join(args.o,'pom.xml'))
        CWD=args.o

    if args.j:
        chdir(CWD)
        jarThis(args.i)

