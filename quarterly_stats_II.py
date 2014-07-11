#!/usr/bin/env python

import stats_proc
import csv
import pandas as pd
from os import listdir
from os.path import isfile, join

def main():

    while True:
        res_direct = "results/"
        direct = "gsr_excel_files"
        nameList = [f for f in listdir( direct ) if isfile(join(direct, f)) ]
    
        print "\n\n\n"
        print "Reading in file names..."
        print "\n\n\n"
        print "The following are the valid file names: "
        for i in nameList:
            print i
        print "\n\n\n"

        while True:
            open_name = raw_input( "Please type the name of the file you wish to open: " )
            print open_name
            if open_name in nameList:
                break
                print "\n\n\n"
            print "Invalid file name. Please enter a name from the following list: "
            for i in nameList:
                print i

        direct += "/"
        direct += open_name

        data = stats_proc.read_file( direct )
        clean_data = stats_proc.clean( data )
        freq_data, dates = stats_proc.data_select( clean_data )
        stats_proc.display_dates( dates )
        results_data, anova_occ, anova_rLength, stats = stats_proc.process( freq_data, dates )
        total_results, freq_stats = stats_proc.process_all( freq_data )
        numbers_stats, count_stats = stats_proc.process_count_freq( freq_data )
        
        data_file, total_file, number_file = res_direct, res_direct, res_direct
        data_file += open_name[0:7]
        total_file += open_name[0:7]
        number_file += open_name[0:7]
        data_file += "_room_res.xls"
        total_file += "_overall.xls"
        number_file += "_num_res.xls"
        
        print results_data, "\n"
        print total_results, "\n"
        print numbers_stats, "\n"

        print data_file
		
        stats_proc.save_file( results_data, data_file, stats )
        stats_proc.save_file( total_results, total_file, freq_stats )
        stats_proc.save_file( numbers_stats, number_file, count_stats ) 
        
        while True:
            answer = raw_input("If you wish to process another file, please type 'y'. If you wish to quit, type 'n': " )
            if answer.lower() in [ 'y', 'n' ]:
                break
                print "Invalid choice. Please try again."
        
        if answer.lower() == 'n':
            break

if __name__== "__main()__":
        main()

