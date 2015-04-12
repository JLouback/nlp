from __future__ import print_function
__author__="Juliana Louback <jl4354@.columbia.edu>"

from question4 import init_t
from question4 import model1
from question4 import model1_tvalues
from question4 import model1_alignments
from question5 import model2
from question5 import model2_alignments
from question6 import unscramble
import time
import logging
import sys
"""
Usage:
python questions.py n

Runs functions for questions 4, 5, 6. See individual files for specifics.
The parameter n indicates how many iterations of IBM model 1 and 2 should be run.

Output:
tvalues.txt = t values for devwords.txt, question 4.
q4_output = alignments for IBM model 1, question 4
q5_output = alignments for IBM model 2, question 5
unscrambled.en = result of finding best sentence translation, question 6

"""

start_time = time.time()
n = int(sys.argv[1])
# Question 4
#Read in corpus, initialize t(f|e) for each unique English word-foreign word combo
t = init_t("corpus.en", "corpus.de")
#Run n iterations of the EM algorithm for IBM model 1
model1("corpus.en", "corpus.de",t,n)
#For each English word e in devwords.txt, print the 10 foreign words with the highest t(f|e) and the value.
model1_tvalues(t)
#Find alignments for the first 20 sentence pairs in the training data according to model 1 t values
model1_alignments(t)

#Question 5
# Run n iterations of the EM algorithm for IBM model 2
t,q = model2("corpus.en", "corpus.de",t,n)
#Find alignments for the first 20 sentence pairs in the training data according to model 2 t values
model2_alignments(t, q)

# Question 6
unscramble("scrambled.en", "original.de", t, q)

logging.warning("--- %s seconds ---" % (time.time() - start_time))