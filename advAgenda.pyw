#coding: utf-8

import time
import tkinter as tk
import io
import os


global day, activity_list, note_list

# Timeline visuelle
def make_TimeLine(fen):	# Invoque update_Time_Stamp() & set_save_file
	global Timeline, Time_stamp
	"""
		Timeline: 	Canvas de représentation visuelle
		Time_stamp:	Ligne représentant l'heure actuelle

		i: 	Compteur
		x:	Position qui avance de 36 pxl pour marquer chaque heure
		
		Pour dessiner les 24 heures de la journée:
			(1):	Ecrit les heures en haut de la Timeline
			(2):	Dessine une longue ligne verticale marquant les heures
			(3)(4):	Dessine une petite ligne pour marquer les quarts d'heure
			(5):	Dessine un rectangle gris pour représenter les heures
			(6):	Dessine une moyenne ligne pour marquer les demies heures
			(7):	Ecrit les demies heures

		update_Time_Stamp():	MaJ du curseur orange d'heure
		set_save_file():		Créer/Charge le fichier save
	"""
	Timeline = tk.Canvas(fen, width=863, height = 50, bg = 'grey')
	Time_stamp = Timeline.create_line(0,0,0,0,fill='orange',width=2)
	launch = 0

	i = 0
	x = 0
	y = 5


	
	while i < 24:

		Timeline.create_text(x,y, text=i, font=('Times',8,'bold'))		# (1)
		Timeline.create_line(x,16,x,9, fill='white', tag='Hour_line')	# (2)
		Timeline.create_line(x+8,13,x+8,16, fill='white')				# (3)
		Timeline.create_line(x+24,13,x+24,16, fill='white')				# (4)
		Timeline.create_rectangle(x,16,x+36,60,state='normal',\
								outline='white', tag='rect')			# (5)
		Timeline.create_line(x+16,10,x+16,16, fill='white')				# (6)
		Timeline.create_text(x+16,9, text='30', font=("Times",'6', 'bold'),tag='hour') # (7)
		
		i += 1
		x += 36
	
	Timeline.grid(row=0,column=0, columnspan=5)


	update_Time_Stamp()

	set_save_file()
def update_Time_Stamp():
	"""
		current_time:	Heure actuelle
		Hseconde:		Heure en secondes
		Mseconde:		Minute en secondes
		Time_stampX:	Position du Time_stamp

		Calcule le nombre de seconde écoulées depuis minuit
	"""
	global Timeline, Time_stamp, Time_stampX
	current_time = time.strftime('%H:%M:%S')

	hour = int(current_time[:2])
	Hseconde = hour * 3600
	minute = int(current_time[3:5])
	Mseconde = minute * 60
	seconde = int(current_time[6:8])

	tot_seconde = Hseconde + Mseconde + seconde + 10
	Time_stampX =  tot_seconde/100
	
	Timeline.coords(Time_stamp, Time_stampX,0, Time_stampX,60)
	Timeline.tag_raise(Time_stamp,'hour')

	Timeline.tag_raise(Time_stamp,'rect')
	Time_stampX += 1
	fen.after(10000000,update_Time_Stamp)


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
# tabulation dans note
def space_jump(eventorigin):
	global note
	E = '     '
	note.insert('insert',E)
# Ouvre un menu pour gérer l'heure


def add_activities():	# Peut invoque save_manage_list()	# A RENDRE MODULABLE
	global H, day, Entry_list, note, activity_list, note_list, act_window
	act_window = tk.Toplevel()
	act_window.title('Heure: {}'.format(H))
	panneau = tk.Frame(act_window, width=165, height = 195).grid(row=0,column=0,columnspan=2,rowspan=7)
	act_window.resizable(False, False)
	
	function_list =[]
	i = 1
	while i < len(activity_list)+1:
		function_list.append(day[H][i])
		i += 1
	Entry_list = list()
	
	screen_width = act_window.winfo_screenwidth()
	screen_height = act_window.winfo_screenheight()

	x = (screen_width/2)-(863/2)
	y = (screen_height/2)-(50/2)

	note = tk.Text(act_window, width=25, height=18, wrap=tk.WORD)
	note.bind("<KeyPress-Tab>", space_jump)
	Note = note_list[H]
	if len(Note) >= 1:
		note.insert('insert',Note)

	i = 0
	rowi=0
	while i < len(activity_list):
		value = str(function_list[i])
		tk.Label(act_window,parent = panneau, text=activity_list[i], justify=tk.LEFT).grid(row=rowi,column=0, sticky=tk.N)
		En = tk.Entry(act_window,parent = panneau, width=5)
		Entry_list.append(En)
		Entry_list[i].insert(0,value)
		Entry_list[i].grid(row=rowi,column=1, sticky=tk.N)
		rowi = i+1
		i += 1
	
	note.grid(row=0, column=2,rowspan = len(activity_list),columnspan=3, sticky=tk.E)
	tk.Button(act_window, text='Save', command= save_manage_list, highlightcolor='grey').grid(row=len(activity_list)+1,column=0,sticky=tk.S+tk.W+tk.E)
	tk.Button(act_window, text = 'Quit', command=act_window.destroy).grid(row=len(activity_list)+1,column=1,sticky=tk.S+tk.W+tk.E)
	tk.Button(act_window, text='Clear', command = clear_rect).grid(row=len(activity_list)+1,column=2,sticky=tk.S+tk.W+tk.E)
	tk.Button(act_window, text='<', command =previous_hour ).grid(row=len(activity_list)+1, column=3, sticky=tk.S+tk.E+tk.W)
	tk.Button(act_window, text='>', command =next_hour ).grid(row=len(activity_list)+1, column=4, sticky=tk.S+tk.W+tk.E)
# Sauvegarde les modification faites dans add_activities
def save_manage_list():	# Invoque save_hour_note()
	global H, Entry_list, Timeline, day
	
	i = 0
	while i < len(Entry_list):
		day[H][i+1] = int(Entry_list[i].get())
		i += 1

	x = int(H * 36)
	Timeline.create_rectangle(x,16,x+36,60,state='normal',\
				outline='white', fill='grey', tag='del_rect')

	save_hour_note()
	save_Hour_list()
# Sauvegarde et écrit dans le fichier save_note
def save_hour_note():
	global H, note, list_text

	# Vérifie la présence de Save_note.txt
	local = time.localtime() # Création du fichier Save
	filename = make_note_save_file()
	

	infile = io.open(filename,encoding='utf-8',mode ='r+') # Ouvre le fichier en lecture écriture
	oldNote = note_list[H]
	Note = str(note.get(0.0, index2=tk.END)) # Récupère le contenu du widget text
	i = 0
	replace = ''
	while i < len(Note):
		if Note[i] != '\n':
			replace += Note[i]
		i += 1

	Note = replace
	text = infile.read()	# Récupère toute les nptes de la journée
	list_text = text.split('¤') # Sépare les heures des notes et des retours chariots
	infile.close()

	infile = io.open(filename,encoding='utf-8',mode ='r+') # Ouvre le fichier en lecture écriture

	old = infile.read()
	infile.close()
	old = old.split('¤')
	i = 1
	while i < len(old):
		if int(old[i]) == H:
			old[i+1] = Note
			break
		i += 2
	infile = io.open(filename, encoding='utf-8', mode='w')
	Note = str('¤'.join(old))
	infile.write(Note)

	#infile.write(Note)

	infile.close()

# Retourne un fichier.txt pour sauvegarder les activités
def make_save_file():
	
	# Création du fichier Save
	local = time.localtime()

	text = ''
	FileName = str(local.tm_yday) + '.txt'

	return str(FileName)
# Retourne un fichier.txt pour sauvegarder les activités
def make_note_save_file():
	
	# Création du fichier Save
	local = time.localtime()

	text = ''
	FileName = str(local.tm_yday) + '_Note.txt'

	return str(FileName)
# Créer ou charge le fichier save
def set_save_file():	# Invoque save_Hour_list() ou check_save()

	FileName = make_save_file()

	try	:
		file = io.open(FileName,encoding='utf-8',mode='r+')
		check_save()
	except FileNotFoundError:		

	# Si le fichier n'existe pas
	#else:
		# Créer le fichier
		file = io.open(FileName,encoding='utf-8',mode='w+')
		file.close()
		# et ouvre le fichier en écriture délétion
		file = io.open(FileName,'w+', encoding='utf-8')
		file.close()
		save_Hour_list()
# Sauvegarde et écrit dans un fichier les données de la journée
def save_Hour_list():	# Invoque check_save()	# A RENDRE MODULABLE
	global  day, activity_list

	local = time.localtime()
	FileName = make_save_file()
	save_path = 'C:\\Users\\Lucas\\Desktop\\Sam\\Prog\\projets\\AdvAgenda\\'+ FileName

	# Ouvre le fichier save
	file = open(FileName,'r+')

	#=========En tête de fichier==========
	hour = str(local.tm_hour)
	minute = str(local.tm_min)
	seconde = str(local.tm_sec)

	day_time = str(local.tm_mday)
	month = time.strftime('%B')
	year = str(local.tm_year)

	current_time = day_time +'/'+ month +'/'+ year +\
				'  ' + hour +':'+ minute +':'+ seconde + '\n\n'
	
	file.write(str(current_time))
	#=======================================
	
	i = 0

	while i < 24:
		j = 0
		while j < len(activity_list):
			if j == 0 and i != 0:
				text ='\n' + str(day[i][j]) + ' '
				file.write(text)
			else:
				text = str(day[i][j]) + ' '
				file.write(text)
			j += 1
		i += 1
	
	#==========Fin de fichier========
	text = ''
	text += '\n'
	text += '=' * 60
	text += '\n\n'
	file.write(str(text))
	file.close()
	#================================

	check_save() 
# Lis le fichier save
def check_save():		# Invoque  update_Timeline(), update_note() et update_Hour_list()
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


# Action lors du click sur une heure
def select_rect(eventorigin):	# Invoque add_activities
	global H, Hour_list, saveButton
	x = eventorigin.x
	H = int(x/36)
	#Button(fen, text='cig', command= draw_cig).grid(row=2, column=0, sticky=W)
	#tk.Label(fen, text = 'Heure: {}'.format(H)).grid(row=0,column=0, sticky=tk.W+tk.N)
	#Button(fen, text = 'Manage', command = add_activities).grid(row=1,column=0,sticky=W)
	add_activities() 
# Vide l'heure
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


# Met à jour la liste des notes/heures 
def update_note_hour_list(Hour_list, note, hour):
	if note_list[hour] != str(note):
		note_list[hour] = str(note)
		return True
	else :
		return False
# Met a jour la liste des activités/heures visuelle
def update_Hour_list():
	global activity_list, day
	
	FileName = make_save_file()
	fichier = open(FileName, 'r+')

	save_list = list() # Données
	fichier.readline()
	fichier.readline()

	i = 0
	while i < 24:
		j = 0
		text = fichier.readline()
		save_list = text.split(' ')
		while j < len(activity_list):
			if day[i][j] != save_list[j] and j != 0 and j != 10:
				day[i][j] = save_list[j]
			j += 1
		i += 1

	return day
# Met a jour la timeline visuelle
def update_Timeline():	# Invoque get_empty_hour_list()
	global Time_stamp, activity_list, day

	"""
	Se répète pour chaque heure de la journée
	'pos1' définit le début du rectangle d'heure en pixels
	'pos' définit la longueur du rectangle  en fonction de la durée
	'j' permet d'accéder aux attributs de Hour_list via function_list
	'tot' vérifie que le temps d'activité n'excède pas les 60 minutes / heures

	'pos1 += pos' permet d'avancer le début du prochain rectangle d'activité à la fin du précédent
	"""

	color = ['light blue', 'red', 'yellow', 'light green','purple','blue']

	i = 0
	while i < 24:
		
		function_list = [int(day[i][3]), int(day[i][2]), int(day[i][4]),int(day[i][5]),\
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
			Timeline.tag_raise(Time_stamp,'cig')
		i += 1
		update_Time_Stamp()


"""===============STATISTIQUES==========="""
# Met a jour la liste des activités/heures visuelle STATISTIQUE
def update_list_stat(day_list, file, save_list, hour):

	Hour_list_stat[hour].add_cig( int( save_list[1] ) )
	Hour_list_stat[hour].add_prog( int( save_list[2] ) )
	Hour_list_stat[hour].add_multimedia( int( save_list[3] ) )
	Hour_list_stat[hour].add_pote( int( save_list[4] ) )
	Hour_list_stat[hour].add_crypto( int( save_list[5] ) )
	Hour_list_stat[hour].add_depense( int( save_list[6] ) )
	Hour_list_stat[hour].add_wow(int( save_list[7]))
	Hour_list_stat[hour].add_taff(int( save_list[8]))

def get_all_save():
	"""
	1) Initialisation
		- day_list stocke les données de tous les
		  jours passés organisés par [jour][Heure]
		  	- Init day_list ajout à day_list 24 sous
		  	  tableau de 6 attributs vides pour chaque
			  save_file lue
		- save_file stocke la liste des fichiers save passés
		- save_note stocke la liste des fichiers note passés
	2) listage fichier présent
		- Remplissage d'Hour_list avec 24 heures
		- os.listdir('.')
			- Trie save_note et save_file
	3) Lecture fichiers antécédents
		- Ouverture des fichiers avec save_file
		- Lecture des fichier
			- Découpage des lignes de données
			- Stockage dans day_list[save_file][Hour]
			  sous la forme [5, 1,0,20,10,30,20]
		- Créer un fichier _yday_save_stats.txt
		  et y stocke les données des jours précédents
	"""
	
	#===========================INITIALISATION================================

	# Contient une journée
	day_list = []
	# Stocke les saves
	save_file = list()
	# Stocke les notes
	save_note = list()

	#======================LISTAGE FICHIER PRESENT=============================

	# Lecture des save présentes dans le CWD
	# Tant qu'il y a des fichier / dossiers
	for folder in os.listdir('.'):
		# Stocke les saves dans save_file 
		# Si le nom du fichier <= à 7
		if len(folder) <= 7:
			if folder != 'src.py' and folder != 'AdvAgenda'and folder != 'Executable'\
			and folder != 'save_stats.txt':
				save_file.append(folder)
		# Si len(folder)> à 7 alors stocke les saves dans save_note
		else:
			if folder != 'src.py' and folder != 'advAgenda.pyw' and folder != 'Executable'\
			and folder != 'save_stats.txt':
				save_note.append(folder)

	#==========================INIT DAY_LIST======================================
	
	i = 0 
	while i < len(save_file):
		day_list.append([[0]*6]*24)
		i += 1
	
	#====================LECTURE FICHIER ANTECEDANT==============================

	i = 0
	# Lire tant qu'il y a des fichier dans save_file
	while i < len(save_file):
		j = 0
		ofi = open(save_file[i], 'r')
		ofi.readline()
		ofi.readline()

		# On enregistre chaque heure dans day_list[Jour][Heure]
		while j < 24:
			line = ofi.readline()
			day_list[i][j] = line.split(' ')
			j += 1
		
		ofi.close()
		i += 1

	# On note le résultat dans un nouveau fichier.txt
	local = time.localtime()
	FileName = str(local.tm_yday) + 'save_stats.txt'
	ofi = open(FileName, 'w')

	i = 0
	while i < len(day_list):
		k = 0
		while k < 24:
			ofi.write(str(day_list[i][k]))
			k +=1
		i += 1
	ofi.close()

	
	"""
	ofi = open('save_stats.txt', 'r')
	# Récupère les données de save_stats.txt
	x = ofi.read()
	# Stocke dans value ces données
	value = x.split(' ')
	x = value
	
	n, bin, patches = plt.hist(x, len(day_list), normed=1, facecolor='red'\
								,alpha=0.5)

	plt.xlabel('Time')
	plt.ylabel('Value')
	plt.title('Evolution depuis {} jours'.format(temps_tot))


	plt.show()

	"""

"""===============MAIN=================="""

Time_stampX = 0 
SaveH = 0


activity_list = ["Cig","Prog","Multimedia","Fac",\
				"Pote",'Revenu',"Dépense","Jeux",'Taff']

day = []
note_list = []

i = 0
while i < 24:
	day.append([[0]*10])
	note_list.append('')
	i += 1
i = 0
while i < len(day):
	j = 0
	tab = [i]
	while j < len(activity_list):
		tab.append(0)
		j += 1
	day[i] = tab
	i += 1

fen = tk.Tk()
fen.resizable(False, False)
fen.title('Everyday')

make_TimeLine(fen)		# Créer la ligne visuelle
update_Time_Stamp()		# MaJ de l'heure sur la timeline
update_Timeline() 		# Affiche les activités

screen_width = fen.winfo_screenwidth()
screen_height = fen.winfo_screenheight()

x = (screen_width/2)-(863/2)
y = (screen_height/2)-(50/2)

fen.geometry('%dx%d+%d+%d'%(863, 50, x, y))

Timeline.bind('<Button-1>', select_rect)
fen.mainloop()
