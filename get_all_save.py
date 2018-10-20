#coding: utf-8
import os

"""
	Make all save in one file
"""

def get_all_save():
	activity_list = ["Cig","Python","Passif","Housing",\
				"Friend",'Income',"Outcome","Game",\
				'Work','Web-dev']
	exclude_file = ['advAgenda.pyw','README.md','.git','.gitignore', 'test.py',' all_save.txt']

	save_file = [x for x in os.listdir('.') if x not in exclude_file]
	save_note = []
	width = len(activity_list) + 1
	height = 24
	day_list = [[[0]*width]*height]*len(save_file)
	cumul_list = [0]*int(len(activity_list)+1)

	# For the save file
	for z,file in enumerate(save_file):
		# If it's note a note_save
		if len(file) <= 7:
			# Open it reading mode
			with open(file,'r') as save_files:
				# read all from the third line 
				save_lines = save_files.readlines()[2:]
				# For every line ine the file
				for i, line in enumerate(save_lines):	
					# Delete '\n' and ' '
					line = line.replace('\n', '')
					# Convert to list
					line = line.split(' ')
					# delete empty index (might be two in a row)
					if line[-1] == "":
						del line[-1]
						if line[-1] == "":
							del line[-1]
					if line[0] =="":
						del line[0]
					# Save the data in the all_data_list
					day_list[z][i] = line
					
					for j,value in enumerate(line):
						cumul_list[j] += int(value)
			save_files.close()
		
		elif len(file) >= 7:
			save_note.append(file)
	

"""
Tentative d'exrire day_list dans un fichier en séparant les jours par '-', les heures par '/' et les activités par ' '
Mais l'écriture répète le dernier jour enregistré
"""


	txt = ''
	test_d = 0
	test_h = 0
	with open('all_save.txt','w') as all_save :
		for d, day in enumerate(day_list):
			for h, hour in enumerate(day_list[d]):
				txt = ''
				if test_d != d:
					test_d = d
					txt +='-'
				for a, activity in enumerate(day_list[d][h]):
					if test_h != h:
						test_h = h
						txt += '/'	
					txt += str(day_list[d][h][a])+' '
				all_save.write(txt)

	return day_list

day_list = get_all_save()

with open('all_save.txt', 'r') as file:
	save = file.readline()

days = save.split('-')
save_day_list = []
one_day = []
for d, day in enumerate(days):
	one_day = str(day).split('/')
	save_day_list.append(one_day)

print(save_day_list[2])
