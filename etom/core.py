import json
from typing import Any, Dict, List, Union

import toml
from cryptography.fernet import Fernet


class EncryptedTOML:
    """
    A class for handling encrypted TOML files.

    This class provides methods to encrypt, decrypt, save, load, and update
    TOML data using Fernet symmetric encryption.
    """

    def __init__(self, key: Union[str, bytes]):
        """
        Initialize the EncryptedTOML instance with an encryption key.

        Args:
                key (Union[str, bytes]): The encryption key. If a string is provided,
                                                                 it will be encoded to bytes.

        Raises:
                ValueError: If the key is None.
        """
        if key is None:
            raise ValueError("Key must be provided")
        elif isinstance(key, str):
            key = key.encode()
        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> bytes:
        """
        Encrypt the given string data.

        Args:
                data (str): The data to encrypt.

        Returns:
                bytes: The encrypted data.
        """
        return self.fernet.encrypt(data.encode())

    def decrypt(self, encrypted_data: bytes) -> str:
        """
        Decrypt the given encrypted data.

        Args:
                encrypted_data (bytes): The data to decrypt.

        Returns:
                str: The decrypted data as a string.
        """
        return self.fernet.decrypt(encrypted_data).decode()

    def save(self, data: Dict[str, Any], filename: str) -> None:
        """
        Save the given data as an encrypted TOML file.

        Args:
                data (Dict[str, Any]): The data to save.
                filename (str): The name of the file to save the data to.
        """
        encrypted_data = self.encrypt(toml.dumps(data))
        with open(filename, "wb") as f:
            f.write(encrypted_data)

    def load(self, filename: str) -> Dict[str, Any]:
        """
        Load and decrypt data from an encrypted TOML file.

        Args:
                filename (str): The name of the file to load data from.

        Returns:
                Dict[str, Any]: The decrypted data as a dictionary.
        """
        with open(filename, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = self.decrypt(encrypted_data)
        return toml.loads(decrypted_data)

    def update(self, filename: str, new_data: Dict[str, Any]) -> None:
        """
        Update an encrypted TOML file with new data.

        This method loads the existing data, updates it with the new data,
        and then saves the updated data back to the file.

        Args:
                filename (str): The name of the file to update.
                new_data (Dict[str, Any]): The new data to update the file with.
        """
        current_data = self.load(filename)
        current_data.update(new_data)
        self.save(current_data, filename)

    def update_key(self, filename: str, key_path: List[str], value: Any) -> None:
        """
        Update a specific key in an encrypted TOML file.

        This method allows updating a nested key by providing a key path.

        Args:
                filename (str): The name of the file to update.
                key_path (List[str]): The path to the key to update.
                value (Any): The new value to set for the key.

        Raises:
                KeyError: If a key in the key_path does not exist.
        """
        data = self.load(filename)
        current = data
        for key in key_path[:-1]:
            if key not in current:
                raise KeyError(f"Key '{key}' not found in path {key_path}")
            current = current[key]
        current[key_path[-1]] = value
        self.save(data, filename)

    @staticmethod
    def generate_key() -> bytes:
        """
        Generate a new Fernet encryption key.

        Returns:
                bytes: A new Fernet encryption key.
        """
        return Fernet.generate_key()

    @staticmethod
    def save_key(key: bytes, filename: str) -> None:
        """
        Save an encryption key to a file.

        Args:
                key (bytes): The encryption key to save.
                filename (str): The name of the file to save the key to.
        """
        with open(filename, "wb") as f:
            f.write(key)

    @staticmethod
    def load_key(filename: str) -> bytes:
        """
        Load an encryption key from a file.

        Args:
                filename (str): The name of the file to load the key from.

        Returns:
                bytes: The loaded encryption key.
        """
        with open(filename, "rb") as f:
            return f.read()

    def to_json(self, filename: str) -> str:
        """
        Convert an encrypted TOML file to a JSON string.

        Args:
                filename (str): The name of the encrypted TOML file to convert.

        Returns:
                str: The data from the TOML file as a JSON-formatted string.
        """
        data = self.load(filename)
        return json.dumps(data, indent=2)

    def from_json(self, json_str: str, filename: str) -> None:
        """
        Create an encrypted TOML file from a JSON string.

        Args:
                json_str (str): The JSON-formatted string to convert.
                filename (str): The name of the file to save the encrypted TOML data to.
        """
        data = json.loads(json_str)
        self.save(data, filename)
