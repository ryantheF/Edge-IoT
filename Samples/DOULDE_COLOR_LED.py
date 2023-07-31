#coding:utf-8

# 导入UI模块
import tkinter as Tkinter
# 导入GPIO控制薄块
import RPi.GPIO as GPIO
# 定时器模块
import threading

# 主页面设置
top = Tkinter.Tk()
top.geometry('500x300')
top.title("双色LED灯控制器")
l = Tkinter.Label(top, text='欢迎使用双色LED灯控制器', bg='green', font=('Arial', 18), width=30, height=2)
l.pack()

# 定义引脚
pins = {0:12,1:35}
# 设置使用的引脚编码模式
GPIO.setmode(GPIO.BOARD)
# 设置隐藏警告
GPIO.setwarnings(False)
# 初始化物理引脚 13 和 15
GPIO.setup(pins[0],GPIO.OUT)
GPIO.setup(pins[1],GPIO.OUT)

# 定义全局字段 用来处理闪烁功能
# f:是否闪烁  l:下次点亮红灯或绿灯
f = False
l = False

# 控制红灯亮
def redClick():
    global f
    f = False
    GPIO.output(pins[0],GPIO.HIGH)
    GPIO.output(pins[1],GPIO.LOW)
	
# 控制绿灯亮
def greenClick():
    global f
    f = False
    GPIO.output(pins[0],GPIO.LOW)
    GPIO.output(pins[1],GPIO.HIGH)

# 退出程序
def stopClick():
    global f
    f = False
    GPIO.output(pins[0],GPIO.LOW)
    GPIO.output(pins[1],GPIO.LOW)
    GPIO.cleanup()
    exit()

# 循环闪烁
def loop():
    global f
    global timer
    global l
    if f == False:
        return
    timer = threading.Timer(1,loop)
    timer.start()
    if l:
        GPIO.output(pins[0],GPIO.HIGH)
        GPIO.output(pins[1],GPIO.LOW)
    else:
        GPIO.output(pins[0],GPIO.LOW)
        GPIO.output(pins[1],GPIO.HIGH)
    # 转换下次闪烁的颜色
    l = not l

# 定义全局定时器
timer = threading.Timer(2, loop)

# 开始进行闪烁
def flckerClick():
    global f
    global timer
    f = True
    timer = threading.Timer(1,loop)
    timer.start()

# UI上的按钮布局
redButton = Tkinter.Button(top, text="红灯停", height='3', command=redClick)
redButton.pack()

greenButton = Tkinter.Button(top, text="绿灯行", height='3', command=greenClick)
greenButton.pack()

flckerButton = Tkinter.Button(top, text="闪烁请注意", height='3', command=flckerClick)
flckerButton.pack()

stopButton = Tkinter.Button(top, text="关闭", height='3', command=stopClick)
stopButton.pack()
# 进入消息循环
top.mainloop()
