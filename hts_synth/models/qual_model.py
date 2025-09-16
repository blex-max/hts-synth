from array import array
import math
from typing import Protocol, runtime_checkable, Any
from collections.abc import Sequence
import numpy as np
import pysam


@runtime_checkable
class HasQualArrayProtocol(Protocol):
    query_qualities: Sequence[int] | array[Any] | None


def refine_quals(
    query_qualities: Sequence[int] | array[Any] | None
) -> list[int] | None:
    """
    helper to minimise the pain of pysam types with qualities
    """
    if query_qualities is None:
        return None
    if isinstance(query_qualities, array):
        retq = map(int, query_qualities.tolist())
    else:
        retq = query_qualities
    return list(retq)


class NaiveQualModel:
    means: list[float]
    sds: list[float]

    def __init__(
            self,
            distribution_by_posn: list[tuple[float, float]]
    ):
        self.means = [x[0] for x in distribution_by_posn]
        self.sds = [x[1] for x in distribution_by_posn]

    def get_quality_scores(
            self,
            rng: np.random.Generator
    ) -> list[int]:
        sampled_quals = list(map(lambda x: int(rng.normal(*x)), zip(self.means, self.sds)))
            # NEAT: make sure score is in range and an int
            # alex: it bothers me that the modelled data would ever produce something outside that range
            # score = round(score)
            # if score > 42:
            #     score = 42
            # if score < 1:
            #     score = 1
        return sampled_quals

    @staticmethod
    def learn_quality_probabilities(
        fq: pysam.FastxFile,
    ):
        # ASSUMPTION: No length variance in reads input
        # NOTE: zip is really useful here since it exhausts on the shortest iterable
        # which means we can very quietly deal with slightly short sequences
        # TODO: Add entry if we find a longer read than we expected
        rinit = next(fq)
        # breakpoint()
        init_quals = refine_quals(rinit.get_quality_array())
        if init_quals is None:
            raise ValueError
        means = [WelfordsRunningMean(q) for q in init_quals]
        total_count = 1  # convenient
        distrib_by_pos: list[tuple[float, float]] = []
        for read in fq:
            total_count += 1
            quals = refine_quals(read.get_quality_array())
            if quals is None:
                raise ValueError
            for rm, val in zip(means, quals):
                rm.update(val)
        else:
            if total_count < 3:
                raise RuntimeError('iterator was too short!')
            for rm in means:
                rm.finalise()
                distrib_by_pos.append(rm.mean_and_sd)

        return distrib_by_pos


class WelfordsRunningMean:
    agg: tuple[int, float, float]
    finalised_mean: tuple[float, float, float] | None

    def __init__(
        self,
        init_val: int | float
    ):
        self.agg = (1, init_val, 0)
        self.finalised_mean = None

    # For a new value new_value, compute the new count, new mean, the new M2.
    # mean accumulates the mean of the entire dataset
    # M2 aggregates the squared distance from the mean
    # count aggregates the number of samples seen so far
    def update(
        self,
        new_value: int
    ) -> None:
        (count, mean, m2) = self.agg
        count += 1
        delta = new_value - mean
        mean += delta / count
        delta2 = new_value - mean
        m2 += delta * delta2
        self.agg = (count, mean, m2)

    # Retrieve the mean, variance and sample variance from an aggregate
    def finalise(
        self,
    ):
        (count, mean, M2) = self.agg
        if count < 2:
            raise RuntimeError('Insufficient observations to finalise')
        else:
            (mean, variance, sample_variance) = (mean, M2 / count, M2 / (count - 1))
            self.finalised_mean = (mean, variance, sample_variance)

    @property
    def mean_and_sd(
        self,
        population: bool = False
    ):
        """
        return finalised running mean with either the sample or the popluation standard deviation
        """
        if self.finalised_mean is None:
            raise RuntimeError('Aggregate has not been finalised')
        mean, variance, sample_variance = self.finalised_mean
        if population:
            sd = math.sqrt(variance)
        else:
            sd = math.sqrt(sample_variance)
        return mean, sd

    
