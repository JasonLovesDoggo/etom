# Encrypted TOML (eTOM)

[![PyPI version](https://badge.fury.io/py/etom.svg)](https://badge.fury.io/py/etom)
[![codecov](https://codecov.io/gh/andrewp-as-is/etom/branch/master/graph/badge.svg)](https://codecov.io/gh/andrewp-as-is/etom)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A Python library for handling encrypted TOML files.

## Installation

You can install the library using pip:

```
pip install etom
```

## Usage

Here's a basic example of how to use the EncryptedTOML class:

```python
from etom import EncryptedTOML

# Create an instance
etom = EncryptedTOML()

# Save encrypted TOML data
data = {"section": {"key": "value"}}
etom.save(data, "config.encrypted.toml")

# Load and decrypt TOML data
loaded_data = etom.load("config.encrypted.toml")

# Update existing encrypted TOML file
new_data = {"section": {"new_key": "new_value"}}
etom.update("config.encrypted.toml", new_data)

# Update a specific key
etom.update_key("config.encrypted.toml", ["section", "specific_key"], "specific_value")

# Convert to JSON
json_str = etom.to_json("config.encrypted.toml")

# Create from JSON
etom.from_json(json_str, "new_config.encrypted.toml")
```

## Running Tests

To run the tests, use the following command:

```
poetry run pytest
```

## License

This project is licensed under the Gpl-3.0 License—see the [LICENSE](LICENSE) file for details.
