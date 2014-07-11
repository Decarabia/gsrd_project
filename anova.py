#!/usr/bin/env python

import pandas as pd
import numpy as np
import openpyxl
import scipy.stats as st

ONE = 'Sheet1'

# gsrd.xls contains all the data that program reads in.

occ = 'sorted_occ_results.xls'
rLength = 'sorted_rLength_results.xls'
gsrd = 'gsrd.xls'

ROOMS = [ 270, 271, 272, 273, 274, 309, 314, 352, 370, 371, 409, 410, 411, 509, 510, 511 ]
ROOM_INPUT = [ '270', '271', '272', '273', '274', '309', '352', '370', '371', '409', '410', '411', '509', '510', '511' ]

# stats contains the column headers for the output file. Any changes in the statistics to be calculated
# and recorded have to be reflected here.

occ_stats = [ 'Occupant_Observations', 'Occupant_Mean', 'Occupant_LCI', 'Occupant_UCI', 'Occupant_STD' ]  
rLength_stats = [ 'Minutes_per_Day_Observations', 'Minutes_per_Day_Mean', 'Minutes_per_Day_LCI', 'Minutes_per_Day_UCI', 'Minutes_per_Day_STD' ]
gsrd_header =  [ 'Date', 'Day', 'Time', 'Floor', 'Room', 'Reserved', 'InUse', 'Occ', 'Start', 'End', 'Remaining', 'AdHoc', 'Size', 'Quarter', 'Finals', 'RLength' ]

# freq_results.xls is the output file.

#data_file = 
sorted_occ = 'sorted_occ_results.xls'
sorted_rLength = 'sorted_rLength_results.xls'

# In the future, main needs to be functionally decomposed so that it will
# be easier to maintain. The calculations and the output should be
# in seperate functions.

choice_list = [ '1', '2', '3' ]
choice_sub_list = [ '1', '2' ]

def anova():
	
	print "\n\n\n"
	print "Loading files...\n\n\n"

	while True:

		xls_file = pd.ExcelFile( occ )
        	table = xls_file.parse( ONE )
        	anova_occ = pd.DataFrame( table, columns = occ_stats )
	
		xls_file = pd.ExcelFile( rLength )
		table = xls_file.parse( ONE )
		anova_rLength = pd.DataFrame( table, columns = rLength_stats )
		
		xls_file = pd.ExcelFile( gsrd )
		table = xls_file.parse( ONE )
		gsr_data = pd.DataFrame( table, columns = gsrd_header )
		save_list = []		

		while True:
			print "Enter 1 to see occupant statistics and to select occupant data for ANOVA.\n"
			print "Enter 2 to see reservation length statistics and to select reservation length data for ANOVA.\n"
			print "Enter 3 to quit."
			choice = raw_input( "Enter your selection: " )
			if choice in choice_list:
				break
			print "Please make a valid selection."
	
		if choice == '1':
			occ_list = []
			print "\n\n\n"
			print anova_occ
			print "\n\n\n"
			
			while True:
				while True:
					print "Rooms that have been selected: " , occ_list
					room_number = raw_input( "Enter a room number for comparison: " )
					room_value = int( room_number )
					if room_number == '':
						room_number = '0'
					if room_value in occ_list:
						print "This number was already entered. Please choose a different room."	
					if room_value in ROOMS and room_value not in occ_list:
						occ_list.append( room_value )
						break
					print "Invalid room number. Please try again."
				
				while True:
					occ_choice = raw_input( "Enter 1 to add another room or 2 to see and save ANOVA results: " )
					if occ_choice in choice_sub_list:
						break
					print "Invalid choice. Please try again."
				
				if occ_choice == '2':
					pieces = []
					for i in occ_list:
						occ_data = gsr_data[ gsr_data[ 'Room' ] == i ]
						occ_data = np.array( occ_data[ 'Occ' ].dropna() )
						pieces.append( occ_data )
					f_val, p_val = st.f_oneway( *pieces )
					print "\n\n\n"
					print "p value is ", p_val
					print "If ", p_val, " > 0.05, then the means of the rooms are highly likely to be equal."
					print "\n\n\n"
					p_val_list = []
					for i in occ_list:
						p_val_list.append( p_val )
					results_df = pd.DataFrame( { 'Rooms Compared':occ_list, 'P_Value': p_val_list }	)
					print "Names of save files already created in this session: ", save_list
					while True:	
						save_file = raw_input( "Enter the name of the file for saving the ANOVA results: " )
						if save_file in save_list:
							print "A save file with this name has already been created.\nPlease enter a different name."
						if save_file not in save_list:
							save_list.append( save_file )
							results_df.to_excel( save_file, ONE )
							break
					break		
	
		if choice == '2':
			rLength_list = []
			print "\n\n\n"
			print anova_rLength
			print "\n\n\n"
		
			while True:
				while True:
					print "Rooms that have been selected: ", rLength_list
					room_number = raw_input( "Enter a room number for comparison: " )
					room_value = int( room_number )
					if room_number == '':
						room_number = '0'
					if room_value in rLength_list:
						print "This number was already entered. Please choose a different room."
					if room_value in ROOMS and room_value not in rLength_list:
						rLength_list.append( room_value )
						break
					print "Invalid room number. Please try again."
				
				while True:
					rLength_choice = raw_input( "Enter 1 to add another room or 2 to see and save ANOVA results: " )
                                	if rLength_choice in choice_sub_list:
                                		break
                           		print "Invalid choice. Please try again."
			
				if rLength_choice == '2':
					pieces = []
					for i in rLength_list:
						rLength_data = gsr_data[ gsr_data[ 'Room' ] == i ]
						rLength_data = np.array( rLength_data[ 'RLength' ].dropna() )
						pieces.append( rLength_data )
					f_val, p_val = st.f_oneway( *pieces )
					print "\n\n\n"
					print "p value ", p_val
					print "\n\n\n"
	 				print "If ", p_val, " > 0.05, then the means of the rooms are highly likely to be equal."
                               		print "\n\n\n"
					p_val_list = []
					for i in rLength_list:
						p_val_list.append( p_val )
                                	results_df = pd.DataFrame( { 'Rooms Compared':rLength_list, 'P_Value': p_val_list } )
                                	print "Names of save files already created in this session: ", save_list
                                
					while True:	
                                		save_file = raw_input( "Enter the name of the file for saving the ANOVA results: " )
                                        	if save_file in save_list:
                                        		print "A save file with this name has already been created.\nPlease enter a different name."
                                      		if save_file not in save_list:
                                        		save_list.append( save_file )
                                                	results_df.to_excel( save_file, ONE )
                                                	break
                                        	break

					break
						
		if choice == '3':
			break			
						
					
if __name__== "__anova__":
        anova()

