### etrex class - to provide helper function for interfaceing to 
### garmin etrex handheld gps with serial interface

import serial


class Waypoint:
	def __init__(self, packet):
		self.data=packet
		
	## return an int for the symbol	
	def symbol(self):
		return int(self.data[8]+self.data[7],16)
		
	## return the text name of the waypoint	
	def name(self):
		nstr=""
		for n in self.data[51:61]:
			if n=='00':
				break
			nstr=nstr+n
		name=bytes.fromhex(nstr).decode('utf-8')
		return name.split('\0')[0]

	#return a float for the latitdue of the waypoint
	def lat(self):
		msb=bytes.fromhex(" ".join(self.data[30:31]))
		msb=int.from_bytes(msb, byteorder="little")		
		
		lb=bytes.fromhex(" ".join(self.data[27:31]))
		ss=int.from_bytes(lb, byteorder="little")

		if msb>127:
			binary_representation = format(ss, f'0{32}b') # '0110'
			inverted_binary = ''.join(['1' if bit == '0' else '0' for bit in binary_representation]) # '1001'
			ss = int(inverted_binary, 2) + 1
			ss=ss*-1
			
		return ss*(180/(2**31))
		
	## return longitude for waypoint
	def lon(self):
		msb=bytes.fromhex(" ".join(self.data[34:35]))
		msb=int.from_bytes(msb, byteorder="little")		
		lb=bytes.fromhex(" ".join(self.data[31:35]))
		ss=int.from_bytes(lb, byteorder="little")
		# check if E or W
		if msb>127:
			binary_representation = format(ss, f'0{32}b') # '0110'
			inverted_binary = ''.join(['1' if bit == '0' else '0' for bit in binary_representation]) # '1001'
			ss = int(inverted_binary, 2) + 1 
			ss = ss*-1
		return ss*(180/(2**31))



### start of etrex Class left Waypoint above incase this class needs to access

class etrex():

	port=""
	baud=9600
	ser=""
	
	def __init__(self, port="/dev/ttyUSB0"):
		self;
		self.port=port
		self.ser = serial.Serial(self.port, self.baud, timeout=1)
	
	def sendpacket(self, inpacket):
		self.ser.write(inpacket)
		self.ser.flush()
		
	def readpacket(self):
		packet=[]
		pct=0
		bv=self.ser.read(1)
		packet.append(bv.hex())
		pct=pct+1
		bv=self.ser.read(1)
		packet.append(bv.hex())
		pct=pct+1
		bv=self.ser.read(1)
		packet.append(bv.hex())
		plen = int.from_bytes(bv)
		
		##print(packet)

		#for pct in range(3,plen+6):
		ibv=0
		lastibv=int.from_bytes(bv)

		while True: 
			bv=self.ser.read(1)
			ibv=int.from_bytes(bv)

			if lastibv==16 and ibv==16:
				pass
			else:
				packet.append(bv.hex())
				
			if (ibv==3) and (lastibv==16):
				break
			lastibv=ibv
		
		return packet
	
	
	def send_ack(self):
		ack =bytes([16, 6, 2, 27, 0, 221, 16, 3])
		self.sendpacket(ack)
	
		
	def off(self):
		offlst = bytes([16, 10, 2, 8, 0, 236, 16,3])
		self.sendpacket(offlst)
	
		
	def info(self):
		pck=bytes([16, 254, 0, 2, 16, 3])
		self.sendpacket(pck)
		## get ack - should verify
		packet=self.readpacket()
		## get data packet
		packet=self.readpacket()
		## extract text from packet
		infostr=bytes.fromhex(" ".join(packet[7:len(packet)-4])).decode('utf=8')
		infostr=infostr.replace('\0', '\n')
		## return the useful text
		return(infostr)
		
	def download_waypoints(self):
		##reqwp ="10 0A 02 07 00 ED 10 03"
		wplist=[]
		
		reqwp=bytes([16, 10, 2, 7, 0, 237, 16,3])
		self.sendpacket(reqwp)
		
		packet=self.readpacket()
		pid=int(packet[1],16)
	
		while pid!=12:
			self.send_ack()
			packet=self.readpacket()
			pid=int(packet[1],16)
			if pid==35:
				wplist.append(packet)
			##print(f"PID = {pid}")
			
		return wplist	
