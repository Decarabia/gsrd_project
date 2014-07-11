#!/usr/bin/env python

def main():

	#import anova
	import append
	#import regression
	import data_selection

	choice_list = [ '1' , '2' ,'3']

	print "Welcome to the GSR statistics program.\n\n\n"
	
	while True:
		while True:
			print " Choose among the following options.\n"
			print " 1. Combine all available data into a single file.\n"
			print " 2. Generate descriptive statistics.\n"
			
			#The commented options are processes that are not currently used/needed.
			#print " 3. Perform ANOVA tests.\n"
			#print " 4. Perform Multiple Regression and related tests.\n"

			print " 3. Quit.\n"
			choice = raw_input("Please enter the number of your choice: ")
			if choice in choice_list:
				break
			print "Please enter a number from 1 to 6."
		
		if choice == '1':
			append.append()
		
		if choice == '2':
			data_selection.main()
		
		#if choice == '3':
			#anova.anova()
			
		#if choice == '4': 
			#regression.main()
		
		if choice == '3':
			break
			

if __name__== "__main__":
        main()

