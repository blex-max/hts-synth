import re
from collections.abc import Iterable
from dataclasses import fields
from itertools import groupby
from typing import Any, Callable, TypeVar

dna_re = re.compile("^[ACGT]*$")
dna_complement_tr_table = str.maketrans("ACGT", "TGCA")
R = TypeVar("R")


def is_dna(s: str) -> bool:
    return dna_re.match(s) is not None


def reverse_complement(seq: str) -> str:
    return seq[::-1].translate(dna_complement_tr_table)


def parse_opt_int_group(m: re.Match[str], i: int) -> int:
    g = m.group(i)
    return int(g) if g else 0


def has_duplicates(items: list[str]) -> bool:
    return len(set(items)) != len(items)


def get_dataclass_fields(cls: Any) -> list[str]:
    return [f.name for f in fields(cls)]


def get_not_none(it: Any):
    return [x for x in it if x is not None]


def is_adaptor_valid(adaptor: str | None) -> bool:
    return adaptor is None or is_dna(adaptor)


def get_codon_offset_complement(offset: int) -> int:
    match offset:
        case 0:
            return 0
        case 1:
            return 2
        case 2:
            return 1
        case _:
            raise ValueError("Invalid codon offset!")


def get_cds_ext_3_length(frame: int, length: int) -> int:
    """
    Calculate how many nucleotides are missing from the last codon based on the length of the sequence.
    """
    return (3 - (length + frame) % 3) % 3


def bool_to_int_str(x: bool) -> str:
    return "1" if x else "0"


def clamp_non_negative(n: int) -> int:
    return max(0, n)


def get_end(start: int, length: int) -> int:
    """Get inclusive end position given start and length."""
    return start + clamp_non_negative(length - 1)


def is_unique_ascending(a: list[Any]) -> bool:
    n = len(a)
    if n == 0:
        return True
    return all(a[i] > a[i - 1] for i in range(1, n))
