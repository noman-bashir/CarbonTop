import sys
for line in reversed(list(open("/nfs/obelix/users2/smritidas/CarbonTop/code/power_model/power_output2"))):
    l=line.rstrip()
    if(l.split(',')[2]==sys.argv[1]):
        print(l.split(',')[3])
        break
