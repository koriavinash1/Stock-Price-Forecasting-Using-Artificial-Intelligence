# initial sigma, mean from normal distributuion: 0.09, 10


import numpy as np  

solution = np.array([0.5, 0.1])

def f(w): return -np.sum((w - solution)**2)

npop = 500      # population size  
sigma = 0.1    # noise standard deviation  
alpha = 0.001  # learning rate  
w = np.random.randn(3) # initial guess  
for i in range(300):  
	N = np.random.randn(npop, 3)
	R = np.zeros(npop)
for j in range(npop):
	w_try = w + sigma*N[j]
	R[j] = f(w_try)
A = (R - np.mean(R)) / np.std(R)
w = w + alpha/(npop*sigma) * np.dot(N.T, A)