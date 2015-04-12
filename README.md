# nlp
Code for assignments from prof. Michael Collin's NLP course, COMSW4705 Spring 2015 at Columbia U.

The code for individual questions is in the files question4.py, question5.py, question6.py

Since they build on each other (q5 uses t values obtained in q4; q6 uses t and q values from q5), I run them all sequentially in questions.py. I did this to facilitate correction - if TAs divide corrections by questions or students

============================================================
Q4, Q5, Q6 (Runtime for n=3 is ~6 minutes)
Usage:
python questions.py n

Runs functions for questions 4, 5, 6. See individual files for specifics.
The parameter n indicates how many iterations of IBM model 1 and 2 should be run.

Output:
tvalues.txt = t values for devwords.txt, question 4.
q4_output = alignments for IBM model 1, question 4
q5_output = alignments for IBM model 2, question 5
unscrambled.en = result of finding best sentence translation, question 6


============================================================
Q4 (Runtime for n=5 is ~3 minutes)
Usage:
python question4.py n

The parameter n indicates how many iterations of IBM model 1 should be run.
The t-values obtained for the words in devwords.txt will be saved to the file tvalues.txt
The alignments for the first 20 sentences will be saved to the file q4_output

Question 4:  Initialize t(f|e) values with uniform distribution, run
5 iterations of the EM algorithm for IBM model 1


============================================================
Q5 (Runtime for n=5 is ~7 minutes)
Usage:
python question5.py n

The parameter n indicates how many iterations of IBM model 1 and 2 should be run.
The alignments for the first 20 sentences will be saved to the file q5_output

Question 5:  Initialize t(f|e) values with 5 iterations of IBM model 1
(see question4.py) and q(j|i, l, m) with 1/l+1. Run 5 rounds of IBM model 2

============================================================
Q6 (Runtime for n=5 is ~8 minutes)
Note: The only difference between question6.py and questions.py is that question6.py does not calculate/save t values and alignments as is done for Q4, Q5.
Usage:
python question6.py n

The parameter n indicates how many iterations of model 1 and 2 should be run. 

Question 6: For each German sentence find the English sentence that produces the highest-scoring alignment.
