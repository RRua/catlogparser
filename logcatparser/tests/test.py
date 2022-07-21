from unittest import TestCase
import os
from ..logCatParser import *

this_test_file_path = os.path.dirname(os.path.abspath(__file__))


class SimpleTest(TestCase):
	def test_nr_exception_in_sample(self):
		test_file_path = os.path.join(this_test_file_path, "log_samples", "metaLog.log")
		parser = LogCatParser("threadtime")
		parser.parse_file(test_file_path)
		self.assertEqual(len(parser.get_logs_of_error("JavaException")), parser.stats.know_errors["JavaException"])