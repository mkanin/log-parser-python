"""Test for split."""
from unittest import TestCase

import ddt as ddt

from services import split


@ddt.ddt
class TestSplit(TestCase):
    """The class TestSplit."""

    @ddt.data(
        ("", 1),
        ("a", 1),
        ("a b", 2),
        ("a  b", 2),
        ("a   b", 2),
        ("a b c", 3),
        ("a  b c", 3),
        ("a  b  c", 3),
        ("a   b  c", 3),
        ("a   b   c", 3),
    )
    @ddt.unpack
    def test_split(self, input_str, res_length):
        """Tests split function."""
        res = split(input_str)
        self.assertEqual(res_length, len(res))
