
class nmea:
	
	sentence = ""
	def __init__(self, sentence):
		self.sentence = sentence.split(',')
		
	def msgid(self):
		return self.sentence[0]


class GPGGA(nmea):
	
	## lat formatted as degrees and Minutes
	def latdm(self):
		s=self.sentence
		lat=f'{s[3]}  {s[2][0:2]} {s[2][2:9]}'
		return lat
		
	## lon formatted as degrees and Minutes
	def londm(self):
		s=self.sentence
		lon=f'{s[5]} {s[4][0:3]} {s[4][3:10]}'
		return lon
		
	## lat formatted as decimal degrees	N + and S -
	def lat(self):
		s=self.sentence
		ns=1.0
		if s[3]=='S':
			ns=-1.0		
		degs=(float(s[2][0:2]))
		mins=float(s[2][2:9])	
		lat=degs+(mins/60.0)
		lat=lat*ns
		lat=round(lat,6)
		lat="{:11.6f}".format(lat)
		return(lat)
		
	## lon formatted as decimal degrees E + and W -	
	def lon(self):
		s=self.sentence
		ew=1
		if s[5]=='E':
			ew=-1
		degs=float(s[4][0:3])
		mins=float(s[4][3:10])
		lon=degs+(mins/60.0)
		lon=round(lon*ew,6)
		lon="{:11.6f}".format(lon)
		return lon

	def pfi(self):
		s=self.sentence
		pfi_dict = {
			'0':'Fix not available or invalid',
			'1':'GPS/SPS mode fix valid',
			'2':'Differential GPS/SPS fix valid',
			'6':'Dead Reckoning fix valid'
		}
		fix=s[6]
		return pfi_dict[fix]
	
	def num_of_satelites(self):
		return int(self.sentence[7])
		
		
	## UTC time adjusted by 5 hours for me
	def time_of_day(self):
		utime=self.sentence[1]
		hrs=utime[0:2]
		hrs=int(hrs)-5
		mins=utime[2:4]
		secs=utime[4:9]
		utime =f'{hrs}:{mins}:{secs}'
		return utime

	## returns a list of info for easy printing to oled screen
	def info(self):
		m=[]
		m.append(f'Time : {self.time_of_day()}')	
		m.append(f'Lat  : {self.lat()}')
		m.append(f'Lon  : {self.lon()}')
		m.append(f'Sats :   {self.num_of_satelites()}')
		return m
		



