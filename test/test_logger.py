import logging
import unittest
from main import color_logger  # 替换为实际模块名


class TestColorLogger(unittest.TestCase):

    def setUp(self):
        """在每个测试之前执行，初始化日志记录器"""
        self.logger = color_logger()

    def test_logger_not_none(self):
        """测试logger是否成功创建"""
        self.assertIsNotNone(self.logger)

    def test_logger_has_handlers(self):
        """测试logger是否有处理器"""
        self.assertGreater(len(self.logger.handlers), 0)

    def test_logger_level(self):
        """测试logger的日志级别"""
        self.assertEqual(self.logger.level, logging.DEBUG)

    def test_console_handler_level(self):
        """测试控制台处理器的日志级别"""
        console_handler = self.logger.handlers[0]
        self.assertEqual(console_handler.level, logging.DEBUG)

    def test_file_handler_level(self):
        """测试文件处理器的日志级别"""
        file_handler = self.logger.handlers[1]
        self.assertEqual(file_handler.level, logging.INFO)


if __name__ == '__main__':
    unittest.main()
