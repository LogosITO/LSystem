import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import rule  # type: ignore # noqa: E402


class RulePatternTestCase(unittest.TestCase):
    def test_good_pattern_first(self):
        test_step = 'F->FF'
        self.assertNotEqual(rule.parse_rule(test_step), None)
    
    def test_good_pattern_second(self):
        test_step = 'A<F>B->FF'
        self.assertNotEqual(rule.parse_rule(test_step), None)
    
    def test_good_pattern_third(self):
        test_step = 'A<F(0.5)->FF'
        self.assertNotEqual(rule.parse_rule(test_step), None)

    def test_pattern_raise(self):
        self.assertRaises(TypeError, rule.parse_rule)


class RuleMethodsTestCase(unittest.TestCase):
    data = ['J(0.5)->JJ', 'A<F(0.5)->FF', 'A<B>A->FB']

    def test_searching_first(self):
        test_value = rule.give_rule_with_base('F', self.data)
        self.assertEqual(test_value, self.data[1])
    
    def test_searching_second(self):
        test_value = rule.give_rule_with_base('I', self.data)
        self.assertEqual(test_value, None)
    
    def test_requirements_checker_first(self):
        test_state = 'ABAAA'
        val = rule.check_pos_requirements(self.data[2], test_state, 1)
        self.assertEqual(val, True)

    def test_requirements_checker_second(self):
        test_state = 'AAAAA'
        val = rule.check_pos_requirements(self.data[2], test_state, 1)
        self.assertEqual(val, False)
    
