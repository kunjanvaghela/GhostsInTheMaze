import os
import subprocess
import sys

# def run_parallel(*functions):
#     '''
#     Run functions in parallel
#     '''
#     from multiprocessing import Process
#     processes = []
#     for function in functions:
#         proc = Process(target=function)
#         proc.start()
#         processes.append(proc)
#     for proc in processes:
#         proc.join()

# ans = os.system("python3 hello.py " + str(1))
# print(ans)
# # os.system("python3 mainAgent2.py " + str(nr_of_ghosts))
# run_parallel(os.system("python3 hello.py " + str(1)), os.system("python3 hello.py " + str(1+100)))

procs = []
for i in range(1,100):
    proc = subprocess.Popen([sys.executable, 'mainAgent2.py', str(i)])
    procs.append(proc)

for proc in procs:
    proc.wait()
