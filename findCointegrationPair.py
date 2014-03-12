#!/usr/bin/python
# -*- coding: utf-8 -*-
#findCointegrationPair.py
import os, csv, multiprocessing
import numpy as np
import ADF_Series

#读取分钟线数据
def loadBarDataFun():
	dataList = []
	list_dirs = os.walk("F:\\backTestData")
	for root, folders, files in list_dirs:
		for f in files:
			dataDate = f[:10]
			if dataDate > "2013-02-04" and dataDate < "2013-03-04":
				path = os.path.join(root, f)
				print path
				reader = csv.reader(open(path))
				firstLine = True
				for line in reader:
					if not firstLine:
						dataList.append(line)
					if not dataList and firstLine:
						dataList.append(line)
					firstLine = False
	return zip(*dataList)[1:]

def getSeries(data):
	series = []
	for num in data:
		if num == "None":
			series.append(0)
		else:
			series.append(float(num))
	return series

def creatADFSeriesFun(dataDict, data):
	print data[0]
	series = getSeries(data[1:])
	dataDict[data[0]] = ADF_Series.C_ADF_Series(True,series)
	print dataDict[data[0]].diffRank
	print dataDict[data[0]].model_1_param
	print dataDict[data[0]].model_2_param
	print dataDict[data[0]].model_3_param

def creatFile(dataDict):
	logFile = open("results.csv", "a")
	content = "stock, rank, model_1_delta_t, model_2_delta_t, model_3_delta_t\n"
	for stock, data in dataDict.items():
		content = "%s,%d,%f,%f,%f\n"%(stock, data.diffRank, 
			data.model_1_param["delta_t"], data.model_2_param["delta_t"], data.model_3_param["delta_t"])
	logFile.write(content)
	logFile.close()

def main():
	dataList = loadBarDataFun()
	dataDict = {}

	pool = multiprocessing.Pool(processes= int(multiprocessing.cpu_count()*0.4))
	for data in dataList:
		result = pool.apply_async(creatADFSeriesFun, (dataDict,data))
	pool.close()
	pool.join()

	creatFile(dataDict)



if __name__ == '__main__':
	main()