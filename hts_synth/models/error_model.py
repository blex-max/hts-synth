from enum import Enum
from typing import Optional

import numpy as np

class Variant(Enum):
    Insertion = 1
    Deletion = 2
    SNV = 3


class ErrorModel():
    """
        Class used to store the pobability of errors
    """
    error_chances: dict = {
        Variant.Insertion: 0.01,
        Variant.Deletion: 0.01,
        Variant.SNV: 0.05
    }

    def __init__(self, error_chances: Optional[dict] = None):
        if error_chances:
            self.error_chances = error_chances

        self.bins: dict[str, tuple] = self.__build_bins()
        

    def __build_bins(self) -> dict[str, tuple]:
        """
        This function constructs the bins based on the error_chances of the class
        """
        bins = {}
        min = 0

        for key, error_probability in self.error_chances.items():
            bins[key] = (min, error_probability)
            min = error_probability

        return bins

    def __apply_insertion(self, seq: str, position: int) -> str:
        ...
    
    def __apply_deletion(self, seq: str, position: int) -> str:
        ...
        
    def __apply_snv(self, seq: str, position: int) -> str:
        ...

    def apply_errors(self, reference_sequence: str) -> str:

        for index, base in enumerate(reference_sequence):
            number = np.random.random()

            for var_type, bin_range in self.bins.items(): 
                if number in range(bin_range[0], bin_range[1]):
                    match var_type:
                        case Variant.Insertion:
                            self.__apply_insertion(reference_sequence, index)
                        case Variant.Deletion:
                            self.__apply_deletion(reference_sequence, index)
                        case Variant.SNV:
                            self.__apply_snv(reference_sequence, index)
        
        return reference_sequence
