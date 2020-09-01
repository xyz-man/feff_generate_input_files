'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
from cfg.config import *
from lib.generate_feff_inp import FEFFVariablesReplacer
from lib.generate_run_initial import SLURMVariablesReplacer
from lib.dir_and_file_operations import *
import shutil
import subprocess


class Project:
    name = PROJECT_NAME
    project_dir_path = create_out_data_folder(PROJECT_DIR_PATH, first_part_of_folder_name=name)

    def run(self):
        # start cycle for generate folders with feff.inp and run_initial.sl files:
        distance = 0
        target_atom_id = 1
        while distance <= TARGET_ATOM_MAX_DISTANCE:
            sub_folder_path = create_out_data_folder(self.project_dir_path, first_part_of_folder_name='tmp')

            obj_slurm = SLURMVariablesReplacer()
            obj_slurm.out_dir_path = sub_folder_path
            obj_slurm.job_name = "id={}_{}".format(target_atom_id, TARGET_ATOM_TAG)
            obj_slurm.do_routine()

            obj_feff = FEFFVariablesReplacer()
            obj_feff.out_dir_path = sub_folder_path
            obj_feff.target_atom_number = target_atom_id
            obj_feff.do_routine()

            distance = obj_feff.atom_distance
            new_sub_folder_name = "{tag}_n={id}_d={dst}".format(
                tag=TARGET_ATOM_TAG,
                dst=distance,
                id=target_atom_id)
            shutil.move(sub_folder_path, os.path.join(self.project_dir_path, new_sub_folder_name))
            if distance > TARGET_ATOM_MAX_DISTANCE:
                shutil.rmtree(os.path.join(self.project_dir_path, new_sub_folder_name))
                print('*****'*10)
                print('***  Atomic distance above the limit')
                print('***  remove the last created directory: ', os.path.join(self.project_dir_path,
                                                                             new_sub_folder_name))
                print('*****' * 10)

            if distance <= TARGET_ATOM_MAX_DISTANCE:
                # if distance is correct run sbatch:
                self.run_sbatch(dir_path=os.path.join(self.project_dir_path, new_sub_folder_name))

            target_atom_id = target_atom_id + 1

    def run_sbatch(self, dir_path=None):
        if dir_path is not None:
            os.chdir(dir_path)
            subprocess.call('sbatch ./run_initial.sl', shell=True)


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = Project()
    obj.run()
