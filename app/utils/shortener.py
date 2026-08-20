import random
import string


def generate_short_code(length: int = 6) -> str:

    if length < 0:
        raise ValueError(
            "Length cannot be negative"
        )

    characters = string.ascii_letters + string.digits

    return "".join(
        random.choices(characters, k=length)
    )
    