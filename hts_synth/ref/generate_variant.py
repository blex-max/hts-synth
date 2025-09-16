import random
import numpy as np
from typing import Sequence

from .enums import VariantType
from .variant import Variant

class VariantGenerator():
    """
    A class for generating synthetic genomic variants that simulate VCF file contents.
    
    This class creates random genomic variants (insertions, deletions, substitutions) 
    based on a reference sequence and specified event counts. It's designed for 
    synthetic data generation in bioinformatics applications.
    
    Attributes:
        bases (List[str]): Available DNA bases for variant generation.
        ref_offset (int): Tracking offset for reference sequence position adjustments.
        events (Sequence[int]): Number of each variant type to generate.
        ref_sequence (str): The reference genomic sequence.
    """
    def __init__(self, ref_sequence: str, events: Sequence[int]):
        """
        Initialise a VariantGenerator with a reference sequence and event counts.
        
        Args:
            ref_sequence (str): The reference genomic sequence to generate variants against.
            events (Sequence[int]): A sequence containing the number of each variant type
                                  to generate, indexed by VariantType enum values:
                                  - events[0]: Number of insertions (VariantType.INSERTION)
                                  - events[1]: Number of deletions (VariantType.DELETION)
                                  - events[2]: Number of substitutions (VariantType.SUBSTITUTION)
        
        Note:
            The events parameter should have at least 3 elements corresponding to
            the three variant types defined in VariantType enum.
        """
        self.bases = ['A', 'C', 'G', 'T']
        self.ref_offset = 0
        self.events = events
        self.ref_sequence = ref_sequence


    def generate_random_variant_sequence(self):
        """
        Generate a random sequence of variants based on the configured event counts.
        
        This method creates a synthetic variant sequence by randomly placing insertions,
        deletions, and substitutions across the reference sequence. The positions are
        determined using a random permutation to ensure even distribution.
        
        Returns:
            List[Variant]: A list of Variant objects representing the generated variants.
                          Each variant contains position, reference, and alternative sequences.
        
        Note:
            - Uses numpy random seed of 0 for reproducible results
            - The total sequence length is calculated as the maximum of reference length
              and alternative length (ref_length + insertions - deletions)
            - Event positions are randomly distributed across the total length
        """
        ref_length = len(self.ref_sequence)
        num_insertions = self.events[VariantType.INSERTION]
        num_deletions = self.events[VariantType.DELETION]
        num_substitutions = self.events[VariantType.SUBSTITUTION]
        alt_length = ref_length + (num_insertions - num_deletions)
        total_length = max(ref_length, alt_length)
        num_events = num_insertions + num_deletions + num_substitutions
        event_indices = list(np.random.permutation(total_length)[:num_events])
        
        variant_sequence = []
        for i in range(total_length):
            ref, alt = self.get_ref_alt(i, event_indices, num_insertions, num_deletions)

            variant = Variant(pos=i, ref=ref, alt=alt)
            variant_sequence.append(variant)

        return variant_sequence

    def get_ref_alt(self, index, event_indices, num_insertions, num_deletions):
        """
        Determine the reference and alternative sequences for a given position.
        
        This method decides what type of variant (if any) should occur at a specific
        index based on the predetermined event positions and counts.
        
        Args:
            index (int): The current position being processed in the sequence.
            event_indices (List[int]): List of positions where variants should occur.
            num_insertions (int): Total number of insertions to generate.
            num_deletions (int): Total number of deletions to generate.
        
        Returns:
            tuple[str, str]: A tuple containing (reference_sequence, alternative_sequence):
                - For insertions: ("", random_base)
                - For deletions: (reference_base, "")
                - For substitutions: (reference_base, random_base)
                - For no variant: (reference_base, reference_base)
        
        Note:
            - Event types are determined by position in event_indices list:
              - First num_insertions positions are insertions
              - Next num_deletions positions are deletions  
              - Remaining positions are substitutions
            - Modifies self.ref_offset for insertions to track position shifts
        """
        if index in event_indices:
            if event_indices.index(index) < num_insertions:
                self.ref_offset -= 1
                return "", random.choice(self.bases)
            elif event_indices.index(index) < num_insertions + num_deletions:
                ref_value = self.ref_sequence[index + self.ref_offset]
                return ref_value, ""
            else:
                return self.ref_sequence[index + self.ref_offset], random.choice(self.bases)
        else:
            return self.ref_sequence[index + self.ref_offset], self.ref_sequence[index + self.ref_offset]
