#!/usr/bin/python
# -*- coding: utf-8 -*-
from scipy.optimize import leastsq
import numpy as np

class C_ARMA_Series(list):
	def __init__(self, series):
		list.__init__([])
		self.extend(series)
		self.model_1_param = {"delta":0}
		self.model_2_param = {"alpha":0, "delta": 0}
		self.model_3_param = {"alpha":0, "beta":0, "delta": 0}
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
		t = 0
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

	#模型1拟合
	def fitting_model_1_fun(self, x):
		y = np.diff(x)
		p0 = [1] + int(len(y)*0.9)*[0]
		plsq = leastsq(self.getResidualsFun, p0, args=(y, x[:-1], self.model_1_fun))
		self.model_1_param["delta"] = plsq[0][0]
		print self.model_1_fun(x[:-1], plsq[0])
	#模型2拟合
	def fitting_model_2_fun(self, x):
		y = np.diff(x)
		p0 = [1, 2] + int(len(y)*0.9)*[0]
		plsq = leastsq(self.getResidualsFun, p0, args=(y, x[:-1], self.model_2_fun))
		self.model_2_param["alpha"], self.model_2_param["delta"] = plsq[0][:2]
		print self.model_2_fun(x[:-1], plsq[0])
	#模型3拟合
	def fitting_model_3_fun(self, x):
		y = np.diff(x)
		p0 = [1, 2, 3] + int(len(y)*0.9)*[0]
		plsq = leastsq(self.getResidualsFun, p0, args=(y, x[:-1], self.model_3_fun))
		self.model_3_param["alpha"], self.model_3_param["beta"], self.model_3_param["delta"] = plsq[0][:3]
		print self.model_3_fun(x[:-1], plsq[0])

	def getResidualsFun(self, p, y, x, func):
		fx = func(x, p)
		residuals = []
		for i in xrange(len(y)):
			residuals.append(y[i]-fx[i])
		return residuals


def main():
	a = C_ARMA_Series([1,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,1,2])

	a.fitting_model_1_fun(a)
	a.fitting_model_2_fun(a)
	a.fitting_model_3_fun(a)

	print a.model_1_param
	print a.model_2_param
	print a.model_3_param

if __name__ == '__main__':
	main()		