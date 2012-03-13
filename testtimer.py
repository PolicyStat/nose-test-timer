import csv
import time

from nose.plugins.base import Plugin

class TestTimer(Plugin):
    "This plugin provides test timings"

    name = 'test-timer'
    score = 1

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
                          default=0,
                          help='Only capture tests that take longer than the specified number of seconds FLOAT')

    def configure(self, options, config):
        """Configures the test timer plugin."""
        super(TestTimer, self).configure(options, config)
        self.config = config
        self.options = options
        self.tests = {}

    def startTest(self, test):
        """Initializes a timer before starting a test."""
        self.tests[test.address()] = [time.time(), time.time()]

    def stopTest(self, test):
        self.tests[test.address()][1] = time.time()

    def _fully_qualified_test_address(self, test):
        path, module, rest = test
        name = None
        if module:
            name = module
            if rest:
                name = '%s:%s' % (module, rest)
        return name

    def _generate_report(self):
        test_deltas = []
        for address, times in self.tests.iteritems():
            delta = times[1] - times[0]
            test_deltas.append([delta,
                self._fully_qualified_test_address(address)])
        test_deltas_sorted = sorted(test_deltas)

        reports = []
        for delta, test in test_deltas_sorted:
            if delta <= self.options.get('threshold', 0):
                continue
            report = ['%0.4f' % delta, test]
            reports.append(report)
        return reports

    def _write_csv(self, reports):
        if self.options.output_csv is not None:
            with open(self.options.output_csv, 'wb') as f:
                writer = csv.writer(f)
                writer.writerows(reports)

    def report(self, stream):
        """Report the test times"""
        if not self.enabled:
            return
        reports = self.generate_report()
        self._write_csv(reports)
        for report in reports:
            stream.writeln(' - '.join(report))

