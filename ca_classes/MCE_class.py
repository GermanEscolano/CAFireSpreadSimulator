


import numpy as np
import matplotlib.pyplot as plt

class MCE:

    rep_count = 0

    def __init__(self, ca_fire_simul, rep_number):
        self.ca_fire_simul = ca_fire_simul
        dimension = self.ca_fire_simul.field.dimension
        self.rep_number = rep_number
        self.running_avg = np.zeros(dimension)
        self.running_var = np.zeros(dimension)

    def run(self, running_avg_step = 0, running_var_step = 0, verbose = False, plot_results = False):
        self.rep_count = 0
        s_k = 0
        while self.rep_count < self.rep_number:
            print(f'Replication {self.rep_count} / {self.rep_number}')  ################
            self.ca_fire_simul.field.reset_state()
            self.ca_fire_simul.start_fire()
            current_cell_state = self.ca_fire_simul.run()
            last_running_avg = self.running_avg

            self.running_avg = self.running_avg + (
                current_cell_state - self.running_avg) / (self.rep_count + 1)

            s_k = s_k + (current_cell_state - self.running_avg) * (
                current_cell_state - last_running_avg)
            self.running_var = s_k / (self.rep_count + 1)

            self.rep_count += 1

        return self.running_avg

    def plot(self):
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        ax3.imshow(self.running_avg)
        plt.show()


if __name__ == '__main__':
    from ca_classes import field_class, fire_simulation_class

    field_obj = field_class.field([300, 300])

    fire_simul_obj = fire_simulation_class.fire_simulation(field_obj, [(5, 5)], 1000)

    fire_simul_obj.start_fire()

    MCE_obj = MCE(fire_simul_obj, 10)

    final_prob_burn = MCE_obj.run()

    print(final_prob_burn)

    final_state = fire_simul_obj.run()

    fig1, ax1 = plt.subplots(figsize=(8, 6))

    ax1.imshow(final_prob_burn)
    plt.show()
