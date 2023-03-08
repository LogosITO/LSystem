from typing import Union, NamedTuple


most_used_angle_symbols = ['+', '-', '^', '(', ')', '&', '?']


FPair = NamedTuple('FPair', [('first', float), ('second', float)])
IPair = NamedTuple('IPair', [('first', int), ('second', int)])


def URE_handler(range: Union[FPair, IPair], error_message: str = ''):
    if range.first < 0 or range.second < 0 or range.second - range.first < 0:
        raise ValueError(error_message)
    

def RFR_handler(value: float, value_name: str = ''):
    if value < 0 or value > 1:
        raise ValueError(f"{value_name} is not located between 0 and 1!")


def is_balanced(text, brackets="()[]{}"):
    opening_brackets, closing_brackets = brackets[::2], brackets[1::2]
    stack = list()
    for character in text:
        if character in opening_brackets:
            stack.append(opening_brackets.index(character))
        elif character in closing_brackets:
            if stack and stack[-1] == closing_brackets.index(character):
                stack.pop()
            else:
                return False
    return (not stack)
