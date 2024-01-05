# FIRST集合计算模块
'''
API:
constructor(grammar_file: str) -> dict: 
    输入: 需构造FIRST集的文法所在的文件
    输出: 构造出的FIRST集合的字典: key为文法符号, value为FIRST集合元素构成的列表

get_string_FIRST(string: list, FIRST: dict) -> list:
    输入: 要求的文法符号串形成的列表, 求FIRST集时已知的各个文法符号的FIRST集
    输出: 求得的FIRST集元素构成的列表
'''

import json
from typing import Tuple
from extended_grammar_constructor import constructor as EGC

# 将给定产生式的左部和右部分开
def get_symbol(production: str) -> Tuple[str, list]:
    left_part, right_part = production.split('->')
    left_part = left_part.strip()
    right_symbols = right_part.strip().split(' ')
    return left_part, right_symbols

# 根据给定的FIRST集计算当前string的FIRST集
def get_string_FIRST(string: list, FIRST: dict) -> list:
    res = []
    empty_stringable = True
    for symbol in string:
        if 'ε' not in FIRST.get(symbol):
            res.extend(FIRST.get(symbol))
            empty_stringable = False
            break
        else:
            # 加入除 ε 外所有元素
            res.extend(x for x in FIRST.get(symbol) if x != 'ε')
    # 所有文法符号均可为空串, 则FIRST中包含ε
    if empty_stringable:
        res.append('ε')
    # 去重
    return list(set(res))

# 计算给定文法各个符号的FIRST 
def constructor(grammar: dict) -> dict:
    # 文法符号的FIRST集的字典, 映射关系为文法符号->FIRST集合
    FIRST = {}
    
    # 对终结符 a 有 FIRST(a) = {a}
    terminal = grammar.get('terminal', None)
    for symbol in terminal:
        FIRST[symbol] = [symbol]

    # 构造非终结符的FIRST集
    non_terminal = grammar.get('non_terminal', None)
    for symbol in non_terminal:
        FIRST[symbol] = []
    production = grammar.get('production', None)
    while True:
        modified = False
        for p in production:
            left, right = get_symbol(p)
            # print(left, right)
            if right == ['ε']: # 产生式形如 A -> ε
                if 'ε' not in FIRST.get(left):
                    FIRST.get(left).append('ε')
                    modified = True
            else:
                added_symbols = get_string_FIRST(right, FIRST)
                for symbol in added_symbols:
                    if symbol not in FIRST.get(left):
                        FIRST.get(left).append(symbol)
                        modified = True
        if modified == False:
            break
    return FIRST

if __name__ == "__main__":
    grammar = EGC('grammar.json')
    FIRST = constructor(grammar)
    # 把FIRST集写入文件FIRST.json
    with open("FIRST.json", 'w') as json_file:
        json.dump(FIRST, json_file, indent=4)