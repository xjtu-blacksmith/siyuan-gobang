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
        x = round(cursor_x / mesh)
        y = round(cursor_y / mesh)
        # 以下的这个判断结构很重要，要记得
        if putchess(x, y) == True:          # 玩家下成功以后才能由AI下
            y, x = basic_AI()
            while putchess(x, y) == False:  # AI要下成功为止
                print('Fail')
                x, y = choice(range(15)), choice(range(15)) # 随机的AI

def putchess(x, y):
    global player, flag
    radius = 10     # 棋子半径
    colors = ['black', 'white']
    if (in_area(x, y)) and (flag[y, x] == 0):
        gamearea.create_oval(mesh * (x + 1) - radius, 
          mesh * (y + 1) - radius,
          mesh * (x + 1) + radius, 
          mesh * (y + 1) + radius,
          fill = colors[player - 2])
        flag[y, x] = player
        if check_win() == True:
            tkinter.messagebox.showinfo('提示', '玩家%d胜利!' % (player - 1))
            exit()
        player = 5 - player
        return True
    return False


def in_area(x, y):
    return (0 <= x < 15) and (0 <= y < 15)

def check_win():
    global flag, size, player
    def prod(five_list):
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