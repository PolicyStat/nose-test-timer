import unittest
import mock
from testtimer import TestTimer

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
