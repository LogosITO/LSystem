from typing import Union, NamedTuple
from queue import Queue


most_used_angle_symbols = ['+', '-', '^', '(', ')', '&', '?']


FPair = NamedTuple('FPair', [('first', float), ('second', float)])
IPair = NamedTuple('IPair', [('first', int), ('second', int)])


def URE_handler(range: Union[FPair, IPair], error_message: str = ''):
    if range.first < 0 or range.second < 0 or range.second - range.first < 0:
        raise ValueError(error_message)
    
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