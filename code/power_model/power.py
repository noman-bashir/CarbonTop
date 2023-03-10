import os
import subprocess
import time
import sys
import tracemalloc
import threading
def perf_run():
    print("perf_start:"+str(time.time()))
    cmd='perf stat -x, -o cpu_output_1 -p %s sleep %s' % (sys.argv[1], sys.argv[2])
    p=os.system(cmd)
    print("perf_end:"+str(time.time()))

def power_calc():
    print("power_start: "+str(time.time()))
    with open('cpu_output_1') as reader:
        lines = [line.rstrip('\n') for line in reader]
    task_clock=float(lines[2].split(',')[0])
    context_switch = float(lines[3].split(',')[0])
    cpu_migration = float(lines[4].split(',')[0])
    page_faults = float(lines[5].split(',')[0])
    cycles = float(lines[6].split(',')[0])
    instructions =float( lines[7].split(',')[0])
    branches = float(lines[8].split(',')[0])
    branch_misses = float(lines[9].split(',')[0])
    cmd2 = 'python3 predict.py %f,%f,%f,%f,%f,%f,%f,%f >> power_output ' % (task_clock, context_switch, cpu_migration, page_faults, cycles, instructions, branches, branch_misses)
    p1=os.system(cmd2)
    print("power_end: "+ str(time.time()))

if __name__=='__main__':
    start_time = time.time()
    #tracemalloc.start()
    i=0;
    while(i<5):
        i+=1
        perf = threading.Thread(target=perf_run)
        perf.start()
        power = threading.Thread(target=power_calc)
        
        perf.join()
        power.start()
        

    #print(tracemalloc.get_traced_memory())
    #tracemalloc.stop()
    total_time = time.time() - start_time
    print(total_time)
    power.join()
#Task Clock, Context-Switches, CPU-migrations, page-faults, cycles, instructions, branches, branch-misses

