import numpy as np

from data import Data
from solver import Solver


class AverageApproximation(Solver):
    def __init__(self, data: Data) -> None:
        self.data = data

        self.bell_timing = self.data.T // (self.data.num_bells + 1)

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

        for index in range(self.data.num_bells + 1):
            bells.append(index * self.bell_timing)
            self._ring_bell(schedule, bells, assigned_teams)

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