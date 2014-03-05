#!/usr/bin/python
# -*- coding: utf-8 -*-
from scipy.optimize import leastsq
import numpy as np
import matplotlib.pyplot as plt

class C_ADF_Series(list):
	def __init__(self, series):
		list.__init__([])
		self.extend(series)
		self.model_1_param = {"delta":0, "delta_t": 0}
		self.model_2_param = {"alpha":0, "delta": 0, "delta_t": 0}
		self.model_3_param = {"alpha":0, "beta":0, "delta": 0, "delta_t": 0}
	#模型1方法
	def model_1_fun(self, X, p):
		#fun: delta_X(t) = delta*X(t-1) + sigma(beta(i)*delta_X(t-1), i=1~m) + epsilon(t)
		delta = p[0]
		betas = p[1:]
		delta_X = []
		for x in X:
			deltaX = x*delta
			num = 0
			for betaX in delta_X[::-1]:
				if num < len(p[1:]):
					deltaX = deltaX + betaX*betas[num]
					num = num + 1
			delta_X.append(deltaX)
		return delta_X
	#模型2方法
	def model_2_fun(self, X, p):
		#fun: delta_X(t) = alpha + delta*X(t-1) + sigma(beta(i)*delta_X(t-1), i=1~m) + epsilon(t)
		alpha = p[0]
		delta = p[1]
		betas = p[2:]
		delta_X = []
		for x in X:
			deltaX = alpha + x*delta
			num = 0
			for betaX in delta_X[::-1]:
				if num < len(p[2:]):
					deltaX = deltaX + betaX*betas[num]
					num = num + 1
			delta_X.append(deltaX)
		return delta_X
	#模型3方法
	def model_3_fun(self, X, p):
		#fun: delta_X(t) = alpha + beta*t + delta*X(t-1) + sigma(beta(i)*delta_X(t-1), i=1~m) + epsilon(t)
		alpha = p[0]
		beta  = p[1]
		delta = p[2]
		betas = p[3:]
		delta_X = []
		t = 1
		for x in X:
			deltaX = alpha + beta*t + x*delta
			num = 0
			for betaX in delta_X[::-1]:
				if num < len(p[3:]):
					deltaX = deltaX + betaX*betas[num]
					num = num + 1
			delta_X.append(deltaX)
			t = t + 1
		return delta_X
	#拟合方法
	#模型1拟合
	def fitting_model_1_fun(self, x):
		y = np.diff(x)
		p0 = [1] + int(2)*[0]
		plsq = leastsq(self.getResidualsFun, p0, args=(y, x[:-1], self.model_1_fun))
		fit_y = self.model_1_fun(x[:-1], plsq[0])
		t = self.getT(
			x[:-1], y, fit_y,
			plsq[0][0], 0)
		self.model_1_param["delta"] = plsq[0][0]
		self.model_1_param["delta_t"] = t
		return fit_y
	#模型2拟合
	def fitting_model_2_fun(self, x):
		y = np.diff(x)
		p0 = [1, 2] + int(2)*[0]
		plsq = leastsq(self.getResidualsFun, p0, args=(y, x[:-1], self.model_2_fun))
		fit_y = self.model_2_fun(x[:-1], plsq[0])
		t = self.getT(
			x[:-1], y, fit_y,
			plsq[0][1], 0)
		self.model_2_param["alpha"], self.model_2_param["delta"] = plsq[0][:2]
		self.model_2_param["delta_t"] = t
		return fit_y
	#模型3拟合
	def fitting_model_3_fun(self, x):
		y = np.diff(x)
		p0 = [1, 2, 3] + int(2)*[0]
		plsq = leastsq(self.getResidualsFun, p0, args=(y, x[:-1], self.model_3_fun))
		fit_y = self.model_3_fun(x[:-1], plsq[0])
		t = self.getT(
			x[:-1], y, fit_y,
			plsq[0][2], 0)
		self.model_3_param["alpha"], self.model_3_param["beta"], self.model_3_param["delta"] = plsq[0][:3]
		self.model_3_param["delta_t"] = t
		return fit_y
	#计算参数的t分布
	def getT(self, x, y, fit_y, beta, beta0):
		SSR = 0
		x_SSR = 0
		x_mean = np.mean(x)
		for i in xrange(len(x)):
			SSR = SSR + (y[i] - fit_y[i])*(y[i] - fit_y[i])
			x_SSR = x_SSR + (x[i] - x_mean)*(x[i] - x_mean)
		return (beta - beta0)*np.sqrt(len(x) - 2)/np.sqrt(SSR/x_SSR)
	def getResidualsFun(self, p, y, x, func):
		fx = func(x, p)
		residuals = []
		for i in xrange(len(y)):
			residuals.append(y[i]-fx[i])
		return residuals


def main():
	a = C_ADF_Series([
		7802.5,
		8694.2,
		9073.7,
		9651.8,
		10557.3,
		11510.8,
		13272.8,
		14966.8,
		16273.7,
		17716.3,
		18696.7,
		17847.4,
		19347.8,
		21830.9,
		25053.0,
		29269.1,
		32056.2,
		34467.5,
		37331.9,
		39988.5,
		42713.1,
		45625.8,
		49238.0,
		53962.5,
		60078.0,
		67282.2,
		76096.3,
		88002.1,
		101616.3
		])

	x = np.arange(len(a))[1:]
	y = np.diff(a)

	y1 = a.fitting_model_1_fun(a) 
	y2 = a.fitting_model_2_fun(a)
	y3 = a.fitting_model_3_fun(a)

	print a.model_1_param
	print a.model_2_param
	print a.model_3_param


	print "--------------"
	b = C_ADF_Series(np.diff(a))
	x = np.arange(len(b))[1:]
	y = np.diff(b)

	y1 = b.fitting_model_1_fun(b) 
	y2 = b.fitting_model_2_fun(b)
	y3 = b.fitting_model_3_fun(b)

	print b.model_1_param
	print b.model_2_param
	print b.model_3_param


	print "--------------"
	c = C_ADF_Series(np.diff(b))
	x = np.arange(len(c))[1:]
	y = np.diff(c)

	y1 = c.fitting_model_1_fun(c) 
	y2 = c.fitting_model_2_fun(c)
	y3 = c.fitting_model_3_fun(c)

	print c.model_1_param
	print c.model_2_param
	print c.model_3_param



	#y2 = a.model_3_fun(a[:-1], [-223.7,-101.2,0.093,0.733])
	#y1 = a.model_3_fun(a[:-1], [-161.674, -121.095, 0.11232, 0.807062, -0.23258])

	#diff = []
	#for i in xrange(len(y)):
	#	diff.append(y3[i] - y[i])

	#y_mean = np.mean(y)
	#R1, R2 = 0, 0
	#for i in xrange(len(y)):
	#	R1 = R1 + (y[i] - y1[i])*(y[i] - y1[i])
	#	R2 = R2 + (y[i] - y_mean)*(y[i] - y_mean)
	#R = 1- R1/R2
	#print R


	l = plt.plot(x, y, "o")
	l1, l2, l3 = plt.plot(x, y3, "r", x, y2, "g", x, y1, "y",)

	plt.show()

if __name__ == '__main__':
	main()		