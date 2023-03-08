from string import punctuation, ascii_lowercase, ascii_uppercase
from math import ceil
from lsystem import WMLLSystem
from drawer import Drawer
from random import randint, uniform, choices, shuffle, choice, random
from typing import Optional, Callable
from utils import IPair, FPair, URE_handler, RFR_handler


class BaseRandomLSystemGenerator:
    # Main generator params
    _axiom_len_range: IPair = IPair(1, 3)
    _alphabet_len_range: IPair = IPair(3, 6)
    __angles_number_range: IPair = IPair(2, 4)
    __angle_value_range: FPair = FPair(-90.0, 90.0)
    _rule_length_range: IPair = IPair(6, 24)
    _rules_number_range = IPair(2, 7)
    _branch_length_range: FPair = FPair(2.0, 10.0)
    _deflection_range: FPair = FPair(-90.0, 90.0)
    _save_symbol: str = '['
    _paste_symbol: str = ']'

    _result_lsystem:  WMLLSystem = WMLLSystem()

    def set_axiom_len_range(self, new_alr: IPair):
        URE_handler(new_alr, 'Axiom length range is not available!')
        self._axiom_len_range = new_alr

    def set_alphabet_len_range(self, new_alr: IPair):
        URE_handler(new_alr, 'Alphabet length range is not available!')
        self._alphabet_len_range = new_alr

    def set_angles_number_range(self, new_anr: IPair):
        URE_handler(new_anr, 'Angles number range is not available!')
        self._angles_number_range = new_anr

    def set_angle_value_range(self, new_avr: FPair):
        self._angle_value_range = new_avr

    def set_rule_length_range(self, new_rlr: IPair):
        URE_handler(new_rlr, 'Rule length range is not available!')
        self._rule_length_range = new_rlr

    def set_rules_number_range(self, new_rnr: IPair):
        URE_handler(new_rnr, 'Rules number range is not available!')
        self._rules_number_range = new_rnr

    def set_branch_length_range(self, new_blr: FPair):
        URE_handler(new_blr, 'Branch length range is not available!')
        self._branch_length_range = new_blr

    def set_deflection_range(self, new_dr: FPair):
        self._deflection_range = new_dr

    def get_using_symbols(self) -> str:
        result = ''.join(self._result_lsystem.alphabet.keys()) + \
                 ''.join(self._result_lsystem.angles.keys()) + \
                 self._save_symbol + self._paste_symbol
        return result

    def get_lsystem(self) -> WMLLSystem:
        return self._result_lsystem

    def generate_alphabet(self) -> dict[str, float]:
        symbols_num: int = randint(self._alphabet_len_range.first,
                                   self._alphabet_len_range.second)
        symbols: str = ascii_uppercase[:symbols_num]
        lborder: float = self._branch_length_range.first
        rborder: float = self._branch_length_range.second
        values = [uniform(lborder, rborder) for i in range(len(symbols))]
        alphabet = {key: value for key, value in zip(symbols, values)}
        alphabet = dict(sorted(alphabet.items(), key=lambda x: x[1]))
        self._result_lsystem.alphabet = alphabet
        return alphabet

    def generate_angles(self) -> dict[str, float]:
        angles_number = randint(self.__angles_number_range.first,
                                self.__angles_number_range.second)
        symbols = (punctuation + ascii_lowercase)[:angles_number]
        lborder: float = self.__angle_value_range.first
        rborder: float = self.__angle_value_range.second
        values = [uniform(lborder, rborder) for i in range(len(symbols))]
        angles = {key: value for key, value in zip(symbols, values)}
        self._result_lsystem.angles = angles
        return angles

    def generate_axiom(self, symbols: Optional[str] = None) -> str:
        if symbols is None:
            symbols = ''.join(self._result_lsystem.alphabet.keys())
        axiom_length: int = randint(self._axiom_len_range.first,
                                    self._axiom_len_range.second)
        diff_symbols_number: int = randint(self._axiom_len_range.first,
                                           min(len(symbols), axiom_length))
        line: str = ''.join(choices(symbols, k=diff_symbols_number))
        line.rjust(axiom_length, line[-1])
        shuffle(list(line))
        self._result_lsystem.axiom = line
        self._result_lsystem.state = self._result_lsystem.axiom
        return line

    def generate_random_rule(self, diff_symbols: list[str] = None) -> str:
        if diff_symbols is None:
            diff_symbols = self.get_using_symbols()
        rule_length: int = randint(self._rule_length_range.first,
                                   self._rule_length_range.second) - 2
        base_rule_len = randint(1, ceil(rule_length / 8))
        base_rule: str = ''.join(choices(diff_symbols, k=base_rule_len))
        result = ''.join(choices(self.get_using_symbols(), k=rule_length))
        rule = base_rule + '->' + result
        return rule

    def generate_rules(self, 
                       rule_generator_func: Callable = None,
                       symbols = None) -> list[str]:
        if rule_generator_func is None:
            rule_generator_func = self.generate_random_rule
        rule_length: int = randint(self._rules_number_range.first,
                                   self._rules_number_range.second)
        rules = list()
        for i in range(rule_length):
            if symbols is not None:
                rules.append(rule_generator_func(symbols))
            else:
                rules.append(rule_generator_func())
        self._result_lsystem.rules = rules
        return rules


class BaseTreeGenerator(BaseRandomLSystemGenerator):
    __increasion_coefficient: int = 2
    __turn_possibility: float = 0.05
    __absolute_angle_range: FPair = FPair(10.0, 20.0)
    __angle_pair_number_range: IPair = IPair(1, 2)
    __not_bracket_possibility: float = 0.15

    def generate_angles(self) -> dict[str, float]:
        angle_pair_number = randint(self.__angle_pair_number_range.first, 
                                    self.__angle_pair_number_range.second)
        symbols, angles = punctuation[:angle_pair_number * 2 + 1], dict()
        print(angle_pair_number, symbols)
        for i in range(angle_pair_number):
            angle = uniform(self.__absolute_angle_range.first, 
                            self.__absolute_angle_range.second)
            angles[symbols[i]] = -angle
            angles[symbols[i+1]] = angle
        self._result_lsystem.angles = angles
        return angles


    def set_increasion_coefficient(self, new_ic: int):
        if new_ic <= 0:
            raise ValueError('New increasion coeff value below or equal zero!')
        self.__increasion_coefficient = new_ic

    def set_turn_possibility(self, new_tb: float):
        RFR_handler(new_tb, 'Turn possibility')
        self.__turn_possibility = new_tb

    def set_non_bracket_possibility(self, new_nbp):
        RFR_handler(new_nbp, 'Non dracket possibility')
        self.__not_bracket_possibility = new_nbp

    def get_using_symbols(self) -> str:
        return super().get_using_symbols() + '*' * 2

    def generate_increasion_rule(self) -> str:
        symbol = choice(list(self._result_lsystem.axiom))
        rule = symbol + '->' + (symbol * self.__increasion_coefficient)
        return rule

    def generate_ccrule(self) -> str:
        rule_length: int = randint(self._rule_length_range.first,
                                   self._rule_length_range.second) - 2
        base_symbol = self._result_lsystem.axiom[0]
        res = self.generate_tree_rule()
        return base_symbol + '->' + res[res.index('>') + 1:]

    def generate_tree_rule(self) -> str:
        rule_length: int = randint(self._rule_length_range.first,
                                   self._rule_length_range.second) - 2
        base_symbols = list(self._result_lsystem.alphabet.keys())
        base_length = randint(1, ceil(rule_length // 5) + 1)
        diff_base_symbols_num = randint(1, base_length)
        base_symbols = choices(base_symbols, k=diff_base_symbols_num)
        res_symbols, sm = '', self._result_lsystem.angles.keys()
        for i in range(rule_length - base_length):
            if random() < self.__turn_possibility:
                res_symbols += str(choice(list(sm)))
            elif random() > 1 - self.__not_bracket_possibility:
                res_symbols += str(choice(['[', ']']))
            res_symbols += str(choice(self.get_using_symbols()))
        return ''.join(base_symbols) + '->' + res_symbols

    def generate_tree_rules(self) -> list[str]:
        rules = self.generate_rules(self.generate_tree_rule)
        rules.append(self.generate_increasion_rule())
        rules.append(self.generate_ccrule())
        self._result_lsystem.rules = rules
        return rules


if __name__ == '__main__':
    god = BaseTreeGenerator()
    god.set_angle_value_range(FPair(-20, 20.0))
    god.set_axiom_len_range(IPair(2, 3))
    god.set_branch_length_range(FPair(7.0, 20.0))
    god.set_rules_number_range(IPair(2, 3))
    print('BEFORE:')
    print(god.generate_alphabet())
    print(god.generate_angles())
    print(god.generate_axiom())
    print(god.generate_tree_rules())
    ls = god.get_lsystem()
    ls.thickness = 10
    ls.generate(3)
    print(ls.state)
    pen = Drawer()
    pen.thickness_reduction = 1.0
    pen.image_size = (4000, 2000)
    pen.draw_tree([2000, 1000], ls)
