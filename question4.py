from __future__ import print_function
__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import defaultdict
import time
import collections
import logging
from itertools import izip

"""
Usage:
python question4.py n

The parameter n indicates how many iterations of IBM model 1 should be run.
The t-values obtained for the words in devwords.txt will be saved to the file tvalues.txt
The alignments for the first 20 sentences will be saved to the file q4_output

Question 4:  Initialize t(f|e) values with uniform distribution, run
5 iterations of the EM algorithm for IBM model 1

"""

#Initialize t(f|e) values with uniform distribution
def init_t(source_corpus, foreign_corpus):
    source = file(source_corpus, "r")
    foreign = file(foreign_corpus, "r")
    unique_f = len(set(w.lower() for w in open(foreign_corpus).read().split()))
    t = collections.defaultdict(dict)
    for e_line, f_line in izip(open(source_corpus), open(foreign_corpus)):
        e_set = set(e_line.strip().split(" "))
        e_set.add("NULL")
        for e in e_set:
            for f in set(f_line.strip().split(" ")):
                # t(f|e) is given by 1 over unique foreign words + 1 (NULL)
                t[e][f] = 1/float(unique_f + 1)
    return t

# IBM model 1
def model1(source_corpus, foreign_corpus, t, n):
    for s in range(0, n):
        count = defaultdict(int)
        count_e = defaultdict(int)
        for e_line, f_line in izip(open(source_corpus), open(foreign_corpus)):
            # Go over words in f, e
            for f in list(f_line.strip().split(" ")):
                # include NULL for possible source alignments
                e_list = list(e_line.strip().split(" "))
                e_list.append('NULL')
                # Calculate sum first
                sum_e = 0
                for e in e_list:
                    sum_e += t[e][f]
                for e in e_list:
                    # Update rule
                    count[(f,e)] += (t[e][f] / float(sum_e))
                    count_e[e] += (t[e][f] / float(sum_e))
        # Update t values
        for (f,e) in count.keys():
            t[e][f] = float(count[(f,e)]) / float(count_e[e])
    return t

#For each English word e in devwords.txt, print the 10 foreign words with the highest t(f|e) and the value.
def model1_tvalues(t):
    devwords = open("devwords.txt","r")
    tvalues = open("tvalues.txt", "w")
    word = devwords.readline().strip()
    while word:
        print(word, file=tvalues)
        print(sorted(t[word].items(), key=lambda x:x[1], reverse=True)[0:10], file=tvalues)
        print("", file=tvalues)
        word = devwords.readline().strip()

#Find alignments for the first 20 sentence pairs in the training data, save to output file
def model1_alignments(t):
    source = open("corpus.en", "r")
    foreign = open("corpus.de", "r")
    q4 = open("q4_output", "w")
    for j in range(0,20):
        line_e = source.readline().strip()
        line_f = foreign.readline().strip()
        alignments = []
        for f in range(0, len(line_f.split(" "))):
            alignment = 0;
            probability = 0;
            for e in range(0, len(line_e.split(" "))):
                p = t[line_e.split(" ")[e]][line_f.split(" ")[f]]
                if probability < p:
                    probability = p
                    alignment = e+1
            # Check NULL alignment
            if probability < t["NULL"][line_f.split(" ")[f]]:
                probability = t["NULL"][line_f.split(" ")[f]]
                alignment = 0
            alignments.append(alignment)
        print(line_e, file=q4)
        print(line_f, file=q4)
        print(alignments, file=q4)
        print("", file=q4)
    source.close()
    foreign.close()
    q4.close()

def main():
    start_time = time.time()
    n = int(sys.argv[1])
    #Read in corpus, initialize t(f|e) for each unique English word-foreign word combo
    t = init_t("corpus.en","corpus.de")
    #Run  5 iterations of the EM algorithm for IBM model 1
    model1("corpus.en","corpus.de",t,n)
    #Print t values for words in devwords.txt
    model1_tvalues(t)
    #Find alignments for the first 20 sentence pairs in the training data, save to output
    model1_alignments(t)
    logging.warning("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':     # if the function is the main function ...
    main()