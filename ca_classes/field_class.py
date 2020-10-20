
import itertools
import numpy as np


class field:
    """ Class that contains all necessary info about the field and how is discretized in the simulation.
    """
    veg_type = {'agricultural': -0.3,
                'thickets': 0,
                'Hallepo-pine': 0.4}
    #Just example, should be mofified

    veg_density = {'sparse': -0.4,
                   'normal': 0,
                   'dense': 0.3}
    #Just example, should be mofified

    def __init__(self, dimension, wind_velocity = 0, wind_direction = [0, 0], cell_states = None, cell_heigh = None,
                 cell_veg_type = None, cell_veg_density = None, cell_size = 10):
        self.dimension = dimension
        self.wind_velocity = wind_velocity
        self.wind_direction = wind_direction

        if cell_states is None:
            cell_states = np.full(dimension, 1) #maybe should change 1 for a constant like FUEL
        self.cell_states = cell_states

        if cell_heigh is None:
            cell_heigh = np.zeros(dimension)
        self.cell_heigh = cell_heigh

        if cell_veg_type is None:
            cell_veg_type = np.full(dimension, self.veg_type['thickets'])
        self.cell_veg_type = cell_veg_type

        if cell_veg_density is None:
            cell_veg_density = np.full(dimension, self.veg_density['normal'])
        self.cell_veg_density = cell_veg_density

        self.cell_size = cell_size
        self.original_state = self.cell_states


    def set_states(self, state_mat):
        '''
        TO DO add funtionality to make sure is adding correct type of data and size
        :param state_mat:
        :return:
        '''
        self.cell_states = state_mat

    def set_heights(self, heights_mat):
        self.cell_heigh = heights_mat

    def reset_state(self):
        self.cell_states = self.original_state

