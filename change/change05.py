#!/usr/bin/env python3
import sys
import getopt
import configparser
from multiprocessing import Process, Queue
from datetime import datetime


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
    t = datetime.now()
    time = datetime.strftime(t, '%Y-%m-%d %H:%M:%S')
    lower = float(config['JiShuL'])
    height = float(config['JiShuH'])
    yanglao = float(config['YangLao'])
    yiliao = float(config['YiLiao'])
    shiye = float(config['ShiYe'])
    gongshang = float(config['GongShang'])
    shengyu = float(config['ShengYu'])
    gongjijin = float(config['GongJiJin'])

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
        result = [tid, tsalary, shebao, geshui, shuihou, time]
        queue2.put(result)


def write(outputfile):
    while queue2.empty() == False:
        dayin = queue2.get()
        result = "{},{},{:.2f},{:.2f},{:.2f},{}".format(dayin[0], dayin[1], dayin[2], dayin[3], dayin[4], dayin[5])
        print(result)
        with open(outputfile, 'a') as afile:
            afile.write(result + '\n')

def usage():
    print("Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata")

cityname = "DEFAULT"
tempconfig = {}

options, args = getopt.getopt(sys.argv[1:], "hC:c:d:o:", ["help"])
for name, value in options:
    if name in ("-h","--help"):
        usage()
    if name in ("-C"):
        cityname = value
    if name in ("-c"):
        configfilePath = value
    if name in ("-d"):
        userdatafilePath = value
    if name in ("-o"):
        outputfilePath = value

conf = configparser.ConfigParser()
conf.read(configfilePath)
options = conf.options(cityname.upper())
tempconfig['JiShuL'] = conf.get(cityname.upper(), 'JiShuL')
tempconfig['JiShuH'] = conf.get(cityname.upper(), 'JiShuH')
tempconfig['YangLao'] = conf.get(cityname.upper(), 'YangLao')
tempconfig['YiLiao'] = conf.get(cityname.upper(), 'YiLiao')
tempconfig['ShiYe'] = conf.get(cityname.upper(), 'ShiYe')
tempconfig['GongShang'] = conf.get(cityname.upper(), 'GongShang')
tempconfig['ShengYu'] = conf.get(cityname.upper(), 'ShengYu')
tempconfig['GongJiJin'] = conf.get(cityname.upper(), 'GongJiJin')



queue1 = Queue()
queue2 = Queue()

p1 = Process(target=read, args=(userdatafilePath,))
p1.start()
p1.join()
p2 = Process(target=claculate, args=(tempconfig,))
p2.start()
p2.join()
p3 = Process(target=write, args=(outputfilePath,))
p3.start()
p3.join()