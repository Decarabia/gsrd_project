#!/usr/bin/env python

import pandas as pd
import numpy as np


headers = [ 'Date', 'Day', 'Time', 'Floor', 'Room', 'Reserved', 'InUse', 'Occ', 'Start', 'End', 'Remaining', 'AdHoc', 'Size', 'Quarter', 'Finals' ]
file_name = 'gsrd.xls'
ONE = 'Sheet1'
save_file = 'corr_result.xls'
indices =  ['Day', 'Time', 'Floor', 'Reserved', 'Size', 'Quarter', 'Finals', 'InUse']

def readIn():

        temp_data = pd.read_excel( file_name, ONE, names = headers, headers = None )
        regress_data = temp_data[ indices ]
        regress_data = regress_data.dropna()
	print regress_data.corr()
        result = regress_data.corr()
	result.to_excel( save_file, ONE )	
	
def main():	
	
	readIn()	

if __name__== "__main__":
	main()

