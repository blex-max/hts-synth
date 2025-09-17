from hts_synth.ref.reference import Reference
from hts_synth.reads import ReadGenerator

reference = Reference("example_reference.fa")

mutated_segment = reference.get_mutated_sequence("chr1", 1000, 1010, [1, 0, 0])
print(f"Mutated  = {mutated_segment.sequence} length = {len(mutated_segment.sequence)}")

generator = ReadGenerator(reference_segment, quality_model, error_probabilities)

for read in generator.emit_reads(10):
  print(read.query_sequence)
