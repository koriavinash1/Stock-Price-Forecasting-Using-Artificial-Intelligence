epochs = 500
batch_size = 25
dropout = 0.2
variables_device = "/cpu:0"
processing_device = "/cpu:0"

sequence_length = 20 # input timesteps 
learning_rate = 1e-3
prediction_length = 2 # expected output sequence length
embedding_dim = 5 # input dimension total number of features in our case

## BOSHLTD/ MICO same....

COMPANIES = ['EICHERMOT',  'BOSCHLTD', 'MARUTI', 'ULTRACEMCO', 'HEROMOTOCO',\
		 	'TATAMOTORS', 'BPCL', 'AXISBANK', 'TATASTEEL', 'ZEEL',\
				'CIPLA', 'TATAPOWER', 'BANKBARODA', 'NTPC', 'ONGC'];

Twitter_consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
Twitter_consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' 

Twitter_access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
Twitter_access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

TOI_api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
TOI_top_news_end_point = 'https://newsapi.org/v1/articles?source=cnbc&sortBy=top&apiKey='	

TOI_business_end_point  = 'https://newsapi.org/v1/articles?source=cnbc&sortBy=top&apiKey='
