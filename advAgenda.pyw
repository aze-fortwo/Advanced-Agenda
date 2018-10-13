#coding: utf-8

import time
import tkinter as tk
import io
import os


global day, activity_list, note_list, day_list, save_file, save_note
# Create list with 24 index with len(activity_list)+1 index
def make_day():
	global day
	# Create an empty day_list without hour index
	# at the start of the hour line
	i = 0
	while i < 24:
		day.append([[0]*int(len(activity_list)+1)])
		note_list.append('')
		i += 1
	i = 0

	# Write hour h at the start of the hour line
	while i < len(day):
		j = 0
		tab = [i]
		while j < len(activity_list):
			tab.append(0)
			j += 1
		day[i] = tab
		i += 1
# Visual Timeline
def make_TimeLine(fen):
	global Timeline, Marker
	"""
		Timeline: 	Visual Timeline
		Time_stamp:	Actual hour orange line

		i: 	Counter
		x:	Position wich move right of 36 pxls for every hour
		
		PDraw the 24 hours of the day:
			(1):	Write hours on top of timeline
			(2):	Draw a long vertical line for marking the hour
			(3)(4):	Draw a little vertical line for marking the 1/4 hour
			(5):	Draw a medium vertical line  for marking the half hour
			(6):	Draw a grey rectangle for representing the hour
			(7):	Write '30' above every half hour

		update_Time_Stamp():	MaJ du curseur orange d'heure
		set_save_file():		Créer/Charge le fichier save
	"""
	Timeline = tk.Canvas(fen, width=863, height = 50, bg = 'grey')
	launch = 0

	i = 0
	x = 0
	y = 5

	while i < 24:
		Timeline.create_text(x,y, text=i, font=('Times',8,'bold'))		# (1)
		Timeline.create_line(x,16,x,9, fill='white', tag='Hour_line')	# (2)
		Timeline.create_line(x+9,13,x+9,16, fill='white')				# (3)
		Timeline.create_line(x+25,13,x+25,16, fill='white')				# (4)
		Timeline.create_line(x+18,10,x+18,16, fill='white')				# (5)
		Timeline.create_rectangle(x,16,x+36,60,state='normal',\
								outline='white', tag='rect')			# (6)
		Timeline.create_text(x+18,7, text='30', font=("Times",'6', 'bold'),tag='hour') # (7)
		i += 1
		x += 36
	
	Timeline.grid(row=0,column=0, columnspan=5)
	time_marker()
	set_save_file()
# Display an indicator of actual time on Timeline
def time_marker():	
	"""
		current_time:	Heure actuelle
		Hseconde:		Heure en secondes
		Mseconde:		Minute en secondes
		MarkerX:	Position du Marker

		Calcule le nombre de seconde écoulées depuis minuit
		Calcule la position du curseur en fonction de l'heure
		Se relance toutes les 180 000 ms soit 3 min
	"""
	Timeline.delete('marker')
	current_time = time.strftime('%H:%M:%S')

	hour = int(current_time[:2])
	Hseconde = hour * 3600
	minute = int(current_time[3:5])
	Mseconde = minute * 60
	seconde = int(current_time[6:8])

	MarkerX = (hour *36) + int((Mseconde + seconde)/100)
	Marker = Timeline.create_rectangle(MarkerX-5,0,MarkerX+5,10, fill='red', outline='red', tag='marker')
	Marker_pointer = Timeline.create_polygon(MarkerX-5,10,MarkerX+5,10,MarkerX,16, fill='red', tag='marker')
	fen.after(180000,time_marker)
# Make or load the save_file & note_save_file of the day
def set_save_file():
	global day_list, save_file, activity_list, day
	"""
		(1)	Get the save_file name of the day
		(2)	Create note_save_file
		(3) check_save()
		(4)	save_Hour_list()

	"""
	dayfile = make_save_file()	#(1)

	i = 0
	value = 0
	while i < len(save_file):
		if save_file[i] == dayfile:
			check_save()									#(3)
			value = 1
		i += 1		
	
	if value != 1:
		file = io.open(dayfile, encoding='utf-8',mode='w')	
		file.close()
		save_Hour_list()									#(4)
# Write in save_file the day data
def save_Hour_list():
	global  day, activity_list, day_list
	"""
	(1)	Actual hour
	(2) Write file creation on top of save_file
	(3) 'i' is hour and 'j' is activities
	(4) len(acticity_list) = len(day[i])-1
	(5) At every start of line set a '\n'
		and write the activity hour
	(6) Write the rest of activity value of the hour 'i'
	(7)	Update the all day_list with new modification
	(8) Check_save()
	"""

	local = time.localtime()		#(1)
	FileName = make_save_file()
	# Ouvre le fichier save
	file = open(FileName,'r+')

	hour = str(local.tm_hour)
	minute = str(local.tm_min)
	seconde = str(local.tm_sec)

	day_time = str(local.tm_mday)
	month = time.strftime('%B')
	year = str(local.tm_year)

	current_time = day_time +'/'+ month +'/'+ year +\
				'  ' + hour +':'+ minute +':'+ seconde + '\n'
	
	file.write(str(current_time))					#(2)
	
	i = 0
	while i < 24:									#(3)
		j = 0
		while j < len(activity_list)+1:				#(4)
			if j == 0:		
				text ='\n' + str(day[i][j]) + ' '	#(5)
				file.write(text)
			else:
				text = str(day[i][j]) + ' '			#(6)
				file.write(text)
			j += 1
		i += 1
	
	file.close()
	day_list = get_all_save()						#(7)
	check_save() 									#(8)
# Read save_file and note_save_file for updating day
def check_save():
	global list_text, note_list

	update_Hour_list()
	update_Timeline()
	
	noteFile = make_note_save_file()

	# Vérifie la non-présence de Save_note.txt
	if os.path.exists(noteFile) == False:
		file = io.open(noteFile,encoding='utf-8',mode='w+')
		i = 0
		while i < 24:		# Rentre chaque heure avec les marqueurs à chaque ligne
			text = '¤'+str(i)+'¤'
			file.write(text)
			i += 1
		file.close()
	else:
		fichier = io.open(noteFile,encoding='utf-8',mode ='r+')
	
		text = fichier.read()
		text_list = text.split('¤')
		i = 0
		while i < len(text_list):
			if i != 0 and i % 2 == 0:
				save = text_list[i]
				update_note_hour_list(note_list, save,int(text_list[i-1]))
			i += 1
		fichier.close()
def update_Hour_list():
	global activity_list, day, save_file
	
	FileName = make_save_file()
	fichier = open(FileName, 'r+')

	save_list = list()
	fichier.readline()
	fichier.readline()

	i = 0
	while i < 24:
		j = 0
		text = fichier.readline()
		save_list = text.split(' ')
		while j < len(activity_list)+1:
			if day[i][j] != save_list[j] and j != 0:
				day[i][j] = save_list[j]
			j += 1
		i += 1

	return day
def update_Timeline():	
	global activity_list, day

	"""
	Se répète pour chaque heure de la journée
	'pos1' définit le début du rectangle d'heure en pixels
	'pos' définit la longueur du rectangle  en fonction de la durée
	'j' permet d'accéder aux attributs de Hour_list via function_list
	'tot' vérifie que le temps d'activité n'excède pas les 60 minutes / heures

	'pos1 += pos' permet d'avancer le début du prochain rectangle d'activité à la fin du précédent
	"""

	color = ['light blue', 'red',  'yellow', 'light green','purple','blue']

	i = 0
	while i < 24:
		
		function_list = [int(day[i][2]), int(day[i][3]), int(day[i][4]),int(day[i][5]),\
						int(day[i][8]),int(day[i][9])]

		pos1 = i*36
		pos = 0
		j = 0
		tot = 0

		while j < len(function_list):
			if function_list[j] != 0:
				pos = function_list[j]
				pos /= 5
				pos *= 3
				
				k = 0
				while k < len(function_list):
					tot += function_list[k]
					k += 1

				if tot <= 60:
					Timeline.create_rectangle(pos1+1,17,pos1+pos-1,59, outline=color[j],\
							fill=color[j])
					pos1 += pos -1
				else:
					Timeline.create_rectangle(pos1+1,17,pos1+pos-1,59, outline=color[j],\
							fill=color[j])					


			j += 1

		cig = int(day[i][1])
		cigx = 36*i
		j = 0
		while j < cig:
			if j == 3:
				break
			Timeline.create_line(cigx+4,20,cigx+4,40,fill='white', width=2,tag='cig')
			Timeline.create_line(cigx+4,40,cigx+4,60,fill='orange', width=2,tag='cig')
			j += 1
			cigx += 3 
		i += 1
def select_rect(eventorigin):
	global H, Hour_list, saveButton
	x = eventorigin.x
	H = int(x/36)
	add_activities() 	
	if H >= 20:
		day_resume()	
# New menu for add activity
def add_activities():
	global H, day, Entry_list, note, activity_list, note_list, act_window
	"""
	(1)	act_window:		Window for activity modification
	(2)	panneau:		Stock Entry and Label
	(3)	function_list:	Stock hour H activities
	(4)	Entry_list:		Stock Entry for save_manage_hour()
	Create a new window
	Put a frame on the left side of it		
			note_list:		Sock  notes
			Note:			Get houre note H
	(5)(6) Make note widget with binding
	(7) If note is not empty, make it appear on the note widget
	(8)	Get day data in function_list
	(9)	while activities left:
			(1)	Write activity name in the frame
			(2)	Put an entry next to the act_name
			(3)	Add this entry to Entry_list
			(4) Insert the activity value in the
				corresponding entry
			(5) Grid the Entry
	(10)	Create save, quit, next, previous, clear button and
			grid them below the last Entry
	"""
	act_window = tk.Toplevel()		#(1)
	act_window.title('Hour: {}'.format(H))		#(2)
	panneau = tk.Frame(act_window, width=165, height = 195).grid(row=0,column=0,columnspan=3,rowspan=7)
	act_window.resizable(False, False)
	
	function_list =[]	#(3)
	Entry_list = []		#(4)

	note = tk.Text(act_window, width=25, height=18, wrap=tk.WORD) #(5)
	note.bind("<KeyPress-Tab>", space_jump)	#(6)
	Note = note_list[H]		
	if len(Note) >= 1:		#(7)
		note.insert('insert',Note)

	i = 1
	while i < len(activity_list)+1:		#(8)
		function_list.append(day[H][i])
		i += 1


	i = 0
	rowi=0
	while i < len(activity_list):		#(9)
		value = str(function_list[i]) 						#(1)
		tk.Label(act_window,parent = panneau, text=activity_list[i], justify=tk.LEFT).grid(row=rowi,column=0, sticky=tk.N)
		En = tk.Entry(act_window,parent = panneau, width=5) #(2)
		Entry_list.append(En) 								#(3)
		Entry_list[i].insert(0,value) 						#(4)
		Entry_list[i].grid(row=rowi,column=1, sticky=tk.N)  #(5)
		rowi = i+1
		i += 1
	
	#(10)
	note.grid(row=0, column=2,rowspan = len(activity_list),columnspan=5, sticky=tk.E)
	tk.Button(act_window, text='Save', command= save_manage_list, highlightcolor='grey').grid(row=len(activity_list)+1,column=0,sticky=tk.S+tk.W+tk.E)
	tk.Button(act_window, text = 'Quit', command=act_window.destroy).grid(row=len(activity_list)+1,column=1,sticky=tk.S+tk.W+tk.E)
	tk.Button(act_window, text='Clear', command = clear_rect).grid(row=len(activity_list)+1,column=2,sticky=tk.S+tk.W+tk.E)
	tk.Button(act_window, text='<<', command =previous_day ).grid(row=len(activity_list)+1, column=3, sticky=tk.S+tk.E+tk.W)
	tk.Button(act_window, text='<', command =previous_hour ).grid(row=len(activity_list)+1, column=4, sticky=tk.S+tk.E+tk.W)
	tk.Button(act_window, text='>', command =next_hour ).grid(row=len(activity_list)+1, column=5, sticky=tk.S+tk.W+tk.E)
	tk.Button(act_window, text='>>', command =next_day ).grid(row=len(activity_list)+1, column=6, sticky=tk.S+tk.W+tk.E)
# Save add_activities modifications
def save_manage_list():
	global H, Entry_list, Timeline, day, day_list
	"""
	(1)	While there is activity:
			Update day[Hour] with the Entry value
	(2)	Reset the Hour on graphical timeline for re-drawing
	(3)	save_hour_note():	Write note in note file
	(4)	save_hour_list():	Write save in save file
	"""
	i = 0
	while i < len(activity_list):	#(1)
		day[H][i+1] = int(Entry_list[i].get())
		i += 1

	x = int(H * 36)
	Timeline.create_rectangle(x,16,x+36,60,state='normal',\
				outline='white', fill='grey', tag='del_rect') #(2)

	save_hour_note()	#(3)
	save_Hour_list()	#(4)
def day_resume():
	global day_list, activity_list, day
	cumul = [0] * int(len(activity_list)+1)
	resume_window = tk.Toplevel()
	resume_window.title('Daily resume')
	j = 0
	while j < 24:		
		k = 0
		while k < len(day_list[-1][j]):
			if k != 0:
				base = int(cumul[k-1])
				base += int(day_list[-1][j][k])
				cumul[k-1] = base
			k += 1			

		j += 1
	
	i = 0
	while i < len(activity_list):
		tk.Label(resume_window, text=activity_list[i]).grid(row=i, column=0)
		if i != 0 and i != 6 and i != 7:
			txt = str(cumul[i])+' min'
		elif i == 6 or i == 7:
			txt = str(cumul[i]) + '€'
		else:
			txt = cumul[i]
		tk.Label(resume_window, text=txt).grid(row=i, column=1)
		i += 1
def update_note_hour_list(note_list, note, hour):
	if note_list[hour] != str(note):
		note_list[hour] = str(note)
		return True
	else :
		return False
# Save note in add_activities()
def save_hour_note():
	global H, note, oldNote_list
	"""
	(1)	Create note_save_file
	(2)	Open note_save_file
	(3) Open note_save_file in read mode
	(4)	Get the content of the note widget
		in add_activities() -> newNote
	(5)	Get note_save_file content -> oldNote_list 
	(6)	Find the index H in oldNote_list 
		add newNote after index H
	(7) Make newNote_list for note_save_file
	(8)	Erase old note_save_file and write newNote_list in it
	"""

	filename = make_note_save_file()		#(1)
	newNote = str(note.get(0.0, index2=tk.END))	#(2)
	infile = io.open(filename, encoding='utf-8', mode='r')	#(3)
	text = infile.read()		
	oldNote_list = text.split('¤')	#(4)

	i = 1
	while i < len(oldNote_list):	#(5)
		if int(oldNote_list[i]) == H:
			oldNote_list[i+1] = newNote
			break
		i += 2
	
	infile.close()

	infile = io.open(filename, encoding='utf-8', mode='w')	#(6)
	
	newNote_list = str('¤'.join(oldNote_list))	#(7)
	infile.write(newNote_list)	#(8)
	infile.close()
def clear_rect():
	global H, Timeline, Entry_list, Time_stamp, note
	i = 0
	while i < len(activity_list):
		if i != 0:
			day[H][i] = 0
		i += 1
	x = int(H * 36)
	Timeline.create_rectangle(x,16,x+36,60,state='normal',\
				outline='white', fill='grey', tag='del_rect')
	i = 0
	while i < len(Entry_list):
		Entry_list[i].delete(0, last=100)
		Entry_list[i].insert(0,'0')
		i += 1
	Timeline.tag_raise(Time_stamp, 'del_rect')

	note.delete(0.0, index2=tk.END)
	
	save_hour_note()
	save_Hour_list()
def next_hour():
	global H, act_window
	act_window.destroy()
	H += 1
	add_activities()
def previous_hour():
	global H, act_window
	act_window.destroy()
	H -= 1
	add_activities()
def next_day():
	global day, activity_list, note_list, day_list, save_file, save_note
	date = make_save_file()
	date = int(date[:3])

	i = 0
	value = 0
	while i < len(save_file):
		if save_file[i] == date:
			value = 1
			break
		i += 1
def previous_day():
	global day, activity_list, note_list, day_list, save_file, save_note
	date = make_save_file()
	date = int(date[:3])
	print(date)
def space_jump(eventorigin):
	global note
	E = '     '
	note.insert('insert',E)
# Return the save_file name of the day
def make_save_file():
	local = time.localtime()

	text = ''
	FileName = str(local.tm_yday) + '.txt'

	return FileName
# Return the note_save_file name of the day
def make_note_save_file():
	
	local = time.localtime()

	text = ''
	noteFile = str(local.tm_yday) + '_Note.txt'

	return noteFile
def get_all_save():
	global activity_list, save_file, save_note, day_list
	day_list = []
	save_file = list()
	save_note = list()

	for folder in os.listdir('.'):
		if len(folder) <= 7:
			if folder != '' and folder != 'advAgenda.pyw'and folder != '.git'\
			and folder != 'README.md':
				save_file.append(folder)

		else:
			if folder != '' and folder != 'advAgenda.pyw'and folder != '.git'\
			and folder != 'README.md':
				save_note.append(folder)

	i = 0
	while i < len(save_file):
		ofi = open(save_file[i], 'r')
		ofi.readline()
		ofi.readline()
		j = 0
		while j < 24:
			brutline = ofi.readline()
			line = brutline.split(' ')
			base = line[0]
			line[0] = save_file[i][:3]+'.'+base
			k = 0
			while k < len(line):
				if line[k] == '\n':
					del line[k]
					break
				if line[k] == '':
					del line[k]
				k += 1
			day[j] = line
			j += 1
		day_list.append(day)
		i += 1
	
	return day_list
def make_stats(day_list):
	global activity_list
	cumul_list = [0]* int(len(activity_list)+1)
	print(cumul_list)
	print(day_list[0][23])
	i = 0
	while i < len(day_list):
		j = 0
		while j < len(day_list[i]):
			
			k = 0
			while k < len(day_list[i][j]):
				if day_list[i][j][k] == '\n':
					del day_list[i][j][k]
					break
				elif day_list[i][j][k] == '':
					del day_list[i][j][k] 
					break
				k += 1
			
			k = 0
			while k < len(day_list[i][j]):
				base = cumul_list[k]
				base += int(day_list[i][j][k])
				cumul_list[k] = base
				k += 1
			j += 1
		i += 1



Time_stampX = 0 
SaveH = 0
save_file = []
save_note = []
day = []
day_list = []
note_list = []
activity_list = ["Cig","Code","Multimedia","Maison",\
				"Friend",'Income',"Outcome","Game",\
				'Work']


make_day()
day_list = get_all_save()
#Reset day
make_day()


fen = tk.Tk()
fen.resizable(False, False)
fen.title('Everyday')
make_TimeLine(fen)		# Créer la ligne visuelle

screen_width = fen.winfo_screenwidth()
screen_height = fen.winfo_screenheight()

x = (screen_width/2)-(863/2)
y = (screen_height/2)-(50/2)

fen.geometry('%dx%d+%d+%d'%(863, 50, x, y))

Timeline.bind('<Button-1>', select_rect)
fen.mainloop()
