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
from tempfile import NamedTemporaryFile
from cfg.config import *
from lib_pkg.bases_feff import *
import re
from lib_pkg.dir_and_file_operations import *
from collections import OrderedDict as odict


class FEFFVariablesReplacer:
    def __init__(self):
        self.src_full_filename = PATH_TO_SRC_FEFF_INPUT_FILE
        self.out_dir_path = None
        self.out_tmp_file = None
        self.out_base_filename = os.path.basename(self.src_full_filename)
        self.out_full_filename = None
        self.vars_dict = odict()
        self.current_atom_line_number = 0
        self.target_atom_number = 0
        self.atom_distance = 0

    def fill_vars_dict(self):
        obj = FEFFinputVariable()
        obj.name = 'admixture'
        obj.target_tag = TARGET_ATOM_TAG
        obj.target_ipot = TARGET_ATOM_IPOT
        obj.rebuild()
        self.vars_dict[str(obj.name)] = obj

    def create_out_tmp_folder(self):
        if self.out_dir_path is None:
            self.out_dir_path = create_out_data_folder(get_full_folder_path(self.src_full_filename),
                                                       first_part_of_folder_name='feff_out')

    def create_out_tmp_file(self):
        if self.out_tmp_file is None:
            self.out_tmp_file = NamedTemporaryFile(dir=self.out_dir_path, delete=False)

    def generate_out_full_filename(self):
        # self.out_base_filename = os.path.basename(self.src_full_filename)
        self.out_full_filename = os.path.join(self.out_dir_path, 'feff.inp')

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
                for line in fin:
                    # print(line)
                    if line.startswith(' ATOMS'):
                        is_atoms_block = True
                        print('is_atoms_block: ', is_atoms_block)
                    if line.startswith(' END'):
                        is_atoms_block = False
                        print('is_atoms_block: ', is_atoms_block)

                    if is_atoms_block:
                        for key, val in self.vars_dict.items():
                            if not val.immutable:
                                if val.search_pattern in line:
                                    wanted_atom_idx = wanted_atom_idx + 1
                                    if self.target_atom_number == wanted_atom_idx:
                                        val.input_line = line
                                        val.rebuild()
                                        self.atom_distance = val.value.distance
                                        line = val.output_string
                                        print('new line: ', line)
                                        print('atom distance: ', self.atom_distance)
                                    else:
                                        line = ''
                    fout.write(line.encode('utf8'))
                # To make sure the content is written to disk at a given point, you can use file.flush
                fout.flush()
                # Note that the docs recommend to use os.fsync(fd) after invoking flush() of the file object. flush
                # clears Python's file object buffer, fsync instructs the OS to write its file system buffers
                # corresponding to the filedescriptor to disk.
                os.fsync(fout.fileno())
            os.rename(fout.name, self.out_full_filename)

    def do_routine(self):
        self.create_out_tmp_folder()
        self.create_out_tmp_file()
        self.generate_out_full_filename()
        self.copy_src_file_to_out_dir()
        self.fill_vars_dict()
        self.replace_values_in_file()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = FEFFVariablesReplacer()
    obj.target_atom_number = 3
    obj.do_routine()

