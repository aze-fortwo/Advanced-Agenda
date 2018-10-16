#coding: utf-8

import time
import tkinter as tk
import io
import os


global day, activity_list, note_list, day_list, save_file, save_note, launched
launched = 0
# Create list with 24 index with len(activity_list)+1 index
def make_day():
	# Create an empty day_list without hour index
	# at the start of the hour line
	global day
	
	day = []

	i = 0
	while i < 24:
		day.append([[0]*int(len(activity_list)+1)])
		note_list.append('')
		i += 1

	# Write hour h at the start of the hour line
	i = 0
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
	global Timeline, Marker, launched
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
	if launched == 0:
		set_save_file()
# Display an indicator of actual time on Timeline
def time_marker():	
	"""
	Position of the red arker on top of timeline wich represent actual hour
	1) Convert actual time (HH:MM:SS) to second from midnight
	2) One hour = 36 pixels, 1 sec = 0.01 pixels -> Xs/100 = pixels traveled
	3) Draw marker on canvas with updated position
	4) Every 3 minutes, the marker should travel 1 pixel right
	"""
	Timeline.delete('marker')
	current_time = time.strftime('%H:%M:%S')

	#1)
	hour = int(current_time[:2])
	Hseconde = hour * 3600
	minute = int(current_time[3:5])
	Mseconde = minute * 60
	seconde = int(current_time[6:8])

	#2)
	MarkerX = (hour *36) + int((Mseconde + seconde)/100)

	#3)
	Marker = Timeline.create_rectangle(MarkerX-5,0,MarkerX+5,10, fill='red', outline='red', tag='marker')
	Marker_pointer = Timeline.create_polygon(MarkerX-5,10,MarkerX+5,10,MarkerX,16, fill='red', tag='marker')

	#4)
	fen.after(180000,time_marker)
# Make or load the save_file & note_save_file of the day
def set_save_file():
	global save_file, act_day, launched
	"""
		(1)	Get the save_file name of the day
		(2) read_save_file()
		(3)	write_save_day()

	"""
	dayfile = get_day_txt()	#(1)
	act_day = dayfile[:3]

	i = 0
	value = 0
	while i < len(save_file):
		if save_file[i] == dayfile and launched == 0:
			read_save_file()									#(2)
			value = 1
		i += 1		
	
	if value != 1 and launched == 0:
		file = io.open(dayfile, encoding='utf-8',mode='w')	
		file.close()
		write_save_day()									#(3)
# Write in save_file the day data
def write_save_day():
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
	(8) read_save_file()
	"""

	local = time.localtime()		#(1)
	FileName = get_day_txt()
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
	read_save_file() 									#(8)
# Read save_file and note_save_file for updating day
def read_save_file():
	global note_list
	#If this is the first launch
	if launched == 0:
		# Get the last day
		FileName = get_day_txt()
		# Update global day with this file content
		update_list(FileName)
	# Update visual timeline
	update_Timeline()
	
	# Make note file save
	noteFile = get_day_txt()[:3] + '_Note.txt'

	# if no note save file already exist
	if os.path.exists(noteFile) == False:
		# Create a new note file
		file = io.open(noteFile,encoding='utf-8',mode='w+')
		i = 0
		# Write every Hour with '¤' between hour and note as ¤0¤Note¤1¤¤2¤...
		while i < 24:		
			text = '¤'+str(i)+'¤'
			file.write(text)
			i += 1
		file.close()
	else:
		# Read the note file save
		fichier = io.open(noteFile,encoding='utf-8',mode ='r+')
	
		text = fichier.read()
		# Split note from hour 
		text_list = text.split('¤')
		i = 0
		while i < len(text_list):
			# Every 2 element of the list and if the element is not the first one
			if i != 0 and i % 2 == 0:
				# Save the note content
				save = text_list[i]
				# Check if note isn't already like that 
				# If not, update it
				update_note_list(note_list, save,int(text_list[i-1]))
			i += 1
		fichier.close()
# Get save from file and update day with it
def update_list(FileName):
	global activity_list, day
	
	# Open the save_file
	fichier = open(FileName, 'r+')

	#Contain split version of line in the save 
	save_list = list()
	fichier.readline()
	fichier.readline()

	i = 0
	while i < 24:
		j = 0
		text = fichier.readline()
		save_list = text.split(' ')
		# len(activity_list) +1 because of the hour at position 0 in day[i][0]
		while j < len(activity_list)+1:
			# If the actual saved data are outdated
			if day[i][j] != save_list[j] and j != 0:
			# Replace old save by new written
				day[i][j] = save_list[j]
			j += 1
		i += 1
# Update visual timeline
def update_Timeline():	
	global activity_list, day, launched

	"""
	Repeat every hour of the day (24 for knowledge)
	'pos1' define the first point of the hour rectangle
	'pos' define the lenght of the rectangle regard to the time passed
	'tot' check if the total time of activity doesn't exceed 60 minutes (if multy activity for exemple)
	"""
	# Color added to the rectangle when draw
	color = ['light blue', 'red',  'yellow', 'light green','purple','blue']

	i = 0
	while i < 24:
		
		# All visual data needed are here
		function_list = [int(day[i][2]), int(day[i][3]), int(day[i][4]),int(day[i][5]),\
						int(day[i][8]),int(day[i][9])]

		# Convert hour to pixels (1h=36 pixels)
		pos1 = i*36
		pos = 0
		j = 0



		while j < len(function_list):
			# If there is data to draw
			if function_list[j] != 0:
				pos = function_list[j]
				# 5 min is 3 pixels
				pos /= 5
				# We get how much pixels from total seconds
				pos *= 3
				tot = 0
				# Get activity cumul of the hour
				k = 0
				while k < len(function_list):
					tot += function_list[k]
					k += 1

				# Is activity_cumul > 60 ?
				if tot <= 60:
					Timeline.create_rectangle(pos1+1,17,pos1+pos-1,59, outline=color[j],\
							fill=color[j])
					pos1 += pos 
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
	if launched == 0:
		launched = 1
	elif launched == 'o':
		pass
# Get from the pos of the cursor the hour selected on timeline
def select_rect(eventorigin):
	global H, Hour_list, saveButton
	x = eventorigin.x
	H = int(x/36)
	manage() 	
	if H >= 20:
		day_resume()	
# Menu for adding activity
def manage():
	global H, day, Entry_list, note, activity_list, note_list, manage_window, launched
	"""
	(1)	manage_window:		Window for activity modification
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
	manage_window = tk.Toplevel()		#(1)
	manage_window.title('Hour: {}'.format(H))		#(2)
	panneau = tk.Frame(manage_window, width=165, height = 195).grid(row=0,column=0,columnspan=3,rowspan=7)
	manage_window.resizable(False, False)
	
	function_list =[]	#(3)
	Entry_list = []		#(4)

	note = tk.Text(manage_window, width=25, height=18, wrap=tk.WORD) #(5)
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
		tk.Label(manage_window,parent = panneau, text=activity_list[i], justify=tk.LEFT).grid(row=rowi,column=0, sticky=tk.N)
		# If this is not an old save display
		if launched != 'o':
			En = tk.Entry(manage_window,parent = panneau, width=5) #(2)
		else:
			En = tk.Entry(manage_window,parent = panneau, width=5) #(2)
		Entry_list.append(En) 								#(3)
		Entry_list[i].insert(0,value) 						#(4)
		Entry_list[i].grid(row=rowi,column=1, sticky=tk.N)  #(5)
		rowi = i+1
		i += 1
	
	#(10)
	note.grid(row=0, column=2,rowspan = len(activity_list),columnspan=5, sticky=tk.E)
	tk.Button(manage_window, text = 'Quit', command=manage_window.destroy).grid(row=len(activity_list)+1,column=1,sticky=tk.S+tk.W+tk.E)
	tk.Button(manage_window, text='<<', command =previous_day ).grid(row=len(activity_list)+1, column=3, sticky=tk.S+tk.E+tk.W)
	tk.Button(manage_window, text='<', command =previous_hour ).grid(row=len(activity_list)+1, column=4, sticky=tk.S+tk.E+tk.W)
	tk.Button(manage_window, text='>', command =next_hour ).grid(row=len(activity_list)+1, column=5, sticky=tk.S+tk.W+tk.E)
	tk.Button(manage_window, text='>>', command =next_day ).grid(row=len(activity_list)+1, column=6, sticky=tk.S+tk.W+tk.E)
	if launched != 'o':
		tk.Button(manage_window, text='Save', command= save_manage, highlightcolor='grey').grid(row=len(activity_list)+1,column=0,sticky=tk.S+tk.W+tk.E)
		tk.Button(manage_window, text='Clear', command = clear_rect).grid(row=len(activity_list)+1,column=2,sticky=tk.S+tk.W+tk.E)
# Save manage modifications
def save_manage():
	global H, Entry_list, Timeline, day
	"""
	(1)	While there is activity:
			Update day[Hour] with the Entry value from manage window
	(2)	Reset the Hour on graphical timeline for re-drawing
	(3)	write_save_note():	Write note in note file
	(4)	write_save_day():	Write save in save file
	"""
	i = 0
	while i < len(activity_list):	#(1)
		day[H][i+1] = int(Entry_list[i].get())
		i += 1

	x = int(H * 36)
	Timeline.create_rectangle(x,16,x+36,60,state='normal',\
				outline='white', fill='grey', tag='del_rect') #(2)

	write_save_note()	#(3)
	write_save_day()	#(4)
# Display sum of activity from actual day
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
		if i != 0 and i != 5 and i != 6:
			txt = str(cumul[i])+' min'
		elif i == 5 or i == 6:
			txt = str(cumul[i]) + '€'
		else:
			txt = cumul[i]
		tk.Label(resume_window, text=txt).grid(row=i, column=1)
		i += 1
# Get save from file and update day note with it
def update_note_list(note_list, note, hour):
	if note_list[hour] != str(note):
		note_list[hour] = str(note)
		return True
	else :
		return False
# Save note in manage window
def write_save_note():
	global H, note, oldNote_list
	"""
	(1)	Create note_save_file
	(2)	Open note_save_file
	(3) Open note_save_file in read mode
	(4)	Get the content of the note widget
		in manage() -> newNote
	(5)	Get note_save_file content -> oldNote_list 
	(6)	Find the index H in oldNote_list 
		add newNote after index H
	(7) Make newNote_list for note_save_file
	(8)	Erase old note_save_file and write newNote_list in it
	"""

	notefile = get_day_txt()		#(1)
	# Make note file save
	filename = notefile[:3] + '_Note.txt'

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
# Clean the hour rect and delete hour activity
def clear_rect():
	global H, Timeline, Entry_list, note

	# Set the activity data at 0 for the hour H
	i = 0
	while i < len(activity_list):
		if i != 0:
			day[H][i] = 0
		i += 1
	# Get the position of the hour rect in timeline
	x = int(H * 36)
	# Create a grey rect on top of it
	Timeline.create_rectangle(x,16,x+36,60,state='normal',\
				outline='white', fill='grey', tag='del_rect')
	i = 0

	# Clear the entry data in manage window
	while i < len(Entry_list):
		Entry_list[i].delete(0, last=100)
		Entry_list[i].insert(0,'0')
		i += 1
	# Clear the note in manage window
	note.delete(0.0, index2=tk.END)
# Repeat clear_rect for the 24h
def clear_timeline():
	global H
	# H is global so take it's old value
	save = H
	# For the 24 hour
	i = 0
	while i < 24:
		H = i
		clear_rect() # Clear hour [i]
		i += 1
	# Set to H his old value
	H = save
# '>' button in manage window
def next_hour():
	global H, manage_window
	# Close the manage window of the actual hour
	manage_window.destroy()
	# Increment actual hour 
	H += 1
	# Open manage window with updated hour
	manage()
# '<' button in manage window
def previous_hour():
	global H, manage_window
	# Close the manage window of the actual hour
	manage_window.destroy()
	# Decrease actual hour 
	H -= 1
	# Open manage window with updated hour
	manage()
# '>>' button in manage window
def next_day():
	global act_day, relative_day, launched, manage_window
	# Actual day of the year (Ex: 255/365, 256 = relative_day)
	# incremented of 1
	relative_day = int(act_day[:3]) +1 
	relative_day = str(relative_day) + '.txt'
	# Clear all hour rect for drawing
	clear_timeline()
	# Read relative_day file and upsate global day with it
	update_list(relative_day)
	# Draw the day + 1
	update_Timeline()
	# Set the actual day(the day wich is displayed) as 256
	act_day = relative_day[:3]
	# If the day+1 is not today
	if relative_day != get_day_txt(): 
		# Mark the actual display as old
		# For prevent saving in old files
		launched = 'o'
	else :
		# Set the saving possible for today
		launched = 1
	# Destroy then create new window for updating content inside
	manage_window.destroy()
	manage()
# '<<' button in manage window
def previous_day():
	global act_day, relative_day, launched, manage_window
	# Actual day of the year (Ex: 255/365, 256 = relative_day)
	# incremented of 1
	relative_day = int(act_day[:3]) - 1 
	relative_day = str(relative_day) + '.txt'
	# Clear all hour rect for drawing
	clear_timeline()
	# Read relative_day file and upsate global day with it
	update_list(relative_day)
	# Draw the day + 1
	update_Timeline()
	# Set the actual day(the day wich is displayed) as 256
	act_day = relative_day[:3]
	# If the day+1 is not today
	if relative_day != get_day_txt(): 
		# Mark the actual display as old
		# For prevent saving in old files
		launched = 'o'
	else :
		# Set the saving possible for today
		launched = 1
	# Destroy then create new window for updating content inside
	manage_window.destroy()
	manage()
# Shortkey for tab = '     ' 
def space_jump(eventorigin):
	global note
	E = '     '
	note.insert('insert',E)
# Return the save_file name of the day
def get_day_txt():
	local = time.localtime()

	text = ''
	FileName = str(local.tm_yday) + '.txt'

	return FileName
# Read all the save_file and save it in day_list
def get_all_save():
	global activity_list, save_file, save_note, day, day_list
	saveDay = day
	# Used for copying saved day into day_list 1 by 1
	dDay = [[0]*int(len(activity_list)+1)]*24
	# day_list[day][hour]
	day_list = []
	# Listing of all the file (note and save)
	save_file = list()
	save_note = list()

	# While there is save in the working directory
	for folder in os.listdir('.'):
		# The save folder are minimum:'1.txt' to '365.txt' so [0;7]
		if len(folder) <= 7:
			if folder != '' and folder != '.git':
				# If the file isn't GitHub directory
				# Add it to the save_file list
				save_file.append(folder)
		# So it can be a note save_file
		else:
			if folder != '' and folder != 'advAgenda.pyw'and folder != '.git'\
			and folder != 'README.md' and folder != 'test.txt':
				# If it is, save it in save_note
				save_note.append(folder)

	i = 0
	# While there is save_file to read
	while i < len(save_file):
		update_list(save_file[i])
		day_list.append(day)
		i += 1
	day = saveDay
	return day_list
	
# Set the environment for accessing every data of the day_list
def make_stats():
	global activity_list, day_list
	cumul_list = [0]* int(len(activity_list))
	
	i = 0
	# While there is day
	while i < len(day_list):
		j = 0
		# While there is hour in a day
		while j < 23:
			#k = 1 because day_list[i][j][0] == (tm_yday.txt) and cumul
			# list do not want that in his maths
			k = 1
			# Repeat for every activity + the tm_yday code at day_list[0]
			while k < len(activity_list)+1:
				# [k - 1] because len(activity_list) + 1 have one more index 
				# than cumul list, so when k = 2 -> cumul_list[1]
				cumul_list[k-1] += int(day_list[i][j][k])

				k += 1
			j += 1
		i += 1

	print(cumul_list)

	i = 0
	while i < len(activity_list):
		i += 1


Time_stampX = 0 
SaveH = 0
save_file = []
save_note = []
day = []
day_list = []
note_list = []
activity_list = ["Cig","Code","Multimedia","Housing",\
				"Friend",'Income',"Outcome","Game",\
				'Work']



fen = tk.Tk()

make_day()
get_all_save()

make_stats()

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
