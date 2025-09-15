import random
from typing import Sequence
from enums import VariantType
import numpy as np
from variant import Variant

class VariantGenerator():

    def __init__(self, ref_sequence: str, events: Sequence[int]):
        """
        Generate a synthetic sequence of variants, simulating the contents of a VCF file
        :param ref_sequence: reference sequence
        :param events:
        """
        self.bases = ['A', 'C', 'G', 'T']
        self.ref_offset = 0
        self.events = events
        self.ref_sequence = ref_sequence


    def generate_random_variant_sequence(self):
        """
        Generate a random variant sequence based on a set of events
        """
        ref_length = len(self.ref_sequence)
        num_insertions = self.events[VariantType.INSERTION]
        num_deletions = self.events[VariantType.DELETION]
        num_substitutions = self.events[VariantType.SUBSTITUTION]
        alt_length = ref_length + (num_insertions - num_deletions)
        total_length = max(ref_length, alt_length)
        num_events = num_insertions + num_deletions + num_substitutions

        event_indices = list(np.random.permutation(total_length)[:num_events])
        print(f'Event indices: {event_indices}')

        variant_sequence = []
        for i in range(total_length):
            ref, alt = self.get_ref_alt(i, event_indices, num_insertions, num_deletions)
            variant = Variant(pos=i, ref=ref, alt=alt)
            variant_sequence.append(variant)

        return variant_sequence

    def get_ref_alt(self, index, event_indices, num_insertions, num_deletions):
        if index in event_indices:
            if event_indices.index(index) < num_insertions:
                self.ref_offset -= 1
                return None, random.choice(self.bases)
            elif event_indices.index(index) < num_insertions + num_deletions:
                ref_value = self.ref_sequence[index + self.ref_offset]
                return ref_value, None
            else:
                return self.ref_sequence[index + self.ref_offset], random.choice(self.bases)
        else:
            return self.ref_sequence[index + self.ref_offset], self.ref_sequence[index + self.ref_offset]