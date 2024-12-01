from solver import Solver
from data import Data


class GurobiSolver(Solver):
    def __init__(self, data: Data) -> None:
        self.data = data
