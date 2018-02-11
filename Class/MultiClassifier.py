#!/usr/bin/python3

from Math import *
from Classifier import *

import csv
from threading import Thread

class MultiClassifier(Math):

	allClassifier = []
	nbInput = 0
	nbOutput = 0
	nbClassifier = 0
	m = None

	def __init__(self, nbInput, allOutput):
		# print allOutput
		self.nbOutput = len(allOutput)
		self.nbInput = nbInput
		self.m = Math()
		for i,d in enumerate(allOutput):
			self.addClassifier(i, d)

	def printInfo(self):
		for i in self.allClassifier:
			i.printInfo()

	def addClassifier(self, number, nameOutput):
		cl = Classifier(self.nbInput, number, nameOutput)
		self.allClassifier.append(cl)
		self.nbClassifier = len(self.allClassifier)

	def predictAll(self, X):
		out = []
		for i,d in enumerate(self.allClassifier):
			out.append(d.predict(X))
		return np.array(out)

	def train(self, X, Y):

		### Without thread
		# allLoss = []
		# for i,d in enumerate(self.allClassifier):
		# 	# print("TRAIN" + str(i))
		# 	loss = d.train(X, Y, i)
			# allLoss.append(loss)

		##########################################################

		thread_list = []
		allLoss = []
		for i,d in enumerate(self.allClassifier):

			t = Thread(target=d.train, args=(X, Y, i))
			t.start()
			thread_list.append(t)

		for thread in thread_list:
			thread.join()

		for i,d in enumerate(self.allClassifier):
			allLoss.append(d.getLoss())

		return np.array(allLoss)

	def getNbClassifier(self):
		return self.nbClassifier

	def getMax(self, X):
		pr = self.predictAll(X)
		# print("PREDICT ALL: " + str(pr))
		return self.m.argMax(pr)

	def setLr(self, lr):
		for i,d in enumerate(self.allClassifier):
			d.setLr(lr)

	def saveWeight(self):
		All = []
		with open('weight', 'w+') as file:
			for i,d in enumerate(self.allClassifier):
				name = d.getOutputName()
				weight = d.getWeight()
				
				tmp = []
				tmp.append(name)
				for i in weight:
					tmp.append(i)
				All.append(tmp)

		with open('weight.csv', 'w+') as file:
			csvWriter = csv.writer(file, delimiter=',')
			csvWriter.writerows(All)
