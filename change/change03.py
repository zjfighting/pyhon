#!/usr/bin/env python3
import sys
import os

class Config():
    def __init__(self, configfile):
        self.config = configfile

    def get_config(self):
        return self.config

class UserData():
    shebao = 0.00
    geshui = 0.00
    shuihou = 0.00

    def __init__(self, tid, tsalary, tconfig):
        self.id = tid
        self.salary = tsalary
        self.config = tconfig

    def calculator(self):
        lower = self.config['JiShuL']
        height = self.config['JiShuH']
        yanglao = self.config['YangLao']
        yiliao = self.config['YiLiao']
        shiye = self.config['ShiYe']
        gongshang = self.config['GongShang']
        shengyu = self.config['ShengYu']
        gongjijin = self.config['GongJiJin']
        if self.salary < lower:
            self.shebao = lower * (yanglao + yiliao + shiye + gongshang + shengyu + gongjijin)
        elif self.salary >= lower and salary <= height:
            self.shebao = self.salary * (yanglao + yiliao + shiye + gongshang + shengyu + gongjijin)
        elif salary > height:
            self.shebao = height * (yanglao + yiliao + shiye + gongshang + shengyu + gongjijin)
        self.geshui = get(self.salary - self.shebao - 3500)
        self.shuihou = self.salary - self.shebao - self.geshui

    def dumptofile(self, outputfile):
        result = "{},{},{:.2f},{:.2f},{:.2f}".format(self.id, self.salary, self.shebao, self.geshui, self.shuihou)
        with open(outputfile, 'a') as afile:
            afile.write(result)

def get(number):
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


configfile = {}
userdatafile = {}

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

with open(userdatafilePath) as file:
    for line in file:
        result = line.split(',')
        id = int(result[0])
        salary = int(result[1])
        userdatafile[id] = salary

userdata=[]

for key, value in userdatafile.items():
    user = UserData(key, value, config.get_config())
    userdata.append(user)

for user in userdata:
    user.calculator()
    user.dumptofile(outputfilePath)