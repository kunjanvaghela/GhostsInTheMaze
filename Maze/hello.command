#!/usr/bin/env python

import sys
import time

st = time.time()
res = sys.argv[1]
time.sleep(int(sys.argv[1]))
et = time.time() - st
print("Hello " + res + str(et))
