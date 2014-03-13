#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, csv, numpy

Earnings = {}

TimeSection = []
BeginTime = 0
EndTime = 0

MaxOpenNum = 0

def getOpenNum(time):
	num = 0
	for section in TimeSection:
		if time > section[0] and time < section[1]:
			num = num + 1
	return num

def loadEarningsFun():
	global Earnings, TimeSection, BeginTime, EndTime, MaxOpenNum
	reader = csv.reader(open("tradePointsFinal.csv"))
	for line in reader:
		if Earnings.has_key(line[0]):
			Earnings[line[0]].append(float(line[-1]))
		else:
			Earnings[line[0]] = [float(line[-1])]
		#计算最大持仓对数
		TimeSection.append((float(line[3]), float(line[5])))
		if not BeginTime and not EndTime:
			BeginTime, EndTime = float(line[3]), float(line[5])
		if float(line[3]) < BeginTime:
			BeginTime = float(line[3])
		if float(line[5]) > EndTime:
			EndTime = float(line[5])
	for time in numpy.arange(BeginTime, EndTime, 1000):
		num = getOpenNum(time)
		if num > MaxOpenNum:
			MaxOpenNum = num
	print MaxOpenNum

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

	#loadPairFun(pairs)


if __name__ == '__main__':
	main()