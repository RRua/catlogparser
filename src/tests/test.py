
from ..logCatParser import *


def test_nr_exception_in_sampple():
	parser = LogCatParser("threadtime","log_samples/metaLog.log")
	parser.parseFile()
	assert parser.stats.errors["Exception"] == 1