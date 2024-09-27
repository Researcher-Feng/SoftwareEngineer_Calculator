import unittest
from main import generate_exercises
class TestGenerateExercises(unittest.TestCase):

    def test_generate_exercises(self):
        """Test if generate_exercises produces the correct number of exercises and unique answers."""
        n = 10  # Number of exercises to generate
        r = 10  # Range for numbers
        exercises, answers = generate_exercises(n, r)

        # Check that we have the correct number of exercises
        self.assertEqual(len(exercises), n)
        self.assertEqual(len(answers), n)

        # Check for duplicates in exercises
        self.assertEqual(len(exercises), len(set(exercises)))

        # Check for duplicates in answers
        self.assertEqual(len(answers), len(set(answers)))

        # Check for negative answers
        for answer in answers:
            # 检查答案是否包含负号
            self.assertFalse('-' in answer, f"Invalid answer: {answer} is negative")

    def test_generate_exercises_with_progress_bar(self):
        """Test if generate_exercises with a progress bar works correctly."""
        n = 5  # Number of exercises to generate
        r = 5  # Range for numbers
        exercises, answers = generate_exercises(n, r, bar=True)

        # Check that we have the correct number of exercises
        self.assertEqual(len(exercises), n)
        self.assertEqual(len(answers), n)

        # Check for duplicates in answers
        self.assertEqual(len(answers), len(set(answers)))

if __name__ == '__main__':
    unittest.main()
