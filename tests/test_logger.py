import unittest
import sys

sys.path.append('/Users/shruti/Documents/projects/data-collection-pipeline/project')
import logger

class LoggerTestCase(unittest.TestCase):

    def setUp(self):
        self.user = logger.Logger()
        pass

    def test_log_error(self):

        expected_value = None
        actual_value = None

        self.assertEqual(expected_value, actual_value)


unittest.main(argv=[''], verbosity=2, exit=False)