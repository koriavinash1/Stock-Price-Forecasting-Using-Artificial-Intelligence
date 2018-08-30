import pandas as pd

def csv2json(path):
	df = pd.read_csv(path)
	return_data = [{"date":date, "INR/gms": price} for date, price in zip(df['Date'].as_matrix(), df['INR(/grms)'].as_matrix())]
	return return_data