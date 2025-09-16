from .generate_variant import VariantGenerator
from .seq_converter import apply_variants


def main():
    generator = VariantGenerator(sequence=("ACTTGGAAGT"), events=[1, 1, 1])
    variants = generator.generate_random_variant_sequence()
    alt_length = len(variants)
    print(
        apply_variants(ref_start=0, ref_seq="ACTTGGAAGT", alt_length=alt_length, variants=variants)
    )


if __name__ == "__main__":
    main()
