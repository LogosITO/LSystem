import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from lsystem import rule 
from lsystem.utils import IPair


data = ['J[0.5]->JJ', 'A<F[0.5]->FF',
        'A<B>A->FB', '!A<K>!B->KBAA',
        'A<F>!A->FF', 'J->F+-A']


grwb = lambda val: rule.get_rules_with_base(val, data) 
gfrwb = lambda val: rule.get_first_rule_with_base(val, data)


class RulePatternTestCase(unittest.TestCase):
    def test_good_pattern(self):
        with self.subTest():
            test_step = 'F->FF'
            self.assertNotEqual(rule.parse_rule(test_step), None)
        with self.subTest():
            test_step = 'A<F>B->FF'
            self.assertNotEqual(rule.parse_rule(test_step), None)
        with self.subTest():
            test_step = 'A<F[0.5]->FF'
            self.assertNotEqual(rule.parse_rule(test_step), None)
        with self.subTest():
            test_step = 'F->F+FF'
            self.assertNotEqual(rule.parse_rule(test_step), None)
        with self.subTest():
            test_step = 'F(x)->F(x+1)'
            self.assertNotEqual(rule.parse_rule(test_step), None)

    def test_pattern_raise(self):
        self.assertRaises(TypeError, rule.parse_rule)


class RuleMethodsTestCase(unittest.TestCase):

    def test_grwb(self):
        with self.subTest():
            self.assertEqual(grwb('F'), [data[1], data[-2]])
        with self.subTest():
            self.assertEqual(grwb('I'), [])
        with self.subTest():
            self.assertEqual(grwb('J'), [data[0], data[-1]])
        with self.subTest():
            self.assertEqual(grwb('K'), [data[3]])
        
    def test_gfrwb(self):
        with self.subTest():
            self.assertEqual(gfrwb('F'), data[1])
        with self.subTest():
            self.assertEqual(gfrwb('I'), None)
        with self.subTest():
            self.assertEqual(gfrwb('J'), data[0])
        with self.subTest():
            self.assertEqual(gfrwb('K'), data[3])

    def test_requirements_checker(self):
        with self.subTest():
            test_state = 'ABAAA'
            val = rule.check_pos_requirements(data[2], test_state, 1)
            self.assertEqual(val, True)
        with self.subTest():
            test_state = 'AAAAA'
            val = rule.check_pos_requirements(data[2], test_state, 1)
            self.assertEqual(val, False)
        with self.subTest():
            test_state = 'AFBA'
            val = rule.check_pos_requirements(data[4], test_state, 1)
            self.assertEqual(val, True)

class PatternCreaterTestCase(unittest.TestCase):
    r = rule.RulePatternCreater()

    def searching_test(self):
        with self.subTest():
            with self.assertRaises(ValueError):
                self.r.add_group_info('bas', 'ABC', IPair(1, 2))
        with self.subTest():
            with self.assertRaises(ValueError):
                self.r.add_group_info('base', 'ABC', IPair(-1, 3))

    def adding_info_test(self):
        self.r.add_group_info('base', 'sdf', IPair(2, 5))
        self.assertEqual(r'^(?P<RLN>)(?P<BASE>)(?P<PAR>)(?P<RRN>)->\
                         (?P<RES>)(?P<RPAR>)$', self.r.get_pattern())

    def tearDown(self):
        self.r.clear_changes()
