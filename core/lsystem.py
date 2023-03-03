import rule
from dataclasses import dataclass, field


@dataclass(init=True, frozen=False)
class BaseLSystem:
    axiom: str = field(init=True, default='')
    thickness: float = field(init=True, default=1)
    alphabet: dict[str, float] = field(init=True, default_factory=dict)
    angles: dict[str, float] = field(init=True, default_factory=dict)
    rules: list[str] = field(init=True, default_factory=list)
    parametrized_rules: list[str] = field(init=True, default_factory=list)
    length_reduction: float = field(init=True, default=0.95)
    state: str = field(init=False, default='')

    def __post_init__(self):
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
                next_state += el
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


@dataclass(init=True, frozen=False)
class WMLLSystem(BaseLSystem):
    leaf_symbol: str = '*'

    def __post_init__(self):
        super().__post_init__()

    def add_rule(self, new_rule: str) -> bool:
        return super().add_rule(new_rule)
