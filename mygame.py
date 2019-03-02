from tkinter import *
import tkinter.messagebox

def prod(numbers):
    result = 1
    for i in range(len(numbers)):
        result *= numbers[i]
    return result

def putchess(event):
    global player, flag
    radius = 10     # 棋子半径
    colors = ['black', 'white']     # 
    cursor_x = event.x - mesh
    cursor_y = event.y - mesh
    order_x = round(cursor_x / mesh)
    order_y = round(cursor_y / mesh)
    if (in_area(order_x, order_y)) and (flag[order_x][order_y] == 0):
        gamearea.create_oval(mesh * (order_x + 1) - radius, 
          mesh * (order_y + 1) - radius,
          mesh * (order_x + 1) + radius, 
          mesh * (order_y + 1) + radius,
          fill = colors[player - 2])
        flag[order_x][order_y] = player
        if check_win(player) == True:
            tkinter.messagebox.showinfo('提示', '玩家%d胜利!' % (player - 1))
            exit()
        player = 5 - player

def in_area(x, y):
    return (0 <= x < 15) and (0 <= y < 15)

def check_win(player):
    global flag, size
    for i in range(size):
        for j in range(size):
            if j <= size - 5:
                bottom_flag = prod(flag[i][j:j+5])
                if bottom_flag == player ** 5:
                    return True
            if i <= size - 5:
                right_tuple = [flag[k][j] for k in range(i,i+5)]
                right_flag = prod(right_tuple)
                if right_flag == player ** 5:
                    return True
    return False

if __name__ == '__main__':
    # 定义基本的尺寸变量
    mesh = 30
    size = 15
    player = 2
    # 创建棋盘
    flag = []
    for i in range(size):
        flag.append([0] * size)
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
    gamearea.bind('<Button-1>', putchess)   # 绑定鼠标左击事件
    window.mainloop()