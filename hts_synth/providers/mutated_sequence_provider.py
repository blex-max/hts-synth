from typing import Sequence

from faker.providers import BaseProvider

from hts_synth.ref import generate_variant, seq_converter


class MutatedSequenceProvider(BaseProvider):
    """
    Mutated Sequence Provider
    """

    def mutated_reference_sequence(self, reference_sequence: str, events: Sequence[int]) -> str:
        """

        :param reference_sequence: sequence to mutate
        :param events: number of insertions, deletions, and substitutions to apply
        :return: mutated sequence string
        """
        generator = generate_variant.VariantGenerator(ref_sequence=reference_sequence, events=events)
        variants = generator.generate_random_variant_sequence()
        alt_length = len(variants)
        return seq_converter.apply_variants(ref_start=0, ref_seq=reference_sequence, alt_length=alt_length, variants=variants)
