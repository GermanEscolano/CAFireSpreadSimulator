import itertools
import random
import numpy as np

from . import neighborhood
from .field_class import field

class fire_simulation:
    neighborhood_obj = neighborhood.MooreNeighborhood(neighborhood.EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS)

    p_h = 0.3
    C1 = 0.045
    C2 = 0.131
    C3 = 0.19

    verbose = False

    def __init__(self, field, fire_origin):
        self.field = field
        self.fire_origin = fire_origin

    def evolve(self):
        new_cell_states = np.copy(self.field.cell_states)
        for coord in itertools.product(*[range(dim) for dim in self.field.dimension]):
            if fire_simulation.verbose: print(f'Evaluated cell: {coord}')
            if self.field.cell_states[coord] == 1:
                prob_no_set_fire = self.get_cell_prob_no_burn(coord)
                if random.random() > prob_no_set_fire:
                    new_cell_states[coord] = 2
            elif self.field.cell_states[coord] == 2:
                new_cell_states[coord] = 3
        self.field.cell_states = new_cell_states

    def get_cell_prob_no_burn(self, coord):
        coord_neigs = self.neighborhood_obj.calculate_cell_neighbor_coordinates(coord, self.field.dimension)

        if fire_simulation.verbose: print(f'Neig cells: {coord_neigs}')

        list_prob_propagate_from_neig = []

        for coord_neig in coord_neigs:
            coord_neig = tuple(coord_neig)
            if self.field.cell_states[coord_neig] == 2:
                prob_propagate_cell_to_cell = self.get_prob_propagate_from_neig(coord, coord_neig)
                list_prob_propagate_from_neig.append(prob_propagate_cell_to_cell)
                if fire_simulation.verbose: print(f'Burning_neig: {coord_neig} ---> prob fire propagates = {prob_propagate_cell_to_cell}')

        cell_prob_no_burn = np.prod([1 - elem for elem in list_prob_propagate_from_neig])

        if fire_simulation.verbose: print(f'Prob evaluated cell does not set on fire: {cell_prob_no_burn}')
        if fire_simulation.verbose: print(f'------------')

        return cell_prob_no_burn

    def get_prob_propagate_from_neig(self, coord_orig, coord_neig):

        p_veg = self.field.cell_veg_type[coord_neig]

        p_den = self.field.cell_veg_density[coord_neig]

        V = self.field.wind_velocity
        wind_direction = self.field.wind_direction
        vector_from_neig_to_orig = np.array(coord_orig) - np.array(coord_neig)

        propagation_wind_angle = self.angle_between_vectors(vector_from_neig_to_orig, wind_direction)
        f_t = np.exp(self.C2 * V * (np.cos(propagation_wind_angle)))
        p_w = f_t * np.exp(self.C1 * V)

        height_neig = self.field.cell_heigh[coord_neig]
        height_orig = self.field.cell_heigh[coord_orig]

        p_heigh = np.exp(self.C3 * (height_orig - height_neig))

        return self.p_h * (1 + p_veg) * (1 + p_den) * p_w * p_heigh

    def set_fire(self):
        for coord in self.fire_origin:
            self.field.cell_states[coord] = 2

    def set_fire_parameters(self, p_h, C1, C2, C3):
        self.p_h = p_h
        self.C1 = C1
        self.C2 = C2
        self.C3 = C3


    @staticmethod
    def angle_between_vectors(v1, v2):
        if type(v1) is tuple or type(v1) is tuple:
            v1 = np.array(v1)
            v2 = np.array(v2)
        """ Returns the angle in radians between vectors 'v1' and 'v2'::"""
        return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))


if __name__ == '__main__':

    field_obj = field([10, 10])

    fire_simul_obj = fire_simulation(field_obj, [(2, 2)])

    fire_simul_obj.set_fire_parameters(1,2,3,4)

    print(fire_simulation.C1)
    print(fire_simul_obj.C1)


