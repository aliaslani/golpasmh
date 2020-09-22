import subprocess
import time
import sys

if __name__ == "__main__":
    
    proc = subprocess.Popen(['python3', 'test2.py'])
    print ("start process with pid %s" % proc.pid)
    time.sleep(50)
    # kill after 50 seconds if process didn't finish
    if proc.poll() is None:
        print ("Killing process %s with pid %s " % (to_run,proc.pid))
        proc.kill()