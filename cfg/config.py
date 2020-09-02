'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
from  lib.dir_and_file_operations import PROJECT_FOLDER_PATH, get_upper_folder_name
import os

print('PROJECT_FOLDER_PATH:', PROJECT_FOLDER_PATH)
PATH_TO_SRC_FEFF_INPUT_FILE = os.path.join(PROJECT_FOLDER_PATH, 'cfg', 'feff_inp', 'feff_ZnO-i-Yb-tetra_101.inp')

PATH_TO_SRC_SLURM_RUN_FILE = os.path.join(PROJECT_FOLDER_PATH, 'cfg', 'batch_inp', 'run_initial.sl')


# the atom whose position we want to change:
TARGET_ATOM_TAG = 'Yb-tetra'
# TARGET_ATOM_TAG = 'Yb-octa'
TARGET_ATOM_IPOT = 3

PROJECT_NAME = 'ZnO_i=[{}]_p=[101]'.format(TARGET_ATOM_TAG)

PROJECT_DIR_PATH = '/home/yugin/PycharmProjects/feff_generate_input_files/tmp'
# PROJECT_DIR_PATH = '/mnt/nfsv4/abel_share/free_share/ZnO/'

# start feff calculations by using SLURM sbatch command:
START_CALCULATION = True

# local/remote:
TYPE_OF_CALCULATION = 'local'
# TYPE_OF_CALCULATION = 'remote'

# if TYPE_OF_CALCULATION='remote':
# if TYPE_OF_CALCULATION='remote' make sure PROJECT_DIR_PATH is located in the shared folder with the remote host
PATH_TO_SHARE_PROJECT_FOLDER_ON_REMOTE_HOST = '/mnt/nfsv4/abel_share/free_share/ZnO/'
SSH_COMMAND_CONNECT_TO_REMOTE_HOST = 'ssh wien2k@10.88.0.245'  # wien2k_abel
# SSH_COMMAND_CONNECT_TO_REMOTE_HOST = 'ssh wien2k@10.88.0.244'  # wien2k_paradox

# max distance for structure rebuild procedure:
TARGET_ATOM_MAX_DISTANCE = 2

# number of FEFF calculation processes (SLURM: #SBATCH -n 4):
NUMBER_OF_TASKS = 8




if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    print(PROJECT_FOLDER_PATH)
    print(get_upper_folder_name(PROJECT_FOLDER_PATH))
    print(os.path.basename(PROJECT_FOLDER_PATH))
    print(os.path.dirname(PROJECT_FOLDER_PATH))
