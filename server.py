import redis
import tornado.ioloop
import tornado.web
import xml.etree.cElementTree as etree
import json 

_host = "127.0.0.1"
_port = 6379
_db = 0
_r = None
enable_white_list = False
whitelist = ["131.94.19.25"]

class putdata(tornado.web.RequestHandler):
	#responses are sent in json
	def get(self):
		self.set_header("Content-Type", "application/json")
		#if we don't have all the variables send back an error		
		try:
			name = self.get_argument("name")
			cpu = self.get_argument("cpu")
			network = self.get_argument("network")
			memory = self.get_argument("memory")	
		except:
			self.write(json.dumps({"status": "error, invalid input"}))
			return
		#check if an ip is in the white list
		if enable_white_list:
			keepgoing = False
			for ip in whitelist:
				if ip == self.request.remote_ip:
					keepgoing = True
			if keepgoing:
				print "passed!"
			else:
				self.write(json.dumps({"status": "error, invalid user!"}))
				return
		#send data to redis and log results			 	
		_r.set(name, memory+";"+cpu+";"+network+";")
		self.write(json.dumps({"status": "ok"}))
		print(name +": Memory " + memory+"; Cpu "+cpu+"; Network "+network+"; from ip " + self.request.remote_ip)

class getdata(tornado.web.RequestHandler):
	def get(self):
		keys = _r.keys()
		root = etree.Element("root")

		for key in keys:
			datastr = _r.get(key)
			data = datastr.split(";")
			
			if len(data) == 4:
				infonode = etree.SubElement(root, key)
				memorynode = etree.SubElement(infonode, "memory")
				memorynode.text = data[0]
				cpunode = etree.SubElement(infonode,"cpu")
				cpunode.text = data[1]
				networknode= etree.SubElement(infonode, "network")
				networknode.text = data[2]
			else:
				pass				 
	
		self.set_header("Content-Type", "text/xml")		
		self.write(etree.tostring(root))
		print(etree.tostring(root))
		
application = tornado.web.Application([
	(r"/", putdata),
	(r"/getdata", getdata),
])

def connection():
	_r = redis.StrictRedis(host=_host, port=_port, db=_db)
	return _r

if __name__ == '__main__':
	_r = connection()
	application.listen(666)
	tornado.ioloop.IOLoop.instance().start()

