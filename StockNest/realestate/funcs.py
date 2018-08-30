import pandas as pd
import math
import numpy as np

def csv2json(path):
	df = pd.read_csv(path)
	df = df.dropna(axis=0, how='any')
	return_data = [{"pid":parcelid, "lat": latitude, "log": longitude, "rid":regionidzip,"sqfeet":lotsizesquarefeet} for parcelid, latitude, longitude, regionidzip, lotsizesquarefeet in zip(df['parcelid'].as_matrix(), df['latitude'].as_matrix(), df['longitude'].as_matrix(), df['regionidzip'].as_matrix(), df['lotsizesquarefeet'].as_matrix())]
	return return_data

def logerror2price(ppty, error):
	return np.exp(error + np.log(ppty.price))