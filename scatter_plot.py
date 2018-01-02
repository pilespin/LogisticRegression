#!/usr/bin/python

import csv
import sys
import math

from Dataset import *

import numpy as np
import matplotlib.pyplot as plt

import time
import sys

def checkArg(argv):
	if len(sys.argv) <= 1:
		print "Missing file"
		exit(1)

	file = sys.argv[1]

	try:
		open(file, 'r')
	except IOError:
		print "Can't read: " + file
		exit(1)
	return (file)

def addFeatureOnSubplot(index, X, name, indexSubplot):

	color = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
		  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
		  '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
		  '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
		  '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
		  '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
		  '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
		  '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
		  '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
		  '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']

	ax = plt.subplot(2, 2, indexSubplot)
	plt.tight_layout()
	ax.set_xlim([-10, len(X) + 10])

	Xs = sorted(X)
	clr = color[index]
	plt.scatter(np.arange(len(X)), X, color=clr, alpha=0.5, label=name)
	plt.scatter(np.arange(len(X)), Xs, color=clr, alpha=0.5)
	plt.legend()
	plt.ylabel('Worst <---> Best')
	# plt.xlabel('Evaluation')

def main():

	file = checkArg(sys.argv)

	d = Dataset()

	d.loadFile(file)

	fig, axes = plt.subplots(figsize=(18,10))
	fig.tight_layout()

	index = 6
	while index <= 18:
		
		mean = d.mean(d.getFeature(index))
		std = d.standardDeviation(d.getFeature(index), mean)

		if mean >= -10 and mean <= 10 and std >= -10 and std <= 10:
			addFeatureOnSubplot(index, d.getFeature(index), d.getName(index), 1)
		elif mean >= -500 and mean <= 500 and std >= -500 and std <= 500:
			addFeatureOnSubplot(index, d.getFeature(index), d.getName(index), 2)
		elif mean >= -2000 and mean <= 2000 and std >= -2000 and std <= 2000:
			addFeatureOnSubplot(index, d.getFeature(index), d.getName(index), 3)
		else:
			addFeatureOnSubplot(index, d.getFeature(index), d.getName(index), 4)

		index+=1


	# plt.title(d.getName(index))

	plt.savefig('scatter_plot.png')
	plt.show()


main()

