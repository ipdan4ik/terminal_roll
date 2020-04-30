from numpy import random
import re
import sys
import time
import curses

data = []
prob = []

if len(sys.argv) > 2:
    print('Too many arguments!')
    sys.exit()
if len(sys.argv) == 1:
    print('Too few arguments!')
    sys.exit()
in_file = sys.argv[1]
if_none = 0
with open(in_file, 'r') as f:
    for line in f:
        x = re.search(r'\[.+\]', line)
        if x is None:
            prob.append(0.1)
            data.append(line)
            if_none += 1
        else:
            y = line[x.end():-1]
            prob.append(float(line[x.start()+1:x.end()-1]))
            data.append(y)

final_data = []
for i, j in zip(data, prob):
    final_data += [i for x in range(int(j*10))]
random.shuffle(final_data)
for i in range(4):
    final_data.append(final_data[i])

start_time = time.time()
n = random.randint(5, 10)
previous_slowdown = start_time
slowdown = 0.2
i = 1

curse = curses.initscr()
curses.noecho()
curses.cbreak()

while time.time() < start_time + n:
    if i < len(final_data)-3:
        i += 1
    else:
        i = 2
    visible_data = ['  '*(abs(x-i)) + final_data[x] for x in range(i - 2, i + 3)]
    now_time = time.time()
    for k in range(5):
        curse.addstr(k, 0, visible_data[k] + ' '*(50-len(final_data[k])))
    curse.refresh()
    if now_time >= previous_slowdown + n/5:
        slowdown += 0.1
        previous_slowdown += n/5
    time.sleep(slowdown)


visible_data = []
for x in range(i-2, i+3):
    visible_data.append('  '*(abs(x-i)) + final_data[x] + ' '*(50-len(final_data[x])))

for x in range(i-2, i):
    curse.addstr(x-i+2, 0, '  '*(abs(x-i)) + final_data[x] + ' '*(50-len(final_data[x])))
curse.addstr(2, 0, final_data[x] + ' <<<' + ' '*(50-len(final_data[x])), curses.A_BOLD)
curse.addstr(2, 50, '<Press any key..>')
for x in range(i+1, i+3):
    curse.addstr(x-i+2, 0, '  '*(abs(x-i)) + final_data[x] + ' '*(50-len(final_data[x])))
curse.refresh()

curses.echo()
curses.nocbreak()
curse.getkey()
curses.endwin()
