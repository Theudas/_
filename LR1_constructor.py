# 构造LR1分析表

import json
from typing import Tuple
from collections import Counter
from extended_grammar_constructor import constructor as extended_grammar_constructor
from FIRST_calculator import constructor as FIRST_constructor
from FIRST_calculator import get_string_FIRST


# 将给定产生式(字符串表示)拆成左部和右部
def get_symbol(production: str) -> Tuple[str, list]:
    left_part, right_part = production.split('->')
    left_part = left_part.strip()
    right_symbols = right_part.strip().split(' ')
    return left_part, right_symbols


# 将给定的产生式集合拆成左部集合(left = ['X', 'Y'])和右部集合(right = [[], []])
def split_production(production: list) -> Tuple[list, list]:
    left = []
    right = []
    for p in production:
        left_part, right_part = get_symbol(p)
        left.append(left_part)
        right.append(right_part)
    return left, right

# 计算项目集闭包
def closure(item: list, grammar: dict, FIRST: dict) -> list:
    '''
    item = [[production, dot, lookahead]]
    其中 dot 表示点在产生式右部第几个文法符号的前面(从0开始编号), 特别的, 当 dot = len(右部) 时表示规约项目
    '''
    grammar_production = grammar.get('production')
    grammar_left = grammar.get('left')
    grammar_right = grammar.get('right')
    grammar_non_terminal = grammar.get('non_terminal')
    count = 0
    while count < len(item):
        i = item[count]
        cur_production_index = grammar_production.index(i[0]) # 当前要处理的产生式的索引
        if i[1] == len(grammar_right[cur_production_index]): # 是一个归约项目
            pass
        elif grammar_right[cur_production_index][i[1]] in grammar_non_terminal: # 是一个待约项目
            # 对于形如 A -> α · B, 找到所有 B 为左部的产生式的 index
            indices = [] 
            for index, value in enumerate(grammar_left):
                if value == grammar_right[cur_production_index][i[1]]:
                    indices.append(index)
            # 计算向前看符号串
            r = grammar_right[cur_production_index][(i[1] + 1):]
            r.append(i[2])
            lookahead = get_string_FIRST(r, FIRST)
            new_item = []
            for index in indices:
                for symbol in lookahead:
                    new_item.append([grammar_production[index], 0, symbol])
            for it in new_item:
                if it not in item:
                    item.append(it)
        else: # 是一个移进项目
            pass
        count += 1
    return item

# 给定项目 item 找出项目集中所有能在相同输入进行转移的项目编号
def get_same_items_index(item: list, cur_item: list, production: list, right: list) -> list:
    indices = []
    production_index = production.index(item[0])
    symbol = right[production_index][item[1]]  # 下一个输入符号
    for index, item in enumerate(cur_item):
        if len(right[production.index(item[0])]) <= item[1]:
            continue
        elif right[production.index(item[0])][item[1]] == symbol:
            indices.append(index)
    return indices

# 计算new_item是否在项目集族items中位置, 若小于len(items)则已存在, 返回在items中索引
def get_item_index(new_item: list, items: list) -> int:
    new_item_hashable = frozenset(tuple(it) for it in new_item)
    for index, existing_item in enumerate(items):
        existing_item_hashable = frozenset(tuple(it) for it in existing_item)
        if existing_item_hashable == new_item_hashable:
            return index
    return len(items)

# 构造该文法的LR(1)项目集规范族
def constructor(grammar: dict, FIRST: dict) -> dict:
    # 将产生式拆成左部和右部, 方便后续操作
    production = grammar.get('production', None)
    left, right = split_production(production)
    grammar['left'] = left
    grammar['right'] = right
    terminal = grammar.get('terminal', None)
    LR1 = {} # LR(1)分析表
    '''
    LR1 = {state1 : {'A' : state2, 'a' : ['R'/'S', index]}}
    表示在state1遇到非终结符转移到state2,
    遇到终结符a根据第index条产生式规约或
    移入并转移到状态index
    '''
    items = [] # 项目集规范族
    equal_item = {}
    items.append(closure([["E' -> E", 0, '$']], grammar, FIRST))
    state_index = 0
    while state_index < len(items):
        cur_item = items[state_index]
        # 计算状态state_index的goto和action
        LR1[state_index] = {}
        is_checked = [False] * len(cur_item)
        for i, item in enumerate(cur_item):
            if is_checked[i]: # 已经加入新的项目了
                continue
            else:
                production_index = production.index(item[0])
                condition_1 = item[1] == len(right[production_index])
                condition_2 = right[production_index] == ['ε']
                if condition_1 or condition_2: # 是一个归约项目
                    if LR1[state_index].get(item[2], None) == None:
                        if production_index == 0:
                            LR1[state_index][item[2]] = 'ACC'
                        else:
                            LR1[state_index][item[2]] = ['R', production_index]
                    elif LR1[state_index][item[2]] != ['R', production_index]:
                        print('归约存在冲突')
                        return None # 存在冲突, 不是LR(1)文法, 返回None
                elif right[production_index][item[1]] in terminal: # 是一个移进项目
                    # 对于 a , 找到项目集中所有形如A -> α · a β的项目，加入项目集规范族
                    indices = get_same_items_index(item, cur_item, production, right)
                    new_item = []
                    for index in indices:
                        is_checked[index] = True
                        new_item.append([cur_item[index][0], 
                                         cur_item[index][1] + 1, 
                                         cur_item[index][2]])
                    new_item = closure(new_item, grammar, FIRST)
                    new_item_index = get_item_index(new_item, items)
                    symbol = right[production_index][item[1]]
                    if LR1[state_index].get(symbol, None) == None:
                        LR1[state_index][symbol] = ['S', new_item_index]
                    elif LR1[state_index][symbol] != ['S', new_item_index]:
                        print('移进项目存在冲突')
                        return None
                    if new_item_index == len(items):
                        items.append(new_item)
                else: # 是一个待约项目
                    # 对于 B ,找到项目集中所有形如A -> α · B β的项目，加入项目集规范族
                    indices = get_same_items_index(item, cur_item, production, right)
                    new_item = []
                    for index in indices:
                        is_checked[index] = True
                        new_item.append([cur_item[index][0], 
                                         cur_item[index][1] + 1, 
                                         cur_item[index][2]])
                    new_item = closure(new_item, grammar, FIRST)
                    new_item_index = get_item_index(new_item, items)
                    symbol = right[production_index][item[1]]
                    if LR1[state_index].get(symbol, None) == None:
                        LR1[state_index][symbol] = new_item_index
                    elif LR1[state_index][symbol] != new_item_index:
                        print('待约项目存在冲突')
                        return None
                    if new_item_index == len(items):
                        items.append(new_item)
        state_index += 1
    with open("closure.json", 'w') as json_file:
        json.dump(items, json_file, indent=2)
    return LR1



if __name__ == "__main__":
    with open('extended_grammar.json', 'r') as json_file:
        grammar = json.load(json_file)
    FIRST = FIRST_constructor(grammar)
    FIRST['$'] = ['$'] # 加入结束符 $
    
    LR1 = constructor(grammar, FIRST)

    # 把LR(1)分析表写入文件LR1.json
    with open("LR1.json", 'w') as json_file:
        json.dump(LR1, json_file, indent=2)