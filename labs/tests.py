from django.test import TestCase

from .models import Result


class ResultFlagTests(TestCase):
    def test_flags_values_outside_reference_range(self):
        below = Result(value=2, ref_low=3, ref_high=8)
        within = Result(value=5, ref_low=3, ref_high=8)
        above = Result(value=10, ref_low=3, ref_high=8)

        self.assertTrue(below.flagged)
        self.assertFalse(within.flagged)
        self.assertTrue(above.flagged)
