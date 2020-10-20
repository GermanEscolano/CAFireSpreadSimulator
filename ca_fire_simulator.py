import numpy as np
import itertools

from ca_classes.field_class import field
from ca_classes.fire_simulation_class import fire_simulation
from ca_classes.MCE_class import MCE

########### External data ############

dimension = [100, 100]

test_cell_states = np.full(dimension, 1)
for coord in itertools.product(*[range(dim) for dim in dimension]):
    if coord[0] in list(range(40, 60)) and coord[1] in list(range(70, 80)):
        test_cell_states[coord] = 0

test_cell_height = np.zeros(dimension)
for i in range(dimension[0]):
    for j in range(dimension[1]):
        test_cell_height[i, j] = 4 * np.sqrt(i ** 2 + j ** 2)

#######################################

field_obj = field(dimension=dimension,
                  wind_velocity=6,
                  wind_direction=[0,1],
                  cell_states=test_cell_states,
                  cell_height=test_cell_height,
                  cell_veg_type=0,
                  cell_veg_density=0,
                  cell_size=10)

field_obj.plot()

fire_simul_obj = fire_simulation(field=field_obj,
                                 fire_origin=[(50, 50)],
                                 max_period_num=10,
                                 plot=True)

MCE_obj = MCE(ca_fire_simul=fire_simul_obj,
              rep_number=3)

MCE_obj.run()

MCE_obj.plot()

