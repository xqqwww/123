import random # 导入random模块，用于生成随机数
import sys # 导入sys模块，用于访问系统相关的参数和功能
import time # 导入time模块，用于处理时间相关的操作
import pygame # 导入pygame模块，用于创建图形界面和游戏
from blocks import block_s, block_i, block_j, block_l, block_o, block_t, block_z # 从blocks文件中导入不同形状的方块
SCREEN_WIDTH, SCREEN_HEIGHT = 450, 750 # 设置屏幕的宽度和高度
BG_COLOR = (40, 40, 60)  # 设置背景色为深蓝色
BLOCK_COL_NUM = 10  # 设置每行的方格数为10
SIZE = 30  # 设置每个小方格的大小为30像素
BLOCK_ROW_NUM = 25  # 设置每列的方格数为25
BORDER_WIDTH = 4  # 设置游戏区的边框宽度为4像素
RED = (200, 30, 30)  # 设置红色，用于显示GAME OVER的字体颜色
def judge_game_over(stop_all_block_list):
    """
    判断游戏是否结束
    """
    if "O" in stop_all_block_list[0]: # 如果第一行有方块，说明游戏区已经满了
        return True # 返回True，表示游戏结束
def change_speed(score):
    # 定义一个函数，用于根据分数改变方块下落的速度
    speed_level = [("1", 0.5, 0, 20), ("2", 0.4, 21, 50), ("3", 0.3, 51, 100), ("4", 0.2, 101, 200), ("5", 0.1, 201, None)] # 定义一个列表，存储不同的速度等级，每个元素是一个元组，包含速度信息，速度值，分数范围
    for speed_info, speed, score_start, score_stop in speed_level: # 遍历列表中的每个元素
        if score_stop and score_start <= score <= score_stop: # 如果分数在某个范围内
            return speed_info, speed # 返回对应的速度信息和速度值
        elif score_stop is None and score >= score_start: # 如果分数超过了最高的范围
            return speed_info, speed # 返回最高的速度信息和速度值
def judge_lines(stop_all_block_list):
    """
    判断是否有同一行的方格，如果有则消除
    """
    # 定义一个函数，用于判断是否有满格的行，如果有则消除并移动剩余的行
    move_row_list = list() # 创建一个空列表，用于存储需要移动的行的索引
    # 消除满格的行
    for row, line in enumerate(stop_all_block_list): # 遍历游戏区的每一行，得到行的索引和内容
        if "." not in line: # 如果这一行没有. 那么就意味着全部是O，即满格
            # 消除这一行
            stop_all_block_list[row] = ['.' for _ in range(len(line))] # 将这一行的内容替换为全是. 的列表
            move_row_list.append(row) # 将这一行的索引添加到移动列表中

    # 如果没有满格的行，则结束此函数
    if not move_row_list: # 如果移动列表为空
        return 0 # 返回0，表示没有消除任何行

    # 移动剩余的行到下一行
    for row in move_row_list: # 遍历移动列表中的每个索引
        stop_all_block_list.pop(row) # 从游戏区中删除这一行
        stop_all_block_list.insert(0, ['.' for _ in range(len(line))]) # 在游戏区的最上方插入一行全是. 的列表

    return len(move_row_list) * 10 # 返回消除的行数乘以10，作为得分
def add_to_stop_all_block_list(stop_all_block_list, current_block, current_block_start_row, current_block_start_col):
    """
    将当前已经停止移动的block添加到列表中
    """
    # 定义一个函数，用于将当前的方块添加到游戏区中
    for row, line in enumerate(current_block): # 遍历当前方块的每一行，得到行的索引和内容
        for col, block in enumerate(line): # 遍历当前方块的每一列，得到列的索引和内容
            if block != '.': # 如果方块的内容不是.，即有颜色
                stop_all_block_list[current_block_start_row + row][current_block_start_col + col] = "O" # 将游戏区中对应的位置设置为O，表示有方块
def change_current_block_style(current_block):
    """
    改变图形的样式
    """
    # 定义一个函数，用于改变当前方块的形状
    # 计算出，当前图形样式属于哪个图形
    current_block_style_list = None # 创建一个空变量，用于存储当前方块所属的图形列表
    for block_style_list in [block_s, block_i, block_j, block_l, block_o, block_t, block_z]: # 遍历所有的图形列表
        if current_block in block_style_list: # 如果当前方块在某个图形列表中
            current_block_style_list = block_style_list # 将这个图形列表赋值给当前方块所属的图形列表

    # 得到当前正在用的图形的索引（下标）
    index = current_block_style_list.index(current_block) # 从当前方块所属的图形列表中找到当前方块的索引
    # 它的下一个图形的索引
    index += 1 # 将索引加一，得到下一个图形的索引
    # 防止越界
    index = index % len(current_block_style_list) # 用模运算，防止索引超过图形列表的长度
    # 返回下一个图形
    return current_block_style_list[index] # 从当前方块所属的图形列表中返回下一个图形
def judge_move_right(current_block, current_block_start_col):
    """
    判断是否可以向右移动
    """
    # 定义一个函数，用于判断当前方块是否可以向右移动
    # 先判断列的方式是从右到左
    for col in range(len(current_block[0]) - 1, -1, -1): # 从当前方块的最右边的列开始，向左遍历每一列，得到列的索引
        # 得到1列的所有元素
        col_list = [line[col] for line in current_block] # 用列表推导式，得到当前方块的这一列的所有元素
        # 判断是否碰到右边界
        if 'O' in col_list and current_block_start_col + col >= BLOCK_COL_NUM: # 如果这一列有O，即有颜色，而且当前方块的起始列加上这一列的索引大于等于游戏区的列数，说明已经到达右边界
            return False # 返回False，表示不能向右移动
    return True # 如果没有碰到右边界，返回True，表示可以向右移动
def judge_move_left(current_block, current_block_start_col):
    """
    判断是否可以向左移动
    """
    # 定义一个函数，用于判断当前方块是否可以向左移动
    # 先判断列的方式是从左到右
    for col in range(len(current_block[0])):
        # 得到1列的所有元素
        col_list = [line[col] for line in current_block]
        # 判断是否碰到右边界
        if 'O' in col_list and current_block_start_col + col < 0:
            return False # 如果有'O'表示方块的部分，并且列的位置小于0，说明不能再向左移动，返回False
    return True # 否则，返回True，表示可以向左移动

def judge_move_down(current_block, current_block_start_row, current_block_start_col, stop_all_block_list):
    """
    判断是否碰撞到其它图形或者底边界
    """
    # 定义一个函数，用于判断当前方块是否碰撞到其它图形或者底边界
    # 得到其它图形所有的坐标
    stop_all_block_position = list() # 创建一个空列表，用于存储已经停止移动的方块的坐标
    for row, line in enumerate(stop_all_block_list):
        for col, block in enumerate(line):
            if block != ".":
                stop_all_block_position.append((row, col)) # 遍历停止移动的方块列表，如果不是'.'，说明有方块，就把它的行和列的坐标加入到列表中
        # print(stop_all_block_position) # 这一行是用于调试的，可以打印出停止移动的方块的坐标
    # 判断碰撞
    for row, line in enumerate(current_block):
        if 'O' in line and current_block_start_row + row >= BLOCK_ROW_NUM:
            # 如果当前行有0，且从起始行开始算+当前显示的行，超过了总行数，那么就认为碰到了底部
            return False # 返回False，表示不能再向下移动
        for col, block in enumerate(line):
            if block != "." and (current_block_start_row + row, current_block_start_col + col) in stop_all_block_position:
                return False # 如果当前方块的部分不是'.'，并且它的坐标和停止移动的方块的坐标重合，说明碰撞了，返回False
    return True # 否则，返回True，表示可以向下移动

def get_block():
    """
    创建一个图形
    """
    # 定义一个函数，用于创建一个随机的图形
    block_style_list = random.choice([block_s, block_i, block_j, block_l, block_o, block_t, block_z]) # 从预定义的图形列表中随机选择一个
    return random.choice(block_style_list) # 从选择的图形中随机选择一个旋转的样式，返回这个图形

def main():
    pygame.init() # 初始化pygame库
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 创建一个窗口，大小为屏幕的宽和高
    pygame.display.set_caption('俄罗斯方块') # 设置窗口的标题为'俄罗斯方块'
    current_block = get_block()  # 当前图形，调用get_block函数得到一个随机的图形
    current_block_start_row = -2  # 当前图片从哪一行开始显示图形，初始值为-2，表示从屏幕外开始下落
    current_block_start_col = 4  # 当前图形从哪一列开始显示，初始值为4，表示从中间开始
    next_block = get_block()  # 下一个图形，调用get_block函数得到一个随机的图形
    last_time = time.time() # 记录上一次下落的时间，初始值为当前的时间
    speed = 0.5  # 降落的速度，初始值为0.5秒一格
    speed_info = '1'  # 显示的速度等级，初始值为1
    # 定义一个列表，用来存储所有的已经停止移动的形状
    stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)] # 创建一个二维列表，用'.'表示空白，用于存储已经停止移动的方块的位置
    # 字体
    font = pygame.font.Font('yh.ttf', 24)  # 黑体24，创建一个字体对象，用于显示文字
    game_over_font = pygame.font.Font("yh.ttf", 72) # 黑体72，创建一个字体对象，用于显示游戏结束的文字
    game_over_font_width, game_over_font_height = game_over_font.size('GAME OVER') # 获取游戏结束的文字的宽度和高度，用于居中显示
    game_again_font_width, game_again_font_height = font.size('鼠标点击任意位置，再来一局') # 获取再来一局的文字的宽度和高度，用于居中显示
    # 得分
    score = 0 # 初始得分为0
    # 标记游戏是否结束
    game_over = False # 初始游戏状态为未结束
    # 创建计时器（防止while循环过快，占用太多CPU的问题）
    clock = pygame.time.Clock() # 创建一个时钟对象，用于控制游戏的帧率

    while True:  # 创建一个无限循环，用于不断更新游戏的状态
        for event in pygame.event.get():  # 遍历pygame的事件列表，处理用户的输入
            if event.type == pygame.QUIT:  # 如果用户点击了关闭按钮，退出游戏
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 如果用户按下了键盘上的某个键
                if event.key == pygame.K_LEFT:  # 如果用户按下了左方向键
                    if judge_move_left(current_block,
                                       current_block_start_col - 1):  # 调用judge_move_left函数，判断当前方块是否可以向左移动一格
                        current_block_start_col -= 1  # 如果可以，就把当前方块的起始列减一
                elif event.key == pygame.K_RIGHT:  # 如果用户按下了右方向键
                    if judge_move_right(current_block,
                                        current_block_start_col + 1):  # 调用judge_move_right函数，判断当前方块是否可以向右移动一格
                        current_block_start_col += 1  # 如果可以，就把当前方块的起始列加一
                elif event.key == pygame.K_UP:  # 如果用户按下了上方向键
                    current_block_next_style = change_current_block_style(
                        current_block)  # 调用change_current_block_style函数，得到当前方块的下一个旋转样式
                    if judge_move_left(current_block_next_style, current_block_start_col) and \
                            judge_move_right(current_block_next_style, current_block_start_col) and \
                            judge_move_down(current_block, current_block_start_row, current_block_start_col,
                                            stop_all_block_list):
                        # 判断新的样式没有越界，即可以向左、右、下移动
                        current_block = current_block_next_style  # 如果没有越界，就把当前方块的样式更新为新的样式
                elif event.key == pygame.K_DOWN:  # 如果用户按下了下方向键
                    # 判断是否可以向下移动，如果碰到底部或者其它的图形就不能移动了
                    if judge_move_down(current_block, current_block_start_row + 1, current_block_start_col,
                                       stop_all_block_list):  # 调用judge_move_down函数，判断当前方块是否可以向下移动一格
                        current_block_start_row += 1  # 如果可以，就把当前方块的起始行加一
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:  # 如果用户按下了鼠标的某个按钮
                if game_over:  # 如果游戏已经结束
                    # 重置游戏用到的变量
                    current_block = get_block()  # 当前图形，调用get_block函数得到一个随机的图形
                    current_block_start_row = -2  # 当前图片从哪一行开始显示图形，初始值为-2，表示从屏幕外开始下落
                    current_block_start_col = 4  # 当前图形从哪一列开始显示，初始值为4，表示从中间开始
                    next_block = get_block()  # 下一个图形，调用get_block函数得到一个随机的图形
                    stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in
                                           range(BLOCK_ROW_NUM)]  # 创建一个二维列表，用'.'表示空白，用于存储已经停止移动的方块的位置
                    score = 0  # 重置得分为0
                    game_over = False  # 重置游戏状态为未结束
        # 判断是否修改当前图形显示的起始行
        if not game_over and time.time() - last_time > speed:  # 如果游戏没有结束，并且当前时间减去上一次下落的时间大于速度，说明需要下落一格
            last_time = time.time()  # 更新上一次下落的时间为当前时间
            # 判断是否可以向下移动，如果碰到底部或者其它的图形就不能移动了
            if judge_move_down(current_block, current_block_start_row + 1, current_block_start_col,
                               stop_all_block_list):  # 调用judge_move_down函数，判断当前方块是否可以向下移动一格
                current_block_start_row += 1  # 如果可以，就把当前方块的起始行加一
            else:  # 如果不能
                # 将这个图形存储到统一的列表中，这样便于判断是否成为一行
                add_to_stop_all_block_list(stop_all_block_list, current_block, current_block_start_row,
                                           current_block_start_col)  # 调用add_to_stop_all_block_list函数，把当前方块的位置和样式添加到停止移动的方块列表中
                # 判断是否有同一行的，如果有就消除，且加上分数
                score += judge_lines(stop_all_block_list)  # 调用judge_lines函数，判断是否有可以消除的行，如果有，就消除并返回消除的行数，加到得分上
                # 判断游戏是否结束（如果第一行中间有O那么就表示游戏结束）
                game_over = judge_game_over(
                    stop_all_block_list)  # 调用judge_game_over函数，判断是否游戏结束，如果结束，就把game_over变量设为True
                # 调整速度
                speed_info, speed = change_speed(score)  # 调用change_speed函数，根据得分调整速度等级和速度值
                # 创建新的图形
                current_block = next_block  # 把当前方块更新为下一个方块
                next_block = get_block()  # 把下一个方块更新为一个随机的图形
                # 重置数据
                current_block_start_col = 4  # 把当前方块的起始列重置为4
                current_block_start_row = -2  # 把当前方块的起始行重置为-2

    # 画背景（填充背景色）
        screen.fill(BG_COLOR) # 调用screen对象的fill方法，用背景色填充整个窗口
        # 画游戏区域分隔线
        pygame.draw.line(screen, (100, 40, 200), (SIZE * BLOCK_COL_NUM, 0), (SIZE * BLOCK_COL_NUM, SCREEN_HEIGHT), BORDER_WIDTH)# 调用pygame.draw.line函数，画一条竖线，用于分隔游戏区域和右侧的信息区域，颜色为紫色，宽度为边框宽度
        # 显示当前图形
        for row, line in enumerate(current_block):# 遍历当前方块的每一行，用row表示行号，line表示行内容
            for col, block in enumerate(line): # 遍历当前行的每一列，用col表示列号，block表示方块的部分
                if block != '.': # 遍历当前行的每一列，用col表示列号，block表示方块的部分
                    pygame.draw.rect(screen, (20, 128, 200), ((current_block_start_col + col) * SIZE, (current_block_start_row + row) * SIZE, SIZE, SIZE), 0)
        # 调用pygame.draw.rect函数，画一个矩形，用于表示方块的部分，颜色为蓝色，位置根据当前方块的起始行和列以及行号和列号计算，大小为方格的大小
        # 显示所有停止移动的图形
        for row, line in enumerate(stop_all_block_list): # 调用pygame.draw.rect函数，画一个矩形，用于表示方块的部分，颜色为蓝色，位置根据当前方块的起始行和列以及行号和列号计算，大小为方格的大小
            for col, block in enumerate(line): # 遍历当前行的每一列，用col表示列号，block表示方块的部分
                if block != '.':# 如果方块的部分不是'.'，说明有方块
                    pygame.draw.rect(screen, (20, 128, 200), (col * SIZE, row * SIZE, SIZE, SIZE), 0)# 调用pygame.draw.rect函数，画一个矩形，用于表示方块的部分，颜色为蓝色，位置根据行号和列号计算，大小为方格的大小
        # 画网格线 竖线
        for x in range(BLOCK_COL_NUM): # 遍历游戏区域的每一列，用x表示列号
            pygame.draw.line(screen, (0, 0, 0), (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1) # 调用pygame.draw.line函数，画一条竖线，用于表示网格线，颜色为黑色，宽度为1，位置根据列号计算
        # 画网格线 横线
        for y in range(BLOCK_ROW_NUM): # 遍历游戏区域的每一行，用y表示行号
            pygame.draw.line(screen, (0, 0, 0), (0, y * SIZE), (BLOCK_COL_NUM * SIZE, y * SIZE), 1)# 调用pygame.draw.line函数，画一条横线，用于表示网格线，颜色为黑色，宽度为1，位置根据行号计算
        # 显示右侧（得分、速度、下一行图形）
        # 得分
        score_show_msg = font.render('得分: ', True, (255, 255, 255)) # 调用字体对象的render方法，生成一个显示'得分:'的图像，颜色为白色
        screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 10)) # 调用screen对象的blit方法，把得分的图像绘制到窗口的右上角，距离右边框10个像素，距离上边框10个像素
        score_show_msg = font.render(str(score), True, (255, 255, 255)) # 调用字体对象的render方法，生成一个显示得分值的图像，颜色为白色
        screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 50)) # 调用screen对象的blit方法，把得分值的图像绘制到窗口的右上角，距离右边框10个像素，距离上边框50个像素
        # 速度
        speed_show_msg = font.render('速度: ', True, (255, 255, 255)) # 调用字体对象的render方法，生成一个显示'速度:'的图像，颜色为白色
        screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 100))# 调用screen对象的blit方法，把速度的图像绘制到窗口的右上角，距离右边框10个像素，距离上边框100个像素
        speed_show_msg = font.render(speed_info, True, (255, 255, 255))# 调用字体对象的render方法，生成一个显示速度等级的图像，颜色为白色
        screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 150))# 调用screen对象的blit方法，把速度等级的图像绘制到窗口的右上角，距离右边框10个像素，距离上边框150个像素
        # 下一个图形（文字提示）
        next_style_msg = font.render('下一个: ', True, (255, 255, 255)) # 调用字体对象的render方法，生成一个显示'下一个:'的图像，颜色为白色
        screen.blit(next_style_msg, (BLOCK_COL_NUM * SIZE + 10, 200))# 调用screen对象的blit方法，把下一个的图像绘制到窗口的右上角，距离右边框10个像素，距离上边框200个像素
        # 下一个图形（图形）
        for row, line in enumerate(next_block): # 遍历下一个方块的每一行，用row表示行号，line表示行内容
            for col, block in enumerate(line): # 遍历当前行的每一列，用col表示列号，block表示方块的部分
                if block != '.': # 如果方块的部分不是'.'，说明有方块
                    pygame.draw.rect(screen, (20, 128, 200), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE, SIZE, SIZE), 0)# 调用pygame.draw.rect函数，画一个矩形，用于表示方块的部分，颜色为蓝色，位置根据行号和列号计算，大小为方格的大小
                    # 显示这个方格的4个边的颜色
                    # 左
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE), 1)# 调用pygame.draw.line函数，画一条黑色的竖线，用于表示方块的左边，宽度为1，位置根据行号和列号计算
                    # 上
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE), 1) # 调用pygame.draw.line函数，画一条黑色的横线，用于表示方块的上边，宽度为1，位置根据行号和列号计算
                    # 下
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1) # 调用pygame.draw.line函数，画一条黑色的横线，用于表示方块的下边，宽度为1，位置根据行号和列号计算
                    # 右
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1) # 调用pygame.draw.line函数，画一条黑色的竖线，用于表示方块的右边，宽度为1，位置根据行号和列号计算
        # 显示游戏结束画面
        if game_over:# 如果游戏已经结束
            game_over_tips = game_over_font.render('GAME OVER', True, RED)# 调用字体对象的render方法，生成一个显示'GAME OVER'的图像，颜色为红色
            screen.blit(game_over_tips, ((SCREEN_WIDTH - game_over_font_width) // 2, (SCREEN_HEIGHT - game_over_font_height) // 2))# 调用screen对象的blit方法，把游戏结束的图像绘制到窗口的中间，位置根据图像的宽度和高度计算
            # 显示"鼠标点击任意位置，再来一局"
            game_again = font.render('鼠标点击任意位置，再来一局', True, RED) # 调用字体对象的render方法，生成一个显示'鼠标点击任意位置，再来一局'的图像，颜色为红色
            screen.blit(game_again, ((SCREEN_WIDTH - game_again_font_width) // 2, (SCREEN_HEIGHT - game_again_font_height) // 2 + 80)) # 调用screen对象的blit方法，把再来一局的图像绘制到窗口的中间下方，位置根据图像的宽度和高度计算


        # 刷新显示（此时窗口才会真正的显示）
        pygame.display.update() # 调用pygame.display.update函数，更新整个窗口的显示，把之前绘制的图像和文字显示出来
        # FPS（每秒钟显示画面的次数）
        clock.tick(60)  # 通过一定的延时，实现1秒钟能够循环60次，相当于控制游戏的帧率为60帧
if __name__ == '__main__':
    main()