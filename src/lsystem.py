import rule
from typing import NoReturn
from dataclasses import dataclass, field


@dataclass(frozen=False)
class LSystem:
    axiom: str
    alphabet: dict[str, float]
    angles: dict[str, float]
    rules: list[str]
    state: str = field(init=False)

    def __post_init__(self):
        self.state = self.axiom

    def step(self) -> NoReturn:
        next_state = ''
        for idx, el in enumerate(self.state):
            now = rule.give_rule_with_base(el, self.rules)
            if now is None:
                continue
            if rule.check_all_requirements(now, self.state, idx) is True:
                next_state += rule.parse_rule(now)['Result']
        self.state = next_state