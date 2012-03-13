import unittest
import mock
from nose_test_timer import TestTimer

class TestTimerTest(unittest.TestCase):

    def setUp(self):
        self.test = mock.Mock(
            address=mock.Mock(return_value=mock.sentinel.address)
        )
        self.timer = TestTimer()
        self.timer.configure({}, {})


    @mock.patch('time.time', return_value=mock.sentinel.time)
    def test_startTest(self, time_mock):
        self.timer.startTest(self.test)
        actual = self.timer.tests.get(mock.sentinel.address, None)
        expected = [mock.sentinel.time, mock.sentinel.time]
        self.assertEqual(actual, expected)

    @mock.patch('time.time', return_value=mock.sentinel.time_start)
    def test_stopTest(self, time_mock):
        self.timer.startTest(self.test)
        time_mock.return_value = mock.sentinel.time_stop
        self.timer.stopTest(self.test)
        actual = self.timer.tests.get(mock.sentinel.address, None)
        expected = [mock.sentinel.time_start, mock.sentinel.time_stop]
        self.assertEqual(actual, expected)

    def test_fully_qualified_test_address_nothing(self):
        address = self.timer._fully_qualified_test_address(
                (None, None, None))
        self.assertEqual(address, None)

    def test_fully_qualified_test_address_module(self):
        address = self.timer._fully_qualified_test_address(
                (None, 'module', None))
        self.assertEqual(address, 'module')

    def test_fully_qualified_test_address_module_and_name(self):
        address = self.timer._fully_qualified_test_address(
                (None, 'module', 'foo'))
        self.assertEqual(address, 'module:foo')

    def test_generate_report_is_empty(self):
        reports = self.timer._generate_report()
        self.assertEqual(reports, [])

    def test_generate_report_returns_reports(self):
        self.test.address.return_value = (None, 'foo', 'bar')
        with mock.patch('time.time', return_value=1):
            self.timer.startTest(self.test)
        with mock.patch('time.time', return_value=10):
            self.timer.stopTest(self.test)
        self.timer._fully_qualified_test_address = mock.Mock(
                return_value=mock.sentinel.address)
        expected = [['%0.4f' % 9, mock.sentinel.address]]
        actual = self.timer._generate_report()
        self.assertEqual(actual, expected)

    def test_report_should_generate_a_report(self):
        with mock.patch.object(self.timer, '_generate_report',
                mocksignature=True) as generate_report:
            with mock.patch.object(self.timer, '_write_csv',
                    mocksignature=True):
                generate_report.return_value = []
                self.timer.enabled = True
                self.timer.report(None)
            self.assertTrue(generate_report.called)

    def test_report_should_write_csv_report(self):
        with mock.patch.object(self.timer, '_generate_report',
                mocksignature=True):
            with mock.patch.object(self.timer, '_write_csv',
                    mocksignature=True) as write_csv:
                self.timer.enabled = True
                self.timer.report(None)
                self.assertTrue(write_csv.called)

