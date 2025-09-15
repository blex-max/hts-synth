from hts_synth.wrappers.sam import SamFlag, create_synthetic_read_pair


class TestSam:
    def test_sam_flag(self):
        assert SamFlag.READ_PAIRED == 0x001
        assert SamFlag.READ_MAPPED_IN_PROPER_PAIR == 0x002
        assert SamFlag.READ_UNMAPPED == 0x004
        assert (
            SamFlag.READ_UNMAPPED
            | SamFlag.READ_MAPPED_IN_PROPER_PAIR
            | SamFlag.READ_PAIRED
            == 0x007
        )

    def test_create_synthetic_read_pair(self):
        read = create_synthetic_read_pair("ACGT", "8AAA", flag=SamFlag.READ_PAIRED)

        assert read.query_sequence == "ACGT"
        assert read.query_qualities_str == "8AAA"
        assert read.flag == SamFlag.READ_PAIRED

        assert read.query_name == "synthetic_read/1"
        assert read.reference_id == 0
        assert read.reference_start == 100
        assert read.next_reference_start == 100
