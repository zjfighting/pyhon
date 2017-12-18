#!/usr/bin/env python3
import sys
from multiprocessing import Process, Queue

class Config():
    def __init__(self, configfile):
        self.config = configfile

    def get_config(self):
        return self.config

def getgeshui(number):
    if number < 0:
        geshui = 0.00
    elif number >= 0 and number < 1500:
        geshui = number * 0.03
    elif number >= 1500 and number < 4500:
        geshui = number * 0.1 - 105
    elif number >= 4500 and number < 9000:
        geshui = number * 0.2 - 555
    elif number >= 9000 and number < 35000:
        geshui = number * 0.25 - 1005
    elif number >= 35000 and number < 55000:
        geshui = number * 0.3 - 2755
    elif number >= 55000 and number < 80000:
        geshui = number * 0.35 - 5505
    elif number > 80000:
        geshui = number * 0.45 - 13505
    return geshui

def read(userdatafilePath):
    with open(userdatafilePath) as file:
        for line in file:
            result = line.split(',')
            id = int(result[0])
            salary = int(result[1])
            gongzi = [id, salary]
            queue1.put(gongzi)

def claculate(config):
    lower = config['JiShuL']
    height = config['JiShuH']
    yanglao = config['YangLao']
    yiliao = config['YiLiao']
    shiye = config['ShiYe']
    gongshang = config['GongShang']
    shengyu = config['ShengYu']
    gongjijin = config['GongJiJin']

    while queue1.empty() == False:
        tempgongzi = queue1.get()
        tid = tempgongzi[0]
        tsalary = tempgongzi[1]
        print("{}::{}".format(tid,tsalary))
        if tsalary < lower:
            shebao = lower * (yanglao + yiliao + shiye + gongshang + shengyu + gongjijin)
        elif tsalary >= lower and tsalary <= height:
            shebao = tsalary * (yanglao + yiliao + shiye + gongshang + shengyu + gongjijin)
        elif tsalary > height:
            shebao = height * (yanglao + yiliao + shiye + gongshang + shengyu + gongjijin)
        geshui = getgeshui(tsalary - shebao - 3500)
        shuihou = tsalary - shebao - geshui
        result = [tid, tsalary, shebao, geshui, shuihou]
        queue2.put(result)


def write(outputfile):
    while queue2.empty() == False:
        dayin = queue2.get()
        result = "{},{},{:.2f},{:.2f},{:.2f}".format(dayin[0], dayin[1], dayin[2], dayin[3], dayin[4])
        print(result)
        with open(outputfile, 'a') as afile:
            afile.write(result + '\n')


configfile = {}

args = sys.argv[1:]

index = args.index('-c')
configfilePath = args[index + 1]
index = args.index('-d')
userdatafilePath = args[index + 1]
index = args.index('-o')
outputfilePath = args[index + 1]

with open(configfilePath) as file:
    for line in file:
        line.strip()
        result = line.split('=')
        configfile[result[0].strip()] = float(result[1].strip())

config = Config(configfile)

queue1 = Queue()
queue2 = Queue()


p1 = Process(target=read, args=(userdatafilePath,))
p1.start()
p1.join()
p2 = Process(target=claculate, args=(config.get_config(),))
p2.start()
p2.join()
p3 = Process(target=write, args=(outputfilePath,))
p3.start()
p3.join()


