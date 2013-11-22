import requests
import psutil
import time
import datetime
import math

SERVER_NAME = "testserver"
REPORT_TIME = 150
URL ="http://mediadev2.fiu.edu:666/"

def run():
	
	while 1:
		netstart = psutil.net_io_counters().bytes_sent
		cpu = psutil.cpu_percent(interval=1)
		memory = psutil.virtual_memory().percent
		netend = psutil.net_io_counters().bytes_sent
		time.sleep(1)
		network = (netend - netstart) * (7.62939 * math.pow(10,-6))
		
		try:
			r = requests.get( URL + "?name=" + SERVER_NAME + "&memory=" + str(memory) +"&cpu="+ str(cpu) +"&network=" + str(network))
			ts = time.time()
			realtime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			if(r.status_code == 200):
				print "Updated : CPU MEMORY NETWORK " + str(cpu) + " " + str(memory) + " " + str(network) + " at " + realtime
			else:
				print "network error unable to send data at " + realtime
			time.sleep(REPORT_TIME)
		except:
			print "Exception happened, lets roll out in a few seconds."
			time.sleep(20)

if __name__ == '__main__':
	run()
