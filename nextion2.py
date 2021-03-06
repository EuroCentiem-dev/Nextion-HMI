#
#https://wiki.itead.cc/wiki/Nextion_Instruction_Set
#
import sys
import time
from threading import Thread
import socket
import domoticz.client

CRLF = '\r\n'


class nextion():

	ERRORS={
		"00": "Invalid instruction",
		"01": "Successful execution of instruction",
		"02": "Component ID invalid",
		"03": "Page ID invalid",
		"04": "Picture ID invalid",
		"05": "Font ID invalid",
		"11": "Baud rate setting invalid",
		"12": "Curve control ID number or channel number is invalid",
		"1a": "Variable name invalid",
		"1b": "Variable operation invalid"
		}

	MESSAGES={
		"65": "Touch event return data",
		"66": "Current page ID number returns"
		}

	RED   =63488
	BLUE  =31
	GRAY  =33840
	BLACK =0
	WHITE =65535
	GREEN =2016	
	BROWN =48192
	YELLOW=65504
	
	def __init__(self,sock, pageDefinitions=None):
		self.name='mine'
		print 'initialized'
		self.sock = sock
		#while True:
			#try:
				#self.setBkCmd(3)
				#break
			#except:
				#print "Wait..."
				#time.sleep(1)
#  
#  name: nextion.nxRead
#  @param: 	command (string to be processsed
#  @return	data array of events
#  
	def nxAnalyze(self,command):
		
		print 'my module will process' , command
		r = command
		#r = r.encode("hex")
#		print 'encoded is this', r
		a = r.split('ffffff')
		data=[]
		for elem in a:
			d = dict(EventName="",EventID='',PageID='',ComponentID="",Event="",X="", Y=0)
			#print elem[0:2]
			if elem[0:2] == "65":
				# 0x65 + PageID + ComponentID + TouchEvent + END
				d["EventName"]="Touchevent"
				d["EventID"]=elem[0:2]
				d["PageID"]=elem[2:4]
				d["ComponentID"]=elem[4:6]
				d["Event"]=elem[6:8]
				d["X"]=''
				d["Y"]=''
				data.append(d)
				
			if elem[0:2] == "66":
				# 0x66 + PageID + END
				d["EventName"]="Pageevent"
				d["EventID"]=elem[0:2]
				d["PageID"]=elem[2:4]
				d["ComponentID"]=''
				d["Event"]=''
				d["X"]=''
				d["Y"]=''
				data.append(d)

				
			if elem[0:2] == "67":
				# 0x67 + PageID + X High + X Low + +Y High + Y Low + Evebt state + END
				d["EventName"]="Touch Coordinate"
				d["EventID"]=elem[0:2]
				d["PageID"]=elem[2:4]
				d["ComponentID"]=''
				d["Event"]=''
				d["X"]=elem[4:8]
				d["Y"]=elem[8:12]
				data.append(d)

			if elem[0:2] == "68":
				# 0x68 + PageID + X High + X Low + +Y High + Y Low + Evebt state + END
				d["EventName"]="Touch Event in sleep mode"
				d["EventID"]=elem[0:2]
				d["PageID"]=elem[2:4]
				d["ComponentID"]=''
				d["Event"]=''
				d["X"]=elem[4:8]
				d["Y"]=elem[8:12]
				data.append(d)
				
			
		return data

	def nxRead(self,cmax=100,timeout=0):
		s=''
		t=''
		LF=chr(255)
		self.command=''
		#LF.encode('hex')
		done=False
		print "reading"
		data=''
		message=''
		time_now = time.clock()
		def _reader():

			import select
			count=0
			command=''
			print "reader"
			time_now = time.clock()
			#Dummy data also disable data = sock.recv(512)
			#data2 = '65001701'
			#data2.decode('hex')
			#print data2.decode('hex')+ chr(255) + chr(255) + chr(255) + CRLF
			#data = data2.decode('hex')+ chr(255) + chr(255) + chr(255) + CRLF
			s=''
			while timeout==0 or (time.clock()-time_now)<timeout:
				time_now = time.clock()
				print >>sys.stderr, 'waiting for data ...'
				ready = select.select([sock],[],[],1)
				if ready[0]:
					data = sock.recv(1)
				else:
					continue

				if data is None or data=="":
					print >>sys.stderr, 'data is empty'
					continue

				c = ord(data)
				print >>sys.stderr, 'encode data',data.encode('hex')
				print >>sys.stderr, 'message c',c
				
				#if c==0xff and len(s)==0:
					#continue

				if True:
					
					s += data
					message = s.encode('hex')
					print >>sys.stderr, 'encode message data',message
					print >>sys.stderr, 'encode s data',s
					print >>sys.stderr, 'message ', message.find('ffffff')
					
					if message.find('ffffff') > 0:
						self.command = message[:message.find('ffffff')+6]
						rightstring = message[message.find('ffffff')+6:] 
						if len(rightstring) ==0:
							s=''
							print >>sys.stderr, 'Command 176 ', self.command, 'leftover',rightstring
							return 
			return self.command
			print >>sys.stderr, 'Command 178 ', self.command
		
		#print "180",self.command
		t = Thread(target=_reader)
		t.start()
		t.join()
		return self.command
		
	def setText(self,id,value):
		s =self.nxWrite(id+'.txt="'+str(value)+'"')
		print >>sys.stderr, 'code recieved "%s"' % s
		print >>sys.stderr, 'code recieved @ setText"%s"' % s[:2]
		#if s[:2]!='01' and len(s) == 8 and s!=None:
			##raise ValueError(nextion.getErrorMessage(s[0])+": id: "+id+" text:"+ value)
			#print >>sys.stderr, nextion.getErrorMessage(s[:2])+": id: "+id+" text:"+ value
			#return
			##raise ValueError(nextion.getErrorMessage(s[:2])+": id: "+id+" text:"+ value)
		#else:
			#return s
		return
			
	def drawCircle(self,x,y,r,color):
		s=self.nxWrite('cir %s,%s,%s,%s' % (x,y,r,color))
		#if s[0]!=0x01:
			#raise ValueError(nextion.getErrorMessage(s[0]))

	@staticmethod
	def getErrorMessage(s):
		return nextion.ERRORS[s]
		

	def nxWrite(self,s):
		s =    s+chr(255) + chr(255) + chr(255) 
		print >>sys.stderr, 'sending "%s"' % s
		sock.send(s)
		data = self.nxRead(s)
		print data
		return data

	def nxWait(self):
		return 'wait'
		

if __name__ == "__main__":
	
	cnx={}
	with open('test2.txt','r') as f:
		for line in f:
			key,val=line.split()
			cnx[key]=val
	print cnx
	
	#
	# Put all variables to 
	#
	
	server_ip =cnx['EspEasy_ip']
	server_port =cnx['EspEasy_port']
	

	def get_constants(prefix):
		"""Create a dictionary mapping socket module constants to their names."""
		return dict( (getattr(socket, n), n)
			for n in dir(socket)
			if n.startswith(prefix)
			)

	families = get_constants('AF_')
	types = get_constants('SOCK_')
	protocols = get_constants('IPPROTO_')

	# Create a TCP/IP socket
	sock = socket.create_connection((server_ip, server_port))
	sock.settimeout(1.0)

	print >>sys.stderr, 'Family  :', families[sock.family]
	print >>sys.stderr, 'Type    :', types[sock.type]
	print >>sys.stderr, 'Protocol:', protocols[sock.proto]
	print >>sys.stderr
	

	nextion_client = nextion(sock)
	dmz = domoticz.client.client()
	#Create a unique Name
	

	#load configuration from domoticz
	AllDevices = dmz.getDevices()
	
	#print AllDevices['Sunrise']
	#print AllDevices['sunrise']
	#print AllDevices['sunset']
	#print AllDevices
	
	#MijnBericht = nextion_client.setText('Sunrise',AllDevices['Sunrise'])
	#MijnBericht = nextion_client.setText('Sunset',AllDevices['Sunset'])
	while True:

		MijnBericht = nextion_client.nxRead()
		print "*** Jumping to main" 
		print MijnBericht
		MijnData = nextion_client.nxAnalyze(MijnBericht)
		print "***"
		print MijnData
		Event = MijnData[0]
		if Event['EventID']=='65':
			print 'touch gevonden'
			dmz_command=Event['EventID']+ Event['PageID']+ Event['ComponentID']
			print dmz_command
			if dmz_command in cnx:
				dmz.putToggle(cnx[dmz_command])
				
