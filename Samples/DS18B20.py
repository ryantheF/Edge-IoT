"""This sensor is available using 1-wire communication.
It reads the temperature immediately after connecting with the device.
You may find the output data in the device_file diretory.
We use this python program to give a straightforward output that everyone can understand.
"""

import os,time
# 传感器编号
name = "28-3ce1e380385a"
# 设备记录数据的文件地址
device_file ='/sys/bus/w1/devices/' + name + '/w1_slave'

# 读取文件数据
def read_temp_raw():
    f = open(device_file,'r')
    lines = f.readlines()
    f.close()
    return lines

# 解析温度数据
def read_temp():
    lines = read_temp_raw()
    # 此行默认不是'YES' 表明未读取到有效数据
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        # 循环继续读
        lines = read_temp_raw()
    # 找到第2行的't='的位置
    equals_pos = lines[1].find('t=')
    # 将温度数据取出
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0
    return temp_c

while True:
    print('%fC'%read_temp())
    time.sleep(1)