#coding:utf-8

# 导入UI模块
import tkinter as Tkinter

#SMBus (System Management Bus,系统管理总线) 
import smbus   #在程序中导入“smbus”模块
import RPi.GPIO as GPIO # 导入树莓派GPIO模块
import time # 导入定时器模块
import threading


# 主页面设置
top = Tkinter.Tk()
top.geometry('500x300')
top.title("操纵杆控制圆球")

# 当前圆球的坐标
currentX = 0
currentY = 0
# 当前圆球的颜色是否红色
currentColor = True

# 进行窗口的初始化
canvas = Tkinter.Canvas(top, width=500, height=300, borderwidth=0, highlightthickness=0)
canvas.grid()

# 进化画布的初始化
circle = canvas.create_oval(currentX, currentY, 100, 100, fill="red", outline="")

# 定义移动圆球的方法
def moveCircle(c, x, y):
    global currentX, currentY
    moveX = x
    moveY = y
    if x >= 0:
        if x + currentX > 400:
            moveX = 400 - currentX
            currentX = 400
        else:
            currentX += x
    else:
        if x + currentX < 0:
            moveX = -currentX
            currentX = 0
        else:
            currentX += x
    if y >= 0:
        if y + currentY > 200:
            moveY = 200 - currentY
            currentY = 200
        else:
            currentY += y
    else:
        if y + currentY < 0:
            moveY = -currentY
            currentY = 0
        else:
            currentY += y	
    canvas.move(c, moveX, moveY)

# 定义改变圆球颜色的方法
def changeColor(c):
    global currentColor
    canvas.itemconfig(c, fill= 'red' if currentColor else 'blue')
    currentColor = not currentColor


bus = smbus.SMBus(1)         #创建一个smbus实例

# 通过PCF8591读取模拟信号

# 摇杆X引脚的模拟数据
def readX():
    #发送一个控制字节到设备 表示要读取AIN0通道的数据
    bus.write_byte(0x48,0x40)   
    bus.read_byte(0x48)         # 空读一次，消费掉无效数据
    return bus.read_byte(0x48)  # 返回某通道输入的模拟值A/D转换后的数字值

# 摇杆Y引脚的模拟数据
def readY():
	#发送一个控制字节到设备 表示要读取AIN1通道的数据
    bus.write_byte(0x48,0x41)   
    bus.read_byte(0x48)         # 空读一次，消费掉无效数据
    return bus.read_byte(0x48)  # 返回某通道输入的模拟值A/D转换后的数字值

# 通过GPIO读取数字信号

# 设置使用的引脚编码模式
GPIO.setmode(GPIO.BOARD)
# 按键使用引脚 BCM 17
BTN = 11
# 引脚初始化 设置下拉高电平
GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 创建定时器函数，用来检查摇杆动作
def fun_timer():
    global timer
    x = readX()
    y = readY()
    press = GPIO.input(BTN)
    print('X：', x)
    print('Y：', y)
    print('按钮：', press)

    if x <= 5:
        moveCircle(circle, -40, 0)
    elif x <= 50:
        moveCircle(circle, -10, 0)
    if x >= 250:
        moveCircle(circle, 40, 0)
    elif x>= 200:
        moveCircle(circle, 10, 0)
    if y <= 10:
        moveCircle(circle, 0, -10)
    if y >= 245:
        moveCircle(circle, 0, 10)

    timer = threading.Timer(0.2, fun_timer)
    timer.start()

timer = threading.Timer(0.2, fun_timer)
timer.start()

# 定义GPIO输入端口的回调
def btnCallback(channel):
    if not GPIO.input(channel):
        changeColor(circle)

# 添加输入引脚电平变化的回调函数
GPIO.add_event_detect(BTN, GPIO.FALLING, callback=btnCallback, bouncetime=200)

top.mainloop()