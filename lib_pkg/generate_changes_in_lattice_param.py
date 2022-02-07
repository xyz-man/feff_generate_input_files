'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 01.02.2022
'''

import logging
from tempfile import NamedTemporaryFile
from lib_pkg.bases_feff import *
import re
from lib_pkg.dir_and_file_operations import *
from collections import OrderedDict as odict
from time import sleep
from lib_pkg.generate_move_target_atom_feff_inp import FEFFVariablesReplacerMoveTargetAtom
from lib_pkg.crystal.zno_ideal import ZnOCrystalStructure


class FEFFVariablesReplacerChangeLatticeParam(FEFFVariablesReplacerMoveTargetAtom):
    '''
    Change a, b, c lattice parameters
    '''
    def __init__(self):
        super(FEFFVariablesReplacerChangeLatticeParam, self).__init__()
        self.a_lattice = None
        self.b_lattice = None
        self.c_lattice = None
        self.crystal_structure = ZnOCrystalStructure()
        self.crystal_structure.cluster_size = 6
        self.crystal_structure.header_comment += '\nTITLE Cluster size: Rmax={}'.format(
            self.crystal_structure.cluster_size)

    def replace_values_in_file(self):
        if (self.src_full_filename is not None):
            self.crystal_structure.a = self.a_lattice
            self.crystal_structure.b = self.b_lattice
            self.crystal_structure.c = self.c_lattice
            self.crystal_structure.init()

            self.crystal_structure.path_to_out_feff_input = self.out_full_filename
            self.crystal_structure.write_file()

    def do_routine(self):
        self.create_out_tmp_folder()
        # self.create_out_tmp_file()
        self.generate_out_full_filename()
        self.copy_src_file_to_out_dir()
        self.fill_vars_dict()
        self.replace_values_in_file()
        # sleep(5)

    def show_properties(self):
        print_object_properties_value_in_table_form(self)


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = FEFFVariablesReplacerChangeLatticeParam()
    obj.target_atom_number = 1
    obj.do_routine()
    obj.show_properties()

