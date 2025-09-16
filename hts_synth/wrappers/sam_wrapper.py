from enum import IntFlag

from pysam import AlignedSegment


class SamFlag(IntFlag):
    """
    Properties of the SAM flag.

    Create a new SAM flag by combining these using bitwise OR, eg:
        flag = SamFlag.FIRST_IN_PAIR | SamFlag.READ_MAPPED_IN_PROPER_PAIR | SamFlag.READ_PAIRED
    """

    READ_PAIRED = 0x001
    READ_MAPPED_IN_PROPER_PAIR = 0x002
    READ_UNMAPPED = 0x004
    MATE_UNMAPPED = 0x008
    READ_REVERSE_STRAND = 0x010
    MATE_REVERSE_STRAND = 0x020
    FIRST_IN_PAIR = 0x040
    SECOND_IN_PAIR = 0x080
    NOT_PRIMARY_ALIGNMENT = 0x100
    READ_FAILS_PLATFORM_VENDOR_QUALITY_CHECKS = 0x200
    READ_IS_PCR_OR_OPTICAL_DUPLICATE = 0x400
    SUPPLEMENTARY_ALIGNMENT = 0x800


def create_synthetic_read_pair(sequence: str, qualities: str, flag: int = 0) -> AlignedSegment:
    """
    Wrap a sequence and qualities into a PySam AlignedSegment.

    Args:
        sequence (str): The sequence of the read.
        qualities (str): The quality string of the read.
        flag (int, optional): SAM flag for the read. Defaults to 0.
    """
    read = AlignedSegment()

    read.query_sequence = sequence
    read.query_qualities_str = qualities
    read.flag = flag

    # TODO: update these with appropriate values
    read.query_name = "synthetic_read/1"
    read.reference_id = 0
    read.reference_start = 100
    read.next_reference_start = 100
    read.mapping_quality = 20

    return read
