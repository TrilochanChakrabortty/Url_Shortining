import string, pytest

from app.utils.shortener import generate_short_code


# ============================================================
# TEST DEFAULT SHORT CODE LENGTH
# ============================================================

def test_generate_short_code_default_length():

    # Act
    short_code = generate_short_code()

    # Assert
    assert len(short_code) == 6


# ============================================================
# TEST CUSTOM SHORT CODE LENGTH
# ============================================================

def test_generate_short_code_custom_length():

    # Arrange
    length = 10

    # Act
    short_code = generate_short_code(length)

    # Assert
    assert len(short_code) == length


# ============================================================
# TEST ALLOWED CHARACTERS
# ============================================================

def test_generate_short_code_contains_valid_characters():

    # Act
    short_code = generate_short_code()

    # Arrange
    allowed_characters = (
        string.ascii_letters + string.digits
    )

    # Assert
    assert all(
        char in allowed_characters
        for char in short_code
    )
    
# checking the edge cases 

def test_generate_short_code_zero_length():

    short_code = generate_short_code(0)

    assert short_code == ""
    assert len(short_code) == 0
    
    
def test_generate_short_code_large_length():

    length = 100

    short_code = generate_short_code(length)

    assert len(short_code) == length
    


def test_generate_short_code_negative_length():

    with pytest.raises(ValueError):
        generate_short_code(-5)
        
