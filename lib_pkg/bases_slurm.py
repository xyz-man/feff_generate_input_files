'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 31.08.2020
'''
from lib_pkg.bases import Variable


class SLURMVariable(Variable):
    output_string_base = "#SBATCH --{name}={val}\n"
    search_pattern_base = "#SBATCH --{}"

    def create_output_string(self):
        self.output_string = self.output_string_base.format(
            name=self.name,
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
        print('name: ', self.name)
        print('value: ', self.value)
        print('old_value: ', self.old_value)
        print('default_value: ', self.default_value)
        print('comment: ', self.comment)
        print('output_string: ', self.output_string)
        print('help_string: ', self.help_string)
        print('search_pattern: ', self.search_pattern)
        print('immutable: ', self.immutable)


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = SLURMVariable()
    obj.name = 'ntasks'
    obj.value = 5
    obj.help_string = """--ntasks=<number>
sbatch does not launch tasks, it requests an allocation of resources and submits a batch script. 
This option advises the Slurm controller that job steps run within the allocation will launch a 
maximum of number tasks and to provide for sufficient resources. The default is one task per node, 
but note that the --cpus-per-task option will change this default.
    """
    obj.rebuild()
    obj.show()

