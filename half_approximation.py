import numpy as np

from data import Data
from solver import Solver


class HalfApproximation(Solver):
    def __init__(self, data: Data) -> None:
        self.data = data

        self.solution = None
        self.utilization = None
        self.bells = None

    def solve(self):
        if not self.utilization:
            self.utilization, self.solution, self.bells = self._solve()
        return self.utilization, self.solution, self.bells

    def _solve(self):
        bells = []

        schedule = np.zeros((self.data.num_teams, self.data.T))
        assigned_teams = [0 for _ in range(self.data.num_teams)]

        utilization = 0

        bells.append(0)

        self._ring_bell(schedule, bells, assigned_teams)

        for t in range(self.data.T):
            utilization_t = np.sum(schedule[:, t])

            utilization_new = (utilization * (t - bells[-1]) + utilization_t / self.data.num_teams) / (t + 1 - bells[-1])

            if utilization_new < 0.5:
                if len(bells) == self.data.num_bells + 1:
                    break
                bells.append(t)

                self._ring_bell(schedule, bells, assigned_teams)

                utilization = utilization_t / self.data.num_teams
            else:
                utilization = utilization_new

        return np.sum(schedule), schedule, bells[1:]
    
    def _ring_bell(self, schedule, bells, assigned_teams):
        bell_time = bells[-1]
        for team in range(self.data.num_teams):
            if bell_time < self.data.T:
                if schedule[team][bell_time] == 0:
                    new_plane = self.data.plane_services[team]

                    for i in range(new_plane[assigned_teams[team]]):
                        if bell_time + i < self.data.T:
                            schedule[team][bell_time + i] = 1

                    assigned_teams[team] = assigned_teams[team] + 1

        return schedule, assigned_teams