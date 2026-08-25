from cryptography.fernet import Fernet, InvalidToken


def generate_encryption_key() -> str:
    """
    Generate a new Fernet encryption key.
    Run this once and store the key securely.
    """
    return Fernet.generate_key().decode()


def encrypt_value(value: str, key: str) -> str:
    """
    Encrypt a string using the supplied Fernet key.
    """
    if not value:
        raise ValueError("Value to encrypt cannot be empty")

    if not key:
        raise ValueError("Encryption key cannot be empty")

    cipher = Fernet(key.encode())

    return cipher.encrypt(value.encode()).decode()


def decrypt_value(encrypted_value: str, key: str) -> str:
    """
    Decrypt an encrypted string using the supplied Fernet key.
    """
    if not encrypted_value:
        raise ValueError("Encrypted value cannot be empty")

    if not key:
        raise ValueError("Encryption key cannot be empty")

    try:
        cipher = Fernet(key.encode())

        return cipher.decrypt(
            encrypted_value.encode()
        ).decode()

    except InvalidToken as exc:
        raise ValueError(
            "Unable to decrypt value. "
            "The encryption key may be incorrect."
        ) from exc