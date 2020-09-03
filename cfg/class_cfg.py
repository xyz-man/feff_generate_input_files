'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 02.09.2020
'''
import logging
import datetime
from cfg.settings import *
from lib_pkg.dir_and_file_operations import PROJECT_ROOT_DIRECTORY_PATH
import os
from pathlib import Path
import prettytable as pt


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


class Configuration:
    DEBUG = DEBUG
    ROOT_PROJECT_DIRECTORY_NAME = ROOT_PROJECT_DIRECTORY_NAME

    SRC_FEFF_INPUT_FILE_NAME = SRC_FEFF_INPUT_FILE_NAME
    SRC_SLURM_RUN_FILE_NAME = SRC_SLURM_RUN_FILE_NAME

    PATH_TO_CONFIGURATION_DIRECTORY = None
    PATH_TO_SRC_FEFF_INPUT_FILE = None
    PATH_TO_SRC_SLURM_RUN_FILE = None

    TARGET_ATOM_TAG = TARGET_ATOM_TAG
    TARGET_ATOM_IPOT = TARGET_ATOM_IPOT

    PROJECT_NAME = PROJECT_NAME
    PROJECT_OUT_DIRECTORY_PATH = PROJECT_OUT_DIRECTORY_PATH

    START_CALCULATION = START_CALCULATION
    TYPE_OF_CALCULATION = TYPE_OF_CALCULATION

    PATH_TO_SHARE_PROJECT_FOLDER_ON_REMOTE_HOST = PATH_TO_SHARE_PROJECT_FOLDER_ON_REMOTE_HOST
    SSH_COMMAND_CONNECT_TO_REMOTE_HOST = SSH_COMMAND_CONNECT_TO_REMOTE_HOST

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
        while status:
            if root_project_folder_name == os.path.basename(dir_path):
                status = False
                cfg_path = os.path.join(dir_path, 'cfg')
                break
            dir_path = Path(dir_path).parent

        cls.PATH_TO_CONFIGURATION_DIRECTORY = cfg_path

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
        cls.init_cfg_folder()
        cls.init_feff_input_file()
        cls.init_slurm_run_file()

    @classmethod
    def show_properties(cls):
        print_object_properties_value_in_table_form(cls)


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