from error_model import ErrorModel

import numpy as np
from pysam import AlignedSegment

from typing import Iterator

# placeholder - Alex has been looking at this
class QualityModel():
    def get_qualities(self):
        ...

class ReadGenerator():
    """ 
    Class used to generate reads

    Attributes:
        quality_model (QualityModel): The model dictating the quality of the read
        error_model (ErrorModel): The model dictating the probability of errors within the read
    """
    def __init__(self, quality_model: QualityModel, error_model: ErrorModel):
        self.quality_model = quality_model
        self.error_model = error_model

    def generate(self, reference_sequence: str) -> AlignedSegment:

        read = AlignedSegment()

        # if the error model says to add an edit (ins/del/snv), add one here
        read.query_sequence = self.error_model.apply_errors(reference_sequence)
        read.query_qualities_str = self.quality_model.get_qualities()
        #read.flag = 

        read.query_name = "synthetic_read/1" # TODO - neat includes chrom and base position
        read.reference_id = 0
        read.reference_start = 100
        read.next_reference_start = 100
        read.mapping_quality = 20

        return read
        

    def generate_multiple(self, reference_sequence: str, amount: int = 10) -> Iterator[AlignedSegment]:
        """
        Fucntion used to generate multiple reads

        Args:
            reference_sequence(str): The reference sequence used to generate the reads
            amount(int): The amount of reads to generate
        """
        for i in range(amount):
            yield self.generate(reference_sequence)
