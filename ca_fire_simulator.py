import time

import numpy as np
import itertools
import matplotlib.pyplot as plt

from ca_classes.field_class import field
from ca_classes.fire_simulation_class import fire_simulation


script_start_time = time.time()

# fire_event_ca_simulation.verbose = True

dimension = [100, 100]
wind_velocity = 3
wind_direction = [1, 1]

final_burned_prob = np.zeros(dimension)

num_replications = 3
replication_counter = 1

num_periods = 1000

test_cell_states = np.full(dimension, 1)
for coord in itertools.product(*[range(dim) for dim in dimension]):
    if coord[0] in list(range(40, 60)) and coord[1] in list(range(70, 80)):
        test_cell_states[coord] = 0

test_cell_height = np.zeros(dimension)
for i in range(dimension[0]):
    for j in range(dimension[1]):
        test_cell_height[i, j] = 2 * np.sqrt(i ** 2 + j ** 2)

field_obj = field(dimension=dimension,
                  wind_velocity=wind_velocity,
                  wind_direction=wind_direction,
                  cell_states=test_cell_states,
                  cell_heigh=test_cell_height)

fig1, ax1 = plt.subplots(2, 2, figsize=(8, 6))
ax1[0, 0].set_title('Cell Heights')
h_ax = ax1[0, 0].imshow(field_obj.cell_heigh)
fig1.colorbar(h_ax, ax=ax1[0, 0])
ax1[0, 1].set_title('Wind direction and intensity')
ax1[0, 1].text(0.95, 0.01, f'Wind velocity: {field_obj.wind_velocity} m/s',
               verticalalignment='bottom', horizontalalignment='right',
               transform=ax1[0, 1].transAxes,
               color='green', fontsize=15)
ax1[0, 1].quiver([0], [0], [field_obj.wind_direction[0]], [field_obj.wind_direction[1]], angles='xy', scale_units='xy',
                 scale=field_obj.wind_velocity)
ax1[0, 1].set_xlim(-1, 1)
ax1[0, 1].set_ylim(-1, 1)
ax1[1, 0].set_title('Vegetation type')
ax1[1, 0].imshow(field_obj.cell_veg_type)
ax1[1, 1].set_title('Vegetation density')
ax1[1, 1].imshow(field_obj.cell_veg_density)

fig2, ax2 = plt.subplots(figsize=(8, 6))

replications_start_time = time.time()
while replication_counter <= num_replications:

    field_obj.reset_state()

    fire_simulation_obj = fire_simulation(field_obj, [(50, 50)])

    fire_simulation_obj.set_fire()

    still_fire = True

    period_counter = 1

    period_start_time = time.time()
    while period_counter <= num_periods and still_fire:

        fire_simulation_obj.evolve()

        ax2.clear()
        ax2.set_title('Ongoing simulation')
        ax2.text(105, 5, f'Replication: {replication_counter}')
        ax2.text(105, 10, f'Period: {period_counter}')
        ax2.imshow(fire_simulation_obj.field.cell_states)
        plt.draw()
        plt.pause(0.001)

        period_counter += 1

        if np.any(fire_simulation_obj.field.cell_states == 2):
            still_fire = True
        else:
            still_fire = False

        avg_period_time = (time.time()-period_start_time) / num_periods

    replication_counter += 1

    final_burned_prob = final_burned_prob + (
            fire_simulation_obj.field.cell_states - final_burned_prob) / replication_counter

avg_replication_time = (time.time() - replications_start_time) / num_replications
plt.close(fig2)

print("---One periord avg execution time: %s seconds ---" % (avg_period_time))
print("---One replication avg execution time: %s seconds ---" % (avg_replication_time))
print("---Script execution time: %s seconds ---" % (time.time() - script_start_time))


fig3, ax3 = plt.subplots(figsize=(8, 6))
ax3.set_title('Final results')
ax3.imshow(final_burned_prob)
plt.show()
