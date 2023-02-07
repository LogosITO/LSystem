import rule
from dataclasses import dataclass, field


@dataclass(frozen=False)
class LSystem:
    axiom: str
    thickness: float
    alphabet: dict[str, float]
    angles: dict[str, float]
    rules: list[str]
    length_reduction: float = field(init=True, default=0.95)
    state: str = field(init=False, default='')

    def __post_init__(self):
        if len(self.alphabet) < 1:
            raise "Alphabet does not exist!"
        self.state = self.axiom

    def add_rule(self, new_rule: str) -> bool:
        if new_rule in self.rules:
            return True
        try:
            rule.parse_rule(new_rule)
        except TypeError:
            return False
        self.rules.append(new_rule)
        return True

    def step(self):
        next_state = ''
        for idx, el in enumerate(self.state):
            now = rule.give_rule_with_base(el, self.rules)
            if now is None:
                continue
            if rule.check_all_requirements(now, self.state, idx) is True:
                next_state += rule.parse_rule(now)['Result']
        if next_state != '':
            self.state = next_state

    def generate(self, depth: int):
        if depth < 1:
            raise ValueError
        for i in range(depth):
            self.step()
