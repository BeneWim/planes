import matplotlib.pyplot as plt
import numpy as np

from solver import Solver


class Visualizer:
    def __init__(self, solver: Solver) -> None:
        self.solver = solver

    def show_schedule(self):
        plt.matshow(self.solver.solution)

        num_columns = self.solver.solution.shape[1]
        plt.xticks(ticks=np.arange(num_columns))

        plt.xticks(np.arange(-0.5, self.solver.solution.shape[1], 1), minor=True)
        plt.yticks(np.arange(-0.5, self.solver.solution.shape[0], 1), minor=True)

        # Enable grid for minor ticks (which are shifted)
        plt.grid(True, which='minor', axis='both', color='black', linestyle='--', linewidth=1)

        for bell in self.solver.bells:
            plt.axvline(x=bell - 0.5, color="green", linestyle="-", linewidth=5)
