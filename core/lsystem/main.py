import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from typing import Optional
from dataclasses import dataclass, field
from rule import (parse_rule,
                  check_all_requirements,
                  get_rules_with_base)
from string import ascii_letters


@dataclass(init=True, frozen=False)
class BaseLSystem:
    axiom: str = field(init=True, default='')
    thickness: float = field(init=True, default=4)
    alphabet: dict[str, float] = field(init=True, default_factory=dict)
    angles: dict[str, float] = field(init=True, default_factory=dict)
    rules: list[str] = field(init=True, default_factory=list)
    parametrized_rules: list[str] = field(init=True, default_factory=list)
    length_reduction: float = field(init=True, default=0.95)
    state: str = field(init=False, default='')

    def __post_init__(self) -> None:
        self.state = self.axiom
        # self.rules.sort()

    def add_rule(self, new_rule: str) -> bool:
        if new_rule in self.rules:
            return True
        try:
            parse_rule(new_rule)
        except TypeError:
            return False
        self.rules.append(new_rule)
        return True

    def change_rules(self, new_rules: list[str]) -> bool:
        if self.rules == new_rules:
            return True
        else:
            self.rules = new_rules
            return True

    def step(self) -> None:
        next_state = ''
        for idx, el in enumerate(self.state):
            rules_now = get_rules_with_base(el, self.rules)
            if len(rules_now) == 0:
                next_state += el
                continue
            for now in rules_now:
                if check_all_requirements(now, self.state, idx) is True:
                    next_state += parse_rule(now)['Result']
                    continue

        if next_state != '':
            self.state = next_state

    def generate(self, depth: int) -> None:
        if depth < 1:
            raise ValueError
        for i in range(depth):
            self.step()


@dataclass(init=True, frozen=False)
class WMLLSystem(BaseLSystem):
    leaf_symbol: str = field(init=True, default='*')

    def __post_init__(self):
        super().__post_init__()

    def add_rule(self, new_rule: str) -> bool:
        return super().add_rule(new_rule)


@dataclass(init=True, frozen=False)
class StateHandler:
    state: Optional[str] = field(init=True, default=None)
    pre_result: list[str] = field(init=False, default_factory=list)
    result: list[str] = field(init=False, default_factory=list)

    def __post_init__(self):
        if self.state is None:
            raise ValueError("You hadn't pushed state in your StateHandler!")

    def __break(self) -> None:
        sequences = []
        msq = self.state[0]
        for idx in range(1, len(self.state)):
            el = self.state[idx]
            if el in msq:
                msq += el
            else:
                sequences.append(msq)
                msq = el
        else:
            sequences.append(msq)
        self.pre_result = sequences
        self.result = self.pre_result

    def __beautifier(self) -> None:
        prs = []
        for idx, seq in enumerate(self.pre_result):
            el = seq[0]
            if el == '[':
                while el != ']':
                    seqf = self.result[idx]
                    el = seqf[0]
                    idx += 1
            elif seq[0] in ascii_letters:
                prs.append(idx)
        for i in range(len(self.result)):
            if i in prs:
                new_seq = ''
                for el in self.result[i]:
                    new_seq = new_seq + el + '|'
                else:
                    self.result[i] = new_seq

    def __linker(self) -> None:
        return ''.join(self.result)

    def out(self):
        self.__break()
        self.__beautifier()
        res = self.__linker()
        return res
