__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import defaultdict
import time
import collections
import logging

"""
Usage:
python question4.py corpus.en corpus.de devwords.txt > q4_output

Question 4:  Initialize t(f|e) values with uniform distribution, run
5 iterations of the EM algorithm for IBM model 1

"""

#Initialize t(f|e) values with uniform distribution
def init_t(source_corpus, foreign_corpus):
    source = file(source_corpus, "r")
    foreign = file(foreign_corpus, "r")
    unique_f = len(set(w.lower() for w in open(foreign_corpus).read().split()))
    t = collections.defaultdict(dict)
    f_line = foreign.readline().strip()
    e_line = source.readline().strip()
    while e_line:
        e_set = set(e_line.split(" "))
        e_set.add("NULL")
        for e in e_set:
            for f in set(f_line.split(" ")):
                # t(f|e) is given by 1 over unique foreign words + 1 (NULL)
                t[e][f] = 1/float(unique_f + 1)
        e_line = source.readline().strip()
        f_line = foreign.readline().strip()
    source.close()
    foreign.close()
    return t

# IBM model 1
def model1(source_corpus, foreign_corpus, t):
    source = file(source_corpus, "r")
    foreign = file(foreign_corpus, "r")
    count = defaultdict(int)
    count_e = defaultdict(int)
    f_line = foreign.readline().strip()
    e_line = source.readline().strip()
    while e_line:
        # Go over words in f, e
        for f in list(f_line.split(" ")):
            # include NULL for possible source alignments
            e_list = list(e_line.split(" "))
            e_list.append('NULL')
            # Calculate sum first
            sum_e = 0
            for e in e_list:
                sum_e += t[e][f]
            for e in e_list:
                # Update rule
                count[(f,e)] += (t[e][f] / float(sum_e))
                count_e[e] += (t[e][f] / float(sum_e))
        f_line = foreign.readline().strip()
        e_line = source.readline().strip()
    source.seek(0)
    foreign.seek(0)
    f_line = foreign.readline().strip()
    e_line = source.readline().strip()
    # Update t values
    while e_line:
        f_set = set(f_line.split(" "))
        e_set = set(e_line.split(" "))
        e_set.add("NULL")
        for f in f_set:
            for e in e_set:
                t[e][f] = float(count[(f,e)]) / float(count_e[e])
        f_line = foreign.readline().strip()
        e_line = source.readline().strip()
    source.close()
    foreign.close()
    return t

def main():
    start_time = time.time()
    #Read in corpus, initialize t(f|e) for each unique English word-foreign word combo
    t = init_t(sys.argv[1],sys.argv[2])
    #Run  5 iterations of the EM algorithm for IBM model 1
    for i in range(0,5):
        t = model1(sys.argv[1],sys.argv[2],t)

    #For each English word e in devwords.txt, print the 10 foreign words with the highest t(f|e) and the value.
    devwords = file(sys.argv[3],"r")
    word = devwords.readline().strip()
    while word:
        print("English word: "),
        print(word)
        print("Top 10 foreign words:"),
        print(sorted(t[word].items(), key=lambda x:x[1], reverse=True)[0:10])
        print("")
        word = devwords.readline().strip()

    #Find alignments for the first 20 sentence pairs in the training data
    source = file(sys.argv[1], "r")
    foreign = file(sys.argv[2], "r")

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
        print(line_e)
        print(line_f)
        print(alignments)
        print("")

    source.close()
    foreign.close()
    logging.warning("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':     # if the function is the main function ...
    main()