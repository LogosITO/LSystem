import re

# LSystem step rule pattern

base = r'(?P<Base>[A-Za-z]+)'
pos = r'(?P<Possibility>(\d(\.|\,)\d))'
res = r'(?P<Result>[A-Za-z]+)'
rrn = r'(?P<RequiredRightNeighbour>[A-Za-z]+)'
rln = r'(?P<ReguiredLeftNeighbour>[A-Za-z]+)'
pattern = fr'^({rln}.)?{base}(\({pos}\))?(.{rrn})?..{res}$'


def parse_rule(data: str) -> dict[str, str]:
    auto = re.compile(pattern)
    m = auto.search(data)
    if m is None:
        raise TypeError
    return m.groupdict()


def search_rule_with_base(base: str, rules: list[str]) -> bool:
    for rule in rules:
        if base == parse_rule(rule)['Base']:
            return True
    return False


def check_pos_requirements(rule: str, idx: int, state: str) -> bool:
    dict_rule: dict[str, str] = parse_rule(rule)
    rneighbour: str = dict_rule['RequiredRightNeighbour']
    lneighbour: str = dict_rule['ReguiredLeftNeighbour']
    right, left = False, False
    if state[idx+1:idx+len(rneighbour)+1] == rneighbour or rneighbour is None:
        right = True
    if state[idx-len(lneighbour):idx] == lneighbour or lneighbour is None:
        left = True
    return bool(right * left)


if __name__ == '__main__':
    test_rule1 = 'F->FF'
    test_rule2 = 'A<F>B->FF'
    test1, test2 = 'F', 'A'
    test_state1, test_state2 = 'AFB', 'FFF'
    print(parse_rule(test_rule1))
    print(parse_rule(test_rule2))
    print(search_rule_with_base(test1, [test_rule1, test_rule2]))
    print(check_pos_requirements(test_rule2, 1, test_state1))
    print(check_pos_requirements(test_rule2, 1, test_state2))
