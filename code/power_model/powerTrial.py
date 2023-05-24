import os
import subprocess
import time
import sys
import tracemalloc
import concurrent.futures
import threading

stopProcessing = False

def get_all_pids():
    ps_cmd =  ['ps', '-e', '-o', 'pid']
    out = subprocess.Popen(ps_cmd, stdout = subprocess.PIPE).communicate()[0]
    out = ''.join(map(chr,out))
    out = out.splitlines()
    out.pop(0)
    return out

def perf_run(pid):
    i=0
    
    while(True):
        i+=1
        op_file = 'cpu_output_%s'%(pid)
        cmd='perf stat -x, -o %s -p %s sleep %s' % (op_file, pid, sys.argv[1])
        start_time = time.time()
        p=os.system(cmd)
        end_time = time.time()
        power_thread = threading.Thread(target=power_calc,args=(pid,start_time,end_time,))
        power_thread.start()
    rm(pid)
            
def power_calc(pid,start,end):
    cpu_output = 'cpu_output_%s' %(pid)
    with open(cpu_output) as reader:
        lines = [line.rstrip('\n') for line in reader]
    task_clock=0.0 if (lines[2].split(',')[4]=="<not defined>" or lines[2].split(',')[4]=="") else float(lines[2].split(',')[4])
    context_switch = 0.0 if (lines[3].split(',')[4]=="<not defined>" or lines[3].split(',')[4]=="") else float(lines[3].split(',')[4])
    cpu_migration = 0.0 if (lines[4].split(',')[4]=="<not defined>" or lines[4].split(',')[4]=="") else float(lines[4].split(',')[4])
    page_faults = 0.0 if (lines[5].split(',')[4]=="<not defined>" or lines[5].split(',')[4]=="") else float(lines[5].split(',')[4])
    cycles = 0.0 if (lines[6].split(',')[4]=="<not defined>" or lines[6].split(',')[4]=="") else float(lines[6].split(',')[4])
    instructions =0.0 if (lines[7].split(',')[4]=="<not defined>" or lines[7].split(',')[4]=="") else float( lines[7].split(',')[4])
    branches = 0.0 if (lines[8].split(',')[4]=="<not defined>" or lines[8].split(',')[4]=="") else float(lines[8].split(',')[4])
    branch_misses = 0.0 if (lines[9].split(',')[4]=="<not defined>" or lines[9].split(',')[4]=="") else float(lines[9].split(',')[4])

    lock = threading.Lock()
    lock.acquire()

    cmd2 = ["python3", "predict.py",str(task_clock)+","+str(context_switch)+","+str(cpu_migration)+","+str(page_faults)+","+str(cycles)+","+str(instructions)+","+str(branches)+","+str(branch_misses)]
    p1 = str(subprocess.Popen(cmd2,stdout=subprocess.PIPE).communicate()[0])
    
    with open("power_output2","a") as fp:
        fp.write(str(start)+","+str(end)+","+pid+","+p1[2:-3]+" \n")
    
    lock.release()
    print(str(start)+"-"+str(end)+" for pid:"+pid+" carbon output:" + p1[2:-3])

def rm(pid):
    cmd='sudo rm cpu_output_%s' %(pid)
    os.system(cmd)

if __name__=='__main__':
    pids = get_all_pids()
    
    with open("power_output2","w") as fp:
        fp.write("start_time,end_time,pid,power \n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(pids)) as executor:     
        for i in range(0,len(pids)):
            executor.submit(perf_run,str(pids[i]).strip())
        executor.shutdown()
        
#Task Clock, Context-Switches, CPU-migrations, page-faults, cycles, instructions, branches, branch-misses

