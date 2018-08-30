# simple graph just using MLP for prediction
import tensorflow as tf
import matplotlib.pyplot as plt2
import input_data
import numpy as np
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from funcs import defineVariables, preActivation, save


def take_input():
	company_str = input("Enter company name for training:  ")

	while not os.path.exists("../csv-data/gainers/"+ company_str + ".NS.csv"):
		print "Company not found"
		company_str = input("Enter company name for training:  ")
	return company_str

# Create Directory if doesn't exist
def create_directory(company_str): 
	if not os.path.exists("../modeldata/"+ company_str):
		os.mkdir("../modeldata/"+company_str)

	if not os.path.exists("../modeldata/"+company_str+"/weights"):
	    os.mkdir("../modeldata/"+company_str+"/weights")

	if not os.path.exists("../modeldata/"+company_str+"/biases"):
	    os.mkdir("../modeldata/"+company_str+"/biases")

	if not os.path.exists("../modeldata/"+company_str+"/logs"):
	    os.mkdir("../modeldata/"+company_str+"/logs")

# placeholders
def define_placeholders(sequence_length, prediction_length):
	seq_input = tf.placeholder(tf.float32,
				shape = (None, sequence_length),
				name="input_to_model")

	seq_output = tf.placeholder(tf.float32, 
				shape = (None, prediction_length), 
				name= "output_of_model")

	keep_prob = tf.placeholder(tf.float32)
	return seq_input, seq_output, keep_prob

def load_company_data(company_str):
	company = input_data.load_data(company = company_str)
	return company

def print_status(learning_rate, batch_size, epochs, company_str):
	print "COMPANY NAME = {}".format(company_str)+\
		  ", LEARNING RATE = {}".format(learning_rate)+\
		  ", BATCH SIZE = {}".format(batch_size)+\
		  ", EPOCHS = {}".format(epochs)

	print "#####################################################################"

def declare_variables(sequence_length, prediction_length, variables_device, company_str):
	with tf.device(variables_device):
		weights = {
			'layer1' : defineVariables([sequence_length, sequence_length//2], company_str+'wc1'),
			'layer2' : defineVariables([sequence_length//2, prediction_length], company_str+'wc2')
		}
		biases = {
			'layer1': defineVariables([sequence_length//2], company_str+'bc1'),
			'layer2': defineVariables([prediction_length], company_str+'bc2')
		}
	return weights, biases

def model(seq_input, weights, biases, keep_prob, company_str):
	with tf.variable_scope(company_str+'MLP_layer1') as scope:
		pre_activation = preActivation(seq_input, weights['layer1'], biases['layer1'])
		activation = tf.nn.sigmoid(pre_activation)
		dropout_layer = tf.nn.dropout(activation, keep_prob, name="dropout2")

	with tf.variable_scope(company_str+'MLP_layer2') as scope:
		pre_activation = preActivation(dropout_layer, weights['layer2'], biases['layer2'])
		output = pre_activation
	return output

def p_values(seq_output, predictions):
	total_error = tf.reduce_sum(tf.square(tf.subtract(seq_output, tf.reduce_mean(seq_output))))
	unexplained_error = tf.reduce_sum(tf.square(tf.subtract(seq_output, predictions)))
	R_squared = tf.subtract(tf.div(total_error, unexplained_error),1.0)
	R = tf.multiply(tf.sign(R_squared),tf.sqrt(tf.abs(unexplained_error)))

	MAPE = tf.reduce_mean(tf.abs(tf.div(tf.subtract(seq_output, predictions), seq_output)))
	RMSE = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(seq_output, predictions))))
	return total_error, unexplained_error, R_squared, R, MAPE, RMSE

def model_compilation(output, seq_output, learning_rate, weights):
	start_time = time.time()
	saver = tf.train.Saver()

	# use MSE for cost function
	cost = tf.losses.mean_squared_error(output, seq_output)
	tf.summary.scalar("cost", cost)

	# regularization term L2 normalization for loss calculation
	# conc
	regularizer = tf.nn.l2_loss(weights['layer1']) +\
				  tf.nn.l2_loss(weights['layer2'])
	reg_loss = tf.reduce_mean(cost + 1e-4 * regularizer)

	# optimizer function using RMSProp/ Adam optimizer
	optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(reg_loss)
	print "Compilation time:  {}sec".format(time.time() - start_time)
	
	return saver, optimizer, cost

def run_model(init, output, saver, IS_RESTORE_BASED, company_str, company, epochs, seq_input, seq_output, keep_prob, dropout, optimizer, cost, batch_size, prediction_length,sequence_length, processing_device, display_steps, weights, biases, total_error, unexplained_error, R_squared, R, MAPE, RMSE):
	merged = tf.summary.merge_all()
	with tf.device(processing_device):
		with tf.Session() as sess:
			if IS_RESTORE_BASED:
				saver.restore(sess, "../modeldata/"+company_str+"/logs/model.ckpt")

			sess.run(init)
			train_writer = tf.summary.FileWriter('../modeldata/'+company_str+'/logs/', sess.graph)

			train_start = time.time()
			step = 1
			while company.train.epochs_completed <= epochs:
				step += 1
				company_data, company_labels = company.train.next_batch()
				output_data = np.reshape(company_labels.T[1].T, (batch_size, prediction_length))

				_, loss, rsq, r, te, une, mape, rmse = sess.run([optimizer, cost, R_squared, R, total_error, unexplained_error, MAPE, RMSE], feed_dict={seq_input: company_data.T[1].T, seq_output: output_data, keep_prob: dropout})

				if step % display_steps == 0:
					print "Epochs completed: {}".format(company.train.epochs_completed) +\
					 				"  loss: {}".format(loss) + "  step: {}".format(step)

				if company.train.epochs_completed == epochs - 1:
					p_valfile = open("../graphdata/"+company_str+"_pval.js", "w")
					p_valfile.write("var " + company_str + "_total_error = " + str(te) + ";")
					p_valfile.write("var " + company_str + "_unexplained_error = " + str(une) + ";")
					p_valfile.write("var " + company_str + "_R_squared = " + str(rsq) + ";")
					p_valfile.write("var " + company_str + "_R = " + str(r) + ";")
					p_valfile.write("var " + company_str + "_MAPE = " + str(mape) + ";")
					p_valfile.write("var " + company_str + "_RMSE = " + str(rmse) + ";")
					p_valfile.close()

			print "Optimization Completed. Training time:  {}sec".format(time.time() - train_start)	
			# save weights, biases, model:
			save(sess.run(weights['layer1']), "../modeldata/"+company_str+"/weights/layer1")
			save(sess.run(weights['layer2']), "../modeldata/"+company_str+"/weights/layer2")
			save(sess.run(biases['layer1']), "../modeldata/"+company_str+"/biases/layer1")
			save(sess.run(biases['layer2']), "../modeldata/"+company_str+"/biases/layer2")
			save_path = saver.save(sess, "../modeldata/"+company_str+"/logs/model.ckpt")
			
			test_data, test_labels = company.test.next_batch()
			test_labels = np.reshape(test_labels.T[1].T[:15], (15, prediction_length))
			test_data = np.reshape(test_data.T[1].T[:15], (15, sequence_length))
			
			predictions = sess.run(output, feed_dict={seq_input: test_data, keep_prob: 1.0})

			

			predictions = np.reshape(predictions, (15, prediction_length))

	        labels, pred = [], []
	        for data, label, prediction in zip(test_data, test_labels, predictions):
	        	labels.append(np.concatenate((data,label), 0).tolist())
	        	pred.append(np.concatenate((data, prediction),0).tolist())

	        final_data, final_label = [], []
	        temp = 1
	        for d, l in zip(labels, pred):
	        	final_data.append(d[0])
	        	final_label.append(l[0])
	        	final_data[:-1] += pred[temp - 1:][0]
	        	final_label[:-1] += labels[temp - 1:][0]
	        	temp +=1
	        	# print temp

	        error = 0.05
	        resultfile = open("../resultfile.txt", "a")
	        if pred[0][len(pred[0]) - 2] > (pred[0][len(pred[0]) - 1] + error):
	        	res_str =  "CLOSING PRICE WILL GO UP FOR "+ company_str +" >> BUY MORE SHARE..."
	        else:
	        	res_str = "CLOSING PRICE WILL GO Down FOR "+ company_str +" >> SELL MORE SHARE..."

	        resultfile.write(res_str)
	        resultfile.write("\n")

	        plt2.plot(test_labels.T[0][:-1], color='red', label='prediction')
	        plt2.plot(predictions.T[0][1:], color='blue', label='actual')
	        plt2.title(company_str)
	        plt2.xlabel('days')
	        plt2.ylabel('normalized closing prices')
	        plt2.legend(loc='upper left')
	        plt2.savefig("../graph/prediction"+company_str+".png")
	        plt2.close()

	        datafile = open("../graphdata/"+company_str+"_data.js", "w")
	        labelfile = open("../graphdata/"+company_str+"_label.js", "w")
	        datafile.write("var " +company_str+"_CLOSING_PRICE_DATA = [ 0")
	        labelfile.write("var " +company_str+"_CLOSING_PRICE_LABEL = [ 0")
	        for dat, lab in zip(final_data[:-1], final_label[:-1]):
	        	datafile.write(", '")
	        	labelfile.write(", '")
	        	datafile.write(str(dat))
	        	labelfile.write(str(lab))
	        	datafile.write("'")
	        	labelfile.write("'")
	        
	        datafile.write(" ];")
	        labelfile.write(" ];")

	        datafile.close()
	        labelfile.close()
	        print "Completed....."