#coding:utf-8

# 导入GPIO控制薄块
import RPi.GPIO as GPIO
# 设置使用的引脚编码模式
GPIO.setmode(GPIO.BOARD)
# 定义震动开关引脚 BCM5
swi_shake = 29
# 定义倾斜开关引脚 BCM6
swi_slop = 31
# Define red light pin
red = 12
# Define green light pin
green = 35

# 进行开关引脚的初始化，设置为输入引脚，且默认为高电平
GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(swi_shake, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(swi_slop, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 定义状态变化的回调函数
def switch_shake(channel):
	# 低电平为开关打开状态
	if not GPIO.input(channel):
		print("注意，发生了震动！")
		GPIO.output(red,GPIO.HIGH)
		GPIO.output(green,GPIO.LOW)
def switch_slop(channel):
	# 低电平为开关打开状态
	if not GPIO.input(channel):
		print("注意，发生了倾斜！")
		GPIO.output(green,GPIO.HIGH)
		GPIO.output(red,GPIO.LOW)
# 添加输入引脚电平变化的回调函数
GPIO.add_event_detect(swi_shake, GPIO.FALLING, callback=switch_shake, bouncetime=200)
GPIO.add_event_detect(swi_slop, GPIO.FALLING, callback=switch_slop, bouncetime=200)

while True:
	pass