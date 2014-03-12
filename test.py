#!/usr/bin/python
# -*- coding: utf-8 -*-
#test.py
import multiprocessing

def do_calculation(data):
    return data*2
def start_process():
    print 'Starting',multiprocessing.current_process().name

if __name__=='__main__':
    print "\xe5\xb9\xb3\xe4\xbb\x93"
    inputs=list(range(10))
    print 'Inputs  :',inputs

    builtin_output=map(do_calculation,inputs)
    print 'Build-In :', builtin_output

    pool_size=multiprocessing.cpu_count()*2
    pool=multiprocessing.Pool(processes=pool_size,
        initializer=start_process,)

    pool_outputs=pool.map(do_calculation,inputs)
    pool.close()
    pool.join()

    print 'Pool  :',pool_outputs