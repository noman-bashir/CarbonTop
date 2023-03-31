import os
import subprocess
import time
import sys
import tracemalloc
import threading
def get_all_pids():
    ps_cmd =  ['ps', '-e', '-o', 'pid']
    out = subprocess.Popen(ps_cmd, stdout = subprocess.PIPE).communicate()[0]
    out = ''.join(map(chr,out))
    out = out.splitlines()
    out.pop(0)
    return out

def perf_run(pid):
    print("perf_start:"+str(time.time()))
    cmd='perf stat -x, -o cpu_output_1 -p %s sleep %s' % (str(pid), sys.argv[1])
    p=os.system(cmd)
    print("perf_end:"+str(time.time()))

def power_calc():
    print("power_start: "+str(time.time()))
    with open('cpu_output_1') as reader:
        lines = [line.rstrip('\n') for line in reader]
    task_clock=float(lines[2].split(',')[4])
    context_switch = float(lines[3].split(',')[4])
    cpu_migration = float(lines[4].split(',')[4])
    page_faults = float(lines[5].split(',')[4])
    cycles = float(lines[6].split(',')[4])
    instructions =float( lines[7].split(',')[4])
    branches = float(lines[8].split(',')[4])
    branch_misses = float(lines[9].split(',')[4])
    cmd2 = 'python3 predict.py %f,%f,%f,%f,%f,%f,%f,%f >> power_output ' % (task_clock, context_switch, cpu_migration, page_faults, cycles, instructions, branches, branch_misses)
    p1=os.system(cmd2)
    print("power_end: "+ str(time.time()))

if __name__=='__main__':
    start_time = time.time()
    #tracemalloc.start()
    #i=0;
    pids = get_all_pids()
    for pid in pids:
        perf = threading.Thread(target=perf_run, args=(pid,))
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

