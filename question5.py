__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import defaultdict
from question4 import init_t
from question4 import model1
import time
import logging
from itertools import izip

"""
Usage:
python question5.py corpus.en corpus.de > q5_output

Question 5:  Initialize t(f|e) values with 5 iterations of IBM model 1
(see question4.py) and q(j|i, l, m) with 1/l+1. Run 5 rounds of IBM model 2

"""

# t(f|e) values with 5 iterations of IBM model 1. The q(j|i,l,m) initialization is done in model2
def init_params(source_corpus, foreign_corpus):
    # Start with uniform distribution
    t = init_t(source_corpus, foreign_corpus)
    # Run  5 iterations of the EM algorithm for IBM model 1
    for i in range(0,5):
        t = model1(source_corpus, foreign_corpus, t)
    return t

# IBM model 2
def model2(source_corpus, foreign_corpus, t):
    c_fe = defaultdict(int);c_e = defaultdict(int);c_ilm = defaultdict(int)
    c = defaultdict(int);q = defaultdict(int)
    for e_line, f_line in izip(open(source_corpus), open(foreign_corpus)):
        m = len(f_line.strip().split(" "))
        l = len(e_line.strip().split(" "))
        e_line = "NULL " + e_line
        # Go over words in e, f
        for i in range(1, m+1):
            f = f_line.strip().split(" ")[i-1]
            # Calculate the delta denominator, set default values for  q(j|i,l,m)
            delta_d = 0
            for j in range(0, l+1):
                e = e_line.strip().split(" ")[j]
                if (j,i,l,m) not in q:
                    q[(j,i,l,m)] = 1/float(l+1)
                delta_d += q[(j,i,l,m)] * t[e][f]
            for j in range(0, l+1):
                e = e_line.strip().split(" ")[j]
                # Update rule
                delta = (q[(j,i,l,m)] * t[e][f])/float(delta_d)
                c_fe[(f,e)] += delta
                c_e[e]+= delta
                c_ilm[(i,l,m)] += delta
                c[(j,i,l,m)] += delta
    for e_line, f_line in izip(open(source_corpus), open(foreign_corpus)):
        m = len(f_line.strip().split(" "))
        l = len(e_line.strip().split(" "))
        e_line = "NULL " + e_line
        # Go over words in e, f
        for i in range(1, m+1):
            f = f_line.strip().split(" ")[i-1]
            for j in range(0, l+1):
                e = e_line.strip().split(" ")[j]
                t[e][f] = float(c_fe[(f,e)]) / float(c_e[e])
                q[(j,i,l,m)] = float(c[(j,i,l,m)]) / float(c_ilm[(i,l,m)])
    return t,q

def main():
    start_time = time.time()
    #Read in corpus, initialize t(f|e) with 5 iterations of the EM algorithm for IBM model 1
    t = init_params(sys.argv[1],sys.argv[2])
    #Run  5 iterations of the EM algorithm for IBM model 1
    for i in range(0,1):
        t,q = model2(sys.argv[1],sys.argv[2],t)
    #Find alignments for the first 20 sentence pairs in the training data
    source = file(sys.argv[1], "r")
    foreign = file(sys.argv[2], "r")
    for k in range(0,20):
        e_line = source.readline().strip()
        line = e_line
        f_line = foreign.readline().strip()
        alignments = []
        m = len(f_line.split(" "))
        l = len(e_line.split(" "))
        e_line = "NULL " + e_line
        # Go over words in e, f
        for i in range(1, m+1):
            f = f_line.split(" ")[i-1]
            alignment = 0;
            probability = 0;
            for j in range(0, l+1):
                e = e_line.split(" ")[j]
                p = q[(j,i,l,m)] * t[e][f]
                if probability < p:
                    probability = p
                    alignment = j
            alignments.append(alignment)
        print(line)
        print(f_line)
        print(alignments)
        print("")

    source.close()
    foreign.close()
    logging.warning("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()