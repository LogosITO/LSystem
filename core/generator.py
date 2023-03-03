from string import punctuation, ascii_lowercase, ascii_uppercase
from random import randint, choices, shuffle, uniform
from math import ceil, floor
from typing import Union, NamedTuple
from lsystem import WMLLSystem
from drawer import Drawer


most_used_angle_symbols = ['+', '-', '^', '(', ')', '&', '?']


FPair = NamedTuple('FPair', [('first', float), ('second', float)])
IPair = NamedTuple('IPair', [('first', int), ('second', int)])


def URE_handler(range: Union[FPair, IPair], error_message: str = ''):
    if range.first < 0 or range.second < 0 or range.second - range.first < 0:
        raise ValueError(error_message)


class BaseRandomLSystemGenerator:
    #Main generator params
    __axiom_len_range: IPair = IPair(1, 3)
    __alphabet_len_range: IPair = IPair(3, 6)
    __angles_number_range: IPair = IPair(2, 4)
    __angle_value_range: FPair = FPair(-90.0, 90.0)
    __rule_length_range: IPair = IPair(6, 24)
    __rules_number_range = IPair(2, 7)
    __branch_length_range: FPair = FPair(2.0, 10.0)
    __deflection_range: FPair = FPair(-90.0, 90.0)

    __increase_coeff: int = 2

    __result_lsystem:  WMLLSystem = WMLLSystem()
    
    def set_axiom_len_range(self, new_alr: IPair):
        URE_handler(new_alr, 'Axiom length range is not available!')
        self.__axiom_len_range = new_alr

    def set_alphabet_len_range(self, new_alr: IPair):
        URE_handler(new_alr, 'Alphabet length range is not available!')
        self.__alphabet_len_range = new_alr
    
    def set_angles_number_range(self, new_anr: IPair):
        URE_handler(new_anr, 'Angles number range is not available!')
        self.__angles_number_range = new_anr

    def set_angle_value_range(self, new_avr: FPair):
        self.__angle_value_range = new_avr

    def set_rule_length_range(self, new_rlr: IPair):
        URE_handler(new_rlr, 'Rule length range is not available!')
        self.__rule_length_range = new_rlr

    def set_branch_length_range(self, new_blr: FPair):
        URE_handler(new_blr, 'Branch length range is not available!')
        self.__branch_length_range = new_blr

    def set_deflection_range(self, new_dr: FPair):
        self.__deflection_range = new_dr

    def get_lsystem(self) -> WMLLSystem:
        return self.__result_lsystem

    def generate_alphabet(self) -> dict[str, float]:
        symbols_num: int = randint(self.__alphabet_len_range.first,
                                   self.__alphabet_len_range.second)
        symbols: list[str] = choices(ascii_uppercase, k=symbols_num)
        lborder: float = self.__branch_length_range.first
        rborder: float = self.__branch_length_range.second
        values = [uniform(lborder, rborder) for i in range(len(symbols))]
        alphabet = {key: value for key, value in zip(symbols, values)}
        alphabet = dict(sorted(alphabet.items(), key=lambda x: x[1]))
        self.__result_lsystem.alphabet = alphabet
        return alphabet
    
    def generate_angles(self) -> dict[str, float]:
        angles_number = randint(self.__angles_number_range.first,
                                self.__angles_number_range.second)
        symbols = (punctuation + ascii_lowercase)[:angles_number]
        lborder: float = self.__angle_value_range.first
        rborder: float = self.__angle_value_range.second
        values = [uniform(lborder, rborder) for i in range(len(symbols))]
        angles = {key: value for key, value in zip(symbols, values)}
        self.__result_lsystem.angles = angles
        return angles

    def generate_axiom(self, symbols: str = None) -> str:
        if symbols is None:
            symbols = ''.join(self.__result_lsystem.alphabet.keys())
        axiom_length: int = randint(self.__axiom_len_range.first,
                                    self.__axiom_len_range.second)
        different_symbols_number: int = randint(self.__axiom_len_range.first,
                                                min(len(symbols), axiom_length))
        line: str = ''.join(choices(symbols, k=different_symbols_number))
        line.rjust(axiom_length, line[-1])
        shuffle(list(line))
        self.__result_lsystem.axiom = line
        self.__result_lsystem.state = self.__result_lsystem.axiom
        return line

    def generate_increasing_rule(self, symbol: str) -> str:
        increasing_rule: str = symbol + '->' + symbol[0] * self.__increase_coeff
        return increasing_rule

    def generate_important_rule(self, base_symbol: str, 
                                symbols: str, asymbols: str) -> str:
        imp_rule = base_symbol + '->' + ''.join(choices(symbols + asymbols, 
                                                        k=len(symbols)))
        return imp_rule
    
    def generate_random_rule(self, diff_symbols: set[str]) -> str:
        rule_length: int = randint(self.__rule_length_range.first, 
                                   self.__rule_length_range.second) - 2
        base_rule_len = rule_length // 10 + 1
        end_rule_len = rule_length - base_rule_len
        base_rule: str = ''.join(choices(diff_symbols, k=base_rule_len)) 
        result = ''.join(choices(list(self.__result_lsystem.angles.keys()) + \
                         list(self.__result_lsystem.alphabet.keys()), 
                         k=rule_length))
        rule = base_rule + '->' + result
        return rule

    def generate_rules(self) -> list[str]:
        rule_length: int = randint(self.__rules_number_range.first,
                                   self.__rules_number_range.second)
        rules = []
        diff_symbols = set(self.__result_lsystem.axiom)
        pair_with_max_branch = list(self.__result_lsystem.alphabet.items())[-1]
        rules.append(self.generate_important_rule(self.__result_lsystem.axiom[0],
                     ''.join(self.__result_lsystem.alphabet.keys()), 
                     ''.join(self.__result_lsystem.angles.keys())))
        rules.append(self.generate_increasing_rule(pair_with_max_branch[0]))
        for i in range(rule_length):
            rules.append(self.generate_random_rule(''.join(self.__result_lsystem.alphabet.keys())))
        self.__result_lsystem.rules = rules
        return rules 


    
if __name__ == '__main__':
    god = BaseRandomLSystemGenerator()
    god.set_angle_value_range(FPair(0.0, 90.0))
    god.set_axiom_len_range(IPair(2, 3))
    print(god.generate_alphabet())
    print(god.generate_angles())
    print(god.generate_axiom())
    print(god.generate_rules())
    ls = god.get_lsystem()
    ls.generate(6)
    print(ls.state)
    pen = Drawer()
    pen.draw_tree([1000, 650], ls)