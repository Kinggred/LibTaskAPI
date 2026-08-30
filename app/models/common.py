from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator


class BookState(StrEnum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


def validate_six_digit_identifier(value: str) -> str:
    if len(value) != 6:
        raise ValueError("Identifier must contain exactly 6 digits")

    if not value.isdigit():
        raise ValueError("Identifier must contain digits only.")

    return value


SixDigitIdentifier = Annotated[
    str,
    AfterValidator(validate_six_digit_identifier),
]
