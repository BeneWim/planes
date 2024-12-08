import numpy as np

class Data:
    def __init__(
        self,
        num_teams: int = 5,
        num_bells: int = 5,
        T: int = 20,
        distribution: str = "normal",
        max_time: int = 5,
        sum_to_T: bool = False,
        equal_assignment: bool = False,
        seed: int = 42,
        team_limit: int = 5,
    ) -> None:
        self.num_teams = num_teams
        self.num_bells = num_bells
        self.T = T
        self.distribution = distribution
        self.max_time = max_time
        self.sum_to_T = sum_to_T
        self.equal_assignment = equal_assignment
        self.seed = seed
        self.team_limit = team_limit

        self.plane_services = []

        self.generator = np.random.default_rng(self.seed)

        self.generate_service_times()

    def generate_service_times(self):
        for i in range(self.num_teams):
            self.plane_services.append(self.random_service_times())

    def random_service_times(self):
        if self.distribution == "normal":
            if self.sum_to_T:
                return self.random_integers_with_fixed_T()
            else:
                return self.random_integers_with_fixed_bells()
        else:
            raise ValueError("distribution not supported")

    # def random_integers_with_fixed_T(self):
    #     random_points = sorted(self.generator.sample(range(1, self.T),  - 1))

    #     # Include 0 and target_sum to form partitions
    #     random_points = [0] + random_points + [target_sum]

    #     # Compute differences between consecutive points
    #     random_integers = [random_points[i + 1] - random_points[i] for i in range(x)]

    #     return random_integers

    def random_integers_with_fixed_T(self):
        numbers = []
        remaining_sum = self.T

        for _ in range(self.num_bells):
            random_number = self.generator.integers(1, remaining_sum)
            numbers.append(random_number)

            if remaining_sum - random_number <= 1:
                break

            remaining_sum -= random_number

        if remaining_sum > 0:
            numbers.append(remaining_sum)

        return numbers

    def random_integers_with_fixed_bells(self):
        numbers = []
        remaining_sum = self.T

        for _ in range(self.num_bells + 1):
            random_number = self.generator.integers(
                1, min(remaining_sum, self.team_limit)
            )

            if remaining_sum - random_number <= 1:
                numbers.append(remaining_sum)

                break
            else:
                numbers.append(random_number)

            remaining_sum -= random_number

        return numbers
