import sys,time
def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    progress_x=0
    x=0
    sys.stdout.write("#" * (x - progress_x))
   #  sys.stdout.write("king ming")
    sys.stdout.flush()
    progress_x = x

def endProgress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()


# startProgress("king ")

for x in range(10):
    print(f'{x}\r', end="")
    time.sleep(1)
print()