'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
from tempfile import NamedTemporaryFile
from cfg.config import *
from lib_pkg.bases_slurm import *
import re
from lib_pkg.dir_and_file_operations import *
from collections import OrderedDict as odict


class SLURMVariablesReplacer:
    def __init__(self):
        self.src_full_filename = PATH_TO_SRC_SLURM_RUN_FILE
        self.out_dir_path = None
        self.out_tmp_file = None
        self.out_base_filename = os.path.basename(self.src_full_filename)
        self.out_full_filename = None
        self.vars_dict = odict()
        self.job_name = "test_job"

    def fill_vars_dict(self):
        obj = SLURMVariable()
        obj.name = 'ntasks'
        obj.value = NUMBER_OF_TASKS
        obj.output_string_base = "#SBATCH --{name}={val}\n"
        obj.search_pattern_base = "#SBATCH --{}"
        obj.help_string = """--ntasks=<number>
        sbatch does not launch tasks, it requests an allocation of resources and submits a batch script. 
        This option advises the Slurm controller that job steps run within the allocation will launch a 
        maximum of number tasks and to provide for sufficient resources. The default is one task per node, 
        but note that the --cpus-per-task option will change this default."""
        obj.rebuild()
        self.vars_dict[str(obj.name)] = obj

        obj = SLURMVariable()
        obj.name = 'job-name'
        obj.value = '"{}"'.format(self.job_name)
        obj.output_string_base = "#SBATCH --{name}={val}\n"
        obj.search_pattern_base = "#SBATCH --{}"
        obj.help_string = """--job-name=<jobname>
        Specify a name for the job allocation. The specified name will appear along with the job id number when 
        querying running jobs on the system. The default is the name of the batch script, or just "sbatch" if the 
        script is read on sbatch's standard input."""
        obj.rebuild()
        self.vars_dict[str(obj.name)] = obj

    def create_out_tmp_folder(self):
        if self.out_dir_path is None:
            self.out_dir_path = create_out_data_folder(get_full_folder_path(self.src_full_filename),
                                                       first_part_of_folder_name='slarm_out')

    def create_out_tmp_file(self):
        if self.out_tmp_file is None:
            self.out_tmp_file = NamedTemporaryFile(dir=self.out_dir_path, delete=False)

    def generate_out_full_filename(self):
        self.out_base_filename = os.path.basename(self.src_full_filename)
        self.out_full_filename = os.path.join(self.out_dir_path, self.out_base_filename)

    def move_tmp_to_out_file(self):
        if (self.out_full_filename is not None) and (self.out_tmp_file is not None):
            shutil.move(self.out_tmp_file, self.out_full_filename)

    def replace_values_in_file(self):
        if (self.src_full_filename is not None) and (self.out_tmp_file is not None):
            with open(self.src_full_filename, 'r') as fin, \
                    self.out_tmp_file as fout:
                for line in fin:
                    # print(line)
                    for key, val in self.vars_dict.items():
                        if not val.immutable:
                            if val.search_pattern in line:
                                line = val.output_string
                                print('new line: ', line)
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
        self.fill_vars_dict()
        self.replace_values_in_file()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = SLURMVariablesReplacer()
    obj.do_routine()
