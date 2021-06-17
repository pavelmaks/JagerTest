import re
import time

s = "1537,2.5,10,22,50,10"
start_time = time.time()
time.sleep(30)

nums = re.findall(r'\d*\.\d+|\d+', s)

nums = [float(i) for i in nums]

print(start_time-time.time())