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
from lib_pkg.bases import Variable
import re
import numpy as np
import prettytable as pt
from cfg.config import *


class AtomDescription:
    x = None
    y = None
    z = None
    ipot = None
    tag = None
    element_name = None
    distance = None
    out_line = None
    is_comment = False

    def get_values_from_line(self, line=None):
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

    def generate_line(self):
        star = ' '
        if self.distance > TARGET_ATOM_MAX_DISTANCE:
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

    def show(self):
        x = pt.PrettyTable([
            'x',
            'y',
            'z',
            'ipot',
            'tag',
            'distance',
            'element',
        ])
        x.add_row(
            [
                self.x,
                self.y,
                self.z,
                self.ipot,
                self.tag,
                self.distance,
                self.element_name,
            ]
        )
        print(x)


class FEFFinputVariable(Variable):
    value = AtomDescription()
    target_ipot = TARGET_ATOM_IPOT
    target_tag = TARGET_ATOM_TAG
    output_string_base = ""
    search_pattern_base = "  {ipot}  {tag}."
    input_line = None

    def create_output_string(self):
        self.output_string = self.value.generate_line()
        return self.output_string

    def create_search_pattern(self):
        self.search_pattern = self.search_pattern_base.format(
            ipot=self.target_ipot,
            tag=self.target_tag)
        return self.search_pattern

    def rebuild(self):
        if self.reset_to_default_value:
            self.value = self.default_value
        if self.input_line is not None:
            self.value.get_values_from_line(self.input_line)
            self.create_output_string()
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

    obj2 = FEFFinputVariable()
    obj2.input_line = line
    obj2.rebuild()
    obj2.show()




