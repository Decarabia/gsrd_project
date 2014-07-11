#!/usr/bin/env python

# freq_II.py
# Paul Gelbach

# Overview: freq.py generates descriptive statistics using gsrd.xls. It computes
# statistics for InUse ( whether a room is in use or not ), Occ ( the number of people in a room),
# and RLength ( the length of room reservations )

import stats_proc

# gsrd.xls contains all the data that program reads in.
name = 'results/gsrd.xls'

# Data is saved to these files

data_file = 'results/freq_result.xls'
overall_data = 'results/overall_mean.xls'
overall_count_stats = 'results/overall_count_stats.xls'


#stats_proc.py contains all the documentation for these functions.

def main():
	
	choice_list = [ '1', '2', '3' ]
	while True:
		while True:
			print "1. Generate Descriptive Statistics for Each Room.\n"
			print "2. Generate Overall Descriptive Statistics (i.e. All Data is processed together).\n"
			print "3. Go Back to Descriptive Statistics Menu.\n"
			choice = raw_input( "Please enter the number of your choice: ")
			if choice in choice_list:
				break
			print "Please enter a number from 1 to 3.\n"

		if choice == '1':
			data = stats_proc.read_file( name )
			freq_data, dates = stats_proc.data_select( data )	
			stats_proc.display_dates( dates )
			
			#Some of what stats_proc.process returns isn't going to be used later.
			#Be sure to complete the removal process in the future.
			results_data, anova_occ, anova_rLength, stats = stats_proc.process( freq_data, dates )
			stats_proc.save_file( results_data, data_file, stats )

		if choice == '2':
			#Proccess data from rooms together.
			data = stats_proc.read_file( name )
			freq_data, dates = stats_proc.data_select( data )
			stats_proc.display_dates( dates )
			data, stats = stats_proc.process_all ( freq_data )
			stats_proc.save_file( data, overall_data, stats )
			print data
			
			#Generates occpant frequency statistics.
			data = stats_proc.read_file( name )
			count_stats, occ_stats = stats_proc.process_count_freq( data )
			stats_proc.save_file( count_stats, overall_count_stats, occ_stats )
			print count_stats
	
		if choice == '3':
			break
 
if __name__== "__main__":
        main()


