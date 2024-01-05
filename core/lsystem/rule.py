import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import re
from utils import IPair
from random import random
from typing import Optional, Final
from string import punctuation


base = r'(?P<Base>[A-Za-z + - ( )]+)'
par = r'\((?P<Parameters>[^,\)]+(?:, [^,\)]*)*)\)'
pos = r'(?P<Possibility>(0(\.)(\d)+))'
res = fr'(?P<Result>[A-Za-z {punctuation} \W]+)'
rpar = r'\((?P<ResultParameters>[^,\)]+(?:, [^,\)]*)*)\)'
rrn = r'(?P<RequiredRightNeighbour>(!?[A-Za-z + -]+))'
rln = r'(?P<ReguiredLeftNeighbour>(!?[A-Za-z + -]+))'


base_pattern: Final[str] = \
    fr'^({rln}<)?{base}({par})?(\[{pos}\])?(>{rrn})?->{res}({rpar}?)?$'


class RulePatternCreater:
    __base = [r'^', r'(?P<RLN>)<', r'(?P<BASE>)', r'\[(?P<POS>)(0(\.)(\d)+)\]',
              r'>(?P<RRN>)', r'->(?P<RES>)', r'$']
    __base_names = ['RLN', 'BASE', 'POS', 'RRN', 'RES']

    def __add_suitable_chars(self, group_idx: int, symbols: str) -> None:
        group = self.__base[group_idx]
        idx = group.find(')')
        group = group[:idx] + f'[{symbols}]' + group[idx:]
        self.__base[group_idx] = group

    def __add_range_of_chars(self, group_idx: int, borders: IPair) -> None:
        group = self.__base[group_idx]
        start, end = group.find(']'), group.find(')')
        group = group[:start + 1] + '{' + str(borders.first) + ',' + \
            str(borders.second) + '}' + group[end:]
        self.__base[group_idx] = group

    def add_group_info(self, group_name: str, symbols: str, borders: IPair):
        gn = group_name.upper()
        for key, group in enumerate(self.__base):
            if gn in group:
                self.__add_suitable_chars(key, symbols)
                self.__add_range_of_chars(key, borders)

    def get_group(self, group_name: str) -> str | None:
        for group in self.__base:
            if group_name in group:
                return group
        else:
            return None

    def get_pattern(self):
        res = r'{}'.format(''.join(self.__base))
        return res

    def get_group_names(self):
        return self.__base_names

    def delete_group(self, group_name: str) -> None:
        gn = group_name.upper()
        if gn not in ['BASE', 'RES']:
            for group in self.__base:
                if gn in group:
                    del self.__base[self.__base.index(group)]
                    print(self.get_pattern())
        else:
            raise ValueError('Mistake. There is no such group in the pattern!')

    def delete_groups(self, group_names: list[str]) -> None:
        for group_name in group_names:
            self.delete_group(group_name.upper())

    def check_futility(self, group_name: str) -> bool:
        group = self.get_group(group_name)
        if group is None:
            return False
        if ('{' in group and '}' in group and '[' in group and ']' in group) or len(group) > 15:
            return True
        return False

    def check_existance(self, group_name: str) -> bool:
        if self.get_group(group_name) is not None:
            return True
        return False

    def clear_changes(self):
        self.__base = [r'^', r'(?P<RLN>)<', r'(?P<BASE>)', r'\[(?P<POS>)(0(\.)(\d)+)\]',
                       r'>(?P<RRN>)', r'->(?P<RES>)', r'$']


def parse_rule(data: str, pattern=base_pattern) -> dict[str, str]:
    auto = re.compile(pattern)
    m = auto.search(data)
    if m is None:
        raise TypeError('The rule does not match the given pattern!')
    return m.groupdict()


def change_rule(data: str, group_name: str, new_data: str) -> str:
    res = ''
    for group, g_data in parse_rule(data).items():
        if group == group_name:
            res += new_data
        if g_data is not None:
            res += group
    return res


def get_first_rule_with_base(base: str, rules: list[str]) -> Optional[str]:
    for rule in rules:
        if base == parse_rule(rule)['Base']:
            return rule
    return None


def get_rules_with_base(base: str, rules: list[str]) -> list[str]:
    res = list()
    for rule in rules:
        if base == parse_rule(rule)['Base']:
            res.append(rule)
    return res


def check_pos_requirements(rule: str, state: str, idx: int) -> bool:
    if state[idx] != parse_rule(rule)['Base']:
        return False
    dict_rule: dict[str, str] = parse_rule(rule)
    req_rnb: str = dict_rule['RequiredRightNeighbour']
    req_lnb: str = dict_rule['ReguiredLeftNeighbour']
    right, left = False, False
    rneg, lneg = False, False
    if req_rnb is None:
        right = True
    else:
        rneighbour = state[idx+1:idx+len(req_rnb)+1]
        rneg = '!' in req_rnb
    if req_lnb is None:
        left = True
    else:
        lneighbour = state[idx-len(req_lnb):idx]
        lneg = '!' in req_lnb
    if not right and (rneg and rneighbour[1:] != req_rnb or
       not rneg and (rneighbour == req_rnb or req_rnb is None)):
        right = True
    if not left and (lneg and lneighbour[1:] != req_lnb or
       not lneg and (lneighbour == req_lnb or req_lnb is None)):
        left = True
    return bool(right * left)


def check_posibility(rule: str) -> bool:
    pos: Optional[str] = parse_rule(rule)['Possibility']
    if pos is None or random() <= float(pos):
        return True
    return False


def check_all_requirements(rule: str, state: str, idx: int) -> bool:
    pos_req: bool = check_pos_requirements(rule, state, idx)
    posibility: bool = check_posibility(rule)
    return bool(pos_req * posibility)


if __name__ == '__main__':
    rl = RulePatternCreater()
    rl.add_group_info('base', 'ABC', IPair(1, 3))
    rl.add_group_info('rln', 'FC', IPair(1, 2))
    print(rl.get_pattern())
