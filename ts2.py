from json import load
import subprocess
x = 'start chrome https://www.youtube.com '

d = x.split()
subprocess.run(d,shell=True)
print()