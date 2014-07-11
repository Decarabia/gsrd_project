#!/usr/bin/env python

import freq_II
import quarterly_stats_II
import term_stats
import year_stats

def main():

	choice_list = ['1', '2', '3', '4', '5' ]

	while True:
		while True:
			print "Choose among the following options.\n"
			print "1. Generate descriptive statistics for all available data.\n"
			print "2. Generate descriptive statistics for a single quarter (e.g. data from Fall 2013).\n"
			print "3. Generate descriptive statistics by year.\n"
			print "4. Generate descriptive statistics by term (e.g. data from every Fall).\n"
			print "5. Back to main menu.\n"
			choice = raw_input( "Please enter the number of your choice: ")
			if choice in choice_list:
				break
			print "Please enter a number from 1 to 5."
	
		if choice == '1':
			freq_II.main()
	
		if choice == '2':
			quarterly_stats_II.main()
	
		if choice == '3':
			year_stats.main()
	
		if choice == '4':
			term_stats.main()
		
		if choice == '5':
			break
		
if __name__== "__main__":
        main()

