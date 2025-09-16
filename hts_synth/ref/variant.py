from __future__ import annotations

from dataclasses import dataclass, replace
from typing import NoReturn

from ..ref.enums import VariantType
from ..ref.utils import get_end


def _raise_no_ref_alt() -> NoReturn:
    raise ValueError("Invalid variant: both REF and ALT are null!")


@dataclass(slots=True)
class Variant:
    pos: int
    ref: str
    alt: str

    def __str__(self) -> str:
        return (
            f"{self.pos}del{self.ref}"
            if not self.alt
            else f"{self.pos}ins{self.alt}"
            if not self.ref
            else f"{self.pos}{self.ref}>{self.alt}"
        )

    def __post_init__(self) -> None:
        if not self.ref and not self.alt:
            _raise_no_ref_alt()

    @property
    def ref_len(self) -> int:
        return len(self.ref)

    @property
    def alt_len(self) -> int:
        return len(self.alt)

    @property
    def alt_ref_delta(self) -> int:
        return self.alt_len - self.ref_len

    @property
    def ref_end(self) -> int:
        return get_end(self.pos, self.ref_len)

    @property
    def type(self) -> VariantType:
        if self.ref:
            return VariantType.SUBSTITUTION if self.alt else VariantType.DELETION
        if self.alt:
            return VariantType.INSERTION
        _raise_no_ref_alt()

    @property
    def is_insertion(self) -> bool:
        return self.type == VariantType.INSERTION

    @classmethod
    def get_del(cls, start: int, ref: str) -> Variant:
        """Create a deletion."""
        return cls(start, ref, "")

    @classmethod
    def get_ins(cls, start: int, alt: str) -> Variant:
        """Create an insertion."""
        return cls(start, "", alt)

    def clone(self, pos: int | None = None):
        return replace(self, pos=pos if pos is not None else self.pos)

    def offset(self, offset: int):
        return self.clone(pos=self.pos + offset)
