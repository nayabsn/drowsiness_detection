import os
import subprocess

def launch_subprocess(command):
    global p
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def sh(print_msg=True):
    
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.rstrip()
        line = line.decode('utf8')
        line = str(line)
        line = line[39:41]
        if line != "sf":
            line = "0x"+line
            line = int(line,0)
        else:
            continue
        if print_msg:
            #print(">>>", line)
            break
        lines.append(line)
    return line

launch_subprocess('''gatttool -t random -b F2:BD:B3:70:9E:6A --char-write-req --handle=0x0011 --value=0100 --listen''')

while True:
    rrr = sh()
    print("BPM:", rrr)
