from hts_synth.reads.read_generator import QualityModel, ReadGenerator
from hts_synth.ref.reference import Reference

reference = Reference("example_reference.fa")

mutated_segment = reference.get_mutated_sequence("chr1", 1000, 1010, [1, 0, 0])
print(f"Mutated  = {mutated_segment.sequence} length = {len(mutated_segment.sequence)}")

generator = ReadGenerator(reference.get_sequence("chr1", 1000, 1010), QualityModel())

for read in generator.emit_reads(10):
    print(read.query_sequence)
