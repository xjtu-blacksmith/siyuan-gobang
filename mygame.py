from tkinter import *
import tkinter.messagebox
from pprint import pprint
from random import choice
from numpy import *

def rountine(event):
    global player
    if player == 2:
        cursor_x = event.x - mesh
        cursor_y = event.y - mesh
        x = round(cursor_x / mesh)          # x代表着屏幕上的横坐标，棋盘上的列
        y = round(cursor_y / mesh)          # y代表着屏幕上的纵坐标，棋盘上的行
        # 以下的这个判断结构很重要，要记得
        if putchess(x, y) == True:          # 玩家下成功以后才能由AI下
            y, x = minmax_AI()               # 确定AI下棋的最佳位点
            while putchess(x, y) == False:  # AI要下成功为止（Debug功能）
                print('Fail')
                x, y = choice(range(15)), choice(range(15)) # 随机的AI

def putchess(x, y):
    '在指定位置尝试放置棋子，y为行，x为列'
    global player, flag
    radius = 10             # 棋子半径
    colors = ['black', 'white']
    if (in_area(x, y)) and (flag[y, x] == 0):           # 在区域内且无其它棋子
        gamearea.create_oval(mesh * (x + 1) - radius, 
          mesh * (y + 1) - radius,
          mesh * (x + 1) + radius, 
          mesh * (y + 1) + radius,
          fill = colors[player - 2])                    # 画棋子
        flag[y, x] = player                             # 数组标号
        if check_win() == True:                         # 检查该玩家是否胜利
            tkinter.messagebox.showinfo('提示', '玩家%d胜利!' % (player - 1))
            exit()
        player = 5 - player                             # 对换
        return True                                     # 放棋成功
    return False                                        # 放棋失败


def in_area(x, y):
    '界定坐标是否在域内'
    return (0 <= x < 15) and (0 <= y < 15)

def check_win():
    '检查当前玩家是否胜利，由下棋函数调用'
    global flag, size, player
    def prod(five_list):
        '连乘函数'
        count = 1
        for item in five_list:
            count *= item
        return count
    for i in range(size):
        for j in range(size):
            if j <= size - 5:
                right_flag = prod(flag[i, j:j+5])
                if right_flag == player ** 5:
                    return True
            if i <= size - 5:
                bottom_tuple = [flag[i + k, j] for k in range(5)]
                bottom_flag = prod(bottom_tuple)
                if bottom_flag == player ** 5:
                    return True
            if j <= size - 5 and i <= size - 5:
                right_bottom_tuple = [flag[i + k, j + k] for k in range(5)]
                right_bottom_flag = prod(right_bottom_tuple)
                if right_bottom_flag == player ** 5:
                    return True
            if i <= size - 5 and j >= 4:
                left_bottom_tuple = [flag[i + k, j - k] for k in range(5)]
                left_bottom_flag = prod(left_bottom_tuple)
                if left_bottom_flag == player ** 5:
                    return True
    return False

def check_area():
    '检查棋盘上的非空区域大小，缩小搜索范围'
    global flag, size
    min_row, min_column, max_row, max_column = size-1, size-1, 0, 0
    for row in range(size):
        for column in range(size):
            if flag[row, column] != 0:
                min_row = min([row, min_row])
                min_column = min([column, min_column])
                max_row = max([row, max_row])
                max_column = max([column, max_column])
    min_row, min_column = max([0, min_row - 2]), max([0, min_column - 2])
    max_row, max_column = min([size - 1, max_row + 2]), min([size - 1, max_column + 2])
    return min_row, min_column, max_row, max_column

def minmax_AI():
    '采用极大极小算法的AI'
    global flag, size, player
    def evaluate(count, vacancyB, vacancyA):
        '对棋型进行评分'
        if count == 5:
            return 50000
        elif count == 4:
            if vacancyA * vacancyB == 0:
                return 1000
            else:
                return 5000
        elif count == 3:
            if vacancyA * vacancyB == 0:
                return 100
            else:
                return 500
        elif count == 2 and vacancyA * vacancyB > 0:
            return 50
        else:
            return 0

    def judge_game():
        '对整个游戏局面进行评估'
        line_list = []
        min_row, min_column, max_row, max_column = check_area()
        for i in range(min_row, max_row + 1):
            line_list.append(flag[i, min_column:max_column + 1])
        for i in range(min_column, max_column + 1):
            line_list.append(flag[min_row:max_row + 1,i])
        value = 0
        for i in range(len(line_list)):
            value += judge_line(line_list[i], player)
            value -= judge_line(line_list[i], 5 - player)
        return value

    def judge_line(line, the_player, from_place=False, current=0):
        '对某一列进行棋型估分'
        mine = False        # 定义当前位置是否为己方的棋子
        count = 0
        span = len(line)
        hit_start, hit_end = 0, 0
        line_value = 0
        for i in range(span):
            if line[i] == the_player:
                if mine == False:
                    mine = True
                    count = 1
                    hit_start = i
                else:
                    count += 1
            else:
                mine = False
                if count > 1:
                    hit_end = i
                    if from_place == False or hit_start <= current <= hit_end:
                        for j in range(hit_start, -1, -1):
                            if line[j] > 0:
                                break
                        vacancy_before = hit_start - j
                        for j in range(hit_end, span):
                            if line[j] > 0:
                                break
                        vacancy_after = j - hit_end
                        if count + vacancy_before + vacancy_after >= 5:
                            line_value += evaluate(count, vacancy_before, vacancy_after)
                        i = j   # 下一次检查直接从本区域的空边界开始，节省时间
                count = 0
        return line_value

    def judge_place(row, column, the_player):
        '对某一位置放下的棋子产生的棋型估分'
        flag[row, column] = the_player
        line_list = []
        current_list = []
        line_list.append(flag[row])
        current_list.append(column)
        line_list.append(flag[...,column])
        current_list.append(row)
        if column > row:
            line_list.append([flag[row + k, column + k] for k in range(- row,size - column)])
            current_list.append(row)
        else:
            line_list.append([flag[row + k, column + k] for k in range(- column,size - row)])
            current_list.append(column)
        if size - row > column:
            line_list.append([flag[size - row + k, column + k] for k in range(- column, row)])
            current_list.append(column)
        else:
            line_list.append([flag[size - row + k, column + k] for k in range(row - size, size - column)])
            current_list.append(row)
        value = 0
        for i in range(len(line_list)):
            value += judge_line(line_list[i], the_player, True, current_list[i])
        flag[row, column] = 0
        return value + min([row, column, size - row - 1, size - column - 1])

    def minmax(depth, the_player, counter=0):
        '不带alpha-beta剪枝的minmax优化算法'
        best_score, best_row, best_column = -5000000, 0, 0
        min_row, min_column, max_row, max_column = check_area()
        best_list = []
        for row in range(min_row, max_row + 1):
            for column in range(min_column, max_column + 1):
                if flag[row, column] == 0:
                    best_list.append([judge_place(row, column, the_player) +\
                      judge_place(row, column, 5 - the_player), row, column])
        best_list.sort()
        best_list = best_list[-4:]
        for i in range(len(best_list)):
            row, column = best_list[i][1], best_list[i][2]
            init_score = best_list[i][0]
            if depth == 1:
                score = init_score
                flag[row, column] = the_player
                score += judge_game() + min([row, column, size - row - 1, size - column - 1])
                counter += 1
            else:
                flag[row, column] = the_player
                score, tmp, tmp, counter = minmax(depth - 1, 5 - the_player, counter)
                score = - score
                counter += 1
            if score > best_score:
                best_score, best_row, best_column = score, row, column
            flag[row, column] = 0
        return best_score, best_row, best_column, counter

    best_score, best_row, best_column, a_counter= minmax(3, player)
    print(a_counter)
    return best_row, best_column





if __name__ == '__main__':
    # 定义基本的尺寸变量
    mesh = 30
    size = 15
    player = 2
    # 创建棋盘
    flag = zeros([size, size], dtype = int)
    # 创建窗口
    window = Tk()                       # 注册窗口
    window.title('思源杯五子棋锦标赛')   # 标题
    window.geometry(str(mesh * (size + 1)) + 'x' + str(mesh * (size + 1)))
    # 绘制游戏区域的画布
    gamearea = Canvas(window,
      bg = '#E7C981',
      width = mesh * (size + 1),
      height = mesh * (size + 1))
    gamearea.pack()
    for i in range(size):
        gamearea.create_line(mesh, mesh * (i + 1), mesh * size, mesh * (i + 1))
        gamearea.create_line(mesh * (i + 1), mesh, mesh * (i + 1), mesh * size)
    gamearea.bind('<Button-1>', rountine)   # 绑定鼠标左击事件
    window.mainloop()