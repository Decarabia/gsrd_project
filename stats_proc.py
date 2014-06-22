#!/usr/bin/env python

import pandas as pd
import numpy as np
import scipy.stats as st
import abba.stats
import xlrd as xl
import datetime as dr
import math

#Update file operations so that subdirectories are used
#from os import path

#Sheet number of the excel file to be read in. 
ONE = 'Sheet1'

#rLength is processed AFTER this date, since we do not have rLength data before it.
START = 41306

#Group study room numbers.
ROOMS = [ 270, 271, 272, 273, 274, 309, 314, 352, 370, 371, 409, 410, 411, 509, 510, 511 ]

# Headers reflects the columns in the excel files. Any changes there should be reflected here.
headers = [ 'Date', 'Day', 'Time', 'Floor', 'Room', 'Reserved', 'InUse', 'Occ', 'Start', 'End', 'Remaining', 'AdHoc', 'Size', 'Quarter', 'Finals', 'RLength' ]

# stats contains the column headers for the output file. Any changes in the statistics to be calculated
# and recorded have to be reflected here.

stats = [ 'InUse_Observations', 'InUse_Mean', 'InUse_STD', 'InUse_LCI', 'InUse_UCI', 'Occupant_Observations', 'Occupant_Mean', 'Occupant_STD', 'Occupant_LCI', 'Occupant_UCI', 'Occupant_Max',  'Minutes_per_Day_Observations', 'Minutes_per_Day_Mean', 'Minutes_per_Day_STD', 'Minutes_per_Day_LCI', 'Minutes_per_Day_UCI', 'Minutes_per_Day_Max' ]

freq_stats =  [ 'InUse_Observations', 'InUse_Mean', 'InUse_STD', 'InUse_LCI', 'InUse_UCI' ]
occ_stats = [ 'Occupant_Observations', 'Occupant_Proportion', 'Occupant_STD', 'Occupant_Lower_Confidence_Interval', 'Occupant_Upper_Confidence_Interval' ]

#Reads in the file.
def read_file( name ):
	
        xls_file = pd.ExcelFile( name )
        table = xls_file.parse( ONE )
        data = pd.DataFrame( table, columns = headers )

        return data

#Selects according to the term in which it was gathered.
def data_by_term( term, data ):
	
	freq_data_var = data[ [ 'Room', 'InUse', 'Occ', 'Date', 'RLength', 'Quarter' ] ]
	term_data = freq_data_var[ freq_data_var[ 'Quarter' ] == term ]
	
	return term_data

#Selects accourding the year in which the data was gathered
def data_by_year( year, data ):
	year_min = xl.xldate.xldate_from_date_tuple( ( year, 1, 1 ), 0) 
	year_max = xl.xldate.xldate_from_date_tuple( ( year, 12, 31 ), 0)
	year_range = range( int(year_min), int(year_max) )
	freq_data_var = data[ [ 'Room', 'InUse', 'Occ', 'Date', 'RLength' ] ]
	year_data = freq_data_var[ np.logical_and(freq_data_var[ 'Date' ] <= year_max, year_min <= freq_data_var[ 'Date' ])  ] 
	
	return year_data
	
# Puts relevant data into a dataframe. May need to be updated for greater flexibility.
def data_select( data ):
	
	# If other statistics are to be calculated ( such as for the time remaining
	# the list [ 'Room, 'InUse'...] will have to include the appropriate column header.

	freq_data_var = data[ [ 'Room', 'InUse', 'Occ', 'Date', 'RLength'] ]
        dates_var = freq_data_var[ 'Date' ].unique()
        dates_var = dates_var[ np.logical_not( np.isnan( dates_var ) )]
        dates_var = np.sort(dates_var)

        return freq_data_var, dates_var

#Saves data. In the future this may need to be changed to except an indefinite number of parameters.
#The column headings should be changes so the save file is more readable.
def save_file( results_data, data_file, stats ):

        print "Saving..."
        results_data.to_excel( data_file, ONE, cols = stats )

#Displays which dates will be processed. Useful for catching data entry errors. 
def display_dates( dates_var ):
	
	#Displays all dates in general format. Useful for determining if any date data is missing.
   	print "Dates to be processed..."
        print dates_var

#Does all the statistical calculations and then puts them into a data frame. May need to be further decomposed in the future, but is suitable for now.

def clean( data ):
	  
	for i in data.index:
		if data.loc[i, 'Reserved'] == 1:
			j = i + 16
			if j <= max( range ( len (data.index ) ) ):
				start_first = data.loc[ i, 'Start' ]
                                start_second = data.loc[ j, 'Start' ]
                                end_first = data.loc[i , 'End']
                                end_second = data.loc[j , 'End']
                                if ( start_first == start_second and end_first == end_second  ):
             				data.loc[j] = np.nan
	return data

#This function should be reevaluated so that functional composition is maintained.
#Right now it duplicates processes found in other functions which is unnecessary. 
#At the moment the save file name is hardcoded. This should be amended as soon as possible.

def process_all( use_data ):

	inUse = use_data[ ['InUse', 'Occ'] ].dropna()
	occ = use_data[ use_data[ 'InUse' ] == 1 ]
        inUse = inUse[ 'InUse' ]
        print occ
        se = st.sem( occ )
        occ_int = se * st.t._ppf( (1+.95)/2, len( occ )-1 )
        occ_lci = occ.mean()-occ_int
        occ_uci = occ.mean()+occ_int
     	interval = abba.stats.confidence_interval_on_proportion ( inUse.mean()*inUse.count(), inUse.count(), .95 )
        iu_lci = interval[1]
        iu_uci = interval[2]

	room_stats = pd.DataFrame( { 'InUse_Observations':inUse.count(),\
 	'InUse_Mean':inUse.mean(), 'InUse_STD':inUse.std(), 'InUse_LCI':iu_lci,\
	'InUse_UCI':iu_uci}, columns = freq_stats, index = [1] )
 
 	return room_stats, freq_stats

#Returns stats on how often 0, 1 and more than one person are observed using a group study room

def process_count_freq( freq_data ):
	
        use_occ_data = freq_data[ ['InUse', 'Occ'] ]
        use_occ_data = use_occ_data.dropna()
	total = use_occ_data[ 'Occ' ].count()
        occ_zero = use_occ_data[ use_occ_data[ 'Occ' ] == 0 ]
	occ_one = use_occ_data[ use_occ_data[ 'Occ' ] == 1 ]
	occ_two = use_occ_data[ use_occ_data[ 'Occ' ] >= 2 ]

	#These are for confirming that the data frames
	#contain what they are supposed to contain. Remove
	#them when everything is finished. Each one should
	#be empty.

	#print occ_zero[ occ_zero['Occ'] != 0 ]
	#print occ_one[ occ_one[ 'Occ' ] != 1 ]
	#print occ_two[occ_two[ 'Occ' ] > 1]

	
	zero_stats = confidence_int( occ_zero, total, 0 )
	one_stats = confidence_int( occ_one, total, 1 )
	two_stats = confidence_int( occ_two, total, 2 )
	res_list = [ zero_stats, one_stats, two_stats ]
	final_res = pd.concat( res_list )

	return final_res, occ_stats

def confidence_int( occ_data, count, index_value ):
	
	occ_data = occ_data[ 'Occ' ].count()
	prop_data = float( occ_data )/float( count )

        interval = abba.stats.confidence_interval_on_proportion ( occ_data, count, .95 )
        occ_lci = interval[1]
        occ_uci = interval[2]

	prop_std = math.sqrt( ( prop_data * (1 - prop_data )/ count ))  

	stats = pd.DataFrame( {'Occupant_Observations': occ_data,\
	'Occupant_Proportion': prop_data, 'Occupant_STD': prop_std,\
	'Occupant_Lower_Confidence_Interval': occ_lci,\
	'Occupant_Upper_Confidence_Interval': occ_uci  }, columns = occ_stats, index = [index_value] )

	return stats

def process( freq_data, dates ):

	freq_pieces = []

	for i in ROOMS:

		# This block computes the statistics for InUse and Occ.

                rLength_pieces = []
                print "Processing", i
                use_data = freq_data[ freq_data[ 'Room' ] == i ]
                inUse = use_data[ 'InUse' ]
                occ = use_data[ use_data[ 'InUse' ] == 1 ]
                occ = occ[ 'Occ' ]
                occ = occ.dropna()
                se = st.sem( occ )
                occ_int = se * st.t._ppf( (1+.95)/2, len( occ )-1 )
                occ_lci = occ.mean()-occ_int
                occ_uci = occ.mean()+occ_int
                interval = abba.stats.confidence_interval_on_proportion ( inUse.mean()*inUse.count(), inUse.count(), .95 )
                iu_lci = interval[1]
                iu_uci = interval[2]

                # This block adds up the the reserved time for each day

                for j in dates:
			if j > START:
                                lengths = use_data[ use_data[ 'Date' ] == j ].dropna()
                                rLength = lengths[ 'RLength' ].sum()
                                rLength_pieces.append( rLength )
		
		
		# If the file contains no rLength data, the relevant fields must be set to 0.

                #if dates.max() < START:
                 #      print dates.max()
                  #     rLength_pieces = [0]

                # The reserved time for each day is averaged and then the appropriate statistics
                # are calculated.

                rLength_n = len( rLength_pieces )
                length_sum = np.sum( rLength_pieces )
                length_mean = ( length_sum / rLength_n )
                length_std = np.array( rLength_pieces ).std()
                s_e = st.sem( rLength_pieces )
                length_int = s_e * st.t._ppf( (1+.95)/2, len( rLength_pieces)-1 )
                length_lci = length_mean - length_int
                length_uci = length_mean + length_int
		#minutes_per_day_obv = len( rLength_pieces )
		#max_minutes = max( rLength_pieces )
		
		# If the file contains no rLength data, the relevant fields must be set to 0.	
		if dates.max() < START:
			print dates.max()
			print "No reservation length data recorded\n"
			minutes_per_day_obv = 0
			max_minutes = 0
			length_mean = 0
			length_std = 0
			length_lci = 0
			length_uci = 0
		else:
			minutes_per_day_obv = len( rLength_pieces )
                	max_minutes = max( rLength_pieces )
	
	
                # The stats for each room are then stored in a one-row dataframe, which are then concatenated
                # into a single dataframe.

		room_stats = pd.DataFrame( { 'InUse_Observations':inUse.count(), 'InUse_Mean':inUse.mean(), 'InUse_STD':inUse.std(), 'InUse_LCI':iu_lci, 'InUse_UCI':iu_uci, 'Occupant_Observations' : occ.count(), 'Occupant_Mean': occ.mean(), 'Occupant_STD' : occ.std(), 'Occupant_LCI' : occ_lci, 'Occupant_UCI': occ_uci, 'Occupant_Max': occ.max() , 'Minutes_per_Day_Observations': minutes_per_day_obv , 'Minutes_per_Day_Mean': length_mean, 'Minutes_per_Day_STD': length_std, 'Minutes_per_Day_LCI': length_lci, 'Minutes_per_Day_UCI': length_uci, 'Minutes_per_Day_Max': max_minutes }, index = [i] )

                freq_pieces.append( room_stats )

	results_data = pd.concat( freq_pieces )

        anova_occ = results_data[ ['Occupant_Observations', 'Occupant_Mean', 'Occupant_LCI', 'Occupant_UCI', 'Occupant_STD'] ]
        anova_occ = anova_occ.sort(['Occupant_Mean', 'Occupant_LCI', 'Occupant_UCI', 'Occupant_Observations', 'Occupant_STD'])
        anova_rLength = results_data[ ['Minutes_per_Day_Observations', 'Minutes_per_Day_Mean', 'Minutes_per_Day_LCI', 'Minutes_per_Day_UCI', 'Minutes_per_Day_STD']]
        anova_rLength = anova_rLength.sort( ['Minutes_per_Day_Mean', 'Minutes_per_Day_LCI', 'Minutes_per_Day_UCI', 'Minutes_per_Day_Observations', 'Minutes_per_Day_STD'])

        #print "printing sorted occupant means..."
        #print "\n\n\n"
        #print anova_occ
        #print "\n\n\n"

        #print "printing sorted reservations time means..."
        #print "\n\n\n"
        #print anova_rLength
        #print "\n\n\n"

        #print results_data[ ['InUse_Observations', 'InUse_Mean', 'InUse_STD', 'InUse_LCI', 'InUse_UCI'] ]
        #print results_data[ ['Occupant_Observations', 'Occupant_Mean', 'Occupant_STD', 'Occupant_LCI', 'Occupant_UCI', 'Occupant_Max'] ]
        #print results_data[ ['Minutes_per_Day_Observations', 'Minutes_per_Day_Mean', 'Minutes_per_Day_STD', 'Minutes_per_Day_LCI', 'Minutes_per_Day_UCI', 'Minutes_per_Day_Max'] ]

        return results_data, anova_occ, anova_rLength, stats


