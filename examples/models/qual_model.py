import sys

import pysam
from numpy.random import default_rng

from hts_synth.models.qual_model import NaiveQualLearner, NaiveQualSim

fqpath = sys.argv[1]  # fragile I know
np_rng = default_rng(24601)
with pysam.FastxFile(fqpath) as tfq:
    learned_distribs = NaiveQualLearner.model_from_fastq(tfq)
    qual_gen = NaiveQualSim(learned_distribs, np_rng)
    example_score_iter = qual_gen.yield_n(10)
    # I suggest putting a breakpoint here and inspecting stuff
