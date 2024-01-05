# 该模块用于将输入的文法改写为拓广文法

import json

# 返回改写后拓广文法的字典
def constructor(grammar_file: str) -> dict:
    # 读入输入的文法
    with open(grammar_file, 'r') as json_file:
        grammar = json.load(json_file)

    # 起始符改为 E'
    start_symbol = 'E\''

    # 将新的起始符 E' 加入非终结符集合中
    non_terminal = grammar.get('non_terminal', None)
    non_terminal.insert(0, 'E\'')

    # 加入一条产生式 E' -> E
    production = grammar.get('production', None)
    production.insert(0, 'E\' -> E')

    grammar.update({'start_symbol' : start_symbol, 
                    'non_terminal' : non_terminal, 
                    'production':production})
    return grammar

if __name__ == "__main__":
    grammar = constructor('grammar.json')
    # 把拓广文法字典写入文件extended_grammar.json
    with open("extended_grammar.json", 'w') as json_file:
        json.dump(grammar, json_file, indent=4)