import json

items = []

with open("closure.json", 'r') as json_file:
    items = json.load(json_file)

index = 0

for item in items:
    print(f'I{index}:')
    index = index + 1
    a = []
    b = []
    for it in item:
        production = it[0]
        production = production + ' '
        dot = it[1] + 1
        lookahead = it[2]
        arrow_index = production.find('->')
        spaces_after_arrow = [pos for pos, char in enumerate\
                              (production[arrow_index + 2:]) if char.isspace()]
        if len(spaces_after_arrow) >= dot:
            target_space_index = arrow_index + 2 + spaces_after_arrow[dot - 1]
        modified_str = production[:target_space_index] + '·' \
        + production[target_space_index:]
        if modified_str not in a:
            a.append(modified_str)
            b.append([lookahead])
        else:
            num = a.index(modified_str)
            b[num].append(lookahead)
    cnt = 0
    for aa in a:
        print(f'{aa},  {b[cnt]}')
        cnt = cnt + 1