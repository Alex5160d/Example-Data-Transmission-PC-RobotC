#!/usr/bin/env python

from bluetooth import *
import sys

class NXTcontrol:
	def __init__(self):
		"""
		 the connection will be faster if you fill it with the NXT addess
		 And need to be filled if several NXT are used at the same time
		"""
		self.addr = None
		self.uuid = "00001101-0000-1000-8000-00805F9B34FB"
		self.mailbox = 0x00 # mailbox number
		self.sock = self.connect()

	def connect(self):
		service_matches = find_service( uuid = self.uuid, address = self.addr )
		if len(service_matches) == 0:
			print("couldn't find the NXT")
			sys.exit(0)

		first_match = service_matches[0]
		port = first_match["port"]
		name = first_match["name"]
		host = first_match["host"]

		print("connecting to \"%s\" on %s COM%s" % (name, host, port))

		# Create the client socket
		sock = BluetoothSocket( RFCOMM )
		sock.connect((host, port))
		print("connected")
		return sock


	def robotControl(self, *params):
		numParams = len(params)
		if numParams == 0:
			print "At least onemust be given"
			return

		command = bytearray(5 + numParams)

		command[0] = 0x00 # with reply telegram
		command[1] = 0x09 # messagewrite direct command
		command[2] = self.mailbox
		command[3] = numParams + 1 #size of the message (with terminator)
		for i in xrange(numParams):
			if params[i] < 0 or params[i] > 255:
				print params[i], "is not an ubyte"
				return
			command[4 + i] = bytes(chr(params[i]))
		command[4 + numParams] = 0x00

		header = bytearray([0x00, 0x00])
		header[0] = bytes(chr(len(command)))

		command = buffer(command, 0, len(command))
		header = buffer(header, 0, len(header))

		self.sock.send(header)
		self.sock.send(command)
		length = ord(self.sock.recv(1)) + 256*ord(self.sock.recv(1)) # get the reply size

		for i in xrange(length): # get the reply
			self.sock.recv(1)





