import time
from keras.layers import LSTM, GRU, Dropout, Dense, Input,\
                                        Activation, Bidirectional, Flatten, LeakyReLU
from keras.models import Model, Sequential, load_model
from keras.callbacks import TensorBoard, CSVLogger, EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from attention_wrapper import Attention
from constants import batch_size, epochs, learning_rate, dropout
import os
from StockNest.celery import app 
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

@app.task(blind=True)
def build_LSTMmodel(sequence_length, prediction_length , embedding_dim=1):
    print "model build started"
    model = Sequential()
    # modelInput = Input(shape=(sequence_length, embedding_dim), name='modelinput')

    # model.add(modelInput)

    model.add(LSTM(128, input_shape=(sequence_length, embedding_dim), return_sequences=True))
    # model.add(Activation('relu'))
    model.add(Dropout(dropout))
    model.add(Bidirectional(LSTM(64, return_sequences=True)))
    # model.add(Activation('relu'))
    model.add(Dropout(dropout))
    model.add(Flatten())
    model.add(Dense(128, activation='sigmoid'))
    model.add(Dropout(dropout))
    model.add(Dense(64,  activation='sigmoid'))
    model.add(Dropout(dropout))
    model.add(Dense(prediction_length, activation='sigmoid'))
    startComp = time.time()
    model.compile(loss='mean_squared_logarithmic_error',optimizer='rmsprop',metrics=['mae', 'acc'])
    model.summary()
    print "Net Compilation Time: {}sec".format(time.time() - startComp)
    return model

@app.task(blind=True)
def trainNetwork(trainData, trainLabels, \
                        testData, testLabels, model, company,\
                        epochs=500, batch_size=256):
    startTrain = time.time()
    if not os.path.exists("./results"):
        os.mkdir("./results")

    print("./results/"+company)
    if not os.path.exists("./results/"+company):
        os.mkdir("./results/"+company )
        os.mkdir("./results/"+company+"/bestmodels")

    checkpointer = ModelCheckpoint(filepath="./results/"+company+"/bestmodels/fn_model.{epoch:02d}-{val_acc:.2f}.hdf5",\
                                     verbose=1, monitor='val_acc', save_best_only=True, save_weights_only=False, mode='max', period=1)
    tf_board = TensorBoard(log_dir='./results/'+company+'/logs', histogram_freq=0, write_graph=True, write_images=True)
    csv_logger = CSVLogger('./results/'+company+'training.log')
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.001)
    early_stopping = EarlyStopping(monitor='val_loss', patience=50)

    model_info = model.fit(trainData, trainLabels, epochs=epochs, batch_size=batch_size,\
                                validation_split=0.1, callbacks=[tf_board, csv_logger, early_stopping, checkpointer, reduce_lr], verbose=1)
    print "Total training period for company {} is: {}sec".format(company, (time.time()-startTrain))
    startTest = time.time()
    test_mse, test_mae, test_acc = model.evaluate(testData, testLabels, batch_size=batch_size)
    print "Total testing period for company {} is: {}sec; test mse: {}; test mae: {}".\
                                                        format(company, (time.time() - startTest), test_mse, test_mae)
    # model prediction for graph 
    pred = model.predict(testData, batch_size=batch_size)
    print (pred)
    return model_info.history, test_mse, test_mae, test_acc, model, pred, testLabels

# @app.task(blind=True)
def predictOutput(modelpath, data):
    print modelpath
    model = load_model(modelpath)
    predictions = model.predict(data)
    return predictions

import tweepy
import requests
from textblob import TextBlob
from constants import Twitter_consumer_key, Twitter_consumer_secret,\
                                    Twitter_access_token, Twitter_access_token_secret,\
                                    TOI_api_key, TOI_top_news_end_point, TOI_business_end_point

@app.task(blind=True)
def getTweetDetails(company, date):
    auth = tweepy.OAuthHandler(Twitter_consumer_key, Twitter_consumer_secret)
    auth.set_access_token(Twitter_access_token, Twitter_access_token_secret)
    print ("[{}] collecting tweets company: {}".format(os.getpid(), company))
    api = tweepy.API(auth)
    public_tweets = api.search(company)
    info, rtcount, tsub, tpol = [], [], [], []
    for tweet in public_tweets:
        if not tweet.retweeted:
            info.append(tweet.text)
            rtcount.append(tweet.retweet_count)
            analysis = TextBlob(tweet.text)
            tpol.append(analysis.sentiment.polarity)
            tsub.append(analysis.sentiment.subjectivity)
    return info, rtcount, tsub, tpol

@app.task(blind=True)
def getNewsDetails(company, date):
    latestData = requests.get(TOI_business_end_point+TOI_api_key)
    print ("[{}] collecting news company: {}".format(os.getpid(), company))
    ni, ns, np = [], [], []
    for data in latestData.json()['articles']:
        news = TextBlob(data['title']+data['description'])
        if news.words.count(company, case_sensitive=False):
            ni.append(data['title']+data['description'])
            ns.append(news.sentiment.subjectivity)
            np.append(news.sentiment.polarity)
    return ni, ns, np

# TODO: very important to bias the users towards profit
# TODO: Find very strong way to segrigate, metric(very strong set of rules)
def customMetric():
    pass