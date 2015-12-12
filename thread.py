from threading import Thread

import time

def test(a,b):
	print "Functia test pornita"
	for i in range(1,a):
		b +=1

	print b
	return b

	
def timer(name,delay,repeat):
	print "Timer: " + name + " Started"
	while repeat > 0:
		time.sleep(delay)
		print name + ": " +str(time.ctime(time.time()))
		repeat -=1
	print "Timer: " + name + " Completed"


def Main():
	t1= Thread(target=timer,args=("Timer1",1,5))
	t2= Thread(target=timer,args=("Timer2",2,5))
	t3= Thread(target=test,args=(10,2))
	t3.start()
	t1.start()
	t2.start()
	print "Main Completed"

if __name__ == "__main__":
	Main() 