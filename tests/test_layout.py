from django.test import TestCase
from material.layout import _children_sizes, AUTO


class Test(TestCase):
    def test_auto_spread_child_on_same_line(self):
        sizes = _children_sizes([AUTO, AUTO], grid_size=12, keep_in_row=True)
        self.assertEqual(sizes, [6, 6])

    def test_auto_spread_child_on_new_line(self):
        sizes = _children_sizes([AUTO, AUTO, AUTO], grid_size=4, keep_in_row=False)
        self.assertEqual(sizes, [4, 4, 4])

    def test_auto_spread_child_fails(self):
        with self.assertRaises(ValueError):
            _children_sizes(
                [AUTO, AUTO, AUTO, AUTO, AUTO],
                grid_size=12, keep_in_row=True
            )

    def test_spread_over_free_place(self):
        sizes = _children_sizes([8, AUTO, 3], grid_size=12, keep_in_row=True)
        self.assertEqual(sizes, [8, 1, 3])

    def test_spread_two_elements_over_free_place(self):
        sizes = _children_sizes([5, AUTO, 3, AUTO], grid_size=12, keep_in_row=True)
        self.assertEqual(sizes, [5, 2, 3, 2])

    def test_cant_spread_too_much(self):
        with self.assertRaises(ValueError):
            _children_sizes(
                [12, 1],
                grid_size=12, keep_in_row=True
            )
