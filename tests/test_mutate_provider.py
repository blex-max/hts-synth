class TestMutate:

    def test_mutate(self, faker):
        mutated_sequence = faker.mutated_reference_sequence(reference_sequence="ACTTGGAAGT", events=[1, 1, 1])
        assert mutated_sequence
        assert len(mutated_sequence) == 10

    def test_delete(self, faker):
        mutated_sequence = faker.mutated_reference_sequence(reference_sequence="ACTTGGAAGT", events=[0, 1, 0])
        assert mutated_sequence
        assert len(mutated_sequence) == 9

    def test_insertion(self, faker):
        mutated_sequence = faker.mutated_reference_sequence(reference_sequence="ACTTGGAAGT", events=[1, 0, 0])
        assert mutated_sequence
        assert len(mutated_sequence) == 11

    def test_substitution(self, faker):
        reference_sequence = "ACTTGGAAGT"
        mutated_sequence = faker.mutated_reference_sequence(reference_sequence=reference_sequence, events=[0, 0, 1])
        assert mutated_sequence
        assert len(mutated_sequence) == 10
        assert mutated_sequence != reference_sequence
