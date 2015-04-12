from __future__ import print_function
__author__="Juliana Louback <jl4354@.columbia.edu>"

from question4 import init_t
from question4 import model1
from question5 import model2
import time
import logging
import math
import sys

"""
Usage:
python question6.py n

The parameter n indicates how many iterations of model 1 and 2 should be run. I found that simply running
each once results in 89% accuracy according to eval_scramble.py

Question 6: For each German sentence find the English sentence that produces the highest-scoring alignment.


"""

# This function assumes t and q are given.
def unscramble(source_corpus, foreign_corpus, t, q):
    source = open(source_corpus, "r")
    foreign = open(foreign_corpus, "r")
    unscrambled = open("unscrambled.en", "w")
    for f_line in foreign.readlines():
        probability = -1000000000
        source.seek(0)
        for e_line in source.readlines():
            temp_prob = 0
            m = len(f_line.strip().split(" "))
            l = len(e_line.strip().split(" "))
            e_line_null = "NULL " + e_line
            # Go over words in e, f
            for i in range(1, m+1):
                f = f_line.strip().split(" ")[i-1]
                word_prob = 0
                for j in range(0, l+1):
                    e = e_line_null.strip().split(" ")[j]
                    qt = q.get((j,i,l,m),0.00000001) * t[e].get(f,0.00000001)
                    word_prob = max(word_prob, qt)
                temp_prob += math.log(word_prob)
            if probability < temp_prob:
                probability = temp_prob
                line = e_line
        print(line.strip(), file=unscrambled)
    source.close()
    foreign.close()
    unscrambled.close()

def main():
    start_time = time.time()
    n = int(sys.argv[1])
    #Read in corpus, initialize t(f|e) with uniform distribution
    t = init_t("corpus.en", "corpus.de")
    #Run  1 iterations of the EM algorithm for IBM model 1
    model1("corpus.en", "corpus.de",t,n)
    #Run  5 iterations of the EM algorithm for IBM model 2
    t,q = model2("corpus.en", "corpus.de",t,n)
    #Find english sentence with highest probability for german sentences
    unscramble("scrambled.en", "original.de", t, q)
    logging.warning("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()