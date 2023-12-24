import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from lsystem import main as ls  # type: ignore # noqa: E402


class BaseLSystemTestCase(unittest.TestCase):
    Test_LSystem = ls.BaseLSystem('F', 10, {'F': 10, 'A': 5},
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

if __name__ == '__main__':
    unittest.main()