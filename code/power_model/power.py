import os
import subprocess
import time
import sys
import tracemalloc
def power_calc():
    cmd='perf stat -x, -o cpu_output_1 -p %s sleep 4' % sys.argv[1]
    p=os.system(cmd)

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
    cmd2 = 'python3 predict.py %f,%f,%f,%f,%f,%f,%f,%f ' % (task_clock, context_switch, cpu_migration, page_faults, cycles, instructions, branches, branch_misses)
    p1=os.system(cmd2)

if __name__=='__main__':
    tracemalloc.start()
    power_calc()
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()

#Task Clock, Context-Switches, CPU-migrations, page-faults, cycles, instructions, branches, branch-misses

