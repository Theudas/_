# 该模块用于输入待分析的文法

import json

# 文法字典
grammar = {}

terminal = ['+', '-', '*', '/', '(', ')', 'num']    # 终结符
non_terminal = ['E', 'T', 'F']                      # 非终结符
start_symbol = 'E'                                  # 起始符
production = []                                     # 产生式

# 加入产生式
production.append('E -> E + T')
production.append('E -> E - T')
production.append('E -> T')
production.append('T -> T * F')
production.append('T -> T / F')
production.append('T -> F')
production.append('F -> ( E )')
production.append('F -> num')

# 将文法写入文法字典
grammar['terminal'] = terminal
grammar['non_terminal'] = non_terminal
grammar['start_symbol'] = start_symbol
grammar['production'] = production

# 把文法字典写入文件grammar.json
with open("grammar.json", 'w') as json_file:
    json.dump(grammar, json_file, indent=4)