import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import lsystem as ls # type: ignore # noqa: E402

class LSystemTestCase(unittest.TestCase):
    Test_LSystem = ls.LSystem('F', 10, {'F': 10, 'A': 5}, \
                              {'-': 30, '+': 30},
                              ['F->FAF', 'A<F->FA'])

    def test_rule_adding(self):
        with self.subTest():
            new_rule = 'FFFF->FF'
            res = self.Test_LSystem.add_rule(new_rule)
            self.assertEqual(res, True)
        with self.subTest():
            new_rule = 'F'
            res = self.Test_LSystem.add_rule(new_rule)
            self.assertEqual(res, False)
        with self.subTest():
            new_rule = 'F->FAF'
            res = self.Test_LSystem.add_rule(new_rule)
            self.assertEqual(res, True)
        
