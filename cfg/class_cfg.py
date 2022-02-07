'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 02.09.2020
'''
import datetime
from cfg.settings import *
from lib_pkg.dir_and_file_operations import PROJECT_ROOT_DIRECTORY_PATH, delete_file, delete_folder
import os
import sys
from enum import Enum, auto
from copy import deepcopy
from pathlib import Path
import prettytable as pt
import subprocess
import shutil
import jsonpickle, json
from lib_pkg.serializer import JsonClassSerializable

try:
    from cfg.settings import TARGET_ATOM_TAG
except ImportError:
    print('Import Error: TARGET_ATOM_TAG is None')
    TARGET_ATOM_TAG = None

try:
    from cfg.settings import TARGET_ATOM_IPOT
except ImportError:
    print('Import Error: TARGET_ATOM_IPOT is None')
    TARGET_ATOM_IPOT = None

try:
    from cfg.settings import CENTRAL_ATOM_TAG
except ImportError:
    print('Import Error: CENTRAL_ATOM_TAG is None')
    CENTRAL_ATOM_TAG = None

try:
    from cfg.settings import CENTRAL_ATOM_IPOT
except ImportError:
    print('Import Error: CENTRAL_ATOM_IPOT is None')
    CENTRAL_ATOM_IPOT = None

try:
    from cfg.settings import ZERO_IPOT_ATOM_TAG
except ImportError:
    print('Import Error: ZERO_IPOT_ATOM_TAG is None')
    ZERO_IPOT_ATOM_TAG = None

try:
    from cfg.settings import ZERO_IPOT_ATOM_IPOT
except ImportError:
    print('Import Error: ZERO_IPOT_ATOM_IPOT is None')
    ZERO_IPOT_ATOM_IPOT = None


def print_object_properties_value_in_table_form(obj):
    table = pt.PrettyTable([
        'Name',
        'Value',
    ])
    for key, value in obj.__dict__.items():
        if (not key.startswith('__')) and ('classmethod' not in str(value)):
            table.add_row(
                [
                    str(key),
                    str(value),
                ]
            )
    print(table)


class BaseClass(JsonClassSerializable):
    def get_serialized_dict_of_properties(self):
        out = {}
        for key, value in self.__dict__.items():
            if (not key.startswith('__')) and ('classmethod' not in str(value)):
                try:
                    json.dumps(value)
                    out[key] = value
                except Exception as err:
                    out[key] = str(value)
        return out

    def show_properties(self):
        print_object_properties_value_in_table_form(self)

    def get_properties_in_json_form(self):
        out = jsonpickle.encode(self.get_serialized_dict_of_properties())
        return out


def update_one_value_to_another_value(a, b):
    if a is not None and b is None:
        b = deepcopy(a)
    if b is not None and a is None:
       a = deepcopy(b)

    return a, b


class CalculationType(Enum):
    LOCAL = auto()
    REMOTE_BY_NFS_AND_SSH = auto()
    REMOTE_BY_SSH = auto()


class Configuration(JsonClassSerializable):
    DEBUG = DEBUG
    MAXIMUM_NUMBER_OF_ITERATIONS = 125
    LEAVE_A_COPY_OF_THE_FILE_ON_THE_LOCAL_HOST = False
    ROOT_PROJECT_DIRECTORY_NAME = ROOT_PROJECT_DIRECTORY_NAME

    try:
        LATTICE_A_RANGE = LATTICE_A_RANGE
        LATTICE_B_RANGE = LATTICE_B_RANGE
        LATTICE_C_RANGE = LATTICE_C_RANGE
    except NameError:
        LATTICE_A_RANGE = None
        LATTICE_B_RANGE = None
        LATTICE_C_RANGE = None

    TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE = TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE
    list_of_procedure_changing_input_structure_types = [
        'move_target_atom',
        'move_zero_ipot_atom',
        'change_crystal_a_parameter',
        'change_crystal_b_parameter',
        'change_crystal_c_parameter',
        'change_crystal_abc_parameters',
    ]

    POLARIZATION = POLARIZATION
    SRC_FEFF_INPUT_FILE_NAME = SRC_FEFF_INPUT_FILE_NAME
    SRC_SLURM_RUN_FILE_NAME = SRC_SLURM_RUN_FILE_NAME

    PATH_TO_CONFIGURATION_DIRECTORY = None
    PATH_TO_TEMP_DIRECTORY = None
    PATH_TO_ROOT_PROJECT_DIRECTORY = None
    PATH_TO_SRC_FEFF_INPUT_FILE = None
    PATH_TO_SRC_SLURM_RUN_FILE = None

    TARGET_ATOM_TAG = TARGET_ATOM_TAG
    TARGET_ATOM_IPOT = TARGET_ATOM_IPOT

    CENTRAL_ATOM_TAG  = CENTRAL_ATOM_TAG
    CENTRAL_ATOM_IPOT = CENTRAL_ATOM_IPOT

    ZERO_IPOT_ATOM_TAG  = ZERO_IPOT_ATOM_TAG
    ZERO_IPOT_ATOM_IPOT = ZERO_IPOT_ATOM_IPOT

    PROJECT_NAME = PROJECT_NAME
    PROJECT_OUT_DIRECTORY_PATH_ON_LOCAL_HOST = PROJECT_OUT_DIRECTORY_PATH_ON_LOCAL_HOST
    PROJECT_OUT_DIRECTORY_PATH_ON_REMOTE_HOST = PROJECT_OUT_DIRECTORY_PATH_ON_REMOTE_HOST
    PROJECT_CURRENT_OUT_LOCAL_HOST_DIRECTORY_PATH = None
    PROJECT_CURRENT_OUT_REMOTE_HOST_DIRECTORY_PATH = None

    START_CALCULATION = START_CALCULATION
    TYPE_OF_CALCULATION = CalculationType.LOCAL

    PATH_TO_SHARE_PROJECT_FOLDER_ON_REMOTE_HOST = PATH_TO_SHARE_PROJECT_FOLDER_ON_REMOTE_HOST
    SSH_COMMAND_CONNECT_TO_REMOTE_HOST = SSH_COMMAND_CONNECT_TO_REMOTE_HOST
    REMOTE_HOST_LOGIN_IP = SSH_COMMAND_CONNECT_TO_REMOTE_HOST.split(' ')[-1]

    TARGET_ATOM_MAX_DISTANCE = TARGET_ATOM_MAX_DISTANCE
    MAXIMUM_LINE_NUMBER_OF_INPUT_FEFF_FILE = MAXIMUM_LINE_NUMBER_OF_INPUT_FEFF_FILE
    NUMBER_OF_TASKS = NUMBER_OF_TASKS

    @classmethod
    def validate_input_data(cls):
        try:
            pass
        except ValueError:
            print("Incorrect")

    @classmethod
    def init_cfg_folder(cls):
        dir_path = PROJECT_ROOT_DIRECTORY_PATH
        root_project_folder_name = cls.ROOT_PROJECT_DIRECTORY_NAME
        status = True
        cfg_path = PROJECT_ROOT_DIRECTORY_PATH
        tmp_path = PROJECT_ROOT_DIRECTORY_PATH
        while status:
            if root_project_folder_name == os.path.basename(dir_path):
                status = False
                cfg_path = os.path.join(dir_path, 'cfg')
                tmp_path = os.path.join(dir_path, 'tmp')
                break
            dir_path = Path(dir_path).parent

        cls.PATH_TO_CONFIGURATION_DIRECTORY = cfg_path
        cls.PATH_TO_ROOT_PROJECT_DIRECTORY = dir_path
        cls.PATH_TO_TEMP_DIRECTORY = tmp_path

    @classmethod
    def init_feff_input_file(cls):
        cls.PATH_TO_SRC_FEFF_INPUT_FILE = \
            os.path.join(
                cls.PATH_TO_CONFIGURATION_DIRECTORY,
                'feff_inp',
                cls.SRC_FEFF_INPUT_FILE_NAME)

    @classmethod
    def init_slurm_run_file(cls):
        cls.PATH_TO_SRC_SLURM_RUN_FILE = \
            os.path.join(
                cls.PATH_TO_CONFIGURATION_DIRECTORY,
                'batch_inp',
                cls.SRC_SLURM_RUN_FILE_NAME)

    @classmethod
    def init(cls):
        cls.__call__()
        if 'remote' == TYPE_OF_CALCULATION:
            Configuration.TYPE_OF_CALCULATION = CalculationType.REMOTE_BY_NFS_AND_SSH
        if 'remote_ssh' == TYPE_OF_CALCULATION:
            Configuration.TYPE_OF_CALCULATION = CalculationType.REMOTE_BY_SSH

        if cls.TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE not in \
                cls.list_of_procedure_changing_input_structure_types:
            cls.TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE = 'move_target_atom'
            out_txt = 'The input variable is invalid. Change the variable to its default value: [{}]'\
                .format(cls.TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE)
            print(out_txt)
            if cls.TARGET_ATOM_TAG is None:
                if cls.ZERO_IPOT_ATOM_TAG is not None:
                    cls.TARGET_ATOM_TAG, cls.ZERO_IPOT_ATOM_TAG = update_one_value_to_another_value(
                        cls.TARGET_ATOM_TAG, cls.ZERO_IPOT_ATOM_TAG)
                elif cls.CENTRAL_ATOM_TAG is not None:
                    cls.TARGET_ATOM_TAG, cls.CENTRAL_ATOM_TAG = update_one_value_to_another_value(cls.TARGET_ATOM_TAG,
                                                                                                cls.CENTRAL_ATOM_TAG)

        if cls.TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE == 'move_zero_ipot_atom':
            cls.TARGET_ATOM_TAG = cls.ZERO_IPOT_ATOM_TAG
            print('TARGET_ATOM_TAG = ZERO_IPOT_ATOM_TAG')
            print('TARGET_ATOM_TAG = {}'.format(cls.TARGET_ATOM_TAG))
            cls.TARGET_ATOM_IPOT = cls.ZERO_IPOT_ATOM_IPOT
            print('TARGET_ATOM_IPOT = ZERO_IPOT_ATOM_IPOT')
            print('TARGET_ATOM_IPOT = ', cls.TARGET_ATOM_IPOT)

        if cls.TYPE_OF_PROCEDURE_CHANGING_INPUT_STRUCTURE == 'change_crystal_a_parameter':
            cls.TARGET_ATOM_TAG = cls.ZERO_IPOT_ATOM_TAG
            print('TARGET_ATOM_TAG = ZERO_IPOT_ATOM_TAG')
            print('TARGET_ATOM_TAG = {}'.format(cls.TARGET_ATOM_TAG))
            cls.TARGET_ATOM_IPOT = cls.ZERO_IPOT_ATOM_IPOT
            print('TARGET_ATOM_IPOT = ZERO_IPOT_ATOM_IPOT')
            print('TARGET_ATOM_IPOT = ', cls.TARGET_ATOM_IPOT)

        cls.init_cfg_folder()
        cls.init_feff_input_file()
        cls.init_slurm_run_file()


    @classmethod
    def show_properties(cls):
        print_object_properties_value_in_table_form(cls)

    @classmethod
    def scp_copy_file_to_remote_host(cls, local_host_file_path=None, remote_host_out_file_path=None):
        scp_command = 'scp {file} {login}:{dir} '.format(
            file=local_host_file_path,
            login=Configuration.REMOTE_HOST_LOGIN_IP,
            dir=remote_host_out_file_path,
        )
        subprocess.call(scp_command, shell=True)

    @classmethod
    def scp_copy_directory_to_remote_host(cls, local_host_dir_path=None, remote_host_out_dir_path=None):
        scp_command = 'scp -r {dir} {login}:{out} '.format(
            dir=local_host_dir_path,
            login=Configuration.REMOTE_HOST_LOGIN_IP,
            out=remote_host_out_dir_path,
        )
        subprocess.call(scp_command, shell=True)

    @classmethod
    def scp_move_file_to_remote_host(cls, local_host_file_path=None, remote_host_out_file_path=None):
        Configuration.scp_copy_file_to_remote_host(local_host_file_path, remote_host_out_file_path)
        if not cls.LEAVE_A_COPY_OF_THE_FILE_ON_THE_LOCAL_HOST:
            delete_file(local_host_file_path)

    @classmethod
    def scp_move_directory_to_remote_host(cls, local_host_dir_path=None, remote_host_out_dir_path=None):
        Configuration.scp_copy_directory_to_remote_host(local_host_dir_path, remote_host_out_dir_path)
        if not cls.LEAVE_A_COPY_OF_THE_FILE_ON_THE_LOCAL_HOST:
            delete_folder(local_host_dir_path)

    @classmethod
    def create_dir_on_remote_host(cls, dir_path_on_remote_host):
        ssh_command = '{ssh} << EOF \n mkdir -p  {dir}\n EOF'.format(
            ssh=Configuration.SSH_COMMAND_CONNECT_TO_REMOTE_HOST,
            dir=dir_path_on_remote_host,
        )
        subprocess.call(ssh_command, shell=True)

    @classmethod
    def get_serialized_dict_of_properties(cls):
        out = {}
        for key, value in cls.__dict__.items():
            if (not key.startswith('__')) and ('classmethod' not in str(value)):
                try:
                    json.dumps(value)
                    out[key] = value
                except Exception as err:
                    out[key] = str(value)
        return out

    @classmethod
    def get_properties_in_json_form(cls):
        out = cls.get_serialized_dict_of_properties()
        out_serialize = jsonpickle.encode(out,
                                          # indent=4,
                                          )
        return out_serialize


tmp_obj = Configuration()
Configuration.init()

# importing logger settings
try:
    from cfg.logger_settings import *
except Exception as e:
    # in case of any error, pass silently.
    print('===='*10)
    print('logger settings not loaded')
    print('===='*10)


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    Configuration.show_properties()
    # a = Configuration()
    # a.encode_("test_00")
    # b = Configuration()
    # b.decode_("test")
    # b.show_properties()