from rule import *
from random import *
from dataclasses import dataclass, field
from string import ascii_uppercase
from utils import IPair, most_used_angle_symbols


@dataclass(init=True, frozen=False)
class DefaultRuleGenerator:
    alpha_border: IPair = field(init=True, default=IPair(2, 4))
    angles_border: IPair = field(init=True, default=IPair(2, 4))
    groups_to_delete: IPair = field(init=True, default=IPair(0, 3))
    rule_sym_number: IPair = field(init=True, default=IPair(1, 5))
    god: RulePatternCreater = field(init=False, default_factory=RulePatternCreater)

    @staticmethod
    def __generate_alpha_sym(base_alphabet, sym_borders: IPair):
        fa, sa = sym_borders.first, sym_borders.second
        symbols = sample(base_alphabet, randint(fa, sa))
        return symbols

    def __generate_alphabet(self):
        return self.__generate_alpha_sym(ascii_uppercase, self.alpha_border)
    
    def __generate_angles(self):
        return self.__generate_alpha_sym(most_used_angle_symbols, self.angles_border)
    
    def __delete_random_groups(self):
        alpha = self.__generate_alphabet()
        to_delete = self.god.get_base_optional_groups()
        fg, sg = self.groups_to_delete.first, self.groups_to_delete.second
        del_groups = sample(to_delete, randint(fg, sg))
        self.god.delete_groups(del_groups)
        return self.god.get_pattern()
    
    def __change_groups(self):
        alpha, angles = ''.join(self.__generate_alphabet()), ''.join(self.__generate_angles())
        self.god.add_group_info('BASE', alpha, IPair(1, 1))
        groups = [group for group in self.god.get_all_groups() if group != 'BASE' and group in self.god.get_pattern()]
        for group in groups:
            self.god.add_group_info(group, alpha + angles, self.rule_sym_number)
        return self.god.get_pattern()

    def __generate_rules(self):
        return self.__delete_random_groups()

    def out(self):
        self.__delete_random_groups()
        return self.__change_groups()

if __name__ == '__main__':
    gen = DefaultRuleGenerator()
    res = gen.out()
    print(res)
    print(generate_rule(res))