from solver import Solver
from data import Data
import gurobipy as gp
from gurobipy import GRB

class GurobiSolver(Solver):
    def __init__(self, data: Data) -> None:
        self.data = data

    def solve(self) -> None:

        # Example data (adjust as needed)
        self.data.num_teams = 3  # Number of teams
        m = [3, 2, 4]  # Number of planes per team
        # service_times = [[1, 2, 3], [2, 3], [4, 1, 2, 3]]  # Service times for each plane
        # B = 20  # Number of bell rings
        self.data.plane_services
        # T = 100  # Time horizon

        # Create a model
        model = gp.Model("airport_bell_schedule")

        # Decision Variables
        # b_i integer variable representing the time at which bell b rings (i.e., when the bell is signaled for a team to depart a plane).
        b = model.addVars(self.data.num_bells + 1, vtype=GRB.INTEGER, name="b")

        # Waiting time for each plane p of team i 
        w = {}
        for i in range(self.data.num_teams): 
            for p in range(len(self.data.plane_services[i])):  # For each plane in team i
                w[i, p] = model.addVar(vtype=GRB.CONTINUOUS, name=f"w_{i}_{p}")

        # Start time for each plane p of team i
        st = {}
        for i in range(self.data.num_teams): 
            for p in range(len(self.data.plane_services[i])):  # For each plane in team i
                st[i, p] = model.addVar(vtype=GRB.INTEGER, name=f"st_{i}_{p}")

        x = {}
        for i in range(self.data.num_teams):
            for p in range(len(self.data.plane_services[i])):  # For each plane in team i
                for j in range(self.data.num_bells + 1):
                    x[i, p, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{p}_{j}")

        # Minimize the total waiting time for all teams
        model.setObjective(gp.quicksum(w[i, p] for i in range(n) for p in range(len(self.data.plane_services[i]))), GRB.MINIMIZE)


        # CONSTRAINTS

        # Max number of bells that can ring at the
        for i in range(self.data.num_teams):
            for p in range(len(self.data.plane_services[i])):
                model.addConstr(gp.quicksum(x[i, p, j] for i in range(self.data.num_bells + 1)) <= 1)
                    
        # Add that first bell is at time 0 and plane 0 of all teams starts at time 0
        model.addConstr(b[0] == 0)
        for i in range(self.data.num_teams):
            model.addConstr(st[i, 0] == 0)


        # 1. Each plane in a team must be serviced in order
        # 2. Waiting time for each team at each plane is the diffrence between the start time of the service + service time and the next start time
        for i in range(self.data.num_teams):
            for p in range(len(self.data.plane_services[i]) - 1):
                model.addConstr(st[i, p] + self.data.plane_services[i][p] <= st[i, p + 1])
                model.addConstr(w[i, p] == st[i, p + 1] - (st[i, p] + self.data.plane_services[i][p]))

        # Add the waiting time after the last plane of each team
        for i in range(self.data.num_teams):
            model.addConstr(w[i, len(self.data.plane_services[i]) - 1] == self.data.T - (st[i, len(self.data.plane_services[i]) - 1] + self.data.plane_services[i][len(self.data.plane_services[i]) - 1]))


        # 3. Bell ring times must be ordered
        for i in range(self.data.num_bells - 1):
            model.addConstr(b[i] <= b[i + 1])
        # model.addConstr(b[self.data.num_bells - 1] <= self.data.T)

        # 4. Connect the bell ring times to the start times of the teams
        for i in range((min(self.data.num_teams, self.data.num_bells))):
            for p in range(len(self.data.plane_services[i])):
                model.addConstr(b[i] <= st[i, p])

        # Solve the model
        model.optimize()

        # Print the optimal solution
        if model.status == GRB.OPTIMAL:
            for i in range(self.data.num_teams):
                for p in range(len(self.data.plane_services[i])):
                    print(f"Team {i} Plane {p} starts at {st[i, p].x}")
            for i in range(self.data.num_bells):
                print(f"Bell {i} rings at {b[i].x}")
        else:
            print("No optimal solution found.")