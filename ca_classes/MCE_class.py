



class MCE_class:

    def __init__(self, ca_fire_simul, rep_number):
        self.ca_fire_simul = ca_fire_simul
        self.rep_number = rep_number

    def run(self, running_avg_step, running_var_stp, verbose, plot_results):


        self.ca_fire_simul.run()
