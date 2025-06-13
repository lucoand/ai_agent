import unittest
import subprocess
import os

class TestCalculator(unittest.TestCase):

    def test_division_by_zero(self):
        process = subprocess.Popen(['python', 'main.py', '1 / 0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.assertIn("Error: division by zero", stderr.decode())

if __name__ == '__main__':
    unittest.main()
