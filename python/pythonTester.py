import math
import random
list = []
x = []
for i in range(5):
	x.append(random.randrange(5))
	
list.append(x)

x = []
for i in range(5):
	x.append(random.randrange(10) + 5 )
	
list.append(x)

print list

list = zip(*list)
print list
list.sort()
print list