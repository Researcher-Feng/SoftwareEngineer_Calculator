import logging
import unittest
from main import color_logger


class TestColorLogger(unittest.TestCase):

    def setUp(self):
        """Executed before each test, initializing the logger"""
        self.logger = color_logger()

    def test_logger_not_none(self):
        """Test if the logger is successfully created"""
        self.assertIsNotNone(self.logger)

    def test_logger_has_handlers(self):
        """Test if the logger has handlers"""
        self.assertGreater(len(self.logger.handlers), 0)

    def test_logger_level(self):
        """Test the logging level of the logger"""
        self.assertEqual(self.logger.level, logging.DEBUG)

    def test_console_handler_level(self):
        """Test the logging level of the console handler"""
        console_handler = self.logger.handlers[0]
        self.assertEqual(console_handler.level, logging.DEBUG)

    def test_file_handler_level(self):
        """Test the logging level of the file handler"""
        file_handler = self.logger.handlers[1]
        self.assertEqual(file_handler.level, logging.INFO)


if __name__ == '__main__':
    unittest.main()
