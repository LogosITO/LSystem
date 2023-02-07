import re
from random import random, seed
from typing import Optional

# LSystem step rule pattern

base = r'(?P<Base>[A-Za-z + -]+)'
pos = r'(?P<Possibility>(\d(\.|\,)(\d)+))'
res = r'(?P<Result>[A-Za-z \W]+)'
rrn = r'(?P<RequiredRightNeighbour>[A-Za-z + -]+)'
rln = r'(?P<ReguiredLeftNeighbour>[A-Za-z + -]+)'
pattern = fr'^({rln}<)?{base}(\({pos}\))?(>{rrn})?->{res}$'


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
    rneighbour: str = dict_rule['RequiredRightNeighbour']
    lneighbour: str = dict_rule['ReguiredLeftNeighbour']
    right, left = False, False
    if rneighbour is None or state[idx+1:idx+len(rneighbour)+1] == rneighbour:
        right = True
    if lneighbour is None or state[idx-len(lneighbour):idx] == lneighbour:
        left = True
    return bool(right * left)


def check_posibility(rule: str) -> bool:
    seed(0)
    pos: Optional[str] = parse_rule(rule)['Possibility']
    if pos is None or random() <= float(pos):
        return True
    return False


def check_all_requirements(rule: str, state: str, idx: int) -> bool:
    pos_req: bool = check_pos_requirements(rule, state, idx)
    posibility: bool = check_posibility(rule)
    return bool(pos_req * posibility)


if __name__ == '__main__':
    test_rule1 = 'F->F+F'
    test_rule2 = 'A<F>B->FF'
    test1, test2 = 'F', 'A'
    test_state1, test_state2 = 'AFB', 'FFF'
    print(parse_rule(test_rule1))
    print(parse_rule(test_rule2))
    print(give_rule_with_base(test1, [test_rule1, test_rule2]))
    print(check_pos_requirements(test_rule2, test_state1, 1))
    print(check_pos_requirements(test_rule2, test_state2, 1))
