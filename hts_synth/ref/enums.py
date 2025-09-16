from enum import IntEnum


class VariantType(IntEnum):
    INSERTION = 0
    DELETION = 1
    SUBSTITUTION = 2
    UNKNOWN = 3


class VariantClassification(IntEnum):
    CLASSIFIED = 0
    UNCLASSIFIED = 1
    MONOMORPHIC = 2
