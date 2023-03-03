import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import generator as gen   # type: ignore # noqa: E402


class SettersPatternCase(unittest.TestCase):
    def ure_handler_test(self):
        with self.subTest():
            self.assertRaises(ValueError, gen.URE_handler, (-1, 10))
        with self.subTest():
            self.assertRaises(ValueError, gen.URE_handler, (10, -2))
        with self.subTest():
            self.assertRaises(ValueError, gen.URE_handler, (10, 2))
    
    #TODO: do tests for generating rules)
