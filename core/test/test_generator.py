import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils import IPair
from rule import parse_rule
import generator as gen   # type: ignore # noqa: E402

class SettersPatternCase(unittest.TestCase):
    def ure_handler_test(self):
        with self.subTest():
            self.assertRaises(ValueError, gen.URE_handler, (-1, 10))
        with self.subTest():
            self.assertRaises(ValueError, gen.URE_handler, (10, -2))
        with self.subTest():
            self.assertRaises(ValueError, gen.URE_handler, (10, 2))
    
class MethodsTestCase(unittest.TestCase):
    test_gen = gen.BaseRandomLSystemGenerator()

    def generate_alphabet_test(self):
        with self.subTest():
            self.test_gen._alphabet_len_range = IPair(1, 2)
            self.test_gen._result_lsystem.alphabet = \
                self.test_gen.generate_alphabet()
            self.assertGreater(len(self.test_gen._result_lsystem.alphabet, 0))
        with self.subTest():
            self.test_gen._alphabet_len_range = IPair(1, 3)
            self.test_gen._result_lsystem.alphabet = \
                self.test_gen.generate_alphabet()
            self.assertLess(len(self.test_gen._result_lsystem.alphabet, 4))
    
    def generate_axiom_test(self):
        with self.subTest():
            self.test_gen._axiom_len_range = IPair(1, 2)
            self.test_gen._result_lsystem.axiom = \
                self.test_gen.generate_axiom()
            self.assertGreater(len(self.test_gen._result_lsystem.axiom, 0))
        with self.subTest():
            self.test_gen._axiom_len_range = IPair(1, 3)
            self.test_gen._result_lsystem.axiom = \
                self.test_gen.generate_axiom()
            self.assertLess(len(self.test_gen._result_lsystem.axiom, 4))
        
    def generate_random_rule_test(self):
        with self.subTest():
            r = self.test_gen.generate_random_rule()
            self.assertRegexpMatches(r)
        with self.subTest():
            r = self.test_gen.generate_random_rule()
            self.assertLess(len(r), 
                            self.test_gen._rule_length_range.second + 1)
        with self.subTest():
            r = self.test_gen.generate_random_rule()
            self.assertGreater(len(r), 
                               self.test_gen._rule_length_range.first - 1)

    """ TODO: Do more stable tests for BaseRandomLSystemGenerator 
              Do some tests for TreeGenerator """
