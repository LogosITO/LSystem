import re
from random import random, seed
from typing import Optional
from globals import LAS


base = fr'(?P<Base>[A-Za-z + - ( ) {LAS}]+)'
par = r'\((?P<Parameters>[^,\)]+(?:, [^,\)]*)*)\)'
pos = r'(?P<Possibility>(\d(\.|\,)(\d)+))'
res = fr'(?P<Result>[A-Za-z {LAS} \W]+)'
rpar = r'\((?P<ResultParameters>[^,\)]+(?:, [^,\)]*)*)\)'
rrn = r'(?P<RequiredRightNeighbour>(!?[A-Za-z + -]+))'
rln = r'(?P<ReguiredLeftNeighbour>(!?[A-Za-z + -]+))'


pattern = fr'^({rln}<)?{base}({par})?(\[{pos}\])?(>{rrn})?->{res}({rpar}?)?$'


def parse_rule(data: str) -> dict[str, str]:
    auto = re.compile(pattern)
    m = auto.search(data)
    if m is None:
        raise TypeError('The rule does not match the given pattern!')
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
    seed(1)
    pos: Optional[str] = parse_rule(rule)['Possibility']
    if pos is None or random() <= float(pos):
        return True
    return False


def check_all_requirements(rule: str, state: str, idx: int) -> bool:
    pos_req: bool = check_pos_requirements(rule, state, idx)
    posibility: bool = check_posibility(rule)
    return bool(pos_req * posibility)
