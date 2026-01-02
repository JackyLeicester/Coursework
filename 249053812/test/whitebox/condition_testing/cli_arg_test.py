import io
import os
import unittest
from unittest.mock import patch

from src import main
from src.evaluator import RuntimeEvaluationError


class TestCliArgs(unittest.TestCase):
    def setUp(self):
        self.file_name_access = "test_access"
        self.file_name_no_access = "test_no_access"
        self.test_file_contents_access = "print(arg);"
        self.test_file_contents_no_access = "print(1);"

        with open(self.file_name_access, "w") as f:
            f.write(self.test_file_contents_access)

        with open(self.file_name_no_access, "w") as f:
            f.write(self.test_file_contents_no_access)

    def tearDown(self):
        if os.path.exists(self.file_name_access):
            os.remove(self.file_name_access)

        if os.path.exists(self.file_name_no_access):
            os.remove(self.file_name_no_access)

    @patch("sys.argv", new=["main.py", "test_access", "--", "1"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_args_present_and_accessed(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue(), "1")

    @patch("sys.argv", new=["main.py", "test_no_access", "--", "1.1"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_args_present_and_not_accessed(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue(), "1")

    @patch("sys.argv", new=["main.py", "test_access", "--", "1", "2"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_multiple_arguments(self, mock_stdout):
        self.assertRaises(SystemExit, main)

    @patch("sys.argv", new=["main.py", "test_access"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_args_absent_and_accessed(self, mock_stdout):
        self.assertRaises(RuntimeEvaluationError, main)

    @patch("sys.argv", new=["main.py", "test_no_access"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_args_absent_and_not_accessed(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue(), "1")


if __name__ == "__main__":
    unittest.main()
