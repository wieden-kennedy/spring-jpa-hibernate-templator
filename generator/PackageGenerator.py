from os import mkdir,chdir
from os.path import join,exists

class PackageGenerator:
    def __init__(self,root_dir,basepackage,java_src_dir):
        self.root_dir = root_dir
        self.basepackage = basepackage
        self.java_src_dir = java_src_dir

    def generatePackagesIfNotPresent(self):
        chdir(self.root_dir)
        for item in self.java_src_dir.split('/'):
            if not exists(item):
                mkdir(item)
                chdir(item)
            else:
                chdir(item)

        for item in self.basepackage.split('.'):
            if not exists(item):
                mkdir(item)
                chdir(item)
            else:
                chdir(item)

        chdir(self.root_dir)

    def generate(self):
        self.generatePackagesIfNotPresent()