# Domoticz API
# https://www.domoticz.com/wiki/Domoticz_API/JSON_URL%27s

import re
import uuid  
import urllib2
import urllib
import json

"""
server_prefix="http://"
server_ip="http://192.168.0.115"
server_port="8080"
server_page="json.htm?"
CompleteServerUrl= server_prefix + server_ip + ":" + server_port + "/" + server_page
"""
# pydict = {'list': [{'k1': '60411', 'k2': 'val'}], 'Id': '775'}
# jsondata = json.dumps(pydict)
# postreq = urllib2.Request(_url, jsondata)
# postreq.add_header('Content-Type', 'application/json')
# resp = urllib2.urlopen(postreq)
# print "resp:", resp.read()

class client(object):
	def __init__(self):
		
		self.server_prefix="http://"
		self.server_ip="192.168.0.115"
		self.server_port="8080"
		self.server_page="json.htm?"
		self.CompleteServerUrl= self.server_prefix + self.server_ip + ":" + self.server_port + "/" + self.server_page
		self.data = {}
		self.response=""
		print "init"

		# Form a unique deviceName based on a mac adress
	
	def makeDeviceName(self):
		DeviceID = ''.join(re.findall('..', '%012x' % uuid.getnode()))
		return DeviceID
		
	def putToggle(self,idx):
		self.data['type']="command"
		self.data['param']="switchlight"
		self.data['idx']=idx
		self.data['switchcmd']="Toggle"
		MyResponse=self.MakeJsonCall()
		return MyResponse
	 
		# Check in the existing installation if the Hardware exists
	def getDevices(self):
		self.data['type']="devices"
		#self.data['filter']="all"
		self.data['filter']="temp"
		self.data['used']="true"
		self.data['order']="Name"
		MyResponse=self.MakeJsonCall()
		return MyResponse
	
		# Register the Hardware against the server
	def RegisterHardware(self):
		
		
		data['type'] = "command"
		data['param'] = "addhardware"
		data['htype']=15
		data['port']=1
		data['name']=self.MyDeviceName
		data['enabeld']="true"

		# Make the JsonCall and evaluate the result and/or catch the fault	
		response = NextionTest1(data)
		
		#afterward to get the id, either you have your last created id from an index you maintain or sort the hardware page for last ID: 
		#/json.htm?type=hardware
		data['type'] = "hardware"
		
		response = NextionTest1(data)

		return MyDeviceIdx
		
		# make a JsonCall and return the data
	def MakeJsonCall(self):
		#print (self.CompleteServerUrl)
		JsonData = json.dumps(self.data)
		JsonData = urllib.urlencode(self.data)
		#print(self.CompleteServerUrl)
		print self.data ,JsonData
		postreq = urllib2.Request(self.CompleteServerUrl + JsonData,headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
		f = urllib2.urlopen(postreq)
		response = json.loads(f.read())
		return response
