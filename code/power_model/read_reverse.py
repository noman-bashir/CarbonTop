import sys
import os
from datetime import datetime
import time


path = os.getcwd()
power = True
energy = True
no_time_passed = True
pid = 1
start_time = 0
end_time = time.time()
total_power = 0
total_energy = 0

inputArgs = sys.argv
i = 1

while i < len(inputArgs):
    
    if inputArgs[i] == '-pid':
        i += 1
        pid = inputArgs[i]
    elif inputArgs[i] == '-p':
        i += 1
        power = True if inputArgs[i] == 'True' else False
    elif inputArgs[i] == '-e':
        i += 1
        energy = True if inputArgs[i] == 'True' else False
    elif inputArgs[i] == '-st':
        no_time_passed = False
        i += 1
        start_time = (datetime.strptime(inputArgs[i], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.fromtimestamp(0)).total_seconds()
    elif inputArgs[i] == '-et':
        no_time_passed = False
        i += 1
        end_time = (datetime.strptime(inputArgs[i], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.fromtimestamp(0)).total_seconds()
    elif inputArgs[i] == '-m':
        no_time_passed = False
        i += 1
        start_time = time.time() - float(inputArgs[i])*60
    i += 1

if start_time == 0:
    if os.path.isdir('/proc/{}'.format(pid)):
        for line in reversed(list(open("power_output2"))):
            l = line.rstrip().split(',')
            if l[2] == pid and (no_time_passed == True or float(l[1]) <= end_time):
                if power == True:
                    print('power -' + l[3])
                if energy == True:
                    print('energy -' + l[4])
                break
    else:
        print("process is not running currently")
else:    
    for line in reversed(list(open("power_output2"))):
        l=line.rstrip().split(',')
    
        if l[2]==pid:
            if float(l[1]) < start_time:
               break
            if (float(l[0]) >= start_time or float(l[1]) >= start_time) and (float(l[1]) <= end_time or float(l[0]) <= end_time):
                if power == True:
                    total_power += float(l[3])
                if energy == True:
                    total_energy += float(l[4])

    if power == True:
        print("total power : " + str(total_power))
    if energy == True:
        print("total energy : " + str(total_energy))
