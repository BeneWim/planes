import numpy as np


class Data:
    def __init__(
        self,
        num_teams: int = 5,
        num_bells: int = 5,
        T: int = 20,
        max_time: int = 5,
        seed: int = 42,
        team_limit: int = 5,
    ) -> None:
        self.num_teams = num_teams
        self.num_bells = num_bells
        self.T = T
        self.max_time = max_time
        self.seed = seed
        self.team_limit = team_limit

        self.plane_services = []

        self.generator = np.random.default_rng(self.seed)

        self.generate_service_times()

    def generate_service_times(self):
        for i in range(self.num_teams):
            self.plane_services.append(self.random_integers_with_fixed_bells())

    # def random_integers_with_fixed_T(self):
    #     numbers = []
    #     remaining_sum = self.T

    #     for _ in range(self.num_bells):
    #         random_number = self.generator.integers(1, remaining_sum)
    #         numbers.append(random_number)

    #         if remaining_sum - random_number <= 1:
    #             break

    #         remaining_sum -= random_number

    #     if remaining_sum > 0:
    #         numbers.append(remaining_sum)

    #     return numbers

    def random_integers_with_fixed_bells(self):
        numbers = []
        remaining_sum = self.T
        distribution = self.generator.integers(1, 5)

        for _ in range(self.num_bells + 1):
            # random_number = self.generator.integers(
            #     1, min(remaining_sum, self.team_limit)
            # )
            random_number = int(self.sample_distribution(distribution))

            if remaining_sum - random_number <= 1:
                numbers.append(remaining_sum)

                break
            else:
                numbers.append(random_number)

                remaining_sum -= random_number

        return numbers

    def sample_distribution(self, num_distribution: int):
        if num_distribution == 1:
            return self.generator.integers(1, self.team_limit)
        elif num_distribution == 2:
            outcomes = [1, 2, 3, 4, 5]

            probabilities = [0.5, 0.3, 0.1, 0.05, 0.05]

            return np.random.choice(outcomes, size=1, p=probabilities)
        elif num_distribution == 3:
            outcomes = [5, 4, 3, 2, 1]

            probabilities = [0.5, 0.3, 0.1, 0.05, 0.05]

            return np.random.choice(outcomes, size=1, p=probabilities)
        elif num_distribution == 4:
            outcomes = [1, 2, 3, 4, 5]

            probabilities = [0.05, 0.25, 0.4, 0.25, 0.05]

            return np.random.choice(outcomes, size=1, p=probabilities)
        else:
            raise ValueError("num_distribution not supported")
