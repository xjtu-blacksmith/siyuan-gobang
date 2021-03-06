# 思源杯五子棋项目 siyuan-gobang
这是一个计划用于开发人工智能五子棋游戏的仓库，目前包含的内容有：

- 作者之前在编程课上开发的`cpp`版本五子棋源码，不包含AI模块，含禁手判别。
- 百度百科“禁手”词条的网页快照，页面截取时间为2018.5.12。
- `python`版本的源代码（`mygame.py`）

正在进行的工作：
- 开始`python`版本的框架搭建
- `cpp`源码的注释补充
- 学习两种基本的AI算法：决策树算法（含alpha-beta剪枝），强化学习方法

## 工作日志
### 2019.02.24
- 为 `cpp`源码“随性地”添加了一些注释
- 初步搭建了`tkinter`的界面，呈现于`mygame.py`文件中，已可以在棋盘上交替放置棋子

### 2019.03.03
- 完善了游戏终局的判断规则
- 编写了一个只会横纵择优、不知防守的`basic_AI`

### 2019.04.29
- 尝试编写了使用决策树进行搜索的`minmax_AI`，未完成

### 2019.05.01
- 完善了`minmax_AI`的机制，已能在深度为1（不预判）的情况下作出比basic_AI好得多的决策
- 删除了`basic_AI`的代码

### 2019.05.02
- 进一步优化了`minmax_AI`的功能，大大减轻了搜索量，已能在深度为3（预判一轮）的情况下流畅运行
- 尝试了alpha-beta剪枝算法，未获成功（还没有完全理解其机制如何融合到我的程序中……）

### 2019.06.21
- 为`mygame.py`补充了大量的注释，标注了当前存在的问题
- 修正了`minmax_AI`中个别子函数的漏洞，完善了其功能
- 删除了`gobang.cpp`文件，因其功能均已实现了
