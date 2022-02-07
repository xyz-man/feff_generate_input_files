'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 01.02.2022
'''
from pymatgen.core import Lattice, Structure, Element
from pymatgen.io.feff.inputs import Header, Atoms, Tags, Potential
from pprint import pprint
from cfg.class_cfg import Configuration, BaseClass, JsonClassSerializable


class FEFFLatticeStructure(BaseClass):
    def __init__(self):
        self.lattice = None

        # [Element('Zn'), Element('O')]:
        self.species = None
        self.space_group_number = None

        # [ [1 / 3, 2 / 3, 0.00000],
        #   [1 / 3, 2 / 3, 0.37780], ]:
        self.atoms_coord = None
        self.atom_coords_are_cartesian = False
        self.structure_tolerance = 1e-9
        self.structure = None
        self.cluster_size = None
        self.absorbing_atom = None
        self.path_to_src_feff_input = None
        self.path_to_out_feff_input = None

        # struct: Structure object, See pymatgen.core.structure.Structure.
        #     source: User supplied identifier, i.e. for Materials Project this
        #         would be the material ID number
        #     comment: Comment for first header line
        self.header_user_identifier = None
        self.header_comment = None
        self._header = None
        self._tags = None
        self._atoms = None
        self._potentials = None

        self.is_load_potentials_from_file = False

    def init(self):
        self.init_structure()
        self.init_header()
        self.init_atoms()
        self.init_potentials()
        self.init_tags()

    def init_header(self):
        self._header = Header(struct=self.structure, source=self.header_user_identifier, comment=self.header_comment)

    def init_structure(self):
        self.structure = Structure.from_spacegroup(
            sg=self.space_group_number,
            lattice=self.lattice,
            species=self.species,
            coords=self.atoms_coord,
            coords_are_cartesian=self.atom_coords_are_cartesian,
            tol=self.structure_tolerance,
        )

    def init_tags(self):
        self._tags = Tags().from_file(filename=self.path_to_src_feff_input)

    def init_potentials(self):
        if self.is_load_potentials_from_file:
            self._potentials = Potential(struct=self.structure, absorbing_atom=self.absorbing_atom). \
                pot_string_from_file(self.path_to_src_feff_input)
        else:
            self._potentials = Potential(struct=self.structure, absorbing_atom=self.absorbing_atom)

    def init_atoms(self):
        self._atoms = Atoms(
            struct=self.structure,
            absorbing_atom=self.absorbing_atom,
            radius=self.cluster_size
        )

    def write_file(self):
        with open(self.path_to_out_feff_input, "w") as f:
            f.write(str(self._header) + "\n")
            f.write(str(self._tags) + "\n")
            f.write(str(self._potentials) + "\n")
            f.write(str(self._atoms) + "\n")


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    zno_lattice_init = Lattice.from_parameters(
        a=3.25330, b=3.25330, c=5.20730,
        alpha=90.00000, beta=90.00000, gamma=120.00000,
    )
    zno_structure = Structure.from_spacegroup(
        sg=186, lattice=zno_lattice_init,
        species=[Element('Zn'), Element('O')],
        coords=[
            [1 / 3, 2 / 3, 0.00000],
            [1 / 3, 2 / 3, 0.37780],
        ],
        coords_are_cartesian=False,
        tol=1e-9,
    )
    print(zno_structure)
    print(zno_structure.get_space_group_info())
    out_file_name = '/home/yugin/PycharmProjects/neurons/data/src/feff.inp.new2'
    file_name = '/home/yugin/PycharmProjects/neurons/data/src/feff.inp.old'
    atoms_obj = Atoms(zno_structure, 'O', 12)
    pprint(atoms_obj.struct.cart_coords)
    pprint(atoms_obj.get_lines())

    header_obj = Header(struct=zno_structure)
    pot_obj = Potential(zno_structure, 'O')


    tags_obj = Tags().from_file(filename=file_name)
    pprint(tags_obj.as_dict())

    pot_obj.pot_string_from_file(filename=file_name)
    pprint(pot_obj)
    atoms_obj.atoms_string_from_file(filename=file_name)
    pprint(atoms_obj.as_dict())

    header_obj.write_file(out_file_name)
    tags_obj.write_file(out_file_name)
    pot_obj.write_file(out_file_name)
    atoms_obj.write_file(out_file_name)
    # paths_obj = Paths()
    # header_obj.from_file(file_name)
    print()