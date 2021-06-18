import os
import subprocess

def sh(command, print_msg=True):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
            print(">>>", line)
        lines.append(line)
    return lines
  
print('run():')
sh('''
gatttool -t random -b F2:BD:B3:70:9E:6A --char-write-req --handle=0x0011 --value=0100 --listen
''')
