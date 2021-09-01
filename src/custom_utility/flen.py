from statistics import *
import subprocess, shlex

def get_line_lengths():
     cmd = 'wc -l  ../[a-z0-2]*.pdf'
     out = subprocess.check_output(
          cmd, shell=True).decode('utf-8')
     print(out) 
     #subprocess.run()
     for l,line  in enumerate(out.splitlines()):
          parts = line.split()
          print(l, ":  ",  line)
          if parts[0].strip().lower() == 'total':
               break
          nlines = int(parts[0].strip())
          if not nlines:
               continue # пропустить пустые файлы
     yield (nlines, parts[-1].strip())
#subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
data = list(get_line_lengths())
lengths = [d[0] for d in data]
sample = lengths[::2]

print("Basic statistics:")
print(' count: {:3d}'.format(len(lengths)))
print(" min : {:6.2f}".format(min(lengths)))
print(' max : {:6.2f}'.format(max(lengths)))
print(' mean : {:6.2f}'.format(mean(lengths)))
print('\nPopulation variance:')
print(' pstdev : {:6.2f}'.format(pstdev(lengths)))
print(' pvariance : {:6.2f}'.format(pvariance(lengths)))