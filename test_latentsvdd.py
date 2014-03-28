import cvxopt as co
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

from latentsvdd import LatentSVDD
from so_multiclass import SOMultiClass

if __name__ == '__main__':

	# generate raw training data
	Dtrain1 = co.normal(2,100)*0.3 + 2
	Dtrain2 = co.normal(2,100)*0.2 + 0
	Dtrain3 = co.normal(2,100)*0.3 - 1
	Dtrain = co.matrix([[Dtrain1], [Dtrain2], [Dtrain3], [Dtrain3/2-2]])

	# generate structured object
	sobj = SOMultiClass(Dtrain,co.matrix([14]))

	# train svdd
	lsvdd = LatentSVDD(sobj,0.0025)
	(cs, states, msg) = lsvdd.train_ql()
	print(cs)
	print(states)

	# generate test data grid
	delta = 0.1
	x = np.arange(-4.0, 8.0, delta)
	y = np.arange(-4.0, 8.0, delta)
	X, Y = np.meshgrid(x, y)    
	(sx,sy) = X.shape
	Xf = np.reshape(X,(1,sx*sy))
	Yf = np.reshape(Y,(1,sx*sy))
	Dtest = np.append(Xf,Yf,axis=0)
	print(Dtest.shape)

	# generate structured object
	predsobj = SOMultiClass(co.matrix(Dtest),co.matrix([14]))

	(res,lats,msg) = lsvdd.apply(predsobj)
	print(res.size)

	# nice visualization
	Z = np.reshape(res,(sx,sy))
	plt.contourf(X, Y, Z)
	plt.contour(X, Y, Z, [np.array(lsvdd.get_threshold())[0,0]])
	plt.scatter(Dtrain[0,:],Dtrain[1,:],10)
	plt.show()

	print('finished')