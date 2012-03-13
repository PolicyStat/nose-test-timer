import operator
import csv

from nose.plugins.base import Plugin
from time import time

class TestTimer(Plugin):
    "This plugin provides test timings"

    name = 'test-timer'
    score = 1

    def _timeTaken(self):
        if hasattr(self, '_timer'):
            taken = time() - self._timer
        else:
            # test died before it ran (probably error in setup())
            # or success/failure added before test started probably
            # due to custom TestResult munging
            taken = 0.0
        return taken

    def options(self, parser, env):
        """Sets additional command line options."""
        super(TestTimer, self).options(parser, env)
        parser.add_option('--test-timer-output-csv',
                          type='string',
                          dest='output_csv',
                          default=None,
                          help='Path to CSV output')
        parser.add_option('--test-timer-threshold',
                          type='float',
                          dest='threshold',
                          default=None,
                          help='Only capture tests that take longer than the specified number of seconds FLOAT')

    def configure(self, options, config):
        """Configures the test timer plugin."""
        super(TestTimer, self).configure(options, config)
        self.config = config
        self.options = options
        self._timed_tests = {}

    def startTest(self, test):
        """Initializes a timer before starting a test."""
        self._timer = time()

    def stopTest(self, test):
        self._timed_tests[test.address()] = self._timeTaken()

    def report(self, stream):
        """Report the test times"""
        if not self.enabled:
            return
        build_report = self.options.output_csv is not None
        d = sorted(self._timed_tests.iteritems(), key=operator.itemgetter(1))
        reports = []
        for test, time_taken in d:
            if time_taken < self.options.threshold:
                continue
            file, module, rest = test
            test_name = 'unknown test'
            if module:
                test_name = module
                if rest:
                    test_name = '%s:%s' % (module, rest)
            if build_report:
                reports.append(['%0.4f' % time_taken, test_name])
            stream.writeln("%0.4f - %s" % (time_taken, test_name))
        if build_report:
            with open(self.options.output_csv, 'wb') as f:
                writer = csv.writer(f)
                stream.writeln('writerows')
                writer.writerows(reports)

