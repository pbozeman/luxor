import unittest

from luxor import client as lc


class TestErrors(unittest.TestCase):
    def test_raise_for_status_ok(self):
        lc.raise_for_status({"Status": 0})

    def test_raise_for_status_error(self):
        with self.assertRaises(lc.LuxorErrorUnknownMethod):
            lc.raise_for_status({"Status": 1})

    def test_raise_for_status_random(self):
        with self.assertRaises(lc.LuxorErrorUnexpectedStatus):
            lc.raise_for_status({"Status": "a"})
