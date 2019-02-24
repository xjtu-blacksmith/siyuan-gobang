from tkinter import *

def putchess(event):
    global player
    radius = 10
    colors = ['black', 'white']
    cursor_x = event.x - mesh
    cursor_y = event.y - mesh
    order_x = round(cursor_x / mesh)
    order_y = round(cursor_y / mesh)
    gamearea.create_oval(mesh * (order_x + 1) - radius, 
      mesh * (order_y + 1) - radius,
      mesh * (order_x + 1) + radius, 
      mesh * (order_y + 1) + radius,
      fill = colors[player - 2])
    player = 5 - player


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
    gamearea.bind('<Button-1>', putchess)
    window.mainloop()