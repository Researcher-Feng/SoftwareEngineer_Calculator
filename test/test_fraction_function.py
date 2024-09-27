import unittest
from fractions import Fraction
from main import convert_mixed_to_fraction, convert_fraction_to_mixed


class TestConversionFunctions(unittest.TestCase):
    def test_convert_mixed_to_fraction(self):
        """Test the conversion of mixed numbers to fractions"""
        # Test conversion of mixed numbers to fractions
        self.assertEqual(convert_mixed_to_fraction("3'1/2"), "7/2")
        self.assertEqual(convert_mixed_to_fraction("2'3/4"), "11/4")
        self.assertEqual(convert_mixed_to_fraction("0'1/3"), "1/3")

        # Test conversion of multiple mixed numbers
        self.assertEqual(convert_mixed_to_fraction("3'1/2 + 1'1/4"), "7/2 + 5/4")

        # Test that expressions without mixed numbers remain unchanged
        self.assertEqual(convert_mixed_to_fraction("5/2 + 1/4"), "5/2 + 1/4")

    def test_convert_fraction_to_mixed(self):
        """Test the conversion of fractions to mixed numbers"""
        # Test conversion of fractions to mixed numbers
        self.assertEqual(convert_fraction_to_mixed("7/2"), "3'1/2")
        self.assertEqual(convert_fraction_to_mixed("11/4"), "2'3/4")
        self.assertEqual(convert_fraction_to_mixed("1/3"), "1/3")

        # Test conversion of fractions to whole numbers
        self.assertEqual(convert_fraction_to_mixed("6/3"), "2")

        # Test conversion of fractions to whole numbers
        self.assertEqual(convert_fraction_to_mixed("6"), "6")

        # Test invalid input
        self.assertIsNone(convert_fraction_to_mixed("5/a"))
        self.assertIsNone(convert_fraction_to_mixed("1/0"))  # Case where denominator is zero


if __name__ == '__main__':
    unittest.main()
