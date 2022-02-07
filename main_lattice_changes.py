'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 04.02.2022
'''
from cfg.class_cfg import Configuration, CalculationType
from lib_pkg.generate_changes_in_lattice_param import FEFFVariablesReplacerChangeLatticeParam
from lib_pkg.generate_run_initial import SLURMVariablesReplacer
from lib_pkg.dir_and_file_operations import *
from lib_pkg.bases_stored_config import VarObject
from main import Project
import shutil
import subprocess


class ProjectLatticeChanges(Project):
    def is_inside_computation_limit(self):
        # check the computation restrictions
        out = False
        if self.current_cycle_index < Configuration.MAXIMUM_NUMBER_OF_ITERATIONS:
            out = True
        return out

    def run(self):
        self.init()
        # start cycle for generate folders with feff.inp and run_initial.sl files:
        self.current_atomic_distance = 0
        target_atom_id = 1
        FEFFReplacerClass = None
        sub_folder_name_txt = None
        if 'change_crystal_abc_parameters' in \
                Configuration.TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE:
            FEFFReplacerClass = FEFFVariablesReplacerChangeLatticeParam

        for ab_lattice in Configuration.LATTICE_A_RANGE:
            for c_lattice in Configuration.LATTICE_C_RANGE:
                if self.is_inside_computation_limit():
                    self.current_cycle_index += 1
                    sub_folder_path = create_out_data_folder(self.project_dir_path, first_part_of_folder_name='tmp')

                    obj_slurm = SLURMVariablesReplacer()
                    obj_slurm.out_dir_path = sub_folder_path
                    obj_slurm.job_name = "abc=id_{}".format(self.current_cycle_index)
                    obj_slurm.do_routine()

                    obj_feff = FEFFReplacerClass()
                    obj_feff.out_dir_path = sub_folder_path
                    obj_feff.a_lattice = ab_lattice
                    obj_feff.b_lattice = ab_lattice
                    obj_feff.c_lattice = c_lattice
                    obj_feff.do_routine()

                    new_sub_folder_name = "a=[{al:1.3f}]_b=[{bl:1.3f}]_c=[{cl:1.3f}]_n={n:04d}" \
                        .format(
                        al=ab_lattice,
                        bl=ab_lattice,
                        cl=c_lattice,
                        n=self.current_cycle_index,
                    )

                    # shutil.move(sub_folder_path, os.path.join(self.project_dir_path, new_sub_folder_name))
                    self.move_temp_dir_to_specified_directory(
                        dir_path=sub_folder_path,
                        where_to_move_dir_path=os.path.join(self.project_dir_path, new_sub_folder_name)
                    )

                    # if distance is correct run sbatch:
                    if self.does_the_feff_calculation_start:
                        self.run_sbatch(
                            dir_path=os.path.join(self.project_dir_path, new_sub_folder_name),
                        )
                    var_obj = VarObject()
                    var_obj.add_variable_to_dict(name='N', value=self.current_cycle_index)
                    var_obj.add_variable_to_dict(name='a_lattice', value=ab_lattice)
                    var_obj.add_variable_to_dict(name='b_lattice', value=ab_lattice)
                    var_obj.add_variable_to_dict(name='c_lattice', value=c_lattice)
                    var_obj.add_variable_to_dict(name='polarization', value=Configuration.POLARIZATION)
                    var_obj.add_variable_to_dict(name='directory_name', value=new_sub_folder_name)
                    self.config_obj.add_object_to_list_of_dicts(var_obj)

        self.config_obj.store_data_to_pickle_file()
        self.config_obj.store_data_to_json_file()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    Configuration.LEAVE_A_COPY_OF_THE_FILE_ON_THE_LOCAL_HOST = True
    obj = ProjectLatticeChanges()
    obj.does_the_feff_calculation_start = True
    obj.run()
    obj.config_obj.load_data_from_pickle_file()
    obj.config_obj.load_data_from_json_file()
    obj.config_obj.show()
    print()
