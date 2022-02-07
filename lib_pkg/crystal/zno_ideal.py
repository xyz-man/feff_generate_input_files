'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 01.02.2022
'''
import os
from pymatgen.core import Lattice, Structure, Element
from pymatgen.io.feff.inputs import Header, Atoms, Tags, Potential
from pprint import pprint
from lib_pkg.crystal.feff_sucture import FEFFLatticeStructure
from cfg.class_cfg import Configuration


class ZnOCrystalMixin(FEFFLatticeStructure):
    def __init__(self):
        super(ZnOCrystalMixin, self).__init__()
        self.lattice = Lattice.from_parameters(
            a=3.25330, b=3.25330, c=5.20730,
            alpha=90.00000, beta=90.00000, gamma=120.00000,
        )
        self.species = [Element('Zn'), Element('O')]
        self.space_group_number = 186
        self.atoms_coord = [
            [1 / 3, 2 / 3, 0.00000],
            [1 / 3, 2 / 3, 0.37780],
        ]
        self.atom_coords_are_cartesian = False
        self.structure_tolerance = 1e-9
        self.structure = None
        self.cluster_size = 12
        self.absorbing_atom = "O"
        self.path_to_src_feff_input = '/home/yugin/PycharmProjects/neurons/data/src/feff.inp.old'
        self.path_to_out_feff_input = '/home/yugin/PycharmProjects/neurons/data/src/feff.inp.new2'

        # struct: Structure object, See pymatgen.core.structure.Structure.
        #     source: User supplied identifier, i.e. for Materials Project this
        #         would be the material ID number
        #     comment: Comment for first header line
        self.header_user_identifier = 'author: Yevgen Syryanyy'
        self.header_comment = 'Automatic generated feff.inp file'


class ZnOCrystalStructure(ZnOCrystalMixin):
    def __init__(self):
        super(ZnOCrystalStructure, self).__init__()
        self.a = 3.25330
        self.b = 3.25330
        self.c = 5.20730
        self.path_to_src_feff_input = Configuration.PATH_TO_SRC_FEFF_INPUT_FILE
        self.is_load_potentials_from_file = True

    def init(self):
        self.lattice = Lattice.from_parameters(
            a=self.a,
            b=self.b,
            c=self.c,
            alpha=90.00000, beta=90.00000, gamma=120.00000,
        )
        super(ZnOCrystalStructure, self).init()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    zno_obj = ZnOCrystalStructure()
    zno_obj.cluster_size = 6
    zno_obj.init()
    zno_obj.show_properties()
    # pprint(zno_obj.show_properties())
    zno_obj.encode_('test_zno.txt')
    # zno_obj.write_file()