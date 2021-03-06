'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
import logging
from lib_pkg.bases import Variable
import re
import numpy as np
import prettytable as pt
from cfg.class_cfg import Configuration, print_object_properties_value_in_table_form


class AtomDescription:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.ipot = None
        self.tag = None
        self.element_name = None
        self.distance = None
        self.out_line = None
        self.out_line_for_zero_ipot = None
        self.is_comment = False

    def get_values_from_line(self, line=None):
        try:
            if line is not None:
                coord = re.findall(r"[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?", line)
                coord_line = np.asarray(coord, dtype='float')
                self.x = coord_line[0]
                self.y = coord_line[1]
                self.z = coord_line[2]
                self.ipot = int(coord_line[3])
                self.distance = coord_line[-1]
                tag_match = re.findall(r"[A-Za-z0-9_.-]+", line)
                self.tag = tag_match[4]
                self.element_name = re.findall(r"[A-Z][a-z]?[0-9]?", line)[0]
        except Exception as err:
            error_txt = 'AtomDescription: Can not parse input line: "{}" \n'.format(line)
            logging.getLogger("error_logger").error(error_txt + repr(err))
            if Configuration.DEBUG:
                print()
                print(error_txt, repr(err))

    def generate_line(self):
        star = ' '
        if self.distance > Configuration.TARGET_ATOM_MAX_DISTANCE:
            self.is_comment = True
        if self.is_comment:
            star = '*'

        space_num = 14 - len(self.tag)
        if space_num < 1:
            space_num = 1
        space_txt = " "*space_num

        self.out_line = '{s}  {x:+.5f}   {y:+.5f}   {z:+.5f}  {ipot}  {tag}{spc}{dst:.5f}\n' \
            .format(
                    s=star,
                    x=self.x,
                    y=self.y,
                    z=self.z,
                    ipot=self.ipot,
                    tag=self.tag,
                    spc=space_txt,
                    dst=self.distance,
                    ).replace('+', ' ')
        # print(self.out_line)
        return self.out_line

    def generate_line_for_zero_ipot(self):
        star = ' '
        if self.distance > Configuration.TARGET_ATOM_MAX_DISTANCE:
            self.is_comment = True
        if self.is_comment:
            star = '*'

        space_num = 14 - len(self.tag)
        if space_num < 1:
            space_num = 1
        space_txt = " "*space_num

        self.out_line_for_zero_ipot = '{s}  {x:+.5f}   {y:+.5f}   {z:+.5f}  {ipot}  {tag}{spc}{dst:.5f}\n' \
            .format(
                    s=star,
                    x=self.x,
                    y=self.y,
                    z=self.z,
                    ipot=0,
                    tag=self.tag,
                    spc=space_txt,
                    dst=self.distance,
                    ).replace('+', ' ')
        # print(self.out_line)
        return self.out_line_for_zero_ipot

    def show(self):
        print_object_properties_value_in_table_form(self)


class FEFFinputVariable(Variable):
    def __init__(self):
        self.value = AtomDescription()
        self.target_ipot = Configuration.TARGET_ATOM_IPOT
        self.target_tag = Configuration.TARGET_ATOM_TAG
        self.output_string_base = ""
        self.output_string_base_for_zero_ipot = ""
        self.search_pattern_base = "  {ipot}  {tag}."
        self.input_line = None
        self.search_pattern = None
        self.search_pattern_zero_ipot = None

    def create_output_string(self):
        self.output_string = self.value.generate_line()
        return self.output_string

    def create_output_string_for_zero_ipot(self):
        self.output_string_base_for_zero_ipot = self.value.generate_line_for_zero_ipot()
        return self.output_string_base_for_zero_ipot

    def create_search_pattern(self):
        self.search_pattern = self.search_pattern_base.format(
            ipot=self.target_ipot,
            tag=self.target_tag)
        self.search_pattern_zero_ipot = self.search_pattern_base.format(
            ipot=0,
            tag=self.target_tag)
        return self.search_pattern, self.search_pattern_zero_ipot

    def rebuild(self):
        if self.reset_to_default_value:
            self.value = self.default_value
        if self.input_line is not None:
            self.value.get_values_from_line(self.input_line)
            self.create_output_string()
            self.create_output_string_for_zero_ipot()
            self.create_search_pattern()
        else:
            self.create_search_pattern()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    line = '   -1.87829   -0.00000   -0.66549  3  Yb-tetra.2    1.99270'
    line = '2.81744   -1.62665    1.93816  3  Yb-tetra.4    3.78687'
    obj = AtomDescription()
    obj.get_values_from_line(line)
    obj.show()
    obj.generate_line()
    obj.show()

    obj2 = FEFFinputVariable()
    obj2.input_line = line
    obj2.rebuild()
    obj2.show()




