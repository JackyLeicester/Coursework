import unittest
from bmi_calculator import BMICalculator

class TestBMICalculator(unittest.TestCase):
    def testObesity(self):
        self.assertIn("obesity", BMICalculator().bmi_calculator(85.3, 1.56))

    def testOverweight(self):
        self.assertIn("overweight", BMICalculator().bmi_calculator(65.9, 1.6))

    def testHealthy(self):
        self.assertIn("healthy", BMICalculator().bmi_calculator(45.5, 1.549))

    def testUnderweight(self):
        self.assertIn("underweight", BMICalculator().bmi_calculator(45.5, 1.6))

    def testError(self):
        self.assertIn("error", BMICalculator().bmi_calculator(-2, 1.56))