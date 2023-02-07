import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import rule  # type: ignore # noqa: E402


class RulePatternTestCase(unittest.TestCase):
    def test_good_pattern(self):
        with self.subTest():
            test_step = 'F->FF'
            self.assertNotEqual(rule.parse_rule(test_step), None)
        with self.subTest():
            test_step = 'A<F>B->FF'
            self.assertNotEqual(rule.parse_rule(test_step), None)
        with self.subTest():
            test_step = 'A<F(0.5)->FF'
            self.assertNotEqual(rule.parse_rule(test_step), None)
        with self.subTest():
            test_step = 'F->F+FF'
            self.assertNotEqual(rule.parse_rule(test_step), None)

    def test_pattern_raise(self):
        self.assertRaises(TypeError, rule.parse_rule)


class RuleMethodsTestCase(unittest.TestCase):
    data = ['J(0.5)->JJ', 'A<F(0.5)->FF', 'A<B>A->FB']

    def test_searching(self):
        with self.subTest():
            case_value = rule.give_rule_with_base('F', self.data)
            self.assertEqual(case_value, self.data[1])
        with self.subTest():
            case_value = rule.give_rule_with_base('I', self.data)
            self.assertEqual(case_value, None)
        with self.subTest():
            case_value = rule.give_rule_with_base('J', self.data)
            self.assertEqual(case_value, self.data[0])

    def test_requirements_checker(self):
        with self.subTest():
            test_state = 'ABAAA'
            val = rule.check_pos_requirements(self.data[2], test_state, 1)
            self.assertEqual(val, True)
        with self.subTest():
            test_state = 'AAAAA'
            val = rule.check_pos_requirements(self.data[2], test_state, 1)
            self.assertEqual(val, False)
