#!/usr/bin/env python

# append.py
# Paul Gelbach
# Overview: append.py reads in data from excel files, cleans it, and displays some of the data entry errors
# and then stores all of the data in an excel file called gsrd.xls

import pandas as pd
import numpy as np
#import csv
#import openpyxl
from os import listdir
from os.path import isfile, join



def append():

    ONE = 'Sheet1'
    
    # headers refers to the columns of the excel files. Any changes to the columns must be reflected in headers.
    headers = [ 'Date', 'Day', 'Time', 'Floor', 'Room', 'Reserved', 'InUse', 'Occ', 'Start', 'End', 'Remaining', 'AdHoc', 'Size', 'Quarter', 'Finals', 'RLength' ]
    
    # 'gsrd.xls' stores the data after it has been processed. It is meant to contain all of the recorded data.
    data_file = "results/gsrd.xls"
    # readapp() is the sole function of this program and carries out the operations described above. It needs to be
    # further decomposed so that it only combines all the data and then returns all the data. A second function should
    # handle storing the data to a file. Also, appending to a dataframe at the end of each pass is not the most
    # effiecient way to perform this task; each excel file should get its own data frame, which should be appended
    # to a list. The complete list should be concatenated into a single data frame.
    
    regress_data = pd.DataFrame( columns = headers )
    direct = "gsr_excel_files/"
    nameList = [f for f in listdir( direct ) if isfile(join(direct, f)) ]
                           
	# The filenames are stored in a list.
	#nameList = []
     #   with open( NAMES ) as filenames:
	#	reader = csv.reader( filenames, quotechar='|' )
	#	for row in reader:
	#		nameList.append( ','.join(row) )
	#print nameList
    print "Reading in files..."
    # For each name in the list, a file is opened, and then put into the main dataframe.
    for i in nameList:
        print "File now being read: ", i
        name = i
        dir_name = direct + name
        xls_file = pd.ExcelFile( dir_name )
        table = xls_file.parse( ONE )
        room_data = pd.DataFrame( table, columns = headers )		
		
		# Data entry errors are detected by this block
        for i in room_data.index:
            if room_data.loc[ i, 'Reserved' ] > 1:
                print i, "Reserved"
            if room_data.loc[ i, 'InUse' ] > 1:
                print i, "InUse"
            if room_data.loc[ i, 'AdHoc' ] > 1:
                print i, "AdHoc"
            if room_data.loc[i, 'RLength'] > 121:
                print i, "RLength"
            if room_data.loc[i, 'RLength'] < -1:
                print i, "RLength"
		
		# Reservations that have been counted twice are removed by this block.
        for i in room_data.index:
            if room_data.loc[ i, 'Reserved' ] == 1:
                j = i + 16
                if j <= max( range ( len (room_data.index ) ) ):
                    start_first = room_data.loc[i , 'Start']
                    start_second = room_data.loc[ j , 'Start' ]
                    end_first = room_data.loc[ i, 'End' ]
                    end_second = room_data.loc[j , 'End']
                    if ( start_first == start_second and end_first == end_second ):
                        room_data.loc[j] = np.nan
                if room_data.loc[i, 'RLength' ] > 120:
                    room_data.loc[i] = np.nan
        regress_data = regress_data.append( room_data )
	
    regress_data = regress_data.reset_index()
    print regress_data
	
# Data is saved to an excel file.
    regress_data.to_excel( data_file, ONE, cols = headers )	

def main():
	append()

if __name__== "main()":
	append()
