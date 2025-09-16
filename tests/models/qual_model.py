import sys
import pysam
from hts_synth.models.qual_model import NaiveQualModel

fqpath = sys.argv[1]  # fragile I know
with pysam.FastxFile(fqpath) as tfq:
    learned_distribs = NaiveQualModel.learn_quality_probabilities(tfq)
