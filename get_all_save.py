#coding: utf-8


import os

activity_list = ["Cig","Code","Multimedia","Housing",\
				"Friend",'Income',"Outcome","Game",\
				'Work']

exclude_file = ['test.py','advAgenda.pyw','README.md','.git','.gitignore']

file_list = [x for x in os.listdir('.') if x not in exclude_file]

width = len(activity_list) + 1
height = 24
day = [[0]*width]*height


for file in file_list:
	if len(file) <= 7:
		with open(file,'r') as save_file:
			save_line = save_file.readlines()[3:]
			for h, line in enumerate(save_line):
				line = line.replace('\n','')
				print(line)
				for m,value in enumerate(line.split(" ")):
					day[h][m] += int(value)

