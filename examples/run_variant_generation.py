from hts_synth.ref.generate_variant import VariantGenerator
from hts_synth.ref.seq_converter import apply_variants

full_reference_sequence = "ACTTGGAAGTTCGA"

segment_reference_sequence = "ACTTGGAAGT"

print(f"Original = {segment_reference_sequence}")

generator = VariantGenerator(ref_sequence=segment_reference_sequence, events=[1, 0, 0])

variants = generator.generate_random_variant_sequence()

for var in variants:
    print(var)

modified_segment_sequence = apply_variants(
    ref_start=0, ref_seq=full_reference_sequence, alt_length=len(variants), variants=variants
)

print(f"Modified = {modified_segment_sequence}")
