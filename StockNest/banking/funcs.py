import pandas as pd
import json

def csv2json(path):
	data = pd.read_csv(path)
	headers = list(data)
	return_list = [json.loads(data.iloc[i].to_json()) for i in range(len(data))]
	return return_list, headers
