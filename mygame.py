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
            y, x = basic_AI()               # 确定AI下棋的最佳位点
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

def basic_AI():
    global flag, size, player
    value = zeros([size, size], dtype = int) 
    def count_five(five_list):
        if sum(five_list) == player * 5:    # 连五
            return 50000
        elif sum(five_list) == player * 4:
            if five_list[0] == 0 or five_list[4] == 0:  # 无法判断(先做活四处理)
                return 5000
            else:       # 冲四
                return 1000
        else:
            return 0
    best_i, best_j = 0, 0
    max_score = 0
    for i in range(size):
        for j in range(size):
            if flag[i, j] == 0:
                new_flag = flag.copy()
                new_flag[i, j] = player
                for k in range(max([0, i - 4]), min([size - 6, i])):
                    bottom_tuple = [new_flag[k + l, j] for l in range(5)]
                    value[i, j] = max([value[i, j], count_five(bottom_tuple) + min([i, j, size - i - 1, size - j - 1])])
                for k in range(max([0, j - 4]), min([size - 6, j])):
                    right_tuple = new_flag[i, k:k+5]
                    value[i, j] = max([value[i, j], count_five(right_tuple) + min([i, j, size - i - 1, size - j - 1])])
                if value[i, j] > max_score:
                    max_score = value[i, j]
                    best_i, best_j = i, j
    return best_i, best_j

def new_AI():
    '采用极大极小算法的新AI'
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
        for i in range(size):
            line_list.append(flag[i])
            line_list.append(flag[...,i])
            if 4 <= i <= 13:
                line_list.append([flag[i - k, k] for k in range(i + 1)])
                line_list.append([flag[i - k, size - k] for k in range(i + 1)])
                line_list.append([flag[size - i + k, k] for k in range(i + 1)])
                line_list.append([flag[size - i + k, size - k] for k in range(i + 1)])
            elif i == 14:
                line_list.append([flag[k, k] for k in range(size)])
                line_list.append([flag[k, size - k] for k in range(size)])
        value = 0
        for i in range(len(line_list)):
            value += judge_line(line_list[i], player)
            value -= judge_line(line_list[i], 5 - player)
        return value

    def judge_line(line, the_player, from_place=False, current = 0):
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
                    if from_place == False or (from_place == True and hit_start < current < hit_end):
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
        line_list.append(flag[row] + [column])  # 复合列表，最后一位存取当前棋子的位置
        line_list.append(flag[...,column] + [row])
        # 斜线暂未完成
        # if column > row:
        #     line_list.append([flag[row + k, column + k] for k in range(- row:size - row + 1)] + [row + 1])
        # else:
        #     line_list.append([flag[row + k, column + k] for k in range(- column:size - column + 1)] + [column + 1])
        # if size - row > column:
        #     line_list.append([flag[size - row + k, column + k] for k in range(- column:size - column + 1)] + [column + 1])
        # else:
        #     line_list.append([flag[size - row + k, column + k] for k in range(row - size: row + 1)] + [])
        value = 0
        for line in line_list:
            value += judge_line(line[:-1], the_player, True, line[len(line) - 1])
        flag[row, column] = 0
        return value + min([row, column, size - row - 1, size - column - 1])

    value = zeros([size, size], dtype = int)
    max_score = 0
    best_i, best_j = 0, 0
    for i in range(size):
        for j in range(size):
            if flag[i, j] == 0:
                value[i, j] = judge_place(i, j, player)
                if value[i, j] > max_score:
                    best_i, best_j = i, j
                    max_score = value[i, j]
    return best_i, best_j





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