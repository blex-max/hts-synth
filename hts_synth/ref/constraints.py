import random
from collections.abc import Sequence

from .enums import VariantType
from .variant import Variant
from ..model.qual_model import NaiveQualModelBase


class EditEvent:
    """
    Represents a single edit event to be applied to a read.
    """
    ALLOWED_VALS_ON_READ = ["r1", "r2", "both"]

    def __init__(
        self,
        edit_type: VariantType,
        size: int,
        count: Tuple[int, int],
        on_read: str = 'r1'
    ):
        self.edit_type = edit_type
        self.size = size
        self.count = count
        if on_read not in ALLOWED_VALS_ON_READ:
            mesage = f"Value `{on_read}` not a valid option for `on_read`. "
            message += f"Valid values are 'r1', 'r2', 'both'."
            raise ValueError(message)

        self.on_read = on_read

class Constraints:
    """
    Imposes post-generation edits on sequencing reads, placeholder for
    model (not yet implemented).
    """
    def __init__(self, *edit_events: EditEvent, model: NaiveQualModelBase=None):
        self.edit_events = list(edit_events)

    def apply(self, read: str, read_name: str) -> str:
        """
        Applies all relevant edit events to the given read.
        """
        return read

