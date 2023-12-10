import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import re
from utils import IPair, URE_handler
from random import random
from typing import Optional, Final
from string import punctuation

base = r'(?P<Base>[A-Za-z + - ( )]+)'
par = r'\((?P<Parameters>[^,\)]+(?:, [^,\)]*)*)\)'
pos = r'(?P<Possibility>(\d(\.|\,)(\d)+))'
res = fr'(?P<Result>[A-Za-z {punctuation} \W]+)'
rpar = r'\((?P<ResultParameters>[^,\)]+(?:, [^,\)]*)*)\)'
rrn = r'(?P<RequiredRightNeighbour>(!?[A-Za-z + -]+))'
rln = r'(?P<ReguiredLeftNeighbour>(!?[A-Za-z + -]+))'


pattern: Final[str] = fr'^({rln}<)?{base}({par})?(\[{pos}\])?(>{rrn})?->{res}({rpar}?)?$'


class RulePatternCreater:
    __base = r'^(?P<RLN>)(?P<BASE>)(?P<PAR>)(?P<RRN>)->(?P<RES>)(?P<RPAR>)$'

    def __add_suitable_chars(self, group_idx: int, symbols: str):
        self.__base = self.__base[:group_idx] + f'[{symbols}]' + self.__base[group_idx:]

    def __add_range_of_chars(self, group_idx: int, borders: IPair):
        f_idx = self.__base[group_idx:].find(']') + group_idx + 1
        self.__base = self.__base[:f_idx] + '{'+ str(borders.first) + ',' + \
             str(borders.second) + '}' + self.__base[f_idx:]
    
    def add_group_info(self, group_name: str, symbols: str, borders: IPair):
        URE_handler(borders, 'Using counters range is not available!')
        group_idx = self.__base.find(group_name.upper())
        if group_idx == -1:
            raise ValueError('Group name does not exist!')
        idx = group_idx + len(group_name) + 1
        self.__add_suitable_chars(group_idx=idx, symbols=symbols)
        self.__add_range_of_chars(group_idx=idx, borders=borders)
        
    def get_pattern(self):
        return self.__base
    
    def clear_changes(self):
        self.__base = r'^(?P<RLN>)(?P<BASE>)(?P<PAR>) \
            (?P<RRN>)->(?P<RES>)(?P<RPAR>)$'
    

def parse_rule(data: str) -> dict[str, str]:
    auto = re.compile(pattern)
    m = auto.search(data)
    if m is None:
        raise TypeError('The rule does not match the given pattern!')
    return m.groupdict()

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
