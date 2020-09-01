'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
PATH_TO_SRC_FEFF_INPUT_FILE = \
    '/home/yugin/PycharmProjects/feff_generate_input_files/cfg/feff_inp/feff_ZnO-i-Yb-tetra.inp'

PATH_TO_SRC_SLURM_RUN_FILE = \
    '/home/yugin/PycharmProjects/feff_generate_input_files/cfg/batch_inp/run_initial.sl'


# the atom whose position we want to change:
# TARGET_ATOM_TAG = 'Yb-tetra'
TARGET_ATOM_TAG = 'Yb-octa'
TARGET_ATOM_IPOT = 3

PROJECT_NAME = 'ZnO_i=[{}]'.format(TARGET_ATOM_TAG)
PROJECT_DIR_PATH = '/home/yugin/PycharmProjects/feff_generate_input_files/tmp'

# max distance for structure rebuild procedure:
TARGET_ATOM_MAX_DISTANCE = 2

# number of FEFF calculation processes (SLURM: #SBATCH -n 4):
NUMBER_OF_TASKS = 6




if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
