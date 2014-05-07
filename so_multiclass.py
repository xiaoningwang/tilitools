from cvxopt import matrix,spmatrix,sparse
import numpy as np
import math as math



class SOMultiClass:
	""" Multi class structured object."""

	X = [] # (matrix) data 
	y = [] # (vector) labels (if present)
	samples = -1 # (scalar) number of training data samples
	dims = -1 # (scalar) number of input dimensions
	num_classes = -1 # (scalar) number of classes 


	def __init__(self, X, classes, y=[]):
		self.X = X
		self.y = y
		(self.dims, self.samples) = X.size
		self.num_classes = classes		

	def argmin(self, sol, idx):
		return self.argmax(sol,idx, opt_type='quadratic')

	def argmax(self, sol, idx, add_loss=False, opt_type='linear'):
		nd = self.dims
		d = 0  # start of dimension in sol
		val = -10**10
		cls = -1 # best class

		for c in range(self.num_classes):
			foo = sol[d:d+nd].trans()*self.X[:,idx]
			# the argmax of the above function
			# is equal to the argmax of the quadratic function
			# foo = + 2*foo - normPsi
			# since ||\Psi(x_i,z)|| = ||\phi(x_i)|| = y \forall z   
			d += nd
			if (np.single(foo)>np.single(val)):
				val = foo
				cls = c

		if (opt_type=='quadratic'):
			normPsi = self.X[:,idx].trans()*self.X[:,idx]
			val = 2*val - normPsi

		jfm = self.get_joint_feature_map(idx,cls)
		return (val,cls,jfm)
		

	def calc_loss(self, idx, y):
		return self.y[idx]!=y

	def get_joint_feature_map(self, idx, y=-1):
		if y==-1:
			y=self.y[idx]

		nd = self.dims
		mc = self.num_classes
		phi = matrix(0.0,(nd*mc,1))
		phi[nd*y:nd*(y+1)] = self.X[:,idx]
		return phi

	def get_num_samples(self):
		return self.samples


	def get_num_dims(self):
		return self.dims*self.num_classes