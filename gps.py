import tkinter as tk
from tkinter import IntVar
import tkinter.font as tkFont
import platform

### use Add to do myinit() for run when file starts
from etrexclass import etrex, Waypoint
import os
import json
from tkinter import filedialog as fd
from tkinter import messagebox

def getport():
	os.system("dmesg | grep ttyUSB > portinfo.txt")
	with open("portinfo.txt", "r") as fn:
		txt=fn.read()
		fn.close()
		val=txt.find("ttyUSB")
		port=f'/dev/{txt[val:len(txt)-1]}'
		##print(port)
		gpstext.delete('1.0', tk.END)
		gpstext.insert('1.0', txt)
		port_entry.delete(0,'end')
		port_entry.insert(0,port)


def myinit():
	getport()
	global gps
	global wpselected, wplist
	wplist=[]
	wpselected=""
	### add port rather than default /dev/ttyUSB0 in class
	gps=etrex()


def on_dlwpbtn_clicked():
	global gps
	global wplist
	
	if wplist!=[]:
		ans=messagebox.askyesno("Info","Clear existing Waypoints?")
		if ans==False:
			return

	wplist=[]
	wplist=gps.download_waypoints()
	
	gpstext.delete('1.0',tk.END)
	gpstext.insert('1.0',"requesting Waypoints...")
	gpstext.update()
	
	wplistbox.delete(0, tk.END)
	wplistbox.update()
	
	for w in wplist:
		wp=Waypoint(w)
		name=wp.name()+'          '
		name=name[0:12]
		symbol=(str(wp.symbol())+"     ")[0:6]
		lat=wp.lat()
		lon=wp.lon()
		wpstr=name+symbol+f'{lat: 4.5f}  {lon: 4.5f}'
		wplistbox.insert(tk.END, wpstr)
def readpacket():
	global ser
	packet=[]
	
	pct=0
	bv=ser.read(1)
	packet.append(bv.hex())
	pct=pct+1
	bv=ser.read(1)
	packet.append(bv.hex())
	pct=pct+1
	bv=ser.read(1)
	packet.append(bv.hex())
	plen = int.from_bytes(bv)
	
	#print(packet)

	#for pct in range(3,plen+6):
	ibv=0
	lastibv=int.from_bytes(bv)

	while True: 
		bv=ser.read(1)
		ibv=int.from_bytes(bv)

		if lastibv==16 and ibv==16:
			pass
		else:
			packet.append(bv.hex())
			
		if (ibv==3) and (lastibv==16):
			break
		lastibv=ibv
		
	##print(packet)
	return packet

 
def on_gibtn_clicked():

	global gps
	infostr=gps.info()
	gpstext.delete('0.0', tk.END)
	gpstext.insert('0.0', infostr)
def on_gpsoffbtn_clicked():
	global gps
	## off in etrex class
	gps.off()
	
def on_loadwpBtn_clicked():
	
	global wplist
	
	if wplist!=[]:
		ans=messagebox.askyesno("Info","Clear existing Waypoints?")
		if ans==False:
			return
	
	filetypes = (
		('JSON files', '*.json'),
		('All files', '*.*')
		)

	filedir=fd.askopenfilename(filetypes=filetypes)
	print(f'[{filedir}]')
	if filedir=="":
		return
		
	wplist=[]
	wplistbox.delete(0, tk.END)
	wplistbox.update()
	
	with open(filedir, "r") as f:
		wplist=json.load(f)
		f.close()
	
	for w in wplist:
		wp=Waypoint(w)
		name=wp.name()+'          '
		name=name[0:12]
		symbol=(str(wp.symbol())+"     ")[0:6]
		lat=wp.lat()
		lon=wp.lon()
		wpstr=name+symbol+f'{lat: 4.5f}  {lon: 4.5f}'
		wplistbox.insert(tk.END, wpstr)
	
def on_mapbtn_clicked():
	global wpselected, wplist

	if wpselected=="":
		messagebox.showinfo("Info","Waypoint has not been selected")
		return
		
	wpselected=wpselected
	
	wp=Waypoint(wplist[wpselected])
	cmd="/usr/bin/chromium https://googlemaps.com/?q="
	cmd=cmd+f'{wp.lat()},{wp.lon()}'
	os.system(cmd)
	

def on_portbtn_clicked():
	getport()


##on_portbtn_clicked()
def on_qbtn_clicked():

	root.destroy()

def on_savewpBtn_clicked():
	
	if wplist==[]:
		messagebox.showinfo("Info","Waypoints have not been loaded")
		return
	
	filetypes = (
		('JSON files', '*.json'),
		('All files', '*.*')
		)

	filedir=fd.asksaveasfilename(initialfile=f'wp.json', filetypes=filetypes)
	print(f'[{filedir}]')
	if filedir=="":
		return
		
	with open(filedir, "w") as f:
		json.dump(wplist, f)
		f.close()
	
def on_testbtn_clicked():
	print("In gps_on_testbtn_clicked.py")

def on_wplistbox_clicked(event):
	global wplist, wpselected
	wpselected=wplistbox.curselection()[0]
	wp=Waypoint(wplist[wpselected])
	wpstr=f'Name : {wp.name()}\nLat  : {wp.lat()}\nLon  : {wp.lon()}'
	gpstext.delete('1.0',tk.END)
	gpstext.insert('1.0',wpstr)
	gpstext.update()

def on_wpselbtn_clicked():
	global wplist, wpselected
	
		
	ans=messagebox.askyesno("Info","Clear existing Waypoints?")
	if ans==False:
		return

	wpselected=""
	wplist=[]
	
	gpstext.delete('1.0',tk.END)	
	wplistbox.delete(0, tk.END)
	wplistbox.update()
	gpstext.update()
	
def on_wxbtn_clicked():

	global wpselected, wplist
	
	if wpselected=="":
		messagebox.showinfo("Info","Waypoint has not been selected")
		return
	
	wp=Waypoint(wplist[wpselected])
	cmd="/usr/bin/chromium 'forecast.weather.gov/MapClick.php?"
	cmd=cmd+f"lat={wp.lat()}"
	cmd=cmd+"&"
	cmd=cmd+f"lon={wp.lon()}'"
	os.system(cmd)

	
root=tk.Tk()
root.title("GPS Console V1.0")
root.geometry("500x650+59+80")

ost=platform.system()
if ost=="Darwin":
	monospace_font = tkFont.Font(family="Menlo", size=10)
elif ost=="Windows":
	monospace_font = tkFont.Font(family="Consolas", size=10)
else:
	monospace_font = tkFont.Font(family="Monospace", size=10)

gpsfrm=tk.Frame(root, borderwidth=2, relief="groove", bg="#d9d9d9" )
gpsfrm.place(x=11,y=12,height=200, width=450)

qbtn=tk.Button(root, text="Exit", bg="#d9d9d9", fg="#000000", command=on_qbtn_clicked )
qbtn.place(x=376,y=615,height=25, width=80)

port_entry=tk.Entry(gpsfrm, bg="white", fg="#000000" )
port_entry.place(x=7,y=142,height=25, width=166)

gpstext=tk.Text(gpsfrm, bg="white", fg="#000000" )
gpstext.place(x=4,y=12,height=100, width=350)

portbtn=tk.Button(gpsfrm, text="Port", bg="#d9d9d9", fg="#000000", command=on_portbtn_clicked )
portbtn.place(x=366,y=145,height=25, width=80)

portlab=tk.Label(gpsfrm, text="Serial Port", bg="#d9d9d9", fg="#000000" )
portlab.place(x=12,y=122,height=23, width=71)

gpsoffbtn=tk.Button(gpsfrm, text="GPS Off", bg="#d9d9d9", fg="#000000", command=on_gpsoffbtn_clicked )
gpsoffbtn.place(x=366,y=87,height=25, width=80)

gibtn=tk.Button(gpsfrm, text="GPS Info", bg="#d9d9d9", fg="#000000", command=on_gibtn_clicked )
gibtn.place(x=366,y=12,height=25, width=80)

mapbtn=tk.Button(gpsfrm, text="Map", bg="#d9d9d9", fg="#000000", command=on_mapbtn_clicked )
mapbtn.place(x=366,y=37,height=25, width=80)

wxbtn=tk.Button(gpsfrm, text="Weather", bg="#d9d9d9", fg="#000000", command=on_wxbtn_clicked )
wxbtn.place(x=366,y=62,height=25, width=80)

infolab=tk.Label(root, text="GPS Info", bg="#d9d9d9", fg="#000000" )
infolab.place(x=22,y=4,height=23, width=58)

wayptfrm=tk.Frame(root, borderwidth=2, relief="groove", bg="#d9d9d9" )
wayptfrm.place(x=10,y=229,height=380, width=450)

wayptlab=tk.Label(root, text="Waypoints", bg="#d9d9d9", fg="#000000" )
wayptlab.place(x=20,y=218,height=23, width=71)

wplistbox=tk.Listbox(wayptfrm, font=monospace_font , bg="#ffffff", fg="#000000" )
wplistbox.place(x=12,y=32,height=300, width=350)
wplistbox.bind('<<ListboxSelect>>', on_wplistbox_clicked)


dlwpbtn=tk.Button(wayptfrm, text="Download", bg="#d9d9d9", fg="#000000", command=on_dlwpbtn_clicked )
dlwpbtn.place(x=366,y=32,height=25, width=80)

wpselbtn=tk.Button(wayptfrm, text="Clear", bg="#d9d9d9", fg="#000000", command=on_wpselbtn_clicked )
wpselbtn.place(x=12,y=336,height=33, width=67)

savewpBtn=tk.Button(wayptfrm, text="Save", bg="#d9d9d9", fg="#000000", command=on_savewpBtn_clicked )
savewpBtn.place(x=366,y=262,height=25, width=80)

loadwpBtn=tk.Button(wayptfrm, text="Load", bg="#d9d9d9", fg="#000000", command=on_loadwpBtn_clicked )
loadwpBtn.place(x=366,y=302,height=25, width=80)

myinit()

root.focus_force()
root.mainloop()
