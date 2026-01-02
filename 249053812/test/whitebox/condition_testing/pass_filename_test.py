import unittest
import os

from src import read_file_contents


class TestReadFileContents(unittest.TestCase):
    def setUp(self):
        self.file_name = "test_file.txt"
        self.test_file_contents = "This is a test file."
        with open(self.file_name, "w") as f:
            f.write(self.test_file_contents)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_null(self):
        self.assertRaises(ValueError, read_file_contents, None)

    def test_empty_filename(self):
        self.assertIsNone(read_file_contents(""))

    def test_existing_filename(self):
        self.assertEqual(self.test_file_contents, read_file_contents(self.file_name))

    def test_non_existing_filename(self):
        self.assertIsNone(read_file_contents("non-existent-file.txt"))


if __name__ == "__main__":
    unittest.main()
