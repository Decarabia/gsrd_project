#!/usr/bin/env python

import pandas as pd
from statsmodels import api as sm
from patsy import dmatrices
import numpy as np

headers = [ 'Date', 'Day', 'Time', 'Floor', 'Room', 'Reserved', 'InUse', 'Occ', 'Start', 'End', 'Remaining', 'AdHoc', 'Size', 'Quarter', 'Finals', 'RLength' ]
file_name = "gsrd.xls"
ONE = "Sheet1"
save_file = "regression_results.xls"

def readIn():
	
	temp_data = pd.read_excel( file_name, ONE, names = headers, headers = None )
	regress_data = temp_data[  [ 'Time', 'Room', 'Reserved', 'Occ' ] ]
	regress_data = regress_data.dropna()
	regress_data = regress_data.reset_index()
	print regress_data	
	
	return regress_data

def regression( data_df ):
	
	result_list = []
	rooms = data_df[ 'Room' ].drop_duplicates()
	
	for i in rooms:
		room_data = data_df[ data_df[ 'Room'] == i ]
		y, X = dmatrices( 'Occ ~ Time + Reserved ', data=room_data, return_type = "dataframe")
		mod = sm.OLS(y, X)
		res = mod.fit()
		print res.summary()
		final = expResults( res )
		final_df = pd.DataFrame( final )
		result_list.append( final_df )
	
	final_result = pd.concat( result_list )
	final_result.to_excel( save_file, ONE )

def expResults( results ):

	stats = pd.Series( { 'r2': results.rsquared, 'adj_r2': results.rsquared_adj } )
	results_df = pd.DataFrame( {'params': results.params,
				    'pvals': results.pvalues,
				    'std': results.bse,
				    'statistics': stats } )
	
	fisher_df = pd.DataFrame( {'params': { '_f_test': results.fvalue}, 'pvals': {'_f_test': results.f_pvalue } } )
	res_series = pd.concat( [results_df, fisher_df]).unstack()	
	return res_series.dropna()


def main():

	#headers = [ 'Date', 'Day', 'Time', 'Floor', 'Room', 'Reserved', 'InUse', 'Occ', 'Start', 'End', 'Remaining', 'AdHoc', 'Size', 'Quarter', 'Finals', 'RLength' ]
	#file_name = 'gsrd.xls'
	#ONE = 'Sheet1'
	#save_file = 'regression_results.xls'

	
	print "processing beginning...."
	data_df = readIn().copy()
	regression( data_df )
	
	#y,X=dmatrices( 'Occ ~ Day + Time + Size + Quarter + Reserved + Finals + Floor', data=data_df, return_type= "dataframe" )
	#print "...printing y..."
	#print "...printing X...."
	#print y
	#print X
	#mod = sm.OLS(y, X)
	#res = mod.fit()
	#print res.summary()
	#final = expResults( res )
	#final_df = pd.DataFrame( final )
	#final_df.to_excel( save_file, ONE )

if __name__== "__main__":
	main()

	
