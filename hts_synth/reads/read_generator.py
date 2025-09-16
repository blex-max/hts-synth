import numpy as np
import pysam
from pysam import AlignedSegment

from typing import Iterator, Iterable, Optional, Dict

from ..ref.enums import VariantType
from ..ref.generate_variant import VariantGenerator

class QualityModel():
    """
    Placeholder class for the quality model Alex was working on
    """
    def get_quality_scores(self, length: int) -> Iterable[str]:
        """
        Placeholder function for quality string generation

        Args: 
            len (int): length of sequence to generate quality scores for 
        """
        return [0 for i in range(length)]


class ReadGenerator():
    """ 
    Class used to generate reads

    Attributes:
        quality_model (QualityModel): Object that provides a `quality_string()` function
        error_rates (Dict): A dict containing the rate at which errors could occur
    """
    error_probabilities = {
        VariantType.INSERTION: 0.01,
        VariantType.DELETION: 0.01,
        VariantType.SUBSTITUTION: 0.05
    }
    
    def __init__(self, quality_model: QualityModel, error_probabilities:Optional[Dict[VariantType, float]] = None):
        """
        Initialise a Read Generator with a model for generating quality scores (currently a placeholder) and 
        a dictionary of sequencing error probabilities

        Args:
            quality_model (QualityModel): object that provides a `quality_string()` function
            error_probabilities (Dict): optional dict containing the rate at which errors could occur
        """
        self.quality_model = quality_model
        if error_probabilities:
            self.error_probabilities = error_probabilities


    def generate(self, reference_position: int, reference_sequence: str) -> AlignedSegment:
        """
        Function to generate a synthetic read by applying mutations based on simulated sequencing errors to 
        a section of the reference sequence

        Args: 
            reference_position (int): The starting position within the reference of the reference sequence
            reference_sequence (str): The reference sequence used to generate the reads
        """
        # [num_insertions, num_deletions, num_substitutions]
        events = [round(rate * len(reference_sequence)) for rate in self.error_probabilities.values()]

        variant_generator = VariantGenerator(reference_sequence, events)

        read = AlignedSegment()

        read.query_sequence = ''.join(variant.alt for variant in variant_generator.generate_random_variant_sequence())
        print(self.quality_model.get_quality_scores(len(read.query_sequence)))
        read.query_qualities_str = pysam.qualities_to_qualitystring(qualities=self.quality_model.get_quality_scores(len(read.query_sequence)))

        # TODO actually generate read properties - meaningful name and correct flag
        # Should this function return a pair of reads for paired end sequencing?
            # Should this be a seperate function?

        # read.flag = ?
        read.query_name = "synthetic_read/1"
        read.reference_id = 0
        read.reference_start = reference_position
        read.next_reference_start = reference_position + len(read.query_sequence)
        read.mapping_quality = 20
        
        return read
        

    def generate_multiple(self, reference_position: int, reference_sequence: str, amount: int = 10) -> Iterator[AlignedSegment]:
        """
        Function used to generate multiple reads

        Args:
            reference_position (int): The starting position within the reference of the reference sequence
            reference_sequence (str): The reference sequence used to generate the reads
            amount (int): The amount of reads to generate
        """
        for i in range(amount):
            yield self.generate(reference_position, reference_sequence)
