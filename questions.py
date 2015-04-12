from __future__ import print_function
__author__="Juliana Louback <jl4354@.columbia.edu>"

from question4 import init_t
from question4 import model1
from question5 import model2
import time
import logging
import math
"""
Usage:
python questions.py

Runs functions for questions 4, 5, 6. See individual files for specifics.
Output:
tvalues.txt = t values for devwords.txt, question 4.
q4_output = alignments for IBM model 1, queston 4
q5_output = alignments for IBM model 2, queston 5

"""

start_time = time.time()
# Question 4

#Read in corpus, initialize t(f|e) for each unique English word-foreign word combo
t = init_t("corpus.en", "corpus.de")
#Run  5 iterations of the EM algorithm for IBM model 1
model1("corpus.en", "corpus.de",t,5)

#For each English word e in devwords.txt, print the 10 foreign words with the highest t(f|e) and the value.
devwords = open("devwords.txt","r")
tvalues = open("tvalues.txt", "w")
word = devwords.readline().strip()
while word:
    print(word, file=tvalues)
    print(sorted(t[word].items(), key=lambda x:x[1], reverse=True)[0:10], file=tvalues)
    print("",file=tvalues)
    word = devwords.readline().strip()
tvalues.close()

#Find alignments for the first 20 sentence pairs in the training data according to model 1 t values
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
q4.close()

#Question 5

#Run  4 iterations of the EM algorithm for IBM model 1
# I found that 4 iterations results in 100% alignment accuracy with the sample
t,q = model2("corpus.en", "corpus.de",t,5)

#Find alignments for the first 20 sentence pairs in the training data according to model 1 t values
source.seek(0)
foreign.seek(0)
q5 = open("q5_output", "w")
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
    print(line, file=q5)
    print(f_line, file=q5)
    print(alignments, file=q5)
    print("", file=q5)
q5.close()

# Question 6

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
                    qt = q.get((j,i,l,m),0.0000001) * t[e].get(f,0.0000001)
                    word_prob = max(word_prob, qt)
                temp_prob += math.log(word_prob)
            if probability < temp_prob:
                probability = temp_prob
                line = e_line
        print(line.strip(), file=unscrambled)
    source.close()
    foreign.close()
    unscrambled.close()

unscramble("scrambled.en", "original.de", t, q)

logging.warning("--- %s seconds ---" % (time.time() - start_time))