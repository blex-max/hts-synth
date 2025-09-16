class TestRead:
    def test_read(self, faker):
        read = faker.read(10)
        assert read
        assert len(read.sequence) == 10
        read2 = faker.read(5)
        assert len(read2.sequence) == 5
