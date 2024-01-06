import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from lsystem import utils
from lsystem import rule
from lsystem import generator as gen


class MRGTestCase(unittest.TestCase):
    MRG = gen.ManualRuleGenerator()

    def test_parsing_generated_rule(self):
        with self.subTest():
            self.MRG.groups_to_delete = ['RRN', 'POS']
            r = self.MRG.generate_rule()
            try:
                rule.parse_rule(r)
            except ValueError:
                self.fail("parse_rule raised ValueEror unexpecdetly!")
        with self.subTest():
            self.MRG.groups_to_delete = ['RRN', 'RLN']
            r = self.MRG.generate_rule()
            try:
                rule.parse_rule(r)
            except ValueError:
                self.fail("parse_rule raised ValueEror unexpecdetly!")
        with self.subTest():
            self.MRG.expand_deps_dict({'RRN': utils.IPair(1, 2), 'RLN': utils.IPair(2, 3)})
            r = self.MRG.generate_rule()
            try:
                rule.parse_rule(r)
            except ValueError:
                self.fail("parse_rule raised ValueEror unexpecdetly!")

    def test_impossible_cases(self):
        with self.subTest():
            self.MRG.to_delete = ['RRN']
            self.MRG.expand_deps_dict({'RRN': utils.IPair(1, 2), 'BASE': utils.IPair(2, 3)})
            r = self.MRG.generate_rule()
            try:
                rule.parse_rule(r)
            except ValueError:
                self.fail("parse_rule raised ValueEror unexpecdetly!")
        with self.subTest():
            self.MRG.expand_deps_dict({'RRN': utils.IPair(1, 2), 'POS': utils.IPair(2, 2)})
            self.MRG.to_delete = ['RRN', 'POS']
            r = self.MRG.generate_rule()
            try:
                rule.parse_rule(r)
            except ValueError:
                self.fail("parse_rule raised ValueEror unexpecdetly!")
        with self.subTest():
            self.MRG.to_delete = ['BASE', 'RES']
            r = self.MRG.generate_rule()
            try:
                rule.parse_rule(r)
            except ValueError:
                self.fail("parse_rule raised ValueEror unexpecdetly!")


if __name__ == '__main__':
    unittest.main()
