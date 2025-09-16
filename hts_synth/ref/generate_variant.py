import random
from collections.abc import Sequence

import numpy as np

from ..ref.enums import VariantType
from ..ref.variant import Variant


class VariantGenerator:
    def __init__(self, sequence: str, events: Sequence[int]):
        """
        Generate a synthetic sequence of variants, simulating the contents of a VCF file.

        :param sequence: sequence to mutate
        :param events: insertions, deletions, substitutions
        """
        self.bases = ["A", "C", "G", "T"]
        self.ref_offset = 0
        self.events = events
        self.sequence = sequence

    def generate_random_variant_sequence(self):
        """Generate a random variant sequence based on a set of events."""
        ref_length = len(self.sequence)
        num_insertions = self.events[VariantType.INSERTION]
        num_deletions = self.events[VariantType.DELETION]
        num_substitutions = self.events[VariantType.SUBSTITUTION]
        alt_length = ref_length + (num_insertions - num_deletions)
        total_length = max(ref_length, alt_length)
        num_events = num_insertions + num_deletions + num_substitutions
        np.random.seed(0)
        event_indices = list(np.random.permutation(total_length)[:num_events])

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
                return "", random.choice(self.bases)
            elif event_indices.index(index) < num_insertions + num_deletions:
                ref_value = self.sequence[index + self.ref_offset]
                return ref_value, ""
            else:
                substitution_choices = self.bases
                substitution_choices.remove(self.sequence[index + self.ref_offset])
                return self.sequence[index + self.ref_offset], random.choice(substitution_choices)
        else:
            return self.sequence[index + self.ref_offset], self.sequence[index + self.ref_offset]
