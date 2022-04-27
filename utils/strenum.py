import logging

from enum import Enum

logger: logging.Logger = logging.getLogger(__name__)


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value

    # Should be `name` instead of `self` as per documentation, but SonarLint throws error.
    # https://docs.python.org/3.6/library/enum.html#using-automatic-values
    def _generate_next_value_(self, start, count, last_values):
        return self
