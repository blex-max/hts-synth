Faker Interface Documentation
============================

This document describes how to set up and use the two custom Faker providers available in hts-synth: ``ReadProvider`` and ``MutatedSequenceProvider``.

Setup
-----

To use the custom Faker providers, you need to first create a Faker instance and add the providers to it:

.. code-block:: python

    from faker import Faker
    from hts_synth.providers.read_provider import ReadProvider
    from hts_synth.providers.mutated_sequence_provider import MutatedSequenceProvider

    # Create a Faker instance
    faker = Faker()
    
    # Add the custom providers
    faker.add_provider(ReadProvider)
    faker.add_provider(MutatedSequenceProvider)

ReadProvider
------------

The ``ReadProvider`` generates synthetic sequencing reads using a quality model and error probabilities.

Methods
~~~~~~~

``read(reference_position=100, reference_sequence="ATGCTGTG", error_probabilities=None)``
    Generates a synthetic read as an ``AlignedSegment`` object.

    **Parameters:**
    
    * ``reference_position`` (int, optional): The reference position for the read. Default: 100
    * ``reference_sequence`` (str, optional): The reference sequence to base the read on. Default: "ATGCTGTG"
    * ``error_probabilities`` (dict[VariantType, float] | None, optional): Dictionary mapping variant types to their error probabilities. Default: None

    **Returns:**
    
    * ``AlignedSegment``: A synthetic sequencing read

    **Example:**
    
    .. code-block:: python

        # Generate a read with default parameters
        read = faker.read()
        print(read.sequence)  # Output: synthetic sequence
        
        # Generate a read with custom parameters
        custom_read = faker.read(
            reference_position=200,
            reference_sequence="ATGCATGCATGC",
            error_probabilities={VariantType.SUBSTITUTION: 0.01}
        )

MutatedSequenceProvider
-----------------------

The ``MutatedSequenceProvider`` generates mutated DNA sequences by applying a specified number of insertions, deletions, and substitutions to an input sequence.

Methods
~~~~~~~

``mutated_sequence(sequence, events)``
    Generates a mutated version of the input sequence.

    **Parameters:**
    
    * ``sequence`` (str): The input DNA sequence to mutate
    * ``events`` (Sequence[int]): A sequence of three integers representing the number of insertions, deletions, and substitutions to apply

    **Returns:**
    
    * ``str``: The mutated DNA sequence

    **Example:**
    
    .. code-block:: python

        # Original sequence
        original_seq = "ATGCATGCATGC"
        
        # Apply 1 insertion, 1 deletion, and 2 substitutions
        mutated_seq = faker.mutated_sequence(
            sequence=original_seq,
            events=[1, 1, 2]  # [insertions, deletions, substitutions]
        )
        print(f"Original: {original_seq}")
        print(f"Mutated:  {mutated_seq}")

Complete Example
----------------

Here's a complete example showing how to set up and use both providers:

.. code-block:: python

    from faker import Faker
    from hts_synth.providers.read_provider import ReadProvider
    from hts_synth.providers.mutated_sequence_provider import MutatedSequenceProvider
    from hts_synth.ref.enums import VariantType

    # Setup
    faker = Faker()
    faker.add_provider(ReadProvider)
    faker.add_provider(MutatedSequenceProvider)

    # Generate a synthetic read
    synthetic_read = faker.read(
        reference_position=150,
        reference_sequence="ATGCGTACGTACGTAC"
    )
    print(f"Read sequence: {synthetic_read.sequence}")

    # Generate a mutated sequence
    original_sequence = "ATGCGTACGTACGTAC"
    mutated_sequence = faker.mutated_sequence(
        sequence=original_sequence,
        events=[2, 1, 3]  # 2 insertions, 1 deletion, 3 substitutions
    )
    print(f"Original sequence: {original_sequence}")
    print(f"Mutated sequence:  {mutated_sequence}")

Testing Setup
-------------

For testing purposes, you can set up the providers in a pytest fixture as shown:

.. code-block:: python

    import pytest
    from faker import Faker
    from hts_synth.providers.read_provider import ReadProvider
    from hts_synth.providers.mutated_sequence_provider import MutatedSequenceProvider

    @pytest.fixture(scope="session")
    def faker():
        faker = Faker()
        faker.add_provider(ReadProvider)
        faker.add_provider(MutatedSequenceProvider)
        yield faker