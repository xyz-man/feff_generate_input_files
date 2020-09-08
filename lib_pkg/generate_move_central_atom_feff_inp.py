'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 08.09.2020
'''
import logging
from tempfile import NamedTemporaryFile
from lib_pkg.bases_feff import *
import re
from lib_pkg.dir_and_file_operations import *
from collections import OrderedDict as odict
from time import sleep
from lib_pkg.generate_move_target_atom_feff_inp import FEFFVariablesReplacerMoveTargetAtom


class FEFFVariablesReplacerMoveTheroIpotAtom(FEFFVariablesReplacerMoveTargetAtom):
    '''
    move atom with IPOT=0
    '''

    def replace_values_in_file(self):
        if (self.src_full_filename is not None) and (self.out_tmp_file is not None):
            is_atoms_block = False
            with open(self.src_full_filename, 'r') as fin, \
                    self.out_tmp_file as fout:
                under_processing_atom_idx = 0
                for current_file_line in fin:
                    self.current_file_line_number = self.current_file_line_number + 1
                    # print(line)
                    if current_file_line.startswith(' ATOMS'):
                        is_atoms_block = True
                        # print('is_atoms_block: ', is_atoms_block)
                    if current_file_line.startswith(' END'):
                        is_atoms_block = False
                        # print('is_atoms_block: ', is_atoms_block)

                    if is_atoms_block:
                        for target_key, target_value_dict in self.vars_dict_target_atom.items():
                            for central_atom_key, central_atom_value_dict in self.vars_dict_central_atom.items():
                                if not target_value_dict.immutable:
                                    if target_value_dict.search_pattern in current_file_line:
                                        under_processing_atom_idx = under_processing_atom_idx + 1
                                        if self.target_atom_number == under_processing_atom_idx:
                                            target_value_dict.input_line = current_file_line
                                            target_value_dict.rebuild()
                                            self.atom_distance = target_value_dict.value.distance
                                            self.atom_coordinate_x = target_value_dict.value.x
                                            self.atom_coordinate_y = target_value_dict.value.y
                                            self.atom_coordinate_z = target_value_dict.value.z
                                            current_file_line = target_value_dict.output_string_base_for_zero_ipot
                                            # print('new line: ', current_file_line)
                                            # print('atom distance: ', self.atom_distance)
                                            if self.atom_distance < 0.00000001:
                                                current_file_line = ''
                                        else:
                                            # current_file_line = ''
                                            pass

                                        if Configuration.MAXIMUM_LINE_NUMBER_OF_INPUT_FEFF_FILE is not None and \
                                                self.current_file_line_number > \
                                                Configuration.MAXIMUM_LINE_NUMBER_OF_INPUT_FEFF_FILE:
                                            if not self.is_stop_event_happened:
                                                tmp_atom_obj = AtomDescription()
                                                tmp_atom_obj.get_values_from_line(current_file_line)

                                                print('*****' * 10)
                                                print('***  Line number above the limit.')
                                                print('***  Set TARGET_ATOM_MAX_DISTANCE to new value')
                                                print('***  TARGET_ATOM_MAX_DISTANCE Old: ',
                                                      Configuration.TARGET_ATOM_MAX_DISTANCE)
                                                print('***  TARGET_ATOM_MAX_DISTANCE New: ', tmp_atom_obj.distance)
                                                print('*****' * 10)
                                                Configuration.TARGET_ATOM_MAX_DISTANCE = tmp_atom_obj.distance
                                                self.is_stop_event_happened = True
                                            current_file_line = ''

                                    #         routine for central atom:
                                    if central_atom_value_dict.search_pattern in current_file_line:
                                        central_atom_value_dict.input_line = current_file_line
                                        central_atom_value_dict.rebuild()
                                        self.atom_distance = central_atom_value_dict.value.distance
                                        self.atom_coordinate_x = central_atom_value_dict.value.x
                                        self.atom_coordinate_y = central_atom_value_dict.value.y
                                        self.atom_coordinate_z = central_atom_value_dict.value.z
                                        current_file_line = central_atom_value_dict.output_string
                                        # print('new line: ', current_file_line)
                                        # print('atom distance: ', self.atom_distance)
                                        if self.atom_distance > 0.00000001:
                                            current_file_line = ''

                    fout.write(current_file_line.encode('utf8'))
                # To make sure the content is written to disk at a given point, you can use file.flush
                fout.flush()
                # Note that the docs recommend to use os.fsync(fd) after invoking flush() of the file object. flush
                # clears Python's file object buffer, fsync instructs the OS to write its file system buffers
                # corresponding to the filedescriptor to disk.
                os.fsync(fout.fileno())
            os.rename(fout.name, self.out_full_filename_before_clean)

    def clean_atomic_coordinate_values_in_file(self):
        '''
        execute this method after 'replace_values_in_file' only
        this method delete all duplicates in x,y,z
        '''
        if (self.out_full_filename_before_clean is not None) and (self.out_tmp_file is not None):
            is_atoms_block = False
            with open(self.out_full_filename_before_clean, 'r') as fin, \
                    self.out_tmp_file_cleaned as fout:
                under_processing_atom_idx = 0
                current_atom_obj = AtomDescription()
                for current_file_line in fin:
                    self.current_file_line_number = self.current_file_line_number + 1
                    # print(line)
                    if current_file_line.startswith(' ATOMS'):
                        is_atoms_block = True
                        # print('is_atoms_block: ', is_atoms_block)
                    if current_file_line.startswith(' END'):
                        is_atoms_block = False
                        # print('is_atoms_block: ', is_atoms_block)

                    if is_atoms_block:
                        current_atom_obj.get_values_from_line(current_file_line)
                        for key, value_dict in self.vars_dict_central_atom.items():
                            if value_dict.search_pattern not in current_file_line:
                                if (self.atom_distance == current_atom_obj.distance) and \
                                        (self.atom_coordinate_x == current_atom_obj.x) and \
                                        (self.atom_coordinate_y == current_atom_obj.y) and \
                                        (self.atom_coordinate_z == current_atom_obj.z):
                                    current_file_line = ''
                        for key, value_dict in self.vars_dict_target_atom.items():
                            if value_dict.search_pattern not in current_file_line:
                                if (self.atom_distance == current_atom_obj.distance) and \
                                        (self.atom_coordinate_x == current_atom_obj.x) and \
                                        (self.atom_coordinate_y == current_atom_obj.y) and \
                                        (self.atom_coordinate_z == current_atom_obj.z):
                                    current_file_line = ''
                    fout.write(current_file_line.encode('utf8'))
                # To make sure the content is written to disk at a given point, you can use file.flush
                fout.flush()
                # Note that the docs recommend to use os.fsync(fd) after invoking flush() of the file object. flush
                # clears Python's file object buffer, fsync instructs the OS to write its file system buffers
                # corresponding to the filedescriptor to disk.
                os.fsync(fout.fileno())
            if Configuration.DEBUG:
                print('cleaned file:', self.out_full_filename)
            else:
                os.remove(self.out_full_filename_before_clean)
            os.rename(fout.name, self.out_full_filename)

    def do_routine(self):
        self.create_out_tmp_folder()
        self.create_out_tmp_file()
        self.generate_out_full_filename()
        self.copy_src_file_to_out_dir()
        self.fill_vars_dict()
        self.replace_values_in_file()
        # print('before clean:')
        # sleep(5)
        self.clean_atomic_coordinate_values_in_file()

    def show_properties(self):
        print_object_properties_value_in_table_form(self)


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = FEFFVariablesReplacerMoveTheroIpotAtom()
    obj.target_atom_number = 6
    obj.do_routine()
    obj.show_properties()
