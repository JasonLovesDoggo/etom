import json
import os
import tempfile
import unittest

from etom.core import EncryptedTOML


class TestEncryptedTOML(unittest.TestCase):
    def setUp(self):
        self.key = EncryptedTOML.generate_key()
        self.etom = EncryptedTOML(self.key)
        self.test_data = {
            "section1": {"key1": "value1", "key2": 42},
            "section2": {"nested": {"key3": [1, 2, 3]}},
        }
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "test.encrypted.toml")

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        os.rmdir(self.temp_dir)

    def test_save_and_load(self):
        self.etom.save(self.test_data, self.temp_file)
        loaded_data = self.etom.load(self.temp_file)
        self.assertEqual(self.test_data, loaded_data)

    def test_update(self):
        self.etom.save(self.test_data, self.temp_file)
        new_data = {"section1": {"key1": "updated_value"}}
        self.etom.update(self.temp_file, new_data)
        loaded_data = self.etom.load(self.temp_file)
        self.assertEqual(loaded_data["section1"]["key1"], "updated_value")

    def test_update_key(self):
        self.etom.save(self.test_data, self.temp_file)
        self.etom.update_key(self.temp_file, ["section2", "nested", "key3"], [4, 5, 6])
        loaded_data = self.etom.load(self.temp_file)
        self.assertEqual(loaded_data["section2"]["nested"]["key3"], [4, 5, 6])

    def test_json_conversion(self):
        self.etom.save(self.test_data, self.temp_file)
        json_str = self.etom.to_json(self.temp_file)
        new_file = os.path.join(self.temp_dir, "new.encrypted.toml")
        self.etom.from_json(json_str, new_file)
        loaded_data = self.etom.load(new_file)
        self.assertEqual(self.test_data, loaded_data)
        os.remove(new_file)

    def test_init_with_none_key(self):
        with self.assertRaises(ValueError):
            EncryptedTOML(None)  # Test the case where key is None

    def test_update_with_empty_new_data(self):
        self.etom.save(self.test_data, self.temp_file)
        self.etom.update(self.temp_file, {})  # Test update with empty new_data
        loaded_data = self.etom.load(self.temp_file)
        self.assertEqual(self.test_data, loaded_data)  # Data should remain unchanged

    def test_update_key_with_nonexistent_path(self):
        self.etom.save(self.test_data, self.temp_file)
        with self.assertRaises(KeyError):
            self.etom.update_key(self.temp_file, ["nonexistent", "path"], "new_value")

    def test_update_key_with_existing_nested_path(self):
        self.etom.save(self.test_data, self.temp_file)
        self.etom.update_key(
            self.temp_file, ["section2", "nested", "new_key"], "new_value"
        )
        loaded_data = self.etom.load(self.temp_file)
        self.assertEqual(loaded_data["section2"]["nested"]["new_key"], "new_value")

    def test_from_json_with_invalid_json(self):
        invalid_json = "this is not valid json"
        new_file = os.path.join(self.temp_dir, "invalid.encrypted.toml")
        with self.assertRaises(json.JSONDecodeError):
            self.etom.from_json(invalid_json, new_file)


if __name__ == "__main__":
    unittest.main()
