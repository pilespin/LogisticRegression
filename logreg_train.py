#!/usr/bin/python

from Dataset import *
from Classifier import *
from MultiClassifier import *
from Math import *

import numpy as np
import csv
import sys	

from sklearn.metrics import accuracy_score

# import matplotlib.pyplot as plt

# np.set_printoptions(precision=4)
# np.set_printoptions(suppress=True)

def checkArg(argv):
	if len(sys.argv) <= 1:
		print("Missing file")
		exit(1)

	file = sys.argv[1]

	try:
		open(file, 'r')
	except IOError:
		print("Can't read: " + file)
		exit(1)
	return (file)

def csvToArray(file):
	file = open(file, "r")
	arr = csv.reader(file, delimiter=',')

	X = []
	Y = []

	i = 0
	for line in arr:
		i+=1
		if i!=1:
			X.append(line[0])
			Y.append(line[1])
	
	if len(X) != len(Y):
		print("Error")
		exit(1)
	
	return (X, Y)

#############################################################

def getHouseByIndex(d, index):
	house = d.getDataset()[index][1]
	return house

def getIndex(X, querie):
	i = 0
	for x in X:
		i+=1
		if x == querie:
			return int(i)
	return -1

def getInputInDataset(d, index, inFloat=False):
	start = 6
	end = 18

	X = []
	if inFloat == True:
		while start <= end:
			tmp = d.getDataset()[index][start]
			if len(tmp) > 0:
				X.append(float(d.getDataset()[index][start]))
			else:
				X.append(float(0))
			start += 1
	else:
		while start <= end:
			X.append(d.getDataset()[index][start])
			start += 1
	return np.array(X)

def generateDataset(d, index=-1):

	X = []
	Y = []

	houseArray = d.getFeature(1, uniq=True)

	for i in range(d.getLength()):
		x = getInputInDataset(d, i, inFloat=True)
		y = getIndex(houseArray, getHouseByIndex(d, i))

		if index == -1 or (y == index):
			X.append(x)
			Y.append([y])

	X = np.array(X)
	Y = np.array(Y)
	if len(X) != len(Y):
		print("Error when generate dataset")
		exit(1)
	return X, Y

def generatePrediction(allclassifier, X, Y):
	y_pred = []
	y_true = []
	m = Math()

	for i,x in enumerate(X):
		# for j,y in enumerate(x):
		output = allclassifier.getMax(x) + 1
		# print output
		# print Y[i][0]

		y_pred.append(output)
		y_true.append(Y[i][0])

	if len(y_true) != len(y_pred):
		print("Error when generate prediction")
		exit(1)

	return np.array(y_true), np.array(y_pred)


##############################
############ MAIN ############
##############################

def main():

	nbInput = 13
	nbOutput = 4

	file = checkArg(sys.argv)

	d = Dataset()
	d.loadFile(file)

	allclassifier = MultiClassifier(nbInput, nbOutput)

	X, Y = generateDataset(d)

	for i in range(nbOutput):
		allclassifier.addClassifier(i)

	oldLoss = 0
	allclassifier.setLr(0.01)

	for j in range(9999):
		loss = allclassifier.train(X, Y)
		pr = allclassifier.predictAll(X[0])
		mx = allclassifier.getMax(X[0])
		print(pr)
		print(mx)
		pr = allclassifier.predictAll(X[1])
		mx = allclassifier.getMax(X[1])
		print(pr)
		print(mx)
		allLoss = loss.sum()
		# print ('-----------------')
		# print (allLoss)
		# print (loss)

		# if abs(oldLoss) > abs(allLoss) and lr > 0.00001:
		# 	lr /= 10
		# 	print("DECREASE TO " + str(lr))
		# 	allclassifier.setLr(lr)
		# oldLoss = allLoss


		# aa = allclassifier.predictAll(X)
		# print(str(aa))

		allclassifier.saveWeight()
		
		# print(y_true)
		# print(y_pred)
		# print(loss)
	
		y_true, y_pred = generatePrediction(allclassifier, X, Y)

		# print(y_true)
		# print(y_pred)

		acc = accuracy_score(y_true, y_pred) * 100
		# print("epoch: {0:<15.5g} LOSS: {1:<15.5g} Accuracy: {2:<15.5g}" \
		# .format(j, allLoss, acc))
		print("epoch: {0:<15.5g} Loss1: {1:<15.5g} Loss2: {2:<15.5g} Loss3: {3:<15.5g} Loss4: {4:<15.5g} LOSS: {5:<15.5g} Accuracy: {6:<15.5g}" \
		.format(j, loss[0], loss[1], loss[2], loss[3], allLoss, acc))


main()
