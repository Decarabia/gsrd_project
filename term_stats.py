#!/usr/bin/env python

import stats_proc


def main():
		
	term_list = [ 'fall', 'winter', 'spring', 'summer' ] 
	name = 'results/gsrd.xls'	

	#Read in file.
	data = stats_proc.read_file( name )
	
	
	# Get name of Term
	while True:
		
		term = raw_input( "Please enter the term (e.g fall, spring, etc): ")
		term = term.lower()
		if term in term_list:
			break
		print "\n\n\n"
		print "No such term. Please try again."
		print "\n\n\n"
	
	if term == 'fall':
		term_num = 1

	if term == 'winter':
		term_num = 2

	if term == 'spring':
		term_num = 3	
	if term == 'summer':
		term_num = 4
	
	print term_num, '\n'
	#Select Data
	term_data = stats_proc.data_by_term( term_num, data )

	end_data, dates = stats_proc.data_select( term_data )

	# Process
	stats_proc.display_dates( dates )	
	
	results_data, anova_occ, anova_rLength, stats = stats_proc.process( end_data, dates )
	total_data, total_stats = stats_proc.process_all( end_data )
        numbers_data, numbers_stats = stats_proc.process_count_freq( end_data )

	print results_data,"\n"
	print total_data, "\n"
	print numbers_data, "\n"

	# Save results
	numbers = 'results/assesment'
	save = "results/" + term
	save += '.xls'
	total_save = 'results/' + term
	total_save += 'total.xls'
	numbers = numbers + term + ".xls"

	stats_proc.save_file( results_data, save, stats)
	stats_proc.save_file( total_data, total_save, total_stats )
	stats_proc.save_file( numbers_data, numbers, numbers_stats )

if __name__== "__main__":
        main()

