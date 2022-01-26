
from ..logCatParser import *


def test_nr_exception_in_sample():
	parser = LogCatParser("threadtime","log_samples/metaLog.log")
	parser.parseFile()
	assert parser.stats.errors["Exception"] == 1
	assert parser.stats.errors["NoProviderInfo"] == 50
