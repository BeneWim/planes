from copy import deepcopy

import numpy as np

from data import Data
from solver import Solver


class Approximation(Solver):
    def __init__(self, data: Data) -> None:
        self.data = data

        self.solution = None
        self.utilization = None
        self.bells = None

    def solve(self):
        if not self.utilization:
            schedule = np.zeros((self.data.num_teams, self.data.T))
            assigned_teams = [0 for _ in range(self.data.num_teams)]
            schedule, assigned_teams = self._ring_bell(schedule, [0], assigned_teams)

            bells = []
            for bell in range(self.data.num_bells):
                arr = []
                for team in range(self.data.num_teams):
                    arr.append(self._new_bell(schedule, team))

                median_time = int(np.ceil(np.median(arr)))
                bells.append(median_time)
                schedule, assigned_teams = self._ring_bell(schedule, bells, assigned_teams)

            self.utilization, self.solution, self.bells = np.sum(schedule), schedule, bells
        return self.utilization, self.solution, self.bells

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

    def _new_bell(self, schedule, team):
        return self._find_last_one_index(schedule[team])

    def _find_last_one_index(self, array):
        if np.any(array == 1):
            return np.where(array == 1)[0][-1] + 1
        else:
            raise ValueError("No 1 found")
