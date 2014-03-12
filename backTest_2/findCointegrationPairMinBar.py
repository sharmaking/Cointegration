#!/usr/bin/python
# -*- coding: utf-8 -*-
#findCointegrationPair.py
import os, csv, multiprocessing
from scipy.optimize import leastsq
import numpy as np
import ADF_Series


Plate = {}
RZRQ = []
Results = {}
StockPrice = []

#读取股票价格
def loadStockPrice():
	global StockPrice
	reader = csv.reader(open("20140218.csv"))
	for line in reader:
		if line:
			if float(line[3]) > 7:
				StockPrice.append(line[0])
#读取板块
def loadPlateFun():
	global Plate
	reader = csv.reader(open("plate.csv"))
	for line in reader:
		num = 0
		plateName = ""
		for data in line:
			if not num:
				plateName = data
				if plateName == "rzrq:":
					break
				Plate[plateName] = []
			else:
				if data:
					Plate[plateName].append(data)
			num = num + 1
#读取融资融券标的
def loadRZRQStockFun():
	global RZRQ
	reader = csv.reader(open("rzrq.csv"))
	for line in reader:
		for data in line:
			if data:
				RZRQ.append(data)
#读取分钟线数据
def loadBarDataFun():
	barData = {}
	list_dirs = os.walk("F:\\HistoryData\\60")
	for root, folders, files in list_dirs:
		for f in files:
			dataDate = float(f[:8])
			if dataDate >= 20131001 and dataDate <= 20131201:
				path = os.path.join(root, f)
				reader = csv.reader(open(path))
				print path
				for line in reader:
					if line:
						stock = line[0]
						if stock in RZRQ:
							if not barData.has_key(stock):
								barData[stock] = {}
							if len(line[2]) == 5:
								line[2] = "0"+(line[2])
							barData[stock][line[1] + line[2]] = float(line[3])
	return barData
#判断是否在同一板块
def isInTheSamePlateFun(stock1,stock2):
	if stock1 == stock2:
		return False
	for plateName, stocks in Plate.items():
		if (stock1 in stocks) and (stock2 in stocks):
			#print "%s and %s is in the same Plate '%s'" %(stock1, stock2,plateName[:-1])
			return True
	return False

def creatADFSeriesNewFun(stockCode, dataDict, data):
	print stockCode
	dataDict[stockCode] = ADF_Series.C_ADF_Series(True,data)
	print dataDict[stockCode].diffRank
	print dataDict[stockCode].model_1_param
	print dataDict[stockCode].model_2_param
	print dataDict[stockCode].model_3_param

def creatFile(dataDict):
	logFile = open("results2.csv", "a")
	content = "stock, rank, model_1_delta_t, model_2_delta_t, model_3_delta_t\n"
	for stock, data in dataDict.items():
		content = "%s,%d,%f,%f,%f\n"%(stock, data.diffRank, 
			data.model_1_param["delta_t"], data.model_2_param["delta_t"], data.model_3_param["delta_t"])
	logFile.write(content)
	logFile.close()

#筛选配对股票
def stockPairSelectFun(key, X, Y):
	beta, isCointegration, MEAN, STD, _open, _close, _stopLoss = fittingSeriesFun(X, Y)
	print key, beta, MEAN, STD, isCointegration
	#if "beta < 1.3 and beta > 0.7" and STD < 0.03:
	#lock.acquire()
	logFile = open("results.csv", "a")
	content = "%s,%f,%f,%f,:,%f,%f,%f,%s\n"%(key, beta, MEAN, STD, _open, _close, _stopLoss, str(isCointegration))
	logFile.write(content)
	logFile.close()
	#lock.release()			
	pass
def getPairKeyFun(stock1, stock2, barData1, barData2):
	if stock1 > stock2:
		series = formatSeriesFun(barData1, barData2)
		return "%s-%s"%(stock1, stock2), series
	if stock1 < stock2:
		series = formatSeriesFun(barData2, barData1)
		return "%s-%s"%(stock2, stock1), series
def formatSeriesFun(barData1, barData2):
	barDataList1 = sorted(barData1.iteritems(), key=lambda d:d[0])
	barDataList2 = sorted(barData2.iteritems(), key=lambda d:d[0])
	allDateKey = list(set(zip(*barDataList1)[0]+zip(*barDataList2)[0]))
	allDateKey.sort()
	resulteSeries = []
	for dateKey in allDateKey:
		if barData1.has_key(dateKey) and barData2.has_key(dateKey):
			resulteSeries.append((barData1[dateKey], barData2[dateKey]))
	return resulteSeries
def fittingSeriesFun(X, Y):
	x, y = X, Y

	x = np.log(x)
	y = np.log(y)

	p0 = [1.6,0] # 第一次猜测的函数拟合参数
	plsq = leastsq(residuals, p0, args=(y, x))

	beta = plsq[0][0]

	St = []
	for i in xrange(len(x)):
		s = x[i] - beta*y[i]
		St.append(s)
	mean = np.mean(St)
	std = np.std(St)

	test = []
	for data in St:
		s = (data - mean)/std
		test.append(s)
	test = np.abs(test)
	test.sort()

	x, y = X, Y
	x = ADF_Series.C_ADF_Series(False,x)
	y = ADF_Series.C_ADF_Series(False,y)
	St = ADF_Series.C_ADF_Series(False,St)

	isCointegration = False
	if St.diffRank < x.diffRank or St.diffRank < y.diffRank:
		isCointegration = True

	return beta, isCointegration, mean, std, test[len(test)*0.90], test[len(test)*0.04], 2*test[-1]-test[len(test)*0.99]
def func(x, p):
	beta, A = p
	a = []
	for i in x:
		a.append(beta*i + A)
	return a
def residuals(p, y, x):
	fx = func(x, p)
	newY = []
	for i in xrange(len(x)):
		newY.append(y[i]-fx[i])
	return newY

def main():
	#读取股票价格
	loadStockPrice()
	#读取板块
	loadPlateFun()
	#读取融资融券标的
	loadRZRQStockFun()
	barData = loadBarDataFun()

	global Results
	lock = multiprocessing.Lock()
	pool = multiprocessing.Pool(processes= 6)
	for stock1, barData1 in barData.items():
		for stock2, barData2 in barData.items():
			if isInTheSamePlateFun(stock1, stock2):	#如果在同一个板块
				key, series = getPairKeyFun(stock1, stock2, barData1, barData2)
				if stock1 != stock2 and not Results.has_key(key):
					if stock1 in StockPrice and stock2 in StockPrice:
						Results[key] = series
						X, Y = zip(*series)
						pool.apply_async(func= stockPairSelectFun, args= (key, X, Y))

	pool.close()
	pool.join()

if __name__ == '__main__':
	main()