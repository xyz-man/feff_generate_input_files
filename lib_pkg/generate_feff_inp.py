'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
import logging
from tempfile import NamedTemporaryFile
from lib_pkg.bases_feff import *
import re
from lib_pkg.dir_and_file_operations import *
from collections import OrderedDict as odict
from time import sleep


class FEFFVariablesReplacer:
    def __init__(self):
        self.src_full_filename = Configuration.PATH_TO_SRC_FEFF_INPUT_FILE
        self.out_dir_path = None
        self.out_tmp_file = None
        self.out_tmp_file_cleaned = None
        self.out_base_filename = os.path.basename(self.src_full_filename)
        self.out_full_filename = None
        self.out_full_filename_before_clean = None
        self.vars_dict = odict()
        self.current_file_line_number = 0
        self.target_atom_number = 0
        self.atom_distance = 0
        self.atom_coordinate_x = 0
        self.atom_coordinate_y = 0
        self.atom_coordinate_z = 0
        self.is_stop_event_happened = False

    def fill_vars_dict(self):
        obj = FEFFinputVariable()
        obj.name = 'admixture'
        obj.target_tag = Configuration.TARGET_ATOM_TAG
        obj.target_ipot = Configuration.TARGET_ATOM_IPOT
        obj.rebuild()
        self.vars_dict[str(obj.name)] = obj

    def create_out_tmp_folder(self):
        if self.out_dir_path is None:
            self.out_dir_path = create_out_data_folder(get_full_folder_path(self.src_full_filename),
                                                       first_part_of_folder_name='feff_out')

    def create_out_tmp_file(self):
        if self.out_tmp_file is None:
            self.out_tmp_file = NamedTemporaryFile(dir=self.out_dir_path, delete=False)
        if self.out_tmp_file_cleaned is None:
            self.out_tmp_file_cleaned = NamedTemporaryFile(dir=self.out_dir_path, delete=False)

    def generate_out_full_filename(self):
        # self.out_base_filename = os.path.basename(self.src_full_filename)
        self.out_full_filename = os.path.join(self.out_dir_path, 'feff.inp')
        self.out_full_filename_before_clean = os.path.join(self.out_dir_path, 'feff_bifore_clean.inp')

    def move_tmp_to_out_file(self):
        if (self.out_full_filename is not None) and (self.out_tmp_file is not None):
            shutil.move(self.out_tmp_file, self.out_full_filename)

    def copy_src_file_to_out_dir(self):
        if (self.src_full_filename is not None) and (self.out_dir_path is not None):
            out_file_full_name = os.path.join(self.out_dir_path, os.path.basename(self.src_full_filename))
            shutil.copy(self.src_full_filename, out_file_full_name)

    def replace_values_in_file(self):
        if (self.src_full_filename is not None) and (self.out_tmp_file is not None):
            is_atoms_block = False
            with open(self.src_full_filename, 'r') as fin, \
                    self.out_tmp_file as fout:
                wanted_atom_idx = 0
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
                        for key, value_dict in self.vars_dict.items():
                            if not value_dict.immutable:
                                if value_dict.search_pattern in current_file_line:
                                    wanted_atom_idx = wanted_atom_idx + 1
                                    if self.target_atom_number == wanted_atom_idx:
                                        value_dict.input_line = current_file_line
                                        value_dict.rebuild()
                                        self.atom_distance = value_dict.value.distance
                                        self.atom_coordinate_x = value_dict.value.x
                                        self.atom_coordinate_y = value_dict.value.y
                                        self.atom_coordinate_z = value_dict.value.z
                                        current_file_line = value_dict.output_string
                                        # print('new line: ', current_file_line)
                                        # print('atom distance: ', self.atom_distance)
                                        if self.atom_distance < 0.00000001:
                                            current_file_line = ''
                                    else:
                                        current_file_line = ''

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
                wanted_atom_idx = 0
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
                        for key, value_dict in self.vars_dict.items():
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
    obj = FEFFVariablesReplacer()
    obj.target_atom_number = 3
    # obj.do_routine()
    obj.show_properties()
