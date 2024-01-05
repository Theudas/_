# LR(1) 移入-归约分析

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from collections import deque

from extended_grammar_constructor import constructor as EGC
from FIRST_calculator import constructor as FC
from LR1_constructor import constructor as LR1C

grammar = EGC('grammar.json')     # 给定文法的拓广文法
non_terminal = grammar.get('non_terminal')
terminal = grammar.get('terminal')
production = grammar.get('production')
FIRST = FC(grammar)               # 构造给定文法所有文法符号的FIRST集
FIRST['$'] = ['$']                # 加入结束符 $
LR1 = LR1C(grammar, FIRST)        # 构造给定文法的LR(1)分析表
State = [0]                       # 状态栈
Symble = ['-']                    # 符号栈
user_input = input()              # 用户输入
user_input = user_input.split()
input_queue = deque()
for word in user_input:
    input_queue.append(word)
input_queue.append('$')
output = None

class LR1Parsing(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        global grammar, non_terminal, terminal, production, FIRST, \
        LR1, State, Symble, input_queue, output
        self.setGeometry(100, 100, 1000, 800)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(0, 0, 1000, 800)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 600)
        self.tableWidget.setHorizontalHeaderLabels(['State栈', 'Symble栈', '输入', '分析动作'])
        print('start parsing')
        self.startParsing()
    def addTableRow(self, State, Symble, input_queue, output):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        state = ' '.join(map(str, State))
        symble = ' '.join(Symble)
        cur_input = ' '.join(input_queue)
        cur_output = ' '.join(output)
        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(state))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(symble))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(cur_input))
        self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(cur_output))
    def startParsing(self):
        while True:
            if len(State) == len(Symble):   
                cur_state = State[-1]
                state_transform = LR1.get(cur_state, None)
                input_stack_top = input_queue[0]
                ACTION = state_transform.get(input_stack_top, None)
                if ACTION == None:
                    output = 'Error'
                    self.addTableRow(State, Symble, input_queue, output)
                    break
                elif ACTION == 'ACC':
                    output = 'ACC'
                    self.addTableRow(State, Symble, input_queue, output)
                    break
                elif ACTION[0] == 'S':
                    output = 'Shift ' + str(ACTION[1])
                    self.addTableRow(State, Symble, input_queue, output)
                    input_queue.popleft()
                    State.append(ACTION[1])
                    Symble.append(input_stack_top)
                else:
                    output = 'Reduce by ' + production[ACTION[1]]
                    self.addTableRow(State, Symble, input_queue, output)
                    left_part, right_part = production[ACTION[1]].split('->')
                    left_part = left_part.strip()
                    right_symbols = right_part.strip().split(' ')
                    for symbol in reversed(right_symbols):
                        if symbol == Symble[-1]:
                            State.pop()
                            Symble.pop()
                        else:
                            output = 'Error'
                            self.addTableRow(State, Symble, input_queue, output)
                            break
                    Symble.append(left_part)
            else:
                cur_state = State[-1]
                state_transform = LR1.get(cur_state, None)
                GOTO = state_transform.get(Symble[-1], None)
                if GOTO == None:
                    output = 'Error'
                    self.addTableRow(State, Symble, input_queue, output)
                    break
                else:
                    State.append(GOTO)



if __name__ == '__main__':
    if LR1 == None:
        print('该文法不是LR(1)文法, 无法进行LR(1)分析')
    else:
        app = QApplication(sys.argv)
        lr1_parsing = LR1Parsing()
        lr1_parsing.show()
        sys.exit(app.exec_())