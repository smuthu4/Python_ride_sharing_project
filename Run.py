import Trips
from time import time
minutes = int(raw_input("Window size (minutes) to run this algorithm:  "))
seconds = minutes*60
start = time()
Trips.get_all(seconds)
end = time()
diff = end - start
m, s = divmod(diff, 60)
h, m = divmod(m, 60)
print "Time taken for algorithm is %d:%02d:%02d" % (h, m, s)


