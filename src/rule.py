import re

# LSystem step rule pattern

base = r'(?P<Base>[A-Za-z]+)'
pos = r'(?P<Possibility>(\d(\.|\,)\d))'
res = r'(?P<Result>[A-Za-z]+)'
rrn = r'(?P<RequiredRightNeighbour>[A-Za-z]+)'
rln = r'(?P<ReguiredRightNeighbour>[A-Za-z]+)'
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


if __name__ == '__main__':
    test_rule = 'F->FF'
    print(parse_rule(test_rule))
