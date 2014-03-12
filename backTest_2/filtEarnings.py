#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, csv

Earnings = {}


def loadEarningsFun():
	global Earnings
	reader = csv.reader(open("tradePointsFinal.csv"))
	for line in reader:
		if Earnings.has_key(line[0]):
			Earnings[line[0]].append(float(line[-1]))
		else:
			Earnings[line[0]] = [float(line[-1])]

def getAllEarningFun():
	global Earnings
	result =[]
	for stockKey, Earning in Earnings.items():
		_earning = 0
		for data in Earning:
			_earning = _earning + data
		Earning = _earning

		result.append((stockKey, Earning))

	return result

#读取配对参数
def loadPairFun(pairs):
	filtPara = ""
	reader = csv.reader(open("results.csv"))
	for line in reader:
		if line:
			if line[0] in pairs:
				for data in line:
					filtPara = filtPara + str(data) + ","
				filtPara = filtPara + "\n"

	logFile = open("filtPara.csv", "a")
	logFile.write(filtPara)
	logFile.close()

def main():
	#读取价格
	loadEarningsFun()

	result = getAllEarningFun()

	result = sorted(result, key=lambda d:d[1])

	#print result[-20:], len(result[-10:])

	print result, len(result)

	pairs = []
	for x in result:
		pairs.append(x[0])

	#loadPairFun(pairs)


if __name__ == '__main__':
	main()