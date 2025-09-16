from hts_synth.reads import ReadGenerator

from hts_synth.reads.read_generator import QualityModel

def test_read_generator():
    read_generator = ReadGenerator(QualityModel())

    read = read_generator.generate(100, 'ATGCTGTG')

    assert read.query_sequence is not None
