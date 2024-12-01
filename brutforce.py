from copy import deepcopy

import numpy as np

from data import Data
from solver import Solver


class Brutforce(Solver):
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

            self.utilization, self.solution, self.bells = self._solve([], schedule, assigned_teams)
        return self.utilization, self.solution, self.bells

    def _solve(self, bells, schedule, assigned_teams):
        if len(bells) == self.data.num_bells:
            return np.sum(schedule), schedule, bells

        utilizations = []
        schedules = []
        sol_bells = []

        for team in range(self.data.num_teams):
            new_schedule = deepcopy(schedule)
            new_assigned_teams = deepcopy(assigned_teams)
            new_bells = deepcopy(bells)

            bell = self._new_bell(new_schedule, team)

            new_bells.append(bell)

            new_schedule, new_assigned_teams = self._ring_bell(
                new_schedule, new_bells, new_assigned_teams
            )

            utilization, sol_schedule, sol_bell = self._solve(
                new_bells, new_schedule, new_assigned_teams
            )

            utilizations.append(utilization)
            schedules.append(sol_schedule)
            sol_bells.append(sol_bell)

        index = utilizations.index(max(utilizations))
        return utilizations[index], schedules[index], sol_bells[index]

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
