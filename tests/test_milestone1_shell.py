import unittest
from pathlib import Path


class Milestone1ShellTests(unittest.TestCase):
    def test_placeholder_pages_exist(self):
        html = Path('app/index.html').read_text(encoding='utf-8')
        required_labels = [
            'Today',
            'Orders',
            'Products &amp; Stock',
            'Make / Buy',
            'Money',
            'Settings',
        ]

        for label in required_labels:
            self.assertIn(label, html)

    def test_placeholder_note_present(self):
        html = Path('app/index.html').read_text(encoding='utf-8')
        self.assertIn('Placeholder page for Milestone 1.', html)


if __name__ == '__main__':
    unittest.main()
