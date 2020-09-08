'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
import logging
from cfg.class_cfg import Configuration
from lib_pkg.generate_move_target_atom_feff_inp import FEFFVariablesReplacerMoveTargetAtom
from lib_pkg.generate_move_zero_ipot_atom_feff_inp import FEFFVariablesReplacerMoveZeroIpotAtom
from lib_pkg.generate_run_initial import SLURMVariablesReplacer
from lib_pkg.dir_and_file_operations import *
from lib_pkg.bases_stored_config import StoredConfigVariable, VarObject
import shutil
import subprocess


class Project:
    def __init__(self):
        self.name = Configuration.PROJECT_NAME
        self.project_dir_path = Configuration.PROJECT_CURRENT_OUT_DIRECTORY_PATH
        self.current_atomic_distance = None
        self.config_obj = StoredConfigVariable()

    def init(self):
        if self.project_dir_path is None:
            self.project_dir_path = create_out_data_folder(Configuration.PROJECT_OUT_DIRECTORY_PATH,
                                                           first_part_of_folder_name=self.name)
            Configuration.PROJECT_CURRENT_OUT_DIRECTORY_PATH = self.project_dir_path
            self.config_obj.dir_path = Configuration.PROJECT_CURRENT_OUT_DIRECTORY_PATH
            print('project_dir_path:', self.project_dir_path)

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
        FEFFReplacerClass = None
        sub_folder_name_txt = None
        if 'move_target_atom' in \
                Configuration.TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE:
            FEFFReplacerClass = FEFFVariablesReplacerMoveTargetAtom
        if 'move_zero_ipot_atom' in \
                Configuration.TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE:
            FEFFReplacerClass = FEFFVariablesReplacerMoveZeroIpotAtom

        while self.is_inside_computation_limit():
            sub_folder_path = create_out_data_folder(self.project_dir_path, first_part_of_folder_name='tmp')

            obj_slurm = SLURMVariablesReplacer()
            obj_slurm.out_dir_path = sub_folder_path
            obj_slurm.job_name = "{}=id_{}".format(target_atom_id, Configuration.TARGET_ATOM_TAG)
            obj_slurm.do_routine()

            obj_feff = FEFFReplacerClass()
            obj_feff.out_dir_path = sub_folder_path
            obj_feff.target_atom_number = target_atom_id
            obj_feff.do_routine()

            self.current_atomic_distance = obj_feff.atom_distance
            new_sub_folder_name = "central=[{ctag}]_moves=[{ttag}]_p=[{pol}]_n={id:04d}_d={dst}"\
                .format(
                ctag=Configuration.CENTRAL_ATOM_TAG,
                ttag=Configuration.TARGET_ATOM_TAG,
                pol=Configuration.POLARIZATION,
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
                var_obj = VarObject()
                var_obj.add_variable_to_dict(name='id', value=target_atom_id)
                var_obj.add_variable_to_dict(name='distance', value=self.current_atomic_distance)
                var_obj.add_variable_to_dict(name='polarization', value=Configuration.POLARIZATION)
                var_obj.add_variable_to_dict(name='directory_name', value=new_sub_folder_name)
                self.config_obj.add_object_to_list_of_dicts(var_obj)

            target_atom_id = target_atom_id + 1
        self.config_obj.store_data_to_pickle_file()

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
    obj.config_obj.load_data_from_pickle_file()
    print()
    # ssh_command = 'ssh wien2k@10.88.0.245 << EOF \n cd ~\n pwd\n date\n hostname\nEOF'
    # print(ssh_command)
    # subprocess.call(ssh_command, shell=True)

