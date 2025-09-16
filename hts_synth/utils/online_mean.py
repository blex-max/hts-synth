import math


class WelfordsRunningMean:
    """
    Quick implementation of Welford's online mean algorithm.

    Attributes:
        agg (tuple[int, float, float]): aggregate containing the total number of observations, and the accumulated mean and squared distance from the mean from those observations (m2)
    """

    agg: tuple[int, float, float]

    def __init__(self, init_val: int | float):
        """
        Initialise object.

        Args:
            init_val (int | float): the value of the first observation, to initialise the online mean with
        """
        self.agg = (1, init_val, 0)

    def update(self, new_value: int) -> None:
        """
        For a new observation, use the current aggregate to calculate the new aggregate (counts, mean, m2).
        """
        (count, mean, m2) = self.agg
        count += 1
        delta = new_value - mean
        mean += delta / count
        delta2 = new_value - mean
        m2 += delta * delta2
        self.agg = (count, mean, m2)

    def yield_moments(self, population: bool = False):
        """
        Return finalised running mean with either the sample or the popluation standard deviation.

        Args:
            population (bool): whether to return the sample or population sample deviaition
        """
        (count, mean, m2) = self.agg
        if count < 2:
            raise RuntimeError("Insufficient observations to finalise")
        if population:
            sd = math.sqrt(m2 / count)
        else:
            sd = math.sqrt(m2 / (count - 1))
        return mean, sd
