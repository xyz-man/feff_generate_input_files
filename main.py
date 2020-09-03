'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
import logging
from cfg.class_cfg import Configuration
from lib_pkg.generate_feff_inp import FEFFVariablesReplacer
from lib_pkg.generate_run_initial import SLURMVariablesReplacer
from lib_pkg.dir_and_file_operations import *
import shutil
import subprocess


class Project:
    name = Configuration.PROJECT_NAME
    project_dir_path = None
    current_atomic_distance = None

    def init(self):
        if self.project_dir_path is None:
            self.project_dir_path = create_out_data_folder(Configuration.PROJECT_OUT_DIRECTORY_PATH,
                                                           first_part_of_folder_name=self.name)

    def is_inside_computation_limit(self):
        # check the computation restrictions
        out = False
        if self.current_atomic_distance < Configuration.TARGET_ATOM_MAX_DISTANCE:
            out = True
        return out

    def run(self):
        self.init()
        # start cycle for generate folders with feff.inp and run_initial.sl files:
        self.current_atomic_distance = 0
        target_atom_id = 1
        while self.is_inside_computation_limit():
            sub_folder_path = create_out_data_folder(self.project_dir_path, first_part_of_folder_name='tmp')

            obj_slurm = SLURMVariablesReplacer()
            obj_slurm.out_dir_path = sub_folder_path
            obj_slurm.job_name = "id={}_{}".format(target_atom_id, Configuration.TARGET_ATOM_TAG)
            obj_slurm.do_routine()

            obj_feff = FEFFVariablesReplacer()
            obj_feff.out_dir_path = sub_folder_path
            obj_feff.target_atom_number = target_atom_id
            obj_feff.do_routine()

            self.current_atomic_distance = obj_feff.atom_distance
            new_sub_folder_name = "{tag}_n={id}_d={dst}".format(
                tag=Configuration.TARGET_ATOM_TAG,
                dst=self.current_atomic_distance,
                id=target_atom_id)
            shutil.move(sub_folder_path, os.path.join(self.project_dir_path, new_sub_folder_name))
            if not self.is_inside_computation_limit():
                shutil.rmtree(os.path.join(self.project_dir_path, new_sub_folder_name))
                print('*****' * 10)
                print('***  Atomic distance above the limit')
                print('***  remove the last created directory: ', os.path.join(self.project_dir_path,
                                                                               new_sub_folder_name))
                print('*****' * 10)

            if self.is_inside_computation_limit():
                # if distance is correct run sbatch:
                self.run_sbatch(
                    dir_path=os.path.join(self.project_dir_path, new_sub_folder_name),
                )

            target_atom_id = target_atom_id + 1

    def run_sbatch(self, dir_path=None):
        if Configuration.START_CALCULATION:
            if dir_path is not None:
                if 'local' == Configuration.TYPE_OF_CALCULATION:
                    os.chdir(dir_path)
                    subprocess.call('sbatch ./run_initial.sl', shell=True)
                if 'remote' == Configuration.TYPE_OF_CALCULATION:
                    dir_path_on_remote_host = os.path.join(
                        Configuration.PATH_TO_SHARE_PROJECT_FOLDER_ON_REMOTE_HOST,
                        get_upper_folder_name(dir_path),
                        os.path.basename(dir_path),
                    )
                    print('dir_path_on_remote_host: ', dir_path_on_remote_host)
                    ssh_command = '{ssh} << EOF \n cd {dir}\n pwd\n sbatch ./run_initial.sl \nEOF'.format(
                        ssh=Configuration.SSH_COMMAND_CONNECT_TO_REMOTE_HOST,
                        dir=dir_path_on_remote_host,
                    )
                    subprocess.call(ssh_command, shell=True)


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = Project()
    obj.run()
    # ssh_command = 'ssh wien2k@10.88.0.245 << EOF \n cd ~\n pwd\n date\n hostname\nEOF'
    # print(ssh_command)
    # subprocess.call(ssh_command, shell=True)

