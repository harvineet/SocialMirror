from multiprocessing import Pool
import param_spread_alpha_beta
import sys
import os

def xfrange(start, stop, step):
	while start < stop:
		yield start
		start += step
		
def sysCall(alpha,beta,sim_run):
	os.system('python synthetic_diffusion.py '+str(alpha)+' '+str(beta)+' '+str(sim_run))
	
if __name__ == '__main__':
	a1 = 0.1
	a2 = 2
	step_a = 0.1
	b1 = 1
	b2 = 16
	step_b = 1
	sim_run = sys.argv[1]
	pool = Pool(processes=5) 
	for alpha in xfrange(a1,a2,step_a):
		for beta in xfrange(b1,b2,step_b):
			pool.apply_async(sysCall, args=(alpha,beta,sim_run))
	pool.close()
	pool.join()
						