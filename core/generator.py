from string import ascii_uppercase
from random import randint, choices, shuffle, uniform
from typing import Union, NamedTuple


def URE_handler(range: tuple[Union[int, float],
                Union[int, float]], error_message: str):
    if range[0] < 0 or range[1] or range[1] - range[0] < 0:
        raise ValueError(error_message)


FPair = NamedTuple('FPair', [('first', float), ('second', float)])
IPair = NamedTuple('IPair', [('first', int), ('second', int)])


class RandomLSystemGenerator:
    __axiom_len_range: IPair = IPair(1, 3)
    __alphabet_len_range: IPair = IPair(2, 5)
    __rule_length_range: IPair = IPair(4, 20)
    __branch_length_range: FPair = FPair(2.0, 10.0)
    __deflection_range: FPair = FPair(-90.0, 90.0)

    def set_axiom_len_range(self, new_alr: IPair):
        URE_handler(new_alr, 'Axiom length range is not available!')
        self.__axiom_len_range = new_alr

    def set_alphabet_len_range(self, new_alr: IPair):
        URE_handler(new_alr, 'Alphabet length range is not available!')
        self.__alphabet_len_range = new_alr

    def set_rule_length_range(self, new_rlr: IPair):
        URE_handler(new_rlr, 'Rule length range is not available!')
        self.__rule_length_range = new_rlr

    def set_branch_length_range(self, new_blr: FPair):
        URE_handler(new_blr, 'Branch length range is not available!')
        self.__branch_length_range = new_blr

    def set_deflection_range(self, new_dr: FPair):
        self.__deflection_range = new_dr

    def generate_alphabet(self) -> dict[str, float]:
        symbols_num: int = randint(self.__alphabet_len_range.first,
                                   self.__alphabet_len_range.second)
        symbols: list[str] = choices(ascii_uppercase, k=symbols_num)
        lborder: float = self.__branch_length_range.first
        rborder: float = self.__branch_length_range.second
        values = [uniform(lborder, rborder) for i in range(len(symbols))]
        alphabet = {key: value for key, value in zip(symbols, values)}
        return alphabet

    def generate_axiom(self, symbols: str) -> str:
        axiom_length: int = randint(self.__axiom_len_range.first,
                                    self.__axiom_len_range.second)
        different_symbols_number: int = randint(self.__axiom_len_range.first,
                                                axiom_length)
        line: str = ''.join(choices(symbols, k=different_symbols_number))
        line.rjust(axiom_length, line[-1])
        shuffle(list(line))
        return line

    # TODO: Finish this class and go to the more interesting objects)\
