import pysam

from ..ref.generate_variant import VariantGenerator
from ..ref.seq_converter import apply_variants


class ReferenceSegment:
    def __init__(self, chrom: str, start: int, end: int, sequence: str):
        self.chrom = chrom
        self.start = start
        self.end = end
        self.sequence = sequence


class Reference:
    def __init__(self, fasta_path: str):
        """
        Initialise a Reference to hold reference information
        """
        self.fasta = pysam.FastaFile(fasta_path)

    def get_sequence(self, chrom: str, start: int, end: int):
        """
        Returns a ReferenceSegment object.
        Coordinates are 0-based, end-exclusive.
        """
        seq = self.fasta.fetch(chrom, start, end)
        return ReferenceSegment(chrom, start, end, seq)
    
    def get_mutated_sequence(self, chrom: str, start: int, end: int, events: list):
        """
        Returns a ReferenceSegment object.
        Coordinates are 0-based, end-exclusive.
        """
        if len(events) != 3:
            raise ValueError("Events should contain 3 values - number of insertions, number of deletions, number of substitutions")
        num_ins, num_del, num_sub = events

        original_length = end - start

        length_change = num_ins - num_del

        padded_end = end + abs(length_change)

        if padded_end > end:
            full_reference_sequence = self.fasta.fetch(chrom, start, padded_end)
        else:
            full_reference_sequence = self.fasta.fetch(chrom, start, end)

        segment_length = end - start
        segment_reference_sequence = full_reference_sequence[:segment_length]

        generator = VariantGenerator(segment_reference_sequence, events)

        variants = generator.generate_random_variant_sequence()

        modified_segment_sequence = apply_variants(ref_start=0, ref_seq=full_reference_sequence, alt_length=len(variants) + length_change, variants=variants)

        modified_segment_sequence = modified_segment_sequence[:original_length]

        return ReferenceSegment(chrom, start, end, modified_segment_sequence)
