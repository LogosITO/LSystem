from rule import *
from random import *
from dataclasses import dataclass, field
from string import ascii_uppercase
from utils import IPair, generator_angle_symbols, is_balanced
from main import WMLLSystem
from abc import ABC, abstractmethod
from xeger import xeger


@dataclass(init=True, frozen=False)
class RuleGenerator(ABC):
    god: RulePatternCreater = field(init=False, default_factory=RulePatternCreater)

    @staticmethod
    def _generate_alpha_sym(base_alphabet, sym_borders: IPair):
        fa, sa = sym_borders.first, sym_borders.second
        symbols = sample(base_alphabet, randint(fa, sa))
        return symbols

    @abstractmethod
    def generate_alphabet_symbols(self):
        pass

    @abstractmethod
    def generate_angles_symbols(self):
        pass

    @abstractmethod
    def generate_rule(self):
        pass


@dataclass(init=True, frozen=False)
class DefaultRuleGenerator(RuleGenerator):
    alpha_border: IPair = field(init=True, default=IPair(2, 4))
    angles_border: IPair = field(init=True, default=IPair(2, 4))
    groups_to_delete: IPair = field(init=True, default=IPair(0, 2))
    rule_sym_number: IPair = field(init=True, default=IPair(1, 5))
    alpha_symbols: list[str] = field(init=False, default_factory=list)
    angles_symbols: list[str] = field(init=False, default_factory=list)

    def generate_alphabet_symbols(self) -> list[str]:
        self.alpha_symbols = self._generate_alpha_sym(ascii_uppercase, self.alpha_border)
        return self.alpha_symbols

    def generate_angles_symbols(self) -> list[str]:
        self.angles_symbols = self._generate_alpha_sym(generator_angle_symbols, self.angles_border)
        return self.angles_symbols

    def __delete_random_groups(self) -> str:
        # alpha = self.generate_alphabet_symbols()
        to_delete = [group for group in self.god.get_group_names() if group not in ['BASE', 'RES']]
        fg, sg = self.groups_to_delete.first, self.groups_to_delete.second
        del_groups = sample(to_delete, randint(fg, sg))
        self.god.delete_groups(del_groups)
        return self.god.get_pattern()

    def __change_groups(self) -> str:
        alpha, angles = ''.join(self.generate_alphabet_symbols()), \
                        ''.join(self.generate_angles_symbols())
        try:
            self.god.add_group_info('BASE', alpha, IPair(1, 1))
        except ValueError:
            raise ValueError('Some problem with RulePatternCreator.pattern!')
        groups = [group for group in self.god.get_group_names() if group != 'BASE' and
                  self.god.get_group(group) is not None]
        for group in groups:
            self.god.add_group_info(group, alpha + angles, self.rule_sym_number)
        return self.god.get_pattern()

    def get_final_pattern(self):
        return self.god.get_pattern()

    def generate_rule(self) -> str:
        self.__delete_random_groups()
        pat = self.__change_groups()
        self.god.clear_changes()
        return xeger(pat)


@dataclass(init=True, frozen=False)
class ManualRuleGenerator(RuleGenerator):
    alphabet: str = field(init=True, default='FXYG')
    positive_angles_alpha: str = field(init=True, default='+#')
    negative_angles_alpha: str = field(init=True, default='@=')
    leaf_symbol: str = field(init=True, default='*')
    groups_to_delete: list[str] | None = field(init=True, default=None)
    deps_dict: dict[str, IPair | None] = field(init=True, default_factory=dict)

    def __post_init__(self):
        self.__deps_dict_beautifier()
        self.__deps_dict_editor()
        self.deps_dict['BASE'] = IPair(1, 1)

    def __deps_dict_editor(self) -> None:
        for group in self.god.get_group_names():
            if group not in self.deps_dict.keys():
                rf = randint(1, 2)
                rs = rf + randint(0, 3)
                self.deps_dict[group] = IPair(rf, rs)

    def __deps_dict_beautifier(self) -> None:
        for key in self.deps_dict.keys():
            if key not in self.god.get_group_names():
                del self.deps_dict[key]

    def expand_deps_dict(self, new_deps: dict[str, IPair]) -> None:
        self.deps_dict.update(new_deps)

    def generate_alphabet_symbols(self) -> list[str]:
        return self.alphabet

    def generate_angles_symbols(self) -> list[str]:
        return self.positive_angles_alpha + self.negative_angles_alpha

    def __generate_result(self, result_len: int = 4) -> str:
        self.god.add_group_info('res', self.alphabet, IPair(1, result_len*2))
        rnd_len = randint(1, 1) * 2
        len_in_brackets = result_len - rnd_len
        res = ''.join(choices(self.alphabet, k=1)) + '[' + choice(self.positive_angles_alpha) + \
            ''.join(sample(self.alphabet, len_in_brackets)) + self.leaf_symbol + \
            choice(self.negative_angles_alpha) + ']' + ''.join(choices(self.alphabet, k=1))
        return res

    def generate_rule(self):
        if self.groups_to_delete is not None:
            self.god.delete_groups(self.groups_to_delete)
        for key, value in self.deps_dict.items():
            n_key = key.upper()
            if not self.god.check_futility(n_key) and n_key != 'RES' and n_key != 'POS':
                self.god.add_group_info(n_key, self.alphabet, value)
            else:
                continue
        res = self.god.get_pattern(), None
        if is_balanced(self.god.get_pattern()):
            res = self.god.get_pattern(), xeger(self.god.get_pattern())
        else:
            raise UnboundLocalError
        res = res[1].split('->')[0] + '->' + self.__generate_result()
        self.god.clear_changes()
        return res


@dataclass(init=True, frozen=False)
class LSystemGenerator:
    angles_values_borders: IPair = field(init=True, default=IPair(-120, 120))
    alpha_values_borders: IPair = field(init=True, default=IPair(0, 10))
    rules_number_borders: IPair = field(init=True, default=IPair(1, 3))
    axiom_len_borders: IPair = field(init=True, default=IPair(2, 3))
    RG: RuleGenerator = field(init=False, default_factory=DefaultRuleGenerator)
    __result: WMLLSystem = field(init=False, default_factory=WMLLSystem)

    def __generate_alphabet(self) -> dict[str, int]:
        symbols = self.RG.generate_alphabet_symbols()
        fv, fs = self.alpha_values_borders.first, self.alpha_values_borders.second
        values = [randint(fv, fs) for _ in range(len(symbols))]
        res = dict(zip(symbols, values))
        self.__result.alphabet = res
        return res

    def __generate_angles(self) -> dict[str, int]:
        symbols = self.RG.generate_angles_symbols()
        fv, fs = self.angles_values_borders.first, self.angles_values_borders.second
        values = [randint(fv, fs) for _ in range(len(symbols))]
        res = dict(zip(symbols, values))
        self.__result.angles = res
        return res

    def __generate_all_rules(self) -> list[str]:
        fr, sr = self.rules_number_borders.first, self.rules_number_borders.second
        number = randint(fr, sr)
        res = []
        for _ in range(number):
            gg = self.RG.generate_rule()
            if base not in self.__result.axiom:
                change_rule(gg, 'BASE', choice(self.__result.axiom))
            res.append(gg)
        sym = choice(self.__result.axiom)
        res.append(f'{sym}->{sym}{sym}')
        self.__result.change_rules(res)
        return res

    def __generate_axiom(self) -> str:
        f, s = self.axiom_len_borders.first, self.axiom_len_borders.second
        ax_len = randint(f, s)
        res = list(self.__result.alphabet.keys())
        if len(res) <= ax_len:
            self.__result.axiom = ''.join(res)[randint(0, len(res) - 1)]
        else:
            self.__result.axiom = ''.join(sample(res, k=ax_len))
        self.__result.state = self.__result.axiom
        return res

    def set_generator(self, new_RG: RuleGenerator) -> bool:
        try:
            self.RG = new_RG
        except:
            return False
        return True

    def out(self):
        self.__generate_alphabet()
        self.__generate_angles()
        self.__generate_axiom()
        self.__generate_all_rules()
        return self.__result


if __name__ == '__main__':
    MRG = ManualRuleGenerator()
    MRG.expand_deps_dict({'RRN': IPair(1, 1), 'RLN': IPair(1, 1)})
    print(MRG.deps_dict)
    print(MRG.generate_rule())
    LG = LSystemGenerator()
    LG.set_generator(MRG)
    print(LG.out().rules)
