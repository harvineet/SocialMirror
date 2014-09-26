from multiprocessing import Pool
import param_spread_alpha_beta
import sys

def xfrange(start, stop, step):
    while start < stop:
        yield start
        start += step
		
if __name__ == '__main__':
	a1 = 0
	a2 = 1
	step_a = 0.1
	b1 = 1
	b2 = 10
	step_b = 1
	sim_run = sys.argv[1]
	pool = multiprocessing.Pool(processes=4) 
	for alpha in xfrange(a1,a2,step_a):
		for beta in xfrange(b1,b2,step_b):
			pool.apply_async(param_spread_alpha_beta.main, args=(alpha,beta,sim_run))
	pool.close()
    pool.join()
		