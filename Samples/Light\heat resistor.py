#coding:utf-8

#SMBus (System Management Bus,系统管理总线) 
import smbus   #在程序中导入“smbus”模块
import RPi.GPIO as GPIO 
import time

bus = smbus.SMBus(1)         #创建一个smbus实例


# 通过PCF8591读取模拟信号

# 数据亮度的模拟数据
def readLight():
    #发送一个控制字节到设备 表示要读取AIN0通道的数据
    bus.write_byte(0x48,0x40)   
    bus.read_byte(0x48)         # 空读一次，消费掉无效数据
    return bus.read_byte(0x48)  # 返回某通道输入的模拟值A/D转换后的数字值

def readTemperature():
	#发送一个控制字节到设备 表示要读取AIN1通道的数据
    bus.write_byte(0x48,0x41)   
    bus.read_byte(0x48)         # 空读一次，消费掉无效数据
    return bus.read_byte(0x48)  # 返回某通道输入的模拟值A/D转换后的数字值

# 通过GPIO读取数字信号

# 设置使用的引脚编码模式
GPIO.setmode(GPIO.BOARD)
# 光敏模块的数字输出引脚 BCM 17
LP = 11
# 热敏模块的数字输出引脚 BCM 18
TP = 12
# 引脚初始化
GPIO.setup(LP, GPIO.IN)
GPIO.setup(TP, GPIO.IN)

while True:
	print('--------分割线----------')
	print('亮度数字信号：', GPIO.input(LP))
	print('亮度模拟信号：', readLight())
	print('温度数字信号：', GPIO.input(TP))
	print('温度模拟信号：', readTemperature())
	time.sleep(2)