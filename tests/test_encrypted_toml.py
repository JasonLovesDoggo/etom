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


if __name__ == "__main__":
	unittest.main()
