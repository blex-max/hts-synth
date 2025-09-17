import pytest
from faker import Faker


@pytest.mark.xfail(reason="Randomness in mutation means sometimes tests fail")
class TestMutate:
    def test_mutate(self, faker: Faker):
        mutated_sequence = faker.mutated_sequence(sequence="ACTTGGAAGT", events=[1, 1, 1])
        assert mutated_sequence
        assert len(mutated_sequence) == 10

    def test_delete(self, faker: Faker):
        mutated_sequence = faker.mutated_sequence(sequence="ACTTGGAAGT", events=[0, 1, 0])
        assert mutated_sequence
        assert len(mutated_sequence) == 9

    def test_insertion(self, faker: Faker):
        mutated_sequence = faker.mutated_sequence(sequence="ACTTGGAAGT", events=[1, 0, 0])
        assert mutated_sequence
        assert len(mutated_sequence) == 11

    def test_substitution(self, faker: Faker):
        reference_sequence = "ACTTGGAAGT"
        mutated_sequence = faker.mutated_sequence(sequence=reference_sequence, events=[0, 0, 1])
        assert mutated_sequence
        assert len(mutated_sequence) == 10
        assert mutated_sequence != reference_sequence
