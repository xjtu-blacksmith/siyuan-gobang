# -----------------------
#       mygame.py
#     思源五子棋主程序
#
# author: xjtu-blacksmith
#
# -----------------------

from tkinter import *
import tkinter.messagebox
from pprint import pprint
from random import choice
from numpy import *

# state: dependent
# description: minmax_AI
def rountine(event):
    '游戏循环，执行双方的下棋功能'
    global player
    if player == 2:                         # 玩家下棋
        cursor_x = event.x - mesh
        cursor_y = event.y - mesh
        x = round(cursor_x / mesh)          # x代表着屏幕上的横坐标，棋盘上的列
        y = round(cursor_y / mesh)          # y代表着屏幕上的纵坐标，棋盘上的行
        # 以下的这个判断结构很重要，要记得
        if putchess(x, y) == True:          # 玩家下成功以后才能由AI下
            y, x = minmax_AI(1)               # 确定AI下棋的最佳位点
            while putchess(x, y) == False:  # AI要下成功为止（Debug功能）
                print('Fail')
                x, y = choice(range(15)), choice(range(15)) # 随机的AI

# state: dependent 
# description: minmax_AI
def rountine_AI(event):
    'AI对弈循环，仅供测试使用'
    global player
    row, column = minmax_AI(1)              # 黑方下棋
    while putchess(column, row)==False:     # AI搜索失败，则随机放子
        print('Fail')
        row, column = choice(range(15)), choice(range(15))
    row, column = minmax_AI(1)              # 白方下棋
    while putchess(column, row)==False:
        print('Fail')
        row, column = choice(range(15)), choice(range(15))
    tkinter.messagebox.showinfo('提示', '本轮棋已下完，请您开始下一轮')
        
# state: passed
def putchess(row, column):
    '在指定位置尝试放置棋子，并绘制之；同时判断游戏是否胜利'
    global player, flag
    radius = 10                         # 棋子半径
    colors = ['black', 'white']         # 颜色，用于绘制棋子
    if (in_area(row, column)) and (flag[column, row] == 0): # 在区域内且无其它棋子
        gamearea.create_oval(mesh * (row + 1) - radius, 
          mesh * (column + 1) - radius,
          mesh * (row + 1) + radius, 
          mesh * (column + 1) + radius,
          fill = colors[player - 2])    # 在指定位置画画棋子
        flag[column, row] = player      # 数组标号
        if check_win() == True:         # 检查该玩家是否胜利，调用check_win()子函数
            tkinter.messagebox.showinfo('提示', '玩家%d胜利!' % (player - 1))
            exit()                      # 程序退出
        player = 5 - player             # 对换玩家
        return True                     # 返回值表示放棋成功
    return False                        # 返回值表示放棋失败

# state: passed
def in_area(x, y):
    '界定坐标是否在域内'
    return (0 <= x < 15) and (0 <= y < 15)

# state: passed
def check_win():
    '检查当前玩家是否胜利，由下棋函数调用'
    global flag, size, player
    def prod(five_list):
        '连乘函数，以简便的计算判断输赢'
        count = 1
        for item in five_list:
            count *= item
        return count
    # 主程序段开始    
    for i in range(size):
        for j in range(size):
            if j <= size - 5:
                right_flag = prod(flag[i, j:j+5])   # 判断列乘积
                if right_flag == player ** 5:
                    return True
            if i <= size - 5:
                bottom_tuple = [flag[i + k, j] for k in range(5)]   # 判断行乘积
                bottom_flag = prod(bottom_tuple)
                if bottom_flag == player ** 5:
                    return True
            if j <= size - 5 and i <= size - 5:
                right_bottom_tuple = [flag[i + k, j + k] for k in range(5)] # 判断二四象限对角线乘积
                right_bottom_flag = prod(right_bottom_tuple)
                if right_bottom_flag == player ** 5:
                    return True
            if i <= size - 5 and j >= 4:
                left_bottom_tuple = [flag[i + k, j - k] for k in range(5)]  # 判断一三象限对角线乘积
                left_bottom_flag = prod(left_bottom_tuple)
                if left_bottom_flag == player ** 5:
                    return True
    return False

# state: passed
def check_area():
    '检查棋盘上的非空区域大小，以便缩小搜索范围'
    global flag, size
    min_row, min_column, max_row, max_column = size - 1, size - 1, 0, 0     # 初值设定
    for row in range(size):
        for column in range(size):
            if flag[row, column] != 0:                                      # 发现棋子
                min_row = min([row, min_row])
                min_column = min([column, min_column])
                max_row = max([row, max_row])
                max_column = max([column, max_column])                      # 标定新的极值
    min_row, min_column = max([0, min_row - 2]), max([0, min_column - 2])   # 沿极值向外拓展2格
    max_row, max_column = min([size - 1, max_row + 2]), min([size - 1, max_column + 2])
    return min_row, min_column, max_row, max_column

# state: imperfect
# description: 部分功能不完善；棋型判断不理想；缺少alpha-beta剪枝
def minmax_AI(depth=3):
    '采用极大极小算法的AI'

    global flag, size, player

    # state: imperfect
    # description: 对于间断棋型未计分，导致对“活三”、“冲四”等棋型的识别较为片面
    def evaluate(count, vacancyB, vacancyA):
        '子程序，对棋型进行评分'
        if count == 5:                      # 连五，胜利
            return 50000
        elif count == 4:
            if vacancyA * vacancyB == 0:    # 冲四 
                return 1000
            else:                           # 活四
                return 5000
        elif count == 3:
            if vacancyA * vacancyB == 0:    # 冲三
                return 100
            else:                           # 活三
                return 500
        elif count == 2 and vacancyA * vacancyB > 0:    # 二连
            return 50
        else:                               # 无特殊棋型
            return 0

    # state: imperfect
    # description: 对角线未评估
    def judge_game():
        '子程序，对整个游戏局面进行评估'
        line_list = []                      # 列表初始化
        min_row, min_column, max_row, max_column = check_area() # 确定搜索范围
        for i in range(min_row, max_row + 1):
            line_list.append(flag[i, min_column:max_column + 1])
        for i in range(min_column, max_column + 1):
            line_list.append(flag[min_row:max_row + 1,i])       # 将行与列编入列表
        value = 0
        for i in range(len(line_list)):
            value += judge_line(line_list[i], player)
            value -= judge_line(line_list[i], 5 - player)       # 评估各列分数，求和
        return value                        # 返回总价值

    # state: imperfect
    # description: 未判断间断棋型
    def judge_line(line, the_player, from_place=False, current=0):
        '子程序，对某一列进行棋型估分'
        mine = False        # 定义变量，以判断当前位置是否为己方的棋子
        count = 0           # 计数器
        span = len(line)    # 列长度，行列与对角线并不相同
        hit_start, hit_end = 0, 0
        line_value = 0      # 价值初始化
        for i in range(span):           # 遍历整列
            if line[i] == the_player:   # 检测到己方棋子
                if mine == False:       # 尚未开始记录
                    mine = True         # 自此开始记录
                    count = 1
                    hit_start = i
                else:                   # 正在记录
                    count += 1
            else:                       # 检测到对手棋子或空隙
                mine = False            # 结束记录
                if count > 1:           # 孤子不计分
                    hit_end = i
                    # 当from_place为True时（由judge_place调用），需寻找落子点current，
                    # 否则（由judge_game）不必判断
                    if from_place == False or hit_start <= current <= hit_end:
                        vacancy_before, vacancy_after = 0, 0
                        for j in range(hit_start - 1, -1, -1):  # 从头向外推，遇子即停
                            if line[j] > 0:
                                vacancy_before = hit_start - j - 1      # 记录左侧空隙
                                break
                        for j in range(hit_end, span):          # 从尾向外推，遇子即停
                            if line[j] > 0:
                                vacancy_after = j - hit_end             # 记录右侧空隙
                                break
                        if count + vacancy_before + vacancy_after >= 5: # 有效区域大于5，价值足够
                            line_value += evaluate(count, vacancy_before, vacancy_after)
                        i = j   # 下一次检查直接从本区域的空边界开始，节省时间
                count = 0
        return line_value

    # state: passed
    def judge_place(row, column, the_player):
        '子程序，对某一位置放下的棋子产生的棋型估分'
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

    # state: imperfect
    # description: 程序环节的正确性有待评估；子函数功能不完善
    def minmax(depth, the_player):
        '子程序（主程序），不带alpha-beta剪枝的minmax优化算法'
        best_score, best_row, best_column = -5000000, 0, 0
        min_row, min_column, max_row, max_column = check_area()
        best_list = []
        for row in range(min_row, max_row + 1):
            for column in range(min_column, max_column + 1):
                if flag[row, column] == 0:
                    best_list.append([judge_place(row, column, the_player) +\
                      judge_place(row, column, 5 - the_player), row, column])
        best_list.sort()
        best_list = best_list[-3:]
        for i in range(len(best_list)):
            row, column = best_list[i][1], best_list[i][2]
            init_score = best_list[i][0]
            if depth == 1:
                score = init_score
                flag[row, column] = the_player
                score += judge_game() + min([row, column, size - row - 1, size - column - 1])
                flag[row, column] = 0
            else:
                flag[row, column] = the_player
                score, tmp, tmp = minmax(depth - 1, 5 - the_player)
                score = - score
                flag[row, column] = 0
            if score > best_score:
                best_score, best_row, best_column = score, row, column
        return best_score, best_row, best_column

    best_score, best_row, best_column= minmax(depth, player)
    return best_row, best_column


# state: passed
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