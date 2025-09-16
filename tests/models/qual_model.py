import sys
import pysam
from hts_synth.models.qual_model import NaiveQualModel
from numpy.random import default_rng

fqpath = sys.argv[1]  # fragile I know
with pysam.FastxFile(fqpath) as tfq:
    learned_distribs = NaiveQualModel.learn_quality_probabilities(tfq)
    qual_gen = NaiveQualModel(learned_distribs)
    np_rng = default_rng(24601)
    example_score= qual_gen.get_quality_scores(np_rng)
    # I suggest putting a breakpoint here and inspecting stuff
