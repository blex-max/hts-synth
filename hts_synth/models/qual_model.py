from array import array
from collections.abc import Sequence
from typing import Any
import numpy as np
import pysam

from hts_synth.utils.online_mean import WelfordsRunningMean


def refine_quals(query_qualities: Sequence[int] | array[Any] | None) -> list[int] | None:
    """
    Modfiy common iterables of quality scores into a standard list int.

    Mostly a helper to minimise the pain of pysam types with qualities - whatever they are, get them into a list[int] or None

    Args:
        query_qualities (Sequence[int] | array[Any] | None): unprocessed qualities (probably from a pysam method)
    """
    if query_qualities is None:
        return None
    if isinstance(query_qualities, array):
        retq = map(int, query_qualities.tolist())
    else:
        retq = query_qualities
    return list(retq)


class NaiveQualModelBase:
    pass


class NaiveQualSim(NaiveQualModelBase):
    """
    A naive model of base quality which can simulate quality arrays based on input per-position normal distributions.

    - assumes positions are entirely independent
    - has no sense of genomic position
    - is totally independent of bases/other features
    For each position the model simply samples a score from a normal distribution with the provided mean and (sample) SD.
    Read length is implicit to the length of the model parameters provided at init.

    The class also contains an online learning algorithm to learn parameters from an input pysam.FastxFile (fastq).
    The algorithm uses Welford's Running Mean so as to be reasonably efficient.

    Attributes:
        means (list[float]): Model parameter, distribution means of quality by position
        sds (list[float]): Model paramter, distribution of standard deviations of quality by position
    """

    means: list[float]
    sds: list[float]
    _rng: np.random.Generator

    def __init__(
        self,
        distribution_by_posn: list[tuple[float, float]],
        rng: np.random.Generator | None = None,  # default None will instantiate an unseeded generator for you
        default_seed: int = 24601
    ):
        """
        Initialise object.
        
        Args:
            distribution_by_posn (list[tuple[float, float]]): The model from which the object will simulate quality. Tuples of mean and standard deviation up to desired read length
            rng (numpy.random.Generator): Random number generator that the object should use during simulation, usually provided via numpy.random.default_rng()
        """
        self.means = [x[0] for x in distribution_by_posn]
        self.sds = [x[1] for x in distribution_by_posn]
        if rng is not None:
            self._rng = rng
        else:
            self._rng = np.random.default_rng(default_seed)

    def _yield_result(
        self,
    ) -> list[int]:
        sampled_quals = [int(self._rng.normal(*x)) for x in zip(self.means, self.sds)]
        return sampled_quals

    def yield_n(self, n: int):
        """
        Return n simulated quality arrays.

        Args:
            n (int): total number of results to return
        """
        for _ in range(n):
            yield self._yield_result()


class NaiveQualLearner(NaiveQualModelBase):
    """
    Online learning algorithm for building model parameters from real data, from which NaiveQualSim can then simulate data.

    Attributes:
        online_means (list[WelfordsRunningMean]): online learner for each position
        nobs (int): number of observations
    """

    online_means: list[WelfordsRunningMean]
    _nobs: int

    def __init__(self, initial_qualities: list[int]) -> None:
        """
        Initialise object.
        
        Args:
            initial_qualities (list[int]): the first observation from data, with which to prime the learner instance (i.e. start the online means)
        """
        self.online_means = [WelfordsRunningMean(q) for q in initial_qualities]
        self._nobs = 1

    def update(self, new_quals: list[int]):
        """
        Update the online means for each position.

        Args:
            new_quals (list[int]): quality scores of the new observation
        """
        for rm, val in zip(self.online_means, new_quals):  # zip exhausts on shortest iterable
            rm.update(val)
        self._nobs += 1

    @property
    def observations(
        self
    ):
        """
        Number of total observations the model has learned from so far.
        """
        return self._nobs

    def yield_model(self):
        """
        Return distribution model of quality score for each position as learned so far.
        """
        model: list[tuple[float, float]] = []
        for rm in self.online_means:
            model.append(rm.yield_moments())

        return model

    @classmethod
    def model_from_fastq(
        cls,
        fq: pysam.FastxFile,
    ):
        """
        From a fastq file handle as opened by pysam, learn a model from that data.

        Args:
            fq (pysam.FastxFile): Open pysam file handle to fastq
        """
        # ASSUMPTION: No length variance in reads input
        # NOTE: zip is really useful here since it exhausts on the shortest iterable
        # which means we can very quietly deal with slightly short sequences
        # TODO: Add entry if we find a longer read than we expected
        rinit = next(fq)
        init_quals = refine_quals(rinit.get_quality_array())
        if init_quals is None:
            raise ValueError

        learner = cls(init_quals)

        for read in fq:
            quals = refine_quals(read.get_quality_array())
            if quals is None:
                raise ValueError
            learner.update(quals)
        else:
            return learner.yield_model()
