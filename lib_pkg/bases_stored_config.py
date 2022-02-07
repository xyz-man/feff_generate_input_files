'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 07.09.2020
'''
import logging
import pickle
import json
import jsonpickle
import os
from typing import Optional
from lib_pkg.dumper import dump
from lib_pkg.bases import Variable
from cfg.class_cfg import Configuration, \
    print_object_properties_value_in_table_form, \
    pt, CalculationType, BaseClass, JsonClassSerializable


def clean_loaded_json_variable_dict(input_dict: dict = None) -> dict:
    if input_dict is not None:
        if isinstance(input_dict, dict):
            if len(input_dict) > 0:
                for val, item in input_dict.items():
                    tmp = None
                    try:
                        tmp = item['_class_object']['dict']
                        item = tmp
                    except:
                        pass
                    input_dict[val] = clean_loaded_json_variable_dict(item)
    return input_dict


class VarObject(JsonClassSerializable):
    def __init__(self):
        self.dict_of_stored_vars = {}

    def add_variable_to_dict(self, name: Optional[str] = None, value=None):
        if name is not None and value is not None:
            self.dict_of_stored_vars[name] = value

    def show_properties(self):
        table = pt.PrettyTable([
            'Name',
            'Value',
        ])
        for key, value in self.dict_of_stored_vars.items():
            if (not key.startswith('__')) and ('classmethod' not in str(value)):
                table.add_row(
                    [
                        str(key),
                        str(value),
                    ]
                )
        print('dict_of_stored_vars:')
        print(table)


class StoredConfigVariable(JsonClassSerializable):
    def __init__(self):
        self.description_line = None
        self.delimiter = None
        self.file_name_of_stored_vars = 'vars_configuration'
        self.stored_file_extension = \
            {
                'pickle': '.pckl',
                'json': '.json',
             }
        self.dir_path = Configuration.PROJECT_CURRENT_OUT_LOCAL_HOST_DIRECTORY_PATH
        self.config = Configuration
        self.config_json = Configuration.get_properties_in_json_form()
        self.list_of_variable_dicts = {}
        self.loaded_vars = None

    def add_object_to_list_of_dicts(self, input_obj: Optional[VarObject] = None):
        if input_obj is not None:
            n = 1
            if self.list_of_variable_dicts is not None:
                n = len(self.list_of_variable_dicts) + 1
            self.list_of_variable_dicts[n] = input_obj

    def flush(self):
        self.description_line = None
        self.delimiter = None
        self.file_name_of_stored_vars = 'vars_configuration.pckl'
        self.dir_path = Configuration.PROJECT_CURRENT_OUT_LOCAL_HOST_DIRECTORY_PATH
        self.list_of_variable_dicts = {}
        self.loaded_vars = None

    def show(self):
        # print(dump(self))
        print_object_properties_value_in_table_form(self)
        table = pt.PrettyTable([
            'Name',
            'Value',
        ])
        for key, value in self.list_of_variable_dicts.items():
            table.add_row(
                [
                    str(key),
                    str(value.dict_of_stored_vars),
                ]
            )
        print('list_of_variable_dicts:')
        print(table)

    def store_data_to_pickle_file(self):
        if self.dir_path is None:
            self.dir_path = Configuration.PROJECT_OUT_DIRECTORY_PATH_ON_LOCAL_HOST
            print('dir_path:', self.dir_path)
        pckl_file = os.path.join(
            self.dir_path,
            self.file_name_of_stored_vars + self.stored_file_extension['pickle'])
        with open(pckl_file, 'wb') as f:
            self.config_json = Configuration.get_properties_in_json_form()
            pickle.dump([self], f)
            f.close()
        if Configuration.TYPE_OF_CALCULATION is CalculationType.REMOTE_BY_SSH:
            remote_host_out_dir = os.path.join(
                Configuration.PROJECT_OUT_DIRECTORY_PATH_ON_REMOTE_HOST,
                os.path.basename(self.dir_path),
            )
            remote_host_out_file_path = os.path.join(
                remote_host_out_dir,
                self.file_name_of_stored_vars + self.stored_file_extension['pickle'],
            )
            Configuration.scp_move_file_to_remote_host(
                local_host_file_path=pckl_file,
                remote_host_out_file_path=remote_host_out_file_path,
            )

    def store_data_to_json_file(self):
        if self.dir_path is None:
            self.dir_path = Configuration.PROJECT_OUT_DIRECTORY_PATH_ON_LOCAL_HOST
            print('dir_path:', self.dir_path)
        json_file = os.path.join(
            self.dir_path,
            self.file_name_of_stored_vars + self.stored_file_extension['json'])
        self.encode_(json_file)
        # with open(json_file, 'w', encoding='utf-8') as f:
        #     self.config_json = Configuration.get_properties_in_json_form()
        #     json_object = jsonpickle.encode(self)
        #     json.dump(json_object, f, ensure_ascii=False)
        #     f.close()
        if Configuration.TYPE_OF_CALCULATION is CalculationType.REMOTE_BY_SSH:
            remote_host_out_dir = os.path.join(
                Configuration.PROJECT_OUT_DIRECTORY_PATH_ON_REMOTE_HOST,
                os.path.basename(self.dir_path),
            )
            remote_host_out_file_path = os.path.join(
                remote_host_out_dir,
                self.file_name_of_stored_vars + self.stored_file_extension['json'],
            )
            Configuration.scp_move_file_to_remote_host(
                local_host_file_path=json_file,
                remote_host_out_file_path=remote_host_out_file_path,
            )

    def load_data_from_pickle_file(self):
        # Getting back the objects:
        if self.dir_path is None:
            self.dir_path = Configuration.PROJECT_OUT_DIRECTORY_PATH_ON_LOCAL_HOST
            print('dir_path:', self.dir_path)
        data_file = os.path.join(
                self.dir_path,
                self.file_name_of_stored_vars + self.stored_file_extension['pickle']
        )
        if os.path.isfile(data_file):
            with open(data_file, 'rb') as f:
                obj = pickle.load(f)
            # print('')
            try:
                self.loaded_vars = obj[0]
                # self.last_used_file_path = obj[0].last_used_file_path
            except Exception as err:
                error_txt = 'TextConfigVariable: load_data_from_pickle_file: \n'
                error_txt = error_txt + '{} does not have needed attributes\n'.format(self.file_name_of_stored_vars)
                logging.getLogger("error_logger").error(error_txt + repr(err))
                if Configuration.DEBUG:
                    print(error_txt, repr(err))

    def load_data_from_json_file(self):
        # Getting back the objects:
        if self.dir_path is None:
            self.dir_path = Configuration.PROJECT_OUT_DIRECTORY_PATH_ON_LOCAL_HOST
            print('dir_path:', self.dir_path)
        data_file = os.path.join(
                self.dir_path,
                self.file_name_of_stored_vars + self.stored_file_extension['json']
        )
        if os.path.isfile(data_file):
            with open(data_file, 'r') as infile:
                obj = json.load(
                    infile,
                    # object_hook=self.json_to_class
                )
            try:
                self.loaded_vars = clean_loaded_json_variable_dict(obj)
                # self.loaded_vars['config'] = self.loaded_vars['config']['_class_object']['dict']
                # self.last_used_file_path = obj[0].last_used_file_path
            except Exception as err:
                error_txt = 'TextConfigVariable: load_data_from_pickle_file: \n'
                error_txt = error_txt + '{} does not have needed attributes\n'.format(self.file_name_of_stored_vars)
                logging.getLogger("error_logger").error(error_txt + repr(err))
                if Configuration.DEBUG:
                    print(error_txt, repr(err))


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj_tmp = VarObject()
    obj_tmp.add_variable_to_dict(name='v', value=10)
    obj_tmp.add_variable_to_dict(name='vv', value=100)
    obj_tmp.show_properties()
    obj = StoredConfigVariable()
    obj.show_properties()
    obj.description_line = 'Test description'
    obj.delimiter = '/t'
    obj.add_object_to_list_of_dicts(obj_tmp)
    obj.show()
    obj.encode_("test_22")
    # obj.store_data_to_pickle_file()
    # obj.store_data_to_json_file()
    # obj.load_data_from_pickle_file()
    obj.load_data_from_json_file()
    obj.show_properties()
    obj.show()
