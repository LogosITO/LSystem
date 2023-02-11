import re
from random import random, seed
from typing import Optional


base = r'(?P<Base>[A-Za-z + - ( )]+)'
pos = r'(?P<Possibility>(\d(\.|\,)(\d)+))'
res = r'(?P<Result>[A-Za-z\W]+)'
rrn = r'(?P<RequiredRightNeighbour>(!?[A-Za-z + -]+))'
rln = r'(?P<ReguiredLeftNeighbour>(!?[A-Za-z + -]+))'

pattern = fr'^({rln}<)?{base}(\[{pos}\])?(>{rrn})?->{res}?$'


def parse_rule(data: str) -> dict[str, str]:
    auto = re.compile(pattern)
    m = auto.search(data)
    if m is None:
        raise TypeError
    return m.groupdict()


def give_rule_with_base(base: str, rules: list[str]) -> Optional[str]:
    for rule in rules:
        if base == parse_rule(rule)['Base']:
            return rule
    return None


def check_pos_requirements(rule: str, state: str, idx: int) -> bool:
    if state[idx] != parse_rule(rule)['Base']:
        return False
    dict_rule: dict[str, str] = parse_rule(rule)
    req_rnb: str = dict_rule['RequiredRightNeighbour']
    req_lnb: str = dict_rule['ReguiredLeftNeighbour']
    rneighbour = state[idx+1:idx+len(req_rnb)+1]
    lneighbour = state[idx-len(req_lnb):idx]
    right, left = False, False
    rneg, lneg = '!' in req_rnb, '!' in req_lnb
    if rneg and rneighbour[1:] != req_rnb or \
       not rneg and (rneighbour == req_rnb or req_rnb is None):
        right = True
    if lneg and lneighbour[1:] != req_lnb or \
       not lneg and (lneighbour == req_lnb or req_lnb is None):
        left = True
    return bool(right * left)


def check_posibility(rule: str) -> bool:
    seed(1)
    pos: Optional[str] = parse_rule(rule)['Possibility']
    if pos is None or random() <= float(pos):
        return True
    return False


def check_all_requirements(rule: str, state: str, idx: int) -> bool:
    pos_req: bool = check_pos_requirements(rule, state, idx)
    posibility: bool = check_posibility(rule)
    return bool(pos_req * posibility)
