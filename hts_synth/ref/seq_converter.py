import re

# Modified 2025
from collections.abc import Sequence

from ..ref.variant import Variant


def apply_variants(
    ref_start: int, ref_seq: str, alt_length: int, variants: Sequence[Variant]
) -> str:
    """
    Alter a DNA sequence based on a set of variants.

    Assumptions:
    - variants are fully in range of the reference sequence
    - variants do not overlap with each other
    - variants are sorted by position
    """
    if not variants:
        return ref_seq

    # Preallocate altered sequence
    alt_seq = bytearray(alt_length)

    ref = ref_seq
    ref_start = ref_start
    ref_length = len(ref_seq)
    n = len(variants)

    i = 0  # REF seq base offset
    j = 0  # ALT seq base offset
    k = 0  # variant index

    # Next variant (assumption: variants are sorted by position)
    v: Variant = variants[k]

    if v.pos > ref_start:
        # Copy the head of the reference sequence unaffected by variants
        delta = v.pos - ref_start
        alt_seq[:delta] = ref[:delta].encode("ascii")

        i = delta
        j = delta

    while i < ref_length:
        ref_pos = ref_start + i
        if v and v.pos == ref_pos:
            # Apply variant
            for c in v.alt:
                alt_seq[j] = ord(c)
                j += 1

            # Skip REF bases
            i += v.ref_len

            k += 1
            if k < n:
                # Step to the next variant
                v = variants[k]

            else:
                break

        else:
            # Copy REF base
            alt_seq[j] = ord(ref[i])

            i += 1
            j += 1

    if i < ref_length:
        # Copy the tail of the reference sequence unaffected by variants
        alt_seq[j:] = ref[i:].encode("ascii")

    return re.sub(r"[^ACGT]", "", alt_seq.decode("ascii"))
