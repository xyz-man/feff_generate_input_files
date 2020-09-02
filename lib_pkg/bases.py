'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
from cfg.class_cfg import print_object_properties_value_in_table_form


class Variable:
    name = ''
    value = None
    default_value = None
    old_value = None
    comment = ''
    help_string = ''
    output_string = ''
    search_pattern = ''
    # variable will be change:
    immutable = False
    reset_to_default_value = False
    output_string_base = "  integer,parameter :: {nm} = {val}     ! {com}\n"
    search_pattern_base = 'parameter :: {} '

    def rebuild(self):
        if self.reset_to_default_value:
            self.value = self.default_value
        self.create_output_string()
        self.create_search_pattern()

    def create_output_string(self):
        if self.comment:
            self.output_string = self.output_string_base.format(
                nm=self.name,
                val=self.value,
                com=self.comment,
            )
        else:
            self.output_string = "  integer,parameter :: {nm} = {val}\n".format(
                nm=self.name,
                val=self.value,
            )
        return self.output_string

    def create_search_pattern(self):
        self.search_pattern = self.search_pattern_base.format(self.name)
        return self.search_pattern

    def flush(self):
        self.name = ''
        self.value = None
        self.default_value = None
        self.old_value = None
        self.comment = ''
        self.help_string = ''
        self.output_string = ''
        self.search_pattern = ''
        self.immutable = False

    def show(self):
        print_object_properties_value_in_table_form(self)


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = Variable()
    obj.name = 'nclxtd'
    obj.value = 100
    obj.comment = 'Maximum number of atoms for tdlda module.'
    obj.rebuild()
    obj.show()

