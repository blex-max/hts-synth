from hts_synth.ref.reference import Reference

reference = Reference("example_reference.fa")

original_segment = reference.get_sequence("chr1", 1000, 1010)
print(f"Original = {original_segment.sequence} length = {len(original_segment.sequence)}")

mutated_segment = reference.get_mutated_sequence("chr1", 1000, 1010, [1, 0, 0])
print(f"Mutated  = {mutated_segment.sequence} length = {len(mutated_segment.sequence)}")
