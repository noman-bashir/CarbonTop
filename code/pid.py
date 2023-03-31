import subprocess
import re

# Return a list of all processes in /proc
def getAllPids():
    psCmd = ['ps', '-e', '-o', 'pid']
    out = subprocess.Popen(psCmd, stdout=subprocess.PIPE).communicate()[0]
    out = ''.join(map(chr,out))
    print("out",type(out))
    out=out.splitlines()
    out.pop(0)
    return out

# Return a dictionary mapping process IDs to container names
def getContProcs():
    pids = getAllPids()
    groupMapping = {}
    print("pids:",pids[0])
    for pid in pids:
        pid=pid.strip()
        print("pid:",str(pid))
        cat = ["cat", "/proc/"+str(pid)+"/cgroup"]
        catOut = str(subprocess.Popen(cat, stdout=subprocess.PIPE).communicate()[0])
        print("catOut",catOut)
        group = re.findall(r"memory", str(catOut))[0]

        groupMapping[pid] = group
    
    return groupMapping

if __name__ == "__main__":
    # getAllPids()

    getContProcs()

    pass
